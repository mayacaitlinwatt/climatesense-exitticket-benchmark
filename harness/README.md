# Harness — evaluate.py

The ClimateSense evaluation harness scores AI system outputs against the v0.1 benchmark dataset.

## Requirements
- Python 3.8+
- No external dependencies required

## Input files

| File | Description |
|---|---|
| `data/sample_v0.1/dataset_sample_v0.1.jsonl` | Student responses + gold labels |
| `data/sample_v0.1/predictions_example_v0.1.jsonl` | AI system predictions to evaluate |
| `data/sample_v0.1/teacher_ratings_example_v0.1.csv` | Teacher usefulness ratings |

## Usage

### Score predictions only
```bash
python harness/evaluate.py \
  --dataset data/sample_v0.1/dataset_sample_v0.1.jsonl \
  --predictions data/sample_v0.1/predictions_example_v0.1.jsonl \
  --out outputs_pred \
  --baseline_condition academic_standard
```

### Score teacher usefulness only
```bash
python harness/evaluate.py \
  --dataset data/sample_v0.1/dataset_sample_v0.1.jsonl \
  --teacher_ratings data/sample_v0.1/teacher_ratings_example_v0.1.csv \
  --out outputs_teacher
```

### Run both tracks together
```bash
python harness/evaluate.py \
  --dataset data/sample_v0.1/dataset_sample_v0.1.jsonl \
  --predictions data/sample_v0.1/predictions_example_v0.1.jsonl \
  --teacher_ratings data/sample_v0.1/teacher_ratings_example_v0.1.csv \
  --out outputs_all
```

## Output files

The harness writes results to the specified `--out` directory:

| File | Description |
|---|---|
| `scored_report_v0.1.json` | Full scored report (all metrics) |
| `scored_report_by_condition_v0.1.csv` | Accuracy/robustness broken down by response-form condition |
| `scored_report_by_label_v0.1.csv` | Accuracy broken down by misconception family |
| `confusion_matrix_v0.1.csv` | Confusion matrix for prediction scoring |

See `docs/adoption_quickstart_v0.1.md` for guidance on interpreting results.

## Arguments

| Argument | Required | Description |
|---|---|---|
| `--dataset` | Yes | Path to dataset JSONL file |
| `--predictions` | No* | Path to predictions JSONL file |
| `--teacher_ratings` | No* | Path to teacher ratings CSV |
| `--out` | Yes | Output directory (created if not exists) |
| `--baseline_condition` | No | Condition to use as robustness baseline (default: `academic_standard`) |

*At least one of `--predictions` or `--teacher_ratings` must be provided.

## Licensing
Code in this directory is licensed under Apache 2.0. See `../LICENSE-APACHE-2.0.txt`.
