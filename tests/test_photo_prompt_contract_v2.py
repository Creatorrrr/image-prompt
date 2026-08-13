from __future__ import annotations

import copy
from contextlib import redirect_stdout
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
PHOTO_RESEARCH_DIR = ROOT / "docs" / "research-evidence" / "photo-prompt"
PHOTO_FIXTURE_DIR = ROOT / "tests" / "fixtures" / "photo_prompt"
WRAPPER_PATH = SCRIPT_DIR / "generate_photo_prompt.py"
EVAL_PATH = SCRIPT_DIR / "eval_semantic.py"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
GENERALIZATION_PATH = PHOTO_FIXTURE_DIR / "generalization_cases.jsonl"
HOLDOUT_PATH = PHOTO_FIXTURE_DIR / "generalization_holdout_cases.jsonl"
DOMAIN_HOLDOUT_V2_PATH = PHOTO_FIXTURE_DIR / "generalization_domain_holdout_v2.jsonl"
RETRIEVAL_HOLDOUT_V3_PATH = PHOTO_FIXTURE_DIR / "semantic_retrieval_holdout_v3.jsonl"
RETRIEVAL_HOLDOUT_V4_PATH = PHOTO_FIXTURE_DIR / "semantic_retrieval_holdout_v4.jsonl"
SUBCULTURE_RETRIEVAL_HOLDOUT_V1_PATH = PHOTO_FIXTURE_DIR / "semantic_retrieval_holdout_subculture_v1.jsonl"
WORLDBUILDING_RETRIEVAL_HOLDOUT_V1_PATH = PHOTO_FIXTURE_DIR / "semantic_retrieval_holdout_worldbuilding_v1.jsonl"
CJK_WORLDBUILDING_RETRIEVAL_HOLDOUT_V1_PATH = PHOTO_FIXTURE_DIR / "semantic_retrieval_holdout_cjk_worldbuilding_v1.jsonl"
CHARACTER_MOE_RETRIEVAL_CONTRACT_V1_PATH = PHOTO_FIXTURE_DIR / "semantic_retrieval_contract_character_moe_v1.jsonl"
NATURAL_MOE_RESPONSE_CONTRACT_V1_PATH = PHOTO_FIXTURE_DIR / "natural_moe_response_contract_v1.jsonl"
NATURAL_MOE_RENDER_REVIEW_V1_PATH = PHOTO_FIXTURE_DIR / "render_natural_moe_user_review_v1.jsonl"
RESEARCH_EVIDENCE_PATH = PHOTO_RESEARCH_DIR / "research_evidence.jsonl"
CHARACTER_MOE_RESEARCH_DIR = PHOTO_RESEARCH_DIR / "character_moe"
CHARACTER_MOE_CROSSWALK_PATH = PHOTO_RESEARCH_DIR / "character_moe_topic_crosswalk_v1.json"
RESEARCH_EXTENSION_PATH = SKILL_DIR / "assets" / "photo_prompt_research_extension.json"
SUBCULTURE_EXTENSION_PATH = SKILL_DIR / "assets" / "photo_prompt_subculture_extension.json"
WORLDBUILDING_EXTENSION_PATH = SKILL_DIR / "assets" / "photo_prompt_worldbuilding_extension.json"
CJK_WORLDBUILDING_EXTENSION_PATH = SKILL_DIR / "assets" / "photo_prompt_cjk_worldbuilding_extension.json"
CHARACTER_MOE_EXTENSION_PATH = SKILL_DIR / "assets" / "photo_prompt_character_moe_extension.json"
SCENE_EXPRESSION_EXTENSION_PATH = SKILL_DIR / "assets" / "photo_prompt_scene_expression_extension.json"
SCENE_EXPRESSION_WORLDBUILDING_PATH = SKILL_DIR / "assets" / "photo_prompt_scene_expression_worldbuilding.json"
SCENE_EXPRESSION_CJK_PATH = SKILL_DIR / "assets" / "photo_prompt_scene_expression_cjk.json"
SCENE_EXPRESSION_CHARACTER_MOE_PATH = SKILL_DIR / "assets" / "photo_prompt_scene_expression_character_moe.json"
SCENE_EXPRESSION_BASELINE_PATH = PHOTO_FIXTURE_DIR / "render_scene_expression_baseline_v1.json"
SCENE_QUALITY_HOLDOUT_PATH = PHOTO_FIXTURE_DIR / "render_scene_quality_holdout_v1.jsonl"
SCENE_QUALITY_VISUAL_REVIEW_PATH = PHOTO_FIXTURE_DIR / "render_scene_quality_visual_review_v1.json"
CHARACTER_MOE_QUALITY_HOLDOUT_PATH = PHOTO_FIXTURE_DIR / "render_character_moe_quality_holdout_v1.jsonl"
CHARACTER_MOE_QUALITY_VISUAL_REVIEW_PATH = PHOTO_FIXTURE_DIR / "render_character_moe_quality_visual_review_v1.json"
VIEWER_EXPERIENCE_HOLDOUT_PATH = PHOTO_FIXTURE_DIR / "render_viewer_experience_holdout_v1.jsonl"
VIEWER_EXPERIENCE_VISUAL_REVIEW_PATH = PHOTO_FIXTURE_DIR / "render_viewer_experience_visual_review_v1.json"
QUALITY_LAYERS_PATH = SKILL_DIR / "assets" / "photo_prompt_quality_layers.json"
DOMAIN_VISUAL_REVIEW_PLAN_PATH = PHOTO_FIXTURE_DIR / "visual_review_domain_extension_plan.json"
DOMAIN_VISUAL_REVIEW_RESULTS_PATH = PHOTO_FIXTURE_DIR / "visual_review_domain_extension_results.json"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import audit_composed_prompt  # noqa: E402
import audit_image_render_request  # noqa: E402
import audit_moe_render_review  # noqa: E402
import audit_scene_expression  # noqa: E402
import eval_semantic  # noqa: E402
import generate_photo_prompt  # noqa: E402
import prompt_generator  # noqa: E402


