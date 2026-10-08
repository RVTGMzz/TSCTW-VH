"""Read-only origin matrix for Castaway story selector text; not runtime path proof."""
import collections
import json
from pathlib import Path
from validate_runtime import RUNTIME, read_records, row_identity, load_row_overrides, load_row_translations

KEYWORDS = ('Shipwrecked and Single', 'Wanmami Island', 'shipwreck survivor')
CONTEXT_KEYWORDS = ('shipwrecked', 'wanmami')
ROW_TRANSLATIONS = {
    row_identity(r): r['vi'] for r in load_row_translations()
}
OVERRIDES = {row_identity(r): r['category'] for r in load_row_overrides()}
UI = json.loads((RUNTIME / 'translations' / 'ui.json').read_text())


def short(value, n=260):
    return (value[:n] + '…') if len(value) > n else value


def main():
    matches = []
    sources = [
        ('candidate_catalog', read_records('catalog')),
        ('inherited_review', read_records('review_queue')),
    ]
    for origin, rows in sources:
        for r in rows:
            value = r.get('en') or ''
            if not any(key.lower() in value.lower() for key in KEYWORDS):
                continue
            ident = row_identity(r)
            translated = ROW_TRANSLATIONS.get(ident, UI.get(value))
            matches.append({
                'source_kind': origin,
                'package': r['package'],
                'key': r['key'],
                'row': r['row'],
                'language': r['language'],
                'type': r.get('type'),
                'source_category': r.get('category'),
                'exact_override_category': OVERRIDES.get(ident),
                'english': short(value),
                'vietnamese_available': translated is not None,
                'vietnamese': short(translated or ''),
                'description': short(r.get('description') or ''),
            })
    matches.sort(key=lambda r: (r['package'], r['key'], r['row']))
    print('=== CASTAWAY STORY SELECTOR SOURCE CANDIDATES ===')
    print(json.dumps({
        'searched_text': list(KEYWORDS),
        'matching_rows': len(matches),
        'packages': dict(collections.Counter(row['package'] for row in matches)),
        'language_counts': dict(collections.Counter(str(row['language']) for row in matches)),
        'runtime_source_verified': False,
        'reason': 'Static inventory matches do not prove what the running game reads.',
        'rows': matches[:100],
        'truncated_matches': max(len(matches) - 100, 0),
    }, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()
