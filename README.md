# The Sims Castaway Stories — Việt hóa

Bản dịch cộng đồng cho bản PC. Bản phát hành hiện tại: **Text v0.6, 486 câu/nhãn duy nhất** (715 mục chuỗi tính cả ngôn ngữ Mỹ/Anh và các bảng). Font03 đã được Ron xác nhận chạy ổn; **v0.6 chưa được kiểm tra trực tiếp trong game**.

Nguồn dịch đang tiếp tục sau v0.6:
- `extra07`: 127 mapping UI/gameplay.
- `extra08`: 65 mapping thoại/nhật ký Castaway, instance 611–624.
- `extra09`: 56 mapping nhật ký đầu game, instance 601–610.

Tổng mapping nguồn hiện tại là **737**, nhưng các batch mới **chưa được build vào package và chưa được test trong game**.

## Phong cách dịch

Đọc [`TRANSLATION_STYLE.md`](TRANSLATION_STYLE.md). Thoại/nhật ký dùng tiếng Việt tự nhiên, vui và hơi Gen Z khi hợp cảnh; UI/tutorial/cảnh báo vẫn rõ và gọn. Narrator ưu tiên “mình” để không khóa giới tính người chơi.

## Tải bản cài

Bản cài v0.6 được chia sẻ riêng trong cuộc trò chuyện dưới tên `Castaway-Text06.zip`. Repo này lưu mã nguồn, bảng dịch và trạng thái dự án để tiếp tục; **không chứa file game hay gói `.package`**.

## Tiếp tục dịch

Đọc [`CONTINUE_WITH_MODEL.md`](CONTINUE_WITH_MODEL.md) trước khi sửa bản dịch. Các bảng nằm trong `translations/`; mã DBPF/QFS và builder nằm trong `src/builder/`.

`build_v06.py` chưa đọc `extra07/08/09`. Khi build bản mới cần builder/allowlist riêng và các package từ bản game người dùng sở hữu. Không đưa package gốc hoặc package đã vá lên repo công khai.

## Thư mục

- `translations/`: bản dịch nền và phần bổ sung từng đợt (`extra05` đến `extra09`).
- `src/builder/`: parser DBPF, QFS và script build/kiểm tra.
- `installer-source/`: script cài/gỡ và manifest cho v0.6; payload không nằm trong repo.
- `castaway-english-strings.json`: catalog tiếng Anh dùng để rà câu chưa dịch; không phải package game.
- `validation.json`: kết quả kiểm tra cấu trúc của build v0.6, không đại diện cho các batch draft mới.
