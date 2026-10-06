import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from tools.photo_data_maintenance.common import MaintenanceError, RECIPES, canonical, decode, digest, normalized, sha
from tools.photo_data_maintenance.corpus import DEFAULT_ROOT, capture_draft, make_inventory, raw_entities
from tools.photo_data_maintenance.links import build_links, path_key, query
from tools.photo_data_maintenance.quality import analyze
from tools.photo_data_maintenance.report import activate, current_report, difference, load_report, pointer_directory, read_pointer, require_current, write_report
from tools.photo_data_maintenance.reviews import load_reviews, review_states


def fixture():
    candidates = [
        {"id": "axis", "en": "upper frontal light axis", "concept_units": ["upper frontal light axis"]},
        {"id": "eye", "en": "vertical catchlight pair", "concept_units": ["vertical catchlight pair"]},
        {"id": "alone", "en": "separate unlinked option"},
    ]
    bundles = [
        {"id": "beauty", "member_candidates": [{"id": "slot:light:axis"}, {"id": "slot:light:eye"}],
         "associated_profile_ids": ["two_sources", "soft_shadow"], "components": [{"id": "axis"}]},
        {"id": "second", "member_candidates": [{"id": "slot:light:eye"}], "associated_profile_ids": ["two_sources"], "components": [{"id": "axis"}]},
    ]
    data = {"slots": {"light": candidates}, "candidate_bundles": bundles}
    registry = {"profiles": [{"id": "two_sources"}, {"id": "soft_shadow"}, {"id": "unlinked"}]}
    return make_inventory({}, {}, data, registry)


def captured(root, mode="generation"):
    return {"inventory": fixture(), "findings": [], "source_files": {"test.json": b'{}'},
            "binding": {"input_mode": mode, "source_root": str(root.resolve()), "generation_id": "a" * 64 if mode == "generation" else None,
                        "source_fingerprint": "b" * 64}}


class RelationshipTests(unittest.TestCase):
    def test_raw_ambiguous_and_missing_references_are_all_reported(self):
        values = {"source.json": {"slots": {"light": [{"id": "same"}], "prop": [{"id": "same"}]},
                                 "visual_semantics": [{"id": "b", "candidate_ids": ["same", "missing"], "hard_profile_ids": ["gone"]}]}}
        errors = []
        records, sources = raw_entities(values, {"source.json": "candidate"}, errors)
        findings = analyze(make_inventory(records, sources), errors)
        self.assertEqual(sum(row["rule"] == "bundle_member_unresolved" for row in findings), 2)
        self.assertEqual(sum(row["rule"] == "bundle_profile_unresolved" for row in findings), 1)

    def test_explicit_slot_resolves_same_entry_id(self):
        values = {"source.json": {"slots": {"light": [{"id": "same"}], "prop": [{"id": "same"}]},
                                 "visual_semantics": [{"id": "b", "candidate_ids": ["same"], "candidate_slots": {"same": "light"}}]}}
        errors = []; records, sources = raw_entities(values, {"source.json": "candidate"}, errors)
        self.assertEqual(analyze(make_inventory(records, sources), errors), [])

    def test_many_to_many_bidirectional(self):
        inv = fixture(); links = build_links(inv)
        candidate = query(inv, links, "slot:light:eye")
        profile = query(inv, links, "profile:two_sources")
        paths = [row["nodes"] for row in profile["paths"]]
        self.assertEqual(candidate["path_count"], 3)
        self.assertIn(["slot:light:eye", "bundle:beauty", "profile:two_sources"], paths)
        self.assertIn(["slot:light:eye", "bundle:second", "profile:two_sources"], paths)
        self.assertEqual(len(links["edges"]), 6)
        self.assertTrue(all(edge["type"] in {"member_of", "associated_with"} for edge in links["edges"]))

    def test_partial_clue_never_promotes_profile(self):
        result = query(fixture(), build_links(fixture()), "slot:light:eye")
        self.assertEqual(result["profile_activation"], "independent_request_evidence_only")
        self.assertTrue(all(row["meaning_support"] == "not_inferred" for row in result["paths"]))

    def test_unlinked_is_valid(self):
        inv = fixture(); links = build_links(inv)
        self.assertEqual(query(inv, links, "slot:light:alone")["paths"], [])
        self.assertIn("profile:unlinked", links["unlinked"])

    def test_missing_endpoint_fails(self):
        inv = fixture()
        inv["nodes"] = [node for node in inv["nodes"] if node["id"] != "profile:soft_shadow"]
        with self.assertRaisesRegex(MaintenanceError, "reference_invalid"):
            build_links(inv)

    def test_slot_identity_stays_distinct(self):
        records = {"slot:camera:same": {"id": "slot:camera:same", "kind": "candidate", "slot": "camera", "record": {"id": "same"}},
                   "slot:prop:same": {"id": "slot:prop:same", "kind": "candidate", "slot": "prop", "record": {"id": "same"}}}
        self.assertEqual(make_inventory(records, {})["counts"]["candidate"], 2)

    def test_same_words_different_scope_are_only_review_leads(self):
        records = {f"slot:{slot}:camera": {"id": f"slot:{slot}:camera", "kind": "candidate", "slot": slot,
                   "record": {"id": "camera", "en": "a disposable camera", "affected_properties": [{"target": slot}]}}
                   for slot in ["camera", "prop"]}
        findings = analyze(make_inventory(records, {}))
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["severity"], "review")
        self.assertEqual(findings[0]["details"]["distinct_scope_signatures"], 2)

    def test_short_and_abstract_are_not_automatically_defects(self):
        records = {"slot:mood:x": {"id": "slot:mood:x", "kind": "candidate", "slot": "mood", "record": {"id": "x", "en": "calm"}}}
        self.assertEqual(analyze(make_inventory(records, {})), [])

    def test_numbers_negations_and_direction_survive_normalization(self):
        self.assertNotEqual(normalized("two lights above"), normalized("two lights below"))
        self.assertNotEqual(normalized("two lights"), normalized("no two lights"))
        self.assertNotEqual(normalized("2 lights"), normalized("3 lights"))

    def test_json_duplicate_and_nonfinite_rejected(self):
        for raw in [b'{"x":1,"x":2}', b'{"x":NaN}']:
            with self.assertRaises(ValueError): decode(raw)


