"""Build a LOCAL, reversible v0.8 TEST payload from the user's ORIGINAL game packages.

Never auto-installs, never includes Documents saves, never includes fonts or executables.
This is a candidate TEST builder and is NOT proof of in-game functionality.
"""
import argparse
import collections
import hashlib
import json
import shutil
from pathlib import Path

from build_v07 import FULL_REQUIRED, STR_TYPE, derive_targets, load_translations, load_v06_history, patch_package
from dbpf import entries, unpack, strings
from check_runtime_packages import apply
from safe_rebase_runtime import inspect_prepatched, load_reviewed_legacy_migrations
from stage_runtime_inputs import select_inventory
from validate_runtime import ROOT, RUNTIME, assess, effective_records, load_maps, load_row_translations, row_identity


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def strict_locations(core, runtime, output):
    core, runtime, output = core.resolve(), runtime.resolve(), output.resolve()
    for ancestor in (core, runtime):
        if output == ancestor or ancestor in output.parents or output in ancestor.parents:
            raise ValueError("Output must be outside both original input trees (and may not contain either tree).")
    if output.exists() and any(output.iterdir()):
        raise ValueError("Output folder exists and is nonempty; refusing to overwrite a previous TEST.")
    return core, runtime, output


def source_inventory():
    all_records = json.loads((RUNTIME / "inventory.json").read_text(encoding="utf-8"))
    inventory = select_inventory(all_records)
    if any(row["errors"] for row in inventory):
        raise ValueError("Original audited inputs have parse errors")
    return inventory


def verify_inputs(core, runtime, inventory):
    required_core = sorted(FULL_REQUIRED)
    missing_core = [x for x in required_core if not (core/x).is_file()]
    if missing_core:
        raise FileNotFoundError("Missing ORIGINAL core Text files: " + ", ".join(missing_core))
    for row in inventory:
        path = runtime / row["package"]
        if not path.is_file():
            raise FileNotFoundError(f"Missing original runtime package: {path}")
        if path.stat().st_size != row["bytes"] or digest(path) != row["sha256"]:
            raise ValueError(f"Runtime baseline mismatch (modded or wrong version): {path}")
    return required_core


def refuse_pretranslated_core(core, names, v06_history):
    """Reject detectable v0.6/v0.7a Vietnamese rows in presumed original Text inputs.

    Exact prior package/instance/language/value fingerprints are high-signal
    rejection evidence, though not a complete original-version verifier.
    """
    for name in names:
        source=core/name
        data=source.read_bytes()
        for type_id, group_id, instance, offset, size in entries(data):
            if type_id!=STR_TYPE:
                continue
            for lang,value,desc in strings(unpack(data[offset:offset+size])):
                english_sources=v06_history.get((name,instance,lang,value),())
                if any(english!=value for english in english_sources):
                    raise ValueError(
                        f"Core Text input appears to contain an earlier Vietnamese patch: {source}, "
                        f"STR# instance {instance}, language {lang}. Restore ORIGINAL English Text "
                        "or use --runtime-only on an existing v0.7a installation."
                    )


def runtime_patch(source, path, records, maps, decisions, exact, preserve_unrecognized=False, legacy_migrations=None):
    before = source.read_bytes()
    after, count, resources = apply(before, records, maps, decisions, exact, preserve_unrecognized=preserve_unrecognized, legacy_migrations=legacy_migrations)
    repeated, n2, resource2 = apply(after, records, maps, decisions, exact, preserve_unrecognized=preserve_unrecognized, legacy_migrations=legacy_migrations)
    if repeated != after or n2 or resource2:
        raise AssertionError(f"Runtime patch is not idempotent: {path}")
    return after, count, resources


def manifest_row(path, source, patched, count, resources):
    return {
        "path": path,
        "original_sha256": digest(source),
        "patched_sha256": hashlib.sha256(patched).hexdigest(),
        "changed_rows": count,
        "changed_resources": resources,
    }


