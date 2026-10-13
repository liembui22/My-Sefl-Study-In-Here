---
name: naigym-auto-edit-reel
description: Dựng tự động hàng loạt reel NaiGym trong DaVinci Resolve từ đầu đến file xuất cuối — enhance audio Audition, gom source b-roll/nhạc/SFX, chèn b-roll + nhạc + SFX theo clip mẫu, compound từng clip, làm phụ đề SRT miễn phí, burn sub và xuất từng clip.
---

# NaiGym — Dựng reel tự động (Audition → Resolve → Final)

Quy trình đã chạy thật cho 32 reel nói chuyện (talking-head) của NaiGym. Dùng khi Liêm đưa một loạt clip thô và một clip mẫu đã edit sẵn (thường là clip 1), muốn các clip còn lại được làm giống mẫu và xuất ra từng file.

Cách làm việc chung:
- Mọi thao tác trên máy Liêm đi qua máy tính đã liên kết (computer use + shell trên các thư mục đã kết nối).
- Thao tác Resolve hàng loạt luôn bằng **script Lua chạy từ menu Workspace > Scripts > Edit**, không click tay từng clip. Script nằm ở thư mục `C:\Users\TEN_USER\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Edit` (xin quyền kết nối thư mục này; trong shell nó là `$HOME/mnt/Edit`). Mỗi script ghi log `.txt` cạnh nó để đọc kết quả qua shell.
- Không bao giờ sửa timeline gốc: script đầu tiên nhân bản thành `Timeline 1 - Claude dung` và mọi script sau kiểm tra tên timeline có chữ "Claude" mới chạy.
- Giữ một task list theo 8 bước dưới, báo nháp sớm, và hỏi trước khi làm việc khó đảo ngược.

## Bước 0 — Nhận việc và khảo sát

1. Hỏi/ xác nhận: thư mục clip thô (vd `Downloads\40 reel clip`), project Resolve (vd "40 clip"), clip mẫu, số clip cần làm, có cần sub không, xuất vào đâu.
2. Mở Resolve, xem clip mẫu: các track (tiêu đề Essential Titles, logo, b-roll, nhạc, SFX, phụ đề), vị trí, zoom, style sub. Đọc note Liêm để trên timeline.
3. Chạy một script "probe" chỉ đọc để lấy: tên timeline, fps, độ phân giải, start frame, danh sách item V1 (tên + start/end), đường dẫn media, preset render. Mẫu:

```lua
local LOG=[[...\Scripts\Edit\naigym_check_log.txt]]
local f=io.open(LOG,"w"); local resolve=Resolve and Resolve() or resolve
local P=resolve:GetProjectManager():GetCurrentProject(); local T=P:GetCurrentTimeline()
f:write("TL "..T:GetName().." fps "..T:GetSetting("timelineFrameRate").." start "..T:GetStartFrame().."\n")
for i,it in ipairs(T:GetItemListInTrack("video",1) or {}) do f:write(i.."\t"..it:GetStart().."\t"..it:GetEnd().."\t"..(it:GetName() or "").."\n") end
f:close()
```

Ghi lại **ranh giới frame của từng clip** (start của clip n → start clip n+1). Mọi bước sau dùng bảng này.

## Bước 1 — Enhance audio trong Adobe Audition

Thao tác Liêm đã chuẩn hoá, lặp cho từng clip i:
1. Mở clip i (single-click chọn, double-click mở, rồi **chụp màn hình xác nhận đúng file đã mở** — mở hụt từng gây chạy NR 2 lần lên sai clip).
2. Effects → Noise Reduction/Restoration → Noise Reduction (process) → Apply. **Làm 2 lần.**
3. Bấm Apply ở Effects Rack.
4. Export vào thư mục `done` (vd `40 reel clip\Audio enhance\Compound Clip i.wav`).
Nếu lỡ áp sai: Ctrl+Z về đúng trạng thái rồi export lại. File wav sau đó thay audio gốc trong Resolve.

## Bước 2 — Lập danh sách tài nguyên để Liêm đi tìm (collect 1 lần)

1. Đọc tiêu đề từng clip (Essential Titles trên timeline) và nội dung nói.
2. Mỗi clip cần **3 b-roll** khớp chủ đề; thêm bộ dùng chung: 5 bài nhạc nền xoay vòng, SFX whoosh/hit/riser/flash, vài b-roll gym dự phòng.
3. **Gom theo chủ đề** để Liêm tải một lần dùng nhiều clip. Bộ chủ đề đã dùng:
   - `Tập Luyện trong Phòng Nai Gym` (footage tự quay tại phòng — ưu tiên số 1)
   - `Sức khỏe, đau mỏi, nghỉ ngơi`
   - `Tập tại nhà, ngoài trời, thể thao khác`
   - `Đo lường, thời gian, ghi chép`
   - `Đồ Ăn và dinh dưỡng`
   - `SFX` (gồm cả nhạc nền)
