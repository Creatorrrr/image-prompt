#!/usr/bin/env python3
"""Compile research artifacts inside this directory; never register runtime data."""
import collections
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HEADER = ["id", "domain", "label", "keywords", "slot", "owner", "sources",
          "components", "relations", "boundary", "status"]
DOMAINS = {
    "combustion": "불과 연소", "flame_structure": "화염 구조", "flame_geometry": "화염 형상",
    "color_light": "색과 불빛", "heat_air": "열과 공기", "smoke_residue": "연기와 잔류물",
    "thermal_damage": "재료 손상", "fire_events": "화재 사건", "fire_suppression": "소방과 방호",
    "wildfire": "산불과 생태", "domestic_fire": "연료와 생활", "craft_industry": "공예와 산업",
    "food": "요리와 향미", "solar": "태양과 우주기상", "camera_optics": "카메라 광학",
    "noncombustion": "불처럼 보이는 비연소 현상", "culture_fantasy": "문화와 판타지",
    "body_relation": "신체와 재료 접촉", "violence_context": "폭력 맥락",
    "metaphor_context": "비유와 동기",
}
CLAIM_LIMITS = [
    "Visual forms below are researcher-authored realizations, not quotations or unique scientific definitions.",
    "Still pixels do not establish temperature, reaction speed, chemical identity, safety, sound, smell, taste, cause, intent, consent or clinical diagnosis.",
    "Keyword associations are research links, not exact runtime aliases or requester obligations.",
]
SLOT_EFFECTS = {
    "prop": ("setting", "object.arrangement"), "action": ("action", "source_target_connection"),
    "surface_material": ("material", "surface_state"), "ambient_particle": ("atmosphere", "particle_structure"),
    "light_shape": ("lighting", "emission_geometry"), "subject": ("subject", "visible_form"),
    "surreal_physics_detail": ("concept", "fictional_physical_form"), "color": ("color", "owned_color"),
    "lighting": ("lighting", "receiver_illumination"), "reflection_logic": ("lighting", "reflection_transport"),
    "lens_artifact": ("camera", "optical.lens_artifact"), "aftermath_trace": ("material", "residual_trace"),
    "location": ("setting", "spatial_structure"), "texture": ("material", "surface_structure"),
    "hair_style": ("appearance", "hair.local_surface_state"), "costume_style": ("appearance", "clothing.form"),
    "weather": ("atmosphere", "cloud_structure"), "color_grading": ("camera", "processing.channel_color"),
    "body_pose": ("pose", "hands.position"), "garment_detail": ("appearance", "garment.local_surface_state"),
}
CONTEXT_COMPONENTS = {("F038", "offscreen_source"), ("F130", "channel"), ("F130", "color_table")}
PRIMARY_PROTOTYPES = [
    "F001", "F003", "F004", "F005", "F014", "F037", "F041", "F048",
    "F058", "F070", "F082", "F083", "F085", "F105", "F123", "F132",
    "F149", "F152",
]
REUSE = {
    "F131": ("photo_prompt_editing_effects_extension.json", "pe_veiling_flare"),
    "F132": ("photo_prompt_editing_effects_extension.json", "pe_aligned_ghosts"),
    "F133": ("photo_prompt_editing_effects_extension.json", "pe_horizontal_anamorphic_streak"),
    "F127": ("photo_prompt_space_extension.json", "coronal_mass_ejection_observation_subject"),
}
ADJACENT = {("F130", "청색 화염"), ("F130", "녹색 화염"), ("F130", "보라색 화염"),
            ("F136", "불꽃 폭포"), ("F040", "복사열")}

