# Checkpoint cho model tiếp theo

## Mục tiêu
Tiếp tục Việt hóa The Sims Castaway Stories PC theo từng phần nhỏ, giữ bản chơi ổn định của Ron. Giao tiếp với Ron bằng tiếng Việt thân mật, gọi là Ron; hướng dẫn ngắn và rõ.

**Bắt buộc đọc `TRANSLATION_STYLE.md` trước khi dịch.**

## Trạng thái đã xác nhận
- Game portable ở `G:\Castaway-Portable`. Ron đã xác nhận vào game được và tùy chọn đồ họa hoạt động.
- Font Việt hóa Font03 hoạt động ổn; không thay font khi chỉ thêm dịch chuỗi.
- Bản chữ v0.4 đã được Ron xác nhận hiển thị ổn; v0.5/v0.6 là các build sau đó, **v0.6 chưa được Ron thử trực tiếp**.
- Bản build v0.6 có 486 câu/nhãn duy nhất qua `Options`, `UIText`, `Live`, `Neighborhood`, `Tutorial`; chi tiết ở `validation.json`.
- Nguồn dịch sau v0.6 hiện có thêm:
  - `extra07`: 127 mapping UI/gameplay.
  - `extra08`: 65 mapping nhật ký/thoại `UIText` instance 611–624.
  - `extra09`: 56 mapping nhật ký đầu game `UIText` instance 601–610.
- Tổng mapping nguồn khi gộp các bảng hiện là **737**. Đây **không phải** số chuỗi đã build hoặc test trong game.
- `extra08` + `extra09` đã được hậu kiểm lại sau commit: câu gốc có trong catalog, placeholder `%...` và `$NeighborLocal:n` giữ đúng số lần, line break điều khiển giữ đúng; 0 lỗi.
- File cài v0.6 `Castaway-Text06.zip` đã được giao riêng trong cuộc trò chuyện; repo không có payload nhị phân hoặc package game.

## Tone mới theo yêu cầu Ron
- Thoại/nhật ký cần tự nhiên, vui, lém lỉnh, có Gen Z vừa phải; ví dụ “u là trời”, “thiệt hông pa”, “hết cứu”, “phá mood” khi đúng tình huống.
- Không biến mọi câu thành meme. Cảnh buồn, nguy hiểm, bệnh tật, cái chết hoặc cảm xúc chân thành phải hạ slang.
- Narrator dùng “mình” để giữ trung tính giới tính vì người chơi có thể chọn nam/nữ.
- NPC có giới tính/ngôi xưng rõ thì dịch theo ngữ cảnh; không tự đoán.
- UI/tutorial/cảnh báo vẫn ưu tiên rõ nghĩa, ngắn gọn.
- Chi tiết đầy đủ: `TRANSLATION_STYLE.md`.

## Quy tắc kỹ thuật
1. Không xóa/gộp tùy tiện thư mục backup. Không yêu cầu cài lại game.
2. Giữ nguyên tên nhân vật/tên riêng và không dịch bừa nhãn placeholder.
3. Giữ nguyên `%s`, `%d`, `$NeighborLocal:n` và đúng số lần xuất hiện.
4. Tooltip `|`: giữ nguyên metadata phía sau mô tả.
5. Giữ line break điều khiển khi cần.
6. Sửa bảng dịch UTF-8, không sửa trực tiếp package trong giai đoạn biên tập.
7. Catalog có nhiều chuỗi The Sims 2/EP không dùng trong Castaway; không dịch hàng loạt chỉ vì còn tiếng Anh.
8. Không ghi “đã test trong game” trừ khi Ron xác nhận.

## Build và release
- `build_v06.py` vẫn chỉ đọc `translations.tsv`, `extra05.json`, `extra06.json`; chưa đọc `extra07/08/09`.
- Khi tạo builder mới, không sửa phá `build_v06.py`.
- Các instance mới cần rà cho draft sau v0.6:
  - `Options`: 128/130.
  - `UIText`: 22/137/169/170/176/501/601–624/700.
  - `Live`: 131/144/145/211.
  - `Neighborhood`: 130/131.
- Repo hiện **không có các file .package cần để build/test**, nên chưa thể tạo build mới chỉ từ source repo.
- Khi Ron muốn build bản mới, **không yêu cầu cả thư mục game**. Với toàn bộ batch mới hiện tại, trước tiên chỉ cần xin đúng: `Options.package`, `UIText.package`, `Live.package`, `Neighborhood.package` từ baseline mà Ron đang dùng (ưu tiên bản v0.6 đang cài nếu build incremental). `Tutorial.package` không có mapping mới trong extra07–09.
- Sau khi có package đúng baseline mới tạo builder/manifest và kiểm tra DBPF/QFS. Chỉ Ron mới xác nhận test trong game.

## Việc tiếp theo
1. Tiếp tục rà các chuỗi Castaway-specific chưa dịch trong `Live` và `UIText`, ưu tiên gameplay/thoại thực sự dùng.
2. Loại trừ danh sách tên bản địa và nội dung EP không liên quan.
3. Khi đủ một mốc hợp lý mới tạo build mới, không cần dừng dịch chỉ vì chưa có package.
