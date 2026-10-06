# Runtime sweep — v0.8 work in progress

This is a reproducible **partial translation checkpoint**, not a release or a claim that the game is fully localized. See `coverage.json` for exact counts and the remaining work. No v0.8 TEST payload has been released from this checkpoint.

## Source and scope

- `inventory.json`: staged package paths, SHA-256, resource/index counts, parse results and explicitly preserved legacy technical tables.
- `catalog.json.gz`: English candidate rows, including exact package, full DBPF key, row ordinal, language, metadata and selection reason.
- `review_queue.json.gz`: untagged/legacy text whose player visibility is unresolved. It is **not** treated as translated or safe to discard.
- `translations/*.json`: exact source-to-Vietnamese maps by category. New runtime maps supplement existing `translations/extra*.json`; the original v0.6 history and v0.7 sources are unchanged.
- `scope_decisions.json`: explicit decisions to retain proper names, exclude diagnostic dumps/asset identifiers, or defer suspicious menu entries for review.
- `remaining.json.gz`: unresolved candidate rows, generated from the maps and decisions.
- `coverage.json`: source QA and coverage; source validation passing does not mean coverage is complete or the game has been tested.

Gzip files contain UTF-8 JSON using escaped characters to preserve invalid legacy bytes losslessly. Decompress with Python's `gzip` module. The gzip timestamp is fixed to zero for reproducible artifacts.

## Uploaded neighborhood provenance

Ron confirmed the supplied N001/N002 files came from Documents saves. See `input_provenance.json`. Their paths under `TSData/Res/UserData` in this audit are staging aliases, not their real origin. Never package these whole saves as installation-template replacements. No re-upload is needed.

## Reproduce

Use Python 3.11+ and stage the packages at the exact paths listed in `inventory.json` under `work/input/`. The duplicated uploads are **Text/Wants.package** (4,486,248 bytes) and **Wants/Wants.package** (633,090 bytes); do not interchange them.

```sh
python src/builder/audit_runtime.py --input work/input --output runtime
python src/builder/validate_runtime.py --write
python src/builder/check_runtime_packages.py
```

The auditor writes human-readable local JSON as well as the committed gzip snapshots. Source-only QA needs no game packages:

```sh
python src/builder/validate_runtime.py
python src/builder/build_v07.py --audit-only
```

`validate_runtime.py --require-complete` intentionally fails while unresolved work remains. Do not remove this gate to label a partial sweep complete.

`check_runtime_packages.py` creates **development QA output only**, outside the baseline inputs. It checks input hashes, exact row/metadata identity, full chained placeholders, control-character sequence, compression round trips, table padding, 20/24-byte indices, DIR sizes, preservation of unrelated resources and byte-identical results on a second application. It does not combine core Text patches, fonts or an installer and is not a v0.8 release builder.

## Outstanding

1. Translate remaining catalog and story/career/dialog rows; reconcile item labels across hints, menus and catalog.
2. Review inherited/untagged resources with object and behavior context. Cast metadata is a useful seed, not proof of runtime reachability. Default exclusions outside confirmed scope are heuristic, not a claim that all untagged STR# text is internal.
3. Verify the selector's actual runtime source. See `SELECTOR_DIAGNOSIS.md`. Do not overwrite a user's active neighborhood save with an installation template.
4. Build one consolidated v0.8 TEST only after source coverage, scope review, package QA and font/installer QA. In-game testing remains Ron's verification; do not claim it has happened here.

## Reviewed inherited interactions

`row_scope_overrides*.json` currently contain 1,182 exact row guards: 802 menu, 293 dialog, 77 catalog, nine story and one tutorial row. Each row is guarded by full DBPF key, row ordinal, language, original value and original description. The loader validates every shard together and rejects cross-shard duplicates, stale rows or mismatched source metadata. Object names from same-group OBJD resources document evidence where available. This remains a curated list of evidence-backed player-facing rows, not a rule that every CS or EP string must be translated.

Run `python src/builder/review_runtime_context.py` after completing extraction to attach same-group object names and Cast text ownership to the remaining queue. `review_context.json.gz` and its summary are evidence for further review; they do not claim runtime reachability and do not silently remove rows from coverage. Do not run dependent validation while extraction is still writing its snapshots.

Current selected source includes 1,551 story/career/runtime-story values, 987 menu values, 945 catalog values, 36 dialog values and 126 tutorial values. Effective candidate coverage is 7,850 rows with zero missing/review candidate decisions and zero parser errors. The effective inherited review queue is 37,337 rows; the compressed snapshots remain at the preceding extraction until package bytes are available again. Story-selector runtime source is unverified. No consolidated v0.8 TEST release has been produced.


