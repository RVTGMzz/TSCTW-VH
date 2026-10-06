# Runtime text audit checkpoint

Checkpoint: 2026-10-05.

Repo này vẫn là **source-only**. Không commit package game gốc hoặc package đã patch.

## Vì sao cần runtime sweep

Source sweep cũ chỉ phủ các Text package được catalog hóa. Test thật trong game cho thấy còn nhiều chuỗi người chơi nhìn thấy nằm ngoài nhóm đó, đặc biệt trong `TSData/Res/Objects/objects.package`, `TSData/Res/Text/Wants.package` và dữ liệu neighborhood.

Ron yêu cầu từ mốc này **không vá theo screenshot từng câu nữa**. Screenshot chỉ dùng làm bug report / xác nhận. Việc tiếp theo phải audit toàn bộ resource player-facing có liên quan rồi dịch theo cụm.

## Package Ron đã cung cấp ở phiên 2026-10-04/05

Các file sau đã được dùng để điều tra runtime nhưng **không nằm trong repo**:

- `TSData/Res/Objects/objects.package`
- `TSData/Res/Objects/Global/Behavior.package`
- `TSData/Res/ObjectScripts/ObjectScripts.package`
- `TSData/Res/Catalog/CANHObjects/catcanhobjects.bundle.package`
- `TSData/Res/Text/EPText.package`
- `TSData/Res/Text/Wants.package` (file lớn khoảng 4.4 MB)
- `TSData/Res/Wants/Goals.package`
- `TSData/Res/Wants/Wants.package`
- `TSData/Res/Wants/WantTrees.package`
- `TSData/Res/Wants/WantTuning.package`
- `TSData/Res/UserData/Neighborhoods/NeighborhoodManager.package`
- `TSData/Res/UserData/Neighborhoods/N001/N001_Neighborhood.package`
- `TSData/Res/UserData/Neighborhoods/N002/N002_Neighborhood.package`
- cùng 7 Text package v0.7 đã dùng trước đó.

Nếu model mới cần build/scan lại, hãy yêu cầu Ron upload đúng các package cần thiết; không yêu cầu cả game nếu chưa cần.

## DBPF/resource findings đã xác nhận

`objects.package` dùng index entry **24 byte**, khác parser Text cũ 20 byte. Với DBPF 24-byte, DIR records tương ứng 20 byte.

Các resource text quan trọng trong `objects.package`:

- `TTAs = 0x54544173`: pie menu / interaction labels.
- `CTSS = 0x43545353`: catalog title + description.
- `STR# = 0x53545223`: gameplay/UI/tutorial/runtime text.

Không được áp builder 20-byte cũ trực tiếp vào `objects.package` nếu chưa hỗ trợ index 24-byte.

## Các runtime string đã locate chắc chắn

### Pie menu / interaction trong objects.package

Đã locate và/hoặc từng patch thử:
- `Go Here → Đi tới đây`
- `Go Here! → Tới đây!`
- `Run Here → Chạy tới đây`
- `Skip Here → Nhảy chân sáo tới đây`
- `Watch Clouds → Ngắm mây`
- `Pick Up Hatchet → Nhặt rìu nhỏ`
- `Pick Up Machete → Nhặt dao phát`
- `Pick Up Coconut → Nhặt dừa`
- `Spear Fish → Đâm cá`
- `Pick Up Small Object → Nhặt vật nhỏ`
- `Dig in Sand → Đào cát`

Các string **vẫn còn thấy English sau test và phải được sweep theo resource/ngữ cảnh**, không chỉ thay global mù:
- `Examine`
- `Use`
- `Drink Coconut Juice`
- `Gather Coconuts`
- `Look Around`
- `Scan Horizon`
- `Monkey Around`

Ví dụ resource đã locate:
- group `0x7fe6afcd`, TTAs instance `0x1`: Drink Coconut Juice, Gather Coconuts, Look Around, Scan Horizon, Monkey Around.
- nhiều group khác có `Examine` và `Use`; phải phân biệt interaction thật với internal/test/expansion strings.

## Catalog / reward strings đã locate trong objects.package

### Hatchet
Hai CTSS group trùng nội dung, phải xử lý cả hai:
- `0x7f04cee9`
- `0x7f12081f`

English:
- `Hatchet`
- `With the hatchet, the days of lugging entire trees across the island are no longer! Use the hatchet to chop wood into smaller pieces that can easily be transported.`

