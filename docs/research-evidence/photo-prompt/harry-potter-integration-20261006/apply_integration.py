#!/usr/bin/env python3
"""Apply reviewed equivalent expressions and morphology to an isolated checkout."""
from __future__ import annotations
import argparse, copy, csv, hashlib, json
from collections import defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
RESEARCH = OUT.parent / "harry-potter-appearance-20261006"
NEW_CANDIDATES = "photo_prompt_character_appearance_extension.json"
NEW_PROFILES = "photo_prompt_visual_obligations_appearance_relations.json"
LABELS = {"H003":"같은 후드의 대비되는 안팎 면과 연속 가장자리",
          "H043":"어두운 윗머리와 밝은 옆·아래 모발의 색 영역",
          "H051":"한 얼굴 피부에 분산된 작은 색점",
          "H075":"선택한 얼굴 범위와 눈 구멍을 갖는 별도 가면",
          "H090":"긴 천 코트의 넓은 어깨와 대비되는 테두리"}

# These are explicitly reviewed owner/property scopes, not imported draft paths.
SCOPES = {
 "H001":("costume_style",[("appearance","wardrobe.outer_garment.structure")]),
 "H002":("garment_detail",[("appearance","wardrobe.layering")]),
 "H003":("garment_detail",[("appearance","wardrobe.details.hood_attachment"),("appearance","wardrobe.color.hood_inside")]),
 "H004":("garment_detail",[("appearance","wardrobe.details.tie_topology"),("appearance","wardrobe.color.tie_stripes")]),
 "H005":("garment_detail",[("appearance","wardrobe.details.knit_edge_trim"),("appearance","wardrobe.color.knit_trim")]),
 "H006":("garment_detail",[("appearance","wardrobe.details.chest_emblem")]),
 "H009":("garment_detail",[("appearance","wardrobe.layering.short_shoulder_cover")]),
 "H013":("garment_detail",[("appearance","wardrobe.details.chest_jabot")]),
 "H014":("garment_detail",[("appearance","wardrobe.details.vest_crest"),("material","wardrobe.surface.vest_padding"),("appearance","wardrobe.layering.vest_cloak")]),
 "H016":("wearable_accessory",[("appearance","wardrobe.details.handwear.cardinality")]),
 "H018":("garment_detail",[("appearance","wardrobe.details.wear_edges"),("material","wardrobe.surface.wear_state")]),
 "H023":("garment_detail",[("appearance","wardrobe.details.chest_monogram"),("material","wardrobe.surface.knit_loops")]),
 "H027":("garment_detail",[("appearance","wardrobe.details.short_skirt.projecting_tiers")]),
 "H028":("garment_detail",[("appearance","wardrobe.details.paired_bird_motif_heart")]),
 "H037":("hair_style",[("appearance","hair.style.short_tip_directions")]),
 "H038":("hair_style",[("appearance","hair.style.volume_flyaway")]),
 "H040":("hair_style",[("appearance","hair.style.backward_direction"),("appearance","hair.surface.dry_looking_strands")]),
 "H041":("hair_style",[("appearance","hair.style.large_wave_continuity")]),
 "H042":("hair_style",[("appearance","hair.style.ringlet_continuity")]),
 "H043":("hair_color",[("appearance","hair.color.region_placement")]),
 "H045":("hair_style",[("appearance","hair.style.single_bun_attachment")]),
 "H048":("wearable_accessory",[("appearance","wardrobe.details.eyewear.round_rims_bridge")]),
 "H049":("wearable_accessory",[("appearance","wardrobe.details.eyewear.half_moon_rims")]),
 "H050":("eye_detail",[("appearance","face.eyes.lens_bounded_magnification")]),
 "H051":("skin_condition",[("appearance","face.skin.localized_dot_pattern")]),
 "H058":("body_marking",[("appearance","face.skin.forehead.angular_scar_path")]),
 "H061":("eye_detail",[("body_geometry","face.eyes.replacement_interface"),("appearance","face.eyes.replacement_surface")]),
 "H063":("anatomical_connection",[("body_geometry","body.hand.replacement_connection"),("appearance","body.hand.replacement_surface")]),
 "H065":("body_marking",[("appearance","body.skin.forearm.skull_serpent_motif")]),
 "H075":("wearable_accessory",[("appearance","wardrobe.accessories.mask.coverage_apertures")]),
 "H076":("wearable_accessory",[("appearance","wardrobe.accessories.mask.incised_ornament"),("material","wardrobe.accessories.mask.surface.reflection")]),
 "H077":("wearable_accessory",[("appearance","wardrobe.accessories.necklace.hourglass_ring_topology")]),
 "H078":("wearable_accessory",[("appearance","wardrobe.accessories.necklace.cork_attachment")]),
 "H079":("wearable_accessory",[("appearance","wardrobe.accessories.earring.root_fruit_attachment")]),
 "H080":("wearable_accessory",[("appearance","wardrobe.accessories.earring.star_attachment")]),
 "H082":("wearable_accessory",[("appearance","wardrobe.accessories.hat.lion_object_support")]),
 "H083":("prop",[("appearance","prop.pouch.structure"),("material","prop.pouch.bead_surface")]),
 "H087":("wearable_accessory",[("appearance","wardrobe.accessories.earring.hoop_attachment")]),
 "H090":("garment_detail",[("appearance","wardrobe.details.coat.shoulder_outline"),("appearance","wardrobe.color.coat_edge_contrast")]),
 "H093":("expression",[("expression","face.expression.eyelid_openness"),("expression","face.expression.mouth_corner_asymmetry")]),
 "H106":("hair_style",[("appearance","hair.style.gathering_point"),("appearance","wardrobe.accessories.hair.ribbon_attachment")]),
 "H120":("hair_color",[("appearance","hair.color.pale_low_yellow_hue")]),
}
CANDIDATE_EQUIVALENTS = {
 "blonde_long_hair":["long light-blonde hair extending down from the scalp","두피에서 길게 내려오는 밝은 금발"],
 "slicked_back_wet":["wet-looking hair strands slicked rearward over the scalp","젖은 듯한 모발 결이 두피를 따라 뒤로 붙어 눕는다"],
 "silver_blonde_gothic_hair":["cool silver-blonde hair within the selected gothic styling","선택한 고딕 스타일의 차가운 은빛 금발"],
 "faded_blonde_rooted_hair":["faded blonde lengths with darker scalp-side roots still visible","바랜 금발 길이 위에 두피 쪽의 더 어두운 뿌리색이 보인다"],
 "playful_smirk":["a playfully uneven small smile","장난스러운 비대칭의 작은 웃음"],
 "wireframe_round_glasses":["a pair of round eyeglass lenses surrounded by slim wire rims","한 쌍의 둥근 안경 렌즈 둘레에 가는 금속선 테가 있다"],
 "full_beard":["a full covering of beard hair around the lower face","얼굴 아래쪽을 넓게 덮는 풍성한 수염"],
 "translucent_spirit_glow_surface":["a translucent softly luminous spirit-like surface","빛이 은은하게 번지는 반투명한 영체 같은 표면"],
 "velvet_fabric_surface":["soft dense textile pile with velvet-like directional sheen","벨벳 같은 방향성 광택을 내는 부드럽고 빽빽한 천 기모"],
 "sheer_organza_chiffon_transmission":["light passes through fine organza or chiffon with readable fabric threads and edges","천의 실 조직과 가장자리가 읽히는 얇은 오간자나 시폰으로 빛이 비친다"],
 "brocade_raised_supplementary_weft_surface":["raised supplementary pattern yarns lie over a separate woven brocade ground","별도 브로케이드 바탕 직조 위로 추가 무늬 실이 도드라진다"],
 "pleat_fold_ridge_valley_geometry":["repeated real cloth folds retain ridges valleys and separate moving layer edges","실제로 접힌 천의 반복 주름에 능선과 골 및 따로 움직이는 층 가장자리가 남는다"],
 "ca_cap_projections":["two pointed cap-shell projections have bases connected to the same cap surface","같은 모자 표면에 밑동이 이어진 뾰족한 돌출부 두 개가 있다"],
 "bm_scar_surface":["a local scar-like line or patch differs in both color and surface relief","국소 흉터 같은 선이나 반점에 색과 표면 높낮이 차이가 함께 있다"],
}

