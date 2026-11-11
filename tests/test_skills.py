import hashlib
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "socratic-tutor", "lob-microstructure", "market-making", "etf-arbitrage",
    "order-book-reconstruction", "queue-position-modeling", "hft-market-replay",
    "execution-analysis", "quant-research-validation", "tick-data-engineering",
    "low-latency-performance", "exchange-gateway-engineering",
    "agent-based-market-simulation", "pre-trade-risk-controls",
    "volatility-market-making", "production-trading-operations",
}
UPSTREAM_SHA256 = "9190b68440ad99be4d865c63b87939f23a362efac0776c5a67c93d1498bb5e37"


class RepositoryTests(unittest.TestCase):
    def test_expected_skill_directories_exist(self):
        actual = {
            path.name for path in ROOT.iterdir()
            if path.is_dir() and (path / "SKILL.md").exists()
        }
        self.assertEqual(actual, EXPECTED)

    def test_frontmatter_name_matches_directory(self):
        for name in EXPECTED:
            text = (ROOT / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"), name)
            name_line = next(line for line in text.splitlines() if line.startswith("name:"))
            parsed_name = name_line.split(":", 1)[1].strip().strip('"').strip("'")
            self.assertEqual(parsed_name, name)
            self.assertRegex(name, r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

    def test_openai_metadata_exists_for_every_skill(self):
        for name in EXPECTED:
            path = ROOT / name / "agents" / "openai.yaml"
            self.assertTrue(path.is_file(), name)
            content = path.read_text(encoding="utf-8")
            for field in ("display_name:", "short_description:", "default_prompt:", "allow_implicit_invocation:"):
                self.assertIn(field, content, (name, field))

    def test_retained_jane_street_skill_is_unchanged(self):
        path = ROOT / "socratic-tutor" / "SKILL.md"
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), UPSTREAM_SHA256)

    def test_new_skills_are_quant_and_hft_scoped(self):
        required = {
            "lob-microstructure": ["order-flow imbalance", "adverse selection"],
            "market-making": ["inventory", "markout"],
            "etf-arbitrage": ["creation", "redemption", "basket"],
            "queue-position-modeling": ["queue", "fill"],
            "hft-market-replay": ["latency", "historical"],
            "low-latency-performance": ["p99", "tail"],
            "exchange-gateway-engineering": ["acknowledgement", "recovery"],
            "pre-trade-risk-controls": ["kill", "limits"],
        }
        for name, phrases in required.items():
            body = (ROOT / name / "SKILL.md").read_text(encoding="utf-8").lower()
            for phrase in phrases:
                self.assertIn(phrase.lower(), body, (name, phrase))

    def test_research_and_operations_warn_against_unvalidated_live_use(self):
        for name in [
            "quant-research-validation", "hft-market-replay",
            "pre-trade-risk-controls", "production-trading-operations",
        ]:
            body = (ROOT / name / "SKILL.md").read_text(encoding="utf-8").lower()
            self.assertTrue("live" in body or "production" in body, name)

    def test_license_and_notice_are_present(self):
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        notice = (ROOT / "NOTICE").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Apache License", license_text)
        self.assertIn("Version 2.0, January 2004", license_text)
        for clause in range(1, 10):
            self.assertRegex(license_text, rf"(?m)^\s*{clause}\.")
        self.assertTrue(license_text.rstrip().endswith("limitations under the License."))
        self.assertIn("Copyright 2026 HARSH SINGH", notice)
        self.assertIn("Apache License, Version 2.0", notice)
        self.assertIn("not relicensed under Apache-2.0", notice)
        self.assertIn("[NOTICE](NOTICE)", readme)

    def test_retained_jane_street_skill_keeps_separate_mit_license(self):
        retained_license = (ROOT / "socratic-tutor" / "LICENSE.md").read_text(encoding="utf-8")
        notice = (ROOT / "NOTICE").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Jane Street Group, LLC", retained_license)
        self.assertIn("MIT License", retained_license)
        self.assertIn("not relicensed under Apache-2.0", notice)

    def test_readme_credits_original_and_reference_sources(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for item in ["HftBacktest", "ML4T", "ABIDES", "Nasdaq", "Avellaneda", "Jane Street", "ETF"]:
            self.assertIn(item, readme)
        self.assertIn("not affiliated", readme.lower())

    def test_structural_validator_passes(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_skills.py")],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