Bản dịch seed:
- `Rìu nhỏ`
- `Có chiếc rìu nhỏ này rồi thì khỏi phải ì ạch vác nguyên cây khắp đảo nữa! Dùng nó chặt gỗ thành từng khúc nhỏ để mang đi cho nhẹ nhàng.`

### Don't Wear Short Shorts Loveseat
CTSS group `0x7f5f2e77`.

English:
- `"Don't Wear Short Shorts" Loveseat`
- mô tả dài về loveseat, tropical rustic và splinters.

Đã có bản dịch thử ở v0.7a. Đây chỉ là seed; runtime sweep phải xử lý toàn bộ catalog Castaway chứ không dừng ở item này.

### Concoction Junction
CTSS group `0x7f0b0b4b`, instance `0x7d0`.

English:
- `Concoction Junction`
- `Herbs! You know the effects and the correct doses of every individual species on the island, but now it's time to spread your wings. What does this one do if you add it to that other one? This is what you need in order to find out!`

Ảnh test mới nhất xác nhận vẫn còn English. Cần dịch cả title + description.

### Shell Lamp
CTSS group `0x7f5ecd66`, instance `0x7d0`.

English:
- `"Out a Home, But In a Hut" Shell Lamp`
- `Did you ever stop to think that the shells you find along the beach are more than just pretty? Sure, some poor beach dwelling creature may now be out of a home now. But at least you got a workable table lamp out of the deal.`

Ảnh test mới nhất xác nhận vẫn còn English.

## Wants / goal / aspiration findings

Trong `TSData/Res/Text/Wants.package` đã locate:
- generic `Get $ObjectType`
- `Get This`
- generic hint `To get this object, look in the Barter Catalog or the Build Catalog...`
- `an Easel` / `Easels`
- `Get the Hatchet`
- các Castaway hints như Examine Beached Debris, Examine the Idol, Use the Raft, Drink Coconut Juice...

Trong `Live.package` đã locate:
- `Aspiration Value → Điểm Khát vọng`.

Runtime sweep mới phải audit **toàn bộ Wants/Goals player-facing**, không chỉ những goal xuất hiện trong screenshot.

## Story selector / neighborhood

Trong các file Ron cung cấp đã locate chính xác:

`N001_Neighborhood.package`, CTSS instance 1:
- `Shipwrecked and Single`
- mô tả bắt đầu `Very little is known about this remote tropical paradise...`

`N002_Neighborhood.package`, CTSS instance 1:
- `Wanmami Island`
- mô tả bắt đầu `Wanmami Island is home to the local, the lost, and the long-range mariner...`

Một patch local v0.7b đã ghi Vietnamese vào các slot English/UK-English của hai CTSS này và structural validation PASS, **nhưng Ron cài xong vẫn thấy màn selector English**. Vì vậy chưa được coi là fix runtime.

Model tiếp theo phải tìm nguồn thực tế game đang đọc: kiểm duplicate copies, template/save/runtime neighborhood data, cache/copy path và các resource khác. Không kết luận chỉ dựa trên việc CTSS trong N001/N002 đã được patch.

## Runtime test đã có

Ron đã thực sự chạy game sau v0.7, v0.7a và v0.7b. Kết quả:
- nhiều UI Text cũ hiển thị tiếng Việt bình thường;
- runtime gameplay text ngoài catalog cũ vẫn còn English;
- v0.7a/v0.7b **không được xem là hoàn thiện**;
- screenshot mới nhất còn English ở story selector descriptions/titles, Career/Story reward tooltip, catalog items và pie-menu interactions.

## Quy tắc cho sweep tiếp theo

1. Không dịch tất cả English trong `objects.package` một cách mù quáng: package chứa rất nhiều internal/debug/base-game/expansion/test strings.
2. Ưu tiên player-facing resource: TTAs, CTSS và STR# thực sự dùng trong Castaway.
3. Dùng description/group/resource context để phân biệt Castaway với inherited Sims 2 junk.
4. Dịch theo **cụm resource**, không theo screenshot đơn lẻ.
5. Giữ placeholder, token, line break, metadata và ngôn ngữ khác.
6. Với title/description catalog: giữ tên riêng khi cần; văn phong mô tả có thể vui, tự nhiên, hơi Gen Z nhưng không lạm dụng.
7. UI/menu/hint: ngắn, rõ, tự nhiên.
8. Sau khi tạo runtime source, commit source mapping + audit report vào repo. Package game/payload test vẫn không commit.
9. Build một **bản tổng hợp mới** (ưu tiên v0.8 test) thay vì bắt Ron cài tiếp nhiều patch lẻ.
10. Chỉ gọi "hoàn tất" sau khi audit player-facing đã có report tái lập được và Ron test runtime.

