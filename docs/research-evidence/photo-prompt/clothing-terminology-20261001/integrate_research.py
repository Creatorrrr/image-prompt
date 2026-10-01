"""Build reviewed visible variants; research families are never alias tables.

Authoring lives here, outside the distributed skill. Generated runtime JSON is
the authored data source consumed by the existing extension machinery.
"""
from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
MAINTENANCE = ROOT / "docs/research-evidence/photo-prompt/extension-maintenance"
MODULES = {
    "garment_structure": "clothing_structure",
    "textile_surface": "textile_surface",
    "accessory_structure": "accessory_structure",
    "traditional_variants": "traditional_clothing_detail",
}
# Context or provenance is not visible evidence. Keep these in the research
# backlog rather than silently promoting them to material/heritage claims.
HELD_VARIANTS = {
    ("CT033", 1): "Cut direction requires a grain/edge reference; folds do not prove bias cutting.",
    ("CT078", 1): "Silk-fiber content is not established by satin-like highlights.",
    ("CT082", 1): "Fiber composition and stretch performance are not established by silhouette.",
}
VISIBLE_REWRITES = {
    ("CT026", 1): "a sports jersey with a large numeral attached to its front panel",
    ("CT026", 2): "a plain jersey-knit top with a continuous solid-color front panel",
    ("CT027", 1): "an opened shirt placket showing paired flat fastener discs",
    ("CT033", 2): "a skirt falling in fluid diagonal fabric folds",
    ("CT074", 2): "a close-fitting dress fabric following the existing torso contour",
    ("CT119", 2): "a smooth domed cabochon with a continuous curved visible face",
    ("CT121", 1): "a red faceted stone with visible angular faces and perimeter",
}
BLUEPRINT_VARIANTS = {
    "henley_placket": 1, "sweetheart": 1, "raglan_setin_drop": 1,
    "puff_gigot": 1, "princess_dart": 1, "pocket_patch_welt_seam": 2,
    "piping_binding_welt": 1, "bra_wire_boning": 2,
    "twill_herringbone": 2, "bail_connector": 1,
    "oxford_derby_brogue": 1, "jeogori_parts": 1,
    "norigae_attachment": 1, "kimono_wrap_obi": 1, "tuck_relation": 1,
}


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()


def file_digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def property_path(record, slot):
    n = int(record["id"][2:])
    if slot == "footwear":
        return "wardrobe.footwear." + record["slug"]
    if slot == "wearable_accessory":
        return "wardrobe.accessories." + record["slug"]
    if slot == "surface_material":
        return "wardrobe.surface." + record["slug"]
    if 34 <= n <= 39:
        return "wardrobe.neckline"
    if 44 <= n <= 50:
        return "wardrobe.sleeves." + record["slug"]
    return "wardrobe.details." + record["slug"]


def selected_profile(record, variant, en, ko, blueprint):
    stem = record["id"].lower() + "_v" + str(variant)
    exact = [en, ko]
    if blueprint:
        profile = copy.deepcopy(blueprint["profile_draft"])
        # The reviewed Korean variant is intentionally specific, never the
        # whole family heading or every member of terms_for_research.
        components = profile["authored_components"]["components"]
    else:
        components = [{
            "id": "visible_relation", "match_terms": exact,
            "evidence_field": "visible_relation_phrase", "evidence_terms": [en],
            "min_content_words": 3,
            "instruction": "Realize this selected visible construction on its stated owner: " + en,
            "render_gate": {"id": "vo_clt_" + stem, "review_scale": "native",
                            "description": en + "; inspect the stated owner, boundary and connection at native resolution. Occlusion or a nearby substitute fails this visible relation."},
        }]
        profile = {"authored_components": {"contract_version": "photo-authored-visual-components/v1",
                                          "components": components}}
    profile.update({
        "id": "clothing_" + stem, "category": "clothing_visible_relation",
        "activation": {
            "exact_terms": exact, "requires_adult_character": False,
            "semantic_discovery_requires_component_evidence": True,
            "hard_activation": {"contract_version": "photo-visual-hard-activation/v1",
                                "required_any_groups": [{"id": "selected_visible_variant", "any_terms": exact}]},
        },
        "semantics": {
            "definition": en if len(en.split()) >= 8 else "The selected " + record["owner_domain"].replace("_", " ") + " is visibly rendered as " + en + ".",
            "paraphrase_examples": [
                "observable " + record["owner_domain"].replace("_", " ") + " detail showing " + en.removeprefix("a ").removeprefix("an "),
            ],
            "contrast_examples": [record["confusion_boundary"]],
            "claim_limits": [
                "This is one explicitly selected visible variant, not the universal definition of every related research term.",
                "Visible geometry does not establish hidden construction, fiber content, gemstone identity, physical function or wearer identity.",
                "Related variants are alternatives; their component pools are not an all-of requirement.",
                "A required connection must be visible at native resolution; a prompt label or printed imitation is insufficient.",
            ],
        },
        "concept_candidate": {"concept_terms": [ko, en]},
        "runtime_expression": {"default_mode": "definition_with_optional_label", "prompt_label_terms": [],
                               "forbidden_prompt_terms": [], "runtime_forbidden_labels": []},
        "reject_substitutes": [record["confusion_boundary"]],
    })
    for comp in components:
        # Component evidence is a discovery aid, not an extra exact trigger.
        # In particular, two-component variants must accept each component's
        # own independently worded evidence rather than repeating the entire
        # family sentence in every group.
        comp["match_terms"] = list(dict.fromkeys(exact + comp["evidence_terms"]))
        comp["render_gate"]["id"] = "vo_clt_" + stem + "_" + comp["id"]
    return profile


