# v0.8 TEST readiness and localization exit criteria

**Status:** Not ready to release (2026-10-09). This document describes verifiable milestones; it is NOT a declaration that the game is already localized. Use the latest Source Audit run and `RUNTIME_HANDOFF_2026-10-09.md` for numbers.

## Key distinction: inherited review rows are not untranslated game text

The large inherited pool includes base Sims 2 and expansion STR#/TTAs/CTSS rows, duplicates, internal helpers, obsolete objects and potentially player-visible text. **Do not treat its raw count as the number of sentences still needing translation or as a percent-complete measure.** Conversely do not exclude the whole pool: some inherited rows are active in Castaway.

A row is safely dealt with only if its full package/resource key, ordinal, language, original English text and metadata are preserved and there is one of:
1. a category mapping applied through an exact `row_scope_overrides_NN.json` with player-facing evidence;
2. a context-specific `row_translation_overrides_NN.json`;
3. an evidence-backed `row_review_decisions_NN.json` retain/exclude decision;
4. a documented and validated automatic internal/opaque/unused exclusion.

**Risk-first review (do not spend equal effort on every inherited row):**
- **P0:** explicitly Castaway-owned story/dialog/interaction/menu, goals/rewards/Wants, neighborhood and selector text, and any English still reproduced in a player's test.
- **P1:** mixed shared-controller rows, frequently used base interactions, household/survival catalog items, social/family memories where the game actually exposes the memory UI.
- **P2:** unowned/legacy furniture, distant base-game catalog, expansions lacking Castaway reachability. Review exact evidence and record scoped decisions; no blind translation or blanket exclusion.
- **Internal:** documented debug/deleted/hidden helpers can be excluded only under existing validated rules.

The useful progress metric is **P0/P1 verified coverage and runtime tests**, alongside raw inherited counts. A falling inherited number by itself is not proof the game looks translated.

## Gate A — reproducible source coverage

- [ ] Latest Source Audit passes, with `untranslated_or_review_candidate_rows=0` and `parse_errors=0`.
- [ ] Review every high-confidence Castaway/active-base P0/P1 interaction and catalog family using fresh broad triage; retain a residual list with reasons for doubtful rows.
- [ ] All source rows preserve placeholders, line endings and metadata; non-Castaway expansion-only text is not globally translated.
- [ ] Confirm item name + catalog description + menu choice + hint/notification consistency for common survival interactions; audit normal story/career/reward/Wants separately.

## Gate B — selector/runtime ownership (currently open)

- [ ] Determine the **actual game-process data path**, fallback and resource precedence for the new-game/story selector (`Shipwrecked and Single`, `Wanmami Island`).
- [ ] Confirm the selector translations appear *in-game* after an exact-resource patch; source-only patching of N001/N002 save copies has not established this.
- [ ] Do not distribute Ron's Documents save packages wholesale. If a user-owned save must be patched, back it up and modify only specifically validated text resources.

## Gate C — package writer and safe combined installer (currently open)

- [ ] Re-stage Ron's previously supplied original runtime package baselines with their recorded hashes, including **both different Wants.package** files.
- [ ] Rerun current-source `check_runtime_packages.py` QA and compare exact package/resource/row metadata.
- [ ] Verify compression/DBPF parsing (especially 24-byte `objects.package` entries), untouched resource hashes, round-trip, idempotence, token preservation and font rendering.
- [ ] Build one **consolidated reversible v0.8 TEST** installer containing compatible core Text + runtime text + existing working font; provide backup/restore and validate before public release. Do not commit commercial game package content to the source repo.

## Gate D — focused in-game test (currently open)

- [ ] Test a clean starting story, new-game/story selector, chapter progression and household/story dialogs.
- [ ] Test pie-menu/object labels, item descriptions, crafting/barter/storage/cooking/fishing, goals/Wants, skills/career, rewards, basic social and family notifications.
- [ ] Confirm default English is absent from **verified Castaway-facing** screens at the tested locations. Log any exceptions with screenshot + exact resource ID and fix the owner family, not just the screenshot string.
- [ ] Confirm no crashes, corrupted saves, broken placeholders, regressions or missing Vietnamese glyphs.

## Two separate definitions of done

**v0.8 TEST is ready** only when A/B/C pass and a reversible tester package is built. D still requires Ron's actual Windows-game test; therefore a package labelled TEST is not a completed localization.

**Full release is done** only after D passes, known reproducible player-facing English regressions are resolved (or explicitly documented and accepted), and any remaining inherited pool is classified enough that the user-facing completeness claim has evidence. Do not demand an arbitrary zero for every legacy debug/expansion string while ignoring the actual in-game UI.

### Blocking facts at this checkpoint

- A source-only PASS is available, but does not verify the package writer on the current source.
- The selector read path is **unverified**.
- The last recorded structural writer QA verified **7,502 candidate rows**, and is **stale** relative to the current Source Audit.
- There is **no consolidated v0.8 TEST payload** and no completed fresh Windows in-game validation.
- Continue triage without asking Ron to re-upload already provided packages for source-only decisions; if a new isolated working environment has no baseline package bytes for the actual builder, identify their exact paths and only then request the minimum necessary files.

### Next work order

1. High-confidence P0/P1 inherited menus, Castway-owned item/catalog/rewards and mixed social/survival resources.
2. Selector source/precedence diagnosis and reproducible instrumented test.
3. Restore current baseline package QA and build an incremental reversible consolidated test.
4. Ron's game test, fixes by resource family, then final release audit.
