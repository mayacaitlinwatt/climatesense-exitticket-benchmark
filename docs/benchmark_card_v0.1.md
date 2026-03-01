# Benchmark Card — ClimateSense Exit-Ticket Benchmark v0.1

**Version:** 0.1 (Public Preview)  
**Date:** 2026-02-28  
**Maintainer:** People's Evidence Lab | stevewatt13@peoplesevidencelab.com  
**License:** CC BY 4.0 (data/docs) | Apache 2.0 (code)

---

## Intended use

This benchmark is designed for **researchers, vendors, and districts** evaluating AI systems that assist with formative assessment in K–12 science classrooms. Specifically, it supports evaluation of AI tools that analyze student exit-ticket responses to:

- Identify misconception families in student science responses
- Generate feedback useful to teachers for next instructional steps

Intended users include: AI developers, education technology vendors, learning scientists, and school/district assessment teams conducting AI tool evaluation.

---

## Not intended for

- **Grading or high-stakes decisions** of any kind
- Direct use with students without educator review and adaptation
- Evaluation of student learning outcomes as individuals
- Contexts outside grades 9–10 science without additional validation

---

## Scope

| Attribute | Value |
|---|---|
| Grade band | 9–10 |
| Domain | Climate systems & carbon cycling |
| Response type | Short science explanations (exit tickets) |
| Language | English (primary); multilingual-leaning and code-switched conditions included |
| Data origin (v0.1) | Constructed exemplars |
| Misconception families (v0.1) | 6 (see `schema/label_taxonomy_v0.1.md`) |
| Expression conditions | academic_standard, telegraphic_short_form, multilingual_leaning, dialectal_variety, code_switched |

---

## Evaluation tracks and metrics

### Track 1 — Misconception detection
- **Primary metric:** Accuracy (predicted label vs. gold label)
- **Robustness metric:** Accuracy delta across expression conditions relative to `academic_standard` baseline
- **Reported by:** misconception family, expression condition, prompt

### Track 2 — Teacher usefulness
- **Primary metric:** Teacher Usefulness Composite (mean of 4 dimensions, 0–3 scale)
  - Correctness / Diagnostic validity
  - Clarity (teacher-time reality)
  - Actionability (feed-forward)
  - Instructional alignment
- **Safety flags:** Hallucination rate, unsafe recommendation rate
- **Adoption signal:** "Would you use this?" item (reported separately)
- **Reported by:** misconception family, expression condition, prompt

---

## Limitations

- v0.1 data are **constructed exemplars**, not validated with authentic student responses. Results should be interpreted as proof-of-concept only.
- Misconception families are limited to 6 in v0.1. Real-world student responses may involve families not yet represented.
- Teacher usefulness scoring at v0.1 uses a small rater pool (3–6 educators). Inter-rater reliability is not formally computed until v1.0.
- The benchmark currently covers English-language responses only. Multilingual-leaning and code-switched conditions are included as response-form variation, not as a full multilingual benchmark.
- Content validity (accuracy of misconception family definitions) has not yet been externally reviewed by climate science experts at v0.1.

---

## Versioning policy

| Version | Status | Data origin | Reliability |
|---|---|---|---|
| 0.1 | Public preview | Constructed exemplars | Spot-check only |
| 1.0 (planned) | Validated benchmark | Educator-constructed + authentic | Formal IRR (kappa/alpha) |

Breaking changes to label definitions or schema will increment the minor version and be logged in `CHANGELOG.md`.

---

## Citation

> People's Evidence Lab. (2026). *ClimateSense Exit-Ticket Benchmark v0.1* [Public preview]. https://github.com/PeoplesEvidenceLab/climatesense-exitticket-benchmark

See `CITATION.cff` for machine-readable citation metadata.