## Cảnh báo về các số liệu tạm thời trong chat cũ

Trong phiên trước có các status message nói đã sweep một số lượng lớn resource. Những con số đó **không được persist thành audit/source file trong repo trước khi phiên bị ngắt**. Model tiếp theo không được coi chúng là bằng chứng hoàn tất. Hãy chạy lại audit, lưu kết quả và commit trước khi dùng số đếm để báo tiến độ.


## Reproducible checkpoint — 2026-10-05

The runtime extraction and current translations are now under `runtime/`. See `runtime/coverage.json` for actual coverage, `runtime/inventory.json` for input SHA-256 and parse results, and `runtime/remaining.json.gz` for unfinished candidate rows. The separate `runtime/review_queue.json.gz` preserves unresolved inherited/untagged text.

The new DBPF reader/writer supports both 20-byte and 24-byte indices and preserves table suffix bytes. Some Cast-tagged rows are diagnostics or internal identifiers: decisions are explicit in `runtime/scope_decisions.json`. A successful parser or token check is **not** a full sweep completion claim.

The selector's active source is still unverified; inspect `runtime/SELECTOR_DIAGNOSIS.md` before applying any save changes. Do not overwrite an existing neighborhood save with a template. There is no consolidated v0.8 TEST release yet.

### Correction — uploaded save origin (2026-10-05)

Ron confirmed the supplied N001/N002 packages are from Documents saves. Earlier template-origin assumptions are superseded. See `runtime/input_provenance.json` and `runtime/SELECTOR_DIAGNOSIS.md`. Do not request the same files again and do not ship them wholesale as installation templates.

### Runtime translation checkpoint — 2026-10-05 (continued)

Catalog maps now contain 904 entries (899 translated, five intentional unchanged names); six excluded and two review values remain in the tagged catalog audit. Story/career maps contain 974 of 1,544 selected unique values, including adult/junior/pet career descriptions, main plot, and female dialogue variants. Total runtime mapping entries: 3,675. Full scope is still incomplete: 570 story values and the untagged review queue remain; selector runtime source is unverified. See current coverage and package QA, including source hashes. No v0.8 TEST archive has been released. Supplied Documents saves must never be distributed wholesale.

### Latest checkpoint — complete selected story set + inherited menu expansion

Supersedes the preceding numerical checkpoint: runtime maps now contain 4,339 entries. All 1,544 selected story/career values have Vietnamese mappings, including chance-card choices/results and male/female variants. Menu coverage is 923 unique translated values after 510 exact inherited rows (167 labels) were promoted with OBJD ownership evidence; 93 new translations were added, and chess “Cheat” was resolved as “Chơi gian”. Catalog remains 899 translated + five retained map entries.

Source QA passes, but the full sweep remains INCOMPLETE: 17 candidate rows and 38,556 inherited rows remain under review. Continue with `runtime/row_scope_overrides.json`, `runtime/review_context.json.gz`, its summary, and remaining candidate snapshot. Run extraction to completion before generating dependent reports. Selector read-path verification and the consolidated safe installer are still outstanding. No v0.8 TEST archive exists.

### Candidate triage follow-up — 2026-10-05

The prior checkpoint's 17 candidate rows have now all been resolved by exact source context. Candidate coverage reports 0 untranslated/review rows across 7,178 rows: catalog 900 translated / 7 excluded / 5 retained; menu 923 translated / 6 excluded. `Basket Ghost` is translated as `Giỏ ma`; remaining entries were identified as developer placeholders, legacy action, developer age action, expansion potion, marker object or blank description and explicitly excluded in `scope_decisions.json`. This does not resolve the separate 38,556 inherited review rows. The selector runtime source remains unverified, and v0.8 TEST is not built. Ron has no new upload request at this stage; when a consolidated test package is ready, the remaining user step will be one install and focused in-game verification.

### Audit filter correction — 2026-10-05

