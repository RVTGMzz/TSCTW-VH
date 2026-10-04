# The Sims Castaway Stories — Việt hóa

Bản dịch cộng đồng cho bản PC.

## Trạng thái

- Bản phát hành đã đóng gói gần nhất: **Text v0.6 — 486 câu/nhãn duy nhất**. Font03 đã được Ron xác nhận hoạt động ổn.
- **v0.6 chưa được Ron kiểm tra trực tiếp đầy đủ trong game.**
- Nguồn dịch hiện đi tới **`extra38`**.
- Không dùng số unique mapping ghi tay nữa vì các batch sau có override/key trùng có chủ đích; chạy `python src/builder/build_v07.py --audit-only` để lấy số merged chính xác.
- Các batch sau v0.6 **chưa được đóng gói thành bản test mới** vì repo không chứa file `.package` của game.

## Phạm vi đã phủ

Ngoài nhật ký/cốt truyện Castaway, source hiện đã phủ phần lớn UI dùng thật:
- Buy Mode / Build Mode categories, công cụ, tooltip và lỗi đặt vật thể.
- Create-a-Sim: các bước tạo Sim, giới tính/tuổi, tóc, mặt, trang điểm, quần áo, cung hoàng đạo và tính cách.
- Neighborhood: gia đình, khu đất, đổi/xóa khu phố, lot management.
- Simology: Khát vọng, mức Khát vọng, quan hệ, trường học, sở thích, lịch làm việc.
- Story/Camera, Inventory, Collection, system/loading messages.
- Popup save/quit, tutorial nhanh, battery warning và các thông báo Castaway thường gặp.
- Thoại/popup được Việt hóa tự nhiên, vui và hơi Gen Z theo style guide khi phù hợp.

Toàn bộ chuỗi **gắn tag Castaway rõ ràng và có nội dung cần dịch** đã được xử lý. Những mục Cast-tagged còn tiếng Anh chủ yếu là **tên riêng/địa điểm, phím tắt, tên nhạc và copyright**, được cố ý giữ nguyên.

Các package như `eCAS.package` (Body Shop), `UIText2.package` (nhãn expansion) và `Installer.package` (chuỗi Seasons) là di sản không thuộc gameplay Castaway nên không dịch đại trà.

## Phong cách dịch

Đọc [`TRANSLATION_STYLE.md`](TRANSLATION_STYLE.md).

- Thoại/nhật ký: tự nhiên, có cá tính, Gen Z vừa phải khi hợp cảnh.
- Narrator ưu tiên “mình” để trung tính giới tính.
- Cảnh buồn/nguy hiểm/tình cảm nghiêm túc phải hạ slang.
- UI/tutorial/cảnh báo vẫn ngắn, rõ và chính xác.
- Không phá placeholder, metadata tooltip hoặc line break điều khiển.

## Kiểm tra source

`extra23`–`extra29` đã được audit ở mốc trước. Từ `extra32` đến `extra38` bổ sung Build/Buy tools, object stats, Castaway Needs, animal motives, Simology/skills/career, 24 tên chương, Player Profile, mô tả Wanmami và Barter/alternate skill tooltips.

Builder v0.7 nay có `--audit-only` để merge và kiểm toàn bộ source mà không cần package game; audit còn phát hiện placeholder/line-break/tooltip metadata sai và ký tự Cyrillic lạc.

## Build / test

Builder mới đã có tại **`src/builder/build_v07.py`**; `build_v06.py` được giữ nguyên.

`build_v07.py`:
- đọc `translations.json` và toàn bộ `extra*.json` theo thứ tự số;
- ghi lại override của batch sau;
- dùng catalog để suy ra STR# instance cần sửa;
- giữ allowlist package đã audit;
- bảo toàn language khác, description, string order/count và compression state;
- kiểm placeholder, line break, tooltip metadata, DBPF/QFS round-trip;
- giữ rule ngữ cảnh `Neighborhood.package: Play → Chơi`;
- có `--audit-only` để kiểm source mà không cần package game.

Builder **chưa được chạy end-to-end với package thật** vì repo source-only, nên chưa có bản test mới và chưa có claim runtime test.

Build incremental từ v0.6 hiện cần đúng 7 file:
- `Options.package`
- `UIText.package`
- `Live.package`
- `Neighborhood.package`
- `Build.package`
- `CAS.package`
- `CAS_Shared.package`

Không cần cả thư mục game. `Tutorial.package` chỉ cần nếu rebuild full từ original baseline.

Chi tiết: [`BUILD.md`](BUILD.md).

## Thư mục

- `translations/`: bảng dịch nền và batch bổ sung tới `extra38`.
- `src/builder/`: parser DBPF/QFS và builder.
- `installer-source/`: nguồn installer/manifest của v0.6; payload không nằm trong repo.
- `castaway-english-strings.json`: catalog tiếng Anh dùng để audit; không phải package game.
- `validation.json`: validation của build v0.6, chưa đại diện cho draft hiện tại.

Chỉ ghi “đã test trong game” khi Ron xác nhận trực tiếp.
