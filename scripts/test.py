#!/usr/bin/env python3
"""Run metadata, Lua prototype, syntax, and deterministic packaging checks offline."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from zipfile import ZipFile

from build import MOD_FILES, ROOT, build


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


class ModTests(unittest.TestCase):
    def test_metadata(self):
        info = json.loads(
            (ROOT / "info.json").read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_keys,
        )
        self.assertEqual(info["name"], "void-undergrounds-vanilla")
        self.assertEqual(info["version"], "0.1.0")
        self.assertRegex(info["version"], r"^\d+\.\d+\.\d+$")
        self.assertEqual(info["title"], "Void Undergrounds Vanilla")
        self.assertTrue(info["author"])
        self.assertTrue(info["description"])
        self.assertEqual(info["factorio_version"], "2.0")
        self.assertEqual(
            info["dependencies"], ["base >= 2.0.77", "space-age >= 2.0.77"]
        )

    def test_lua_syntax_and_prototypes(self):
        interpreter = os.environ.get("LUA")
        if not interpreter:
            interpreter = next(
                (path for name in ("lua5.2", "lua", "lua5.4", "lua5.3", "luajit")
                 if (path := shutil.which(name))),
                None,
            )
        self.assertIsNotNone(interpreter, "Install Lua or set LUA to its executable path")
        subprocess.run([interpreter, "-v"], check=True)
        subprocess.run([interpreter, "tests/prototypes.lua"], cwd=ROOT, check=True)

    def test_archive_structure_integrity_and_reproducibility(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            first = build(base / "first")
            # Change the process umask: archive permissions must still be stable.
            previous_umask = os.umask(0o077)
            try:
                second = build(base / "second")
            finally:
                os.umask(previous_umask)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(first.name, "void-undergrounds-vanilla_0.1.0.zip")
            folder = "void-undergrounds-vanilla_0.1.0"
            with ZipFile(first) as archive:
                self.assertIsNone(archive.testzip())
                self.assertEqual(
                    archive.namelist(), [f"{folder}/{name}" for name in MOD_FILES]
                )
                for filename in MOD_FILES:
                    member = archive.getinfo(f"{folder}/{filename}")
                    self.assertEqual(archive.read(member), (ROOT / filename).read_bytes())
                    self.assertEqual(member.external_attr >> 16, 0o100644)
                    self.assertEqual(member.date_time, (1980, 1, 1, 0, 0, 0))
                metadata = json.loads(archive.read(f"{folder}/info.json"))
                self.assertEqual(folder, f"{metadata['name']}_{metadata['version']}")

    def test_only_intended_mod_entrypoint(self):
        self.assertEqual(
            sorted(path.name for path in ROOT.glob("*.lua")), ["data-final-fixes.lua"]
        )
        self.assertNotIn("control.lua", MOD_FILES)
        self.assertFalse((ROOT / "settings.lua").exists())
        self.assertIn("MIT License", (ROOT / "LICENSE").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
