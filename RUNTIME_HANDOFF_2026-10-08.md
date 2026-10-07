# Runtime handoff — 2026-10-08

This file supersedes all older numerical checkpoints in `CONTINUE_WITH_MODEL.md`, `NEXT_SESSION_PROMPT.md`, `RUNTIME_HANDOFF_2026-10-07.md`, `runtime/coverage.json`, and `runtime/package_qa.json` whenever those numbers disagree with the latest Source Audit.

## Authoritative checkpoint

Continue from commit `8f3d10c2ba3cdc7d43b4dcc344a2e0a54362fd65` or newer.

Latest verified Source Audit:
- workflow run **344**
- commit **8f3d10c**
- conclusion **PASS**
- **6,278 translation map entries**
- **1,339 context-specific exact-row translations**
- **13,604 effective candidate rows**
- **0 untranslated/review candidate rows**
- **22,498 unresolved inherited review rows**
- **1,349 automatic inherited-row exclusions**
- **0 parse errors**
- selector runtime source: **NOT VERIFIED**
- v0.8 TEST: **NOT RELEASED**
- current in-game validation: **NOT COMPLETED**

Current translated category highlights from Source Audit:
- catalog: **1,046 translated**, 7 excluded, 5 retained
- menu: **1,472 translated**, 6 excluded
- dialog: **357 translated**
- story: **1,552 translated**
- tutorial: **150 translated**
- UI: **235 translated**, 15 excluded
- wants: **518 translated**
- neighborhood: 39 translated, 66 retained
- character: 21 translated, 21 retained
- object: 36 translated
- text: 1 translated

## Important stale generated files

`runtime/coverage.json` is an older generated snapshot (5,325 entries / 9,085 candidates / 30,862 unresolved) and is NOT authoritative for current source state.

`runtime/package_qa.json` is also stale. Its last structurally verified package snapshot covers **7,502 candidate rows**. Current Source Audit has **13,604 candidate rows**, so package-writer QA is behind by **6,102 rows**.

Do not rewrite package-QA provenance by hand. Before any release claim, rerun the package writer/round-trip/idempotence/unrelated-resource checks against Ron's already supplied baseline packages.

## Exact-row architecture — do not flatten it

Current numbered exact layers are continuous:
- `runtime/row_scope_overrides_02.json` through `row_scope_overrides_65.json`
- `runtime/row_translation_overrides_01.json` through `row_translation_overrides_49.json`
- `runtime/row_review_decisions_01.json` through `row_review_decisions_107.json`

Use them correctly:
1. **row_scope_overrides** = promote an inherited exact row when it can reuse an approved category English→Vietnamese mapping.
2. **row_translation_overrides** = exact row needs its own Vietnamese value because the English label is ambiguous/collides by context.
3. **row_review_decisions** = exact retain/exclude decision after evidence review.
4. **auto_review_decision()** = only evidence-backed automatic internal/debug/unused/opaque exclusions. Exact decisions override automatic heuristics.

Never replace old shards wholesale. Add a new numbered shard or update a shard only when fixing a proven fingerprint error.

## Major completed work since the previous handoff

The sweep moved from a mostly Cast-tagged queue into broad inherited runtime review using `triage_review_queue.py --include-unowned`.

Completed or substantially expanded player-facing coverage includes:
- Castaway invisible-marker Get In / Teleport Here and the formerly ambiguous bush **Use → Đi vệ sinh** exact row
- clothing browse/try/buy/dress-for-work
- plant/garden actions
- stereo controls/stations
- lesson/join actions
- social/toddler interactions and teaching/show-off menus
- mapped global social and mapped animal interactions
- Chapter 1 exact story title and telescope interaction
- phone services, Sim-to-Sim phone, phonebook, pizza delivery, emergency calls and transport dialogs
- computer/email interactions and dialogs
- travel restrictions and base travel actions
- Social Bunny name/actions
- conversation topic menus
- Wants/aspiration notifications
- mailbox interactions/text
- reading/bookcase interactions
- mirror interactions/charisma notification
- alarm clock, outdoor trash, food-social and base garden actions
- recliner, Toasting Set, bars
- friendship and adoption notifications
- police car actions/service dialogs
- toddler/TV/bookcase/coordinate interactions
- motive desperation labels
- fireplace interactions + base catalog copy
- shower catalog copy
- television catalog/channels and repeated base TV interactions
- base living-chair catalog
- base mirror catalog

Recent evidence-backed classifications/exclusions include broad University, Nightlife, Pets, Seasons and Open for Business residue; phone expansion branches; owned-car/Nightlife travel; retail/debug helpers; Garden Club residue; Pets mammal cage; Seasons juice interactions; police-car University/helper residue; television tuning/mirror helpers; expansion transport; expansion television/fireplace/living-chair/mirror catalog content.

Do not redo these families from scratch. Read recent commit history when in doubt.

## Broad inherited triage is now the main path

`src/builder/triage_review_queue.py` has an `--include-unowned` mode. The Source Audit workflow prints the top unowned inherited groups plus targeted large families.

Use the latest successful Source Audit log, not the old compressed-snapshot ranking, to choose the next batch.

### Current high-value unresolved families near the top of run 344

These are examples of the current queue, not blanket decisions:

