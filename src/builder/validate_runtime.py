"""Source-only runtime QA and honest coverage; --require-complete is a release gate."""
from pathlib import Path
import argparse
import collections
import gzip
import json
import re
from build_v07 import PRINTF_RE, metadata_signature, CYRILLIC_RE

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / 'runtime'
DOLLAR_RE = re.compile(r'\$[A-Za-z0-9_]+(?::\d+)*')


def read_records(name):
    return json.loads(gzip.decompress((RUNTIME/(name+'.json.gz')).read_bytes()))



def row_identity(row):
    return row['package'], tuple(row['key']), row['row']


def load_row_overrides():
    """Load exact row guards from the base file plus numbered review shards."""
    rows = []
    for path in sorted(RUNTIME.glob('row_scope_overrides*.json')):
        data = json.loads(path.read_text())
        if not isinstance(data, list):
            raise ValueError(('Row override shard must be a JSON list', path.name))
        rows.extend(data)
    return rows


def effective_records():
    """Merge exact row overrides into committed snapshots for source-only QA.

    A full package extraction still regenerates catalog/review snapshots. Between
    extractions, new exact overrides may legitimately still live in review_queue;
    promote only rows whose package/key/ordinal/language/source/description all
    match the committed baseline. Already-extracted overrides are accepted when
    the same identity is already present in catalog with the target category.
    """
    records = read_records('catalog')
    review = read_records('review_queue')
    override_rows = load_row_overrides()
    overrides = {}
    for override in override_rows:
        identity = (override['package'], tuple(override['key']), override['row'])
        if identity in overrides:
            raise ValueError(('Duplicate row override', identity))
        overrides[identity] = override

    catalog_by_id = {row_identity(row): row for row in records}
    review_by_id = {row_identity(row): row for row in review}
    promoted = []
    promoted_ids = set()
    for identity, override in overrides.items():
        if identity in catalog_by_id:
            row = catalog_by_id[identity]
            if row['category'] != override['category'] or (row['language'], row['en'], row['description']) != (override['language'], override['en'], override['description']):
                raise ValueError(('Extracted override mismatch', identity))
            continue
        row = review_by_id.get(identity)
        if row is None:
            raise ValueError(('Row override missing from catalog and review snapshots', identity))
        if row['category'] != 'review' or (row['language'], row['en'], row['description']) != (override['language'], override['en'], override['description']):
            raise ValueError(('Pending row override baseline mismatch', identity))
        promoted_row = dict(row)
        promoted_row['category'] = override['category']
        promoted_row['reason'] = override['reason']
        promoted.append(promoted_row)
        promoted_ids.add(identity)

    if promoted:
        records.extend(promoted)
        review = [row for row in review if row_identity(row) not in promoted_ids]
    return records, review


def validate(en, vi):
    if not vi.strip() or '\0' in vi or CYRILLIC_RE.search(vi):
        raise ValueError(('Empty, NUL or Cyrillic translation', en))
    # Keep full chained parameters and even the source's $0bject typo intact.
    for regex in (DOLLAR_RE, PRINTF_RE):
        if regex.findall(en) != regex.findall(vi):
            raise ValueError(('Token/order mismatch', en, vi))
    if re.findall(r'\r\n|\r|\n', en) != re.findall(r'\r\n|\r|\n', vi):
        raise ValueError(('Line-break sequence mismatch', en))
    if metadata_signature(en) != metadata_signature(vi):
        raise ValueError(('Tooltip metadata mismatch', en))


def load_maps():
    maps = {}
    for path in sorted((RUNTIME/'translations').glob('*.json')):
        def no_duplicate(pairs):
            result = {}
            for key,value in pairs:
                if key in result:
                    raise ValueError(('Duplicate source key', path, key))
                result[key] = value
            return result
        data = json.loads(path.read_text(), object_pairs_hook=no_duplicate)
        for en,vi in data.items():
            validate(en,vi)
        maps[path.stem] = data
    return maps


def assess():
    maps = load_maps()
    records, review = effective_records()
    decisions = {}
    for row in json.loads((RUNTIME/'scope_decisions.json').read_text()):
        key = row['category'], row['en']
        if key in decisions:
            raise ValueError(('Duplicate scope decision', key))
        decisions[key] = row
    groups = collections.defaultdict(dict)
    remaining = []
    for row in records:
        category, en = row['category'], row['en']
        decision = decisions.get((category,en))
        if decision:
            status = decision['status']
        elif en in maps.get(category,{}):
            status = 'translated'
        else:
            status = 'missing'
        groups[category][en] = status
        if status in ('missing','review'):
            remaining.append(dict(row,status=status))
    inventory = json.loads((RUNTIME/'inventory.json').read_text())
    parse_errors = sum(len(x['errors']) for x in inventory)
    report = {
        'status': 'incomplete' if remaining or review or parse_errors else 'source-complete',
        'in_game_tested': False,
        'scope': 'Cast localization metadata + exact same-resource English variants + reviewed exact row overrides. Remaining inherited rows are unresolved, not silently excluded.',
        'categories': {c:dict(collections.Counter(rows.values())) for c,rows in sorted(groups.items())},
        'translation_map_entries': sum(map(len,maps.values())),
        'candidate_rows': len(records),
        'untranslated_or_review_candidate_rows': len(remaining),
        'untagged_review_rows': len(review),
        'parse_errors': parse_errors,
        'selector_runtime_source_verified': False,
        'release_gate': 'Do not publish v0.8 TEST as a completed sweep until candidate translations, untagged classification, selector source and package QA are complete.',
    }
    return report, remaining


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write',action='store_true')
    ap.add_argument('--require-complete',action='store_true')
    args = ap.parse_args()
    report, remaining = assess()
    if args.write:
        (RUNTIME/'coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        encoded = (json.dumps(remaining,ensure_ascii=True,separators=(',',':'))+'\n').encode()
        (RUNTIME/'remaining.json.gz').write_bytes(gzip.compress(encoded,mtime=0))
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if report['parse_errors'] or (args.require_complete and report['status']!='source-complete'):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
