"""Read-only story-selector diagnostic for the user's OWN Castaway installation/saves.

This locates copies of the N001/N002 title CTSS resource, records their current
English/Vietnamese state and exact path. Static source matches are NOT proof of
game-process read precedence. No source file is edited, copied or backed up.
"""
import argparse
import hashlib
import json
from pathlib import Path

from runtime_dbpf import Package, parse_table, TEXT_TYPES
from validate_runtime import ROOT, RUNTIME

CTSS = 0x43545353
STORY_GROUP = 0xFFFFFFFF
STORY_INSTANCE = 1
EXPECTED = {
    "N001": "Shipwrecked and Single",
    "N002": "Wanmami Island",
}


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as fd:
        for block in iter(lambda: fd.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def inspect_package(path, story_id, source_kind, mappings):
    info = {
        "source_kind": source_kind,
        "story_id": story_id,
        "path": str(path),
        "exists": path.is_file(),
        "resource_found": False,
        "read_path_observed": False,
    }
    if not path.is_file():
        return info
    info["bytes"] = path.stat().st_size
    info["sha256"] = digest(path)
    try:
        package = Package(path.read_bytes())
        info["index_width"] = package.width
        key = (CTSS, STORY_GROUP, STORY_INSTANCE, 0) if package.width == 24 else (CTSS, STORY_GROUP, STORY_INSTANCE)
        entry = next((x for x in package.entries if x.key == key), None)
        if entry is None:
            info["note"] = "No matching CTSS title key; this is not proof game ignores the file."
            return info
        info["resource_found"] = True
        info["resource_key"] = list(key)
        raw = package.raw(entry)
        rows, unused_tail = parse_table(raw)
        expected = EXPECTED[story_id]
        translated = mappings.get(expected)
        info["title_rows"] = []
        for i, row in enumerate(rows):
            if i > 1:
                break
            lang, value, description = row
            state = ("original_english" if value == expected else
                     "mapped_vietnamese" if i == 0 and translated and value == translated else
                     "other_or_modified")
            info["title_rows"].append({
                "row": i, "language": lang, "state": state,
                "value_preview": value[:160],
                "description_preview": description[:80],
            })
        if not info["title_rows"]:
            info["note"] = "Resource has no title row"
    except (ValueError, IndexError, KeyError, UnicodeError) as exc:
        info["error"] = f"{type(exc).__name__}: {exc}"
    return info


def candidates(game_root, save_root):
    # Probe template candidates and live Documents copies separately.
    # The audit's TSData/Res/UserData prefix for N001/N002 was only a staging alias.
    for story_id in EXPECTED:
        filename = f"{story_id}_Neighborhood.package"
        yield ("installation_template", story_id,
               game_root / "TSData/Res/UserData/Neighborhoods" / story_id / filename)
    if save_root is not None:
        for story_id in EXPECTED:
            filename = f"{story_id}_Neighborhood.package"
            yield ("documents_save", story_id, save_root / "Neighborhoods" / story_id / filename)


def main():
    ap = argparse.ArgumentParser(description="Read-only comparison of story-selector CTSS title candidates. NO SAVE MODIFICATIONS.")
    ap.add_argument("--game-root", type=Path, required=True)
    ap.add_argument("--save-root", type=Path, help="Active Documents game-data folder, for example .../Electronic Arts/The Sims Castaway Stories")
    ap.add_argument("--report", type=Path, default=ROOT/"work"/"selector_probe.json")
    args = ap.parse_args()
    game = args.game_root.resolve()
    if not (game/"TSData").is_dir():
        ap.error(f"Not a game installation containing TSData: {game}")
    save = args.save_root.resolve() if args.save_root else None
    maps = json.loads((RUNTIME/"translations"/"ui.json").read_text(encoding="utf-8"))
    probes = [inspect_package(path, story, source, maps)
              for source, story, path in candidates(game, save)]
    report = {
        "purpose": "static selector file/source preflight, not an in-game read path trace",
        "read_path_observed": False,
        "live_game_tested": False,
        "number_of_candidates": len(probes),
        "found_files": sum(item["exists"] for item in probes),
        "found_title_resources": sum(item["resource_found"] for item in probes),
        "important": ("If a Documents title is already Vietnamese while game UI remains English, "
                      "the UI likely reads another source or language fallback. Inspect process access and precedence."),
        "candidates": probes,
    }
    report_path = args.report.resolve()
    if report_path == game or game in report_path.parents or (
        save is not None and (report_path == save or save in report_path.parents)
    ):
        ap.error("Report output must be outside installation and save folders")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({
        "found_files": report["found_files"],
        "title_resources": report["found_title_resources"],
        "report": str(report_path),
        "game_read_path_verified": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
