# Checkpoint cho model tiếp theo

## Mục tiêu
Tiếp tục Việt hóa The Sims Castaway Stories PC theo từng phần nhỏ, giữ bản chơi ổn định của Ron. Giao tiếp với Ron bằng tiếng Việt thân mật, gọi là Ron; hướng dẫn ngắn và rõ.

## Trạng thái đã xác nhận
- Game portable ở `G:\Castaway-Portable`. Ron đã xác nhận vào game được và tùy chọn đồ họa hoạt động.
- Font Việt hóa Font03 hoạt động ổn; không thay font khi chỉ thêm dịch chuỗi.
- Bản chữ v0.4 đã được Ron xác nhận hiển thị ổn; v0.5/v0.6 là các build sau đó, v0.6 chưa được Ron thử trực tiếp.
- Bản dịch có 486 câu/nhãn duy nhất qua `Options`, `UIText`, `Live`, `Neighborhood`, `Tutorial`; chi tiết ở `validation.json`. Chưa dịch toàn bộ cốt truyện.
- File cài v0.6 `Castaway-Text06.zip` đã được giao riêng trong cuộc trò chuyện; repo không có payload nhị phân.

## Quy tắc quan trọng
1. Không xóa/gộp tùy tiện thư mục backup. Không yêu cầu cài lại game.
2. Giữ nguyên tên nhân vật David Bennett, Jessica Knight, Wanmami, Felicity và tên riêng; không dịch bừa nhãn placeholder.
3. Khi dịch chuỗi có `%s`, `%d`… phải giữ nguyên placeholder. Với tooltip `|`, giữ nguyên các trường metadata sau mô tả. Giữ nguyên số dòng/placeholder điều khiển khi cần.
4. Sửa bảng dịch dạng UTF-8, thêm mapping mới vào TSV/JSON thích hợp. Tránh sửa trực tiếp package.
5. Chỉ vá các resource STR# đã định trong builder; giữ ngôn ngữ khác, mô tả, thứ tự và số lượng chuỗi. Giữ QFS hợp lệ và kiểm tra round-trip.
6. Ưu tiên các đoạn GUI, hướng dẫn, tooltip, thông báo và nội dung gameplay ngắn; chưa mở rộng dịch story dài nếu chưa kiểm tra font/encoding và dung lượng.
7. Trước khi tạo build mới, cần có input packages hợp pháp tại `work/text/Text/`. Không có chúng thì tiếp tục biên tập TSV/JSON, không giả lập kết quả build.

## Build và release
- `build_v06.py` dùng `translations.tsv`, `extra05.json`, `extra06.json`, `dbpf.py`, `qfs.py` và các input package cục bộ. Script hiện baseline `Options.package` + `UIText.package` từ Text v0.5; các package khác từ bản game gốc.
- `build_v05.py` tương tự nhưng baseline Options/UIText là v0.4. `build_v04.py` là nhánh build cũ. Kiểm tra các đường dẫn tương đối nếu đưa source ra khỏi `work/`.
- Hash baseline được ghi trong manifest v0.6. Installer tạo backup riêng và kiểm tra hash trước khi khôi phục. Khi phát hành v0.7, thiết kế uninstall về v0.6 và kiểm tra thực tế trước khi nói là tương thích.
- Không ghi là “đã test trong game” trừ khi Ron xác nhận.

## Việc tiếp theo gợi ý
Trước tiên nhờ Ron thử v0.6, chụp màn hình các phần mới và báo lỗi/trống nếu có. Sau đó cập nhật checkpoint theo phản hồi. Đợt dịch tiếp nên rà `UIText` trợ giúp còn lại, phần hội thoại tutorial và tooltip gameplay đang dùng; loại trừ resources Sims 2/EP không dùng trong Castaway.
