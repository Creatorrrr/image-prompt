from __future__ import annotations

import copy
import hashlib
import json
import random
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import audit_composed_prompt  # noqa: E402
import audit_image_render_request  # noqa: E402
import audit_image_render_review  # noqa: E402
import prompt_generator  # noqa: E402
import record_image_run  # noqa: E402


REQUEST = "같은 의미를 유지하면서 손에 든 주요 소품이 실제 소품처럼 보이도록 다시 만들어줘"
ACTOR = "the adult field engineer"
OBJECT = "one compact inspection lamp"
INTERACTION = (
    "the adult field engineer holds one compact inspection lamp by its rubber "
    "handle in her right hand"
)
RECOGNITION = (
    "one compact inspection lamp shows a cylindrical metal housing and a single glass lens"
)


def envelope(request_id: str = "repair-current") -> dict:
    return {
        "contract_version": "photo-request-envelope/v1",
        "provenance": "requesting_user",
        "request_id": request_id,
        "request_text": REQUEST,
        "request_sha256": hashlib.sha256(REQUEST.encode("utf-8")).hexdigest(),
        "active_spans": [
            {
                "span_id": "repair",
                "start": 0,
                "end": len(REQUEST),
                "text": REQUEST,
            }
        ],
    }


def repair_core(
    *,
    actor: str = ACTOR,
    object_phrase: str = OBJECT,
    interaction_phrase: str = INTERACTION,
    recognition_phrase: str = RECOGNITION,
    interaction_state: str = "held",
    contact: str = "required",
    relation_origin: str = "parent_preserved",
) -> dict:
    baseline = (
        "A documentary repair portrait shows the adult field engineer beside a cold "
        f"conduit at dusk. {interaction_phrase}. {recognition_phrase}. She checks the "
        "frozen seam while blue workshop light defines the object and contact clearly."
    )
    preserved = ["concept", "subject", "event"]
    allowed = ["framing", "composition", "lighting", "camera", "material"]
    if relation_origin == "parent_preserved":
        preserved.append("action")
    else:
        allowed.append("action")
    return {
        "contract_version": "photo-authorial-core/v3",
        "provenance": "agent_prepack",
        "source_request": REQUEST,
        "interpreted_intent": (
            "Preserve the intended adult actor and important prop interaction while "
            "repairing only its rendered fidelity"
        ),
        "subject": "one adult field engineer",
        "setting": "a cold industrial conduit bay at dusk",
        "event": "the engineer checks a frozen seam while using an inspection object",
        "visual_priorities": [
            "adult engineer remains the subject",
            "important object class stays legible",
            "intended hand interaction remains intact",
        ],
        "baseline_prompt_en": baseline,
        "user_definitions": [],
        "interpretation_provenance": [
            {
                "term": "same-meaning prop fidelity retry",
                "source_text": REQUEST,
                "basis": "request_context",
                "resolution": (
                    "retain the parent actor-object relation and improve only the visible object and contact fidelity"
                    if relation_origin == "parent_preserved"
                    else "freeze the requester's explicit correction of the parent actor-object relation"
                ),
                "sources": [],
            }
        ],
        "unresolved_ambiguities": [],
        "user_exclusions": [],
        "runtime_forbidden_labels": [],
        "intent_lock": {
            "contract_version": "photo-intent-lock/v1",
            "priority": "requesting_user",
            "semantic_anchors": [
                {
                    "anchor_id": "concept",
                    "source_text": REQUEST,
                    "dimension": "concept",
                    "prompt_evidence": "A documentary repair portrait",
                },
                {
                    "anchor_id": "subject",
                    "source_text": REQUEST,
                    "dimension": "subject",
                    "prompt_evidence": "the adult field engineer beside a cold conduit",
                },
                {
                    "anchor_id": "event",
                    "source_text": REQUEST,
                    "dimension": "event",
                    "prompt_evidence": "She checks the frozen seam",
                },
                {
                    "anchor_id": "action",
                    "source_text": REQUEST,
                    "dimension": "action",
                    "prompt_evidence": interaction_phrase,
                },
            ],
            "locked_dimensions": ["concept", "subject", "event", "action"],
            "open_dimensions": [
                "framing",
                "composition",
                "lighting",
                "camera",
                "material",
            ],
        },
        "semantic_assertions": [
            {
                "assertion_id": "important_prop_interaction",
                "dimension": "action",
                "polarity": "required",
                "source_span_ids": ["repair"],
                "affected_dimensions": ["action"],
                "axes": {
                    "interaction_state": interaction_state,
                    "actor_object_contact": contact,
                    "object_importance": "supporting",
                },
                "evidence": {
                    "interaction_phrase": interaction_phrase,
                    "recognition_phrase": recognition_phrase,
                },
            }
        ],
        "request_lineage": {
            "contract_version": "photo-request-lineage/v2",
            "parent_request_id": "repair-parent",
            "parent_core_sha256": "a" * 64,
            "preserved_dimensions": preserved,
            "allowed_changes": allowed,
            "repair_targets": [
                {
                    "repair_id": "important_prop",
                    "source_span_ids": ["repair"],
                    "importance": "supporting",
                    "relation_origin": relation_origin,
                    "actor_phrase": actor,
                    "object_phrase": object_phrase,
                    "interaction_state": interaction_state,
                    "actor_object_contact": contact,
                    "protected_dimensions": ["action"],
                    "allowed_repair_axes": [
                        "object_geometry",
                        "contact_geometry",
                        "local_pose",
                        "camera",
                        "framing",
                        "lighting",
                        "material",
                    ],
                    "interaction_phrase": interaction_phrase,
                    "recognition_phrase": recognition_phrase,
                }
            ],
        },
        "style": {
            "domain": "documentary_portrait",
            "family": "restrained industrial editorial",
            "evidence": ["documentary repair portrait", "blue workshop light"],
        },
        "variation_key": "generic-render-repair-test",
    }


