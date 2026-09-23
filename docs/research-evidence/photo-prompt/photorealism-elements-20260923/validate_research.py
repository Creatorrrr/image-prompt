#!/usr/bin/env python3
"""Validate research references and materialize unexecuted evaluation specifications."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / "skills" / "photo-prompt-image-generator" / "assets"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def eval_cases(proposals: list[dict]) -> list[dict]:
    cases: list[dict] = []
    for proposal in proposals:
        policy_only = proposal["status"] in {
            "policy_guard_not_pixel_profile",
            "optional_governance_rule",
        }
        conditions_key = "policy_conditions" if policy_only else "required_visible_components"
        base = {
            "kind": "policy_specification" if policy_only else "pixel_rubric_specification",
            "proposal_id": proposal["id"],
            "declared_owner": proposal["owner"],
            "execution_status": "not_run",
            "result": "unscored",
        }
        cases.append(
            {
                **base,
                "id": f"{proposal['id']}_positive",
                "input": proposal["candidate_expression_en"],
                "expected": (
                    "pass_only_if_policy_conditions_honored"
                    if policy_only
                    else "pass_only_if_all_components_visible_on_same_owner_in_same_image"
                ),
                conditions_key: proposal[conditions_key],
            }
        )
        for index, near_miss in enumerate(proposal["near_misses"], start=1):
            cases.append(
                {
                    **base,
                    "id": f"{proposal['id']}_near_miss_{index}",
                    "input": near_miss,
                    "expected": (
                        "fail_if_policy_boundary_violated"
                        if policy_only
                        else "fail_if_this_substitutes_for_required_relation"
                    ),
                    conditions_key: proposal[conditions_key],
                }
            )

    cross_cases = [
        ("broad_photorealistic", "photorealistic portrait", "no_new_hard_profile"),
        ("broad_8k", "8K masterpiece best quality", "no_new_hard_profile"),
        ("broad_lens", "85mm portrait lens", "no_new_hard_profile"),
        ("broad_raw", "RAW DSLR", "metadata_or_optional_only"),
        ("broad_hdr", "HDR photo", "no_exposure_hard_profile"),
        ("broad_film", "film look", "no_film_material_hard_profile"),
        ("broad_candid", "candid photograph", "no_action_trace_hard_profile"),
        ("broad_documentary", "documentary photograph", "no_real_event_authenticity_claim"),
        ("broad_cctv", "CCTV timestamp overlay", "no_fixed_view_hard_profile"),
        ("lens_distance_conflict", "close wide-angle face with telephoto-distance compression", "flag_geometry_conflict"),
        ("dof_conflict", "f/1.2 shallow DOF and all planes sharp to infinity", "flag_focus_conflict"),
        ("lighting_conflict", "hard point light with a broad soft shadow edge", "flag_light_quality_conflict"),
        ("clean_product_conflict", "pristine product catalog with heavy wear on every surface", "reject_unsolicited_wear"),
        ("phone_process_conflict", "modern phone night photo always dark noisy and clipped", "reject_universal_media_rule"),
        ("news_provenance", "AI-generated news-style image of a fictional scene", "retain_synthetic_provenance"),
        ("reference_boundary", "portrait reference showing visible adult appearance", "no_identity_or_biometric_inference"),
    ]
    for case_id, text, expected in cross_cases:
        cases.append(
            {
                "id": case_id,
                "kind": "routing_or_provenance_specification",
                "input": text,
                "expected": expected,
                "execution_status": "not_run",
                "result": "unscored",
            }
        )
    return cases


def validate() -> tuple[list[dict], dict]:
    sources = load("sources.json")["sources"]
    proposals = load("visual-proposals.json")["proposals"]
    bundles = load("candidate-bundles.json")["bundles"]
    coverage = load("coverage-map.json")["sections"]
    registry = json.loads((ASSETS / "photo_prompt_visual_obligations.json").read_text())
    dictionary = json.loads((ASSETS / "photo_prompt_tags.json").read_text())

    source_ids = [row["id"] for row in sources]
    proposal_ids = [row["id"] for row in proposals]
    bundle_ids = [row["id"] for row in bundles]
    profile_ids = {row["id"] for row in registry["profiles"]}
    slot_ids = {
        name: {row["id"] for row in rows}
        for name, rows in dictionary["slots"].items()
    }
    assert len(source_ids) == len(set(source_ids)) == 26
    assert len(proposal_ids) == len(set(proposal_ids)) == 21
    assert len(bundle_ids) == len(set(bundle_ids)) == 14
    assert [row["n"] for row in coverage] == list(range(1, 41))

    for row in sources:
        assert row["url"].startswith("https://"), row["id"]
        assert row["supports"] and row["limit"], row["id"]

    for row in proposals:
        assert row["owner"], row["id"]
        conditions_key = (
            "policy_conditions"
            if row["status"] in {"policy_guard_not_pixel_profile", "optional_governance_rule"}
            else "required_visible_components"
        )
        assert len(row[conditions_key]) >= 3, row["id"]
        assert len(row["near_misses"]) >= 3, row["id"]
        assert row["source_ids"] and set(row["source_ids"]) <= set(source_ids), row["id"]
        assert set(row["existing_profile_ids"]) <= profile_ids, row["id"]
        assert set(row["recommended_slots"]) <= set(slot_ids), row["id"]

    for row in bundles:
        assert row["proposals"] and set(row["proposals"]) <= set(proposal_ids), row["id"]
        assert set(row["existing_profile_ids"]) <= profile_ids, row["id"]
        assert row["source_ids"] and set(row["source_ids"]) <= set(source_ids), row["id"]
        for slot, ids in row["seed_slots"].items():
            assert slot in slot_ids and set(ids) <= slot_ids[slot], (row["id"], slot)
        assert row["do_not_infer"], row["id"]

    for row in coverage:
        assert set(row["proposed"]) <= set(proposal_ids), row["n"]
        assert row["boundary"], row["n"]

    cases = eval_cases(proposals)
    case_ids = [row["id"] for row in cases]
    assert len(case_ids) == len(set(case_ids)) == 100
    result = {
        "scope": "research_artifacts_only",
        "sources": len(sources),
        "proposals": len(proposals),
        "bundles": len(bundles),
        "referenced_conversation_sections": len(coverage),
        "evaluation_specifications": len(cases),
    }
    return cases, result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-cases", action="store_true")
    args = parser.parse_args()
    cases, result = validate()
    path = HERE / "evaluation-cases.jsonl"
    rendered = "\n".join(json.dumps(row, ensure_ascii=False) for row in cases) + "\n"
    if args.write_cases:
        path.write_text(rendered, encoding="utf-8")
    else:
        assert path.read_text(encoding="utf-8") == rendered, "evaluation cases are stale"
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
