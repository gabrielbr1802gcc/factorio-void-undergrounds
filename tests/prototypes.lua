-- Offline regression fixtures; these do not simulate Factorio's engine.
-- Shapes and numeric values checked against wube/factorio-data tag 2.0.77.
local patch = assert(loadfile("data-final-fixes.lua")) -- Also checks Lua syntax.

-- Standalone equivalent of the table.deepcopy helper provided by Factorio.
local function deepcopy(value, seen)
  if type(value) ~= "table" then return value end
  seen = seen or {}
  if seen[value] then return seen[value] end
  local result = {}
  seen[value] = result
  for key, child in pairs(value) do
    result[deepcopy(key, seen)] = deepcopy(child, seen)
  end
  return result
end
table.deepcopy = deepcopy

local function equal(actual, expected, path)
  path = path or "data.raw"
  assert(type(actual) == type(expected), path .. ": type changed")
  if type(expected) ~= "table" then
    assert(actual == expected, path .. ": unexpected value")
    return
  end
  for key, value in pairs(expected) do
    equal(actual[key], value, path .. "." .. tostring(key))
  end
  for key in pairs(actual) do
    assert(expected[key] ~= nil, path .. "." .. tostring(key) .. ": unexpected key")
  end
end

local names = {
  "underground-belt", "fast-underground-belt",
  "express-underground-belt", "turbo-underground-belt"
}
local distances = {5, 7, 9, 11}
local speeds = {0.03125, 0.0625, 0.09375, 0.125}

local function fixture()
  -- Space Age assigns the SAME table to all five underground masks.
  local shared = {layers = {lava_tile = true, empty_space = true}}
  local belts = {}
  for index, name in ipairs(names) do
    belts[name] = {
      type = "underground-belt", name = name,
      max_distance = distances[index], speed = speeds[index],
      collision_mask = {layers = {object = true, empty_space = true}},
      collision_box = {{-0.4, -0.4}, {0.4, 0.4}},
      underground_collision_mask = shared
    }
  end
  -- Another mod may reuse the vanilla masks, even for placement collisions.
  belts["custom-underground"] = {
    max_distance = 99, underground_collision_mask = shared, collision_mask = shared
  }
  return {
    ["underground-belt"] = belts,
    ["pipe-to-ground"] = {
      ["pipe-to-ground"] = {
        type = "pipe-to-ground", name = "pipe-to-ground",
        collision_mask = {layers = {object = true, empty_space = true}},
        fluid_box = {
          volume = 100,
          pipe_connections = {
            {direction = 0, position = {0, 0}},
            {
              connection_type = "underground", direction = 8, position = {0, 0},
              max_underground_distance = 10, underground_collision_mask = shared
            }
          }
        }
      },
      ["custom-pipe"] = {underground_collision_mask = shared}
    },
    ["transport-belt"] = {untouched = {speed = 0.25, collision_mask = shared}},
    pipe = {pipe = {fluid_box = {volume = 100}}},
    tile = {["empty-space"] = {collision_mask = shared}},
    recipe = {untouched = {enabled = false}},
    technology = {untouched = {unit = {count = 100}}}
  }, shared
end

local function pipe_connections(raw)
  return raw["pipe-to-ground"]["pipe-to-ground"].fluid_box.pipe_connections
end

local passed = 0
local function test(name, run)
  run()
  passed = passed + 1
  print("PASS " .. name)
end

test("only five intended masks change; lava, range, speed, placement and other prototypes survive", function()
  local raw, original = fixture()
  local expected = deepcopy(raw)
  -- Break fixture aliases before expressing the five expected changes.
  for _, name in ipairs(names) do
    expected["underground-belt"][name].underground_collision_mask = {
      layers = {lava_tile = true}
    }
  end
  pipe_connections(expected)[2].underground_collision_mask = {layers = {lava_tile = true}}
  data = {raw = raw}
  patch()
  equal(raw, expected)
  equal(original, {layers = {lava_tile = true, empty_space = true}}, "original shared mask")
  for _, name in ipairs(names) do
    assert(raw["underground-belt"][name].underground_collision_mask ~= original)
  end
  assert(pipe_connections(raw)[2].underground_collision_mask ~= original)
end)

test("custom layers and collision options are preserved", function()
  local raw, original = fixture()
  original.layers.water_tile = true
  original.not_colliding_with_itself = true
  original.consider_tile_transitions = false
  original.colliding_with_tiles_only = true
  data = {raw = raw}
  patch()
  local expected = deepcopy(original)
  expected.layers.empty_space = nil
  for _, name in ipairs(names) do
    equal(raw["underground-belt"][name].underground_collision_mask, expected, name)
  end
  equal(pipe_connections(raw)[2].underground_collision_mask, expected, "pipe mask")
  assert(original.layers.empty_space == true)
end)

test("pipe connections are selected by type rather than array index", function()
  local raw, original = fixture()
  local connections = pipe_connections(raw)
  local underground = connections[2]
  connections[1].underground_collision_mask = original
  connections[2] = {connection_type = "linked", linked_connection_id = 1,
                    underground_collision_mask = original}
  connections[3] = underground
  connections[4] = deepcopy(underground)
  connections[4].max_underground_distance = 8
  local expected = deepcopy(connections)
  for _, index in ipairs({3, 4}) do
    expected[index].underground_collision_mask = {layers = {lava_tile = true}}
  end
  data = {raw = raw}
  patch()
  equal(connections, expected, "pipe connections")
  equal(connections[3].underground_collision_mask, connections[4].underground_collision_mask)
end)

test("reapplying the patch has no additional effect", function()
  data = {raw = fixture()}
  patch()
  local first = deepcopy(data.raw)
  local mask = data.raw["underground-belt"][names[1]].underground_collision_mask
  patch()
  equal(data.raw, first)
  assert(data.raw["underground-belt"][names[1]].underground_collision_mask == mask)
end)

test("absent or already corrected masks are not synthesized or replaced", function()
  for _, mask in ipairs({false, {}, {layers = {}}, {layers = {lava_tile = true}}}) do
    local raw = fixture()
    local value = mask or nil
    raw["underground-belt"][names[1]].underground_collision_mask = value
    pipe_connections(raw)[2].underground_collision_mask = value
    data = {raw = raw}
    patch()
    assert(raw["underground-belt"][names[1]].underground_collision_mask == value)
    assert(pipe_connections(raw)[2].underground_collision_mask == value)
  end
end)

test("missing vanilla prototypes or optional fluid structures are tolerated", function()
  local cases = {
    {},
    {["underground-belt"] = {}, ["pipe-to-ground"] = {}},
    {["pipe-to-ground"] = {["pipe-to-ground"] = {}}},
    {["pipe-to-ground"] = {["pipe-to-ground"] = {fluid_box = {}}}}
  }
  for _, raw in ipairs(cases) do
    local before = deepcopy(raw)
    data = {raw = raw}
    patch()
    equal(raw, before)
  end
end)

print(string.format("%d Lua prototype regression cases passed", passed))
