"""Check final evidence/source correspondence and collect the exact closure."""
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys
from sample import HERE, ROOT, SKILL
from trace_io import read_trace

sys.path[:0] = [str(ROOT), str(SKILL / "scripts")]
import photo_candidate_corpus as c
import photo_runtime_sources as runtime
import photo_slot_queries as queries
from photo_embedding_provider import validate_vector, SPACE
from verify_hybrid import frozen


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source = c.validate(c.load(SKILL / "assets"))
    baseline = c.decode((HERE / "BASELINE.json").read_bytes())
    corpus_sha = c.digest(source)
    reports = {name: c.decode((HERE / (name + ".json")).read_bytes()) for name in (
        "INTEGRITY-VERIFICATION", "HYBRID-VERIFICATION", "ADULT-HUMAN-VERIFICATION",
        "ROLE-REVERSE-VERIFICATION", "REVERSE-REVIEW-VERIFICATION", "LEDGER-SUMMARY")}
    for name, report in reports.items():
        if name != "LEDGER-SUMMARY":
            assert report["verified"]
        assert (report.get("source_sha256") or report.get("corpus_sha256")) == corpus_sha
    count = 0
    scenarios = []
    for case, language in (("linen", "en"), ("linen", "ko"), ("object", "en"), ("adult-human", "en"), ("adult-human", "ko")):
        if case == "adult-human":
            path = ROOT / reports["ADULT-HUMAN-VERIFICATION"]["fixture"]
            import prompt_generator as g
            controls = c.decode((path / "creative-controls.json").read_bytes())
            core = g.load_authorial_core_arg(path / "authorial-core.json",
                request_envelope=g.load_request_envelope_arg(path / "request-envelope.json"), creative_control_snapshot=controls)
        else:
            core, controls, _ = frozen(case)
        context = c.decode((HERE / (case + "-" + language + "-contexts.json")).read_bytes())
        trace_path = HERE / (case + "-" + language + "-retrieval.json.gz")
        trace = read_trace(trace_path)
        assert trace["canonical_sha256"] == c.digest({key: value for key, value in trace.items() if key != "canonical_sha256"})
        assert trace["corpus_sha256"] == corpus_sha and trace["query_context_sha256"] == context["canonical_sha256"]
        assert trace["source_authorial_core_sha256"] == core["canonical_sha256"]
        for slot in trace["active_slot_ids"]:
            queries.validate(context["slots"][slot], core, controls, source["slot_catalog"], slot)
            assert not trace["slot_searches"][slot]["tag_admission_filter"]
        assert len(trace["selected_candidate_ids"]) == len(set(trace["selected_candidate_ids"])) <= 64
        count += len(trace["active_slot_ids"])
        scenarios.append({"case": case, "language": language, "subject": core["subject"],
            "query_count": len(trace["active_slot_ids"]), "trace_value_sha256": c.digest(trace),
            "trace_file_sha256": sha(trace_path), "source_binding_conditions_unchanged": True})
    assert count == reports["HYBRID-VERIFICATION"]["query_count"] + reports["ADULT-HUMAN-VERIFICATION"]["query_count"] == 165
    contexts = c.decode((HERE / "ROLE-DISCOVERY-CONTEXTS.json").read_bytes())
    assert len(contexts) == 139 and set(contexts) == set(source["slot_catalog"])
    for slot, context in contexts.items():
        assert context["binding"]["slot_spec_sha256"] == c.digest(source["slot_catalog"][slot])
        assert context["text_sha256"] == hashlib.sha256(context["text"].encode()).hexdigest()
        assert context["space"] == SPACE
        validate_vector(context["vector"], SPACE["dimensions"])
        assert context["execution"]["provider_executed"] and context["execution"]["http_status"] == 200
    # The 721 new files must be precisely the active manifest closure. No old
    # layout or unrelated runtime tree is included in this task's staging.
    manifest_path = SKILL / "assets/photo_candidate_search.json"
    manifest = c.decode(manifest_path.read_bytes())
    closure = []
    for spec in [manifest["metadata"], *manifest["shards"]]:
        path = SKILL / "assets" / spec["path"]
        assert path.is_file() and path.stat().st_size == spec["bytes"] and sha(path) == spec["sha256"]
        closure.append(str(path.relative_to(ROOT)))
    assert len(closure) == len(set(closure)) == 721
    root = SKILL / "assets/photo_candidate_search_shards" / manifest["layout_id"]
    assert set(closure) == {str(path.relative_to(ROOT)) for path in root.iterdir() if path.is_file()}
    publisher = runtime.RuntimeSnapshotProvider(SKILL)
    snapshot = publisher.acquire()
    assert snapshot.generation_id == reports["HYBRID-VERIFICATION"]["generation_id"]
    for name, expected in baseline["protected_dirty_files"].items():
        assert sha(ROOT / name) == expected
    first_tests = (HERE / "NATIVE-TESTS.log").read_text()
    final_tests = (HERE / "PILOT-BOUNDARY-TESTS.log").read_text()
    assert "Ran 85 tests" in first_tests and "FAILED (errors=1)" in first_tests
    assert first_tests.count("ERROR:") == 1 and "ModuleNotFoundError: No module named 'photo_candidate_corpus'" in first_tests
    assert "Ran 12 tests" in final_tests and "\nOK\n" in final_tests
    files = {path.name: sha(path) for path in sorted(HERE.iterdir()) if path.is_file()
        and path.name not in {"FINAL-VERIFICATION.json", "COMMIT.json"}}
    report = {"schema": "photo-slot-tag-pilot-final-verification/v1", "verified": True,
        "source_sha256": corpus_sha, "generation_id": snapshot.generation_id, "layout_id": manifest["layout_id"],
        "ledger_records": reports["LEDGER-SUMMARY"]["reviewed_count"], "relationship_decisions": reports["LEDGER-SUMMARY"]["relationship_decisions"],
        "source_text_effect_condition_policy_and_binding_preservation": "pass",
        "native_tag_writes": 0, "catalog_count": len(source["slot_catalog"]),
        "native_query_count": count, "role_only_query_count": len(contexts), "scenarios": scenarios,
        "existing_selected_regression_executions_passed": 84, "new_boundary_cases_passed": 6,
        "new_module_rerun_executions_passed": 12, "initial_test_import_error_resolved": True,
        "guard_assertion_scope_correction_recorded": "FIRST-SCENARIO-CHECKPOINT.json",
        "active_index_closure_files": closure, "evidence_file_sha256": files,
        "unrelated_dirty_files_preserved": baseline["protected_dirty_files"],
        "push_performed": False, "boundary": "Stage 4 pilot and native catalog/index/runtime verification; stage 5 source corrections/metadata and stage 6 persistent tag application remain required."}
    (HERE / "FINAL-VERIFICATION.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ("verified", "ledger_records", "native_query_count", "role_only_query_count", "native_tag_writes", "catalog_count")}))


if __name__ == "__main__":
    main()
