# Release roadmap

The roadmap separates implemented foundations from future research and validation gates. Version numbers are targets, not claims that a release has shipped.

| Version | Main objective | Scope and acceptance gate | Status |
|---|---|---|---|
| 0.2.0 | Evaluation framework and session-state improvements | Versioned learner-state companion, assessment rubric, trigger/boundary evaluation cases, and scorer that separates structural checks from model behavior. | Implemented in this PR |
| 0.3.0 | Adaptive assessment and spaced-repetition improvements | Add evidence-aware difficulty adaptation, calibrated review scheduling, and regression cases for level promotion, demotion, and retention. Require user-visible evidence for every mastery change. | Planned |
| 0.4.0 | Cross-agent compatibility and automated validation | Portable install tooling, optional host metadata, manifest checks, preservation checks, and CI across supported Python versions. | Implemented in this PR |
| 0.5.0 | Mathematical reasoning and research tutor | Add mathematical-reasoning and research-paper-tutor skills, with code-understanding and interview-simulator as complementary learning tools; validate each with trigger and boundary scenarios. | Initial skills and cases added; behavioral runs pending |
| 1.0.0 | Stable, tested skill collection with documented benchmarks | Freeze schemas and compatibility promises, document supported hosts, complete blinded skill-enabled versus baseline evaluations, publish model/host/run details and limitations, and resolve critical failures. | Future release gate |

## Release discipline

- Do not publish a benchmark score until responses have been generated under a recorded model/host configuration and reviewed using the rubric.
- Treat the 40 starter prompts as a regression suite, not an industry benchmark.
- Keep the 16 existing skills' instruction files unchanged during this restructure. Any future edits require a separate, explicit change with corresponding evaluation updates.
- Use release tags only after the relevant acceptance gates pass.
