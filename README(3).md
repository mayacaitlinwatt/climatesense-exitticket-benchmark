# ClimateSense Exit-Ticket Benchmark — v0.1 Public Preview

> **Status:** Public preview / proof-of-concept (constructed exemplars)  
> **Not for grading or high-stakes decisions.**

## What this is

The ClimateSense Exit-Ticket Benchmark is an open evaluation harness for AI systems that support formative assessment in K–12 science classrooms. It measures whether an AI system can correctly identify **student misconception families** in short exit-ticket responses about climate systems and carbon cycling (grades 9–10).

This v0.1 public preview includes:
- A runnable evaluation harness (`harness/evaluate.py`)
- Sample dataset, predictions, and teacher ratings (constructed exemplars)
- Dataset schema and label taxonomy
- Label protocol and teacher usefulness rubric
- Benchmark card, governance notes, and quickstart guide

This repository is published as a **delivery-readiness artifact** for GRNT001 (ClimateSense, People's Evidence Lab).

---

## What it measures

| Track | What's evaluated | Key metric |
|---|---|---|
| Misconception detection | Does the AI correctly identify the misconception family? | Accuracy, robustness delta across response-form conditions |
| Teacher usefulness | Is the AI's feedback useful for a teacher's next instructional move? | Teacher Usefulness Composite (0–3 scale, 4 dimensions) |
| Safety | Does the AI hallucinate or give unsafe recommendations? | Hallucination flag rate, unsafe flag rate |

---

## Quickstart

### Prerequisites
- Python 3.8+
- No external dependencies required for the base harness

### Run predictions scoring
```bash
python harness/evaluate.py \
  --dataset data/sample_v0.1/dataset_sample_v0.1.jsonl \
  --predictions data/sample_v0.1/predictions_example_v0.1.jsonl \
  --out outputs_pred \
  --baseline_condition academic_standard
```

### Run teacher usefulness scoring
```bash
python harness/evaluate.py \
  --dataset data/sample_v0.1/dataset_sample_v0.1.jsonl \
  --teacher_ratings data/sample_v0.1/teacher_ratings_example_v0.1.csv \
  --out outputs_teacher
```

### Run both
```bash
python harness/evaluate.py \
  --dataset data/sample_v0.1/dataset_sample_v0.1.jsonl \
  --predictions data/sample_v0.1/predictions_example_v0.1.jsonl \
  --teacher_ratings data/sample_v0.1/teacher_ratings_example_v0.1.csv \
  --out outputs_all
```

See `harness/README.md` for full usage documentation.

---

## Repository structure

```
climatesense-exitticket-benchmark/
  README.md                          ← you are here
  CHANGELOG.md                       ← version history
  CITATION.cff                       ← how to cite
  LICENSE-APACHE-2.0.txt             ← code license
  LICENSE-CC-BY-4.0.txt              ← data/docs license

  data/sample_v0.1/                  ← example inputs (constructed exemplars)
  schema/                            ← dataset schema + label taxonomy
  harness/                           ← runnable evaluation harness
  docs/                              ← benchmark card, protocols, governance
```

---

## Scope and limitations

- **Grade band:** 9–10
- **Domain:** Climate systems & carbon cycling (short science explanations)
- **Data origin:** Constructed exemplars (v0.1); not authentic student data
- **Not for:** grading, high-stakes decisions, or direct use without educator review
- **Intended for:** researchers, vendors, and districts evaluating AI formative assessment tools

---

## Licensing

- **Code** (`harness/`): [Apache 2.0](LICENSE-APACHE-2.0.txt)
- **Data and documentation** (`data/`, `docs/`, `schema/`): [CC BY 4.0](LICENSE-CC-BY-4.0.txt)

---

## How to cite

See `CITATION.cff`. Quick citation:

> People's Evidence Lab. (2026). *ClimateSense Exit-Ticket Benchmark v0.1* [Public preview]. https://github.com/PeoplesEvidenceLab/climatesense-exitticket-benchmark

---

## Contact

Questions, issues, or adoption inquiries: **stevewatt13@peoplesevidencelab.com**  
File issues via the [Issues tab](../../issues) using the provided templates.
