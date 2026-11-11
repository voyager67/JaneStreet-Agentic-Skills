import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_SHA256 = "9190b68440ad99be4d865c63b87939f23a362efac0776c5a67c93d1498bb5e37"


class SkillRepositoryTests(unittest.TestCase):
    def test_expected_skill_count(self):
        skills = [p for p in ROOT.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()]
        self.assertGreaterEqual(len(skills), 16)

    def test_frontmatter_and_folder_names(self):
        for folder in (p for p in ROOT.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()):
            text = (folder / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"), folder.name)
            frontmatter = text.split("\n---\n", 1)[0]
            self.assertIn(f"name: {folder.name}", frontmatter)
            self.assertRegex(frontmatter, r"(?m)^description:\s*.+$")

    def test_unique_skill_names(self):
        names = []
        for path in ROOT.glob("*/SKILL.md"):
            frontmatter = path.read_text(encoding="utf-8").split("\n---\n", 1)[0]
            names.append(next(line.split(":", 1)[1].strip() for line in frontmatter.splitlines() if line.startswith("name:")))
        self.assertEqual(len(names), len(set(names)))

    def test_jane_street_skill_is_unchanged(self):
        path = ROOT / "socratic-tutor" / "SKILL.md"
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), UPSTREAM_SHA256)

    def test_root_documents_exist(self):
        for target in ("README.md", "LICENSE", "NOTICE", "CONTRIBUTING.md", "SKILLS.md"):
            self.assertTrue((ROOT / target).is_file(), target)

    def test_readme_license_and_notice_links(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for target in ("LICENSE", "NOTICE", "CONTRIBUTING.md"):
            self.assertIn(f"]({target})", readme)


if __name__ == "__main__":
    unittest.main()