### Sweep batch: Castaway fire-pit cooking menu (2026-10-05)

Reviewed the exact TTAs rows attached to the Castaway Outdoor Fire Pit and Fire Pit Survival objects. Added all nine player-facing cooking choices found in those menus, including nested Grill/Pot paths and Server Dinner. The source records each DBPF key, row ordinal, language, original string/description, and same-group object names in `row_scope_overrides.json`; Vietnamese values are in `translations/menu.json`. Debug-only entries in the same menus (such as `rr`, state setters, or tester choices) were not promoted.

Reproducible result: 18 exact rows promoted; 9 new menu values; candidate snapshot 7,196 rows with zero missing/review; inherited queue decreased from 38,009 to 37,991. Parser reports zero errors. `validate_runtime.py --write` and `build_v07.py --audit-only` pass. Development package QA re-applies the selected translations twice to the supplied baseline packages, verifies idempotence and preserves untouched resources; it does not claim in-game verification or release readiness.


### Sweep batch: Castaway catalog descriptions (2026-10-05)

Reviewed two exact CTSS families attached to Castaway objects: the tropical food stand and the talking-bird companion. Promoted six English/UK-English rows with owning-object evidence. Three new catalog strings were translated; existing Surfer Paul title and description entries were retained as-is (merge/superset). Candidate snapshot is now 7,202 rows with zero missing/review; catalog has 903 translated values, seven exclusions and five intentionally retained names. The inherited queue is 37,985 rows and is still not fully classified.


### Sweep batch: portal dialogue, bird interactions and popups (2026-10-05)

Reviewed player-visible STR#/TTAs families using exact object and dialog context: visitor departure lines documented as notices the player sees (11 values × 10 portal resources = 220 rows); beach-combing, talking-bird and animal-fight popups (20 rows); orangutan choice dialogs and interaction labels (28 rows); bookcase/easel/fetch/pet/trash hints (30 rows); and bird-cage pie menu actions (22 rows). The developer-only ASPYR nanny diagnostic, bird stock/debug controls, unrelated book resources and unverified expansion entries were not promoted.

Current totals: 834 exact inherited row guards (558 menu, 270 dialog, six catalog); 938 translated menu values; 35 dialog values; 903 catalog values; 7,502 candidate rows with no missing/review rows; 37,685 inherited rows still awaiting broader classification. Placeholder/order and line-break validation passes; source-level package QA passes with idempotent writes and unrelated-resource preservation. No in-game test or v0.8 archive is claimed.


### Sweep batch: early-story runtime rows and raft/door interactions (2026-10-06)

Promoted 14 exact inherited rows with strong Castaway ownership evidence: early chapter monologue/tutorial text in Ch01/Ch02 controllers, `Build Onto` on the Castaway raft, and both UK-English `Leave World` variants on the House of Tuzu door. Nine new translation-map entries were added; existing `Leave World` mappings were reused. Candidate coverage is now 7,516 rows with zero missing/review decisions; the inherited queue is 37,671 rows. Derived catalog/review/context snapshots were regenerated in-repo. Package-writer QA is intentionally marked stale until `check_runtime_packages.py` can be rerun against the user-owned package bytes; no new in-game result is claimed.


### Sweep batch: CS - Urn - Ghost death/grave text (2026-10-06)

Promoted four exact player-facing rows on the already-audited Castaway urn/ghost object: the death-dialog title `Rest In Peace`, `Here Lies %s`, the death/grave description, and the UK-English `Rest In Piece` variant. Debug death-type setters and ghost test actions in the same resource remain outside scope. One dialog mapping and three catalog mappings were added.

Source-only QA now computes **effective records** by merging exact pending `row_scope_overrides.json` rows with the committed catalog/review snapshots in memory. This means a small evidence-backed batch no longer requires hand-editing large gzip snapshots; a future full package extraction will materialize the same overrides into fresh snapshots. `check_runtime_packages.py` uses the same effective record set. Effective coverage: 7,520 candidate rows, 0 missing/review candidate rows, 37,667 inherited review rows, 4,404 translation-map entries. Package-writer QA remains stale until the user-owned baseline package bytes are available to rerun it.


### Sweep batch: Castaway changing-table interactions (2026-10-06)

