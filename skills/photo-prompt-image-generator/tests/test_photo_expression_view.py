from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("photo_expression_view_tested", HERE.parent / "scripts/photo_expression_view.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def make_record(cid: str, cue: str, *, retrieval_class: str = "positive",
                meaning_en: str = "A source-authored meaning.",
                meaning_ko: str = "출처가 작성한 의미.",
                definition: str = "Meaning and evidence boundary.",
                field: str = "aliases") -> dict:
    literal_values = {
        "cue": cue,
        "en": meaning_en,
        "ko": meaning_ko,
        "definition": definition,
    }
    references = {"aliases": [], "keywords": [], "labels": []}
    references[field] = ["cue"]
    native_tree = {
        "aliases": [{"$literal": "cue"}] if field == "aliases" else [],
        "keywords": [{"$literal": "cue"}] if field == "keywords" else [],
    }
    record_kind = "diagnostic" if retrieval_class == "diagnostic" else "visual_option"
    return {
        "id": cid,
        "record_kind": record_kind,
        "effects": {"dimensions": [], "properties": []} if retrieval_class == "diagnostic" else {
            "dimensions": ["framing"], "properties": [{"dimension": "framing"}],
        },
        "provenance": [{"source": "fixture#source", "sha256": "a" * 64}],
        "native": {"schema": MODULE.NATIVE_TREE_SCHEMA, "tree": native_tree},
        "meaning": {
            "schema": MODULE.MEANING_SCHEMA,
            "literals": literal_values,
            "primary": {"base": {
                "/content/en": "en",
                "/content/ko": "ko",
                "/content/definition": "definition",
            }},
            "search": {"fields": references},
            "retrieval_class": retrieval_class,
        },
    }


def make_module(*records: dict) -> dict:
    return {"schema": MODULE.NATIVE_MODULE_SCHEMA,
            "candidates": {record["id"]: record for record in records}}


def lookup(module: dict, query: str) -> dict:
    return MODULE.lookup_module(
        module,
        query,
        module_sha256="b" * 64,
        generation_id="c" * 64,
        native_generation_id="d" * 64,
        execution={"mode": "maintenance_read_only", "freeze_verified": False},
    )


