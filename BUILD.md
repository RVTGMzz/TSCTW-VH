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
- giữ override ngữ cảnh `Neighborhood.package: Play → Chơi`;
- có `--audit-only` để merge và kiểm source mà không cần package game;
- audit-only kiểm placeholder, line break, tooltip metadata, catalog presence và ký tự Cyrillic lạc.

### Audit source trước khi build

Từ root repo chạy:

`python src/builder/build_v07.py --audit-only`

Lệnh này **không cần file `.package`**. Kết quả ghi vào:

`work/build_v07/source_audit.json`

Nên chạy audit-only trước mọi build test mới. Repo còn có workflow `.github/workflows/source-audit.yml` để tự chạy kiểm tra này khi source dịch, catalog hoặc builder thay đổi.\n\nMốc CI 2026-10-04: **PASS**, 1.774 mapping sau merge; 1.774 key thuộc package allowlist; 0 key thiếu khỏi catalog.

### Build incremental từ bản v0.6 Ron đang dùng

> **CẢNH BÁO 2026-10-04:** bản `build_v07.py` hiện trên repo vẫn có lỗi incremental với các key đã được Việt hóa ở v0.6 rồi bị batch sau override. Bản test v0.7 đầu tiên đã được build bằng logic sửa context-aware và idempotency PASS. Trước lần build incremental tiếp theo, phải tích hợp fix dựa trên `validation.json` v0.6 để nhận diện `(package, STR# instance, language, old_vi) → English source`. Không dùng nguyên logic `value in translations` cho baseline v0.6.


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

- Builder mới đã được review source và sửa lỗi khai báo regex trong audit mode, nhưng **chưa được thực thi end-to-end trong runtime repo ở phiên hiện tại**. Build package thật vẫn cần file game do người dùng cung cấp.
- Structural validation không thay thế test trong game Windows.
- Chỉ ghi “đã test trong game” khi Ron xác nhận trực tiếp.
- Font03 đang hoạt động ổn theo xác nhận trước đó; không rebuild font nếu chỉ thay text.
