# The Sims Castaway Stories — Việt hóa

Bản dịch cộng đồng cho bản PC.

## Trạng thái

- Bản phát hành đã đóng gói gần nhất: **Text v0.6 — 486 câu/nhãn duy nhất**. Font03 đã được Ron xác nhận hoạt động ổn.
- **v0.6 chưa được Ron kiểm tra trực tiếp đầy đủ trong game.**
- Nguồn dịch hiện đi tới **`extra44`**.
- **Source audit v0.7 đã PASS trên GitHub Actions ngày 2026-10-04:** 1.774 mapping sau merge, 1.774/1.774 key hiện diện trong package allowlist, 0 key thiếu khỏi catalog. Có 274 override có chủ đích giữa các batch.\n- Không dùng số unique mapping ghi tay; chạy `python src/builder/build_v07.py --audit-only` để tái kiểm bất cứ lúc nào.
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

`extra23`–`extra29` đã được audit ở mốc trước. `extra32`–`extra42` bổ sung Build/Buy tools, object stats, Castaway Needs, animal motives, Simology/skills/career, tên chương, Player Profile, mô tả Wanmami, Barter và shortcut UI. `extra43`–`extra44` là lượt cleanup cuối cho Story/Neighborhood và hai popup hệ thống còn hữu ích.

Builder v0.7 nay có `--audit-only` để merge và kiểm toàn bộ source mà không cần package game; audit còn phát hiện placeholder/line-break/tooltip metadata sai và ký tự Cyrillic lạc. Workflow `.github/workflows/source-audit.yml` tự chạy audit khi source dịch, catalog hoặc builder thay đổi.

### Audit hoàn thiện source

Đã rà theo package sau khi merge các batch liên quan:
- **Options**: phần còn tiếng Anh chỉ là 16/32-bit và tên thể loại nhạc.
- **Neighborhood**: còn dịch vụ TheSims2.com cũ / College không dùng; gameplay UI đã phủ.
- **CAS**: các mục còn lại là placeholder nội bộ hoặc key đã được dịch ở bảng dùng chung.
- **Build**: chỉ còn số giá, tile trùng bị đánh dấu xóa và placeholder developer.
- **Live**: còn tên bản địa, điểm A–F, ký hiệu thứ, University/Pets/PlantSim và token nội bộ.
- **UIText**: phần còn lại chủ yếu là Exchange/TheSims2.com, Sims 1 import cũ, album Pleasantview/Veronaville/Strangetown, expansion/Body Shop hoặc tên sản phẩm.

Vì vậy **core translation sweep được xem là hoàn tất ở mức source**; tiếng Anh còn lại không được dịch chỉ để chạy theo tỷ lệ phần trăm.

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
- có `--audit-only` để kiểm source mà không cần package game;
- nhận diện các câu đã dịch trong baseline v0.6 theo package/resource/ngôn ngữ bằng `validation.json`; giá trị mơ hồ không bị áp sai ngữ cảnh.

Builder đã qua kiểm tra cú pháp và thử logic ánh xạ lịch sử v0.6. **Chưa chạy end-to-end với package thật**, nên chưa có build v0.7 mới hay claim runtime test.

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

- `translations/`: bảng dịch nền và batch bổ sung tới `extra44`.
- `src/builder/`: parser DBPF/QFS và builder.
- `installer-source/`: nguồn installer/manifest của v0.6; payload không nằm trong repo.
- `castaway-english-strings.json`: catalog tiếng Anh dùng để audit; không phải package game.
- `validation.json`: validation của build v0.6, chưa đại diện cho draft hiện tại.

Chỉ ghi “đã test trong game” khi Ron xác nhận trực tiếp.
