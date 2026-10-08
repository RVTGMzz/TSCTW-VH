"""Synthetic DBPF binary regression tests; NO commercial game data is used."""
import struct
import unittest

from check_runtime_packages import apply
from runtime_dbpf import Package, parse_table, encode_table

STR = 0x53545223
CTSS = 0x43545353


def fake_table():
    head = bytearray(68)
    name = b"Test - Castaway UI"
    head[:len(name)] = name
    head[64:66] = bytes([0xfd, 0xff])
    struct.pack_into("<H", head, 66, 3)
    rows = [
        [1, "Examine", "Castaway action"],
        [2, "Examine", "Castaway action"],
        [3, "Examiner", "Do not translate other languages"],
    ]
    payload = b"".join(bytes([lang]) + value.encode("utf-8") + bytes([0]) + desc.encode("utf-8") + bytes([0]) for lang, value, desc in rows)
    return bytes(head) + payload + bytes([3, 0]) + b"PAD"


def fixture(index_width):
    header = bytearray(96)
    header[:4] = b"DBPF"
    keys = [
        ((CTSS, 0x11, 0x2000) if index_width == 20 else (CTSS, 0x11, 0x2000, 0)),
        ((STR, 0x12, 0x2001) if index_width == 20 else (STR, 0x12, 0x2001, 0)),
    ]
    resources = [fake_table(), b"OTHER NON-TEXT PAYLOAD"]
    struct.pack_into("<3I", header, 36, len(keys), len(header), len(keys) * index_width)
    ix = bytearray()
    offset = len(header) + len(keys) * index_width
    for key, raw in zip(keys, resources):
        ix.extend(struct.pack("<" + "I" * (index_width // 4), *key, offset, len(raw)))
        offset += len(raw)
    return bytes(header + ix + b"".join(resources)), keys


class RuntimeDbpfWriterTests(unittest.TestCase):
    def test_str_and_ctss_patch_20_and_24_byte_indices(self):
        for width in (20, 24):
            with self.subTest(width=width):
                original, keys = fixture(width)
                package = Package(original)
                self.assertEqual(package.width, width)
                row_keys = [{
                    "package": "TSData/Res/Objects/objects.package",
                    "key": list(keys[0]),
                    "row": row,
                    "language": lang,
                    "en": "Examine",
                    "description": "Castaway action",
                    "category": "menu",
                } for row, lang in [(0, 1), (1, 2)]]
                # Real writer, but only synthetic package bytes and tiny approved mapping.
                patched, changed, resource_count = apply(
                    original, row_keys, {"menu": {"Examine": "Xem xét"}}, set(), {})
                self.assertEqual((changed, resource_count), (2, 1))
                new_package = Package(patched)
                index = {e.key: e for e in new_package.entries}
                rows, tail = parse_table(new_package.raw(index[keys[0]]))
                self.assertEqual([r[1] for r in rows], ["Xem xét", "Xem xét", "Examiner"])
                self.assertEqual(rows[2][2], "Do not translate other languages")
                self.assertEqual(tail, bytes([3, 0]) + b"PAD")
                # Non-target resource bytes and original header remain identical.
                old_index = {e.key: e for e in package.entries}
                self.assertEqual(new_package.raw(index[keys[1]]), package.raw(old_index[keys[1]]))
                self.assertEqual(patched[:96], original[:96])
                again, n2, changed_resources2 = apply(
                    patched, row_keys, {"menu": {"Examine": "Xem xét"}}, set(), {})
                self.assertEqual((again, n2, changed_resources2), (patched, 0, 0))

    def test_writer_refuses_wrong_source_and_unapproved_rows(self):
        original, keys = fixture(24)
        candidate = {"package": "TSData/Res/Objects/objects.package", "key": list(keys[0]),
                     "row": 0, "language": 1, "en": "Wrong English", "description": "Castaway action",
                     "category": "menu"}
        with self.assertRaises(ValueError):
            apply(original, [candidate], {"menu": {"Wrong English": "Sai"}}, set(), {})
        patched, rows, res = apply(original, [candidate], {"menu": {}}, set(), {})
        self.assertEqual((patched, rows, res), (original, 0, 0))


if __name__ == "__main__":
    unittest.main()
