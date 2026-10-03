"""Run merge-focused regression modules in independent unittest processes."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / "tests"
sys.path.insert(0, str(ROOT))

MODULES = (
    "test_photo_acting_expression_data",
    "test_photo_pose_vocabulary_semantics",
    "test_photo_liminal_active_use_korean_data_cleanup",
    "test_photo_scene_data_cleanup",
    "test_photo_capture_physics_alternatives",
    "test_photo_cumulonimbus_anvil_alternative",
    "test_photo_dress_positive_paraphrase",
    "test_photo_environment_alternative_consistency",
    "test_photo_glacier_surface_alternative",
    "test_photo_kebaya_material_alternative",
    "test_photo_leading_line_gate_alternatives",
    "test_photo_object_morphology_ownership",
    "test_photo_overhead_hand_alternative",
    "test_photo_prop_conditional_contact",
    "test_photo_receiver_material_response",
    "test_photo_residual_positive_guards",
    "test_photo_wet_hair_weight_alternative",
    "test_photo_wrap_skirt_side_alternative",
    "test_photo_semantic_index",
    "test_photo_visual_profile_retrieval",
    "test_photo_visual_obligations",
    "test_photo_candidate_semantics",
    "test_photo_research_integration",
    "test_photo_authorial_core_v6",
    "test_photo_body_morphology_semantics",
    "test_photo_traditional_clothing_semantics",
    "test_photo_hair_visual_semantics",
    "test_photo_natural_environment_semantics",
    "test_photo_lighting_visual_semantics",
    "test_photo_portrait_composition_semantics",
    "test_photo_weapon_visual_semantics",
    "test_photo_positive_retrieval",
    "test_photo_prepack_isolation",
)


def test_ids(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from test_ids(item)
        else:
            yield item.id()


def worker(module):
    if module not in MODULES:
        raise ValueError(module)
    OUT.mkdir(parents=True, exist_ok=True)
    suite = unittest.TestLoader().discover(str(ROOT / "tests"), pattern=module + ".py")
    discovered = list(test_ids(suite))
    start = time.monotonic()
    with (OUT / (module + ".log")).open("w") as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    record = {
        "module": module,
        "discovered_ids": discovered,
        "tests_run": result.testsRun,
        "success": result.wasSuccessful(),
        "failures": [{"id": test.id(), "traceback": trace} for test, trace in result.failures],
        "errors": [{"id": test.id(), "traceback": trace} for test, trace in result.errors],
        "skipped": [{"id": test.id(), "reason": reason} for test, reason in result.skipped],
        "expected_failures": [test.id() for test, _ in result.expectedFailures],
        "unexpected_successes": [test.id() for test in result.unexpectedSuccesses],
        "elapsed_seconds": round(time.monotonic() - start, 3),
    }
    (OUT / (module + ".json")).write_text(json.dumps(record, indent=2) + "\n")
    return 0 if record["success"] else 1


def launch(module):
    completed = subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), "--worker", module],
        cwd=ROOT, capture_output=True, text=True,
    )
    path = OUT / (module + ".json")
    if not path.exists():
        raise RuntimeError(f"{module}: {completed.returncode}: {completed.stderr[-2000:]}")
    record = json.loads(path.read_text())
    record["process_exit_code"] = completed.returncode
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker")
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    if args.worker:
        return worker(args.worker)
    start = time.monotonic()
    expected = sorted(
        test_id
        for module in MODULES
        for test_id in test_ids(unittest.TestLoader().discover(str(ROOT / "tests"), pattern=module + ".py"))
    )
    print(f"Running {len(expected)} tests in {len(MODULES)} selected modules", flush=True)
    records = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(launch, module) for module in MODULES]
        for future in as_completed(futures):
            record = future.result()
            records.append(record)
            print(f"{len(records)}/{len(MODULES)} {record['module']}: "
                  f"{'PASS' if record['success'] else 'FAIL'} {record['tests_run']}", flush=True)
    actual = sorted(test_id for record in records for test_id in record["discovered_ids"])
    summary = {
        "schema_version": "acting-expression-merge-focused-tests/v1",
        "coverage": "selected local, upstream and shared runtime modules; not the entire repository",
        "discovery_multiset_equal": actual == expected,
        "discovery_ids_sha256": hashlib.sha256("\n".join(expected).encode()).hexdigest(),
        "module_count": len(records),
        "tests_discovered": len(expected),
        "tests_run": sum(record["tests_run"] for record in records),
        "success": actual == expected and all(record["success"] for record in records),
        "failures": [row for record in records for row in record["failures"]],
        "errors": [row for record in records for row in record["errors"]],
        "skipped": [row for record in records for row in record["skipped"]],
        "expected_failures": [row for record in records for row in record["expected_failures"]],
        "unexpected_successes": [row for record in records for row in record["unexpected_successes"]],
        "elapsed_seconds": round(time.monotonic() - start, 3),
        "modules": sorted(records, key=lambda record: record["module"]),
    }
    (HERE / "FOCUSED-TESTS.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({key: value for key, value in summary.items() if key != "modules"}), flush=True)
    return 0 if summary["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
