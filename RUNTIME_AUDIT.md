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
