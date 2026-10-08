"""Rebase safety tests: already-patched runtime packages with exact auditable rows."""
import unittest
import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from test_runtime_dbpf_writer import fixture
from runtime_dbpf import Package, parse_table, encode_table
from check_runtime_packages import apply
from safe_rebase_runtime import inspect_prepatched
from prepare_v08_test import build
from install_v08_local import install, restore


REL = "TSData/Res/Objects/objects.package"
MAPS = {"menu": {"Examine": "Xem xét"}}


def inputs():
    original, keys=fixture(24)
    rows=[{"package":REL,"key":list(keys[0]),"row":row,"language":row+1,
           "en":"Examine","description":"Castaway action","category":"menu"}
          for row in (0,1)]
    inventory={"package":REL, "sha256":hashlib.sha256(original).hexdigest(),
               "bytes":len(original), "index_width":24,"resources":2,"errors":[]}
    return original,rows,inventory


def partially_translated(original, rows):
    # Modify ONLY the first vetted source row to an already-approved Vietnamese value.
    return apply(original,rows[:1],MAPS,set(),{})[0]


class SafeRebaseTests(unittest.TestCase):
    def test_prepatched_file_exact_source_and_approved_vi_both_accepted(self):
        original,rows,item=inputs()
        modified=partially_translated(original,rows)
        self.assertNotEqual(original,modified)
        report=inspect_prepatched(modified,item,rows,MAPS,set(),{})
        self.assertEqual(report["english_source_rows"],1)
        self.assertEqual(report["already_approved_vietnamese_rows"],1)
        self.assertEqual(report["verified_row_count"],2)

    def test_unknown_translation_is_rejected(self):
        original,rows,item=inputs()
        p=Package(original)
        entry=next(x for x in p.entries if x.key==tuple(rows[0]["key"]))
        raw=p.raw(entry)
        parsed,_=parse_table(raw)
        parsed[0][1]="NOT AN APPROVED TRANSLATION"
        changed=p.patch({entry.key:encode_table(raw,parsed)})
        with self.assertRaisesRegex(ValueError, "Unrecognized translated"):
            inspect_prepatched(changed,item,rows,MAPS,set(),{})

    def test_older_vietnamese_is_preserved_and_other_english_is_translated(self):
        original,rows,item=inputs()
        pkg=Package(original)
        entry=next(x for x in pkg.entries if x.key==tuple(rows[0]["key"]))
        raw=pkg.raw(entry)
        values,_=parse_table(raw)
        values[0][1]="Tôi đây!"  # A historical translation not equal to current mapping.
        previous=pkg.patch({entry.key:encode_table(raw,values)})
        with self.assertRaisesRegex(ValueError, "Unrecognized translated"):
            inspect_prepatched(previous,item,rows,MAPS,set(),{})
        result=inspect_prepatched(previous,item,rows,MAPS,set(),{},preserve_unrecognized=True)
        self.assertEqual(result["unrecognized_rows_preserved"],1)
        self.assertEqual(result["english_source_rows"],1)
        final,changed,res=apply(previous,rows,MAPS,set(),{},preserve_unrecognized=True)
        self.assertEqual((changed,res),(1,1))
        final_pkg=Package(final)
        final_entry=next(x for x in final_pkg.entries if x.key==tuple(rows[0]["key"]))
        translated,_=parse_table(final_pkg.raw(final_entry))
        self.assertEqual([r[1] for r in translated[:2]],["Tôi đây!","Xem xét"])
        self.assertEqual(apply(final,rows,MAPS,set(),{},preserve_unrecognized=True)[0],final)
        self.assertEqual(final_pkg.raw(next(x for x in final_pkg.entries if x.key!=tuple(rows[0]["key"]))),
                         pkg.raw(next(x for x in pkg.entries if x.key!=tuple(rows[0]["key"]))))

    def test_unknown_value_does_not_bypass_metadata_identity(self):
        original,rows,item=inputs()
        modified=partially_translated(original,rows)
        bad=[dict(rows[0],description="Incorrect metadata"),rows[1]]
        with self.assertRaisesRegex(ValueError, "metadata mismatch"):
            inspect_prepatched(modified,item,bad,MAPS,set(),{},preserve_unrecognized=True)
        with self.assertRaisesRegex(ValueError, "metadata differs"):
            apply(modified,bad,MAPS,set(),{},preserve_unrecognized=True)

    def test_wrong_structure_is_rejected(self):
        original,rows,item=inputs()
        modified=partially_translated(original,rows)
        item=dict(item,resources=3)
        with self.assertRaisesRegex(ValueError, "DBPF structure"):
            inspect_prepatched(modified,item,rows,MAPS,set(),{})

    def test_unrelated_binary_changes_preserved_by_safe_rebase(self):
        original,rows,item=inputs()
        p=Package(original)
        other=next(x for x in p.entries if x.key!=tuple(rows[0]["key"]))
        binary=p.patch({other.key:b"pre-existing object mod retained"})
        translated=partially_translated(binary,rows)
        report=inspect_prepatched(translated,item,rows,MAPS,set(),{})
        self.assertEqual(report["already_approved_vietnamese_rows"],1)
        final,changed,_=apply(translated,rows,MAPS,set(),{})
        self.assertEqual(changed,1)
        q=Package(final)
        second=next(x for x in q.entries if x.key==other.key)
        self.assertEqual(q.raw(second),b"pre-existing object mod retained")

    def test_build_from_modified_runtime_installs_then_restores_exact_previous_bytes(self):
        original,rows,item=inputs()
        modified=partially_translated(original,rows)
        with TemporaryDirectory() as tmp:
            root=Path(tmp)
            game=root/"game"
            input_root=root/"input"
            core=root/"unused_core"
            output=root/"candidate"
            game_path=game/REL
            staged=input_root/REL
            for path in (game_path,staged):
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_bytes(modified)
            audit={"parse_errors":0,"untranslated_or_review_candidate_rows":0,"candidate_rows":2}
            with (patch("prepare_v08_test.assess",return_value=(audit,[])),
                  patch("prepare_v08_test.source_inventory",return_value=[item]),
                  patch("prepare_v08_test.effective_records",return_value=(rows,[])),
                  patch("prepare_v08_test.load_maps",return_value=MAPS),
                  patch("prepare_v08_test.load_row_translations",return_value=[])):
                with self.assertRaisesRegex(ValueError, "original missing/hash mismatch"):
                    build(core,input_root,root/"strict",runtime_only=True)
                result=build(core,input_root,output,runtime_only=True,allow_prepatched_runtime=True)
            self.assertEqual(result["modified_baseline_checks"][0]["already_approved_vietnamese_rows"],1)
            self.assertEqual(result["install_files"][0]["changed_rows"],1)
            backup=root/"backup"
            self.assertIn("DRY RUN",install(output,game,backup)["result"])
            install(output,game,backup,dry_run=False)
            self.assertNotEqual(game_path.read_bytes(),modified)
            restore(game,backup,dry_run=False)
            self.assertEqual(game_path.read_bytes(),modified)
            self.assertEqual((backup/REL).read_bytes(),modified)


if __name__=="__main__":
    unittest.main()
