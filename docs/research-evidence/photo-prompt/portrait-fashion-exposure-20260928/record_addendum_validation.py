"""Bind appended-analysis checks; distinguish frozen first-pass results."""
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
    value = (HERE / name).read_text()
    assert re.search(rf"Ran {count} tests in", value) and value.rstrip().endswith("OK"), name
    return {"status": "PASS", "test_methods": count, "log": name, "phase": "appended_analysis_final_data"}


def diagnostics(prefix, visual):
    report = read(prefix + "retrieval-results.json")
    assert report["registry_sha256"] == visual["registry_sha256"]
    fixture = HERE / (prefix + "retrieval_probes.json")
    assert hashlib.sha256(fixture.read_bytes()).hexdigest() == report["fixture_sha256"]
    cases = report["cases"]
    positive = [c for c in cases if c["kind"] == "positive_paraphrase"]
    hard = sum(c["any_new_hard_hit"] for c in cases)
    assert hard == 0, "Advisory discovery must not create mandatory geometry"
    return {
        "expected_positive_discovery": f"{sum(bool(c['expected_discovered']) for c in positive)}/{len(positive)}",
        "positive_misses": [c["id"] for c in positive if not c["expected_discovered"]],
        "new_hard_activations": f"{hard}/{len(cases)}",
        "adjacent_cases_with_optional_hits": [c["id"] for c in cases if c["kind"] == "adjacent_negative" and c["new_optional_hits"]],
        "fixture_sha256": report["fixture_sha256"], "independent_holdout": False,
        "context": "Forced adult_context=True for every diagnostic, including nonhuman and negative queries; ranking stress, not actual nonhuman candidate adoption.",
        "results": prefix + "retrieval-results.json",
        "limit": "Optional hit presence is a diagnostic, not evidence of automatic adoption. Negated or unrelated regions may still retrieve adjacent optional concepts.",
    }


def main():
    historical = read("revisions/initial/validation.json")
    snapshot = read("revisions/initial/snapshot-manifest.json")
    for item in snapshot["files"].values():
        raw = (HERE / "revisions/initial" / item["snapshot"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == item["sha256"]
    assert (HERE / "retrieval_probes.json").read_bytes() == (HERE / "revisions/initial/retrieval_probes.json").read_bytes()
    sources, catalog, proposals = read("sources.json"), read("keyword_catalog.json"), read("proposals.json")
    ext = json.loads((ASSETS / "photo_prompt_portrait_fashion_exposure_extension.json").read_text())
    profiles = json.loads((ASSETS / "photo_prompt_visual_obligations_portrait_fashion_exposure.json").read_text())["profiles"]
    visual = json.loads((ASSETS / "photo_prompt_visual_profile_index.json").read_text())
    semantic = json.loads((ASSETS / "photo_prompt_semantic_index.json").read_text())
    assert "metadata is valid" in (HERE / "dictionary-validation.log").read_text()
    assert "index ok" in (HERE / "visual-index-check.log").read_text()
    assert read("semantic-index-check.log")["status"] == "ok"
    assert read("projection-idempotence.json")["status"] == "PASS"
    assert len(proposals["proposals"]) == sum(len(r) for r in ext["slots"].values())
    report = {
        "checked_at": "2026-09-28", "phase": "appended_analysis",
        "scope": "Local research and runtime-data integration with scoped contracts and authored retrieval diagnostics; no pixels, aesthetics or SNS qualification.",
        "base_revision": historical["base_revision"],
        "source_count": len(sources["sources"]), "source_counts_by_phase": sources["source_counts_by_phase"],
        "keyword_table_group_count": catalog["group_count"], "term_form_count": catalog["term_form_count"],
        "keyword_phase_counts": catalog["phase_counts"], "keyword_counting_note": catalog["counting_note"],
        "cumulative_profiles": len(profiles), "cumulative_candidates": len(proposals["proposals"]),
        "cumulative_optional_bundles": len(ext["visual_semantics"]),
        "appended_delta": {"profiles": len(profiles) - historical["new_profiles"],
                           "candidates": len(proposals["proposals"]) - historical["new_candidates"],
                           "optional_bundles": len(ext["visual_semantics"]) - historical["new_optional_bundles"]},
        "focused_tests": passed_log("focused-tests.log", 12),
        "related_contracts": passed_log("remaining-contracts.log", 48),
        "dictionary_validation": "PASS", "visual_index_validation": "PASS", "semantic_index_validation": "PASS",
        "visual_index": {"profiles": len(visual["entries"]), "exact_terms": len(visual["exact_lookup"]), "registry_sha256": visual["registry_sha256"]},
        "semantic_index": {"entries": semantic["entry_count"], "shards": len(semantic["shards"]), "dictionary_sha256": semantic["dictionary_hash"]},
        "embedding_reuse": read("embedding-reuse.json"),
        "original_retrieval_diagnostics_on_updated_index": diagnostics("", visual),
        "appended_retrieval_diagnostics": diagnostics("addendum_", visual),
        "historical_first_pass": {
            "validation": "revisions/initial/validation.json", "snapshot": "revisions/initial/snapshot-manifest.json",
            "broad_run": historical["initial_broad_related_run"],
            "baseline_reproduction": historical["baseline_reproduction"],
            "limit": "Routing traceback equality applies to first-pass data. The 120-row legacy routing suite and its 8 failed rows were not rerun for this appended revision. Current checks are the separately recorded 12+48 scoped methods.",
        },
        "test_authoring_repairs": {
            "first_attempt": "appended-tests-first-attempt.log",
            "reason": "Two newly authored assertions compared raw authored profiles with runtime-normalized profiles, and checked a project glossary alias in the exact-term field. Corrected to compare authored with authored and inspect project_glossary_aliases. No old fixture, expected label or retrieval query changed.",
        },
        "pixel_status": "NOT_RUN", "user_judgment": "NOT_REQUESTED", "sns_effectiveness": "NOT_EVALUATED",
        "complete_suite_pass": False, "git_delivery": "LOCAL_UNCOMMITTED",
    }
    paths = [p for p in HERE.iterdir() if p.suffix in {".py", ".json", ".log", ".md"} and p.name != "validation.json"]
    paths.extend(ASSETS / n for n in ["photo_prompt_portrait_fashion_exposure_extension.json", "photo_prompt_visual_obligations_portrait_fashion_exposure.json", "photo_prompt_tags.json", "photo_prompt_visual_profile_index.json", "photo_prompt_semantic_index.json"])
    paths.extend([ROOT / "skills/photo-prompt-image-generator/scripts/prompt_generator.py", ROOT / "tests/test_photo_portrait_fashion_exposure.py", ROOT / "docs/research-evidence/photo-prompt/extension-maintenance/photo_prompt_portrait_fashion_exposure_extension.json"])
    report["file_sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths))}
    (HERE / "validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"Bound {len(profiles)} profiles and {len(proposals['proposals'])} candidates to current scoped checks.")


if __name__ == "__main__":
    main()
