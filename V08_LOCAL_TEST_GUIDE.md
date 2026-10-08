# v0.8 TEST — tạo bản vá trên máy người dùng (nguồn-only)

> **Chưa phải bản phát hành.** Các công cụ này vừa được thêm vào repo để dựng và thử bản vá trên **package gốc thuộc máy người dùng**, không tải game gốc lên GitHub. Không ai đã xác nhận game Windows chạy ổn với v0.8. Không phát tán package thương mại hoặc save Documents.

## Chọn đúng chế độ

**A. Runtime overlay trên v0.7a (ưu tiên để kiểm thử trước).** Giữ nguyên 7 Text package và các font đang chạy ổn của v0.7a, chỉ vá nhóm runtime Objects/Wants/EPText mới. Cần **10 file cài đặt runtime gốc có hash khớp audit**; các file core Text có thể đang là bản v0.7a. **Không thay đổi save.** Đây là bản kiểm thử thành phần runtime, chưa phải bản Việt hóa tổng hợp cuối cùng.

**B. Full original Text + runtime.** Khi đã có đủ **8 file Text gốc chưa vá** (Options, UIText, Live, Neighborhood, Build, CAS, CAS_Shared, Tutorial), builder tạo từ nguồn tiếng Anh của Text và 10 file runtime gốc. Cần xác nhận rõ Text là nguyên bản bằng cờ `--core-original-confirmed` (cờ này là tuyên bố của người vận hành, không phải kiểm tra hash tự động). Font đang dùng vẫn được giữ nguyên, không được đóng gói hoặc sửa tự động.

Hai đường build đều phát hiện *bản cài/nguồn sai hash* của 10 runtime package và dừng, thay vì viết đè. Nếu một trong 10 file đang bị mod/patch trước đó, hãy khôi phục **đúng file gốc** từ bản sao lưu/cài đặt sạch của cùng bản game; không tắt kiểm tra để ép chạy.

## Thao tác trên Windows (PowerShell tại thư mục repo)

Cần Python 3.11 trở lên. Đóng game trước khi định cài. **Các lệnh sau KHÔNG làm thay đổi thư mục game cho đến khi có `--apply --game-closed`.**

**1. Kiểm tra 10 file runtime trong bản Castaway đang cài**

```powershell
python src/builder/stage_runtime_inputs.py --game-root "G:/Castaway-Portable"
```

Nếu `work/baseline_preflight.json` cho biết `verified: 10`, dùng `--copy-verified` để copy đúng 10 file gốc sang `work/input` trong repo. Công cụ không tự sửa game và không đụng tới Documents.

```powershell
python src/builder/stage_runtime_inputs.py --game-root "G:/Castaway-Portable" --copy-verified
```

Lưu ý: staging không ghi đè file có sẵn. Nếu đã từng stage, dùng thư mục output mới trống qua `--output` rồi truyền đường dẫn mới đó cho builder. Hai `Wants.package` nằm ở **hai nhánh thư mục khác nhau**, tuyệt đối không hoán đổi.

**2A. Tạo bản thử runtime overlay cho v0.7a**

```powershell
python src/builder/prepare_v08_test.py --runtime-only --runtime-input "work/input" --output "work/v08_runtime_test"
```

Hoặc **2B.** Khi có toàn bộ Text gốc chưa vá, đặt chúng trong `work/text/Text` và chạy:

```powershell
python src/builder/prepare_v08_test.py --core-original-confirmed --core-input "work/text/Text" --runtime-input "work/input" --output "work/v08_full_test"
```

Kết quả chỉ nằm ở `work/v08_*_test/Payload` và `manifest.json`. Builder xuất **chỉ các package có thay đổi**, đối chiếu nguyên trạng 10 package runtime, kiểm tra nguồn, byte round-trip và idempotence. **Không đưa save Documents, fonts hoặc EXE vào payload**. Không tự cài hay đụng file game.

**3. Xem trước việc cài (dry run)**

```powershell
python src/builder/install_v08_local.py --game-root "G:/Castaway-Portable" --bundle "work/v08_runtime_test" --backup "G:/Castaway-Backup-v08"
```

Nếu toàn bộ package hiện tại khớp hash gốc trong `manifest.json`, công cụ chỉ báo **DRY RUN**. Nếu máy đang dùng patch runtime cũ, nó sẽ dừng; không được bỏ điều kiện hash.

**4. Cài thử chỉ sau khi đã thoát game và dry run PASS**

```powershell
python src/builder/install_v08_local.py --game-root "G:/Castaway-Portable" --bundle "work/v08_runtime_test" --backup "G:/Castaway-Backup-v08" --apply --game-closed
```

Nó sao lưu file gốc dưới `G:/Castaway-Backup-v08` (một đường dẫn mới **ngoài thư mục game**), ghi `restore_manifest.json`, kiểm tra hash rồi mới thay. Nếu có lỗi trong lúc ghi sẽ thử rollback. Không đóng gói hoặc sửa font hiện tại.

**5. Khôi phục gốc (khi cần)**

```powershell
python src/builder/install_v08_local.py --game-root "G:/Castaway-Portable" --backup "G:/Castaway-Backup-v08" --restore --game-closed
```

Khôi phục file gốc bằng hash đã lưu. Nếu file bị một mod khác sửa sau khi cài, lệnh sẽ từ chối ghi đè ngoài ý muốn. Bản sao lưu được giữ lại. **Không cần, và không được, thay save N001/N002 để cài overlay.**

## Kiểm tra màn chọn chuyện mà không sửa save

```powershell
python src/builder/probe_story_selector.py --game-root "G:/Castaway-Portable" --save-root "C:/Users/USERNAME/Documents/Electronic Arts/The Sims Castaway Stories"
```

Thay `USERNAME`/thư mục bằng vị trí Documents thực tế (có thể là OneDrive). Đọc `work/selector_probe.json`: đối chiếu bản trong thư mục cài và bản Documents, chưa kết luận thứ tự nguồn game thực sự đọc cho đến khi có quan sát trong game hoặc file-access trace.

## Phần chưa hoàn thành

- Chưa thử các lệnh build/cài trên **10 package thật** sau source checkpoint (CI chỉ chạy dữ liệu **giả lập**); chưa có bản zip payload để gửi người dùng từ phiên chat này.
- Chưa được xác minh Story Selector hiện tiếng Việt trong game. Lệnh probe là read-only nên không sửa được lỗi tự nó.
- Chưa test thực tế game với font, Save/Load, Story Mode, Rewards, Wants, Examine/Use, vật phẩm và menu.
- Runtime overlay không cập nhật các file Text core của v0.7a; full build yêu cầu nguồn Text gốc.
- Source Audit PASS không có nghĩa là mọi nội dung kế thừa đã được triage hoặc game đã hoàn toàn Việt hóa.

Để làm bản phát hành công khai, cần **QA bằng package thật + xác nhận Windows/gameplay + installer phục hồi an toàn**. Không phát hành bản build thử tổng hợp một cách mù.
