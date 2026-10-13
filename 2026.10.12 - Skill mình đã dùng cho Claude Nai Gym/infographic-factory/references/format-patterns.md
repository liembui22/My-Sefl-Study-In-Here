# Layout & Format — chọn bố cục cho từng slide

> Bố cục được tổng quát hoá từ ảnh mẫu NaiGym cung cấp và từ các lô reel đã làm. Không copy màu, font, logo hay nội dung của thương hiệu khác. Mọi layout đều dùng hệ màu/font NaiGym và có sẵn trong `scripts/render_infographic.py`.

## Slide 1 — Hook (`"type": "hook"`, trường `layout`)

| layout | Trông như thế nào | Hợp khi |
|---|---|---|
| `photo` | Ảnh thật tràn khung, phủ tối dần, headline ở dưới | Có ảnh hội viên/không gian đẹp — mặc định khi có ảnh |
| `split` | Chữ bên trái, ảnh dọc bên phải, nền sáng | Muốn sạch, nhẹ hơn photo |
| `poster` | Nền tối, chữ lớn, không ảnh | Câu hook đủ mạnh tự đứng |
| `question` | Nền vàng, dấu "?" khổng lồ làm nền | Câu hỏi / quan niệm phổ biến |
| `chat` | Bong bóng tin nhắn hội viên ↔ NaiGym trên ảnh mờ | Dạng hỏi–đáp FAQ |
| `versus` | Chia đôi A (sáng) / B (tối) + vòng VS | So sánh 2 lựa chọn |

## Slide 2 — Nội dung (`"type": "value"`, trường `format`)

| format | Cấu trúc | Hợp khi | Giới hạn |
|---|---|---|---|
| `checklist` | Danh sách đánh số, mỗi mục 1 dòng chính + 1 dòng phụ | Việc nên làm / tránh, các bước | ≤ 5 mục |
| `grid` | Lưới 2×2 hoặc 3×2 thẻ có icon | 4–6 ý ngang hàng ngắn | 4 hoặc 6 ô |
| `radial` | Vòng tròn trung tâm + nhánh có icon | Các thành phần của một nhóm | ≤ 6 nhánh |
| `comparison` | 3 cột Good / Better / Best | Có trục mức độ tăng dần | 3 cột, luôn có câu "mức nào cũng hợp lệ" |
| `myth-bust` | Khối "quan niệm sai" gạch ngang → "sự thật" + cơ chế | Đập tan hiểu lầm (Trụ 1 + 4) | Mọi claim phải có nguồn |
| `timeline` | Thanh thời gian 3–4 mốc | Diễn biến theo thời gian (trong hiệp → vài giờ → vài ngày) | ≤ 4 mốc |
| `stat` | Một con số khổng lồ + diễn giải | Một số liệu có nguồn, đủ ấn tượng | Chỉ dùng số có nguồn |
| `flow` | Câu hỏi → nhánh CÓ / KHÔNG | Quyết định theo tình huống | 2 nhánh |

Mọi format nhận thêm `"note"` (một dòng chú thích cuối) và `"theme": "dark" | "light" | "yellow"`.

## Slide 3 — CTA (`"type": "cta"`, trường `layout`)

| layout | Trông như thế nào |
|---|---|
| `split` | Câu đúc kết + nút bên trái, ảnh dọc bên phải (mặc định khi có ảnh) |
| `band` | Chữ + nút ở trên, dải ảnh rộng ở dưới |
| `solid` | Nền vàng/tối, chỉ chữ + nút (khi không có ảnh) |

## Xoay vòng bố cục trong một lô
- Không để 2 reel liền nhau dùng cùng layout hook **và** cùng format nội dung.
- Trộn nền: một lô nên có cả slide tối, sáng và vàng — tránh cả lô một màu.
- Mỗi lô nên có ≥ 50% hook dùng ảnh thật (`photo`, `split`, `chat`).
- Gợi ý vòng xoay cho lô 6 reel: `photo+checklist` → `chat+timeline` → `versus+flow` → `question+grid` → `split+myth-bust` → `poster+stat`.

## Chọn format khi chủ đề khớp nhiều kiểu
1. Có hiểu lầm phổ biến + cơ chế khoa học → `myth-bust`.
2. Diễn biến theo thời gian → `timeline`.
3. Quyết định "nếu… thì…" → `flow`.
4. Các ý ngang hàng → `grid` (ngắn) hoặc `radial` (là thành phần của một nhóm).
5. Có trục mức độ → `comparison`.
6. Còn lại → `checklist` (an toàn nhất).