4. Viết từ khoá **tiếng Anh** cho từng cảnh (kho stock tìm tốt hơn), vd "bicep curl close up muscle", "late night snacking fridge", "measuring waist tape".
5. Nguồn miễn phí gợi ý:
   - B-roll: Pexels Videos, Pixabay Videos, Mixkit, Coverr, Videvo (free); Storyblocks/Envato nếu có tài khoản.
   - Nhạc: Pixabay Music, YouTube Audio Library, Mixkit, Uppbeat (free tier), Freepik/Magnific (bộ nhạc `magnific-*` đã dùng).
   - SFX: Pixabay Sound Effects, Mixkit SFX, Freesound, Zapsplat.
   - Tiêu chí: video ngang ≥720p, dài 5–10 giây, không watermark, vibe upbeat/motivational cho nhạc.
6. Xuất bảng này thành **artifact checklist** (tick lưu trên trình duyệt, nút chép từ khoá theo nhóm). Liêm bỏ tất cả vào một thư mục (vd `NaiGym Claude ...\Source edit tự động`) và kết nối thư mục đó.

## Bước 3 — Chèn b-roll, nhạc, SFX theo mẫu

1. Quét thư mục source bằng shell + `ffprobe`: lấy tên file, thời lượng, độ phân giải mỗi b-roll. Xem thumbnail (contact sheet bằng ffmpeg) để chọn cảnh hợp chủ đề.
2. Chọn cho mỗi clip 3 b-roll **ngẫu nhiên nhưng hợp lý** theo tiêu đề (Liêm dặn: đừng câu nệ quá; tránh lặp liền kề; footage phòng Nai Gym dùng nhiều).
3. Sinh một script Lua duy nhất làm tất cả:
   - `DuplicateTimeline('Timeline 1 - Claude dung')`, `SetCurrentTimeline`.
   - Tạo bin `Claude B-roll`, `ImportMedia` toàn bộ file cần dùng.
   - Với từng clip (lấy range từ item V1 tên `Compound Clip n`): đặt b-roll ở **video track 4**, vùng thân bài (bắt đầu ~sau 18 s hoặc 20% độ dài, kết thúc trước ~12% cuối); 3 cảnh nếu đủ chỗ, ít hơn nếu clip ngắn; mỗi cảnh ~3,5 s, cắt từ đoạn giữa file.
   - Zoom b-roll lấp khung dọc: `z = max(1, (w/h)/(W/H)) * 1.05` với W/H là khung timeline (vd 1828x1332), footage cùng khung giữ 1.0. `SetProperty('ZoomX',z)`, `('ZoomY',z)`.
   - Mỗi lần chèn b-roll: 1 whoosh ở **A2**, đặt sớm 4 frame, xoay vòng bộ SFX.
   - Nhạc nền ở **A3**, chạy hết độ dài clip, xoay vòng 5 bài (clip mẫu giữ nguyên nhạc của nó).
   - Dùng `MP:AppendToTimeline({{mediaPoolItem=mi,startFrame=a,endFrame=b,mediaType=1|2,trackIndex=k,recordFrame=r}})`.
   - In ra/ghi log số b-roll, sfx, nhạc đã thêm và lỗi thiếu file.
4. Chụp màn hình kiểm tra vài clip, báo Liêm xem trước khi đi tiếp.

## Bước 4 — Compound từng clip (để xuất riêng)

Giống clip mẫu: mỗi clip gộp toàn bộ item video+audio nằm trọn trong range của nó thành `Compound Clip n`.
- Script nhân bản backup `... - ban truoc compound` trước.
- Duyệt **từ clip cuối về đầu** (n = N..2), gom item có `start>=S and end<=E` trên mọi track video/audio, `T:CreateCompoundClip(items,{name="Compound Clip "..n})`. Hàm này có thể trả về nil nhưng vẫn chạy được — kiểm tra lại bằng probe.
- **Chỉ chạy một lần**; chạy lại sẽ lồng compound thêm một lớp.

## Bước 5 — Phụ đề SRT miễn phí, không giới hạn

1. Dùng **AutoSubs** (plugin miễn phí cho Resolve, Workspace > Scripts > AutoSubs), model Whisper (Small đủ tốt cho tiếng Việt), ngôn ngữ Vietnamese.
   - Kẹt 0% → **tắt GPU Acceleration** và dùng chế độ **File** (chọn file audio) thay vì timeline.
   - AutoSubs tự đổi preset Deliver sang **Audio Only** — nhớ đổi lại trước khi xuất.
