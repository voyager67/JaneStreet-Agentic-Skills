import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install_skills.py"


class InstallerTests(unittest.TestCase):
    def run_installer(self, *args):
        return subprocess.run([sys.executable, str(INSTALLER), *args],
                              cwd=ROOT, capture_output=True, text=True, check=False)

    def test_custom_install_copies_complete_nested_skill_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_installer("--agent", "custom", "--destination", tmp,
                                        "--skills", "market-making")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            target = Path(tmp) / "market-making"
            self.assertTrue((target / "SKILL.md").is_file())
            self.assertTrue((target / "agents" / "openai.yaml").is_file())

    def test_existing_skill_is_not_overwritten_without_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "market-making"
            target.mkdir()
            (target / "sentinel.txt").write_text("keep", encoding="utf-8")
            result = self.run_installer("--agent", "custom", "--destination", tmp,
                                        "--skills", "market-making")
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual((target / "sentinel.txt").read_text(encoding="utf-8"), "keep")

    def test_dry_run_does_not_create_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "not-created"
            result = self.run_installer("--agent", "custom", "--destination", str(destination),
                                        "--skills", "lob-microstructure", "--dry-run")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertFalse(destination.exists())

    def test_new_learning_skill_is_installable(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_installer("--agent", "custom", "--destination", tmp,
                                        "--skills", "research-paper-tutor")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((Path(tmp) / "research-paper-tutor" / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
