#!/usr/bin/env python3
"""
ClimateSense — Minimal Evaluator Harness (Skeleton) + Teacher Usefulness

This runnable "test rig" can:
1) Score classification predictions against gold labels.
2) Optionally score teacher usefulness ratings (rubric A–D + safety flags) against the dataset,
   producing aggregate reports overall and disaggregated by expression condition and misconception.

Inputs:
- Dataset: JSONL or CSV with gold labels and expression_condition
- Predictions: JSONL or CSV with predicted_label (optional if you only want teacher usefulness outputs)
- Teacher ratings: CSV with rubric scores per record_id (and optionally model_id/run_id/rater_id)

Outputs:
- scored_report.json, scored_report_by_label.csv, scored_report_by_condition.csv, confusion_matrix.csv
- teacher_usefulness_report_overall.csv
- teacher_usefulness_by_condition.csv
- teacher_usefulness_by_misconception.csv
- teacher_safety_flags_summary.csv
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional


REQUIRED_DATASET_FIELDS = [
    "record_id",
    "item_id",
    "prompt_text",
    "response_text",
    "expression_condition",
    "gold_label_primary",
]

REQUIRED_PREDICTION_FIELDS = [
    "record_id",
    "predicted_label",
]

REQUIRED_TEACHER_RATING_FIELDS = [
    "record_id",
    "model_id",
    "run_id",
    "rater_id",
    "rubric_version",
    "correctness_0_3",
    "clarity_0_3",
    "actionability_0_3",
    "instructional_alignment_0_3",
    "hallucination_flag_0_1",
    "unsafe_flag_0_1",
]


def _is_csv(path: Path) -> bool:
    return path.suffix.lower() == ".csv"


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def load_csv(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [dict(r) for r in reader]


def load_table(path: Path) -> List[Dict[str, Any]]:
    if _is_csv(path):
        return load_csv(path)
    # default to JSONL
    return load_jsonl(path)


def validate_fields(rows: List[Dict[str, Any]], required: List[str], label: str) -> None:
    if not rows:
        raise ValueError(f"{label} file appears empty.")
    missing = [k for k in required if k not in rows[0]]
    if missing:
        raise ValueError(f"{label} missing required fields: {missing}. Found keys: {sorted(rows[0].keys())}")


def safe_div(a: float, b: float) -> float:
    return float(a) / float(b) if b else 0.0


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)


def write_cm_csv(path: Path, cm_table: List[List[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        for row in cm_table:
            w.writerow(row)


def compute_prediction_metrics(
    gold_rows: List[Dict[str, Any]],
    pred_rows: List[Dict[str, Any]],
    baseline_condition: str = "academic_standard",
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]], List[List[Any]]]:

    pred_by_id: Dict[str, Dict[str, Any]] = {p["record_id"]: p for p in pred_rows}

    labels = sorted(set([r["gold_label_primary"] for r in gold_rows] + [p["predicted_label"] for p in pred_rows]))
    label_index = {lab: i for i, lab in enumerate(labels)}

    # confusion matrix
    cm = [[0 for _ in labels] for _ in labels]  # rows=gold, cols=pred

    y_true: List[str] = []
    y_pred: List[str] = []
    missing_preds: List[str] = []

    # per-condition accuracy counters
    by_condition = defaultdict(lambda: {"n": 0, "correct": 0})

    for r in gold_rows:
        rid = r["record_id"]
        if rid not in pred_by_id:
            missing_preds.append(rid)
            continue
        gt = r["gold_label_primary"]
        pr = pred_by_id[rid]["predicted_label"]

        y_true.append(gt)
        y_pred.append(pr)

        cm[label_index[gt]][label_index[pr]] += 1

        cond = r.get("expression_condition", "UNKNOWN")
        by_condition[cond]["n"] += 1
        if gt == pr:
            by_condition[cond]["correct"] += 1

    # overall accuracy
    overall_n = len(y_true)
    overall_correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    overall_acc = safe_div(overall_correct, overall_n)

    # one-vs-rest per-label precision/recall/f1
    by_label = {lab: {"tp": 0, "fp": 0, "fn": 0, "support": 0} for lab in labels}
    for t in y_true:
        by_label[t]["support"] += 1

    for t, p in zip(y_true, y_pred):
        for lab in labels:
            if p == lab and t == lab:
                by_label[lab]["tp"] += 1
            elif p == lab and t != lab:
                by_label[lab]["fp"] += 1
            elif p != lab and t == lab:
                by_label[lab]["fn"] += 1

    per_label_metrics: List[Dict[str, Any]] = []
    for lab in labels:
        tp = by_label[lab]["tp"]
        fp = by_label[lab]["fp"]
        fn = by_label[lab]["fn"]
        prec = safe_div(tp, tp + fp)
        rec = safe_div(tp, tp + fn)
        f1 = safe_div(2 * prec * rec, prec + rec) if (prec + rec) else 0.0
        per_label_metrics.append(
            {
                "label": lab,
                "precision": round(prec, 3),
                "recall": round(rec, 3),
                "f1": round(f1, 3),
                "support": int(by_label[lab]["support"]),
            }
        )

    macro_f1 = safe_div(sum(m["f1"] for m in per_label_metrics), len(per_label_metrics))

    # by-condition breakdown + robustness delta vs baseline
    baseline_acc = None
    if by_condition[baseline_condition]["n"]:
        baseline_acc = safe_div(by_condition[baseline_condition]["correct"], by_condition[baseline_condition]["n"])

    by_condition_rows: List[Dict[str, Any]] = []
    for cond, stats in sorted(by_condition.items(), key=lambda kv: kv[0]):
        acc = safe_div(stats["correct"], stats["n"])
        delta = ""
        if baseline_acc is not None and cond != baseline_condition:
            delta = round(acc - baseline_acc, 3)
        by_condition_rows.append(
            {
                "expression_condition": cond,
                "n": int(stats["n"]),
                "accuracy": round(acc, 3),
                "robustness_delta_vs_baseline": delta,
                "baseline_condition": baseline_condition,
            }
        )

    # confusion matrix rows with headers
    cm_table: List[List[Any]] = []
    cm_table.append(["gold\\pred"] + labels)
    for i, gold_lab in enumerate(labels):
        cm_table.append([gold_lab] + cm[i])

    report = {
        "n_scored": overall_n,
        "n_missing_predictions": len(missing_preds),
        "overall_accuracy": round(overall_acc, 3),
        "macro_f1": round(macro_f1, 3),
        "baseline_condition": baseline_condition,
        "missing_prediction_record_ids": missing_preds[:50],  # cap for readability
        "notes": [
            "This harness is a minimal skeleton intended to demonstrate reproducible scoring and reporting.",
            "For v0.1 public preview, datasets may include constructed exemplars; do not generalize performance to authentic student populations.",
        ],
    }

    return report, per_label_metrics, by_condition_rows, cm_table


def _to_float(x: Any) -> Optional[float]:
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).strip()
    if s == "":
        return None
    try:
        return float(s)
    except Exception:
        return None


def _to_int(x: Any) -> Optional[int]:
    f = _to_float(x)
    if f is None:
        return None
    return int(round(f))


def compute_teacher_usefulness(
    dataset_rows: List[Dict[str, Any]],
    rating_rows: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Returns:
      - overall rows
      - by_condition rows
      - by_misconception rows
      - safety summary rows
    """

    # Index dataset fields needed for grouping
    ds_by_id = {r["record_id"]: r for r in dataset_rows}

    # Group ratings by (model_id, run_id)
    groups = defaultdict(list)
    missing_dataset = 0

    for rr in rating_rows:
        rid = rr.get("record_id")
        if rid not in ds_by_id:
            missing_dataset += 1
            continue
        key = (rr.get("model_id", "UNKNOWN"), rr.get("run_id", "UNKNOWN"), rr.get("rubric_version", "UNKNOWN"))
        groups[key].append(rr)

    def row_scores(rr: Dict[str, Any]) -> Dict[str, Optional[float]]:
        a = _to_float(rr.get("correctness_0_3"))
        b = _to_float(rr.get("clarity_0_3"))
        c = _to_float(rr.get("actionability_0_3"))
        d = _to_float(rr.get("instructional_alignment_0_3"))
        e = _to_float(rr.get("would_use_in_class_0_3"))  # optional
        halluc = _to_int(rr.get("hallucination_flag_0_1"))
        unsafe = _to_int(rr.get("unsafe_flag_0_1"))
        comp = None
        if None not in (a, b, c, d):
            comp = (a + b + c + d) / 4.0
        return {
            "a_correctness": a,
            "b_clarity": b,
            "c_actionability": c,
            "d_alignment": d,
            "e_would_use": e,
            "composite": comp,
            "hallucination": halluc,
            "unsafe": unsafe,
        }

    overall_rows: List[Dict[str, Any]] = []
    by_condition_rows: List[Dict[str, Any]] = []
    by_misconception_rows: List[Dict[str, Any]] = []
    safety_rows: List[Dict[str, Any]] = []

    for (model_id, run_id, rubric_version), rows in sorted(groups.items()):
        # Overall aggregation
        agg = defaultdict(float)
        counts = defaultdict(int)

        # breakdown structures
        cond_agg = defaultdict(lambda: (defaultdict(float), defaultdict(int)))
        misc_agg = defaultdict(lambda: (defaultdict(float), defaultdict(int)))

        halluc_n = 0
        unsafe_n = 0
        total_n = 0
        composite_missing = 0

        for rr in rows:
            scores = row_scores(rr)
            rid = rr["record_id"]
            ds = ds_by_id[rid]
            cond = ds.get("expression_condition", "UNKNOWN")
            misc = ds.get("gold_label_primary", "UNKNOWN")

            total_n += 1
            if scores["hallucination"] == 1:
                halluc_n += 1
            if scores["unsafe"] == 1:
                unsafe_n += 1

            # Overall: average each dimension when present
            for k, v in [("correctness", scores["a_correctness"]),
                         ("clarity", scores["b_clarity"]),
                         ("actionability", scores["c_actionability"]),
                         ("alignment", scores["d_alignment"]),
                         ("would_use", scores["e_would_use"]),
                         ("composite", scores["composite"])]:
                if v is None:
                    if k == "composite":
                        composite_missing += 1
                    continue
                agg[k] += float(v)
                counts[k] += 1

            # By condition
            a1, c1 = cond_agg[cond]
            for k, v in [("correctness", scores["a_correctness"]),
                         ("clarity", scores["b_clarity"]),
                         ("actionability", scores["c_actionability"]),
                         ("alignment", scores["d_alignment"]),
                         ("would_use", scores["e_would_use"]),
                         ("composite", scores["composite"])]:
                if v is None:
                    continue
                a1[k] += float(v)
                c1[k] += 1

            # By misconception
            a2, c2 = misc_agg[misc]
            for k, v in [("correctness", scores["a_correctness"]),
                         ("clarity", scores["b_clarity"]),
                         ("actionability", scores["c_actionability"]),
                         ("alignment", scores["d_alignment"]),
                         ("would_use", scores["e_would_use"]),
                         ("composite", scores["composite"])]:
                if v is None:
                    continue
                a2[k] += float(v)
                c2[k] += 1

        overall_rows.append({
            "model_id": model_id,
            "run_id": run_id,
            "rubric_version": rubric_version,
            "n_ratings": total_n,
            "mean_correctness_0_3": round(safe_div(agg["correctness"], counts["correctness"]), 3) if counts["correctness"] else "",
            "mean_clarity_0_3": round(safe_div(agg["clarity"], counts["clarity"]), 3) if counts["clarity"] else "",
            "mean_actionability_0_3": round(safe_div(agg["actionability"], counts["actionability"]), 3) if counts["actionability"] else "",
            "mean_instructional_alignment_0_3": round(safe_div(agg["alignment"], counts["alignment"]), 3) if counts["alignment"] else "",
            "mean_would_use_in_class_0_3": round(safe_div(agg["would_use"], counts["would_use"]), 3) if counts["would_use"] else "",
            "mean_usefulness_composite_0_3": round(safe_div(agg["composite"], counts["composite"]), 3) if counts["composite"] else "",
            "composite_missing_count": composite_missing,
            "hallucination_flag_rate": round(safe_div(halluc_n, total_n), 3) if total_n else "",
            "unsafe_flag_rate": round(safe_div(unsafe_n, total_n), 3) if total_n else "",
        })

        safety_rows.append({
            "model_id": model_id,
            "run_id": run_id,
            "rubric_version": rubric_version,
            "n_ratings": total_n,
            "hallucination_flag_count": halluc_n,
            "unsafe_flag_count": unsafe_n,
            "hallucination_flag_rate": round(safe_div(halluc_n, total_n), 3) if total_n else "",
            "unsafe_flag_rate": round(safe_div(unsafe_n, total_n), 3) if total_n else "",
            "notes": "Flag rates are reported separately from rubric means (binary safety checks).",
        })

        for cond, (a, c) in sorted(cond_agg.items(), key=lambda kv: kv[0]):
            by_condition_rows.append({
                "model_id": model_id,
                "run_id": run_id,
                "rubric_version": rubric_version,
                "expression_condition": cond,
                "n_ratings": c.get("composite", 0) or max(c.values()) if c else 0,
                "mean_usefulness_composite_0_3": round(safe_div(a["composite"], c["composite"]), 3) if c.get("composite") else "",
                "mean_correctness_0_3": round(safe_div(a["correctness"], c["correctness"]), 3) if c.get("correctness") else "",
                "mean_clarity_0_3": round(safe_div(a["clarity"], c["clarity"]), 3) if c.get("clarity") else "",
                "mean_actionability_0_3": round(safe_div(a["actionability"], c["actionability"]), 3) if c.get("actionability") else "",
                "mean_instructional_alignment_0_3": round(safe_div(a["alignment"], c["alignment"]), 3) if c.get("alignment") else "",
                "mean_would_use_in_class_0_3": round(safe_div(a["would_use"], c["would_use"]), 3) if c.get("would_use") else "",
            })

        for misc, (a, c) in sorted(misc_agg.items(), key=lambda kv: kv[0]):
            by_misconception_rows.append({
                "model_id": model_id,
                "run_id": run_id,
                "rubric_version": rubric_version,
                "gold_label_primary": misc,
                "n_ratings": c.get("composite", 0) or max(c.values()) if c else 0,
                "mean_usefulness_composite_0_3": round(safe_div(a["composite"], c["composite"]), 3) if c.get("composite") else "",
                "mean_correctness_0_3": round(safe_div(a["correctness"], c["correctness"]), 3) if c.get("correctness") else "",
                "mean_clarity_0_3": round(safe_div(a["clarity"], c["clarity"]), 3) if c.get("clarity") else "",
                "mean_actionability_0_3": round(safe_div(a["actionability"], c["actionability"]), 3) if c.get("actionability") else "",
                "mean_instructional_alignment_0_3": round(safe_div(a["alignment"], c["alignment"]), 3) if c.get("alignment") else "",
                "mean_would_use_in_class_0_3": round(safe_div(a["would_use"], c["would_use"]), 3) if c.get("would_use") else "",
            })

    # Add a note row if any rating rows didn't match dataset
    if missing_dataset:
        safety_rows.append({
            "model_id": "",
            "run_id": "",
            "rubric_version": "",
            "n_ratings": "",
            "hallucination_flag_count": "",
            "unsafe_flag_count": "",
            "hallucination_flag_rate": "",
            "unsafe_flag_rate": "",
            "notes": f"{missing_dataset} teacher rating rows had record_id values not found in dataset; they were skipped.",
        })

    return overall_rows, by_condition_rows, by_misconception_rows, safety_rows


