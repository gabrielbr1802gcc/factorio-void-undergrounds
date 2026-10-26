# Validation of 0.1.0

Target inspected: **Factorio 2.0.77 + Space Age**.

**The user installed and tested Void Undergrounds Vanilla in Factorio 2.0.77
with Space Age and confirmed that it works.** This report was provided while
preparing the first public 0.1.0 release, after the `v0.1.0-beta` release.

## User-reported in-game validation

The evidence is the user's confirmation of successful installation and general
functionality. No scenario-by-scenario results, logs, screenshots, layouts, or
measurements were supplied. This is user-reported validation; the agent did not
run the Factorio executable or independently observe the game test.

| In-game scenario | Evidence status |
| --- | --- |
| Installation and general functionality on 2.0.77 + Space Age | CONFIRMED BY USER |
| Each of the four belt tiers and individual belt/fluid scenarios | PENDING specific results |
| Lava continues to block underground connections | PENDING specific results |
| Exact maximum range and one tile beyond | PENDING specific results |
| Throughput measurements against a vanilla baseline | PENDING specific results |
| Rejected endpoint placement in empty space | PENDING specific results |
| Behavior after save/reload | PENDING specific results |
| Ordinary logistics and compatibility with other mods | PENDING specific results |

The earlier beta documentation correctly recorded that no engine test had been
performed at that point. The user report supersedes that general status without
establishing coverage of the individual scenarios above. The stable `v0.1.0`
release keeps `data-final-fixes.lua` byte-identical to `v0.1.0-beta`. Existing
saves and user mod folders were not modified by the agent.

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
| Installable ZIP | PASS | Exact root directory and five expected files; bytes, CRCs, modes and timestamps checked |
| Reproducible build | PASS | Two outputs byte-identical, including under different process umasks |
| Changelog format | PASS | Official 2.0.77 format checked: 99-dash separator, version/date, category/entry indentation, no duplicate entries or trailing whitespace |
| Portal listing preparation | PASS | Internal name, title, summary, category, tags, MIT enum, source, Factorio version and dependencies checked against the requested values and package metadata |
| Lua unchanged from beta | PASS | Byte-for-byte comparison with `v0.1.0-beta:data-final-fixes.lua` |
| Official 2.0.77 references | PASS | Six pinned hashes, API field types, original ranges/speeds, actual shared-mask assignments and official copy helper verified |
| General in-game functionality on 2.0.77 + Space Age | USER CONFIRMED | Installation and general operation reported by the user; detailed matrix remains pending |
| Factorio engine test executed by the agent | NOT RUN | No compatible installation was available to the agent |

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

These checks were rerun for the public release. They use representative fixtures
and selected official source fragments, not the complete Factorio data loader.
They verify prototype values and packaging; the user report is the separate
evidence of general in-game functionality. Neither establishes the complete
in-game scenario coverage listed above.

The new changelog was checked against the
[official 2.0.77 changelog format](https://lua-api.factorio.com/2.0.77/auxiliary/changelog-format.html).
Portal listing checks validate the prepared files; they do not indicate portal
publication or server-side acceptance.

## Remaining manual validation

Use the README's manual checklist in an isolated test profile and a disposable
Space Age game on exactly 2.0.77 to document every belt tier, individual item and
fluid scenarios, exact range boundaries, measured throughput, lava blocking,
rejected endpoint placement, ordinary logistics, and save/reload. These specific
results remain pending; they must not be inferred from the general confirmation.

## Mod Portal publication status

The first 0.1.0 submission is prepared, but it has not been published by the
agent. No Factorio.com authentication was explicitly supplied or available
through a connected Factorio tool, and private credential stores were not
searched. The public mod-details API returned HTTP 404 and the public list query
for `void-undergrounds-vanilla` with `version=2.0.77` returned no results during
preparation. Direct website requests returned HTTP 403 in this environment.

After manual submission, the public page, release `0.1.0`, Factorio `2.0`
compatibility, mandatory Space Age dependency, and in-game mod-manager listing
still need verification. See [the publication instructions](mod-portal/README.md).
