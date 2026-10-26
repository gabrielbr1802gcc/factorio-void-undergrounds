First public **0.1.0** release of Void Undergrounds Vanilla for
**Factorio 2.0.77 + Space Age**.

The user installed and tested the mod in that game version and confirmed that
it works. This confirms general functionality; no specific results were supplied
for every belt tier, individual belt/fluid scenarios, lava blocking, exact range
boundaries, throughput, endpoint placement, or save/reload. Those detailed checks
remain pending. The agent did not independently run Factorio.

The Lua implementation is unchanged from `v0.1.0-beta`: it removes only
`empty_space` from the four vanilla underground belt masks and vanilla
pipe-to-ground's underground connections. It preserves `lava_tile`, placement
collision data, original range/speed fields, and other prototype properties.
There are no added entities, recipes, technologies, runtime handlers, or
scripted item/fluid transfers.

Updated the documentation to record the user report and its limits. Added
homepage metadata, a Factorio changelog, and an English Mod Portal description
with submission metadata and manual publication instructions. The Mod Portal
submission is prepared; publication and mod-manager availability are pending
Factorio.com authentication and subsequent verification.

Automated checks were rerun: metadata and Lua syntax, 6 prototype regression
cases under Lua 5.2.1 and LuaJIT, 4 official-reference verification groups, and
ZIP contents, integrity and byte-for-byte build reproducibility. These checks
remain distinct from the user's in-game report. See
[VALIDATION.md](https://github.com/gabrielbr1802gcc/factorio-void-undergrounds/blob/v0.1.0/docs/VALIDATION.md).

Download the attached **`void-undergrounds-vanilla_0.1.0.zip`**. Keep it zipped
when copying it to your Factorio profile's `mods` folder. GitHub's automatic
**Source code** archives are not the installable mod package.

The internal mod version remains `0.1.0`. The historical `v0.1.0-beta` tag and
its asset are preserved; `v0.1.0` identifies this public release without moving
or replacing the beta tag.
