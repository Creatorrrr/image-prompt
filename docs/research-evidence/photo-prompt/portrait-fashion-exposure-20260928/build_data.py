"""Maintenance-only authored research and deterministic runtime projection.

Sources justify terminology; these all-of relations are authored proposals.
This file is not a pre-core prompt source or a rendered-quality claim.
"""
import hashlib
import json
from pathlib import Path
from addendum_data import NEW_SPECS, NEW_EXTRA, NEW_BUNDLES

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


# name, Korean label, related discovery terms, owner, slot, dimensions,
# positive components, adjacent negatives, source IDs, specific limitation.
SPECS = [
    ("cleavage", "목선 안에서 보이는 가슴골", ["가슴골", "cleavage", "intermammary contour"],
     "central upper-chest contour inside the declared neckline", "garment_detail", ["appearance"],
     ["a central depression between the breasts is visible inside the adult subject's neckline",
      "the neckline edges remain attached to a continuous constructed garment",
      "the central skin contour stays distinguishable from fabric folds and cast shadows"],
     ["deep V neckline without a central skin depression", "large bust alone", "clavicle shadow", "a painted black line on fabric", "mineral cleavage"],
     ["S01", "S02"], "크기·좌우 대칭·골의 깊이·관능성은 요구하지 않는다. 목선과 피부 표면의 소유권만 판별한다."),
    ("back_face", "열린 등과 돌아본 얼굴의 동시 가독성", ["백리스", "open-back portrait", "backless", "over-the-shoulder glance"],
     "open-back garment boundary and the same adult subject's face", "subject_framing", ["appearance", "pose", "framing"],
     ["the open back is bounded by visible garment edges on the same adult torso",
      "the returned face remains readable beside the exposed back in the same frame",
      "the head neck shoulders and torso connect continuously through the turn"],
     ["a rear portrait with the face entirely hidden", "a front neckline substituted for the back opening", "a detached head turned beyond the neck connection"],
     ["S08", "S11"], "얼굴 포함은 이 좁은 구성의 선택 조건이다. backless라는 단어만으로 모든 사진에 얼굴이나 특정 각도를 강제하지 않는다."),
    ("cowl", "목선에 매달린 카울 드레이프", ["카울넥", "cowl neck", "draped neckline"],
     "fabric folds belonging to the neckline opening", "garment_detail", ["appearance", "material"],
     ["soft hanging folds descend between the neckline's visible attachment points",
      "the folded edge belongs to the same continuous garment opening",
      "fold depth and contact shadows keep the fabric separate from the underlying surface"],
     ["an independent scarf placed over a plain neckline", "ruching gathered at a fixed seam", "a drawn V stripe", "a raised knitted cowl collar"],
     ["S11", "S18", "S05"], "낮게 늘어지는 드레스 카울을 다룬다. 두꺼운 니트 카울 칼라와 구분하며 재단 방향은 픽셀에서 확정하지 않는다."),
    ("halter", "목 주변으로 연결되는 홀터 지지", ["홀터넥", "halter neck", "neck-supported straps"],
     "halter strap path between bodice and neck", "garment_detail", ["appearance"],
     ["the bodice connects to a strap or fabric band passing around the neck",
      "the shoulders remain outside that visible neck-supported path",
      "strap joins and garment contact remain continuous on the same adult subject"],
     ["two ordinary shoulder straps", "a necklace detached from the bodice", "an open back without a neck support", "a scarf over a strapless top"],
     ["S17", "S06"], "사전의 전형적 목 지지와 일반 형태 지식에 기반한 설계이다. 등·복부가 항상 드러난다는 상의 정의를 모든 홀터 드레스에 강제하지 않는다."),
    ("one_shoulder", "원숄더의 비대칭 지지 경로", ["원숄더", "one-shoulder", "asymmetric neckline"],
     "one shoulder-supported garment edge and the opposite shoulder", "garment_detail", ["appearance"],
     ["one garment support passes over a single shoulder of the adult subject",
      "the opposite shoulder is outside the same asymmetrical neckline edge",
      "the diagonal garment edge and its attachment remain visibly continuous"],
     ["two straps partly hidden by hair", "both shoulders below an off-shoulder neckline", "asymmetric hair over a symmetric top"],
     ["S18", "S12"], "비대칭과 원숄더는 동의어가 아니다. 여러 가는 끈이 한 어깨를 지지할 수도 있으므로 끈 개수 대신 지지하는 어깨를 판별한다."),
    ("skimming", "몸을 따라 흐르면서 여유가 남는 핏", ["보디스키밍", "body-skimming", "fluid body-following drape"],
     "garment surface relative to torso and hip contour", "wardrobe_style", ["appearance", "material"],
     ["the garment follows the adult torso and hip contour with local hanging ease",
      "continuous folds bridge between contact areas rather than compressing every body plane",
      "the hem and side edges remain visible as a separate textile layer"],
     ["uniform tight compression without hanging ease", "a loose sack with no body-following contour", "a satin highlight alone", "assumed bias grain from silhouette"],
     ["S05", "S07"], "bodycon과 겹칠 수 있는 연속적인 핏이다. 보이지 않는 바이어스 재단, 섬유 종류, 보정 정도를 확정하지 않는다."),
    ("ruching", "지정 부위에 고정되는 루싱", ["루싱", "ruching", "ruched detail", "gathered seam"],
     "localized gathered fabric and its seam or attachment", "garment_detail", ["appearance", "material"],
     ["small repeated folds converge into the declared gathered seam or attachment",
      "the gathering stays localized within the same adult garment panel",
      "surrounding fabric remains continuous through the gathered region"],
     ["unanchored wrinkles across the entire dress", "regular pleats with no localized gathering", "skin compression lines", "floating cords unrelated to fabric"],
     ["S12", "S14"], "루싱 위치는 요청에서 정한다. 모든 주름, 드레이프, 플리츠를 같은 항목으로 취급하지 않는다."),
    ("slit", "옆선 트임과 한쪽 다리의 연속성", ["사이드 슬릿", "side slit", "thigh-high slit", "walking slit"],
     "two edges of a skirt side opening and one continuous leg", "garment_detail", ["appearance", "pose"],
     ["two finished edges form a side opening in a continuous skirt panel",
      "one anatomically continuous leg is visible through that bounded opening",
      "the remaining skirt panel keeps its own hem and plausible hanging folds"],
     ["the whole skirt lifted as one hem", "a gap between shorts legs", "a waist cutout", "a detached extra leg", "slit-scan photography"],
     ["S12", "S08"], "정지와 보행 모두 가능하다. thigh-high가 기본 높이를 강제하지 않으며, 보행 위상은 추가 요청일 때만 별도로 묶는다."),
    ("cutout", "허리 컷아웃의 닫힌 의복 경계", ["허리 컷아웃", "waist cut-out", "side cut-out", "peekaboo cutout"],
     "bounded opening within one waist garment panel", "garment_detail", ["appearance"],
     ["a closed garment edge bounds the declared waist opening on the adult subject",
      "visible fabric bridges connect the panels around that opening",
      "the opening exposes the same body surface while its garment edge retains thickness"],
     ["the gap between a crop top and separate trousers", "an open jacket front", "a dark printed patch", "a tear without a designed closed boundary"],
     ["S06", "S07"], "주변 의복의 닫힌 경계가 이 설계의 판별 조건이다. cut-out 전체를 허리 형태로 환원하지 않는다."),
    ("midriff", "크롭 톱과 하의 사이의 복부 띠", ["크롭 톱", "exposed midriff", "crop top gap", "복부 노출"],
     "separate top hem and lower garment waistband", "garment_detail", ["appearance"],
     ["a separate top hem and lower garment waistband bound a visible midriff band",
      "both garment edges remain continuous around the same adult torso",
      "the skin band stays distinct from any printed panel or garment cutout"],
     ["a waist cutout inside a one-piece garment", "a skin-tone fabric panel", "a low waistband under a long covering top"],
     ["S06", "S07"], "밴드 높이, 배꼽 가시성, 복부 형태, low-rise 여부는 독립적인 추가 선택이다."),
    ("volume_contrast", "몸에 맞는 이너와 여유 있는 외층", ["작은 이너 큰 겉옷", "fitted inner oversized outerwear", "layer volume contrast"],
     "fitted inner garment and separate loose outer garment", "wardrobe_style", ["appearance", "material"],
     ["a fitted inner garment and a separate loose outer garment remain individually readable",
      "the outer layer stands away from the body while the inner follows its local contour",
      "visible overlaps hems or lapels establish the two garments' layer order"],
     ["one loose garment with a printed inner panel", "two equally tight layers", "bare skin mistaken for an inner garment", "unrelated background volume"],
     ["S10", "S06"], "이너는 티셔츠·니트·캐미솔·브라렛 등 독립 선택이다. 언더웨어와 성적 어필을 자동 활성화하지 않는다."),
    ("hem_foundation", "밑단 뒤 기반층의 한정된 부분 보임", ["판치라", "panchira", "パンチラ", "skirt hem underwear glimpse"],
     "skirt hem occluding a separate opaque brief layer", "garment_detail", ["appearance"],
     ["a skirt hem occludes most of a separate opaque brief layer on the adult subject",
      "a bounded part of that layer remains visible beside the occluding hem",
      "a curved leg-opening edge and adjacent fabric panel identify the same separate brief layer"],
     ["a trouser waistband with an inner strap above it", "a petticoat hem", "safety shorts with separate leg hems", "a printed underwear motif", "underwear seen through transparent fabric"],
     ["S03", "S04", "S06"], "정지 사진은 실제 순간성·우연성·동의·촬영 의도를 증명하지 않는다. 이 좁은 의복 관계는 몰래 촬영하는 시점이나 치마를 들추는 행동을 지정하지 않는다."),
    ("neck_foundation", "네크라인 뒤 별도 기반층의 가장자리", ["브라치라", "brachira", "ブラチラ", "neckline bra edge glimpse"],
     "outer neckline edge and separate opaque bra or bralette edge", "garment_detail", ["appearance"],
     ["the outer neckline occludes part of a separate opaque bra or bralette layer",
      "the visible inner edge belongs to that constructed layer rather than a necklace or printed trim",
      "both layers keep a readable overlap order on the same adult subject"],
     ["cleavage without an inner garment", "a necklace inside a neckline", "integrated lace trim on one garment", "underwear as the only top layer"],
     ["S04", "S10", "S06"], "브라치라와 가슴골·무네치라는 보이는 대상이 다르다. 스트랩만 보이는 경우는 별도 형태이며 이 네크라인 관계의 필수 조건이 아니다."),
    ("face_garment", "얼굴과 선택한 의복 디테일의 동시 가독성", ["인물 중심 패션 사진", "face and garment detail readable", "face-focused fashion portrait"],
     "same adult face and requester-selected garment feature", "composition", ["framing", "composition"],
     ["the adult subject's visible face and selected garment feature occupy the same coherent frame",
      "focus light and scale keep both the facial expression and garment feature readable",
      "supporting hands hair and foreground leave those two declared regions distinguishable"],
     ["a face crop that removes the requested garment feature", "a body-only crop", "an unreadably small face", "a bright garment patch substituted for expression"],
     ["S08", "S16"], "동시 가독성은 직접 관찰 조건이다. 얼굴이 항상 가장 밝아야 한다거나 가까운 사진만 매력적이라는 규칙은 만들지 않는다.")
]

