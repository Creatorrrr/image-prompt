from __future__ import annotations

import copy
import ast
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
from tests import photo_prompt_fixtures as fixtures


def valid_core() -> dict:
    raw = {
        "contract_version": "photo-authorial-core/v3",
        "provenance": "agent_prepack",
        "source_request": "A cloud bread editorial still life with a quiet morning atmosphere without people",
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

    current = fixtures.core(raw["source_request"], baseline_prompt_en=raw["baseline_prompt_en"])
    current.update(raw)
    current["contract_version"] = "photo-authorial-core/v3"
    return current


def normalize_core(raw):
    return prompt_generator.normalize_authorial_core(
        raw,
        request_envelope=prompt_generator.normalize_request_envelope(
            fixtures.envelope(raw["source_request"])
        ),
    )


class PhotoPrepackIsolationTests(unittest.TestCase):
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
            "the `skill.md` procedure, the named neutral catalog, and the named creative-control definition/resolver are the only project-local material available before the core",
            skill_text,
        )
        self.assertIn(
            "`precore/visual_feature_catalog.json`, only in phase 1 after resolving the request's meaning",
            skill_text,
        )
        self.assertIn(
            "any file under this skill's `assets/`, `references/`, or `scripts/` directories",
            skill_text,
        )
        precore_dir = SKILL_DIR / "precore"
        self.assertEqual(
            {
                path.name
                for path in precore_dir.iterdir()
                if path.name not in {".DS_Store", "__pycache__"}
            },
            {"visual_feature_catalog.json", "creative_controls.json", "creative_controls.py"},
        )
        resolver = (precore_dir / "creative_controls.py").read_text(encoding="utf-8")
        imports = set()
        for node in ast.walk(ast.parse(resolver)):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add((node.module or "").split(".")[0])
        self.assertLessEqual(
            imports,
            {
                "__future__",
                "argparse",
                "copy",
                "hashlib",
                "json",
                "math",
                "pathlib",
                "random",
                "secrets",
                "re",
            },
        )
        self.assertNotIn("assets/", resolver)
        self.assertNotIn("scripts/", resolver)
        catalog_text = (
            (precore_dir / "visual_feature_catalog.json").read_text(encoding="utf-8").casefold()
        )
        profile_ids = {
            str(profile.get("id") or "").casefold()
            for profile in self.registry.get("profiles") or []
        }
        profile_index = prompt_generator.load_visual_profile_index_payload(
            SKILL_DIR / "assets" / "photo_prompt_visual_profile_index.json"
        )
        profile_ids.update(str(profile_id).casefold() for profile_id in profile_index["entries"])
        self.assertEqual(
            sorted(
                profile_id
                for profile_id in profile_ids
                if profile_id and profile_id in catalog_text
            ),
            [],
        )
        controls_text = (
            (precore_dir / "creative_controls.json").read_text(encoding="utf-8").casefold()
        )
        self.assertEqual(
            [
                profile_id
                for profile_id in profile_ids
                if profile_id and profile_id in controls_text
            ],
            [],
        )

    def test_core_requires_a_resolved_ambiguity_boundary_and_auditable_web_basis(self):
        raw = valid_core()
        normalized = normalize_core(raw)
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
            normalize_core(missing_boundary)

        unresolved = copy.deepcopy(raw)
        unresolved["unresolved_ambiguities"] = ["whether cloud names food or weather"]
        with self.assertRaisesRegex(ValueError, "ask the requester or research"):
            normalize_core(unresolved)

        unsourced_web = copy.deepcopy(raw)
        unsourced_web["interpretation_provenance"][0]["sources"] = []
        with self.assertRaisesRegex(ValueError, "requires at least one HTTP"):
            normalize_core(unsourced_web)

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

    def test_public_current_flow_resolves_profile_only_after_receiving_a_frozen_core(self):
        source_text = "성인 여성의 절대공역 사진"
        core = {
            "contract_version": "photo-authorial-core/v3",
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
                "contract_version": "photo-intent-lock/v2",
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
        core["semantic_assertions"] = []
        core["request_lineage"] = None
        pack = fixtures.run_current(
            core,
            seed=19,
            creativity=0,
            envelope_input=envelope,
            extra_args=("--visual-intent-json", json.dumps(visual_intent)),
        )
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

    def test_frozen_core_revision_decisions_are_rejected(self):
        pack = {
            "semantic_clarification": {
                "candidates": [
                    {
                        "id": "core",
                        "source": "agent_prepack_interpretation",
                        "revisable": False,
                        "required_in_final_prompt": True,
                        "applicability": {"status": "required"},
                    }
                ]
            }
        }
        composed = {
            "semantic_clarification_decisions": [
                {
                    "clarification_id": "core",
                    "decision": "superseded_by_revision",
                    "rationale": "replace frozen meaning",
                    "prompt_evidence": "bread",
                }
            ]
        }
        self.assertTrue(audit_composed_prompt.audit_semantic_clarification(pack, composed, "bread"))


if __name__ == "__main__":
    unittest.main()
