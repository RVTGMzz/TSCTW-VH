# Translation Style Guide — TSCTW-VH

## Giọng dịch mục tiêu
Bản Việt hóa phải tự nhiên, có cá tính và vui đúng chất The Sims Castaway Stories. Không dịch từng chữ kiểu máy.

### 1. Thoại / nhật ký / độc thoại
- Ưu tiên tiếng Việt đời thường, dí dỏm, hơi Gen Z khi hợp cảnh.
- Có thể dùng những cách nói như: “u là trời”, “thiệt hông pa”, “hết cứu”, “phá mood”, “xịn”, “ổn áp”, “vui muốn xỉu”, “tới công chuyện”, “dính thiệt rồi”...
- **Không nhét slang vào mọi câu.** Mục tiêu là nghe như người thật đang nói, không phải một chuỗi meme.
- Giữ punchline, chơi chữ và nhịp hài của bản gốc; được phép chuyển ý để câu đùa hoạt động bằng tiếng Việt thay vì bám từng chữ.
- Khi cảnh chuyển sang bệnh tật, cái chết, mất mát, nguy hiểm hoặc cảm xúc chân thành, giảm slang và ưu tiên cảm xúc/ngữ cảnh.

### 2. Ngôi xưng và giới tính
- Người chơi có thể chọn nhân vật nam hoặc nữ, nên các đoạn narrator trung tính ưu tiên **“mình”**, tránh tự gán “anh/cô/tôi là đàn ông/phụ nữ” khi bản gốc không xác định.
- Với NPC có giới tính/ngôi quan hệ đã rõ trong ngữ cảnh, dịch nhất quán theo nhân vật.
- Không đoán giới tính chỉ từ tên nếu catalog không đủ bằng chứng.
- Romance với placeholder như `$NeighborLocal:2` nên dùng cấu trúc trung tính: “người ta”, “hai đứa”, “mình với $NeighborLocal:2” khi cần.

### 3. UI / tutorial / cảnh báo
- UI, nút bấm, tutorial, lỗi hệ thống và mô tả gameplay phải ngắn, rõ, dễ hiểu.
- Không Gen Z hóa những phần cần thao tác chính xác.
- Thuật ngữ gameplay phải nhất quán với các bảng đã dịch.

### 4. Tên riêng và thuật ngữ đặc thù
- Giữ nguyên tên nhân vật và địa danh riêng: David Bennett, Jessica Knight, Wanmami, Felicity, Rhinehart, Spaulding, Village Harbor, Scavenger Fields, Creepy Hollow...
- Với tên vật phẩm/di vật đặc thù như `Staff of Tuzu`, `Chalice of Days`, ưu tiên giữ nguyên cho tới khi dự án có glossary thống nhất.
- Không dịch bừa chuỗi tên người bản địa trong catalog.

### 5. Placeholder và metadata — tuyệt đối không phá
- Giữ nguyên và đúng **số lần xuất hiện** của `%s`, `%d`, `$NeighborLocal:0`, `$NeighborLocal:1`, `$NeighborLocal:2` và các token tương tự.
- Tooltip có dạng `Label|Description|metadata...`: chỉ dịch label/description; các trường metadata phía sau phải giữ nguyên.
- Giữ số lượng và kiểu xuống dòng `\r` / `\n` nếu chuỗi gốc có điều khiển bố cục.
- Trước commit phải chạy kiểm tra catalog + placeholder + metadata/line break.

## Ví dụ tone
- Dry: “Tôi đã gặp một số dân làng và nhận quà.”
- Mục tiêu: “Mình gặp thêm mấy người dân đảo cực dễ mến, lại còn được tặng quà nữa. U là trời, hôm nay lời quá.”
- Nhưng cảnh buồn không làm meme: “Bart qua đời ngay trước mắt mình...” thay vì cố chèn slang.

## Quy tắc test
Không bao giờ ghi “đã test trong game” nếu Ron chưa xác nhận trực tiếp.
