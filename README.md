# Void Undergrounds Vanilla

Experimental Factorio **2.0.77 + Space Age** mod. It removes the `empty_space`
layer from the underground connection masks of the four vanilla underground
belts and vanilla pipe-to-ground. This is intended to let their underground
connections cross gaps in a space platform within the original connection range.

**Status: verified against the 2.0.77 API and with offline regression tests;
not tested inside Factorio. In-game functionality is not yet confirmed.**

## Installation

1. Download **`void-undergrounds-vanilla_0.1.0.zip`** from the
   [experimental release](https://github.com/gabrielbr1802gcc/factorio-void-undergrounds/releases/tag/v0.1.0-beta).
   Choose the uploaded mod asset; GitHub's automatic **Source code** archives
   are not the installable package.
2. With Factorio closed, copy that ZIP into the `mods` directory of the Factorio
   installation/profile you want to use. Keep it zipped.
3. Start Factorio 2.0.77 with Space Age enabled, enable **Void Undergrounds
   Vanilla**, and restart if prompted. Space Age's required official dependencies
   must also be enabled.

The ZIP contains a single root folder, `void-undergrounds-vanilla_0.1.0`, with
`info.json`, `data-final-fixes.lua`, `README.md`, and `LICENSE` inside.

## How it works

The entire change runs once during the data stage in `data-final-fixes.lua`.
It targets only:

| Vanilla entity | Underground mask location | Original range field |
| --- | --- | --- |
| `underground-belt` | `underground_collision_mask` | `max_distance = 5` |
| `fast-underground-belt` | `underground_collision_mask` | `max_distance = 7` |
| `express-underground-belt` | `underground_collision_mask` | `max_distance = 9` |
| `turbo-underground-belt` | `underground_collision_mask` | `max_distance = 11` |
| `pipe-to-ground` | `fluid_box.pipe_connections[*].underground_collision_mask`, for `connection_type = "underground"` | `max_underground_distance = 10` |

These numbers are prototype field values, not a promise of that many empty tiles
between endpoints. The engine keeps its normal distance and pairing rules.

Each affected mask is copied before removing `layers.empty_space`. The mod
preserves `lava_tile`, any other collision layers/options, belt speeds, fluid box
properties, and distance fields. Copying matters because Space Age assigns one
shared Lua table to the five masks; another prototype could also reference it.
The ordinary entity `collision_mask` and tile prototypes remain untouched, so
endpoint placement retains vanilla restrictions, including the requirement for
platform foundation at the endpoints. The game still handles all transport and
pairing through its normal underground systems.

There are no added entities, recipes, technologies, settings, migrations,
`control.lua`, tick handlers, or scripted item/fluid transfers.

## Limitations

- No Factorio executable with Space Age was available for validation. Loading,
  actual belt/fluid transfer, lava blocking, endpoint placement, and behavior
  after save/reload still need in-game checks.
- Prototype changes apply to these entity names on **all surfaces**. They cannot
  be scoped to platforms without additional machinery. Only `empty_space` is
  removed; this may also affect other tiles using that collision layer.
- Other mods' added underground entities are outside the scope. Existing custom
  ranges or speeds on the five vanilla names are preserved.
- Another mod running later in `data-final-fixes` can overwrite the same fields.
  Compatibility with overhaul mods and other Factorio versions is unverified.
- `factorio_version` targets 2.0; dependencies require base and Space Age 2.0.77
  or later. The inspected reference is exactly 2.0.77.

## Build and offline tests

Requirements: Python 3.9+ and a Lua interpreter for tests. Lua 5.2 is preferred;
the code also uses a subset supported by LuaJIT. No Python packages are needed.
Run from the repository root:

```sh
python3 scripts/test.py
python3 scripts/build.py
```

To select a specific interpreter:

```sh
LUA=/path/to/lua5.2 python3 scripts/test.py
```

The build script writes `dist/void-undergrounds-vanilla_0.1.0.zip`. It uses an
explicit file list, fixed timestamps and permissions, fixed entry order, and
stored ZIP entries so repeated builds of the same files are byte-identical,
independent of file mtimes, process umask, or zlib version. It excludes Git
metadata, scripts, tests, and documentation under `docs/`.

Tests execute the actual mod code against representative Lua fixtures, including
the vanilla shared-mask layout. They check all five target masks, preservation
of lava, ranges, speeds and placement data, unchanged other prototypes, custom
collision options, normal/linked pipe connections, missing data, and idempotence.
Python checks metadata and ZIP structure, contents, CRCs, and reproducibility.
Fixtures are not the Factorio loader or a transport simulation. See
[validation details](docs/VALIDATION.md) for results and exact reference hashes.

An additional reference check downloads six pinned official files into a
separate cache, verifies their SHA-256 hashes and API types, and executes the
original shared-mask assignment block with the official `table.deepcopy`
helper and this mod. It also checks the original range and speed values:

```sh
python3 scripts/check_reference.py /tmp/void-undergrounds-reference --download
# Reuse the cache offline afterward:
python3 scripts/check_reference.py /tmp/void-undergrounds-reference
```

This deliberately executes only those source fragments, not the full game data
stage. `LUA` can select the interpreter for this check as well. Repository scripts
and `docs/` are available in the source repository, outside the installable ZIP.

## Manual test on Factorio 2.0.77

Use a **separate test profile** and a fresh disposable Space Age game, with only
the official mods and this mod enabled. Keep your normal mods directory and
existing saves separate. Compare against the same setup with this mod disabled.

1. Confirm the exact Factorio version and that startup reaches the menu without
   a prototype validation error.
2. In the map editor, prepare a space platform with two foundation areas separated
   by a narrow gap of actual empty-space tiles. Keep the areas attached to the
   hub by a foundation detour if needed: platform foundation connectivity is a
   separate vanilla rule and is unchanged by this mod.
3. For each of the four belt tiers, place a correctly aligned input/output pair
   on foundation, within its normal range, across the gap. Feed items and confirm
   continuous arrival at the output. Repeat in another orientation.
4. Connect two pipe-to-ground endpoints across the gap, supply a fluid, and confirm
   actual flow into the receiving network. Verify both endpoints remain on foundation.
5. For each entity, compare a solid-foundation layout and an empty-space layout at
   the normal maximum range, then one tile beyond it. The extra distance must
   remain disconnected. Compare belt throughput with the baseline; this mod
   should not change it.
6. Attempt to place each endpoint on empty space: ordinary placement must fail.
   On Vulcanus, put a lava tile between otherwise valid endpoints and verify the
   underground link stays blocked, for belts and pipes.
7. Save and reload **only the disposable test save**, then confirm the links and
   actual transport persist. Check ordinary ground undergrounds and unrelated
   logistics still behave as in the baseline.

Record the game version, enabled mods, layouts, and observations when reporting
results. Automated tests do not substitute for this checklist.

## Technical references

- [Space Age's shared mask assignments, tag 2.0.77](https://github.com/wube/factorio-data/blob/2.0.77/space-age/base-data-updates.lua#L20-L26)
- [UndergroundBeltPrototype API 2.0.77](https://lua-api.factorio.com/2.0.77/prototypes/UndergroundBeltPrototype.html#underground_collision_mask)
- [PipeConnectionDefinition API 2.0.77](https://lua-api.factorio.com/2.0.77/types/PipeConnectionDefinition.html#underground_collision_mask)
- [CollisionMaskConnector API 2.0.77](https://lua-api.factorio.com/2.0.77/types/CollisionMaskConnector.html)
- [Machine-readable API 2.0.77](https://lua-api.factorio.com/2.0.77/prototype-api.json)
- [Core collision mask utilities 2.0.77](https://github.com/wube/factorio-data/blob/2.0.77/core/lualib/collision-mask-util.lua)

MIT licensed. Unofficial community mod, not affiliated with Wube Software.