A reproducible audit bug had treated descriptions containing `! Don't translate.` as inherited review instead of explicit exclusions because the filter only matched `Do not translate`. The filter now recognizes both wordings. Re-running source audit and context extraction reduced the inherited queue from 38,556 to 38,009 rows; the 547 removed rows have explicit non-translation metadata. Candidate coverage remains 0 missing/review rows, with zero package parse errors. User action: none yet; no package needs re-upload. When the consolidated v0.8 test package is ready, Ron's requested step is one installation followed by focused game verification.


## Sweep continuation — Castaway fire-pit cooking (2026-10-05)

Added the nine missing player-facing cooking options attached to the Castaway fire-pit menus, with 18 exact TTAs row overrides and object-name evidence. This extends the curated menu source rather than globally translating inherited labels. Debug/test rows in the same resources remain outside scope. The reproducible source and current package QA are in `runtime/row_scope_overrides.json`, `runtime/translations/menu.json`, `runtime/review_context.json.gz`, `runtime/coverage.json`, and `runtime/package_qa.json`. Candidate coverage is complete within the selected scope (7,196 rows, no missing/review); 37,991 inherited rows remain unresolved, so the overall runtime sweep and v0.8 release gate remain incomplete. In-game state is untested.


## Sweep continuation — Castaway catalog families (2026-10-05)

Added exact CTSS source rows for the Castaway tropical food stand and talking-bird companion. The owning-object names and original descriptions are preserved in `runtime/row_scope_overrides.json`; three absent Vietnamese values were added to `runtime/translations/catalog.json`. Two existing Surfer Paul translations were preserved unchanged. Candidate coverage now reports 7,202 rows, zero untranslated/review; the separate inherited queue has 37,985 rows. No in-game reachability is claimed for the untagged queue, and the overall sweep remains incomplete.


## Sweep continuation — portal, pet and gameplay dialogue (2026-10-05)

Added documented visitor-departure dialogue to 10 Castaway portal resources, plus object-scoped beach-combing and talking-bird popups, animal fight/fetch messages, bookcase/easel notices, and the talking-bird cage menu. `row_scope_overrides.json` now stores 834 exact source guards: 558 menu rows, 270 dialog rows and six catalog rows. Source maps contain 938 menu values, 35 dialog values and 903 catalog values. Candidate snapshot is 7,502 rows with zero missing/review decisions; 37,685 inherited rows remain unresolved. Parser errors are zero. The broad sweep and selector read-path are not complete; no v0.8 TEST or in-game result is claimed.


The latest disposable package QA passes: all 6,677 selected rows across the runtime packages were written, re-read and applied a second time without additional changes; unrelated resources were preserved. This is structural/source QA, not an in-game verification.


## Sweep continuation — early story runtime rows and raft/door interactions (2026-10-06)

Reviewed and promoted 14 exact inherited rows rather than broad resource families: seven unique early-story monologue values across Ch01/Ch02 controllers, one Live Mode tutorial instruction, `Build Onto` on the Castaway raft, and the two existing `Leave World` spellings on the House of Tuzu door. Debug TTAs, hex identifiers and unrelated inherited rows in the same resources remain outside selected scope. Runtime maps now contain 4,400 entries; candidate coverage is 7,516 rows with zero missing/review decisions; 37,671 inherited rows remain. Source snapshots and context summaries were regenerated. The previous disposable package QA predates this batch and is marked stale pending a package-byte rerun; selector read-path and in-game verification remain outstanding.


## Sweep continuation — CS - Urn - Ghost death/grave text (2026-10-06)

The Castaway urn/ghost object already had its functional menu actions audited. Four remaining player-facing rows in the same owner were promoted by exact package/key/ordinal/language/source/description guards: `Rest In Peace` (death dialog title), `Here Lies %s`, the deepest-sympathies death/grave description, and the UK-English `Rest In Piece` variant. Debug death-type setters, Create Ghost and related developer actions remain in inherited review.

To remove the brittle need to hand-regenerate large gzip snapshots for every small exact-row batch, source-only validation now merges pending exact overrides into the committed catalog/review snapshots in memory. Already-extracted overrides are cross-checked against catalog rows; pending overrides must match the review baseline exactly. Development package QA consumes the same effective record set. Effective source totals are 4,404 map entries, 7,520 selected candidate rows, zero missing/review candidate decisions and 37,667 inherited review rows. The physical compressed snapshots still represent the prior extraction until package bytes are available again; package QA remains stale and no new in-game result is claimed.


## Sweep continuation — Castaway changing-table interactions (2026-10-06)

