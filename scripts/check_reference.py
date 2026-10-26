#!/usr/bin/env python3
"""Verify the pinned official 2.0.77 API/source and execute its mask assignments.

Use --download to populate a separate cache directory. Without it, runs offline.
Only the relevant assignment block and deepcopy function are executed, not the
complete Factorio data stage or the game engine.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import urllib.request

from build import ROOT

SOURCE = "https://raw.githubusercontent.com/wube/factorio-data/2.0.77/"
REFERENCES = {
    "base-data-updates.lua": (SOURCE + "space-age/base-data-updates.lua",
        "574a7fb8d083eef5183bbf913f445457d75be59d4c871205d6239d485e5fcad3"),
    "base-transport-belts.lua": (SOURCE + "base/prototypes/entity/transport-belts.lua",
        "46cec8476aa185d82f4a40de4e8ff5852538447a4f4b8115ba6e97533b51bf6f"),
    "base-entities.lua": (SOURCE + "base/prototypes/entity/entities.lua",
        "26d738a076608130081d8cfa4a0d36dc39d2f98d40abb45735930b41841d06e4"),
    "transport-belts.lua": (SOURCE + "space-age/prototypes/entity/transport-belts.lua",
        "6ede8b6ffe1f9118d4e58dc3d07f13165970650f5b5aef8489facfa6b174bb44"),
    "util.lua": (SOURCE + "core/lualib/util.lua",
        "2abc4d4ec3e8cd47cee197231ce45b7bc34cf7a1aaa841cdfe3b776d67094a1f"),
    "prototype-api.json": ("https://lua-api.factorio.com/2.0.77/prototype-api.json",
        "29772ece6140b515d295a504c6f9ac5bc9e653d8b1470e8cd6db825f93fcc756"),
}


def check(directory, download):
    directory.mkdir(parents=True, exist_ok=True)
    sources = {}
    for filename, (url, digest) in REFERENCES.items():
        path = directory / filename
        if download:
            with urllib.request.urlopen(url, timeout=30) as response:
                content = response.read()
            if hashlib.sha256(content).hexdigest() != digest:
                raise ValueError(f"Reference hash mismatch: {filename}")
            path.write_bytes(content)
        content = path.read_bytes()
        if hashlib.sha256(content).hexdigest() != digest:
            raise ValueError(f"Reference hash mismatch: {filename}")
        sources[filename] = content.decode("utf-8")
    print("PASS six official reference files match their pinned SHA-256 hashes", flush=True)

    api = json.loads(sources["prototype-api.json"])
    assert api["application_version"] == "2.0.77"
    properties = {}
    for section in ("prototypes", "types"):
        for entry in api[section]:
            properties[entry["name"]] = {p["name"]: p for p in entry.get("properties", [])}
    for owner in ("UndergroundBeltPrototype", "PipeConnectionDefinition"):
        assert properties[owner]["underground_collision_mask"]["type"] == "CollisionMaskConnector"
    assert properties["PipeToGroundPrototype"]["fluid_box"]["type"] == "FluidBox"
    assert properties["FluidBox"]["pipe_connections"]["type"] == {
        "complex_type": "array", "value": "PipeConnectionDefinition"
    }
    assert properties["CollisionMaskConnector"]["layers"]["type"] == {
        "complex_type": "dictionary", "key": "CollisionLayerID",
        "value": {"complex_type": "literal", "value": True}
    }
    assert 'Only loaded if `connection_type` is `"underground"`.' in (
        properties["PipeConnectionDefinition"]["underground_collision_mask"]["description"]
    )
    print("PASS exact 2.0.77 API types and nested pipe connection location", flush=True)

    names = ["underground-belt", "fast-underground-belt",
             "express-underground-belt", "turbo-underground-belt"]
    definitions = []
    for index, name in enumerate(names):
        source = sources["transport-belts.lua" if index == 3 else "base-transport-belts.lua"]
        block = source.split(f'name = "{name}",', 1)[1].split("\n  },", 1)[0]
        distance = int(re.search(r"max_distance = (\d+)", block).group(1))
        speed = float(re.search(r"speed = ([\d.]+)", block).group(1))
        assert distance == (5, 7, 9, 11)[index]
        assert speed == (0.03125, 0.0625, 0.09375, 0.125)[index]
        definitions.append(f'[{json.dumps(name)}] = {{max_distance = {distance}, speed = {speed}}}')
    pipe_source = sources["base-entities.lua"].split('name = "pipe-to-ground",', 1)[1]
    assert int(re.search(r"max_underground_distance = (\d+)", pipe_source).group(1)) == 10
    print("PASS original belt distances/speeds and pipe underground distance", flush=True)

    assignments = sources["base-data-updates.lua"].split(
        "local underground_collision_mask = ", 1
    )[1].split("\nfor k = 1, 7 do", 1)[0]
    assignments = "local underground_collision_mask = " + assignments
    assert assignments.count("= underground_collision_mask") == 5
    helper = sources["util.lua"].split("function table.deepcopy(object)", 1)[1]
    helper = "function table.deepcopy(object)" + helper.split("function table.compare", 1)[0]
    script = helper + "\nlocal belts = {" + ",".join(definitions) + "}\n" + """
local connections = {{}, {connection_type = "underground", max_underground_distance = 10}}
data = {raw = {
  ["underground-belt"] = belts,
  ["pipe-to-ground"] = {["pipe-to-ground"] = {fluid_box = {pipe_connections = connections}}}
}}
""" + assignments + """
local shared = belts["underground-belt"].underground_collision_mask
assert(shared.layers.empty_space and shared.layers.lava_tile)
for _, belt in pairs(belts) do assert(belt.underground_collision_mask == shared) end
assert(connections[2].underground_collision_mask == shared)
local before = table.deepcopy(data.raw)
dofile(arg[1])
for name, belt in pairs(belts) do
  assert(belt.underground_collision_mask.layers.empty_space == nil)
  assert(belt.underground_collision_mask.layers.lava_tile == true)
  assert(belt.max_distance == before["underground-belt"][name].max_distance)
  assert(belt.speed == before["underground-belt"][name].speed)
end
assert(connections[2].underground_collision_mask.layers.empty_space == nil)
assert(connections[2].underground_collision_mask.layers.lava_tile == true)
assert(connections[2].max_underground_distance == 10)
assert(shared.layers.empty_space == true)
print("PASS actual upstream shared-mask assignments and deepcopy helper with this mod")
"""
    interpreter = os.environ.get("LUA") or shutil.which("lua5.2") or shutil.which("luajit") or shutil.which("lua")
    if not interpreter:
        raise RuntimeError("Install Lua or set LUA to its executable path")
    with tempfile.TemporaryDirectory() as temporary:
        path = Path(temporary) / "reference-check.lua"
        path.write_text(script, encoding="utf-8")
        subprocess.run([interpreter, str(path), str(ROOT / "data-final-fixes.lua")], check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Separate directory for the official reference files")
    parser.add_argument("--download", action="store_true", help="Fetch pinned public references first")
    args = parser.parse_args()
    check(args.directory, args.download)
