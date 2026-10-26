## Vanilla underground connections across platform gaps

**Void Undergrounds Vanilla** allows vanilla underground belts and
pipe-to-ground connections to cross gaps of empty space between supported areas
of a space platform. Both endpoints still need to stand on valid foundation.

It works with the vanilla underground belt, fast underground belt, express
underground belt, turbo underground belt, and pipe-to-ground. Existing entities
and the game's normal underground connection system do the work.

### Minimal change, vanilla transport

- Original underground distance fields are preserved. This mod does not extend
  underground reach.
- Belt speeds and fluid properties are unchanged. No throughput properties are
  increased.
- No new entities, recipes, or technologies are added.
- No scripted teleportation or item/fluid transfers are used.
- The lava collision restriction is retained.
- Endpoints cannot be built directly in empty space through this mod.

The implementation removes only `empty_space` from the relevant underground
collision masks during the data stage. It adds no runtime scripts or tick
handlers. Ordinary placement collision masks and unrelated prototypes are left
alone.

### Compatibility and validation

Requires **Factorio 2.0.77 or later in the 2.0 series, with Space Age enabled**.
The inspected API and the reported game test are for **2.0.77 + Space Age**.

General functionality has been confirmed in a user-reported game test on that
version. Specific results for every belt tier, individual belt/fluid
scenarios, lava blocking, exact range boundaries, throughput measurements,
endpoint placement, and save/reload have not been reported and remain pending.
Automated prototype and packaging tests also pass; these are separate from the
user's in-game report.

The changes apply to the five vanilla entity names on all surfaces. Other mods
can override the same masks, and custom underground entities are outside this
mod's scope. Platform foundation connectivity rules still apply.

[Source code, validation details, and issue reports](https://github.com/gabrielbr1802gcc/factorio-void-undergrounds)

License: **MIT**. Unofficial community mod, not affiliated with Wube Software.