Reviewed the dedicated `CS - Changing Table - Castaway` STR# interaction family. Promoted 22 exact source rows across English and UK English for diaper changes, everyday/PJ dressing, putting a baby/toddler down, and planning toddler everyday/PJ outfits. Ten new menu values were added; `Put $Object Down` reused the existing translation. The four Outerwear values in each language were deliberately not promoted: their EP7 provenance alone does not prove Castaway player reachability.

Effective source totals are 4,414 map entries, 7,542 candidate rows, zero missing/review candidate decisions and 37,645 inherited review rows. These 22 rows are pending exact overrides applied in memory by source-only QA until a full package extraction regenerates the compressed snapshots. Package QA remains stale and no in-game result is claimed.


## Sweep continuation — Lomi Lomi Salmon + Outdoor Hut toilet (2026-10-06)

Reviewed two clearly player-facing Castaway-owned resource families. `CS - Food - Lomi Lomi Salmon` contributes 25 exact STR# rows across English and UK English for meal, serving, get-food and resume-cooking menu paths; nine new menu mappings were added and `Resume Cooking` reused the existing translation. `CS - Toilet - Outdoor Hut` contributes 10 exact core TTAs rows for flush/clean/unclog/play/flush-down, all reusing existing menu mappings.

Expansion/debug residue in the same toilet resource remains unresolved rather than being mass-promoted: EP6 pet-training strings, `Throw Up Test`, and developer dirty/clogged state setters. Effective source totals: 4,423 map entries, 7,577 selected candidate rows, zero missing/review candidate decisions and 37,610 inherited review rows. Package QA still predates these exact-row batches and no in-game verification is claimed.


## Sweep continuation — Birthday Cake + toddler furniture catalog (2026-10-06)

Promoted 18 exact source rows with Castaway ownership and player-facing evidence: Birthday Cake interactions/catalog, Birthday Cake Box title, Potty Chair catalog and Plastic High Chair catalog. Added two menu and seven catalog mappings. Explicit developer/placeholder rows in the same resources were left unresolved rather than translated by association.

Effective totals are 4,432 translation-map entries, 7,595 candidate rows, zero missing/review candidate decisions and 37,592 inherited review rows. The package-writer QA snapshot still predates these exact-row promotions; no in-game verification is claimed.


## Sweep continuation — item catalog + object interactions (2026-10-06)

Added 55 exact source rows in two passes. Catalog coverage expanded across clearly owned Castaway objects (market basket, toys, changing table, diary/book, dishes, baby bottle, birthday-cake slice, toy box and diaper), while the interaction pass added Recycle, Veg Out and explicitly documented View rows on Castaway pickup/accessory objects. Mismatched inherited rows such as Cup O' Ramen under unrelated food-stand objects were deliberately left under review.

Current effective source totals are 4,454 translation-map entries, 7,650 candidate rows, 962 translated menu values, 933 translated catalog values, zero missing/review candidate decisions and 37,537 inherited review rows. Parser errors are zero. Package-writer QA still predates the latest exact-row promotions; selector runtime source and in-game verification remain outstanding.


## Sweep continuation — Shaman/crafting + exact Examine/Use trace (2026-10-06)

Promoted 22 exact Shaman/crafting interaction rows using existing Vietnamese mappings, then traced the two reported English leftovers by exact value. Examine resolves to a duplicate light/torch resource variant backed by same-group Cast Menu COM rows; 11 matching functional rows were promoted. Use resolves to an inherited bush urination interaction with no owner and a collided group containing unrelated pet-cage Cast text, so it remains unresolved pending stronger runtime ownership evidence.

Effective totals: 4,454 maps, 7,683 candidate rows, 0 missing/review candidate rows, 37,504 inherited review rows, 0 parse errors. Package-writer QA is still stale and selector runtime source remains unverified.


## Consolidated inherited checkpoint — 2026-10-06

Source Audit now reports 4,486 translation-map entries and 7,790 effective candidate rows with zero missing/review candidate decisions and zero parser errors. The inherited review queue is 37,397 rows. Current translated maps include 986 menu values and 941 catalog values. Exact override inventory is 1,122 guards: 772 menu, 271 dialog, 69 catalog, nine story and one tutorial.

