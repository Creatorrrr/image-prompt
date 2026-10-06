#!/usr/bin/env python3
"""Build research-only proposals. Never writes live skill assets or indexes."""
from pathlib import Path
from collections import Counter
import json, re, hashlib, sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
STATUS = "RESEARCH_DRAFT_NOT_ADOPTED"

def read(name):
    return json.loads((OUT / name).read_text())

def write(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

REUSE = {
    "uncanny_valley_local_mismatch": ("profile", "uncanny_coherence_mismatch"),
    "wongwi_identity_return": ("candidate", "korean_wongwi_unresolved_return"),
    "ghost_general_identity": ("profile", "human_ghost_identity_breach"),
    "mall_operational_absence": ("candidate", "liminal_empty_mall"),
    "liminal_maintained_use_gap": ("profile", "liminal_transition_use_gap"),
    "low_key_key_fill": ("candidate", "low_key"),
    "high_key_even_fill": ("candidate", "high_key"),
    "hard_light_shadow_edge": ("candidate", "hard_flash"),
    "soft_light_transition": ("candidate", "soft_window"),
    "backlight_source_separation": ("candidate", "backlight"),
    "rim_edge_localization": ("candidate", "rim_light"),
    "practical_visible_source": ("candidate", "mixed_daylight_tungsten"),
    "negative_space_reserved_region": ("candidate", "negative_space"),
    "frame_within_threshold": ("candidate", "frame_within_frame"),
    "dutch_camera_roll": ("candidate", "dutch_tilt_direction"),
    "low_angle_height": ("candidate", "pc_pc07_component_2"),
    "high_angle_height": ("candidate", "pc_pc11_component_2"),
    "deep_focus_dual_evidence": ("candidate", "deep_focus"),
    "shallow_focus_unresolved_back": ("candidate", "shallow_depth"),
    "mirror_shared_geometry": ("candidate", "appearing_only_in_reflection"),
    "returning_past_identity": ("profile", "human_ghost_identity_breach"),
}

SPECIAL_RELATIONS = {
    "reflection_pose_disagreement": [("shares_identity_with","reflected adult","physical adult"),("mouth_pose_differs_from","reflected mouth","physical mouth")],
    "shadow_independent_pose": [("cast_from","connected shadow","visible adult caster"),("pose_differs_from","shadow hand","caster hand")],
    "doppelganger_pair_divergence": [("matches_appearance_of","second adult","first adult"),("occupies_independent_position_from","second adult","first adult")],
    "translucent_body_occlusion": [("transmits_visible_structure_of","apparition torso","background rail")],
    "levitation_clearance": [("separated_by_visible_air_gap_from","both feet","floor")],
    "folk_horror_collective_boundary": [("limits_route_of","adult residents","adult visitor"),("isolates_alternative_routes_of","landscape","visitor")],
    "cosmic_incompatible_scale": [("provides_scale_for","small observer","vast environment"),("pattern_differs_from","water reflection","sky pattern")],
    "bodily_fusion_shared_junction": [("continuously_joins_at_visible_junction","organic tissue","metal structure")],
    "parasite_host_junction": [("attaches_at_visible_junction_to","distinct organism","host body")],
    "elevator_presence_comparison": [("contains_additional_presence_beyond","aligned reflection","physical elevator occupancy")],
    "recording_local_discrepancy": [("depicts_additional_presence_beyond","room recording","corresponding physical room")],
    "dust_removed_silhouette": [("locally_interrupts","clean human-shaped region","settled dust field")],
}

def main():
    seeds = read("SEED-INVENTORY.json")["rows"]
    slot_dimensions = read("CURRENT-CONTRACT.json")["slot_dimensions"]
    seed_by = {s["id"]: s for s in seeds}
    sources = {r["id"]: r for r in read("SOURCES.json")["records"]}
    units, candidates, mappings, coverage = [], [], [], []
    for filename in ("CARD-INPUT.psv","CARD-INPUT-2.psv"):
        for line in (OUT / filename).read_text().splitlines():
            if not line or line.startswith("#"):
                continue
            ref, slug, mode, slot, meaning, raw_parts, confound, raw_sources = line.split("|")
            seed_id = "seed_" + ref
            seed = seed_by[seed_id]
            parts = raw_parts.split("^^")
            uid = "hvr_" + slug
            refs = raw_sources.split(",")
            factual_gap = any(sources[s]["status"] in {"unavailable","reference_link_only"} for s in refs)
            relations = SPECIAL_RELATIONS.get(slug, [("jointly_visible_in_same_event", parts[0], " and ".join(parts[1:]) or "the declared comparison context")])
            relations = [{"id": f"relation_{n:02d}", "type": t, "subject": a, "object": b} for n,(t,a,b) in enumerate(relations,1)]
            static = mode in {"visual","reuse","variant_hold","bundle"}
            # The owner and effect records are research metadata. They are not added as new runtime keys.
            owner = ("declared actor and exact comparison target" if slot in {"relational_action","reflection_logic","gaze_target","contact_point"}
                     else "declared existing body and connected region" if slot in {"anatomical_connection","eye_detail","skin_condition","skin_finish","face_shape_relation","species_marker","body_pose"}
                     else "declared spatial plane, object, light source, or recording surface named by the components")
            components = [{"id": f"component_{n:02d}", "observable_predicate_en": p,
                           "owner_binding": owner, "review_scale": "native",
                           "evidence_field": f"component_{n:02d}_phrase"}
                          for n,p in enumerate(parts,1)]
            exact = "explicit_concrete_relation_only" if slug in SPECIAL_RELATIONS else "none_proposed_for_broad_seed_label"
            unit = {
                "id":uid, "seed_refs":[seed_id], "label":seed["label"], "section":seed["section"],
                "meaning_ko":meaning, "mode":mode, "proposed_slot":slot,
                "source_refs":refs, "source_support_scope":"Checked source claims only. Every concrete arrangement below is a research-authored visual proposal, not source prose or a mandatory definition.",
                "factual_verification":"SOURCE_GAP_RETAINED" if factual_gap else "SOURCE_FRAMEWORK_PARTIAL_ONLY",
                "whole_seed_row_verified":False,
                "components":components, "relations":relations,
                "confusion_boundaries":[x.strip() for x in confound.split(";")],
                "static_image_status":"PROPOSED_NOT_RENDERED" if static else "NO_DIRECT_STILL_IMAGE_PROOF",
                "exact_activation_proposal":exact,
                "candidate_adoption":"optional_after_core_only",
                "research_status":STATUS,
                "pixel_gates":[{"id":f"vo_{uid}_{n:02d}","description":p,"review_scale":"native"}
                               for n,p in enumerate(parts,1)] if static else [],
                "proof_limits":["A literal prompt phrase proves authored intent only.","A hidden or substituted required comparison is UNOBSERVABLE_NOT_PASS.","Perceptual fear strength and user preference remain separate from instruction fidelity."],
            }
            units.append(unit)
            candidate_id = None
            if mode in {"visual","variant_hold"}:
                candidate_id = "hr_" + slug
                entry = {"id":candidate_id,"ko":seed["label"].split("—")[0].strip(),"en":parts[0],"tags":[],
                         "concept_units":parts,"relations":relations,
                         "aliases":[],"keywords":[],
                         "embedding_text":"; ".join(parts)}
                candidates.append({
                    "id":candidate_id,"semantic_id":uid,"slot":slot,"entry_projection":entry,
                    "source_refs":refs,"adoption_ready":False,
                    "status":"HELD_FOR_VARIANT_SOURCE" if mode=="variant_hold" else STATUS,
                    "activation":"optional_postcore","broad_seed_alias_activation":False,
                    "effect_review":{"current_declared_slot_dimensions":slot_dimensions.get(slot,[]),"owner_binding":owner,
                                   "required_open_properties":"Check every component and relation against the current intent lock; this proposed slot alone is not permission.",
                                   "whole_scene_review":"Reject implicit added people, changed identity, clothing, light, objects, or timing that conflict with requester-owned meaning."},
                    "confusion_boundaries":unit["confusion_boundaries"],
                    "requires_pre_adoption":["Existing-ID deduplication","Concrete evidence and native gates","Current candidate schema and property-scope validation","Source-only metadata kept out of runtime entry"],
                })
            existing = []
            if slug in REUSE:
                kind, identity = REUSE[slug]
                existing = [{"kind":kind,"id":identity,"relation":"neighbor_to_refine_not_whole_seed_equivalence"}]
            priority = "P0" if slug in SPECIAL_RELATIONS or mode=="reuse" else "P1" if mode=="visual" else "P2_SOURCE_HOLD" if mode=="variant_hold" else "P3_CONTEXT_OR_OTHER_MEDIA"
            mappings.append({"semantic_id":uid,"mode":mode,"priority":priority,"existing_links":existing,
                             "candidate_draft_id":candidate_id,
                             "candidate_source_proposal":"assets/photo_prompt_horror_extension.json" if candidate_id else None,
                             "profile_source_proposal":"assets/photo_prompt_visual_obligations_horror.json" if static else None,
                             "registration":"Use only photo_prompt_source_manifest.json after deduplication; neither proposed file exists in live runtime for this package.",
                             "next_action":"Refine neighboring source preserving its meaning" if mode=="reuse" else "Research-only context; no automatic still-image requirement" if not static else "Review and deduplicate proposal before authoring live source"})
            coverage.append({"id":seed_id,"semantic_id":uid,"mode":mode,"source_refs":refs,
                             "whole_seed_row_verified":False,"research_decision":"retained_with_explicit_scope"})
    write("SEMANTIC-UNITS.json",{"schema_version":"horror-research-units/v1","status":STATUS,"units":units})
    write("CANDIDATE-DRAFTS.json",{"schema_version":"horror-research-candidate-proposals/v1","status":STATUS,"candidates":candidates})
    write("RUNTIME-MAPPING.json",{"schema_version":"horror-research-runtime-mapping/v1","mappings":mappings})
    write("SEED-COVERAGE.json",{"schema_version":"horror-research-seed-coverage/v1","rows":coverage})
    by_slug = {u["id"][4:]:u for u in units}
    bundle_specs = [
        ("korean_threshold_trace",["wongwi_identity_return","wet_hair_skin_contact","shroud_floor_drag","twilight_detail_threshold","bundle_korean_threshold_trace"]),
        ("clean_cctv_difference",["recording_local_discrepancy","high_key_even_fill","bundle_clean_cctv_difference"]),
        ("bright_folk_boundary",["folk_horror_collective_boundary","daylight_exposed_threat","palette_daylight_ritual","bundle_bright_folk_boundary"]),
        ("analog_instruction_gap",["analog_broadcast_intrusion","palette_display_limited","warning_rule_visual_context","bundle_analog_instruction_gap"]),
        ("cosmic_water_mismatch",["cosmic_incompatible_scale","palette_underwater_depth","negative_space_reserved_region","bundle_cosmic_water_mismatch"]),
        ("body_industrial_junction",["bodily_fusion_shared_junction","palette_flesh_steel","industrial_processing_route","bundle_body_industrial_junction"]),
        ("mirror_pose_disagreement",["reflection_pose_disagreement","mirror_shared_geometry","deep_focus_dual_evidence"]),
        ("independent_shadow_pose",["shadow_independent_pose","practical_visible_source","frame_within_threshold"]),
        ("physical_doppelganger",["doppelganger_pair_divergence","deep_focus_dual_evidence"]),
        ("water_ghost_variant",["water_ghost_variant","wet_hair_skin_contact","flooded_depth_uncertainty"]),
        ("tool_animacy",["tsukumogami_tool_agency","corrosion_used_touch_zone"]),
        ("giallo_witness_fragment",["giallo_partial_witness","incomplete_witness_fragment","palette_neon_opposed_sources"]),
    ]
    bundles=[]
    for n,(name, slugs) in enumerate(bundle_specs,1):
        members=[by_slug[s] for s in slugs]
        bundles.append({"id":f"hvb_{n:02d}_{name}","semantic_members":[u["id"] for u in members],
                        "member_draft_ids":["hr_"+s for s in slugs if any(c["id"]=="hr_"+s for c in candidates)],
                        "reuse_links":[link for s in slugs for link in next(m for m in mappings if m["semantic_id"]=="hvr_"+s)["existing_links"]],
                        "joint_components":[c["observable_predicate_en"] for u in members for c in u["components"]],
                        "relations":members[0]["relations"],"adoption":"optional",
                        "profile_activation":"independent_request_evidence_only",
                        "all_members_required_if_selected":True,
                        "status":"HELD_FOR_VARIANT_SOURCE" if any(u["mode"]=="variant_hold" for u in members) else STATUS,
                        "no_hard_activation_by_association":True,
                        "not_a_template":"Members may be declined. The six seed combinations are examples, not scene presets.",
                        "whole_scene_guard":"Resolve identity, actor count, material, view and effect ownership against frozen requester intent. Choose simultaneously visible evidence, and collapse duplicate units before runtime authoring."})
    write("BUNDLE-DRAFTS.json",{"schema_version":"horror-research-bundle-proposals/v1","bundles":bundles})
    palettes=[
        ("moon_ink",["#101419","#607685","#C7D0D5"],["background","depth layer","focal edge"]),
        ("mold_ward",["#7A8778","#D7D3B8","#714739"],["stain","tile","corroded metal"]),
        ("single_crimson",["#111111","#DED8C8","#8C1C24"],["background","pale surface","one focal accent"]),
        ("candle_night",["#211912","#B77836","#253C51"],["shadow","local light pool","far space"]),
        ("neon",["#B91F73","#168C95","#17121F"],["source-one receiving surface","source-two receiving surface","shadow"]),
        ("faded_photo",["#8C7359","#CBBDA3","#625A52"],["print","paper backing","fading within print"]),
        ("underwater",["#091B23","#285662","#A3BDB6"],["far depth","near water","submerged focal surface"]),
        ("clean_room",["#E8E7E2","#CADBE0","#202426"],["wall planes","fixtures","bounded opening"]),
        ("daylight_ritual",["#D6BD6B","#EEE8D8","#637D49"],["straw ground","flowers","leaves"]),
        ("flesh_machine",["#B58A80","#626A6D","#572C32"],["organic material","hardware","local junction"]),
        ("broadcast",["#193C8D","#78926B","#B7B8AE"],["display blue","display green","display gray"]),
        ("metal_monochrome",["#0C0C0C","#727272","#EAEAEA"],["dark matte","mid-tone surface","specular highlight"]),
    ]
    write("PALETTE-DRAFTS.json",{"schema_version":"horror-research-palettes/v1","origin":"Exact hex values transcribed from the reference's authored examples; owner assignment is this research's proposal.","fear_effect_verified":False,
                              "palettes":[{"id":"hpal_"+s,"hex":h,"proposed_owners":o,"adoption":"optional","numeric_hex_pixel_requirement":False} for s,h,o in palettes]})
    make_profiles(by_slug)
    make_regression(units)
    make_pixels(by_slug)
    counts={"seed_rows":len(seeds),"semantic_units":len(units),"candidate_drafts":len(candidates),
            "candidate_ready_for_live_adoption":0,"existing_neighbor_mappings":sum(bool(m["existing_links"]) for m in mappings),
            "bundle_drafts":len(bundles),"palettes":len(palettes),"sources":len(sources),
            "source_depth_counts":dict(Counter(s["status"] for s in sources.values())),
            "mode_counts":dict(Counter(u["mode"] for u in units)),
            "live_assets_changed_by_builder":0,"index_builds_run":0,"native_generations_run":0,
            "regression_cases_executed":0,"user_visual_acceptance":"NOT_REQUESTED_FOR_RESEARCH"}
    write("RESEARCH-STATS.json",counts)
    md=["# 호러 시각 의미 카드\n","2026-10-06 KST. 250개 입력 항목 전부를 유지한 연구용 카드다. 구체적인 연출은 독자 설계이며 원 출처의 권고나 고정 정의가 아니다. 후보·profile·영상/음향 계획의 실행과 이미지 성공은 아직 검증하지 않았다.\n"]
    section=None
    for u in units:
        if section!=u["section"]:
            section=u["section"];md.append("\n## 절 "+section+"\n")
        md.append("\n### "+u["id"]+" — "+u["label"]+"\n")
        md.append(u["meaning_ko"]+"\n")
        md.append("- 반영 구분: "+u["mode"]+"; 원본 슬롯 제안: "+u["proposed_slot"]+".\n")
        md.append("- 관찰 구성: "+" / ".join(c["observable_predicate_en"] for c in u["components"])+".\n")
        md.append("- 관계: "+"; ".join(r["subject"]+" → "+r["type"]+" → "+r["object"] for r in u["relations"])+".\n")
        md.append("- 혼동 경계: "+"; ".join(u["confusion_boundaries"])+".\n")
        md.append("- 정지 이미지 증거: "+u["static_image_status"]+"; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.\n")
        md.append("- 근거 범위: "+", ".join("["+s+"](SOURCES.md#"+s.lower()+")" for s in u["source_refs"])+"; "+u["factual_verification"]+". 전체 seed 사실 검증은 아님.\n")
    (OUT/"SEMANTIC-CARDS.md").write_text("".join(md))
    md=["# 출처 및 읽기 범위\n","각 링크의 확인 문장만 그 읽기 수준으로 확인했다. 카드의 구체적인 장면은 연구자가 설계한 제안이다. 원문 일부 또는 메타데이터의 확인을 모든 키워드의 사실 검증으로 집계하지 않는다.\n"]
    for s in sources.values():
        md.append("\n<a id=\""+s["id"].lower()+"\"></a>\n## "+s["id"]+" — "+s["title"]+"\n\n")
        md.append("["+s["publisher"]+"]("+s["url"]+") · "+s["status"]+" · "+s["kind"]+"\n\n"+s["checked_claim"]+"\n\n한계: "+s["limits"]+"\n")
    (OUT/"SOURCES.md").write_text("".join(md))
    print(json.dumps(counts,ensure_ascii=False))

def make_profiles(by):
    prototypes=[]
    for slug in ("reflection_pose_disagreement","shadow_independent_pose","folk_horror_collective_boundary"):
        u=by[slug]; comps=u["components"]
        evidence=[{"field":c["evidence_field"],"requirement":{"min_content_words":3,"must_mention_any":[c["observable_predicate_en"]]}} for c in comps]
        profile={"id":"hvr_profile_"+slug,"category":"relational_horror_proposal",
                 "activation":{"exact_terms":["; ".join(c["observable_predicate_en"] for c in comps)],
                               "requires_adult_character":True,"semantic_discovery_requires_component_evidence":True},
                 "semantics":{"definition":u["meaning_ko"],"paraphrase_examples":["; ".join(c["observable_predicate_en"] for c in comps)],"contrast_examples":u["confusion_boundaries"]},
                 "concept_candidate":{"concept_terms":[c["observable_predicate_en"] for c in comps]},
                 "runtime_expression":{"default_mode":"definition_only","prompt_label_terms":[],"forbidden_prompt_terms":[],"runtime_forbidden_labels":[]},
                 "reject_substitutes":u["confusion_boundaries"],
                 "authored_components":{
                     "contract_version":"photo-authored-visual-components/v2",
                     "components":[{"id":c["id"],"match_terms":[c["observable_predicate_en"]]} for c in comps],
                     "discovery":{"minimum_component_groups":len(comps),"required_group_ids":[c["id"] for c in comps]},
                     "obligations":[{"component_ids":[c["id"] for c in comps],"evidence":evidence,
                                    "instruction":"Keep all compared owners jointly visible within the same coherent scene. "+"; ".join(c["observable_predicate_en"] for c in comps)+".",
                                    "render_gates":[{"id":g["id"],"review_scale":g["review_scale"],"description":"The original saved image must visibly show "+g["description"]+". A hidden owner or partial comparison fails."} for g in u["pixel_gates"]]}]
                 }}
        prototypes.append({"semantic_id":u["id"],"profile":profile,"status":"COMPILER_PROTOTYPE_NOT_REGISTRY_QUALIFIED","adoption_ready":False})
    write("PROFILE-PROTOTYPES.json",{"schema_version":"horror-research-profile-prototypes/v1","prototypes":prototypes})

def make_regression(units):
    cases=[]
    for u in units:
        if u["mode"] not in {"visual","reuse","variant_hold"}:
            continue
        cases.extend([
            {"id":u["id"]+"_ko","semantic_id":u["id"],"kind":"lexical_context_positive","query":u["label"]+"。"+u["meaning_ko"],"expected":"Meaning preserved; broad label alone remains insufficient for hard activation."},
            {"id":u["id"]+"_en","semantic_id":u["id"],"kind":"component_paraphrase_development","query":"; ".join(c["observable_predicate_en"] for c in u["components"]),"expected":"Optional discovery may expose the complete relation; score or rank creates no hard duty."},
            {"id":u["id"]+"_negative","semantic_id":u["id"],"kind":"adjacent_hard_negative","query":u["confusion_boundaries"][0],"expected":"This substitute alone must not establish the target meaning or satisfy its required comparison."},
            {"id":u["id"]+"_missing","semantic_id":u["id"],"kind":"selection_to_pixel_mutation","query":"Remove or occlude "+u["components"][0]["observable_predicate_en"],"expected":"If selected or independently required, missing literal or native evidence fails the complete contract."},
        ])
    controls=[
        ("ghostwriter","ghostwriter editing a book"),("ghosting_messages","a friend ghosting text messages"),
        ("ghost_kitchen","a ghost kitchen cooking a meal"),("lens_ghosting","optical lens ghosting aligned with a lamp"),
        ("dark_fashion","an adult wearing black gothic lace in ordinary daylight"),
        ("clean_office","an ordinary clean occupied office"),("no_people","an empty corridor with no people or creatures"),
        ("no_gore","horror scene with no gore, based on a mirror mismatch"),
        ("quoted_horror_term","an essay discussing the word horror, with no image-generation request"),
        ("ordinary_twins","two ordinary adult twins with matching clothes"),
        ("ordinary_shadow","one adult's physically consistent shadow beneath a lamp"),
        ("high_key_detail","a bright high-key image retaining white fabric detail"),
        ("deep_staging_shallow_focus","a deep hallway whose rear figure remains blurred"),
        ("audio_only","an ostinato and a non-diegetic drone in a soundtrack"),
    ]
    write("REGRESSION-PLAN.json",{"schema_version":"horror-research-regression-plan/v1","status":"PLANNED_NOT_EXECUTED","development_cases":cases,
          "global_controls":[{"id":i,"query":q,"expected":"Do not activate unrelated new horror duties; preserve explicit requester definitions and exclusions."} for i,q in controls],
          "source_authored_cases":len(cases),"independent_holdouts":0,
          "holdout_policy":"Author fresh whole requests before implementation; do not treat these source-derived examples as independent evidence.",
          "additional_contract_cases":["exact/approximate lane separation","negation and quoted-text scope","same-owner identity binding","conditional visibility","property lock","subject count and no-people","stale source/index hash","literal relation and every selected bundle component","strict gate-set parity"]})

def make_pixels(by):
    specs=[
        ("mirror",["reflection_pose_disagreement","mirror_shared_geometry"]),
        ("shadow",["shadow_independent_pose","practical_visible_source"]),
        ("doppelganger",["doppelganger_pair_divergence"]),
        ("reflection_count",["elevator_presence_comparison"]),
        ("cctv_count",["recording_local_discrepancy"]),
        ("transparency",["translucent_body_occlusion"]),
        ("levitation",["levitation_clearance"]),
        ("folk_daylight",["folk_horror_collective_boundary","daylight_exposed_threat"]),
        ("cosmic",["cosmic_incompatible_scale"]),
        ("tool",["tsukumogami_tool_agency"]),
        ("dokkaebi",["dokkaebi_object_origin"]),
        ("body_fusion",["bodily_fusion_shared_junction"]),
        ("parasite",["parasite_host_junction"]),
        ("body_melt",["body_melt_support_loss"]),
        ("giallo",["giallo_partial_witness"]),
        ("low_key",["low_key_key_fill"]),
        ("high_key",["high_key_even_fill"]),
        ("underlight",["underlight_face_planes"]),
        ("one_red",["palette_single_crimson"]),
        ("broadcast_plane",["analog_broadcast_intrusion","palette_display_limited"]),
        ("dust",["dust_removed_silhouette"]),
        ("wet_hair_variant",["water_ghost_variant","wet_hair_skin_contact"]),
    ]
    write("PIXEL-QUALIFICATION-PLAN.json",{"schema_version":"horror-research-pixel-plan/v1","status":"PLANNED_NOT_EXECUTED","native_generations_run":0,
        "case_groups":[{"id":name,"semantic_ids":["hvr_"+s for s in ss],
                       "gates":[g for s in ss for g in by[s]["pixel_gates"]],
                       "status":"SOURCE_HOLD" if any(by[s]["mode"]=="variant_hold" for s in ss) else "PROPOSED_NOT_RUN",
                       "minimum_view":"All compared owners and relevant joints, floor contacts, optical planes, or source directions must be simultaneously visible.",
                       "evaluation":{"partial_is_fail":True,"hidden_required":"UNOBSERVABLE_NOT_PASS","moderation_blocked":"BLOCKED_UNSCORED","sound_or_duration_in_still":"NOT_OBSERVABLE","prompt_audit_is_pixel_proof":False}}
                       for name,ss in specs],
        "arms":["A: preserved pre-adoption baseline, independently authored before local retrieval","B: same requester meaning with reviewed optional new data","C: separately declared adjacent-confusion control, not an improvement comparator"],
        "execution_boundary":"Future user-authorized rendering only. Record exact request/core/lock, candidate exposure, selection, literal prompt, audit/runtime bytes, output hash, original pixels and user judgment. A/B causal inference requires compatible generation conditions and a frozen comparator; C measures discrimination only."})

if __name__=="__main__":
    main()
