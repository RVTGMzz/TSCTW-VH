# Checkpoint cho model tiếp theo

## Mục tiêu
Tiếp tục Việt hóa The Sims Castaway Stories PC theo từng phần nhỏ, giữ bản chơi ổn định của Ron. Giao tiếp với Ron bằng tiếng Việt thân mật, gọi là Ron; hướng dẫn ngắn và rõ.

## Trạng thái đã xác nhận
- Game portable ở `G:\Castaway-Portable`. Ron đã xác nhận vào game được và tùy chọn đồ họa hoạt động.
- Font Việt hóa Font03 hoạt động ổn; không thay font khi chỉ thêm dịch chuỗi.
- Bản chữ v0.4 đã được Ron xác nhận hiển thị ổn; v0.5/v0.6 là các build sau đó, **v0.6 chưa được Ron thử trực tiếp**.
- Bản build v0.6 có 486 câu/nhãn duy nhất qua `Options`, `UIText`, `Live`, `Neighborhood`, `Tutorial`; chi tiết ở `validation.json`.
- Ngày 2026-10-04 đã đối chiếu `castaway-english-strings.json` với `translations.json`, `extra05.json`, `extra06.json` và thêm **127 mapping nháp cho v0.7** vào `translations/extra07.json` + `translations/extra07.tsv`. Tổng mapping nguồn sau khi gộp các bảng là 616; đây **không phải** số chuỗi đã build/test trong game.
- Batch `extra07` ưu tiên UI/gameplay: Story/Collection, loading Castaway, thông báo Village/Neighborhood, Inventory, tính cách/Simology, Fitness/tuổi Sim, 12 cung hoàng đạo, Aspiration và lỗi đặt/xây vật thể thường gặp.
- Chưa dịch tiếp nhật ký cốt truyện dài ở `UIText` instance 601–624 trong batch này.
- File cài v0.6 `Castaway-Text06.zip` đã được giao riêng trong cuộc trò chuyện; repo không có payload nhị phân.

## Quy tắc quan trọng
1. Không xóa/gộp tùy tiện thư mục backup. Không yêu cầu cài lại game.
2. Giữ nguyên tên nhân vật David Bennett, Jessica Knight, Wanmami, Felicity và tên riêng; không dịch bừa nhãn placeholder.
3. Khi dịch chuỗi có `%s`, `%d`… phải giữ nguyên placeholder. Với tooltip `|`, giữ nguyên các trường metadata sau mô tả. Giữ nguyên số dòng/placeholder điều khiển khi cần.
4. Sửa bảng dịch dạng UTF-8, thêm mapping mới vào TSV/JSON thích hợp. Tránh sửa trực tiếp package.
5. Chỉ vá các resource STR# đã định trong builder; giữ ngôn ngữ khác, mô tả, thứ tự và số lượng chuỗi. Giữ QFS hợp lệ và kiểm tra round-trip.
6. Ưu tiên GUI, hướng dẫn, tooltip, thông báo và gameplay ngắn. Catalog chứa rất nhiều chuỗi The Sims 2/EP không dùng trong Castaway; không dịch hàng loạt chỉ vì chúng còn tiếng Anh.
7. Trước khi tạo build mới, cần input packages hợp pháp. Không có chúng thì chỉ biên tập TSV/JSON, không giả lập kết quả build.
8. Không ghi là “đã test trong game” trừ khi Ron xác nhận.

## Kiểm tra batch v0.7 draft
- 127/127 câu tiếng Anh trong `extra07` có mặt trong catalog.
- Không trùng key với ba bảng trước.
- Placeholder printf (`%s`, `%d`...) được đối chiếu tự động: 0 lỗi.
- Tooltip có metadata `|` được đối chiếu phần metadata sau mô tả: 0 lỗi.
- Tên riêng/địa danh như `Village Market`, `Village Harbor` được giữ nguyên khi chúng đóng vai trò tên địa điểm.
- Chưa chạy builder/QFS cho v0.7 và chưa thử Windows/game.

## Build và release
- `build_v06.py` dùng `translations.tsv`, `extra05.json`, `extra06.json`, `dbpf.py`, `qfs.py` và input package cục bộ. Script hiện baseline `Options.package` + `UIText.package` từ Text v0.5; các package khác từ bản game gốc.
- `build_v06.py` **chưa đọc `extra07.json`** và allowlist hiện tại cũng chưa bao phủ các STR# mới của batch v0.7.
- Khi làm `build_v07.py`, cần thêm `extra07.json` và rà allowlist tối thiểu cho các instance có mapping mới: `Options` 128/130; `UIText` 22/137/169/170/176/501/700; `Live` 131/144/145/211; `Neighborhood` 130/131. Chỉ thêm instance sau khi kiểm tra đúng resource thực tế.
- Nếu tái tạo v0.6 từ source hiện có, chỉ cần các file `.package` sau trong `work/text/Text/`: **Options.package, UIText.package, Live.package, Neighborhood.package, Tutorial.package**; không cần gửi cả thư mục game.
- Với v0.7, chưa chốt builder/baseline. Nếu build incremental từ v0.6 thì ưu tiên xin đúng các package bị batch mới chạm tới thay vì cả game; cập nhật hash/installer để uninstall quay về v0.6.
- Hash baseline được ghi trong manifest v0.6. Installer tạo backup riêng và kiểm tra hash trước khi khôi phục.

## Việc tiếp theo gợi ý
1. Rà thêm các chuỗi Castaway ngắn trong `UIText`/ `Live` nhưng loại trừ danh sách tên người bản địa và nội dung EP không dùng.
2. Sau đó tạo `build_v07.py` riêng, không sửa phá `build_v06.py`.
3. Khi cần build, yêu cầu Ron gửi đúng các `.package` cần thiết, không yêu cầu tải lại cả game.
4. Sau khi Ron thử build mới và gửi ảnh/lỗi, mới cập nhật trạng thái “đã test trong game”.
