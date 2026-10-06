# Checkpoint cho model tiếp theo

## Mục tiêu
Hoàn thiện Việt hóa The Sims Castaway Stories PC, build một bản test mới, rồi để Ron test thực tế. Giao tiếp bằng tiếng Việt thân mật, gọi là Ron; không hỏi lại thông tin đã có.

**Bắt buộc đọc `TRANSLATION_STYLE.md` và `BUILD.md` trước khi làm tiếp.**

## Trạng thái đã xác nhận
- Game portable: `G:\Castaway-Portable`.
- Font03 đã được Ron xác nhận chạy ổn; không thay font khi chỉ thêm chuỗi.
- v0.4 từng được Ron xác nhận hiển thị ổn.
- Bản đóng gói gần nhất là **Text v0.6**, 486 câu/nhãn duy nhất; **v0.6 chưa được Ron test trực tiếp đầy đủ**.
- Repo source-only, không chứa package game/payload đã vá.
- Nguồn dịch hiện tới **`extra44`**.
- **Audit thật đã PASS ngày 2026-10-04 trên GitHub Actions:** 1.774 mapping sau merge; 1.774/1.774 key có mặt trong package allowlist; 0 key thiếu khỏi catalog; 274 override có chủ đích.\n- Không dùng số merged mapping ghi tay nữa; chạy `python src/builder/build_v07.py --audit-only` để tái kiểm.

## Tiến độ dịch
- `extra07`: 127 UI/gameplay.
- `extra08`: 65 nhật ký/thoại instance 611–624.
- `extra09`: 56 nhật ký đầu game instance 601–610.
- `extra10`–`extra22`: Castaway UI, Build/Buy, Neighborhood, CAS, Story/Camera, aspiration/attraction và base-game UI dùng lại.
- `extra23`: 102 mapping shopping/cart + relationship UI/tooltip.
- `extra24`: 51 trường học, sở thích trò chuyện, baby popup.
- `extra25`: 97 Create-a-Sim core, 12 cung hoàng đạo + mô tả tính cách.
- `extra26`: 49 placement/update/loading UI.
- `extra27`: 13 moniker Khát vọng trẻ nhỏ.
- `extra28`: 19 interaction/sell/delete/capture messages.
- `extra29`: 13 CAS steps + neighborhood chooser/chuyển màn.
- `extra30`: 15 tinh chỉnh save/quit/tutorial/battery/lot prompts — tất cả là override của key đã có.
- `extra31`: 15 nhãn ngày/tuần — xác nhận giống bảng nền, không tăng unique.
- `extra32`: 37 Build/Buy tools + object stat labels/tooltips.
- `extra33`: 33 Castaway Needs + animal motives.
- `extra34`: 40 Simology/skills/career/status strings.
- `extra35`: 50 tên chương/section Castaway.
- `extra36`: 8 Player Profile + residential-lot warning.
- `extra37`: 3 Collection/Wanmami neighborhood descriptions.
- `extra38`: 7 Barter Mode + alternate skill tooltip resource IDs.
- `extra39`: 12 phone/party UI.
- `extra40`: 2 CAS name-entry labels.
- `extra41`: 104 shortcut/help/controls + Castaway misc UI.
- `extra42`: 29 control-panel/keybind labels.
- `extra43`: 10 Story/Neighborhood/core UI cleanup.
- `extra44`: 2 popup hệ thống cuối: application crash + missing required content.

### Hậu kiểm
`extra23`–`extra29`: 344 mapping, 0 duplicate nội bộ, 0 missing catalog, 0 placeholder mismatch, 0 line-break mismatch, 0 tooltip metadata mismatch, 0 Cyrillic stray.