2. Xuất SRT cho cả timeline rồi **tách theo ranh giới clip** thành `Compound Clip n_01.srt` (thời gian tính lại từ 0 cho mỗi clip). Lưu vào `Source edit tự động\SRT N clip\`.
3. Sửa chính tả từng cue (từ chuyên môn gym, tên NaiGym, dấu câu), giữ nguyên timing; không để câu cuối clip bị rớt — gộp phần đuôi vào cue trước nếu Whisper làm mất.
4. Thay thế miễn phí khác nếu không dùng AutoSubs: CapCut desktop (auto caption, export SRT), Subtitle Edit + Whisper, hoặc Whisper chạy local.

## Bước 6 — Đưa phụ đề vào timeline theo style mẫu

1. Ghép SRT các clip cần thêm thành một file (giờ tính theo timeline), copy vào thư mục Scripts.
2. Script: `ImportMedia({srt})` rồi `AppendToTimeline({{mediaPoolItem=it,startFrame=0,recordFrame=start,trackIndex=1}})`.
   - **Lưu ý:** với phụ đề, `recordFrame` bị bỏ qua — nó luôn được nối vào **cuối timeline**. Sửa: chọn toàn bộ cue mới, Timeline > Select Clips Forward on All Tracks (hoặc chọn track ST1), gõ offset âm (vd `-223028` = −(độ lệch)) + Enter để dời về đúng chỗ. Kiểm tra cue đầu khớp frame start của clip đầu tiên.
3. Style: dùng đúng style của sub mẫu trên ST1 (màu vàng, font/viền như mẫu) — áp qua Inspector của track phụ đề (Track style) để cả track đồng bộ.
4. Đọc lại bằng script liệt kê `GetItemListInTrack("subtitle",1)` (start, end, text) để kiểm tra không có cue nào chạy qua ranh giới clip. Sửa text lẻ trong Inspector > Caption.
5. Lưu project (Ctrl+S).

## Bước 7 — Xuất từng clip, burn sub

1. Trang Deliver: chọn preset video Liêm dùng (đã dùng **H.265 Master, MP4**, timeline resolution, 29.97). Bỏ Audio Only nếu AutoSubs đã đổi.
2. Tạo thư mục output (vd `40 reel clip\Final`) và xin quyền kết nối nó để kiểm tra file.
3. Script thêm job cho từng clip:

```lua
P:SetCurrentRenderMode(1)
P:SetRenderSettings({ExportVideo=true, ExportAudio=true, ExportSubtitle=true, SubtitleFormat="BurnIn"})
for i=1,N do
  P:SetRenderSettings({SelectAllFrames=false, MarkIn=B[i], MarkOut=B[i+1]-1,
                       TargetDir=OUT, CustomName=string.format("Clip %02d", i)})
  P:AddRenderJob()
end
```
   (B = bảng ranh giới frame tuyệt đối, vd 108000 = 01:00:00:00.) Sau đó kéo panel Video xuống kiểm tra **Subtitle Settings: Export Subtitle ✓, Format = Burn into video**.
4. `P:StartRendering()` từ một script riêng (nút "Render 1" trên UI chỉ render job đang chọn).
5. **Kiểm tra bằng ffprobe** khi từng file xong: thời lượng phải bằng (B[i+1]−B[i])/fps. Đã gặp lỗi **job đầu tiên ra chỉ 11 frame** → đổi tên file lỗi, khi queue xong thì `DeleteAllRenderJobs()`, thêm lại riêng job đó và render lại.
6. Trích một frame (ffmpeg `-ss 10 -frames:v 1`) xem sub đã burn đúng style chưa.

## Bước 8 — Bàn giao

Báo ngắn: số clip đã xuất, thư mục, clip nào phải render lại, việc còn lại (vd hook cao trào đầu clip, transition flash/zoom chưa làm). Lưu project. Nhả khoá máy tính.

## Mẹo / lỗi đã gặp

- Cửa sổ Claude có thể che nửa phải màn hình; click vào viewer Resolve để lấy lại focus trước khi bấm phím tắt.
- Console Resolve hay bị thu nhỏ → luôn chạy script qua menu Workspace > Scripts thay vì console.
- Không có lệnh xoá trong thư mục kết nối: muốn bỏ file thì `mv` vào thư mục `_tmp_check`/`_to_delete`.
- Mọi sửa sai trên timeline: Ctrl+Z ngay và kiểm tra Edit > History.
- Clip mẫu làm hook cao trào đầu clip + chuyển cảnh smooth zoom/flash có SFX — phần này chưa tự động hoá; hỏi Liêm trước nếu muốn làm.
