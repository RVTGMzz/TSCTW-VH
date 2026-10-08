"""Conservative compatibility audit for prepatched Castaway runtime packages.

Does NOT waive resource/row/language/metadata checks and does NOT identify
unknown game versions as original. All eligible translated row identities must
still match the audited English OR the exact currently approved Vietnamese.
Unknown edits on target resources block installation. Non-target resources stay
byte-identical during patching.
"""
import collections
from runtime_dbpf import Package, parse_table
from validate_runtime import row_identity


def inspect_prepatched(data, inventory_item, rows, maps, decisions, exact_translations):
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

    english = translated = 0
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
            else:
                raise ValueError((
                    "Unrecognized translated/source text, refusing unsafe overwrite",
                    inventory_item["package"], key, n, actual[:100]
                ))
            checked_rows += 1
    return {
        "package": inventory_item["package"],
        "index_width": package.width,
        "resources": package.count,
        "verified_row_count": checked_rows,
        "english_source_rows": english,
        "already_approved_vietnamese_rows": translated,
        "resource_count_checked": len(groups),
        "interpretation": "audited row-compatible modified baseline, NOT the original SHA-256",
    }
