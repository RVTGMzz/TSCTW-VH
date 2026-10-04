# Build notes

The repository is source-only. The scripts were originally run from a local `work/` directory, where their inputs and translation maps sit beside the Python files.

For a local build:

1. Clone this repository.
2. Create a local `work/` directory. Copy `src/builder/*.py` and `translations/*.tsv` / `translations/*.json` into `work/`.
3. Put user-owned extracted packages in `work/text/Text/`. For `build_v06.py`, use Text v0.5 `Options.package` and `UIText.package`, plus original `Live.package`, `Neighborhood.package`, and `Tutorial.package`.
4. Run `python build_v06.py` from the copied `work/` directory. It writes the package payload and manifest to a sibling `Castaway-Text-v06/` directory.

For font rebuilds, the original font assets belong under `work/fonts/Fonts/`; install `fontTools` locally first.

The full extraction `english.json` and all binary source/output assets are intentionally omitted. Do not commit game packages, fonts copied from the game, or patched payloads. Structural checks do not replace testing in the original Windows game.
