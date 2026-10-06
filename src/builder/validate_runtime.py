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


def auto_review_decision(row):
    """Return an evidence-backed automatic inherited-row decision, or None.

    A leading asterisk is the game's hidden/helper interaction convention in the
    audited Castaway runtime tables. Exact overrides/translations/manual review
    decisions always take precedence, so a future proven exception can still be
    promoted explicitly.
    """
    en = row.get('en') or ''
    description = row.get('description') or ''
    if en.startswith('*'):
        return {
            'status': 'excluded',
            'reason': 'Leading * marks a hidden/helper interaction; current accepted exact promotions contain zero star-prefixed player-facing rows.',
        }
    if re.search(r'\bdeleted\b|\bnot needed\b|\bnot used\b|\bunused\b', description, re.I):
        return {
            'status': 'excluded',
            'reason': 'Source metadata explicitly marks the inherited row deleted/not-needed/not-used/unused; no accepted promotion uses this metadata family.',
        }
    if re.match(r'^(?:DEBUG|DBG)\b', en, re.I):
        return {
            'status': 'excluded',
            'reason': 'DEBUG/DBG-prefixed inherited interaction or diagnostic; current accepted exact promotions contain zero rows from this value family.',
        }
    if re.fullmatch(r'(?:[0-9a-f]{8}|bebe[0-9a-f]+|ecdb[0-9a-f]+)', en, re.I):
        return {
            'status': 'excluded',
            'reason': 'Opaque internal string identifier/hash rather than player-facing copy; no accepted promotion uses this value family.',
        }
    return None


def load_row_overrides():
    """Load exact row guards from the base file plus numbered review shards."""
    rows = []
    for path in sorted(RUNTIME.glob('row_scope_overrides*.json')):
        data = json.loads(path.read_text())
        if not isinstance(data, list):
            raise ValueError(('Row override shard must be a JSON list', path.name))
        rows.extend(data)
    return rows


def load_row_review_decisions():
    """Load exact inherited-row exclude/retain decisions from numbered shards."""
    rows = []
    for path in sorted(RUNTIME.glob('row_review_decisions*.json')):
        if path.name == 'row_review_decisions_applied.json':
            continue
        data = json.loads(path.read_text())
        if not isinstance(data, list):
            raise ValueError(('Row review decision shard must be a JSON list', path.name))
        rows.extend(data)
    return rows


