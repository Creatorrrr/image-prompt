# Camera evidence structure: staged implementation and acceptance

Baseline: origin/main `8a0fb5b8dd30d70bc9dbae7f63fbce38daa3bbfc`.
Branch: `codex/camera-evidence-structure-20261003`. Provider/render calls: none.
Requested effort: high; the environment exposes no model/effort settings API.

## 1. New-author handoff, using existing contracts

Keep core v3, property anchors v2 and semantic assertion wire shapes. Introduce an
opt-in camera authoring declaration in an existing camera assertion: a capture-owner
role, separate requested/open/excluded decisions for direction and height, and
literal owner/direction/height evidence. Required axes must correspond to existing
camera property anchors (or an already justified whole-camera lock); the assertion
cannot substitute for or weaken those locks. Use advisory polarity on a partially
open camera dimension and required polarity only when camera is already fully locked.

A new-author CLI mode requires the declaration before candidate data loads. Marked
declarations are validated even outside that CLI mode. Existing frozen cores without
it remain valid. Validate axis completeness as explicitly reviewed by the author,
source/target/anchor linkage and literal evidence; do not claim code understands all
request meanings or proves the declared owner is correct. Never add an incidental
camera requirement merely to fill the declaration.

Use owner plus the relevant axis evidence for a slot, avoiding unrelated axes or
background prose. Existing unmarked typed evidence retains its historical behavior.
Evaluate complete author-written envelope/core/control/review inputs through the
public CLI; no fixture helper may infer their subject, event, anchors, locks or prose.
Technical hashing is separate from authored semantics. Test missing declarations,
missing axes, stale/nonliteral evidence, wrong target/anchor linkage, and exclusion.

## 2. Minimal bounded legacy clause projection

Separate capture-owner noun phrase, camera/lens predicate, same-owner coordination
and local negation. Support composable direct and reduced-relative owner phrases,
copular/passive direction and locative height, and a lens reference only when its
single owner is explicit in the same sentence. Preserve literal spans; do not
translate, complete prose or rewrite frozen cores. Do not borrow another actor's
orientation or convert low height into upward direction. Keep depicted-camera,
multiple-camera, ambiguous ownership and exclusion guards conservative.

Use a small local grammar, not a general dependency parser or a growing list of
fixture-specific sentences. No new dependency or model. Preserve current simple
clause output where possible. Stop at unrelated actors/clauses and abstain when
polarity or attachment is unresolved. If complexity cannot remain bounded, narrow
the supported grammar and document misses rather than weaken controls.

## 3. Evaluation gates

- Prior V1 and V2 stay unchanged, with first-pass and post-seen reports preserved.
  V2 is now a development control, never a new blind holdout. Its original 0/6
  positive and 8/8 negative results, including KO_TWO's core rejection, remain.
- Freeze source before obtaining new independent EN/KO requests with English
  baselines. Ask parent for fresh authors then; they must not see implementation,
  old cases or candidate data. Include complete independently authored inputs for
  the new-author path, plus separate prose-only legacy probes.
- Cover up/down, low-horizontal, direct/indirect owners, object/subject directions,
  background cameras, multiple-camera ambiguity and local negation. Require no
  new wrongly attributed/negated positive projections in negative controls and a
  measured positive recall gain; do not tune on the final unseen set.
- Report separately: raw owner/axis extraction, literal query forwarding, correct
  candidate exposure, formal compatibility and optional adoption. A schema pass or
  candidate exposure is not semantic ownership, final adoption or pixel quality.
- Compare before/after on identical production load_runtime_data and quality layers.
  Preserve all 24 frozen original/corrected input/core hashes, 64 candidate ceiling,
  optional adoption, public shuffle, unknown-effect rejection and zero-adoption
  baseline audits. Investigate exposure changes beyond the intended slots.
- Run focused authoring/parser/core/isolation regressions, dictionary/index checks
  and complete feasible isolated unittest discovery on final source. Reproduce any
  failures on the fresh baseline rather than assuming historical assets are absent.
- Preserve all historical evidence, boundaries and vectors. No reembedding unless
  changed embedding inputs actually require it (not anticipated for this delta).

## 4. Publication

Push a separate branch/draft PR with concrete evidence. Coordinate the final main
publication window with parent, fetch/merge current main, verify source and DATA
identity or rerun affected checks, then complete the already authorized normal
merge/push. Verify remote SHA and PR merged state; never force-push. The prior DATA
loop ended at 13:52:49 UTC and this request does not restart it.

## Limits and stop conditions

Positive legacy recall alone cannot justify negative-control ownership leakage.
Incorrect but syntactically valid author declarations need independent semantic
review. Related unknown candidate property effects remain incompatible under locks.
Report final holdout misses and admission failures without rewriting expectations.
No text/contract result is evidence of improved rendering quality.
