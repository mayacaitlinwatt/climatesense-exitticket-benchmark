---
ArtifactID: "GRNT001-TU-2026-001-ClimateSense-TeacherUsefulnessRubric-v0.1"
Title: "ClimateSense — Teacher Usefulness Rubric v0.1"
Date: "2026-02-28"
Version: "0.1"
Maintainer: "Steve Watt (People’s Evidence Lab)"
ArtifactType: "Rubric"
Project: "GRNT001 ClimateSense Exit-Ticket Benchmark"
Scope:
  GradeBand: "9–10"
  Domain: "Climate systems & carbon cycling (short science explanations)"
License: "CC BY 4.0 (recommended for documentation)"
Tags:
  - "#GRNT001"
  - "#ClimateSense"
  - "#teacher_usefulness"
  - "#formative_assessment"
  - "#rubric"
  - "#benchmark"
Evidence_Backbone:
  - "Black & Wiliam (1998) — formative assessment improves learning when evidence is used to adapt teaching"
  - "Hattie & Timperley (2007) — feedback answers: Where am I going? How am I going? Where to next?"
  - "Shute (2008) — formative feedback should be specific, credible, and designed to improve learning"
---

## 🧭 Provenance Summary
This rubric operationalizes “teacher usefulness” for AI-generated feedback in formative assessment. It is intentionally lightweight (0–3 scale) to support Track 1 proof-of-concept work while remaining grounded in widely cited formative assessment and feedback frameworks.

# ClimateSense — Teacher Usefulness Rubric v0.1

## 1) Purpose
This rubric rates whether an AI system’s feedback is **useful to a teacher** for formative assessment—i.e., it supports understanding, next instructional steps, and safe classroom use.

This is **not** a general writing-quality rubric. It is purpose-built for GRNT001’s goal: making “teacher usefulness” a measurable attribute of AI-assisted exit-ticket analysis.

## 2) What is being rated
For each student response, the AI may produce:
- `feedback_text` (diagnosis + explanation)
- `next_step_text` (a recommended teacher move)

Teachers rate these outputs using the dimensions below.

## 3) Scoring scale (0–3)
Use the same scale for each core dimension:

- **0 — Not usable / harmful**  
  Incorrect, misleading, unsafe, or unusable under real classroom constraints.

- **1 — Weak**  
  Some useful signal, but vague, incomplete, unclear, or hard to act on.

- **2 — Good**  
  Clear and mostly correct; actionable with minor gaps.

- **3 — Excellent**  
  Clear, correct, and directly supports a high-quality next instructional move.

## 4) Core dimensions (scored 0–3)

### A) Correctness / Diagnostic validity
**Question:** Is the feedback scientifically and instructionally correct for the prompt and misconception family?  
- 0: Incorrect diagnosis or fabricated claims; likely to mis-teach.
- 1: Partly correct but important errors/omissions.
- 2: Correct with minor caveats.
- 3: Clearly correct and appropriately scoped.

### B) Clarity (teacher-time reality)
**Question:** Is it understandable quickly and without jargon?  
- 0: Confusing, verbose, or unclear.
- 1: Some clarity but requires interpretation.
- 2: Clear and concise; minimal ambiguity.
- 3: Immediately clear; teacher can act with confidence.

### C) Actionability (“Where to next?” / feed-forward)
**Question:** Does it propose a concrete next step a teacher can use now?  
- 0: No next step or impractical/unhelpful step.
- 1: Generic guidance (e.g., “review the concept”) with no concrete move.
- 2: Specific next step (question/activity/check) that is feasible.
- 3: Specific, feasible, and well-matched to the diagnosed misconception.

### D) Instructional alignment (formative, not punitive)
**Question:** Is it aligned with formative assessment (supports learning, not grading/punishment)?  
- 0: Punitive, grade-like, or misaligned with learning goals.
- 1: Somewhat aligned, but unclear intent or tone.
- 2: Aligned; supports instructional adaptation.
- 3: Strongly aligned; supports growth and learning progression.

## 5) Safety flags (binary; record separately)
Record these as Y/N (or 1/0). These are not averaged into the composite score.

- **Hallucination / fabrication flag:** Does the AI introduce made-up facts or content not supported by the student response/prompt?
- **Unsafe / inappropriate recommendation flag:** Does the AI recommend something unsafe, inappropriate, or clearly misaligned to classroom context?

## 6) Optional adoption signal item (recommended)
### E) “Would you use this?”
**Question:** Would you use this feedback in your classroom *as written*? (0–3)  
This single item can be reported separately as an adoption-facing signal of perceived usefulness.

## 7) Suggested aggregation (for reporting)
For each model/run:
- Compute **Teacher Usefulness Composite** = average(A–D).
- Report mean and distribution overall and by:
  - misconception family
  - expression condition (robustness lens)
  - prompt

Also report the rate of:
- hallucination flags
- unsafe flags

## 8) Reliability (right-sized for Track 1)
- v0.1: 3–6 educators rate a small subset; report simple agreement summaries.
- v1.0+: add inter-rater agreement (e.g., percent agreement; kappa/alpha if appropriate) and refine anchor examples.
