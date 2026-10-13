-- Bat dau render TAT CA job trong Render Queue (nut "Render 1" tren UI chi render job dang chon).
local resolve=Resolve and Resolve() or resolve
resolve:GetProjectManager():GetCurrentProject():StartRendering()
