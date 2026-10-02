"""Local, manually selected resolver diagnostics, not an independent benchmark.

No embedding API or public generation is called. Canonical controls copy
registry phrases deliberately; they test wiring rather than generalization.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
import prompt_generator as pg

CONCEPTS = [
    ("rembrandt_face_light_pattern", "성인 인물의 렘브란트 조명 사진"),
    ("racerback_sports_bra_strap_convergence", "성인 모델이 레이서백 스포츠브라를 입은 뒷모습"),
    ("panning_subject_tracking_motion_relation", "달리는 자전거를 패닝으로 찍은 사진"),
    ("pe_red_object_splash_relation", "빨간 컵만 컬러로 남기고 나머지는 흑백으로"),
    ("y2kr_flip_phone", "성인이 화면과 키패드가 있는 옛날 폴더폰을 펼쳐 들고 있는 사진"),
    ("clothing_ct001_v1", "목 아래에 짧은 단추 여밈이 있는 헨리넥 셔츠의 상반신 사진"),
    ("pc_pc02_owner_relation", "성인 인물이 몸은 사선으로 돌리고 얼굴은 카메라를 바라보는 사진"),
    ("ed_cafe_pickup_wait", "성인 손님이 카페 픽업대 앞에서 준비된 음료를 받기 전에 기다리는 사진"),
]


def main():
    started = time.monotonic()
    registry = pg.load_visual_obligation_registry(SKILL / "assets/photo_prompt_visual_obligations.json")
    index_path = SKILL / "assets/photo_prompt_visual_profile_index.json"
    index = json.loads(index_path.read_text())
    profiles = {p["id"]: p for p in registry["profiles"]}
    cases = []
    for target, natural in CONCEPTS:
        p = profiles[target]
        exact = next((t for t in p["activation"]["exact_terms"] if any("가" <= c <= "힣" for c in t)), p["activation"]["exact_terms"][0])
        components = "; ".join(g["any_terms"][0] for g in p["semantics"]["component_semantics"]["groups"])
        cases.extend([
            {"target": target, "tier": "natural_request_only", "request": natural, "baseline": ""},
            {"target": target, "tier": "source_derived_exact_control", "request": exact, "baseline": ""},
            {"target": target, "tier": "source_derived_component_control", "request": natural, "baseline": components},
        ])
    for request in ["Y2K 감성의 성인 패션 사진", "성인 인물의 사진에 패닝은 제외해줘",
                    "avoid racerback sports bra; use parallel shoulder straps instead", "plain adult portrait without a named lighting pattern"]:
        cases.append({"target": None, "tier": "broad_or_negative_control", "request": request, "baseline": ""})
    results = []
    for i, case in enumerate(cases, 1):
        q = case["request"]
        rows = [{"source": "user_requirement", "text": q, "polarity": "required"}]
        if case["baseline"]:
            rows.append({"source": "authorial_core_baseline", "text": case["baseline"], "polarity": "required"})
        fields = {"active_request": [q], "baseline_prompt": [case["baseline"]]}
        raw_rank = pg.rank_bm25f(index["bm25f"], fields, limit=8)
        raw_ids = [row["document_id"] for row in raw_rank]
        resolved = pg.resolve_visual_profile_hits(registry, rows,
            visual_profile_index=index, query_text=q + " " + case["baseline"],
            query_fields=fields, adult_context=True)
        hits = [{k: h.get(k) for k in ["profile_id", "match_basis", "applicability_status", "hard_eligible", "optional_eligible"]}
                for h in resolved["hits"]]
        target_hit = next((h for h in hits if h["profile_id"] == case["target"]), None)
        result = {**case, "lexical_target_rank_before_applicability":
                  raw_ids.index(case["target"]) + 1 if case["target"] in raw_ids else None,
                  "target_hit": target_hit, "hits": hits,
                  "hard_profile_ids": [h["profile_id"] for h in hits if h["hard_eligible"]]}
        results.append(result)
        print(f"{i}/{len(cases)} {case['tier']} {case['target']}: {target_hit}", flush=True)
        (OUT / "retrieval-probes.json").write_text(json.dumps({
            "method": "Full current resolver with exact and BM25F lanes; no query embeddings.",
            "limitations": ["Manually selected examples are not demand-weighted or independent holdouts.",
                "Empty-baseline requests are stress diagnostics, not valid public generation cores.",
                "Canonical exact/component controls are registry-derived and establish wiring only.",
                "No envelope/core audit, candidate adoption audit, API generation, or pixel test was performed."],
            "registry_sha256": pg.visual_profile_registry_sha256(registry),
            "index_file_sha256": hashlib.sha256(index_path.read_bytes()).hexdigest(),
            "cases": results, "completed": i == len(cases), "elapsed_seconds": round(time.monotonic()-started, 3)
        }, ensure_ascii=False, indent=2) + "\n")
    summary = {}
    for tier in {c["tier"] for c in results}:
        group = [r for r in results if r["tier"] == tier]
        summary[tier] = {"cases": len(group), "target_retrieved": sum(r["target_hit"] is not None for r in group),
                         "cases_with_any_hard": sum(bool(r["hard_profile_ids"]) for r in group)}
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
