# Build notes

Repo này là **source-only**. Không commit file game, font lấy từ game, package gốc hoặc payload đã vá.

## Build v0.6 cũ

`src/builder/build_v06.py` được giữ nguyên để tái tạo bản cũ. Nó chỉ biết các bảng dịch/allowlist của v0.6 và không được dùng cho source hiện tại.

## Builder kế tiếp: build_v07.py

`src/builder/build_v07.py` là builder mới cho draft hiện tại.

Nó:
- đọc `translations/translations.json` và toàn bộ `translations/extra*.json` theo thứ tự số;
- cho phép batch sau tinh chỉnh batch trước và ghi các override vào `validation.json`;
- dùng `castaway-english-strings.json` để suy ra đúng STR# instance có chứa English key đã dịch;
- chỉ cho phép các package đã audit;
- chỉ sửa language ID 1/2;
- giữ nguyên số lượng/thứ tự string, description, ngôn ngữ khác, compression state và resource không liên quan;
- kiểm placeholder, line break, tooltip metadata, QFS round-trip và decompressed-size directory;
- giữ override ngữ cảnh `Neighborhood.package: Play → Chơi`.

### Build incremental từ bản v0.6 Ron đang dùng

Đặt đúng 7 file user-owned sau vào:

`work/text/Text/`

- `Options.package`
- `UIText.package`
- `Live.package`
- `Neighborhood.package`
- `Build.package`
- `CAS.package`
- `CAS_Shared.package`

Không cần gửi cả game. `Tutorial.package` không có delta mới sau v0.6.

Từ root repo chạy:

`python src/builder/build_v07.py`

Output:

`work/build_v07/`

gồm:
- `Payload/TSData/Res/Text/*.package`
- `manifest.json`
- `validation.json`

### Rebuild từ original baseline

Nếu **không** dùng package từ bản v0.6 đã cài mà rebuild lại từ original, cần thêm:

- `Tutorial.package`

và chạy:

`python src/builder/build_v07.py --full`

Chế độ này sẽ yêu cầu đủ 8 package và áp toàn bộ mapping nguồn hiện có.

## Lưu ý

- Builder mới đã được kiểm tra cú pháp/logic source nhưng **chưa thể chạy end-to-end** trong repo vì repo không có package game.
- Structural validation không thay thế test trong game Windows.
- Chỉ ghi “đã test trong game” khi Ron xác nhận trực tiếp.
- Font03 đang hoạt động ổn theo xác nhận trước đó; không rebuild font nếu chỉ thay text.
