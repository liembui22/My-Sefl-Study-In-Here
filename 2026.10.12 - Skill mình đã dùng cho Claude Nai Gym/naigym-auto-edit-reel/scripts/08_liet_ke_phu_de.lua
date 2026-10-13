-- Liet ke cue tren ST1 (start, end, text) de kiem tra phu de khong vuot ranh gioi clip.
local LOG=[[C:\Users\TEN_USER\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Edit\naigym_check_log.txt]]
local f=io.open(LOG,"w"); local resolve=Resolve and Resolve() or resolve
local T=resolve:GetProjectManager():GetCurrentProject():GetCurrentTimeline()
for _,it in ipairs(T:GetItemListInTrack("subtitle",1) or {}) do f:write(it:GetStart().."\t"..it:GetEnd().."\t"..(it:GetName() or "").."\n") end
f:close()
