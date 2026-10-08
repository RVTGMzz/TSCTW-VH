"""Read-only selector probe tests using 100% artificial DBPF data."""
import json
import struct
import tempfile
import unittest
from pathlib import Path

from probe_story_selector import EXPECTED, candidates, inspect_package

TITLE_KEY = (0x43545353, 0xFFFFFFFF, 1, 0)


def make_sample_package(title):
    header = bytearray(96)
    header[:4] = b"DBPF"
    header[64:66] = bytes([0xfd, 0xff])  # Unused main file header bytes.
    raw = bytearray(68)
    raw[64:66] = bytes([0xfd, 0xff])
    struct.pack_into("<H", raw, 66, 2)
    for value in (title, "This is an invented test description"):
        raw.extend(bytes([1]))
        raw.extend(value.encode("utf-8"))
        raw.append(0)
        raw.extend(b"Test metadata")
        raw.append(0)
    struct.pack_into("<3I", header, 36, 1, 96, 24)
    offset = 96 + 24
    index = struct.pack("<6I", *TITLE_KEY, offset, len(raw))
    return bytes(header) + index + bytes(raw)


class SelectorSourceTests(unittest.TestCase):
    def test_documents_paths_remain_separate_from_install_templates(self):
        game, documents = Path("/game"), Path("/documents")
        found = list(candidates(game, documents))
        self.assertEqual(len(found), 4)
        self.assertEqual({source for source, story, path in found}, {"installation_template", "documents_save"})
        for source, story, path in found:
            self.assertEqual(story in EXPECTED, True)
            self.assertTrue(path.as_posix().endswith(f"/{story}/{story}_Neighborhood.package"))
        self.assertEqual(len(list(candidates(game, None))), 2)

    def test_title_state_detects_original_and_translated_without_mutating_file(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/"N001_Neighborhood.package"
            original_title = EXPECTED["N001"]
            vi_title = "Đắm tàu và độc thân"
            maps = {original_title: vi_title}
            path.write_bytes(make_sample_package(original_title))
            previous = path.read_bytes()
            en = inspect_package(path, "N001", "documents_save", maps)
            self.assertTrue(en["resource_found"])
            self.assertEqual(en["index_width"], 24)
            self.assertEqual(en["resource_key"], list(TITLE_KEY))
            self.assertEqual(en["title_rows"][0]["state"], "original_english")
            self.assertFalse(en["read_path_observed"])
            self.assertEqual(path.read_bytes(), previous)
            path.write_bytes(make_sample_package(vi_title))
            previous = path.read_bytes()
            vi = inspect_package(path, "N001", "documents_save", maps)
            self.assertEqual(vi["title_rows"][0]["state"], "mapped_vietnamese")
            self.assertEqual(path.read_bytes(), previous)

    def test_missing_package_does_not_claim_runtime_verification(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/"does-not-exist.package"
            info = inspect_package(path, "N002", "installation_template", {})
            self.assertFalse(info["exists"])
            self.assertFalse(info["resource_found"])
            self.assertFalse(info["read_path_observed"])


if __name__ == "__main__":
    unittest.main()
