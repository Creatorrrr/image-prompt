from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
REGISTRY_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_obligations.json"
WRAPPER_PATH = SCRIPT_DIR / "generate_photo_prompt.py"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import audit_composed_prompt  # noqa: E402
import prompt_generator  # noqa: E402


def valid_core() -> dict:
    return {
        "contract_version": "photo-authorial-core/v1",
        "provenance": "agent_prepack",
        "source_request": "A cloud bread editorial still life with a quiet morning atmosphere",
        "interpreted_intent": (
            "A quiet editorial still life translating cloud bread into airy hand-shaped food"
        ),
        "subject": "one airy hand-shaped bread loaf",
        "setting": "a quiet morning bakery counter",
        "event": "soft steam rises while crumbs settle beside the loaf",
        "visual_priorities": ["airy bread structure", "quiet morning light"],
        "baseline_prompt_en": (
            "An airy hand-shaped bread loaf rests on a pale bakery counter while soft steam rises, "
            "fine crumbs settle beside it, quiet morning light reveals the porous structure, and a "
            "restrained editorial frame keeps every tactile detail calm and legible. Fine-grained "
            "surface cues, coherent depth, controlled highlights, and quiet shadow detail keep the "
            "completed photographic hierarchy specific, balanced, natural, and visually unambiguous."
        ),
        "user_definitions": [],
        "interpretation_provenance": [
            {
                "term": "cloud bread",
                "source_text": "cloud bread",
                "basis": "public_web_research",
                "resolution": "an airy hand-shaped bread with porous structure",
                "sources": ["https://example.org/reference/cloud-bread"],
            }
        ],
        "unresolved_ambiguities": [],
        "user_exclusions": ["people"],
        "style": {
            "domain": "general_photo",
            "family": "restrained editorial still life",
            "evidence": ["quiet morning light", "tactile porous detail"],
        },
        "variation_key": "prepack-isolation-test",
    }


