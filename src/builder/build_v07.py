from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import json
import re
import struct

from dbpf import entries, unpack, strings
from qfs import compress as qfs_compress

ROOT = Path(__file__).resolve().parents[2]
TRANSLATIONS_DIR = ROOT / "translations"
CATALOG_PATH = ROOT / "castaway-english-strings.json"
V06_VALIDATION_PATH = ROOT / "validation.json"
DEFAULT_INPUT = ROOT / "work" / "text" / "Text"
DEFAULT_OUTPUT = ROOT / "work" / "build_v07"

STR_TYPE = 0x53545223
DIR_TYPE = 0xE86B1EEF

ALLOWED_PACKAGES = {
    "Options.package",
    "UIText.package",
    "Live.package",
    "Neighborhood.package",
    "Build.package",
    "CAS.package",
    "CAS_Shared.package",
    "Tutorial.package",
}

INCREMENTAL_REQUIRED = {
    "Options.package",
    "UIText.package",
    "Live.package",
    "Neighborhood.package",
    "Build.package",
    "CAS.package",
    "CAS_Shared.package",
}

FULL_REQUIRED = INCREMENTAL_REQUIRED | {"Tutorial.package"}

PACKAGE_OVERRIDES = {
    "Neighborhood.package": {
        "Play": "Chơi",
    },
}

PRINTF_RE = re.compile(
    r"%(?:\d+\$)?[-+0#]*\d*(?:\.\d+)?(?:hh|h|ll|l|L|z|j|t)?[diuoxXfFeEgGaAcspnD]"
)
DOLLAR_RE = re.compile(r"\$[A-Za-z][A-Za-z0-9_]*(?::\d+)?")
CYRILLIC_RE = re.compile(r"[\u0400-\u04FF]")


def token_signature(text: str) -> list[str]:
    return PRINTF_RE.findall(text) + DOLLAR_RE.findall(text)


def line_signature(text: str) -> tuple[int, int]:
    return text.count("\r"), text.count("\n")


def metadata_signature(text: str) -> list[str] | None:
    parts = text.split("|")
    return parts[2:] if len(parts) >= 3 else None


def translated_value(package_name: str, en: str, translations: dict[str, str]) -> str:
    return PACKAGE_OVERRIDES.get(package_name, {}).get(en, translations[en])


def load_v06_history() -> dict[tuple[str, int, int, str], set[str]]:
    """Map each v0.6 translated row back to its English source key."""
    if not V06_VALIDATION_PATH.is_file():
        raise FileNotFoundError(
            f"Missing v0.6 validation baseline: {V06_VALIDATION_PATH}"
        )

    validation = json.loads(V06_VALIDATION_PATH.read_text(encoding="utf-8"))
    history: dict[tuple[str, int, int, str], set[str]] = {}

    for file_report in validation.get("files", []):
        package = file_report.get("file")
        if package not in ALLOWED_PACKAGES:
            continue
        for change in file_report.get("changes", []):
            key = (
                package,
                int(change["instance"]),
                int(change["language"]),
                change["vi"],
            )
            history.setdefault(key, set()).add(change["en"])

    return history


def resolve_source_value(
    package: str,
    instance: int,
    language: int,
    value: str,
    translations: dict[str, str],
    v06_history: dict[tuple[str, int, int, str], set[str]],
) -> tuple[str, str] | None:
    """Resolve an English baseline string or an unambiguous v0.6 Vietnamese value."""
    if value in translations:
        return value, translated_value(package, value, translations)

    candidates = v06_history.get((package, instance, language, value), set())
    final_values = {
        translated_value(package, en, translations)
        for en in candidates
        if en in translations
    }
    if len(final_values) != 1:
        return None

    final_value = next(iter(final_values))
    source_keys = [
        en for en in candidates
        if en in translations and translated_value(package, en, translations) == final_value
    ]
    return (source_keys[0], final_value) if source_keys else None


