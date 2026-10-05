"""Verify the reviewed validator path repair and unchanged historical rules."""
import json
import re
import subprocess
import sys
import time
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT))
groups = [
    ["tests.test_photo_cute_inventory_boundary_history",
     "tests.test_subculture_illustration_photo_boundary",
     "tests.test_photo_current_boundary_snapshot"],
    ["tests.test_photo_seduction_source_boundary_history"],
    ["tests.test_photo_architecture_zero_delta_boundary",
     "tests.test_photo_motion_inventory_boundary_history"],
    ["tests.test_subculture_illustration_universal_scene_v3.UniversalSceneCurrentOracleV2Tests.test_current_oracle_exact_projection_lineage_and_mapping_totals",
     "tests.test_subculture_illustration_universal_scene_v3.UniversalSceneCurrentOracleV2Tests.test_descriptive_baseline_cannot_override_module_or_manifest_authority",
     "tests.test_subculture_illustration_universal_scene_v3.UniversalSceneRuntimeContractTests.test_v1_v2_exact_replay_and_photo_baseline_remain_immutable"],
]
counts = [unittest.defaultTestLoader.loadTestsFromNames(names).countTestCases() for names in groups]
plan = {"test_count": sum(counts), "groups": [
    {"index": i, "expected_tests": counts[i], "targets": names} for i, names in enumerate(groups)]}
(HERE / "VALIDATOR-REPAIR-REGRESSION-PLAN.json").write_text(json.dumps(plan, indent=2) + "\n")
running = []
for i, names in enumerate(groups):
    log = HERE / f"validator-repair-group-{i}.log"
    handle = log.open("w")
    proc = subprocess.Popen([sys.executable, "-u", "-m", "unittest", *names],
                            cwd=ROOT, stdout=handle, stderr=subprocess.STDOUT)
    running.append((i, proc, handle, log))
done = []
while running:
    for row in running[:]:
        i, proc, handle, log = row
        if proc.poll() is None:
            continue
        handle.close()
        content = log.read_text()
        count = re.search(r"Ran (\d+) tests? in", content)
        done.append({"index": i, "exit_code": proc.returncode, "log": log.name,
                     "expected_tests": counts[i], "actual_tests": int(count[1]) if count else 0})
        running.remove(row)
        print(f"validator repair group {i}: exit={proc.returncode}", flush=True)
    if running:
        time.sleep(1)
result = {"test_count": sum(counts), "targets": [name for group in groups for name in group],
          "groups": sorted(done, key=lambda item: item["index"]),
          "all_pass": all(row["exit_code"] == 0 and row["actual_tests"] == row["expected_tests"] for row in done)}
(HERE / "VALIDATOR-REPAIR-REGRESSION-RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result), flush=True)
sys.exit(0 if result["all_pass"] else 1)
