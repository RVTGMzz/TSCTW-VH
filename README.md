# The Sims Castaway Stories — Việt hóa

Bản dịch cộng đồng cho bản PC.

## Trạng thái

- Bản phát hành đã đóng gói gần nhất: **Text v0.6 — 486 câu/nhãn duy nhất**. Font03 đã được Ron xác nhận hoạt động ổn.
- **v0.6 chưa được Ron kiểm tra trực tiếp đầy đủ trong game.**
- Nguồn dịch đang phát triển sau v0.6 hiện đi tới **`extra29`**.
- Tổng số mapping nguồn hiện tại: **1.760**. Đây là số mapping trong source, **không phải số chuỗi đã build/test trong game**.
- Các batch mới sau v0.6 **chưa được đóng gói thành bản test mới** vì repo không chứa file `.package` của game.

## Phạm vi đã phủ

Ngoài nhật ký/cốt truyện Castaway, source hiện đã phủ thêm phần lớn UI dùng thật:
- Buy Mode / Build Mode categories, công cụ, tooltip và lỗi đặt vật thể.
- Create-a-Sim: bước tạo Sim, giới tính/tuổi, tóc, mặt, trang điểm, quần áo, cung hoàng đạo và tính cách.
- Neighborhood: gia đình, khu đất, đổi/xóa khu phố, lot management.
- Simology: Khát vọng, mức Khát vọng, quan hệ, trường học, sở thích, lịch làm việc.
- Story/Camera, Inventory, Collection, system/loading messages.
- Một số hội thoại/popup được Việt hóa tự nhiên, vui và hơi Gen Z theo style guide.

Toàn bộ chuỗi **gắn tag Castaway rõ ràng và có nội dung cần dịch** đã được xử lý. Những mục Cast-tagged còn tiếng Anh chủ yếu là **tên riêng/địa điểm, phím tắt, tên nhạc và copyright**, được cố ý giữ nguyên.

Các package như `eCAS.package` (Body Shop), `UIText2.package` (nhãn expansion) và `Installer.package` (chuỗi Seasons) được xem là di sản không thuộc gameplay Castaway nên không dịch đại trà.

## Phong cách dịch

Đọc [`TRANSLATION_STYLE.md`](TRANSLATION_STYLE.md).

- Thoại/nhật ký: tự nhiên, có cá tính, Gen Z vừa phải khi hợp cảnh.
- Narrator ưu tiên “mình” để trung tính giới tính.
- Cảnh buồn/nguy hiểm/tình cảm nghiêm túc phải hạ slang.
- UI/tutorial/cảnh báo vẫn ngắn, rõ và chính xác.
- Không phá placeholder, metadata tooltip hoặc line break điều khiển.

## Kiểm tra source

Các batch `extra23`–`extra29` hiện có **344 mapping**, không trùng key lẫn nhau. Hậu kiểm gần nhất:
- 0 câu thiếu trong catalog.
- 0 lỗi placeholder.
- 0 lỗi line break điều khiển.
- 0 lỗi metadata tooltip.
- 0 ký tự Cyrillic lạc vào bản dịch.

## Build / test

`build_v06.py` là builder cũ và **không đọc các batch mới**. Không sửa phá builder v0.6; bản kế tiếp cần builder riêng.

Các batch mới hiện chạm tới:
- `Options.package`
- `UIText.package`
- `Live.package`
- `Neighborhood.package`
- `Build.package`
- `CAS.package`
- `CAS_Shared.package`

Nếu build incremental từ bản v0.6 Ron đang cài, chỉ cần đúng các package bị chạm ở trên. `Tutorial.package` không có mapping mới sau v0.6. Không cần gửi cả thư mục game và không đưa package game lên repo công khai.

Chỉ ghi “đã test trong game” khi Ron xác nhận trực tiếp.

## Thư mục

- `translations/`: bảng dịch nền và các batch bổ sung tới `extra29`.
- `src/builder/`: parser DBPF/QFS và builder.
- `installer-source/`: nguồn installer/manifest của v0.6; payload không nằm trong repo.
- `castaway-english-strings.json`: catalog tiếng Anh dùng để audit; không phải package game.
- `validation.json`: validation của build v0.6, chưa đại diện cho draft hiện tại.
