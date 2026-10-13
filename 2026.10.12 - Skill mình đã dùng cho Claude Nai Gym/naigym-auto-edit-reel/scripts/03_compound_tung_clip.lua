-- Gop moi clip (2..32) thanh 1 compound clip giong mau clip 1
local LOG = [[C:\Users\TEN_USER\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Edit\naigym_compound_log.txt]]
local f = io.open(LOG, "w")
local function log(...) local t={} for i=1,select('#',...) do t[#t+1]=tostring(select(i,...)) end local s=table.concat(t,"\t") print(s) if f then f:write(s.."\n") f:flush() end end

local resolve = Resolve and Resolve() or resolve
local P = resolve:GetProjectManager():GetCurrentProject()
local T = P:GetCurrentTimeline()
log("timeline", T:GetName())
if not T:GetName():find("Claude") then log("STOP: khong phai timeline Claude") if f then f:close() end return end

local B = T:DuplicateTimeline(T:GetName() .. " - ban truoc compound")
log("backup", B and B:GetName() or "FAILED")
P:SetCurrentTimeline(T)
log("current", P:GetCurrentTimeline():GetName())

local function ranges()
  local R = {}
  for _, it in ipairs(T:GetItemListInTrack("video", 1)) do
    local n = tonumber((it:GetName() or ""):match("^Compound Clip (%d+)$"))
    if n and n >= 2 then R[n] = {it:GetStart(), it:GetEnd()} end
  end
  return R
end

local R = ranges()
local done, fail = 0, 0
for n = 32, 2, -1 do
  local r = R[n]
  if r then
    local S, E = r[1], r[2]
    local items, cross = {}, 0
    for _, kind in ipairs({"video", "audio"}) do
      for tr = 1, T:GetTrackCount(kind) do
        for _, it in ipairs(T:GetItemListInTrack(kind, tr) or {}) do
          local a, b = it:GetStart(), it:GetEnd()
          if a >= S and b <= E then items[#items+1] = it
          elseif a < E and b > S then cross = cross + 1 end
        end
      end
    end
    local c = T:CreateCompoundClip(items, {name = "Compound Clip " .. n})
    if c then done = done + 1 else fail = fail + 1 end
    log("clip", n, "items", #items, "cross", cross, c and "OK" or "FAIL")
  else
    log("clip", n, "not found")
  end
end
log("DONE", "ok", done, "fail", fail)
if f then f:close() end