## Audit theo package — source sweep hoàn tất
- **Options.package**: semantic audit sạch; phần còn tiếng Anh là 16/32-bit và tên thể loại nhạc, giữ nguyên.
- **Neighborhood.package**: gameplay UI sạch; phần còn lại là TheSims2.com/College không dùng hoặc key dùng chung đã dịch.
- **CAS.package**: gameplay UI sạch; phần còn lại là placeholder nội bộ hoặc key dùng chung đã dịch.
- **Build.package**: gameplay UI sạch; chỉ còn số giá, duplicate catalog bị đánh dấu xóa và developer placeholder.
- **Live.package**: gameplay Castaway sạch; phần còn lại là Cast Names, grades/day initials, PlantSim/University/Pets hoặc token nội bộ.
- **UIText.package**: phần hữu ích đã phủ; phần còn lại chủ yếu là dead Exchange/web, Sims 1 import, base-Sims2 neighborhood albums, expansion/Body Shop/legal/internal strings.

Không dịch các nhóm trên chỉ để tăng % dịch. Bước có giá trị tiếp theo là build/test thực tế rồi sửa theo những chuỗi thật sự còn lòi trong game.

## Mốc audit quan trọng
Các chuỗi **tag Castaway rõ ràng và thật sự cần dịch** đã được phủ. Cast-tagged còn tiếng Anh chủ yếu là:
- tên người bản địa / tên nhân vật,
- tên địa điểm,
- key bindings/phím tắt,
- tên nhạc,
- copyright/legal ngắn.

Không dịch các mục này chỉ để làm đẹp tỷ lệ.

Các nhóm cố ý bỏ qua:
- `eCAS.package`: Body Shop/CaSIE.
- `UIText2.package`: tên expansion cũ.
- `Installer.package`: chuỗi Seasons.
- `Credits.package`, phần lớn `MusicTitles.package`.
- University/Nightlife/OFB/Pets/Seasons thừa kế không dùng trong Castaway.
- online service/Exchange đã chết nếu không ảnh hưởng gameplay.

## Tone pass mới nhất
- Đã rà lại `extra08`–`extra09`: narrator dùng **“mình”** trung tính giới tính; các ngôi “ông/anh” còn lại đều gắn với NPC/đối tượng có giới rõ trong ngữ cảnh gốc.
- Thoại/nhật ký giữ chất nói tự nhiên, có thể dùng code-switching Gen Z vừa phải như “KPI”, “fail”, “offer”, “DIY” khi câu đùa hợp ngữ cảnh; không nhét vào cảnh nghiêm túc.
- `extra35` là batch cuối override tiêu đề chương; đã punch-up một số title: **“Tui Sẽ Sống Sót”**, **“Tới Công Chuyện Rồi”**, **“Con Mắt Ràng Buộc”**, **“Vẫn Chưa Tìm Được Thứ Mình Muốn”**.
- Khi chỉnh file batch đã tồn tại phải **merge/superset**, không replace mù. Đã khôi phục các key cũ từng bị rơi ở `extra26` và `extra28`.

## Tone
- Thoại/nhật ký tự nhiên, vui, lém lỉnh, Gen Z vừa phải.
- Không spam meme.
- Cảnh buồn/nguy hiểm/bệnh tật/cái chết/romance nghiêm túc phải hạ slang.
- Narrator dùng “mình” để trung tính giới tính.
- NPC có giới/ngôi xưng rõ thì dịch theo ngữ cảnh.
- UI/tutorial/cảnh báo: rõ, ngắn, chính xác.

## Quy tắc kỹ thuật
1. Giữ nguyên tên riêng và token `%s`, `%d`, `%D`, `$NeighborLocal:n`, `$Object`.
2. Tooltip có `|`: giữ nguyên metadata sau mô tả.
3. Giữ line break `\r` / `\n`.
4. Không dịch DO NOT TRANSLATE / expansion rác.
5. Không ghi “đã test trong game” nếu Ron chưa xác nhận.

## Builder mới — đã có
File: **`src/builder/build_v07.py`**.

