# naigym-auto-edit-reel — bộ lưu trữ

Quy trình dựng tự động reel NaiGym: Audition → Resolve (b-roll, nhạc, SFX, compound, phụ đề) → xuất từng clip có burn sub.

- `SKILL.md` — hướng dẫn đầy đủ 8 bước (bản giống skill đã lưu trong tài khoản Claude).
- `scripts/` — script Lua cho DaVinci Resolve, đánh số theo thứ tự chạy. Copy vào
  `C:\Users\TEN_USER\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Edit`
  rồi chạy qua Workspace > Scripts > Edit. Mỗi script ghi log .txt cùng thư mục.
  - 01 probe (chỉ đọc) · 02 b-roll/nhạc/SFX · 03 compound từng clip (chỉ chạy 1 lần) · 04 thêm phụ đề SRT
  - 05 thêm job xuất từng clip + burn sub · 06 render lại 1 clip lỗi · 07 bắt đầu render · 08 liệt kê phụ đề
  - Các script có số clip, ranh giới frame và đường dẫn của dự án 40 clip — sửa lại cho dự án mới.
- `templates/` — trang checklist tài nguyên (mở bằng trình duyệt).
- `reference/` — thông số dự án mẫu và cấu trúc thư mục source.

Muốn cài lại skill vào Claude: nhắn Claude "cài skill từ file SKILL.md này" và gửi kèm file.

> Thay `TEN_USER` trong các đường dẫn bằng tên user Windows của bạn trước khi chạy script.
