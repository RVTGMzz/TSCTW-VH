# Checkpoint cho model tiếp theo

## Mục tiêu
Hoàn thiện Việt hóa The Sims Castaway Stories PC, sau đó build một bản test mới cho Ron. Giao tiếp bằng tiếng Việt thân mật, gọi là Ron; không hỏi lại thông tin đã có.

**Bắt buộc đọc `TRANSLATION_STYLE.md` trước khi dịch.**

## Trạng thái đã xác nhận
- Game portable: `G:\Castaway-Portable`.
- Font03 đã được Ron xác nhận chạy ổn; không thay font khi chỉ thêm chuỗi.
- v0.4 từng được Ron xác nhận hiển thị ổn.
- Bản đóng gói gần nhất là **Text v0.6**, 486 câu/nhãn duy nhất; **v0.6 chưa được Ron test trực tiếp đầy đủ**.
- Repo là source-only, không chứa package game/payload đã vá.
- Nguồn dịch hiện tới **`extra29`**, tổng **1.760 mapping nguồn**. Đây không phải số chuỗi đã build/test.

## Tiến độ dịch sau v0.6
- `extra07`: 127 UI/gameplay.
- `extra08`: 65 nhật ký/thoại instance 611–624.
- `extra09`: 56 nhật ký đầu game instance 601–610.
- `extra10`–`extra22`: mở rộng Castaway UI, Build/Buy, Neighborhood, CAS, Story/Camera, aspiration/attraction và base-game UI dùng lại.
- `extra23`: 102 mapping, gồm shopping/cart UI + relationship UI/tooltip.
- `extra24`: 51 mapping trường học, sở thích trò chuyện, baby popup.
- `extra25`: 97 mapping Create-a-Sim core, 12 cung hoàng đạo + mô tả tính cách.
- `extra26`: 49 mapping placement/update/loading UI.
- `extra27`: 13 moniker Khát vọng trẻ nhỏ.
- `extra28`: 19 interaction/sell/delete/capture messages.
- `extra29`: 13 nhãn CAS steps + neighborhood chooser/chuyển màn.

### Hậu kiểm gần nhất
`extra23`–`extra29`:
- 344 mapping.
- 0 duplicate key giữa các batch.
- 0 missing catalog.
- 0 placeholder mismatch.
- 0 line-break mismatch.
- 0 tooltip metadata mismatch.
- 0 ký tự Cyrillic lạc.

## Mốc audit quan trọng
Các chuỗi có **tag Castaway rõ ràng** và thực sự cần dịch đã được phủ. Phần Cast-tagged còn tiếng Anh chủ yếu là:
- danh sách tên người bản địa / tên nhân vật,
- tên địa điểm,
- key bindings/phím tắt,
- tên nhạc,
- copyright/legal ngắn.

Các mục này **không được dịch chỉ để làm đẹp tỷ lệ**.

Ngoài ra:
- `eCAS.package` chủ yếu là Body Shop/CaSIE, không phải gameplay Castaway.
- `UIText2.package` chỉ có tên expansion cũ.
- `Installer.package` là chuỗi The Sims 2 Seasons.
- `Credits.package` và phần lớn `MusicTitles.package` không phải ưu tiên gameplay.
- Catalog có rất nhiều chuỗi University/Nightlife/OFB/Pets/Seasons kế thừa nhưng không dùng trong Castaway; không dịch đại trà.

## Tone
- Thoại/nhật ký tự nhiên, vui, lém lỉnh, Gen Z vừa phải: “u là trời”, “thiệt hông pa”, “hết cứu”, “phá mood”... khi đúng cảnh.
- Không spam meme.
- Cảnh buồn/nguy hiểm/bệnh tật/cái chết/romance nghiêm túc phải hạ slang.
- Narrator dùng “mình” để giữ trung tính nam/nữ.
- NPC có giới/ngôi xưng rõ thì dịch theo ngữ cảnh.
- UI/tutorial/cảnh báo: ưu tiên rõ nghĩa và ngắn.
- Chi tiết: `TRANSLATION_STYLE.md`.

## Quy tắc kỹ thuật
1. Giữ nguyên tên riêng và các token như `%s`, `%d`, `%D`, `$NeighborLocal:n`, `$Object`.
2. Tooltip có `|`: giữ nguyên metadata phía sau phần mô tả.
3. Giữ line break điều khiển `\r` / `\n`.
4. Không dịch các chuỗi được đánh dấu DO NOT TRANSLATE hoặc expansion thừa chỉ để đạt 100%.
5. Không chỉnh package trực tiếp trong giai đoạn biên tập.
6. Không nói “đã test trong game” nếu Ron chưa xác nhận.

## Build mới
- `build_v06.py` chỉ đọc bảng cũ tới `extra06`; không sửa phá file này.
- Bản kế tiếp cần builder riêng, đọc toàn bộ mapping đã duyệt tới `extra29`.
- Nên derive target STR# instances từ `castaway-english-strings.json` + exact English keys trong mappings, rồi vẫn giữ allowlist package/resource và validation DBPF/QFS.
- Draft mới chạm các package:
  - `Options.package`
  - `UIText.package`
  - `Live.package`
  - `Neighborhood.package`
  - `Build.package`
  - `CAS.package`
  - `CAS_Shared.package`
- Nếu build **incremental từ v0.6 đang cài**, xin Ron đúng 7 file trên từ bản đang dùng. Không cần cả thư mục game. `Tutorial.package` không có delta mới.
- Nếu rebuild từ original thay vì v0.6 baseline thì phải tính lại cả phần v0.6/Tutorial và manifest rollback; không được tự đoán.

## Việc tiếp theo
1. Làm một lượt audit cuối các chuỗi base-game kế thừa có khả năng hiện thật; bỏ online service chết, Body Shop, expansion dư, names/music/legal.
2. Sau audit, tạo builder mới riêng (không phá v0.6).
3. Khi cần build, xin đúng 7 `.package` ở trên.
4. Build + validate DBPF/QFS/placeholder/other languages.
5. Gửi Ron bản test; chỉ sau khi Ron chạy game mới ghi trạng thái test.
