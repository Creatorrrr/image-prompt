"""Fresh reconstruction controls; no generation, publication, or provider use.

Synthetic delta fixtures are intentionally distinct from the fresh latest pack
evidence. Rehashing selected fixtures exercises the independent semantic checks.
"""
from __future__ import annotations

import copy
import ast
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from tests import photo_camera_guidance_v36 as v

ROOT = Path(__file__).resolve().parents[1]


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


class SemanticBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.original_raw = (ROOT / v.V35_PACK).read_bytes()
        self.assertEqual(v.digest(self.original_raw), v.V35_PACK_SHA256)
        self.original = json.loads(self.original_raw)
        self.current = copy.deepcopy(self.original)
        before = self.current[0]["pack_id"]
        self.current[0]["pack_id"] = "synthetic-v36-control"
        path = "/0/semantic_clarification/candidates/1/applicability/diagnostics"
        diagnostics = {"applicable": False, "checks": [{"blocking_effect": True}]}
        self.current[0]["semantic_clarification"]["candidates"][1]["applicability"]["diagnostics"] = copy.deepcopy(diagnostics)
        self.changes = [{"operation": "replace", "pointer": "/0/pack_id", "before": before,
                         "after": "synthetic-v36-control"}, {"operation": "add", "pointer": path, "after": diagnostics}]
        self.raw = encoded(self.current)
        self.proof = {"reviewed_upstream_pack_delta": copy.deepcopy(self.changes), "reviewed_doc_only_pack_delta": [],
                      "current_pack_sha256": v.digest(self.raw), "current_pack_id": self.current[0]["pack_id"],
                      "preserved_public_candidate_count": 64}
        self.baseline = {"sha256": v.digest(self.raw), "pack_id": self.current[0]["pack_id"], "public_candidate_count": 64}
        self.addCleanup(mock.patch.stopall)
        mock.patch.object(v, "UPSTREAM_PACK_SHA256", v.digest(self.raw)).start()
        mock.patch.object(v, "REVIEWED_DELTA_SHA256", v.digest(v.canonical(self.changes))).start()
        mock.patch.object(v, "REVIEWED_POINTERS", tuple(row["pointer"] for row in self.changes)).start()

    def check(self, current=None, proof=None, baseline=None, unedited=None):
        current = self.current if current is None else current
        v.qualify_pack(proof or self.proof, baseline or self.baseline, current[0], encoded(current),
                       self.original_raw, self.raw if unedited is None else unedited)

    def reject_rehashed(self, mutation, pattern):
        current = copy.deepcopy(self.current)
        mutation(current[0])
        raw = encoded(current)
        proof, baseline = copy.deepcopy(self.proof), copy.deepcopy(self.baseline)
        proof["current_pack_sha256"] = baseline["sha256"] = v.digest(raw)
        proof["current_pack_id"] = baseline["pack_id"] = current[0]["pack_id"]
        # Deliberately waive the immutable latest-byte anchor to isolate the
        # deeper semantic guard. Production cannot waive that independent seal.
        with mock.patch.object(v, "UPSTREAM_PACK_SHA256", v.digest(raw)):
            with self.assertRaisesRegex(AssertionError, pattern):
                self.check(current, proof, baseline, unedited=raw)

    def test_exact_reviewed_delta_reconstructs_entire_pack(self):
        self.check()

    def test_rehashed_candidate_id_meaning_and_order_changes_fail(self):
        def order(pack):
            rows = pack["semantic_clarification"]["candidates"]
            rows[1], rows[2] = rows[2], rows[1]
        mutations = [lambda p: p["semantic_clarification"]["candidates"][1].update(id="other"),
                     lambda p: p["semantic_clarification"]["candidates"][1].update(interpreted_meaning="other meaning"), order]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.reject_rehashed(mutation, "entire pack")

    def test_rehashed_applicability_and_diagnostic_truth_fail(self):
        mutations = [lambda p: p["semantic_clarification"]["candidates"][1]["applicability"].update(status="eligible"),
                     lambda p: p["semantic_clarification"]["candidates"][1]["applicability"]["diagnostics"].update(applicable=True),
                     lambda p: p["semantic_clarification"]["candidates"][1]["applicability"]["diagnostics"]["checks"][0].update(blocking_effect=False)]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.reject_rehashed(mutation, "entire pack")

    def test_rehashed_core_lock_negative_controls_budget_and_safety_fail(self):
        mutations = [lambda p: p["authorial_core"].update(subject="changed subject"),
                     lambda p: p["authorial_core"]["intent_lock"]["locked_dimensions"].remove("subject"),
                     lambda p: p.update(negative_en=""),
                     lambda p: p["creative_controls"].update(creativity=999),
                     lambda p: p["authorial_composition"].update(prompt_budget={}),
                     lambda p: p["safety"].update(status="unrestricted")]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.reject_rehashed(mutation, "protected surface")

    def test_seed_and_candidate_inventory_fail_even_after_rehash(self):
        self.reject_rehashed(lambda p: p["provenance"].update(seed=910001), "seed")
        def expand(pack):
            slot = next(s for s in pack["slots"].values() if s["candidates"])
            slot["candidates"].append(copy.deepcopy(slot["candidates"][0]))
        self.reject_rehashed(expand, "entire pack")

    def test_json_types_are_preserved(self):
        self.assertFalse(v.same(False, 0))
        self.assertFalse(v.same(True, 1))
        self.assertFalse(v.same(1, 1.0))
        self.reject_rehashed(lambda p: p["semantic_clarification"]["candidates"][1].update(required_in_final_prompt=0), "entire pack")

    def test_latest_raw_bytes_and_delta_have_separate_fixed_seals(self):
        current = copy.deepcopy(self.current); current[0]["pack_id"] = "changed"
        with self.assertRaisesRegex(AssertionError, "documentation pack differs"):
            self.check(current)
        proof = copy.deepcopy(self.proof); proof["reviewed_upstream_pack_delta"][0]["after"] = "changed"
        with self.assertRaisesRegex(AssertionError, "delta seal"):
            self.check(proof=proof)

    def test_documentation_delta_must_be_empty(self):
        proof = copy.deepcopy(self.proof); proof["reviewed_doc_only_pack_delta"] = self.changes
        with self.assertRaisesRegex(AssertionError, "must be empty"):
            self.check(proof=proof)

    def test_replace_requires_exact_before(self):
        changes = copy.deepcopy(self.changes); changes[0]["before"] = "incorrect"
        with self.assertRaisesRegex(AssertionError, "BEFORE"):
            v.apply_delta(self.original, changes)

    def test_add_requires_fresh_key(self):
        before = copy.deepcopy(self.original)
        before[0]["semantic_clarification"]["candidates"][1]["applicability"]["diagnostics"] = {"already": "present"}
        with self.assertRaisesRegex(AssertionError, "fresh key"):
            v.apply_delta(before, self.changes)

    def test_duplicate_and_overlapping_deltas_fail(self):
        with self.assertRaisesRegex(AssertionError, "duplicate/overlapping"):
            v.apply_delta(self.original, self.changes + [self.changes[0]])
        path = self.changes[1]["pointer"] + "/applicable"
        extra = {"operation": "replace", "pointer": path, "before": False, "after": True}
        with mock.patch.object(v, "REVIEWED_POINTERS", (*v.REVIEWED_POINTERS, path)):
            with self.assertRaisesRegex(AssertionError, "duplicate/overlapping"):
                v.apply_delta(self.original, self.changes + [extra])

    def test_unsupported_operation_and_unregistered_pointer_fail(self):
        for operation in ("remove", "move", "copy", "test"):
            with self.subTest(operation=operation), self.assertRaisesRegex(AssertionError, "unsupported"):
                v.apply_delta(self.original, [{"operation": operation}])
        row = {"operation": "replace", "pointer": "/0/authorial_core", "before": {}, "after": {}}
        with self.assertRaisesRegex(AssertionError, "unreviewed delta pointer"):
            v.apply_delta(self.original, [row])


class SourceBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def write(self, name, raw):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        return path

    def test_asset_mismatch_fails_before_any_import_read_or_cli(self):
        for version in (None, 36, 35, 6):
            with self.subTest(version=version), mock.patch.object(v, "proof_document") as proof, \
                    mock.patch.object(v, "history_module") as history, mock.patch.object(v, "validate_current") as current, \
                    mock.patch.object(subprocess, "run") as run:
                with self.assertRaisesRegex(AssertionError, "asset directory mismatch"):
                    v.dispatch(self.root / "wrong", source_root=self.root, baseline_version=version)
                for method in (proof, history, current, run):
                    method.assert_not_called()

    def test_direct_current_and_history_entrypoints_bind_asset_root_first(self):
        with mock.patch.object(v, "qualification_context") as context, mock.patch.object(v, "dispatch") as dispatch:
            with self.assertRaisesRegex(AssertionError, "asset directory mismatch"):
                v.validate_current(self.root / "wrong", source_root=self.root)
            with self.assertRaisesRegex(AssertionError, "asset directory mismatch"):
                v.dispatch_historical(self.root / "wrong", source_root=self.root, baseline_version=35)
            context.assert_not_called(); dispatch.assert_not_called()

    def test_historical_failure_propagates_without_current_fallback(self):
        helper = mock.Mock(); helper.dispatch_historical.side_effect = RuntimeError("exact missing historical source")
        with mock.patch.object(v, "proof_document", return_value={"source_files_after": {}}), \
                mock.patch.object(v, "history_module", return_value=helper), mock.patch.object(v, "validate_current") as current:
            with self.assertRaisesRegex(RuntimeError, "exact missing historical source"):
                v.dispatch_historical(self.root / v.ASSETS, source_root=self.root, baseline_version=35)
            current.assert_not_called()

    def test_invalid_version_never_uses_latest(self):
        for value in (True, False, "36", 36.0, 5, 37):
            with self.subTest(value=value), mock.patch.object(v, "validate_current") as current:
                with self.assertRaisesRegex(AssertionError, "Unsupported"):
                    v.dispatch(self.root / v.ASSETS, source_root=self.root, baseline_version=value)
                current.assert_not_called()

    def test_frozen_inputs_baselines_shards_and_evidence_reject_changed_bytes(self):
        for label in ("frozen inputs", "historical baselines", "active shards", "evidence"):
            path = self.write("fixture.json", b'{"original":true}')
            mapping = {"fixture.json": v.digest(path.read_bytes())}
            v.verify_files(self.root, mapping, label, 1)
            path.write_bytes(b'{"original":false}')
            with self.subTest(label=label), self.assertRaisesRegex(AssertionError, "bytes drift"):
                v.verify_files(self.root, mapping, label, 1)

    def test_inventory_count_missing_path_and_symlinks_fail(self):
        path = self.write("fixture.json", b"{}")
        mapping = {"fixture.json": v.digest(b"{}")}
        with self.assertRaisesRegex(AssertionError, "inventory"):
            v.verify_files(self.root, mapping, "frozen inputs", 4)
        path.unlink()
        with self.assertRaisesRegex(AssertionError, "regular file"):
            v.verify_files(self.root, mapping, "frozen inputs")
        other = self.write("other.json", b"{}"); path.symlink_to(other)
        with self.assertRaisesRegex(AssertionError, "symlink"):
            v.verify_files(self.root, mapping, "frozen inputs")

    def test_proof_bytes_attribution_and_zero_data_count_are_sealed(self):
        value = {"schema": "photo-camera-guidance-transition/v36", "upstream_commit": v.UPSTREAM_PIN,
                 "reviewed_skill_sha256": v.SKILL_SHA256, "data_improvement_count_delta": 0,
                 "historical_comparison_control": "observational_runtime_mismatch", "doc_only_comparison_control": "same_runtime"}
        path = self.write(v.PROOF, encoded(value))
        with mock.patch.object(v, "PROOF_SHA256", v.digest(path.read_bytes())):
            self.assertEqual(v.load_proof(self.root), value)
            path.write_bytes(encoded({**value, "data_improvement_count_delta": 1}))
            with self.assertRaisesRegex(AssertionError, "proof seal"):
                v.load_proof(self.root)
        for change in ({"data_improvement_count_delta": False}, {"data_improvement_count_delta": 1},
                       {"historical_comparison_control": "same_runtime"}, {"doc_only_comparison_control": "observational"}):
            path.write_bytes(encoded({**value, **change}))
            with self.subTest(change=change), mock.patch.object(v, "PROOF_SHA256", v.digest(path.read_bytes())):
                with self.assertRaisesRegex(AssertionError, "comparison attribution"):
                    v.load_proof(self.root)

    def test_history_helper_bytes_are_authenticated_before_import(self):
        self.write(v.HISTORY, b"raise RuntimeError('must not execute')\n")
        with self.assertRaisesRegex(AssertionError, "history helper drift"):
            v.history_module(self.root)

    def test_command_only_allows_output_destination_change(self):
        old = json.loads((ROOT / v.V35_BASELINE).read_bytes())["command"]
        command = old.copy(); command[-1] = "/tmp/v36-new-output.json"
        v.verify_command(command, old)
        for index in (0, 1, old.index("--seed") + 1, old.index("--authorial-core-json") + 1):
            mutated = command.copy(); mutated[index] = "changed"
            with self.subTest(index=index), self.assertRaisesRegex(AssertionError, "command/input/seed"):
                v.verify_command(mutated, old)

    def test_duplicate_json_keys_and_nonfinite_values_are_rejected(self):
        for raw in (b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}'):
            with self.subTest(raw=raw), self.assertRaises(AssertionError):
                v.strict_json(raw)


