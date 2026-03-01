# Changelog

All notable changes to the ClimateSense Exit-Ticket Benchmark will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).  
This project uses semantic versioning starting at v0.1 (public preview).

---

## [v0.1] — 2026-02-28 — Initial Public Preview

### Added
- Runnable evaluation harness (`harness/evaluate.py`) supporting:
  - Misconception-family prediction scoring
  - Teacher usefulness scoring
  - Combined run mode
- Sample dataset, predictions, and teacher ratings (constructed exemplars, grades 9–10, climate/carbon cycling domain)
- Dataset schema (`schema/dataset_schema_v0.1.json`) and label taxonomy (`schema/label_taxonomy_v0.1.md`)
- Label Protocol v0.1 (`docs/GRNT001-ClimateSense-LabelProtocol-v0.1.md`)
- Teacher Usefulness Rubric v0.1 (`docs/GRNT001-ClimateSense-TeacherUsefulnessRubric-v0.1.md`)
- Benchmark Card v0.1 (`docs/benchmark_card_v0.1.md`)
- Adoption Quickstart (`docs/adoption_quickstart_v0.1.md`)
- Governance and Issues guide (`docs/governance_and_issues.md`)
- Apache 2.0 license (code) and CC BY 4.0 license (data/docs)
- CITATION.cff

### Notes
- Data are **constructed exemplars** — not authentic student responses.
- **Not for grading or high-stakes decisions.**
- v1.0 will include validated data, inter-rater reliability reporting, and expanded misconception families.
