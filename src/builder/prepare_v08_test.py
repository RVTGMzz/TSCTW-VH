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

from build_v07 import FULL_REQUIRED, derive_targets, load_translations, load_v06_history, patch_package
from check_runtime_packages import apply
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


def runtime_patch(source, path, records, maps, decisions, exact):
    before = source.read_bytes()
    after, count, resources = apply(before, records, maps, decisions, exact)
    repeated, n2, resource2 = apply(after, records, maps, decisions, exact)
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


def build(core, runtime, output, core_original_confirmed=False, runtime_only=False):
    core, runtime, output = strict_locations(core, runtime, output)
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
            if not path.is_file() or path.stat().st_size != item["bytes"] or digest(path) != item["sha256"]:
                raise ValueError(f"Runtime original missing/hash mismatch: {path}")
    maps = load_maps()
    decisions = {(r["category"], r["en"]) for r in json.loads((RUNTIME/"scope_decisions.json").read_text(encoding="utf-8"))}
    exact = {(r["package"],tuple(r["key"]),r["row"]):r for r in load_row_translations()}
    effective, _ = effective_records()
    grouped = collections.defaultdict(list)
    for r in effective:
        grouped[r["package"]].append(r)

    changed = []
    summaries = []
    payload = output/"Payload"
    try:
        # Build core directly from its original English source, not from prior v0.7a patches.
        core_translations, sources, overrides = load_translations()
        targets, _ = derive_targets(core_translations)
        history = load_v06_history()
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
            patched, count, resources = runtime_patch(source, rel, grouped[rel], maps, decisions, exact)
            summaries.append({"package":rel,"scope":"runtime","changed_rows":count})
            if count:
                target = payload/rel
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(patched)
                changed.append(manifest_row(rel,source,patched,count,resources))
        if not changed:
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
    args=ap.parse_args()
    manifest=build(args.core_input,args.runtime_input,args.output,args.core_original_confirmed,args.runtime_only)
    print(json.dumps({"candidate":"prepared locally; NOT in-game tested",
                      "changed_files":len(manifest["install_files"]),
                      "changed_rows":sum(i["changed_rows"] for i in manifest["install_files"]),
                      "manifest":str(args.output/"manifest.json")},ensure_ascii=False))


if __name__ == "__main__":
    main()
