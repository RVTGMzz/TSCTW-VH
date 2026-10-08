> **UPDATE 2026-10-09 — authoritative source checkpoint:** run **414 PASS**, commit **`92dbfaf6b5b3633e874ce4b0d401d2e4b3b2a97c`** or newer. **7,038 translation-map entries**, **2,047 exact-row translations**, **14,582 effective candidate rows**, **0 untranslated/review candidate rows**, **20,296 unresolved inherited rows**, **1,349 automatic exclusions**, **0 parse errors**. This update supersedes all previous counts in this handoff and older docs. Source Audit: https://github.com/RVTGMzz/TSCTW-VH/actions/runs/37827502082. **v0.8 TEST is NOT released.** The story selector runtime source is not verified and package QA is stale at 7,502 rows (current verification gap **7,080**).

## Continuation after run 407 — verified run 414

The 2026-10-09 continuation made **400 exact inherited-row decisions** since run 407: **268 source-level exact translations** and **132 evidence-backed exclusions**. Unresolved inherited decreased **20,696 → 20,296** while all candidate translation gates remained clean.

- `runtime/row_translation_overrides_69.json`: 20 exact base Sim-memory CTSS rows (5 families): moving out, Logic maximum, death, refused engagement, embarrassment at party.
- `runtime/row_translation_overrides_70.json`: 100 exact CTSS rows (25 family/romance/skill/cooking/friendship/fight resources), including English/UK English variants.
- `runtime/row_review_decisions_141.json`: 132 exact inherited CTSS rows from 38 legacy resources excluded because they explicitly refer to Sims 2 University college/scholarships, Sims 2 werewolf/PlantSim transformations, or Seasons Garden Club. This is NOT a blanket exclusion of Castaway animal/garden rows.
- `runtime/row_translation_overrides_71.json`: 80 exact memory rows (20 resources): skill, grandchild, first kiss, promotion, fire, marriage, ghosts, toilet training, love, demotion and adoption. Gender-neutral first-person narration maintained, including a corrected original romance phrase.
- `runtime/row_translation_overrides_72.json`: 68 exact memory rows (17 resources): achievement, cheating, make-out, skills, engagement, infant development, fighting and dating rejection.
- `.github/workflows/source-audit.yml`: added `--include-unowned --object-contains "Memory -" --groups 280 --samples 8` to expose the inherited memory family queue reproducibly.

All exact rows carry original package, full DBPF key, row ordinal, language, English text and description; translated rows preserve $-tokens and original line-break controls. This is **source QA** only: full runtime player visibility and release-readiness have NOT been verified. Latest green Source Audit at run 414 confirms the source-coverage and parse gates.

### Next checkpoint instructions

Read this update FIRST, then the remainder of this handoff and `TRANSLATION_STYLE.md`/`BUILD.md`/`runtime/README.md`. Continue from commit `92dbfaf6b` or newer. Next shard numbers after inspection: **row_translation_overrides_73.json**, **row_review_decisions_142.json**, **row_scope_overrides_82.json**. Use latest source audit triage with --include-unowned, split mixed inherited families per exact row and evidence. Prioritize actual Castaway UI/catalog/interaction reachability and untouched base memory families; do not retranslate the newly handled groups. Do not promote all legacy catalog or expansion-specific objects. Keep the selector diagnosis and package QA as separate release gates. Do not distribute original game packages or Documents saves.

---

# Runtime handoff — 2026-10-09

This supersedes numeric checkpoints in `RUNTIME_HANDOFF_2026-10-08.md`, `NEXT_SESSION_PROMPT.md`, `CONTINUE_WITH_MODEL.md`, `RUNTIME_AUDIT.md`, `runtime/README.md` and the older generated JSON snapshots. The source-only repository is NOT a v0.8 release.

