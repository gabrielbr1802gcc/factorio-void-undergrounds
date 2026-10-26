Experimental release targeting **Factorio 2.0.77 + Space Age**.

Removes only `empty_space` from the underground collision masks of the four
vanilla underground belts and the vanilla pipe-to-ground's underground
connections. Masks are copied first to avoid modifying shared tables.
`lava_tile`, endpoint placement collisions, original ranges, speeds, and fluid
properties are preserved. No new prototypes or runtime scripts are added.

**Validation:** checked the official 2.0.77 source and prototype API, parsed and
executed the Lua with standalone interpreters, tested representative prototype
fixtures for unintended changes, and checked the installable ZIP's contents,
integrity, and byte-for-byte build reproducibility. These are static/offline
checks, not a Factorio engine test.

**No in-game test was possible:** a compatible Factorio + Space Age executable
was not available. Successful loading and actual transport across empty space
are unconfirmed. Manual testing is still required for belts, fluids, normal
range limits, lava blocking, invalid endpoint placement, and save/reload.
See the README's manual test instructions and `docs/VALIDATION.md`.

Download the attached **`void-undergrounds-vanilla_0.1.0.zip`** and copy it, still
zipped, into a separate Factorio test profile's `mods` directory. Enable Space
Age and the mod, then restart. Use a disposable game for initial validation.
GitHub's automatic **Source code (zip)** and **Source code (tar.gz)** downloads
are not the installable Factorio package.

The mod version is `0.1.0`; `v0.1.0-beta` is this GitHub pre-release's tag.
