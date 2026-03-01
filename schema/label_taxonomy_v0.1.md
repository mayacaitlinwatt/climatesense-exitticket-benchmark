# Label Taxonomy v0.1 — ClimateSense Exit-Ticket Benchmark

**Version:** 0.1  
**Scope:** Grades 9–10 | Climate systems & carbon cycling | Short science explanations  
**Status:** Public preview (v0.1 constructed exemplars)

---

## Non-misconception labels (escape valves)

These labels apply when a response does not map to a misconception family.

| Label | When to use |
|---|---|
| `SCIENTIFICALLY_CORRECT` | Response correctly explains the relevant mechanism with no significant error. |
| `UNCLEAR_INSUFFICIENT_EVIDENCE` | Response is too vague, short, or ambiguous to infer understanding. |
| `OFF_TOPIC_NOISY` | Response does not address the prompt, even if it contains climate-related words. |

---

## Misconception families (v0.1)

Each family is assigned a short ID (`MFxx`) and a canonical name.  
For full inclusion/exclusion rules and anchor examples, see the Label Protocol (`docs/GRNT001-ClimateSense-LabelProtocol-v0.1.md`).

| ID | Short name | Plain-language description |
|---|---|---|
| `MF01_ozone_vs_greenhouse` | Ozone / greenhouse conflation | Student confuses ozone layer depletion with the greenhouse effect or global warming. |
| `MF02_heat_trapping_reversal` | Heat-trapping reversal | Student believes CO₂ or greenhouse gases cool the atmosphere rather than trap heat. |
| `MF03_weather_vs_climate` | Weather / climate conflation | Student uses short-term weather events as direct evidence for or against climate change. |
| `MF04_carbon_disappears` | Carbon disappears | Student believes carbon (CO₂) simply disappears or is destroyed rather than cycling through reservoirs. |
| `MF05_sun_primary_cause` | Sun as primary cause | Student attributes current warming primarily to increased solar output rather than anthropogenic GHGs. |
| `MF06_natural_cycles_only` | Natural cycles only | Student acknowledges climate change but attributes it solely to natural cycles, dismissing human contribution. |

> **Note:** v0.1 includes 6 misconception families as proof-of-concept. v1.0 will expand and validate the taxonomy with educator input and reliability testing.

---

## Versioning

Changes to label definitions, inclusion/exclusion rules, or the family list must:
1. Bump the taxonomy version (e.g., v0.1 → v0.2)
2. Be logged in `CHANGELOG.md`
3. Trigger re-labeling of affected records

---

## License
CC BY 4.0 — People's Evidence Lab, 2026.
