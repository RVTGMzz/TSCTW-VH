"""Pure-file preflight regression checks; requires NO commercial game packages."""
import hashlib
import tempfile
import unittest
from pathlib import Path

from stage_runtime_inputs import inspect, source_for, inside


class BaselinePreflightTests(unittest.TestCase):
    def test_resolves_saved_neighborhoods_only_in_documents(self):
        game = Path("/fake/Castaway")
        save = Path("/fake/Documents/Castaway")
        self.assertEqual(
            source_for("TSData/Res/UserData/Neighborhoods/N001/N001_Neighborhood.package", game, save),
            save / "Neighborhoods/N001/N001_Neighborhood.package")
        self.assertEqual(
            source_for("TSData/Res/Text/Wants.package", game, save),
            game / "TSData/Res/Text/Wants.package")
        self.assertIsNone(source_for("TSData/Res/UserData/Neighborhoods/N002/N002_Neighborhood.package", game, None))

    def test_original_hash_and_missing_save_are_hard_gates(self):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            game = root / "game"
            save = root / "saves"
            pkg = "TSData/Res/Text/Wants.package"
            content = b"fake input, no commercial contents"
            path = game / pkg
            path.parent.mkdir(parents=True)
            path.write_bytes(content)
            item = {"package": pkg, "sha256": hashlib.sha256(content).hexdigest(), "bytes": len(content)}
            self.assertEqual(inspect([item], game, save)[0]["status"], "verified")
            path.write_bytes(b"incorrect baseline")
            self.assertEqual(inspect([item], game, save)[0]["status"], "baseline_mismatch")
            save_row = {"package": "TSData/Res/UserData/Neighborhoods/N001/N001_Neighborhood.package",
                        "sha256": "0" * 64, "bytes": 10}
            self.assertEqual(inspect([save_row], game, None)[0]["status"], "save_root_required")
            self.assertEqual(inspect([save_row], game, save)[0]["status"], "missing")

    def test_staging_folder_must_not_be_inside_game_or_save(self):
        base = Path("/fake/game")
        save = Path("/fake/documents")
        self.assertTrue(inside(base / "TSData/Res", base))
        self.assertTrue(inside(save / "Neighborhoods", save))
        self.assertFalse(inside(Path("/fake/work/input"), base))
        self.assertFalse(inside(Path("/fake/work/input"), save))


if __name__ == "__main__":
    unittest.main()
