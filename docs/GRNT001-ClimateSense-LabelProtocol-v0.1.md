---
ArtifactID: "GRNT001-LABEL-2026-001-ClimateSense-LabelProtocol-v0.1"
Title: "ClimateSense — Label Protocol v0.1 (Gold Labels for Misconception Families)"
Date: "2026-02-28"
Version: "0.1"
Maintainer: "Steve Watt (People’s Evidence Lab)"
ArtifactType: "Protocol"
Project: "GRNT001 ClimateSense Exit-Ticket Benchmark"
Scope:
  GradeBand: "9–10"
  Domain: "Climate systems & carbon cycling (short science explanations)"
Status: "Public preview / PoC-ready"
License: "Documentation CC BY 4.0 (recommended)"
Tags:
  - "#GRNT001"
  - "#ClimateSense"
  - "#labeling"
  - "#benchmark"
  - "#targeted_universalism"
  - "#provenance"
Provenance:
  CreatedBy: "ChatGPT with user direction"
  CreatedFor: "Grant submission support + v0.1 public preview repo"
  Inputs:
    - "ClimateSense v0.5 proposal (user-provided)"
  Notes: "Defines how gold labels are assigned, adjudicated, and recorded for benchmarking."
---

## 🧭 Provenance Summary
This protocol specifies how ClimateSense assigns and governs **gold labels** (human-derived ground truth) for short student responses. It is designed to be **transparent, repeatable, and scalable** from a small v0.1 public preview (constructed exemplars) to a validated v1.0 benchmark with educator/content-expert labeling and basic reliability reporting.

---

# ClimateSense — Label Protocol v0.1

## 1) Purpose
ClimateSense evaluates AI systems that support formative assessment by detecting:
- **Misconception family** (the underlying “type of wrong idea”), or
- **Scientifically correct / unclear / off-topic** outcomes.

This protocol defines how we create the **gold label** for each response so the evaluator harness can compute accuracy, robustness deltas across response-form conditions, and (optionally) teacher-usefulness scoring.

## 2) Definitions (plain English)

### Gold label
The **gold label** is the benchmark’s best-available “ground truth” for what a response demonstrates.  
It is **human-assigned** using a documented taxonomy and rules. “Gold” does not mean perfect; it means **auditable and consistent enough** to score systems against.

### Misconception family
A **misconception family** is a bucket for a recurring, recognizable wrong idea (e.g., “ozone hole causes warming” or “carbon disappears quickly”).  
Different phrasing can still map to the same family.

### Response-form condition
A **condition** is a property of the **response text form** (register/structure), not a student identity.  
Example conditions include academic-standard, telegraphic short-form, multilingual-leaning, dialectal variety features, and code-switched phrasing.

## 3) Label space (what labels are allowed)
Each record receives **one primary label** from:

### A) Misconception families
- `MFxx_<short_name>` (e.g., `MF01_ozone_vs_greenhouse`, `MF04_carbon_disappears`)

### B) Non-misconception labels (escape valves)
- `SCIENTIFICALLY_CORRECT`
- `UNCLEAR_INSUFFICIENT_EVIDENCE`
- `OFF_TOPIC_NOISY`

**Optional (recommended):**
- `secondary_labels`: list of additional misconception families if a response contains mixed ideas.
- `label_confidence`: `high | medium | low` (or numeric 0–1).

## 4) Taxonomy artifacts required before labeling
Labeling must be based on an explicit taxonomy package:

1. **Misconception Family Cards** (one per family), each containing:
   - Name + short ID (`MFxx`)
   - 1–2 sentence definition
   - Inclusion rules (what counts)
   - Exclusion rules (what does *not* count)
   - 2–3 positive examples + 2–3 counterexamples
   - (Optional) teacher next-step hint

2. **Benchmark Card** (dataset scope, limitations, intended use)

For v0.1, these can be “draft” but must exist.

## 5) Who labels (roles)
Minimum roles by version:

### v0.1 (public preview / proof-of-concept)
- **Primary labeler:** project team (PEL)
- **Reviewer (recommended):** 1 educator OR assessment specialist for spot-checking

### v1.0 (validated benchmark)
- **Labelers:** ≥2 independent educators and/or assessment specialists
- **Content check:** ≥1 climate content expert (can be an educator with strong content expertise)
- **Adjudicator:** designated third rater or consensus lead

## 6) Labeling procedure (step-by-step)