EXTRA = [
    ("hair_clearance", "머리카락과 의상 지지 구조의 분리", "body_orientation", ["pose", "appearance"],
     ["hair lies beside the declared garment strap or open-back edge", "the selected support path remains visible on the same adult subject"], ["S08", "S11"]),
    ("opaque_lace_trim", "불투명 슬립 위에 붙은 레이스 가장자리", "garment_detail", ["appearance", "material"],
     ["lace trim is attached to the edge of a separate opaque slip panel", "the lace threads and solid panel remain visually distinct"], ["S06", "S07"]),
    ("sheer_liner", "부분 시어와 불투명 안감의 분리", "texture", ["material", "appearance"],
     ["a translucent fabric panel retains visible weave and seams over a separate opaque liner", "the liner edge and transmitted light establish the two-layer order"], ["S07", "S14"]),
    ("relaxed_supported_turn", "지지된 앉은 자세와 작은 회전", "body_pose", ["pose"],
     ["the seat supports the adult subject while the torso makes a restrained turn", "the pelvis and connected limbs occupy plausible space around that same seat"], ["S08"])
]

HOMONYM_EXCLUSIONS = {
    "pfe_cleavage": ["mineral cleavage", "crystal cleavage", "geological cleavage", "광물 벽개"],
    "pfe_halter": ["horse halter", "horse headstall", "halter for a horse", "말 굴레"],
    "pfe_navel": ["navel orange", "navel oranges", "navel-gazing", "네이블 오렌지"],
    "pfe_slit": ["slit-scan", "slit scan", "slit lamp", "슬릿 스캔", "세극등"]
}


