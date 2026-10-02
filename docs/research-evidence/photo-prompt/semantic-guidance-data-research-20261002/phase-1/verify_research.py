"""Validate research provenance and file integrity, not model or pixel quality."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import Counter
import hashlib
import json
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]


def read(name):
    return json.loads((OUT / name).read_text())


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def validate():
    snapshot = read("source-snapshot.json")
    cards = read("concept-cards.json")["cards"]
    sources = read("sources.json")["items"]
    proposals = read("profile-data-proposals.json")["proposals"]
    references = read("reference-observations.json")["items"]
    cases = [json.loads(line) for line in (OUT / "context-cases.jsonl").read_text().splitlines()]
    for records in (cards, sources, references, cases):
        assert len(records) == len({r["id"] for r in records}), "duplicate research IDs"
    source_ids = {s["id"] for s in sources}
    profile_rows = {r["profile"]["id"]: r for r in snapshot["profiles"]}
    card_ids = {c["id"] for c in cards}
    assert len(cards) == 14 and len({c["family"] for c in cards}) == 12
    assert len(proposals) == 15
    assert len({p["profile_id"] for p in proposals}) == 15
    assert {p["profile_id"] for p in proposals} == set(profile_rows)
    assert {p for c in cards for p in c["profile_ids"]} == set(profile_rows)
    label_names = {
        "pilot-aircraft": ["pilot", "파일럿"],
        "dress-one-unit": ["one-piece", "one piece", "원피스"],
        "character-transition": ["corruption", "흑화", "타락"],
        "reserved-help": ["kuudere", "쿠데레", "クーデレ"],
        "cowl-draped-opening": ["cowl", "카울"],
        "single-shoulder-support": ["one-shoulder", "원숄더"],
        "local-gathered-folds": ["ruching", "루싱", "셔링", "shirring"],
        "textile-transmission": ["sheer", "시어"],
        "fine-open-cells": ["tulle", "mesh", "메시", "튤"],
        "paired-front-fastening": ["corset", "busk", "코르셋", "버스크"],
        "separated-focus-zones": ["split diopter", "split-diopter", "디옵터"],
        "warm-highlight-halo": ["halation", "할레이션"],
        "broad-cheek-lit": ["broad lighting", "브로드"],
        "short-cheek-lit": ["short lighting", "쇼트"],
    }
    for c in cards:
        assert c["source_ids"] and set(c["source_ids"]) <= source_ids
        assert c["research_status"] == "authored_draft_not_runtime_applied"
        assert c["invariants"] and len(c["invariants"]) == len({i["id"] for i in c["invariants"]})
        assert all(i["owner"] and i["relation"] and i["basis"] == "project_selected_scope" for i in c["invariants"])
        assert len(c["variants"]) == len(c["positive_contexts"]) == len(c["contrast_contexts"]) == 3
        for size in ("short", "detailed"):
            for lang in ("ko", "en"):
                text = c["neutral_descriptions"][size][lang]
                assert isinstance(text, str) and text.strip()
                assert all(label.casefold() not in text.casefold() for label in label_names[c["id"]]), (c["id"], size, lang, "name leakage")
        assert all(x["semantic_relation"] == "matches_selected_scope" for x in c["positive_contexts"])
        assert all(x["semantic_relation"] != "matches_selected_scope" for x in c["contrast_contexts"])
        assert c["claim_limits_ko"] and c["remaining_evidence_gaps_ko"]
    allowed_relations = {"matches_selected_scope", "different_sense", "outside_selected_scope",
                         "contradicts_required_relation", "insufficient_evidence"}
    assert len(cases) == 84
    for row in cases:
        assert row["card_id"] in card_ids and set(row["source_ids"]) <= source_ids
        assert row["semantic_relation"] in allowed_relations
        assert set(row["request"]) == {"ko", "en"} and all(row["request"].values())
        assert set(row["candidate_profile_ids"]) <= set(profile_rows)
        assert row["split"] == "authoring_development_examples_not_blind_holdout"
        assert row["model_result"] == row["pixel_result"] == "NOT_RUN"
        assert bool(row["expected_profile_ids"]) == (row["semantic_relation"] == "matches_selected_scope")
    assert Counter(r["card_id"] for r in cases) == Counter({c: 6 for c in card_ids})
    for p in proposals:
        original = profile_rows[p["profile_id"]]
        assert p["source_file"] == original["source_file"]
        assert p["baseline_compiled_profile_sha256"] == canonical_hash(original["profile"])
        assert p["status"] == "unapplied_append_only_review_proposal"
        assert {op["path"] for op in p["operations"]} == {"semantics.paraphrase_examples", "semantics.contrast_examples", "semantics.claim_limits"}
        for op in p["operations"]:
            assert op["operation"] == "append_unique" and op["values"]
            assert len(op["values"]) == len(set(op["values"]))
            assert all(isinstance(v, str) and v.strip() for v in op["values"])
    for r in references:
        assert r["source_id"] in source_ids and r["card_id"] in card_ids
        assert r["image_file_collected"] is False and r["observed"] and r["not_resolved"]
    changed_skill_files = [r["path"] for r in snapshot["protected_skill_files"]
                           if not (ROOT / r["path"]).is_file() or
                           hashlib.sha256((ROOT / r["path"]).read_bytes()).hexdigest() != r["sha256"]]
    skill = ROOT / "skills/photo-prompt-image-generator"
    sys.path.insert(0, str(skill / "scripts"))
    import prompt_generator as pg
    loaded = pg.load_visual_obligation_registry(skill / "assets/photo_prompt_visual_obligations.json")["profiles"]
    current = {p["id"]: p for p in loaded}
    changed_selected_profiles = [ident for ident, row in profile_rows.items()
                                 if ident not in current or canonical_hash(current[ident]) != canonical_hash(row["profile"])]
    source_file_protection_pass = not changed_skill_files and not changed_selected_profiles
    report = dict(
        checked_at_kst=datetime.now(timezone(timedelta(hours=9))).isoformat(),
        validation_scope="structural integrity, foreign keys, target-name omission, frozen-file preservation; not semantic equivalence or model evaluation",
        structural_status="PASS", source_file_protection_status="PASS" if source_file_protection_pass else "DRIFT_DETECTED",
        baseline_head=snapshot["head"],
        observed_head=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        baseline_loaded_profiles=snapshot["loaded_profile_count"], observed_loaded_profiles=len(loaded),
        protected_skill_files=len(snapshot["protected_skill_files"]), changed_skill_files=changed_skill_files,
        changed_selected_profiles=changed_selected_profiles,
        counts=dict(sources=len(sources), concept_families=len({c["family"] for c in cards}),
                    concept_cards=len(cards), target_profiles=len(proposals),
                    variants=sum(len(c["variants"]) for c in cards),
                    bilingual_cases=len(cases), natural_request_texts=sum(len(c["request"]) for c in cases),
                    neutral_descriptions=sum(len(c["neutral_descriptions"][s]) for c in cards for s in ("short", "detailed")),
                    reference_observations=len(references)),
        source_access_counts=dict(Counter(s["access_status"] for s in sources)),
        context_relation_counts=dict(Counter(c["semantic_relation"] for c in cases)),
        not_run=["independent bilingual review", "blind semantic evaluation", "retrieval/routing evaluation",
                 "image generation", "moderation/acceptance-rate evaluation", "generated-image pixel qualification"],
    )
    return report


if __name__ == "__main__":
    result = validate()
    (OUT / "validation-results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["source_file_protection_status"] != "PASS":
        raise SystemExit("Concurrent source drift detected; research remains tied to the original snapshot.")
