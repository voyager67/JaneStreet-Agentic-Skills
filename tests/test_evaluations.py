import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import evaluate_skills


class EvaluationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = evaluate_skills.load_cases(evaluate_skills.CASES_PATH)

    def test_every_skill_has_trigger_and_boundary_cases(self):
        self.assertEqual(evaluate_skills.validate_cases(self.cases), [])
        self.assertEqual(evaluate_skills.validate_local_case_files(self.cases), [])
        coverage = {}
        for case in self.cases:
            coverage.setdefault(case["skill"], set()).add(case["kind"])
        for skill in evaluate_skills.skill_names():
            self.assertEqual(coverage[skill], {"trigger", "boundary"}, skill)

    def test_render_does_not_leak_expected_behaviors_or_skill_names(self):
        rendered = evaluate_skills.render_cases(self.cases, "hft-market-replay", "markdown")
        self.assertIn("CASE-009", rendered)
        self.assertIn("exchange timestamps", rendered)
        self.assertNotIn("expected_behaviors", rendered)
        self.assertNotIn("critical_failures", rendered)
        self.assertNotIn("Uses only information received", rendered)
        self.assertNotIn("hft-market-replay", rendered)

    def test_new_learning_skills_have_renderable_cases(self):
        for skill in ("mathematical-reasoning", "code-understanding", "research-paper-tutor", "interview-simulator"):
            rendered = evaluate_skills.render_cases(self.cases, skill, "markdown")
            self.assertIn("CASE-", rendered)
            self.assertNotIn(skill, rendered)

    def test_score_summary_flags_critical_failures(self):
        case = next(c for c in self.cases if c["id"] == "CASE-009")
        result = {
            "case_id": case["id"], "model": "test-model", "run_id": "test-run",
            "reviewer": "reviewer",
            "scores": {key: 2 for key in evaluate_skills.DIMENSIONS},
            "critical_failures": ["Used future information"],
        }
        self.assertEqual(evaluate_skills.validate_results([result], self.cases), [])
        run = evaluate_skills.summarize_results([result], self.cases, 1.6)["runs"][0]
        self.assertEqual(run["critical_failure_count"], 1)
        self.assertEqual(run["case_passes"], 0)

    def test_score_summary_accepts_complete_clean_case(self):
        case = next(c for c in self.cases if c["id"] == "CASE-015")
        result = {
            "case_id": case["id"], "model": "test-model", "run_id": "test-run",
            "reviewer": "reviewer",
            "scores": {key: 2 for key in evaluate_skills.DIMENSIONS},
            "critical_failures": [],
        }
        run = evaluate_skills.summarize_results([result], self.cases, 1.6)["runs"][0]
        self.assertEqual(run["case_passes"], 1)
        self.assertEqual(run["mean_score"], 2.0)


if __name__ == "__main__":
    unittest.main()