def validate_translation(en: str, vi: str) -> None:
    if CYRILLIC_RE.search(vi):
        raise AssertionError(("unexpected Cyrillic character", en, vi))
    if token_signature(en) != token_signature(vi):
        raise AssertionError(("placeholder mismatch", en, vi, token_signature(en), token_signature(vi)))
    if line_signature(en) != line_signature(vi):
        raise AssertionError(("line break mismatch", en, vi, line_signature(en), line_signature(vi)))
    meta = metadata_signature(en)
    if meta is not None and meta != metadata_signature(vi):
        raise AssertionError(("tooltip metadata mismatch", en, vi))


def translation_files() -> list[Path]:
    files = [TRANSLATIONS_DIR / "translations.json"]

    def extra_number(path: Path) -> int:
        m = re.fullmatch(r"extra(\d+)\.json", path.name)
        return int(m.group(1)) if m else 10**9

    files.extend(sorted(TRANSLATIONS_DIR.glob("extra*.json"), key=extra_number))
    return [p for p in files if p.exists()]


def load_translations() -> tuple[dict[str, str], list[str], list[dict[str, str]]]:
    merged: dict[str, str] = {}
    origin: dict[str, str] = {}
    used_files: list[str] = []
    overrides: list[dict[str, str]] = []

    for path in translation_files():
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise TypeError(f"{path} must contain a JSON object")
        used_files.append(path.name)

        for en, vi in data.items():
            if not isinstance(en, str) or not isinstance(vi, str):
                raise TypeError(f"{path}: translation keys and values must be strings")
            if en in merged and merged[en] != vi:
                overrides.append(
                    {
                        "en": en,
                        "from_file": origin[en],
                        "from_vi": merged[en],
                        "to_file": path.name,
                        "to_vi": vi,
                    }
                )
            merged[en] = vi
            origin[en] = path.name

    return merged, used_files, overrides


def derive_targets(translations: dict[str, str]) -> tuple[dict[str, set[int]], dict[str, int]]:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    targets = {name: set() for name in ALLOWED_PACKAGES}
    hits: dict[str, int] = {}

    for row in catalog:
        package = row.get("file")
        en = row.get("text")
        instance = row.get("id")
        if package not in ALLOWED_PACKAGES or en not in translations:
            continue
        targets[package].add(int(instance))
        hits[en] = hits.get(en, 0) + 1

    return targets, hits


def audit_translation_source(
    translations: dict[str, str],
    targets: dict[str, set[int]],
    used_files: list[str],
    overrides: list[dict[str, str]],
) -> dict[str, object]:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    locations: dict[str, list[dict[str, object]]] = {}

    for row in catalog:
        en = row.get("text")
        if not isinstance(en, str):
            continue
        locations.setdefault(en, []).append(
            {
                "file": row.get("file"),
                "id": row.get("id"),
            }
        )

    for en, vi in translations.items():
        validate_translation(en, vi)

    missing_from_catalog = sorted(en for en in translations if en not in locations)
    allowed_mapping_keys = sorted(
        en
        for en in translations
        if any(loc.get("file") in ALLOWED_PACKAGES for loc in locations.get(en, []))
    )

    target_summary = {
        package: sorted(instances)
        for package, instances in sorted(targets.items())
        if instances
    }

    return {
        "runtime_tested": False,
        "translation_files": used_files,
        "translation_mapping_count": len(translations),
        "translation_overrides": overrides,
        "mapping_keys_present_in_allowed_packages": len(allowed_mapping_keys),
        "mapping_keys_missing_from_catalog": missing_from_catalog,
        "target_resource_instances": target_summary,
        "checks": [
            "All merged source mappings pass placeholder, line-break and tooltip-metadata validation.",
            "Vietnamese values are checked for accidental Cyrillic characters.",
            "Catalog presence is reported without requiring game package files.",
            "No claim of in-game testing is made by this audit.",
        ],
    }


def encode_string_table(raw: bytes, rows: list[list[object]]) -> bytes:
    body = b"".join(
        bytes([int(lang)])
        + str(value).encode("utf-8", "surrogateescape")
        + b"\0"
        + str(description).encode("utf-8", "surrogateescape")
        + b"\0"
        for lang, value, description in rows
    )
    return raw[:68] + body


