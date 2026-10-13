# Platform Specs — kích thước chuẩn từng nền tảng

> Đồng bộ với `Bo-Quy-Chuan-Dong-Bo-Nhan-Dien-NaiGym.docx` (mục A. Mạng xã hội). Nếu nền tảng đổi spec, cập nhật cả 2 nơi. Ghi ngày rà soát gần nhất mỗi khi sửa: 2026-09-07.

| Nền tảng | Loại | Kích thước (px) | Ghi chú |
|---|---|---|---|
| Facebook Page | Ảnh đại diện | 170×170 | Hiển thị tròn ~128×128 — dùng `logo-mark.png`, nền đặc (không để trong suốt) |
| Facebook Page | Ảnh bìa | 820×312 (desktop) | Dùng `logo-full.png`, tránh đặt nội dung sát vùng bị nút/avatar che |
| Facebook Page/Group | Ảnh bài đăng (feed) | 1200×630 | Tỷ lệ ~1.91:1, watermark `logo-mark.png` góc dưới phải |
| Facebook/Instagram | Story/Reels | 1080×1920 | Chừa vùng an toàn ~250px trên & dưới, tránh bị UI nền tảng che |
| Instagram | Ảnh đại diện | 320×320 | `logo-mark.png` |
| Instagram | Bài feed (vuông) | 1080×1080 | Mặc định cho carousel 3 slide nếu không chỉ định khác |
| Instagram | Bài feed (dọc) | 1080×1350 | Tỷ lệ 4:5 — chiếm nhiều diện tích feed hơn ảnh vuông, ưu tiên khi muốn tăng hiển thị |
| TikTok | Ảnh đại diện | 200×200 | `logo-mark.png` |
| TikTok | Video/ảnh bìa | 1080×1920 | Dùng chung khung Story |

## Mặc định khi không được chỉ định nền tảng
Dùng **Instagram bài feed vuông (1080×1080)** làm mặc định cho carousel 3 slide — dễ tái sử dụng sang Facebook post (crop về 1200×630 nếu cần) và là kích thước phổ biến nhất cho carousel nhiều slide. Chỉ đổi sang 1080×1350 hoặc 1080×1920 khi PT/chủ phòng gym nêu rõ nền tảng ưu tiên.

Tham số `--width`/`--height` trong `scripts/render_infographic.py` nhận trực tiếp các cặp số ở trên (hoặc khai báo `"platform"` trong JSON). Mặc định script xuất đúng số pixel nền tảng; thêm `--scale 2` nếu cần ảnh nét gấp đôi (vd để in hoặc crop lại).

Bố cục trong script co giãn theo chiều rộng, nên khổ 1080×1350 và 1080×1920 dùng chung JSON với 1080×1080 — nhưng vẫn phải xem `_tong-quan.png` sau khi đổi khổ, vì khoảng trống dọc sẽ khác.
