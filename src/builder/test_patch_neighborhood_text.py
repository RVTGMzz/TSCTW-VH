"""Synthetic-only backup/restore test for opt-in N001/N002 localization."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_runtime_dbpf_writer import fixture
from patch_neighborhood_text import (
    apply_saved_neighborhood_updates, restore_saved_neighborhoods,
    build_saved_neighborhood_updates, guarded_source_paths, selector_translation_status, SAVE_ALIASES,
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

    def test_opt_in_selector_title_really_changes_source_and_restores(self):
        from runtime_dbpf import encode_table
        from diagnose_visible_strings import selector_source_matrix
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            save,original,_=self.prepare_fake_documents(root)
            original_package=Package(original)
            key=original_package.entries[0].key
            raw=original_package.raw(original_package.entries[0])
            rows,tail=parse_table(raw)
            en="Wanmami Island"
            vi="Đảo Wanmami"
            rows[0][1]=en
            source=original_package.patch({key:encode_table(raw,rows)})
            n002=save/"Neighborhoods/N002/N002_Neighborhood.package"
            n002.write_bytes(source)
            record={"package":SAVE_ALIASES["N002"],"key":list(key),"row":0,
                    "language":rows[0][0],"en":en,"description":rows[0][2],
                    "category":"ui"}
            backup=root/"backup"
            original_hash=n002.read_bytes()
            with (patch("patch_neighborhood_text.effective_records",return_value=([record],[])),
                  patch("patch_neighborhood_text.load_maps",return_value={"ui":{en:vi}}),
                  patch("patch_neighborhood_text.load_row_translations",return_value=[])):
                patched=apply_saved_neighborhood_updates(save,backup)
            self.assertEqual(patched["changed_rows"],1)
            after=selector_source_matrix([n002])["matches"]
            self.assertTrue(any(r["field"]=="island_title" and r["state"]=="vietnamese" for r in after))
            self.assertFalse(any(r["field"]=="island_title" and r["state"]=="english" for r in after))
            restore_saved_neighborhoods(save,backup)
            self.assertEqual(n002.read_bytes(),original_hash)
            self.assertEqual((save/"Neighborhoods/N001/N001_Neighborhood.package").read_bytes(),original)

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

    def test_selector_status_is_read_only_for_unrelated_synthetic_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            save,original,rows=self.prepare_fake_documents(root)
            before=selector_translation_status(save)
            self.assertFalse(before["runtime_read_precedence_verified"])
            self.assertTrue(all(v=={"english":0,"vietnamese":0} for v in before["fields"].values()))
            for island in ("N001","N002"):
                source=save/"Neighborhoods"/island/f"{island}_Neighborhood.package"
                self.assertEqual(source.read_bytes(),original)

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
