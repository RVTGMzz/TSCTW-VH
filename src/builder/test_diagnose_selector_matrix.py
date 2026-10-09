"""Read-only selector source matrix regression on fictional DBPF package bytes."""
import struct
import tempfile
import unittest
from pathlib import Path
from diagnose_visible_strings import selector_source_matrix, selector_source_area, SELECTOR_ANCHORS


def package_with_title(title):
    table=bytearray(68)
    table[64:66]=bytes((253,255))
    struct.pack_into("<H",table,66,1)
    table.extend(bytes((1,))+title.encode("utf-8")+bytes((0,))+b"Cast Neighborhood COM"+bytes((0,)))
    header=bytearray(96)
    header[:4]=b"DBPF"
    struct.pack_into("<3I",header,36,1,96,20)
    key=(0x53545223,0xFFFFFFFF,1)
    return bytes(header)+struct.pack("<5I",*key,116,len(table))+bytes(table)


class SelectorMatrixTest(unittest.TestCase):
    def test_windows_paths_are_classified_correctly(self):
        self.assertEqual(selector_source_area(r"G:\\Castaway-Portable\\TSData\\Res\\UserData\\Neighborhoods\\N002\\N002_Neighborhood.package"),"installation_neighborhood")
        self.assertEqual(selector_source_area(r"C:\\Users\\Player\\Documents\\Electronic Arts\\The Sims Castaway Stories\\Neighborhoods\\N002\\N002_Neighborhood.package"),"documents_neighborhood")
        self.assertEqual(selector_source_area(r"G:\\Castaway-Portable\\TSData\\Res\\Text\\UIText.package"),"game_text")
        self.assertEqual(selector_source_area(r"G:\Castaway-Portable\TSData\Res\UserData\Neighborhoods\N002\N002_Neighborhood.package"),"installation_neighborhood")

    def test_original_and_localized_titles_appear_with_source_and_do_not_modify_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            english=root/"TSData/Res/UserData/Neighborhoods/N002/N002_Neighborhood.package"
            vietnamese=root/"Documents/Electronic Arts/The Sims Castaway Stories/Neighborhoods/N001/N001_Neighborhood.package"
            for p in (english,vietnamese):
                p.parent.mkdir(parents=True,exist_ok=True)
            english.write_bytes(package_with_title("Wanmami Island"))
            vietnamese.write_bytes(package_with_title("Đắm tàu và độc thân"))
            old=(english.read_bytes(),vietnamese.read_bytes())
            report=selector_source_matrix([english,vietnamese])
            self.assertFalse(report["runtime_read_precedence_verified"])
            self.assertEqual(len(report["matches"]),2)
            self.assertEqual({r["state"] for r in report["matches"]},{"english","vietnamese"})
            self.assertEqual({r["source_area"] for r in report["matches"]},
                             {"installation_neighborhood","documents_neighborhood"})
            self.assertEqual(old,(english.read_bytes(),vietnamese.read_bytes()))

    def test_all_four_fields_match_english_and_vietnamese(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            base=root/"TSData/Res/UserData/Neighborhoods"
            observed=[]
            for i,(field,(en,vi)) in enumerate(SELECTOR_ANCHORS.items()):
                for language,value in (("english",en),("vietnamese",vi)):
                    target=base/("N001" if i%2 else "N002")/("N001_Neighborhood.package" if i%2 else "N002_Neighborhood.package")
                    # Read each fixture independently to avoid writing a fake
                    # multi-resource package that could conceal key collisions.
                    target.parent.mkdir(parents=True,exist_ok=True)
                    target.write_bytes(package_with_title(value))
                    hits=selector_source_matrix([target])["matches"]
                    observed.extend((r["field"],r["state"]) for r in hits)
            self.assertEqual(set(observed),
                {(name,status) for name in SELECTOR_ANCHORS for status in ("english","vietnamese")})

    def test_non_selector_file_skipped(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"objects.package"
            path.write_bytes(b"not even DBPF")
            self.assertEqual(selector_source_matrix([path])["matches"],[])


if __name__=="__main__":
    unittest.main()
