from __future__ import annotations

import copy
import hashlib
import json
import random
import subprocess
import tempfile
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
import audit_image_render_request  # noqa: E402
import prompt_generator  # noqa: E402
from tests import photo_prompt_fixtures as fixtures


_TEST_PROMPT_BUDGET_EXTENSION = (
    "Fine-grained surface cues, coherent near-to-far depth, controlled highlights, legible "
    "shadow detail, and an intentional focal hierarchy keep the completed photographic frame "
    "specific, balanced, natural, and visually unambiguous."
)


class PhotoAuthorialCoreTests(unittest.TestCase):
    @staticmethod
    def envelope(*args, **kwargs):
        return fixtures.envelope(*args, **kwargs)

    @staticmethod
    def core(*args, **kwargs):
        return fixtures.core(*args, **kwargs)

    def run_wrapper_raw(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(WRAPPER_PATH), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def run_current(self, core, *, seed=91, creativity=1):
        return fixtures.run_current(core, seed=seed, creativity=creativity)

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

    def test_general_core_is_prepack_hash_bound_and_unbound_generation_is_rejected(self):
        source = (
            "Photorealistic blue porcelain teacup still life in a quiet rainlit kitchen "
            "without people or bright sunlight"
        )
        raw_core = self.core(source, exclusions=("people", "bright sunlight"))
        envelope = prompt_generator.normalize_request_envelope(self.envelope(source))
        normalized = prompt_generator.normalize_authorial_core(
            raw_core,
            request_envelope=envelope,
        )
        self.assertEqual(normalized["provenance"], "agent_prepack")
        self.assertRegex(normalized["canonical_sha256"], r"^[0-9a-f]{64}$")

        invalid = copy.deepcopy(raw_core)
        invalid["candidate_ids"] = ["slot:location:private-answer"]
        with self.assertRaisesRegex(ValueError, "pack-derived or unsupported"):
            prompt_generator.normalize_authorial_core(
                invalid,
                request_envelope=envelope,
            )

        pack = self.run_current(raw_core)
        core = pack["authorial_core"]
        retrieval = pack["provenance"]["retrieval_query"]
        self.assertEqual(pack["contract_version"], "photo-candidate-pack/v6")
        self.assertEqual(core["source_request"], normalized["source_request"])
        self.assertEqual(core["baseline_prompt_en"], normalized["baseline_prompt_en"])
        self.assertEqual(retrieval["source_authorial_core_sha256"], core["canonical_sha256"])
        core_clarification = next(
            row
            for row in pack["semantic_clarification"]["candidates"]
            if row["id"] == "clarification:authorial-core:interpreted-intent"
        )
        self.assertEqual(core_clarification["applicability"]["status"], "required")
        self.assertFalse(core_clarification["revisable"])
        self.assertTrue(core_clarification["required_in_final_prompt"])
        self.assertEqual(
            pack["intent_preservation"]["source_intent_lock_sha256"],
            core["intent_lock"]["canonical_sha256"],
        )
        self.assertIn("baseline_prompt_en", retrieval["source_fields"])
        self.assertFalse(retrieval["exclusions_used_as_positive_query"])
        self.assertTrue(pack["coverage"]["intent_constraints"]["no_people"])
        self.assertFalse(pack.get("adult_appeal", {}).get("enabled"))

        missing = self.run_wrapper_raw(
            "--selection-mode",
            "rule",
            "--emit-candidate-pack",
            "--candidate-pack-version",
            "v6",
        )
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("requires --authorial-core-json", missing.stderr)

        mismatched = copy.deepcopy(raw_core)
        mismatched["source_request"] = "a request that was never supplied"
        mismatched["creative_controls_sha256"] = pack["creative_controls"]["canonical_sha256"]
        with tempfile.TemporaryDirectory() as temp:
            controls_path = Path(temp) / "controls.json"
            review_path = Path(temp) / "review.json"
            envelope_path = Path(temp) / "envelope.json"
            core_path = Path(temp) / "core.json"
            envelope_path.write_text(json.dumps(self.envelope(source), ensure_ascii=False))
            core_path.write_text(json.dumps(mismatched))
            controls_path.write_text(json.dumps(pack["creative_controls"]))
            review_path.write_text(json.dumps(fixtures.review(raw_core["baseline_prompt_en"])))
            mismatch_run = self.run_wrapper_raw(
                "--selection-mode",
                "rule",
                "--emit-candidate-pack",
                "--candidate-pack-version",
                "v6",
                "--request-envelope-json",
                str(envelope_path),
                "--authorial-core-json",
                str(core_path),
                "--creative-controls-json",
                str(controls_path),
                "--embodiment-review-json",
                str(review_path),
            )
        self.assertNotEqual(mismatch_run.returncode, 0)
        self.assertIn("creative-control snapshot is stale", mismatch_run.stderr)
        with self.assertRaisesRegex(
            ValueError, "must exactly match request envelope request_text bytes"
        ):
            prompt_generator.normalize_authorial_core(mismatched, request_envelope=envelope)

        legacy = self.run_wrapper_raw(
            "--selection-mode",
            "rule",
            "--seed",
            "91",
            "--emit-candidate-pack",
            "--concept-lock",
            source,
        )
        self.assertNotEqual(legacy.returncode, 0)
        self.assertIn("authorial-core", legacy.stderr)

    def test_request_envelope_and_intent_lock_fail_closed_for_arbitrary_topics(self):
        source = "Create a glass lighthouse above a frozen lake, lit by green moonlight"
        active_texts = (
            "glass lighthouse above a frozen lake",
            "green moonlight",
        )
        baseline = (
            "One glass lighthouse floats above a frozen lake as cracked ice reflects its clear "
            "silhouette, while green moonlight creates long emerald shadows, pale mist, crisp "
            "surface texture, distant depth, and a quiet impossible nocturnal event."
        )
        raw_core = self.core(
            source,
            interpreted_intent=(
                "A physically legible surreal photograph of a glass lighthouse floating above frozen water under green moonlight"
            ),
            subject="one glass lighthouse",
            setting="a wide frozen lake at night",
            event="one glass lighthouse floats above a frozen lake",
            visual_priorities=(
                "transparent glass lighthouse silhouette",
                "frozen lake surface texture",
                "green moonlight shadows",
            ),
            baseline_prompt_en=baseline,
            interpretations=(
                {
                    "term": "floating lighthouse event",
                    "source_text": active_texts[0],
                    "basis": "request_context",
                    "resolution": "a glass lighthouse visibly floating above a frozen lake",
                    "sources": [],
                },
                {
                    "term": "lighting modifier",
                    "source_text": active_texts[1],
                    "basis": "request_context",
                    "resolution": "green moonlight visibly controls the scene lighting and shadows",
                    "sources": [],
                },
            ),
            locked_dimensions=("concept", "subject", "event", "lighting"),
            open_dimensions=(
                "framing",
                "composition",
                "camera",
                "color",
                "material",
                "atmosphere",
            ),
            anchor_evidence=(
                "quiet impossible nocturnal event",
                "One glass lighthouse",
                "glass lighthouse floats above a frozen lake",
                "green moonlight creates long emerald shadows",
            ),
        )
        for anchor in raw_core["intent_lock"]["semantic_anchors"]:
            anchor["source_text"] = (
                active_texts[1] if anchor["dimension"] == "lighting" else active_texts[0]
            )
        envelope = prompt_generator.normalize_request_envelope(self.envelope(source, active_texts))
        normalized = prompt_generator.normalize_authorial_core(
            raw_core,
            request_envelope=envelope,
        )
        retrieval_text, provenance = prompt_generator.authorial_core_retrieval_text(normalized)
        self.assertIn(active_texts[0], retrieval_text)
        self.assertIn(active_texts[1], retrieval_text)
        self.assertEqual(
            provenance["active_scope_sha256"],
            prompt_generator.canonical_json_sha256(normalized["request_binding"]["active_spans"]),
        )
        forged_binding = copy.deepcopy(normalized)
        forged_binding["request_binding"]["request_envelope_sha256"] = "0" * 64
        forged_material = copy.deepcopy(forged_binding)
        forged_material.pop("canonical_sha256")
        forged_material.pop("core_id")
        forged_binding["canonical_sha256"] = prompt_generator.canonical_json_sha256(forged_material)
        forged_binding["core_id"] = forged_binding["canonical_sha256"][:16]
        self.assertFalse(audit_composed_prompt.authorial_core_intent_contract_valid(forged_binding))

        missing_envelope = self.run_wrapper_raw(
            "--selection-mode",
            "rule",
            "--emit-candidate-pack",
            "--candidate-pack-version",
            "v6",
            "--authorial-core-json",
            json.dumps(raw_core, ensure_ascii=False),
        )
        self.assertNotEqual(missing_envelope.returncode, 0)
        self.assertIn("requires --request-envelope-json", missing_envelope.stderr)

        unanchored = copy.deepcopy(raw_core)
        unanchored["intent_lock"]["semantic_anchors"] = [
            row
            for row in unanchored["intent_lock"]["semantic_anchors"]
            if row["dimension"] != "lighting"
        ]
        unanchored["intent_lock"]["locked_dimensions"].remove("lighting")
        unanchored["intent_lock"]["open_dimensions"].append("lighting")
        with self.assertRaisesRegex(ValueError, "coverage for every active"):
            prompt_generator.normalize_authorial_core(
                unanchored,
                request_envelope=envelope,
            )

        missing_event_lock = copy.deepcopy(raw_core)
        missing_event_lock["intent_lock"]["semantic_anchors"] = [
            row
            for row in missing_event_lock["intent_lock"]["semantic_anchors"]
            if row["dimension"] != "event"
        ]
        missing_event_lock["intent_lock"]["locked_dimensions"].remove("event")
        missing_event_lock["intent_lock"]["open_dimensions"].append("event")
        with self.assertRaisesRegex(ValueError, "concept, subject, and event"):
            prompt_generator.normalize_authorial_core(
                missing_event_lock,
                request_envelope=envelope,
            )

        forged_definition = copy.deepcopy(raw_core)
        forged_definition["user_definitions"] = [
            {
                "term": "green moonlight",
                "source_text": "green moonlight",
                "interpreted_meaning": "a soothing natural green ambient light",
                "prompt_evidence": "green moonlight creates long emerald shadows",
            }
        ]
        with self.assertRaisesRegex(ValueError, "bare term"):
            prompt_generator.normalize_authorial_core(
                forged_definition,
                request_envelope=envelope,
            )

    def test_authorial_core_text_is_the_actual_semantic_query_and_changes_selection(self):
        data = {
            "version": "test",
            "presets": [
                {
                    "id": "test_preset",
                    "en": "test preset",
                    "required_slots": ["location"],
                    "filters": {"location": {"ids": ["red_studio", "misty_forest"]}},
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
        red_source = "A red geometric studio product photograph without a misty forest"
        red_core = prompt_generator.normalize_authorial_core(
            self.core(
                red_source,
                interpreted_intent="A precise red geometric studio study with ordered planes and hard edges",
                setting="a red geometric studio interior",
                baseline_prompt_en=(
                    "A blue porcelain teacup stands inside a red geometric studio where ordered "
                    "planes, hard edges, restrained reflections, exact shadows, quiet spacing, and "
                    "tactile glaze form a precise product photograph."
                ),
                exclusions=("misty forest",),
            ),
            request_envelope=prompt_generator.normalize_request_envelope(self.envelope(red_source)),
        )
        forest_source = "A misty cedar forest product photograph without a red studio"
        forest_core = prompt_generator.normalize_authorial_core(
            self.core(
                forest_source,
                interpreted_intent="A quiet misty cedar forest study with layered trunks and diffuse air",
                setting="a misty cedar forest clearing",
                baseline_prompt_en=(
                    "A blue porcelain teacup rests within a misty cedar forest where layered trunks, "
                    "diffuse air, damp bark, quiet depth, restrained reflections, and tactile glaze "
                    "form an atmospheric product photograph."
                ),
                exclusions=("red studio",),
            ),
            request_envelope=prompt_generator.normalize_request_envelope(
                self.envelope(forest_source)
            ),
        )
        red_query, red_provenance = prompt_generator.authorial_core_retrieval_text(red_core)
        forest_query, forest_provenance = prompt_generator.authorial_core_retrieval_text(
            forest_core
        )
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
            "location",
            data,
            data["presets"][0],
            random.Random(8),
            {},
            semantic_context=forest_context,
        )
        self.assertEqual(red_selected["id"], "red_studio")
        self.assertEqual(forest_selected["id"], "misty_forest")

    def test_clarification_is_stable_while_creativity_widens_seeded_augmentation(self):
        source = "Photorealistic blue porcelain teacup still life in a quiet rainlit kitchen"
        core = self.core(source)
        low = self.run_current(core, seed=401, creativity=0)
        medium = self.run_current(core, seed=401, creativity=2)
        high = self.run_current(core, seed=401, creativity=3)

        clarifications = [
            {
                key: value
                for key, value in pack["semantic_clarification"].items()
                if key != "source_authorial_core_sha256"
            }
            for pack in (low, medium, high)
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
            tuple(
                sorted(
                    row["id"]
                    for row in self.run_current(core, seed=seed, creativity=3)[
                        "creative_augmentation"
                    ]["candidates"]
                )
            )
            for seed in (501, 502, 503)
        }
        self.assertGreaterEqual(len(seed_sets), 2)

    def test_contextual_term_meanings_materialize_without_one_fixed_story(self):
        absolute_source = "성인 여성의 절대공역 매력을 강조한 사진"
        absolute = self.run_current(
            self.core(
                absolute_source,
                interpreted_intent="An adult fashion portrait emphasizing attractive true inner thigh negative space",
                subject="an unmistakably adult woman",
                setting="a restrained fashion photography studio",
                event="she holds her legs close in a deliberate standing pose",
                visual_priorities=(
                    "close adult leg geometry",
                    "true inner thigh opening",
                    "attractive focal negative space",
                ),
                baseline_prompt_en=(
                    "An unmistakably adult woman stands with knees close while a narrow background "
                    "opening is bounded by the actual upper inner-thigh contours, framed as attractive "
                    "negative space with a tight thigh-dominant crop and no false garment gap."
                ),
                interpretations=(
                    {
                        "term": "절대공역",
                        "source_text": "절대공역",
                        "basis": "agent_general_knowledge",
                        "resolution": "true negative space bounded by close upper inner thigh contours",
                        "sources": [],
                    },
                ),
                locked_dimensions=(
                    "concept",
                    "subject",
                    "event",
                    "pose",
                    "body_geometry",
                ),
                anchor_evidence=(
                    "attractive negative space",
                    "unmistakably adult woman",
                    "narrow background opening is bounded",
                    "stands with knees close",
                    "actual upper inner-thigh contours",
                ),
            ),
            creativity=0,
        )
        thigh = self.obligation(absolute, "inner_thigh_negative_space")
        self.assertIsNotNone(thigh)
        self.assertNotIn(
            "appeal_emphasis_phrase", thigh["prompt_binding"]["required_evidence_fields"]
        )
        self.assertIn("both feet touch or nearly touch", thigh["composition_instruction"])
        self.assertIn(
            "vo_inner_thigh_attractive_composition",
            {row["id"] for row in thigh["render_gates"]},
        )

        ahegao_source = "성인 여성의 아헤가오 표정 사진"
        ahegao = self.run_current(
            self.core(
                ahegao_source,
                interpreted_intent="A fully clothed adult portrait translating the named expression into simultaneous facial components",
                subject="an unmistakably adult woman",
                setting="a neutral close portrait studio",
                event="she briefly loses composure in one readable expression",
                visual_priorities=(
                    "asymmetric upward eye drift",
                    "external centered tongue tip",
                    "subtle blush and fatigue",
                ),
                baseline_prompt_en=(
                    "An unmistakably adult woman in a fully clothed portrait shows asymmetric upward "
                    "eye drift, relaxed brows, a small rounded open mouth, a centered external tongue "
                    "tip, subtle cheek blush, and a slightly fatigued release all at once."
                ),
                interpretations=(
                    {
                        "term": "아헤가오",
                        "source_text": "아헤가오",
                        "basis": "agent_general_knowledge",
                        "resolution": "simultaneous upward eyes external tongue blush and tired release",
                        "sources": [],
                    },
                ),
                runtime_forbidden_labels=("아헤가오",),
                locked_dimensions=(
                    "concept",
                    "subject",
                    "event",
                    "expression",
                ),
                anchor_evidence=(
                    "slightly fatigued release all at once",
                    "unmistakably adult woman",
                    "shows asymmetric upward eye drift",
                    "relaxed brows, a small rounded open mouth",
                ),
            ),
            creativity=0,
        )
        overwhelmed = self.obligation(ahegao, "composite_overwhelmed_expression")
        self.assertIsNotNone(overwhelmed)
        self.assertIn(
            "subtle_blush_phrase", overwhelmed["prompt_binding"]["required_evidence_fields"]
        )
        self.assertIn(
            "fatigued_release_phrase", overwhelmed["prompt_binding"]["required_evidence_fields"]
        )
        self.assertIn("아헤가오", overwhelmed["runtime_expression"]["forbidden_prompt_terms"])

        bare = self.run_current(
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
                interpretations=(
                    {
                        "term": "아헤가오",
                        "source_text": "아헤가오",
                        "basis": "agent_general_knowledge",
                        "resolution": "simultaneous upward eyes external tongue blush and tired release",
                        "sources": [],
                    },
                ),
                runtime_forbidden_labels=("아헤가오",),
                locked_dimensions=(
                    "concept",
                    "subject",
                    "event",
                    "expression",
                ),
                anchor_evidence=(
                    "separate readable components",
                    "A close portrait",
                    "centered external tongue tip",
                    "upward-directed eyes, relaxed brows",
                ),
            ),
            creativity=0,
        )
        self.assertIsNone(self.obligation(bare, "composite_overwhelmed_expression"))
        self.assertEqual(
            self.profile_clarification(bare, "composite_overwhelmed_expression")["applicability"][
                "status"
            ],
            "requires_existing_adult_context",
        )

        corruption_source = "성인 여성 캐릭터가 타락해가는 변신 사진"
        corruption = self.run_current(
            self.core(
                corruption_source,
                interpreted_intent="An adult character visibly crossing from a former identity into a dark current state",
                subject="an unmistakably adult woman character",
                setting="a dim ceremonial chamber interior",
                event="an unfinished embodied transformation spreads across her body",
                visual_priorities=(
                    "former identity remains visible",
                    "unfinished on body boundary",
                    "context specific visible cause",
                ),
                baseline_prompt_en=(
                    "An unmistakably adult character remains mid-transition: her former identity stays "
                    "visible beside a dark current state, an unfinished on-body boundary still spreads, "
                    "and a present-tense visible cause makes the transformation readable."
                ),
                interpretations=(
                    {
                        "term": "타락",
                        "source_text": "타락",
                        "basis": "request_context",
                        "resolution": "an embodied identity transition rather than political corruption",
                        "sources": [],
                    },
                ),
            ),
            creativity=0,
        )
        corruption_obligation = self.obligation(corruption, "embodied_corruption_transition")
        self.assertIsNotNone(corruption_obligation)
        self.assertNotIn(
            "allegiance_choice_phrase",
            corruption_obligation["prompt_binding"]["required_evidence_fields"],
        )
        self.assertNotIn(
            "suppressed_remnant_phrase",
            corruption_obligation["prompt_binding"]["required_evidence_fields"],
        )

        elegance_source = "타락한 우아함 무드의 성인 여성 패션 사진"
        elegance = self.run_current(
            self.core(
                elegance_source,
                interpreted_intent="A decadent fallen elegance mood with no character transformation or allegiance change",
                subject="an unmistakably adult fashion model",
                setting="a faded ornate salon interior",
                event="she maintains a composed editorial fashion pose",
                visual_priorities=(
                    "decadent elegance atmosphere",
                    "faded luxurious materials",
                    "composed adult poise",
                ),
                baseline_prompt_en=(
                    "An unmistakably adult fashion model holds a composed editorial pose inside a faded "
                    "salon, expressing decadent elegance through tarnished gold, bruised velvet, restrained "
                    "shadows, and weathered luxury without a character transformation."
                ),
                interpretations=(
                    {
                        "term": "타락한 우아함",
                        "source_text": "타락한 우아함",
                        "basis": "request_context",
                        "resolution": "a decadent elegance mood without an embodied identity transition",
                        "sources": [],
                    },
                ),
            ),
            creativity=0,
        )
        self.assertIsNone(self.obligation(elegance, "embodied_corruption_transition"))
        self.assertEqual(
            self.profile_clarification(elegance, "embodied_corruption_transition")["applicability"][
                "status"
            ],
            "context_mismatch",
        )

        mesugaki_source = "성인 메스가키 캐릭터의 도도하고 건방진 초상"
        mesugaki = self.run_current(
            self.core(
                mesugaki_source,
                interpreted_intent="An unmistakably adult rival with haughty smug poise and fresh youthful adult styling",
                subject="an unmistakably adult peer rival",
                setting="a clean competitive portrait studio",
                event="she holds a poised arrogant expression toward the camera",
                visual_priorities=(
                    "haughty facial baseline",
                    "smug adult poise",
                    "fresh youthful adult styling",
                ),
                baseline_prompt_en=(
                    "An unmistakably adult peer rival faces the camera with a raised brow, half-lidded "
                    "eyes, a cool superior smirk, poised arrogant bearing, and fresh youthful adult "
                    "styling while behavior, not childlike morphology, carries the archetype."
                ),
                interpretations=(
                    {
                        "term": "메스가키",
                        "source_text": "메스가키",
                        "basis": "agent_general_knowledge",
                        "resolution": "adult haughty smug poise with youthful adult styling",
                        "sources": [],
                    },
                ),
                runtime_forbidden_labels=("메스가키",),
                locked_dimensions=(
                    "concept",
                    "subject",
                    "event",
                    "role",
                    "expression",
                    "style",
                ),
                anchor_evidence=(
                    "behavior, not childlike morphology, carries the archetype",
                    "unmistakably adult peer rival",
                    "faces the camera with a raised brow",
                    "cool superior smirk",
                    "half-lidded eyes",
                    "fresh youthful adult styling",
                ),
            ),
            creativity=0,
        )
        status_play = self.obligation(mesugaki, "adult_mesugaki_status_play")
        self.assertIsNotNone(status_play)
        required = status_play["prompt_binding"]["required_evidence_fields"]
        self.assertIn("adult_youthful_styling_phrase", required)
        self.assertNotIn("small_setback_phrase", required)
        self.assertNotIn("warm_crack_phrase", required)
        self.assertIn("메스가키", status_play["runtime_expression"]["forbidden_prompt_terms"])

    def test_current_composition_audit_binds_core_and_rejects_copying(self):
        source = (
            "Photorealistic blue porcelain teacup still life in a quiet rainlit kitchen "
            "without people or bright sunlight"
        )
        pack = self.run_current(
            self.core(source, exclusions=("people", "bright sunlight")),
            seed=91,
            creativity=2,
        )
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
                "decision": "applied" if row.get("required_in_final_prompt") else "rejected",
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
            "chosen_visual_concept_ids": [],
            "authorial_core_binding": {
                "source_authorial_core_sha256": pack["authorial_core"]["canonical_sha256"],
                "source_intent_lock_sha256": pack["authorial_core"]["intent_lock"][
                    "canonical_sha256"
                ],
                "preserved_anchor_ids": [
                    row["anchor_id"]
                    for row in pack["authorial_core"]["intent_lock"]["semantic_anchors"]
                ],
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
        composed["embodiment_review"] = fixtures.composition_review(pack, composed["prompt_en"])
        audit = audit_composed_prompt.audit_composed_prompt(pack, composed)
        self.assertEqual(audit["status"], "pass", audit["failures"])

        render_request = {
            "schema_version": "photo-image-render-request/v2",
            "source_embodiment_preflight_sha256": pack["embodiment_preflight"]["canonical_sha256"],
            "pack_id": pack["pack_id"],
            "runtime_prompt_en": f"{prompt}\n\nAvoid: {pack['negative_en']}",
            "runtime_negative_en": pack["negative_en"],
            "source_intent_lock_sha256": pack["authorial_core"]["intent_lock"]["canonical_sha256"],
            "references": [],
            "audit_boundary": {
                "composed_prompt_audit_status": "pass",
                "runtime_prompt_audit_status": "not_run",
                "inherits_composed_prompt_pass": False,
            },
        }
        runtime_audit = audit_image_render_request.audit_image_render_request(
            pack,
            composed,
            render_request,
        )
        self.assertEqual(runtime_audit["status"], "pass", runtime_audit["failures"])
        unbound_render = copy.deepcopy(render_request)
        unbound_render.pop("source_intent_lock_sha256")
        unbound_audit = audit_image_render_request.audit_image_render_request(
            pack,
            composed,
            unbound_render,
        )
        self.assertIn(
            "source_intent_lock_sha256",
            {row["check"] for row in unbound_audit["failures"]},
        )

        missing_binding = copy.deepcopy(composed)
        missing_binding.pop("authorial_core_binding")
        missing_audit = audit_composed_prompt.audit_composed_prompt(pack, missing_binding)
        self.assertIn(
            "authorial_core_binding",
            {row["check"] for row in missing_audit["failures"]},
        )

        locked_change = copy.deepcopy(composed)
        locked_change["authorial_core_binding"]["authorial_decisions"][0]["dimension"] = "subject"
        locked_change_audit = audit_composed_prompt.audit_composed_prompt(
            pack,
            locked_change,
        )
        self.assertIn(
            "intent_lock_authorial_dimensions",
            {row["check"] for row in locked_change_audit["failures"]},
        )

        missing_anchor = copy.deepcopy(composed)
        missing_anchor["prompt_en"] = missing_anchor["prompt_en"].replace(
            "rainlit window reflections",
            "wet glass reflections",
        )
        missing_anchor_audit = audit_composed_prompt.audit_composed_prompt(
            pack,
            missing_anchor,
        )
        self.assertIn(
            "intent_lock_prompt_evidence",
            {row["check"] for row in missing_anchor_audit["failures"]},
        )

        superseded = copy.deepcopy(composed)
        core_decision = next(
            row
            for row in superseded["semantic_clarification_decisions"]
            if row["clarification_id"] == "clarification:authorial-core:interpreted-intent"
        )
        core_decision.update(
            {
                "decision": "superseded_by_revision",
                "revision_basis": "candidate_pack_clarification",
                "revised_meaning": "a materially different replacement concept authored after retrieval",
                "revision_source_ids": [pack["creative_augmentation"]["candidates"][0]["id"]],
                "prompt_evidence": "deliberate stillness around the handle",
            }
        )
        superseded_audit = audit_composed_prompt.audit_composed_prompt(
            pack,
            superseded,
        )
        self.assertTrue(
            "semantic_clarification_decisions"
            in {row["check"] for row in superseded_audit["failures"]}
        )

        mutated_pack = copy.deepcopy(pack)
        mutated_pack["provenance"]["retrieval_query"]["query_sha256"] = "0" * 64
        retrieval_failures = audit_composed_prompt.audit_authorial_core(
            mutated_pack,
            composed,
            prompt,
        )
        self.assertIn(
            "authorial_core_integrity",
            {row["check"] for row in retrieval_failures},
        )

        reordered_priority = copy.deepcopy(pack)
        reordered_priority["intent_preservation"]["priority_order"].reverse()
        priority_failures = audit_composed_prompt.audit_authorial_core(
            reordered_priority,
            composed,
            prompt,
        )
        self.assertIn(
            "intent_preservation_contract",
            {row["check"] for row in priority_failures},
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
                        "affected_dimensions": ["material"],
                    }
                )
        copied_audit = audit_composed_prompt.audit_composed_prompt(pack, copied)
        self.assertIn(
            "creative_augmentation_transform",
            {row["check"] for row in copied_audit["failures"]},
        )
        locked_creative = copy.deepcopy(copied)
        for decision in locked_creative["creative_augmentation_brief"]["decisions"]:
            if decision["candidate_id"] == candidate_id:
                decision["affected_dimensions"] = ["subject"]
        locked_creative_audit = audit_composed_prompt.audit_composed_prompt(
            pack,
            locked_creative,
        )
        self.assertIn(
            "intent_lock_creative_dimensions",
            {row["check"] for row in locked_creative_audit["failures"]},
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
            interpretations=(
                {
                    "term": "아헤가오",
                    "source_text": "아헤가오",
                    "basis": "agent_general_knowledge",
                    "resolution": "simultaneous upward eyes external tongue blush and tired release",
                    "sources": [],
                },
            ),
            runtime_forbidden_labels=("아헤가오",),
        )
        pack = self.run_current(core, creativity=0)
        retrieval_text, retrieval = prompt_generator.authorial_core_retrieval_text(
            pack["authorial_core"]
        )
        self.assertIn("아헤가오", retrieval_text)
        self.assertIn("upward-directed eyes", retrieval_text)
        self.assertIn("source_request_scope", retrieval["source_fields"])
        self.assertNotIn("source_request_scope", retrieval["redacted_source_fields"])
        self.assertEqual(retrieval["runtime_forbidden_label_count"], 1)
        self.assertEqual(pack["provenance"]["retrieval_query"], retrieval)
        decisions = []
        for row in pack["semantic_clarification"]["candidates"]:
            status = row["applicability"]["status"]
            decisions.append(
                {
                    "clarification_id": row["id"],
                    "decision": (
                        "rejected" if status == "requires_existing_adult_context" else "applied"
                    ),
                    "rationale": "respects contextual applicability",
                    "prompt_evidence": "upward-directed eyes",
                }
            )
        failures = audit_composed_prompt.audit_semantic_clarification(
            pack,
            {"semantic_clarification_decisions": decisions},
            "A portrait with upward-directed eyes, labeled 아헤가오.",
        )
        self.assertIn(
            "semantic_clarification_sensitive_label",
            {row["check"] for row in failures},
        )


if __name__ == "__main__":
    unittest.main()
