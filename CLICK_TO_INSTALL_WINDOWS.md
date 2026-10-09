# Castaway Stories Việt hóa v0.8 TEST — Cài một lần nhấn trên Windows

**[TẢI EXE MỚI NHẤT — Build 66](https://github.com/RVTGMzz/TSCTW-VH/releases/download/castaway-v08-test-windows-66/VotriValley-Castaway-v08-TEST.exe)** · [GitHub Release](https://github.com/RVTGMzz/TSCTW-VH/releases/tag/castaway-v08-test-windows-66) · [CI Build 66 PASS](https://github.com/RVTGMzz/TSCTW-VH/actions/runs/37865230511).

Không cần cài Python hay công cụ lập trình. EXE chỉ chứa mã vá và bản dịch, **không chứa game của EA**. Bản này đã qua test cấu trúc và thử cài/khôi phục trên package giả; **vẫn là TEST, chưa xác minh toàn bộ gameplay thực tế**.

## Bước 1 — cài Text + runtime

1. Thoát hẳn game, đóng các trình cài Build 29/Build 23 cũ.
2. Mở EXE Build 66, chọn thư mục có `TSData`, ví dụ `G:\Castaway-Portable`.
3. Bấm **Cài Việt hóa v0.8 TEST**, xác nhận. Ứng dụng kiểm tra và sao lưu các package sẽ chỉnh, bổ sung chỉ những dòng tiếng Anh *đúng nguồn* trong runtime **và Text**. Hai dòng đã dịch cũ của ghế đá được nâng cấp bằng quy tắc exact-row đã kiểm duyệt; những dòng lạ được giữ nguyên. Không ghi đè font hoặc save Documents trong bước này.
4. Nếu thành công, mở game kiểm tra **Thu hút/Mất hứng**, **Phần thưởng Khát vọng**, item mô tả và menu.

**Khôi phục các package Text/runtime:** thoát game, mở EXE, nhấn **Khôi phục bản trước**. Ứng dụng trả lại byte nguyên trạng lúc trước khi bấm Cài, bao gồm những bản Việt hóa cũ; **không** xóa dữ liệu tiến trình nhân vật/nhà trong Documents.

## Bước 2 — tùy chọn, chỉ khi muốn Việt hóa tên đảo và tiểu sử trong save

**Đây là bước RIÊNG, có thể bỏ qua**. Tên `Wanmami Island`, hai giới thiệu Story Mode, tiểu sử Candy/Linea và các tên địa điểm được tìm thấy ở N001/N002 của Documents, chứ không chỉ trong các package cài đặt.

1. **Thoát hoàn toàn game**, nên có thêm bản sao lưu save cá nhân nếu đây là save đang chơi lâu.
2. Nhấn **Việt hóa đảo & tiểu sử...**. Nếu có nhiều profile/Documents (kể cả OneDrive), chọn đúng thư mục dữ liệu game đang dùng có folder `Neighborhoods`.
3. Đọc cảnh báo và đồng ý **chỉ nếu muốn sửa nội dung chữ trong save**. Công cụ sao lưu nguyên bản N001/N002, kiểm định resource key/ngôn ngữ/metadata rồi chỉ cập nhật các dòng khớp tiếng Anh gốc. Không thay bằng package save của người khác, không đổi đồ/nhà/tiến trình.
4. Chạy lại game kiểm tra màn chọn `Đảo Wanmami`, các mô tả và tiểu sử.

**Khôi phục riêng dữ liệu đảo:** đóng game, chọn **Khôi phục dữ liệu đảo**. Nếu game đã lưu tiến trình mới sau khi dịch đảo, công cụ sẽ **từ chối** tự động ghi đè, tránh làm mất dữ liệu chơi. Đây là đường khôi phục **khác** với nút Khôi phục bản trước của gói Text/runtime.

> *Lưu ý:* Resource này đã được truy vết tới package trên đĩa, nhưng chưa xác minh game thực sự ưu tiên đọc đúng bản Documents đang sửa. Bước 2 vẫn là thử nghiệm, không bảo đảm ngay lập tức hết tiếng Anh ở màn chọn chuyện.

## Bước 3 — giúp rà toàn bộ các nhóm còn tiếng Anh

Những tên **Pine Tree**, **Row of Trees**, cảnh báo dùng **Elixir of Life** lúc chưa đạt Khát vọng Vàng, và phiên bản đoạn hướng dẫn Thu hút/Mất hứng dài hơn hiện chưa có chủ resource được xác minh từ catalog đã kiểm tra.

Trong EXE, nhấn **Rà chữ còn sót** (chỉ đọc file, không sửa game), đợi hoàn tất, sau đó nhấn **Lưu báo cáo...** để lưu TXT UTF-8. Gửi file đó trong cuộc trò chuyện để tiếp tục dịch theo **cả resource/cụm**, không vá từng ảnh. Báo cáo có thể ghi lại đường dẫn Windows cá nhân, hãy mở xem trước khi gửi.

## Dòng ghi công

Yêu cầu chính xác: **“Việt hóa bởi Votri Valley”**. Chưa chèn được vào game: tên ứng dụng nằm trong một chuỗi tiêu đề cửa sổ, còn logo ở màn mở đầu là giao diện/đồ họa khác; chỉnh chuỗi tên ứng dụng không tạo được dòng nhỏ nằm dưới logo. Đang tìm tài nguyên layout/splash phù hợp. Không chèn gian lận vào Credits của EA hoặc gây lỗi game để báo hoàn tất.

## An toàn và phạm vi TEST

- Dùng đúng file EXE từ GitHub Releases của repo này; Windows có thể cảnh báo ứng dụng chưa ký số. Không cần tắt Defender.
- Cài Text/runtime và sửa save là **hai thao tác khác nhau** với hai loại backup khác nhau. Không làm hai việc này nếu game đang mở.
- Nếu công cụ báo lỗi DBPF hoặc metadata, giữ nguyên file, xuất **Lưu báo cáo...** gửi để rà đúng nguồn, **đừng xóa** `objects.package` hoặc `Wants.package`.
- Lần cài lại khi không còn dòng *khớp tiếng Anh gốc* để bổ sung sẽ chỉ thông báo, không làm thay đổi file và không tạo thêm backup.
- Bản thử chưa giải quyết lỗi đồ họa map đảo Wanmami vốn cũng xuất hiện ở bản gốc chưa Việt hóa.