class ShardRegistrationTests(unittest.TestCase):
    setUp = SourceBoundaryTests.setUp
    write = SourceBoundaryTests.write

    def test_current_registration_is_distinct_from_original(self):
        current, old = {}, {}
        sources = {}
        for label, inventory in (("current", current), ("old", old)):
            members = {}
            for kind in ("semantic", "visual_profile"):
                rows = []
                for index in range(16):
                    raw = encoded({"vector": [index, kind]})
                    path = f"photo_prompt_{kind}_index_shards/{label}/{index}.json"
                    name = v.PHOTO + "/assets/" + path
                    inventory[name] = v.digest(raw); members[name] = raw
                    rows.append({"path": path, "sha256": v.digest(raw)})
                    if label == "current": self.write(name, raw)
                members[v.PHOTO + f"/assets/photo_prompt_{kind}_index.json"] = encoded({"shards": rows})
            def payload(name, *, sha256=None, members=members):
                raw = members[name]
                if sha256: self.assertEqual(v.digest(raw), sha256)
                return raw
            sources[label] = mock.Mock(payload=mock.Mock(side_effect=payload))
        original = mock.Mock(original=sources["old"], proof={"active_shards_after": old})
        v.verify_shards(self.root, current, sources["current"], original)
        altered_hash = dict(current); altered_hash[next(iter(altered_hash))] = "0" * 64
        altered_path = dict(current); name = next(iter(altered_path)); altered_path[name + ".unknown"] = altered_path.pop(name)
        for claimed in (old, altered_hash, altered_path):
            with self.subTest(claimed=claimed), self.assertRaisesRegex(AssertionError, "exact upstream registration"):
                v.verify_shards(self.root, claimed, sources["current"], original)
        (self.root / next(iter(current))).write_bytes(b"changed")
        with self.assertRaisesRegex(AssertionError, "bytes drift"):
            v.verify_shards(self.root, current, sources["current"], original)