def save(name, payload):
    (ROOT / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")

def rows():
    result = []
    for raw in (ROOT / "SEMANTIC-ROWS.tsv").read_text().splitlines()[1:]:
        values = raw.split("|")
        if len(values) != len(HEADER):
            raise ValueError((values[0], len(values)))
        row = dict(zip(HEADER, values))
        result.append(row)
    return result

def proposed_effects(row):
    dim, prop = SLOT_EFFECTS[row["slot"]]
    target = row["owner"]
    if row["domain"] == "camera_optics":
        target = "image_plane"
    effects = [{"dimension": dim, "target": target, "property": prop}]
    if row["id"] == "F041":
        effects = [
            {"dimension": "atmosphere", "target": "heated_air_path", "property": "refractive_structure"},
            {"dimension": "camera", "target": "image_plane", "property": "optical.apparent_distortion"},
        ]
    if row["id"] == "F149":
        effects.append({"dimension": "relationship", "target": "selected_skin_patch", "property": "wax_contact"})
    if row["id"] == "F150":
        effects.append({"dimension": "material", "target": "selected_garment_patch", "property": "thermal_damage"})
    return effects

def main():
    authored = rows()
    seeds = json.loads((ROOT / "SEED-INVENTORY.json").read_text())["seeds"]
    sources = json.loads((ROOT / "SOURCES.json").read_text())["sources"]
    sources_by_id = {row["id"]: row for row in sources}
    ids = [row["id"] for row in authored]
    assert len(ids) == len(set(ids))
    assert ids == [f"F{i:03}" for i in range(1, len(ids) + 1)]
    cards, drafts, mapping, profiles, coverage = [], [], [], [], []
    for row in authored:
        sid = row["id"]
        source_ids = [] if row["sources"] == "none" else row["sources"].split(",")
        assert set(source_ids) <= set(sources_by_id)
        terms = row["keywords"].split(";")
        linked_seeds = [seed["seed_id"] for seed in seeds if seed["term_ko"] in terms]
        renderable = row["status"] != "context"
        components = []
        relations = []
        if renderable:
            for i, value in enumerate(row["components"].split("~"), 1):
                owner, phrase = value.split("::", 1)
                components.append({
                    "id": f"component_{i}", "owner_role": owner, "observable_form_en": phrase,
                    "evidence_class": "request_or_observation_metadata" if (sid, owner) in CONTEXT_COMPONENTS else "native_visible_form",
                })
            assert len(components) == 3
            for i, value in enumerate(row["relations"].split(";"), 1):
                subject, rel_type, obj = value.split(">")
                relations.append({"id": f"{sid.lower()}_relation_{i}", "type": rel_type, "subject": subject, "object": obj})
        effects = proposed_effects(row) if renderable else []
        source_limits = [note for src in source_ids for note in sources_by_id[src]["limitations"] if "추가" in note or "전문" in note]
        followup = any(word in row["boundary"] for word in ["추가", "전용", "전문", "판본별"])
        card = {
            "id": sid, "domain": row["domain"], "label_ko": row["label"],
            "seed_ids": linked_seeds, "research_keyword_associations": terms,
            "visual_status": row["status"], "renderable": renderable,
            "meaning_basis": "creative_proposal" if row["status"] == "creative" or not source_ids else "source_boundary_plus_authored_visual_projection",
            "source_ids": source_ids, "source_access_limits": source_limits,
            "definition_or_context_ko": row["components"] if not renderable else row["label"],
            "observable_components": components, "relations": relations,
            "confusion_boundaries": [row["boundary"]], "claim_limits": CLAIM_LIMITS,
            "further_source_review_required": followup,
            "candidate_id": f"fire_{sid.lower()}" if renderable else None,
            "proposed_slot": row["slot"] if renderable else None,
            "proposed_effects": effects,
            "owner_resolution_status": "not_runtime_verified",
            "activation_policy": "request meaning resolved before retrieval; approximate matches advisory; complete selected realization only",
        }
        cards.append(card)
        if not renderable:
            mapping.append({"unit_id": sid, "decision": "glossary_or_context_only", "runtime_target": None, "reason": row["boundary"]})
            continue
        phrase = "; ".join(c["observable_form_en"] for c in components)
        dimensions = list(dict.fromkeys(e["dimension"] for e in effects))
        entry = {
            "id": f"fire_{sid.lower()}", "ko": row["label"], "en": phrase, "weight": 0.45,
            "tags": [row["domain"]], "aliases": [row["label"]],
            "keywords": [row["label"]], "paraphrases": [phrase],
            "concept_terms": [c["observable_form_en"] for c in components],
            "concept_units": [c["observable_form_en"] for c in components],
            "relations": relations, "affected_dimensions": dimensions, "affected_properties": effects,
            "core_assertion_discovery": True,
            "embedding_text": row["label"] + "; " + phrase,
        }
        drafts.append({
            "unit_id": sid, "slot": row["slot"], "runtime_entry_proposal": entry,
            "research_only": True,
            "review_status": "additional_source_review" if followup else "owner_consumer_mapping_pending",
            "eligibility_requirements": [
                "The frozen request/core already supports this subject, source, carrier, event and observation mode.",
                "Resolve every target/property to the same owner; reject closed dimensions or locked properties.",
                "Do not infer violence, ritual, sexual tone, age, intent or chemistry from a broad fire token.",
                "Whole compound candidates remain optional and cannot replace the independent baseline.",
            ],
        })
        if sid in REUSE:
            file_name, entry_id = REUSE[sid]
            target = file_name
            decision = "review_existing_equivalence_before_extension"
            existing = entry_id
        elif row["domain"] == "solar":
            target = "photo_prompt_space_extension.json"
            decision = "extend_existing_domain_if_owner_and_observation_mode_match"
            existing = None
        elif row["domain"] == "camera_optics":
            target = "photo_prompt_editing_effects_extension.json"
            decision = "extend_existing_domain_after_optical_source_review"
            existing = None
        else:
            target = "photo_prompt_fire_relations_extension.json"
            decision = "proposed_new_atomic_entry"
            existing = None
        mapping.append({
            "unit_id": sid, "candidate_id": entry["id"], "decision": decision, "runtime_target": target,
            "existing_id_to_review": existing, "slot": row["slot"],
            "effects_proposed": effects, "consumer_mapping": "pending",
            "alias_policy": "research seed names are not copied as unconditional aliases",
        })
        if sid not in PRIMARY_PROTOTYPES:
            continue
        component_rows = [{"id": c["id"], "match_terms": [c["observable_form_en"]]} for c in components]
        evidence = [{
            "field": f"{c['id']}_phrase",
            "requirement": {"min_content_words": 3, "must_mention_any": [c["observable_form_en"]]},
        } for c in components]
        gates = [{
            "id": f"vo_fire_{sid.lower()}_{i}", "review_scale": "native",
            "description": f"Inspect this visible component on its declared owner {c['owner_role']}: {c['observable_form_en']}. Hidden, partial or transferred realization fails.",
        } for i, c in enumerate(components, 1)]
        gates.append({
            "id": f"vo_fire_{sid.lower()}_owned_relation", "review_scale": "both",
            "description": "Verify the complete same-owner connection in one coherent frame: " +
                           "; ".join(f"{r['subject']} {r['type']} {r['object']}" for r in relations) +
                           ". Neighboring objects and disconnected substitutes do not satisfy the relation.",
        })
        proposition = phrase + "."
        profile = {
            "id": f"fire_rel_{sid.lower()}", "category": "fire_component_relation",
            "activation": {
                "exact_terms": [proposition], "requires_adult_character": False,
                "semantic_discovery_requires_component_evidence": True,
                "hard_activation": {
                    "contract_version": "photo-visual-hard-activation/v1",
                    "required_any_groups": [{"id": "complete_owned_proposition", "any_terms": [proposition]}],
                },
            },
            "semantics": {
                "definition": phrase, "paraphrase_examples": [row["label"], phrase],
                "visual_components": [c["observable_form_en"] for c in components],
                "contrast_examples": [row["boundary"]], "claim_limits": CLAIM_LIMITS,
            },
            "authored_components": {
                "contract_version": "photo-authored-visual-components/v2",
                "components": component_rows,
                "discovery": {"minimum_component_groups": 2, "required_group_ids": ["component_2"]},
                "obligations": [{
                    "component_ids": [c["id"] for c in components], "evidence": evidence,
                    "instruction": "Preserve the complete selected realization and every declared owner connection: " + phrase + ".",
                    "render_gates": gates,
                }],
            },
            "concept_candidate": {
                "concept_terms": [row["label"]] + [c["observable_form_en"] for c in components],
                "core_assertion_discovery": True, "affected_dimensions": dimensions, "affected_properties": effects,
            },
            "runtime_expression": {"default_mode": "definition_with_optional_label", "prompt_label_terms": [],
                                   "forbidden_prompt_terms": [], "runtime_forbidden_labels": []},
            "reject_substitutes": [row["boundary"]],
        }
        profiles.append(profile)
    for seed in seeds:
        links = [{
            "unit_id": card["id"],
            "relation": "contrast_or_adjacent_reference" if (card["id"], seed["term_ko"]) in ADJACENT else
                        "context_only" if not card["renderable"] else "optional_visual_realization",
        } for card in cards if seed["seed_id"] in card["seed_ids"]]
        assert links, f"Unaccounted seed: {seed['seed_id']} {seed['term_ko']}"
        coverage.append({"seed_id": seed["seed_id"], "term_ko": seed["term_ko"], "links": links,
                         "coverage_status": "accounted_in_research", "runtime_alias_authorized": False})
    save("SEMANTIC-UNITS.json", {"schema_version": "fire-research-semantics/v1", "status": "research_only", "cards": cards})
    save("CANDIDATE-DRAFTS.json", {"schema_version": "fire-research-candidate-drafts/v1", "status": "not_registered_or_integrated", "drafts": drafts})
    save("PROFILE-PROTOTYPES.json", {"schema_version": "fire-research-profile-prototypes/v1", "status": "compiler_shape_prototypes_only", "profiles": profiles})
    save("RUNTIME-MAPPING.json", {"schema_version": "fire-research-adoption-plan/v1", "rows": mapping})
    save("SEED-COVERAGE.json", {"schema_version": "fire-research-seed-coverage/v1", "coverage": coverage,
                               "limits": "Accounting is not independent verification of every seed definition, runtime exposure or rendered success."})
    by_domain = collections.Counter(c["domain"] for c in cards)
    stats = {"semantic_cards": len(cards), "candidate_drafts": len(drafts), "context_only_cards": sum(not c["renderable"] for c in cards),
             "creative_cards": sum(c["visual_status"] == "creative" for c in cards), "profile_prototypes": len(profiles),
             "prototype_compound_gates": sum(len(p["authored_components"]["obligations"][0]["render_gates"]) for p in profiles),
             "reference_seed_rows": len(seeds), "accounted_seed_rows": len(coverage), "primary_or_institutional_sources": len(sources),
             "sources_by_access_level": dict(collections.Counter(s["access_level"] for s in sources)),
             "domains": dict(by_domain), "runtime_integration": False, "image_generation": False}
    save("RESEARCH-STATS.json", stats)
    markdown = ["# 불 관련 시각 의미 카드", "", "각 카드의 외형은 출처의 현상 경계 위에 설계한 선택적 실현이다. 용어 전체에 강제하지 않는다.",
                "맥락 카드에는 픽셀 gate를 만들지 않는다. 출처 수준은 SOURCES.json에 따로 표시했다.", ""]
    for domain in DOMAINS:
        markdown += [f"## {DOMAINS[domain]}", ""]
        for card in (c for c in cards if c["domain"] == domain):
            markdown += [f"### {card['id']} {card['label_ko']}", "",
                         f"분류: {card['visual_status']}. 연결 용어: {' · '.join(card['research_keyword_associations'])}.", ""]
            if card["renderable"]:
                markdown += [f"- {c['owner_role']}: {c['observable_form_en']}" for c in card["observable_components"]]
                markdown += ["", "관계: " + "; ".join(f"{r['subject']} → {r['type']} → {r['object']}" for r in card["relations"]) + ".", ""]
            else:
                markdown += [card["definition_or_context_ko"], ""]
            markdown += ["경계: " + card["confusion_boundaries"][0], ""]
            if card["source_ids"]:
                markdown += ["근거: " + ", ".join(f"[{source} {sources_by_id[source]['title']}]({sources_by_id[source]['url']})" for source in card["source_ids"]) + ".", ""]
            else:
                markdown += ["근거 수준: 연구자의 창작 제안 또는 문맥 분리 원칙. 특정 역사·과학·임상 정의의 검증으로 주장하지 않는다.", ""]
    (ROOT / "SEMANTIC-CARDS.md").write_text("\n".join(markdown) + "\n")
    source_md = ["# 출처와 근거 범위", "", "출처의 정의·경계와 본 조사의 구체적 시각 설계를 분리한다. 전문 접근이 제한된 경우 검색 문구 또는 저자 초록 범위를 명시한다.", ""]
    for source in sources:
        source_md += [f"## {source['id']} [{source['title']}]({source['url']})", "",
                      f"확인일: {source['accessed_date']}. 접근 수준: {source['access_level']}.", "",
                      *source["research_claims"], "", *["- " + note for note in source["limitations"]], ""]
    (ROOT / "SOURCES.md").write_text("\n".join(source_md) + "\n")
    print(json.dumps(stats, ensure_ascii=False))

if __name__ == "__main__":
    main()

