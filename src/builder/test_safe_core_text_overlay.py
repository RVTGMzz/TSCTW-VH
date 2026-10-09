"""Synthetic-only validation for exact-English core Text overlay."""
import json
import struct
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from runtime_dbpf import Package, parse_table
from safe_core_text_overlay import approved_core_locations, core_patch, collect_core_overlay, exact_visible_patch, VISIBLE_TEXT_TARGETS, TREE_TARGETS, patch_installed_selector, SELECTOR_KEY, INSTALLED_SELECTOR_FILES
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



def synthetic_single_string(key, value, language=1):
    table=bytearray(68)
    table[64:66]=bytes([0xfd,0xff])
    struct.pack_into("<H",table,66,1)
    table.extend(bytes([language])+value.encode("utf-8")+b"\0"+b"Cast Catalog COM\0")
    width=4*(len(key)+2)
    header=bytearray(96)
    header[:4]=b"DBPF"
    struct.pack_into("<3I",header,36,1,96,width)
    return bytes(header)+struct.pack("<"+"I"*(len(key)+2),*key,96+width,len(table))+bytes(table)


def synthetic_selector_package(first, second, key=SELECTOR_KEY, language=1):
    table=bytearray(68)
    table[64:66]=bytes((253,255))
    struct.pack_into("<H",table,66,3)
    for lang,value,description in (
        (language,first,"Cast Neighborhood COM"),
        (language,second,"Cast Neighborhood COM"),
        (3,"Other language must survive","Keep metadata")
    ):
        table.extend(bytes((lang,))+value.encode("utf-8")+bytes((0,))
                     +description.encode("utf-8")+bytes((0,)))
    header=bytearray(96)
    header[:4]=b"DBPF"
    struct.pack_into("<3I",header,36,1,96,24)
    return bytes(header)+struct.pack("<6I",*key,120,len(table))+bytes(table)