def main():
    records = json.loads((HERE / "semantic-records.json").read_text())["records"]
    blueprints = {b["research_slug"]: b for b in json.loads((HERE / "profile-candidate-blueprints.json").read_text())["blueprints"]}
    labels = {}
    for line in (HERE / "variant-authoring.psv").read_text().splitlines():
        if line and not line.startswith("#"):
            rid, one, two = line.split("|")
            labels[rid] = [one, two]
    assert set(labels) == {r["id"] for r in records}
    sources = json.loads((HERE / "sources.json").read_text())
    source_rows = sources.get("sources", sources.get("records", []))
    by_source = {s["id"]: s for s in source_rows}
    extensions = {m: {"schema_version": "photo-prompt-research-extension/v1", "slots": {}, "visual_semantics": []} for m in MODULES}
    registries = {m: {"schema_version": "photo-visual-obligation-registry-extension/v1",
                      "relation_contract_version": "photo-visual-relation/v1",
                      "description": "Explicit visible clothing variants with owner-scoped components; broad research families remain advisory.",
                      "profiles": []} for m in MODULES}
    bindings, backlog, ids = [], [], {}
    for r in records:
        if r["source_support"] == "source_expand_required":
            backlog.append({"research_id": r["id"], "variant": "all", "reason": "Additional primary definition required; family names not promoted.", "source_ids": r["source_ids"]})
            continue
        for v, draft in enumerate(r["candidate_phrase_drafts"], 1):
            if (r["id"], v) in HELD_VARIANTS:
                backlog.append({"research_id": r["id"], "variant": v, "reason": HELD_VARIANTS[(r["id"], v)]})
                continue
            bp = blueprints.get(r["slug"]) if BLUEPRINT_VARIANTS.get(r["slug"]) == v else None
            en = VISIBLE_REWRITES.get((r["id"], v), bp["candidate_draft"]["en"] if bp else draft["en"])
            ko = labels[r["id"]][v - 1]
            slot = bp["slot_proposal"] if bp else r["primary_slot_proposal"]
            stem = r["id"].lower() + "_v" + str(v)
            cid = "clt_" + stem
            profile = selected_profile(r, v, en, ko, bp)
            units = [c["evidence_terms"][0] for c in profile["authored_components"]["components"]]
            profile["semantics"]["visual_components"] = list(dict.fromkeys(units))
            relations = copy.deepcopy(bp["candidate_draft"]["relations"]) if bp else [{
                "id": "visible_owner_relation", "type": "has_visible_construction",
                "subject": r["owner_domain"].replace("_", " "), "object": en,
            }]
            # keywords aid search; they do not assert alias equivalence.
            keywords = list(dict.fromkeys([ko, en, r["title_ko"]] + [t for t in r["terms_for_research"] if t.casefold() in en.casefold()]))
            candidate = {
                "id": cid, "ko": ko, "en": en, "weight": 0.35,
                "aliases": [ko], "keywords": keywords,
                "embedding_text": " | ".join([en, ko, r["owner_domain"].replace("_", " ")] + units),
                "concept_units": units, "relations": relations, "tags": ["clothing"],
                "affected_dimensions": ["appearance"],
                "affected_properties": [{"dimension": "appearance", "target": "main_subject", "property": property_path(r, slot)}],
                "core_assertion_discovery": True,
            }
            profile["concept_candidate"].update({key: copy.deepcopy(candidate[key])
                                                 for key in ("core_assertion_discovery", "affected_dimensions", "affected_properties")})
            extensions[r["module_proposal"]]["slots"].setdefault(slot, []).append(candidate)
            registries[r["module_proposal"]]["profiles"].append(profile)
            ids[(r["id"], v)] = (cid, slot, profile, r["module_proposal"])
            bindings.append({
                "research_id": r["id"], "slug": r["slug"], "variant": v,
                "candidate_id": cid, "slot": slot, "profile_id": profile["id"],
                "component_ids": [c["id"] for c in profile["authored_components"]["components"]],
                "render_gate_ids": [c["render_gate"]["id"] for c in profile["authored_components"]["components"]],
                "source_ids": r["source_ids"], "source_support": r["source_support"],
                "evidence_basis": "source_feature_informed_authored_variant" if r["source_support"] == "direct_feature" else "family_context_only_authored_visible_variant",
                "source_bindings": [{"source_id": sid, "source_record_sha256": digest(by_source[sid])} for sid in r["source_ids"] if sid in by_source],
                "geometry_is_authored": True, "view_for_testing": r["visibility_view_proposal"],
                "routing": "pending", "native_pixels": "not_tested", "user_acceptance": "not_tested",
            })
    # Only coherent, explicitly authored combinations. Alternative silhouettes,
    # attachment sites and textile variants are not bundled indiscriminately.
    joints = [
        ("henley_raglan", "one shirt carries a short front placket and neckline-to-underarm sleeve seams", [("CT001",1),("CT044",1)]),
        ("shirt_collar_cuff", "one woven shirt has its folded collar and separately buttoned sleeve cuffs", [("CT002",2),("CT049",2)]),
        ("coat_storm_belt", "one trench has a waist belt and a separate flap over its back panel", [("CT009",1),("CT009",2)]),
        ("cargo_patch_gusset", "one trouser pocket has a flap over its mouth and raised side gussets", [("CT015",1),("CT059",2)]),
        ("overalls_bib", "one overall joins shoulder straps to the chest bib above its trouser waistband", [("CT016",1),("CT016",2)]),
        ("structured_channels_lacing", "one structured bodice has visible vertical channels beside crossed eyelet lacing", [("CT072",2),("CT055",1)]),
        ("sweetheart_princess", "one bodice combines a paired curved upper edge with curved front-to-side panel seams", [("CT036",1),("CT031",1)]),
        ("gigot_shawl", "one jacket has rounded shawl lapels and sleeves narrowing from a full upper arm", [("CT042",2),("CT046",1)]),
        ("shirt_yoke_backhem", "one shirt has an attached rear shoulder yoke and a longer rear hem", [("CT029",1),("CT062",2)]),
        ("toggle_loop", "opposite garment fronts meet through a toggle-and-cord-loop connection and a visible tie", [("CT054",2),("CT057",2)]),
        ("welt_lapel", "one jacket has a visible notched collar junction and welt-framed pocket slit", [("CT042",1),("CT058",2)]),
        ("ruffle_binding", "one top carries a gathered sleeve-edge ruffle and separately bound neckline", [("CT065",1),("CT066",2)]),
        ("bra_cup_underband", "the same bra joins two distinct cups by a bridge above its underband", [("CT070",2),("CT071",1)]),
        ("bra_strap_casing", "the same bra has a visible strap ring-and-slider and curved casing beneath its cups", [("CT073",1),("CT072",1)]),
        ("linen_sheer_layers", "one slub-textured cloth surface belongs to a sheer outer panel above a separate lining", [("CT078",2),("CT079",1)]),
        ("bail_layered_necklaces", "two distinct neck chains sit at different heights and one passes through its pendant bail", [("CT110",1),("CT116",1)]),
        ("ring_head_prongs", "one ring band supports its raised head and prongs curling over the stone edge", [("CT111",1),("CT114",1)]),
        ("ring_halo_bezel", "one central stone has a continuous bezel and a surrounding halo of smaller stones", [("CT111",2),("CT114",2)]),
        ("hat_ribbon", "one hat has a creased crown, surrounding brim and ribbon around the crown base", [("CT099",1),("CT099",2)]),
        ("derby_tongue", "one lace-up shoe has eyelet facings above the vamp and a tongue beneath the laces", [("CT122",1),("CT128",1)]),
        ("mule_squaretoe", "one backless shoe exposes the heel and has a broad straight toe edge", [("CT124",1),("CT129",1)]),
        ("bag_turnlock_handles", "one structured bag has two top handles and a turnlock-fastened flap", [("CT131",2),("CT132",2)]),
        ("jeogori_dongjeong_goreum", "one jeogori has a separately edged collar and ties attached to its overlapping fronts", [("CT135",1),("CT135",2)]),
        ("jeogori_norigae", "jeogori front ties support the norigae connector above its hanging knot and tassel", [("CT135",2),("CT137",1)]),
        ("kimono_overlap_obi", "one kimono has wearer-left over wearer-right front panels secured by the waist obi", [("CT139",1),("CT139",2)]),
        ("kebaya_sarong_kerosang", "one kebaya above a wrapped sarong closes through three linked kerosang brooches", [("CT141",1),("CT141",2)]),
        ("sari_continuity", "the same wrapped sari cloth continues into a visible pallu over one shoulder", [("CT142",1),("CT142",2)]),
        ("rear_volume_underskirt", "one skirt has rear-concentrated volume and a distinct inner layer at its hem", [("CT149",1),("CT149",2)]),
        ("mail_shoulder_plate", "a separate mail mesh lies beneath an attached shoulder armor plate", [("CT152",1),("CT153",1)]),
        ("layered_camisole_pendant", "an open shirt lies over a separate camisole while the pendant rests on the outer blouse layer", [("CT155",1),("CT155",2)]),
    ]
    # The last extension is loaded after all three other clothing modules.
    # Cross-module bundles can therefore resolve their members without changing
    # the loader or imposing any new runtime route.
    for slug, proposition, members in joints:
        details = [ids[pair] for pair in members]
        components = []
        for n, (_, _, prof, _) in enumerate(details, 1):
            for comp in prof["authored_components"]["components"]:
                components.append({"id": "member_" + str(n) + "_" + comp["id"], "visible_evidence": comp["evidence_terms"]})
        extensions["traditional_variants"]["visual_semantics"].append({
            "id": "clothing_b_" + slug, "primary_visual_proposition": proposition,
            "component_groups": components, "candidate_ids": [d[0] for d in details],
            "candidate_slots": {d[0]: d[1] for d in details}, "hard_profile_ids": [d[2]["id"] for d in details],
            "relations": [{"id": "shared_owner", "type": "same_frame_owner_relation", "subject": "the request-supported garment or accessory", "object": proposition}],
            "confusion_boundaries": ["Bundle members are one selected combination; related family variants are not automatically required.", "A hidden or relocated required connection cannot be inferred from a nearby decorative substitute."],
            "candidate_only": True, "activation_mode": "independent_component_request_evidence_only",
            "source_keywords": [proposition],
        })
    runtime_files = []
    for module, basename in MODULES.items():
        ext = extensions[module]
        registry = registries[module]
        registry_path = ASSETS / ("photo_prompt_visual_obligations_" + basename + ".json")
        write(registry_path, registry)
        record_id = "photo_prompt_" + basename + "_extension"
        rows = [b for b in bindings if next(r for r in records if r["id"] == b["research_id"])["module_proposal"] == module]
        record = {
            "contract_version": "photo-extension-maintenance/v1", "record_id": record_id,
            "source_filename": record_id + ".json", "authored_source_sha256": digest(ext),
            "runtime_keys": ["slots", "visual_semantics"],
            "maintenance_only": {
                "research_path": str(HERE.relative_to(ROOT)), "source_ledger_sha256": file_digest(HERE / "sources.json"),
                "research_records_sha256": file_digest(HERE / "semantic-records.json"),
                "variant_authoring_sha256": file_digest(HERE / "variant-authoring.psv"),
                "runtime_registry_sha256": digest(registry), "variant_bindings": rows,
                "scope_limit": "Family-context sources support context only; geometry and gates are authored. Render qualification is separate and pending per source hash.",
            },
        }
        write(MAINTENANCE / (record_id + ".json"), record)
        ext["maintenance_ref"] = {"contract_version": "photo-extension-maintenance-ref/v1", "record_id": record_id, "sha256": digest(record)}
        extension_path = ASSETS / (record_id + ".json")
        write(extension_path, ext)
        runtime_files.extend([extension_path, registry_path])
    manifest = {
        "contract_version": "clothing-terminology-runtime-integration/v1",
        "research_record_count": len(records), "integrated_family_count": len({b["research_id"] for b in bindings}),
        "candidate_count": len(bindings), "profile_count": len(bindings),
        "native_gate_count": sum(len(b["render_gate_ids"]) for b in bindings), "joint_bundle_count": len(joints),
        "slot_counts": dict(Counter(b["slot"] for b in bindings)), "backlog": backlog,
        "variant_bindings": bindings,
        "runtime_files": [{"path": str(p.relative_to(ROOT)), "sha256": file_digest(p)} for p in runtime_files],
        "qualification_boundary": "Runtime integration is not image qualification. Three independent image cases qualify only their actually exposed/adopted/tested visible relations.",
    }
    write(HERE / "runtime-integration.json", manifest)
    print(json.dumps({k: v for k, v in manifest.items() if k not in {"variant_bindings", "runtime_files", "backlog"}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
