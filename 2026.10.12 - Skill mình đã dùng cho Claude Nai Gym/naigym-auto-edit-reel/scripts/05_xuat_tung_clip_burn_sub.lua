local LOG = [[C:\Users\TEN_USER\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Edit\naigym_render_log.txt]]
local f = io.open(LOG, "w")
local resolve = Resolve and Resolve() or resolve
local P = resolve:GetProjectManager():GetCurrentProject()
local T = P:GetCurrentTimeline()
local OUT = [[C:\Users\TEN_USER\Downloads\40 reel clip\Final]]
if bmd and bmd.createdir then bmd.createdir(OUT) else os.execute('mkdir "'..OUT..'"') end
local B = {108000,109858,111522,113374,115157,116821,118271,120108,121194,122412,123227,124299,125579,126708,128156,129362,130601,131711,133367,134648,135821,137312,138497,139646,140566,141853,143104,143929,145131,146134,146996,147887,148528}
-- check boundaries against V1 items
local items = T:GetItemListInTrack("video",1) or {}
f:write("TL "..T:GetName().." V1 items: "..#items.."\n")
for i,it in ipairs(items) do f:write(i.."\t"..it:GetStart().."\t"..it:GetEnd().."\t"..(it:GetName() or "").."\n") end
P:SetCurrentRenderMode(1)
local ok0 = P:SetRenderSettings({ExportVideo=true, ExportAudio=true, ExportSubtitle=true, SubtitleFormat="BurnIn"})
f:write("subtitle settings ok: "..tostring(ok0).."\n")
for i=1,32 do
  local name = string.format("Clip %02d", i)
  local ok = P:SetRenderSettings({SelectAllFrames=false, MarkIn=B[i], MarkOut=B[i+1]-1, TargetDir=OUT, CustomName=name})
  local id = P:AddRenderJob()
  f:write(name.."\t"..B[i].."-"..(B[i+1]-1).."\tset="..tostring(ok).."\tjob="..tostring(id).."\n")
end
f:write("Jobs: "..#(P:GetRenderJobList() or {}).."\n")
f:close()