Builder:
- đọc `translations/translations.json` + mọi `extra*.json` theo thứ tự số;
- batch sau được phép tinh chỉnh batch trước; override được ghi vào validation;
- derive target STR# từ catalog + exact English key;
- chỉ patch language ID 1/2 trong package allowlist;
- bảo toàn description, other languages, resource order/count, compression state và untouched bytes;
- kiểm DBPF/QFS round-trip, decompressed-size directory, placeholder, line break, tooltip metadata;
- giữ package-specific override `Neighborhood.package: Play → Chơi`;
- có `--audit-only` để merge/validate source không cần package game;
- audit-only kiểm placeholder, line break, tooltip metadata, catalog presence và ký tự Cyrillic lạc;
- output `work/build_v07/Payload/...`, `manifest.json`, `validation.json`.

`--audit-only` đã được thêm vào builder; source audit PASS trên CI ngày 2026-10-04. Builder đã tích hợp ánh xạ lịch sử v0.6 theo package/resource/language và đã qua kiểm tra cú pháp cùng logic tổng hợp. **Chưa chạy end-to-end với package thật** vì repo source-only.

### Package cần khi build incremental từ v0.6
Chỉ cần 7 file từ bản Ron đang dùng:
- `Options.package`
- `UIText.package`
- `Live.package`
- `Neighborhood.package`
- `Build.package`
- `CAS.package`
- `CAS_Shared.package`

Không cần cả thư mục game. `Tutorial.package` chỉ cần nếu chạy `--full` từ original baseline.

## Phát hiện khi build test v0.7 (2026-10-04)
- Ron đã cung cấp đủ 7 package incremental từ bản đang dùng; `UIText2.package` cũng được gửi để kiểm tra nhưng xác nhận chỉ chứa tên expansion legacy và **không patch**.
- Phát hiện lỗi incremental: builder cũ chỉ nhận diện English gốc nên bỏ sót các câu v0.6 cần override.
- Đã tích hợp fix vào `build_v07.py`: dùng `validation.json` v0.6 để ánh xạ `(package, instance, language, old_vi) → English source`; giá trị lịch sử mơ hồ bị bỏ qua nếu các ứng viên cho ra bản dịch cuối khác nhau.
- Đã kiểm tra cú pháp và chạy thử logic với trường hợp mơ hồ, duy nhất, English baseline và override riêng theo package. Chưa chạy end-to-end với package game trong lượt hiện tại.
- Bản test đã được tạo ở phiên chat dưới tên `TSCTW_VH_v0.7_TEST.zip`; chưa được đánh dấu runtime tested cho tới khi Ron chạy game.

## Runtime text discovery / v0.7a (2026-10-04)
- Từ ảnh test của Ron, phát hiện nhiều gameplay string không nằm trong 7 Text package cũ mà nằm ở `TSData/Res/Objects/objects.package` và `TSData/Res/Text/Wants.package`.
- `objects.package` dùng DBPF index entry **24 byte** (khác 20 byte của Text package), DIR entry tương ứng 20 byte. Các resource text quan trọng: `TTAs 0x54544173` (pie menu), `CTSS 0x43545353` (catalog title/description), và `STR# 0x53545223`.
- Đã build local **v0.7a runtime fix** từ chính package Ron cung cấp. Vá: `Go Here → Đi tới đây`, `Run Here → Chạy tới đây`, `Skip Here → Nhảy chân sáo tới đây`, `Watch Clouds → Ngắm mây`; Hatchet Story Reward + mô tả; item `"Don't Wear Short Shorts" Loveseat` + mô tả; Want `Get $ObjectType` + `an Easel`; `Aspiration Value → Điểm Khát vọng`.
- Hatchet có **hai CTSS group trùng nội dung** (`0x7f04cee9` và `0x7f12081f`); phải patch cả hai.
- Build v0.7a thay đổi 16+ resource trong `objects.package`, 3 resource trong Text `Wants.package`, và 1 resource trong `Live.package`; modified resources đều QFS round-trip / parse lại thành công.
- File test của phiên chat: `TSCTW_VH_v0.7a_RUNTIME_FIX.zip`. Chưa đánh dấu runtime tested cho tới khi Ron chạy game.
- **Story selector vẫn chưa fix:** `Shipwrecked and Single`, `Wanmami Island` và mô tả vẫn không nằm trong các package vừa scan. Bước kế tiếp cần Ron cung cấp `TSData/Res/UserData/Neighborhoods/N001/N001_Neighborhood.package` và `.../N002/N002_Neighborhood.package` để locate metadata runtime.

