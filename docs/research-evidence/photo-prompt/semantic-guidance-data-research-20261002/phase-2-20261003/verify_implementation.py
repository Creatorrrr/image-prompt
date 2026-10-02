"""Verify installed data against the frozen research and implementation baselines."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

from build_plan import OUT, ROOT, read, sha

ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
STAGE = ROOT / "tmp/semantic-guidance-apply-20261003"
EVIDENCE = OUT / "implementation"

def load(path): return json.loads(path.read_text())
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def test_receipt(prefix, require_pass=True):
    log = (STAGE / f"{prefix}-tests.log").read_text()
    suites = ET.parse(STAGE / f"{prefix}-tests.xml").getroot().findall("testsuite")
    failed = [
        {"classname": case.get("classname"), "name": case.get("name")}
        for suite in suites for case in suite.iter("testcase")
        if case.find("failure") is not None or case.find("error") is not None
    ]
    if require_pass:
        assert not failed, failed
        assert all(int(s.get("failures", 0)) == int(s.get("errors", 0)) == 0 for s in suites)
    summary = re.search(r"(\d+) passed(?:, (\d+) subtests passed)? in ([\d.]+)s", log)
    assert summary, "Completed pytest result missing: " + prefix
    return {"status": "FAIL" if failed else "PASS", "passed_primary_tests": int(summary[1]), "passed_subtests": int(summary[2] or 0),
            "duration_seconds": float(summary[3]), "failed_cases": failed,
            "junit_sha256": digest(STAGE / f"{prefix}-tests.xml"),
            "log_sha256": digest(STAGE / f"{prefix}-tests.log")}

def main(require_tests):
    sys.path.insert(0, str(ASSETS.parent / "scripts"))
    import prompt_generator as pg
    baseline = load(EVIDENCE / "baseline.json")
    snapshot = read("current-snapshot.json")
    plans = read("profile-change-plan.json")["plans"]
    graph_plan = read("character-scope-plan.json")
    receipt = load(EVIDENCE / "install-receipt.json")
    installed = {r["path"] for r in receipt["files"]}
    for row in receipt["files"]:
        assert digest(ROOT / row["path"]) == row["after_sha256"], row["path"]
    changed_tests = {r["path"] for r in receipt.get("test_changes", [])}
    for row in receipt.get("test_changes", []):
        assert baseline["protected_file_sha256"][row["path"]] == row["before_sha256"]
        assert digest(ROOT / row["path"]) == row["after_sha256"]
    unchanged = {p: h for p, h in baseline["protected_file_sha256"].items() if p not in installed | changed_tests}
    for relative, expected in unchanged.items():
        assert digest(ROOT / relative) == expected, "Unrelated source changed: " + relative
    for relative, expected in baseline["copied_asset_sha256"].items():
        if relative not in installed:
            assert digest(ROOT / relative) == expected, relative

    # Compare complete authored JSON records, not only the edited fields.
    targets_by_file = {}
    for plan in plans:
        targets_by_file.setdefault(Path(plan["source_file"]).name, {})[plan["profile_id"]] = plan
    for name, file_plans in targets_by_file.items():
        before, after = load(STAGE / "before/assets" / name), load(ASSETS / name)
        assert {k: v for k, v in before.items() if k != "profiles"} == {k: v for k, v in after.items() if k != "profiles"}
        assert [r["id"] for r in before["profiles"]] == [r["id"] for r in after["profiles"]]
        for old, new in zip(before["profiles"], after["profiles"]):
            plan = file_plans.get(new["id"])
            if plan:
                assert sha(old) == plan["before_raw_profile_sha256"]
                assert sha(new) == plan["after_raw_profile_sha256"]
            else:
                assert old == new, new["id"]
    graph_name = Path(graph_plan["source_file"]).name
    old_graph, new_graph = load(STAGE / "before/assets" / graph_name), load(ASSETS / graph_name)
    old_record = next(r for r in old_graph["character_mechanism_graph"]["concept_profiles"] if r["id"] == "kuudere")
    new_record = next(r for r in new_graph["character_mechanism_graph"]["concept_profiles"] if r["id"] == "kuudere")
    assert sha(old_record) == graph_plan["before_sha256"]
    repair_path = EVIDENCE / "repair-plan.json"
    graph_after_sha = load(repair_path)["after_record_sha256"] if receipt.get("repair") else graph_plan["after_sha256"]
    assert sha(new_record) == graph_after_sha
    restored_graph = copy.deepcopy(new_graph)
    restored_graph["character_mechanism_graph"]["concept_profiles"] = [old_record if r["id"] == "kuudere" else r
        for r in restored_graph["character_mechanism_graph"]["concept_profiles"]]
    assert restored_graph == old_graph
    pg.validate_character_mechanism_graph(new_graph)

    registry = pg.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
    profiles = {p["id"]: p for p in registry["profiles"]}
    preserved_fields = preserved_gates = 0
    for plan in plans:
        pid = plan["profile_id"]
        before, after = snapshot["selected_profiles"][pid], profiles[pid]
        assert before["required_evidence_fields"] == after["required_evidence_fields"]
        assert before["runtime_expression"] == after["runtime_expression"]
        assert [(g["id"], g["review_scale"]) for g in before["render_gates"]] == [(g["id"], g["review_scale"]) for g in after["render_gates"]]
        for key in ("exact_terms", "hard_activation", "requires_adult_character"):
            assert before["activation"].get(key) == after["activation"].get(key), (pid, key)
        old_component = before["semantics"].get("component_semantics", {})
        new_component = after["semantics"].get("component_semantics", {})
        for key in ("required_group_ids", "minimum_component_groups"):
            assert old_component.get(key) == new_component.get(key), (pid, key)
        for field in before["required_evidence_fields"]:
            assert before["evidence_requirements"][field]["min_content_words"] == after["evidence_requirements"][field]["min_content_words"]
        preserved_fields += len(after["required_evidence_fields"])
        preserved_gates += len(after["render_gates"])

    visual = pg.load_visual_profile_index(ASSETS / "photo_prompt_visual_profile_index.json", registry)
    old_visual = load(STAGE / "before/assets/photo_prompt_visual_profile_index.json")
    assert visual["exact_lookup"] == old_visual["exact_lookup"]
    changed_visual = sorted(k for k, v in visual["entries"].items() if v != old_visual["entries"][k])
    assert changed_visual == sorted(p["profile_id"] for p in plans)
    data = pg.load_json(ASSETS / "photo_prompt_tags.json")
    semantic = pg.load_semantic_index_payload(ASSETS / "photo_prompt_semantic_index.json")
    pg.validate_semantic_index_metadata(semantic, data)
    old_manifest = load(STAGE / "before/assets/photo_prompt_semantic_index.json")
    old_entries = {}
    for row in old_manifest["shards"]:
        path = ASSETS / row["path"]
        assert digest(path) == row["sha256"], "Original immutable shard changed: " + row["path"]
        old_entries.update(load(path)["entries"])
    assert semantic["entry_order"] == old_manifest["entry_order"]
    changed_semantic = sorted(k for k, v in semantic["entries"].items() if v != old_entries[k])
    assert changed_semantic == ["character_response_concept:kuudere"]
    for key in ("provider", "embedding_model", "embedding_dimensions"):
        assert visual[key] == old_visual[key]
        assert semantic[key] == old_manifest[key]
    before_data = copy.deepcopy(data)
    before_data["character_mechanism_graph"]["concept_profiles"] = [old_record if r["id"] == "kuudere" else r
        for r in before_data["character_mechanism_graph"]["concept_profiles"]]
    assert pg.dictionary_hash(before_data) == old_manifest["dictionary_hash"]

    result = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if require_tests else "DATA_CHECKS_PASS_TESTS_PENDING",
        "changed_authored_files": len(targets_by_file) + 1,
        "changed_profile_records": len(plans), "profile_field_operations": sum(len(p["operations"]) for p in plans),
        "changed_graph_records": 1, "graph_field_operations": len(graph_plan["operations"]),
        "unrelated_protected_files_preserved": len(unchanged),
        "original_shard_files_preserved": sum("_shards/" in p for p in unchanged),
        "frozen_holdout_files_preserved": sum("holdout" in p for p in unchanged),
        "required_evidence_fields_preserved": preserved_fields, "render_gate_ids_and_scales_preserved": preserved_gates,
        "runtime_modes_preserved": True, "exact_and_hard_activation_preserved": True,
        "visual_index": {"profiles": len(visual["entries"]), "exact_terms": len(visual["exact_lookup"]),
            "changed_entries": changed_visual, "reused_entries_unchanged": len(visual["entries"]) - len(changed_visual),
            "registry_sha256": visual["registry_sha256"]},
        "semantic_index": {"entries": len(semantic["entries"]), "changed_entries": changed_semantic,
            "reused_entries_unchanged": len(semantic["entries"]) - len(changed_semantic),
            "dictionary_hash": semantic["dictionary_hash"], "shards": len(semantic["shards"])},
        "embedding_provider": visual["provider"], "embedding_model": visual["embedding_model"],
        "embedding_dimensions": visual["embedding_dimensions"],
        "unique_changed_embedding_items": len(changed_visual) + len(changed_semantic),
        "successful_embedding_items": len(changed_visual) + len(changed_semantic) + receipt.get("repair", {}).get("successful_embedding_items", 0),
        "llm_evaluation_calls": 0, "image_generation_calls": 0,
        "skill_logic_files_changed_by_this_task": 0,
        "new_regression_test_files": 1, "adjusted_existing_test_files": len(changed_tests),
        "graph_regression_repair_applied": bool(receipt.get("repair")),
        "unverified": ["independent language/semantic evaluation", "model retrieval precision and recall",
            "model moderation outcomes", "generated image structure preservation", "user acceptance"],
    }
    if require_tests:
        result["tests"] = {"baseline": test_receipt("baseline"),
            "initial_post_apply": test_receipt("post-apply", require_pass=False),
            "final_post_repair": test_receipt("post-repair")}
        for name, expected in {
            "post-apply-dictionary-validation.log": "photo prompt dictionary metadata is valid",
            "post-apply-visual-index-check.log": "visual profile index ok:",
        }.items():
            assert expected in (STAGE / name).read_text(), name
        result["dictionary_validation"] = "PASS"
    (EVIDENCE / "post-apply-validation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-tests", action="store_true")
    main(parser.parse_args().require_tests)