Promoted 22 exact English/UK-English rows (11 interaction labels) on `CS - Changing Table - Castaway` and its lead/variant owners. Ten new Vietnamese menu mappings were added; `Put $Object Down` reused the existing mapping. The batch covers changing diapers, dressing a baby/toddler in everyday clothes or PJs, putting the child down, and planning toddler everyday/PJ outfits. Four Outerwear labels × two languages remain under inherited review because they are EP7-specific and Castaway runtime reachability is not established.

Effective coverage is now 7,542 candidate rows with zero missing/review candidate decisions, 37,645 inherited review rows and 4,414 translation-map entries. Package-writer QA remains stale pending access to the user-owned baseline package bytes.


### Sweep batch: Lomi Lomi Salmon + Outdoor Hut toilet (2026-10-06)

Promoted 35 exact inherited menu rows with Castaway owner evidence. The Lomi Lomi Salmon resource contributes 25 English/UK-English rows for eating, serving, getting and resuming the salmon dish; nine new Vietnamese menu mappings were added and the existing `Resume Cooking` mapping was reused. The Castaway Outdoor Hut toilet contributes 10 core interactions (`Flush`, `Clean`, `Unclog`, `Play With`, `Flush Down`) reusing existing translations.

Pet-training rows such as `Train to Pee` / `Be Trained to Pee`, `Throw Up Test`, and developer `*Set ... State` rows remain under inherited review. Effective source totals are 4,423 translation-map entries, 7,577 candidate rows, zero missing/review candidate decisions and 37,610 inherited review rows. Package-writer QA remains stale pending a rerun against the user-owned baseline package bytes; no in-game result is claimed.


### Sweep batch: Birthday Cake + toddler furniture catalog (2026-10-06)

Promoted 18 exact rows from clearly owned Castaway resources: four player-facing Birthday Cake TTAs rows, four Birthday Cake catalog rows, two Birthday Cake Box title rows, four Potty Chair catalog rows and four Plastic High Chair catalog rows. Added two menu mappings and seven catalog mappings. The catalog copy keeps product names such as Tinkle Trainer 6000 and Kinder Koddler while localizing the surrounding Sims-style humor.

Developer/internal candidates remain under review, including Birthday Cake Age Trans/Dynamic Menu rows, the cake-box placeholder description marked `not needed?`, and the high chair's bare-metadata TTAs. Effective source totals: 4,432 mappings, 7,595 candidate rows, zero missing/review candidate decisions and 37,592 inherited review rows. Package-writer QA remains stale pending the baseline package-byte rerun; no in-game result is claimed.


### Sweep batch: item catalog + object interactions (2026-10-06)

Two evidence-backed batches added 55 exact inherited rows. The first promoted 30 catalog rows covering Market Basket, Xylophone, Changing Table, Diary, Teddy Bear, Book, serving/meal dishes, Baby Bottle, Birthday Cake Slice and the Peg Box toy; 17 new Vietnamese catalog mappings were added. The second promoted 25 rows: Toy Box and Diaper catalog text, Recycle on Book/Diary, Veg Out on Castaway seating, and View on the Warning Totem/Hatchet/Staff of Tuzu/Pickaxe pickup objects. `View` reused the existing `Ngắm` mapping.

Obviously mismatched or weak inherited text remains unresolved instead of being translated by association, including `Cup O' Ramen` under Tropical Ribs/Pineapple Surprise, pet/plantbaby expansion residue, maintenance/state/debug actions, and generic Repair rows without equivalent player-facing evidence. Effective totals: 4,454 mappings, 7,650 candidate rows, zero missing/review candidate decisions, 37,537 inherited review rows, zero parse errors. Package-writer QA remains stale pending the user-owned baseline package-byte rerun; no in-game result is claimed.


### Sweep batch: Shaman/crafting + duplicate light menu (2026-10-06)

Promoted 22 exact Shaman/crafting rows whose Vietnamese labels already existed in the menu map: five Shaman potion Browse pairs plus functional Make One/Make Many/Practice/Scrap/Continue/Sell actions on the Castaway electronic crafting station and toy bench. Dynamic Menu remains under review.

The exact-value trace for the reported `Examine` / `Use` leftovers found two very different inherited cases. `Examine` belongs to a duplicate light/torch TTAs variant in the same group as explicit `Cast Menu COM` rows, so 11 matching player-facing rows in that variant were promoted and reuse existing translations, including `Examine → Xem xét`. `Use` belongs to a bush interaction ("outgoing & lazy male sims... low bladder") in a group that also collides with Castaway bird-cage/pet text; without object ownership or matching Cast menu evidence it remains review-only rather than being patched blindly.

