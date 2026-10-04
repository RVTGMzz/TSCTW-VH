# Checkpoint cho model tiếp theo

## Mục tiêu
Hoàn thiện Việt hóa The Sims Castaway Stories PC, build một bản test mới, rồi để Ron test thực tế. Giao tiếp bằng tiếng Việt thân mật, gọi là Ron; không hỏi lại thông tin đã có.

**Bắt buộc đọc `TRANSLATION_STYLE.md` và `BUILD.md` trước khi làm tiếp.**

## Trạng thái đã xác nhận
- Game portable: `G:\Castaway-Portable`.
- Font03 đã được Ron xác nhận chạy ổn; không thay font khi chỉ thêm chuỗi.
- v0.4 từng được Ron xác nhận hiển thị ổn.
- Bản đóng gói gần nhất là **Text v0.6**, 486 câu/nhãn duy nhất; **v0.6 chưa được Ron test trực tiếp đầy đủ**.
- Repo source-only, không chứa package game/payload đã vá.
- Nguồn dịch hiện tới **`extra31`**.
- Tổng **unique mapping nguồn: 1.760**. `extra30` và `extra31` chỉ override/xác nhận key đã có nên không tăng unique count.

## Tiến độ dịch
- `extra07`: 127 UI/gameplay.
- `extra08`: 65 nhật ký/thoại instance 611–624.
- `extra09`: 56 nhật ký đầu game instance 601–610.
- `extra10`–`extra22`: Castaway UI, Build/Buy, Neighborhood, CAS, Story/Camera, aspiration/attraction và base-game UI dùng lại.
- `extra23`: 102 mapping shopping/cart + relationship UI/tooltip.
- `extra24`: 51 trường học, sở thích trò chuyện, baby popup.
- `extra25`: 97 Create-a-Sim core, 12 cung hoàng đạo + mô tả tính cách.
- `extra26`: 49 placement/update/loading UI.
- `extra27`: 13 moniker Khát vọng trẻ nhỏ.
- `extra28`: 19 interaction/sell/delete/capture messages.
- `extra29`: 13 CAS steps + neighborhood chooser/chuyển màn.
- `extra30`: 15 tinh chỉnh save/quit/tutorial/battery/lot prompts — tất cả là override của key đã có.
- `extra31`: 15 nhãn ngày/tuần — xác nhận giống bảng nền, không tăng unique.

### Hậu kiểm
`extra23`–`extra29`: 344 mapping, 0 duplicate nội bộ, 0 missing catalog, 0 placeholder mismatch, 0 line-break mismatch, 0 tooltip metadata mismatch, 0 Cyrillic stray.

## Mốc audit quan trọng
Các chuỗi **tag Castaway rõ ràng và thật sự cần dịch** đã được phủ. Cast-tagged còn tiếng Anh chủ yếu là:
- tên người bản địa / tên nhân vật,
- tên địa điểm,
- key bindings/phím tắt,
- tên nhạc,
- copyright/legal ngắn.

Không dịch các mục này chỉ để làm đẹp tỷ lệ.

Các nhóm cố ý bỏ qua:
- `eCAS.package`: Body Shop/CaSIE.
- `UIText2.package`: tên expansion cũ.
- `Installer.package`: chuỗi Seasons.
- `Credits.package`, phần lớn `MusicTitles.package`.
- University/Nightlife/OFB/Pets/Seasons thừa kế không dùng trong Castaway.
- online service/Exchange đã chết nếu không ảnh hưởng gameplay.

## Tone
- Thoại/nhật ký tự nhiên, vui, lém lỉnh, Gen Z vừa phải.
- Không spam meme.
- Cảnh buồn/nguy hiểm/bệnh tật/cái chết/romance nghiêm túc phải hạ slang.
- Narrator dùng “mình” để trung tính giới tính.
- NPC có giới/ngôi xưng rõ thì dịch theo ngữ cảnh.
- UI/tutorial/cảnh báo: rõ, ngắn, chính xác.

## Quy tắc kỹ thuật
1. Giữ nguyên tên riêng và token `%s`, `%d`, `%D`, `$NeighborLocal:n`, `$Object`.
2. Tooltip có `|`: giữ nguyên metadata sau mô tả.
3. Giữ line break `\r` / `\n`.
4. Không dịch DO NOT TRANSLATE / expansion rác.
5. Không ghi “đã test trong game” nếu Ron chưa xác nhận.

## Builder mới — đã có
File: **`src/builder/build_v07.py`**.

Builder:
- đọc `translations/translations.json` + mọi `extra*.json` theo thứ tự số;
- batch sau được phép tinh chỉnh batch trước; override được ghi vào validation;
- derive target STR# từ catalog + exact English key;
- chỉ patch language ID 1/2 trong package allowlist;
- bảo toàn description, other languages, resource order/count, compression state và untouched bytes;
- kiểm DBPF/QFS round-trip, decompressed-size directory, placeholder, line break, tooltip metadata;
- giữ package-specific override `Neighborhood.package: Play → Chơi`;
- output `work/build_v07/Payload/...`, `manifest.json`, `validation.json`.

**Chưa chạy end-to-end** do repo không có package thật. Đây là blocker hiện tại cho build/test, không phải thiếu source dịch.

### Package cần khi build incremental từ v0.6
Chỉ cần 7 file từ bản Ron đang dùng:
- `Options.package`
- `UIText.package`
- `Live.package`
- `Neighborhood.package`
- `Build.package`
- `CAS.package`
- `CAS_Shared.package`

Không cần cả thư mục game. `Tutorial.package` chỉ cần nếu chạy `--full` từ original baseline.

## Việc tiếp theo
1. Audit cuối các base-game strings có khả năng hiện thật, nhưng **tra source trước khi tạo batch mới** để tránh lặp key như extra30/31.
2. Khi audit đạt mốc hợp lý, xin Ron đúng 7 package trên.
3. Chạy `build_v07.py`, đọc validation và sửa mọi lỗi trước khi đóng gói.
4. Gửi bản test cho Ron.
5. Chỉ sau khi Ron chạy game mới cập nhật trạng thái “tested”.
