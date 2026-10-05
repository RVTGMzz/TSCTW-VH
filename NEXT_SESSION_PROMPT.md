# Prompt mở phiên tiếp theo

Copy/paste nguyên khối dưới đây vào chat mới:

---

Tiếp tục dự án Việt hóa **The Sims Castaway Stories PC** trong repo:
https://github.com/RVTGMzz/TSCTW-VH

Hãy dùng GitHub connector đúng repo `RVTGMzz/TSCTW-VH`, đọc kỹ theo thứ tự:
1. `CONTINUE_WITH_MODEL.md`
2. `RUNTIME_AUDIT.md`
3. `TRANSLATION_STYLE.md`
4. `BUILD.md`
5. `README.md`
6. các bảng dịch hiện có trong `translations/`

Mục tiêu đợt này KHÔNG phải vá từng câu tôi chụp. Tôi muốn làm một **runtime sweep toàn diện** cho mọi text người chơi thật sự nhìn thấy trong Castaway: pie menu/interaction, tên+mô tả item, Story/Career/Aspiration rewards, Wants/Goals/hints, story/neighborhood metadata, gameplay popup/UI/tutorial và story/dialog runtime.

Quan trọng:
- Không dịch mù mọi English trong `objects.package` vì có rất nhiều debug/internal/expansion rác.
- Phải phân loại player-facing theo resource/context rồi dịch theo cụm.
- `objects.package` dùng DBPF index entry 24 byte; TTAs = 0x54544173, CTSS = 0x43545353, STR# = 0x53545223.
- Ron đã test v0.7/v0.7a/v0.7b trong game và vẫn còn English. Đọc `RUNTIME_AUDIT.md` để biết các string/resource đã locate.
- Story selector `Shipwrecked and Single / Wanmami Island` đã patch thử trong N001/N002 nhưng runtime vẫn hiện English, nên phải tìm nguồn game thật sự đang đọc.
- Đừng báo "đã sweep hết" nếu chưa có audit/source file tái lập được và commit lên repo.
- Khi sửa batch/source cũ phải merge/superset, không replace mù.
- Giữ placeholder/token/line break/metadata; narration dùng "mình" trung tính giới tính; thoại tự nhiên, Gen Z vừa phải; UI/hint rõ ngắn.
- Repo source-only: không commit package game gốc hoặc payload đã patch.

Nếu cần package để scan/build, nói chính xác file nào tôi phải upload. Tôi đã có sẵn các package runtime từng dùng: `objects.package`, Text `Wants.package`, `Goals.package`, Wants subsystem, `Behavior.package`, `ObjectScripts.package`, `EPText.package`, `N001_Neighborhood.package`, `N002_Neighborhood.package` và 7 Text package v0.7.

Ưu tiên của tôi: **dịch thật sự toàn bộ phần cần Việt hóa, đừng đợi tôi chụp gì rồi chỉ sửa cái đó**. Sau khi sweep + QA xong, hãy build một **bản tổng hợp v0.8 TEST** để tôi cài một lần và test tiếp.

---



## Checkpoint bổ sung 2026-10-05

Sau khi đọc các tài liệu trên, đọc `runtime/README.md`, `runtime/coverage.json`, `runtime/package_qa.json` và `runtime/SELECTOR_DIAGNOSIS.md`. Tiếp tục từ `runtime/remaining.json.gz` và queue chưa phân loại `runtime/review_queue.json.gz`. Đã có bản dịch runtime theo nhóm, không làm lại hoặc thay thế mù. Đây vẫn là checkpoint chưa hoàn thành; chưa có bản tổng hợp v0.8 TEST. Không lấy số câu đã dịch làm bằng chứng toàn game đã hết English.

### Correction — uploaded save origin (2026-10-05)

Ron confirmed the supplied N001/N002 packages are from Documents saves. Earlier template-origin assumptions are superseded. See `runtime/input_provenance.json` and `runtime/SELECTOR_DIAGNOSIS.md`. Do not request the same files again and do not ship them wholesale as installation templates.

### Runtime translation checkpoint — 2026-10-05 (continued)

Catalog maps now contain 904 entries (899 translated, five intentional unchanged names); six excluded and two review values remain in the tagged catalog audit. Story/career maps contain 974 of 1,544 selected unique values, including adult/junior/pet career descriptions, main plot, and female dialogue variants. Total runtime mapping entries: 3,675. Full scope is still incomplete: 570 story values and the untagged review queue remain; selector runtime source is unverified. See current coverage and package QA, including source hashes. No v0.8 TEST archive has been released. Supplied Documents saves must never be distributed wholesale.

### Latest checkpoint — complete selected story set + inherited menu expansion

Supersedes the preceding numerical checkpoint: runtime maps now contain 4,339 entries. All 1,544 selected story/career values have Vietnamese mappings, including chance-card choices/results and male/female variants. Menu coverage is 923 unique translated values after 510 exact inherited rows (167 labels) were promoted with OBJD ownership evidence; 93 new translations were added, and chess “Cheat” was resolved as “Chơi gian”. Catalog remains 899 translated + five retained map entries.

Source QA passes, but the full sweep remains INCOMPLETE: 17 candidate rows and 38,556 inherited rows remain under review. Continue with `runtime/row_scope_overrides.json`, `runtime/review_context.json.gz`, its summary, and remaining candidate snapshot. Run extraction to completion before generating dependent reports. Selector read-path verification and the consolidated safe installer are still outstanding. No v0.8 TEST archive exists.