def load_row_translations():
    """Load context-specific translations for exact rows with duplicated source text."""
    rows = []
    seen = set()
    for path in sorted(RUNTIME.glob('row_translation_overrides*.json')):
        data = json.loads(path.read_text())
        if not isinstance(data, list):
            raise ValueError(('Row translation shard must be a JSON list', path.name))
        for row in data:
            identity = (row['package'], tuple(row['key']), row['row'])
            if identity in seen:
                raise ValueError(('Duplicate exact row translation', identity))
            if row.get('category') not in ('menu','catalog','ui','story','tutorial','want','dialog','object','text','character','neighborhood'):
                raise ValueError(('Unsupported exact row translation category', identity, row.get('category')))
            validate(row['en'], row['vi'])
            seen.add(identity)
            rows.append(row)
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

    row_translations = {}
    for translation in load_row_translations():
        identity = (translation['package'], tuple(translation['key']), translation['row'])
        if identity in overrides:
            raise ValueError(('Row cannot be both generic-promoted and exact-translated', identity))
        row_translations[identity] = translation

    review_decisions = {}
    for decision in load_row_review_decisions():
        identity = (decision['package'], tuple(decision['key']), decision['row'])
        if identity in review_decisions:
            raise ValueError(('Duplicate row review decision', identity))
        if identity in overrides or identity in row_translations:
            raise ValueError(('Row cannot be both promoted/exact-translated and excluded/retained', identity))
        if decision.get('status') not in ('excluded', 'retain'):
            raise ValueError(('Unsupported row review decision status', identity, decision.get('status')))
        review_decisions[identity] = decision
    applied_path = RUNTIME/'row_review_decisions_applied.json'
    applied_decisions = {}
    if applied_path.exists():
        for decision in json.loads(applied_path.read_text()):
            identity = (decision['package'], tuple(decision['key']), decision['row'])
            applied_decisions[identity] = decision

    catalog_by_id = {row_identity(row): row for row in records}
    review_by_id = {row_identity(row): row for row in review}
    promoted = []
    promoted_ids = set()
    decided_ids = set()
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
            raise ValueError((
                'Pending row override baseline mismatch', identity,
                'source', (row['category'], row['language'], repr(row['en']), repr(row['description'])),
                'override', (override['category'], override['language'], repr(override['en']), repr(override['description'])),
            ))
        promoted_row = dict(row)
        promoted_row['category'] = override['category']
        promoted_row['reason'] = override['reason']
        promoted.append(promoted_row)
        promoted_ids.add(identity)

    for identity, translation in row_translations.items():
        if identity in catalog_by_id:
            row = catalog_by_id[identity]
            if row['category'] != translation['category'] or (row['language'], row['en'], row['description']) != (translation['language'], translation['en'], translation['description']):
                raise ValueError(('Extracted exact row translation mismatch', identity))
            continue
        row = review_by_id.get(identity)
        if row is None:
            raise ValueError(('Exact row translation missing from catalog and review snapshots', identity))
        if row['category'] != 'review' or (row['language'], row['en'], row['description']) != (translation['language'], translation['en'], translation['description']):
            raise ValueError((
                'Pending exact row translation baseline mismatch', identity,
                'source', (row['category'], row['language'], repr(row['en']), repr(row['description'])),
                'translation', (translation['category'], translation['language'], repr(translation['en']), repr(translation['description'])),
            ))
        promoted_row = dict(row)
        promoted_row['category'] = translation['category']
        promoted_row['reason'] = translation['reason']
        promoted.append(promoted_row)
        promoted_ids.add(identity)

    for identity, decision in review_decisions.items():
        if identity in catalog_by_id:
            raise ValueError(('Row review decision overlaps candidate row', identity))
        row = review_by_id.get(identity)
        if row is None:
            applied = applied_decisions.get(identity)
            if applied != decision:
                raise ValueError(('Row review decision missing from review snapshot and applied-decision inventory', identity))
            continue
        if row['category'] != 'review' or (row['language'], row['en'], row['description']) != (decision['language'], decision['en'], decision['description']):
            raise ValueError((
                'Pending row review decision baseline mismatch', identity,
                'source', (row['category'], row['language'], repr(row['en']), repr(row['description'])),
                'decision', (decision['status'], decision['language'], repr(decision['en']), repr(decision['description'])),
            ))
        decided_ids.add(identity)

    auto_decided_ids = set()
    for row in review:
        identity = row_identity(row)
        if identity in promoted_ids or identity in decided_ids:
            continue
        if auto_review_decision(row):
            auto_decided_ids.add(identity)

    if promoted:
        records.extend(promoted)
    if promoted_ids or decided_ids or auto_decided_ids:
        review = [
            row for row in review
            if row_identity(row) not in promoted_ids
            and row_identity(row) not in decided_ids
            and row_identity(row) not in auto_decided_ids
        ]
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
    exact_translations = {
        (r['package'], tuple(r['key']), r['row']): r
        for r in load_row_translations()
    }
    raw_review = read_records('review_queue')
    overrides_ids = {
        (r['package'], tuple(r['key']), r['row'])
        for r in load_row_overrides()
    }
    exact_translation_ids = {
        (r['package'], tuple(r['key']), r['row'])
        for r in load_row_translations()
    }
    manual_decision_ids = {
        (r['package'], tuple(r['key']), r['row'])
        for r in load_row_review_decisions()
    }
    auto_review_exclusions = sum(
        1 for row in raw_review
        if row_identity(row) not in overrides_ids
        and row_identity(row) not in exact_translation_ids
        and row_identity(row) not in manual_decision_ids
        and auto_review_decision(row)
    )
    records, review = effective_records()
    decisions = {}
    for row in json.loads((RUNTIME/'scope_decisions.json').read_text()):
        key = row['category'], row['en']
        if key in decisions:
            raise ValueError(('Duplicate scope decision', key))
        decisions[key] = row
    group_statuses = collections.defaultdict(lambda: collections.defaultdict(list))
    remaining = []
    for row in records:
        category, en = row['category'], row['en']
        identity = row_identity(row)
        decision = decisions.get((category,en))
        if identity in exact_translations:
            status = 'translated'
        elif decision:
            status = decision['status']
        elif en in maps.get(category,{}):
            status = 'translated'
        else:
            status = 'missing'
        group_statuses[category][en].append(status)
        if status in ('missing','review'):
            remaining.append(dict(row,status=status))

    categories = {}
    for category, values in sorted(group_statuses.items()):
        collapsed = {}
        for en, statuses in values.items():
            if any(s in ('missing','review') for s in statuses):
                collapsed[en] = 'missing'
            elif 'translated' in statuses:
                collapsed[en] = 'translated'
            else:
                collapsed[en] = statuses[0]
        categories[category] = dict(collections.Counter(collapsed.values()))

    inventory = json.loads((RUNTIME/'inventory.json').read_text())
    parse_errors = sum(len(x['errors']) for x in inventory)
    report = {
        'status': 'incomplete' if remaining or review or parse_errors else 'source-complete',
        'in_game_tested': False,
        'scope': 'Cast localization metadata + exact same-resource English variants + reviewed exact row overrides/translations. Remaining inherited rows are unresolved, not silently excluded.',
        'categories': categories,
        'translation_map_entries': sum(map(len,maps.values())) + len(exact_translations),
        'exact_row_translation_entries': len(exact_translations),
        'candidate_rows': len(records),
        'untranslated_or_review_candidate_rows': len(remaining),
        'untagged_review_rows': len(review),
        'auto_review_exclusions': auto_review_exclusions,
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
