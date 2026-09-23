"""Compile the researched photographic elements into optional runtime data.

Research sources and coverage stay in docs. Runtime entries contain only
observable scene relations. Broad authenticity and RAW claims are not profiles.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(value: dict) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


# One candidate per visible proposal. A four-part contract is added only where
# the existing registry lacks that specific owner relationship.
# id | slot | affected dimension | scene-neutral expression | four owner-bound components
SPEC = """
environmental_portrait_subject_place|composition|composition|Keep the adult subject, the functional place, and the ongoing task legible in one environmental frame.|the adult subject remains identifiable at environmental portrait scale;the place has visible task-specific fixtures or objects;the subject's action or position connects to those fixtures;the frame retains enough surrounding space to explain the task
observed_action_trace|relational_action|action|Show the actor, the object of the action, and a small visible consequence in the same frame.|the actor's specific hand or body action is visible;the action's target object is visible in the same frame;contact or the approach path is spatially possible;the action leaves a small visible result or immediate state change
camera_distance_subject_scale|shot_scale|framing|Set camera distance so the requested body coverage and surrounding space share one coherent perspective.|the requested body coverage is visible;head and body scale follow one perspective;nearby structures scale coherently with camera distance;the requested environmental margin remains around the subject
focus_plane_subject_falloff|focus|camera|Keep the task-bearing subject details readable while foreground and background soften according to distance.|the specified subject detail is the clearest plane;near and far objects soften according to their distances;subject edges transition naturally into the background;the important action target remains readable
scene_owned_exposure_tradeoff|lighting|lighting|Expose the indoor subject for readable detail while retaining a spatially credible brighter window and a limited highlight loss.|the indoor subject retains needed readable detail;window and room brightness differ consistently across space;only a small high-luminance window region loses detail;the interior retains tonal depth rather than uniform HDR brightness
skin_detail_lighting_scale|skin_finish|appearance|At portrait scale, preserve gentle skin tone changes and lighting-shaped detail without imposing blemishes.|the adult face or hand is large enough to inspect;lit skin shows gentle tone and fine texture differences;skin shadows and highlights follow the visible form;eyes lips and skin remain distinct instead of one plastic surface
hair_strand_owner_and_cause|hair_style|appearance|Keep a few flyaway hairs attached to the hairline, with their direction explained by the scene's motion or air.|flyaway strands connect to the hairline or tie point;local strands agree with the main hair direction;their movement agrees with the stated breeze dampness or action;hair and facial contours remain separate without penetration
fabric_tension_fold_attachment|garment_detail|appearance|Let garment folds start at visible seams, joints, or a pulling hand and follow the fabric's actual movement.|the garment's fabric texture or sheen is distinguishable;folds originate at a seam joint or pulling contact;fold direction agrees with the body's action or pose;folds preserve the garment silhouette and closure
surface_wear_contact_owner|texture|material|Confine the chosen wear or handling trace to the material and contact point that could produce it.|the base material has its own reflection or roughness response;the selected wear or trace sits at a reachable contact point;trace strength fits the scene's use and cleanliness;underlying edges and reflections remain coherent beneath the trace
object_contact_shadow_support|contact_point|relationship|Seat the object on a visible support with a small contact shadow and scene-consistent falloff.|the object and its supporting surface are both visible;local darkening or compression touches the load-bearing point;shadow direction and softness agree with the scene light;object shape and support contact align without a gap
reflection_scene_binding|reflection_logic|composition|Bind the selected reflection to a visible surface, matching source object, and camera viewpoint.|the reflecting surface has a visible position and angle;only a source object in the scene appears at the corresponding reflection position;reflection strength and distortion fit the surface and viewpoint;light and shadow geometry remain mutually consistent
casual_crop_subject_legibility|platform_framing|framing|Let a frame edge crop a peripheral moving part while keeping the adult and the main action legible.|one peripheral part meets or exits a plausible frame edge;the adult and task-bearing action remain legible;camera height and tilt match the observer's position;the cropped part continues in a physically possible direction
shadows_local_digital_noise|grain_profile|style|If the selected digital capture is dim, keep fine noise mainly in the shadows while the lit subject stays readable.|bright and shadowed image regions differ in visible noise;fine luminance or chroma noise concentrates in darker regions;critical subject edges and face remain readable;the noise resembles digital processing rather than scratches or print dust
jpeg_edge_blocking|format|format|For an explicitly reposted compressed image, keep mild compression near high-contrast edges without obscuring the action.|a file screen or repost context is explicit;slight ringing or blocking sits near high-contrast edges;flat tone areas remain distinct from edge damage;compression does not conceal the main gesture
film_grain_print_scan_scope|film_emulation|style|Keep restrained grain inside the picture area and any scan dust on the separate print surface.|grain belongs to the photographic picture area;grain varies with tone without hiding face or material structure;any specks remain on the print or scan layer;the look does not imply an actual film capture history
instant_print_material_object|prop||Show a complete instant print as a physical card with an image window, border, thickness, and supported contact.|the image window and card border have a clear boundary;card thickness edges and hand support are visible;photographic color and tone remain inside the image window;the card casts a contact shadow consistent with its position
fixed_surveillance_observation|camera_height|camera|Use a stationary high viewpoint that covers the monitored passage, with the passing adult occupying a small part.|a high fixed installation viewpoint is spatially readable;the monitored entrance or passage occupies a broad view;the moving subject occupies a limited portion of the frame;image limitations remain consistent with the scene without exaggerated damage
camcorder_still_temporal_container|medium|style|Present one camcorder video frame at a legible action phase with only local motion smear and coherent frame treatment.|a single video-frame container or cue is visible;the actor or moving object is caught in one action phase;motion trace is local to moving parts;frame format tone and resolution form a coherent video image
atmospheric_distance_contrast|ambient_particle|atmosphere|Keep near forms detailed and let distant forms lose some contrast only along the actual long viewing path.|multiple near middle and far depth references are visible;far objects have lower contrast than near objects;the atmospheric effect agrees with weather and light;near material detail remains as readable as requested
"""

REUSE = {
    "camera_distance_subject_scale": ["wide_angle_near_field_perspective", "telephoto_distance_compression_relation"],
    "focus_plane_subject_falloff": ["shallow_depth_focus_falloff_relation"],
    "skin_detail_lighting_scale": ["sheer_complexion_texture_preservation", "glass_skin_specular_diffuse_balance"],
    "reflection_scene_binding": ["wet_surface_light_reflection_owner_relation", "mirror_selfie_reflection_device_topology"],
}
OPTIONAL_ONLY = {"shadows_local_digital_noise", "jpeg_edge_blocking", "film_grain_print_scan_scope"}
CUES = {
    "environmental_portrait_subject_place": "environmental portrait;working room;task-specific setting",
    "observed_action_trace": "visible hand action;hand meets object;immediate action result;object placement",
    "camera_distance_subject_scale": "medium camera distance;natural subject scale;environmental margin",
    "focus_plane_subject_falloff": "natural depth of field;readable working hands;near and far focus",
    "scene_owned_exposure_tradeoff": "bright window;dim deeper room;window-room exposure contrast;limited highlight flare",
    "skin_detail_lighting_scale": "realistic skin texture;portrait-scale tonal detail;lit facial texture",
    "hair_strand_owner_and_cause": "wind pushes loose hair;hairline-attached strands;hair moves with the breeze",
    "fabric_tension_fold_attachment": "fine garment creases;sleeve folds;fabric creases at a bent elbow",
    "surface_wear_contact_owner": "localized handling trace;fingerprints at a touched rim;material-specific wear",
    "object_contact_shadow_support": "faint shadow under the object;object fully supported on its surface;local contact shadow",
    "reflection_scene_binding": "wet patch reflects a source;localized wet reflection;reflection aligned to source",
    "casual_crop_subject_legibility": "casual phone framing;peripheral frame crop;readable action despite crop",
    "shadows_local_digital_noise": "fine noise in dim shadows;shadow-local digital noise",
    "jpeg_edge_blocking": "reposted compressed image;mild high-contrast edge blocking",
    "film_grain_print_scan_scope": "restrained film grain;grain inside the picture area;print scan specks",
    "instant_print_material_object": "instant print card;physical print border;card thickness",
    "fixed_surveillance_observation": "fixed high viewpoint;wide monitored passage;small passing subject",
    "camcorder_still_temporal_container": "single camcorder still;one video action phase;local motion trace",
    "atmospheric_distance_contrast": "near foreground detail;distant structure fades;distant lower contrast;weather-consistent haze",
}
SPEC_ROWS = {}
for row in SPEC.strip().splitlines():
    name, slot, dimension, expression, components = row.split("|")
    SPEC_ROWS["pr_" + name] = {
        "slot": slot,
        "dimensions": [dimension] if dimension else [],
        "expression": expression,
        "components": components.split(";"),
    }

proposals = read(HERE / "visual-proposals.json")["proposals"]
profiles = []
slots: dict[str, list[dict]] = {}
coverage = []
for proposal in proposals:
    pid = proposal["id"]
    if pid not in SPEC_ROWS:
        coverage.append({
            "proposal_id": pid,
            "disposition": "research_policy_only",
            "reason": "Capture authenticity or universal imperfection policy is not pixel evidence.",
            "source_ids": proposal["source_ids"],
        })
        continue
    spec = SPEC_ROWS[pid]
    owner = proposal["owner"]
    units = spec["components"]
    stem = pid.removeprefix("pr_")
    cues = CUES[stem].split(";")
    aliases = [proposal["label_ko"], stem.replace("_", " ") + " relation"]
    if stem not in REUSE and stem not in OPTIONAL_ONLY:
        definition = "; ".join(units)
        profile = {
            "id": pid,
            "category": "photographic_scene_relation",
            "activation": {
                "exact_terms": [definition],
                "requires_adult_character": stem not in {"object_contact_shadow_support", "surface_wear_contact_owner", "instant_print_material_object", "atmospheric_distance_contrast"},
                "semantic_discovery_requires_component_evidence": False,
            },
            "semantics": {
                "definition": definition,
                "paraphrase_examples": [spec["expression"], *aliases],
                "visual_components": [*cues, *units],
                "contrast_examples": proposal["near_misses"],
                "claim_limits": [
                    "The named owner and every selected component must be visible in one image.",
                    "Depiction alone does not prove capture history, source authenticity, camera model or actual location.",
                    "A broad photorealism label does not require this relation or any artificial imperfection.",
                ],
            },
            "concept_candidate": {"concept_terms": [*aliases, *cues, *units]},
            "runtime_expression": {
                "default_mode": "definition_with_optional_label",
                "prompt_label_terms": [],
                "forbidden_prompt_terms": [],
                "runtime_forbidden_labels": [],
            },
            "reject_substitutes": proposal["near_misses"],
            "authored_components": {"contract_version": "photo-authored-visual-components/v1", "components": []},
        }
        for index, phrase in enumerate(units, 1):
            profile["authored_components"]["components"].append({
                "id": f"component_{index}",
                "match_terms": [phrase],
                "evidence_field": f"component_{index}_phrase",
                "evidence_terms": [phrase],
                "min_content_words": 3,
                "instruction": f"Show this relation on its selected owner: {phrase}",
                "render_gate": {
                    "id": f"vo_{pid}_{index}",
                    "review_scale": "native" if spec["slot"] in {"hair_style", "garment_detail", "texture", "prop"} else "both",
                    "description": f"{phrase}. Inspect the declared owner; missing, substituted or partly visible evidence fails.",
                },
            })
        profiles.append(profile)
    entry = {
        "id": pid + "_candidate",
        "ko": proposal["label_ko"],
        "en": spec["expression"],
        "weight": 0.45,
        "tags": ["photographic_scene", "photorealism_elements", spec["slot"]],
        "aliases": aliases,
        "keywords": cues,
        "embedding_text": proposal["label_ko"] + "; " + spec["expression"] + "; " + "; ".join([*cues, *units]),
        "concept_units": [proposal["label_ko"], *cues, *units],
        "relations": [{
            "id": pid + "_owner_relation",
            "type": "scene_bound_owner_relation",
            "subject": owner,
            "object": "the selected visible subject and its directly related scene surfaces",
        }],
        "affected_dimensions": spec["dimensions"],
    }
    slots.setdefault(spec["slot"], []).append(entry)
    coverage.append({
        "proposal_id": pid,
        "disposition": "new_profile" if stem not in REUSE and stem not in OPTIONAL_ONLY else
                       "reused_profile" if stem in REUSE else "optional_candidate_only",
        "runtime_profile_ids": [pid] if stem not in REUSE and stem not in OPTIONAL_ONLY else REUSE.get(stem, []),
        "slot": spec["slot"],
        "candidate_id": entry["id"],
        "source_ids": proposal["source_ids"],
    })

bundle_specs = [
    ("pe_window_action", "창가 실내의 행동·노출·초점", [
        "pr_observed_action_trace", "pr_scene_owned_exposure_tradeoff", "pr_focus_plane_subject_falloff"]),
    ("pe_environmental_maker", "인물·작업장·의복·접점", [
        "pr_environmental_portrait_subject_place", "pr_fabric_tension_fold_attachment",
        "pr_object_contact_shadow_support"]),
    ("pe_rain_observation", "거리의 바람·반사·크롭·원경", [
        "pr_hair_strand_owner_and_cause", "pr_reflection_scene_binding",
        "pr_casual_crop_subject_legibility", "pr_atmospheric_distance_contrast"]),
]
bundles = []
for bundle_id, scenario, ids in bundle_specs:
    assert len({SPEC_ROWS[i]["slot"] for i in ids}) == len(ids)
    bundles.append({
        "id": bundle_id,
        "primary_visual_proposition": scenario,
        "component_groups": [{
            "id": i + "_component",
            "visible_evidence": ["; ".join(SPEC_ROWS[i]["components"])],
        } for i in ids],
        "candidate_ids": [i + "_candidate" for i in ids],
        "candidate_slots": {i + "_candidate": SPEC_ROWS[i]["slot"] for i in ids},
        "hard_profile_ids": [i for i in ids if i.removeprefix("pr_") not in REUSE],
        "confusion_boundaries": [
            "Adoption is optional and must respect every locked dimension.",
            "A visual depiction does not verify its capture provenance.",
        ],
        "source_keywords": [scenario, *ids],
        "relations": [{
            "id": bundle_id + "_joint",
            "type": "co_realized_in_one_scene",
            "subject": "all selected component owners",
            "object": "one coherent photographic frame",
        }],
    })

extension = {
    "schema_version": "photo-prompt-research-extension/v1",
    "slots": slots,
    "visual_semantics": bundles,
}
record = {
    "record_id": "photo_prompt_photorealism_elements_extension",
    "authored_source_sha256": digest(extension),
    "maintenance_only": {
        "research_path": str(HERE.relative_to(ROOT)),
        "coverage": coverage,
        "source_ids": sorted({sid for p in proposals for sid in p["source_ids"]}),
        "limits": [
            "Research support concerns observable photographic relations, not a guarantee that generation will satisfy them.",
            "Broad photorealism, documentary, RAW and camera-model labels cannot independently prove capture origin.",
            "Noise, grain, compression, dust and wear remain context-dependent optional candidates.",
        ],
        "bundles_not_runtime": [b["id"] for b in read(HERE / "candidate-bundles.json")["bundles"]],
        "render_status": "not_run",
        "retrieval_revision": "Short positive owner cues calibrated after the first three frozen-core pack exposures; these arms are not an independent holdout.",
    },
}
write(ROOT / "docs/research-evidence/photo-prompt/extension-maintenance" /
      "photo_prompt_photorealism_elements_extension.json", record)
extension["maintenance_ref"] = {
    "contract_version": "photo-extension-maintenance-ref/v1",
    "record_id": record["record_id"],
    "sha256": digest(record),
}
write(ASSETS / "photo_prompt_photorealism_elements_extension.json", extension)
write(ASSETS / "photo_prompt_visual_obligations_photorealism_elements.json", {
    "schema_version": "photo-visual-obligation-registry-extension/v1",
    "relation_contract_version": "photo-visual-relation/v1",
    "description": "Scene-bound photorealistic evidence; no universal authenticity or imperfection claim.",
    "profiles": profiles,
})
write(HERE / "implementation-coverage.json", {
    "new_profiles": len(profiles),
    "candidates": sum(map(len, slots.values())),
    "bundles": len(bundles),
    "rows": coverage,
    "pixel_status": "not_run",
})
print(json.dumps({"new_profiles": len(profiles), "candidates": sum(map(len, slots.values())),
                  "bundles": len(bundles)}))