def normalized_core(**kwargs: object) -> dict:
    normalized_envelope = prompt_generator.normalize_request_envelope(envelope())
    return prompt_generator.normalize_authorial_core(
        repair_core(**kwargs),
        request_envelope=normalized_envelope,
    )


def pack_and_composed(core: dict) -> tuple[dict, dict]:
    contract = prompt_generator.compile_render_repair_contract(core)
    assert contract is not None
    pack = {
        "pack_id": "b" * 16,
        "authorial_core": core,
        "render_repair": contract,
        "negative_en": None,
    }
    composed = {
        "pack_id": pack["pack_id"],
        "prompt_en": core["baseline_prompt_en"],
        "negative_en": None,
        "render_repair_evidence": {
            "source_contract_sha256": contract["canonical_sha256"],
            "evidence": {
                target["repair_id"]: copy.deepcopy(target["frozen_evidence"])
                for target in contract["targets"]
            },
        },
    }
    return pack, composed


class PhotoRenderRepairTests(unittest.TestCase):
    def test_v2_lineage_compiles_generic_prompt_and_pixel_contract(self):
        core = normalized_core()
        self.assertTrue(
            audit_composed_prompt.authorial_core_v3_semantic_contract_valid(core)
        )
        lineage = core["request_lineage"]
        self.assertEqual(lineage["contract_version"], "photo-request-lineage/v2")
        self.assertRegex(lineage["canonical_sha256"], r"^[0-9a-f]{64}$")
        contract = prompt_generator.compile_render_repair_contract(core)
        self.assertIsNotNone(contract)
        assert contract is not None
        self.assertEqual(contract["contract_version"], "photo-render-repair/v1")
        self.assertEqual(
            contract["targets"][0]["relation_origin"], "parent_preserved"
        )
        self.assertEqual(len(contract["required_hard_gates"]), 4)
        self.assertTrue(
            contract["retry_policy"][
                "removal_relocation_concealment_or_transfer_is_not_repair"
            ]
        )

        tampered_lineage = copy.deepcopy(core)
        tampered_lineage["request_lineage"]["repair_targets"][0][
            "interaction_phrase"
        ] = "the object is moved to a wall rack"
        self.assertFalse(
            audit_composed_prompt.authorial_core_v3_semantic_contract_valid(
                tampered_lineage
            )
        )

    def test_requester_corrected_relation_is_frozen_after_parent_change(self):
        core = normalized_core(relation_origin="requester_corrected")
        lineage = core["request_lineage"]
        self.assertIn("action", lineage["allowed_changes"])
        self.assertNotIn("action", lineage["preserved_dimensions"])
        self.assertEqual(
            lineage["repair_targets"][0]["relation_origin"],
            "requester_corrected",
        )

        wrong_origin = repair_core(relation_origin="requester_corrected")
        wrong_origin["request_lineage"]["repair_targets"][0][
            "relation_origin"
        ] = "parent_preserved"
        with self.assertRaisesRegex(ValueError, "declared relation origin"):
            prompt_generator.normalize_authorial_core(
                wrong_origin,
                request_envelope=prompt_generator.normalize_request_envelope(
                    envelope()
                ),
            )

    def test_lineage_requires_locked_action_and_one_assertion_owning_both_phrases(self):
        missing_action = repair_core()
        missing_action["intent_lock"]["locked_dimensions"].remove("action")
        missing_action["intent_lock"]["semantic_anchors"] = [
            row
            for row in missing_action["intent_lock"]["semantic_anchors"]
            if row["dimension"] != "action"
        ]
        missing_action["intent_lock"]["open_dimensions"].append("action")
        with self.assertRaisesRegex(ValueError, "must affect only locked dimensions"):
            prompt_generator.normalize_authorial_core(
                missing_action,
                request_envelope=prompt_generator.normalize_request_envelope(
                    envelope()
                ),
            )

        split_assertions = repair_core()
        first = split_assertions["semantic_assertions"][0]
        first["evidence"] = {"interaction_phrase": INTERACTION}
        second = copy.deepcopy(first)
        second["assertion_id"] = "object_recognition_only"
        second["evidence"] = {"recognition_phrase": RECOGNITION}
        split_assertions["semantic_assertions"].append(second)
        with self.assertRaisesRegex(ValueError, "through one required action"):
            prompt_generator.normalize_authorial_core(
                split_assertions,
                request_envelope=prompt_generator.normalize_request_envelope(
                    envelope()
                ),
            )

        absent_contact = repair_core(contact="absent")
        with self.assertRaisesRegex(ValueError, "cannot remove actor-object contact"):
            prompt_generator.normalize_authorial_core(
                absent_contact,
                request_envelope=prompt_generator.normalize_request_envelope(
                    envelope()
                ),
            )

    def test_legacy_lineage_shape_remains_unchanged(self):
        legacy = repair_core()
        legacy["request_lineage"] = {
            "parent_request_id": "repair-parent",
            "parent_core_sha256": "a" * 64,
            "preserved_dimensions": ["concept", "subject", "event", "action"],
            "allowed_changes": ["framing", "lighting"],
        }
        normalized = prompt_generator.normalize_authorial_core(
            legacy,
            request_envelope=prompt_generator.normalize_request_envelope(envelope()),
        )
        self.assertEqual(normalized["request_lineage"], legacy["request_lineage"])
        self.assertIsNone(prompt_generator.compile_render_repair_contract(normalized))

    def test_composed_audit_recomputes_contract_and_rejects_evasive_prompt(self):
        core = normalized_core()
        pack, composed = pack_and_composed(core)
        self.assertEqual(
            audit_composed_prompt.audit_render_repair_v6(
                pack, composed, composed["prompt_en"]
            ),
            [],
        )

        moved_away = copy.deepcopy(composed)
        moved_away["prompt_en"] = moved_away["prompt_en"].replace(
            f"{INTERACTION}.", "The object hangs on a distant wall rack."
        )
        moved_failures = audit_composed_prompt.audit_render_repair_v6(
            pack, moved_away, moved_away["prompt_en"]
        )
        self.assertIn(
            "render_repair_evidence", {row["check"] for row in moved_failures}
        )

        tampered = copy.deepcopy(composed)
        tampered["render_repair_evidence"]["evidence"]["important_prop"][
            "recognition_phrase"
        ] = "a vague distant accessory"
        self.assertIn(
            "render_repair_evidence",
            {
                row["check"]
                for row in audit_composed_prompt.audit_render_repair_v6(
                    pack, tampered, composed["prompt_en"]
                )
            },
        )

        missing_contract = copy.deepcopy(pack)
        missing_contract.pop("render_repair")
        self.assertIn(
            "render_repair_contract",
            {
                row["check"]
                for row in audit_composed_prompt.audit_render_repair_v6(
                    missing_contract, composed, composed["prompt_en"]
                )
            },
        )

    def test_runtime_request_requires_exact_repair_contract_hash(self):
        core = normalized_core()
        pack, composed = pack_and_composed(core)
        contract_sha = pack["render_repair"]["canonical_sha256"]
        request = {
            "schema_version": "photo-image-render-request/v2",
            "pack_id": pack["pack_id"],
            "source_intent_lock_sha256": core["intent_lock"]["canonical_sha256"],
            "render_repair_contract_sha256": contract_sha,
            "runtime_prompt_en": composed["prompt_en"],
            "runtime_negative_en": None,
            "references": [],
            "audit_boundary": {
                "composed_prompt_audit_status": "pass",
                "runtime_prompt_audit_status": "not_run",
                "inherits_composed_prompt_pass": False,
            },
        }
        passed = audit_image_render_request.audit_image_render_request(
            pack, composed, request
        )
        self.assertNotIn(
            "render_repair_contract_sha256",
            {row["check"] for row in passed["failures"]},
        )

        missing = copy.deepcopy(request)
        missing.pop("render_repair_contract_sha256")
        failed = audit_image_render_request.audit_image_render_request(
            pack, composed, missing
        )
        self.assertIn(
            "render_repair_contract_sha256",
            {row["check"] for row in failed["failures"]},
        )

    def test_render_review_requires_exact_major_gate_set_and_image_hash(self):
        core = normalized_core()
        pack, composed = pack_and_composed(core)
        with tempfile.TemporaryDirectory() as tmp:
            image_path = Path(tmp) / "candidate.png"
            image_path.write_bytes(b"generic-render-repair-pixels")
            image_sha = hashlib.sha256(image_path.read_bytes()).hexdigest()
            review = {
                "schema_version": "photo-image-render-review/v1",
                "pack_id": pack["pack_id"],
                "source_render_repair_contract_sha256": pack["render_repair"][
                    "canonical_sha256"
                ],
                "result": {"path": str(image_path), "sha256": image_sha},
                "reviewer": {
                    "reviewer_id": "unit-test-pixel-reviewer",
                    "method": "direct_pixel_inspection",
                },
                "gates": [
                    {
                        "gate_id": gate["id"],
                        "status": "pass",
                        "reviewed_scales": (
                            ["thumbnail", "native"]
                            if gate["review_scale"] == "both"
                            else [gate["review_scale"]]
                        ),
                        "evidence": "Major geometry and interaction are visibly coherent.",
                    }
                    for gate in pack["render_repair"]["targets"][0][
                        "render_gates"
                    ]
                ],
            }
            passed = audit_image_render_review.audit_image_render_review(
                pack, composed, review
            )
            self.assertEqual(passed["status"], "pass", passed)
            self.assertTrue(passed["technical_qualified"], passed)

            failed_gate = copy.deepcopy(review)
            failed_gate["gates"][2]["status"] = "fail"
            failed_gate["gates"][2]["evidence"] = (
                "The object is no longer held by the intended actor."
            )
            failed = audit_image_render_review.audit_image_render_review(
                pack, composed, failed_gate
            )
            self.assertEqual(failed["status"], "pass", failed)
            self.assertFalse(failed["technical_qualified"])
            self.assertEqual(failed["failed_gate_ids"], [review["gates"][2]["gate_id"]])

            extra = copy.deepcopy(review)
            extra["gates"].append(
                {
                    "gate_id": "invented_gate",
                    "status": "pass",
                    "reviewed_scales": ["native"],
                    "evidence": "Invented supplemental evidence should not qualify.",
                }
            )
            extra_result = audit_image_render_review.audit_image_render_review(
                pack, composed, extra
            )
            self.assertEqual(extra_result["status"], "fail")
            self.assertIn(
                "gate_set", {row["check"] for row in extra_result["failures"]}
            )

            wrong_hash = copy.deepcopy(review)
            wrong_hash["result"]["sha256"] = "0" * 64
            wrong_hash_result = audit_image_render_review.audit_image_render_review(
                pack, composed, wrong_hash
            )
            self.assertEqual(wrong_hash_result["status"], "fail")
            self.assertIn(
                "result.sha256",
                {row["check"] for row in wrong_hash_result["failures"]},
            )

    def test_object_agnostic_contract_handles_multiple_interaction_families(self):
        fixtures = [
            (
                "one black umbrella",
                "the adult field engineer holds one black umbrella by its curved handle in her right hand",
                "one black umbrella shows a central shaft, radial ribs, and a taut canopy",
                "held",
                "required",
                4,
            ),
            (
                "one handheld microphone",
                "the adult field engineer uses one handheld microphone near her mouth with a steady grip",
                "one handheld microphone shows one mesh capsule and one continuous tapered body",
                "used",
                "required",
                4,
            ),
            (
                "one ceramic cup",
                "the adult field engineer hands one ceramic cup to the adult survey partner",
                "one ceramic cup shows a round rim, hollow bowl, and a single curved handle",
                "handed_off",
                "transitional",
                4,
            ),
            (
                "one adjustable wrench",
                "the adult field engineer carries one adjustable wrench by its solid handle at her side",
                "one adjustable wrench shows one fixed jaw, one moving jaw, and one continuous steel handle",
                "carried",
                "required",
                4,
            ),
            (
                "one compact inspection lamp",
                "the adult field engineer observes one compact inspection lamp mounted on a tripod bracket",
                "one compact inspection lamp shows a cylindrical metal housing and a single glass lens",
                "mounted",
                "absent",
                3,
            ),
        ]
        for (
            object_phrase,
            interaction_phrase,
            recognition_phrase,
            state,
            contact,
            gate_count,
        ) in fixtures:
            with self.subTest(object_phrase=object_phrase, state=state):
                core = normalized_core(
                    object_phrase=object_phrase,
                    interaction_phrase=interaction_phrase,
                    recognition_phrase=recognition_phrase,
                    interaction_state=state,
                    contact=contact,
                )
                contract = prompt_generator.compile_render_repair_contract(core)
                assert contract is not None
                self.assertEqual(len(contract["required_hard_gates"]), gate_count)

    def test_v6_candidate_pack_exposes_recomputed_repair_contract(self):
        core = normalized_core()
        assets = SKILL_DIR / "assets"
        data = prompt_generator.load_json(assets / "photo_prompt_tags.json")
        data[prompt_generator.QUALITY_LAYERS_DATA_KEY] = (
            prompt_generator.load_quality_layers(
                assets / "photo_prompt_quality_layers.json"
            )
        )
        registry = prompt_generator.load_visual_obligation_registry(
            assets / "photo_prompt_visual_obligations.json"
        )
        data[prompt_generator.VISUAL_OBLIGATIONS_DATA_KEY] = registry
        data[prompt_generator.VISUAL_PROFILE_INDEX_DATA_KEY] = (
            prompt_generator.load_visual_profile_index(
                assets / "photo_prompt_visual_profile_index.json", registry
            )
        )
        data[prompt_generator.SEMANTIC_INDEX_DATA_KEY] = (
            prompt_generator.load_semantic_index_payload(
                assets / "photo_prompt_semantic_index.json"
            )
        )
        result = prompt_generator.generate_once(
            data,
            random.Random(1919),
            "character_attribute_composition_scene",
            ["en"],
            True,
            12,
            True,
            selection_mode="rule",
            include_trace=True,
            concept_locks=[REQUEST],
            seed=1919,
            creativity=0.0,
            authorial_core=core,
        )
        pack = prompt_generator.build_candidate_pack(result, data, "v6")
        self.assertEqual(pack["contract_version"], "photo-candidate-pack/v6")
        self.assertEqual(
            pack["render_repair"],
            prompt_generator.compile_render_repair_contract(core),
        )

    def test_modern_independent_manifest_preserves_repair_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            image_path = Path(tmp) / "candidate.png"
            image_path.write_bytes(b"recorded-pixels")
            args = record_image_run.parse_args(
                [
                    "--ts",
                    "2026-08-19T12:00:00+09:00",
                    "--prompt-en",
                    "An audited modern independent render-repair prompt.",
                    "--attempt",
                    "1",
                    "--status",
                    "success",
                    "--image-path",
                    str(image_path),
                    "--pack-id",
                    "c" * 16,
                    "--arm-id",
                    "repair-arm",
                    "--worktree-id",
                    "isolated-repair-arm",
                    "--skill-sha256",
                    "d" * 64,
                    "--source-ref",
                    "e" * 40,
                    "--candidate-pack-version",
                    "v6",
                    "--authorial-core-sha256",
                    "f" * 64,
                    "--intent-lock-sha256",
                    "1" * 64,
                    "--render-repair-contract-sha256",
                    "2" * 64,
                    "--failed-repair-gate-id",
                    "rr_important_prop_intended_interaction_matches",
                    "--reference-sha256",
                    "3" * 64,
                    "--image-call-count",
                    "1",
                    "--independent-no-cross-arm-inputs",
                ]
            )
            entry = record_image_run.build_entry(args)
            manifest = record_image_run.build_independent_manifest(entry, args)
            self.assertEqual(
                manifest["contract_version"],
                "photo-independent-run-manifest/v2",
            )
            self.assertEqual(manifest["authorial_core_sha256"], "f" * 64)
            self.assertEqual(manifest["intent_lock_sha256"], "1" * 64)
            self.assertEqual(
                manifest["render_repair_contract_sha256"], "2" * 64
            )
            self.assertEqual(
                manifest["failed_repair_gate_ids"],
                ["rr_important_prop_intended_interaction_matches"],
            )
            schema = json.loads(
                (SKILL_DIR / "assets" / "run_ledger.schema.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertFalse(set(entry) - set(schema["properties"]))


if __name__ == "__main__":
    unittest.main()