class InstalledSelectorTests(unittest.TestCase):
    def test_both_mode_titles_and_descriptions_are_patched_only_by_exact_source(self):
        from diagnose_visible_strings import SELECTOR_ANCHORS
        approved={
            "Shipwrecked and Single":"Đắm tàu và độc thân",
            "Very little is known about this remote tropical paradise. More English description.":"Người ta biết rất ít về thiên đường nhiệt đới xa xôi này. Nội dung đầy đủ.",
            "Wanmami Island":"Đảo Wanmami",
            "Wanmami Island is home to the local, the lost and others.":"Đảo Wanmami là mái nhà của mọi người.",
        }
        for island,fields in (("N001",("Shipwrecked and Single",
               "Very little is known about this remote tropical paradise. More English description.")),
                              ("N002",("Wanmami Island",
               "Wanmami Island is home to the local, the lost and others."))):
            with self.subTest(island=island):
                original=synthetic_selector_package(*fields)
                patched,rows,resources=patch_installed_selector(original,island,approved)
                self.assertEqual((rows,resources),(2,1))
                pkg=Package(patched)
                result,tail=parse_table(pkg.raw(pkg.entries[0]))
                self.assertEqual([result[0][1],result[1][1]],[approved[v] for v in fields])
                self.assertEqual(result[2][1],"Other language must survive")
                self.assertEqual(result[0][2],"Cast Neighborhood COM")
                self.assertEqual(patch_installed_selector(patched,island,approved),(patched,0,0))
                other=synthetic_selector_package("User custom title",fields[1])
                mod,amount,_=patch_installed_selector(other,island,approved)
                self.assertEqual(amount,1)
                self.assertEqual(parse_table(Package(mod).raw(Package(mod).entries[0]))[0][0][1],
                                 "User custom title")
                wrong_key=synthetic_selector_package(*fields,key=(SELECTOR_KEY[0],SELECTOR_KEY[1],2,0))
                self.assertEqual(patch_installed_selector(wrong_key,island,approved),(wrong_key,0,0))

    def test_approved_full_mode_descriptions_patch(self):
        translations=json.loads((Path(__file__).resolve().parents[2]/
            "runtime/translations/ui.json").read_text(encoding="utf-8"))
        for island,title,anchor in (
            ("N001","Shipwrecked and Single","Very little is known about"),
            ("N002","Wanmami Island","Wanmami Island is home to"),
        ):
            long_keys=[k for k in translations if k.startswith(anchor)]
            self.assertEqual(len(long_keys),1)
            source=synthetic_selector_package(title,long_keys[0])
            updated,count,resources=patch_installed_selector(source,island,translations)
            self.assertEqual((count,resources),(2,1))
            rows,_=parse_table(Package(updated).raw(Package(updated).entries[0]))
            self.assertEqual(rows[0][1],translations[title])
            self.assertEqual(rows[1][1],translations[long_keys[0]])

    def test_typographic_apostrophe_does_not_leave_story_description_english(self):
        en="Very little is known about this remote tropical paradise. Its location isn’t recorded."
        ui={"Shipwrecked and Single":"Đắm tàu và độc thân",
            en:"Người ta biết rất ít về thiên đường nhiệt đới xa xôi này."}
        raw=synthetic_selector_package("Shipwrecked and Single",
                                       en.replace("’","'"))
        updated,count,res=patch_installed_selector(raw,"N001",ui)
        self.assertEqual((count,res),(2,1))
        rows,_=parse_table(Package(updated).raw(Package(updated).entries[0]))
        self.assertEqual(rows[1][1],ui[en])

    def test_neighborhood_installer_transaction_restores_original_and_leaves_documents(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            game=root/"game"
            bundle=root/"bundle"
            bundle.mkdir()
            save=root/"Documents"/"Neighborhoods"/"N002"/"N002_Neighborhood.package"
            save.parent.mkdir(parents=True)
            save.write_bytes(b"Players current untouched neighborhood save")
            approved={
                "Shipwrecked and Single":"Đắm tàu và độc thân",
                "Very little is known about this remote tropical paradise. More description.":"Người ta biết rất ít về thiên đường nhiệt đới xa xôi này. Mô tả.",
                "Wanmami Island":"Đảo Wanmami",
                "Wanmami Island is home to the local, the lost. More description.":"Đảo Wanmami là mái nhà của mọi người.",
            }
            originals={}
            for island,relative in INSTALLED_SELECTOR_FILES.items():
                title=("Shipwrecked and Single" if island=="N001" else "Wanmami Island")
                detail=("Very little is known about this remote tropical paradise. More description."
                        if island=="N001" else
                        "Wanmami Island is home to the local, the lost. More description.")
                target=game/relative
                target.parent.mkdir(parents=True,exist_ok=True)
                originals[relative]=synthetic_selector_package(title,detail)
                target.write_bytes(originals[relative])
            (root/"runtime/translations").mkdir(parents=True)
            (root/"runtime/translations/ui.json").write_text(
                json.dumps(approved,ensure_ascii=False),encoding="utf-8")
            catalog=root/"castaway-english-strings.json"
            catalog.write_text("[]",encoding="utf-8")
            with patch("build_v07.load_translations",return_value=({},[],[])):
                manifest=collect_core_overlay(game,bundle,
                    {"schema":"TSCTW-V08-TEST-1","install_files":[]},
                    catalog,root)
            self.assertEqual(manifest["installed_selector_overlay"]["changed_rows"],4)
            self.assertEqual(len(manifest["install_files"]),2)
            backup=root/"backup"
            self.assertIn("DRY RUN",install(bundle,game,backup)["result"])
            self.assertFalse(backup.exists())
            install(bundle,game,backup,dry_run=False)
            self.assertEqual(save.read_bytes(),b"Players current untouched neighborhood save")
            restore(game,backup,dry_run=False)
            for relative,before in originals.items():
                self.assertEqual((game/relative).read_bytes(),before)
            self.assertEqual(save.read_bytes(),b"Players current untouched neighborhood save")


class VisibleOwnerTests(unittest.TestCase):
    def test_canh_tree_exact_identity_and_idempotence(self):
        for key,(en,vi) in TREE_TARGETS.items():
            original=synthetic_single_string(key,en)
            after,rows,resources=exact_visible_patch(original,"catcanhobjects.bundle.package",tree=True)
            self.assertEqual((rows,resources),(1,1))
            result=Package(after)
            self.assertEqual(parse_table(result.raw(result.entries[0]))[0][0][1],vi)
            self.assertEqual(exact_visible_patch(after,"catcanhobjects.bundle.package",tree=True),(after,0,0))
            unknown=synthetic_single_string(key,"Unrelated custom tree")
            self.assertEqual(exact_visible_patch(unknown,"catcanhobjects.bundle.package",tree=True),(unknown,0,0))

    def test_cas_help_exact_language_and_row_guard(self):
        (name,key,ordinal,lang),(english,vietnamese)=next(iter(VISIBLE_TEXT_TARGETS.items()))
        # A language-2 row at the required ordinal, not an ordinal-0 shortcut.
        table=bytearray(68)
        table[64:66]=bytes([0xfd,0xff])
        struct.pack_into("<H",table,66,ordinal+1)
        for i in range(ordinal+1):
            v=english if i==ordinal else "Keep untouched"
            language=lang if i==ordinal else 1
            table.extend(bytes([language])+v.encode("utf-8")+b"\0"+b"CAST UI COM\0")
        header=bytearray(96)
        header[:4]=b"DBPF"
        struct.pack_into("<3I",header,36,1,96,20)
        original=bytes(header)+struct.pack("<5I",*key,116,len(table))+bytes(table)
        after,rows,resources=exact_visible_patch(original,name)
        self.assertEqual((rows,resources),(1,1))
        data=Package(after)
        parsed,_=parse_table(data.raw(data.entries[0]))
        self.assertEqual(parsed[ordinal][1],vietnamese)
        self.assertEqual(parsed[0][1],"Keep untouched")
        self.assertEqual(exact_visible_patch(after,name),(after,0,0))
        self.assertEqual(exact_visible_patch(original,"Live.package"),(original,0,0))

if __name__=="__main__":
    unittest.main()
