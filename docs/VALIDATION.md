# Validation of 0.1.0 experimental

Target inspected: **Factorio 2.0.77 + Space Age**.

**No Factorio engine test was performed.** No Factorio executable was found on
PATH or in the checked home/project, `/opt`, `/usr/local`, `/usr/share`,
`/usr/games`, `/mnt`, and `/media` locations (bounded search). A compatible
Space Age installation was not available. Existing saves and user mod folders
were not modified. Loading and actual in-game transport remain unconfirmed.

## Official API and source verification

Downloaded the versioned `prototype-api.json`; its `application_version` is
`2.0.77`. Confirmed:

- `UndergroundBeltPrototype.underground_collision_mask` is an optional
  `CollisionMaskConnector`.
- `PipeToGroundPrototype.fluid_box` is a `FluidBox` whose `pipe_connections`
  contains `PipeConnectionDefinition` entries. The underground collision mask
  belongs to those entries, not to the pipe entity itself.
- `PipeConnectionDefinition.underground_collision_mask` is a
  `CollisionMaskConnector` used only for `connection_type = "underground"`.
  The API describes tiles between endpoints blocking a connection and requires
  matching masks at both ends.
- `CollisionMaskConnector.layers` maps collision layer IDs to `true`.
  Removing a key with `nil` is valid; the official core collision mask utility
  explicitly describes this operation.
- Space Age's `base-data-updates.lua`, lines 20–26, assigns one shared mask
  containing `lava_tile` and `empty_space` to the four named belts and
  `pipe-to-ground.fluid_box.pipe_connections[2]`.
- The official `core/lualib/util.lua` defines `table.deepcopy`. The mod copies
  each affected mask before deleting a layer to preserve other references.
- Original belt `max_distance` values are 5, 7, 9 and 11; `speed` values are
  0.03125, 0.0625, 0.09375 and 0.125. The pipe connection's
  `max_underground_distance` is 10. These are prototype values, not a measurement
  of empty tiles or throughput in the game.

Primary sources are linked in the [README](../README.md#technical-references).
The six reference files used by the repeatable check have their exact URLs and
SHA-256 hashes pinned in [check_reference.py](../scripts/check_reference.py).
No Wube source files are redistributed in the mod or source repository.

## Executed checks and results

Environment: Python 3.14.8; standalone Lua 5.2.1 built from lua.org's official
release in `/tmp`; existing LuaJIT 2.1.1767980792. No sudo, package installation,
or global Git configuration change was needed.

| Check | Result | Scope |
| --- | --- | --- |
| `info.json` parsing and required metadata | PASS | No duplicate keys; name, version, Factorio 2.0 and mandatory base/Space Age dependencies checked |
| Lua syntax and execution | PASS | Actual mod file parsed and executed with Lua 5.2.1 and LuaJIT |
| Four vanilla underground belts | PASS | Each expected `empty_space` key removed; lava retained |
| Vanilla underground fluid connection | PASS | Nested underground mask corrected; normal and linked connections untouched |
| Range, speed, placement and other data | PASS | Whole fixture comparison allows only the five intended layer removals |
| Other prototypes and shared references | PASS | Original shared table, custom entities, ordinary belts/pipes, tiles, recipes and technologies preserved |
| Custom mask layers/options | PASS | Unrelated layers and options preserved |
| Missing data and repeated execution | PASS | No errors or synthesized masks; repeated application has no additional effect |
| Installable ZIP | PASS | Exact root directory and four expected files; bytes, CRCs, modes and timestamps checked |
| Reproducible build | PASS | Two outputs byte-identical, including under different process umasks |
| Official 2.0.77 references | PASS | Six pinned hashes, API field types, original ranges/speeds, actual shared-mask assignments and official copy helper verified |
| Factorio loader and in-game behavior | NOT RUN | Requires an installed compatible Factorio + Space Age executable |

The regression suite reports **4 Python test groups and 6 Lua regression cases**
per interpreter. The reference check reports **4 additional verification groups**.
The whole-fixture comparison is deliberately broader than just checking mask
values: any other value added, removed or changed in those fixtures fails.

Commands used from the repository root:

```sh
LUA=/tmp/void-undergrounds-reference/lua-5.2.1/src/lua python3 scripts/test.py
python3 scripts/test.py
LUA=/tmp/void-undergrounds-reference/lua-5.2.1/src/lua \
  python3 scripts/check_reference.py /tmp/void-undergrounds-reference
python3 scripts/build.py
```

The reference files were downloaded separately from the pinned URLs before the
offline reference check. To reproduce on another machine, run that script once
with `--download` and a separate cache directory as described in the README.

These checks use representative fixtures and selected official source fragments;
they do not execute the complete Factorio data loader. Preserved prototype fields
support the intended vanilla behavior, but do not prove engine behavior.

## Remaining manual validation

Follow the README's manual test checklist using an isolated test profile and a
new disposable Space Age game on exactly 2.0.77. Confirm successful loading,
actual item and fluid transfer across empty space, vanilla range/throughput,
continued lava blocking, rejected endpoint placement in empty space, ordinary
logistics, and persistence after saving/reloading only the disposable save.
