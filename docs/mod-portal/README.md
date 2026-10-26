# First Factorio Mod Portal submission

Status: **prepared, not published by the agent**. No Factorio.com authentication
was explicitly supplied for this workflow or available through a connected
Factorio tool. No private credentials were searched, extracted, or committed.
GitHub CLI authentication does not authenticate a Factorio.com account.

The public mod-details API returned HTTP 404, and a public list query for this
name with Factorio version `2.0.77` returned no results during preparation.
Direct requests to the Mod Portal website returned HTTP 403 in this environment.
There is no confirmed public mod page or in-game mod-manager listing yet.

## Ready-to-submit material

| Field | Value |
| --- | --- |
| Title | Void Undergrounds Vanilla |
| Internal name | `void-undergrounds-vanilla` |
| Version | `0.1.0` |
| Category | Tweaks (`tweaks`) |
| Tags | Logistics (`logistics`), Fluids (`fluids`) |
| License | MIT (`default_mit`) |
| Factorio compatibility | `2.0` |
| Required mods | `base >= 2.0.77`, `space-age >= 2.0.77` |
| Source | https://github.com/gabrielbr1802gcc/factorio-void-undergrounds |
| Homepage | https://github.com/gabrielbr1802gcc/factorio-void-undergrounds |
| Package | `void-undergrounds-vanilla_0.1.0.zip` |

The summary and portal enum values are in [listing.json](listing.json).
Paste [description.md](description.md) into the portal's long description.
Compatibility and dependencies come from the `info.json` inside the ZIP;
category, tags, license, and source are portal listing fields, not additional
Factorio prototype changes. The listing JSON contains no credentials and is
preparation metadata; uploading the ZIP alone does not apply all these fields.

## Manual publication through Factorio.com

1. Sign in to your own Factorio.com account on the
   [official Mod Portal](https://mods.factorio.com/) and choose **Submit mod**.
2. Download the attached installable ZIP from the
   [GitHub v0.1.0 release](https://github.com/gabrielbr1802gcc/factorio-void-undergrounds/releases/tag/v0.1.0),
   or generate it locally with `python3 scripts/build.py`. Upload that ZIP,
   still zipped, rather than a GitHub Source code archive.
3. Confirm the internal name, title, and version from the ZIP. Set Category to
   **Tweaks**, tags to **Logistics** and **Fluids**, license to **MIT**, and the
   source/homepage to the repository URL above. Use the summary in `listing.json`
   and paste the entire Markdown in `description.md` as the long description.
4. Complete submission and confirm that the mod is public and not deprecated.
   If the mod name or release `0.1.0` already exists by then, inspect its owner
   and contents first; do not create a conflicting entry or upload a second
   release with the same version.

Expected public URL after successful submission:
https://mods.factorio.com/mod/void-undergrounds-vanilla

This is a destination URL, not evidence that publication has happened.

## Verify after submission

Open the public page while logged out and confirm the title, category, both
tags, MIT license, and source link. On its Downloads and Dependencies tabs,
confirm release **0.1.0**, **Factorio 2.0** compatibility, and mandatory
**Space Age**. Check that the package filename matches the GitHub asset.

The following public API URLs need no credentials:

- [Full mod details](https://mods.factorio.com/api/mods/void-undergrounds-vanilla/full)
- [Listing for Factorio 2.0.77](https://mods.factorio.com/api/mods?namelist=void-undergrounds-vanilla&version=2.0.77)

The first response must include release `0.1.0` with
`info_json.factorio_version = "2.0"`, the two required dependencies, the expected
filename, and the correct source/category/tags/license. The second must return
this mod in `results`. Its release `sha1` can be compared with the local ZIP's
SHA-1; use SHA-256 as well for the local/GitHub asset comparison.

Finally, start Factorio **2.0.77 + Space Age** in a separate test profile, open
the in-game **Mods** manager, search for **Void Undergrounds Vanilla**, install
release `0.1.0`, and confirm that the game accepts its dependencies and loads.
Portal metadata checks alone do not prove installation through the game UI.

Record the resulting public URL and verification results in `docs/VALIDATION.md`
and update the README's publication status only after these checks pass. The
general user game-test report does not confirm a Mod Portal installation.

## Official API route for a future authenticated workflow

The official [Mod publish API](https://wiki.factorio.com/Mod_publish_API)
creates a new mod via `init_publish`, then uploads the ZIP to the returned URL.
It requires a key with **ModPortal: Publish Mods** permission. The initial
upload accepts description, category, license, and source URL.

The official [Mod details API](https://wiki.factorio.com/Mod_details_API)
applies title, summary, tags and other listing fields with
**ModPortal: Edit Mods** permission. Updating an existing mod's releases uses
the separate [Mod upload API](https://wiki.factorio.com/Mod_upload_API) and
**ModPortal: Upload Mods** permission. These are separate from GitHub access.
No authenticated API request was attempted for this submission.