def build(core, runtime, output, core_original_confirmed=False, runtime_only=False, allow_prepatched_runtime=False, allow_no_changes=False):
    core, runtime, output = strict_locations(core, runtime, output)
    if allow_prepatched_runtime and not runtime_only:
        raise ValueError("Modified runtime compatibility mode is allowed only on runtime-only overlay")
    if not runtime_only and not core_original_confirmed:
        raise ValueError("Core Text originals not confirmed. Supply --core-original-confirmed ONLY after restoring original core files, not v0.7a patched Text packages.")
    report, _ = assess()
    if report["parse_errors"] or report["untranslated_or_review_candidate_rows"]:
        raise ValueError("Source audit has unresolved candidate rows or parse errors; no candidate TEST build.")
    inventory = source_inventory()
    required_core = verify_inputs(core, runtime, inventory) if not runtime_only else []  # Runtime-only mode is for existing v0.7a Text/font installations.
    if runtime_only:
        for item in inventory:
            path=runtime/item["package"]
            if not path.is_file():
                raise FileNotFoundError(f"Runtime input package missing: {path}")
            if (path.stat().st_size != item["bytes"] or digest(path) != item["sha256"]) and not allow_prepatched_runtime:
                raise ValueError(f"Runtime original missing/hash mismatch: {path}. Use explicit audited compatibility mode instead of disabling exact-row checks.")
    maps = load_maps()
    decisions = {(r["category"], r["en"]) for r in json.loads((RUNTIME/"scope_decisions.json").read_text(encoding="utf-8"))}
    exact = {(r["package"],tuple(r["key"]),r["row"]):r for r in load_row_translations()}
    effective, _ = effective_records()
    grouped = collections.defaultdict(list)
    for r in effective:
        grouped[r["package"]].append(r)
    legacy_migrations = load_reviewed_legacy_migrations(RUNTIME, grouped, maps, exact)

    compatibility_checks = []
    for item in inventory:
        path=runtime/item["package"]
        if path.stat().st_size != item["bytes"] or digest(path) != item["sha256"]:
            if not allow_prepatched_runtime:
                raise ValueError(("Modified runtime input not permitted",str(path)))
            compatibility_checks.append(
                inspect_prepatched(path.read_bytes(),item,grouped[item["package"]],maps,decisions,exact, preserve_unrecognized=True, legacy_migrations=legacy_migrations)
            )

    changed = []
    summaries = []
    payload = output/"Payload"
    try:
        # Runtime-only overlays deliberately do NOT load the original core Text
        # translation catalog, castaway-english-strings.json, or validation.json.
        # Neither is needed for runtime DBPF patching. Load them ONLY in full mode.
        if required_core:
            core_translations, sources, overrides = load_translations()
            targets, _ = derive_targets(core_translations)
            history = load_v06_history()
            refuse_pretranslated_core(core, required_core, history)
        for name in required_core:
            source = core/name
            dest = payload/"TSData"/"Res"/"Text"/name
            details = patch_package(source, dest, targets.get(name, set()), core_translations, history)
            changed_rows = len(details["changes"])
            summaries.append({"package": f"TSData/Res/Text/{name}", "scope":"core", "changed_rows": changed_rows})
            if changed_rows:
                changed.append(manifest_row(f"TSData/Res/Text/{name}",source,dest.read_bytes(),changed_rows,details["changed_resources"]))
            else:
                dest.unlink()

        for item in inventory:
            rel = item["package"]
            source = runtime/rel
            patched, count, resources = runtime_patch(source, rel, grouped[rel], maps, decisions, exact, preserve_unrecognized=allow_prepatched_runtime, legacy_migrations=legacy_migrations)
            summaries.append({"package":rel,"scope":"runtime","changed_rows":count})
            if count:
                target = payload/rel
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(patched)
                changed.append(manifest_row(rel,source,patched,count,resources))
        if not changed and not allow_no_changes:
            raise ValueError("No changed game packages; not generating an empty TEST.")
        if any("UserData/" in r["path"] or not r["path"].startswith("TSData/Res/") for r in changed):
            raise AssertionError("Refusing any Documents save or non-package input in payload")
        if len({r["path"] for r in changed}) != len(changed):
            raise AssertionError("Core/runtime payload path collision")

        manifest = {
            "schema": "TSCTW-V08-TEST-1",
            "build_mode": "runtime-overlay-on-v07a" if runtime_only else "full-original-text-plus-runtime",
            "label": "LOCAL CANDIDATE ONLY: requires actual game test",
            "in_game_tested": False,
            "font": "Keep existing working RonVN font installation; this builder does NOT modify font files",
            "core_text": ("Preserve existing v0.7a core Text files; NOT a consolidated/full rebuild" if runtime_only else "Build all eight original core Text packages"),
            "source_audit": {
                "candidate_rows":report["candidate_rows"],
                "parse_errors":report["parse_errors"],
                "untranslated_candidates":report["untranslated_or_review_candidate_rows"]
            },
            "install_files": sorted(changed,key=lambda x:x["path"]),
            "no_applicable_english_rows": not changed,
            "modified_baseline_checks": compatibility_checks,
            "unrecognized_rows_preserved": sum(x.get("unrecognized_rows_preserved",0) for x in compatibility_checks),
            "reviewed_old_translations_upgraded": sum(x.get("reviewed_legacy_rows_upgradable",0) for x in compatibility_checks),
            "build_summary": summaries,
        }
        output.mkdir(parents=True,exist_ok=True)
        (output/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        return manifest
    except Exception:
        # An incomplete candidate must not masquerade as a usable TEST output.
        if output.exists():
            shutil.rmtree(output)
        raise


def main():
    ap=argparse.ArgumentParser(description="Generate LOCAL v0.8 candidate from original game packages; NEVER modifies installation")
    ap.add_argument("--runtime-input",type=Path,default=ROOT/"work"/"input",help="10 install-owned original packages with exact inventory hash")
    ap.add_argument("--core-input",type=Path,default=ROOT/"work"/"text"/"Text",help="8 original core Text/*.package files")
    ap.add_argument("--output",type=Path,default=ROOT/"work"/"v08_candidate",help="Disposable new empty folder outside original inputs")
    ap.add_argument("--core-original-confirmed",action="store_true",help="Explicit affirmation Text inputs are ORIGINAL not v0.7a-patched")
    ap.add_argument("--runtime-only",action="store_true",help="Incremental runtime TEST OVERLAY for existing v0.7a + working font; skips core Text packages")
    ap.add_argument("--allow-compatible-modified-runtime",action="store_true",help="Explicit conservative rebase for prepatched runtime: validate DBPF index, every target row, metadata, source/approved translation")
    args=ap.parse_args()
    manifest=build(args.core_input,args.runtime_input,args.output,args.core_original_confirmed,args.runtime_only,args.allow_compatible_modified_runtime)
    print(json.dumps({"candidate":"prepared locally; NOT in-game tested",
                      "changed_files":len(manifest["install_files"]),
                      "changed_rows":sum(i["changed_rows"] for i in manifest["install_files"]),
                      "manifest":str(args.output/"manifest.json")},ensure_ascii=False))


if __name__ == "__main__":
    main()
