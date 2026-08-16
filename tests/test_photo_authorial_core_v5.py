from __future__ import annotations

import copy
import json
import random
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
WRAPPER_PATH = SCRIPT_DIR / "generate_photo_prompt.py"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import audit_composed_prompt  # noqa: E402
import prompt_generator  # noqa: E402


class PhotoAuthorialCoreV5Tests(unittest.TestCase):
    @staticmethod
    def core(
        source_request: str,
        *,
        interpreted_intent: str = (
            "A quiet rainlit still life centered on blue porcelain and restrained domestic calm"
        ),
        subject: str = "one blue porcelain teacup",
        setting: str = "a quiet rainlit kitchen counter",
        event: str = "steam rises while window reflections drift across the glaze",
        visual_priorities: tuple[str, ...] = (
            "blue porcelain glaze",
            "rainlit window reflections",
            "delicate rising steam",
        ),
        baseline_prompt_en: str = (
            "A blue porcelain teacup rests on a dark kitchen counter while delicate rising "
            "steam catches rainlit window reflections, with a quiet domestic mood, restrained "
            "slate colors, shallow focus, and tactile glaze detail."
        ),
        definitions: tuple[dict, ...] = (),
        interpretations: tuple[dict, ...] = (),
        exclusions: tuple[str, ...] = ("people", "bright sunlight"),
    ) -> dict:
        return {
            "contract_version": "photo-authorial-core/v1",
            "provenance": "agent_prepack",
            "source_request": source_request,
            "interpreted_intent": interpreted_intent,
            "subject": subject,
            "setting": setting,
            "event": event,
            "visual_priorities": list(visual_priorities),
            "baseline_prompt_en": baseline_prompt_en,
            "user_definitions": list(definitions),
            "interpretation_provenance": list(interpretations),
            "unresolved_ambiguities": [],
            "user_exclusions": list(exclusions),
            "style": {
                "domain": "general_photo",
                "family": "context-led photographic study",
                "evidence": ["restrained color hierarchy", "tactile material detail"],
            },
            "variation_key": "v5-test",
        }

    def run_wrapper_raw(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(WRAPPER_PATH), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def run_v5(
        self,
        core: dict,
        *,
        seed: int = 91,
        creativity: float = 0.5,
    ) -> dict:
        completed = self.run_wrapper_raw(
            "--selection-mode",
            "rule",
            "--seed",
            str(seed),
            "--emit-candidate-pack",
            "--candidate-pack-version",
            "v5",
            "--concept-lock",
            core["source_request"],
            "--authorial-core-json",
            json.dumps(core, ensure_ascii=False),
            "--creativity",
            str(creativity),
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(len(payload), 1)
        return payload[0]

    @staticmethod
    def obligation(pack: dict, profile_id: str) -> dict | None:
        for row in (pack.get("visual_obligations") or {}).get("obligations") or []:
            if row.get("id") == profile_id:
                return row
        return None

    @staticmethod
    def profile_clarification(pack: dict, profile_id: str) -> dict | None:
        for row in (pack.get("semantic_clarification") or {}).get("candidates") or []:
            if row.get("profile_id") == profile_id:
                return row
        return None

    def test_general_core_is_prepack_hash_bound_and_v4_remains_compatible(self):
        source = "Photorealistic blue porcelain teacup still life in a quiet rainlit kitchen"
        raw_core = self.core(source)
        normalized = prompt_generator.normalize_authorial_core(raw_core)
        self.assertEqual(normalized["provenance"], "agent_prepack")
        self.assertRegex(normalized["canonical_sha256"], r"^[0-9a-f]{64}$")

        invalid = copy.deepcopy(raw_core)
        invalid["candidate_ids"] = ["slot:location:private-answer"]
        with self.assertRaisesRegex(ValueError, "pack-derived or unsupported"):
            prompt_generator.normalize_authorial_core(invalid)

        pack = self.run_v5(raw_core)
        core = pack["authorial_core"]
        retrieval = pack["provenance"]["retrieval_query"]
        self.assertEqual(pack["contract_version"], "photo-candidate-pack/v5")
        self.assertEqual(core["canonical_sha256"], normalized["canonical_sha256"])
        self.assertEqual(retrieval["source_authorial_core_sha256"], core["canonical_sha256"])
        core_clarification = next(
            row
            for row in pack["semantic_clarification"]["candidates"]
            if row["id"] == "clarification:authorial-core:interpreted-intent"
        )
        self.assertEqual(core_clarification["applicability"]["status"], "review_required")
        self.assertTrue(core_clarification["revisable"])
        self.assertIn("baseline_prompt_en", retrieval["source_fields"])
        self.assertFalse(retrieval["exclusions_used_as_positive_query"])
        self.assertTrue(pack["coverage"]["intent_constraints"]["no_people"])
        self.assertNotIn("adult_appeal", pack)

        missing = self.run_wrapper_raw(
            "--selection-mode",
            "rule",
            "--emit-candidate-pack",
            "--candidate-pack-version",
            "v5",
            "--concept-lock",
            source,
        )
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("requires --authorial-core-json", missing.stderr)

        mismatched = copy.deepcopy(raw_core)
        mismatched["source_request"] = "a request that was never supplied"
        mismatch_run = self.run_wrapper_raw(
            "--selection-mode",
            "rule",
            "--emit-candidate-pack",
            "--candidate-pack-version",
            "v5",
            "--concept-lock",
            source,
            "--authorial-core-json",
            json.dumps(mismatched),
        )
        self.assertNotEqual(mismatch_run.returncode, 0)
        self.assertIn("must exactly match a user request source", mismatch_run.stderr)

        legacy = self.run_wrapper_raw(
            "--selection-mode",
            "rule",
            "--seed",
            "91",
            "--emit-candidate-pack",
            "--concept-lock",
            source,
        )
        self.assertEqual(legacy.returncode, 0, legacy.stderr)
        self.assertEqual(json.loads(legacy.stdout)[0]["contract_version"], "photo-candidate-pack/v4")

    def test_authorial_core_text_is_the_actual_semantic_query_and_changes_selection(self):
        data = {
            "version": "test",
            "presets": [
                {
                    "id": "test_preset",
                    "en": "test preset",
                    "required_slots": ["location"],
                    "filters": {
                        "location": {"ids": ["red_studio", "misty_forest"]}
                    },
                }
            ],
            "slots": {
                "location": [
                    {"id": "red_studio", "en": "a red geometric studio", "weight": 1},
                    {"id": "misty_forest", "en": "a misty cedar forest", "weight": 1},
                ]
            },
        }
        index = {
            "provider": "gemini",
            "dictionary_hash": prompt_generator.dictionary_hash(data),
            "semantic_text_recipe": prompt_generator.SEMANTIC_TEXT_RECIPE_VERSION,
            "embedding_model": "gemini-embedding-2",
            "embedding_dimensions": 2,
            "entries": {
                "preset:test_preset": {"vector": [1.0, 0.0]},
                "slot:location:red_studio": {"vector": [1.0, 0.0]},
                "slot:location:misty_forest": {"vector": [0.0, 1.0]},
            },
        }
        red_core = prompt_generator.normalize_authorial_core(
            self.core(
                "A red geometric studio product photograph",
                interpreted_intent="A precise red geometric studio study with ordered planes and hard edges",
                setting="a red geometric studio interior",
                baseline_prompt_en=(
                    "A blue porcelain teacup stands inside a red geometric studio where ordered "
                    "planes, hard edges, restrained reflections, exact shadows, quiet spacing, and "
                    "tactile glaze form a precise product photograph."
                ),
                exclusions=("misty forest",),
            )
        )
        forest_core = prompt_generator.normalize_authorial_core(
            self.core(
                "A misty cedar forest product photograph",
                interpreted_intent="A quiet misty cedar forest study with layered trunks and diffuse air",
                setting="a misty cedar forest clearing",
                baseline_prompt_en=(
                    "A blue porcelain teacup rests within a misty cedar forest where layered trunks, "
                    "diffuse air, damp bark, quiet depth, restrained reflections, and tactile glaze "
                    "form an atmospheric product photograph."
                ),
                exclusions=("red studio",),
            )
        )
        red_query, red_provenance = prompt_generator.authorial_core_retrieval_text(red_core)
        forest_query, forest_provenance = prompt_generator.authorial_core_retrieval_text(forest_core)
        observed_queries: list[str] = []

        def fake_embed(text: str, **_: object) -> list[float]:
            observed_queries.append(text)
            return [0.0, 1.0] if "misty cedar forest" in text.lower() else [1.0, 0.0]

        with mock.patch.object(
            prompt_generator,
            "embed_single_semantic_text",
            side_effect=fake_embed,
        ):
            red_context = prompt_generator.make_semantic_context(
                data,
                red_core["source_request"],
                "semantic",
                "medium",
                filter_strictness="soft",
                semantic_weight=1.0,
                semantic_profile="balanced",
                semantic_index=index,
                semantic_dimensions=2,
                gemini_api_key="test-key",
                semantic_axis_mode="off",
                retrieval_text=red_query,
                retrieval_provenance=red_provenance,
                authorial_core_mode=True,
            )
            forest_context = prompt_generator.make_semantic_context(
                data,
                forest_core["source_request"],
                "semantic",
                "medium",
                filter_strictness="soft",
                semantic_weight=1.0,
                semantic_profile="balanced",
                semantic_index=index,
                semantic_dimensions=2,
                gemini_api_key="test-key",
                semantic_axis_mode="off",
                retrieval_text=forest_query,
                retrieval_provenance=forest_provenance,
                authorial_core_mode=True,
            )

        self.assertIn(red_query, observed_queries)
        self.assertIn(forest_query, observed_queries)
        self.assertNotIn("misty forest", red_query.lower())
        self.assertNotIn("red studio", forest_query.lower())
        red_selected = prompt_generator.choose_slot(
            "location", data, data["presets"][0], random.Random(8), {}, semantic_context=red_context
        )
        forest_selected = prompt_generator.choose_slot(
            "location", data, data["presets"][0], random.Random(8), {}, semantic_context=forest_context
        )
        self.assertEqual(red_selected["id"], "red_studio")
        self.assertEqual(forest_selected["id"], "misty_forest")

    def test_clarification_is_stable_while_creativity_widens_seeded_augmentation(self):
        source = "Photorealistic blue porcelain teacup still life in a quiet rainlit kitchen"
        core = self.core(source)
        low = self.run_v5(core, seed=401, creativity=0.0)
        medium = self.run_v5(core, seed=401, creativity=0.5)
        high = self.run_v5(core, seed=401, creativity=1.0)

        clarifications = [
            pack["semantic_clarification"] for pack in (low, medium, high)
        ]
        self.assertEqual(clarifications[0], clarifications[1])
        self.assertEqual(clarifications[1], clarifications[2])
        augmentations = [pack["creative_augmentation"] for pack in (low, medium, high)]
        self.assertEqual(
            {row["hard_eligible_pool_sha256"] for row in augmentations},
            {augmentations[0]["hard_eligible_pool_sha256"]},
        )
        self.assertEqual(
            {row["guard_invariant_sha256"] for row in augmentations},
            {augmentations[0]["guard_invariant_sha256"]},
        )
        self.assertEqual(augmentations[0]["distance_policy"]["allowed_bands"], ["near"])
        self.assertEqual(
            augmentations[1]["distance_policy"]["allowed_bands"],
            ["near", "adjacent"],
        )
        self.assertEqual(
            augmentations[2]["distance_policy"]["allowed_bands"],
            ["near", "adjacent", "lateral"],
        )
        self.assertEqual(
            {row["semantic_band"] for row in augmentations[0]["candidates"]},
            {"near"},
        )
        self.assertIn("adjacent", {row["semantic_band"] for row in augmentations[1]["candidates"]})
        self.assertIn("lateral", {row["semantic_band"] for row in augmentations[2]["candidates"]})
        self.assertNotIn("hybrid_augmentation", high)
        self.assertNotIn("creative_direction", low)
        self.assertTrue(high["creative_direction"]["enabled"])

        seed_sets = {
            tuple(sorted(row["id"] for row in self.run_v5(core, seed=seed, creativity=1.0)["creative_augmentation"]["candidates"]))
            for seed in (501, 502, 503)
        }
        self.assertGreaterEqual(len(seed_sets), 2)

    def test_contextual_term_meanings_materialize_without_one_fixed_story(self):
        absolute_source = "성인 여성의 절대공역 매력을 강조한 사진"
        absolute = self.run_v5(
            self.core(
                absolute_source,
                interpreted_intent="An adult fashion portrait emphasizing attractive true inner thigh negative space",
                subject="an unmistakably adult woman",
                setting="a restrained fashion photography studio",
                event="she holds her legs close in a deliberate standing pose",
                visual_priorities=("close adult leg geometry", "true inner thigh opening", "attractive focal negative space"),
                baseline_prompt_en=(
                    "An unmistakably adult woman stands with knees close while a narrow background "
                    "opening is bounded by the actual upper inner-thigh contours, framed as attractive "
                    "negative space with a tight thigh-dominant crop and no false garment gap."
                ),
                definitions=(
                    {
                        "term": "절대공역",
                        "source_text": "절대공역",
                        "interpreted_meaning": "true negative space bounded by close upper inner thigh contours",
                        "prompt_evidence": "narrow background opening is bounded by the actual upper inner-thigh contours",
                    },
                ),
                exclusions=("wide stance", "garment opening"),
            ),
            creativity=0.0,
        )
        thigh = self.obligation(absolute, "inner_thigh_negative_space")
        self.assertIsNotNone(thigh)
        self.assertIn("appeal_emphasis_phrase", thigh["prompt_binding"]["required_evidence_fields"])
        self.assertIn(
            "vo_inner_thigh_attractive_composition",
            {row["id"] for row in thigh["render_gates"]},
        )

        ahegao_source = "성인 여성의 아헤가오 표정 사진"
        ahegao = self.run_v5(
            self.core(
                ahegao_source,
                interpreted_intent="A fully clothed adult portrait translating the named expression into simultaneous facial components",
                subject="an unmistakably adult woman",
                setting="a neutral close portrait studio",
                event="she briefly loses composure in one readable expression",
                visual_priorities=("asymmetric upward eye drift", "external centered tongue tip", "subtle blush and fatigue"),
                baseline_prompt_en=(
                    "An unmistakably adult woman in a fully clothed portrait shows asymmetric upward "
                    "eye drift, relaxed brows, a small rounded open mouth, a centered external tongue "
                    "tip, subtle cheek blush, and a slightly fatigued release all at once."
                ),
                definitions=(
                    {
                        "term": "아헤가오",
                        "source_text": "아헤가오",
                        "interpreted_meaning": "simultaneous upward eyes external tongue blush and tired release",
                        "prompt_evidence": "asymmetric upward eye drift, relaxed brows, a small rounded open mouth",
                    },
                ),
                exclusions=("아헤가오", "orgasm", "sexual act"),
            ),
            creativity=0.0,
        )
        overwhelmed = self.obligation(ahegao, "composite_overwhelmed_expression")
        self.assertIsNotNone(overwhelmed)
        self.assertIn("subtle_blush_phrase", overwhelmed["prompt_binding"]["required_evidence_fields"])
        self.assertIn("fatigued_release_phrase", overwhelmed["prompt_binding"]["required_evidence_fields"])
        self.assertIn("아헤가오", overwhelmed["runtime_expression"]["forbidden_prompt_terms"])

        bare = self.run_v5(
            self.core(
                "아헤가오",
                interpreted_intent="A shorthand expression request kept age neutral until context is explicitly supplied",
                subject="one expressive portrait subject",
                setting="a neutral close portrait studio",
                event="the face holds a composite overwhelmed expression",
                visual_priorities=("upward eye direction", "external tongue component"),
                baseline_prompt_en=(
                    "A close portrait studies upward-directed eyes, relaxed brows, a small rounded open "
                    "mouth, and a centered external tongue tip as separate readable components under "
                    "plain studio light without assigning age or sexual context."
                ),
                exclusions=("아헤가오", "explicit sexual act"),
            ),
            creativity=0.0,
        )
        self.assertIsNone(self.obligation(bare, "composite_overwhelmed_expression"))
        self.assertEqual(
            self.profile_clarification(bare, "composite_overwhelmed_expression")["applicability"]["status"],
            "requires_existing_adult_context",
        )

        corruption_source = "성인 여성 캐릭터가 타락해가는 변신 사진"
        corruption = self.run_v5(
            self.core(
                corruption_source,
                interpreted_intent="An adult character visibly crossing from a former identity into a dark current state",
                subject="an unmistakably adult woman character",
                setting="a dim ceremonial chamber interior",
                event="an unfinished embodied transformation spreads across her body",
                visual_priorities=("former identity remains visible", "unfinished on body boundary", "context specific visible cause"),
                baseline_prompt_en=(
                    "An unmistakably adult character remains mid-transition: her former identity stays "
                    "visible beside a dark current state, an unfinished on-body boundary still spreads, "
                    "and a present-tense visible cause makes the transformation readable."
                ),
                exclusions=("political corruption", "completed costume swap"),
            ),
            creativity=0.0,
        )
        corruption_obligation = self.obligation(corruption, "embodied_corruption_transition")
        self.assertIsNotNone(corruption_obligation)
        self.assertNotIn("allegiance_choice_phrase", corruption_obligation["prompt_binding"]["required_evidence_fields"])
        self.assertNotIn("suppressed_remnant_phrase", corruption_obligation["prompt_binding"]["required_evidence_fields"])

        elegance_source = "타락한 우아함 무드의 성인 여성 패션 사진"
        elegance = self.run_v5(
            self.core(
                elegance_source,
                interpreted_intent="A decadent fallen elegance mood with no character transformation or allegiance change",
                subject="an unmistakably adult fashion model",
                setting="a faded ornate salon interior",
                event="she maintains a composed editorial fashion pose",
                visual_priorities=("decadent elegance atmosphere", "faded luxurious materials", "composed adult poise"),
                baseline_prompt_en=(
                    "An unmistakably adult fashion model holds a composed editorial pose inside a faded "
                    "salon, expressing decadent elegance through tarnished gold, bruised velvet, restrained "
                    "shadows, and weathered luxury without a character transformation."
                ),
                exclusions=("embodied metamorphosis", "allegiance change"),
            ),
            creativity=0.0,
        )
        self.assertIsNone(self.obligation(elegance, "embodied_corruption_transition"))
        self.assertEqual(
            self.profile_clarification(elegance, "embodied_corruption_transition")["applicability"]["status"],
            "context_mismatch",
        )

        mesugaki_source = "성인 메스가키 캐릭터의 도도하고 건방진 초상"
        mesugaki = self.run_v5(
            self.core(
                mesugaki_source,
                interpreted_intent="An unmistakably adult rival with haughty smug poise and fresh youthful adult styling",
                subject="an unmistakably adult peer rival",
                setting="a clean competitive portrait studio",
                event="she holds a poised arrogant expression toward the camera",
                visual_priorities=("haughty facial baseline", "smug adult poise", "fresh youthful adult styling"),
                baseline_prompt_en=(
                    "An unmistakably adult peer rival faces the camera with a raised brow, half-lidded "
                    "eyes, a cool superior smirk, poised arrogant bearing, and fresh youthful adult "
                    "styling while behavior, not childlike morphology, carries the archetype."
                ),
                definitions=(
                    {
                        "term": "메스가키",
                        "source_text": "메스가키",
                        "interpreted_meaning": "adult haughty smug poise with youthful adult styling",
                        "prompt_evidence": "poised arrogant bearing, and fresh youthful adult styling",
                    },
                ),
                exclusions=("메스가키", "childlike proportions", "schoolchild styling"),
            ),
            creativity=0.0,
        )
        status_play = self.obligation(mesugaki, "adult_mesugaki_status_play")
        self.assertIsNotNone(status_play)
        required = status_play["prompt_binding"]["required_evidence_fields"]
        self.assertIn("adult_youthful_styling_phrase", required)
        self.assertNotIn("small_setback_phrase", required)
        self.assertNotIn("warm_crack_phrase", required)
        self.assertIn("메스가키", status_play["runtime_expression"]["forbidden_prompt_terms"])

    def test_v5_composition_audit_binds_core_and_rejects_copying(self):
        source = "Photorealistic blue porcelain teacup still life in a quiet rainlit kitchen"
        pack = self.run_v5(self.core(source), seed=91, creativity=0.5)
        prompt = (
            "Photorealistic blue porcelain teacup still life in a quiet rainlit kitchen. A blue "
            "porcelain teacup rests on a dark kitchen counter while delicate rising steam catches "
            "rainlit window reflections, with a quiet domestic mood, restrained slate colors, shallow "
            "focus, and tactile glaze detail. Frame the cup slightly off center so the steam bridges "
            "the cool window reflection and dark counter, leaving deliberate stillness around the handle."
        )
        clarification_decisions = [
            {
                "clarification_id": row["id"],
                "decision": "applied",
                "rationale": "preserves governing meaning",
                "prompt_evidence": "quiet domestic mood",
            }
            for row in pack["semantic_clarification"]["candidates"]
        ]
        creative_decisions = [
            {
                "candidate_id": row["id"],
                "decision": "rejected",
                "rationale": "weakens focused still life",
            }
            for row in pack["creative_augmentation"]["candidates"]
        ]
        composed = {
            "pack_id": pack["pack_id"],
            "prompt_en": prompt,
            "negative_en": pack["negative_en"],
            "chosen_candidate_ids": [],
            "composer": "agent",
            "candidate_interpretations": [],
            "authorial_core_binding": {
                "source_authorial_core_sha256": pack["authorial_core"]["canonical_sha256"],
                "preserved_evidence": [
                    "blue porcelain teacup",
                    "delicate rising steam",
                    "rainlit window reflections",
                ],
                "authorial_decisions": [
                    {
                        "dimension": "framing",
                        "decision": "off center cup placement",
                        "rationale": "creates asymmetrical domestic stillness",
                    },
                    {
                        "dimension": "relationship",
                        "decision": "steam bridges reflected window light",
                        "rationale": "links warm presence with cool weather",
                    },
                ],
            },
            "semantic_clarification_decisions": clarification_decisions,
            "creative_augmentation_brief": {"decisions": creative_decisions},
        }
        audit = audit_composed_prompt.audit_composed_prompt(pack, composed)
        self.assertEqual(audit["status"], "pass", audit["failures"])

        missing_binding = copy.deepcopy(composed)
        missing_binding.pop("authorial_core_binding")
        missing_audit = audit_composed_prompt.audit_composed_prompt(pack, missing_binding)
        self.assertIn(
            "authorial_core_binding",
            {row["check"] for row in missing_audit["failures"]},
        )

        mutated_pack = copy.deepcopy(pack)
        mutated_pack["provenance"]["retrieval_query"]["query_sha256"] = "0" * 64
        retrieval_failures = audit_composed_prompt.audit_authorial_core_v5(
            mutated_pack,
            composed,
            prompt,
        )
        self.assertIn(
            "authorial_core_integrity",
            {row["check"] for row in retrieval_failures},
        )

        exclusion_leak = copy.deepcopy(composed)
        exclusion_leak["prompt_en"] += " Bright sunlight floods the counter."
        exclusion_audit = audit_composed_prompt.audit_composed_prompt(
            pack,
            exclusion_leak,
        )
        self.assertIn(
            "authorial_core_exclusion",
            {row["check"] for row in exclusion_audit["failures"]},
        )

        copied = copy.deepcopy(composed)
        candidate = pack["creative_augmentation"]["candidates"][0]
        candidate_id = candidate["id"]
        copied_evidence = " ".join(candidate["concept_terms"][:4])
        copied["prompt_en"] += f" {copied_evidence}."
        copied["chosen_candidate_ids"] = [candidate_id]
        for decision in copied["creative_augmentation_brief"]["decisions"]:
            if decision["candidate_id"] == candidate_id:
                decision.update(
                    {
                        "decision": "transformed",
                        "rationale": "adds a secondary material contrast",
                        "artistic_interpretation": "reframes material against domestic quiet",
                        "transformation": "moves source terms into foreground tension",
                        "prompt_evidence": copied_evidence,
                    }
                )
        copied_audit = audit_composed_prompt.audit_composed_prompt(pack, copied)
        self.assertIn(
            "creative_augmentation_transform",
            {row["check"] for row in copied_audit["failures"]},
        )

    def test_sensitive_label_leak_fails_semantic_clarification_audit(self):
        core = self.core(
            "아헤가오",
            interpreted_intent="A shorthand expression request kept age neutral until context is explicitly supplied",
            subject="one expressive portrait subject",
            setting="a neutral close portrait studio",
            event="the face holds a composite overwhelmed expression",
            visual_priorities=("upward eye direction", "external tongue component"),
            baseline_prompt_en=(
                "A close portrait studies upward-directed eyes, relaxed brows, a small rounded open "
                "mouth, and a centered external tongue tip as separate readable components under "
                "plain studio light without assigning age or sexual context."
            ),
            exclusions=("아헤가오", "explicit sexual act"),
        )
        pack = self.run_v5(core, creativity=0.0)
        retrieval_text, retrieval = prompt_generator.authorial_core_retrieval_text(
            pack["authorial_core"]
        )
        self.assertNotIn("아헤가오", retrieval_text)
        self.assertIn("upward-directed eyes", retrieval_text)
        self.assertIn("source_request", retrieval["redacted_source_fields"])
        self.assertEqual(pack["provenance"]["retrieval_query"], retrieval)
        decisions = []
        for row in pack["semantic_clarification"]["candidates"]:
            status = row["applicability"]["status"]
            decisions.append(
                {
                    "clarification_id": row["id"],
                    "decision": "rejected" if status == "requires_existing_adult_context" else "applied",
                    "rationale": "respects contextual applicability",
                    "prompt_evidence": "upward-directed eyes",
                }
            )
        failures = audit_composed_prompt.audit_semantic_clarification_v5(
            pack,
            {"semantic_clarification_decisions": decisions},
            "A portrait with upward-directed eyes, labeled 아헤가오.",
        )
        self.assertIn(
            "semantic_clarification_sensitive_label",
            {row["check"] for row in failures},
        )

    def test_v5_preserves_existing_adult_appeal_combination_audit(self):
        pack = {
            "adult_appeal": {
                "enabled": True,
                "axes": {},
                "blend": {"emphasis": "sensual_led"},
                "combination_policy": {
                    "risk_groups": {
                        "sheer_layer": {"prompt_terms": ["sheer lingerie layer"]},
                        "ground_angle": {"prompt_terms": ["extreme ground-level angle"]},
                    },
                    "hard_combinations": [
                        {
                            "id": "existing_sheer_ground_angle",
                            "all_of": ["sheer_layer", "ground_angle"],
                            "reason": "existing hard styling-camera combination",
                        }
                    ],
                    "warning_combinations": [],
                },
            }
        }
        prompt = (
            "An unmistakably adult original subject chooses her own pose with a sheer lingerie "
            "layer photographed from an extreme ground-level angle."
        )
        composed = {
            "adult_appeal_brief": {
                "adult_subject_phrase": "unmistakably adult original subject",
                "agency_phrase": "chooses her own pose",
                "axes": {},
                "blend": {"emphasis": "sensual_led"},
            }
        }
        failures, warnings = audit_composed_prompt.audit_adult_appeal_v5(
            pack,
            composed,
            prompt,
            set(),
            {},
        )
        self.assertEqual(warnings, [])
        self.assertIn(
            "adult_appeal_combination_risk",
            {row["check"] for row in failures},
        )


if __name__ == "__main__":
    unittest.main()
