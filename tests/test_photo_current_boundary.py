"""Current-only public contracts and explicit maintenance diagnostics."""

from __future__ import annotations
import contextlib
import copy
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

from tests import photo_prompt_fixtures as fixtures
import prompt_generator as generator
import audit_composed_prompt as auditor
import compose_pack_view
import build_semantic_index
import generate_photo_prompt
import record_image_run


class PhotoCurrentBoundaryTests(unittest.TestCase):
    def test_removed_pack_versions_fail_before_generation(self):
        for version in ("v2", "v3", "v4", "v5"):
            with self.subTest(version=version), self.assertRaisesRegex(ValueError, "v6"):
                generator.build_candidate_pack({}, {}, version)

    def test_old_core_and_intent_lock_versions_are_rejected(self):
        raw = fixtures.core("A blue porcelain teacup in a quiet kitchen")
        envelope = generator.normalize_request_envelope(fixtures.envelope(raw["source_request"]))
        for version in ("photo-authorial-core/v1", "photo-authorial-core/v2"):
            old = copy.deepcopy(raw)
            old["contract_version"] = version
            with self.subTest(version=version), self.assertRaises(ValueError):
                generator.normalize_authorial_core(old, request_envelope=envelope)
        old = copy.deepcopy(raw)
        old["intent_lock"]["contract_version"] = "photo-intent-lock/v1"
        with self.assertRaises(ValueError):
            generator.normalize_authorial_core(old, request_envelope=envelope)

    def test_old_cli_options_are_unknown(self):
        for flag in ("--legacy-replay-reason", "--authorial-request-json", "--hybrid-augmentation",
                     "--surreal-mode", "--surreal-probability", "--surreal-intensity"):
            with self.subTest(flag=flag), contextlib.redirect_stderr(
                io.StringIO()
            ), self.assertRaises(SystemExit) as exc:
                generate_photo_prompt.main([flag, "{}"])
            self.assertEqual(exc.exception.code, 2)

    def test_normal_generation_requires_complete_current_inputs(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as exc:
            generate_photo_prompt.main([])
        self.assertEqual(exc.exception.code, 2)
        with self.assertRaisesRegex(ValueError, "core"):
            generator.build_candidate_pack({}, {})

    def test_sampler_diagnostics_are_not_public_packs(self):
        diagnostic = {"schema_version": "photo-sampler-diagnostic/v1", "diagnostic_only": True}
        result = auditor.audit_composed_prompt(diagnostic, {"prompt_en": "sample"})
        self.assertEqual(result["status"], "fail")
        self.assertIn("contract_version", {row["check"] for row in result["failures"]})
        with self.assertRaises(ValueError):
            compose_pack_view.build_view(diagnostic)

    def test_only_current_view_and_manifest_versions_are_supported(self):
        with self.assertRaises(ValueError):
            compose_pack_view.build_view({}, version="photo-composer-view/v1")
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            record_image_run.parse_args(["--candidate-pack-version", "v4"])

    def test_only_shards_are_completed_indexes_but_checkpoints_resume(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "index.json"
            raw = {
                "provider": "gemini",
                "embedding_model": "test",
                "embedding_dimensions": 2,
                "dictionary_hash": "a" * 64,
                "entries": {"slot:x:y": {"text": "same", "vector": [0.5, 0.5]}},
            }
            path.write_text(json.dumps(raw))
            with self.assertRaises(ValueError):
                generator.load_semantic_index_payload(path)
            checkpoint = Path(tmp) / "build-checkpoint"
            checkpoint.write_text(json.dumps(raw))
            self.assertEqual(
                build_semantic_index.load_checkpoint(checkpoint, raw)["entries"], raw["entries"]
            )
            build_semantic_index.write_sharded_payload(path, raw, shard_count=2)
            self.assertEqual(generator.load_semantic_index_payload(path)["entries"], raw["entries"])

    def test_sampler_api_is_removed(self):
        for name in ("generate_once", "choose_slot", "choose_preset", "candidate_pack_build_slots"):
            self.assertFalse(hasattr(generator, name), name)

    def test_legacy_concept_mode_has_no_adapter(self):
        self.assertFalse(hasattr(generate_photo_prompt, "resolve_concepts"))


if __name__ == "__main__":
    unittest.main()
