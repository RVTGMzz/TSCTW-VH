# The Sims Castaway Stories — Việt hóa

Bản dịch cộng đồng cho bản PC. Bản phát hành hiện tại: **Text v0.6, 486 câu/nhãn duy nhất** (715 mục chuỗi tính cả ngôn ngữ Mỹ/Anh và các bảng). Font03 đã được Ron xác nhận chạy ổn; **v0.6 chưa được kiểm tra trực tiếp trong game**.

Bản dịch nguồn đang tiếp tục cho v0.7: `translations/extra07.json` + `extra07.tsv` hiện bổ sung **127 mapping nháp** cho UI/gameplay. Các mapping này đã được đối chiếu catalog, placeholder và metadata, nhưng **chưa được build vào package và chưa được test trong game**.

## Tải bản cài

Bản cài v0.6 được chia sẻ riêng trong cuộc trò chuyện dưới tên `Castaway-Text06.zip`. Repo này lưu mã nguồn, bảng dịch và trạng thái dự án để tiếp tục; **không chứa file game hay gói `.package`**.

## Tiếp tục dịch

Đọc [`CONTINUE_WITH_MODEL.md`](CONTINUE_WITH_MODEL.md) trước khi sửa bản dịch. Các bảng nằm trong `translations/`; mã DBPF/QFS và builder nằm trong `src/builder/`.

Để build cần các gói lấy từ bản game người dùng sở hữu. Không đưa gói gốc hoặc gói đã vá lên repo công khai. `build_v06.py` đang nhận Text v0.5 làm baseline và chưa đọc `extra07.json`; v0.7 cần builder/allowlist riêng.

## Thư mục

- `translations/`: bản dịch nền và phần bổ sung từng đợt (`extra05`, `extra06`, `extra07`).
- `src/builder/`: parser DBPF, QFS và script build/kiểm tra.
- `installer-source/`: script cài/gỡ và manifest cho v0.6; payload không nằm trong repo.
- `castaway-english-strings.json`: catalog tiếng Anh dùng để rà câu chưa dịch; không phải package game.
- `validation.json`: kết quả kiểm tra cấu trúc của build v0.6, không đại diện cho draft v0.7.
