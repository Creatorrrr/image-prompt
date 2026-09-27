from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/photo-prompt-image-generator/scripts"
sys.path.insert(0, str(SCRIPTS)) if str(SCRIPTS) not in sys.path else None
import photo_embodiment as embodiment
import audit_composed_prompt
import audit_image_render_request
import audit_moe_render_review
import compose_pack_view
import prompt_generator


BASELINE = (
    "An adult technician operates a lever under an open shelf. Her working hand belongs "
    "to the arm nearest the lever, with a relaxed shoulder and a bent elbow beside her "
    "ribs. The forearm crosses the open gap and the wrist follows its line. Her fingers "
    "close around the lever, while both feet rest on the floor. A side view reveals the "
    "connected segments and contact against the still machinery in soft workshop light."
)


def core(baseline=BASELINE, request="A technician operates a lever."):
    return {
        "contract_version": "photo-authorial-core/v3",
        "canonical_sha256": "a" * 64,
        "intent_lock": {"canonical_sha256": "b" * 64},
        "baseline_prompt_en": baseline,
        "request_binding": {"active_spans": [{"span_id": "topic", "text": request}]},
    }


def review(prompt=BASELINE, phase="agent_prepack", scope="body_action"):
    phrases = {
        "body_ownership": "Her working hand belongs to the arm nearest the lever",
        "joint_chain_and_reach": "a relaxed shoulder and a bent elbow beside her ribs",
        "support_and_balance": "both feet rest on the floor",
        "contact_and_space": "Her fingers close around the lever",
        "visibility_and_projection": "A side view reveals the connected segments and contact",
    }
    return {
        "contract_version": embodiment.REVIEW_VERSION,
        "provenance": phase,
        "prompt_sha256": embodiment.text_sha256(prompt),
        "scope": scope,
        "summary": "Synthetic review fixture; exercises binding, not actual visual qualification.",
        "checks": {
            check: {"status": "supported", "reason": "Synthetic case-specific review observation.",
                    "prompt_evidence": [phrases[check]]}
            for check in embodiment.CHECKS
        } if scope == "body_action" else {},
    }


def fixture():
    frozen_core = core()
    policy = embodiment.build_policy(frozen_core, review())
    pack = {"contract_version": "photo-candidate-pack/v6", "authorial_core": frozen_core,
            "provenance": {"embodiment_preflight_required": True}, "embodiment_preflight": policy}
    composed = {"prompt_en": BASELINE, "negative_en": "low resolution", "embodiment_review": {
        "source_contract_sha256": policy["canonical_sha256"],
        "review": review(phase="agent_postcomposition"),
    }}
    return pack, composed


