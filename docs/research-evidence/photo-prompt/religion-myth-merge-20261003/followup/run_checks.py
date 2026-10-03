"""Verify the late data-only merge against its affected contracts and frozen pack."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
MODULES = [
    "tests.test_photo_slide_thickness_alternative",
    "tests.test_photo_convoy_route_alternative",
    "tests.test_photo_ghost_ship_gate_alternative",
    "tests.test_photo_religion_iconography_alternatives",
    "tests.test_photo_visual_profile_retrieval",
    "tests.test_photo_semantic_index",
    "tests.test_photo_era_visual_semantics",
    "tests.test_photo_mythology_visual_semantics",
    "tests.test_photo_religion_iconography_boundary_history",
    "tests.test_subculture_illustration_photo_boundary",
    "tests.test_photo_current_boundary_snapshot",
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reconcile-existing", action="store_true",
                        help="Check saved test records and pack without rerunning their subprocesses.")
    args = parser.parse_args()
    environment = os.environ.copy()
    for name in ("OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY", "ANTHROPIC_API_KEY"):
        environment[name] = ""
    output = HERE / "checks"
    output.mkdir(exist_ok=True)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()
    runner = HERE.parent / "run_tests.py"

    def run_module(module):
        log = output / f"{module}.log"
        with log.open("w") as stream:
            result = subprocess.run([sys.executable, str(runner), "--repo", str(REPO),
                                     "--output", str(output), "--module", module],
                                    cwd=REPO, env=environment, stdout=stream, stderr=subprocess.STDOUT)
        return {"module": module, "returncode": result.returncode, "log_sha256": digest(log)}

    def run_boundary(*, generate=True):
        baseline_path = REPO / "skills/subculture-illustration-image-generator/assets/photo_regression_baseline_v7.json"
        baseline = json.loads(baseline_path.read_text())
        command = baseline["command"].copy()
        generated = HERE / "boundary-pack.json"
        command[command.index("--output-file") + 1] = str(generated)
        if generate:
            with (HERE / "boundary-pack.log").open("w") as stream:
                result = subprocess.run(command, cwd=REPO, env=environment, stdout=stream, stderr=subprocess.STDOUT)
            assert result.returncode == 0
        packs = json.loads(generated.read_text())
        assert isinstance(packs, list) and len(packs) == 1
        pack = packs[0]
        assert digest(generated) == baseline["sha256"]
        assert pack["pack_id"] == baseline["pack_id"]
        return {"output_sha256": digest(generated), "pack_id": pack["pack_id"],
                "unchanged_from_v7": True}

    results = []
    if args.reconcile_existing:
        for module in MODULES:
            record = json.loads((output / f"{module}.json").read_text())
            assert not record["failures"] and not record["errors"] and not record["unexpected_successes"]
            results.append({"module": module, "returncode": 0,
                            "log_sha256": digest(output / f"{module}.log")})
        boundary = run_boundary(generate=False)
    else:
        with ThreadPoolExecutor(max_workers=4) as pool:
            futures = {pool.submit(run_module, module): module for module in MODULES}
            boundary_future = pool.submit(run_boundary)
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                print(f"Completed {len(results)}/{len(MODULES)}: {result['module']} rc={result['returncode']}", flush=True)
            boundary = boundary_future.result()
    records = [json.loads((output / f"{module}.json").read_text()) for module in MODULES]
    runtime = {p.name: digest(p) for p in (REPO / "skills/photo-prompt-image-generator/scripts").glob("*.py")}
    data = {p.name: digest(p) for p in (REPO / "skills/photo-prompt-image-generator/assets").glob("*.json")}
    assert all(r["runtime_sources"] == runtime and r["data_sources"] == data for r in records)
    assert all(r["returncode"] == 0 for r in results)
    assert all(not r["failures"] and not r["errors"] for r in records)
    summary = {"schema_version": "religion-myth-followup-verification/v1", "commit": commit,
               "scope": "Three late upstream data alternatives, their strict duties, combined index/retrieval, preserved religion semantics and both historical boundaries.",
               "tests": sum(r["tests_run"] for r in records), "modules": results,
               "failures": [], "errors": [], "source_hashes_match": True,
               "runtime_sources": runtime, "data_sources": data, "frozen_boundary": boundary,
               "summary_helper_repair": "Generated output is a one-item pack array; saved passing test records and identical pack bytes were reconciled without rerunning them.",
               "full_initial_source_verification": "../VERIFICATION.json",
               "native_calls": 0, "native_results_unchanged": "strict final 0/3 PASS"}
    (HERE / "VERIFICATION.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"tests": summary["tests"], "failures": 0, "errors": 0,
                      "frozen_boundary_unchanged": True}), flush=True)


if __name__ == "__main__":
    main()
