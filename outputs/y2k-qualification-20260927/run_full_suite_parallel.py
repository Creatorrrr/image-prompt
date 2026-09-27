"""Run every discovered test module once in isolated CLI processes.

The three groups are execution partitions, not changed expectations. This
avoids duplicate long-running discovery and focused suites competing for CPU.
"""
import json
import os
import re
import subprocess
import sys
import time
import unittest
from pathlib import Path

ROOT = Path(os.environ.get("Y2K_SOURCE_ROOT", str(Path(__file__).resolve().parents[2]))).resolve()
HERE = Path(os.environ.get("Y2K_SUITE_OUTPUT_DIR", str(Path(__file__).resolve().parent))).resolve()
HERE.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT))


def cases(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from cases(item)
        else:
            yield item


modules = {}
for case in cases(unittest.TestLoader().discover(str(ROOT / "tests"))):
    module = case.__class__.__module__
    modules[module] = modules.get(module, 0) + 1
groups = [[], [], []]
weights = [0, 0, 0]
for module, count in sorted(modules.items(), key=lambda row: -row[1]):
    weight = count * (4 if "visual_profile_retrieval" in module or "visual_obligations" in module else 1)
    index = min(range(3), key=lambda i: weights[i])
    groups[index].append(module)
    weights[index] += weight
plan = {"discovered_tests": sum(modules.values()), "discovered_modules": len(modules), "groups": groups, "all_modules_unique": len({m for g in groups for m in g}) == len(modules)}
(HERE / "full-suite-partitions.json").write_text(json.dumps(plan, indent=2) + "\n")
processes = []
handles = []
started = time.time()
for i, group in enumerate(groups):
    handle = (HERE / f"full-tests-part-{i + 1}.log").open("w")
    handles.append(handle)
    # Discovery returns top-level test names, so add the tests directory to
    # import lookup without changing the workspace or authored data.
    env = dict(__import__("os").environ)
    env["PYTHONPATH"] = str(ROOT / "tests") + __import__("os").pathsep + str(ROOT)
    processes.append(subprocess.Popen([sys.executable, "-m", "unittest", *group, "-v"], cwd=ROOT, stdout=handle, stderr=subprocess.STDOUT, env=env))
for process in processes:
    process.wait()
for handle in handles:
    handle.close()
summary = {"discovered_tests": plan["discovered_tests"], "modules": len(modules), "elapsed_seconds": time.time() - started, "parts": []}
for i, process in enumerate(processes):
    output = (HERE / f"full-tests-part-{i + 1}.log").read_text()
    match = re.search(r"Ran (\d+) tests? in ([\d.]+)s", output)
    summary["parts"].append({"group": i + 1, "exit_code": process.returncode, "tests_run": int(match[1]) if match else None,
                             "result": "pass" if process.returncode == 0 else "failed_or_incomplete",
                             "log": str((HERE / f"full-tests-part-{i + 1}.log").resolve())})
summary["tests_run"] = sum(part["tests_run"] or 0 for part in summary["parts"])
summary["complete_coverage"] = summary["tests_run"] == summary["discovered_tests"]
summary["all_pass"] = all(part["exit_code"] == 0 for part in summary["parts"])
(HERE / "full-suite-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary))
raise SystemExit(not summary["all_pass"])
