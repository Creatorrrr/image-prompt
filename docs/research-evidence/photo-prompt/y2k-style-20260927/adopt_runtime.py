"""Project researched morphology into the existing additive runtime contracts.

Research sources and historical claims remain in maintenance evidence. This
does not rebuild indexes or qualify rendered pixels.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
sys.path.insert(0, str(ROOT / "skills/photo-prompt-image-generator/scripts"))
import photo_candidate_semantics as semantics


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    extension = read(HERE / "runtime-extension.proposed.json")
    components = read(HERE / "semantic-components.proposed.json")["components"]
    by_id = {row["id"]: row for row in components}
    aliases = {}
    bound_variants = []

    # These palettes prescribe garment/accessory owners; four also prescribe
    # a visible material or ornament. Color permission alone cannot admit them.
    for row in extension["slots"]["color"]:
        row["affected_dimensions"] = ["appearance", "color"]
        if row["id"] in {"y2kr_cyber_palette", "y2kr_bling_palette", "y2kr_goth_palette", "y2kr_rave_palette"}:
            row["affected_dimensions"].append("material")

    # Garment proportions describe clothing boundaries, not anatomy. Do not
    # let them silently rewrite a reference subject's body geometry.
    proportions = extension["slots"].pop("silhouette_proportion")
    for row in proportions:
        row["affected_dimensions"] = ["appearance"]
        row["tags"] = ["y2k_morphology_visual_semantics", "garment_detail", "human"]
    extension["slots"]["garment_detail"].extend(proportions)

    # The generic material slot is intentionally non-human. Add clothing-owned
    # versions instead of weakening that shared applicability guard.
    for row in list(extension["slots"]["surface_material"]):
        bound = copy.deepcopy(row)
        bound["id"] += "_garment"
        bound["ko"] += " — 의복 표면"
        bound["concept_units"] = ["on the selected garment surface, " + unit for unit in row["concept_units"]]
        bound["en"] = "; ".join(bound["concept_units"])
        bound["embedding_text"] = bound["en"]
        bound["affected_dimensions"] = ["appearance", "material"]
        bound["tags"] = ["y2k_morphology_visual_semantics", "garment_detail", "human"]
        extension["slots"]["garment_detail"].append(bound)
        aliases[row["id"]] = (bound["id"], "garment_detail")
        bound_variants.append({"source_id": row["id"], "id": bound["id"], "owner": "selected garment surface", "slot": "garment_detail"})

    # Generic portable props keep their unknown-scope restriction. Separate
    # versions state a physical owner/context and the dimensions they change.
    # These are optional staging candidates, never a change to the core action.
    for row in list(extension["slots"]["prop"]):
        bound = copy.deepcopy(row)
        if row["id"] == "y2kr_phone_neckstrap":
            bound["id"] += "_worn"
            bound["affected_dimensions"] = ["appearance"]
            slot, owner = "wearable_accessory", "strap and phone worn around the neck"
            bound["tags"] = ["y2k_morphology_visual_semantics", slot, "human"]
        elif row["id"] == "y2kr_purikura":
            bound["id"] += "_installed"
            bound["affected_dimensions"] = ["setting"]
            slot, owner = "prop", "installed photo booth in the background"
            bound["concept_units"] = ["in the background, " + unit for unit in row["concept_units"]]
            bound["tags"] = ["y2k_morphology_visual_semantics", slot]
        else:
            bound["id"] += "_tabletop"
            bound["affected_dimensions"] = ["setting"]
            slot, owner = "prop", "object resting on a visible working surface"
            bound["concept_units"] = ["on a visible working surface, " + unit for unit in row["concept_units"]]
            bound["tags"] = ["y2k_morphology_visual_semantics", slot]
            if row["id"] == "y2kr_magazine":
                bound["affected_dimensions"].append("text")
        bound["en"] = "; ".join(bound["concept_units"])
        bound["embedding_text"] = bound["en"]
        extension["slots"][slot].append(bound)
        aliases[row["id"]] = (bound["id"], slot)
        bound_variants.append({"source_id": row["id"], "id": bound["id"], "owner": owner, "slot": slot})

    for bundle in extension["visual_semantics"]:
        for old_id in list(bundle["candidate_ids"]):
            if old_id not in aliases:
                continue
            new_id, slot = aliases[old_id]
            bundle["candidate_ids"] = [new_id if value == old_id else value for value in bundle["candidate_ids"]]
            del bundle["candidate_slots"][old_id]
            bundle["candidate_slots"][new_id] = slot
            for relation in bundle["relations"]:
                for end in ("subject", "object"):
                    if relation[end] == old_id:
                        relation[end] = new_id
        if bundle["id"] in {"y2kr_bundle_early_devices", "y2kr_bundle_mid_devices"}:
            bundle["primary_visual_proposition"] = "on one visible working surface, " + bundle["primary_visual_proposition"]
            bundle["component_groups"][-1]["visible_evidence"] = [bundle["primary_visual_proposition"]]

    candidates = {row["id"]: row for rows in extension["slots"].values() for row in rows}
    # The complete visible form follows the selected scoped candidate, so a
    # bundle cannot count a generic sparkle or wrong-owner object as evidence.
    for bundle in extension["visual_semantics"]:
        for group, candidate_id in zip(bundle["component_groups"], bundle["candidate_ids"]):
            group["visible_evidence"] = candidates[candidate_id]["concept_units"]

    profiles = []
    for comp in components:
        units = comp["visible_components"]
        definition = "; ".join(units)
        # Literal complete definitions activate a scoped obligation. Narrow
        # labels are discovery aids only; broad family names are never triggers.
        profile = {
            "id": "y2kr_" + comp["id"],
            "category": "observable_fashion_and_object_morphology",
            "activation": {"exact_terms": [definition], "requires_adult_character": False,
                           "semantic_discovery_requires_component_evidence": False},
            "semantics": {"definition": definition, "paraphrase_examples": [comp["label_ko"], *comp["seed_terms"]],
                          "contrast_examples": comp["confusion_negatives_ko"],
                          "claim_limits": ["A label alone does not require this complete morphology.",
                                           "Evidence must belong to " + comp["owner"] + ".",
                                           "This specifies visible form, not a historical date, wearer identity, or hidden material performance."]},
            "concept_candidate": {"concept_terms": [comp["label_ko"], *comp["seed_terms"], *units]},
            "runtime_expression": {"default_mode": "definition_with_optional_label", "prompt_label_terms": [],
                                   "forbidden_prompt_terms": [], "runtime_forbidden_labels": []},
            "reject_substitutes": comp["confusion_negatives_ko"],
            "authored_components": {"contract_version": "photo-authored-visual-components/v1", "components": [
                {"id": f"component_{i}", "match_terms": [unit], "evidence_field": f"component_{i}_phrase",
                 "evidence_terms": [unit], "min_content_words": 3,
                 "instruction": f"Keep this form visible on {comp['owner']}: {unit}",
                 "render_gate": {"id": f"vo_y2kr_{comp['id']}_{i}", "review_scale": "both",
                                 "description": f"{unit}. Owner: {comp['owner']}. Minimum view: {comp['minimum_view']}. All declared form parts must be readable; a wrong owner or sole confusion substitute fails. Partial is fail; blocked or invisible evidence is unscored."}}
                for i, unit in enumerate(units, 1)]},
        }
        profiles.append(profile)

    maintenance = {
        "id": "y2k-style-research-20260927", "maintenance_only": True,
        "status": "registered_morphology_pixel_qualification_separate",
        "source_ledger_sha256": sha(HERE / "sources.json"),
        "seed_keywords_sha256": sha(HERE / "seed-keywords.json"),
        "proposal_sha256": sha(HERE / "runtime-extension.proposed.json"),
        "semantic_proposal_sha256": sha(HERE / "semantic-components.proposed.json"),
        "counts": {"seed_rows": 308, "morphology_profiles": len(profiles), "runtime_candidates": len(candidates),
                   "optional_bundles": len(extension["visual_semantics"]), "scoped_variants": len(bound_variants)},
        "scoped_variants": bound_variants,
        "corrections": ["Clothing-boundary proportions change appearance rather than anatomy.",
                        "Garment material variants preserve the non-human generic material slot guard.",
                        "Device bundles require a visible working-surface owner and open setting dimension.",
                        "Unscoped generic prop variants remain ineligible for joint adoption.",
                        "Owner-specific palettes declare appearance and, where applicable, material as well as color.",
                        "Broad family names and historical source prose do not activate hard visual profiles."],
        "claim_limits": ["Research operational definitions are not rendered pixel certification.",
                         "Keyword coverage does not establish historical prevalence or every original seed modifier.",
                         "Three complex renders sample the tested concepts; they do not qualify every component."]
    }
    maintenance_path = ROOT / "docs/research-evidence/photo-prompt/extension-maintenance/y2k-style-research-20260927.json"
    write(maintenance_path, maintenance)
    extension["maintenance_ref"]["sha256"] = semantics.digest(maintenance)
    semantics.validate_extension_keys(extension)
    write(ASSETS / "photo_prompt_y2k_extension.json", extension)
    write(ASSETS / "photo_prompt_visual_obligations_y2k.json", {
        "schema_version": "photo-visual-obligation-registry-extension/v1",
        "relation_contract_version": "photo-visual-relation/v1",
        "description": "Observable fashion and device forms with owner-bound component gates; broad era and style labels remain advisory.",
        "profiles": profiles,
    })
    write(HERE / "runtime-adoption.json", {"maintenance_ref": extension["maintenance_ref"], "counts": maintenance["counts"],
          "files": {name: sha(ASSETS / name) for name in ("photo_prompt_y2k_extension.json", "photo_prompt_visual_obligations_y2k.json")}})
    print(json.dumps(maintenance["counts"]))


if __name__ == "__main__":
    main()
