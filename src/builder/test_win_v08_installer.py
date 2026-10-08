"""Synthetic checks for the click-to-install GUI's safety and baseline behavior."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import win_v08_installer as app


class WindowsGuiSafetyTests(unittest.TestCase):
    def test_source_config_uses_bundled_source_tree(self):
        root = app.embedded_root()
        self.assertTrue((root / "runtime" / "inventory.json").is_file())
        mod_stage, mod_builder, mod_qa = app.configure_embedded_sources(root)
        self.assertEqual(mod_stage.RUNTIME, root / "runtime")
        self.assertEqual(mod_builder.RUNTIME, root / "runtime")
        self.assertEqual(mod_qa.RUNTIME, root / "runtime")

    def test_preflight_accepts_only_verified_install_packages_with_font(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            game = root / "Castaway"
            source = root / "bundle"
            (game / "TSData").mkdir(parents=True)
            for rel in app.FONT_RELATIVE:
                p = game / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(b"fake font indicator")
            inventory = []
            for n in range(10):
                rel = f"TSData/Res/Text/sample-{n}.package"
                p = game / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                payload = f"pretend original package #{n}".encode()
                p.write_bytes(payload)
                inventory.append({
                    "package": rel,
                    "sha256": hashlib.sha256(payload).hexdigest(),
                    "bytes": len(payload),
                })
            inventory.extend({
                "package": f"TSData/Res/UserData/Neighborhoods/N00{n}/save.package"
            } for n in (1, 2))
            (source / "runtime").mkdir(parents=True)
            (source / "runtime" / "inventory.json").write_text(json.dumps(inventory))
            with (patch("win_v08_installer.embedded_root", return_value=source),
                  patch("win_v08_installer.game_running", return_value=False)):
                selected = app.preflight(game)
                self.assertEqual(len(selected), 10)
                self.assertTrue(all("UserData" not in r["package"] for r in selected))
                (game / selected[0]["package"]).write_bytes(b"previously patched")
                # Mismatched file is ONLY allowed to proceed to deep DBPF row validation.
                # GUI preflight never directly modifies package bytes.
                self.assertEqual(len(app.preflight(game)), 10)
                (game / app.FONT_RELATIVE[0]).unlink()
                with self.assertRaisesRegex(RuntimeError, "font"):
                    app.preflight(game)

    def test_backups_are_discovered_only_for_same_install_location(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            game = root / "Castaway"
            game.mkdir()
            backup_base = root / "backups"
            leaf = backup_base / app.game_identifier(game) / "20261009-foo"
            leaf.mkdir(parents=True)
            (leaf / "restore_manifest.json").write_text(json.dumps({
                "installation": str(game.resolve()), "schema": "TSCTW-V08-RESTORE-1",
            }))
            with patch("win_v08_installer.backup_base", return_value=backup_base):
                self.assertEqual(app.latest_backup(game), leaf)
                other = root / "OtherCastaway"
                other.mkdir()
                self.assertIsNone(app.latest_backup(other))
            self.assertFalse((game/"restore_manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
