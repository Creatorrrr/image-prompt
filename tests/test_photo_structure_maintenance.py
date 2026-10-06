"""Preserve irregular pre-migration meaning and the post-core source boundary."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tests import photo_prompt_fixtures
import prompt_generator as pg
import photo_source_manifest as sources
from visual_profile_contracts import compile_visual_profile, validate_visual_profile_source


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
BASELINE = json.loads((ROOT / "tests/fixtures/photo_prompt/structure_maintenance_v1.json").read_text())


class PhotoAuthoredComponentSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = pg.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
        cls.profiles = {profile["id"]: profile for profile in cls.registry["profiles"]}

    def grouped_source(self):
        profile = copy.deepcopy(self.profiles["inner_thigh_negative_space"])
        for field in ("required_evidence_fields", "evidence_requirements", "render_gates", "composition_instruction"):
            profile.pop(field)
        profile["semantics"].pop("component_semantics")
        return profile

    def test_every_live_profile_has_one_valid_source(self):
        ids = []
        for name in ["photo_prompt_visual_obligations.json", *sources.extension_files("visual_profile")]:
            for profile in json.loads((ASSETS / name).read_text())["profiles"]:
                with self.subTest(profile=profile["id"]):
                    validate_visual_profile_source(profile)
                ids.append(profile["id"])
        self.assertEqual(ids, [profile["id"] for profile in self.registry["profiles"]])

    def test_irregular_joint_contracts_match_frozen_pre_migration_meaning(self):
        for expected in BASELINE["profiles"]:
            with self.subTest(profile=expected["id"]):
                actual = copy.deepcopy(self.profiles[expected["id"]])
                actual.pop("authored_components")
                self.assertEqual(actual, expected)

    def test_discovery_minimum_does_not_reduce_evidence_or_pixel_duties(self):
        compiled = compile_visual_profile(self.grouped_source())
        groups = compiled["semantics"]["component_semantics"]
        self.assertEqual(groups["minimum_component_groups"], 2)
        self.assertEqual(groups["required_group_ids"], ["negative_space_shape"])
        self.assertEqual(len(groups["groups"]), 3)
        self.assertEqual(len(compiled["required_evidence_fields"]), 5)
        self.assertEqual(len(compiled["render_gates"]), 5)

    def test_joint_duties_survive_context_specialization(self):
        source = self.grouped_source()
        self.assertEqual(compile_visual_profile(source), compile_visual_profile(
            source, context_text="closed eyes", request_text="a close-leg pose",
            matches=lambda text, term: term in text))

    def test_missing_unknown_and_duplicate_bindings_fail(self):
        def unknown(source):
            source["obligations"][0]["component_ids"].append("unknown_component")

        def unbound(source):
            source["obligations"][0]["component_ids"].pop()

        def threshold(source):
            source["discovery"]["minimum_component_groups"] = 4

        def duplicate_evidence(source):
            source["obligations"][0]["evidence"].append(copy.deepcopy(source["obligations"][0]["evidence"][0]))

        def duplicate_gate(source):
            source["obligations"][0]["render_gates"].append(copy.deepcopy(source["obligations"][0]["render_gates"][0]))

        for mutate in (unknown, unbound, threshold, duplicate_evidence, duplicate_gate):
            with self.subTest(mutation=mutate.__name__):
                profile = self.grouped_source()
                mutate(profile["authored_components"])
                with self.assertRaises(ValueError):
                    compile_visual_profile(profile)

    def test_source_duplicates_and_stale_compiled_fields_fail(self):
        raw = self.grouped_source()
        raw["composition_instruction"] = compile_visual_profile(raw)["composition_instruction"]
        with self.assertRaisesRegex(ValueError, "duplicate generated"):
            validate_visual_profile_source(raw)
        raw["composition_instruction"] += " An incompatible replacement changes the relation."
        with self.assertRaisesRegex(ValueError, "conflicts"):
            compile_visual_profile(raw)


class PhotoSourceManifestTests(unittest.TestCase):
    def row(self, file="photo_prompt_example_extension.json", *, order=0, required=True):
        return {"file": file, "kind": "candidate", "required": required, "load_order": order}

    def write_manifest(self, path, rows):
        path.write_text(json.dumps({"contract_version": sources.CONTRACT_VERSION, "sources": rows}))

    def test_registration_preserves_both_load_orders_and_required_policy(self):
        # The sealed baseline order stays exact. This additive appearance
        # domain owns only the two declared trailing registrations.
        original = copy.deepcopy(BASELINE["extension_order"])
        original["candidate"].append("photo_prompt_character_appearance_extension.json")
        original["visual_profile"].append("photo_prompt_visual_obligations_appearance_relations.json")
        original["required_candidates"].append("photo_prompt_character_appearance_extension.json")
        self.assertEqual(list(sources.extension_files("candidate")), original["candidate"])
        self.assertEqual(list(sources.extension_files("visual_profile")), original["visual_profile"])
        self.assertEqual(sources.required_files("candidate"), original["required_candidates"])
        raw = json.loads((ASSETS / "photo_prompt_tags.json").read_text())
        self.assertNotIn("required_extensions", raw["candidate_semantic_policy"])
        self.assertEqual(pg.load_json(ASSETS / "photo_prompt_tags.json")["candidate_semantic_policy"]["required_extensions"],
                         original["required_candidates"])

    def test_invalid_registrations_fail(self):
        cases = [
            [self.row(), self.row(order=1)],
            [self.row(), self.row("photo_prompt_second_extension.json")],
            [self.row(order=2)],
            [self.row("../outside.json")],
            [{**self.row(), "required": "yes"}],
            [{**self.row(), "kind": []}],
            [{**self.row(), "kind": "visual_profile"}],
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest.json"
            for rows in cases:
                with self.subTest(rows=rows):
                    self.write_manifest(path, rows)
                    with self.assertRaises(ValueError):
                        sources.load_source_manifest(path)

    def test_missing_required_and_unregistered_files_are_distinct(self):
        with tempfile.TemporaryDirectory() as tmp:
            assets = Path(tmp)
            manifest = assets / "manifest.json"
            self.write_manifest(manifest, [self.row(), self.row("photo_prompt_optional_extension.json", order=1, required=False)])
            (assets / "photo_prompt_unregistered_extension.json").write_text("{}")
            errors = []
            sources.validate_source_files(assets, errors, manifest)
            self.assertEqual(len(errors), 2)
            self.assertTrue(any("required candidate source is missing" in error for error in errors))
            self.assertTrue(any("unregistered photo source" in error for error in errors))
            self.assertFalse(any("optional" in error for error in errors))

    def test_importing_public_generator_does_not_read_candidate_assets(self):
        code = '''
import sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, "skills/photo-prompt-image-generator/scripts")
read_text, read_bytes, open_path = Path.read_text, Path.read_bytes, Path.open
def guard(original):
    def checked(path, *args, **kwargs):
        if "assets" in path.parts:
            raise AssertionError("candidate asset read before authorial validation")
        return original(path, *args, **kwargs)
    return checked
with patch.object(Path, "read_text", guard(read_text)), patch.object(Path, "read_bytes", guard(read_bytes)), patch.object(Path, "open", guard(open_path)):
    import generate_photo_prompt
'''
        result = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_duplicate_authored_required_list_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "photo_prompt_tags.json"
            path.write_text(json.dumps({"candidate_semantic_policy": {"required_extensions": ["photo_prompt_example_extension.json"]}}))
            with self.assertRaisesRegex(ValueError, "generated from"):
                pg.load_json(path)


if __name__ == "__main__":
    unittest.main()
