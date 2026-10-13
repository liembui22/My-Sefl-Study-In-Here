---
name: infographic-factory
description: Sản xuất hàng loạt carousel/infographic 3 slide cho NaiGym (Hook / Nội dung / CTA) — từ chọn chủ đề, viết kịch bản dễ hiểu, ghép ảnh thật của phòng gym, render PNG đúng brand, tự soát lỗi chữ, tới xuất thư mục reel-NN kèm caption. Dùng khi được giao làm "reel", "carousel", "infographic", "content lấp lịch đăng" hoặc một danh sách chủ đề cần lên nội dung theo lô.
---

# Infographic Factory — Sản xuất hàng loạt infographic NaiGym (v2)

## Vì sao skill này tồn tại
NaiGym cần nguồn nội dung "lấp đầy" khi không kịp làm bài dài/video: carousel ngắn, dễ tiêu thụ, vẫn đúng giọng **The Sage** (xem [`brand-voice.md`](../../domains/brand/brand-voice.md)) — dạy trước khi bán, dựa trên hiểu biết thật chứ không giật tít rỗng. Skill dùng lại 4 trụ nội dung của [`blog-writer`](../blog-writer/SKILL.md) để bài dài và infographic không lệch pha, và luôn ra **ảnh PNG thật** đúng kích thước nền tảng.

**Yellow Zone** (xem [`zones.md`](../../workflow/zones.md)): luôn trình bày kịch bản + ảnh render để PT/chủ phòng gym duyệt. KHÔNG tự đăng, KHÔNG coi là đã chốt khi chưa có xác nhận.

## 5 nguyên tắc rút ra từ các lô đã làm (đọc trước tiên)
1. **Dễ hiểu nhất có thể.** Không để viết tắt chuyên môn trần (RPE, DOMS, GI, 1RM, HIIT, TEF, FITT-VP, PAR-Q…) trên slide. Viết bằng tiếng Việt đời thường, hoặc giải thích ngay bên cạnh. Bảng thay thế: [`references/plain-language.md`](references/plain-language.md). Script tự cảnh báo khi gặp.
2. **Chữ không được đè nhau, không quá to.** Giữ trong giới hạn cỡ chữ ở mục "Quy cách chữ" bên dưới; script tự đo và báo lỗi "chữ đè nhau / tràn khung / bị cắt".
3. **Mỗi reel một bố cục khác.** Trong cùng một lô, không lặp lại cùng cặp layout hook + format nội dung ở 2 reel liền nhau. Xoay vòng giữa các layout ở [`references/format-patterns.md`](references/format-patterns.md).
4. **Ưu tiên ảnh thật của NaiGym.** Ghép ảnh từ kho ảnh phòng gym (thư mục *Source Edit hình ảnh*) vào hook/CTA. Ảnh phải là ảnh thật của NaiGym — không dùng ảnh AI, không ghi tên người trong ảnh, không dùng ảnh thi đấu/huy chương cho chủ đề không liên quan.
5. **Không bịa số, không trùng chủ đề.** Mọi con số phải có nguồn (tài liệu NaiGym: Blog, FAQ, kế hoạch… hoặc nghiên cứu xác minh được). Trước khi lên lô mới, đọc `_danh-sach*.txt` trong thư mục *Reel infographic* để không làm lại chủ đề đã có.

## Khi nào dừng lại hỏi (Stop Rule)
- Chủ đề không khớp rõ trụ nào ở [`references/content-mapping.md`](references/content-mapping.md) → hỏi lại, không ép.
- Cần số liệu nhưng không có nguồn → diễn đạt định tính ("phần lớn", "nhiều trường hợp") hoặc báo phần chưa có nguồn. Không bịa.
- CTA trỏ tới kênh/công cụ chưa tồn tại (calculator, lộ trình tự động, chatbot…) → chỉ dùng CTA thật, xem [`references/cta-caption-rules.md`](references/cta-caption-rules.md).
- Chủ đề chạm ranh giới an toàn (mang thai, chấn thương, nhịn ăn, cường độ cực đoan, trẻ vị thành niên) → áp Trụ 4, gắn nhãn "cần duyệt kỹ" khi trình bày, luôn có câu khuyên hỏi bác sĩ/chuyên gia.
- Nội dung về chương trình/quy trình PT chưa áp dụng thật (vd giai đoạn chuẩn hoá) → gắn nhãn "chỉ đăng khi đã áp dụng thật".
- Chủ đề người dùng đã loại (vd hiện tại: nội dung đi thi đấu, tuyển PT) → không đưa vào lô, trừ khi được yêu cầu lại.
- Lô/tuần chưa rõ số lượng hoặc nền tảng ưu tiên → hỏi trước khi lên danh sách.

## Quy trình

### 1. Lên danh sách chủ đề
- **Một chủ đề**: đi thẳng bước 2.
- **Theo lô**: lấy chủ đề từ nguồn có sẵn của NaiGym (thư mục *Blog*, *FAQ*, tài liệu kế hoạch), loại chủ đề đã có trong `_danh-sach*.txt`, cân tỷ lệ 70/20/10 ở `content-mapping.md`. Trình bày bảng `# | Chủ đề | Nguồn | Trụ | Layout hook | Format nội dung | Ảnh dự kiến` để PT duyệt.

### 2. Chọn trụ + layout
Trụ theo `content-mapping.md`. Layout hook / format nội dung / layout CTA theo `format-patterns.md` — đổi bố cục giữa các reel.

