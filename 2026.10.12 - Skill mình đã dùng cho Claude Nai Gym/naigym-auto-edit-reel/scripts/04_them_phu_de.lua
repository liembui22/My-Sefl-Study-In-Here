local LOG = [[C:\Users\TEN_USER\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Edit\naigym_sub_log.txt]]
local SRT = [[C:\Users\TEN_USER\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Edit\naigym_clip2-32.srt]]
local f = io.open(LOG, "w")
local function log(...) local t={} for i=1,select('#',...) do t[#t+1]=tostring(select(i,...)) end f:write(table.concat(t,"\t").."\n") f:flush() end
local resolve = Resolve and Resolve() or resolve
local P = resolve:GetProjectManager():GetCurrentProject()
local T = P:GetCurrentTimeline()
log("tl", T:GetName(), "subtracks", T:GetTrackCount("subtitle"))
local st = T:GetItemListInTrack("subtitle", 1) or {}
log("ST1 before", #st, st[1] and st[1]:GetStart(), st[#st] and st[#st]:GetEnd())
if not T:GetName():find("Claude") then log("STOP") f:close() return end
local MP = P:GetMediaPool()
local items = MP:ImportMedia({SRT})
log("imported", items and #items or "nil")
local it = items and items[1]
if it then
  log("type", it:GetClipProperty("Type"), "dur", it:GetClipProperty("Duration"))
  local r = MP:AppendToTimeline({{mediaPoolItem = it, startFrame = 0, recordFrame = 108000, trackIndex = 1}})
  log("append", r and #r or "nil")
end
local st2 = T:GetItemListInTrack("subtitle", 1) or {}
log("ST1 after", #st2, "tracks", T:GetTrackCount("subtitle"))
for i=1,T:GetTrackCount("subtitle") do local l=T:GetItemListInTrack("subtitle", i) or {} log("ST"..i, #l, l[1] and l[1]:GetStart(), l[#l] and l[#l]:GetEnd()) end
f:close()