Recent evidence-backed batches include weather/reward interactions, clear Castaway object actions, leaf-pile and native pet-shelter interactions, Sanitation Station changing-table rows, and visible household/catalog items (Average Paws Bedding, mixing/ingredient containers, crib, baking/frying pans). The exact Examine leftover is resolved through the duplicate Castaway light/torch resource; the lone Use leftover is an ownerless base-game bush urination interaction and remains review-only. Package-writer QA and selector runtime verification are still outstanding.


## Sweep continuation — restaurant stove + island pinball catalog (2026-10-06)

Added eight exact CTSS rows and four catalog mappings for the Castaway restaurant stove and Tribal Flame coconut pinball object. Source Audit passes: 4,490 mappings, 7,798 candidates, 0 missing/review candidate rows, 37,389 inherited review rows, 0 parse errors; catalog translated values: 945. Package-writer QA and selector runtime verification remain outstanding.


## Sweep continuation — inherited object interactions + House of Tuzu (2026-10-06)

Added 52 exact inherited row guards in two evidence-backed batches. Batch one promotes player-facing `Play`, `Read`, `Put Away`, `Veg Out`, `Ask To Join` and `Prepare for Hanging` interactions across clear Castaway-owned objects while intentionally retaining debug/test/not-visible rows. Batch two promotes 22 House of Tuzu leaving-neighbor dialog rows and four Grand Piano `Join`/`Dance` rows; the ASPYR nanny developer message and debug-like piano rows remain outside runtime translation scope.

The runtime guard loader now supports `row_scope_overrides*.json` shards so new exact reviews can be committed without rewriting the >1 MB base guard file. Duplicate/stale/mismatch checks remain global across all shards. Source Audit passes at 4,491 mappings, 7,850 candidates, zero missing/review candidate rows, 37,337 inherited review rows and zero parse errors. Exact guard inventory is 1,182 rows: 802 menu, 293 dialog, 77 catalog, nine story and one tutorial. Package QA is stale (7,502 verified versus 7,850 current); selector runtime source remains unverified and no in-game test is claimed.


## Inherited classification + Cast Old FIN tutorial pass (2026-10-06)

Added exact inherited-row classification infrastructure via `row_review_decisions*.json`. Decisions are guarded by package, DBPF key, row ordinal, language, source value and description; validator/triage/audit reject duplicates, overlaps with translation overrides, stale metadata or unsupported decisions. Current exact review-decision inventory is 489 excluded/retained rows.

This sweep also promoted player-facing Tiki counter/bird-cage/Toy Box/catalog/dialog/menu rows and recovered 16 `Cast Old FIN` Tutorial Controller strings while excluding 45 opaque tutorial IDs/helper actions. Seasons Outerwear and University College Research residues were explicitly excluded by exact row. Current Source Audit: 4,519 mappings, 7,894 effective candidates, zero missing/review candidate rows, 36,804 inherited review rows, zero parse errors. Exact translation guards: 1,226 (816 menu, 297 dialog, 87 catalog, 9 story, 17 tutorial). Package QA remains stale at 7,502 verified candidates; no in-game or v0.8 completion claim.


## Context-specific exact-row translation layer (2026-10-06)

Implemented `row_translation_overrides*.json` for inherited collisions where one English value needs different Vietnamese output by owning resource. The validator, audit extractor, triage queue and package writer all use the same exact identity guard. Package application gives exact-row Vietnamese text precedence over ordinary category maps while retaining idempotence/source-baseline checks.

Six catalog rows across Mahi-Mahi, Tropical Ribs and Pineapple Surprise are the first use case; all originally contain the stale `Cup O' Ramen` title/description but now receive object-specific Vietnamese text. Current Source Audit: 4,525 translation entries (six exact-row), 7,900 candidates, 0 missing/review candidate rows, 36,798 inherited review rows, 0 parse errors; catalog translated source values 955. Package QA is stale (7,502 verified vs 7,900 current), selector source remains unverified, no in-game completion claim.


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

Audit-specific note: recent triage tooling also supports value prefixes and regular-expression filters so large inherited families can be measured before any automatic rule is introduced. Keep the invariant that automatic exclusions are evidence-based, measurable, and overridable by an explicit exact row. The latest CI diagnostics report `PROMOTED_STAR_ROWS 0`, `PROMOTED_OPAQUE_ID_ROWS 0`, `PROMOTED_DELETED_META_ROWS 0`, and `PROMOTED_DEBUG_PREFIX_ROWS 0`; 64 accepted promotions currently have bang-only metadata, proving that bang-only metadata alone is **not** a safe exclusion rule.