## Checkpoint mới nhất — runtime sweep toàn diện (2026-10-05)
Ron đã test thật v0.7, v0.7a và v0.7b trong game. Kết luận quan trọng: source sweep cũ **không đồng nghĩa runtime đã phủ hết**. Còn nhiều text player-facing nằm trong `objects.package`, Text `Wants.package`, neighborhood/runtime data.

Ảnh test mới nhất vẫn còn English ở:
- story selector: `Shipwrecked and Single`, `Wanmami Island` và mô tả;
- reward/item: `Concoction Junction` + mô tả;
- catalog: `"Out a Home, But In a Hut" Shell Lamp` + mô tả, và nhiều item khác;
- pie menu: `Examine`, `Use`, `Drink Coconut Juice`, `Monkey Around`, `Look Around`, `Scan Horizon`.

Ron yêu cầu rõ: **không tiếp tục vá từng screenshot**. Phải audit toàn bộ resource player-facing rồi dịch theo cụm, sau đó build một bản tổng hợp mới (ưu tiên v0.8 TEST).

Đã thêm:
- `RUNTIME_AUDIT.md`: checkpoint kỹ thuật/runtime đầy đủ;
- `runtime/known_runtime_strings.json`: seed resource/string đã locate;
- `NEXT_SESSION_PROMPT.md`: prompt copy/paste cho phiên model mới.

**Bắt buộc model tiếp theo đọc `RUNTIME_AUDIT.md` trước khi tiếp tục runtime translation.**

Lưu ý cực quan trọng: các status count lớn từng nói trong chat trước khi phiên bị ngắt không được persist thành audit/source file. Không coi các số đó là bằng chứng đã hoàn tất; phải rerun audit và commit report/source mới được báo tiến độ bằng số.

## Việc tiếp theo
1. Đọc `RUNTIME_AUDIT.md` và `runtime/known_runtime_strings.json`.
2. Nếu package không còn trong context, yêu cầu Ron upload đúng file cần scan; ưu tiên `objects.package`, Text `Wants.package`, N001/N002 và các package runtime liên quan.
3. Viết/hoàn thiện extractor có thể audit DBPF 20-byte và 24-byte, xuất catalog player-facing có package/type/group/instance/row/description.
4. Phân loại Castaway player-facing vs debug/internal/base-game/expansion; **không dịch mù** mọi English trong objects.package.
5. Dịch toàn diện theo cụm: TTAs interaction, CTSS catalog/reward, Wants/Goals/hints, neighborhood/story selector, STR# runtime UI/tutorial/story/dialog.
6. Persist bảng dịch runtime + audit report vào repo để tiến độ có thể tái lập.
7. Sửa story selector bằng cách tìm nguồn runtime thật sự game đang đọc; patch N001/N002 alone đã structural PASS nhưng Ron vẫn thấy English.
8. Build **một bản tổng hợp v0.8 TEST**, không tiếp tục bắt Ron cài nhiều hotfix lẻ.
9. Ron test runtime; chỉ sau đó mới cập nhật phần nào thực sự fixed.


## Runtime source checkpoint — 2026-10-05

