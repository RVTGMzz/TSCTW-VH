"""Read-only audit and opt-in staging of ORIGINAL Castaway runtime baselines.

Source paths belong to the user's local game and Documents folders. Never
change a source package, and never treat a user save as an install template.
"""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

from validate_runtime import ROOT, RUNTIME

SAVE_PREFIX = "TSData/Res/UserData/"


def select_inventory(inventory, include_save_snapshots=False):
    """Default to installation packages; never sneak a Documents snapshot into a TEST payload."""
    if include_save_snapshots:
        return list(inventory)
    return [r for r in inventory if not r["package"].startswith(SAVE_PREFIX)]


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            block = stream.read(1024 * 1024)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def inside(path, parent):
    return path == parent or parent in path.parents


def source_for(package, game_root, save_root):
    if package.startswith(SAVE_PREFIX):
        if save_root is None:
            return None
        return save_root / package[len(SAVE_PREFIX):]
    return game_root / package


def inspect(inventory, game_root, save_root):
    checks = []
    for item in inventory:
        relative = item["package"]
        source = source_for(relative, game_root, save_root)
        result = {
            "package": relative,
            "origin": "Documents/user-save" if relative.startswith(SAVE_PREFIX) else "installation",
            "source": str(source) if source else None,
            "expected_sha256": item["sha256"],
            "expected_bytes": item["bytes"],
        }
        if source is None:
            result["status"] = "save_root_required"
        elif not source.is_file():
            result["status"] = "missing"
        else:
            actual_size = source.stat().st_size
            result["actual_bytes"] = actual_size
            actual = sha256(source)
            result["actual_sha256"] = actual
            result["status"] = "verified" if actual == item["sha256"] and actual_size == item["bytes"] else "baseline_mismatch"
        checks.append(result)
    return checks


def main():
    ap = argparse.ArgumentParser(description="Audit user-owned original Castaway packages safely; default mode does not copy anything.")
    ap.add_argument("--game-root", type=Path, required=True, help="Game folder containing TSData, for example G:/Castaway-Portable")
    ap.add_argument("--save-root", type=Path, help="Actual Documents game-data root containing Neighborhoods/N001, N002 and NeighborhoodManager.package")
    ap.add_argument("--output", type=Path, default=ROOT / "work" / "input", help="Disposable staging directory (default work/input)")
    ap.add_argument("--report", type=Path, default=ROOT / "work" / "baseline_preflight.json")
    ap.add_argument("--include-save-snapshots", action="store_true", help="DEVELOPMENT QA ONLY: require exact old Documents snapshots. Never ship saved games.")
    ap.add_argument("--copy-verified", action="store_true", help="Copy strictly verified original installation packages to a disposable folder; save snapshots are opt-in QA only")
    args = ap.parse_args()

    game_root = args.game_root.resolve()
    save_root = args.save_root.resolve() if args.save_root else None
    output = args.output.resolve()
    report_path = args.report.resolve()
    if not (game_root / "TSData").is_dir():
        ap.error(f"Not a Castaway installation root: {game_root}")
    if inside(output, game_root) or (save_root and inside(output, save_root)):
        ap.error("Staging output must be outside both the game installation and Documents save root")
    inventory = json.loads((RUNTIME / "inventory.json").read_text(encoding="utf-8"))
    # The old audit staged N001/N002/NeighborhoodManager under an install-like alias.
    # In reality these came from Documents; normal TEST builds must not require or ship them.
    selected = select_inventory(inventory, args.include_save_snapshots)
    skipped_save_snapshots = len(inventory) - len(selected)
    results = inspect(selected, game_root, save_root)
    passed = all(r["status"] == "verified" for r in results)
    report = {
        "purpose": "original user-owned package baseline preflight, never a game patch",
        "total": len(results),
        "skipped_save_snapshots": skipped_save_snapshots,
        "included_user_save_snapshots": bool(args.include_save_snapshots),
        "verified": sum(r["status"] == "verified" for r in results),
        "all_verified": passed,
        "staged": False,
        "files": results,
    }
    if args.copy_verified:
        if not passed:
            print("BLOCKED: one or more ORIGINAL game/save package files are missing or have different hashes.")
        else:
            collisions = [str(output / r["package"]) for r in results if (output / r["package"]).exists()]
            if collisions:
                raise SystemExit("BLOCKED: refusing to overwrite existing staged files:\n" + "\n".join(collisions))
            for r in results:
                dest = output / r["package"]
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(r["source"], dest)
                if sha256(dest) != r["expected_sha256"]:
                    dest.unlink(missing_ok=True)
                    raise RuntimeError(("Source changed during staging or copy failed", r["package"]))
            report["staged"] = True
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verified": report["verified"], "total": report["total"], "skipped_save_snapshots": report["skipped_save_snapshots"], "staged": report["staged"], "report": str(report_path)}, ensure_ascii=False))
    if not passed:
        print("No originals changed. A mismatch can mean a modded current install or a different Documents profile; do not patch blindly.")
        raise SystemExit(2)


if __name__ == "__main__":
    main()
