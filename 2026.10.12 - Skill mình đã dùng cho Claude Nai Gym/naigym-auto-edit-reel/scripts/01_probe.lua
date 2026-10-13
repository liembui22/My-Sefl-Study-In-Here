-- Probe chi doc: ten timeline, fps, start frame, item V1, duong dan media, preset render.
local LOG=[[C:\Users\TEN_USER\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Edit\naigym_check_log.txt]]
local f=io.open(LOG,"w"); local resolve=Resolve and Resolve() or resolve
local P=resolve:GetProjectManager():GetCurrentProject(); local T=P:GetCurrentTimeline()
f:write("TL "..T:GetName().." fps "..tostring(T:GetSetting("timelineFrameRate")).." start "..T:GetStartFrame().." end "..T:GetEndFrame().."\n")
for i,it in ipairs(T:GetItemListInTrack("video",1) or {}) do f:write(i.."\t"..it:GetStart().."\t"..it:GetEnd().."\t"..(it:GetName() or "").."\n") end
local n=0
local function walk(fo) for _,c in ipairs(fo:GetClipList() or {}) do local p=c:GetClipProperty("File Path") or "" if p~="" and n<60 then f:write(p.."\n") n=n+1 end end for _,s in ipairs(fo:GetSubFolderList() or {}) do walk(s) end end
walk(P:GetMediaPool():GetRootFolder())
local fc=P:GetCurrentRenderFormatAndCodec() or {}; f:write("FMT "..tostring(fc.format).." / "..tostring(fc.codec).."\n")
for _,v in pairs(P:GetRenderPresetList() or {}) do f:write("PRESET "..tostring(v).."\n") end
f:close()
