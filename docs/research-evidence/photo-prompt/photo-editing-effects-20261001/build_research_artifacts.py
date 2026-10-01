#!/usr/bin/env python3
"""Build research-only matrices and a small, unregistered runtime projection draft."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent


def read(name):
    return json.loads((OUT / name).read_text())


def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def term(label):
    # Preserve case: Soft light (illumination) differs from Soft Light (blend mode).
    return label.split(" / ", 1)[0].strip()


def route(group_id):
    number = int(group_id.split("_")[1])
    if number in {85, 86, 87, 88}:
        return "workflow_or_output_metadata; visible effect only via separately specified projection"
    if number in {12}:
        return "diagnostic_or_source_operation; no automatic aesthetic candidate"
    if number in {59, 60, 61, 63, 64, 65, 66, 67, 69, 70, 71, 73, 81, 82, 83, 84}:
        return "operation_or_relation; requires target/input/result evidence; optional visible-result candidate if appropriate"
    if number in {74, 75, 76, 77, 78, 79, 80}:
        return "explicit_medium_or_style_projection; whole-image versus depicted-object scope required"
    if number in {1, 2, 3, 4, 5, 6, 7, 8, 46, 47}:
        return "contextual_look_or_purpose; authored observable components, no universal recipe"
    return "observable_effect_or_relation; reuse scoped profiles and add atomic optional candidates as needed"


groups = read("concept-proposals.json")["groups"]
by_term = {}
for group in groups:
    for name in group["reference_terms"]:
        if name in by_term:
            raise ValueError(f"Duplicate reference assignment: {name}")
        by_term[name] = group

matrix = []
for row in read("keyword-catalog-coverage.json")["rows"]:
    group = by_term[term(row["label"])]
    matrix.append({
        **row,
        "proposal_group_id": group["id"],
        "semantic_kind": group["semantic_kind"],
        "owner_scope": group["owner_scope"],
        "observable_projection": group["observable_projection"],
        "confusion_boundary": group["confusion_boundary"],
        "proposed_target_slots": group["target_slots"],
        "proposed_affected_dimensions": group["affected_dimensions"],
        "source_ids": group["source_ids"],
        "priority": group["priority"],
        "implementation_route": route(group["id"]),
        "reuse_profile_ids": group["reuse_profile_ids"],
        "semantic_coverage_verified": False,
        "proposal_status": "research_projection_not_runtime_adoption",
    })
save("keyword-matrix.json", {
    "schema_version": "photo-editing-keyword-to-proposal/v1",
    "status": "research_only",
    "rows": matrix,
})

source_by_id = {row["id"]: row for row in read("source-ledger.json")["sources"]}
md = ["# 키워드별 반영 매핑", "", "245개 원문 표 행을 88개 설계 의미군에 연결했다. 이 표의 어휘 매칭은 의미 커버리지나 후보팩 노출을 증명하지 않는다. 다른 owner의 동명 키워드도 검색되므로 실제 항목을 검토해야 한다. 적용 영역·관찰 결과·혼동 경계·기존 항목 ID는 JSON에 보존했다.", "", "| 행 | 원문 키워드 | 의미군 | 적용 영역 | 우선순위 | 어휘 조사 | 출처 |", "|---|---|---|---|---|---|---|"]
for row in matrix:
    status = ("직접 어휘 매칭" if row["exact_label_or_alias_count"] else
              "본문 언급만" if row["text_mention_count"] or row["profile_text_mention_count"] else
              "어휘 매칭 없음")
    cites = ", ".join(f"[{sid}]({source_by_id[sid]['url']})" for sid in row["source_ids"])
    md.append(f"| {row['reference_row']} | {row['label']} | {row['proposal_group_id']} | {row['owner_scope']} | {row['priority']} | {status} | {cites} |")
md += ["", "## 의미군별 관찰 결과와 혼동 경계", "", "아래는 출처를 바탕으로 작성한 데이터 설계 제안이다. 제품별 알고리즘 또는 모든 사진에 적용되는 보정 공식으로 취급하지 않는다.", "", "| 의미군 | 포함 용어 | 관찰 결과 제안 | 혼동 경계 | 후속 반영 경로 |", "|---|---|---|---|---|"]
for group in groups:
    md.append(f"| {group['id']} | {', '.join(group['reference_terms'])} | {group['observable_projection']} | {group['confusion_boundary']} | {route(group['id'])} |")
(OUT / "keyword-matrix.md").write_text("\n".join(md) + "\n")

# A bounded draft for review, not an extension registered with the runtime loader.
# Tuple: slot, ID suffix, Korean label, English label, group, dimensions, concept units.
definitions = [
    ("grain_profile", "fine_midtonal_grain", "중간톤의 미세한 필름형 입자", "fine film-like image-plane grain in midtones", "edit_55", ["style"], ["fine film-like image-plane grain", "midtone detail remains readable"]),
    ("grain_profile", "coarse_film_grain", "거친 필름형 영상 입자", "coarse film-like image-plane grain", "edit_55", ["style"], ["coarse film-like image-plane grain", "grain does not become object damage"]),
    ("grain_profile", "digital_luma_noise", "영상 밝기 성분의 디지털 노이즈", "digital luminance noise on the image plane", "edit_56", ["style"], ["brightness-only digital image-plane speckle", "scene material remains distinct"]),
    ("grain_profile", "digital_chroma_noise", "영상 색 성분의 디지털 노이즈", "digital chroma noise on the image plane", "edit_56", ["style", "color"], ["colored digital image-plane speckle", "speckle does not recolor the subject"]),
    ("quality", "jpeg_edge_blocks", "고대비 경계의 JPEG형 블록 흔적", "JPEG-like block artifacts near high-contrast image edges", "edit_58", ["style"], ["block-pattern image artifacts near contrast edges", "blocks do not become scene objects"]),
    ("quality", "highlight_local_bloom", "밝은 부분 주위의 국부 블룸", "localized luminous bloom around bright image regions", "edit_28", ["style"], ["localized bloom around bright image regions", "non-highlight subject detail remains readable"]),
    ("film_emulation", "red_edge_halation", "필름형 하이라이트 경계의 적주황 번짐", "film-like red-orange halo confined to bright contrast edges", "edit_29", ["style", "color"], ["red-orange film-like halo at bright contrast edges", "unrelated dark edges remain unaffected"]),
    ("quality", "neutral_optical_diffusion", "색중립적 광학 확산형 하이라이트 번짐", "neutral-colored optical-diffusion-like highlight spread", "edit_35", ["style"], ["neutral-colored optical-diffusion-like highlight spread", "recognizable subject details through the softening"]),
    ("quality", "veiling_contrast_loss", "광원 쪽 베일형 대비 감소", "veiling-flare-like contrast reduction on the light-facing image region", "edit_30", ["style"], ["light-facing image region loses contrast under a luminous veil", "no discrete geometric ghost is required"]),
    ("quality", "discrete_flare_ghosts", "광원과 정렬된 분리된 플레어 고스트", "discrete flare-ghost shapes aligned with a bright light source", "edit_30", ["style"], ["discrete flare-ghost shapes aligned with a bright source", "the ghosts are optical image marks, not scene objects"]),
    ("film_emulation", "light_leak_patch", "장면 광원과 분리된 필름형 빛샘 패치", "film-like light-leak patch independent of a scene-light halo", "edit_31", ["style", "color"], ["film-like irregular light-leak patch", "patch does not need a scene-light origin"]),
    ("quality", "sharpening_edge_halo", "선명화 경계의 밝고 어두운 링", "sharpening-like bright and dark edge halos", "edit_54", ["style"], ["paired bright and dark halos along sharpened image edges", "halos do not imply emitted light"]),
    ("color_grading", "lifted_black_floor", "열린 암부와 올라간 검정 바닥", "lifted black floor with readable dark image tones", "edit_14", ["color", "style"], ["lifted black floor across dark image tones", "dark subject information remains readable"]),
    ("color_grading", "gentle_highlight_rolloff", "밝은 계조의 완만한 전이", "gentle highlight roll-off through a gradual bright tonal transition", "edit_15", ["color", "style"], ["gradual bright tonal transition into highlights", "visible highlight shape without a spatial glow requirement"]),
    ("color_grading", "muted_chroma", "형태·명암을 유지한 절제된 색", "restrained image chroma with readable tonal structure", "edit_07", ["color"], ["restrained image chroma", "readable tonal structure"]),
    ("color_grading", "warm_highlight_cool_shadow", "따뜻한 하이라이트와 차가운 그림자의 분리", "warm highlight tint and cool shadow tint in separate tonal regions", "edit_19", ["color"], ["warm tint in bright tonal regions", "cool tint in shadow tonal regions"]),
    ("color_grading", "bright_open_tones", "밝고 열린 계조와 남은 하이라이트 형태", "bright open image tones with readable highlight shape", "edit_13", ["color", "style"], ["bright open image tones", "readable highlight shape"]),
    ("color", "cobalt_cream_tonal_duotone", "계조에 대응한 코발트·크림 두 색 룩", "cobalt-to-cream two-color tonal mapping", "edit_22", ["color", "style"], ["dark image tones mapped to cobalt", "bright image tones mapped to cream"]),
    ("color", "selected_red_color_splash", "지정한 붉은 물체만 색을 유지", "selected red object remains colored in an otherwise achromatic image", "edit_23", ["color"], ["selected red object remains colored", "the rest of the image is achromatic"]),
    ("skin_finish", "texture_preserving_tone_evening", "피부 미세결을 유지한 국부 톤 정리", "local skin-tone evening with readable fine skin texture", "edit_62", ["appearance"], ["local skin-tone evening", "readable fine skin texture without facial-geometry alteration"]),
    ("focus", "extended_near_far_focus", "가까운 부분과 먼 부분에 걸친 선명도", "extended near-to-far readable focus across the subject", "edit_70", ["camera"], ["near and far subject regions both remain in readable focus", "subject geometry remains continuous across focus transitions"]),
    ("focus", "narrow_focus_transition", "선명한 대상과 점진적으로 흐려지는 깊이", "selected subject in sharp focus with gradual depth-dependent defocus", "edit_36", ["camera"], ["selected subject in sharp focus", "gradual depth-dependent defocus away from the focus plane"]),
    ("motion", "tracked_subject_background_trace", "추적된 대상은 읽히고 배경은 방향성 흔적", "tracked moving subject remains readable against directional background streaks", "edit_42", ["camera"], ["tracked moving subject remains readable", "background streaks follow the tracking direction"]),
    ("motion", "flash_core_shutter_trace", "플래시로 읽히는 대상과 긴 셔터의 주변 흔적", "readable flash-lit subject core with ambient slow-shutter traces", "edit_44", ["camera", "lighting"], ["readable flash-lit subject core", "ambient slow-shutter traces remain visible"]),
    ("quality", "readable_microdetail", "과한 테두리 없이 읽히는 미세 세부", "readable fine image detail without exaggerated edge halos", "edit_50", ["style"], ["readable fine image detail", "no exaggerated edge halos"]),
]

slots = {}
provenance = []
for slot, suffix, ko, en, group_id, dimensions, units in definitions:
    entry_id = "edit_research_" + suffix
    # Conservative property scope: broad effects cannot bypass partial locks.
    effects = [{"dimension": dimension, "target": "*", "property": "*"} for dimension in dimensions]
    entry = {"id": entry_id, "ko": ko, "en": en, "weight": 1.0,
             "tags": ["editing_effect", "image_finish"], "keywords": [en],
             "concept_units": units, "affected_dimensions": dimensions,
             "affected_properties": effects}
    slots.setdefault(slot, []).append(entry)
    group = next(g for g in groups if g["id"] == group_id)
    provenance.append({"candidate_id": f"slot:{slot}:{entry_id}", "proposal_group_id": group_id,
                       "source_ids": group["source_ids"], "owner_scope": group["owner_scope"],
                       "weight_status": "neutral_draft_not_empirically_calibrated",
                       "scope_status": "conservative_draft_requires_request_and_pack_review",
                       "native_pixel_status": "not_tested"})

bundle_defs = [
    ("bright_local_bloom", ["bright_open_tones", "gentle_highlight_rolloff", "highlight_local_bloom"], ["highlight_rolloff_tone_response"], ["Highlight spread remains local while subject information and bright tonal transitions remain readable."]),
    ("film_edge_and_grain", ["red_edge_halation", "fine_midtonal_grain", "gentle_highlight_rolloff"], ["film_halation_highlight_edge_relation"], ["Film-like colored edge halo and image-plane grain have different spatial owners."]),
    ("neutral_diffusion_detail", ["neutral_optical_diffusion", "readable_microdetail"], ["diffusion_filter_highlight_halation"], ["Optical-diffusion-like spread coexists with readable subject detail; it need not be a red film halo."]),
    ("digital_flash_trace", ["digital_luma_noise", "flash_core_shutter_trace", "jpeg_edge_blocks"], [], ["Digital image-plane noise, flash-lit readability and ambient traces remain distinct; this does not identify a sensor type."]),
    ("muted_lifted_black_finish", ["muted_chroma", "lifted_black_floor", "fine_midtonal_grain"], [], ["Restrained color, lifted dark tones and grain form an optional look without forcing all nostalgic images into this recipe."]),
    ("tonal_duotone_detail", ["cobalt_cream_tonal_duotone", "readable_microdetail"], ["cr_duotone", "cr_gradient_mapping"], ["Two colors map to tonal image regions while subject details remain readable; two differently colored scene objects are insufficient."]),
]
all_entries = {entry["id"]: (slot, entry) for slot, entries in slots.items() for entry in entries}
bundles = []
for suffix, member_suffixes, profiles, guards in bundle_defs:
    members = ["edit_research_" + member for member in member_suffixes]
    bundles.append({
        "id": "edit_research_bundle_" + suffix,
        "primary_visual_proposition": suffix.replace("_", " "),
        "candidate_only": True,
        "candidate_ids": members,
        "candidate_slots": {member: all_entries[member][0] for member in members},
        "component_groups": [{"id": f"{member}_{index + 1}", "visible_evidence": [unit]}
                             for member in members
                             for index, unit in enumerate(all_entries[member][1]["concept_units"])],
        "hard_profile_ids": profiles,
        "confusion_boundaries": guards,
        "source_keywords": [suffix.replace("_", " ")],
        "relations": [],
    })
draft = {"schema_version": "photo-prompt-research-extension/v1",
         "auto_optional_policy": "authored_filters_only", "slots": slots,
         "visual_semantics": bundles}
save("runtime-projection-draft.json", draft)
save("prototype-provenance.json", {
    "schema_version": "photo-editing-prototype-provenance/v1",
    "status": "unregistered_research_only_not_runtime_ready",
    "candidate_count": len(provenance), "bundle_count": len(bundles),
    "draft_sha256": hashlib.sha256((OUT / "runtime-projection-draft.json").read_bytes()).hexdigest(),
    "entries": provenance,
    "known_limitations": [
        "No preset applicability filters or ranking calibration have been authored.",
        "Wildcard property effects intentionally block partially locked dimensions; refine only after semantic review.",
        "No actual retrieval pack, request binding, selection, prompt audit or native render qualification was performed.",
        "hard_profile_ids in bundle sources compile to advisory associated_profile_ids, never automatic hard activation.",
        "Each component has one evidence unit so simultaneous duties do not collapse to the current minimum_realizations=1 alternatives contract.",
    ],
})

tail_rows = read("reference-keywords.json")["rows"][-6:]
reference = OUT / "reference-conversation.md"
text = reference.read_text()
marker = "\n## 브라우저에서 회수한 끝부분"
if marker in text:
    text = text.split(marker, 1)[0]
tail = [marker, "", "아래는 브라우저 표를 읽어 회수한 구조화 행이다. 위 접두 본문의 byte-exact 연장이 아니다.", "", "| 원문 행 | 용어 | 완결된 설명 |", "|---|---|---|"]
tail += [f"| {row['reference_row']} | {row['label']} | {row['reference_definition']} |" for row in tail_rows]
tail += ["", "16번에는 5개 조합 예시가 있다. 본문에 등장한 Fujifilm Velvia, ASTIA, CLASSIC CHROME, ETERNA, ACROS는 브랜드별 예시로 따로 다루고, 키워드 표 245개 행 수에 더하지 않았다. 참고 대화의 출처 표시는 조사 단서이며 이번 출처 검증을 대신하지 않는다.", ""]
reference.write_text(text + "\n".join(tail))
print(json.dumps({"keyword_rows": len(matrix), "proposal_groups": len(groups),
                  "proposed_candidates": len(provenance), "draft_bundles": len(bundles),
                  "semantic_kind_counts": dict(Counter(group['semantic_kind'] for group in groups))}, ensure_ascii=False))