### 3. Viết kịch bản 3 slide + caption
- **Slide 1 — Hook**: thừa nhận một băn khoăn thật, ≤ 12–14 từ, đọc kịp trong 3 giây. Có thể đặt dạng câu hỏi, tin nhắn hội viên, A vs B.
- **Slide 2 — Nội dung**: một ý chính theo format đã chọn, mỗi dòng ngắn, ≤ 5 mục.
- **Slide 3 — CTA**: một câu đúc kết + một lời mời hành động thật (nhắn tin NaiGym / link in bio) + hashtag.
- **Caption**: hook lại → tóm ý chính → CTA → 3–5 hashtag (mẫu ở `cta-caption-rules.md`).
- Đánh dấu nhấn trong chữ: `[[cụm cần nhấn]]` (tô vàng), `**đậm**`. Không dùng emoji trên slide — dùng icon theo tên (danh sách trong docstring script).

### 4. Chuẩn bị ảnh thật
Chọn ảnh từ kho ảnh NaiGym phù hợp chủ đề (khu tạ, máy, cardio, hội viên đang tập…). Nên thu nhỏ còn cạnh dài ~1400px (JPEG ~82%) để file nhẹ. Ghi đường dẫn ảnh vào trường `"image"` (tương đối so với file JSON). Chưa có ảnh phù hợp → dùng slide `photo_brief` mô tả cần chụp gì.

### 5. Render + tự soát lỗi
Viết file JSON (mẫu: [`references/example-batch.json`](references/example-batch.json)), rồi chạy:

```bash
# soát chữ trước (nhanh, không cần trình duyệt)
python scripts/render_infographic.py --config lo-thang-11.json --lint-only
# render cả lô thẳng vào thư mục Reel infographic (tự nối số reel-NN)
python scripts/render_infographic.py --config lo-thang-11.json --out-dir "../Reel infographic" --strict
```

Script sẽ:
- render từng slide PNG đúng kích thước (`--width/--height`, mặc định 1080×1080; `--scale 2` nếu cần nét gấp đôi);
- đo chữ trong trình duyệt và báo **LỖI** khi chữ đè nhau, tràn khung, bị cắt; **CẢNH BÁO** khi chữ quá nhỏ, có viết tắt khó hiểu, hook quá dài, thiếu caption/hashtag; **GHI CHÚ** liệt kê mọi con số để kiểm nguồn;
- xuất `reel-NN/slide-1..3.png` + `caption.txt`, ghi thêm vào `_danh-sach.txt`, và tạo `_tong-quan.png` (ảnh lưới toàn bộ slide) để rà nhanh.

Không giao khi còn **LỖI**. Sửa JSON (rút ngắn chữ, đổi layout) rồi render lại. Luôn tự mở `_tong-quan.png` xem bằng mắt trước khi trình bày — QA tự động không thay được mắt người.

### 6. Trình bày để duyệt (Yellow Zone)
Gửi `_tong-quan.png` + danh sách reel (chủ đề, nguồn, layout) + các mục cần duyệt kỹ (số liệu, chủ đề nhạy cảm, chương trình chưa áp dụng). Không tự đăng.

### 7. Chốt và lưu trữ
Khi PT/chủ phòng gym xác nhận, thư mục `reel-NN` trong *Reel infographic* chính là bộ giao cuối. Nếu cần sửa chữ, sửa JSON và render lại đúng reel đó với `--start NN`.

## Quy cách chữ (khổ 1080)
| Thành phần | Cỡ chữ | Ghi chú |
|---|---|---|
| Headline hook | 54–84px, line-height ≥ 1.28 | Script tự thu nhỏ theo độ dài |
| Tiêu đề slide nội dung | 44–54px | Font Anton, viết hoa |
| Câu đúc kết CTA | 46–58px | |
| Nội dung chính | 26–32px | Be Vietnam Pro |
| Chữ phụ / mô tả | ≥ 21px | Dưới 20px khó đọc trên điện thoại |
| Header | "NAIGYM" + logo, số trang "01 / 03" | Có sẵn trong mọi slide |

Font: Be Vietnam Pro (nội dung), **Anton** (tiêu đề — tạm thay SVN-Hemi Head vì chưa có file font được cấp phép), Dancing Script (điểm nhấn). Màu: vàng `#FFD10C`, cam `#F59322`, đen `#232323` + nền sáng phụ `#F2F0EB`.

## Tài liệu trong skill
| File | Nội dung |
|---|---|
| `references/content-mapping.md` | 4 trụ nội dung → format, tỷ lệ 70/20/10 cho lô |
| `references/format-patterns.md` | Layout hook / format nội dung / layout CTA, khi nào dùng cái nào, cách xoay vòng |
| `references/plain-language.md` | Bảng thay viết tắt & thuật ngữ khó bằng tiếng Việt dễ hiểu |
| `references/cta-caption-rules.md` | CTA chỉ dùng kênh thật, cấu trúc caption, không bịa số liệu |
| `references/platform-specs.md` | Kích thước pixel từng nền tảng |
| `references/example-batch.json` | File JSON mẫu một lô 2 reel, dùng làm khuôn |
| `scripts/render_infographic.py` | Render PNG + tự soát lỗi + xuất thư mục reel-NN (cần `pip install playwright` và `playwright install chromium`) |