class ReviewTests(unittest.TestCase):
    def review(self, inv):
        path = ["slot:light:eye", "bundle:beauty", "profile:two_sources"]
        hashes = {node["id"]: node["entity_sha256"] for node in inv["nodes"] if node["id"] in path}
        return {"record_id": "review-1", "finding_or_path_key": path_key(path), "decision": "retain",
                "rationale": "one visible part of a collectively described setup", "evidence_refs": ["manual review"],
                "input_entity_hashes": hashes, "recipe_versions": RECIPES, "reviewed_at": "2026-10-07T00:00:00Z",
                "support_level": "partial_support"}

    def test_change_same_id_invalidates_only_related_review(self):
        inv = fixture(); row = self.review(inv)
        self.assertEqual(review_states([row], inv, [], build_links(inv))[row["finding_or_path_key"]]["status"], "current")
        changed = copy.deepcopy(inv)
        target = next(node for node in changed["nodes"] if node["id"] == "slot:light:eye")
        target["record"]["en"] = "single catchlight"
        target["entity_sha256"] = digest([target["kind"], target["slot"], target["record"]])
        self.assertEqual(review_states([row], changed, [], build_links(changed))[row["finding_or_path_key"]]["status"], "stale")

    def test_member_removed_stales_path_even_when_nodes_exist(self):
        inv = fixture(); row = self.review(inv)
        changed = copy.deepcopy(inv)
        bundle = next(node for node in changed["nodes"] if node["id"] == "bundle:beauty")
        bundle["record"]["member_candidates"] = [{"id": "slot:light:axis"}]
        bundle["entity_sha256"] = digest([bundle["kind"], bundle["slot"], bundle["record"]])
        self.assertEqual(review_states([row], changed, [], build_links(changed))[row["finding_or_path_key"]]["status"], "stale")

    def test_missing_endpoint_hash_cannot_claim_current(self):
        inv = fixture(); row = self.review(inv)
        del row["input_entity_hashes"]["bundle:beauty"]
        self.assertEqual(review_states([row], inv, [], build_links(inv))[row["finding_or_path_key"]]["status"], "stale")

    def test_file_move_does_not_invalidate_semantics(self):
        inv = fixture(); row = self.review(inv)
        moved = copy.deepcopy(inv)
        for node in moved["nodes"]: node["source_refs"] = [{"file": "new.json", "pointer": "/x"}]
        self.assertEqual(review_states([row], moved, [], build_links(moved))[row["finding_or_path_key"]]["status"], "current")

    def test_duplicate_review_record_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/"reviews.ndjson"
            row = self.review(fixture())
            path.write_bytes(canonical(row)+b'\n'+canonical(row)+b'\n')
            with self.assertRaisesRegex(MaintenanceError, "duplicate review"): load_reviews(path)


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.capture = captured(self.root)
        self.output = self.root/"report"
        write_report(self.capture, self.output)

    def test_draft_not_queryable(self):
        path = self.root/"draft"
        write_report(captured(self.root, "draft"), path)
        with self.assertRaisesRegex(MaintenanceError, "draft_not_queryable"):
            load_report(path, require_links=True)

    def test_corrupt_report_member_rejected(self):
        (self.output/"links.json").write_bytes(b'{}')
        with self.assertRaisesRegex(MaintenanceError, "checksum mismatch"): load_report(self.output)

    def test_staging_refuses_overwrite(self):
        with self.assertRaisesRegex(MaintenanceError, "output_exists"): write_report(self.capture, self.output)

    def test_unsafe_report_member_rejected(self):
        path = self.output/"manifest.json"; manifest=decode(path.read_bytes())
        manifest["files"]["../outside"] = "a" * 64
        manifest["report_id"] = digest({key: value for key, value in manifest.items() if key != "report_id"})
        path.write_bytes(canonical(manifest))
        with self.assertRaisesRegex(MaintenanceError, "unsafe report member"): load_report(self.output)

    def test_latest_rejects_source_root_and_generation_mismatch(self):
        report=load_report(self.output)
        with self.assertRaisesRegex(MaintenanceError, "authority/root"):
            require_current(report, self.root/"other", self.root)
        snapshot=SimpleNamespace(generation_id="c"*64, manifest={"source_fingerprint":"b"*64})
        with patch('tools.photo_data_maintenance.report.current_generation', return_value=snapshot):
            with self.assertRaisesRegex(MaintenanceError, "current verified source"):
                require_current(report, self.root, self.root)

    def test_coordinated_checksum_rewrite_rejected_against_source(self):
        invpath=self.output/"inventory.json"; inv=decode(invpath.read_bytes())
        node=next(row for row in inv["nodes"] if row["id"] == "slot:light:eye")
        node["record"]["en"]="wrong rewritten description"
        node["entity_sha256"]=digest([node["kind"],node["slot"],node["record"]])
        invpath.write_bytes(canonical(inv))
        path=self.output/"manifest.json"; manifest=decode(path.read_bytes())
        manifest["files"]["inventory.json"]=sha(invpath.read_bytes())
        manifest["report_id"]=digest({key:value for key,value in manifest.items() if key != "report_id"})
        path.write_bytes(canonical(manifest))
        report=load_report(self.output)
        snapshot=SimpleNamespace(generation_id="a"*64, manifest={"source_fingerprint":"b"*64})
        with patch('tools.photo_data_maintenance.report.current_generation', return_value=snapshot), patch('tools.photo_data_maintenance.report.capture_generation', return_value=self.capture):
            with self.assertRaisesRegex(MaintenanceError, "differs from verified generation"):
                require_current(report, self.root, self.root)

    def test_late_publisher_cannot_replace_current(self):
        store=self.root/"store"
        with patch('tools.photo_data_maintenance.report.require_current'):
            first=activate(self.output,store,self.root,self.root,None)
            with self.assertRaisesRegex(MaintenanceError,"publication_superseded"):
                activate(self.output,store,self.root,self.root,None)
        self.assertEqual(read_pointer(pointer_directory(store,str(self.root))),first)

    def test_failed_current_check_leaves_pointer_unchanged(self):
        store=self.root/"store"
        with patch('tools.photo_data_maintenance.report.require_current',side_effect=MaintenanceError('source_revision_pending','pending')):
            with self.assertRaises(MaintenanceError): activate(self.output,store,self.root,self.root,None)
        self.assertIsNone(read_pointer(pointer_directory(store,str(self.root))))

    def test_current_pointer_checked_against_report(self):
        store=self.root/"store"
        with patch('tools.photo_data_maintenance.report.require_current'):
            pointer=activate(self.output,store,self.root,self.root,None)
        self.assertTrue(current_report(store,self.root).is_dir())
        pointer["generation_id"]="f"*64
        (pointer_directory(store,str(self.root))/"CURRENT.json").write_bytes(canonical(pointer))
        with self.assertRaisesRegex(MaintenanceError,"differs from report bindings"):
            current_report(store,self.root)

    def test_deterministic_bodies_and_diff(self):
        other=self.root/"other"; write_report(self.capture,other)
        for name in ["inventory.json","links.json","findings.json"]:
            self.assertEqual((other/name).read_bytes(),(self.output/name).read_bytes())
        self.assertEqual(difference(load_report(self.output),load_report(other))["meaning_changed"],[])


class DraftCaptureTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/"skill"; assets=self.root/"assets"; assets.mkdir(parents=True)
        # Copy only authored JSON, not vectors or the user's mutable checkout.
        manifest=decode((DEFAULT_ROOT/'assets/photo_prompt_source_manifest.json').read_bytes())
        names={'photo_prompt_tags.json','photo_prompt_visual_obligations.json','photo_prompt_source_manifest.json','photo_prompt_quality_layers.json'}
        names.update(row['file'] for row in manifest['sources'])
        for name in names:
            source=DEFAULT_ROOT/'assets'/name
            if source.is_file(): shutil.copyfile(source,assets/name)
        self.store=Path(self.tmp.name)/'runtime'

    def test_content_change_during_draft_capture_rejected(self):
        def edit():
            path=self.root/'assets/photo_prompt_tags.json'
            path.write_bytes(path.read_bytes()+b'\n')
        with self.assertRaisesRegex(MaintenanceError,'capture_changed'):
            capture_draft(self.root,runtime_store=self.store,after_capture=edit)

    def test_quality_policy_change_during_capture_rejected(self):
        def edit():
            (self.root/'assets/photo_prompt_quality_layers.json').write_bytes(b'{}')
        with self.assertRaisesRegex(MaintenanceError,'capture_changed'):
            capture_draft(self.root,runtime_store=self.store,after_capture=edit)

    def test_malformed_semantics_preserves_diagnostic_report(self):
        path=self.root/'assets/photo_prompt_visual_obligations.json'
        value=decode(path.read_bytes());value['profiles'][0]['semantics']='malformed draft';path.write_bytes(canonical(value))
        result=capture_draft(self.root,runtime_store=self.store)
        manifest=write_report(result,Path(self.tmp.name)/'report')
        self.assertGreater(manifest['findings_count']['error'],0)
        self.assertEqual(manifest['validation_status'],'invalid')
        self.assertIn('photo_prompt_quality_layers.json',result['source_files'])

    def test_malformed_slot_collection_preserves_invalid_draft(self):
        path=self.root/'assets/photo_prompt_tags.json'
        original=decode(path.read_bytes())
        for malformed in ([], 'unfinished draft slots'):
            with self.subTest(slots=malformed):
                value=json.loads(json.dumps(original));value['slots']=malformed
                path.write_bytes(canonical(value))
                result=capture_draft(self.root,runtime_store=self.store)
                output=Path(self.tmp.name)/('report-array' if isinstance(malformed,list) else 'report-string')
                manifest=write_report(result,output)
                self.assertGreater(manifest['findings_count']['error'],0)
                self.assertEqual(manifest['validation_status'],'invalid')
                self.assertEqual(result['source_files'][path.name],canonical(value))

    def test_unregistered_source_is_not_adopted(self):
        path=self.root/'assets/photo_prompt_surprise_extension.json';path.write_bytes(b'{"slots":{"prop":[{"id":"surprise"}]}}')
        result=capture_draft(self.root,runtime_store=self.store)
        self.assertTrue(any(row['rule']=='unregistered_source' for row in result['findings']))
        self.assertFalse(any(node['id']=='slot:prop:surprise' for node in result['inventory']['nodes']))

    def test_unfinished_cooperative_edit_is_incomplete(self):
        from tools.photo_data_maintenance.corpus import runtime
        rt,_,_=runtime(self.root)
        directory=rt.SnapshotPublisher(self.root,self.store).directory;directory.mkdir(parents=True)
        (directory/'SOURCE.json').write_bytes(canonical({'epoch':1,'editing':'pending-revision'}))
        result=capture_draft(self.root,runtime_store=self.store)
        self.assertTrue(result['binding']['editing_pending'])
        manifest=write_report(result,Path(self.tmp.name)/'report')
        self.assertEqual(manifest['validation_status'],'incomplete')


if __name__ == '__main__': unittest.main()
