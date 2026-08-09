# Illustration prompt audit mistook a generic subject phrase for a named style

- Recorded: 2026-08-09 02:27 KST
- Status: resolved
- Goal/checkpoint: Research-Backed Subculture Illustration and Artwork Grammar / Stage 5 render qualification
- Affected scope: `subculture-illustration-image-generator/scripts/audit_composed_prompt.py`
- Search terms: named style false positive, illustration of an adult, render qualification
- Related paths: `skills/subculture-illustration-image-generator/scripts/audit_composed_prompt.py`, `tests/test_subculture_illustration_contract_v1.py`
- Resolved by: `docs/passed-reports/2026-08-09-subculture-illustration-authorial-grammar.md`

## Failure

- Conditions or trigger: Audit a clean card prompt containing the ordinary subject phrase `Illustration of an adult artifact restorer`.
- Expected: Generic subject descriptions pass while explicit artist, studio, protected work, and named-style imitation references fail.
- Observed: The named-style pattern combined an uppercase-token expression with a globally case-insensitive search. It therefore interpreted lowercase `an` as a possible proper name and rejected the prompt.
- Impact on the goal: A valid original illustration prompt could be rejected, encouraging composers to evade the guard through arbitrary wording instead of enforcing the intended reference boundary.

## Evidence

- Sanitized artifact: Stage 5 case 4 pre-render `audit.json`.
- Result: `named_style_reference` failure with excerpt `illustration of an`; no artist, studio, work, or franchise was present.

## Cause assessment

- Confirmed cause: The proper-name branch was evaluated with `re.IGNORECASE`, making its `[A-Z]` boundary ineffective; `illustration of` is also a subject-description construction rather than reliable style-imitation evidence.
- Confidence: confirmed.

## Resolution or next safe step

- Resolved: 2026-08-09 02:30 KST.
- Resolution/workaround: Removed `illustration of` from the imitation construction and made the remaining proper-name span explicitly case-sensitive while preserving the surrounding case-insensitive guard. Composer rewording is no longer the product fix.
- Verification: A focused regression accepts `Original illustration of an adult artifact restorer` and still rejects `the art of Hayao Miyazaki`; the 24 stored prompt qualifications recompute cleanly under the updated auditor, and the integrated asset validator passes.

## Reuse guidance

- Avoid: using title-case syntax as a proper-name detector under a globally case-insensitive search.
- Prefer: high-confidence imitation constructions plus a case-sensitive proper-name span, with a regression for ordinary `illustration of an adult` wording.
- Applicable when: prompt guards distinguish named creators or styles from generic subjects.
- Re-check when: adding multilingual named-style detection or changing prompt normalization.