class EmbodimentContractTests(unittest.TestCase):
    def test_freezing_review_does_not_mutate_semantic_core_or_prompt(self):
        frozen = core()
        original = copy.deepcopy(frozen)
        policy = embodiment.build_policy(frozen, review())
        self.assertEqual(frozen, original)
        self.assertEqual(policy["baseline_review"]["prompt_sha256"], embodiment.text_sha256(BASELINE))

    def test_stale_baseline_and_wrong_authoring_phase_are_rejected(self):
        for key, value in [("prompt_sha256", "c" * 64), ("provenance", "agent_postcomposition")]:
            with self.subTest(key=key):
                r = review()
                r[key] = value
                with self.assertRaises(ValueError):
                    embodiment.build_policy(core(), r)

    def test_unresolved_or_repair_needed_findings_block_every_check(self):
        for check in embodiment.CHECKS:
            for status in ("unresolved", "needs_revision", "partial"):
                with self.subTest(check=check, status=status):
                    r = review()
                    r["checks"][check]["status"] = status
                    with self.assertRaises(ValueError):
                        embodiment.build_policy(core(), r)

    def test_missing_evidence_and_nonliteral_controls_do_not_pass(self):
        for evidence in ([], ["plausible posture"], ["a hand from a different person"]):
            r = review()
            r["checks"]["body_ownership"]["prompt_evidence"] = evidence
            with self.subTest(evidence=evidence), self.assertRaises(ValueError):
                embodiment.build_policy(core(), r)

    def test_still_life_can_remain_inapplicable_without_inventing_an_actor(self):
        prompt = "Light reflects from the glaze of a ceramic bowl on the table."
        r = review(prompt, scope="not_applicable")
        policy = embodiment.build_policy(core(prompt), r)
        self.assertEqual(policy["baseline_review"]["checks"], {})

    def test_body_action_cannot_omit_checks_or_mark_everything_inapplicable(self):
        for mode in ("missing", "all_inapplicable"):
            r = review()
            if mode == "missing":
                r["checks"].pop("contact_and_space")
            else:
                for row in r["checks"].values():
                    row.update(status="not_applicable", prompt_evidence=[])
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                embodiment.build_policy(core(), r)

    def test_requested_unusual_structure_is_retained_with_grounded_evidence(self):
        phrase = "a robot with four articulated manipulators"
        prompt = BASELINE + " Beside her stands " + phrase + "."
        request = "Show a robot with four articulated manipulators beside the technician."
        r = review(prompt)
        r["checks"]["body_ownership"].update(
            status="requester_intended", prompt_evidence=[phrase], requester_source_text=phrase)
        self.assertEqual(embodiment.build_policy(core(prompt, request), r)["baseline_review"], r)
        r["checks"]["body_ownership"]["requester_source_text"] = "an agent preference for extra limbs"
        with self.assertRaisesRegex(ValueError, "requester source"):
            embodiment.build_policy(core(prompt, request), r)

    def test_unrelated_animal_motion_uses_its_own_structure(self):
        phrase = "The bird braces its feet and spreads its wings above the branch"
        r = review(phrase)
        for row in r["checks"].values():
            row["prompt_evidence"] = [phrase]
        policy = embodiment.build_policy(core(phrase, "A bird prepares to fly."), r)
        self.assertEqual(policy["baseline_review"]["checks"], r["checks"])
        self.assertNotIn("human", json.dumps(policy))

    def test_missing_or_mutated_policy_is_not_silently_downgraded(self):
        for mode in ("missing", "mutated", "marker_removed"):
            pack, composed = fixture()
            if mode == "missing":
                pack.pop("embodiment_preflight")
            elif mode == "mutated":
                pack["embodiment_preflight"]["required_checks"] = []
            else:
                pack["provenance"].clear()
            with self.subTest(mode=mode):
                self.assertTrue(embodiment.audit_composed(pack, composed))

    def test_final_prompt_change_requires_a_new_review(self):
        pack, composed = fixture()
        self.assertEqual(embodiment.audit_composed(pack, composed), [])
        composed["prompt_en"] += " The working arm is fully straight while the same elbow is sharply bent."
        failures = embodiment.audit_composed(pack, composed)
        self.assertIn("stale", failures[0]["reason"])
        composed["embodiment_review"]["review"]["prompt_sha256"] = embodiment.text_sha256(composed["prompt_en"])
        composed["embodiment_review"]["review"]["checks"]["joint_chain_and_reach"]["status"] = "needs_revision"
        self.assertIn("needs_revision", embodiment.audit_composed(pack, composed)[0]["reason"])

    def test_newly_reviewed_lighting_variation_preserves_contact(self):
        pack, composed = fixture()
        composed["prompt_en"] += " Reflected light traces the same contact."
        composed["embodiment_review"]["review"] = review(composed["prompt_en"], "agent_postcomposition")
        self.assertEqual(embodiment.audit_composed(pack, composed), [])
        self.assertIn("Her fingers close around the lever", composed["prompt_en"])

    def test_final_review_cannot_downgrade_material_action(self):
        pack, composed = fixture()
        composed["embodiment_review"]["review"] = review(phase="agent_postcomposition", scope="not_applicable")
        self.assertIn("downgraded", embodiment.audit_composed(pack, composed)[0]["reason"])

    def test_runtime_requires_binding_and_rejects_added_positive_prose(self):
        pack, composed = fixture()
        request = {"source_embodiment_preflight_sha256": pack["embodiment_preflight"]["canonical_sha256"],
                   "runtime_prompt_en": BASELINE + "\n\nAvoid: low resolution"}
        self.assertEqual(embodiment.audit_runtime(pack, composed, request), [])
        request["runtime_prompt_en"] += " Extend the other arm across the first."
        self.assertTrue(embodiment.audit_runtime(pack, composed, request))
        request["runtime_prompt_en"] = BASELINE
        request.pop("source_embodiment_preflight_sha256")
        self.assertTrue(embodiment.audit_runtime(pack, composed, request))

    def test_legacy_packs_stay_replayable_without_a_new_review_claim(self):
        self.assertEqual(embodiment.audit_composed({}, {"prompt_en": BASELINE}), [])
        self.assertEqual(embodiment.render_gate_ids({}, None), ([], []))
        self.assertTrue(embodiment.audit_composed({}, {"embodiment_review": {}}))

    def test_applicable_pixel_gates_are_derived_from_final_review(self):
        pack, composed = fixture()
        baseline = copy.deepcopy(pack["embodiment_preflight"]["baseline_review"])
        baseline["checks"]["support_and_balance"].update(
            status="not_applicable", prompt_evidence=[], reason="This framing does not make load-bearing material.")
        pack["embodiment_preflight"] = embodiment.build_policy(pack["authorial_core"], baseline)
        composed["embodiment_review"]["source_contract_sha256"] = pack["embodiment_preflight"]["canonical_sha256"]
        composed["embodiment_review"]["review"]["checks"]["support_and_balance"].update(
            status="not_applicable", prompt_evidence=[], reason="This close framing does not make load-bearing material.")
        gates, failures = embodiment.render_gate_ids(pack, composed)
        self.assertEqual(failures, [])
        self.assertEqual(len(gates), 4)
        self.assertNotIn("embodiment_support_and_balance", gates)

    def test_material_baseline_check_cannot_be_suppressed_after_composition(self):
        pack, composed = fixture()
        composed["embodiment_review"]["review"]["checks"]["contact_and_space"].update(
            status="not_applicable", prompt_evidence=[], reason="Attempted suppression of the frozen interaction.")
        self.assertIn("cannot be dropped", embodiment.audit_composed(pack, composed)[0]["reason"])


class EmbodimentPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from tests import test_photo_character_render_review as existing
        existing.PhotoCharacterRenderReviewTests.setUpClass()
        cls.original_pack = copy.deepcopy(existing.PhotoCharacterRenderReviewTests.pack)
        cls.original_composed = copy.deepcopy(existing.PhotoCharacterRenderReviewTests.composed)

    def bound_pair(self):
        pack, composed = copy.deepcopy((self.original_pack, self.original_composed))
        frozen = pack["authorial_core"]
        baseline = frozen["baseline_prompt_en"]
        r = review(baseline)
        for row in r["checks"].values():
            row["prompt_evidence"] = ["wraps the coworker's scraped wrist with practical care"]
        policy = embodiment.build_policy(frozen, r)
        pack["embodiment_preflight"] = policy
        pack["provenance"]["embodiment_preflight_required"] = True
        pack["pack_id"] = audit_composed_prompt.computed_pack_id(pack)
        composed["pack_id"] = pack["pack_id"]
        final = copy.deepcopy(r)
        final.update(provenance="agent_postcomposition", prompt_sha256=embodiment.text_sha256(composed["prompt_en"]))
        composed["embodiment_review"] = {"source_contract_sha256": policy["canonical_sha256"], "review": final}
        return pack, composed

    def test_composed_audit_and_compact_view_preserve_the_new_contract(self):
        pack, composed = self.bound_pair()
        result = audit_composed_prompt.audit_composed_prompt(pack, composed)
        self.assertEqual(result["failures"], [])
        self.assertEqual(compose_pack_view.build_view(pack)["requirements"]["embodiment_preflight"], pack["embodiment_preflight"])
        composed.pop("embodiment_review")
        self.assertIn("embodiment_preflight", {x["check"] for x in audit_composed_prompt.audit_composed_prompt(pack, composed)["failures"]})

    def test_runtime_auditor_checks_full_reviewed_input(self):
        pack, composed = self.bound_pair()
        request = {"schema_version": "photo-image-render-request/v2", "pack_id": pack["pack_id"],
                   "source_intent_lock_sha256": pack["authorial_core"]["intent_lock"]["canonical_sha256"],
                   "source_embodiment_preflight_sha256": pack["embodiment_preflight"]["canonical_sha256"],
                   "runtime_prompt_en": composed["prompt_en"] + "\n\nAvoid: " + composed["negative_en"], "runtime_negative_en": composed["negative_en"],
                   "audit_boundary": {"composed_prompt_audit_status": "pass", "runtime_prompt_audit_status": "not_run", "inherits_composed_prompt_pass": False},
                   "references": []}
        result = audit_image_render_request.audit_image_render_request(pack, composed, request)
        self.assertEqual(result["status"], "pass", result["failures"])
        request["runtime_prompt_en"] += " Make the same arm both straight and bent."
        self.assertIn("embodiment_runtime", {x["check"] for x in audit_image_render_request.audit_image_render_request(pack, composed, request)["failures"]})

    def test_wrapper_emits_bound_policy_without_retrieving_review_prose(self):
        from tests import test_photo_authorial_core_v6 as fixtures
        raw = fixtures.core()
        r = review(raw["baseline_prompt_en"])
        r["summary"] = "REVIEW_ONLY_SENTINEL: synthetic record outside semantic retrieval."
        for row in r["checks"].values():
            row["prompt_evidence"] = ["wraps the coworker's scraped wrist with practical care"]
        with tempfile.TemporaryDirectory() as tmp:
            paths = {}
            for name, value in (("core", raw), ("envelope", fixtures.envelope()), ("review", r)):
                # A review filename must not invoke the dictionary loader's special
                # extension handling, even if it happens to match its basename.
                paths[name] = Path(tmp) / ("photo_prompt_tags.json" if name == "review" else name + ".json")
                paths[name].write_text(json.dumps(value, ensure_ascii=False))
            completed = subprocess.run([
                sys.executable, str(SCRIPTS / "generate_photo_prompt.py"),
                "--selection-mode", "rule", "--seed", "9501", "--creativity", "0",
                "--emit-candidate-pack", "--candidate-pack-version", "v6",
                "--authorial-core-json", str(paths["core"]),
                "--request-envelope-json", str(paths["envelope"]),
                "--embodiment-review-json", str(paths["review"]), "--n", "1",
            ], cwd=ROOT, capture_output=True, text=True, timeout=180)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        pack = json.loads(completed.stdout)[0]
        self.assertEqual(embodiment.policy_from_pack(pack)["baseline_review"], r)
        query, _ = prompt_generator.authorial_core_retrieval_text(pack["authorial_core"])
        self.assertNotIn("REVIEW_ONLY_SENTINEL", query)
        self.assertEqual(pack["authorial_core"]["baseline_prompt_en"], raw["baseline_prompt_en"])

    def test_pixel_review_requires_new_gates_without_claiming_real_pixels(self):
        pack, composed = self.bound_pair()
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "synthetic-review-record.bin"
            image.write_bytes(b"review validator fixture; not rendered image evidence")
            gates = [g["id"] for g in pack["character_response"]["render_gates"]]
            r = {"schema_version": "moe-render-review/v1", "pack_id": pack["pack_id"],
                 "contract_version": "photo-character-response/v1", "reviewer": "synthetic validator fixture",
                 "result_image": str(image), "result_sha256": hashlib.sha256(image.read_bytes()).hexdigest(),
                 "hard_gates": {g: {"status": "pass", "evidence": "Synthetic observation for record validation only."} for g in gates},
                 "user_judgment": {"baseline_available": False, "genuinely_moe": "pending", "better_than_baseline": "not_applicable", "source": "not_yet_received", "evidence": ""}}
            self.assertFalse(audit_moe_render_review.audit_moe_render_review(pack, r, composed=composed)["technical_qualified"])
            for g in embodiment.GATES:
                r["hard_gates"][g] = {"status": "pass", "evidence": "Synthetic observation for record validation only."}
            self.assertTrue(audit_moe_render_review.audit_moe_render_review(pack, r, composed=composed)["technical_qualified"])
            r["hard_gates"]["embodiment_joint_chain_and_reach"]["status"] = "fail"
            self.assertFalse(audit_moe_render_review.audit_moe_render_review(pack, r, composed=composed)["technical_qualified"])


if __name__ == "__main__":
    unittest.main()
