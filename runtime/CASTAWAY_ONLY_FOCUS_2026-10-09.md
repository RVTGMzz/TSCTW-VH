# Castaway-only completion focus — 2026-10-09

**Goal:** finish **The Sims Castaway Stories PC**, not simultaneously localize The Sims 2 or The Sims 2 Legacy Collection. Avoid opportunistic inherited-memory and expansion catalog translations until there is credible Castaway runtime reachability.

## Verified source checkpoint

[Source Audit run 425 PASS](https://github.com/RVTGMzz/TSCTW-VH/actions/runs/37833534628), at commit `8d57a401a675810b96d2da3b17182cb0484f6158`:

- **7,154** aggregated translation-map entries (**2,163** are exact-row translations).
- **14,719** candidate rows, **0** missing/review candidates, **0** parse errors.
- **20,095** inherited rows unresolved; raw count is NOT a count of visible English in Castaway.
- **1,349** automatic exclusions. No validated release or in-game test has been completed for the new source.
- Latest code and docs might be newer than run 425; verify fresh CI after each code change.

## Work completed in this focused pass

1. `runtime/row_scope_overrides_82.json` promotes **21 exact menu rows**: 18 `Sleep` interactions on living chairs and three `Call To Meal.../Guests|Household|Everyone` menu entries, using existing approved category maps. They are source-level candidates, not proven runtime reachability.
2. `runtime/translations/ui.json` changes `Reward` from the awkward `Ban thưởng` to **`Phần thưởng`**, consistent with reward catalog/tutorial.
3. `src/builder/trace_selector_sources.py` runs in Source Audit and records candidate DBPF keys for Shipwrecked/Wanmami. The report checks mappings from EACH source category, not just the UI map.
4. A focused triage is now automatic for `reward|prize|bonus|achievement`, `Examine|Use|Inspect` and survival verbs. This checks family/context instead of blindly translating every similar string.

## Story selector: direct static finding, runtime blocker remains

The read-only tracer found **17 matching audited rows**; **all 17 have source translations**, distributed as:

| Package inventory path | Matching rows | Role |
| --- | ---: | --- |
| `TSData/Res/Objects/objects.package` | 2 | Story ending dialog containing Shipwrecked title |
| `TSData/Res/UserData/Neighborhoods/N001/N001_Neighborhood.package` | 1 | Shipwrecked selector CTSS title |
| `TSData/Res/UserData/Neighborhoods/N002/N002_Neighborhood.package` | 14 | Wanmami selector title/description and person/lot biographies |

The N001 and N002 files came from Ron's **Documents save uploads**; their `TSData/Res/UserData` inventory prefix is a staging alias, **not evidence the installed game reads them there**. `NeighborhoodManager.package` is present in the audit inventory (842 bytes, five resources), but text searches did not locate a selector title in it; no active-game file access trace has been performed. **The selector bug is not a missing Vietnamese source string.** Do not fix by distributing or overwriting the entire N001/N002 save packages. Continue with `runtime/SELECTOR_DIAGNOSIS.md` and an isolated backed-up profile, exact-resource modifications only.

## Rewards, Examine, Use: scope evidence, not mass translation

The targeted `--include-unowned` triage of currently unresolved text shows:
- `Rewards`/prize/bonus hits overwhelmingly refer to The Sims 2 businesses (`Business Rewards`), debug cheat objects, Sims 2 Garden Club rewards, University scholarship, and generic Sims 2 Ingame Help. These are **not yet evidence** of untranslated active Castaway rewards UI.
- `Use` returns many Sims 2 pets/training/aspiration/perfume interactions. Numerous `Use Telescope` rows are on Castaway-named chapter controllers (e.g. `Ch07_G010`, `Ch15_G030`); story ownership is worth investigating, **but does not establish they appear as pie-menu text**. Keep suspicious controller/helper rows unresolved.
- `Fish Using...` comes from `Conversation Holder - Fishing` and `Effect Holder - Pond Fish`, with explicit Sims 2 **EP7** metadata. Do NOT automatically promote it merely because Castaway also has fishing.
- The `Examine` and `Use` mappings already exist in `runtime/translations/menu.json`; a player screenshot is useful for identifying actual missing keys, but do **not** patch only the photographed instance. Trace its exact resource owner and related family.

## No release claims: what unblocks v0.8 TEST

**P0 — next actions**:
1. Verify which package and language row controls the **new-game story selector**, using non-destructive trace/preference and a backup profile.
2. Recover the original game-owned package bytes from the previously supplied archive or the user's local backups **without putting them in GitHub**. Run current `check_runtime_packages.py` against all 13 audited inputs (original hashes), not the old 7,502-row QA baseline. Both similarly named Wants.package files must stay distinct.
3. Rebuild current core Text source with `build_v07.py --full` from an original baseline, then reconcile runtime changes with core Text, the already-working font, and a backup/restore installer. **Do not ship the N001/N002 user-save files**.
4. Test fresh Windows gameplay, story selector, item/rewards catalog, Examine/Use, inventory, wants and chapter progression. Fix exact affected resource families.
5. Ship v0.8 **TEST** only after structural package QA + installer safety gates; full release only after in-game QA. See `runtime/RELEASE_READINESS_V08.md`.

**Current dependency:** source-only GitHub access suffices for triage but not for re-running a binary patch writer or validating the installed Windows process. No original package bytes were found available as usable attachments in this session; no runtime package build has been claimed. Avoid requesting the same N001/N002 Documents save files again.
