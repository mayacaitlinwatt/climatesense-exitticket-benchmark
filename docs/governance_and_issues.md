# Governance and Issues — ClimateSense v0.1

## ⚠️ Important: Not for grading

The ClimateSense benchmark is designed exclusively for **formative, instructional purposes**. It must not be used for:
- Grading students
- High-stakes assessment decisions
- Evaluating individual student performance for accountability purposes
- Any use that would expose students to consequences based on AI output

---

## How to file an issue

Use the [Issues tab](../../issues) with the appropriate template:

| Template | When to use |
|---|---|
| **Bug report** | The harness produces incorrect output, crashes, or behaves unexpectedly |
| **Feature request** | You want to suggest an improvement to the harness, schema, or docs |
| **New misconception family** | You have evidence for a misconception pattern not covered by the current taxonomy |

Please include as much detail as possible. For harness bugs, include your Python version, the command you ran, and the error output.

---

## Versioning policy

ClimateSense uses a two-part version scheme: `major.minor` (e.g., `0.1`, `1.0`).

| Change type | Version bump |
|---|---|
| New data, new families, schema changes | Minor (e.g., 0.1 → 0.2) |
| Breaking schema changes, full revalidation | Major (e.g., 0.x → 1.0) |
| Bug fixes, doc corrections | Patch noted in CHANGELOG, no version bump |

All changes are logged in `CHANGELOG.md`. Taxonomy changes additionally require re-labeling affected records and bumping the taxonomy version.

---

## Data and label governance

- Gold labels are assigned using the Label Protocol (`docs/GRNT001-ClimateSense-LabelProtocol-v0.1.md`).
- Any changes to label definitions or inclusion/exclusion rules are treated as breaking changes and versioned accordingly.
- v0.1 data are **constructed exemplars**. Authentic student data, if introduced in future versions, will be governed under separate data use and privacy agreements.

---

## Contact

Maintainer: Steve Watt — **stevewatt13@peoplesevidencelab.com**  
Organization: [People's Evidence Lab](https://github.com/PeoplesEvidenceLab)