- two ownerless global social TTAs blocks: **Anti-Gossip / Muscle In / Act... / Help Me** — still mixed/unclear; do not mass-promote or mass-exclude
- **Contained Pet - Bird Cage** EP6 rows — Castaway has its own bird-cage/orangutan/bird gameplay, so compare against already selected Castaway resources before deciding
- **Block - Stacking** configure/set-mode rows marked EP2 — likely expansion/configuration residue, but decide exact rows
- **Accessory - Juice Cup** fruit-juice skill notifications marked EP7 — likely Seasons residue
- **LawnTacky** mixes base Kick/Stand Up/View/Talk/Play with EP7 Steal Back Statue — split exact rows
- **Booth - Clothing - Designer** mixes Try On/WooHoo/Try For Baby — verify actual Castaway reachability
- video-game/perfume retail racks mix base Browse/Buy with OFB Restock/Set Price — split exact rows
- seat/dining TTAs with Sit/Veg Out/Nod Off/Find a Snack — likely reusable base actions; prefer approved-map promotion where evidence supports it
- **Wish / Drink / Fall From Heaven** marked EP7 — likely expansion residue
- **Trash Compactor** base Dispose/Take Out Trash/Repair — likely player-facing base gameplay
- emergency phone variants — player-facing base dialogs should be translated unless a row is explicitly expansion-only
- Gossip / Bad Mouth social resources — split base vs expansion rows
- **Bills** mixes base overdue/no-funds dialogs with Nightlife dining-bill text
- pet Bark/Growl/Hiss resources — Pets-tagged but Castaway animal systems exist; do not mass-exclude solely from EP6 metadata
- **Espresso Machine** / Espresso cart — base interactions may be reused; barista career/store variants need context
- low-relationship incoming phone calls — base player-facing dialog
- career cars/vehicles — base Get In/Get Out/Go to Work/Drive may be reused; expansion-specific vehicle branches must be split
- puddles/plants/roaches — generally base player-facing actions mixed with helper/debug or expansion variants; review exact rows

## Translation style still applies

- Dialogue/narration: natural Vietnamese, playful/Gen-Z only where character/context supports it; narrator uses neutral **mình**.
- UI/system/tutorial: short, clear, not meme-heavy.
- Preserve every token and placeholder exactly: `%s`, `%d`, `$Object`, `$NameLocal:n`, `$Local:n`, `$$Local:n`, `$$Money:n:n`, line breaks, etc.
- Keep names/proper nouns unless an approved translation already exists.
- Never add a global mapping for an ambiguous generic English word when an exact-row translation is safer.
- Do not infer player-facing status from an object name alone.

## Story selector remains unresolved

The uploaded N001/N002 packages are from Ron's Documents saves. Do NOT ask for them again and never ship entire saves as templates.

The selector strings exist in those files, but the game-process read path / fallback / precedence has not been verified. Prior in-game testing still showed English. Continue investigation separately from the inherited text sweep; do not claim the selector is fixed from source patching alone.

## Release gates still open

Do **not** publish or label a completed v0.8 TEST until all of these are satisfied:
1. inherited review queue is substantially resolved / completion criterion is explicitly defined
2. selector runtime source/read path is verified
3. package QA is rerun against current source (currently 7,502 verified vs 13,604 candidate rows)
4. consolidated safe installer/build is produced
5. Ron performs focused in-game verification

Ron does not need to upload more files merely to continue source triage.

## Paste-ready next-session instruction

Continue the Vietnamese localization of **The Sims Castaway Stories PC** in GitHub repo `RVTGMzz/TSCTW-VH`.

Read `RUNTIME_HANDOFF_2026-10-08.md` FIRST, then `CONTINUE_WITH_MODEL.md`, `RUNTIME_AUDIT.md`, `TRANSLATION_STYLE.md`, `BUILD.md`, `runtime/README.md`, and the latest Source Audit logs.

Continue from commit `8f3d10c` or newer. Latest authoritative Source Audit run 344 PASS: **6,278 translation entries, 1,339 exact-row translations, 13,604 candidates, 0 missing/review candidates, 22,498 unresolved inherited rows, 1,349 auto-exclusions, 0 parse errors**. Older `runtime/coverage.json` and `runtime/package_qa.json` numerical totals are stale.

Continue the **broad inherited sweep**, not screenshot-by-screenshot. Use `triage_review_queue.py --include-unowned` and exact resource evidence. Preserve all placeholders. Split mixed resources by exact row. Reuse approved mappings through new `row_scope_overrides_NN.json`; use `row_translation_overrides_NN.json` for context-specific collisions; use `row_review_decisions_NN.json` only for evidence-backed retain/exclude decisions. Do not mass-exclude EP6 animal rows merely because they are tagged Pets, because Castaway has animal gameplay.

Do not redo completed phone/computer/travel/mailbox/social/reading/mirror/alarm/trash/recliner/toasting/bar/police/toddler/TV/fireplace/shower/living-chair/mirror-catalog sweeps. Start from the latest run-344 inherited queue. Package QA is stale at 7,502 verified versus 13,604 current candidate rows (gap 6,102). Selector source remains unverified. No completed v0.8 TEST has been released. Do not ask Ron to re-upload previously supplied packages just to continue source triage.
