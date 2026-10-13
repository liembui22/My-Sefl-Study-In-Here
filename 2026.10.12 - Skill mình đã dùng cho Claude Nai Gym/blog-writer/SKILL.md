---
name: blog-writer
description: Viết bài blog chuyên sâu (deep-dive) cho NaiGym theo đúng giọng thương hiệu The Sage — kết hợp cơ chế khoa học/sinh cơ học, tâm lý học hành vi, sự đồng cảm và bảo vệ sức khỏe người tập, dựa trên bài mẫu và bố cục chuẩn đã có. Kèm theo tạo creative brief cho ảnh bìa theo đúng quy trình thiết kế 5 bước và bảng màu/font thương hiệu. Dùng skill này bất cứ khi nào cần viết bài blog/bài viết chuyên sâu về dinh dưỡng, tập luyện, phục hồi, tâm lý tập luyện, hoặc bất kỳ chủ đề kiến thức thể hình nào cho NaiGym — kể cả khi chỉ được giao một chủ đề ngắn gọn chưa có dàn ý.
---

# Blog Writer — Bài viết chuyên sâu NaiGym

## Vì sao skill này tồn tại
NaiGym định vị thương hiệu theo hình mẫu **The Sage** (xem [`brand-voice.md`](../../domains/brand/brand-voice.md)): hiểu sâu trước khi dạy, giáo dục thay vì áp đặt. Bài blog là điểm chạm nơi tinh thần này thể hiện rõ nhất — không phải bài quảng cáo trá hình, mà là kiến thức thật, có trích dẫn thật, viết bằng giọng đồng cảm thật. Skill này đảm bảo mọi bài blog đều đi qua đúng bố cục, đúng giọng văn, và đúng quy tắc trích dẫn đã được rút ra từ bài mẫu NaiGym cung cấp — thay vì mỗi bài một kiểu, loãng dần bản sắc thương hiệu.

**Đây là Yellow Zone** (xem [`zones.md`](../../workflow/zones.md)): luôn trình bày bài viết đầy đủ trong chat để PT/chủ phòng gym đọc và duyệt trước, KHÔNG tự động xuất file hay coi như đã sẵn sàng đăng khi chưa có xác nhận — bài blog là nội dung công khai đại diện thương hiệu.

## Khi nào dừng lại hỏi thay vì tự viết (Stop Rule áp dụng ở đây)
- Chủ đề được giao quá ngắn/mơ hồ, không đủ để xác định trụ nội dung nào áp dụng (xem `references/content-pillars.md`) → hỏi lại để làm rõ góc tiếp cận trước khi viết.
- Chủ đề đòi hỏi trích dẫn nghiên cứu/số liệu khoa học cụ thể nhưng không tìm được nguồn xác thực (đã thử WebSearch) → KHÔNG bịa tên nghiên cứu/tác giả/số liệu, báo lại cho người giao bài biết phần nào chưa có nguồn chắc chắn thay vì tự lấp đầy.
- Chủ đề chạm ranh giới an toàn (cường độ tập cực đoan, nhịn ăn, thực phẩm bổ sung liều cao, chấn thương) → viết thận trọng theo đúng Trụ "Bảo vệ sức khỏe bản thân", không cổ súy dù chủ đề có vẻ "hot"/dễ viral.
- PT/chủ phòng gym chưa xác nhận bài viết trong chat mà đã yêu cầu xuất file/đăng → dừng lại, nhắc rằng cần duyệt trước (Yellow Zone).

## Quy trình

### 1. Xác định chủ đề & trụ nội dung
Đọc chủ đề được giao, xác định trụ nào trong 4 trụ áp dụng (xem [`references/content-pillars.md`](references/content-pillars.md)). Nếu chủ đề đòi hỏi kiến thức chuyên sâu mà chưa chắc chắn (số liệu, cơ chế sinh lý, nghiên cứu), dùng WebSearch để kiểm tra/bổ sung trước khi viết — không viết từ suy đoán khi chủ đề mang tính khoa học.

