# Story selector: source correction and remaining verification

Ron confirmed on 2026-10-05 that the already uploaded N001/N002 files came from the requested **Documents save location**. The earlier assumption that these were installation templates was wrong. Do not ask for these same files again.

See `input_provenance.json` for their exact SHA-256 and staged aliases. The `TSData/Res/UserData/...` paths in the extraction inventory are local staging aliases inherited from the earlier assumption; they are not evidence of the upload origin. These two files are active-save inputs and must never be shipped wholesale as installation templates or replacement saves.

The received files contain CTSS selector titles and descriptions. Their full resource keys and row positions are in `catalog.json.gz`, with translations in `translations/ui.json`. Ron's prior v0.7b test still showed English. Simply assuming a different Documents copy is no longer a sufficient explanation.

The actual game-process read path has not been observed. Continue investigating language fallback, alternate selector resources, package precedence and whether the earlier installed patch touched the same resources. The source confirmation is not an in-game fix verification.

Any eventual application to saves must alter only targeted text resources, keep full-key and original-row guards, create backups and preserve every unrelated resource byte. Never replace a neighborhood save with another complete package.


## Focused diagnosis — external evidence and controlled next test (2026-10-09)

**Evidence found (NOT runtime read-path proof):**
- [Mod The Sims: Castaway neighborhood templates](https://modthesims.info/download.php?p=5421838) identifies **both installation and Documents neighborhood trees**, and states that replacing `NeighborhoodManager.package` can change whether the game treats the story as unlocked. This supports testing the *manager/selector relationship*; it does **not** prove the visible title text resides in that file.
- [Mod The Sims: editing a Castaway neighborhood](https://modthesims.info/showthread.php?t=275135) identifies N001 as Shipwrecked and Single, N002 as Wanmami, and the neighborhood package under Documents; it does **not** prove which source the story-selector UI reads.
- These are community reports and potential leads, not in-game confirmation for Ron's portable setup.

**Controlled read-path matrix before any release:**
1. Inventory and SHA-256 the installation `TSData/Res/UserData/Neighborhoods/NeighborhoodManager.package` and the actual runtime Documents save tree `...`/`Neighborhoods/00000000/NeighborhoodManager.package`, **if present**; check the relevant N001/N002 install templates and Documents copies separately. Paths may differ with profiles/portable installations.
2. Read text resources from every discovered manager and N001/N002 package, record DBPF full key, instance/group, ordinal, language and exact English. Do not conflate same string bytes in different packages.
3. Compare actual title + description resources and language fallback precedence for `Shipwrecked and Single` and `Wanmami Island`. Patch only a **disposable backed-up profile** with unique temporary markers per candidate source, one location at a time, then run the game and note which marker appears. If only one language is patched, test both English and UK-English fallback paths.
4. Restore that profile from backup before distributing any mod. Never ship Ron's real user saves as a template.
5. If none of these resource candidates controls the UI, instrument the game-process file access (read-only tracing of path/handle access) and examine other UI string packages. A matching on-disk string is not enough to assert runtime ownership.

**Conclusion remains unchanged:** selector in-game source/read precedence **NOT VERIFIED**. This is a concrete investigation path, not a solved bug.