### Step 0 — Setup
- Freeze: `label_taxonomy_vX.Y` and `family_cards_vX.Y` for the labeling batch.
- Prepare a labeling sheet/tool that shows:
  - prompt
  - response text
  - condition tag (if applicable)
  - the family cards (or links)

### Step 1 — Independent labeling (required for v1.0; recommended for v0.1)
Each labeler assigns:
- `primary_label`
- `secondary_labels` (optional)
- `label_confidence`
- brief `label_notes` (optional; useful for disagreements)

### Step 2 — Disagreement detection
Flag records for adjudication when:
- primary labels differ, OR
- one labeler marks `UNCLEAR` while another assigns a misconception family, OR
- confidence is low and labelers disagree on boundary cases.

### Step 3 — Adjudication (how gold label is finalized)
Use one of the following methods (pick one and document it):

**A) Third-rater adjudication (recommended)**
- A third rater assigns a label *blind* to prior labels; majority wins.
- If all three differ → adjudicator chooses among:
  - most defensible label per rules, or
  - `UNCLEAR_INSUFFICIENT_EVIDENCE`.

**B) Consensus meeting (acceptable)**
- Two labelers discuss with family cards open.
- If no agreement in ≤2 minutes → assign `UNCLEAR` or escalate to content expert.

### Step 4 — Finalize gold label fields
Store:
- `gold_label_primary`
- `gold_label_secondary` (optional list)
- `gold_label_adjudicated` (boolean)
- `gold_label_method` (e.g., `single_rater`, `third_rater`, `consensus`)
- `gold_label_confidence_final`

## 7) Reliability and quality checks (right-sized)
### v0.1
- Spot check: reviewer examines a random 10–20% sample.
- Record: % of labels confirmed vs revised.

### v1.0
- Compute at least one agreement statistic:
  - percent agreement (minimum), and optionally
  - Cohen’s kappa (2 raters) or Krippendorff’s alpha (multiple raters).
- Report agreement overall and for high-frequency families.
- If agreement is low for a family:
  - revise that family card (tighten inclusion/exclusion),
  - re-label affected items, and
  - note the change in the changelog.

## 8) Handling edge cases (rules reviewers expect)

### Mixed responses
If a response includes multiple misconceptions:
- choose the **dominant** misconception as primary,
- store others as secondary, OR
- if truly inseparable, use `UNCLEAR` with notes.

### Vague / minimal responses
If the response is too short to infer understanding:
- label `UNCLEAR_INSUFFICIENT_EVIDENCE`.

### Off-topic / noisy responses
If response content does not address the prompt:
- label `OFF_TOPIC_NOISY` (even if it contains climate words).

### Near-miss correct responses
If a response is mostly correct but missing a key mechanism:
- label as misconception family only if it matches inclusion rules;
- otherwise use `UNCLEAR` with notes (prevents over-labeling).

## 9) Required dataset fields (minimum)
Each record should include at least:
- `record_id`
- `item_id` / `prompt_id`
- `prompt_text` (or reference)
- `response_text`
- `expression_condition`
- `gold_label_primary`
- `gold_label_secondary` (optional)
- `labeler_role` (or `labeler_ids` in a separate file)
- `gold_label_method`
- `gold_label_adjudicated`
- `benchmark_version`
- `data_origin` (e.g., constructed_exemplar / educator_constructed / authentic_student)
- `usage_restrictions` (e.g., “not for grading/high-stakes”)

## 10) Documentation to publish with each release
For each benchmark release, publish:
- Taxonomy version + family cards
- Label protocol version (this doc)
- A short labeling summary:
  - who labeled (roles, not personal identifiers unless permitted)
  - adjudication method
  - reliability snapshot (for v1.0)
  - known limitations

---

## Appendix A — Minimal “gold label” example fields (JSONL)
```json
{
  "record_id": "CS-000041",
  "item_id": "Q01",
  "expression_condition": "telegraphic_short_form",
  "response_text": "Ozone hole makes Earth hotter.",
  "gold_label_primary": "MF01_ozone_vs_greenhouse",
  "gold_label_secondary": [],
  "gold_label_confidence_final": "high",
  "gold_label_method": "single_rater",
  "gold_label_adjudicated": false,
  "data_origin": "constructed_exemplar",
  "benchmark_version": "0.1",
  "usage_restrictions": "Formative use only; not for grading or high-stakes decisions."
}
```

## Appendix B — Change log pointers
Record all changes to:
- label definitions
- inclusion/exclusion rules
- adjudication rules
in `CHANGELOG.md` and bump the taxonomy version accordingly.