def main():
    profiles, slots, proposals = [], {}, []
    for name, ko, terms, owner, slot, dims, components, negatives, sources, limit in [*SPECS, *NEW_SPECS]:
        ident = "pfe_" + name
        definition = "; ".join(components)
        profile = {
            "id": ident, "category": "portrait_garment_owner_relation",
            "activation": {"exact_terms": [definition], "requires_adult_character": True,
                           "semantic_discovery_requires_component_evidence": False},
            "semantics": {"definition": definition, "paraphrase_examples": [ko, *terms],
                          "contrast_examples": negatives, "claim_limits": [limit,
                          "Only the declared owner relation is observable; actual consent, intent, identity, attractiveness and SNS effectiveness are not pixel claims."]},
            "concept_candidate": {"concept_terms": [ko, *terms, *components]},
            "runtime_expression": {"default_mode": "definition_with_optional_label",
                                  "prompt_label_terms": [], "forbidden_prompt_terms": [], "runtime_forbidden_labels": []},
            "reject_substitutes": negatives,
            "authored_components": {"contract_version": "photo-authored-visual-components/v1", "components": [
                {"id": f"component_{i}", "match_terms": [c], "evidence_field": f"component_{i}_phrase",
                 "evidence_terms": [c], "min_content_words": 3,
                 "instruction": "Preserve the declared owner and make this selected relation visible: " + c,
                 "render_gate": {"id": f"vo_{ident}_{i}", "review_scale": "both" if i < 3 else "native",
                                 "description": c + ". Require the same declared subject and garment; missing, substituted or ambiguous evidence fails."}}
                for i, c in enumerate(components, 1)]}
        }
        if ident in HOMONYM_EXCLUSIONS:
            profile["activation"]["exclude_if_any_terms"] = HOMONYM_EXCLUSIONS[ident]
        profiles.append(profile)
        slots.setdefault(slot, []).append(candidate(ident, ko, terms, components, owner, dims))
        proposals.append({"id": ident, "label_ko": ko, "source_ids": sources,
                          "source_scope": "Terminology or examples only; the all-of visual relation is authored.",
                          "owner": owner, "slot": slot, "affected_dimensions": dims,
                          "components": components, "confounders": negatives, "limitations_ko": limit,
                          "evidence_level": "source_informed_design_not_external_validation",
                          "activation": "complete_relation_exact_or_explicit_opt_in; broad_terms_advisory",
                          "render_status": "NOT_RUN", "user_judgment": "NOT_REQUESTED"})
    for name, ko, slot, dims, components, sources in [*EXTRA, *NEW_EXTRA]:
        ident = "pfe_" + name
        slots.setdefault(slot, []).append(candidate(ident, ko, [], components, ko, dims))
        proposals.append({"id": ident, "label_ko": ko, "source_ids": sources, "slot": slot,
                          "components": components, "affected_dimensions": dims,
                          "evidence_level": "source_informed_optional_candidate", "render_status": "NOT_RUN"})
    bundle_specs = [
        ("back_face", ["back_face", "hair_clearance"], ["back_face"], ["hair obscures back support", "face absent from the requested combined composition"]),
        ("slip_layers", ["skimming", "opaque_lace_trim"], ["skimming", "lace_trim_attached_edge"], ["lace print", "uniform compression substituted for local drape"]),
        ("cowl_layers", ["cowl", "volume_contrast"], ["cowl", "volume_contrast"], ["cowl and outer lapel fused into one fabric edge"]),
        ("leg_face", ["slit", "face_garment"], ["slit", "face_garment"], ["whole lifted hem substituted for a side opening", "face removed by crop"]),
        ("foundation_edge", ["neck_foundation", "volume_contrast"], ["neck_foundation", "volume_contrast"], ["one layer represented as painted texture", "no separate constructed inner edge"]),
        ("midriff_face", ["midriff", "face_garment"], ["midriff", "face_garment"], ["skin-colour panel substituted for skin band", "feature below the crop"])
    ]
    bundle_specs.extend(NEW_BUNDLES)
    by_id = {x["id"]: (slot, x) for slot, rows in slots.items() for x in rows}
    bundles = []
    for name, members, associated, negatives in bundle_specs:
        ids = ["pfe_" + n + "_candidate" for n in members]
        bundles.append({"id": "pfe_bundle_" + name, "primary_visual_proposition": name.replace("_", " "),
                        "component_groups": [{"id": f"member_{i}", "visible_evidence": by_id[x][1]["concept_units"]}
                                             for i, x in enumerate(ids, 1)],
                        "candidate_ids": ids, "candidate_slots": {x: by_id[x][0] for x in ids},
                        "hard_profile_ids": [x if x in {"lace_trim_attached_edge", "clavicle_supraclavicular_hollow"} else "pfe_" + x for x in associated],
                        "confusion_boundaries": negatives,
                        "source_keywords": [by_id[x][1]["ko"] for x in ids],
                        "relations": [{"id": "pfe_bundle_" + name + "_same_subject", "type": "co_realized_with_same_subject_and_garment",
                                       "subject": "the same adult subject and selected garment owners", "object": "all adopted component relations in one photograph"}]})
    ext = {"schema_version": "photo-prompt-research-extension/v1", "slots": slots, "visual_semantics": bundles}
    record = {"record_id": "photo_prompt_portrait_fashion_exposure_extension", "authored_source_sha256": digest(ext),
              "maintenance_only": {"research_path": str(HERE.relative_to(ROOT)), "source_ids": [s["id"] for s in json.loads((HERE / "sources.json").read_text())["sources"]],
                                   "included_proposal_ids": [x["id"] for x in proposals], "deferred_proposals": [],
                                   "render_status": "NOT_RUN", "user_judgment": "NOT_REQUESTED"}}
    ext["maintenance_ref"] = {"contract_version": "photo-extension-maintenance-ref/v1", "record_id": record["record_id"], "sha256": digest(record)}
    save(ASSETS / "photo_prompt_portrait_fashion_exposure_extension.json", ext)
    save(ASSETS / "photo_prompt_visual_obligations_portrait_fashion_exposure.json",
         {"schema_version": "photo-visual-obligation-registry-extension/v1", "relation_contract_version": "photo-visual-relation/v1",
          "description": "Adult portrait garment relations; complete owner relations alone are exact, broad labels remain advisory.", "profiles": profiles})
    save(ROOT / "docs/research-evidence/photo-prompt/extension-maintenance" / (record["record_id"] + ".json"), record)
    save(HERE / "proposals.json", {"schema_version": "portrait-fashion-exposure-research/v1", "proposals": proposals,
                                  "render_status": "NOT_RUN", "user_judgment": "NOT_REQUESTED"})
    print(f"Wrote {len(profiles)} profiles, {sum(map(len, slots.values()))} candidates, {len(bundles)} optional bundles")


def candidate(ident, ko, terms, components, owner, dims):
    return {"id": ident + "_candidate", "ko": ko, "en": "; ".join(components), "weight": 0.45,
            "tags": ["human", "adult", "fashion", "portrait"], "for_any": ["human"],
            "requires_primary_any_tags": ["human"], "requires_all_tags": ["human", "adult"],
            "aliases": [ko, *terms], "keywords": terms or [ko],
            "embedding_text": "; ".join([ko, *terms, *components]),
            "concept_units": components,
            "relations": [{"id": ident + "_owner_relation", "type": "visible_owner_and_boundary",
                           "subject": owner, "object": "the same adult subject and declared garment"}],
            "affected_dimensions": dims}


if __name__ == "__main__":
    main()
