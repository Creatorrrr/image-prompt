# Conditional attachment relations and retired control candidates

The base dictionary stored 21 `safety_profile` entries and 12
`costume_absorption_guard` entries without usable visual ownership. Giving both
slots ownership indiscriminately would activate control prose that could replace
requested clothing, anatomy, framing, or actions.

The stage-2 change reviews all 33 original entries. It retires 28 control
directives from the live candidate corpus and moves five observable attachment
relations into the existing `anatomical_connection` slot. The original entry IDs
and weights are retained. The five relations describe headpiece/horn roots,
hood trim/living ear attachment, decorative/living feather attachment,
rabbit-ear headband/living ears, and stitched lace/living fur boundaries.

Each moved entry has positive semantic text, two relation endpoints, declared
property effects, and primary-context alternatives requiring both requested
carriers. Candidate adoption remains optional. Ordinary costume requests do not
gain these living-anatomy relations. The forced helmet removal/pushback/cutaway
directive and anti-selfie, costume-suppression, and role-control entries are
retired. There is no new suppression or default styling rule.

`tests/fixtures/photo_prompt/slot_guard_roles_v1/ROLE-DECISIONS.json` retains every
original entry, canonical SHA-256, decision, reason, and destination entry. It is
test/evidence data, outside the runtime source registry. Historical death
research references resolve against this preserved archive without reactivating
retired controls. Existing subject/action/mechanism/render data is preserved.

The semantic index is rebuilt from the scoped authored sources. On the
publication base, the corpus has 112 slots and 12,008 semantic documents;
12,003 existing documents are retained, 33 old slot keys are removed, and five
new slot keys reuse the already verified stage-2 embeddings. The visual index
remains at 3,791 profiles. Provider/model/dimensions/full-text/identity checks
qualify vector reuse; the canonical builder regenerates BM25F.

The frozen maintenance fixtures contain six positive and eight negative cases,
including Korean and English requests, property-locked wardrobe, a closed
helmet, and a royal mirror selfie. The role tests check control provenance,
positive/negative retrieval, frozen core preservation, candidate-tag isolation,
property locks, context recomputation, and positive relation text. Related death,
positive-retrieval, candidate-semantics, occasion, core, and pre-core-isolation
tests cover adjacent contracts. The existing 20 natural-language fixtures cover
seven occasion scenes and thirteen unrelated scenes.

On the scoped publication checkout, all 55 focused tests pass. The real public
CLI/view/source-recomputation pipeline passes all 14 role cases (six expected
relations and eight negatives) and all 20 existing natural-language cases.
Frozen core hashes remain unchanged and candidate omission is detected.

Reproduce the focused tests from the repository root:

```sh
.venv/bin/python -m unittest \
  tests.test_photo_slot_guard_roles \
  tests.test_photo_death_afterlife_semantics \
  tests.test_photo_positive_retrieval \
  tests.test_photo_candidate_semantics \
  tests.test_photo_occasion_context_retrieval \
  tests.test_photo_core_retrieval \
  tests.test_photo_prepack_isolation
```

These are authored maintenance cases, not a blind generalization benchmark.
Primary-context matching uses the existing lexical resolver. Full owner/context
precision, adult-domain routing, aliases, and ranking remain later stages.
Contract/retrieval validation does not establish native-image pixel quality.