Read `runtime/README.md`, `runtime/coverage.json` and `runtime/SELECTOR_DIAGNOSIS.md` next. The source now includes runtime mappings and reproducible DBPF audits. This is **partial work toward v0.8**, not a released v0.8 TEST. The core `translations/` history and root `validation.json` are retained.

Continue from `runtime/remaining.json.gz`, without redoing translated entries or replacing previous maps. Review the separate untagged queue. Source-only QA: `python src/builder/validate_runtime.py`; actual package QA: `python src/builder/check_runtime_packages.py` with baseline packages staged per inventory.

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


## Latest checkpoint — 2026-10-06 exact-row inherited promotion

Promoted 14 evidence-backed inherited rows from `objects.package`: early Ch01/Ch02 story/tutorial lines, Castaway raft `Build Onto`, and House of Tuzu `Leave World` variants. Added nine new translation-map entries. Current source: 4,400 map entries, 7,516 candidate rows, zero missing/review candidate rows, 37,671 inherited review rows, zero parse errors. `catalog.json.gz`, `review_queue.json.gz`, `review_context.json.gz`, coverage/inventory/summary and exact row guards are synchronized. Package QA from commit `64658bc` is now explicitly stale because the Library package uploads could not be materialized as raw bytes in this session; do not claim the new snapshot passed package-writer QA until `check_runtime_packages.py` is rerun. Do not ask Ron to re-upload the same packages merely because materialization failed. Story-selector runtime read-path is still unverified and no v0.8 TEST has been released.


## Latest checkpoint — 2026-10-06 urn/ghost + effective override QA

Added four exact player-facing rows on `CS - Urn - Ghost`: death dialog title, grave label/description and UK-English title variant. Debug/test rows in the same resource were deliberately left untouched. Added one dialog and three catalog mappings. Effective source totals: 4,404 translation-map entries, 7,520 candidate rows, zero missing/review candidate rows, 37,667 inherited review rows.

Architecture change: `validate_runtime.py` now merges exact pending `row_scope_overrides.json` rows into the committed snapshots in memory, and `check_runtime_packages.py` uses that effective record set. This avoids manually rewriting large gzip snapshots for every small batch while preserving exact baseline guards; the next full package extraction will materialize them normally. The gzip review/context snapshots therefore still reflect the preceding extraction and are explicitly documented as such. Package-writer QA remains stale pending access to the user-owned package bytes. Continue evidence-based inherited triage; selector runtime read-path and consolidated v0.8 TEST are still outstanding.


## Latest checkpoint — 2026-10-06 Castaway changing table

Promoted 22 exact STR# rows (English + UK English) from the dedicated `CS - Changing Table - Castaway` resource family: diaper, everyday/PJ dressing, put-down and toddler outfit-planning interactions. Added ten new menu mappings and reused the existing `Put $Object Down` translation. EP7 Outerwear rows remain review-only. Effective totals: 4,414 maps, 7,542 candidates, zero missing/review candidate rows, 37,645 inherited review rows. Package QA is still stale pending baseline package-byte access; do not claim an in-game fix yet.


## Latest checkpoint — 2026-10-06 Lomi Lomi Salmon + Outdoor Hut toilet

Promoted 35 exact menu rows: 25 from `CS - Food - Lomi Lomi Salmon` and 10 core interactions from `CS - Toilet - Outdoor Hut`. Added nine new salmon menu mappings; toilet labels and `Resume Cooking` reuse existing translations. Do not promote the toilet's EP6 pet-training, `Throw Up Test`, or developer `*Set ... State` rows without new reachability evidence. Effective totals: 4,423 maps, 7,577 candidates, zero missing/review candidate rows, 37,610 inherited review rows. Package-writer QA remains stale; selector runtime source remains unverified; no v0.8 TEST has been released.


## Latest checkpoint — 2026-10-06 Birthday Cake + toddler catalog