class GuardedExecutionTests(unittest.TestCase):
    def run_guard(self, code):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); script = root / "script.py"; script.write_text(code)
            store = root / "runtime"; store.mkdir()
            return subprocess.run([sys.executable, "-I", "-S", "-B", "-c", v.GUARDED_CHILD,
                                   str(root), str(script), str(root / "pack.json"), str(store)],
                                  env={"PHOTO_RUNTIME_STORE": str(store), "LANG": "C.UTF-8"}, capture_output=True, text=True)

    def test_socket_process_provider_credentials_and_publisher_are_denied(self):
        cases = [("import socket\nsocket.socket()", "socket"),
                 ("import subprocess\nsubprocess.run(['true'])", "subprocess.Popen"),
                 ("def load_api_key(): pass\nload_api_key()", "provider/key"),
                 ("from pathlib import Path\nPath('.env').read_bytes()", "credential file"),
                 ("__name__='photo_runtime_sources'\ndef publish(): pass\npublish()", "publisher/fetch")]
        for code, reason in cases:
            with self.subTest(reason=reason):
                result = self.run_guard(code)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("V36 guard denied: " + reason, result.stderr)

    def test_isolated_local_output_is_allowed(self):
        result = self.run_guard("from pathlib import Path\nPath(__file__).with_name('pack.json').write_text('[]')")
        self.assertEqual(result.returncode, 0, result.stderr)


class ActivatedPublicEntryTests(unittest.TestCase):
    def test_actual_validator_binds_assets_before_loading_v36_support(self):
        # Compile the actual public definition without importing the large
        # validator module or executing any historical fixture-loading code.
        path = ROOT / v.VALIDATOR
        parsed = ast.parse(path.read_text())
        definition = next(node for node in parsed.body if isinstance(node, ast.FunctionDef)
                          and node.name == "validate_photo_regression_baseline")
        tree = ast.Module(body=[definition], type_ignores=[])
        loader = mock.Mock(side_effect=AssertionError("V36 loader must not be touched"))
        namespace = {"__file__": str(path), "Path": Path, "Any": object,
                     "_require": v.require, "_camera_v36_support": loader}
        exec(compile(ast.fix_missing_locations(tree), str(path), "exec"), namespace)
        with self.assertRaisesRegex(AssertionError, "asset directory mismatch"):
            namespace["validate_photo_regression_baseline"](ROOT / "wrong/assets", baseline_version=36)
        loader.assert_not_called()


if __name__ == "__main__":
    unittest.main()
