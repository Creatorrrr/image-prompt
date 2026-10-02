"""The authored baseline owns meaning; retrieval never supplies a scene recipe."""
from __future__ import annotations

import contextlib
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests import photo_prompt_fixtures as fixtures
import generate_photo_prompt as cli
import prompt_generator as generator
import audit_composed_prompt as auditor

ASSETS = fixtures.SCRIPT_DIR.parent / "assets"


class PhotoCoreRetrievalTests(unittest.TestCase):
    def inputs(self):
        raw = fixtures.core("A blue porcelain teacup on a rainlit kitchen counter.")
        controls = generator.creative_controls.resolve(raw["source_request"],
            overrides={"sensual": 0, "fetish": 0, "surreal": 0, "creativity": 1}, seed=7)
        raw["creative_controls_sha256"] = controls["canonical_sha256"]
        core = generator.normalize_authorial_core(raw,
            request_envelope=generator.normalize_request_envelope(fixtures.envelope(raw["source_request"])),
            creative_control_snapshot=controls)
        data = {
            "slots": {"prop": [{"id": "cup", "en": "blue porcelain teacup"},
                                {"id": "unrelated", "en": "orange traffic cone"}],
                      "unowned": [{"id": "padding", "en": "blue porcelain teacup"}]},
            "candidate_semantic_policy": {"slot_dimensions": {"prop": ["material"]}},
            generator.QUALITY_LAYERS_DATA_KEY: generator.load_quality_layers(ASSETS / "photo_prompt_quality_layers.json"),
        }
        return data, core, controls

    def test_grounded_core_activates_only_relevant_owned_slots(self):
        data, core, controls = self.inputs()
        before = copy.deepcopy(core)
        slots, binding, _ = generator.retrieve_core_slots(data, core, controls)
        self.assertEqual(set(slots), {"prop"})
        self.assertEqual([row["entry_id"] for row in slots["prop"]["candidates"]], ["cup"])
        self.assertEqual(binding["candidate_adoption"], "optional")
        self.assertEqual(core, before)
        self.assertEqual(auditor.audit_core_retrieval({"slots": slots, "core_retrieval": binding,
            "authorial_core": core, "creative_controls": controls}, data), [])

    def test_no_lexical_hits_produces_no_padding(self):
        data, core, controls = self.inputs()
        data["slots"]["prop"] = [{"id": "unrelated", "en": "orange traffic cone"}]
        slots, binding, _ = generator.retrieve_core_slots(data, core, controls)
        self.assertEqual(slots, {})
        self.assertEqual(binding["active_slots"], {})

    def test_inventory_and_source_mutation_fail_recomputation(self):
        data, core, controls = self.inputs()
        slots, binding, _ = generator.retrieve_core_slots(data, core, controls)
        pack = {"slots": slots, "core_retrieval": binding, "authorial_core": core,
                "creative_controls": controls}
        pack["slots"]["prop"]["candidates"].clear()
        self.assertTrue(auditor.audit_core_retrieval(pack, data))
        slots, binding, _ = generator.retrieve_core_slots(data, core, controls)
        pack.update(slots=slots, core_retrieval=binding)
        data["slots"]["prop"][0]["en"] = "orange traffic cone"
        self.assertTrue(auditor.audit_core_retrieval(pack, data))

    def test_live_corpus_and_indexes_have_no_retired_document_kinds(self):
        data = generator.load_json(ASSETS / "photo_prompt_tags.json")
        for path in ASSETS.glob("*.json"):
            if "index" in path.name:
                continue
            payload = json.loads(path.read_text())
            def keys(value):
                if isinstance(value, dict):
                    for key, item in value.items():
                        yield key
                        yield from keys(item)
                elif isinstance(value, list):
                    for item in value:
                        yield from keys(item)
            self.assertFalse(any("preset" in key.lower() for key in keys(payload)), path.name)
        self.assertFalse((ASSETS / "concept_recipes.json").exists())
        index = generator.load_semantic_index_payload(ASSETS / "photo_prompt_semantic_index.json")
        expected = {key for key, _, _, _ in generator.iter_semantic_entries(data)}
        self.assertEqual(set(index["entries"]), expected)
        self.assertFalse(any(key.startswith("preset:") for key in index["entries"]))
        generator.validate_semantic_index_metadata(index, data)

    def test_removed_flags_and_data_are_rejected_without_adapters(self):
        required = ["--" + name + "-json" for name in (
            "request-envelope", "authorial-core", "creative-controls", "embodiment-review")]
        base = [item for flag in required for item in (flag, "unused.json")]
        for flag in ("--preset", "--concept", "--selection-mode", "--scene-function", "--set"):
            error = io.StringIO()
            with self.subTest(flag=flag), contextlib.redirect_stderr(error), \
                    mock.patch.object(generator, "load_runtime_data", side_effect=AssertionError("must not load candidates")), \
                    self.assertRaises(SystemExit) as raised:
                cli.main([*base, flag, "old-value"])
            self.assertEqual(raised.exception.code, 2)
            self.assertIn("unrecognized arguments", error.getvalue())
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "photo_prompt_tags.json"
            path.write_text(json.dumps({"presets": []}))
            with self.assertRaisesRegex(ValueError, "unsupported photo corpus fields"):
                generator.load_json(path)
        with self.assertRaisesRegex(ValueError, "unsupported runtime keys"):
            generator.merge_research_extension({}, {
                "schema_version": generator.RESEARCH_EXTENSION_SCHEMA, "presets": []})
        with self.assertRaisesRegex(ValueError, "unsupported coherence rules"):
            generator.merge_research_extension({}, {
                "schema_version": generator.RESEARCH_EXTENSION_SCHEMA,
                "coherence_rules": {"sampling_bias_rules": []}})


if __name__ == "__main__":
    unittest.main()
