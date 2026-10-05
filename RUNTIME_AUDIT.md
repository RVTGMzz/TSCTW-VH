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
