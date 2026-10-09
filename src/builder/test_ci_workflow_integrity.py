"""Guard Windows TEST release workflow against accidental duplicated fragments.

Only stdlib; runs on both Linux source audit and Windows packaging runners.
This structural guard is not a substitute for GitHub's own YAML/Actions parser.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
WINDOWS = ROOT / ".github/workflows/v08-windows-installer.yml"
AUDIT = ROOT / ".github/workflows/source-audit.yml"

class WorkflowIntegrityTests(unittest.TestCase):
    def test_windows_release_has_one_complete_publish_sequence(self):
        source = WINDOWS.read_text(encoding="utf-8")
        expected = (
            "Checkout localization source only",
            "Run binary and delivery regression tests",
            "Build single Windows EXE",
            "Smoke-test FROZEN Windows EXE",
            "Verify portable EXE checksum",
            "Write clear TEST caveats",
            "Provide standalone EXE download",
            "Publish direct EXE",
        )
        for name in expected:
            self.assertEqual(source.count("      - name: " + name), 1, name)
        self.assertEqual(source.count("gh release create $tag "), 1)
        self.assertEqual(source.count("dist/BUILD-IDENTITY.txt"), 3)
        self.assertTrue(source.rstrip().endswith(
            'if ($LASTEXITCODE -ne 0) { throw "GitHub prerelease creation failed" }'))
        self.assertNotIn(') { throw "Invalid EXE SHA256" }', source)
        self.assertIn("python src/builder/test_safe_core_text_overlay.py", source)
        self.assertIn("python src/builder/test_v08_delivery.py", source)

    def test_both_ci_jobs_compile_all_builder_modules(self):
        guard = "python -m compileall -q src/builder"
        self.assertIn(guard, WINDOWS.read_text(encoding="utf-8"))
        self.assertIn(guard, AUDIT.read_text(encoding="utf-8"))

    def test_both_ci_jobs_run_structural_guard(self):
        command = "python src/builder/test_ci_workflow_integrity.py"
        self.assertIn(command, WINDOWS.read_text(encoding="utf-8"))
        self.assertIn(command, AUDIT.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
