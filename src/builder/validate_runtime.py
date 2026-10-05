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
    records = read_records('catalog')
    review = read_records('review_queue')
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
        'scope': 'Cast localization metadata + exact same-resource English variants. Untagged inherited rows remain unresolved, not silently excluded.',
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
