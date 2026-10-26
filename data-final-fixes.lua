-- Factorio 2.0 uses CollisionMaskConnector: {layers = {layer_name = true}}.
local function remove_empty_space(owner)
  local mask = owner.underground_collision_mask
  if mask and mask.layers and mask.layers.empty_space then
    -- Space Age shares this table. Copy it to avoid changing other owners.
    local updated_mask = table.deepcopy(mask)
    updated_mask.layers.empty_space = nil
    owner.underground_collision_mask = updated_mask
  end
end

local belts = data.raw["underground-belt"] or {}
for _, name in ipairs({
  "underground-belt",
  "fast-underground-belt",
  "express-underground-belt",
  "turbo-underground-belt"
}) do
  if belts[name] then
    remove_empty_space(belts[name])
  end
end

local pipe = (data.raw["pipe-to-ground"] or {})["pipe-to-ground"]
if pipe and pipe.fluid_box then
  for _, connection in pairs(pipe.fluid_box.pipe_connections or {}) do
    if connection.connection_type == "underground" then
      remove_empty_space(connection)
    end
  end
end