def main() -> None:
    ap = argparse.ArgumentParser(description="ClimateSense minimal evaluator harness (skeleton) + teacher usefulness")
    ap.add_argument("--dataset", required=True, help="Path to dataset JSONL or CSV containing gold labels")
    ap.add_argument("--predictions", required=False, help="Path to predictions JSONL or CSV containing model outputs")
    ap.add_argument("--teacher_ratings", required=False, help="Path to teacher ratings CSV (rubric scores)")
    ap.add_argument("--out", required=True, help="Output directory for scored reports")
    ap.add_argument("--baseline_condition", default="academic_standard", help="Condition used as baseline for deltas")
    args = ap.parse_args()

    dataset_path = Path(args.dataset)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    dataset_rows = load_table(dataset_path)
    validate_fields(dataset_rows, REQUIRED_DATASET_FIELDS, "Dataset")

    # Prediction scoring (optional)
    if args.predictions:
        pred_path = Path(args.predictions)
        pred_rows = load_table(pred_path)
        validate_fields(pred_rows, REQUIRED_PREDICTION_FIELDS, "Predictions")

        report, per_label, by_cond, cm_table = compute_prediction_metrics(
            gold_rows=dataset_rows,
            pred_rows=pred_rows,
            baseline_condition=args.baseline_condition,
        )

        write_json(out_dir / "scored_report.json", report)
        write_csv(out_dir / "scored_report_by_label.csv", per_label)
        write_csv(out_dir / "scored_report_by_condition.csv", by_cond)
        write_cm_csv(out_dir / "confusion_matrix.csv", cm_table)

        print(f"[Predictions] Scored n={report['n_scored']} (missing predictions: {report['n_missing_predictions']})")
        print(f"[Predictions] Overall accuracy: {report['overall_accuracy']}")
        print(f"[Predictions] Macro-F1: {report['macro_f1']}")

    # Teacher usefulness scoring (optional)
    if args.teacher_ratings:
        ratings_path = Path(args.teacher_ratings)
        rating_rows = load_csv(ratings_path)
        validate_fields(rating_rows, REQUIRED_TEACHER_RATING_FIELDS, "Teacher ratings")

        overall, by_condition, by_misconception, safety = compute_teacher_usefulness(
            dataset_rows=dataset_rows,
            rating_rows=rating_rows,
        )

        write_csv(out_dir / "teacher_usefulness_report_overall.csv", overall)
        write_csv(out_dir / "teacher_usefulness_by_condition.csv", by_condition)
        write_csv(out_dir / "teacher_usefulness_by_misconception.csv", by_misconception)
        write_csv(out_dir / "teacher_safety_flags_summary.csv", safety)

        # Console summary (first overall row)
        if overall:
            r0 = overall[0]
            print(f"[Teacher] Model={r0['model_id']} Run={r0['run_id']} Ratings={r0['n_ratings']}")
            print(f"[Teacher] Mean composite usefulness (0–3): {r0['mean_usefulness_composite_0_3']}")
            print(f"[Teacher] Hallucination rate: {r0['hallucination_flag_rate']}; Unsafe rate: {r0['unsafe_flag_rate']}")

    if not args.predictions and not args.teacher_ratings:
        print("Nothing to do: provide --predictions and/or --teacher_ratings.")


if __name__ == "__main__":
    main()
