# NaiGym Skills

Bộ Agent Skill (dùng với Claude) phục vụ sản xuất nội dung cho NaiGym — blog chuyên sâu, carousel/infographic mạng xã hội và dựng reel tự động trong DaVinci Resolve.

| Skill | Làm gì |
|---|---|
| [`blog-writer`](skills/blog-writer/SKILL.md) | Viết bài blog chuyên sâu theo giọng The Sage (khoa học + tâm lý + đồng cảm + an toàn), kèm creative brief ảnh bìa theo brand. |
| [`infographic-factory`](skills/infographic-factory/SKILL.md) | Sản xuất hàng loạt carousel/infographic 3 slide, render PNG đúng brand và kích thước nền tảng, tự soát lỗi chữ, xuất thư mục `reel-NN/` + caption. |
| [`naigym-auto-edit-reel`](skills/naigym-auto-edit-reel/SKILL.md) | Dựng tự động hàng loạt reel trong DaVinci Resolve: b-roll, nhạc, SFX, compound, phụ đề SRT, burn sub và xuất từng clip. |

## Cấu trúc

```
skills/
├── blog-writer/            SKILL.md + references/
├── infographic-factory/    SKILL.md + references/ + scripts/ (render_infographic.py, font)
└── naigym-auto-edit-reel/  SKILL.md + scripts/ (Lua cho Resolve) + reference/ + templates/
```

## Cách dùng

**Trong Claude (claude.ai / Cowork):** nén từng thư mục skill (vd `skills/blog-writer/`) thành file `.zip` rồi tải lên ở phần Skills.

**Trong một dự án dùng `.claude/`:** chép các thư mục trong `skills/` vào `.claude/skills/`.

### Lưu ý

- Các skill được viết để nằm trong `.claude/` của dự án NaiGym, nên có vài link trỏ tới file **không có trong repo này**: `domains/brand/brand-voice.md`, `domains/brand/brand-identity.md`, `domains/brand/assets/logo-mark.png` và `workflow/zones.md`. Khi dùng ngoài dự án đó, hãy tự thêm các file brand tương ứng (hoặc bỏ qua link).
- `infographic-factory` cần Python 3 và Playwright: `pip install playwright` rồi `playwright install chromium`. Không có logo thì slide vẫn render, chỉ thiếu logo ở header.
- `naigym-auto-edit-reel`: đường dẫn trong script Lua và file tham khảo dùng `C:\Users\TEN_USER\...` — thay `TEN_USER` bằng tên user Windows của bạn. Số clip, ranh giới frame và tên file b-roll là của dự án mẫu 32 clip, cần sửa lại cho dự án mới. Repo không kèm file video/nhạc/SFX.

## Font

Font trong `skills/infographic-factory/scripts/assets/fonts/` (Be Vietnam Pro, Anton, Dancing Script) phát hành theo **SIL Open Font License 1.1** — xem thư mục `licenses/` bên cạnh.
