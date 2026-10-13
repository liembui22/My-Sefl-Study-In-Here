local LOG = [[C:\Users\TEN_USER\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Edit\naigym_check_log.txt]]
local f = io.open(LOG, "w")
local resolve = Resolve and Resolve() or resolve
local P = resolve:GetProjectManager():GetCurrentProject()
if P:IsRenderingInProgress() then f:write("busy\n") f:close() return end
P:DeleteAllRenderJobs()
local OUT = [[C:\Users\TEN_USER\Downloads\40 reel clip\Final]]
P:SetRenderSettings({ExportVideo=true, ExportAudio=true, ExportSubtitle=true, SubtitleFormat="BurnIn"})
local ok = P:SetRenderSettings({SelectAllFrames=false, MarkIn=108000, MarkOut=109857, TargetDir=OUT, CustomName="Clip 01"})
local id = P:AddRenderJob()
for _,j in ipairs(P:GetRenderJobList() or {}) do for k,v in pairs(j) do f:write(k.."="..tostring(v).."  ") end f:write("\n") end
f:write("ok="..tostring(ok).." id="..tostring(id).."\n")
P:StartRendering(id)
f:close()
