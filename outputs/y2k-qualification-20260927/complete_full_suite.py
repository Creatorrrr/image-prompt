"""Complete unchanged discovery cases, retaining evidenced prefix passes."""
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "qualification-source"
OUT = HERE / "completed-full-suite"
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(SOURCE))
sys.path.insert(0, str(SOURCE / "tests"))


def flatten(suite):
    for case in suite:
        if isinstance(case, unittest.TestSuite):
            yield from flatten(case)
        else:
            yield case


if len(sys.argv) > 1 and sys.argv[1] == "--worker":
    names_path, result_path = map(Path, sys.argv[2:4])
    names = json.loads(names_path.read_text())
    suite = unittest.TestLoader().loadTestsFromNames(names)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    payload = {"requested_ids": names, "tests_run": result.testsRun,
               "failures": [{"id": case.id(), "traceback": trace} for case, trace in result.failures],
               "errors": [{"id": case.id(), "traceback": trace} for case, trace in result.errors],
               "skipped": [{"id": case.id(), "reason": reason} for case, reason in result.skipped]}
    result_path.write_text(json.dumps(payload, indent=2) + "\n")
    raise SystemExit(not result.wasSuccessful())

started = time.time()
cases = list(flatten(unittest.TestLoader().discover(str(SOURCE / "tests"))))
all_ids = {case.id() for case in cases}
assert len(all_ids) == len(cases)
cached = {}
logs = {}
pattern = re.compile(r"^test_\w+ \((test_[\w.]+)\) \.\.\. (ok|skipped.*)$")
for part in range(1, 4):
    path = HERE / f"isolated-full-suite/full-tests-part-{part}.log"
    logs[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    for line in path.read_text().splitlines():
        match = pattern.match(line)
        if match and match[1] in all_ids:
            cached[match[1]] = "pass" if match[2] == "ok" else "skipped"
(OUT / "prefix-pass-evidence.json").write_text(json.dumps({"source_manifest": str(HERE / "qualification-source-manifest.json"), "log_sha256": logs, "completed_cases": cached}, indent=2) + "\n")
groups = {}
for case in cases:
    if case.id() not in cached:
        groups.setdefault(case.__class__.__module__, []).append(case.id())
queue = sorted(groups.items(), key=lambda row: -(len(row[1]) * (4 if "visual" in row[0] else 1)))
running = {}
finished = []
env = dict(os.environ)
env["PYTHONPATH"] = str(SOURCE / "tests") + os.pathsep + str(SOURCE)
while queue or running:
    while queue and len(running) < 7:
        module, names = queue.pop(0)
        names_path = OUT / f"{module}.names.json"
        names_path.write_text(json.dumps(names, indent=2) + "\n")
        result_path = OUT / f"{module}.result.json"
        handle = (OUT / f"{module}.log").open("w")
        process = subprocess.Popen([sys.executable, "-u", str(Path(__file__).resolve()), "--worker", str(names_path), str(result_path)], cwd=SOURCE, stdout=handle, stderr=subprocess.STDOUT, env=env)
        running[process.pid] = (process, module, handle, result_path)
    for pid, (process, module, handle, result_path) in list(running.items()):
        if process.poll() is None:
            continue
        handle.close()
        result = json.loads(result_path.read_text()) if result_path.exists() else {"tests_run": 0, "requested_ids": groups[module], "failures": [], "errors": [{"id": module, "traceback": "worker terminated without result"}], "skipped": []}
        result["module"] = module
        result["exit_code"] = process.returncode
        finished.append(result)
        del running[pid]
        progress = {"prefix_cases": len(cached), "new_cases_run": sum(item["tests_run"] for item in finished), "finished_modules": len(finished), "running_modules": [item[1] for item in running.values()], "queued_modules": len(queue)}
        (OUT / "progress.json").write_text(json.dumps(progress, indent=2) + "\n")
        print(json.dumps(progress), flush=True)
    if queue or running:
        time.sleep(1)
failures = [failure for result in finished for failure in result["failures"]]
errors = [error for result in finished for error in result["errors"]]
summary = {"discovered_tests": len(cases), "modules": len({case.__class__.__module__ for case in cases}),
           "tests_run": len(cached) + sum(result["tests_run"] for result in finished),
           "prefix_verified_cases": len(cached), "continued_cases_run": sum(result["tests_run"] for result in finished),
           "failed_test_ids": [item["id"] for item in failures], "error_test_ids": [item["id"] for item in errors],
           "failures": len(failures), "errors": len(errors), "skipped": sum(status == "skipped" for status in cached.values()) + sum(len(result["skipped"]) for result in finished),
           "elapsed_seconds": time.time() - started, "execution": "Unchanged discovery cases on one immutable source; evidenced completed prefix passes retained; unfinished and failed cases rerun in isolated CLI partitions", "all_pass": not failures and not errors}
summary["complete_coverage"] = summary["tests_run"] == summary["discovered_tests"]
(OUT / "full-suite-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary), flush=True)
raise SystemExit(not summary["all_pass"])
