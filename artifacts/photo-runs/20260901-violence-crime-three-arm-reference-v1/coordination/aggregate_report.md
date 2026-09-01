# Violence/crime visual-semantics three-arm result

## Outcome

The runtime data and prompt layer are implemented and structurally valid, but this first strict render qualification is **REVISE**, not promote.

- Package/data: PASS
- Three v6 candidate packs and composed prompts: PASS
- Native generation: two successes, one model-safety input block
- Full pixel qualification under `partial_is_fail`: zero pass, two fail, one blocked
- Assigned-profile pixels among the two rendered arms: arson 4/4 PASS; robbery 3/4 FAIL
- User aesthetic judgment: unscored

The supplied portrait was used only for visible adult appearance in a fictional supporting role. It was never assigned to an offender, victim, or minor, and no identity or same-person claim is made.

## Data applied

- 20 relation-first visual-obligation profiles were added for credible threat, assault, robbery, abduction, hostage-taking, fictional intentional homicide, fictional organized crime, arson, burglary, revenge violence, forensic scene documentation, bloodstain documentation, custodial torture, genocide, war crime, controlled execution, adult nonconsensual sexual violence, declared-minor targeted crime, adult human trafficking, and terrorism.
- Each profile has four independent observable component groups, four literal prompt-evidence fields, four pixel gates, and nearest-substitute rejects. The declared-minor test adds an explicit non-appearance age declaration and reference-role boundary.
- 66 candidate records were added as 11 coherent clusters across six slots: `aesthetic_trend`, `subject`, `action`, `location`, `prop`, and `composition`.
- Broad mood, genre, and field labels remain advisory. Narrow exact meanings create hard visual duties only when their local context is present.
- No violence-specific safety profile, moderation tier, or automatic safety-negative contract was added. Image-model safety remains external to this skill data.
- Generated indexes contain 225 visual profiles / 1,220 exact terms and 7,674 semantic entries.

## Frozen random assignment

Seed `695725796` selected one profile from each of three disjoint predeclared family pools:

| Arm | Assigned profile | Independent complex fictional concept |
|---|---|---|
| 01 | `robbery_forced_property_transfer` | Near-future glass observatory tram station, violent sleet, rare-map courier, stranded commuters, red leather case, brass chronometer, 28 mm frame, sodium and signal lighting |
| 02 | `deliberate_arson_causality` | Early-1990s evidence photograph, shuttered riverfront botanical greenhouse, freezing rain, blue service door, lit path and same-point fire origin |
| 03 | `declared_minor_targeted_crime_relation` | Late-1990s civic reconstruction, underground botanical ferry concourse, explicitly fictional sixteen-year-old victim, nonsexual unlawful-confinement attempt, adult safety-officer intervention |

Each arm froze its authorial core and rubric before candidate-pack retrieval, used no sibling-arm prompt or image, made exactly one native generation call, and performed no retry.

## Strict results

| Arm | Prompt | Tool | Assigned-profile gates | Coordinator common gates | Final |
|---|---:|---:|---:|---:|---:|
| 01 robbery | PASS | success | 3/4 | 3/5 | **FAIL** |
| 02 arson | PASS | success | 4/4 | 4/5 | **FAIL** |
| 03 minor-targeted crime | PASS | input moderation block | 0 pixel gates scored | 0 pixel gates scored | **BLOCKED** |

### Arm 01 — robbery

The image clearly preserves distinct adult roles, a directed crowbar threat, and the courier's initial possession of the red case. It fails the defining result: the offender merely points toward or lightly touches the case and does not visibly grip and pull it into offender control. Because the transfer relation is absent at native scale, both thumbnail and native relation-readability gates also fail.

### Arm 02 — arson

The image shows all four assigned arson relations: actor and target, a continuous ignition path, fire beginning at the same contact point, and flame/scorch growth from that point. The full arm still fails because the reference-guided investigator dominates the foreground instead of remaining a secondary supporting role.

The arm's frozen rubric omitted the coordinator's fifth common `clean_delivery` gate. Root review scored that gate PASS from the saved pixels but records the precommit omission as a test-harness deviation; the frozen arm artifact was not rewritten after seeing the image.

### Arm 03 — declared-minor targeted crime

The v6 pack, prompt, and exact render request all passed audit. The one native image call was blocked at input moderation (`moderation_blocked`, request `e5aedd7d-c213-4e05-9b5d-c1943eee7cb7`). No native image or thumbnail exists, so this arm is BLOCKED and nine pixel gates remain unscored. The block is not converted to a zero or a pixel failure.

## Interpretation and next revision target

This sample establishes that the new arson causality profile can survive a complex single image, while the robbery transfer result needs stronger visible grip, counterforce, and directional displacement. Reference-guided supporting roles also need a firmer scale/placement instruction so appearance continuity cannot take over the frame. The declared-minor profile remains unqualified because the image model produced no pixels.

The bounded evidence does not claim that all 20 added profiles render successfully. It demonstrates structural and prompt behavior across all new data, plus pixel evidence for two randomly selected profiles and a generation outcome for a third. Any next render iteration should repair only the failed visible dimensions and retain one frozen, independent render per arm.

## Evidence files

- `coordination/root_independent_pixel_review.json`
- `coordination/random_assignment.json`
- `coordination/source_snapshot.json`
- `coordination/test_plan.md`
- `arm-01-robbery/arm_report.md`
- `arm-02-arson/arm_report.md`
- `arm-03-minor-crime/arm_report.md`