class ExpressionViewTests(unittest.TestCase):
    def test_positive_alias_is_discovery_only_and_not_a_fact(self):
        result = lookup(make_module(make_record("cand_positive", "one arm beyond the crop")),
                       "  ONE   ARM BEYOND THE CROP  ")

        self.assertEqual(result["status"], "matched")
        self.assertEqual(result["matched_cids"], ["cand_positive"])
        row = result["matches"][0]
        self.assertEqual(row["classification"], "positive_discovery")
        self.assertEqual(row["matched_lookup_cues"][0]["cue_role"], "lookup_cue_only_not_fact")
        self.assertIn("not an independently verified fact", row["meaning"]["basis"])
        self.assertFalse(row["native_approval"])
        self.assertFalse(result["visual_fact_established"])

    def test_diagnostic_is_source_limited_and_carries_no_visual_effect(self):
        row = make_record("cand_diag", "source omitted the other side", retrieval_class="diagnostic",
                          meaning_en="The source does not specify the other side.")
        result = lookup(make_module(row), "source omitted the other side")

        self.assertEqual(result["matches"][0]["classification"], "diagnostic/source_limited")
        self.assertEqual(result["matches"][0]["retrieval_class"], "diagnostic")
        self.assertEqual(result["meaning_variants"][0]["en"], "The source does not specify the other side.")
        self.assertFalse(result["native_approval"])

    def test_one_expression_can_return_all_ambiguous_meaning_variants(self):
        first = make_record("cand_a", "shared cue", meaning_en="Meaning A.")
        second = make_record("cand_b", "shared cue", meaning_en="Meaning B.")
        result = lookup(make_module(first, second), "shared cue")

        self.assertEqual(result["status"], "ambiguous")
        self.assertEqual(result["matched_cids"], ["cand_a", "cand_b"])
        self.assertEqual([row["en"] for row in result["meaning_variants"]], ["Meaning A.", "Meaning B."])

    def test_unrecognized_expression_has_no_inferred_meaning(self):
        result = lookup(make_module(make_record("cand_a", "known cue")), "unseen phrase")

        self.assertEqual(result["status"], "unrecognized")
        self.assertEqual(result["matches"], [])
        self.assertEqual(result["meaning_variants"], [])
        self.assertIsNone(result["lookup"]["inferred_meaning"])

    def test_normalization_does_not_remove_punctuation_or_match_substrings(self):
        module = make_module(make_record("cand_a", "edge-case cue"))

        self.assertEqual(lookup(module, "EDGE-CASE   CUE")["status"], "matched")
        self.assertEqual(lookup(module, "edge case cue")["status"], "unrecognized")
        self.assertEqual(lookup(module, "edge-case")["status"], "unrecognized")

    def test_hash_mismatch_fails_closed_before_parsing(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / MODULE.MODULE_RELATIVE_PATH
            target.parent.mkdir(parents=True)
            target.write_text("{}", encoding="utf-8")
            manifest = {"members": {MODULE.MODULE_RELATIVE_PATH: {
                "sha256": "0" * 64, "bytes": len(b"{}"),
            }}}

            with self.assertRaisesRegex(MODULE.ExpressionViewError, "sealed_candidate_module_hash_mismatch"):
                MODULE._verified_module_bytes(root, manifest)







    def test_canonical_label_is_a_lookup_cue_not_a_new_fact(self):
        row = make_record("cand_label", "literal label", field="labels")
        row["native"]["tree"].pop("aliases")
        row["native"]["tree"].pop("keywords")
        result = lookup(make_module(row), "literal label")

        self.assertEqual(result["matches"][0]["matched_lookup_cues"][0]["field"], "labels")
        self.assertEqual(result["matches"][0]["matched_lookup_cues"][0]["cue_role"], "lookup_cue_only_not_fact")
        self.assertFalse(result["visual_fact_established"])


API_SPEC = importlib.util.spec_from_file_location("expression_dispatch_tested", HERE.parent / "scripts/photo_installed_h_f2.py")
API = importlib.util.module_from_spec(API_SPEC)
API_SPEC.loader.exec_module(API)

class ExpressionDispatchTests(unittest.TestCase):
    def verifier(self, state):
        from unittest.mock import Mock
        from types import SimpleNamespace
        return SimpleNamespace(load_state=Mock(return_value=state),
                               status=Mock(return_value={"phase": "core_frozen"}),
                               verify_freeze=Mock(return_value=({}, {}, {})))

    def test_runtime_overrides_are_rejected_outside_maintenance(self):
        with patch.object(API, "release", side_effect=AssertionError("release loaded")):
            with self.assertRaisesRegex(ValueError, "runtime_overrides_require_explicit_maintenance_mode"):
                API._dispatch_expression_view(["view", "--expression", "cue", "--run", "/run",
                                              "--runtime-store", "/store", "--generation-id", "f" * 64], skill_root=HERE.parent)

    def test_maintenance_can_select_explicit_sealed_generation(self):
        class StopAtRelease(RuntimeError): pass
        with patch.object(API, "release", side_effect=StopAtRelease) as release, patch.object(API, "_expression_config", side_effect=AssertionError("config loaded")):
            with self.assertRaises(StopAtRelease):
                API._dispatch_expression_view(["view", "--expression", "cue", "--maintenance",
                                              "--runtime-store", "/staged/store", "--generation-id", "f" * 64], skill_root=HERE.parent)
            release.assert_called_once_with(Path("/staged/store").resolve(), "f" * 64)

    def test_precore_run_is_blocked_before_frozen_artifact_validation(self):
        verifier = self.verifier({"phase": "controls_bound", "artifacts": {}, "mode": "prompt_only"})
        with patch.object(API, "_neutral_run_files", return_value=verifier), patch.object(API, "release", side_effect=AssertionError("release loaded")), patch.object(API, "_expression_config", side_effect=AssertionError("config loaded")):
            with self.assertRaisesRegex(ValueError, "pre_core_expression_lookup_blocked"):
                API._dispatch_expression_view(["view", "--expression", "cue", "--run", "/run"], skill_root=HERE.parent)
        verifier.status.assert_not_called()
        verifier.verify_freeze.assert_not_called()

    def test_precore_cli_does_not_load_installed_resolver(self):
        import contextlib, io
        verifier = self.verifier({"phase": "request_prepared", "mode": "prompt_only", "artifacts": {}})
        with patch.object(API, "_neutral_run_files", return_value=verifier), patch.object(API, "release", side_effect=AssertionError("release loaded")), patch.object(API, "_expression_config", side_effect=AssertionError("config loaded")), contextlib.redirect_stderr(io.StringIO()) as err:
            code = API.dispatch(["view", "--expression", "cue", "--run", "/run"], skill_root=HERE.parent)
        self.assertEqual(code, 2)
        self.assertIn("pre_core_expression_lookup_blocked", err.getvalue())
        verifier.verify_freeze.assert_not_called()

    def test_valid_frozen_run_records_its_exact_optional_h2_binding(self):
        class StopAtRelease(RuntimeError): pass
        state = {"phase": "core_frozen", "mode": "prompt_only", "artifacts": {"freeze_receipt": {}},
                 "h_f2_binding": {"store": "/bound/store", "generation_id": "e" * 64}}
        verifier = self.verifier(state)
        with patch.object(API, "_neutral_run_files", return_value=verifier), patch.object(API, "release", side_effect=StopAtRelease) as release, patch.object(API, "_expression_config", side_effect=AssertionError("config fallback")):
            with self.assertRaises(StopAtRelease):
                API._dispatch_expression_view(["view", "--expression", "cue", "--run", "/run"], skill_root=HERE.parent)
            release.assert_called_once_with(Path("/bound/store").resolve(), "e" * 64)
        verifier.verify_freeze.assert_called_once_with(state)

    def test_legacy_material_run_without_h2_binding_fails_closed(self):
        state = {"phase": "pack_bound", "mode": "prompt_only", "artifacts": {"freeze_receipt": {}, "pack": {}}}
        verifier = self.verifier(state)
        with patch.object(API, "_neutral_run_files", return_value=verifier), patch.object(API, "release", side_effect=AssertionError("release loaded")), patch.object(API, "_expression_config", side_effect=AssertionError("config loaded")):
            with self.assertRaisesRegex(ValueError, "legacy_run_has_no_h_f2_generation_binding"):
                API._dispatch_expression_view(["view", "--expression", "cue", "--run", "/run"], skill_root=HERE.parent)

if __name__ == "__main__":
    unittest.main()