class PhotoPrepackIsolationV5Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def test_skill_procedure_contains_no_registry_keyword_knowledge(self):
        skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").casefold()
        forbidden_literals: set[str] = set()
        for profile in self.registry.get("profiles") or []:
            forbidden_literals.add(str(profile.get("id") or "").casefold())
            activation = profile.get("activation") or {}
            for field in ("exact_terms", "project_glossary_aliases"):
                forbidden_literals.update(
                    str(term).strip().casefold()
                    for term in activation.get(field) or []
                    if str(term).strip()
                )
            runtime = profile.get("runtime_expression") or {}
            forbidden_literals.update(
                str(term).strip().casefold()
                for term in runtime.get("forbidden_prompt_terms") or []
                if str(term).strip()
            )
        leaked = sorted(term for term in forbidden_literals if term and term in skill_text)
        self.assertEqual(leaked, [])
        self.assertLess(
            skill_text.index("phase 1 — write and freeze"),
            skill_text.index("phase 2 — retrieve"),
        )
        self.assertIn(
            "the `skill.md` procedure is the only project-local material available before the core",
            skill_text,
        )

    def test_core_requires_a_resolved_ambiguity_boundary_and_auditable_web_basis(self):
        raw = valid_core()
        normalized = prompt_generator.normalize_authorial_core(raw)
        self.assertEqual(normalized["unresolved_ambiguities"], [])
        self.assertTrue(
            audit_composed_prompt.authorial_core_interpretation_contract_valid(normalized)
        )
        retrieval_text, provenance = prompt_generator.authorial_core_retrieval_text(normalized)
        self.assertIn("an airy hand-shaped bread with porous structure", retrieval_text)
        self.assertNotIn("https://example.org", retrieval_text)
        self.assertIn("interpretation_resolution", provenance["source_fields"])

        missing_boundary = copy.deepcopy(raw)
        missing_boundary.pop("unresolved_ambiguities")
        with self.assertRaisesRegex(ValueError, "requires unresolved_ambiguities"):
            prompt_generator.normalize_authorial_core(missing_boundary)

        unresolved = copy.deepcopy(raw)
        unresolved["unresolved_ambiguities"] = ["whether cloud names food or weather"]
        with self.assertRaisesRegex(ValueError, "ask the requester or research"):
            prompt_generator.normalize_authorial_core(unresolved)

        unsourced_web = copy.deepcopy(raw)
        unsourced_web["interpretation_provenance"][0]["sources"] = []
        with self.assertRaisesRegex(ValueError, "requires at least one HTTP"):
            prompt_generator.normalize_authorial_core(unsourced_web)

    def test_visual_intent_profile_resolution_occurs_without_a_precore_profile_id(self):
        source_text = "성인 여성의 절대공역 사진"
        normalized = prompt_generator.normalize_visual_intent(
            {
                "contract_version": "photo-visual-intent/v1",
                "provenance": "agent_prepack",
                "obligations": [
                    {
                        "source": "explicit_user_requirement",
                        "scope": "request_only",
                        "source_text": source_text,
                        "bindings": {},
                    }
                ],
            },
            self.registry,
        )
        self.assertEqual(
            normalized["obligations"][0]["profile_id"],
            "inner_thigh_negative_space",
        )

        unknown = copy.deepcopy(normalized)
        unknown.pop("canonical_sha256")
        unknown.pop("request_id")
        unknown["obligations"][0].pop("profile_id")
        unknown["obligations"][0]["source_text"] = "unregistered exact geometry"
        with self.assertRaisesRegex(ValueError, "resolve exactly one"):
            prompt_generator.normalize_visual_intent(unknown, self.registry)

        ambiguous = copy.deepcopy(unknown)
        ambiguous["obligations"][0]["source_text"] = "절대공역과 아헤가오"
        with self.assertRaisesRegex(ValueError, "matched"):
            prompt_generator.normalize_visual_intent(ambiguous, self.registry)

        context_mismatch = copy.deepcopy(unknown)
        context_mismatch["obligations"][0]["source_text"] = "타락한 우아함"
        with self.assertRaisesRegex(ValueError, r"matched \[\]"):
            prompt_generator.normalize_visual_intent(context_mismatch, self.registry)

    def test_public_v5_flow_resolves_profile_only_after_receiving_a_frozen_core(self):
        source_text = "성인 여성의 절대공역 사진"
        core = {
            "contract_version": "photo-authorial-core/v2",
            "provenance": "agent_prepack",
            "source_request": source_text,
            "interpreted_intent": (
                "An adult fashion portrait centered on deliberate negative-space leg geometry"
            ),
            "subject": "one unmistakably adult woman",
            "setting": "a quiet neutral fashion studio",
            "event": "she brings her legs close while holding a balanced standing pose",
            "visual_priorities": [
                "deliberate negative-space geometry",
                "clear adult fashion agency",
            ],
            "baseline_prompt_en": (
                "An unmistakably adult woman stands in a quiet neutral fashion studio, bringing "
                "her legs close in a balanced self-directed pose while a narrow background opening "
                "between the upper inner-thigh contours becomes deliberate focal geometry under "
                "clean soft light and restrained editorial framing. Fine-grained surface cues, "
                "coherent depth, controlled highlights, and quiet shadow detail keep the completed "
                "photographic hierarchy specific, balanced, natural, and visually unambiguous."
            ),
            "user_definitions": [],
            "interpretation_provenance": [
                {
                    "term": "절대공역",
                    "source_text": "절대공역",
                    "basis": "agent_general_knowledge",
                    "resolution": "deliberate negative space bounded by close inner thighs",
                    "sources": [],
                }
            ],
            "unresolved_ambiguities": [],
            "user_exclusions": [],
            "runtime_forbidden_labels": ["절대공역"],
            "intent_lock": {
                "contract_version": "photo-intent-lock/v1",
                "priority": "requesting_user",
                "semantic_anchors": [
                    {
                        "anchor_id": "core_concept",
                        "source_text": "절대공역",
                        "dimension": "concept",
                        "prompt_evidence": "narrow background opening between the upper inner-thigh contours",
                    },
                    {
                        "anchor_id": "core_subject",
                        "source_text": "절대공역",
                        "dimension": "subject",
                        "prompt_evidence": "unmistakably adult woman",
                    },
                    {
                        "anchor_id": "core_event",
                        "source_text": "절대공역",
                        "dimension": "event",
                        "prompt_evidence": "bringing her legs close in a balanced self-directed pose",
                    },
                ],
                "locked_dimensions": ["concept", "subject", "event"],
                "open_dimensions": [
                    "framing",
                    "composition",
                    "lighting",
                    "camera",
                ],
            },
            "style": {
                "domain": "general_photo",
                "family": "restrained adult fashion editorial",
                "evidence": ["clean soft light", "restrained editorial framing"],
            },
            "variation_key": "postcore-profile-resolution",
        }
        envelope = {
            "contract_version": "photo-request-envelope/v1",
            "provenance": "requesting_user",
            "request_id": "postcore-profile-resolution",
            "request_text": source_text,
            "request_sha256": hashlib.sha256(source_text.encode("utf-8")).hexdigest(),
            "active_spans": [
                {
                    "span_id": "topic",
                    "start": 0,
                    "end": len(source_text),
                    "text": source_text,
                }
            ],
        }
        visual_intent = {
            "contract_version": "photo-visual-intent/v1",
            "provenance": "agent_prepack",
            "obligations": [
                {
                    "source": "explicit_user_requirement",
                    "scope": "request_only",
                    "source_text": source_text,
                    "bindings": {},
                }
            ],
        }
        completed = subprocess.run(
            [
                sys.executable,
                str(WRAPPER_PATH),
                "--selection-mode",
                "rule",
                "--seed",
                "19",
                "--emit-candidate-pack",
                "--candidate-pack-version",
                "v5",
                "--request-envelope-json",
                json.dumps(envelope, ensure_ascii=False),
                "--authorial-core-json",
                json.dumps(core, ensure_ascii=False),
                "--visual-intent-json",
                json.dumps(visual_intent, ensure_ascii=False),
                "--creativity",
                "0",
                "--n",
                "1",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        pack = json.loads(completed.stdout)[0]
        self.assertEqual(
            pack["visual_intent"]["obligations"][0]["profile_id"],
            "inner_thigh_negative_space",
        )
        self.assertEqual(
            pack["visual_intent"]["canonical_sha256"],
            pack["visual_obligations"]["source_visual_intent_sha256"],
        )

    def test_authorial_fields_may_disambiguate_but_cannot_hard_activate_profiles(self):
        rows = [
            {
                "source": "authorial_core_baseline",
                "text": "성인 여성의 절대공역 사진",
                "polarity": "advisory",
            }
        ]
        self.assertEqual(
            prompt_generator.candidate_pack_auto_visual_obligation_matches(
                self.registry,
                rows,
            ),
            {},
        )

    def test_only_agent_hypothesis_accepts_a_pack_cited_typed_revision(self):
        core_id = "clarification:authorial-core:interpreted-intent"
        user_id = "clarification:user-definition:immutable"
        creative_id = "slot:lighting:fog-refraction"
        pack = {
            "semantic_clarification": {
                "contract_version": "photo-semantic-clarification/v1",
                "affected_by_creativity": False,
                "affected_by_seed": False,
                "candidates": [
                    {
                        "id": core_id,
                        "source": "agent_prepack_interpretation",
                        "interpreted_meaning": "a quiet blue porcelain domestic study",
                        "applicability": {"status": "review_required"},
                        "required_in_final_prompt": False,
                        "revisable": True,
                    },
                    {
                        "id": user_id,
                        "source": "requesting_user_definition",
                        "interpreted_meaning": "the requester's exact visible definition",
                        "required_prompt_evidence": "soft steam rises beside the loaf",
                        "applicability": {"status": "required"},
                        "required_in_final_prompt": True,
                        "revisable": False,
                    },
                ],
            },
            "creative_augmentation": {"candidates": [{"id": creative_id}]},
        }
        prompt = (
            "Tactile fog curls around fractured amber glass while soft steam rises beside the loaf."
        )
        composed = {
            "semantic_clarification_decisions": [
                {
                    "clarification_id": core_id,
                    "decision": "superseded_by_revision",
                    "revision_basis": "candidate_pack_clarification",
                    "revision_source_ids": [creative_id],
                    "revised_meaning": "an amber material study shaped by refracted fog",
                    "rationale": "pack context resolves the material relationship",
                    "prompt_evidence": "Tactile fog curls around fractured amber glass",
                },
                {
                    "clarification_id": user_id,
                    "decision": "applied",
                    "rationale": "requester definition remains governing",
                    "prompt_evidence": "soft steam rises beside the loaf",
                },
            ]
        }
        self.assertEqual(
            audit_composed_prompt.audit_semantic_clarification_v5(
                pack,
                composed,
                prompt,
            ),
            [],
        )

        illegal = copy.deepcopy(composed)
        illegal["semantic_clarification_decisions"][1].update(
            {
                "decision": "superseded_by_revision",
                "revision_basis": "candidate_pack_clarification",
                "revision_source_ids": [creative_id],
                "revised_meaning": "an agent replacement for the requester definition",
            }
        )
        failures = audit_composed_prompt.audit_semantic_clarification_v5(
            pack,
            illegal,
            prompt,
        )
        self.assertIn(
            "semantic_clarification_revision",
            {row["check"] for row in failures},
        )


if __name__ == "__main__":
    unittest.main()
