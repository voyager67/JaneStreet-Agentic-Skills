import hashlib
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
EXPECTED = {
    "socratic-tutor", "lob-microstructure", "market-making", "etf-arbitrage",
    "order-book-reconstruction", "queue-position-modeling", "hft-market-replay",
    "execution-analysis", "quant-research-validation", "tick-data-engineering",
    "low-latency-performance", "exchange-gateway-engineering",
    "agent-based-market-simulation", "pre-trade-risk-controls",
    "volatility-market-making", "production-trading-operations",
    "mathematical-reasoning", "code-understanding", "research-paper-tutor",
    "interview-simulator",
}
UPSTREAM_SHA256 = "9190b68440ad99be4d865c63b87939f23a362efac0776c5a67c93d1498bb5e37"
PRESERVED_BLOBS = {
    "agent-based-market-simulation": "7bbc34a461b804890227f34271fe4258a7cc0de2",
    "etf-arbitrage": "c3997858a5348585381ddda0b1f79db9381efd5c",
    "exchange-gateway-engineering": "9bec552a16b063afe8d31c9f7f8c039fc08755de",
    "execution-analysis": "b678bcf562b10303f25ea98872a61795d64f70a9",
    "hft-market-replay": "65f5b6faf2998537dd4e7b7f6024a4afaebb59cb",
    "lob-microstructure": "ce74b88b7e596acff3c96903d61fea0866e6fcf9",
    "low-latency-performance": "47e98a0be22bedb3f3003a33b933fd8aac379cf4",
    "market-making": "9663407cc53be668b4fa5d65ef3bc0b33df0be63",
    "order-book-reconstruction": "f91ac3b6b42da7ca49c973ca753ba20a3d066e58",
    "pre-trade-risk-controls": "46898f92acb1a28708d8841aae0e5fcd392a99e2",
    "production-trading-operations": "5add336374371018c908e53d2d7fc7dfd3b5267c",
    "quant-research-validation": "b7ea4bbfe228bd47c8fe1a6c7b19c246013a7313",
    "queue-position-modeling": "e64aeedbbfe6456814dd606b294d25c293eae91e",
    "socratic-tutor": "93bb7befeb73c41b4354175f9ef765547d4f3506",
    "tick-data-engineering": "aa81ac5c70d92ebfb43a9f35c5015dfeef74e9b2",
    "volatility-market-making": "021d41d2332633728f8b6616788a71f4baa2a138",
}


def git_blob_sha(path):
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


class RepositoryTests(unittest.TestCase):
    def test_expected_skill_directories_exist(self):
        actual = {path.name for path in SKILLS_ROOT.iterdir()
                  if path.is_dir() and (path / "SKILL.md").exists()}
        self.assertEqual(actual, EXPECTED)

    def test_frontmatter_name_matches_directory(self):
        for name in EXPECTED:
            text = (SKILLS_ROOT / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"), name)
            name_line = next(line for line in text.splitlines() if line.startswith("name:"))
            parsed_name = name_line.split(":", 1)[1].strip().strip('"').strip("'")
            self.assertEqual(parsed_name, name)
            self.assertRegex(name, r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

    def test_all_original_sixteen_skill_files_are_byte_preserved(self):
        for name, expected in PRESERVED_BLOBS.items():
            path = SKILLS_ROOT / name / "SKILL.md"
            self.assertTrue(path.is_file(), name)
            self.assertEqual(git_blob_sha(path), expected, name)

    def test_openai_metadata_exists_for_every_skill(self):
        for name in EXPECTED:
            path = SKILLS_ROOT / name / "agents" / "openai.yaml"
            self.assertTrue(path.is_file(), name)
            content = path.read_text(encoding="utf-8")
            for field in ("display_name:", "short_description:", "default_prompt:", "allow_implicit_invocation:"):
                self.assertIn(field, content, (name, field))

    def test_retained_jane_street_skill_keeps_separate_mit_license(self):
        path = SKILLS_ROOT / "socratic-tutor" / "SKILL.md"
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), UPSTREAM_SHA256)
        retained_license = (SKILLS_ROOT / "socratic-tutor" / "LICENSE.md").read_text(encoding="utf-8")
        notice = (ROOT / "NOTICE").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Jane Street Group, LLC", retained_license)
        self.assertIn("MIT License", retained_license)
        self.assertIn("not relicensed under", notice)

    def test_socratic_companion_material_is_additive(self):
        tutor = SKILLS_ROOT / "socratic-tutor"
        self.assertTrue((tutor / "references" / "assessment-rubric.md").is_file())
        self.assertTrue((tutor / "references" / "session-state.md").is_file())
        self.assertTrue((tutor / "examples" / "example-session.md").is_file())

    def test_learning_skills_have_distinct_content(self):
        required = {
            "mathematical-reasoning": ["proof", "counterexample", "edge cases"],
            "code-understanding": ["execution path", "root cause", "do not modify"],
            "research-paper-tutor": ["claim map", "reproducibility", "authors' statements"],
            "interview-simulator": ["one question at a time", "scoring rubric", "hiring prediction"],
        }
        for name, phrases in required.items():
            body = (SKILLS_ROOT / name / "SKILL.md").read_text(encoding="utf-8").lower()
            for phrase in phrases:
                self.assertIn(phrase.lower(), body, (name, phrase))

    def test_apache_license_and_notice_are_present(self):
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        notice = (ROOT / "NOTICE").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Apache License", license_text)
        self.assertIn("Version 2.0, January 2004", license_text)
        self.assertIn("Copyright 2026 HARSH SINGH", notice)
        self.assertIn("supplemental references/examples", notice)
        self.assertIn("[NOTICE](NOTICE)", readme)

    def test_readme_credits_sources_and_new_structure(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for item in ["HftBacktest", "ML4T", "ABIDES", "Nasdaq", "Avellaneda", "Jane Street", "ETF"]:
            self.assertIn(item, readme)
        self.assertIn("skills/", readme)
        self.assertIn("ROADMAP.md", readme)
        self.assertIn("not affiliated", readme.lower())

    def test_structural_validator_passes(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_skills.py")],
                                cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