## Authoritative checkpoint
- GitHub commit: **`4c4d30efac9e4a606e2c4c709d44b1e3de308879`** (`4c4d30e`) or newer.
- Source Audit: **run 407**, **PASS** (commit `4c4d30e`).
- **6,770 translation-map entries** (source audit's aggregate count, including exact-row translations).
- **1,779 context-specific exact-row translations**.
- **14,314 effective candidate rows**.
- **0 untranslated/review candidate rows**.
- **20,696 unresolved inherited review rows**.
- **1,349 automatic inherited-row exclusions**.
- **0 parse errors**.
- Selector runtime source: **NOT VERIFIED**; v0.8 TEST: **NOT RELEASED**; in-game validation: **NOT COMPLETED**.

Source Audit link: https://github.com/RVTGMzz/TSCTW-VH/actions/runs/37826382774

## Completed in the 2026-10-09 continuation

Starting from run 404 / commit `ef595a9` (6,634 mappings, 1,643 exact-row translations, 14,164 candidates, 20,846 unresolved inherited):
1. `runtime/row_translation_overrides_67.json` — **76 exact CTSS memory rows** (19 source groups): friendships, romance/rejection, runaway/return, birth, early development, bonus, burned food, moving in and rescue from death. Gender-neutral first-person Vietnamese and exact `$Subject` preservation.
2. `runtime/row_scope_overrides_81.json` — **14 exact TTAs rows** (7 owned modular-stair groups): only `Go Upstairs`/`Go Downstairs`, using approved `menu.json` translations. Mood `Walk...` variants remain unresolved.
3. `runtime/row_translation_overrides_68.json` — **60 exact CTSS memory rows** (15 source groups): losing best friend, bad growing up, learning to talk, inheritance, enemies, quitting job, retirement, three best friends, overachievement, marriage rejection and breakup.

Total **150 inherited rows** moved into candidate translations; run 407 source QA **PASS**, with 0 missing/review candidates and 0 parse errors. These exact translations are source-level coverage, **not proof of in-game reachability**.

## Continue with the broad inherited sweep
- Use `src/builder/triage_review_queue.py --include-unowned` and the latest Source Audit log (run 407), not an old handoff ranking.
- Split mixed resources by exact row and evidence. `row_scope_overrides_NN.json` reuses approved mapping; `row_translation_overrides_NN.json` provides unique context-dependent Vietnamese; `row_review_decisions_NN.json` makes evidence-backed retain/exclude choices.
- New next-shard numbers: scope **82** (scope 81 exists); translation **69** (68 exists); review **141** (140 exists). Always inspect the actual repo tree again before creating a shard.
- Do not blindly classify Castaway-relevant animal, family, social, career or food rows as expansion residue just because they inherit Sims 2 tags. Conversely do not mass-promote all base catalog, memory or expansion leftovers as proven runtime.
- Avoid redoing completed phone, mailbox, computer, emergency calls, fishing/food stock, bills, furniture/menu and earlier catalog sweeps. Refer to the existing 2026-10-08 handoff for completed families.
- Preserve all DBPF key, ordinal, language, English bytes, description metadata and placeholders (including `%s`, `%d`, `$Subject`, `$Object`, `$Local:n`). Narration is neutral `mình`; system UI stays clear, dialogue conversational.
- Repo remains **source-only**. Never commit original or patched commercial game packages or Documents save files.

## Release gates still open
1. **20,696 inherited rows still need review**; avoid claiming this is a full game sweep.
2. Selector `Shipwrecked and Single / Wanmami Island` game-process read path/precedence is **not verified**. N001/N002 supplied previously are Documents saves, not redistributable templates.
3. `runtime/package_qa.json` is stale: last structurally verified snapshot has **7,502 candidate rows**, versus **14,314 now** (difference **6,812**). Do not hand-edit provenance; rerun writer, round-trip, idempotence and unrelated-resource checks with the previously supplied baseline packages when accessible.
4. Consolidated v0.8 installer/font/runtime patch and focused actual in-game validation remain outstanding. No v0.8 TEST release is complete.

## Next-session instruction
Continue translating `RVTGMzz/TSCTW-VH` from `4c4d30e` or newer. Read this file first, then the older handoff, `TRANSLATION_STYLE.md`, `BUILD.md`, `runtime/README.md`, and latest Source Audit logs. Continue the **broad inherited exact-resource sweep**, keep verified metadata and every placeholder intact, commit new shards and verify CI. Do not request Ron to upload the already-supplied packages merely to proceed with source triage. Do not call v0.8 TEST finished.
