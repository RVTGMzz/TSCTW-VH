# Build notes

The build scripts use the local project layout from the working session. Keep this repository source-only. Place user-owned extracted inputs locally (ignored by Git):

- `work/text/Text/Options.package` and `UIText.package` from Text v0.5 for `build_v06.py`
- original `Live.package`, `Neighborhood.package`, and `Tutorial.package` in the same folder
- for font rebuilds, original game fonts under `work/fonts/Fonts/` and installed fontTools

The English string extraction `english.json` and all binary source/output assets are intentionally omitted. Do not commit game packages, fonts copied from the game, or patched payloads. The original Windows game is the runtime test; Linux-side structural checks do not replace it.
