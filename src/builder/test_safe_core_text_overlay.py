"""Synthetic-only validation for exact-English core Text overlay."""
import json
import struct
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from runtime_dbpf import Package, parse_table
from safe_core_text_overlay import approved_core_locations, core_patch, collect_core_overlay
from install_v08_local import install, restore


def sample_source(value="Aspiration Rewards"):
    table = bytearray(68)
    table[64:66] = bytes([0xfd,0xff])
    struct.pack_into("<H",table,66,2)
    for lang,item in [(1,value),(2,"Do not translate other-language value")]:
        table.extend(bytes([lang])+item.encode("utf-8")+b"\0"+b"Cast UI COM\0")
    header=bytearray(96)
    header[:4]=b"DBPF"
    struct.pack_into("<3I",header,36,1,96,20)
    key=(0x53545223,0x11111111,150)
    return bytes(header)+struct.pack("<5I",*key,116,len(table))+bytes(table)


class CoreOverlayTests(unittest.TestCase):
    def test_known_english_in_approved_resource_is_rebased_without_touching_other_language(self):
        original=sample_source()
        catalog=[{"file":"UIText.package","id":150,"text":"Aspiration Rewards",
                  "description":"Cast UI COM"}]
        translations={"Aspiration Rewards":"Phần thưởng Khát vọng"}
        locations=approved_core_locations(catalog,translations)
        patched,changed,res=core_patch(original,"UIText.package",locations)
        self.assertEqual((changed,res),(1,1))
        rows,_=parse_table(Package(patched).raw(Package(patched).entries[0]))
        self.assertEqual(rows[0][1],"Phần thưởng Khát vọng")
        self.assertEqual(rows[1][1],"Do not translate other-language value")
        self.assertEqual(core_patch(patched,"UIText.package",locations),(patched,0,0))
        self.assertEqual(core_patch(original,"CAS.package",locations),(original,0,0))

    def test_other_preexisting_translation_is_preserved(self):
        english=sample_source("Phần thưởng ước mơ phiên cũ")
        loc=approved_core_locations([{"file":"UIText.package","id":150,"text":"Aspiration Rewards"}],
                                    {"Aspiration Rewards":"Phần thưởng Khát vọng"})
        self.assertEqual(core_patch(english,"UIText.package",loc),(english,0,0))

    def test_overlay_one_transaction_install_and_restore(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            game=root/"game"
            target=game/"TSData/Res/Text/UIText.package"
            target.parent.mkdir(parents=True)
            original=sample_source()
            target.write_bytes(original)
            (game/"TSData").mkdir(exist_ok=True)
            bundle=root/"bundle"
            bundle.mkdir()
            catalog=root/"english.json"
            catalog.write_text(json.dumps([{"file":"UIText.package","id":150,
                            "text":"Aspiration Rewards"}]),encoding="utf-8")
            starting={"install_files":[],"schema":"TSCTW-V08-TEST-1"}
            with patch("build_v07.load_translations",return_value=(
                {"Aspiration Rewards":"Phần thưởng Khát vọng"},[],[])):
                manifest=collect_core_overlay(game,bundle,starting,catalog,root)
            self.assertEqual(manifest["core_text_overlay"]["changed_rows"],1)
            self.assertEqual(manifest["install_files"][0]["path"],"TSData/Res/Text/UIText.package")
            backup=root/"backup"
            self.assertIn("DRY RUN",install(bundle,game,backup)["result"])
            install(bundle,game,backup,dry_run=False)
            self.assertNotEqual(target.read_bytes(),original)
            restore(game,backup,dry_run=False)
            self.assertEqual(target.read_bytes(),original)

    def test_ui_folder_uitext_is_supported_when_no_text_folder_copy_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            game=root/"game"
            src=game/"TSData/Res/UI/UIText.package"
            src.parent.mkdir(parents=True)
            src.write_bytes(sample_source())
            folder=root/"candidate"
            folder.mkdir()
            source_catalog=root/"catalog.json"
            source_catalog.write_text(json.dumps([
                {"file":"UIText.package","id":150,"text":"Aspiration Rewards"}
            ]),encoding="utf-8")
            with patch("build_v07.load_translations",return_value=(
                {"Aspiration Rewards":"Phần thưởng Khát vọng"},[],[])):
                result=collect_core_overlay(game,folder,
                    {"schema":"TSCTW-V08-TEST-1","install_files":[]},source_catalog,root)
            self.assertEqual([x["path"] for x in result["install_files"]],
                             ["TSData/Res/UI/UIText.package"])
            self.assertEqual(result["core_text_overlay"]["changed_files"],1)
            self.assertNotEqual(src.read_bytes(),
                                (folder/"Payload"/"TSData/Res/UI/UIText.package").read_bytes())

    def test_opaque_or_wrong_index_text_resource_is_not_touched(self):
        original=sample_source()
        location={("UIText.package",755):{"Aspiration Rewards":"Phần thưởng Khát vọng"}}
        self.assertEqual(core_patch(original,"UIText.package",location),(original,0,0))


if __name__=="__main__":
    unittest.main()
