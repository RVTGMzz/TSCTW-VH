# Việt hóa Castaway Stories v0.8 TEST — cài bằng một file EXE

**Dành cho Windows, không cần cài Python hoặc công cụ phụ.** Bản này là **bản thử nghiệm** mở rộng runtime, tiếp tục sử dụng Text và bộ font Votri Valley v0.7a đã có. Chưa xác nhận trên toàn bộ game và chưa sửa xong nguồn hiển thị chữ màn chọn cốt truyện.

**Build 17 sửa lỗi `Unrecognized translated/source text` khi file đã được Việt hóa trước:** Các dòng có đúng resource/key/row/ngôn ngữ và metadata nhưng nội dung khác bản hiện hành được **giữ nguyên, không ghi đè và không tính là bản dịch mới đã kiểm duyệt**. Chỉ những dòng trùng chính xác tiếng Anh gốc mới được dịch; cấu trúc/metadata sai vẫn khiến trình cài dừng. Hãy dùng [EXE Build 17](https://github.com/RVTGMzz/TSCTW-VH/releases/download/castaway-v08-test-windows-29/VotriValley-Castaway-v08-TEST.exe), không sử dụng Build 11 với lỗi trước đó.

**Lỗi Build 17: `FileNotFoundError: castaway-english-strings.json`.** Đây là lỗi gọi nhầm dữ liệu Text gốc khi đang build runtime overlay. **Build 23** đã tách đúng nhánh runtime-only, không cần file này. GitHub Actions #23 chạy smoke-test ngay trên EXE đóng gói: dữ liệu DBPF giả → tạo payload → dry-run → cài → khôi phục đều PASS. Không cần tải JSON riêng. Nếu Build 17 đã dừng tại lỗi này, **chưa có thao tác cài và chưa có gì cần phục hồi**.

**Khôi phục sau khi cài thành công:** đóng game, mở lại EXE và chọn **Khôi phục bản trước**. Bản sao lưu nằm trong `%LOCALAPPDATA%\\Votri Valley\\Castaway v0.8 TEST\\Backups` và trả lại **đúng các package của ông trước khi cài v0.8**, kể cả Việt hóa cũ; không phải khôi phục bộ game tiếng Anh gốc.

**Build 29 (2026-10-09):** thêm nút **Lưu báo cáo...** để tự xuất log UTF-8 ra máy khi cài có lỗi (người dùng tự xem trước khi chia sẻ; không tự gửi qua mạng). Bấm **Cài** một lần nữa sau khi đã vá đủ những dòng nguồn xác nhận được sẽ được báo **không có gì cần bổ sung**, thay vì báo lỗi hoặc tạo backup mới. [Windows CI #29](https://github.com/RVTGMzz/TSCTW-VH/actions/runs/37861994690) đã PASS kiểm thử dữ liệu dịch và smoke-test EXE đóng gói. Các thay đổi vẫn chỉ được kiểm thử bằng package giả; chưa có kết quả Windows gameplay thật.

## Cách cài

1. Mở [GitHub Releases của dự án](https://github.com/RVTGMzz/TSCTW-VH/releases), chọn bản mới nhất có tên **Castaway Stories Việt hóa v0.8 TEST — Windows**.
2. Bấm tải trực tiếp **`VotriValley-Castaway-v08-TEST.exe`**. *Không cần tải source code hay cài Python*.
3. Thoát hẳn game. Nhấn đúp EXE. Nếu game đang đặt tại `G:\Castaway-Portable`, trình cài sẽ tự nhận; nếu không, nhấn **Chọn thư mục...**, chọn folder có `TSData`.
4. Bấm **Cài Việt hóa v0.8 TEST**. Trình cài tự kiểm tra 10 file `.package` nguyên bản, sao lưu, tạo bản vá từ nguồn dịch, kiểm tra lại rồi cài. Font và các file Text v0.7a vẫn giữ nguyên, không đụng save trong Documents.
5. Sau khi cài, mở game như bình thường. Test cốt truyện, Wants, Rewards, item, menu Examine/Use. Nếu gặp lỗi, quay lại trình cài và chọn **Khôi phục bản trước**.

**Nếu báo sai SHA-256 hoặc file không nguyên bản:** DỪNG. Một trong các package runtime đã bị thay đổi (có thể do mod/bản Việt hóa trước). Đừng tắt kiểm tra hoặc chép đè file bằng bản người khác. Đường khôi phục chỉ khôi phục package mà chính trình cài này đã sao lưu.

**Nếu báo thiếu font:** phiên bản này là *runtime overlay*, chưa chứa font độc lập. Máy cần có bản font Việt hóa v0.7a đang sử dụng tốt. Trình cài cố ý không thay đổi font.

**Nếu Windows cảnh báo ứng dụng chưa ký:** đây là bản thử nghiệm xây dựng tự động từ [mã nguồn của dự án](https://github.com/RVTGMzz/TSCTW-VH). Chỉ chạy khi đã kiểm tra nguồn tải và tin tưởng file; không cần tắt Windows Defender. File EXE từ bên thứ ba không do Votri Valley phát hành không được hỗ trợ.

## Những gì trình cài làm và không làm

- **Có:** nhúng sẵn bản dịch nguồn, dò thư mục portable, vá trong máy người dùng, kiểm tra hash, sao lưu có ngày giờ tại `%LOCALAPPDATA%\Votri Valley\Castaway v0.8 TEST\Backups`, khôi phục bằng nút bấm.
- **Không:** cài Python, mở mạng để tải package game, ghi đè `.exe` của game, sửa save N001/N002 trong Documents, sửa font đang chạy, hoặc phát tán dữ liệu thương mại của EA.
- **Chưa xác minh:** chạy thật trên bộ package đang cài của người dùng, giao diện selector, tương thích save/load và tất cả chữ trong gameplay.

## Dành cho người đóng góp

Build EXE từ `.github/workflows/v08-windows-installer.yml` qua GitHub Actions Windows. Workflow chạy toàn bộ test giả lập, test source, đóng gói với PyInstaller trên runner, chạy `--self-test` trên file EXE đóng gói, upload bản tải xuống và gắn **pre-release TEST**. Bản phát hành trực tiếp luôn phải ghi rõ đây không phải bản v0.8 hoàn chỉnh.
