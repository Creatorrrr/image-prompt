"""Compare actual failure records with source-isolated pre-Y2K replays."""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def normalized_id(value):
    return value.removeprefix("tests.")


def locus(trace):
    frames = re.findall(r'File "[^"]*/tests/([^"/]+)", line (\d+), in ([^\n]+)', trace)
    return list(frames[-1]) if frames else None


def exception_type(trace):
    for line in reversed(trace.splitlines()):
        match = re.match(r"([\w.]+(?:Error|Failure|Exception))(?::|$)", line)
        if match:
            return match[1]
    return None


baseline = {}
files = []
bodycon_before = json.loads((HERE / "bodycon-boundary-before.json").read_text())
bodycon_after = json.loads((HERE / "bodycon-boundary-after.json").read_text())
bodycon_change_verified = (
    bodycon_before["frozen_fixture_compatibility_wrapper"]["hard_profile_ids"] == []
    and bodycon_after["frozen_fixture_compatibility_wrapper"]["hard_profile_ids"] == []
    and bodycon_before["frozen_fixture_compatibility_wrapper"]["optional_profile_ids"] == []
    and bodycon_after["frozen_fixture_compatibility_wrapper"]["optional_profile_ids"] == ["y2kr_bodycon"]
    and not bodycon_after["qipao_hard_activated"]
)
for path in sorted(HERE.glob("baseline-*-comparison.json")):
    data = json.loads(path.read_text())
    for field, kind in [("failure_evidence", "failure"), ("error_evidence", "error")]:
        for row in data.get(field, []):
            baseline.setdefault(normalized_id(row["id"]), []).append({"kind": kind, "traceback": row["traceback"], "file": str(path)})
    if "failure_evidence" in data:
        files.append(str(path))
rows = []
for path in sorted((HERE / "completed-full-suite").glob("*.result.json")):
    data = json.loads(path.read_text())
    for field, kind in [("failures", "failure"), ("errors", "error")]:
        for failure in data[field]:
            identifier = normalized_id(failure["id"])
            candidates = baseline.get(identifier, [])
            matched = next((row for row in candidates if row["kind"] == kind and locus(row["traceback"]) == locus(failure["traceback"]) and exception_type(row["traceback"]) == exception_type(failure["traceback"])), None)
            new_population_change = (bodycon_change_verified and kind == "failure" and identifier == "test_photo_traditional_clothing_semantics.PhotoTraditionalClothingSemanticsTests.test_exact_candidate_and_hard_negative_routing_fixture (case='negative_qipao_collar_only')")
            rows.append({"id": identifier, "kind": kind, "test_assertion_locus": locus(failure["traceback"]), "exception_type": exception_type(failure["traceback"]),
                         "comparison": "same_test_kind_and_locus_reproduced_before_y2k" if matched else "same_test_failed_before_with_different_evidence" if candidates else "new_optional_candidate_population_in_legacy_fixture" if new_population_change else "not_yet_baseline_compared",
                         "baseline_record": matched["file"] if matched else candidates[0]["file"] if candidates else None})
summary = {"failure_events": len(rows), "same_test_kind_and_locus_reproduced": sum(row["comparison"] == "same_test_kind_and_locus_reproduced_before_y2k" for row in rows),
           "different_evidence_for_same_test": sum(row["comparison"] == "same_test_failed_before_with_different_evidence" for row in rows),
           "new_optional_candidate_population_in_legacy_fixture": sum(row["comparison"] == "new_optional_candidate_population_in_legacy_fixture" for row in rows),
           "not_yet_baseline_compared": sum(row["comparison"] == "not_yet_baseline_compared" for row in rows), "baseline_records": files, "results": rows,
           "bodycon_boundary_evidence": {"before": str(HERE / "bodycon-boundary-before.json"), "after": str(HERE / "bodycon-boundary-after.json"), "compatibility_wrapper_population_change_verified": bodycon_change_verified, "typed_resolver_hard_and_optional_after": [bodycon_after["hard_profile_ids"], bodycon_after["optional_profile_ids"]]},
           "scope": "Matches test IDs, outcome kinds, exception types and test assertion locations. It does not establish equality of every diff value or prove absence of all behavioral regressions."}
(HERE / "full-failure-baseline-comparison.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps({key: value for key, value in summary.items() if key not in ["results", "baseline_records"]}))