Effective totals: 4,454 mappings, 7,683 candidate rows, zero missing/review candidate decisions, 37,504 inherited review rows and zero parse errors. Package-writer QA remains stale pending the baseline package-byte rerun; no in-game result is claimed.


### Consolidated inherited sweep checkpoint (2026-10-06)

The effective validator checkpoint has been synchronized after several parallel evidence-backed batches: Ignis Ex Machina/weather reward actions, remaining clear Castaway object actions, Autumn Leaf Pile, Native Pet Shelter, the second Sanitation Station changing-table menu, and a household/catalog pass covering Average Paws Bedding, Mixing Bowl, Ingredients Tray, Kinder Kontainer crib, Baking Pan and Frying Pan.

The exact `Examine` residue reported earlier is already covered by the duplicate Castaway light/torch menu override and maps to `Xem xét`. The remaining exact `Use` inherited row is specifically a base-game bush urination interaction and still has no reliable Castaway owner; it remains review-only rather than being translated blindly.

Authoritative effective totals from Source Audit: 4,486 translation-map entries, 7,790 candidate rows, zero missing/review candidate decisions, 37,397 inherited review rows and zero parser errors. Menu has 986 translated values and catalog has 941. Package-writer QA remains stale, selector runtime source remains unverified, and no v0.8 TEST release is claimed.


### Sweep batch: restaurant stove + island pinball catalog (2026-10-06)

Promoted eight exact CTSS rows for two clear player-facing objects: the Castaway restaurant stove and the island-themed career pinball machine. Four new catalog mappings were added, preserving product names while localizing the Sims-style descriptions. Source Audit passes at 4,490 mappings, 7,798 effective candidate rows, zero missing/review candidate decisions, 37,389 inherited review rows and zero parser errors. Catalog now contains 945 translated values.


### Sweep batch: object interactions + House of Tuzu dialogs (2026-10-06)

Promoted 52 exact inherited rows after source-evidence review. The first 26-row batch covers clear player-facing interactions on Castaway peg boxes, xylophones, the diary, five living chairs, two clothing racks and easel paintings; it adds the new mapping `Prepare for Hanging → Chuẩn bị để treo`. Rows explicitly marked debug, test-only or not actually shown in game were left in review.

A second 26-row batch promotes 22 House of Tuzu leaving-neighbor dialog rows (11 mapped messages across both English-language variants) plus four Grand Piano `Join`/`Dance` action rows. The ASPYR nanny developer note and piano `Break`/`Untune` debug-like rows remain unpromoted. Legacy Windows-1252 metadata is preserved byte-for-byte in exact guards rather than normalized.

Exact row guards can now be split across `runtime/row_scope_overrides*.json` shards; audit, validator and triage merge the shards and still reject duplicates or stale source metadata. Source Audit passes at 4,491 mappings, 7,850 effective candidate rows, zero missing/review candidate decisions, 37,337 inherited review rows and zero parser errors. Package-writer QA is still stale at 7,502 verified candidates and must be rerun before release; no in-game test is claimed.


### Sweep checkpoint: inherited classification + tutorial recovery (2026-10-06)

The inherited sweep now distinguishes exact translated/promoted rows from exact reviewed exclusions. New `row_review_decisions*.json` shards classify source-guarded debug/internal/stale rows without treating a whole CS-named object as unused. Two conservative classification batches removed 426 obvious inherited rows, followed by 45 Tutorial Controller identifier/helper rows and 18 Seasons/University residue rows. Exact review decisions now total 489 rows.

Player-facing work in the same sweep added the Tiki counter locale repair, Castaway bird-cage `Stock`, two Toy Box catalog variants, Penguin Party warning, Grand Piano catalog text, Pyramid Door `Close Door`, Volcano Juice tap action, Native High Chair `Feed Toddler`, Elixir of Life, additional seating/fridge interactions, and 16 previously unselected `Cast Old FIN` tutorial strings. The tutorial batch preserves original CR/LF signatures and Source Audit passes.

Authoritative effective totals: **4,519 translation mappings, 7,894 candidate rows, zero missing/review candidate rows, 36,804 inherited review rows, zero parse errors**. Current translated category totals include menu 990, catalog 953, dialog 37 and tutorial 142. Exact translation guards total **1,226** = 816 menu + 297 dialog + 87 catalog + nine story + 17 tutorial. Exact inherited review decisions total **489**. The compressed extraction snapshots still predate 378 pending exact promotions; source-only validation is authoritative until the next package extraction.

