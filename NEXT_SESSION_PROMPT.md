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

