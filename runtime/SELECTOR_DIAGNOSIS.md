# Story selector: evidence and unresolved runtime source

**Not fixed or runtime-verified by this checkpoint.** Ron tested the N001/N002 installation-template patch in v0.7b and still saw English.

The uploaded templates contain CTSS strings for `Shipwrecked and Single` and `Wanmami Island`. Their exact keys, rows and source descriptions are in `catalog.json.gz`; `translations/ui.json` now includes translations for the two titles and descriptions.

Local portable-launcher source inspected in this session:

- `deliverables/Castaway-Portable-Builder/Source/Launcher.cs` writes a launcher log saying saves use the normal Documents location. The launcher changes installation configuration, not save locations.
- `deliverables/Castaway-Startup-Check/Check-Castaway.ps1` uses `[Environment]::GetFolderPath('MyDocuments')` and `Electronic Arts\The Sims Castaway Stories\Logs`.

This supports, but **does not prove**, the hypothesis that the selector reads a copied neighborhood from the active user-data directory instead of the installation template. A Documents folder can be redirected (e.g. OneDrive); do not hard-code the physical Windows profile path.

Required next evidence: identify the game process's actual N001/N002 read path, or inspect active neighborhood files plus game/user-data path information. Likely files to compare are:

- `<Windows Documents>\Electronic Arts\The Sims Castaway Stories\Neighborhoods\N001\N001_Neighborhood.package`
- `<Windows Documents>\Electronic Arts\The Sims Castaway Stories\Neighborhoods\N002\N002_Neighborhood.package`

If that source is confirmed, patch only the targeted text resources of those existing files, with per-file backup, source checks and restore support. Never replace the whole active save with `TSData\Res\UserData` templates. Preserve all families, relationships, lots, history and unrelated resource bytes.
