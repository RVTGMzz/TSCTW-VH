# The Sims Castaway Stories — Việt hóa

Bản dịch cộng đồng cho bản PC. Trạng thái hiện tại: **Text v0.6, 486 câu/nhãn duy nhất** (715 mục chuỗi tính cả ngôn ngữ Mỹ/Anh và các bảng). Font03 đã được Ron xác nhận chạy ổn; v0.6 chưa được kiểm tra trực tiếp trong game.

## Tải bản cài

Bản cài v0.6 được chia sẻ riêng trong cuộc trò chuyện dưới tên `Castaway-Text06.zip`. Repo này lưu mã nguồn, bảng dịch và trạng thái dự án để tiếp tục; **không chứa file game hay gói `.package`**.

## Tiếp tục dịch

Đọc [`CONTINUE_WITH_MODEL.md`](CONTINUE_WITH_MODEL.md) trước khi sửa bản dịch. Các bảng nằm trong `translations/`; mã DBPF/QFS và builder nằm trong `src/builder/`.

Để build cần các gói gốc lấy từ bản game người dùng sở hữu. Không đưa gói gốc hoặc gói đã vá lên repo công khai. `build_v06.py` đang nhận Text v0.5 làm baseline; đổi baseline thì phải cập nhật hash và quy trình backup trong installer.

## Thư mục

- `translations/`: bản dịch nền và phần bổ sung từng đợt.
- `src/builder/`: parser DBPF, QFS và script build/kiểm tra.
- `installer-source/`: script cài/gỡ và manifest cho v0.6; payload không nằm trong repo.
- `validation.json`: kết quả kiểm tra cấu trúc và phạm vi bảng dịch.
