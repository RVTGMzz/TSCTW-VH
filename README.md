# The Sims Castaway Stories — Việt hóa

## Bản cài Windows mới nhất: v0.8 TEST, Build 66

**[TẢI TRỰC TIẾP EXE — VotriValley-Castaway-v08-TEST.exe](https://github.com/RVTGMzz/TSCTW-VH/releases/download/castaway-v08-test-windows-66/VotriValley-Castaway-v08-TEST.exe)** (khoảng 15,5 MB). Không cần Python. [GitHub Windows CI Build 66 — PASS](https://github.com/RVTGMzz/TSCTW-VH/actions/runs/37865230511). **Đây là TEST: đã thử bộ build, cài và khôi phục trên dữ liệu giả; chưa xác nhận mọi chuỗi và mọi menu trong game thật đã hiển thị tiếng Việt.**

Sau phản hồi bằng ảnh chơi thật ngày 2026-10-09, bản TEST này mở rộng việc xử lý theo **cụm**:

- **Cài Việt hóa v0.8 TEST:** vá các dòng tiếng Anh *đúng nguồn* còn trong cả package runtime và core Text, trên nền bản v0.7a; sao lưu và hỗ trợ khôi phục. Giữ nguyên font và các câu đã Việt hóa khác nguồn, ngoại trừ đúng hai câu tên/mô tả ghế đá đã được kiểm chứng để nâng cấp.
- **Việt hóa đảo & tiểu sử...**: nút **riêng, chủ động xác nhận** để dịch tài nguyên chữ N001/N002 trong save Documents. Tự backup hoàn chỉnh, không thay toàn bộ save bằng file phát hành; chỉ chạy sau khi đã thoát game.
- **Khôi phục dữ liệu đảo:** khôi phục file N001/N002 từ backup riêng; từ chối ghi đè nếu save đã phát sinh tiến trình chơi mới.
- **Rà chữ còn sót:** rà chỉ-đọc các resource còn tiếng Anh từ bản cài, gồm phần thưởng, cây trang trí và bảng Thu hút/Mất hứng. Kết hợp **Lưu báo cáo...** để gửi kết quả; báo cáo có thể chứa đường dẫn Windows cá nhân, nên kiểm tra trước khi chia sẻ.

Cụm đã chỉnh nguồn: tên **Đảo Wanmami**, tên khu vực **Mũi Giáo** (`Spear Point`), tên/mô tả **Ghế đá đôi Êm Một Bên**, phần thưởng **Thuốc trường sinh** và hướng dẫn Thu hút/Mất hứng theo đúng package owner. **Chưa khẳng định** đã xử lý nhóm `Pine Tree`, `Row of Trees`, cảnh báo Gold Aspiration hay dòng **“Việt hóa bởi Votri Valley” trong game** vì chưa xác minh được vị trí/chủ sở hữu tài nguyên màn hình; không sửa bừa logo hoặc Credits của EA.

[Xem hướng dẫn thao tác và phục hồi](CLICK_TO_INSTALL_WINDOWS.md) · [Audit theo ảnh và nguồn còn thiếu](runtime/SCREENSHOT_FAMILY_AUDIT_2026-10-09.md).

> Ghi chú lịch sử trong các mục dưới nói về các build cũ, không phải trạng thái phát hành mới nhất.

Bản dịch cộng đồng cho bản PC.

## Trạng thái

- Bản phát hành đã đóng gói gần nhất: **Text v0.6 — 486 câu/nhãn duy nhất**. Font03 đã được Ron xác nhận hoạt động ổn.
- Ron đã test các build mới hơn v0.6 trong game; xem mục **Runtime test / hướng đi mới** bên dưới.
- Nguồn dịch hiện đi tới **`extra44`**.
- **Source audit v0.7 đã PASS trên GitHub Actions ngày 2026-10-04:** 1.774 mapping sau merge, 1.774/1.774 key hiện diện trong package allowlist, 0 key thiếu khỏi catalog. Có 274 override có chủ đích giữa các batch.\n- Không dùng số unique mapping ghi tay; chạy `python src/builder/build_v07.py --audit-only` để tái kiểm bất cứ lúc nào.
- Repo không chứa package game/payload; các build test v0.7/v0.7a/v0.7b đã được tạo ngoài repo từ package Ron cung cấp.

## Phạm vi đã phủ

Ngoài nhật ký/cốt truyện Castaway, source hiện đã phủ phần lớn UI dùng thật:
- Buy Mode / Build Mode categories, công cụ, tooltip và lỗi đặt vật thể.
- Create-a-Sim: các bước tạo Sim, giới tính/tuổi, tóc, mặt, trang điểm, quần áo, cung hoàng đạo và tính cách.
- Neighborhood: gia đình, khu đất, đổi/xóa khu phố, lot management.
- Simology: Khát vọng, mức Khát vọng, quan hệ, trường học, sở thích, lịch làm việc.
- Story/Camera, Inventory, Collection, system/loading messages.
- Popup save/quit, tutorial nhanh, battery warning và các thông báo Castaway thường gặp.
- Thoại/popup được Việt hóa tự nhiên, vui và hơi Gen Z theo style guide khi phù hợp.

Toàn bộ chuỗi **gắn tag Castaway rõ ràng và có nội dung cần dịch** đã được xử lý. Những mục Cast-tagged còn tiếng Anh chủ yếu là **tên riêng/địa điểm, phím tắt, tên nhạc và copyright**, được cố ý giữ nguyên.

Các package như `eCAS.package` (Body Shop), `UIText2.package` (nhãn expansion) và `Installer.package` (chuỗi Seasons) là di sản không thuộc gameplay Castaway nên không dịch đại trà.

## Runtime test / hướng đi mới

Ron đã test các build v0.7/v0.7a/v0.7b trong game. UI Text cũ hiển thị tiếng Việt, nhưng test xác nhận còn nhiều text player-facing nằm ngoài source catalog ban đầu, đặc biệt trong `objects.package`, Text `Wants.package` và neighborhood/runtime data.

Vì vậy trạng thái hiện tại là: **core Text source sweep hoàn tất, nhưng runtime sweep chưa hoàn tất**. Từ 2026-10-05 dự án chuyển sang audit runtime toàn diện thay vì vá từng screenshot.

Xem:
- [RUNTIME_AUDIT.md](RUNTIME_AUDIT.md)
- [NEXT_SESSION_PROMPT.md](NEXT_SESSION_PROMPT.md)
- [runtime/known_runtime_strings.json](runtime/known_runtime_strings.json)

Mục tiêu kế tiếp: persist catalog + translation runtime có thể tái lập, sau đó build một bản tổng hợp **v0.8 TEST**.

## Phong cách dịch

Đọc [`TRANSLATION_STYLE.md`](TRANSLATION_STYLE.md).

- Thoại/nhật ký: tự nhiên, có cá tính, Gen Z vừa phải khi hợp cảnh.
- Narrator ưu tiên “mình” để trung tính giới tính.
- Cảnh buồn/nguy hiểm/tình cảm nghiêm túc phải hạ slang.
- UI/tutorial/cảnh báo vẫn ngắn, rõ và chính xác.
- Không phá placeholder, metadata tooltip hoặc line break điều khiển.

## Kiểm tra source

`extra23`–`extra29` đã được audit ở mốc trước. `extra32`–`extra42` bổ sung Build/Buy tools, object stats, Castaway Needs, animal motives, Simology/skills/career, tên chương, Player Profile, mô tả Wanmami, Barter và shortcut UI. `extra43`–`extra44` là lượt cleanup cuối cho Story/Neighborhood và hai popup hệ thống còn hữu ích.

Builder v0.7 nay có `--audit-only` để merge và kiểm toàn bộ source mà không cần package game; audit còn phát hiện placeholder/line-break/tooltip metadata sai và ký tự Cyrillic lạc. Workflow `.github/workflows/source-audit.yml` tự chạy audit khi source dịch, catalog hoặc builder thay đổi.

### Audit hoàn thiện source

Đã rà theo package sau khi merge các batch liên quan:
- **Options**: phần còn tiếng Anh chỉ là 16/32-bit và tên thể loại nhạc.
- **Neighborhood**: còn dịch vụ TheSims2.com cũ / College không dùng; gameplay UI đã phủ.
- **CAS**: các mục còn lại là placeholder nội bộ hoặc key đã được dịch ở bảng dùng chung.
- **Build**: chỉ còn số giá, tile trùng bị đánh dấu xóa và placeholder developer.
- **Live**: còn tên bản địa, điểm A–F, ký hiệu thứ, University/Pets/PlantSim và token nội bộ.
- **UIText**: phần còn lại chủ yếu là Exchange/TheSims2.com, Sims 1 import cũ, album Pleasantview/Veronaville/Strangetown, expansion/Body Shop hoặc tên sản phẩm.

Vì vậy **core translation sweep được xem là hoàn tất ở mức source**; tiếng Anh còn lại không được dịch chỉ để chạy theo tỷ lệ phần trăm.

## Build / test

Builder mới đã có tại **`src/builder/build_v07.py`**; `build_v06.py` được giữ nguyên.

`build_v07.py`:
- đọc `translations.json` và toàn bộ `extra*.json` theo thứ tự số;
- ghi lại override của batch sau;
- dùng catalog để suy ra STR# instance cần sửa;
- giữ allowlist package đã audit;
- bảo toàn language khác, description, string order/count và compression state;
- kiểm placeholder, line break, tooltip metadata, DBPF/QFS round-trip;
- giữ rule ngữ cảnh `Neighborhood.package: Play → Chơi`;
- có `--audit-only` để kiểm source mà không cần package game;
- nhận diện các câu đã dịch trong baseline v0.6 theo package/resource/ngôn ngữ bằng `validation.json`; giá trị mơ hồ không bị áp sai ngữ cảnh.

Builder Text v0.7 đã được chạy với package Ron cung cấp và build test đã được Ron cài/chạy trong game. Tuy nhiên builder này **chỉ phủ nhóm Text package cũ**; runtime sweep mới phát hiện thêm nhiều player-facing resource ngoài scope đó. Vì vậy không được coi v0.7 là bản hoàn thiện.

Build incremental từ v0.6 hiện cần đúng 7 file:
- `Options.package`
- `UIText.package`
- `Live.package`
- `Neighborhood.package`
- `Build.package`
- `CAS.package`
- `CAS_Shared.package`

Không cần cả thư mục game. `Tutorial.package` chỉ cần nếu rebuild full từ original baseline.

Chi tiết: [`BUILD.md`](BUILD.md).

## Thư mục

- `translations/`: bảng dịch nền và batch bổ sung tới `extra44`.
- `src/builder/`: parser DBPF/QFS và builder.
- `installer-source/`: nguồn installer/manifest của v0.6; payload không nằm trong repo.
- `castaway-english-strings.json`: catalog tiếng Anh dùng để audit; không phải package game.
- `validation.json`: validation của build v0.6, chưa đại diện cho draft hiện tại.

Chỉ ghi “đã test trong game” khi Ron xác nhận trực tiếp.


### Runtime sweep checkpoint (2026-10-05)

Runtime source, reproducible package audit and development QA are available in [`runtime/README.md`](runtime/README.md). See [`runtime/coverage.json`](runtime/coverage.json) for exact translated/missing/review counts. This checkpoint is incomplete; **v0.8 TEST has not been released**. Core translation history is preserved. Story-selector runtime source remains under investigation.
