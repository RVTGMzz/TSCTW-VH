"""Synthetic-only backup/restore test for opt-in N001/N002 localization."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_runtime_dbpf_writer import fixture
from patch_neighborhood_text import (
    apply_saved_neighborhood_updates, restore_saved_neighborhoods,
    build_saved_neighborhood_updates, guarded_source_paths, SAVE_ALIASES,
)
from runtime_dbpf import Package, parse_table


class SaveLocalizationTests(unittest.TestCase):
    def prepare_fake_documents(self,root):
        save=root/"Electronic Arts"/"The Sims Castaway Stories"
        english,keys=fixture(24)
        for island in ("N001","N002"):
            p=save/"Neighborhoods"/island/f"{island}_Neighborhood.package"
            p.parent.mkdir(parents=True)
            p.write_bytes(english)
        rows=[{
            "package":SAVE_ALIASES[island], "key":list(keys[0]),
            "row":0,"language":1,"en":"Examine","description":"Castaway action",
            "category":"ui",
        } for island in ("N001","N002")]
        return save,english,rows

    def test_opt_in_saves_are_patched_and_restored_without_other_resource_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            save,original,rows=self.prepare_fake_documents(root)
            backup=root/"backups"/"20261009"
            with (patch("patch_neighborhood_text.effective_records",return_value=(rows,[])),
                  patch("patch_neighborhood_text.load_maps",return_value={"ui":{"Examine":"Xem xét"}}),
                  patch("patch_neighborhood_text.load_row_translations",return_value=[])):
                planned=build_saved_neighborhood_updates(save)
                self.assertEqual(len(planned),2)
                self.assertTrue(all(x["rows"]==1 for x in planned))
                self.assertTrue(all(x["source"].read_bytes()==original for x in planned))
                result=apply_saved_neighborhood_updates(save,backup)
            self.assertEqual(result["saved_files"],2)
            self.assertEqual(result["changed_rows"],2)
            self.assertTrue((backup/"restore_manifest.json").exists())
            for island in ("N001","N002"):
                active=save/"Neighborhoods"/island/f"{island}_Neighborhood.package"
                p=Package(active.read_bytes())
                rows_now,_=parse_table(p.raw(p.entries[0]))
                self.assertEqual(rows_now[0][1],"Xem xét")
                self.assertEqual(rows_now[1][1],"Examine")
                self.assertEqual((backup/"Neighborhoods"/island/active.name).read_bytes(),original)
            ret=restore_saved_neighborhoods(save,backup)
            self.assertEqual(ret["restored_files"],2)
            for island in ("N001","N002"):
                active=save/"Neighborhoods"/island/f"{island}_Neighborhood.package"
                self.assertEqual(active.read_bytes(),original)

    def test_refuses_to_erase_player_progress_after_save_changed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            save,original,rows=self.prepare_fake_documents(root)
            backup=root/"backups"/"20261009"
            with (patch("patch_neighborhood_text.effective_records",return_value=(rows,[])),
                  patch("patch_neighborhood_text.load_maps",return_value={"ui":{"Examine":"Xem xét"}}),
                  patch("patch_neighborhood_text.load_row_translations",return_value=[])):
                apply_saved_neighborhood_updates(save,backup)
            path=save/"Neighborhoods"/"N001"/"N001_Neighborhood.package"
            edited=b"player saved more progress"
            path.write_bytes(edited)
            with self.assertRaisesRegex(ValueError,"Save changed"):
                restore_saved_neighborhoods(save,backup)
            self.assertEqual(path.read_bytes(),edited)

    def test_missing_save_is_hard_failure_before_creating_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            save,original,rows=self.prepare_fake_documents(root)
            (save/"Neighborhoods"/"N002"/"N002_Neighborhood.package").unlink()
            with self.assertRaises(FileNotFoundError):
                apply_saved_neighborhood_updates(save,root/"backups"/"test")
            self.assertFalse((root/"backups").exists())


if __name__=="__main__":
    unittest.main()
