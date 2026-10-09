"""Conservative compatibility audit for prepatched Castaway runtime packages.

Does NOT waive resource/row/language/metadata checks and does NOT identify
unknown game versions as original. All eligible translated row identities must
still match the audited English OR the exact currently approved Vietnamese.
Unknown edits on target resources block installation. Non-target resources stay
byte-identical during patching.
"""
import collections
import json
from runtime_dbpf import Package, parse_table
from validate_runtime import row_identity


def load_reviewed_legacy_migrations(runtime_dir, grouped, maps, exact):
    """Allow old->new wording ONLY where all source identifiers still match.

    Never infer old Vietnamese text from whether a string merely looks
    Vietnamese. The migration file lists the exact old approved wording.
    """
    path = runtime_dir / "reviewed_translation_migrations.json"
    if not path.is_file():
        return {}
    records = json.loads(path.read_text(encoding="utf-8"))
    out = {}
    rows_by_id = {
        row_identity(row): row for package_rows in grouped.values() for row in package_rows
    }
    for old_row in records:
        ident = (old_row["package"], tuple(old_row["key"]), old_row["row"])
        if ident in out:
            raise ValueError(("Duplicate reviewed legacy migration", ident))
        original = rows_by_id.get(ident)
        if original is None or any(original[k] != old_row[k] for k in ("language","en","description")):
            raise ValueError(("Reviewed legacy migration source identity mismatches audited data", ident))
        new_vi = exact[ident]["vi"] if ident in exact else maps.get(original["category"],{}).get(original["en"])
        if not new_vi or new_vi == old_row["old_vi"]:
            raise ValueError(("Reviewed legacy migration lacks different approved new translation", ident))
        out[ident] = old_row
    return out


def inspect_prepatched(data, inventory_item, rows, maps, decisions, exact_translations, preserve_unrecognized=False, legacy_migrations=None):
    package = Package(data)
    if package.width != inventory_item["index_width"] or package.count != inventory_item["resources"]:
        raise ValueError((
            "DBPF structure differs from the audited Castaway package",
            inventory_item["package"], package.width, package.count,
            inventory_item["index_width"], inventory_item["resources"],
        ))

    index = {entry.key: entry for entry in package.entries}
    groups = collections.defaultdict(list)
    for row in rows:
        key = (row["category"], row["en"])
        rid = row_identity(row)
        if rid not in exact_translations and (
            key in decisions or row["en"] not in maps.get(row["category"], {})
        ):
            continue
        groups[tuple(row["key"])].append(row)
    if not groups:
        raise ValueError(("No verified translatable resources in modified package", inventory_item["package"]))

    english = translated = preserved = migrated = 0
    legacy_migrations = legacy_migrations or {}
    examples = []
    checked_rows = 0
    for key, targets in groups.items():
        entry = index.get(key)
        if entry is None:
            raise ValueError(("Missing audited DBPF resource", inventory_item["package"], key))
        source_rows, tail = parse_table(package.raw(entry))
        for row in targets:
            n = row["row"]
            if n >= len(source_rows):
                raise ValueError(("Audited row index is missing", inventory_item["package"], key, n))
            language, actual, description = source_rows[n]
            if (language, description) != (row["language"], row["description"]):
                raise ValueError(("Audited row metadata mismatch", inventory_item["package"], key, n))
            rid = row_identity(row)
            vi = (exact_translations[rid]["vi"] if rid in exact_translations
                  else maps[row["category"]][row["en"]])
            if actual == row["en"]:
                english += 1
            elif actual == vi:
                translated += 1
            elif rid in legacy_migrations and actual == legacy_migrations[rid]["old_vi"]:
                migrated += 1
            else:
                if not preserve_unrecognized:
                    raise ValueError((
                        "Unrecognized translated/source text, refusing unsafe overwrite",
                        inventory_item["package"], key, n, actual[:100]
                    ))
                # The row identity and metadata match, but its actual text has
                # unknown provenance (possibly an earlier Vietnamese revision).
                # NEVER treat it as validated Vietnamese and NEVER replace it.
                preserved += 1
                if len(examples) < 12:
                    examples.append({
                        "key": list(key), "row": n,
                        "source_preview": row["en"][:90],
                        "existing_preview": actual[:90],
                    })
            checked_rows += 1
    return {
        "package": inventory_item["package"],
        "index_width": package.width,
        "resources": package.count,
        "verified_row_count": checked_rows,
        "english_source_rows": english,
        "already_approved_vietnamese_rows": translated,
        "reviewed_legacy_rows_upgradable": migrated,
        "unrecognized_rows_preserved": preserved,
        "unrecognized_examples": examples,
        "resource_count_checked": len(groups),
        "interpretation": "audited row-compatible modified baseline, NOT the original SHA-256",
    }
