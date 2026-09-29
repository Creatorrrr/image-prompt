#!/usr/bin/env python3
"""Compile source-linked fashion research into optional photo candidates and bundles.

The checked-in source_pool.json is the reviewable input. This builder changes data,
not the prompt generator's selection, safety, or visual-obligation logic.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ASSET = HERE.parents[3] / "skills/photo-prompt-image-generator/assets/photo_prompt_sensual_fetish_fashion_extension.json"
POOL = HERE / "source_pool.json"
HIDDEN_STRUCTURE = {"XA012", "XA027"}


def candidate_id(origin: str, atom_id: str) -> str:
    return f"sff_{origin}_{atom_id.lower()}"


def addendum_slot(row: dict) -> str:
    atom_id = row["id"]
    if atom_id in {"XA005", "XA028", "XA029", "XA031", "XA032", "XA042", "XA045"}:
        return "wardrobe_style"
    if atom_id in {"XA024", "XA025", "XA026", "XA037", "XA040"}:
        return "wearable_accessory"
    if atom_id in {"XA044", "XA047"}:
        return "texture"
    if atom_id in {"XA038", "XA039", "XA041", "XA048", "XA049"}:
        return "fetish_styling"
    return "garment_detail"


def candidate(row: dict, origin: str, slot: str) -> dict:
    ko = row["term_ko"]
    en = row["term_en"]
    components = row["visible_components"]
    axis = row["axis"]
    dimensions = row.get("dimensions") or (["appearance"] if axis == "S" else ["appearance", "material"])
    aliases = list(dict.fromkeys([en, ko, *row.get("aliases", [])]))
    entry = {
        "id": candidate_id(origin, row["id"]),
        "ko": ko,
        "en": en,
        "weight": 0.42,
        "tags": ["human", "adult", "fashion"] + (["sensual_editorial"] if "S" in axis else []) + (["fetish_fashion"] if "F" in axis else []),
        "for_any": ["human"],
        "aliases": aliases,
        "keywords": aliases[:4],
        "embedding_text": "; ".join([ko, en, *components]),
        "concept_units": [en, *components],
        "relations": [{
            "id": candidate_id(origin, row["id"]) + "_owner",
            "type": "visible_owner_and_boundary",
            "subject": en,
            "object": row["visible_owner"],
        }],
        "affected_dimensions": dimensions,
        "research_source_urls": row["source_urls"],
        "research_origin_id": f"{origin}:{row['id']}",
        "research_confusions": row["confusion_substitutes"],
    }
    if row.get("view_requirement"):
        entry["research_view_requirement"] = row["view_requirement"]
    if "appearance" in dimensions and slot in {
        "wardrobe_style", "garment_detail", "fetish_styling", "footwear",
        "wearable_accessory", "surface_material", "texture",
    }:
        entry["affected_properties"] = [{
            "dimension": "appearance",
            "target": "main_subject",
            "property": "wardrobe",
        }]
    return entry


def bundle(bundle_id: str, name: str, atom_refs: list[tuple[str, dict]],
           visible: list[str], confusions: list[str],
           owner: str, observable_relation: str = "") -> dict:
    assert atom_refs, bundle_id
    components = [
        {"id": f"part_{i}", "visible_evidence": [phrase]}
        for i, phrase in enumerate(visible, 1) if phrase.strip()
    ]
    if not components:
        components = [{"id": "garment_relation", "visible_evidence": [name]}]
    ids = [candidate_id(origin, atom["id"]) for origin, atom in atom_refs]
    return {
        "id": bundle_id,
        "primary_visual_proposition": name,
        "component_groups": components,
        "candidate_ids": ids,
        "candidate_slots": {candidate_id(origin, atom["id"]): atom["_slot"] for origin, atom in atom_refs},
        "hard_profile_ids": [],
        "confusion_boundaries": list(dict.fromkeys(confusions)),
        "source_keywords": [name],
        "relations": [{
            "id": bundle_id + "_same_owner",
            "type": "co_realized_with_same_subject_and_garment",
            "subject": owner,
            "object": observable_relation or "the visible parts of this optional fashion combination",
        }],
    }


def main() -> None:
    pool = json.loads(POOL.read_text())
    assert pool["schema_version"] == "sensual-fetish-source-pool/v1"
    atoms: dict[tuple[str, str], dict] = {}
    slots: dict[str, list[dict]] = {}
    for origin, key in (("pro", "pro_atoms"), ("extra", "addendum_atoms")):
        for source in pool[key]:
            if origin == "extra" and source["id"] in HIDDEN_STRUCTURE:
                continue
            row = dict(source)
            slot = row["slots"][0] if origin == "pro" else addendum_slot(row)
            row["_slot"] = slot
            atoms[(origin, row["id"])] = row
            slots.setdefault(slot, []).append(candidate(row, origin, slot))

    bundles = []
    for row in pool["pro_relations"]:
        refs = [("pro", atoms[("pro", aid)]) for aid in row["atom_ids"]]
        evidence = row["visible_components"]
        bundles.append(bundle(f"sff_relation_pro_{row['id'].lower()}", row["term_en"], refs,
                              evidence, row["confusion_substitutes"],
                              row["visible_owner"], "; ".join(evidence)))
    for row in pool["addendum_relations"]:
        refs = [("extra", atoms[("extra", aid)]) for aid in row["atom_ids"] if ("extra", aid) in atoms]
        evidence = [row["observable_relation"], *[component for _, atom in refs for component in atom["visible_components"]]]
        owners = list(dict.fromkeys(atom["visible_owner"] for _, atom in refs))
        bundles.append(bundle(f"sff_relation_extra_{row['id'].lower()}", row["name"], refs,
                              evidence, [row["failed_confusion"]],
                              " / ".join(owners), row["observable_relation"]))
    for row in pool["pro_packs"]:
        refs = [("pro", atoms[("pro", aid)]) for aid in row["primary_atom_ids"]]
        evidence = row["visible_components"]
        bundles.append(bundle(f"sff_pack_pro_{row['id'].lower()}", row["term_en"], refs,
                              evidence, row["confusion_substitutes"],
                              row["visible_owner"], "; ".join(evidence)))
    for row in pool["addendum_packs"]:
        refs = [("extra", atoms[("extra", aid)]) for aid in row["atom_ids"] if ("extra", aid) in atoms]
        evidence = [row["bounded_content"], *[component for _, atom in refs for component in atom["visible_components"]]]
        owners = list(dict.fromkeys(atom["visible_owner"] for _, atom in refs))
        bundles.append(bundle(f"sff_pack_extra_{row['id'].lower()}", row["name"], refs,
                              evidence, [], " / ".join(owners),
                              row["bounded_content"]))

    ids = [row["id"] for rows in slots.values() for row in rows]
    assert len(ids) == len(set(ids)) == 251
    assert len(bundles) == 116 and len({row["id"] for row in bundles}) == len(bundles)
    output = {
        "schema_version": "photo-prompt-research-extension/v1",
        "existing_preset_filter_extensions": {
            "adult_fetish_fashion_editorial": {
                "wardrobe_style": {"ids": [
                    "sff_pro_y01", "sff_pro_y03", "sff_pro_y06", "sff_pro_y07",
                ]},
                "garment_detail": {"ids": [
                    "sff_pro_h05", "sff_pro_h09", "sff_pro_c14", "sff_pro_c15",
                    "sff_pro_c17", "sff_pro_e10",
                ]},
                "wearable_accessory": {"ids": ["sff_pro_g08"]},
                "footwear": {"ids": ["sff_pro_b11"]},
            },
        },
        "slots": dict(sorted(slots.items())),
        "visual_semantics": bundles,
        "maintenance_ref": {
            "contract_version": "photo-extension-maintenance-ref/v1",
            "record_id": "photo_prompt_sensual_fetish_fashion_extension",
            "sha256": hashlib.sha256(POOL.read_bytes()).hexdigest(),
        },
    }
    ASSET.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"path": str(ASSET), "slots": {key: len(value) for key, value in slots.items()},
                      "candidates": len(ids), "visual_semantics": len(bundles)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
