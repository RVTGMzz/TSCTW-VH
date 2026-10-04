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
- Nguồn dịch hiện tới **`extra44`**.
- Không dùng số merged mapping ghi tay nữa; chạy `python src/builder/build_v07.py --audit-only` để lấy số chính xác.

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
- `extra32`: 37 Build/Buy tools + object stat labels/tooltips.
- `extra33`: 33 Castaway Needs + animal motives.
- `extra34`: 40 Simology/skills/career/status strings.
- `extra35`: 50 tên chương/section Castaway.
- `extra36`: 8 Player Profile + residential-lot warning.
- `extra37`: 3 Collection/Wanmami neighborhood descriptions.
- `extra38`: 7 Barter Mode + alternate skill tooltip resource IDs.
- `extra39`: 12 phone/party UI.
- `extra40`: 2 CAS name-entry labels.
- `extra41`: 104 shortcut/help/controls + Castaway misc UI.
- `extra42`: 29 control-panel/keybind labels.
- `extra43`: 10 Story/Neighborhood/core UI cleanup.
- `extra44`: 2 popup hệ thống cuối: application crash + missing required content.

### Hậu kiểm
`extra23`–`extra29`: 344 mapping, 0 duplicate nội bộ, 0 missing catalog, 0 placeholder mismatch, 0 line-break mismatch, 0 tooltip metadata mismatch, 0 Cyrillic stray.

## Audit theo package — source sweep hoàn tất
- **Options.package**: semantic audit sạch; phần còn tiếng Anh là 16/32-bit và tên thể loại nhạc, giữ nguyên.
- **Neighborhood.package**: gameplay UI sạch; phần còn lại là TheSims2.com/College không dùng hoặc key dùng chung đã dịch.
- **CAS.package**: gameplay UI sạch; phần còn lại là placeholder nội bộ hoặc key dùng chung đã dịch.
- **Build.package**: gameplay UI sạch; chỉ còn số giá, duplicate catalog bị đánh dấu xóa và developer placeholder.
- **Live.package**: gameplay Castaway sạch; phần còn lại là Cast Names, grades/day initials, PlantSim/University/Pets hoặc token nội bộ.
- **UIText.package**: phần hữu ích đã phủ; phần còn lại chủ yếu là dead Exchange/web, Sims 1 import, base-Sims2 neighborhood albums, expansion/Body Shop/legal/internal strings.

Không dịch các nhóm trên chỉ để tăng % dịch. Bước có giá trị tiếp theo là build/test thực tế rồi sửa theo những chuỗi thật sự còn lòi trong game.

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

## Tone pass mới nhất
- Đã rà lại `extra08`–`extra09`: narrator dùng **“mình”** trung tính giới tính; các ngôi “ông/anh” còn lại đều gắn với NPC/đối tượng có giới rõ trong ngữ cảnh gốc.
- Thoại/nhật ký giữ chất nói tự nhiên, có thể dùng code-switching Gen Z vừa phải như “KPI”, “fail”, “offer”, “DIY” khi câu đùa hợp ngữ cảnh; không nhét vào cảnh nghiêm túc.
- `extra35` là batch cuối override tiêu đề chương; đã punch-up một số title: **“Tui Sẽ Sống Sót”**, **“Tới Công Chuyện Rồi”**, **“Con Mắt Ràng Buộc”**, **“Vẫn Chưa Tìm Được Thứ Mình Muốn”**.
- Khi chỉnh file batch đã tồn tại phải **merge/superset**, không replace mù. Đã khôi phục các key cũ từng bị rơi ở `extra26` và `extra28`.

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
- có `--audit-only` để merge/validate source không cần package game;
- audit-only kiểm placeholder, line break, tooltip metadata, catalog presence và ký tự Cyrillic lạc;
- output `work/build_v07/Payload/...`, `manifest.json`, `validation.json`.

`--audit-only` đã được thêm vào builder; source đã được review và sửa lỗi thiếu khai báo regex Cyrillic. Builder vẫn **chưa chạy end-to-end với package thật** vì repo không có package game.

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
**Core translation sweep đã hoàn tất ở mức source và đủ để bước sang build test đầu tiên.**
1. Nhận đúng 7 package từ bản Ron đang dùng: Options, UIText, Live, Neighborhood, Build, CAS, CAS_Shared.
2. Chạy source audit/build v0.7 và đọc `validation.json`; sửa mọi lỗi trước khi đóng gói.
3. Gửi bản test cho Ron và ghi lại mọi tiếng Anh còn lòi, chuỗi bị cắt hoặc ngữ cảnh sai.
4. Chỉ sau khi Ron chạy game mới cập nhật trạng thái “tested”.