Promoted 18 exact rows: four Birthday Cake interactions, four Birthday Cake catalog rows, two Birthday Cake Box title rows, four Potty Chair catalog rows and four Plastic High Chair catalog rows. Added two menu mappings and seven catalog mappings. Leave Age Trans/Dynamic Menu, the cake-box `not needed?` placeholder description, and bare-metadata high-chair TTAs under review. Effective totals: 4,432 maps, 7,595 candidates, zero missing/review candidate rows, 37,592 inherited review rows. Package QA remains stale; selector source remains unverified; no v0.8 TEST has been released.


## Latest checkpoint — 2026-10-06 item catalog + object interactions

Promoted 55 exact inherited rows after the Birthday/Potty/High-Chair sweep. Batch A: 30 catalog rows / 17 new catalog mappings for Market Basket, Xylophone, Changing Table, Diary, Teddy Bear, Book, bowls/plate, Baby Bottle, Birthday Cake Slice and Peg Box. Batch B: 25 rows for Toy Box, Diaper, Recycle, Veg Out and documented View actions on pickup/accessory objects; two new menu and three new catalog mappings. Keep obviously mismatched inherited text (for example Cup O' Ramen under Tropical Ribs/Pineapple Surprise) and maintenance/debug/expansion residue under review.

Effective totals: 4,454 maps, 7,650 candidates, 0 missing/review candidate rows, 37,537 inherited review rows, 0 parse errors. Override guards: 982 total = 645 menu, 271 dialog, 56 catalog, 9 story, 1 tutorial. Package QA remains stale; selector runtime source remains unverified; no v0.8 TEST has been released.


## Latest checkpoint — 2026-10-06 Shaman/crafting + Examine trace

Added 22 exact rows for Shaman potion Browse interactions and two Castaway crafting stations, reusing existing menu translations. Exact-value tracing then resolved the reported Examine residue: 11 duplicate light/torch menu rows were promoted because their same-group Cast Menu COM counterparts are already selected. The remaining Use row is a base-game bush urination interaction in a collided instance with pet-cage Cast text and is intentionally left under review until ownership/reachability can be proven.

Effective totals: 4,454 mappings, 7,683 candidates, 0 missing/review candidate rows, 37,504 inherited review rows, 0 parse errors. Exact override guards: 1,015 total. Package QA remains stale; selector runtime source remains unverified; no v0.8 TEST has been released.


## Latest consolidated checkpoint — 2026-10-06

Trust Source Audit over older handwritten totals. Current effective source: 4,486 mappings, 7,790 candidate rows, 0 missing/review candidate rows, 37,397 inherited review rows, 0 parse errors; menu 986 translated, catalog 941 translated. Exact row guards: 1,122 total = 772 menu, 271 dialog, 69 catalog, 9 story, 1 tutorial. Physical compressed snapshots still predate 274 pending exact overrides.

Recent parallel batches already cover Ignis Ex Machina/weather reward actions, clear Castaway object interactions, Autumn Leaf Pile, Native Pet Shelter, the second Sanitation Station changing-table menu, and visible household catalog items. Do not redo them. Examine is already resolved by the duplicate light/torch menu override. The remaining Use row is a base-game bush urination interaction with no reliable Castaway ownership and must stay review-only unless new runtime evidence appears. Package QA remains stale (7,502 verified candidates vs 7,790 current); selector runtime source remains unverified; no v0.8 TEST has been released.


## Latest checkpoint — 2026-10-06 stove + pinball catalog

Added 8 exact CTSS rows / 4 catalog mappings for the Castaway restaurant stove and island-themed pinball object. Effective totals are now 4,490 maps, 7,798 candidates, 0 missing/review candidate rows, 37,389 inherited review rows, 0 parse errors; catalog 945 translated, menu 986 translated. Exact row guards: 1,130 total = 772 menu, 271 dialog, 77 catalog, 9 story, 1 tutorial. Package QA remains stale (7,502 verified vs 7,798 current); selector source remains unverified; no v0.8 TEST has been released.
