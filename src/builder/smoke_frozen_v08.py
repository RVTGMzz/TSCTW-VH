"""Frozen-EXE integration smoke: no EA packages, only a tiny synthetic DBPF.

Exercises runtime-only bundle -> manifest -> dry-run -> install -> restore
with all core Text files intentionally absent and core catalog calls forbidden.
"""
import hashlib
import json
import shutil
import struct
import tempfile
from pathlib import Path

from runtime_dbpf import Package, parse_table


def smoke():
    import prepare_v08_test as builder
    from install_v08_local import install, restore
    key = (0x43545353, 0x11, 0x2000, 0)
    rel = "TSData/Res/Objects/objects.package"
    table = bytearray(68)
    table[64:66] = b"\xfd\xff"
    struct.pack_into("<H", table, 66, 1)
    table.extend(b"\x01Examine\x00Castaway action\x00")
    header = bytearray(96)
    header[:4] = b"DBPF"
    struct.pack_into("<3I", header, 36, 1, 96, 24)
    index = struct.pack("<6I", *key, 120, len(table))
    original = bytes(header) + index + bytes(table)
    item = {
        "package": rel,
        "sha256": hashlib.sha256(original).hexdigest(),
        "bytes": len(original),
        "index_width": 24,
        "resources": 1,
        "errors": [],
    }
    row = {
        "package": rel, "key": list(key), "row": 0,
        "language": 1, "en": "Examine",
        "description": "Castaway action", "category": "menu",
    }
    patched_functions = {
        "assess": lambda: ({"parse_errors": 0, "untranslated_or_review_candidate_rows": 0, "candidate_rows": 1}, []),
        "source_inventory": lambda: [item],
        "load_maps": lambda: {"menu": {"Examine": "Xem xét"}},
        "load_row_translations": lambda: [],
        "effective_records": lambda: ([row], []),
    }
    def forbid_core():
        raise AssertionError("Runtime-only EXE attempted to load missing core Text catalog")
    patched_functions["load_translations"] = forbid_core
    patched_functions["load_v06_history"] = forbid_core
    originals = {name: getattr(builder, name) for name in patched_functions}
    with tempfile.TemporaryDirectory(prefix="Castaway-Frozen-SelfTest-") as temp:
        root = Path(temp)
        game = root / "game"
        input_root = root / "original_runtime"
        source = input_root / rel
        live = game / rel
        source.parent.mkdir(parents=True)
        live.parent.mkdir(parents=True)
        source.write_bytes(original)
        live.write_bytes(original)
        try:
            for name, fn in patched_functions.items():
                setattr(builder, name, fn)
            result = builder.build(root / "unused_core", input_root, root / "payload",
                                   runtime_only=True, allow_prepatched_runtime=True)
        finally:
            for name, fn in originals.items():
                setattr(builder, name, fn)
        assert result["build_mode"] == "runtime-overlay-on-v07a"
        assert len(result["install_files"]) == 1
        assert result["install_files"][0]["changed_rows"] == 1
        payload = root / "payload"
        parsed = Package((payload / "Payload" / rel).read_bytes())
        rows, _ = parse_table(parsed.raw(parsed.entries[0]))
        assert rows[0][1] == "Xem xét"
        backup = root / "backup"
        assert "DRY RUN" in install(payload, game, backup)["result"]
        installed = install(payload, game, backup, dry_run=False)
        assert installed["files"] == 1
        assert live.read_bytes() != original
        restored = restore(game, backup, dry_run=False)
        assert restored["files"] == 1
        assert live.read_bytes() == original
    return True
