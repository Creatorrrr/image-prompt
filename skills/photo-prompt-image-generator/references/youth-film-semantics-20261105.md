# Youth-film visual semantics — staged source

The 2026-11-05 research draft adds 29 authored optional bilingual visual
realizations and 14 context-only diagnostics in
`assets/photo_youth_film_semantics_20261105.json`,
`assets/photo_candidate_youth_film_20261105.json`, and
`assets/photo_candidate_youth_film_bindings_20261105.json` (29 optional role
bindings). Existing school, campus and music sources should be checked for
full-meaning reuse before adoption; a similar label does not establish
semantic equivalence. The research and candidate geometry are authorial
proposals, not documented shots from the cited films.

Installed H-F2 release `6a2bf89579bce9910a4ea7b22d338853c7c6a2ecfaf670a3cf9bddf053de0dcd`
passed its integrity checks and was selected with canonical snapshots of these 43 records: 29 positive search candidates
and 14 diagnostics excluded from positive retrieval. It retains the prior
release's selection policy and reviewed views, and adds 29 whole-source and
29 source-grounded context views. Their authored source is
`assets/photo_candidate_retrieval_views_youth_film_20261105.json`. The working
source manifest registers the candidate and slot-binding modules; it is separate
from the sealed installed release and does not itself rebuild or activate it.
A later selected release may preserve or
replace its contents; consult `retrieval-runtime.json` and verify that release
rather than assuming the selection is permanent.

An actual 46-query development diagnostic found 19 new candidates in the raw
top 32 for `청춘영화` and 8 for `coming-of-age film scene`; neither query had a
new candidate ranked first. The 26 source-grounded paraphrase probes returned
their intended candidate first, but were not an independent holdout. All 10
contrast probes returned a conflicting source in the raw top two and nine
displayed it. Six unrelated probes retained their old top three; this limited
check does not establish absence of other regressions. In three independent
image tests, new youth candidates were retrieved but none was adopted; all
three final prompts used existing sources as inspiration instead. These results
do not establish that a newly added candidate was realized in pixels.

Search rank or exposure is not native qualification,
permission to alter locked requester meaning, prompt transport, pixel proof or
user acceptance. Review each returned source and its conditions before use. Each relation
must preserve its stated owners, counts, support, directed gaze, contact or
gap, garment carrier, and media boundaries. A hidden required endpoint is
unobservable, not a pass. Genre, age, identity, emotion, event history, sound,
consent and causation are not established by a single visual cue.

For a request that actually names `청춘영화`, scope that literal visual intent
separately from words describing research or workflow; retain other words when
they are themselves part of the requested scene. Use the independent baseline
and the full applicable-slot plan to search for concrete scene, person, object,
action and composition details. Neither a genre-only match nor a high rank
proves that a returned option meets a negative condition, a person count or an
owner-specific guard. Do not add a condition to the request or infer one from
the genre in order to make a candidate applicable.

The research, candidate proposal inventory, limitations and test planning are
recorded in `docs/research-evidence/photo-prompt/youth-film-20261105/`. That
directory is locally ignored by Git; it is not proof that the staged files
have been deployed.

Independent review found and corrected bilingual location/contact differences,
ambiguous aliases and missing stated adult context. Further review is needed:
`requires_adult_context` does not itself prove that each separately identified
person is adult, and the installed guard may reject explicitly nonsexual adult
contexts. Do not infer age from pixels or treat that boolean as individual-owner
proof. Candidate conditions and every declared effect still require native
owner/permission review. The latest H-F2 release also includes reviewed dense
views and selection state that an ordinary native index build does not reproduce.