### 2. Viết theo bố cục chuẩn
Theo đúng khung trong [`references/structure-template.md`](references/structure-template.md): Tiêu đề → Câu giới thiệu (hook) → Đặt vấn đề → Chia Mục (2–4 mục) → Kết bài. Viết đúng giọng văn theo [`references/writing-voice.md`](references/writing-voice.md) — đặc biệt quy tắc trích dẫn (mục 2) và quy tắc con số cụ thể (mục 3) là BẮT BUỘC, không phải gợi ý.

Khi cần đối chiếu cụ thể cách một đoạn nên đọc ra sao, xem lại [`references/sample-blog-protein.md`](references/sample-blog-protein.md) — đây là chuẩn giọng văn thật của NaiGym, không phải bài để copy nội dung.

### 3. Trình bày bài viết trong chat để duyệt
Dán toàn bộ bài viết (đủ Tiêu đề → Kết bài) trực tiếp trong chat, KHÔNG xuất file ngay. Ghi rõ trụ nội dung nào đã áp dụng và nguồn trích dẫn nào đã dùng (kèm link nếu tra cứu qua WebSearch) để PT/chủ phòng gym dễ kiểm tra lại trước khi duyệt.

### 4. Tạo creative brief cho ảnh bìa
Ngay sau bài viết (cùng lượt trình bày), viết một creative brief theo đúng 5 bước trong [`references/image-brief-template.md`](references/image-brief-template.md), rút từ khóa/quote trực tiếp từ bài vừa viết. Đây là brief để PT/designer tự dựng ảnh — skill này không tự tạo file ảnh hoàn chỉnh.

### 5. Xuất file .docx khi đã duyệt
Chỉ khi PT/chủ phòng gym xác nhận bài viết ổn ("chốt", "ok xuất file", hoặc tương đương), dùng skill `docx` sẵn có để xuất file, áp dụng đúng brand tại [`.claude/domains/brand/brand-identity.md`](../../domains/brand/brand-identity.md):
- Logo NaiGym (`logo-full.png` hoặc `logo-mark.png`) ở đầu trang.
- Tiêu đề: SVN-Hemi Head (hoặc font thay thế gần nhất nếu không có sẵn), màu `#232323`, có thể nhấn viền dưới màu `#f59322` giống mẫu tài liệu SOP đã có.
- Nội dung: Be Vietnam Pro, màu `#232323`.
- Cân nhắc chèn 1 pull-quote nổi bật giữa bài (câu myth-busting hoặc câu trao quyền mạnh nhất) bằng font Dancing Script, màu `#ffd10c` — tạo sự nhất quán thị giác với ảnh bìa (xem Bước 4 trong `image-brief-template.md`, "Điểm chạm 2").
- Xuất xong, xác minh lại bằng bước render PDF + xem ảnh trang theo đúng quy trình của skill `docx` trước khi gửi.

## Tài liệu tham khảo trong skill này
| File | Nội dung |
|---|---|
| `references/content-pillars.md` | 4 trụ nội dung (cơ chế sinh học, tâm lý hành vi, đồng cảm, bảo vệ sức khỏe) và cách chọn trụ theo chủ đề |
| `references/structure-template.md` | Khung bố cục chuẩn: Tiêu đề, Hook, Đặt vấn đề, Chia Mục, Kết bài — tổng quát hóa từ bài mẫu |
| `references/writing-voice.md` | Các khuôn mẫu giọng văn cụ thể + quy tắc bắt buộc về trích dẫn khoa học và số liệu |
| `references/sample-blog-protein.md` | Bài mẫu đầy đủ do NaiGym cung cấp — chuẩn đối chiếu giọng văn |
| `references/image-brief-template.md` | Quy trình 5 bước tạo creative brief cho ảnh bìa, kèm bảng màu/font thương hiệu |