def patch_package(
    source: Path,
    destination: Path,
    target_instances: set[int],
    translations: dict[str, str],
    v06_history: dict[tuple[str, int, int, str], set[str]],
) -> dict[str, object]:
    original = source.read_bytes()
    new = bytearray(original)
    original_entries = entries(original)
    index_offset = struct.unpack_from("<I", original, 40)[0]

    changed_decompressed_sizes: dict[tuple[int, int, int], int] = {}
    changes: list[dict[str, object]] = []

    for n, (type_id, group_id, instance_id, offset, size) in enumerate(original_entries):
        if type_id != STR_TYPE or instance_id not in target_instances:
            continue

        raw = unpack(original[offset : offset + size])
        rows = strings(raw)
        updates = 0

        for row in rows:
            language, value, _description = row
            if language not in (1, 2):
                continue

            resolved = resolve_source_value(
                source.name,
                instance_id,
                language,
                value,
                translations,
                v06_history,
            )
            if resolved is None:
                continue

            source_english, translated = resolved
            validate_translation(source_english, translated)
            if translated == value:
                continue

            row[1] = translated
            updates += 1
            changes.append(
                {
                    "instance": instance_id,
                    "language": language,
                    "en": source_english,
                    "vi": translated,
                }
            )

        if not updates:
            continue

        rebuilt = encode_string_table(raw, rows)
        compressed = original[offset + 4 : offset + 6] == b"\x10\xfb"
        packed = qfs_compress(rebuilt) if compressed else rebuilt
        assert unpack(packed) == rebuilt

        new_offset = len(new)
        new.extend(packed)
        struct.pack_into("<II", new, index_offset + n * 20 + 12, new_offset, len(packed))
        changed_decompressed_sizes[(type_id, group_id, instance_id)] = len(rebuilt)

    for type_id, group_id, instance_id, offset, size in original_entries:
        if type_id != DIR_TYPE:
            continue
        assert size % 16 == 0
        for pos in range(offset, offset + size, 16):
            key = struct.unpack_from("<3I", original, pos)
            if key in changed_decompressed_sizes:
                struct.pack_into("<I", new, pos + 12, changed_decompressed_sizes[key])

    assert new[:96] == original[:96]
    new_entries = entries(new)
    assert len(new_entries) == len(original_entries)

    changed_keys = set(changed_decompressed_sizes)

    for old_entry, new_entry in zip(original_entries, new_entries):
        type_id, group_id, instance_id, old_offset, old_size = old_entry
        _, _, _, new_offset, new_size = new_entry
        key = (type_id, group_id, instance_id)
        assert old_entry[:3] == new_entry[:3]

        if type_id == DIR_TYPE:
            assert old_entry == new_entry
            for pos in range(old_offset, old_offset + old_size, 16):
                directory_key = struct.unpack_from("<3I", original, pos)
                assert new[pos : pos + 12] == original[pos : pos + 12]
                before = struct.unpack_from("<I", original, pos + 12)[0]
                after = struct.unpack_from("<I", new, pos + 12)[0]
                assert after == changed_decompressed_sizes.get(directory_key, before)
        elif key not in changed_keys:
            assert old_entry == new_entry
            assert new[old_offset : old_offset + old_size] == original[old_offset : old_offset + old_size]
        else:
            old_raw = unpack(original[old_offset : old_offset + old_size])
            new_raw = unpack(new[new_offset : new_offset + new_size])
            assert old_raw[:68] == new_raw[:68]
            assert unpack(new[new_offset : new_offset + new_size]) == new_raw

            old_compressed = original[old_offset + 4 : old_offset + 6] == b"\x10\xfb"
            new_compressed = new[new_offset + 4 : new_offset + 6] == b"\x10\xfb"
            assert old_compressed == new_compressed

            old_rows = strings(old_raw)
            new_rows = strings(new_raw)
            assert len(old_rows) == len(new_rows)

            for old_row, new_row in zip(old_rows, new_rows):
                language, old_value, old_description = old_row
                new_language, new_value, new_description = new_row
                assert language == new_language
                assert old_description == new_description

                resolved = (
                    resolve_source_value(
                        source.name,
                        instance_id,
                        language,
                        old_value,
                        translations,
                        v06_history,
                    )
                    if language in (1, 2)
                    else None
                )
                if resolved is not None:
                    source_english, expected = resolved
                    validate_translation(source_english, expected)
                    assert new_value == expected
                else:
                    assert new_value == old_value

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(new)

    return {
        "file": source.name,
        "source_sha256": hashlib.sha256(original).hexdigest(),
        "patched_sha256": hashlib.sha256(new).hexdigest(),
        "changed_resources": len(changed_decompressed_sizes),
        "changes": changes,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build the next TSCTW Vietnamese text patch without modifying build_v06.py."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Folder containing user-owned .package files (default: work/text/Text).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Build output folder (default: work/build_v07).",
    )
    parser.add_argument(
        "--audit-only",
        action="store_true",
        help="Validate merged translation sources against the catalog without requiring .package files.",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Require Tutorial.package too and rebuild all known translated text packages from an original baseline.",
    )
    args = parser.parse_args()

    translations, used_files, translation_overrides = load_translations()
    targets, catalog_hits = derive_targets(translations)

    if args.audit_only:
        audit = audit_translation_source(
            translations,
            targets,
            used_files,
            translation_overrides,
        )
        output_root = args.output
        output_root.mkdir(parents=True, exist_ok=True)
        audit_path = output_root / "source_audit.json"
        audit_path.write_text(
            json.dumps(audit, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print("SOURCE AUDIT PASS")
        print("Translation mappings:", audit["translation_mapping_count"])
        print("Mappings in allowed packages:", audit["mapping_keys_present_in_allowed_packages"])
        print("Missing from catalog:", len(audit["mapping_keys_missing_from_catalog"]))
        print("Output:", audit_path)
        return

    v06_history = load_v06_history()
    required = FULL_REQUIRED if args.full else INCREMENTAL_REQUIRED
    missing = sorted(name for name in required if not (args.input / name).is_file())
    if missing:
        raise FileNotFoundError(
            "Missing required package files:\n  - " + "\n  - ".join(missing)
        )

    output_root = args.output
    payload = output_root / "Payload" / "TSData" / "Res" / "Text"
    reports: list[dict[str, object]] = []

    for name in sorted(required):
        report = patch_package(
            args.input / name,
            payload / name,
            targets.get(name, set()),
            translations,
            v06_history,
        )
        reports.append(report)

    unique_changed = {
        change["en"]
        for report in reports
        for change in report["changes"]
    }

    validation = {
        "mode": "full-original" if args.full else "incremental-v06",
        "runtime_tested": False,
        "translation_files": used_files,
        "translation_mapping_count": len(translations),
        "translation_overrides": translation_overrides,
        "catalog_mapping_hits": len(catalog_hits),
        "required_packages": sorted(required),
        "checks": [
            "Only catalog-derived STR# resource instances in audited packages are eligible.",
            "Only language IDs 1 and 2 are translated.",
            "String count, order and descriptions are preserved.",
            "Other languages are preserved byte-for-byte within changed STR# resources.",
            "Untouched resources are byte-identical to the supplied baseline.",
            "Original compression state is preserved.",
            "QFS round-trip and decompressed-size directory entries are verified.",
            "Printf/$ tokens, line breaks and tooltip metadata are preserved.",
            "No claim of in-game testing is made by this builder.",
        ],
        "unique_english_strings_changed": len(unique_changed),
        "files": reports,
    }

    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "validation.json").write_text(
        json.dumps(validation, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    manifest = [
        {
            "path": f"TSData/Res/Text/{report['file']}",
            "original": report["source_sha256"],
            "patched": report["patched_sha256"],
        }
        for report in reports
    ]
    (output_root / "manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    print(
        "PASS",
        [
            (report["file"], len(report["changes"]), report["changed_resources"])
            for report in reports
        ],
    )
    print("Translation mappings:", len(translations))
    print("Unique English strings changed:", len(unique_changed))
    print("Output:", output_root)


if __name__ == "__main__":
    main()