Package-writer QA remains stale at 7,502 verified candidates versus 7,894 current (392-row gap). Story-selector runtime source remains unverified. No new in-game test or v0.8 TEST release is claimed.


### Exact-row translation support + duplicated food stands (2026-10-06)

Added `row_translation_overrides*.json` for context-specific translations when the same inherited English placeholder appears on different Castaway objects. Exact-row translations are guarded by package, DBPF key, row ordinal, language, original value and description; they also carry their own Vietnamese replacement. Validator checks placeholders, line-break signatures and metadata; triage hides selected rows; full extraction promotes them; package QA prefers the exact replacement before falling back to category maps.

First use: the Mahi-Mahi, Tropical Ribs and Pineapple Surprise food-stand resources all inherited the same `Cup O' Ramen` title/description. Six exact catalog rows now receive distinct context-correct Vietnamese names and descriptions without creating a dangerous global `Cup O' Ramen` mapping. Source Audit passes at **4,525 translation entries** (4,519 normal map entries + six exact-row translations), **7,900 effective candidate rows**, zero missing/review candidate rows, **36,798 inherited review rows**, and zero parse errors. Catalog translated source values: 955.

Exact generic translation guards remain 1,226 rows (816 menu, 297 dialog, 87 catalog, 9 story, 17 tutorial); context-specific row translations add six more promoted rows; exact inherited review decisions total 489. Package QA remains stale at 7,502 verified candidates versus 7,900 current. No in-game/v0.8 completion claim.


## 2026-10-07 session handoff

Source-work checkpoint before this documentation sync is commit `942c0d362ac9abc5a68651e7820391de539cefaa` (Source Audit PASS). Trust current Source Audit over all older handwritten totals:

- **5,325 translation entries**, including **591 context-specific exact-row translations**
- **9,085 effective candidate rows**
- **0 missing/review candidate rows**
- **30,862 unresolved inherited review rows**
- **1,349 automatic inherited-row exclusions**
- **0 parse errors**
- category highlights: menu **1,206**, dialog **186**, catalog **955**, tutorial **150**, story **1,552**, object **35**, UI **235**, wants **518**
- selector runtime source still unverified
- package QA still stale at **7,502 verified vs 9,085 current** (gap **1,583**)
- no completed v0.8 TEST release and no new in-game completion claim

The runtime architecture now has four complementary layers. `row_scope_overrides*.json` promotes exact inherited rows that can reuse ordinary category maps. `row_translation_overrides*.json` carries context-specific Vietnamese replacements for exact rows when one inherited English value is ambiguous/stale by object context. `row_review_decisions*.json` records exact manual exclude/retain decisions. Finally, `auto_review_decision()` in `validate_runtime.py` automatically excludes evidence-backed families only when no explicit exact decision overrides them: leading-`*` hidden/helper interactions, metadata marked deleted/not needed/not used/unused, `DEBUG`/`DBG`-prefixed values, and opaque IDs matching eight-hex/`bebe...`/`ecdb...` forms. Accepted exact promotions currently contain zero leading-star, deleted-metadata, opaque-ID or DEBUG/DBG rows; do not weaken these rules without a proven runtime exception.

Large completed sweeps after the older handoff include Castaway phone services/adoption/nanny + House/Birthday/Wedding/Anniversary party flow, human aging/birthday notifications, illness/pregnancy runtime text, household move/inheritance flow, global social interactions, tutorial-controller retained text, story-controller template classification, Pets social/age/disease controller review, hidden-star/deleted/opaque/debug auto-classification, and explicit expansion-only global social residue. Do not redo these families from scratch.

For the next inherited pass, start from the latest Source Audit queue rather than old notes. Highest unresolved families currently include: remaining `CS - Not Allowed on Floor - Invisible Marker` rows such as Teleport/Get In/Catch Flies/Chase Flies/Watch/Play In/Eat/Pee On; ownerless/global social blocks with generic pet/social interactions; stereo/music and lesson menus; retail clothing/browse blocks; plant/garden interactions; pet-purchase dialogs; and a number of low-score controller/test objects. Mixed families must be split by exact evidence. Do not mass-promote because a resource has `CS -` in its owner name, and do not mass-exclude base-game-looking rows when Castaway Free Play demonstrably retains that system.

Physical compressed snapshots still predate most exact work: they represent **7,516 candidates**. Effective math is reconciled as 37,671 review-context rows minus 1,569 pending promotions minus 3,891 manual exact review decisions minus 1,349 automatic exclusions = **30,862 unresolved inherited rows**. Source-only validation is authoritative until the next full extraction/package QA.
