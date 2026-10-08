"""Local v0.8 candidate/install/restore regression tests using invented bytes only."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_runtime_dbpf_writer import fixture as dbpf_fixture
from install_v08_local import install, restore, validate_path
from prepare_v08_test import strict_locations, manifest_row, verify_inputs, build, refuse_pretranslated_core
from build_v07 import FULL_REQUIRED


def h(data):
    return hashlib.sha256(data).hexdigest()


def fixture(root, files=("TSData/Res/Text/Options.package",)):
    game=root/"game"
    bundle=root/"candidate"
    backup=root/"backup"
    game.joinpath("TSData").mkdir(parents=True)
    manifest=[]
    for i,rel in enumerate(files):
        orig=b"ORIGINAL TEST ONLY "+bytes([i])
        new=b"VIETNAMESE TEST ONLY "+bytes([i])
        dst=game/rel
        dst.parent.mkdir(parents=True,exist_ok=True)
        dst.write_bytes(orig)
        payload=bundle/"Payload"/rel
        payload.parent.mkdir(parents=True,exist_ok=True)
        payload.write_bytes(new)
        manifest.append({"path":rel, "original_sha256":h(orig), "patched_sha256":h(new),
                         "changed_rows":1,"changed_resources":1})
    (bundle/"manifest.json").write_text(json.dumps({
        "schema":"TSCTW-V08-TEST-1","in_game_tested":False,"install_files":manifest
    }),encoding="utf-8")
    return game,bundle,backup,manifest


class DeliveryTests(unittest.TestCase):
    def test_dry_run_install_apply_restore_without_touching_saves(self):
        with tempfile.TemporaryDirectory() as tmp:
            game,bundle,backup,manifest=fixture(Path(tmp),(
                "TSData/Res/Text/Options.package",
                "TSData/Res/Text/Wants.package",
                "TSData/Res/Wants/Wants.package",
            ))
            before={f["path"]:(game/f["path"]).read_bytes() for f in manifest}
            self.assertIn("DRY RUN",install(bundle,game,backup)["result"])
            self.assertFalse(backup.exists())
            self.assertEqual({p:(game/p).read_bytes() for p in before},before)
            result=install(bundle,game,backup,dry_run=False)
            self.assertEqual(result["files"],3)
            for f in manifest:
                self.assertEqual(h((game/f["path"]).read_bytes()),f["patched_sha256"])
                self.assertEqual(h((backup/f["path"]).read_bytes()),f["original_sha256"])
            self.assertIn("DRY RUN",restore(game,backup)["result"])
            self.assertEqual(restore(game,backup,dry_run=False)["files"],3)
            self.assertEqual({p:(game/p).read_bytes() for p in before},before)
            # Idempotent recovery even if a previous restoration stopped halfway.
            self.assertEqual(restore(game,backup,dry_run=False)["files"],0)
            self.assertTrue((backup/"restore_manifest.json").is_file())

    def test_mismatched_installed_original_blocks_all_modifications(self):
        with tempfile.TemporaryDirectory() as tmp:
            game,bundle,backup,manifest=fixture(Path(tmp))
            destination=game/manifest[0]["path"]
            destination.write_bytes(b"already patched by another mod")
            with self.assertRaises(ValueError):
                install(bundle,game,backup,dry_run=False)
            self.assertFalse(backup.exists())
            self.assertEqual(destination.read_bytes(),b"already patched by another mod")

    def test_partial_restoration_keeps_unmodified_files_and_finishes(self):
        with tempfile.TemporaryDirectory() as tmp:
            game,bundle,backup,rows=fixture(Path(tmp),(
                "TSData/Res/Text/Options.package","TSData/Res/Wants/Wants.package"))
            install(bundle,game,backup,dry_run=False)
            first=rows[0]
            (game/first["path"]).write_bytes((backup/first["path"]).read_bytes())
            self.assertEqual(restore(game,backup,dry_run=False)["files"],1)
            for r in rows:
                self.assertEqual(h((game/r["path"]).read_bytes()),r["original_sha256"])

    def test_unexpected_edit_blocks_restore_instead_of_overwriting_player_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            game,bundle,backup,rows=fixture(Path(tmp))
            install(bundle,game,backup,dry_run=False)
            p=game/rows[0]["path"]
            p.write_bytes(b"third-party mod installed later")
            with self.assertRaises(ValueError):
                restore(game,backup,dry_run=False)
            self.assertEqual(p.read_bytes(),b"third-party mod installed later")

    def test_rejects_documents_saves_and_unsafe_manifest_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            game,bundle,backup,_=fixture(Path(tmp))
            for unsafe in ("TSData/Res/UserData/Neighborhoods/N001/save.package",
                           "TSData/Res/../../outside.package","C:/Windows/evil.package",
                           "TSData/Res/Text/../../target.package"):
                with self.subTest(path=unsafe), self.assertRaises(ValueError):
                    validate_path(unsafe)
            data=json.loads((bundle/"manifest.json").read_text())
            data["install_files"][0]["path"]="TSData/Res/UserData/Neighborhoods/N001/save.package"
            (bundle/"manifest.json").write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                install(bundle,game,backup,dry_run=False)
            self.assertFalse(backup.exists())

    def test_full_text_guard_rejects_prior_v07_translation(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            (p/"UIText.package").write_bytes(b"synthetic fake Text package")
            history={("UIText.package",85,1,"Xem xét"):{"Examine"}}
            with (patch("prepare_v08_test.entries",return_value=[(0x53545223,0,85,0,12)]),
                  patch("prepare_v08_test.unpack",return_value=b"fake resource"),
                  patch("prepare_v08_test.strings",return_value=[[1,"Xem xét",""]])):
                with self.assertRaises(ValueError):
                    refuse_pretranslated_core(p,["UIText.package"],history)
                self.assertIsNone(refuse_pretranslated_core(p,["UIText.package"],{}))

    def test_runtime_only_builder_produces_installable_payload_without_core_or_save_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            runtime=root/"original_runtime"
            core=root/"absent_text_originals"
            output=root/"candidate"
            package_rel="TSData/Res/Objects/objects.package"
            pkg=runtime/package_rel
            pkg.parent.mkdir(parents=True)
            original, keys=dbpf_fixture(24)
            pkg.write_bytes(original)
            item={"package":package_rel, "sha256":h(original), "bytes":len(original), "errors":[]}
            records=[{"package":package_rel,"key":list(keys[0]),"row":i,
                      "language":i+1,"en":"Examine","description":"Castaway action","category":"menu"}
                     for i in (0,1)]
            audit={"parse_errors":0,"untranslated_or_review_candidate_rows":0,"candidate_rows":2}
            with (patch("prepare_v08_test.assess",return_value=(audit,[])),
                  patch("prepare_v08_test.source_inventory",return_value=[item]),
                  patch("prepare_v08_test.effective_records",return_value=(records,[])),
                  patch("prepare_v08_test.load_maps",return_value={"menu":{"Examine":"Xem xét"}}),
                  patch("prepare_v08_test.load_row_translations",return_value=[]),
                  patch("prepare_v08_test.load_translations",side_effect=FileNotFoundError("core catalog must never be read")),
                  patch("prepare_v08_test.derive_targets",side_effect=AssertionError("core-only function unexpectedly called")),
                  patch("prepare_v08_test.load_v06_history",side_effect=AssertionError("core history unexpectedly used"))):
                result=build(core,runtime,output,runtime_only=True)
                # Re-run on the just-translated file, without original English rows.
                # It must be a clean, non-installable no-op rather than an error.
                pkg.write_bytes((output/"Payload"/package_rel).read_bytes())
                again=build(core,runtime,root/"repeated",
                            runtime_only=True,allow_prepatched_runtime=True,
                            allow_no_changes=True)
                self.assertEqual(again["install_files"],[])
                self.assertTrue(again["no_applicable_english_rows"])
                self.assertEqual(again["build_summary"][0]["changed_rows"],0)
            self.assertEqual(result["build_mode"],"runtime-overlay-on-v07a")
            self.assertEqual(len(result["install_files"]),1)
            self.assertEqual(result["install_files"][0]["path"],package_rel)
            self.assertFalse(any("UserData" in r["path"] for r in result["install_files"]))
            self.assertNotEqual((output/"Payload"/package_rel).read_bytes(),original)
            game=root/"game";dest=game/package_rel
            dest.parent.mkdir(parents=True)
            dest.write_bytes(original)
            backup=root/"backup"
            self.assertIn("DRY RUN",install(output,game,backup)["result"])
            installed=install(output,game,backup,dry_run=False)
            self.assertEqual(installed["files"],1)
            self.assertEqual(restore(game,backup,dry_run=False)["files"],1)
            self.assertEqual(dest.read_bytes(),original)

    def test_builder_rejects_output_over_input_and_mismatched_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            game=root/"source"
            runtime=root/"runtime"
            output=root/"output"
            game.mkdir();runtime.mkdir()
            with self.assertRaises(ValueError):
                strict_locations(game,runtime,game/"candidate")
            with self.assertRaises(ValueError):
                strict_locations(game,runtime,runtime/"candidate")
            strict_locations(game,runtime,output)
            for name in FULL_REQUIRED:
                (game/name).write_bytes(b"synthetic core bytes")
            rel="TSData/Res/Wants/Wants.package"
            source=runtime/rel
            source.parent.mkdir(parents=True)
            source.write_bytes(b"synthetic original")
            item={"package":rel,"bytes":source.stat().st_size,"sha256":h(source.read_bytes())}
            self.assertEqual(verify_inputs(game,runtime,[item]),sorted(FULL_REQUIRED))
            source.write_bytes(b"modified")
            with self.assertRaises(ValueError):
                verify_inputs(game,runtime,[item])
            original=game/"Options.package"
            line=manifest_row("TSData/Res/Text/Options.package",original,b"patched",1,1)
            self.assertEqual(line["original_sha256"],h(original.read_bytes()))
            self.assertEqual(line["patched_sha256"],h(b"patched"))


if __name__=="__main__":
    unittest.main()
