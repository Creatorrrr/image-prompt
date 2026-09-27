"""Bind completed scoped checks and explicit unverified boundaries to final files."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"


def read(name):
    return json.loads((HERE / name).read_text())


def passed_log(name, count):
    text = (HERE / name).read_text()
    assert f"Ran {count} tests" in text and text.rstrip().endswith("OK"), name
    return {"status": "PASS", "test_methods": count, "log": name}


def main():
    sources, catalog, proposals = read("sources.json"), read("keyword_catalog.json"), read("proposals.json")
    visual = json.loads((ASSETS / "photo_prompt_visual_profile_index.json").read_text())
    semantic = json.loads((ASSETS / "photo_prompt_semantic_index.json").read_text())
    probes = read("retrieval-results.json")
    baseline, current = read("baseline-routing-reported-cases.json"), read("current-routing-reported-cases.json")
    assert baseline["failures"] == current["failures"]
    assert baseline["routing_cases"] == current["routing_cases"]
    assert not any("pfe_" in trace for trace in current["failures"])
    assert probes["registry_sha256"] == visual["registry_sha256"]
    assert read("baseline-documentation-failure.json")["unchanged_skill_bytes"]
    assert "metadata is valid" in (HERE / "dictionary-validation.log").read_text()
    assert "index ok" in (HERE / "visual-index-check.log").read_text()
    assert json.loads((HERE / "semantic-index-check.log").read_text())["status"] == "ok"
    initial_log = (HERE / "related-regression.log").read_text()
    positive = [row for row in probes["cases"] if row["kind"] == "positive_paraphrase"]
    assert len(positive) == 6 and all(row["expected_discovered"] for row in positive)
    assert not any(row["any_new_hard_hit"] for row in probes["cases"])
    extension = json.loads((ASSETS / "photo_prompt_portrait_fashion_exposure_extension.json").read_text())
    profiles = json.loads((ASSETS / "photo_prompt_visual_obligations_portrait_fashion_exposure.json").read_text())["profiles"]
    payload = {
        "checked_at": "2026-09-28",
        "scope": "Local research, data integration and scoped contract/retrieval checks; no rendered-quality or SNS-effectiveness qualification.",
        "base_revision": baseline["base_revision"],
        "source_count": len(sources["sources"]),
        "keyword_group_count": catalog["group_count"], "term_form_count": catalog["term_form_count"],
        "new_profiles": len(profiles),
        "new_candidates": sum(len(rows) for rows in extension["slots"].values()),
        "new_optional_bundles": len(extension["visual_semantics"]),
        "focused_tests": passed_log("focused-tests.log", 9),
        "remaining_related_contracts": passed_log("remaining-contracts.log", 48),
        "dictionary_validation": "PASS", "visual_index_validation": "PASS", "semantic_index_validation": "PASS",
        "visual_index": {"profiles": len(visual["entries"]), "exact_terms": len(visual["exact_lookup"]),
                         "registry_sha256": visual["registry_sha256"]},
        "semantic_index": {"entries": semantic["entry_count"], "shards": len(semantic["shards"]),
                           "dictionary_sha256": semantic["dictionary_hash"]},
        "embedding_reuse": read("embedding-reuse.json"),
        "retrieval_diagnostics": {
            "expected_positive_discovery": "6/6", "new_hard_activations": "0/12",
            "optional_false_positive_cases": [row["id"] for row in probes["cases"]
                                              if row["kind"] == "adjacent_negative" and row["new_optional_hits"]],
            "independent_holdout": False, "fixture_sha256": probes["fixture_sha256"],
            "results": "retrieval-results.json",
        },
        "initial_broad_related_run": {
            "status": "INCOMPLETE_WITH_PREEXISTING_FAILURES",
            "completed_passed_methods": len(re.findall(r"^test_.* \.\.\. ok$", initial_log, re.M)),
            "interrupted_section": "120-row legacy routing fixture; unfinished cases are not passes",
            "failed_method_types": 3,
            "observed_failed_assertions": {"skill_phrase_subtests": 4, "selection_list_test": 1, "routing_case_subtests": 8},
            "log": "related-regression.log", "complete_suite_pass": False,
        },
        "baseline_reproduction": {
            "skill_document": "baseline-documentation-failure.json",
            "selection_list": "baseline-visual-intent-failure.json",
            "routing_cases": baseline["routing_cases"], "routing_failed_cases": baseline["failed_tests"],
            "routing_tracebacks_identical_in_base_and_final": True,
            "baseline_results": "baseline-routing-reported-cases.json", "final_results": "current-routing-reported-cases.json",
            "existing_fixtures_modified": False,
        },
        "execution_note": "The newly authored homonym test was corrected to supply source records, as normal callers do; ranking query_text alone is not context authority. No existing holdout or expected outcome was changed.",
        "pixel_status": "NOT_RUN", "user_judgment": "NOT_REQUESTED",
        "sns_effectiveness": "NOT_EVALUATED", "git_delivery": "LOCAL_UNCOMMITTED",
    }
    assert len(proposals["proposals"]) == payload["new_candidates"]
    paths = [*HERE.glob("*.py"), *HERE.glob("*.json"), *HERE.glob("*.log"), HERE / "RESEARCH.md",
             ASSETS / "photo_prompt_portrait_fashion_exposure_extension.json",
             ASSETS / "photo_prompt_visual_obligations_portrait_fashion_exposure.json",
             ASSETS / "photo_prompt_tags.json", ASSETS / "photo_prompt_visual_profile_index.json",
             ASSETS / "photo_prompt_semantic_index.json",
             ROOT / "skills/photo-prompt-image-generator/scripts/prompt_generator.py",
             ROOT / "tests/test_photo_portrait_fashion_exposure.py",
             ROOT / "docs/research-evidence/photo-prompt/extension-maintenance/photo_prompt_portrait_fashion_exposure_extension.json"]
    payload["file_sha256"] = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                              for path in sorted(set(paths)) if path.name != "validation.json"}
    (HERE / "validation.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(f"Recorded {payload['source_count']} sources, {len(profiles)} profiles; 9+48 final scoped tests pass, broad run incomplete.")


if __name__ == "__main__":
    main()