def read(name):
    return json.loads((RESEARCH / name).read_text())
def psv(name):
    return list(csv.DictReader((OUT / name).open(), delimiter="|"))
def append(values, additions):
    return list(dict.fromkeys([*values, *additions]))
def save(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+"\n")
def digest(obj):
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--checkout",required=True);args=ap.parse_args()
    root=Path(args.checkout).resolve();assets=root/"skills/photo-prompt-image-generator/assets"
    documents={p.name:json.loads(p.read_text()) for p in assets.glob("photo_prompt_visual_obligations*.json")}
    owners={p["id"]:(name,p) for name,d in documents.items() for p in d.get("profiles",[])}
    changes=[];changed_files=set()
    equivalent_rows=psv("EXISTING-EXPRESSIONS.psv")
    for row in equivalent_rows:
        name,p=owners[row["id"]];before=copy.deepcopy(p);forms=[row["en"],row["ko"]]
        p["semantics"]["paraphrase_examples"]=append(p["semantics"].get("paraphrase_examples",[]),forms)
        if p.get("concept_candidate"):
            p["concept_candidate"]["concept_terms"]=append(p["concept_candidate"].get("concept_terms",[]),forms)
        authored=p["authored_components"]
        # One component really owns the whole relation; collective v2 remains intact.
        if authored["contract_version"].endswith("/v1") and len(authored["components"])==1:
            c=authored["components"][0]
            c["match_terms"]=append(c["match_terms"],forms)
            c["evidence_terms"]=append(c["evidence_terms"],forms)
        assert before["activation"]==p["activation"]
        original_path=OUT/"before/skills/photo-prompt-image-generator/assets"/name
        original=next(q for q in json.loads(original_path.read_text())["profiles"] if q["id"]==p["id"])
        changes.append({"id":p["id"],"file":name,"kind":"EQUIVALENT_EXPRESSIONS_ONLY","forms_added":forms,
                        "before_profile_sha256":digest(original),"activation_unchanged":True})
        changed_files.add(name)
    for row in psv("EXISTING-COMPONENT-EXPRESSIONS.psv"):
        name,p=owners[row["id"]];authored=p["authored_components"]
        assert authored["contract_version"].endswith("/v1"),row["id"]
        c=next(c for c in authored["components"] if c["id"]==row["component"])
        c["match_terms"]=append(c["match_terms"],[row["en"],row["ko"]])
        c["evidence_terms"]=append(c["evidence_terms"],[row["en"],row["ko"]])
        changed_files.add(name)
    for name in changed_files:save(assets/name,documents[name])

    units={r["id"]:r for r in read("SEMANTIC-UNITS.json")["units"]}
    entry_map={}
    for path in [assets/"photo_prompt_tags.json",*sorted(assets.glob("photo_prompt*extension*.json"))]:
        if path.name==NEW_CANDIDATES:continue
        for slot,rows in json.loads(path.read_text()).get("slots",{}).items():
            for r in rows:
                if r["id"] in CANDIDATE_EQUIVALENTS:entry_map[r["id"]]=(slot,path.name)
    assert set(entry_map)==set(CANDIDATE_EQUIVALENTS)
    context_updates=defaultdict(dict)
    for eid,forms in CANDIDATE_EQUIVALENTS.items():
        slot,source=entry_map[eid];context_updates[slot][eid]={"paraphrases":forms}
    new_profiles=[];new_slots=defaultdict(list);new_records=[]
    for row in psv("NEW-EXPRESSIONS.psv"):
        sid=row["id"];unit=units[sid];label=LABELS.get(sid,unit["label_ko"])
        en=[x.strip() for x in row["alternate_components_en"].split(";")]
        ko=row["components_ko"].split("~");assert len(en)==len(ko)==3
        full_en="; ".join(en)+".";full_ko="; ".join(ko)+"."
        pid="appearance_rel_"+sid.lower();eid="appearance_"+sid.lower()
        slot,scope=SCOPES[sid];dimensions=list(dict.fromkeys(d for d,_ in scope))
        effects=[{"dimension":d,"target":"main_subject","property":p} for d,p in scope]
        precise_forms=[full_en,row["alternate_ko"]]
        approximate_forms=[unit["positive_definition_en"],full_ko,unit["decomposition_ko"]]
        exact_normalized={" ".join(v.casefold().split()) for v in precise_forms}
        approximate_forms=[v for v in approximate_forms if " ".join(v.casefold().split()) not in exact_normalized]
        profile={
          "id":pid,"category":"observable_appearance_component_relation",
          "activation":{"exact_terms":precise_forms,"requires_adult_character":False,
                        "semantic_discovery_requires_component_evidence":True,
                        "hard_activation":{"contract_version":"photo-visual-hard-activation/v1",
                                           "required_any_groups":[{"id":"selected_complete_relation","any_terms":precise_forms}]}},
          "semantics":{"definition":full_en,"paraphrase_examples":approximate_forms,
                       "visual_components":en,"contrast_examples":unit["confusion_boundaries"],
                       "claim_limits":["Only the explicitly selected complete morphology applies; approximate discovery stays advisory.",
                                      "Preserve the declared carrier, source version, reference use and all dimension/property locks.",
                                      "Color, anatomy, age, identity, material chemistry, motion and narrative cause require their own declared scope.",
                                      "Every selected component and owned relation must be visible at native resolution; partial evidence fails and occlusion is unobservable."]},
          "authored_components":{"contract_version":"photo-authored-visual-components/v1","components":[
            {"id":"component_"+str(i+1),"match_terms":[e,k],"evidence_field":"component_"+str(i+1)+"_phrase",
             "evidence_terms":[e,k],"min_content_words":3,
             "instruction":"Preserve this selected component on its own declared carrier: "+e+".",
             "render_gate":{"id":"vo_"+pid+"_"+str(i+1),"review_scale":"native",
                            "description":"Observe this component and its stated carrier in original pixels: "+e+". Required hidden evidence is unobservable and partial realization fails."}}
             for i,(e,k) in enumerate(zip(en,ko))]},
          "concept_candidate":{"concept_terms":[label,*precise_forms],"core_assertion_discovery":True,
                               "affected_dimensions":dimensions,"affected_properties":effects},
          "runtime_expression":{"default_mode":"definition_with_optional_label","prompt_label_terms":[],"forbidden_prompt_terms":[],"runtime_forbidden_labels":[]},
          "reject_substitutes":unit["confusion_boundaries"]}
        # The morphological carrier, not a character name or genre, owns each edge.
        edges=[{k:r[k] for k in ("id","type","subject","object")} for r in unit["relations"]]
        if any(r.get("endpoint_mapping_status") for r in unit["relations"]):
            edges=[{"id":"component_owner_"+str(i+1),"type":"owned_visible_predicate","subject":"declared_main_subject_carrier","object":e}
                   for i,e in enumerate(en)]
        entry={"id":eid,"ko":label,"en":full_en,"weight":0.35,
               "aliases":[row["alternate_ko"]],"paraphrases":[full_ko,row["alternate_ko"]],
               "keywords":[*en,*ko],"embedding_text":" | ".join([full_en,full_ko,row["alternate_ko"]]),
               "concept_units":en,"relations":edges,"tags":["human","observable_relation"],"for_any":["human"],
               "affected_dimensions":dimensions,"affected_properties":effects,"core_assertion_discovery":True}
        new_profiles.append(profile);new_slots[slot].append(entry)
        new_records.append({"semantic_id":sid,"profile_id":pid,"candidate_id":eid,"slot":slot,"owner":"main_subject",
                            "effects":effects,"source_refs":unit["source_refs"],"canon_scope":"Generic observed morphology only; no whole seed-row canon claim.",
                            "status":"NEW_REVIEWED_COMPONENT_RELATION"})
    assert len(new_profiles)==len(SCOPES)==42
    bundle_specs=[
      ("appearance_same_wearer_uniform",["H002","H003","H004","H005","H006"],"separate shirt tie knit and robe layers on one wearer"),
      ("appearance_quilted_duelling_layers",["H013","H014","H016"],"front-hanging jabot and quilted vest are separate components of one selected ensemble"),
      ("appearance_bird_motif_and_star_ornament",["H028","H080"],"paired bird motifs belong to the bodice while the star ornament belongs to the ear"),
      ("appearance_mask_incisions",["H075","H076"],"mask coverage and incised surface ornament belong to one selected mask"),
      ("appearance_hourglass_and_hoop",["H077","H087"],"a ringed hourglass hangs at the neck while the closed hoop hangs at the ear"),
      ("appearance_two_region_hair_and_ribbon",["H043","H106"],"hair color regions and a ribbon at the gathering point belong to one hairstyle")]
    bundles=[]
    for bid,members,proposition in bundle_specs:
        bundles.append({"id":bid,"primary_visual_proposition":proposition,
          "candidate_only":True,"activation_mode":"candidate_only","establishment":"optional",
          "terms":[proposition],"hard_profile_ids":["appearance_rel_"+sid.lower() for sid in members],
          "candidate_ids":["appearance_"+sid.lower() for sid in members],
          "candidate_slots":{"appearance_"+sid.lower():SCOPES[sid][0] for sid in members},
          "component_groups":[{"id":sid.lower()+"_c"+str(j+1),"visible_evidence":[predicate]}
                              for sid in members for j,predicate in enumerate(next(e for e in new_slots[SCOPES[sid][0]] if e["id"]=="appearance_"+sid.lower())["concept_units"])],
          "confusion_boundaries":["Association and bundle selection never activate a profile without independent requester evidence.","Apply only selected complete components with their declared carriers and property effects."],
          "relations":[{"id":"separate_carriers","type":"preserve_declared_owners","subject":"selected_components","object":"their_individually_declared_carriers"}]})
    save(assets/NEW_CANDIDATES,{"schema_version":"photo-prompt-research-extension/v1","slots":dict(new_slots),
                              "existing_slot_context_extensions":dict(context_updates),"visual_semantics":bundles})
    save(assets/NEW_PROFILES,{"schema_version":"photo-visual-obligation-registry-extension/v1",
                            "relation_contract_version":"photo-visual-relation/v1","profiles":new_profiles})
    manifest_path=assets/"photo_prompt_source_manifest.json";manifest=json.loads(manifest_path.read_text())
    for file,kind in [(NEW_CANDIDATES,"candidate"),(NEW_PROFILES,"visual_profile")]:
        # Preserve the existing standalone-registry policy: profile extension
        # files are optional at load time; the full runtime's index hash seals
        # the complete installed profile corpus. Candidate files remain required.
        required=kind=="candidate"
        if not any(r["file"]==file for r in manifest["sources"]):
            order=max(r["load_order"] for r in manifest["sources"] if r["kind"]==kind)+1
            manifest["sources"].append({"file":file,"kind":kind,"required":required,"load_order":order})
        else:
            next(r for r in manifest["sources"] if r["file"]==file)["required"]=required
    save(manifest_path,manifest)
    edited=sorted([*changed_files,NEW_CANDIDATES,NEW_PROFILES,manifest_path.name])
    manifest_record={"status":"AUTHORED_NOT_YET_INDEXED_OR_RENDERED","checkout":str(root),"source_files_changed":edited,
      "existing_profiles_extended":len(equivalent_rows),"existing_profile_component_rows_extended":len(psv("EXISTING-COMPONENT-EXPRESSIONS.psv")),
      "existing_candidates_extended":len(CANDIDATE_EQUIVALENTS),"new_profiles":len(new_profiles),"new_candidates":len(new_records),"optional_bundles":len(bundles),
      "existing_profile_updates":changes,"new_units":new_records,
      "seed_rows_are_not_canon_templates":True,"no_runtime_code_changes":True}
    save(OUT/"ADOPTION-MANIFEST.json",manifest_record)
    print(json.dumps({k:manifest_record[k] for k in ["existing_profiles_extended","existing_profile_component_rows_extended","existing_candidates_extended","new_profiles","new_candidates","optional_bundles","source_files_changed"]},ensure_ascii=False))

if __name__=="__main__":main()