class PhotoPromptContractV2Tests(unittest.TestCase):
    def run_wrapper(self, *args: str):
        completed = subprocess.run(
            [sys.executable, str(WRAPPER_PATH), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return json.loads(completed.stdout)

    def composed_from_hybrid_route(
        self,
        pack: dict,
        route_id: str,
        *,
        accept_count: int = 2,
        extra_chosen: tuple[str, ...] = (),
    ) -> dict:
        hybrid = pack["hybrid_augmentation"]
        authorial_mode = hybrid["contract_version"] == "photo-hybrid-augmentation/v2"
        routes = hybrid["route_contract"]["routes"]
        route = next(row for row in routes if row["id"] == route_id)
        candidate_objects = audit_composed_prompt.candidate_objects_from_pack(pack)
        accepted = set(route["candidate_ids"][:accept_count])
        if authorial_mode:
            evidence = []
            for index, candidate_id in enumerate(route["candidate_ids"]):
                if candidate_id not in accepted:
                    continue
                source_terms = candidate_objects[candidate_id].get("concept_terms") or ["source cue"]
                evidence.append(
                    f"{source_terms[0]} becomes visible through an authored gesture at unfinished beat {index + 1}"
                )
        else:
            evidence = [
                str(candidate_objects[candidate_id]["label_en"])
                for candidate_id in route["candidate_ids"]
                if candidate_id in accepted
            ]
        adult_contract = hybrid.get("adult_appeal", {})
        prompt_parts = []
        adult_brief = None
        if adult_contract.get("enabled"):
            prompt_parts.extend(
                [
                    "An adult original fashion model",
                    "holds a self-directed editorial pose",
                ]
            )
            adult_brief = {
                "adult_subject_phrase": "An adult original fashion model",
                "agency_phrase": "self-directed editorial pose",
                "axes": {
                    axis_id: {
                        "intensity": axis["intensity"],
                        **(
                            {
                                "artistic_interpretation": "Keep the axis subordinate to the scene's agency.",
                                "prompt_evidence": f"an authored {axis_id.replace('_', ' ')} accent follows her deliberate gesture",
                            }
                            if authorial_mode and axis["intensity"] > 0
                            else {}
                        ),
                    }
                    for axis_id, axis in adult_contract["axes"].items()
                },
                "blend": {"emphasis": adult_contract["blend"]["emphasis"]},
            }
            if authorial_mode:
                prompt_parts.extend(
                    axis["prompt_evidence"]
                    for axis in adult_brief["axes"].values()
                    if axis.get("prompt_evidence")
                )
        prompt_parts.extend(evidence)
        decisions = []
        detail_by_id = {detail["candidate_id"]: detail for detail in route["details"]}
        evidence_by_id = dict(zip([candidate_id for candidate_id in route["candidate_ids"] if candidate_id in accepted], evidence))
        for candidate_id in route["candidate_ids"]:
            state = ("transformed" if authorial_mode else "accepted") if candidate_id in accepted else "rejected"
            decision = {
                "candidate_id": candidate_id,
                "decision": state,
                "function": detail_by_id[candidate_id]["function"],
                "rationale": "It supports the selected route without replacing the concept core.",
                "marginal_contribution": "Removing it would reduce visible specificity.",
            }
            if candidate_id in accepted:
                decision["prompt_evidence"] = evidence_by_id[candidate_id]
                if authorial_mode:
                    decision.update(
                        {
                            "artistic_interpretation": "Use the cue as a relational prompt, not as supplied prose.",
                            "transformation": "Placed the cue inside an unfinished character action.",
                            "transformation_dimensions": ["causality", "gesture"],
                        }
                    )
            decisions.append(decision)
        brief = {
            "concept_core": "A coherent modern photographic subject remains the governing idea.",
            "routes_considered": [
                {
                    "route_id": row["id"],
                    "decision": "selected" if row["id"] == route_id else "rejected",
                    "reason": "This route adds the clearest marginal detail."
                    if row["id"] == route_id
                    else "Another route fits the concept more economically.",
                }
                for row in routes
            ],
            "selected_route_id": route_id,
            "decisions": decisions,
        }
        if adult_brief is not None:
            brief["adult_appeal"] = adult_brief
        return {
            "pack_id": pack["pack_id"],
            "prompt_en": "; ".join(prompt_parts) + ".",
            "negative_en": pack.get("negative_en"),
            "chosen_candidate_ids": [*sorted(accepted), *extra_chosen],
            "composer": "agent",
            "augmentation_brief": brief,
        }

    def test_safety_contract_defaults_to_pass_and_evaluates_only_on_request(self):
        base_args = (
            "--concept",
            "유나 바니걸",
            "--selection-mode",
            "rule",
            "--seed",
            "11",
            "--emit-candidate-pack",
        )
        default_pack = self.run_wrapper(*base_args)[0]
        self.assertEqual(
            default_pack["safety"],
            {
                "mode": "automatic",
                "evaluation_requested": False,
                "status": "pass",
                "requires_user_approval": False,
                "items": [],
            },
        )

        evaluated_pack = self.run_wrapper(*base_args, "--safety-evaluation")[0]
        self.assertEqual(evaluated_pack["safety"]["mode"], "explicit_evaluation")
        self.assertTrue(evaluated_pack["safety"]["evaluation_requested"])
        self.assertEqual(evaluated_pack["safety"]["status"], "pass")
        self.assertFalse(evaluated_pack["safety"]["requires_user_approval"])
        self.assertTrue(evaluated_pack["safety"]["items"])
        self.assertTrue(all(item["status"] == "pass" for item in evaluated_pack["safety"]["items"]))

    def test_candidate_pack_integrity_and_assertions_fail_closed(self):
        pack = self.run_wrapper(
            "--preset",
            "product_hero_on_riser",
            "--selection-mode",
            "rule",
            "--seed",
            "17",
            "--emit-candidate-pack",
        )[0]
        chosen_candidate = next(
            candidate
            for slot_payload in pack["slots"].values()
            for candidate in slot_payload["candidates"]
        )
        chosen_id = chosen_candidate["id"]
        chosen_evidence = "an angled glass bottle catches a narrow amber rim"
        composed = {
            "pack_id": pack["pack_id"],
            "prompt_en": (
                "A restrained product still life with believable contact shadow, no text or watermark; "
                f"{chosen_evidence}."
            ),
            "negative_en": pack.get("negative_en"),
            "chosen_candidate_ids": [chosen_id],
            "composer": "agent",
            "candidate_interpretations": [
                {
                    "candidate_id": chosen_id,
                    "artistic_interpretation": "Use the cue as quiet product tension.",
                    "transformation": "Translate it into asymmetric material light.",
                    "prompt_evidence": chosen_evidence,
                }
            ],
        }
        passed = audit_composed_prompt.audit_composed_prompt(pack, composed)
        self.assertEqual(passed["status"], "pass", passed)

        missing_interpretation = copy.deepcopy(composed)
        missing_interpretation.pop("candidate_interpretations")
        missing_result = audit_composed_prompt.audit_composed_prompt(
            pack, missing_interpretation
        )
        self.assertIn(
            "candidate_interpretations",
            {failure["check"] for failure in missing_result["failures"]},
        )

        copied_terms = copy.deepcopy(composed)
        source_only = " ".join(chosen_candidate["concept_terms"][:4])
        copied_terms["candidate_interpretations"][0]["prompt_evidence"] = source_only
        copied_terms["prompt_en"] += f" {source_only}."
        copied_result = audit_composed_prompt.audit_composed_prompt(pack, copied_terms)
        self.assertIn(
            "candidate_interpretation_authorship",
            {failure["check"] for failure in copied_result["failures"]},
        )

        applicability_pack = copy.deepcopy(pack)
        chosen_slot = next(
            candidate
            for slot_payload in applicability_pack["slots"].values()
            for candidate in slot_payload["candidates"]
        )
        chosen_slot["applicability"] = {
            "status": "blocked",
            "source": "test",
            "reason": "synthetic contract violation",
        }
        applicability_pack["pack_id"] = audit_composed_prompt.computed_pack_id(applicability_pack)
        applicability_composed = {
            **composed,
            "pack_id": applicability_pack["pack_id"],
            "chosen_candidate_ids": [chosen_slot["id"]],
            "candidate_interpretations": [
                {
                    "candidate_id": chosen_slot["id"],
                    "artistic_interpretation": "Use the cue as quiet product tension.",
                    "transformation": "Translate it into asymmetric material light.",
                    "prompt_evidence": chosen_evidence,
                }
            ],
        }
        applicability_result = audit_composed_prompt.audit_composed_prompt(
            applicability_pack, applicability_composed
        )
        self.assertIn(
            "candidate_applicability",
            {failure["check"] for failure in applicability_result["failures"]},
        )

        tampered = copy.deepcopy(pack)
        tampered["provenance"]["seed"] = 999
        tampered_result = audit_composed_prompt.audit_composed_prompt(tampered, composed)
        self.assertIn("pack_integrity", {failure["check"] for failure in tampered_result["failures"]})

        spoofed = {**composed, "coverage_assertions": {"not-a-mandatory-intent": "product"}}
        spoofed_result = audit_composed_prompt.audit_composed_prompt(pack, spoofed)
        self.assertIn("coverage_assertions", {failure["check"] for failure in spoofed_result["failures"]})

        unsupported = copy.deepcopy(pack)
        unsupported["contract_version"] = "photo-candidate-pack/v5"
        unsupported_result = audit_composed_prompt.audit_composed_prompt(
            unsupported,
            composed,
        )
        self.assertIn(
            "contract_version",
            {failure["check"] for failure in unsupported_result["failures"]},
        )

        with self.assertRaisesRegex(ValueError, "exactly one pack"):
            audit_composed_prompt.first_pack([])
        with self.assertRaisesRegex(ValueError, "exactly one pack"):
            audit_composed_prompt.first_pack([pack, pack])

    def test_candidate_pack_v4_default_and_v3_v2_compatibility_projection(self):
        common = (
            "--preset",
            "character_attribute_composition_scene",
            "--selection-mode",
            "rule",
            "--seed",
            "810001",
            "--emit-candidate-pack",
        )
        current = self.run_wrapper(*common)[0]
        prior = self.run_wrapper(*common, "--candidate-pack-version", "v3")[0]
        legacy = self.run_wrapper(*common, "--candidate-pack-version", "v2")[0]

        self.assertEqual(current["contract_version"], "photo-candidate-pack/v4")
        self.assertEqual(prior["contract_version"], "photo-candidate-pack/v3")
        self.assertEqual(legacy["contract_version"], "photo-candidate-pack/v2")
        self.assertEqual(current["quality_profile"]["profile_id"], "authorial")
        self.assertEqual(prior["quality_profile"]["profile_id"], "character_scene_grammar")
        self.assertEqual(legacy["quality_profile"]["profile_id"], "character_moe_grammar")
        self.assertNotIn("source", current["quality_profile"])
        self.assertNotIn("source", current["photographic_craft"])
        self.assertNotIn("source", current["artistic_final_touch"])
        self.assertNotIn("argv", current["provenance"])
        self.assertNotIn("preset_id", current["provenance"])
        self.assertFalse(current["preset_reference"]["source_preset_exposed"])
        self.assertTrue(
            current["authorial_composition"]["policy"][
                "chosen_candidate_interpretations_required"
            ]
        )
        self.assertIn("source", legacy["quality_profile"])
        self.assertIn("source", legacy["photographic_craft"])
        for key in ("domain", "topic_id", "family_id"):
            self.assertNotIn(key, current["character_grammar"])
            self.assertIn(key, legacy["character_grammar"])
        self.assertNotIn(
            "inventory_preset_id",
            current["hybrid_augmentation"]["adult_appeal"],
        )
        self.assertEqual(
            current["hybrid_augmentation"]["contract_version"],
            "photo-hybrid-augmentation/v2",
        )
        self.assertEqual(
            prior["hybrid_augmentation"]["contract_version"],
            "photo-hybrid-augmentation/v1",
        )
        self.assertTrue(current["authorial_composition"]["policy"]["agent_is_final_author"])
        self.assertNotIn(
            "label_en",
            next(iter(current["slots"].values()))["candidates"][0],
        )
        self.assertNotIn("selected", next(iter(current["slots"].values())))
        self.assertNotIn(
            "selected_by_sampler",
            next(iter(current["slots"].values()))["candidates"][0],
        )
        self.assertIn(
            "label_en",
            next(iter(prior["slots"].values()))["candidates"][0],
        )
        self.assertIn(
            "source_preset_id",
            legacy["hybrid_augmentation"]["adult_appeal"],
        )

        leaked_routing = copy.deepcopy(current)
        leaked_routing["provenance"]["argv"] = ["--preset", "private-answer"]
        self.assertIn(
            "authorial_private_routing",
            {
                row["check"]
                for row in audit_composed_prompt.audit_v4_authorial_pack(
                    leaked_routing
                )
            },
        )
        leaked_quality = copy.deepcopy(current)
        leaked_quality["photographic_craft"]["top_strategy"] = {
            "id": "private-winner"
        }
        self.assertIn(
            "authorial_quality_routing",
            {
                row["check"]
                for row in audit_composed_prompt.audit_v4_authorial_pack(
                    leaked_quality
                )
            },
        )

        itasha_common = (
            "--preset",
            "itasha_display_culture_documentary",
            "--selection-mode",
            "rule",
            "--seed",
            "42",
            "--emit-candidate-pack",
        )
        current_itasha = self.run_wrapper(*itasha_common)[0]
        prior_itasha = self.run_wrapper(
            *itasha_common,
            "--candidate-pack-version",
            "v3",
        )[0]
        legacy_itasha = self.run_wrapper(
            *itasha_common,
            "--candidate-pack-version",
            "v2",
        )[0]
        current_blob = json.dumps(current_itasha, ensure_ascii=False)
        prior_blob = json.dumps(prior_itasha, ensure_ascii=False)
        legacy_blob = json.dumps(legacy_itasha, ensure_ascii=False)
        self.assertNotIn("aligning_original_graphics_vehicle_wrap", current_blob)
        self.assertNotIn("aligning_rights_cleared_original_vehicle_wrap", current_blob)
        self.assertIn("aligning_original_graphics_vehicle_wrap", prior_blob)
        self.assertNotIn("aligning_rights_cleared_original_vehicle_wrap", prior_blob)
        self.assertIn("aligning_rights_cleared_original_vehicle_wrap", legacy_blob)

    def test_candidate_relevance_uses_public_visual_text_only(self):
        entry = {
            "id": "internal_source_grounded_candidate",
            "en": "an adult craftsperson repairing a lamp",
            "ko": "램프를 수리하는 성인 공예가",
            "aliases": ["lamp repair"],
            "keywords": ["repair"],
            "embedding_text": "cited study market_researched",
            "tags": ["character_moe_grammar", "source_grounded"],
            "kind": ["private_router"],
            "facets": {"content_basis": ["original_character_design"]},
        }
        blob = prompt_generator.candidate_pack_entry_blob(entry)
        self.assertIn("adult craftsperson", blob)
        self.assertIn("lamp repair", blob)
        for private_marker in (
            "internal_source_grounded_candidate",
            "cited study",
            "market_researched",
            "character_moe_grammar",
            "source_grounded",
            "private_router",
            "content_basis",
        ):
            self.assertNotIn(private_marker, blob)

        result = {
            "preset_id": "internal_source_grounded_preset",
            "provenance": {
                "preset_id": "internal_source_grounded_preset",
                "concept_lock": ["visible brass lamp"],
                "additional_requirements": ["warm window light"],
                "user_mandatory_intents": ["visible repair action"],
            },
        }
        trace = {"intent": "document an adult lamp repairer"}
        presets = [
            {
                "id": "preset:internal_source_grounded_preset",
                "preset_id": "internal_source_grounded_preset",
                "label_en": "adult lamp-repair workshop",
                "label_ko": "성인 램프 수리 작업실",
                "family": "market_researched_family",
            }
        ]
        slots = {
            "subject": {
                "selected": "source_grounded_subject",
                "candidates": [
                    {
                        "id": "slot:subject:source_grounded_subject",
                        "entry_id": "source_grounded_subject",
                        "label_en": "an adult repairer",
                        "label_ko": "성인 수리공",
                        "tags": ["character_moe_grammar"],
                        "kind": ["source_grounded"],
                    }
                ],
            }
        }
        mandatory = [
            {
                "text": "source-grounded adult practice",
                "source": "selected_preset.render_contract",
                "source_text": "from a cited study",
            },
            {
                "text": "holding a red notebook",
                "source": "user_requirement",
                "source_text": "holding a red notebook",
            },
        ]
        corpus = prompt_generator.candidate_pack_integration_corpus(
            result, trace, presets, slots, mandatory
        )
        self.assertIn("adult lamp-repair workshop", corpus)
        self.assertIn("holding a red notebook", corpus)
        for private_marker in (
            "internal_source_grounded_preset",
            "market_researched_family",
            "slot:subject",
            "character_moe_grammar",
            "from a cited study",
        ):
            self.assertNotIn(private_marker, corpus)

        source_corpus = prompt_generator.candidate_pack_integration_source_corpus(
            result, trace, mandatory
        )
        self.assertIn("document an adult lamp repairer", source_corpus)
        self.assertIn("holding a red notebook", source_corpus)
        self.assertNotIn("source-grounded adult practice", source_corpus)
        self.assertNotIn("from a cited study", source_corpus)

    def test_safety_tier_remains_guardable_but_does_not_score_or_leak(self):
        preset = {
            "facets": {
                "safety_tier": ["adult_compatible"],
            }
        }
        item = {
            "facets": {
                "safety_tier": ["adult_compatible"],
            }
        }

        self.assertIn(
            "safety_tier:adult_compatible",
            prompt_generator.facet_tokens(item),
        )
        self.assertEqual(
            prompt_generator.semantic_facet_match_score(item, preset, {}),
            0.0,
        )
        self.assertEqual(prompt_generator.candidate_pack_public_facets(item), {})
        guarded_item = {
            "hard_guards": {
                "requires_facets": ["safety_tier:adult_compatible"],
            }
        }
        self.assertTrue(
            prompt_generator.compatible_with_facet_guards(guarded_item, preset, {})
        )
        self.assertFalse(
            prompt_generator.compatible_with_facet_guards(guarded_item, {}, {})
        )

        item["facets"]["manifestation_mode"] = ["diegetic_world_system"]
        preset["facets"]["manifestation_mode"] = ["diegetic_world_system"]
        self.assertEqual(
            prompt_generator.semantic_facet_match_score(item, preset, {}),
            1.0,
        )

        data = prompt_generator.load_json(TAGS_PATH)
        private_topic = data["character_mechanism_graph"]["families"][0]["topic_ids"][0]
        public_tags = prompt_generator.candidate_pack_public_tags(
            data,
            {
                "tags": [
                    "human",
                    "adult",
                    "adult_compatible",
                    "age_context_only",
                    "market_label_nonvisual",
                    "character_moe_grammar",
                    "character_quiet_care_daily_scene_atomic_scene",
                    private_topic,
                ]
            },
        )
        self.assertEqual(public_tags, ["human", "adult"])

        ordinary_result = prompt_generator.generate_once(
            data,
            __import__("random").Random(17),
            "product_hero_on_riser",
            ["en"],
            False,
            0,
            True,
            detail_level="detailed",
            selection_mode="rule",
            seed=17,
        )
        ordinary_pack = prompt_generator.build_candidate_pack(ordinary_result, data)
        self.assertFalse(ordinary_pack["character_grammar"]["enabled"])
        self.assertNotIn("policy_ids", ordinary_pack["character_grammar"])
        self.assertTrue(
            all("family" not in candidate for candidate in ordinary_pack["presets"])
        )

    def test_korean_no_people_intent_never_inverts_to_a_human_subject(self):
        pack = self.run_wrapper(
            "--preset",
            "environmental_portrait_composition",
            "--selection-mode",
            "rule",
            "--seed",
            "23",
            "--additional-requirement",
            "사람 없는 quiet brutalist reading room, no people",
            "--emit-candidate-pack",
        )[0]
        mandatory = {item["text"] for item in pack["mandatory_intents"]}
        self.assertNotIn("사람 없는", mandatory)
        self.assertNotIn("no people", mandatory)
        excluded = [
            row
            for row in pack["intent_contract"]
            if "no_people" in row.get("constraints", [])
        ]
        self.assertTrue(excluded)
        self.assertTrue(all(row["polarity"] in {"excluded", "mixed"} for row in excluded))
        self.assertTrue(pack["slots"]["subject"]["candidates"])
        self.assertTrue(
            all(
                "human" not in candidate.get("kind", [])
                for candidate in pack["slots"]["subject"]["candidates"]
            )
        )
        self.assertNotIn("active_axes", pack["photographic_integration"])
        self.assertNotIn(
            "human",
            pack["quality_profile"]["facets"]["subject_kind"],
        )

    def test_internal_recipe_guidance_keeps_typed_polarity_and_compact_budget(self):
        pack = self.run_wrapper(
            "--concept",
            "회사원",
            "--selection-mode",
            "rule",
            "--seed",
            "42",
            "--hybrid-augmentation",
            "--emit-candidate-pack",
        )[0]

        mandatory = {str(row.get("text") or "") for row in pack["mandatory_intents"]}
        forbidden_positive_intents = {
            "Avoid",
            "glamour",
            "pin-up",
            "fetish",
            "minors-coding",
            "Soft",
            "visual",
            "guidance",
            "should",
            "through",
            "rather",
        }
        self.assertFalse(mandatory & forbidden_positive_intents, mandatory)

        by_source: dict[str, list[dict]] = {}
        for row in pack["intent_contract"]:
            by_source.setdefault(str(row.get("source") or ""), []).append(row)
        self.assertTrue(by_source["role_requirement"])
        self.assertTrue(all(row["polarity"] == "advisory" for row in by_source["role_requirement"]))
        self.assertTrue(by_source["negative_requirement"])
        self.assertTrue(all(row["polarity"] == "excluded" for row in by_source["negative_requirement"]))
        self.assertTrue(by_source["soft_guidance"])
        self.assertTrue(all(row["polarity"] == "advisory" for row in by_source["soft_guidance"]))

        minified_bytes = len(
            json.dumps(pack, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        )
        self.assertLessEqual(minified_bytes, 120_000)

        direct = self.run_wrapper(
            "--concept",
            "회사원",
            "--selection-mode",
            "rule",
            "--seed",
            "42",
            "--detail-level",
            "compact",
        )[0]
        prompt = str(direct["prompt_en"])
        self.assertLessEqual(len(prompt.split()), 120, prompt)
        self.assertIn("office worker", prompt.lower())
        self.assertTrue("lanyard" in prompt.lower() or "access card" in prompt.lower())
        self.assertNotIn("Additional requirements:", prompt)

    def test_user_additional_requirement_remains_one_hard_visible_intent(self):
        requirement = "a red umbrella held above the product"
        pack = self.run_wrapper(
            "--preset",
            "product_hero_on_riser",
            "--selection-mode",
            "rule",
            "--seed",
            "42",
            "--additional-requirement",
            requirement,
            "--emit-candidate-pack",
        )[0]

        self.assertIn(requirement, {row["text"] for row in pack["mandatory_intents"]})
        row = next(
            row
            for row in pack["intent_contract"]
            if row.get("source") == "user_requirement" and row.get("text") == requirement
        )
        self.assertEqual(row["polarity"], "required")
        self.assertEqual(row["priority"], "critical")

    def test_explicit_cat_and_no_people_product_route_subject_facets_consistently(self):
        cat_pack = self.run_wrapper(
            "--concept",
            "고양이",
            "--selection-mode",
            "rule",
            "--seed",
            "42",
            "--hybrid-augmentation",
            "--emit-candidate-pack",
        )[0]
        self.assertNotIn("subject", cat_pack["slots"])
        self.assertIn(
            "subject",
            {row["slot"] for row in cat_pack["authorial_open_slots"]},
        )
        cat_intent = next(
            row for row in cat_pack["intent_contract"] if row.get("text") == "고양이"
        )
        self.assertIn("subject_entry:stray_cat", cat_intent["axis_hints"])
        self.assertIn("animal", cat_pack["quality_profile"]["facets"]["subject_kind"])
        self.assertNotIn("human", cat_pack["quality_profile"]["facets"]["subject_kind"])
        self.assertFalse(cat_pack["hybrid_augmentation"]["adult_appeal"]["enabled"])

        product_pack = self.run_wrapper(
            "--concept",
            "사람 없는 화장품 제품 사진",
            "--selection-mode",
            "rule",
            "--seed",
            "42",
            "--hybrid-augmentation",
            "--emit-candidate-pack",
        )[0]
        subject_kinds = set(product_pack["quality_profile"]["facets"].get("subject_kind", []))
        self.assertNotIn("human", subject_kinds)
        self.assertNotIn("matched_literal_subject_entries", product_pack["quality_profile"])
        self.assertFalse(product_pack["hybrid_augmentation"]["adult_appeal"]["enabled"])

    def test_research_scene_function_is_a_fail_closed_control_and_preserves_no_people(self):
        pack = self.run_wrapper(
            "--preset",
            "natural_process_trace_documentary",
            "--scene-function",
            "revelation",
            "--selection-mode",
            "rule",
            "--seed",
            "42",
            "--additional-requirement",
            "사람 없는 frost-to-melt boundary, no people",
            "--emit-candidate-pack",
            "--candidate-pack-version",
            "v3",
        )[0]
        selected_scene = pack["render_contract"]["selected_scene"]
        self.assertEqual(selected_scene["blueprint_id"], "process_front_crossing")
        self.assertIn("revelation", selected_scene["scene_functions"])
        self.assertEqual(pack["provenance"]["requested_scene_function"], "revelation")
        self.assertNotIn("revelation", {item["text"] for item in pack["mandatory_intents"]})
        self.assertIn("frost-to-melt boundary", selected_scene["atomic_scene"]["subject"]["label_en"])

        human_only = subprocess.run(
            [
                sys.executable,
                str(WRAPPER_PATH),
                "--preset",
                "cjk_villainess_otome_aristocratic_world",
                "--selection-mode",
                "rule",
                "--seed",
                "42",
                "--additional-requirement",
                "사람 없는 장면, no people",
                "--emit-candidate-pack",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(human_only.returncode, 0)
        self.assertIn("no explicitly non-human render scene", human_only.stderr)

        missing_preset = subprocess.run(
            [
                sys.executable,
                str(WRAPPER_PATH),
                "--scene-function",
                "revelation",
                "--selection-mode",
                "rule",
                "--emit-candidate-pack",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(missing_preset.returncode, 0)
        self.assertIn("requires an explicit --preset", missing_preset.stderr)

        person_only_slots = {
            "appearance_type",
            "body_pose",
            "costume_style",
            "hair_style",
            "hand_pose",
            "makeup_style",
            "wardrobe_style",
        }
        for slot, slot_payload in pack["slots"].items():
            self.assertNotIn(slot, person_only_slots)
            for candidate in slot_payload["candidates"]:
                self.assertEqual(
                    candidate["applicability"],
                    {
                        "status": "eligible",
                        "source": "sampler_eligible_pool",
                        "reason": None,
                    },
                )
                self.assertNotIn(
                    "human",
                    {str(item).lower() for item in [*candidate.get("kind", []), *candidate.get("tags", [])]},
                )

    def test_role_scene_variants_rotate_while_identity_core_stays_fixed(self):
        variant_ids = set()
        for seed in range(1, 13):
            _args, explanations = generate_photo_prompt.resolve_concepts(
                ["--selection-mode", "rule", "--seed", str(seed)],
                ["회사원"],
                concept_mode="soft",
            )
            explanation = explanations[0]
            variant_ids.add(explanation["selected_scene_variants"][0]["id"])
            forced = explanation["combined_forced_slots"]
            self.assertEqual(forced["subject"], ["office_worker"])
            self.assertEqual(forced["appearance_type"], ["corporate_professional"])
            self.assertEqual(forced["wardrobe_style"], ["clean_blazer_trousers"])
            self.assertNotIn("person_origin", forced)
        self.assertGreaterEqual(len(variant_ids), 2)

    def test_creative_discovery_pilot_roles_keep_identity_and_reach_atomic_scenes(self):
        expected_identity = {
            "사진작가": {
                "subject": ["photographer_role_model"],
                "costume_style": ["photographer_utility_vest_costume"],
            },
            "바리스타": {"subject": ["young_barista"]},
            "도예가": {"subject": ["ceramic_artist"]},
            "농부": {"subject": ["farmer_at_dawn"]},
            "기자": {"subject": ["field_reporter"]},
            "우주비행사": {
                "subject": ["astronaut_role_model"],
                "costume_style": ["astronaut_flight_suit_costume"],
            },
            "큐레이터": {
                "subject": ["museum_curator_role_model"],
                "costume_style": ["curator_suit_gloves_costume"],
            },
            "정비사": {"subject": ["garage_mechanic"]},
            "도서관 사서": {"subject": ["librarian_at_desk"]},
            "플로리스트": {
                "subject": ["florist_arranging_bouquet"],
                "wardrobe_style": ["knit_cardigan_jeans"],
            },
        }
        recipes = generate_photo_prompt.load_concept_recipes()

        for role, identity in expected_identity.items():
            with self.subTest(role=role):
                recipe = recipes["roles"][role]
                variants = recipe["scene_variants"]
                expected_variant_ids = {variant["id"] for variant in variants}
                self.assertGreaterEqual(len(expected_variant_ids), 2)
                self.assertTrue(set(identity).isdisjoint({slot for variant in variants for slot in variant["set"]}))

                observed_variant_ids = set()
                for seed in range(1, 65):
                    _args, explanations = generate_photo_prompt.resolve_concepts(
                        ["--selection-mode", "rule", "--seed", str(seed)],
                        [role],
                        concept_mode="soft",
                    )
                    explanation = explanations[0]
                    selected_scene = explanation["selected_scene_variants"][0]
                    observed_variant_ids.add(selected_scene["id"])
                    forced = explanation["combined_forced_slots"]
                    for slot, ids in identity.items():
                        self.assertEqual(forced[slot], ids)

                    atomic_group = f"role_scene:{selected_scene['id']}"
                    anchors = {
                        anchor["slot"]: anchor
                        for anchor in explanation["soft_anchor_spec"]["anchors"]
                    }
                    for slot, raw_ids in selected_scene["set"].items():
                        ids = [raw_ids] if isinstance(raw_ids, str) else raw_ids
                        self.assertEqual(anchors[slot]["pool"], ids)
                        self.assertEqual(anchors[slot]["variant_group"], atomic_group)
                        self.assertEqual(anchors[slot]["variant_strategy"], "atomic_scene")

                self.assertEqual(observed_variant_ids, expected_variant_ids)

    def test_high_creativity_marks_existing_contrasts_without_reordering_candidates(self):
        base_args = (
            "--concept",
            "도예가",
            "--selection-mode",
            "rule",
            "--seed",
            "42",
            "--emit-candidate-pack",
        )
        base_pack = self.run_wrapper(*base_args)[0]
        low_pack = self.run_wrapper(*base_args, "--creativity", "0.74")[0]
        creative_pack = self.run_wrapper(*base_args, "--creativity", "0.85")[0]
        repeated_pack = self.run_wrapper(*base_args, "--creativity", "0.85")[0]

        self.assertNotIn("creative_exploration", base_pack)
        self.assertNotIn("creative_exploration", low_pack)
        self.assertNotIn("creative_direction", base_pack)
        self.assertNotIn("creative_direction", low_pack)
        exploration = creative_pack["creative_exploration"]
        self.assertEqual(exploration, repeated_pack["creative_exploration"])
        self.assertEqual(exploration["source"], "exposed_sampler_eligible_pool")
        self.assertGreater(exploration["contrast_candidate_count"], 0)
        direction = creative_pack["creative_direction"]
        self.assertEqual(direction, repeated_pack["creative_direction"])
        self.assertEqual(direction["contract_version"], "photo-creative-direction/v1")
        self.assertEqual(direction["source"], "explicit_creativity_control")
        self.assertEqual(direction["proposal_contract"]["minimum_proposals"], 4)
        self.assertEqual(direction["proposal_contract"]["select_exactly"], 1)
        self.assertEqual(direction["selected_concept_contract"]["rule_break_count"], 1)
        self.assertEqual(direction["selected_concept_contract"]["minimum_visible_consequences"], 2)
        self.assertEqual(
            set(direction["selected_concept_contract"]["authorial_grammar_fields"]),
            {"vantage", "timing", "omission", "material_rule"},
        )
        self.assertEqual(direction["artistic_final_touch_role"], "surface_craft_only_not_authorial_evidence")
        viewer = creative_pack["viewer_experience"]
        self.assertEqual(viewer["contract_version"], "photo-viewer-experience/v1")
        self.assertIn("creative_direction_required", viewer["activation_sources"])
        self.assertEqual(viewer["conditional_rules"]["attachment_required_for_needs"], ["care", "relatedness", "identity"])
        self.assertEqual(
            viewer["conditional_rules"]["commercial_legibility_required_for_objectives"],
            ["comprehend", "remember", "act"],
        )

        self.assertEqual(base_pack["presets"], creative_pack["presets"])
        self.assertEqual(set(base_pack["slots"]), set(creative_pack["slots"]))
        for slot in base_pack["slots"]:
            base_slot = base_pack["slots"][slot]
            creative_slot = creative_pack["slots"][slot]
            self.assertNotIn("selected", base_slot)
            self.assertNotIn("selected", creative_slot)
            self.assertEqual(
                [candidate["id"] for candidate in base_slot["candidates"]],
                [candidate["id"] for candidate in creative_slot["candidates"]],
            )

        for contrast in exploration["contrast_candidates"]:
            slot_payload = creative_pack["slots"][contrast["slot"]]
            candidates = {candidate["id"]: candidate for candidate in slot_payload["candidates"]}
            candidate = candidates[contrast["candidate_id"]]
            self.assertNotIn("replaces_candidate_id", contrast)
            self.assertNotIn("relevance_rank", contrast)
            self.assertNotIn("selected_by_sampler", candidate)
            self.assertEqual(candidate["applicability"]["status"], "eligible")
            self.assertEqual(candidate["applicability"]["source"], "sampler_eligible_pool")
            self.assertGreaterEqual(
                contrast["feature_distance"],
                exploration["minimum_feature_distance"],
            )
        self.assertEqual(
            exploration["composition_guidance"]["candidate_use"],
            "optional_authorial_inspiration",
        )

    def test_hybrid_augmentation_exposes_real_candidate_routes_and_audits_selective_adoption(self):
        base_args = (
            "--preset",
            "candid_iphone_portrait",
            "--selection-mode",
            "rule",
            "--seed",
            "20260809",
            "--emit-candidate-pack",
        )
        ordinary = self.run_wrapper(
            *base_args,
            "--sensual-editorial-intensity",
            "0",
            "--fetish-fashion-intensity",
            "0",
        )[0]
        hybrid_pack = self.run_wrapper(*base_args, "--hybrid-augmentation")[0]
        repeated = self.run_wrapper(*base_args, "--hybrid-augmentation")[0]

        self.assertNotIn("hybrid_augmentation", ordinary)
        hybrid = hybrid_pack["hybrid_augmentation"]
        self.assertEqual(hybrid, repeated["hybrid_augmentation"])
        self.assertEqual(hybrid["contract_version"], "photo-hybrid-augmentation/v2")
        self.assertEqual(hybrid["route_contract"]["route_count"], 3)
        self.assertTrue(hybrid["route_contract"]["allow_select_none"])
        exposed_ids = audit_composed_prompt.candidate_ids_from_pack(hybrid_pack)
        for route in hybrid["route_contract"]["routes"]:
            self.assertGreaterEqual(len(route["candidate_ids"]), 2)
            self.assertLessEqual(len(route["candidate_ids"]), 4)
            self.assertTrue(set(route["candidate_ids"]) <= exposed_ids)
            self.assertEqual(
                route["candidate_ids"],
                [detail["candidate_id"] for detail in route["details"]],
            )

        selected_route = hybrid["route_contract"]["routes"][0]["id"]
        composed = self.composed_from_hybrid_route(hybrid_pack, selected_route)
        passed = audit_composed_prompt.audit_composed_prompt(hybrid_pack, composed)
        self.assertEqual(passed["status"], "pass", passed)

        missing = copy.deepcopy(composed)
        missing.pop("augmentation_brief")
        missing_result = audit_composed_prompt.audit_composed_prompt(hybrid_pack, missing)
        self.assertIn("hybrid_augmentation", {row["check"] for row in missing_result["failures"]})

        rejected_but_chosen = copy.deepcopy(composed)
        rejected_id = next(
            row["candidate_id"]
            for row in rejected_but_chosen["augmentation_brief"]["decisions"]
            if row["decision"] == "rejected"
        )
        rejected_but_chosen["chosen_candidate_ids"].append(rejected_id)
        rejected_result = audit_composed_prompt.audit_composed_prompt(
            hybrid_pack, rejected_but_chosen
        )
        self.assertIn(
            "hybrid_augmentation_provenance",
            {row["check"] for row in rejected_result["failures"]},
        )

    def test_v4_hybrid_requires_new_authorial_context_and_varies_candidate_routes(self):
        packs = [
            self.run_wrapper(
                "--concept",
                "모에한 간호사",
                "--selection-mode",
                "rule",
                "--seed",
                str(seed),
                "--emit-candidate-pack",
            )[0]
            for seed in range(1, 9)
        ]
        signatures = {
            tuple(
                tuple(route["candidate_ids"])
                for route in pack["hybrid_augmentation"]["route_contract"]["routes"]
            )
            for pack in packs
        }
        lenses = {pack["authorial_composition"]["variation_lens"] for pack in packs}
        self.assertGreater(len(signatures), 1)
        self.assertGreater(len(lenses), 1)
        for candidate_pack in packs:
            self.assertEqual(
                {row["slot"] for row in candidate_pack["authorial_open_slots"]},
                {"subject", "action", "location", "prop"},
            )
            self.assertTrue(
                {"subject", "action", "location", "prop"}.isdisjoint(candidate_pack["slots"])
            )

        pack = self.run_wrapper(
            "--preset",
            "candid_iphone_portrait",
            "--selection-mode",
            "rule",
            "--seed",
            "1",
            "--emit-candidate-pack",
        )[0]
        hybrid = pack["hybrid_augmentation"]
        route = hybrid["route_contract"]["routes"][0]
        for detail in route["details"]:
            self.assertNotIn("label_en", detail)
            self.assertNotIn("label_ko", detail)
            self.assertEqual(detail["content_form"], "unordered_inspiration_terms")
            self.assertTrue(detail["concept_terms"])

        composed = self.composed_from_hybrid_route(pack, route["id"])
        self.assertEqual(
            audit_composed_prompt.audit_composed_prompt(pack, composed)["status"],
            "pass",
        )
        copied_terms = copy.deepcopy(composed)
        transformed = next(
            row
            for row in copied_terms["augmentation_brief"]["decisions"]
            if row["decision"] == "transformed"
        )
        source = audit_composed_prompt.candidate_objects_from_pack(pack)[
            transformed["candidate_id"]
        ]
        source_only = " ".join(source["concept_terms"][:3])
        transformed["prompt_evidence"] = source_only
        copied_terms["prompt_en"] += f" {source_only}."
        copied_result = audit_composed_prompt.audit_composed_prompt(pack, copied_terms)
        self.assertIn(
            "hybrid_augmentation_authorial_transform",
            {row["check"] for row in copied_result["failures"]},
        )

        axis_phrase = "an authored sensual editorial accent follows her deliberate gesture"
        reject_all = {
            "pack_id": pack["pack_id"],
            "prompt_en": (
                "An adult original portrait subject holds a self-directed editorial pose; "
                f"{axis_phrase}."
            ),
            "negative_en": pack["negative_en"],
            "chosen_candidate_ids": [],
            "composer": "agent",
            "augmentation_brief": {
                "concept_core": "A private observational portrait governed by the subject's agency.",
                "routes_considered": [
                    {
                        "route_id": row["id"],
                        "decision": "rejected",
                        "reason": "Its vocabulary would narrow the authored portrait.",
                    }
                    for row in hybrid["route_contract"]["routes"]
                ],
                "selected_route_id": "none",
                "all_rejected_reason": "None of the candidate vocabularies improves the governing idea.",
                "decisions": [],
                "adult_appeal": {
                    "adult_subject_phrase": "An adult original portrait subject",
                    "agency_phrase": "self-directed editorial pose",
                    "axes": {
                        axis_id: {
                            "intensity": axis["intensity"],
                            **(
                                {
                                    "artistic_interpretation": "Keep the axis as quiet self-possession.",
                                    "prompt_evidence": axis_phrase,
                                }
                                if axis["intensity"] > 0
                                else {}
                            ),
                        }
                        for axis_id, axis in hybrid["adult_appeal"]["axes"].items()
                    },
                    "blend": {"emphasis": hybrid["adult_appeal"]["blend"]["emphasis"]},
                },
            },
        }
        self.assertEqual(
            audit_composed_prompt.audit_composed_prompt(pack, reject_all)["status"],
            "pass",
        )

    def test_v4_scene_exposes_only_abstraction_and_audits_newly_authored_atoms(self):
        common = (
            "--preset",
            "natural_process_trace_documentary",
            "--selection-mode",
            "rule",
            "--seed",
            "42",
            "--emit-candidate-pack",
        )
        pack = self.run_wrapper(*common)[0]
        prior = self.run_wrapper(*common, "--candidate-pack-version", "v3")[0]
        prior_atoms = prior["render_contract"]["selected_scene"]["atomic_scene"]
        projected_blob = json.dumps(pack, ensure_ascii=False)
        for slot in ("subject", "action", "location", "prop"):
            self.assertNotIn(prior_atoms[slot]["label_en"], projected_blob)

        selected_scene = pack["render_contract"]["selected_scene"]
        self.assertNotIn("blueprint_id", selected_scene)
        self.assertNotIn("source_blueprint_hash", selected_scene)
        self.assertNotIn("atomic_scene", selected_scene)
        self.assertEqual(
            selected_scene["authorial_scene"]["contract_version"],
            "photo-authorial-scene/v1",
        )
        group = next(
            row
            for row in pack["scene_contract"]["groups"]
            if row.get("strategy") == "authorial_scene"
        )
        self.assertNotIn("slots", group)
        self.assertEqual(
            set(group["required_authored_slots"]),
            {"subject", "action", "location", "prop"},
        )

        atoms = {
            "subject": "A thaw line advances through a hand-sized patch of moss",
            "action": "Meltwater loosens one ice crystal while the boundary is still moving",
            "location": "A shaded forest floor at the first hour of morning thaw",
            "prop": "A bent copper field marker catches one suspended droplet",
        }
        composed = {
            "pack_id": pack["pack_id"],
            "prompt_en": (
                "Natural-process trace documentary. "
                + ". ".join(atoms.values())
                + ". Shared side light links the marker and moss, with foreground blur from a real camera position."
            ),
            "negative_en": pack["negative_en"],
            "chosen_candidate_ids": [],
            "composer": "agent",
            "authored_scene": {
                "governing_premise": "Thaw becomes legible as an unfinished material crossing.",
                "artistic_rationale": "The marker turns time into a measurable but intimate trace.",
                "atoms": atoms,
                "interpretive_choices": [
                    {
                        "dimension": "action",
                        "decision": "Freeze the boundary mid-release.",
                        "reason": "An unfinished transition carries more tension than a completed melt.",
                    },
                    {
                        "dimension": "material",
                        "decision": "Use copper against ice and moss.",
                        "reason": "Contrasting thermal surfaces make the process visible.",
                    },
                ],
            },
        }
        passed = audit_composed_prompt.audit_composed_prompt(pack, composed)
        self.assertEqual(passed["status"], "pass", passed)
        missing = copy.deepcopy(composed)
        missing.pop("authored_scene")
        failed = audit_composed_prompt.audit_composed_prompt(pack, missing)
        self.assertIn("authorial_scene", {row["check"] for row in failed["failures"]})

    def test_v4_opens_singleton_role_scene_slots_for_agent_authorship(self):
        pack = self.run_wrapper(
            "--concept",
            "간호사",
            "--selection-mode",
            "rule",
            "--seed",
            "1",
            "--emit-candidate-pack",
        )[0]
        open_contracts = {
            row["slot"]: row for row in pack["authorial_open_slots"]
        }
        self.assertEqual(set(open_contracts), {"subject", "action", "location", "prop"})
        for slot in open_contracts:
            self.assertNotIn(slot, pack["slots"])
        self.assertEqual(
            pack["role_scene_policy"]["selection_mode"],
            "agent_authored_location",
        )
        self.assertNotIn("allowed_locations", pack["role_scene_policy"])
        self.assertNotIn("preferred_locations", pack["role_scene_policy"])

        route_id = pack["hybrid_augmentation"]["route_contract"]["routes"][0]["id"]
        composed = self.composed_from_hybrid_route(pack, route_id, accept_count=1)
        authored_slots = {
            "subject": {
                "prompt_evidence": "an adult nurse with an alert but gentle expression",
                "artistic_rationale": "Professional identity stays clear without copying a role label.",
            },
            "action": {
                "prompt_evidence": "she pauses while warming a cold stethoscope between both palms",
                "artistic_rationale": "A considerate gesture replaces the routine handover scene.",
            },
            "location": {
                "prompt_evidence": "inside a quiet overnight pediatric preparation bay",
                "artistic_rationale": "The care setting supports anticipation rather than crisis.",
                "constraint_acknowledgments": ["clinical_care_space"],
            },
            "prop": {
                "prompt_evidence": "a paper crane left beside the unopened examination kit",
                "artistic_rationale": "The prop implies a prior patient relationship without a chart.",
            },
        }
        composed["authored_slots"] = authored_slots
        composed["prompt_en"] += "; " + "; ".join(
            row["prompt_evidence"] for row in authored_slots.values()
        ) + "."
        composed["coverage_assertions"] = {"간호사": "adult nurse"}
        passed = audit_composed_prompt.audit_composed_prompt(pack, composed)
        self.assertEqual(passed["status"], "pass", passed)

        incompatible = copy.deepcopy(composed)
        incompatible_phrase = "on a highland pasture beside grazing animals"
        incompatible["authored_slots"]["location"]["prompt_evidence"] = incompatible_phrase
        incompatible["prompt_en"] += f" {incompatible_phrase}."
        failed = audit_composed_prompt.audit_composed_prompt(pack, incompatible)
        self.assertIn(
            "authorial_open_slot_constraints",
            {row["check"] for row in failed["failures"]},
        )

    def test_adult_appeal_defaults_to_sensual_only_for_eligible_humans(self):
        common = (
            "--selection-mode",
            "rule",
            "--emit-candidate-pack",
        )
        human = self.run_wrapper(
            "--preset",
            "candid_iphone_portrait",
            "--seed",
            "20260809",
            *common,
        )[0]
        adult = human["hybrid_augmentation"]["adult_appeal"]
        self.assertTrue(adult["enabled"])
        self.assertEqual(adult["activation_source"], "skill_default")
        self.assertEqual(adult["eligibility"]["status"], "eligible")
        self.assertEqual(adult["contract_version"], "photo-adult-appeal/v2")
        self.assertEqual(adult["defaults"]["sensual_editorial_intensity"], 1)
        self.assertEqual(adult["defaults"]["fetish_fashion_intensity"], 0)
        self.assertEqual(adult["defaults"]["emphasis"], "sensual_led")
        self.assertEqual(adult["axes"]["sensual_editorial"]["intensity"], 1)
        self.assertEqual(adult["axes"]["fetish_fashion"]["intensity"], 0)
        self.assertFalse(adult["axes"]["fetish_fashion"]["active"])
        self.assertEqual(adult["axes"]["fetish_fashion"]["candidate_inventory"], [])
        self.assertEqual(adult["blend"]["emphasis"], "sensual_led")
        self.assertEqual(
            set(adult["eligibility"]),
            {"status", "reason", "subject_category"},
        )
        self.assertEqual(
            set(adult["combination_policy"]),
            {"risk_groups", "hard_combinations", "warning_combinations"},
        )

        opted_out = self.run_wrapper(
            "--preset",
            "candid_iphone_portrait",
            "--seed",
            "20260809",
            *common,
            "--sensual-editorial-intensity",
            "0",
            "--fetish-fashion-intensity",
            "0",
        )[0]
        self.assertNotIn("hybrid_augmentation", opted_out)

        nonhuman = self.run_wrapper(
            "--preset",
            "street_documentary",
            "--seed",
            "910000",
            *common,
        )[0]
        self.assertIn(
            "sleeping_dog",
            {candidate["entry_id"] for candidate in nonhuman["slots"]["subject"]["candidates"]},
        )
        self.assertNotIn("hybrid_augmentation", nonhuman)

        direct_prompt = self.run_wrapper(
            "--preset",
            "candid_iphone_portrait",
            "--selection-mode",
            "rule",
            "--seed",
            "20260809",
        )[0]
        direct_adult = direct_prompt["provenance"]["adult_appeal"]
        self.assertTrue(direct_adult["configured"])
        self.assertFalse(direct_adult["enabled"])
        self.assertEqual(direct_adult["application_scope"], "candidate_pack_composition")

    def test_natural_moe_response_contract_routes_multilingual_requests_and_hard_negatives(self):
        data = prompt_generator.load_json(TAGS_PATH)
        data[prompt_generator.QUALITY_LAYERS_DATA_KEY] = prompt_generator.load_quality_layers(
            QUALITY_LAYERS_PATH
        )
        cases = [
            json.loads(line)
            for line in NATURAL_MOE_RESPONSE_CONTRACT_V1_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(cases), 32)
        self.assertEqual(len({case["id"] for case in cases}), 32)
        for case in cases:
            expected = case["expected"]
            response = prompt_generator.resolve_moe_response_intent([case["text"]])
            for key, value in expected.items():
                self.assertEqual(response.get(key), value, (case["id"], key, response))
            routed = prompt_generator.resolve_request_intent_constraints(
                data,
                {"intent": case["text"]},
                {},
            )
            if expected["requested"]:
                self.assertIn("character_moe_grammar", routed["domains"], case["id"])
                self.assertIn(expected["route_id"], routed["scoped_routes"], case["id"])
                self.assertEqual(
                    routed["character_response"]["sexual_tone"],
                    expected["sexual_tone"],
                    case["id"],
                )
                self.assertEqual(
                    routed["character_response"]["aesthetic_baseline"],
                    expected["aesthetic_baseline"],
                    case["id"],
                )
                if expected.get("relationship_register"):
                    self.assertEqual(
                        routed["character_response"]["relationship_register"],
                        expected["relationship_register"],
                        case["id"],
                    )
            else:
                self.assertNotIn("character_moe_grammar", routed["domains"], case["id"])
                self.assertFalse(routed["character_response"]["requested"], case["id"])

    def test_natural_moe_response_contract_materializes_through_public_wrapper(self):
        cases = [
            json.loads(line)
            for line in NATURAL_MOE_RESPONSE_CONTRACT_V1_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        role_contracts = {
            "ko_tsundere_nekomimi_maid": {
                "preset_id": "maid_cafe_cosplay_portrait",
                "subject_id": "slot:subject:maid_cafe_performer",
                "costume_id": "slot:costume_style:frill_apron_maid_costume",
            },
            "ja_tsundere_nekomimi_maid": {
                "preset_id": "maid_cafe_cosplay_portrait",
                "subject_id": "slot:subject:maid_cafe_performer",
                "costume_id": "slot:costume_style:frill_apron_maid_costume",
            },
            "en_tsundere_cat_ear_maid": {
                "preset_id": "maid_cafe_cosplay_portrait",
                "subject_id": "slot:subject:maid_cafe_performer",
                "costume_id": "slot:costume_style:frill_apron_maid_costume",
            },
            "ko_mamang_nekomimi_maid": {
                "preset_id": "maid_cafe_cosplay_portrait",
                "subject_id": "slot:subject:maid_cafe_performer",
                "costume_id": "slot:costume_style:frill_apron_maid_costume",
            },
            "ja_maternal_nekomimi_maid": {
                "preset_id": "maid_cafe_cosplay_portrait",
                "subject_id": "slot:subject:maid_cafe_performer",
                "costume_id": "slot:costume_style:frill_apron_maid_costume",
            },
            "en_motherly_cat_eared_maid": {
                "preset_id": "maid_cafe_cosplay_portrait",
                "subject_id": "slot:subject:maid_cafe_performer",
                "costume_id": "slot:costume_style:frill_apron_maid_costume",
            },
            "ko_gap_moe_guard": {
                "preset_id": "security_guard_watch_portrait",
                "subject_id": "slot:subject:security_guard_role_model",
            },
            "ko_nekomimi_barista": {
                "preset_id": "tray_handoff_counter",
                "subject_id": "slot:subject:young_barista",
            },
            "en_moe_explicit_readable_sign": {
                "preset_id": "tray_handoff_counter",
                "subject_id": "slot:subject:young_barista",
            },
        }
        feline_case_ids = {
            "ko_tsundere_nekomimi_maid",
            "ja_tsundere_nekomimi_maid",
            "en_tsundere_cat_ear_maid",
            "ko_nekomimi_barista",
            "ko_mamang_nekomimi_maid",
            "ja_maternal_nekomimi_maid",
            "en_motherly_cat_eared_maid",
        }

        self.assertEqual(len(cases), 32)
        for index, case in enumerate(cases):
            expected = case["expected"]
            pack = self.run_wrapper(
                "--concept",
                case["text"],
                "--selection-mode",
                "rule",
                "--hybrid-augmentation",
                "--emit-candidate-pack",
                "--seed",
                str(20260840 + index),
                "--candidate-pack-version",
                "v3",
            )[0]

            if not expected["requested"]:
                self.assertNotIn("moe_response", pack, case["id"])
                self.assertFalse(
                    (pack.get("provenance", {}).get("character_response") or {}).get(
                        "requested", False
                    ),
                    case["id"],
                )
                continue

            response = pack["moe_response"]
            for key in (
                "route_id",
                "primary_mechanism",
                "support_mechanisms",
                "aesthetic_baseline",
                "aesthetic_presentation_source",
                "sexual_tone",
            ):
                self.assertEqual(response.get(key), expected[key], (case["id"], key))
            if expected.get("relationship_register"):
                self.assertEqual(
                    response["relationship_register"],
                    expected["relationship_register"],
                    case["id"],
                )
            self.assertEqual(
                response["explicit_text_requested"],
                expected.get("explicit_text_requested", False),
                case["id"],
            )

            adult = pack["hybrid_augmentation"]["adult_appeal"]
            expected_axes = (
                {"sensual_editorial": 0, "fetish_fashion": 0}
                if expected["sexual_tone"] == "nonsexual"
                else {"sensual_editorial": 1, "fetish_fashion": 0}
            )
            self.assertEqual(
                {axis_id: axis["intensity"] for axis_id, axis in adult["axes"].items()},
                expected_axes,
                case["id"],
            )
            self.assertEqual(
                adult["enabled"],
                expected["sexual_tone"] != "nonsexual",
                case["id"],
            )

            role_contract = role_contracts.get(case["id"])
            if role_contract:
                self.assertEqual(
                    pack["provenance"]["preset_id"],
                    role_contract["preset_id"],
                    case["id"],
                )
                self.assertEqual(
                    pack["slots"]["subject"]["selected"],
                    role_contract["subject_id"],
                    case["id"],
                )
                self.assertTrue(pack["slots"]["action"]["selected"], case["id"])
                self.assertTrue(pack["slots"]["location"]["selected"], case["id"])
                if role_contract.get("costume_id"):
                    self.assertEqual(
                        pack["slots"]["costume_style"]["selected"],
                        role_contract["costume_id"],
                        case["id"],
                    )
            else:
                selected_scene = pack["render_contract"]["selected_scene"]
                self.assertTrue(selected_scene["blueprint_id"], case["id"])
                self.assertEqual(
                    set(selected_scene["atomic_scene"]),
                    {"subject", "action", "location", "prop"},
                    case["id"],
                )

            if case["id"] in feline_case_ids:
                self.assertEqual(pack["species_family"]["family"], "feline", case["id"])
                self.assertTrue(pack["species_family"]["enforce"], case["id"])
                self.assertEqual(
                    pack["species_family"]["allowed"],
                    {
                        "species_marker": ["feline_reflective_eye_whisker_shadow"],
                        "anatomical_connection": ["ear_root_in_hairline"],
                    },
                    case["id"],
                )

    def test_natural_moe_paraphrases_materialize_routed_scenes_without_internal_presets(self):
        cases = [
            {
                "id": "ko_tsundere_care_paraphrase",
                "text": (
                    "노출이나 선정적 연출 없이 성인 여성 츤데레 캐릭터가 괜히 퉁명스럽게 "
                    "다친 친구를 챙기는 모습이 정말 모에하게 보여야 해"
                ),
                "preset_id": "character_gap_contrast_scene",
                "mechanism": "denial_care_leak",
                "relationship_register": "peer_liking_under_denial",
                "blueprint_id": "gap_moe_contrast_structure_natural_tsundere_01",
                "aesthetic_baseline": "adult_bishoujo",
                "sexual_tone": "nonsexual",
            },
            {
                "id": "ja_gap_bishonen_paraphrase",
                "text": (
                    "露出なしで、大人の男性キャラクターが失敗を隠そうとして不器用に立て直す"
                    "ギャップ萌えの写真"
                ),
                "preset_id": "character_gap_contrast_scene",
                "mechanism": "baseline_break_reveal",
                "relationship_register": "character_specific_reveal",
                "blueprint_id": "gap_moe_contrast_structure_atomic_04",
                "aesthetic_baseline": "adult_bishonen",
                "sexual_tone": "nonsexual",
            },
            {
                "id": "en_androgynous_nekomimi_paraphrase",
                "text": (
                    "Make an adult androgynous cat-eared character feel genuinely moe through a tiny "
                    "involuntary ear reaction, without sensual framing"
                ),
                "preset_id": "character_nonhuman_expression_scene",
                "mechanism": "nonhuman_reflex_leak",
                "relationship_register": "character_specific_reveal",
                "blueprint_id": "kemonomimi_nonhuman_anthropomorphism_atomic_04",
                "aesthetic_baseline": "adult_beautiful_cute_character",
                "sexual_tone": "nonsexual",
            },
            {
                "id": "ko_nekomimi_sensual_optional_paraphrase",
                "text": (
                    "예쁘고 귀여운 성인 여성 네코미미 캐릭터가 무심코 귀를 움직이는 모에 사진"
                ),
                "preset_id": "character_nonhuman_expression_scene",
                "mechanism": "nonhuman_reflex_leak",
                "relationship_register": "character_specific_reveal",
                "blueprint_id": "kemonomimi_nonhuman_anthropomorphism_atomic_04",
                "aesthetic_baseline": "adult_bishoujo",
                "sexual_tone": "sensual_optional",
            },
        ]
        for index, case in enumerate(cases):
            pack = self.run_wrapper(
                "--concept",
                case["text"],
                "--selection-mode",
                "rule",
                "--emit-candidate-pack",
                "--seed",
                str(20260830 + index),
                "--candidate-pack-version",
                "v3",
            )[0]
            self.assertEqual(pack["provenance"]["preset_id"], case["preset_id"], case["id"])
            self.assertEqual(pack["moe_response"]["primary_mechanism"], case["mechanism"], case["id"])
            self.assertEqual(
                pack["moe_response"]["relationship_register"],
                case["relationship_register"],
                case["id"],
            )
            self.assertEqual(
                pack["moe_response"]["aesthetic_baseline"],
                case["aesthetic_baseline"],
                case["id"],
            )
            self.assertEqual(pack["moe_response"]["sexual_tone"], case["sexual_tone"], case["id"])
            self.assertEqual(
                pack["render_contract"]["selected_scene"]["blueprint_id"],
                case["blueprint_id"],
                case["id"],
            )
            scene_blob = " ".join(
                pack["render_contract"]["selected_scene"]["atomic_scene"][slot]["label_en"]
                for slot in ("subject", "action", "location", "prop")
            ).lower()
            for leakage in ("technician", "repair", "coworker", "maintenance", "shift"):
                self.assertNotIn(leakage, scene_blob, (case["id"], leakage, scene_blob))

    def test_nonsexual_moe_concept_preserves_role_species_and_disables_sensual_default(self):
        pack = self.run_wrapper(
            "--concept",
            "야하지 않은 모에한 성인 네코미미 츤데레 메이드",
            "--selection-mode",
            "rule",
            "--hybrid-augmentation",
            "--emit-candidate-pack",
            "--seed",
            "20260812",
            "--candidate-pack-version",
            "v3",
        )[0]
        self.assertEqual(pack["provenance"]["preset_id"], "maid_cafe_cosplay_portrait")
        self.assertEqual(pack["slots"]["subject"]["selected"], "slot:subject:maid_cafe_performer")
        self.assertEqual(pack["slots"]["location"]["selected"], "slot:location:maid_cafe_interior")
        self.assertEqual(pack["provenance"]["likeness_mode"], "off")
        self.assertEqual(pack["provenance"]["likeness_references"], [])
        self.assertEqual(pack["species_family"]["family"], "feline")
        self.assertTrue(pack["species_family"]["enforce"])

        response = pack["moe_response"]
        self.assertEqual(response["contract_version"], "moe_response_contract/v10")
        self.assertEqual(
            response["composition_guidance"]["prompt_budget"],
            {
                "language": "en",
                "minimum_words": 50,
                "maximum_words": 120,
                "counting_rule": "ascii_words_with_internal_hyphens_or_apostrophes",
                "rule": (
                    "Keep prompt_en between 50 and 120 English words. Reuse short literal phrases across "
                    "moe, viewer, identity, and augmentation evidence instead of stacking explanations."
                ),
            },
        )
        self.assertEqual(response["aesthetic_baseline"], "adult_bishoujo")
        self.assertEqual(response["aesthetic_presentation_source"], "default_bishoujo")
        self.assertEqual(response["primary_mechanism"], "denial_care_leak")
        self.assertIn(
            "active_denial_phrase",
            response["prompt_binding"]["required_evidence_fields"],
        )
        self.assertIn(
            "concealed_affection_phrase",
            response["prompt_binding"]["required_evidence_fields"],
        )
        self.assertIn(
            "care_action_anchor_phrase",
            response["prompt_binding"]["required_evidence_fields"],
        )
        self.assertIn(
            "relationship_gaze_anchor_phrase",
            response["prompt_binding"]["required_evidence_fields"],
        )
        self.assertTrue(
            response["composition_guidance"]["mechanism_specific_evidence"]
            ["denial_care_leak"]["active_denial_phrase_required"]
        )
        self.assertTrue(
            response["composition_guidance"]["mechanism_specific_evidence"]
            ["denial_care_leak"]["concealed_affection_phrase_required"]
        )
        self.assertTrue(
            response["composition_guidance"]["mechanism_specific_evidence"]
            ["denial_care_leak"]["care_action_anchor_phrase_required"]
        )
        self.assertTrue(
            response["composition_guidance"]["mechanism_specific_evidence"]
            ["denial_care_leak"]["relationship_gaze_anchor_phrase_required"]
        )
        self.assertTrue(
            response["composition_guidance"]["mechanism_specific_evidence"]
            ["denial_care_leak"]["partial_recipient_landmark_required"]
        )
        self.assertTrue(
            response["composition_guidance"]["mechanism_specific_evidence"]
            ["denial_care_leak"]["opposed_head_iris_vector_required"]
        )
        self.assertTrue(
            response["composition_guidance"]["mechanism_specific_evidence"]
            ["denial_care_leak"]["off_axis_gaze_geometry_required"]
        )
        self.assertTrue(
            response["composition_guidance"]["mechanism_specific_evidence"]
            ["denial_care_leak"]["dual_positive_microcue_required"]
        )
        self.assertEqual(response["relationship_register"], "peer_liking_under_denial")
        self.assertEqual(response["support_mechanisms"], ["nonhuman_reflex_leak"])
        self.assertEqual(response["sexual_tone"], "nonsexual")
        self.assertEqual(pack["viewer_experience"]["activation_sources"], ["moe_response_required"])

        mamang = self.run_wrapper(
            "--concept",
            "인자한 마망 느낌의 예쁘고 귀여운 성인 캐릭터를 모에하게",
            "--selection-mode",
            "rule",
            "--emit-candidate-pack",
            "--seed",
            "20260818",
            "--candidate-pack-version",
            "v3",
        )[0]
        self.assertEqual(mamang["moe_response"]["primary_mechanism"], "quiet_care_trace")
        self.assertEqual(
            mamang["moe_response"]["relationship_register"],
            "nurturant_benevolence",
        )
        self.assertIn(
            "relaxed brow",
            mamang["moe_response"]["relationship_register_instruction"],
        )
        self.assertIn(
            "reassuring mouth",
            mamang["moe_response"]["relationship_register_instruction"],
        )
        self.assertNotIn(
            "active_denial_phrase",
            mamang["moe_response"]["prompt_binding"]["required_evidence_fields"],
        )
        self.assertNotIn(
            "relationship_gaze_anchor_phrase",
            mamang["moe_response"]["prompt_binding"]["required_evidence_fields"],
        )
        self.assertIn(
            "benevolent_affect_phrase",
            mamang["moe_response"]["prompt_binding"]["required_evidence_fields"],
        )
        self.assertTrue(
            mamang["moe_response"]["composition_guidance"]
            ["mechanism_specific_evidence"]["nurturant_benevolence"]
            ["benevolent_affect_phrase_required"]
        )

        ordinary_care = self.run_wrapper(
            "--concept",
            "친구를 다정하게 챙겨주는 예쁘고 귀여운 성인 캐릭터를 모에하게",
            "--selection-mode",
            "rule",
            "--emit-candidate-pack",
            "--seed",
            "20260818",
            "--candidate-pack-version",
            "v3",
        )[0]
        self.assertEqual(
            ordinary_care["moe_response"]["primary_mechanism"],
            "quiet_care_trace",
        )
        self.assertEqual(
            ordinary_care["moe_response"]["relationship_register"],
            "directed_care_without_role_inference",
        )
        self.assertIn(
            "without inferring motherhood",
            ordinary_care["moe_response"]["relationship_register_instruction"],
        )
        self.assertNotIn(
            "benevolent_affect_phrase",
            ordinary_care["moe_response"]["prompt_binding"]["required_evidence_fields"],
        )

        mamang_nekomimi = self.run_wrapper(
            "--concept",
            "인자한 마망 느낌의 예쁘고 귀여운 성인 네코미미 메이드 캐릭터를 모에하게",
            "--selection-mode",
            "rule",
            "--emit-candidate-pack",
            "--seed",
            "20260818",
        )[0]
        self.assertEqual(
            mamang_nekomimi["moe_response"]["primary_mechanism"],
            "quiet_care_trace",
        )
        self.assertEqual(
            mamang_nekomimi["moe_response"]["relationship_register"],
            "nurturant_benevolence",
        )
        self.assertEqual(
            mamang_nekomimi["moe_response"]["support_mechanisms"],
            ["nonhuman_reflex_leak"],
        )
        self.assertIn(
            "benevolent_affect_phrase",
            mamang_nekomimi["moe_response"]["prompt_binding"]["required_evidence_fields"],
        )

        japanese_mamang_nekomimi = self.run_wrapper(
            "--concept",
            "母性的で優しいママみのある、美しくてかわいい成人猫耳メイドの萌える写真",
            "--selection-mode",
            "rule",
            "--emit-candidate-pack",
            "--seed",
            "20260818",
            "--candidate-pack-version",
            "v3",
        )[0]
        self.assertEqual(
            japanese_mamang_nekomimi["moe_response"]["primary_mechanism"],
            "quiet_care_trace",
        )
        self.assertEqual(
            japanese_mamang_nekomimi["moe_response"]["relationship_register"],
            "nurturant_benevolence",
        )
        self.assertEqual(
            japanese_mamang_nekomimi["moe_response"]["support_mechanisms"],
            ["nonhuman_reflex_leak"],
        )
        self.assertEqual(
            japanese_mamang_nekomimi["provenance"]["preset_id"],
            "maid_cafe_cosplay_portrait",
        )
        self.assertEqual(
            japanese_mamang_nekomimi["slots"]["subject"]["selected"],
            "slot:subject:maid_cafe_performer",
        )
        self.assertEqual(
            japanese_mamang_nekomimi["slots"]["costume_style"]["selected"],
            "slot:costume_style:frill_apron_maid_costume",
        )
        self.assertEqual(japanese_mamang_nekomimi["species_family"]["family"], "feline")
        self.assertEqual(
            japanese_mamang_nekomimi["species_family"]["allowed"],
            {
                "species_marker": ["feline_reflective_eye_whisker_shadow"],
                "anatomical_connection": ["ear_root_in_hairline"],
            },
        )

        japanese_tsundere_nekomimi = self.run_wrapper(
            "--concept",
            "性的ではない猫耳の成人ツンデレメイドが、世話を焼いたことを隠す萌える瞬間",
            "--selection-mode",
            "rule",
            "--emit-candidate-pack",
            "--seed",
            "20260818",
            "--candidate-pack-version",
            "v3",
        )[0]
        self.assertEqual(
            japanese_tsundere_nekomimi["provenance"]["preset_id"],
            "maid_cafe_cosplay_portrait",
        )
        self.assertEqual(
            japanese_tsundere_nekomimi["slots"]["subject"]["selected"],
            "slot:subject:maid_cafe_performer",
        )
        self.assertEqual(
            japanese_tsundere_nekomimi["moe_response"]["primary_mechanism"],
            "denial_care_leak",
        )
        self.assertEqual(
            japanese_tsundere_nekomimi["moe_response"]["support_mechanisms"],
            ["nonhuman_reflex_leak"],
        )
        self.assertEqual(japanese_tsundere_nekomimi["species_family"]["family"], "feline")

        english_mamang_nekomimi = self.run_wrapper(
            "--concept",
            "a pretty and cute adult cat-eared maid with a benevolent motherly moe presence",
            "--selection-mode",
            "rule",
            "--emit-candidate-pack",
            "--seed",
            "20260818",
        )[0]
        self.assertEqual(
            english_mamang_nekomimi["moe_response"]["primary_mechanism"],
            "quiet_care_trace",
        )
        self.assertEqual(
            english_mamang_nekomimi["moe_response"]["relationship_register"],
            "nurturant_benevolence",
        )
        self.assertEqual(
            english_mamang_nekomimi["moe_response"]["support_mechanisms"],
            ["nonhuman_reflex_leak"],
        )

        adult = pack["hybrid_augmentation"]["adult_appeal"]
        self.assertFalse(adult["enabled"])
        self.assertEqual(adult["activation_source"], "explicit_nonsexual_moe")
        self.assertEqual(
            adult["eligibility"]["reason"],
            "explicit_nonsexual_moe_request_suppresses_configured_default",
        )
        self.assertEqual(adult["axes"]["sensual_editorial"]["intensity"], 0)
        self.assertEqual(adult["axes"]["fetish_fashion"]["intensity"], 0)
        mandatory = {row["text"] for row in pack["mandatory_intents"]}
        self.assertTrue({"성인", "네코미미", "츤데레", "메이드"} <= mandatory)
        self.assertFalse({"고양이", "수인"} & mandatory)
        self.assertEqual(
            set(pack["species_family"]["allowed"]),
            {"species_marker", "anatomical_connection"},
        )
        self.assertNotIn("texture", pack["species_family"]["allowed"])
        self.assertFalse({"야하지", "않은", "모에한"} & mandatory)

        generic = self.run_wrapper(
            "--concept",
            "성인 네코미미 바리스타의 모에한 순간",
            "--selection-mode",
            "rule",
            "--emit-candidate-pack",
            "--seed",
            "20260814",
        )[0]
        self.assertEqual(generic["moe_response"]["sexual_tone"], "sensual_optional")
        self.assertTrue(generic["moe_response"]["defaulted_sensual_optional"])
        generic_adult = generic["hybrid_augmentation"]["adult_appeal"]
        self.assertTrue(generic_adult["enabled"])
        self.assertEqual(generic_adult["activation_source"], "skill_default")
        self.assertEqual(generic_adult["axes"]["sensual_editorial"]["intensity"], 1)
        self.assertEqual(generic_adult["axes"]["fetish_fashion"]["intensity"], 0)

        text_pack = self.run_wrapper(
            "--concept",
            "a pretty and cute adult moe barista beside a readable cafe sign",
            "--selection-mode",
            "rule",
            "--emit-candidate-pack",
            "--seed",
            "20260816",
            "--candidate-pack-version",
            "v3",
        )[0]
        self.assertTrue(text_pack["moe_response"]["explicit_text_requested"])
        self.assertNotIn(
            "background_control_phrase",
            text_pack["moe_response"]["prompt_binding"]["required_evidence_fields"],
        )
        self.assertIn(
            "requested_text_boundary",
            text_pack["moe_response"]["composition_guidance"]["render_legibility"],
        )
        self.assertNotIn("readable background text", text_pack["negative_en"])
        self.assertNotIn("signage behind the subject", text_pack["negative_en"])

    def test_identity_controlled_moe_pack_holds_reference_face_constant_and_fails_closed(self):
        pack = self.run_wrapper(
            "--concept",
            "모에한 성인 네코미미 츤데레 메이드",
            "--selection-mode",
            "rule",
            "--reference-edit-mode",
            "identity",
            "--emit-candidate-pack",
            "--seed",
            "20260812",
        )[0]
        self.assertEqual(pack["provenance"]["reference_edit_mode"], "identity")
        response_contract = pack["moe_response"]
        self.assertEqual(response_contract["contract_version"], "moe_response_contract/v10")
        self.assertEqual(
            response_contract["relationship_register"], "peer_liking_under_denial"
        )
        self.assertEqual(response_contract["sexual_tone"], "sensual_optional")
        self.assertIn(
            "reference_identity_phrase",
            response_contract["prompt_binding"]["required_evidence_fields"],
        )
        identity = response_contract["reference_identity_control"]
        self.assertTrue(identity["enabled"])
        self.assertEqual(identity["mode"], "identity")
        self.assertTrue(
            {
                "facial_geometry",
                "eye_aperture",
                "eye_shape_and_spacing",
                "face_length",
                "lower_face_and_jaw_width",
                "adult_age",
            }
            <= set(identity["preserve"])
        )
        self.assertTrue(
            {
                "face_substitution",
                "facial_geometry_beautification",
                "eye_enlargement_or_rounding",
                "face_shortening",
                "jaw_narrowing",
                "de_aging",
            }
            <= set(identity["forbidden"])
        )
        self.assertEqual(
            identity["render_qualification"]["failure_action"],
            "preserve_as_failed_evidence_do_not_promote_or_claim_moe_improvement",
        )
        render_qualification = response_contract["render_qualification"]
        self.assertEqual(
            render_qualification["review_schema_version"],
            "moe-render-review/v1",
        )
        self.assertEqual(
            render_qualification["user_judgment_fields"],
            [
                "baseline_available",
                "genuinely_moe",
                "better_than_baseline",
                "source",
                "evidence",
            ],
        )
        self.assertTrue(
            {
                "three_quarter_head_away",
                "visible_partial_recipient_face_landmark",
                "head_turn_opposes_recipient_anchor",
                "nose_axis_off_lens",
                "small_oblique_iris_return_to_recipient",
                "softened_lower_lids",
                "suppressed_starting_mouth_corner_lift",
                "no_direct_frontal_eye_contact",
            }
            <= set(render_qualification["mechanism_hard_gates"])
        )
        self.assertEqual(
            set(render_qualification["identity_hard_gates"]),
            set(identity["render_qualification"]["hard_gates"]),
        )
        for term in (
            "enlarged or rounder eyes than the identity reference",
            "shortened face compared with the identity reference",
            "narrowed jaw compared with the identity reference",
            "dollified facial proportions",
            "de-aged identity",
        ):
            self.assertIn(term, pack["negative_en"])
        self.assertNotIn("duplicate faces", pack["negative_en"])
        self.assertIn("duplicate primary subject", pack["negative_en"])
        self.assertIn("second full recipient face", pack["negative_en"])
        adult = pack["hybrid_augmentation"]["adult_appeal"]
        self.assertTrue(adult["enabled"])
        self.assertEqual(adult["axes"]["sensual_editorial"]["intensity"], 1)
        self.assertEqual(adult["axes"]["fetish_fashion"]["intensity"], 0)

        prompt = (
            "Adult woman, pretty and cute: refined face, lively eyes, glossy hair. Preserve uploaded portrait: eye "
            "aperture/shape/spacing; nose, lips; face length, lower-face/jaw width; hairline, adult age. No enlarging, "
            "rounding, shortening, narrowing. Customer's bandaged hand fills lower foreground; same adult customer's blurred "
            "partial outer eye and temple sliver stay upper-left at frame edge. Cheek puffed, lips pursed mid-protest. "
            "Three-quarter head turns right; nose points right; only the irises return slightly upper-left. Private liking barely shows: lower "
            "lids soften; one mouth corner starts to lift, then flattens. Mid-bandaging, she holds scraped knuckle; one "
            "wing open. Human-ear-scale near ear turns toward hand; far ear keeps different angle. Pad covers scrape; "
            "wing unfastened. Face, hands, bandage share one focal plane. Unlettered bokeh."
        )
        phrases = {
            "actor_phrase": "Adult woman",
            "aesthetic_baseline_phrase": "Adult woman, pretty and cute: refined face, lively eyes, glossy hair",
            "active_denial_phrase": "Cheek puffed, lips pursed mid-protest",
            "care_action_anchor_phrase": "Customer's bandaged hand fills lower foreground",
            "relationship_gaze_anchor_phrase": "same adult customer's blurred partial outer eye and temple sliver stay upper-left at frame edge",
            "concealed_affection_phrase": "Three-quarter head turns right; nose points right; only the irises return slightly upper-left. Private liking barely shows: lower lids soften; one mouth corner starts to lift, then flattens",
            "affective_leak_phrase": "Private liking barely shows: lower lids soften; one mouth corner starts to lift, then flattens",
            "background_control_phrase": "Unlettered bokeh",
            "baseline_phrase": "Cheek puffed",
            "event_phase_phrase": "Mid-bandaging",
            "trigger_phrase": "Bandaged hand",
            "target_phrase": "one wing open",
            "visible_response_phrase": "Human-ear-scale near ear turns toward hand; far ear keeps different angle",
            "immediate_consequence_phrase": "Pad covers scrape; wing unfastened",
            "continuity_phrase": "Face, hands, bandage",
            "focal_plane_phrase": "Face, hands, bandage share one focal plane",
            "reference_identity_phrase": "Preserve uploaded portrait: eye aperture/shape/spacing; nose, lips; face length, lower-face/jaw width; hairline, adult age. No enlarging, rounding, shortening, narrowing",
        }
        self.assertEqual(audit_composed_prompt.english_prompt_word_count(prompt), 120)
        response = {
            "aesthetic_baseline": "adult_bishoujo",
            "mechanism": "denial_care_leak",
            "relationship_register": "peer_liking_under_denial",
            "baseline": "brisk guarded service",
            "event_phase": "mid-bandaging before the wing fastens",
            "trigger": "the bandaged hand reaches",
            "target": "the open bandage wing",
            "visible_response": "huffed mouth and asymmetric ear turn",
            "immediate_consequence": "the pad covers the scrape while one wing remains open",
            "continuity": "the same adult nekomimi maid",
            "support_mechanisms": ["nonhuman_reflex_leak"],
            "prompt_evidence": phrases,
        }
        self.assertEqual(
            audit_composed_prompt.audit_moe_response(
                {"moe_response": response_contract},
                {"moe_response": response},
                prompt,
            ),
            [],
        )
        missing_identity = copy.deepcopy(response)
        missing_identity["prompt_evidence"].pop("reference_identity_phrase")
        self.assertIn(
            "moe_response_binding",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    {"moe_response": response_contract},
                    {"moe_response": missing_identity},
                    prompt,
                )
            },
        )
        weak_identity = copy.deepcopy(response)
        weak_phrase = "Use the uploaded portrait and make her prettier"
        weak_identity["prompt_evidence"]["reference_identity_phrase"] = weak_phrase
        weak_prompt = prompt.replace(phrases["reference_identity_phrase"], weak_phrase)
        self.assertIn(
            "moe_response_reference_identity",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    {"moe_response": response_contract},
                    {"moe_response": weak_identity},
                    weak_prompt,
                )
            },
        )

        partial_identity = copy.deepcopy(response)
        partial_identity_phrase = (
            "Preserve uploaded portrait identity: eyes, nose, lips, jaw, skin, hairline, adult age; no de-aging"
        )
        partial_identity["prompt_evidence"]["reference_identity_phrase"] = (
            partial_identity_phrase
        )
        partial_identity_prompt = prompt.replace(
            phrases["reference_identity_phrase"], partial_identity_phrase
        )
        self.assertIn(
            "moe_response_reference_identity",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    {"moe_response": response_contract},
                    {"moe_response": partial_identity},
                    partial_identity_prompt,
                )
            },
        )

    def test_mamang_benevolent_affect_requires_concrete_expression_without_tsundere_leak(self):
        contract = prompt_generator.candidate_pack_moe_response(
            {
                "provenance": {
                    "character_response": {
                        "requested": True,
                        "eligible": True,
                        "activation_source": "explicit_natural_language_moe_request",
                        "response_goal": "character_specific_moe",
                        "route_id": "character_quiet_care_daily_scene",
                        "primary_mechanism": "quiet_care_trace",
                        "relationship_register": "nurturant_benevolence",
                        "support_mechanisms": [],
                        "aesthetic_baseline": "adult_bishoujo",
                        "aesthetic_presentation_source": "default_bishoujo",
                        "sexual_tone": "sensual_optional",
                    }
                }
            }
        )
        self.assertIsNotNone(contract)
        self.assertIn(
            "benevolent_affect_phrase",
            contract["prompt_binding"]["required_evidence_fields"],
        )
        prompt = (
            "Adult woman, pretty and cute, with a refined face, lively eyes, glossy hair. "
            "Her relaxed brow, patient soft eyes, reassuring mouth, and calm protective attention stay on her "
            "adult housemate. Caught mid-care, she draws a blanket over tired shoulders while one corner remains "
            "below the shoulder. Her soft eyes and reassuring mouth show warm concern. The housemate's visible "
            "shoulder triggers the adjustment; the blanket edge is still rising. Her adult face, hands, housemate, "
            "and blanket share one focal plane. Plain unlettered living-room bokeh."
        )
        phrases = {
            "actor_phrase": "Adult woman",
            "aesthetic_baseline_phrase": (
                "Adult woman, pretty and cute, with a refined face, lively eyes, glossy hair"
            ),
            "benevolent_affect_phrase": (
                "Her relaxed brow, patient soft eyes, reassuring mouth, and calm protective attention stay on her adult housemate"
            ),
            "affective_leak_phrase": "Her soft eyes and reassuring mouth show warm concern",
            "background_control_phrase": "Plain unlettered living-room bokeh",
            "baseline_phrase": "calm protective attention",
            "event_phase_phrase": "Caught mid-care",
            "trigger_phrase": "The housemate's visible shoulder",
            "target_phrase": "one corner remains below the shoulder",
            "visible_response_phrase": "she draws a blanket over tired shoulders",
            "immediate_consequence_phrase": "the blanket edge is still rising",
            "continuity_phrase": "Her adult face, hands, housemate, and blanket",
            "focal_plane_phrase": "Her adult face, hands, housemate, and blanket share one focal plane",
        }
        response = {
            "aesthetic_baseline": "adult_bishoujo",
            "mechanism": "quiet_care_trace",
            "relationship_register": "nurturant_benevolence",
            "baseline": "calm mature attention",
            "event_phase": "mid-care before the blanket settles",
            "trigger": "the housemate's tired shoulders",
            "target": "the rising blanket edge",
            "visible_response": "soft eyes and a reassuring mouth while both hands adjust the blanket",
            "immediate_consequence": "one corner remains below the shoulder",
            "continuity": "the adult woman and housemate stay in one domestic scene",
            "support_mechanisms": [],
            "prompt_evidence": phrases,
        }
        self.assertEqual(
            audit_composed_prompt.audit_moe_response(
                {"moe_response": contract},
                {"moe_response": response},
                prompt,
            ),
            [],
        )

        generic_kindness = copy.deepcopy(response)
        generic_kindness_phrase = "She looks kind while helping her adult housemate"
        generic_kindness["prompt_evidence"]["benevolent_affect_phrase"] = (
            generic_kindness_phrase
        )
        generic_kindness_prompt = prompt.replace(
            phrases["benevolent_affect_phrase"],
            generic_kindness_phrase,
        )
        self.assertIn(
            "moe_response_benevolent_affect",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    {"moe_response": contract},
                    {"moe_response": generic_kindness},
                    generic_kindness_prompt,
                )
            },
        )

        tsundere_leak = copy.deepcopy(response)
        tsundere_leak_phrase = (
            "Her relaxed brow, patient soft eyes, reassuring mouth, and calm protective attention hold as "
            "her irises return with private liking"
        )
        tsundere_leak["prompt_evidence"]["benevolent_affect_phrase"] = tsundere_leak_phrase
        tsundere_leak_prompt = prompt.replace(
            phrases["benevolent_affect_phrase"],
            tsundere_leak_phrase,
        )
        self.assertIn(
            "moe_response_benevolent_affect",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    {"moe_response": contract},
                    {"moe_response": tsundere_leak},
                    tsundere_leak_prompt,
                )
            },
        )

    def test_generic_moe_aesthetic_route_constrains_preset_before_subject_sampling(self):
        male = self.run_wrapper(
            "--concept",
            "야하지 않은 성인 남자 캐릭터를 미소년 계열로 모에하게",
            "--selection-mode",
            "rule",
            "--emit-candidate-pack",
            "--seed",
            "20260816",
            "--candidate-pack-version",
            "v3",
        )[0]
        self.assertEqual(male["moe_response"]["aesthetic_baseline"], "adult_bishonen")
        self.assertEqual(male["provenance"]["preset_id"], "character_attribute_composition_scene")
        self.assertTrue(
            male["render_contract"]["selected_scene"]["blueprint_id"].startswith(
                "moe_attribute_composition_graph_"
            )
        )
        male_scene = " ".join(
            male["render_contract"]["selected_scene"]["atomic_scene"][slot]["label_en"]
            for slot in ("subject", "action", "location", "prop")
        ).lower()
        for leakage in ("repair", "maintenance", "coworker", "shift", "tool strap"):
            self.assertNotIn(leakage, male_scene)
        self.assertEqual(
            male["slots"]["subject"]["selected"],
            "slot:subject:character_attribute_composition_scene_subject",
        )
        self.assertNotIn(
            "elderly_commuter",
            {candidate["entry_id"] for candidate in male["slots"]["subject"]["candidates"]},
        )

        generic = self.run_wrapper(
            "--concept",
            "야하지 않으면서도 모에한 성인 캐릭터의 사진",
            "--selection-mode",
            "rule",
            "--emit-candidate-pack",
            "--seed",
            "20260817",
            "--candidate-pack-version",
            "v3",
        )[0]
        self.assertEqual(generic["moe_response"]["aesthetic_baseline"], "adult_bishoujo")
        self.assertEqual(generic["provenance"]["preset_id"], "character_attribute_composition_scene")
        generic_scene = " ".join(
            generic["render_contract"]["selected_scene"]["atomic_scene"][slot]["label_en"]
            for slot in ("subject", "action", "location", "prop")
        ).lower()
        for leakage in ("repair", "maintenance", "coworker", "shift", "tool strap"):
            self.assertNotIn(leakage, generic_scene)

        direct = self.run_wrapper(
            "--preset",
            "character_attribute_composition_scene",
            "--selection-mode",
            "rule",
            "--emit-candidate-pack",
            "--seed",
            "20260816",
            "--candidate-pack-version",
            "v3",
        )[0]
        self.assertEqual(
            direct["render_contract"]["selected_scene"]["blueprint_id"],
            "moe_attribute_composition_graph_atomic_01",
        )
        direct_scene = " ".join(
            direct["render_contract"]["selected_scene"]["atomic_scene"][slot]["label_en"]
            for slot in ("subject", "action", "location", "prop")
        ).lower()
        self.assertIn("repair", direct_scene)

        ordinary = self.run_wrapper(
            "--preset",
            "commute_transit_candid",
            "--selection-mode",
            "rule",
            "--emit-candidate-pack",
            "--seed",
            "20260816",
            "--candidate-pack-version",
            "v3",
        )[0]
        self.assertEqual(ordinary["provenance"]["preset_id"], "commute_transit_candid")
        self.assertNotIn("moe_response", ordinary)

    def test_frozen_natural_moe_render_cases_preserve_identity_and_response_contract(self):
        cases = [
            json.loads(line)
            for line in NATURAL_MOE_RENDER_REVIEW_V1_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(cases), 4)
        self.assertEqual(len({case["id"] for case in cases}), 4)
        for case in cases:
            args = [
                "--concept",
                case["request"],
                "--selection-mode",
                case["cli"]["selection_mode"],
                "--candidate-pack-version",
                case["cli"]["candidate_pack_version"],
                "--emit-candidate-pack",
                "--seed",
                str(case["seed"]),
            ]
            if case["cli"].get("preset"):
                args.extend(["--preset", case["cli"]["preset"]])
            pack = self.run_wrapper(*args)[0]
            expected = case["expected"]
            self.assertEqual(pack["provenance"]["preset_id"], expected["preset_id"], case["id"])
            self.assertEqual(pack["provenance"]["likeness_mode"], expected["likeness_mode"], case["id"])
            self.assertEqual(pack["provenance"]["likeness_references"], [], case["id"])
            self.assertEqual(
                pack["moe_response"]["primary_mechanism"],
                expected["primary_mechanism"],
                case["id"],
            )
            self.assertEqual(
                pack["moe_response"]["support_mechanisms"],
                expected["support_mechanisms"],
                case["id"],
            )
            self.assertEqual(pack["moe_response"]["sexual_tone"], expected["sexual_tone"], case["id"])
            self.assertEqual(
                pack["moe_response"]["aesthetic_baseline"],
                expected["aesthetic_baseline"],
                case["id"],
            )
            if expected.get("role"):
                self.assertIn(expected["role"], " ".join(pack["provenance"]["concept_lock"]), case["id"])
            if expected.get("species_family"):
                self.assertEqual(pack["species_family"]["family"], expected["species_family"], case["id"])
                self.assertTrue(pack["species_family"]["enforce"], case["id"])
                for slot, allowed_ids in pack["species_family"]["allowed"].items():
                    exposed_ids = {
                        candidate["entry_id"] for candidate in pack["slots"][slot]["candidates"]
                    }
                    self.assertTrue(set(allowed_ids) <= exposed_ids, (case["id"], slot, exposed_ids))
            if expected.get("blueprint_id"):
                self.assertEqual(
                    pack["render_contract"]["selected_scene"]["blueprint_id"],
                    expected["blueprint_id"],
                    case["id"],
                )

    def test_moe_response_audit_requires_causal_visible_evidence_and_rejects_shortcuts(self):
        contract = prompt_generator.candidate_pack_moe_response(
            {
                "provenance": {
                    "character_response": {
                        "requested": True,
                        "eligible": True,
                        "activation_source": "explicit_natural_language_moe_request",
                        "response_goal": "character_specific_moe",
                        "route_id": "character_gap_contrast_scene",
                        "primary_mechanism": "denial_care_leak",
                        "relationship_register": "peer_liking_under_denial",
                        "support_mechanisms": ["nonhuman_reflex_leak"],
                        "aesthetic_baseline": "adult_bishoujo",
                        "aesthetic_presentation_source": "default_bishoujo",
                        "sexual_tone": "nonsexual",
                    }
                }
            }
        )
        self.assertIsNotNone(contract)
        pack = {"moe_response": contract}
        prompt = (
            "An adult cat-eared maid is a pretty and cute woman: refined face, lively eyes, expressive lips, glossy "
            "hair. Customer's hand fills lower foreground; same adult customer's blurred partial outer eye and temple sliver "
            "stay upper-left at frame edge. Cheek puffed, lips pursed mid-protest. Three-quarter head turns right; nose points right; only "
            "irises make a small oblique return upper-left toward that outer eye. Private liking barely shows: "
            "lower lids soften; one mouth corner starts to lift, then flattens. Mid-handoff, she slides a pastry partway "
            "across an open gap. Compact near ear, no taller than her human ear, turns toward hand; other ear keeps a "
            "different angle. Pastry halfway. Adult face, hands, apron, ears, pastry share one focal plane. Plain "
            "unlettered bokeh."
        )
        phrases = {
            "actor_phrase": "An adult cat-eared maid",
            "aesthetic_baseline_phrase": "An adult cat-eared maid is a pretty and cute woman: refined face, lively eyes, expressive lips, glossy hair",
            "active_denial_phrase": "Cheek puffed, lips pursed mid-protest",
            "care_action_anchor_phrase": "Customer's hand fills lower foreground",
            "relationship_gaze_anchor_phrase": "same adult customer's blurred partial outer eye and temple sliver stay upper-left at frame edge",
            "concealed_affection_phrase": "Three-quarter head turns right; nose points right; only irises make a small oblique return upper-left toward that outer eye. Private liking barely shows: lower lids soften; one mouth corner starts to lift, then flattens",
            "affective_leak_phrase": "Private liking barely shows: lower lids soften; one mouth corner starts to lift, then flattens",
            "background_control_phrase": "Plain unlettered bokeh",
            "baseline_phrase": "Cheek puffed",
            "event_phase_phrase": "Mid-handoff",
            "trigger_phrase": "Customer's hand",
            "target_phrase": "a pastry partway across an open gap",
            "visible_response_phrase": "Compact near ear, no taller than her human ear, turns toward hand; other ear keeps a different angle",
            "immediate_consequence_phrase": "Pastry halfway",
            "continuity_phrase": "Adult face, hands, apron, ears, pastry",
            "focal_plane_phrase": "Adult face, hands, apron, ears, pastry share one focal plane",
        }
        self.assertEqual(audit_composed_prompt.english_prompt_word_count(prompt), 120)
        response = {
            "aesthetic_baseline": "adult_bishoujo",
            "mechanism": "denial_care_leak",
            "relationship_register": "peer_liking_under_denial",
            "baseline": "a brisk and guarded service front",
            "event_phase": "mid-handoff before the helpful action is complete",
            "trigger": "the customer reaches for the plain dessert",
            "target": "the extra wrapped pastry",
            "visible_response": "a huffed mouth, one trigger-side ear turned toward the customer, and tightening tray fingers",
            "immediate_consequence": "the extra pastry remains partway across the counter",
            "continuity": "adult feline maid identity stays readable",
            "support_mechanisms": ["nonhuman_reflex_leak"],
            "prompt_evidence": phrases,
        }
        self.assertEqual(
            audit_composed_prompt.audit_moe_response(pack, {"moe_response": response}, prompt),
            [],
        )

        missing = copy.deepcopy(response)
        missing["prompt_evidence"].pop("immediate_consequence_phrase")
        self.assertIn(
            "moe_response_binding",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    pack, {"moe_response": missing}, prompt
                )
            },
        )
        shortcut = copy.deepcopy(response)
        shortcut["prompt_evidence"]["visible_response_phrase"] = "cute blush"
        shortcut_prompt = prompt + " Cute blush."
        shortcut_checks = {
            row["check"]
            for row in audit_composed_prompt.audit_moe_response(
                pack, {"moe_response": shortcut}, shortcut_prompt
            )
        }
        self.assertIn("moe_response_visible_response", shortcut_checks)
        self.assertIn("moe_response_shortcut", shortcut_checks)

        passive_denial = copy.deepcopy(response)
        passive_denial_phrase = "Her guarded averted gaze"
        passive_denial["prompt_evidence"]["active_denial_phrase"] = passive_denial_phrase
        passive_denial_prompt = prompt.replace("Her tiny huff", passive_denial_phrase)
        self.assertIn(
            "moe_response_active_denial",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    pack,
                    {"moe_response": passive_denial},
                    passive_denial_prompt,
                )
            },
        )

        task_warmth = copy.deepcopy(response)
        task_warmth_phrase = "Her head stays aside; irises return toward the pastry with gentle maternal warmth and softened lower lids"
        task_warmth["prompt_evidence"]["concealed_affection_phrase"] = task_warmth_phrase
        task_warmth_prompt = prompt.replace(
            phrases["concealed_affection_phrase"],
            task_warmth_phrase,
        )
        self.assertIn(
            "moe_response_concealed_affection",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    pack,
                    {"moe_response": task_warmth},
                    task_warmth_prompt,
                )
            },
        )

        off_frame_recipient = copy.deepcopy(response)
        off_frame_anchor_phrase = "The customer's visible hand stays off-frame at lower left"
        off_frame_recipient["prompt_evidence"]["care_action_anchor_phrase"] = (
            off_frame_anchor_phrase
        )
        off_frame_recipient_prompt = prompt.replace(
            phrases["care_action_anchor_phrase"],
            off_frame_anchor_phrase,
        )
        self.assertIn(
            "moe_response_care_action_anchor",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    pack,
                    {"moe_response": off_frame_recipient},
                    off_frame_recipient_prompt,
                )
            },
        )

        collapsed_relationship = copy.deepcopy(response)
        collapsed_phrase = "The same adult customer's hand stays visible in the lower foreground"
        collapsed_relationship["prompt_evidence"]["relationship_gaze_anchor_phrase"] = (
            collapsed_phrase
        )
        collapsed_prompt = prompt.replace(
            phrases["relationship_gaze_anchor_phrase"],
            collapsed_phrase,
        )
        self.assertIn(
            "moe_response_relationship_gaze_anchor",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    pack,
                    {"moe_response": collapsed_relationship},
                    collapsed_prompt,
                )
            },
        )

        imagined_eye_line = copy.deepcopy(response)
        imagined_anchor_phrase = (
            "same adult customer's off-axis face-level eye line stays upper-left"
        )
        imagined_eye_line["prompt_evidence"]["relationship_gaze_anchor_phrase"] = (
            imagined_anchor_phrase
        )
        imagined_prompt = prompt.replace(
            phrases["relationship_gaze_anchor_phrase"],
            imagined_anchor_phrase,
        )
        self.assertIn(
            "moe_response_partial_recipient_landmark",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    pack,
                    {"moe_response": imagined_eye_line},
                    imagined_prompt,
                )
            },
        )

        same_side_turn = copy.deepcopy(response)
        same_side_phrase = (
            "Three-quarter head turns left; nose points left; only irises make a small oblique return upper-left "
            "toward that outer eye. Private liking barely shows: lower lids soften; one mouth corner starts to lift, "
            "then flattens"
        )
        same_side_turn["prompt_evidence"]["concealed_affection_phrase"] = (
            same_side_phrase
        )
        same_side_prompt = prompt.replace(
            phrases["concealed_affection_phrase"],
            same_side_phrase,
        )
        same_side_checks = {
            row["check"]
            for row in audit_composed_prompt.audit_moe_response(
                pack,
                {"moe_response": same_side_turn},
                same_side_prompt,
            )
        }
        self.assertIn("moe_response_opposed_head_iris_vector", same_side_checks)
        self.assertIn("moe_response_concealed_affection", same_side_checks)

        side_eye_only = copy.deepcopy(response)
        side_eye_phrase = (
            "A brief side-eye betrays private liking toward the customer before she suppresses an almost-smile"
        )
        side_eye_only["prompt_evidence"]["concealed_affection_phrase"] = side_eye_phrase
        side_eye_prompt = prompt.replace(
            phrases["concealed_affection_phrase"],
            side_eye_phrase,
        )
        self.assertIn(
            "moe_response_concealed_affection",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    pack,
                    {"moe_response": side_eye_only},
                    side_eye_prompt,
                )
            },
        )

        frontal_liking = copy.deepcopy(response)
        frontal_liking_phrase = (
            "Three-quarter head turns right; nose points right; only irises make a small oblique return upper-left "
            "toward that face-level eye line with direct frontal eye contact. Private liking barely shows: lower "
            "lids soften; one mouth corner starts to lift, then flattens"
        )
        frontal_liking["prompt_evidence"]["concealed_affection_phrase"] = (
            frontal_liking_phrase
        )
        frontal_liking_prompt = prompt.replace(
            phrases["concealed_affection_phrase"], frontal_liking_phrase
        )
        self.assertIn(
            "moe_response_concealed_affection",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    pack,
                    {"moe_response": frontal_liking},
                    frontal_liking_prompt,
                )
            },
        )

        no_mouth_leak = copy.deepcopy(response)
        no_mouth_leak_phrase = (
            "Three-quarter head turns right; nose points right; only irises make a small oblique return upper-left "
            "toward that face-level eye line. Private liking barely shows as lower lids soften, then she suppresses it"
        )
        no_mouth_leak["prompt_evidence"]["concealed_affection_phrase"] = (
            no_mouth_leak_phrase
        )
        no_mouth_leak_prompt = prompt.replace(
            phrases["concealed_affection_phrase"], no_mouth_leak_phrase
        )
        self.assertIn(
            "moe_response_concealed_affection",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    pack,
                    {"moe_response": no_mouth_leak},
                    no_mouth_leak_prompt,
                )
            },
        )

        no_lower_lid_leak = copy.deepcopy(response)
        no_lower_lid_leak_phrase = (
            "Three-quarter head turns right; nose points right; only irises make a small oblique return upper-left "
            "toward that face-level eye line. Private liking barely shows as one mouth corner starts to lift, then flattens"
        )
        no_lower_lid_leak["prompt_evidence"]["concealed_affection_phrase"] = (
            no_lower_lid_leak_phrase
        )
        no_lower_lid_leak_prompt = prompt.replace(
            phrases["concealed_affection_phrase"], no_lower_lid_leak_phrase
        )
        self.assertIn(
            "moe_response_concealed_affection",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    pack,
                    {"moe_response": no_lower_lid_leak},
                    no_lower_lid_leak_prompt,
                )
            },
        )

        cold_only = copy.deepcopy(response)
        cold_only["prompt_evidence"]["affective_leak_phrase"] = (
            "Her annoyed frown, averted gaze, skeptical pout, and cold stare dominate her face"
        )
        cold_prompt = prompt.replace(
            phrases["affective_leak_phrase"],
            cold_only["prompt_evidence"]["affective_leak_phrase"],
        )
        self.assertIn(
            "moe_response_affective_balance",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    pack, {"moe_response": cold_only}, cold_prompt
                )
            },
        )

        split_cold = copy.deepcopy(response)
        split_cold["prompt_evidence"]["baseline_phrase"] = (
            "She maintains an annoyed, skeptical, and listless service front"
        )
        split_cold_prompt = prompt.replace(
            phrases["baseline_phrase"],
            split_cold["prompt_evidence"]["baseline_phrase"],
        )
        self.assertIn(
            "moe_response_affective_balance",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    pack, {"moe_response": split_cold}, split_cold_prompt
                )
            },
        )

        lettered_background = copy.deepcopy(response)
        lettered_background["prompt_evidence"]["background_control_phrase"] = (
            "A chalkboard menu with decorative lettering fills the cafe background"
        )
        lettered_prompt = prompt.replace(
            phrases["background_control_phrase"],
            lettered_background["prompt_evidence"]["background_control_phrase"],
        )
        self.assertIn(
            "moe_response_background_control",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    pack, {"moe_response": lettered_background}, lettered_prompt
                )
            },
        )

        sexualized_checks = {
            row["check"]
            for row in audit_composed_prompt.audit_moe_response(
                pack,
                {"moe_response": response},
                prompt + " A sultry gaze and cleavage-emphasis pose.",
            )
        }
        self.assertIn("moe_response_nonsexual_tone", sexualized_checks)

        generic_casting = copy.deepcopy(response)
        generic_casting["prompt_evidence"]["aesthetic_baseline_phrase"] = (
            "An adult woman stands behind the counter"
        )
        generic_casting_prompt = prompt.replace(
            phrases["aesthetic_baseline_phrase"],
            generic_casting["prompt_evidence"]["aesthetic_baseline_phrase"],
        )
        self.assertIn(
            "moe_response_aesthetic_evidence",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    pack,
                    {"moe_response": generic_casting},
                    generic_casting_prompt,
                )
            },
        )

        wrong_presentation = copy.deepcopy(response)
        wrong_presentation["aesthetic_baseline"] = "adult_bishonen"
        self.assertIn(
            "moe_response_aesthetic_baseline",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    pack,
                    {"moe_response": wrong_presentation},
                    prompt,
                )
            },
        )

        undirected_reflex = copy.deepcopy(response)
        undirected_reflex["prompt_evidence"]["visible_response_phrase"] = (
            "her pursed mouth holds a tiny huff while both ears stand symmetrically upright and her fingers tighten on the tray"
        )
        undirected_prompt = prompt.replace(
            phrases["visible_response_phrase"],
            undirected_reflex["prompt_evidence"]["visible_response_phrase"],
        )
        self.assertIn(
            "moe_response_reflex_direction",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    pack,
                    {"moe_response": undirected_reflex},
                    undirected_prompt,
                )
            },
        )

        oversized_reflex = copy.deepcopy(response)
        oversized_reflex["prompt_evidence"]["visible_response_phrase"] = (
            "her pursed mouth holds a tiny huff while one enormous trigger-side ear turns toward the customer, the other ear keeps its baseline angle, and her fingers tighten on the tray"
        )
        oversized_prompt = prompt.replace(
            phrases["visible_response_phrase"],
            oversized_reflex["prompt_evidence"]["visible_response_phrase"],
        )
        self.assertIn(
            "moe_response_nekomimi_scale_direction",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    pack, {"moe_response": oversized_reflex}, oversized_prompt
                )
            },
        )

        no_state_geometry = copy.deepcopy(response)
        no_state_geometry["prompt_evidence"]["event_phase_phrase"] = (
            "caught during the handoff before her tray hand settles"
        )
        no_state_geometry["prompt_evidence"]["immediate_consequence_phrase"] = (
            "she slides the extra wrapped pastry across the counter anyway"
        )
        no_state_geometry["prompt_evidence"]["target_phrase"] = "the extra pastry"
        no_geometry_prompt = prompt.replace(
            phrases["event_phase_phrase"],
            no_state_geometry["prompt_evidence"]["event_phase_phrase"],
        ).replace(
            phrases["target_phrase"],
            no_state_geometry["prompt_evidence"]["target_phrase"],
        ).replace(
            phrases["immediate_consequence_phrase"],
            no_state_geometry["prompt_evidence"]["immediate_consequence_phrase"],
        )
        self.assertIn(
            "moe_response_state_geometry",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    pack,
                    {"moe_response": no_state_geometry},
                    no_geometry_prompt,
                )
            },
        )

        settled_endpoint = copy.deepcopy(response)
        settled_endpoint["prompt_evidence"]["event_phase_phrase"] = (
            "the completed handoff after her hands have settled"
        )
        settled_prompt = prompt.replace(
            phrases["event_phase_phrase"],
            settled_endpoint["prompt_evidence"]["event_phase_phrase"],
        )
        self.assertIn(
            "moe_response_event_phase",
            {
                row["check"]
                for row in audit_composed_prompt.audit_moe_response(
                    pack,
                    {"moe_response": settled_endpoint},
                    settled_prompt,
                )
            },
        )

        compact_prompt = prompt
        compact_response = response
        self.assertEqual(
            audit_composed_prompt.english_prompt_word_count(compact_prompt),
            120,
        )
        self.assertEqual(
            audit_composed_prompt.audit_moe_response(
                pack,
                {"moe_response": compact_response},
                compact_prompt,
            ),
            [],
        )

        over_budget_prompt = compact_prompt + " " + " ".join(["extra"] * 81)
        over_budget_checks = {
            row["check"]
            for row in audit_composed_prompt.audit_moe_response(
                pack,
                {"moe_response": compact_response},
                over_budget_prompt,
            )
        }
        self.assertIn("moe_response_prompt_budget", over_budget_checks)

    def test_moe_render_review_blocks_failed_pixels_and_keeps_user_as_terminal_judge(self):
        pack = self.run_wrapper(
            "--concept",
            "모에한 성인 네코미미 츤데레 메이드",
            "--selection-mode",
            "rule",
            "--reference-edit-mode",
            "identity",
            "--emit-candidate-pack",
            "--seed",
            "20260812",
        )[0]
        contract = pack["moe_response"]
        required_gates = contract["render_qualification"]["required_hard_gates"]
        passing_gates = {
            gate: {
                "status": "pass",
                "evidence": f"Native pixel review confirms {gate.replace('_', ' ')} in the result.",
            }
            for gate in required_gates
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            result_path = Path(temp_dir) / "render.png"
            result_path.write_bytes(b"fixed-render-bytes")
            result_sha256 = hashlib.sha256(result_path.read_bytes()).hexdigest()
            review = {
                "schema_version": "moe-render-review/v1",
                "pack_id": pack["pack_id"],
                "contract_version": contract["contract_version"],
                "reviewer": "agent_native_pixel_review",
                "result_image": str(result_path),
                "result_sha256": result_sha256,
                "hard_gates": passing_gates,
                "user_judgment": {
                    "baseline_available": True,
                    "genuinely_moe": "pending",
                    "better_than_baseline": "pending",
                    "source": "not_yet_received",
                    "evidence": "",
                },
            }
            pending = audit_moe_render_review.audit_moe_render_review(
                pack, review, review_path=Path(temp_dir) / "review.json"
            )
            self.assertTrue(pending["technical_qualified"])
            self.assertFalse(pending["representative_eligible"])
            self.assertEqual(
                pending["qualification_status"],
                "pending_requesting_user_judgment",
            )

            accepted_review = copy.deepcopy(review)
            accepted_review["user_judgment"]["genuinely_moe"] = "accepted"
            accepted_review["user_judgment"]["better_than_baseline"] = "accepted"
            accepted_review["user_judgment"]["source"] = "requesting_user"
            accepted_review["user_judgment"]["evidence"] = (
                "The user judged the result genuinely moe and better than the baseline."
            )
            accepted = audit_moe_render_review.audit_moe_render_review(
                pack, accepted_review, review_path=Path(temp_dir) / "review.json"
            )
            self.assertTrue(accepted["representative_eligible"])
            self.assertEqual(accepted["qualification_status"], "representative_eligible")

            forged_acceptance = copy.deepcopy(accepted_review)
            forged_acceptance["user_judgment"]["source"] = "not_yet_received"
            forged_acceptance["user_judgment"]["evidence"] = ""
            forged = audit_moe_render_review.audit_moe_render_review(
                pack, forged_acceptance, review_path=Path(temp_dir) / "review.json"
            )
            self.assertFalse(forged["technical_qualified"])
            self.assertFalse(forged["representative_eligible"])
            self.assertIn(
                "user_judgment.source",
                {row["check"] for row in forged["schema_failures"]},
            )

            failed_review = copy.deepcopy(accepted_review)
            failed_review["hard_gates"]["no_direct_frontal_eye_contact"] = {
                "status": "fail",
                "evidence": "The nose and both eyes face the lens in direct frontal contact.",
            }
            failed_review["hard_gates"]["same_person_identity"] = {
                "status": "fail",
                "evidence": "Larger rounder eyes and a narrowed jaw materially change the person.",
            }
            failed = audit_moe_render_review.audit_moe_render_review(
                pack, failed_review, review_path=Path(temp_dir) / "review.json"
            )
            self.assertFalse(failed["technical_qualified"])
            self.assertFalse(failed["representative_eligible"])
            self.assertEqual(failed["qualification_status"], "failed_technical_hard_gates")
            self.assertEqual(
                {row["gate"] for row in failed["failed_hard_gates"]},
                {"no_direct_frontal_eye_contact", "same_person_identity"},
            )

            partial_review = copy.deepcopy(review)
            partial_review["hard_gates"]["small_oblique_iris_return_to_recipient"][
                "status"
            ] = "partial"
            partial = audit_moe_render_review.audit_moe_render_review(
                pack, partial_review, review_path=Path(temp_dir) / "review.json"
            )
            self.assertFalse(partial["technical_qualified"])
            self.assertTrue(partial["schema_failures"])

    def test_render_request_audit_preserves_exact_negative_and_reference_bytes(self):
        pack = self.run_wrapper(
            "--concept",
            "모에한 성인 네코미미 츤데레 메이드",
            "--selection-mode",
            "rule",
            "--reference-edit-mode",
            "identity",
            "--emit-candidate-pack",
            "--seed",
            "20260812",
        )[0]
        composed = {
            "pack_id": pack["pack_id"],
            "prompt_en": "Adult woman preserves her identity while one tiny private-liking cue appears.",
            "negative_en": pack["negative_en"],
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            identity_path = temp_path / "identity.png"
            scene_path = temp_path / "scene.png"
            identity_path.write_bytes(b"identity-reference-bytes")
            scene_path.write_bytes(b"scene-reference-bytes")
            request_path = temp_path / "request.json"
            request = {
                "schema_version": "photo-image-render-request/v2",
                "pack_id": pack["pack_id"],
                "runtime_prompt_en": (
                    "Image 1 is the sole identity reference.\n\n"
                    + composed["prompt_en"]
                    + "\n\nAvoid: "
                    + pack["negative_en"]
                ),
                "runtime_negative_en": pack["negative_en"],
                "references": [
                    {
                        "path": identity_path.name,
                        "sha256": hashlib.sha256(identity_path.read_bytes()).hexdigest(),
                        "role": "sole_identity_and_adult_age_reference",
                    },
                    {
                        "path": scene_path.name,
                        "sha256": hashlib.sha256(scene_path.read_bytes()).hexdigest(),
                        "role": "scene_costume_pose_and_action_reference_only",
                    },
                ],
                "audit_boundary": {
                    "composed_prompt_audit_status": "pass",
                    "runtime_prompt_audit_status": "not_run",
                    "inherits_composed_prompt_pass": False,
                },
            }
            passed = audit_image_render_request.audit_image_render_request(
                pack, composed, request, request_path=request_path
            )
            self.assertEqual(passed["status"], "pass")
            self.assertTrue(passed["negative_matches_pack"])
            self.assertEqual(passed["failures"], [])

            changed_negative = copy.deepcopy(request)
            changed_negative["runtime_negative_en"] = "a shorter hand-written avoid list"
            changed = audit_image_render_request.audit_image_render_request(
                pack, composed, changed_negative, request_path=request_path
            )
            self.assertEqual(changed["status"], "fail")
            self.assertIn(
                "runtime_negative_en",
                {row["check"] for row in changed["failures"]},
            )

            unbound_negative = copy.deepcopy(request)
            unbound_negative["runtime_prompt_en"] = (
                "Image 1 is the sole identity reference.\n\n" + composed["prompt_en"]
            )
            unbound = audit_image_render_request.audit_image_render_request(
                pack, composed, unbound_negative, request_path=request_path
            )
            self.assertIn(
                "runtime_negative_binding",
                {row["check"] for row in unbound["failures"]},
            )

            missing_prompt = copy.deepcopy(request)
            missing_prompt["runtime_prompt_en"] = "A rewritten runtime prompt without the audited core."
            missing = audit_image_render_request.audit_image_render_request(
                pack, composed, missing_prompt, request_path=request_path
            )
            self.assertIn(
                "composed_prompt_binding",
                {row["check"] for row in missing["failures"]},
            )

            inherited = copy.deepcopy(request)
            inherited["audit_boundary"]["runtime_prompt_audit_status"] = "pass"
            inherited["audit_boundary"]["inherits_composed_prompt_pass"] = True
            inherited_result = audit_image_render_request.audit_image_render_request(
                pack, composed, inherited, request_path=request_path
            )
            self.assertTrue(
                {"runtime_prompt_audit_status", "audit_inheritance"}
                <= {row["check"] for row in inherited_result["failures"]}
            )

            wrong_hash = copy.deepcopy(request)
            wrong_hash["references"][0]["sha256"] = "0" * 64
            wrong_hash_result = audit_image_render_request.audit_image_render_request(
                pack, composed, wrong_hash, request_path=request_path
            )
            self.assertIn(
                "references[0].sha256",
                {row["check"] for row in wrong_hash_result["failures"]},
            )

            ambiguous_identity = copy.deepcopy(request)
            ambiguous_identity["references"][1]["role"] = (
                "sole_identity_and_adult_age_reference"
            )
            ambiguous = audit_image_render_request.audit_image_render_request(
                pack, composed, ambiguous_identity, request_path=request_path
            )
            self.assertIn(
                "identity_reference_role",
                {row["check"] for row in ambiguous["failures"]},
            )

    def test_manual_concept_gate_requires_literal_prompt_evidence_and_remains_pending_pixel_review(self):
        pack = {
            "contract_version": "photo-candidate-pack/v3",
            "pack_id": "",
            "negative_en": "",
            "safety": {
                "status": "pass",
                "requires_user_approval": False,
            },
            "concept_gates": [
                {
                    "id": "costume_swap_test",
                    "status": "manual",
                    "check": "two body-rooted cues must survive a costume swap",
                }
            ],
            "slots": {
                "composition": {
                    "candidates": [
                        {
                            "id": "slot:composition:medium_close",
                            "applicability": {"status": "eligible"},
                        }
                    ]
                }
            },
        }
        pack["pack_id"] = audit_composed_prompt.computed_pack_id(pack)
        composed = {
            "pack_id": pack["pack_id"],
            "prompt_en": "Organic ear roots and a skin-to-fur wrist boundary remain visible.",
            "negative_en": "",
            "chosen_candidate_ids": ["slot:composition:medium_close"],
            "composer": "agent",
        }
        missing = audit_composed_prompt.audit_composed_prompt(pack, composed)
        self.assertEqual(missing["status"], "fail")
        self.assertIn("concept_gates", {row["check"] for row in missing["failures"]})

        composed["manual_gate_evidence"] = {
            "costume_swap_test": {
                "review_stage": "pixel_review_required",
                "evidence_phrases": [
                    "Organic ear roots",
                    "skin-to-fur wrist boundary",
                ],
            }
        }
        passed = audit_composed_prompt.audit_composed_prompt(pack, composed)
        self.assertEqual(passed["status"], "pass")
        self.assertIn("manual_concept_gate", {row["check"] for row in passed["warnings"]})

    def test_character_moe_scene_corpus_rebalances_work_repair_and_relationship_shortcuts(self):
        payload = json.loads(SCENE_EXPRESSION_CHARACTER_MOE_PATH.read_text(encoding="utf-8"))
        extensions = payload["existing_preset_render_contract_extensions"]
        scenes = [
            scene
            for extension in extensions.values()
            for scene in extension["scene_blueprints"]
        ]
        self.assertGreaterEqual(len(scenes), 96)

        def scene_blob(scene: dict) -> str:
            return " ".join(
                str(scene.get(field) or "")
                for field in ("subject", "action", "location", "prop")
            ).lower()

        blobs = [scene_blob(scene) for scene in scenes]
        category_terms = {
            "workplace": (
                "coworker",
                "colleague",
                "technician",
                "repairer",
                "workroom",
                "workshop",
                "shift",
                "maintenance",
                "studio",
                "café",
                "cafe",
            ),
            "repair": ("repair", "mend", "patch", "fix", "adjust"),
            "coworker": ("coworker", "colleague", "work partner", "work crew"),
        }
        counts = {
            category: sum(any(term in blob for term in terms) for blob in blobs)
            for category, terms in category_terms.items()
        }
        for category, count in counts.items():
            self.assertLess(count, len(scenes) / 2, (category, count, len(scenes)))

        evidence_counts: dict[str, int] = {}
        for scene in scenes:
            for evidence_type in scene.get("character_evidence_types") or []:
                evidence_counts[str(evidence_type)] = evidence_counts.get(str(evidence_type), 0) + 1
        self.assertGreaterEqual(evidence_counts.get("solo_response", 0), 12)
        self.assertGreaterEqual(evidence_counts.get("expression_led", 0), 6)
        self.assertGreaterEqual(evidence_counts.get("pose_led", 0), 3)
        self.assertGreaterEqual(evidence_counts.get("private_joy", 0), 3)
        self.assertGreaterEqual(evidence_counts.get("earnest_effort", 0), 3)
        self.assertGreaterEqual(sum(scene.get("static_portrait") is True for scene in scenes), 4)

    def test_sensual_editorial_and_fetish_fashion_axes_combine_and_risky_camera_pair_fails(self):
        pack = self.run_wrapper(
            "--preset",
            "adult_fetish_fashion_editorial",
            "--selection-mode",
            "rule",
            "--seed",
            "20260809",
            "--emit-candidate-pack",
            "--hybrid-augmentation",
            "--sensual-editorial-intensity",
            "2",
            "--fetish-fashion-intensity",
            "2",
            "--adult-appeal-emphasis",
            "balanced",
        )[0]
        adult = pack["hybrid_augmentation"]["adult_appeal"]
        self.assertTrue(adult["enabled"])
        self.assertTrue(adult["blend"]["simultaneous_activation_allowed"])
        self.assertEqual(adult["axes"]["sensual_editorial"]["intensity"], 2)
        self.assertEqual(adult["axes"]["fetish_fashion"]["intensity"], 2)
        self.assertGreater(len(adult["axes"]["sensual_editorial"]["candidate_inventory"]), 0)
        self.assertGreaterEqual(len(adult["axes"]["fetish_fashion"]["candidate_inventory"]), 8)
        for route in pack["hybrid_augmentation"]["route_contract"]["routes"]:
            self.assertEqual(
                {detail["axis"] for detail in route["details"] if detail.get("axis")},
                {"sensual_editorial", "fetish_fashion"},
            )

        safe = self.composed_from_hybrid_route(pack, "material_world")
        safe_result = audit_composed_prompt.audit_composed_prompt(pack, safe)
        self.assertEqual(safe_result["status"], "pass", safe_result)

        risky = self.composed_from_hybrid_route(
            pack,
            "material_world",
            extra_chosen=("slot:camera_direction:low_ground_angle",),
        )
        risky["prompt_en"] += " Ground-level low angle."
        risky_result = audit_composed_prompt.audit_composed_prompt(pack, risky)
        self.assertIn(
            "adult_appeal_combination_risk",
            {row["check"] for row in risky_result["failures"]},
        )

    def test_creative_direction_audit_binds_one_developed_concept_and_rejects_contract_gaming(self):
        contract = prompt_generator.candidate_pack_creative_direction(
            {"provenance": {"creativity": 0.85}}
        )
        self.assertIsNotNone(contract)
        pack = {
            "creative_direction": contract,
            "artistic_final_touch": {
                "enabled": True,
                "final_sentence_en": (
                    "Let the final frame keep one quiet imperfection, shared light across subject and setting, "
                    "and a small material trace."
                ),
            },
        }
        proposals = [
            {
                "id": "absence",
                "operator_id": "absence_as_evidence",
                "premise": "The missing vessel is reconstructed only by how the living potter responds to its traces.",
                "familiar_anchor": "An adult potter inspects a finished cup at a dusty worktable.",
                "viewer_expectation": "The cup will be the completed hero object.",
                "rule_break": "A removed vessel remains optically present only through contact traces and alignment behavior.",
                "visible_consequences": [
                    "A clean clay ring interrupts the dusty table.",
                    "The potter aligns the small cup with the empty ring instead of presenting it.",
                ],
                "aboutness": "Craft is remembered through practiced attention rather than display.",
                "signature_phrase": "the absent vase remains visible as a clean clay ring",
            },
            {
                "id": "inversion",
                "operator_id": "expectation_inversion",
                "premise": "The workshop evaluates the maker through accumulated tool positions.",
                "familiar_anchor": "An adult potter stands among familiar tools.",
                "viewer_expectation": "The maker controls every tool.",
                "rule_break": "The arranged tools point toward the maker as if inspecting them.",
                "visible_consequences": ["Tool handles converge on the apron.", "The maker pauses under their alignment."],
                "aboutness": "A lifetime of practice also shapes the practitioner.",
                "signature_phrase": "tool handles converge like a silent jury",
            },
            {
                "id": "extension",
                "operator_id": "rule_extension",
                "premise": "Wet clay transfers touch memory into the workshop architecture.",
                "familiar_anchor": "An adult potter trims a cup.",
                "viewer_expectation": "Fingerprints stay on the clay object.",
                "rule_break": "Every fresh fingerprint also appears on one nearby hard surface.",
                "visible_consequences": ["A matching ridge crosses the table.", "A matching thumb hollow dents the light."],
                "aboutness": "Making changes the place that sustains it.",
                "signature_phrase": "matching fingerprints migrate across the workshop",
            },
            {
                "id": "fold",
                "operator_id": "temporal_fold",
                "premise": "One trimming gesture makes the repaired past and active present co-visible.",
                "familiar_anchor": "An adult potter checks a repaired cup.",
                "viewer_expectation": "The repair belongs to an earlier moment.",
                "rule_break": "The current hand movement continues the old repair seam in reflected light.",
                "visible_consequences": ["The seam aligns with the moving finger.", "Its reflection reaches an unfinished cup."],
                "aboutness": "Repair is an ongoing practice rather than a finished event.",
                "signature_phrase": "one repair seam continues through the present gesture",
            },
        ]
        prompt = (
            "An adult potter inspects a finished cup at a dusty worktable; the absent vase remains visible as a clean clay ring. "
            "A removed vessel is optically present through contact traces, and a clean ring interrupts the dust. "
            "The potter aligns the small cup with the empty ring instead of presenting it. "
            "First read the finished cup, then notice the empty circular trace, then recover a missing larger vessel from the alignment. "
            "The camera waits at shelf height, caught just before the cup meets the ring; the missing vessel never enters the frame, "
            "and every clue is made from fired-clay dust and contact rings."
        )
        evidence = {
            "familiar_anchor_phrase": "An adult potter inspects a finished cup at a dusty worktable",
            "rule_break_phrase": "A removed vessel is optically present through contact traces",
            "visible_consequence_phrases": [
                "a clean ring interrupts the dust",
                "The potter aligns the small cup with the empty ring instead of presenting it",
            ],
            "reveal_path_phrases": [
                "First read the finished cup",
                "then notice the empty circular trace",
                "then recover a missing larger vessel from the alignment",
            ],
            "authorial_grammar_phrases": {
                "vantage": "The camera waits at shelf height",
                "timing": "caught just before the cup meets the ring",
                "omission": "the missing vessel never enters the frame",
                "material_rule": "every clue is made from fired-clay dust and contact rings",
            },
        }
        brief = {
            "ordinary_baseline": ["portrait at a pottery wheel", "hands shaping wet clay", "shelves of finished cups"],
            "rejected_cliches": ["portrait at a pottery wheel", "hands shaping wet clay", "shelves of finished cups"],
            "proposals": proposals,
            "selected_proposal_id": "absence",
            "selection_rationale": "The trace remains photographically ordinary while making the missing object discoverable.",
            "selected_concept": {
                "proposal_id": "absence",
                "familiar_anchor": proposals[0]["familiar_anchor"],
                "rule_break": proposals[0]["rule_break"],
                "visible_consequences": proposals[0]["visible_consequences"],
                "reveal_path": ["recognize the cup", "notice the empty ring", "infer the absent vessel"],
                "aboutness": proposals[0]["aboutness"],
                "authorial_grammar": {
                    "vantage": "Shelf-height observation makes the alignment readable.",
                    "timing": "The shutter waits for the cup to nearly meet the trace.",
                    "omission": "The larger missing vessel is withheld.",
                    "material_rule": "Clay dust and contact rings carry every clue.",
                },
                "prompt_evidence": evidence,
            },
        }
        valid = {"creative_brief": brief}
        self.assertEqual(audit_composed_prompt.audit_creative_direction(pack, valid, prompt), [])

        cases = []
        missing_brief = {}
        cases.append((missing_brief, prompt, "creative_direction"))
        too_few = copy.deepcopy(valid)
        too_few["creative_brief"]["proposals"] = proposals[:3]
        cases.append((too_few, prompt, "creative_direction_proposals"))
        duplicate_move = copy.deepcopy(valid)
        duplicate_move["creative_brief"]["proposals"][1]["operator_id"] = "absence_as_evidence"
        cases.append((duplicate_move, prompt, "creative_direction_operators"))
        stacked_rule = copy.deepcopy(valid)
        stacked_rule["creative_brief"]["selected_concept"]["rule_break"] = ["first", "second"]
        cases.append((stacked_rule, prompt, "creative_direction_rule_break"))
        mixed = copy.deepcopy(valid)
        cases.append((mixed, prompt + " Tool handles converge like a silent jury.", "creative_direction_selection"))
        missing_binding = copy.deepcopy(valid)
        missing_binding["creative_brief"]["selected_concept"]["prompt_evidence"]["rule_break_phrase"] = "not in the prompt"
        cases.append((missing_binding, prompt, "creative_direction_binding"))
        borrowed_touch = copy.deepcopy(valid)
        borrowed_touch["creative_brief"]["selected_concept"]["prompt_evidence"]["authorial_grammar_phrases"]["vantage"] = "shared light"
        cases.append((borrowed_touch, prompt + " Shared light.", "creative_direction_authorial_grammar"))

        for composed, case_prompt, expected_check in cases:
            with self.subTest(expected_check=expected_check):
                checks = {
                    failure["check"]
                    for failure in audit_composed_prompt.audit_creative_direction(pack, composed, case_prompt)
                }
                self.assertIn(expected_check, checks)

    def test_viewer_experience_control_is_additive_and_high_creativity_enables_it_automatically(self):
        base_args = (
            "--concept",
            "보온병 광고",
            "--selection-mode",
            "rule",
            "--seed",
            "900101",
            "--emit-candidate-pack",
        )
        ordinary = self.run_wrapper(*base_args)[0]
        requested = self.run_wrapper(*base_args, "--viewer-experience")[0]
        creative = self.run_wrapper(*base_args, "--creativity", "0.85")[0]

        self.assertNotIn("viewer_experience", ordinary)
        requested_contract = requested["viewer_experience"]
        self.assertEqual(requested_contract["contract_version"], "photo-viewer-experience/v1")
        self.assertEqual(requested_contract["source"], "explicit_viewer_experience_control")
        self.assertEqual(requested_contract["activation_sources"], ["explicit_viewer_experience_control"])
        self.assertEqual(
            creative["viewer_experience"]["activation_sources"],
            ["creative_direction_required"],
        )
        self.assertIn("creative_direction", creative)
        self.assertEqual(ordinary["presets"], requested["presets"])
        self.assertEqual(ordinary["slots"], requested["slots"])
        self.assertEqual(ordinary["negative_en"], requested["negative_en"])

    def test_viewer_experience_audit_binds_visible_causes_and_rejects_response_gaming(self):
        contract = prompt_generator.candidate_pack_viewer_experience(
            {"provenance": {"viewer_experience_requested": True}}
        )
        self.assertIsNotNone(contract)
        pack = {"viewer_experience": contract}
        prompt = (
            "An adult field surveyor and one small original nonhuman companion kneel over the same cracked weather sensor. "
            "The companion braces the loose connector while the surveyor aligns it; the adult surveyor turns the alignment collar "
            "toward the companion, and the companion presses the loose contact into the same cracked weather sensor. "
            "The connector seats and both hands relax, with their shared grip paused over one repaired seam."
        )
        experience = {
            "target_audience": {
                "literacy": "subculture_literate",
                "required_prior_knowledge": "none",
            },
            "viewing_context": "full_screen",
            "primary_viewer_need": "relatedness",
            "intended_experience": "earned tenderness through reciprocal competence",
            "viewer_promise": "care becomes legible through two directed repair actions",
            "first_glance_hook": "an adult and an original nonhuman partner share one damaged device",
            "interpretive_question": "which partner noticed the fault first",
            "affect_evidence": {
                "actor": "the adult surveyor",
                "action": "turns the alignment collar toward the companion",
                "target": "the same cracked weather sensor",
                "consequence": "the connector seats and both hands relax",
            },
            "attachment_channel": "reciprocity",
            "reinspection_reward": {"mode": "none", "description": ""},
            "commercial_objective": "none",
            "prompt_evidence": {
                "first_glance_hook_phrase": "An adult field surveyor and one small original nonhuman companion kneel over the same cracked weather sensor",
                "affect_actor_phrase": "the adult surveyor",
                "affect_action_phrase": "turns the alignment collar toward the companion",
                "affect_target_phrase": "the same cracked weather sensor",
                "affect_consequence_phrase": "The connector seats and both hands relax",
                "attachment_phrase": "The companion braces the loose connector while the surveyor aligns it",
            },
        }
        valid = {"viewer_experience": experience}
        self.assertEqual(audit_composed_prompt.audit_viewer_experience(pack, valid, prompt), [])

        cases = []
        cases.append(({}, prompt, "viewer_experience"))
        stacked = copy.deepcopy(valid)
        stacked["viewer_experience"]["primary_viewer_need"] = ["care", "relatedness"]
        stacked["viewer_experience"]["primary_viewer_needs"] = ["care", "relatedness"]
        cases.append((stacked, prompt, "viewer_experience_affect_stacking"))
        missing_cause = copy.deepcopy(valid)
        missing_cause["viewer_experience"]["affect_evidence"].pop("consequence")
        cases.append((missing_cause, prompt, "viewer_experience_affect_cause"))
        invalid_enum = copy.deepcopy(valid)
        invalid_enum["viewer_experience"]["viewing_context"] = "algorithmic_feed_magic"
        cases.append((invalid_enum, prompt, "viewer_experience_enum"))
        no_attachment = copy.deepcopy(valid)
        no_attachment["viewer_experience"]["attachment_channel"] = "none"
        cases.append((no_attachment, prompt, "viewer_experience_attachment"))
        nonliteral = copy.deepcopy(valid)
        nonliteral["viewer_experience"]["prompt_evidence"]["affect_action_phrase"] = "not in the prompt"
        cases.append((nonliteral, prompt, "viewer_experience_binding"))
        outcome_claim = copy.deepcopy(valid)
        outcome_claim["viewer_experience"]["prompt_evidence"]["attachment_phrase"] = "creates attachment"
        cases.append((outcome_claim, prompt + " It creates attachment.", "viewer_experience_outcome_claim"))
        weak = copy.deepcopy(valid)
        weak["viewer_experience"]["prompt_evidence"]["attachment_phrase"] = "cute"
        cases.append((weak, prompt + " Cute.", "viewer_experience_weak_evidence"))
        youth = copy.deepcopy(valid)
        youth["viewer_experience"]["prompt_evidence"]["attachment_phrase"] = "childlike face"
        cases.append((youth, prompt + " Childlike face.", "viewer_experience_attachment"))
        commercial = copy.deepcopy(valid)
        commercial["viewer_experience"]["commercial_objective"] = "remember"
        cases.append((commercial, prompt, "viewer_experience_binding"))
        creative = copy.deepcopy(valid)
        creative_pack = {**pack, "creative_direction": {"enabled": True}}
        cases.append((creative, prompt, "viewer_experience_reinspection", creative_pack))

        for row in cases:
            if len(row) == 3:
                composed, case_prompt, expected_check = row
                case_pack = pack
            else:
                composed, case_prompt, expected_check, case_pack = row
            with self.subTest(expected_check=expected_check):
                checks = {
                    failure["check"]
                    for failure in audit_composed_prompt.audit_viewer_experience(case_pack, composed, case_prompt)
                }
                self.assertIn(expected_check, checks)

    def test_viewer_experience_holdout_and_visual_review_are_closed_and_distinct(self):
        holdout = [
            json.loads(line)
            for line in VIEWER_EXPERIENCE_HOLDOUT_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(holdout), 3)
        self.assertEqual(len({case["case_id"] for case in holdout}), 3)
        self.assertEqual({case["seed"] for case in holdout}, {900101, 900102, 900103})
        self.assertEqual(
            {case["expected_contract"]["primary_viewer_need"] for case in holdout},
            {"trust", "relatedness", "meaning"},
        )

        review = json.loads(VIEWER_EXPERIENCE_VISUAL_REVIEW_PATH.read_text(encoding="utf-8"))
        summary = eval_semantic.summarize_visual_review(
            VIEWER_EXPERIENCE_VISUAL_REVIEW_PATH
        )["visual_review"]
        self.assertEqual(review["schema_version"], "photo-visual-review/v1")
        self.assertEqual(review["cross_case_review"]["outcome"], "pass")
        self.assertEqual(review["cross_case_review"]["distinct_primary_need_count"], 3)
        self.assertEqual(review["cross_case_review"]["experience_convergence"], "none")
        self.assertEqual(summary["case_count"], 3)
        self.assertEqual(summary["contract_failure_count"], 0)
        self.assertEqual(summary["failed_case_count"], 0)
        self.assertEqual(summary["failed_review_focus_result_count"], 0)
        self.assertEqual(summary["review_focus_result_count"], 18)
        self.assertTrue(summary["passed"])

        holdout_by_id = {case["case_id"]: case for case in holdout}
        self.assertEqual(
            {case["case"] for case in review["cases"]},
            set(holdout_by_id),
        )
        for case in review["cases"]:
            frozen = holdout_by_id[case["case"]]
            self.assertEqual(case["initial_render_count"], 1)
            self.assertEqual(case["pristine_retry_count"], 0)
            self.assertRegex(case["image_sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual(
                {result["focus"] for result in case["review_focus_results"]},
                set(frozen["acceptance_dimensions"]),
            )
            self.assertTrue(all(result["outcome"] == "pass" for result in case["review_focus_results"]))

    def test_v4_scene_candidate_groups_hide_sampler_answers_and_v3_stays_fail_closed(self):
        common = (
            "--concept",
            "회사원",
            "--selection-mode",
            "rule",
            "--seed",
            "9",
            "--emit-candidate-pack",
        )
        pack = self.run_wrapper(*common)[0]
        groups = pack["scene_contract"]["groups"]
        self.assertTrue(groups)
        for group in groups:
            self.assertEqual(group["strategy"], "optional_inspiration_group")
            self.assertFalse(group["sampler_selection_exposed"])
            self.assertTrue(group["all_candidates_may_be_rejected"])
            self.assertNotIn("selected_entry_id", json.dumps(group))
            for slot, slot_contract in group["slots"].items():
                allowed = set(slot_contract["allowed_candidate_ids"])
                candidates = {
                    candidate["id"]
                    for candidate in pack["slots"].get(slot, {}).get("candidates", [])
                }
                self.assertTrue(candidates <= allowed)

        leaked = copy.deepcopy(pack)
        leaked["scene_contract"]["groups"][0]["slots"]["action"][
            "selected_entry_id"
        ] = "holding_coffee_phone"
        self.assertIn(
            "authorial_scene_selection",
            {row["check"] for row in audit_composed_prompt.audit_v4_authorial_pack(leaked)},
        )

        prior = self.run_wrapper(*common, "--candidate-pack-version", "v3")[0]
        self.assertTrue(prior["scene_contract"]["groups"])
        self.assertTrue(
            all(
                group["strategy"] == "atomic_scene"
                for group in prior["scene_contract"]["groups"]
            )
        )
        tampered = copy.deepcopy(prior)
        target_group = tampered["scene_contract"]["groups"][0]
        target_slot, target_contract = next(
            (slot, contract)
            for slot, contract in target_group["slots"].items()
            if contract.get("selected_entry_id")
        )
        target_id = target_contract["selected_entry_id"]
        target_contract["allowed_entry_ids"] = [
            entry_id for entry_id in target_contract["allowed_entry_ids"] if entry_id != target_id
        ]
        tampered["pack_id"] = audit_composed_prompt.computed_pack_id(tampered)
        prompt_terms = " ".join(str(item.get("text") or "") for item in tampered["mandatory_intents"])
        composed = {
            "pack_id": tampered["pack_id"],
            "prompt_en": prompt_terms,
            "negative_en": tampered.get("negative_en"),
            "chosen_candidate_ids": [f"slot:{target_slot}:{target_id}"],
            "composer": "agent",
        }
        result = audit_composed_prompt.audit_composed_prompt(tampered, composed)
        self.assertIn("atomic_scene_contract", {failure["check"] for failure in result["failures"]})

    def test_standalone_role_specific_mixin_does_not_borrow_an_unrelated_bundle(self):
        recipes = generate_photo_prompt.load_concept_recipes()
        mixin = recipes["mixins"]["암살자"]
        selected = generate_photo_prompt.select_bundle_for_mixin(
            "암살자", "암살자", mixin, ["--seed", "1"], None
        )
        self.assertIsNone(selected)

    def test_typed_routing_and_theme_guards_generalize_beyond_portraits(self):
        architecture = self.run_wrapper(
            "--preset",
            "infrastructure_inspection_record",
            "--selection-mode",
            "rule",
            "--seed",
            "29",
            "--additional-requirement",
            "bridge architecture and flood-control infrastructure as the primary subject",
            "--emit-candidate-pack",
            "--candidate-pack-version",
            "v3",
        )[0]
        self.assertIn("environment", architecture["coverage"]["intent_constraints"]["subject_categories"])
        selected_subject = next(
            candidate
            for candidate in architecture["slots"]["subject"]["candidates"]
            if candidate.get("selected_by_sampler")
        )
        self.assertIn("environment", selected_subject["kind"])

        food = self.run_wrapper(
            "--preset",
            "community_kitchen_documentary",
            "--selection-mode",
            "rule",
            "--seed",
            "31",
            "--additional-requirement",
            "restrained observational food process",
            "--emit-candidate-pack",
        )[0]
        exposed_ids = {
            candidate["entry_id"]
            for slot_payload in food["slots"].values()
            for candidate in slot_payload["candidates"]
        }
        self.assertTrue(
            {
                "kinetic_spell_trail_motion",
                "visible_ball_joint_seam",
                "charging_indicator_glow",
                "thermal_lowfi_pov",
                "exposed_joint_focus",
                "boot_flicker_motion",
                "feather_skin_follicle_blend",
                "surface_caustic_light",
            }.isdisjoint(exposed_ids)
        )

    def test_visual_review_contract_rejects_empty_or_unprovenanced_payloads(self):
        with tempfile.TemporaryDirectory() as tmp:
            review_path = Path(tmp) / "review.json"
            review_path.write_text(json.dumps({"cases": []}), encoding="utf-8")
            summary = eval_semantic.summarize_visual_review(review_path)["visual_review"]
        self.assertFalse(summary["passed"])
        self.assertGreaterEqual(summary["contract_failure_count"], 3)
        self.assertEqual(summary["failed_case_count"], 0)

    def test_visual_review_contract_rejects_invalid_enums_and_declared_conflicts(self):
        case = {
            "case": "synthetic",
            "prompt_id": "prompt-1",
            "image_id": "image-1",
            "dual_read": "maybe",
            "archetype_first_read": "pass",
            "body_drift": "none",
            "preset_conflict": "present",
            "role_anchor": "pass",
            "mixin_anchor": "pass",
            "body_coverage_guard": "pass",
            "render_modality": "pass",
            "framing_constraint": "pass",
            "body_emphasis_survived": "yes",
        }
        payload = {
            "schema_version": "photo-visual-review/v1",
            "provenance": {
                "generator_version": "test",
                "tags_hash": "hash",
                "reviewer": "reviewer",
                "reviewed_at": "2026-08-05T00:00:00Z",
            },
            "cases": [case],
        }
        with tempfile.TemporaryDirectory() as tmp:
            review_path = Path(tmp) / "review.json"
            review_path.write_text(json.dumps(payload), encoding="utf-8")
            summary = eval_semantic.summarize_visual_review(review_path)["visual_review"]
        self.assertFalse(summary["passed"])
        self.assertIn("case_field_enum", {failure["check"] for failure in summary["contract_failures"]})
        self.assertEqual(
            set(summary["failed_cases"][0]["failures"]),
            {"preset_conflict", "body_emphasis_survived"},
        )

    def test_domain_visual_review_plan_links_completed_review_but_is_not_acceptance_evidence(self):
        plan = json.loads(DOMAIN_VISUAL_REVIEW_PLAN_PATH.read_text(encoding="utf-8"))
        self.assertEqual(plan["schema_version"], "photo-domain-visual-review-plan/v1")
        self.assertEqual(plan["status"], "completed")
        self.assertFalse(plan["acceptance_artifact"])
        self.assertEqual(plan["review_artifact"], DOMAIN_VISUAL_REVIEW_RESULTS_PATH.name)
        self.assertEqual(len(plan["cases"]), 12)
        self.assertEqual(len({case["preset"] for case in plan["cases"]}), 12)

        summary = eval_semantic.summarize_visual_review(DOMAIN_VISUAL_REVIEW_RESULTS_PATH)["visual_review"]
        self.assertTrue(summary["passed"])
        self.assertEqual(summary["case_count"], 12)
        self.assertEqual(summary["failed_case_count"], 0)
        self.assertEqual(summary["contract_failure_count"], 0)
        self.assertEqual(summary["review_focus_result_count"], 36)
        self.assertEqual(summary["failed_review_focus_result_count"], 0)
        for field in (
            "body_drift",
            "role_anchor",
            "mixin_anchor",
            "body_coverage_guard",
            "body_emphasis_survived",
        ):
            self.assertEqual(summary["field_summaries"][field]["counts"]["not_applicable"], 12)

    def test_visual_review_contract_fails_closed_on_declared_review_focus_failure(self):
        payload = json.loads(DOMAIN_VISUAL_REVIEW_RESULTS_PATH.read_text(encoding="utf-8"))
        payload["cases"] = [dict(payload["cases"][0])]
        payload["cases"][0]["review_focus_results"] = [
            {
                "focus": "required visual evidence",
                "outcome": "fail",
                "evidence": "The required evidence is absent.",
            }
        ]
        with tempfile.TemporaryDirectory() as tmp:
            review_path = Path(tmp) / "review.json"
            review_path.write_text(json.dumps(payload), encoding="utf-8")
            summary = eval_semantic.summarize_visual_review(review_path)["visual_review"]

        self.assertFalse(summary["passed"])
        self.assertEqual(summary["failed_case_count"], 1)
        self.assertEqual(summary["failed_review_focus_result_count"], 1)
        self.assertIn("review_focus", summary["failed_cases"][0]["failures"])

    def test_visual_review_contract_requires_reason_for_not_applicable_fields(self):
        payload = json.loads(DOMAIN_VISUAL_REVIEW_RESULTS_PATH.read_text(encoding="utf-8"))
        payload["cases"] = [dict(payload["cases"][0])]
        payload["cases"][0].pop("not_applicable_reason")
        with tempfile.TemporaryDirectory() as tmp:
            review_path = Path(tmp) / "review.json"
            review_path.write_text(json.dumps(payload), encoding="utf-8")
            summary = eval_semantic.summarize_visual_review(review_path)["visual_review"]

        self.assertFalse(summary["passed"])
        self.assertIn(
            "not_applicable_reason",
            {failure["check"] for failure in summary["contract_failures"]},
        )

    def test_expanded_dictionary_has_operational_domain_packs_facets_and_primary_guards(self):
        tags = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_LAYERS_PATH.read_text(encoding="utf-8"))
        preset_ids = {preset["id"] for preset in tags["presets"]}
        self.assertGreaterEqual(len(preset_ids), 555)
        self.assertTrue(
            {
                "wetland_behavior_documentary",
                "forest_floor_macro_ecology",
                "industrial_process_documentary",
                "infrastructure_inspection_record",
                "farm_to_table_process",
                "community_kitchen_documentary",
                "laboratory_measurement_record",
                "field_sensor_survey",
                "warehouse_flow_documentary",
                "transit_maintenance_record",
                "coastal_resilience_monitoring",
                "urban_heat_air_quality_record",
                "camera_trap_species_monitoring",
                "coastal_benthic_quadrat_survey",
                "orchard_harvest_grading_record",
                "fermentation_batch_monitoring",
                "electronics_repair_diagnostic_record",
                "materials_recovery_sorting_record",
            }
            <= preset_ids
        )
        subject_ids = {entry["id"] for entry in tags["slots"]["subject"]}
        self.assertTrue(
            {
                "pollinator_moth_night",
                "cleanroom_wafer_robot",
                "community_soup_pot",
                "microscope_sample_stage",
                "field_air_quality_station",
                "parcel_sorting_conveyor",
                "rail_switch_actuator",
                "coastal_erosion_marker_array",
                "urban_heat_sensor_station",
                "camera_trap_wildlife_passage",
                "intertidal_quadrat_biota",
                "orchard_fruit_grading_line",
                "fermentation_vessel_batch",
                "open_electronics_repair_board",
                "mixed_material_sorting_stream",
            }
            <= subject_ids
        )
        coastal_subject = next(
            entry for entry in tags["slots"]["subject"] if entry["id"] == "coastal_erosion_marker_array"
        )
        self.assertEqual(
            prompt_generator.subject_category({"subject": coastal_subject}, tags),
            "environment",
        )
        guarded_ids = {
            entry["id"]
            for entries in tags["slots"].values()
            for entry in entries
            if entry.get("requires_primary_any_tags")
        }
        self.assertTrue(
            {
                "kinetic_spell_trail_motion",
                "snowflake_pinpoint_glow",
                "thermal_lowfi_pov",
                "aligning_microscope_sample",
                "collecting_air_sample",
                "routing_parcels_conveyor",
                "inspecting_rail_switch",
                "measuring_shoreline_retreat",
                "logging_surface_temperature",
                "microscopy_measurement_capture",
                "thermal_field_survey_capture",
                "fixed_interval_monitoring_capture",
            }
            <= guarded_ids
        )
        self.assertTrue(
            {
                "relation_type",
                "event_phase",
                "process_stage",
                "capture_modality",
                "weather_effect",
                "movement_type",
            }
            <= set(tags["facet_vocab"])
        )
        operational_domains = {
            "science_inspection",
            "mobility_logistics",
            "climate_adaptation",
            "biodiversity_monitoring",
            "agriculture_food_systems",
            "circular_materials",
        }
        self.assertTrue(operational_domains <= set(quality["quality_profiles"]))
        self.assertTrue(
            operational_domains
            <= {row["domain"] for row in quality["intent_routing"]["domains"]}
        )
        self.assertTrue(
            {
                "relational_coordination",
                "process_stage_evidence",
                "instrument_capture_modality",
                "mobility_flow",
                "climate_material_consequence",
                "biodiversity_observation_protocol",
                "agriculture_batch_traceability",
                "circular_repair_material_flow",
            }
            <= {axis["id"] for axis in quality["photographic_integration"]["axes"]}
        )
        capture_policy = tags["slot_applicability"]["slots"]["capture_context"]
        self.assertTrue({"object", "environment"} <= set(capture_policy["subject_categories"]))
        self.assertTrue(operational_domains <= set(capture_policy["allow_domains"]))
        routing_categories = {
            row["category"] for row in quality["intent_routing"]["subject_categories"]
        }
        self.assertTrue({"animal", "object", "food", "plant", "environment"} <= routing_categories)
        expected_typed_presets = {
            "science_inspection": {"laboratory_measurement_record", "field_sensor_survey"},
            "mobility_logistics": {"warehouse_flow_documentary", "transit_maintenance_record"},
            "climate_adaptation": {"coastal_resilience_monitoring", "urban_heat_air_quality_record"},
            "biodiversity_monitoring": {"camera_trap_species_monitoring", "coastal_benthic_quadrat_survey"},
            "agriculture_food_systems": {"orchard_harvest_grading_record", "fermentation_batch_monitoring"},
            "circular_materials": {"electronics_repair_diagnostic_record", "materials_recovery_sorting_record"},
        }
        for domain, expected_ids in expected_typed_presets.items():
            actual_ids = {
                preset["id"]
                for preset in tags["presets"]
                if domain in prompt_generator.preset_domains(preset, tags)
            }
            self.assertEqual(actual_ids, expected_ids)

    def test_quality_facets_do_not_treat_focus_metadata_as_scene_location(self):
        pack = self.run_wrapper(
            "--preset",
            "laboratory_measurement_record",
            "--selection-mode",
            "rule",
            "--seed",
            "41",
            "--set",
            "focus=zone_focus_street",
            "--emit-candidate-pack",
            "--candidate-pack-version",
            "v3",
        )[0]
        self.assertEqual(pack["quality_profile"]["profile_id"], "science_inspection")
        self.assertNotIn("street", pack["quality_profile"]["facets"].get("place_type", []))

    def test_new_typed_domain_packs_are_scoped_without_legacy_pool_pollution(self):
        tags = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_LAYERS_PATH.read_text(encoding="utf-8"))
        tags[prompt_generator.QUALITY_LAYERS_DATA_KEY] = quality
        presets = {preset["id"]: preset for preset in tags["presets"]}

        typed_presets = {
            "camera_trap_species_monitoring": "biodiversity_monitoring",
            "orchard_harvest_grading_record": "agriculture_food_systems",
            "electronics_repair_diagnostic_record": "circular_materials",
        }
        for preset_id, domain in typed_presets.items():
            preset = presets[preset_id]
            self.assertFalse(
                prompt_generator.preset_matches_automatic_intent_scope(preset, tags, None)
            )
            self.assertTrue(
                prompt_generator.preset_matches_automatic_intent_scope(
                    preset,
                    tags,
                    {
                        "intent_source": "user",
                        "intent_constraints": {"domains": [domain]},
                    },
                )
            )

        legacy_portrait = presets["maid_cafe_cosplay_portrait"]
        scoped_entries = [
            entry
            for entries in tags["slots"].values()
            for entry in entries
            if set(entry.get("tags", []))
            & set(prompt_generator.INTENT_SCOPED_ENTRY_DOMAIN_TAGS)
        ]
        self.assertEqual(len(scoped_entries), 40)
        self.assertTrue(
            all(
                not prompt_generator.entry_matches_preset_domain_scope(entry, legacy_portrait, tags)
                for entry in scoped_entries
            )
        )
        for preset_id in typed_presets:
            preset = presets[preset_id]
            filtered_ids = {
                entry_id
                for slot_filter in (preset.get("filters") or {}).values()
                for entry_id in slot_filter.get("ids", [])
            }
            scoped_for_preset = [entry for entry in scoped_entries if entry["id"] in filtered_ids]
            self.assertTrue(scoped_for_preset)
            self.assertTrue(
                all(
                    prompt_generator.entry_matches_preset_domain_scope(entry, preset, tags)
                    for entry in scoped_for_preset
                )
            )

        axis_profiles = {
            axis["id"]: axis.get("profile_match")
            for axis in quality["photographic_integration"]["axes"]
        }
        self.assertEqual(axis_profiles["biodiversity_observation_protocol"], ["biodiversity_monitoring"])
        self.assertEqual(axis_profiles["agriculture_batch_traceability"], ["agriculture_food_systems"])
        self.assertEqual(axis_profiles["circular_repair_material_flow"], ["circular_materials"])

        shared_facets = {
            "place_type": ["nature"],
            "process_stage": ["monitoring"],
            "capture_modality": ["surveillance"],
        }
        typed_craft = prompt_generator.candidate_pack_photographic_craft(
            tags,
            {"profile_id": "biodiversity_monitoring", "facets": shared_facets},
        )
        legacy_craft = prompt_generator.candidate_pack_photographic_craft(
            tags,
            {"profile_id": "nature", "facets": shared_facets},
        )
        typed_refinements = {
            refinement["id"]
            for dimension in typed_craft["active_dimensions"]
            for refinement in dimension["active_refinements"]
        }
        legacy_refinements = {
            refinement["id"]
            for dimension in legacy_craft["active_dimensions"]
            for refinement in dimension["active_refinements"]
        }
        self.assertIn("field_observation_record", typed_refinements)
        self.assertNotIn("field_observation_record", legacy_refinements)
        self.assertIn(
            "evidence_led",
            {strategy["id"] for strategy in typed_craft["strategy_variants"]},
        )
        self.assertNotIn(
            "evidence_led",
            {strategy["id"] for strategy in legacy_craft["strategy_variants"]},
        )

    def test_generalization_suite_is_executable_and_green(self):
        completed = subprocess.run(
            [
                sys.executable,
                str(EVAL_PATH),
                "--tags",
                str(TAGS_PATH),
                "--generalization-cases",
                str(GENERALIZATION_PATH),
                "--generalization-check",
                "--holdout-cases",
                str(HOLDOUT_PATH),
                "--holdout-check",
                "--domain-holdout-v2-cases",
                str(DOMAIN_HOLDOUT_V2_PATH),
                "--domain-holdout-v2-check",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["generalization_check"]["case_count"], 79)
        self.assertEqual(payload["generalization_check"]["failed_case_count"], 0)
        self.assertEqual(payload["holdout_check"]["case_count"], 24)
        self.assertEqual(payload["holdout_check"]["failed_case_count"], 0)
        self.assertEqual(payload["domain_holdout_v2_check"]["case_count"], 6)
        self.assertEqual(payload["domain_holdout_v2_check"]["failed_case_count"], 0)

    def test_retrieval_holdout_and_research_evidence_contracts_are_versioned(self):
        retrieval_cases = eval_semantic.load_retrieval_holdout_cases(RETRIEVAL_HOLDOUT_V3_PATH)
        self.assertEqual(len(retrieval_cases), 6)
        self.assertTrue(all(case["allowed_selected_presets"] for case in retrieval_cases))
        self.assertTrue(all("preset" not in case for case in retrieval_cases))

        retrieval_v4_cases = eval_semantic.load_retrieval_holdout_cases(RETRIEVAL_HOLDOUT_V4_PATH)
        self.assertEqual(len(retrieval_v4_cases), 22)
        self.assertEqual(retrieval_v4_cases[:6], retrieval_cases)
        self.assertTrue(all(case["allowed_selected_presets"] for case in retrieval_v4_cases))
        self.assertTrue(all("preset" not in case for case in retrieval_v4_cases))

        evidence_rows = [
            json.loads(line)
            for line in RESEARCH_EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertGreaterEqual(len(evidence_rows), 20)
        self.assertEqual(len({row["id"] for row in evidence_rows}), len(evidence_rows))
        self.assertGreaterEqual(len({row["domain"] for row in evidence_rows}), 15)
        merged_tags = prompt_generator.load_json(TAGS_PATH)
        catalog_ids = {str(preset["id"]) for preset in merged_tags["presets"]}
        for entries in merged_tags["slots"].values():
            catalog_ids.update(str(entry["id"]) for entry in entries)
        for row in evidence_rows:
            self.assertEqual(row["schema_version"], "photo-research-evidence/v1")
            self.assertEqual(row["status"], "approved")
            self.assertTrue(str(row["source_url"]).startswith("https://"))
            self.assertTrue(row["abstracted_dimensions"])
            self.assertTrue(row["candidate_ids"])
            self.assertTrue(set(row["candidate_ids"]) <= catalog_ids, row["id"])
            self.assertIn("no ", row["reuse_note"].lower())
            self.assertIn("copied", row["reuse_note"].lower())

    def test_research_extension_is_additive_and_scopes_automatic_slots(self):
        raw_tags = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        extension = json.loads(RESEARCH_EXTENSION_PATH.read_text(encoding="utf-8"))
        merged = prompt_generator.merge_research_extension(copy.deepcopy(raw_tags), copy.deepcopy(extension))

        extension_ids = {preset["id"] for preset in extension["presets"]}
        merged_presets = {preset["id"]: preset for preset in merged["presets"]}
        self.assertEqual(len(extension_ids), 17)
        self.assertTrue(extension_ids <= set(merged_presets))

        for preset_id in extension_ids:
            preset = merged_presets[preset_id]
            self.assertEqual(preset["auto_optional_policy"], "authored_filters_only")
            filter_slots = set(preset.get("filters", {}))
            for spec in prompt_generator.optional_slot_specs(preset, merged):
                if spec.get("source") == "auto":
                    self.assertIn(spec["slot"], filter_slots, (preset_id, spec))

        duplicate = {
            "schema_version": prompt_generator.RESEARCH_EXTENSION_SCHEMA,
            "presets": [{"id": raw_tags["presets"][0]["id"], "filters": {}}],
        }
        with self.assertRaisesRegex(ValueError, "duplicate extension id"):
            prompt_generator.merge_research_extension(copy.deepcopy(raw_tags), duplicate)

        generic_window = prompt_generator.semantic_preset_score_window(
            {"semantic_profile": "conservative", "novelty": "low", "intent_constraints": {"domains": []}}
        )
        typed_window = prompt_generator.semantic_preset_score_window(
            {
                "semantic_profile": "conservative",
                "novelty": "low",
                "intent_constraints": {"domains": ["science_inspection"]},
            }
        )
        self.assertLess(typed_window, generic_window)

    def test_subculture_extension_routes_are_scoped_complete_and_runtime_selectable(self):
        data = prompt_generator.load_json(TAGS_PATH)
        extension = json.loads(SUBCULTURE_EXTENSION_PATH.read_text(encoding="utf-8"))
        extension_ids = {preset["id"] for preset in extension["presets"]}
        route_ids = extension_ids | {"punk_basement_show", "warehouse_rave_uv"}
        presets = {preset["id"]: preset for preset in data["presets"]}

        self.assertEqual(len(extension_ids), 33)
        self.assertEqual(
            set(extension["slot_applicability"]["preset_domain_overrides"]),
            route_ids,
        )
        self.assertTrue(route_ids <= set(presets))

        surface_policy = data["slot_applicability"]["slots"]["surface_material"]
        self.assertNotIn("human", surface_policy["subject_categories"])
        self.assertTrue(surface_policy["allow_domains_override_subject_categories"])
        self.assertEqual(
            prompt_generator.slot_block_reason(
                data,
                "surface_material",
                {"subject_category": "human", "preset_domains": ["sports_motion"]},
            ),
            "subject_category_not_allowed",
        )
        self.assertIsNone(
            prompt_generator.slot_block_reason(
                data,
                "surface_material",
                {
                    "subject_category": "human",
                    "preset_domains": ["subculture_practice"],
                },
            )
        )

        requested_context = {
            "intent_source": "user",
            "intent_constraints": {"domains": ["subculture_practice"]},
        }
        for seed, preset_id in enumerate(sorted(route_ids), start=1):
            preset = presets[preset_id]
            self.assertEqual(
                prompt_generator.preset_domains(preset, data),
                {"subculture_practice"},
            )
            self.assertTrue(
                {"subject", "action", "location", "prop"}
                <= set(preset["required_slots"]),
                preset_id,
            )
            self.assertFalse(
                prompt_generator.preset_matches_automatic_intent_scope(preset, data, None),
                preset_id,
            )
            self.assertTrue(
                prompt_generator.preset_matches_automatic_intent_scope(
                    preset, data, requested_context
                ),
                preset_id,
            )

            result = prompt_generator.generate_once(
                data,
                __import__("random").Random(seed),
                preset_id,
                ["en"],
                False,
                0,
                True,
                detail_level="detailed",
                selection_mode="rule",
                seed=seed,
            )
            choices = result["choices"]
            self.assertTrue(
                set(preset["required_slots"]) <= set(choices),
                (preset_id, sorted(set(preset["required_slots"]) - set(choices))),
            )
            for slot, choice in choices.items():
                authored_ids = set((preset.get("filters", {}).get(slot) or {}).get("ids", []))
                if authored_ids:
                    self.assertIn(choice["id"], authored_ids, (preset_id, slot, choice["id"]))

        first_route, second_route = sorted(route_ids)[:2]
        scoped_context = {
            "intent_source": "user",
            "intent_constraints": {
                "domains": ["subculture_practice"],
                "scoped_routes": [first_route],
            },
        }
        self.assertTrue(
            prompt_generator.preset_matches_automatic_intent_scope(
                presets[first_route], data, scoped_context
            )
        )
        self.assertFalse(
            prompt_generator.preset_matches_automatic_intent_scope(
                presets[second_route], data, scoped_context
            )
        )

        age_only_entries = [
            entry
            for entries in data["slots"].values()
            for entry in entries
            if "age_context_only" in set(entry.get("tags", []))
        ]
        self.assertGreaterEqual(len(age_only_entries), 40)
        for entry in age_only_entries:
            self.assertNotIn("adult", prompt_generator.adult_semantic_tokens(entry), entry["id"])

        legacy = presets["lowrider_night_meet"]
        self.assertFalse(legacy["automatic_discovery"])
        indexed_keys = {
            key for key, _, _, _ in prompt_generator.iter_semantic_entries(data)
        }
        self.assertNotIn("preset:lowrider_night_meet", indexed_keys)
        self.assertEqual(
            prompt_generator.choose_preset(
                data, __import__("random").Random(1), "lowrider_night_meet"
            )["id"],
            "lowrider_night_meet",
        )

        extension_text = json.dumps(extension, ensure_ascii=False).lower()
        for specific_ip_or_brand in (
            "pokemon",
            "mario",
            "gundam",
            "vocaloid",
            "hatsune miku",
            "disney",
            "sanrio",
            "hello kitty",
            "warhammer",
            "dungeons & dragons",
            "marvel",
            "dc comics",
            "nintendo",
            "playstation",
            "xbox",
            "hololive",
            "nijisanji",
            "live2d",
            "comiket",
        ):
            self.assertNotIn(specific_ip_or_brand, extension_text)

    def test_subculture_holdout_and_evidence_cover_all_frozen_themes(self):
        data = prompt_generator.load_json(TAGS_PATH)
        preset_ids = {preset["id"] for preset in data["presets"]}
        cases = eval_semantic.load_retrieval_holdout_cases(
            SUBCULTURE_RETRIEVAL_HOLDOUT_V1_PATH
        )
        self.assertEqual(len(cases), 70)
        self.assertEqual(len({case["id"] for case in cases}), 70)
        target_ids = {
            preset_id
            for case in cases
            for preset_id in case["allowed_selected_presets"]
        }
        self.assertEqual(len(target_ids), 35)
        self.assertTrue(target_ids <= preset_ids)
        data[prompt_generator.QUALITY_LAYERS_DATA_KEY] = prompt_generator.load_quality_layers(
            QUALITY_LAYERS_PATH
        )
        routing_policy = prompt_generator.candidate_pack_intent_routing_policy(data)
        scoped_rules = [
            rule
            for rule in routing_policy["scoped_routes"]
            if rule["domain"] == "subculture_practice"
        ]
        self.assertEqual(len(scoped_rules), 35)
        self.assertEqual({rule["preset_id"] for rule in scoped_rules}, target_ids)
        for rule in scoped_rules:
            self.assertEqual(rule["domain"], "subculture_practice")
            self.assertTrue(rule["aliases"])
        for case in cases:
            routed = prompt_generator.resolve_request_intent_constraints(
                data, {"intent": case["intent"]}, {}
            )
            self.assertIn("subculture_practice", routed["domains"], case["id"])
            self.assertEqual(
                set(routed["scoped_routes"]),
                set(case["allowed_selected_presets"]),
                case["id"],
            )
        self.assertTrue(
            prompt_generator.intent_alias_matches("adult costume makers", "costume maker")
        )
        self.assertTrue(
            prompt_generator.intent_alias_matches("resin garage-kit parts", "garage kit")
        )
        for generic_intent in (
            "a generic studio portrait with neutral clothing and soft light",
            "판타지 코스프레 인물 사진",
            "K-style beauty editorial in a clean studio",
            "자동차 정비사가 주차된 차량을 점검하는 일반 다큐멘터리",
            "직업 교육 작업실에서 공구를 정리하는 모습",
        ):
            routed = prompt_generator.resolve_request_intent_constraints(
                data, {"intent": generic_intent}, {}
            )
            self.assertNotIn("subculture_practice", routed["domains"], generic_intent)
            self.assertFalse(routed["scoped_routes"], generic_intent)

        evidence_rows = [
            json.loads(line)
            for line in RESEARCH_EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip() and json.loads(line).get("domain") == "subculture_practice"
        ]
        self.assertGreaterEqual(len(evidence_rows), 46)
        theme_targets = {
            "cosplay": {"cosplay_fabrication_event_practice"},
            "fan_publishing": {"artist_alley_fan_publishing_exchange"},
            "zine_print": {"diy_zine_print_workshop"},
            "virtual_creator": {"virtual_creator_production_session"},
            "scale_models": {"scale_model_kitbash_workbench"},
            "diorama": {"miniature_diorama_build_workbench"},
            "toy_customization": {
                "doll_toy_customization_workshop",
                "plush_toy_repair_customization",
            },
            "character_suits": {
                "fursuit_fabrication_care",
                "mascot_suit_performance_care",
            },
            "lolita": {"lolita_coordinate_culture"},
            "japanese_street_style": {
                "decora_diy_maximalism",
                "gyaru_shibuya_glam",
                "heisei_y2k_revival",
            },
            "visual_kei": {"visual_kei_live_house"},
            "goth_club_rave": {
                "goth_scene_style_documentary",
                "cybergoth_club_style_documentary",
                "new_romantic_club_style_documentary",
                "warehouse_rave_uv",
            },
            "independent_music": {
                "punk_basement_show",
                "noise_performance_space_documentary",
                "shoegaze_small_venue_documentary",
            },
            "retro_gaming": {
                "retro_arcade_community_practice",
                "retro_lan_byoc_session",
                "retro_speedrun_event_practice",
            },
            "tabletop": {
                "ttrpg_collaborative_session",
                "miniature_wargaming_social_practice",
            },
            "custom_hardware": {
                "custom_pc_build_workbench",
                "mechanical_keyboard_build_workbench",
                "cyberdeck_enclosure_prototyping",
            },
            "vehicle_culture": {
                "lowrider_community_craft",
                "tuner_car_workshop_documentary",
                "itasha_display_culture_documentary",
            },
            "fandom_material": {
                "idol_fandom_material_culture",
                "anime_fandom_collection_exchange",
            },
        }
        self.assertEqual(len(theme_targets), 18)
        for theme, targets in theme_targets.items():
            independent_sources = {
                row["source_url"]
                for row in evidence_rows
                if targets & set(row["candidate_ids"])
            }
            self.assertGreaterEqual(len(independent_sources), 2, (theme, independent_sources))

    def test_worldbuilding_extension_routes_holdout_and_evidence_are_deep_and_scoped(self):
        data = prompt_generator.load_json(TAGS_PATH)
        extension = json.loads(WORLDBUILDING_EXTENSION_PATH.read_text(encoding="utf-8"))
        extension_ids = {preset["id"] for preset in extension["presets"]}
        presets = {preset["id"]: preset for preset in data["presets"]}
        self.assertEqual(len(extension_ids), 18)
        self.assertEqual(len(extension["preset_families"]), 6)
        self.assertEqual(
            sum(len(entries) for entries in extension["slots"].values()),
            288,
        )
        self.assertEqual(
            set(extension["slot_applicability"]["preset_domain_overrides"]),
            extension_ids,
        )
        self.assertTrue(extension_ids <= set(presets))

        world_evidence_slots = {
            "situation_context",
            "occasion_context",
            "narrative_core",
            "capture_context",
            "procedure_step",
            "surface_material",
        }
        requested_context = {
            "intent_source": "user",
            "intent_constraints": {"domains": ["worldbuilding_system"]},
        }
        for preset_id in sorted(extension_ids):
            preset = presets[preset_id]
            self.assertEqual(
                prompt_generator.preset_domains(preset, data),
                {"worldbuilding_system"},
            )
            self.assertTrue(
                {"subject", "action", "location", "prop"} | world_evidence_slots
                <= set(preset["required_slots"]),
                preset_id,
            )
            self.assertGreaterEqual(len(preset["facets"]["world_mechanism"]), 6)
            self.assertFalse(
                prompt_generator.preset_matches_automatic_intent_scope(preset, data, None)
            )
            self.assertTrue(
                prompt_generator.preset_matches_automatic_intent_scope(
                    preset, data, requested_context
                )
            )

            seen_subjects = set()
            for seed in (1, 2):
                result = prompt_generator.generate_once(
                    data,
                    __import__("random").Random(seed),
                    preset_id,
                    ["en"],
                    False,
                    0,
                    True,
                    detail_level="detailed",
                    selection_mode="rule",
                    seed=seed,
                )
                choices = result["choices"]
                self.assertTrue(set(preset["required_slots"]) <= set(choices), preset_id)
                subject_id = choices["subject"]["id"]
                seen_subjects.add(subject_id)
                scene_prefix = subject_id.removesuffix("_subject")
                for slot in (
                    "action",
                    "location",
                    "prop",
                    "situation_context",
                    "occasion_context",
                ):
                    self.assertTrue(
                        choices[slot]["id"].startswith(f"{scene_prefix}_"),
                        (preset_id, seed, slot, subject_id, choices[slot]["id"]),
                    )

                pack = prompt_generator.build_candidate_pack(result, data)
                self.assertEqual(pack["contract_version"], "photo-candidate-pack/v4")
                self.assertTrue(world_evidence_slots <= set(pack["slots"]), preset_id)
                self.assertNotIn("content_basis", preset["facets"], preset_id)
                self.assertFalse(
                    prompt_generator.CONTROL_ONLY_FACET_KEYS
                    & set(pack["quality_profile"]["facets"]),
                    preset_id,
                )
                self.assertTrue(
                    all(
                        not (
                            prompt_generator.CONTROL_ONLY_FACET_KEYS
                            & set(candidate.get("facets", {}))
                        )
                        for candidate in pack["presets"]
                    ),
                    preset_id,
                )
                self.assertTrue(
                    all(
                        not (
                            prompt_generator.CONTROL_ONLY_FACET_KEYS
                            & set(candidate.get("facets", {}))
                        )
                        for slot in pack["slots"].values()
                        for candidate in slot.get("candidates", [])
                    ),
                    preset_id,
                )
                self.assertLessEqual(
                    sum(len(slot["candidates"]) for slot in pack["slots"].values()),
                    prompt_generator.CANDIDATE_PACK_TOTAL_CANDIDATE_LIMIT,
                    preset_id,
                )
            self.assertEqual(len(seen_subjects), 2, preset_id)

        self.assertTrue(
            all("content_basis" not in (preset.get("facets") or {}) for preset in presets.values())
        )

        cases = eval_semantic.load_retrieval_holdout_cases(
            WORLDBUILDING_RETRIEVAL_HOLDOUT_V1_PATH
        )
        self.assertEqual(len(cases), 72)
        self.assertEqual(len({case["id"] for case in cases}), 72)
        targets = {
            preset_id
            for case in cases
            for preset_id in case["allowed_selected_presets"]
        }
        self.assertEqual(targets, extension_ids)
        self.assertTrue(all(len(case["allowed_selected_presets"]) == 1 for case in cases))

        data[prompt_generator.QUALITY_LAYERS_DATA_KEY] = prompt_generator.load_quality_layers(
            QUALITY_LAYERS_PATH
        )
        routing_policy = prompt_generator.candidate_pack_intent_routing_policy(data)
        world_rules = [
            rule
            for rule in routing_policy["scoped_routes"]
            if rule["domain"] == "worldbuilding_system"
        ]
        self.assertEqual(len(world_rules), 18)
        self.assertEqual({rule["preset_id"] for rule in world_rules}, extension_ids)
        for case in cases:
            routed = prompt_generator.resolve_request_intent_constraints(
                data, {"intent": case["intent"]}, {}
            )
            self.assertIn("worldbuilding_system", routed["domains"], case["id"])
            self.assertEqual(
                set(routed["scoped_routes"]),
                set(case["allowed_selected_presets"]),
                case["id"],
            )

        solarpunk_case = next(case for case in cases if case["id"] == "world_solarpunk_ko_02")
        solarpunk_constraints = prompt_generator.resolve_request_intent_constraints(
            data, {"intent": solarpunk_case["intent"]}, {}
        )
        solarpunk_context = {
            "intent_source": "user",
            "intent_constraints": solarpunk_constraints,
        }
        self.assertTrue(
            prompt_generator.preset_matches_automatic_intent_scope(
                presets["civic_solarpunk_institutional_world"], data, solarpunk_context
            )
        )
        self.assertFalse(
            prompt_generator.preset_matches_automatic_intent_scope(
                presets["urban_heat_air_quality_record"], data, solarpunk_context
            )
        )

        for generic_intent in (
            "a generic studio portrait with neutral clothing and soft light",
            "a fantasy castle portrait with an unreadable map and cassette player",
            "documentary photo of city infrastructure maintenance",
            "solar panels and plants on a modern green roof",
            "a Black engineer repairing equipment in a future city",
            "an Indigenous adult using modern technology in a public library",
            "일반 기록관에서 오래된 종이 자료를 정리하는 성인 기록가",
            "판타지 성의 지도를 든 코스프레 인물",
        ):
            routed = prompt_generator.resolve_request_intent_constraints(
                data, {"intent": generic_intent}, {}
            )
            self.assertNotIn("worldbuilding_system", routed["domains"], generic_intent)
            self.assertFalse(routed["scoped_routes"], generic_intent)

        evidence_rows = [
            json.loads(line)
            for line in RESEARCH_EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip() and json.loads(line).get("domain") == "worldbuilding_system"
        ]
        self.assertEqual(len(evidence_rows), 54)
        self.assertEqual(len({row["source_url"] for row in evidence_rows}), 54)
        self.assertEqual({row["topic_id"] for row in evidence_rows}, extension_ids)
        catalog_ids = set(presets)
        for entries in data["slots"].values():
            catalog_ids.update(entry["id"] for entry in entries)
        for preset_id in extension_ids:
            topic_rows = [row for row in evidence_rows if row["topic_id"] == preset_id]
            self.assertEqual(len(topic_rows), 3, preset_id)
            matrix_rows = [row for row in topic_rows if "world_mechanisms" in row]
            self.assertEqual(len(matrix_rows), 1, preset_id)
            matrix = matrix_rows[0]
            self.assertGreaterEqual(len(matrix["world_mechanisms"]), 6)
            self.assertGreaterEqual(len(matrix["photographic_evidence"]), 6)
            self.assertGreaterEqual(len(matrix["boundaries"]), 3)
            self.assertTrue(set(matrix["photographic_evidence"]) <= catalog_ids)
            self.assertTrue(
                all(set(row["candidate_ids"]) <= catalog_ids for row in topic_rows),
                preset_id,
            )

        extension_text = json.dumps(extension, ensure_ascii=False).lower()
        for protected_reference in (
            "pokemon",
            "middle earth",
            "star wars",
            "scp foundation",
            "dungeons & dragons",
            "mothman",
            "bigfoot",
            "hodag",
            "wakanda",
        ):
            self.assertNotIn(protected_reference, extension_text)

    def test_cjk_worldbuilding_extension_routes_are_provenance_locked_and_scoped(self):
        data = prompt_generator.load_json(TAGS_PATH)
        data[prompt_generator.QUALITY_LAYERS_DATA_KEY] = prompt_generator.load_quality_layers(
            QUALITY_LAYERS_PATH
        )
        extension = json.loads(
            CJK_WORLDBUILDING_EXTENSION_PATH.read_text(encoding="utf-8")
        )
        extension_ids = {preset["id"] for preset in extension["presets"]}
        presets = {preset["id"]: preset for preset in data["presets"]}
        entries_by_id = {
            entry["id"]: entry
            for entries in data["slots"].values()
            for entry in entries
        }

        self.assertEqual(len(extension_ids), 20)
        self.assertEqual(len(extension["preset_families"]), 6)
        self.assertEqual(
            sum(len(entries) for entries in extension["slots"].values()),
            356,
        )
        self.assertEqual(len(extension["slots"]["subject"]), 46)
        self.assertEqual(
            set(extension["slot_applicability"]["preset_domain_overrides"]),
            extension_ids,
        )
        self.assertTrue(extension_ids <= set(presets))

        world_evidence_slots = {
            "situation_context",
            "occasion_context",
            "narrative_core",
            "capture_context",
            "procedure_step",
            "surface_material",
        }
        requested_context = {
            "intent_source": "user",
            "intent_constraints": {"domains": ["cjk_narrative_world"]},
        }
        for preset_id in sorted(extension_ids):
            preset = presets[preset_id]
            self.assertEqual(
                prompt_generator.preset_domains(preset, data),
                {"cjk_narrative_world"},
            )
            self.assertTrue(
                {"subject", "action", "location", "prop"} | world_evidence_slots
                <= set(preset["required_slots"]),
                preset_id,
            )
            self.assertGreaterEqual(len(preset["facets"]["world_mechanism"]), 6)
            self.assertFalse(
                prompt_generator.preset_matches_automatic_intent_scope(
                    preset, data, None
                )
            )
            self.assertTrue(
                prompt_generator.preset_matches_automatic_intent_scope(
                    preset, data, requested_context
                )
            )

            seen_subjects = set()
            for seed in range(1, 4):
                result = prompt_generator.generate_once(
                    data,
                    __import__("random").Random(seed),
                    preset_id,
                    ["en"],
                    False,
                    0,
                    True,
                    detail_level="detailed",
                    selection_mode="rule",
                    seed=seed,
                )
                choices = result["choices"]
                subject_id = choices["subject"]["id"]
                seen_subjects.add(subject_id)
                scene_prefix = subject_id.removesuffix("_subject")
                selected_scene_entries = [choices["subject"]]
                for slot in (
                    "action",
                    "location",
                    "prop",
                    "situation_context",
                    "occasion_context",
                ):
                    self.assertTrue(
                        choices[slot]["id"].startswith(f"{scene_prefix}_"),
                        (preset_id, seed, slot, subject_id, choices[slot]["id"]),
                    )
                    selected_scene_entries.append(choices[slot])
                self.assertTrue(
                    all(
                        "cultural_provenance" not in (entries_by_id[entry["id"]].get("facets") or {})
                        for entry in selected_scene_entries
                    )
                )

                if seed == 1:
                    # This assertion inspects the private routing profile. v4
                    # intentionally projects that winner away, so use the v3
                    # diagnostic projection for this internal data check.
                    pack = prompt_generator.build_candidate_pack(result, data, "v3")
                    self.assertTrue(world_evidence_slots <= set(pack["slots"]), preset_id)
                    self.assertEqual(
                        pack["quality_profile"]["profile_id"],
                        "cjk_narrative_world",
                        preset_id,
                    )
                    self.assertNotIn("market_origin", preset["facets"], preset_id)
                    self.assertNotIn("cultural_provenance", preset["facets"], preset_id)
                    self.assertFalse(
                        prompt_generator.CONTROL_ONLY_FACET_KEYS
                        & set(pack["quality_profile"]["facets"]),
                        preset_id,
                    )
                    self.assertLessEqual(
                        sum(
                            len(slot["candidates"])
                            for slot in pack["slots"].values()
                        ),
                        prompt_generator.CANDIDATE_PACK_TOTAL_CANDIDATE_LIMIT,
                        preset_id,
                    )
            self.assertGreaterEqual(len(seen_subjects), 2, preset_id)

        self.assertEqual(
            len(presets["cjk_spirit_underworld_bureaucracy"]["filters"]["subject"]["ids"]),
            3,
        )
        self.assertEqual(
            len(presets["cjk_vrmmo_card_liveops_world"]["filters"]["subject"]["ids"]),
            4,
        )
        self.assertEqual(
            len(
                presets["jp_mecha_kaiju_tokusatsu_disaster_state"]["filters"]["subject"]["ids"]
            ),
            4,
        )
        self.assertEqual(
            len(presets["cjk_magical_idol_virtual_media_world"]["filters"]["subject"]["ids"]),
            3,
        )

        cases = eval_semantic.load_retrieval_holdout_cases(
            CJK_WORLDBUILDING_RETRIEVAL_HOLDOUT_V1_PATH
        )
        self.assertEqual(len(cases), 100)
        self.assertEqual(len({case["id"] for case in cases}), 100)
        self.assertEqual(
            {
                preset_id
                for case in cases
                for preset_id in case["allowed_selected_presets"]
            },
            extension_ids,
        )
        self.assertTrue(all(len(case["allowed_selected_presets"]) == 1 for case in cases))
        for preset_id in extension_ids:
            self.assertEqual(
                sum(
                    preset_id in case["allowed_selected_presets"]
                    for case in cases
                ),
                5,
                preset_id,
            )

        routing_policy = prompt_generator.candidate_pack_intent_routing_policy(data)
        cjk_rules = [
            rule
            for rule in routing_policy["scoped_routes"]
            if rule["domain"] == "cjk_narrative_world"
        ]
        self.assertEqual(len(cjk_rules), 20)
        self.assertEqual({rule["preset_id"] for rule in cjk_rules}, extension_ids)
        for case in cases:
            routed = prompt_generator.resolve_request_intent_constraints(
                data, {"intent": case["intent"]}, {}
            )
            self.assertIn("cjk_narrative_world", routed["domains"], case["id"])
            self.assertEqual(
                set(routed["scoped_routes"]),
                set(case["allowed_selected_presets"]),
                case["id"],
            )

        for generic_intent in (
            "an astronomy photograph of a constellation above a radio tower",
            "ordinary climbers using the stairs of a modern office tower",
            "documentary photo of a civilian emergency response team",
            "a generic fantasy portrait in a castle",
            "a real Daoist temple conservation record",
            "a living martial-arts heritage class",
            "a real disaster shelter documentary",
            "a streamer speaking to a camera in a bedroom",
            "an idol portrait under concert lights",
            "일반 코스프레 인물이 판타지 성 앞에서 포즈를 취하는 장면",
        ):
            routed = prompt_generator.resolve_request_intent_constraints(
                data, {"intent": generic_intent}, {}
            )
            self.assertNotIn("cjk_narrative_world", routed["domains"], generic_intent)
            self.assertFalse(
                extension_ids & set(routed["scoped_routes"]),
                generic_intent,
            )

        evidence_rows = [
            json.loads(line)
            for line in RESEARCH_EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
            and json.loads(line).get("domain") == "cjk_narrative_world"
        ]
        self.assertEqual(len(evidence_rows), 60)
        self.assertEqual(len({row["source_url"] for row in evidence_rows}), 60)
        self.assertEqual({row["topic_id"] for row in evidence_rows}, extension_ids)
        catalog_ids = set(presets)
        for entries in data["slots"].values():
            catalog_ids.update(entry["id"] for entry in entries)
        for preset_id in extension_ids:
            topic_rows = [
                row for row in evidence_rows if row["topic_id"] == preset_id
            ]
            self.assertEqual(len(topic_rows), 3, preset_id)
            self.assertTrue(
                any(
                    row["source_type"].startswith("official_")
                    or "primary" in row["source_type"]
                    for row in topic_rows
                ),
                preset_id,
            )
            self.assertTrue(
                all(
                    row["schema_version"] == "photo-research-evidence/v1"
                    and row["status"] == "approved"
                    and row["reviewed_at"] == "2026-08-07"
                    and row["reuse_note"].strip()
                    for row in topic_rows
                ),
                preset_id,
            )
            matrix_rows = [row for row in topic_rows if "world_mechanisms" in row]
            self.assertEqual(len(matrix_rows), 1, preset_id)
            matrix = matrix_rows[0]
            self.assertIn("market_origin", matrix)
            self.assertIn("term_classifications", matrix)
            self.assertTrue(matrix["term_classifications"], preset_id)
            if isinstance(matrix["term_classifications"], dict):
                self.assertTrue(
                    all(matrix["term_classifications"].values()),
                    preset_id,
                )
            else:
                self.assertTrue(
                    all(
                        classification.get("term")
                        and classification.get("term_level")
                        for classification in matrix["term_classifications"]
                    ),
                    preset_id,
                )
            self.assertGreaterEqual(len(matrix["world_mechanisms"]), 5)
            self.assertGreaterEqual(len(matrix["photographic_evidence"]), 6)
            self.assertGreaterEqual(len(matrix["boundaries"]), 3)
            self.assertTrue(set(matrix["photographic_evidence"]) <= catalog_ids)
            self.assertTrue(
                all(set(row["candidate_ids"]) <= catalog_ids for row in topic_rows),
                preset_id,
            )

        extension_text = json.dumps(extension, ensure_ascii=False).lower()
        for protected_reference in (
            "omniscient reader",
            "전지적 독자",
            "주신 공간",
            "主神空间",
            "轮回者",
            "pokemon",
            "yu-gi-oh",
            "final fantasy",
            "ultraman",
            "gundam",
            "hololive",
        ):
            self.assertNotIn(protected_reference, extension_text)

    def test_character_moe_research_graph_routes_and_sparse_runtime_contract(self):
        manifest = json.loads(
            (CHARACTER_MOE_RESEARCH_DIR / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["schema_version"], "photo-research-evidence-shards/v1")
        self.assertEqual(manifest["domain"], "character_moe_grammar")
        self.assertEqual(manifest["logical_row_count"], 72)
        self.assertEqual(manifest["topic_count"], 24)
        self.assertEqual(manifest["rows_per_topic"], 3)
        self.assertEqual(len(manifest["shards"]), 6)

        rows = []
        for shard in manifest["shards"]:
            path = CHARACTER_MOE_RESEARCH_DIR / shard["file"]
            raw = path.read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), shard["sha256"])
            shard_rows = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line]
            self.assertEqual(len(shard_rows), shard["row_count"])
            self.assertEqual(
                list(dict.fromkeys(row["topic_id"] for row in shard_rows)),
                shard["topic_ids"],
            )
            rows.extend(shard_rows)
        self.assertEqual(len(rows), 72)
        self.assertEqual(len({row["id"] for row in rows}), 72)
        self.assertEqual(len({row["source_url"] for row in rows}), 72)
        self.assertTrue(all(row["domain"] == "character_moe_grammar" for row in rows))
        self.assertTrue(
            all(row["record_role"] in {"topic_matrix", "independent_source"} for row in rows)
        )

        rows_by_id = {row["id"]: row for row in rows}
        topics = sorted({row["topic_id"] for row in rows})
        self.assertEqual(len(topics), 24)
        mechanism_count = 0
        cross_source_count = 0
        matrix_candidate_memberships = []
        for topic_id in topics:
            topic_rows = [row for row in rows if row["topic_id"] == topic_id]
            self.assertEqual(len(topic_rows), 3, topic_id)
            matrices = [row for row in topic_rows if row["record_role"] == "topic_matrix"]
            supports = [row for row in topic_rows if row["record_role"] == "independent_source"]
            self.assertEqual(len(matrices), 1, topic_id)
            self.assertEqual(len(supports), 2, topic_id)
            matrix = matrices[0]
            self.assertEqual(set(matrix["synthesis_evidence_ids"]), {row["id"] for row in supports})
            self.assertEqual(set(matrix["candidate_definitions"]), set(matrix["candidate_ids"]))
            self.assertEqual(
                set(matrix["photographic_evidence_definitions"]),
                set(matrix["photographic_evidence"]),
            )
            self.assertEqual(
                [item["mechanism"] for item in matrix["mechanism_provenance"]],
                matrix["mechanisms"],
            )
            candidate_ids = set(matrix["candidate_ids"])
            matrix_candidate_memberships.extend((candidate_id, topic_id) for candidate_id in candidate_ids)
            self.assertTrue(
                all(set(row["candidate_ids"]) <= candidate_ids for row in supports),
                topic_id,
            )
            mechanism_count += len(matrix["mechanisms"])
            for provenance in matrix["mechanism_provenance"]:
                evidence_ids = provenance["evidence_ids"]
                self.assertTrue(evidence_ids, (topic_id, provenance["mechanism"]))
                self.assertTrue(set(evidence_ids) <= set(rows_by_id), topic_id)
                self.assertTrue(
                    all(rows_by_id[evidence_id]["topic_id"] == topic_id for evidence_id in evidence_ids),
                    topic_id,
                )
                if provenance["provenance"] == "cross_source_synthesis":
                    cross_source_count += 1
                    self.assertGreaterEqual(len(set(evidence_ids)), 2, topic_id)
                    self.assertGreaterEqual(
                        len({rows_by_id[evidence_id]["source_url"] for evidence_id in evidence_ids}),
                        2,
                        topic_id,
                    )
        self.assertEqual(mechanism_count, 194)
        self.assertEqual(cross_source_count, 53)
        self.assertEqual(len(matrix_candidate_memberships), 186)
        self.assertEqual(len({candidate_id for candidate_id, _topic in matrix_candidate_memberships}), 184)

        crosswalk = json.loads(CHARACTER_MOE_CROSSWALK_PATH.read_text(encoding="utf-8"))
        self.assertEqual(crosswalk["domain"], "character_moe_grammar")
        self.assertEqual(len(crosswalk["topics"]), 24)
        self.assertEqual(len(crosswalk["families"]), 8)
        self.assertEqual({topic["topic_id"] for topic in crosswalk["topics"]}, set(topics))
        self.assertEqual(len({topic["route_id"] for topic in crosswalk["topics"]}), 24)

        extension = json.loads(CHARACTER_MOE_EXTENSION_PATH.read_text(encoding="utf-8"))
        graph = extension["character_mechanism_graph"]
        self.assertEqual(graph["schema_version"], prompt_generator.CHARACTER_MECHANISM_GRAPH_SCHEMA)
        self.assertEqual(graph["priority_order"], crosswalk["priority_order"])
        self.assertEqual(graph["max_support_cues"], 2)
        self.assertEqual(len(graph["families"]), 8)
        self.assertEqual(len(graph["runtime_nodes"]), 184)
        self.assertEqual(len(graph["compatibility_edges"]), 24)
        self.assertTrue(graph["guard_rules"])
        self.assertEqual(len(extension["presets"]), 24)

        node_index = {node["id"]: node for node in graph["runtime_nodes"]}
        self.assertEqual(set(node_index), {candidate_id for candidate_id, _topic in matrix_candidate_memberships})
        for candidate_id, topic_id in matrix_candidate_memberships:
            self.assertIn(topic_id, node_index[candidate_id]["topic_ids"])
        self.assertEqual(
            {preset["id"] for preset in extension["presets"]},
            {topic["route_id"] for topic in crosswalk["topics"]},
        )

        data = prompt_generator.load_json(TAGS_PATH)
        data[prompt_generator.QUALITY_LAYERS_DATA_KEY] = prompt_generator.load_quality_layers(
            QUALITY_LAYERS_PATH
        )
        presets = {preset["id"]: preset for preset in data["presets"]}
        routing_policy = prompt_generator.candidate_pack_intent_routing_policy(data)
        character_routes = [
            rule
            for rule in routing_policy["scoped_routes"]
            if rule["domain"] == "character_moe_grammar"
        ]
        self.assertEqual(len(character_routes), 24)
        self.assertEqual(
            {rule["preset_id"] for rule in character_routes},
            {topic["route_id"] for topic in crosswalk["topics"]},
        )

        for topic in crosswalk["topics"]:
            preset_id = topic["route_id"]
            preset = presets[preset_id]
            self.assertEqual(prompt_generator.preset_domains(preset, data), {"character_moe_grammar"})
            blueprints = prompt_generator.render_contract_resolved_scene_blueprints(data, preset)
            expected_blueprint_count = {
                "character_attribute_composition_scene": 7,
                # Four frozen research scenes plus one natural-language-only
                # peer-liking scene. Direct preset replay still cycles over
                # only the four frozen research scenes below.
                "character_gap_contrast_scene": 5,
            }.get(preset_id, 4)
            self.assertEqual(
                len(blueprints),
                expected_blueprint_count,
                preset_id,
            )
            for blueprint in blueprints:
                visual_atoms = " ".join(
                    str(blueprint.get(field) or "")
                    for field in ("subject", "subject_ko", "action", "action_ko", "location", "location_ko", "prop", "prop_ko")
                ).lower()
                for control_phrase in ("provenance", "market term", "market label", "nonvisual"):
                    self.assertNotIn(control_phrase, visual_atoms, (preset_id, blueprint["id"]))
            self.assertGreaterEqual(
                len({function for blueprint in blueprints for function in blueprint["scene_functions"]}),
                2,
                preset_id,
            )
            self.assertLessEqual(sum(bool(item["static_portrait"]) for item in blueprints), 1)
            direct_blueprints = [
                blueprint
                for blueprint in blueprints
                if blueprint.get("natural_moe_default_only") is not True
            ]
            self.assertEqual(
                {
                    prompt_generator.candidate_pack_select_scene_blueprint(
                        {"provenance": {"seed": seed}}, preset, blueprints
                    )["id"]
                    for seed in range(1, 5)
                },
                {blueprint["id"] for blueprint in direct_blueprints},
                preset_id,
            )
            result = prompt_generator.generate_once(
                data,
                __import__("random").Random(810000 + topic["ordinal"]),
                preset_id,
                ["en"],
                True,
                12,
                True,
                detail_level="detailed",
                selection_mode="rule",
                seed=810000 + topic["ordinal"],
            )
            rendered_prompt = prompt_generator.rendered_prompt_blob(result)
            for control_phrase in (
                "market term",
                "market label",
                "term routing",
                "nonvisual",
                "national-style shorthand",
                "provenance",
            ):
                self.assertNotIn(control_phrase, rendered_prompt, preset_id)
            pack = prompt_generator.build_candidate_pack(result, data)
            grammar = pack["character_grammar"]
            self.assertTrue(grammar["enabled"], preset_id)
            self.assertTrue(grammar["valid"], preset_id)
            self.assertEqual(pack["contract_version"], "photo-candidate-pack/v4")
            self.assertNotIn("domain", grammar)
            self.assertNotIn("topic_id", grammar)
            self.assertNotIn("family_id", grammar)
            for private_key in (
                "runtime_anchor_ids",
                "primary_runtime_id",
                "policy_ids",
                "policies",
                "applicable_guard_rules",
                "audience_familiarity",
                "market_origin",
                "compatible_edge_ids",
                "character_evidence_types",
            ):
                self.assertNotIn(private_key, grammar, (preset_id, private_key))
            self.assertGreaterEqual(len(grammar["runtime_nodes"]), 1)
            self.assertLessEqual(len(grammar["runtime_nodes"]), 3)
            self.assertEqual(sum(node["role"] == "primary" for node in grammar["runtime_nodes"]), 1)
            expected_visual_evidence = (
                set(topic["required_evidence_types"])
                - prompt_generator.PRIVATE_CHARACTER_EVIDENCE_TYPES
            )
            self.assertTrue(
                expected_visual_evidence
                <= set(grammar["required_visual_evidence_types"])
            )
            self.assertTrue(
                set(grammar["required_visual_evidence_types"])
                <= set(grammar["visual_evidence_types"])
            )
            self.assertEqual(
                grammar["composition_constraints"],
                {
                    "explicit_adult_original_subject": "required",
                    "observable_evidence": "required",
                    "appearance_inference_from_route": "forbidden",
                    "protected_identity_replication": "forbidden",
                },
            )
            selected_scene = pack["render_contract"]["selected_scene"]
            self.assertEqual(
                set(selected_scene["visual_evidence_types"]),
                set(grammar["visual_evidence_types"]),
            )
            for private_key in (
                "runtime_ids",
                "primary_runtime_id",
                "audience_familiarity",
                "market_origin",
                "selection_source",
                "available_blueprint_count",
                "available_blueprint_ids",
            ):
                self.assertNotIn(private_key, selected_scene, (preset_id, private_key))
            self.assertFalse(
                prompt_generator.CONTROL_ONLY_FACET_KEYS
                & set(pack["quality_profile"]["facets"]),
                preset_id,
            )
            serialized_pack = json.dumps(pack, ensure_ascii=False).lower()
            self.assertNotIn("market_label_nonvisual", serialized_pack, preset_id)
            self.assertNotIn("moe_review", serialized_pack, preset_id)
            self.assertEqual(pack["quality_profile"]["profile_id"], "authorial")
            self.assertFalse(pack["quality_profile"]["source_profile_exposed"])
            self.assertNotIn("character_moe_grammar", serialized_pack)
            legacy_pack = prompt_generator.build_candidate_pack(result, data, "v2")
            self.assertEqual(legacy_pack["contract_version"], "photo-candidate-pack/v2")
            self.assertEqual(legacy_pack["character_grammar"]["topic_id"], topic["topic_id"])
            self.assertEqual(legacy_pack["character_grammar"]["family_id"], topic["family_id"])
            self.assertEqual(
                legacy_pack["quality_profile"]["profile_id"],
                "character_moe_grammar",
            )
            self.assertFalse(pack["evidence_budget"]["enabled"])
            candidate_total = len(pack["presets"]) + sum(
                len(slot_payload["candidates"]) for slot_payload in pack["slots"].values()
            )
            self.assertLessEqual(candidate_total, prompt_generator.CANDIDATE_PACK_TOTAL_CANDIDATE_LIMIT)
            self.assertEqual(
                pack["safety"],
                {
                    "mode": "automatic",
                    "evaluation_requested": False,
                    "status": "pass",
                    "requires_user_approval": False,
                    "items": [],
                },
            )

        cases = eval_semantic.load_retrieval_holdout_cases(
            CHARACTER_MOE_RETRIEVAL_CONTRACT_V1_PATH
        )
        self.assertEqual(len(cases), 96)
        self.assertEqual(len({case["id"] for case in cases}), 96)
        self.assertEqual(
            {preset_id for case in cases for preset_id in case["allowed_selected_presets"]},
            {topic["route_id"] for topic in crosswalk["topics"]},
        )
        for case in cases:
            routed = prompt_generator.resolve_request_intent_constraints(
                data, {"intent": case["intent"]}, {}
            )
            self.assertIn("character_moe_grammar", routed["domains"], case["id"])
            self.assertEqual(set(routed["scoped_routes"]), set(case["allowed_selected_presets"]), case["id"])

        for generic_intent in (
            "an ordinary cute adult portrait in soft window light",
            "a documentary photograph of an actual cat playing with a toy",
            "a real cultural festival costume documentation project",
            "a generic streamer speaking to a camera in a bedroom",
            "a polished idol concert portrait under stage lights",
            "부드러운 조명의 평범한 성인 인물 사진",
            "relationship chemistry between two adult coworkers",
            "pose and proxemics in an editorial office portrait",
            "hair silhouette and state change after rain",
            "signature object bond shown through use and care",
        ):
            routed = prompt_generator.resolve_request_intent_constraints(
                data, {"intent": generic_intent}, {}
            )
            self.assertNotIn("character_moe_grammar", routed["domains"], generic_intent)
            self.assertFalse(
                {topic["route_id"] for topic in crosswalk["topics"]}
                & set(routed["scoped_routes"]),
                generic_intent,
            )

        quality_cases = [
            json.loads(line)
            for line in CHARACTER_MOE_QUALITY_HOLDOUT_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(quality_cases), 8)
        self.assertEqual(
            {case["family_id"] for case in quality_cases},
            {family["id"] for family in crosswalk["families"]},
        )
        visual_review = json.loads(
            CHARACTER_MOE_QUALITY_VISUAL_REVIEW_PATH.read_text(encoding="utf-8")
        )
        visual_summary = eval_semantic.summarize_visual_review(
            CHARACTER_MOE_QUALITY_VISUAL_REVIEW_PATH
        )["visual_review"]
        self.assertEqual(visual_review["schema_version"], "photo-visual-review/v1")
        self.assertEqual(visual_review["cross_case_review"]["outcome"], "pass")
        self.assertEqual(visual_review["cross_case_review"]["family_count"], 8)
        self.assertEqual(visual_review["cross_case_review"]["distinct_event_count"], 8)
        self.assertEqual(
            visual_review["cross_case_review"]["studio_costume_convergence"],
            "none",
        )
        self.assertEqual(visual_summary["case_count"], 8)
        self.assertEqual(visual_summary["failed_case_count"], 0)
        self.assertEqual(visual_summary["contract_failure_count"], 0)
        self.assertEqual(visual_summary["failed_review_focus_result_count"], 0)
        self.assertTrue(visual_summary["passed"])
        self.assertEqual(
            {case["case"] for case in visual_review["cases"]},
            {case["case_id"] for case in quality_cases},
        )
        expected_quality_scene_ids = {
            "character_trait_gap_workshop_reveal": "gap_moe_contrast_structure_atomic_01",
            "character_relationship_reciprocal_rescue": "relationship_chemistry_grammar_atomic_01",
            "character_expression_confusion_translation": "expression_manga_symbol_translation_atomic_01",
            "character_prop_repair_bond": "signature_prop_character_bond_atomic_01",
            "character_hair_state_continuity_after_rain": "hair_silhouette_state_change_atomic_01",
            "character_creepy_cute_protective_encounter": "creepy_cute_monster_moe_atomic_01",
            "character_transformation_recovery_threshold": "transformation_heroine_double_life_atomic_01",
            "character_adult_androgynous_care_competence": "adult_masculine_androgynous_moe_atomic_01",
        }
        for case in quality_cases:
            preset = presets[case["preset_id"]]
            blueprints = prompt_generator.render_contract_resolved_scene_blueprints(data, preset)
            matching = [
                blueprint
                for blueprint in blueprints
                if case["target_scene_function"] in blueprint["scene_functions"]
            ]
            self.assertEqual(len(matching), 1, case["case_id"])
            self.assertEqual(matching[0]["id"], expected_quality_scene_ids[case["case_id"]])
            selected = prompt_generator.candidate_pack_select_scene_blueprint(
                {
                    "provenance": {
                        "seed": case["seed"],
                        "requested_scene_function": case["target_scene_function"],
                    }
                },
                preset,
                blueprints,
            )
            self.assertEqual(selected["id"], expected_quality_scene_ids[case["case_id"]])
            self.assertEqual(selected["selection_source"], "requested_scene_function")
            wrapper_pack = self.run_wrapper(
                "--preset",
                case["preset_id"],
                "--selection-mode",
                "rule",
                "--seed",
                str(case["seed"]),
                "--scene-function",
                case["target_scene_function"],
                "--emit-candidate-pack",
                "--candidate-pack-version",
                "v3",
            )[0]
            self.assertEqual(
                wrapper_pack["render_contract"]["selected_scene"]["blueprint_id"],
                expected_quality_scene_ids[case["case_id"]],
            )
            self.assertNotIn(
                "selection_source",
                wrapper_pack["render_contract"]["selected_scene"],
            )

        extension_text = (
            CHARACTER_MOE_EXTENSION_PATH.read_text(encoding="utf-8")
            + SCENE_EXPRESSION_CHARACTER_MOE_PATH.read_text(encoding="utf-8")
        ).lower()
        for protected_reference in (
            "pokemon",
            "hololive",
            "hatsune miku",
            "gundam",
            "sailor moon",
            "genshin impact",
            "blue archive",
            "uma musume",
        ):
            self.assertNotIn(protected_reference, extension_text)

    def test_scene_expression_pilots_are_diverse_sparse_and_fail_closed(self):
        data = prompt_generator.load_json(TAGS_PATH)
        data[prompt_generator.QUALITY_LAYERS_DATA_KEY] = prompt_generator.load_quality_layers(
            QUALITY_LAYERS_PATH
        )
        extension = json.loads(SCENE_EXPRESSION_EXTENSION_PATH.read_text(encoding="utf-8"))
        self.assertEqual(extension["schema_version"], prompt_generator.RESEARCH_EXTENSION_SCHEMA)

        baseline = json.loads(SCENE_EXPRESSION_BASELINE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(baseline["summary"]["route_count"], 88)
        self.assertEqual(baseline["summary"]["fail_count"], 88)
        holdout = [
            json.loads(line)
            for line in SCENE_QUALITY_HOLDOUT_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(holdout), 12)
        self.assertEqual(len({case["case_id"] for case in holdout}), 12)
        self.assertEqual(
            {source: sum(case["source_extension"] == source for case in holdout) for source in {case["source_extension"] for case in holdout}},
            {"research": 3, "subculture": 3, "worldbuilding": 3, "cjk_worldbuilding": 3},
        )

        review = json.loads(SCENE_QUALITY_VISUAL_REVIEW_PATH.read_text(encoding="utf-8"))
        review_summary = eval_semantic.summarize_visual_review(
            SCENE_QUALITY_VISUAL_REVIEW_PATH
        )["visual_review"]
        self.assertEqual(review["schema_version"], "photo-visual-review/v1")
        self.assertEqual(review_summary["case_count"], 12)
        self.assertEqual(review_summary["failed_case_count"], 0)
        self.assertEqual(review_summary["failed_review_focus_result_count"], 0)
        self.assertTrue(review_summary["passed"])
        self.assertEqual(
            {case["case"] for case in review["cases"]},
            {case["case_id"] for case in holdout},
        )

        pilots = {
            "cjk_ability_academy_lineage_system": "rival_rescue",
            "cjk_status_system_quest_world": "cost_revelation",
            "cjk_villainess_otome_aristocratic_world": "betrothal_decision",
        }
        presets = {preset["id"]: preset for preset in data["presets"]}
        for preset_id, expected_non_operational_scene in pilots.items():
            preset = presets[preset_id]
            blueprints = prompt_generator.render_contract_resolved_scene_blueprints(data, preset)
            self.assertEqual(len(blueprints), 4)
            self.assertIn(expected_non_operational_scene, {item["id"] for item in blueprints})
            self.assertTrue(preset["render_contract"]["topic_intents"])
            scene_tags = set()
            scene_functions = set()
            operational_hits = 0
            documentary_medium_hits = 0
            documentary_genre_hits = 0
            for seed in range(1, 65):
                result = prompt_generator.generate_once(
                    data,
                    __import__("random").Random(seed),
                    preset_id,
                    ["en"],
                    False,
                    0,
                    True,
                    detail_level="detailed",
                    selection_mode="rule",
                    seed=seed,
                )
                pack = prompt_generator.build_candidate_pack(result, data, "v3")
                self.assertTrue(pack["scene_contract"]["enabled"])
                self.assertTrue(pack["render_contract"]["enabled"])
                self.assertEqual(pack["evidence_budget"]["minimum_chosen"], 1)
                self.assertEqual(pack["evidence_budget"]["maximum_chosen"], 2)
                self.assertEqual(len(pack["mandatory_intents"]), 1)
                group = next(
                    group
                    for group in pack["scene_contract"]["groups"]
                    if group.get("source") == "selected_render_blueprint"
                )
                self.assertEqual(set(group["required_slots"]), {"subject", "action", "location", "prop"})
                scene_tags.add(group["group"])
                scene_functions.update(pack["render_contract"]["selected_scene"]["scene_functions"])
                operational_hits += bool(pack["render_contract"]["selected_scene"]["operational"])
                documentary_medium_hits += result["choices"]["medium"]["id"] == "documentary_photo"
                documentary_genre_hits += result["choices"]["genre"]["id"] == "documentary"
            self.assertEqual(len(scene_tags), 4, preset_id)
            self.assertGreaterEqual(len(scene_functions), 3, preset_id)
            self.assertLessEqual(operational_hits, 32, preset_id)
            self.assertLessEqual(documentary_medium_hits, 16, preset_id)
            self.assertLessEqual(documentary_genre_hits, 16, preset_id)

        result = prompt_generator.generate_once(
            data,
            __import__("random").Random(3),
            "cjk_ability_academy_lineage_system",
            ["en"],
            True,
            12,
            True,
            detail_level="detailed",
            selection_mode="rule",
            seed=3,
        )
        pack = prompt_generator.build_candidate_pack(result, data, "v3")
        group = next(
            group
            for group in pack["scene_contract"]["groups"]
            if group.get("source") == "selected_render_blueprint"
        )
        chosen = ["preset:cjk_ability_academy_lineage_system"]
        prompt = ". ".join(
            [
                "Cinematic original adult ability academy practical trial with rivalry, one visible safety consequence, and no readable insignia",
                *(group["slots"][slot]["label_en"] for slot in group["required_slots"]),
            ]
        ) + "."
        valid = audit_composed_prompt.audit_composed_prompt(
            pack,
            {
                "pack_id": pack["pack_id"],
                "prompt_en": prompt,
                "negative_en": pack["negative_en"],
                "chosen_candidate_ids": chosen,
                "composer": "agent",
            },
        )
        valid_checks = {failure["check"] for failure in valid["failures"]}
        self.assertNotIn("mandatory_intent", valid_checks)
        self.assertNotIn("atomic_scene_contract", valid_checks)
        self.assertNotIn("evidence_budget", valid_checks)

        over_budget = copy.deepcopy(chosen)
        for slot in pack["evidence_budget"]["world_clue_slots"]:
            if slot == "prop":
                continue
            selected = pack["slots"].get(slot, {}).get("selected")
            if selected and selected not in over_budget:
                over_budget.append(selected)
        over_budget_audit = audit_composed_prompt.audit_composed_prompt(
            pack,
            {
                "pack_id": pack["pack_id"],
                "prompt_en": prompt,
                "negative_en": pack["negative_en"],
                "chosen_candidate_ids": over_budget,
                "composer": "agent",
            },
        )
        self.assertIn("evidence_budget", {failure["check"] for failure in over_budget_audit["failures"]})

        cross_scene_subject = pack["slots"]["subject"]["candidates"][0]["id"]
        cross_scene = list(chosen)
        cross_scene.append(cross_scene_subject)
        cross_scene_audit = audit_composed_prompt.audit_composed_prompt(
            pack,
            {
                "pack_id": pack["pack_id"],
                "prompt_en": prompt,
                "negative_en": pack["negative_en"],
                "chosen_candidate_ids": cross_scene,
                "composer": "agent",
            },
        )
        self.assertIn("atomic_scene_contract", {failure["check"] for failure in cross_scene_audit["failures"]})

    def test_all_research_routes_have_materialized_scene_expression_contracts(self):
        inventory = audit_scene_expression.build_inventory(
            "2026-08-07T00:00:00+09:00",
            current=True,
        )
        self.assertEqual(inventory["summary"]["route_count"], 112)
        self.assertEqual(inventory["summary"]["pass_count"], 112)
        self.assertEqual(inventory["summary"]["fail_count"], 0)

        data = prompt_generator.load_json(TAGS_PATH)
        data[prompt_generator.QUALITY_LAYERS_DATA_KEY] = prompt_generator.load_quality_layers(
            QUALITY_LAYERS_PATH
        )
        source_specs = (
            (RESEARCH_EXTENSION_PATH, "evidence_documentary"),
            (SUBCULTURE_EXTENSION_PATH, "specialty_practice"),
            (WORLDBUILDING_EXTENSION_PATH, "narrative_world"),
            (CJK_WORLDBUILDING_EXTENSION_PATH, "narrative_world"),
            (CHARACTER_MOE_EXTENSION_PATH, "character_grammar"),
        )
        preset_ids: list[tuple[str, str]] = []
        for path, route_type in source_specs:
            source = json.loads(path.read_text(encoding="utf-8"))
            preset_ids.extend((preset["id"], route_type) for preset in source["presets"])
        self.assertEqual(len(preset_ids), 112)

        presets = {preset["id"]: preset for preset in data["presets"]}
        evidence_rows = [
            json.loads(line)
            for line in RESEARCH_EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        evidence_route_ids = {
            str(candidate_id)
            for row in evidence_rows
            for candidate_id in [row.get("topic_id"), *(row.get("candidate_ids") or [])]
            if str(candidate_id or "")
        }
        for shard in json.loads(
            (CHARACTER_MOE_RESEARCH_DIR / "manifest.json").read_text(encoding="utf-8")
        )["shards"]:
            for line in (CHARACTER_MOE_RESEARCH_DIR / shard["file"]).read_text(
                encoding="utf-8"
            ).splitlines():
                row = json.loads(line)
                evidence_route_ids.add(str(row.get("topic_id") or ""))
                evidence_route_ids.update(str(item) for item in row.get("candidate_ids") or [])
        for preset_id, route_type in preset_ids:
            preset = presets[preset_id]
            self.assertIsInstance(preset.get("render_contract"), dict, preset_id)
            if route_type == "character_grammar":
                grammar = preset["render_contract"].get("character_grammar") or {}
                self.assertIn(grammar.get("topic_id"), evidence_route_ids)
                # Character market/taxonomy labels stay nonvisual.  Their
                # executable contract is the typed topic plus sparse visual
                # atoms, not a generic topic phrase forced into the prompt.
                self.assertFalse(preset["render_contract"].get("topic_intents"), preset_id)
            else:
                self.assertIn(preset_id, evidence_route_ids)
                self.assertTrue(preset["render_contract"].get("topic_intents"), preset_id)
            blueprints = prompt_generator.render_contract_resolved_scene_blueprints(data, preset)
            expected_minimum = 4 if route_type == "narrative_world" else 3
            self.assertGreaterEqual(len(blueprints), expected_minimum, preset_id)
            self.assertTrue(
                all(
                    len(set(blueprint["diegetic_visual_provenance"])) == 1
                    for blueprint in blueprints
                ),
                preset_id,
            )
            direct_blueprints = [
                blueprint
                for blueprint in blueprints
                if blueprint.get("natural_moe_default_only") is not True
            ]
            selected_ids = {
                prompt_generator.candidate_pack_select_scene_blueprint(
                    {"provenance": {"seed": seed}},
                    preset,
                    blueprints,
                )["id"]
                for seed in range(1, 65)
            }
            self.assertEqual(
                selected_ids,
                {blueprint["id"] for blueprint in direct_blueprints},
                preset_id,
            )

        for scene_path in (
            SCENE_EXPRESSION_EXTENSION_PATH,
            SCENE_EXPRESSION_WORLDBUILDING_PATH,
            SCENE_EXPRESSION_CJK_PATH,
            SCENE_EXPRESSION_CHARACTER_MOE_PATH,
        ):
            scene_text = scene_path.read_text(encoding="utf-8").lower()
            for protected_reference in (
                "omniscient reader",
                "전지적 독자",
                "주신 공간",
                "主神空间",
                "轮回者",
                "pokemon",
                "yu-gi-oh",
                "final fantasy",
                "ultraman",
                "gundam",
                "hololive",
            ):
                self.assertNotIn(protected_reference, scene_text, scene_path.name)

    def test_every_research_route_candidate_pack_selects_one_fail_closed_scene(self):
        data = prompt_generator.load_json(TAGS_PATH)
        data[prompt_generator.QUALITY_LAYERS_DATA_KEY] = prompt_generator.load_quality_layers(
            QUALITY_LAYERS_PATH
        )
        preset_ids = []
        for path in (
            RESEARCH_EXTENSION_PATH,
            SUBCULTURE_EXTENSION_PATH,
            WORLDBUILDING_EXTENSION_PATH,
            CJK_WORLDBUILDING_EXTENSION_PATH,
            CHARACTER_MOE_EXTENSION_PATH,
        ):
            source = json.loads(path.read_text(encoding="utf-8"))
            preset_ids.extend(preset["id"] for preset in source["presets"])

        for index, preset_id in enumerate(preset_ids, start=1):
            result = prompt_generator.generate_once(
                data,
                __import__("random").Random(920000 + index),
                preset_id,
                ["en"],
                True,
                12,
                True,
                detail_level="detailed",
                selection_mode="rule",
                seed=920000 + index,
            )
            pack = prompt_generator.build_candidate_pack(result, data, "v3")
            self.assertTrue(pack["scene_contract"]["enabled"], preset_id)
            self.assertTrue(pack["render_contract"]["enabled"], preset_id)
            self.assertEqual(pack["render_contract"]["evidence_route_id"], preset_id)
            is_character_route = pack["character_grammar"]["enabled"]
            if is_character_route:
                self.assertFalse(pack["render_contract"]["topic_intents"], preset_id)
                self.assertFalse(pack["evidence_budget"]["enabled"], preset_id)
                self.assertTrue(pack["character_grammar"]["valid"], preset_id)
                self.assertGreaterEqual(len(pack["character_grammar"]["runtime_nodes"]), 1)
                self.assertLessEqual(len(pack["character_grammar"]["runtime_nodes"]), 3)
            else:
                self.assertTrue(pack["render_contract"]["topic_intents"], preset_id)
                self.assertTrue(pack["evidence_budget"]["enabled"], preset_id)
            self.assertEqual(
                len(set(pack["render_contract"]["selected_scene"]["diegetic_visual_provenance"])),
                1,
                preset_id,
            )
            group = next(
                group
                for group in pack["scene_contract"]["groups"]
                if group.get("source") == "selected_render_blueprint"
            )
            self.assertEqual(set(group["required_slots"]), {"subject", "action", "location", "prop"})
            chosen = [f"preset:{preset_id}"]
            prompt_parts = []
            if pack["render_contract"]["topic_intents"]:
                prompt_parts.append(
                    pack["render_contract"]["topic_intents"][0]["audit_terms"][0]
                )
            for slot in group["required_slots"]:
                prompt_parts.append(group["slots"][slot]["label_en"])
            prompt = ". ".join(prompt_parts) + ". Shared light, foreground occlusion, creased material, caught before the consequence settles."
            audit = audit_composed_prompt.audit_composed_prompt(
                pack,
                {
                    "pack_id": pack["pack_id"],
                    "prompt_en": prompt,
                    "negative_en": pack["negative_en"],
                    "chosen_candidate_ids": chosen,
                    "composer": "agent",
                },
            )
            self.assertEqual(audit["status"], "pass", (preset_id, audit))
            candidate_total = len(pack["presets"]) + sum(
                len(slot_payload["candidates"])
                for slot_payload in pack["slots"].values()
            )
            self.assertLessEqual(
                candidate_total,
                prompt_generator.CANDIDATE_PACK_TOTAL_CANDIDATE_LIMIT,
                preset_id,
            )
            self.assertEqual(pack["pack_id"], audit_composed_prompt.computed_pack_id(pack), preset_id)
            self.assertEqual(
                pack["safety"],
                {
                    "mode": "automatic",
                    "evaluation_requested": False,
                    "status": "pass",
                    "requires_user_approval": False,
                    "items": [],
                },
                preset_id,
            )

    def test_candidate_pack_output_file_preserves_canonical_integrity(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "candidate-pack.json"
            stream = io.StringIO()
            with redirect_stdout(stream):
                exit_code = generate_photo_prompt.main(
                    [
                        "--preset",
                        "cjk_status_system_quest_world",
                        "--selection-mode",
                        "rule",
                        "--seed",
                        "3",
                        "--emit-candidate-pack",
                        "--output-file",
                        str(output_path),
                    ]
                )
            self.assertEqual(exit_code, 0)
            self.assertEqual(stream.getvalue(), "")
            raw = output_path.read_bytes()
            self.assertTrue(raw.endswith(b"\n"))
            pack = json.loads(raw)[0]
            self.assertEqual(pack["pack_id"], audit_composed_prompt.computed_pack_id(pack))

    def test_subculture_extension_override_contract_rejects_unknown_metadata(self):
        raw_tags = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        invalid = {
            "schema_version": prompt_generator.RESEARCH_EXTENSION_SCHEMA,
            "existing_preset_metadata_overrides": {
                raw_tags["presets"][0]["id"]: {"filters": {}}
            },
        }
        with self.assertRaisesRegex(ValueError, "unsupported keys"):
            prompt_generator.merge_research_extension(raw_tags, invalid)

    def test_research_presets_resist_legacy_bleed_and_misleading_intent(self):
        data = prompt_generator.load_json(TAGS_PATH)
        presets = {preset["id"]: preset for preset in data["presets"]}

        sports_wire = presets["sports_action_wire"]
        self.assertEqual(
            sports_wire["filters"]["subject"]["ids"],
            ["athlete_runner"],
        )
        self.assertEqual(
            sports_wire["filters"]["action"]["ids"],
            ["sprinting_track", "frozen_action"],
        )
        for preset_id in (
            "swimmer_lane_splash",
            "combat_sport_sweat",
            "track_sprint_blur",
            "equestrian_dust",
        ):
            preset_text = json.dumps(presets[preset_id], ensure_ascii=False).lower()
            self.assertNotIn("chalk", preset_text)

        pollinator = presets["pollinator_flower_visit_transect"]
        picked = {}
        contract = prompt_generator.make_generation_contract(data, pollinator, picked)
        subject = prompt_generator.choose_slot(
            "subject",
            data,
            pollinator,
            __import__("random").Random(7),
            picked,
            semantic_context=None,
            generation_contract=contract,
        )
        self.assertEqual(subject["id"], "pollinator_flower_visit_event")

        natural_markers = {
            "biological_soil_crust_patch": "biocrust",
            "streambank_erosion_deposition_profile": "geomorphology",
            "cold_surface_condensation_boundary": "condensation_process",
            "seed_radicle_emergence_macro": "germination",
            "freeze_thaw_soil_polygon_patch": "freeze_thaw",
        }
        for seed in range(1, 11):
            pack = self.run_wrapper(
                "--preset",
                "natural_process_trace_documentary",
                "--selection-mode",
                "rule",
                "--seed",
                str(seed),
                "--emit-candidate-pack",
                "--candidate-pack-version",
                "v3",
            )[0]
            selected = {
                slot: next(
                    candidate
                    for candidate in pack["slots"][slot].get("candidates", [])
                    if candidate.get("selected_by_sampler")
                )
                for slot in ("subject", "action", "location", "surface_material")
            }
            marker = natural_markers[selected["subject"]["entry_id"]]
            for slot in ("action", "location", "surface_material"):
                self.assertIn(marker, selected[slot].get("tags", []), (seed, slot, selected[slot]))

    def test_compact_quality_gate_summary_keeps_gate_and_check_counts(self):
        summary = {
            "quality_gate": {"passed": True, "legacy_passed": True},
            "golden_modes": [
                {"mode": "rule", "average_coverage": 1.0, "quality_fail_count": 0, "results": [1, 2]},
            ],
            "generalization_check": {"case_count": 60, "failed_case_count": 0, "results": [1]},
            "retrieval_holdout_v4_check": {"case_count": 22, "failed_case_count": 0, "results": [1]},
        }
        compact = eval_semantic.compact_quality_gate_summary(summary)
        self.assertEqual(compact["quality_gate"]["passed"], True)
        self.assertEqual(compact["checks"]["generalization_check"]["case_count"], 60)
        self.assertEqual(compact["checks"]["retrieval_holdout_v4_check"]["failed_case_count"], 0)
        self.assertNotIn("results", compact["checks"]["generalization_check"])
        with tempfile.TemporaryDirectory() as tmp:
            report_path = Path(tmp) / "quality-report.json"
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                eval_semantic.emit_evaluation_summary(
                    summary,
                    summary_only=True,
                    report_json=report_path,
                )
            printed = json.loads(stdout.getvalue())
            report = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertNotIn("results", printed["checks"]["generalization_check"])
        self.assertEqual(report["generalization_check"]["results"], [1])


if __name__ == "__main__":
    unittest.main()
