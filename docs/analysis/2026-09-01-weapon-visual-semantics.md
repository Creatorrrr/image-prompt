# Weapon visual-semantics strengthening — 2026-09-01

## Scope and evidence boundary

This change translates the broad weapon vocabulary collected in the referenced conversation into six narrow, still-image-testable morphology contracts. It does **not** treat a name, costume, genre, or nearby object as sufficient proof. It also does not infer operability, legal status, sharpness, ammunition state, capability, intent, handling quality, or historical authenticity from pixels.

The supplied portrait is limited to appearance reference for an unmistakably adult fictional subject in the five render evaluations. It is not evidence of identity, personality, occupation, weapon familiarity, protected traits, or same-person status.

## Selected profiles and diagnostic pixels

| Profile | Required visible component relation | Primary confusion boundary |
|---|---|---|
| `rapier_acute_point_elaborate_guard` | long slender straight double-edged blade, acute point, elaborate hand-enclosing guard, one-hand grip and pommel on one axis | broad greatsword, short smallsword, plain cruciform sword, cropped point |
| `halberd_axe_point_rear_spike` | one continuous shaft plus lateral axe blade, apical spear point, rear beak or spike | spear, glaive, poleaxe, oversized fantasy axe |
| `compound_bow_cam_cable_system` | central riser, split limbs, two limb-tip cams, separate bowstring and cable paths | recurve bow, longbow, crossbow, cropped single-cam bow |
| `crossbow_stock_prod_release_system` | longitudinal stock and bolt track joined to transverse prod, spanning string, and release mechanism | ordinary vertical bow, rifle without prod, detached bow-and-stock collage |
| `revolver_chambered_cylinder_system` | multi-chamber cylinder inside frame, barrel aligned to one chamber, grip and trigger guard | semi-automatic pistol slide, generic cylinderless handgun, floating cylinder |
| `ground_mortar_tube_bipod_baseplate_system` | elevated tube seated on ground-contacting baseplate and braced by connected bipod with sight or adjustment hardware | kitchen mortar and pestle, wheeled cannon, shoulder launcher, unsupported tube |

Each profile has five component groups, five evidence fields, five thumbnail/native pixel gates, and at least five explicit reject substitutes. Exact multilingual terms can create hard obligations; broad related terms remain non-activating. Semantic retrieval may propose an optional concept only when the component evidence is present.

## Candidate-pack changes

The candidate pack adds a diagnostic prop/action pair for every profile and narrows legacy aliases that previously collapsed adjacent classes. In particular:

- `greatsword` and `broadsword` no longer alias a longsword candidate.
- `glaive`, `poleaxe`, and generic `polearm` no longer alias a halberd candidate.
- `recurve bow` and `longbow` no longer alias the generic training-bow candidate.
- generic Korean `활` no longer aliases the crossbow candidate.
- `pistol`, `handgun`, Korean `권총`, and generic `총` no longer alias the revolver candidate.
- `assault rifle` and `automatic rifle` no longer alias the generic modern-rifle display candidate.
- legacy public text now describes external reference morphology without asserting operability, deactivation, sharpness, or safety.

Generic hand/object ownership remains governed by the existing `photo-request-lineage/v2` and `photo-render-repair/v1` contracts. The six weapon profiles own subtype morphology only, so a successful object shape cannot hide a failed hand contact and a successful contact cannot hide the wrong weapon class.

## Research basis

- The Metropolitan Museum of Art identifies the rapier by its double-edged acute-point blade and elaborate hand guard: <https://www.metmuseum.org/art/collection/search/24677>
- The Met describes canonical halberd development as an axe blade combined with a spear point above and a spike behind: <https://www.metmuseum.org/art/collection/search/845840>
- World Archery separates compound and recurve equipment and identifies the compound bow's pulley-and-cable system: <https://www.worldarchery.sport/sport/equipment>
- The Met's multi-view crossbow record supplies an official museum morphology reference and preserves the object's transverse-to-longitudinal proportions: <https://www.metmuseum.org/art/collection/search/24924>
- ATF's basic firearm-type boundary distinguishes a revolver by its breechloading chambered cylinder: <https://www.atf.gov/firearms/tools-services-law-enforcement/national-tracing-center/properly-identify-a-firearm-purpose-tracing>
- The U.S. Army's documented 120 mm ground configuration enumerates the tube, bipod, baseplate, and sight unit as one system: <https://www.cpeae.army.mil/Project-Offices/PM-CAS/Organizations/Precision-Fires-Mortars/Products/120MM-MORTAR-SYSTEMS/>
- CVPR 2020 hand-contact research separates hand location, side, contact state, and contacted-object region, supporting independent contact evaluation: <https://openaccess.thecvf.com/content_CVPR_2020/html/Shan_Understanding_Human_Hands_in_Contact_at_Internet_Scale_CVPR_2020_paper.html>

The machine-readable provenance, limitations, reuse notes, candidate IDs, and affected contracts live in `docs/research-evidence/photo-prompt/research_evidence.jsonl`.

## Qualification rule

Static validation, prompt audit, render-request audit, and pixel review are separate evidence layers. A render passes a profile only when all five hard pixel gates pass at their specified review scales and the existing hand/object ownership gate passes when a person is shown interacting with the object. Partial visibility is failure. User aesthetic acceptance remains a separate final judgment.
