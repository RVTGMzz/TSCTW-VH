"""Rank unresolved inherited rows for human review without needing raw package bytes."""
from pathlib import Path
import argparse
import collections
import gzip
import json
import re

from validate_runtime import RUNTIME, row_identity, read_records

VISIBLE_TYPES = {'STR#', 'CTSS', 'TTAs'}
DESC_SIGNAL = re.compile(r'needs? translation|dialog|interaction|catalog|message|tooltip|menu|title', re.I)
TECH_SIGNAL = re.compile(
    r'\bdebug\b|\btest\b|\broute\b|\bspawn\b|\bcontroller\b|\bmarker\b|'
    r'\binvisible\b|\bstate\b|\bprimitive\b|\bfunction\b|\bunused\b|'
    r'\bdo not translate\b|\bdon[\'’]?t translate\b',
    re.I,
)
OBJECT_TECH = re.compile(r'controller|marker|invisible|destination|test|debug', re.I)


def read_context():
    raw = gzip.decompress((RUNTIME/'review_context.json.gz').read_bytes())
    return json.loads(raw)


def score(row):
    names = row.get('object_names') or []
    s = 0
    if any(name.startswith('CS -') for name in names):
        s += 5
    if row.get('shares_group_with_cast_text'):
        s += 4
    if row.get('type') in VISIBLE_TYPES:
        s += 2
    if DESC_SIGNAL.search(row.get('description') or ''):
        s += 2
    if TECH_SIGNAL.search((row.get('en') or '') + '\n' + (row.get('description') or '')):
        s -= 6
    if any(OBJECT_TECH.search(name) for name in names):
        s -= 3
    if (row.get('en') or '').startswith('*'):
        s -= 4
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--groups', type=int, default=24)
    ap.add_argument('--samples', type=int, default=10)
    ap.add_argument('--object-contains', default='')
    ap.add_argument('--value-exact', default='')
    args = ap.parse_args()

    catalog_ids = {row_identity(r) for r in read_records('catalog')}
    overrides = {
        (r['package'], tuple(r['key']), r['row'])
        for r in json.loads((RUNTIME/'row_scope_overrides.json').read_text())
    }
    rows = [
        r for r in read_context()
        if r.get('decision') == 'review'
        and row_identity(r) not in overrides
        and row_identity(r) not in catalog_ids
        and (r.get('en') or '').strip().lower() not in {'n/a', 'na'}
        and (not args.object_contains or any(args.object_contains.lower() in n.lower() for n in (r.get('object_names') or [])))
        and (not args.value_exact or (r.get('en') or '') == args.value_exact)
    ]

    grouped = collections.defaultdict(list)
    for row in rows:
        names = row.get('object_names') or []
        if not (row.get('shares_group_with_cast_text') or any(n.startswith('CS -') for n in names)):
            continue
        grouped[(row['package'], tuple(row['key']), tuple(names))].append(row)

    ranked = []
    for identity, group in grouped.items():
        ranked.append((max(score(r) for r in group), sum(max(score(r), 0) for r in group), identity, group))
    ranked.sort(key=lambda x: (-x[0], -x[1], -len(x[3]), x[2][0], x[2][1]))

    print(json.dumps({
        'effective_review_rows': len(rows),
        'candidate_groups': len(grouped),
        'shown_groups': min(args.groups, len(ranked)),
        'note': 'Ranking only. CS ownership/shared Cast text is evidence for review, not proof of runtime reachability.'
    }, indent=2))

    for rank, (peak, total, identity, group) in enumerate(ranked[:args.groups], 1):
        package, key, names = identity
        print(f"\n=== TRIAGE {rank:02d} peak={peak} total={total} rows={len(group)} ===")
        print('package:', package)
        print('key:', list(key))
        print('objects:', list(names))
        samples = sorted(group, key=lambda r: (-score(r), r['row']))[:args.samples]
        for row in samples:
            print(json.dumps({
                'score': score(row),
                'row': row['row'],
                'language': row['language'],
                'type': row['type'],
                'resource_name': row.get('name'),
                'en': row['en'],
                'description': row['description'],
                'shares_group_with_cast_text': row['shares_group_with_cast_text'],
            }, ensure_ascii=False))


if __name__ == '__main__':
    main()
