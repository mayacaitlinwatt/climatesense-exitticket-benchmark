# Adoption Quickstart — ClimateSense v0.1

This guide explains how vendors, districts, and researchers can use the ClimateSense benchmark to evaluate an AI formative assessment tool.

---

## Who this is for

- **AI/EdTech vendors** who want to demonstrate that their tool performs well on misconception detection and teacher usefulness
- **Districts and schools** evaluating AI tools before adoption
- **Learning scientists and researchers** studying AI performance in formative assessment contexts

---

## What you need to bring

To benchmark your system against ClimateSense v0.1, you need:

1. **Your system's predictions** in JSONL format (one record per line), with fields:
   - `record_id` — matches records in `dataset_sample_v0.1.jsonl`
   - `predicted_label` — your system's predicted misconception family or non-misconception label
   - (Optional) `feedback_text` — AI-generated feedback for teacher usefulness scoring
   - (Optional) `next_step_text` — AI-generated next instructional step

2. **Teacher ratings** (if running Track 2) — use the template at `data/sample_v0.1/teacher_ratings_example_v0.1.csv` and the rubric at `docs/GRNT001-ClimateSense-TeacherUsefulnessRubric-v0.1.md`

---

## Step-by-step

### Step 1 — Run your system on the dataset
Feed `data/sample_v0.1/dataset_sample_v0.1.jsonl` to your AI system. Collect predictions in the format described above.

### Step 2 — Run the harness
```bash
python harness/evaluate.py \
  --dataset data/sample_v0.1/dataset_sample_v0.1.jsonl \
  --predictions your_predictions.jsonl \
  --out my_results \
  --baseline_condition academic_standard
```

### Step 3 — Interpret the outputs

Key outputs in your `--out` directory:

| File | What to look at |
|---|---|
| `scored_report_v0.1.json` | Overall accuracy + robustness delta summary |
| `scored_report_by_condition_v0.1.csv` | How accuracy changes across expression conditions |
| `scored_report_by_label_v0.1.csv` | Per-misconception-family accuracy |
| `confusion_matrix_v0.1.csv` | Where your system confuses families |

**Robustness delta** is the key equity-relevant metric: it shows whether your system's accuracy drops for responses in non-academic-standard conditions (telegraphic, multilingual-leaning, dialectal variety, code-switched). A well-performing system should show minimal delta across conditions.

### Step 4 — (Optional) Run teacher usefulness scoring
Recruit 3–6 educators to rate AI-generated feedback using the Teacher Usefulness Rubric (`docs/GRNT001-ClimateSense-TeacherUsefulnessRubric-v0.1.md`). Enter ratings into the teacher ratings template (`data/sample_v0.1/teacher_ratings_example_v0.1.csv`) and run the harness with `--teacher_ratings`.

---

## Reporting results

When reporting results publicly, please include:
- Benchmark version (`v0.1`)
- Data split used (`sample_v0.1` for public preview)
- Whether teacher usefulness was evaluated and rater pool size
- Any known limitations of your evaluation setup

---

## Questions and issues

Contact: **stevewatt13@peoplesevidencelab.com**  
Or file an issue via the [Issues tab](../../issues).
