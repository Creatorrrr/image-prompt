"""Validate changed fixture dispatch and source guards in isolated processes."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import json
import os
import re
import subprocess
import sys
import time

E = Path(__file__).resolve().parent
W = E.parents[3]
OUT = E / "affected-regression"
OUT.mkdir(exist_ok=True)
paths = set((W / "tests").glob("test_photo_*boundary_history.py"))
paths.update((W / "tests").glob("test_photo_v*_historical_fixture.py"))
extra = [
    "test_photo_architecture_zero_delta_boundary.py",
    "test_photo_current_boundary.py", "test_photo_current_boundary_snapshot.py",
    "test_subculture_illustration_photo_boundary.py",
    "test_subculture_illustration_contract_v1.py",
    "test_subculture_illustration_universal_scene_v3.py",
    "test_photo_photorealism_elements_semantics.py",
    "test_photo_realistic_background_semantics.py",
    "test_photo_palette_applications.py",
    "test_photo_character_appearance_100.py",
    "test_photo_krummholz_korean_alias_data_cleanup.py",
    "test_photo_liminal_active_use_korean_data_cleanup.py",
    "test_photo_protostar_korean_alias_data_cleanup.py",
    "test_photo_shelf_return_korean_state_data_cleanup.py",
]
paths.update(W / "tests" / name for name in extra)
paths.discard(W / "tests/test_photo_data_scope_v34_boundary_history.py")
modules = sorted(".".join(p.relative_to(W).with_suffix("").parts) for p in paths)
modules.sort(key=lambda m: (m == "tests.test_photo_character_appearance_100", m))
prior = json.loads((W / "docs/research-evidence/photo-prompt/color-palette-main-merge-20261007/FULL-REGRESSION-RESULT.json").read_text())
known = {r["module"]: r for r in prior["failed_modules"]}
env = os.environ.copy()
env.update(GEMINI_API_KEY="", GOOGLE_API_KEY="", OPENAI_API_KEY="")


def run(module):
    started = time.monotonic()
    log = OUT / (module + ".log")
    local_env = dict(env, PHOTO_RUNTIME_STORE=str(Path.home() / ".cache/image-prompt/data-links-merge-tests" / module))
    with log.open("w") as stream:
        try:
            result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", module.split(".")[-1] + ".py", "-v"], cwd=W, env=local_env, stdout=stream, stderr=stream, timeout=1800)
            code = result.returncode
        except subprocess.TimeoutExpired:
            code = 124
    content = log.read_text()
    counts = re.findall(r"Ran (\d+) tests?", content)
    failures = re.findall(r"FAILED \(([^)]+)\)", content)
    row = {"module": module, "returncode": code, "tests": int(counts[-1]) if counts else 0,
           "failure_summary": failures[-1] if failures else None,
           "duration_seconds": round(time.monotonic() - started, 3), "log": str(log.relative_to(W))}
    headers = lambda text: [h.replace("(tests.", "(") for h in re.findall(r"^(?:FAIL|ERROR): (.+)$", text, re.MULTILINE)]
    row["failure_cases"] = headers(content)
    old_cases = headers((W / known[module]["log"]).read_text()) if module in known else []
    # A new current-guard test accompanies the authenticated historical cello
    # comparison; it adds one test while preserving all existing failure cases.
    expected_tests = known[module]["tests"] + int(module == "tests.test_photo_character_appearance_100") if module in known else None
    row["same_known_upstream_failure"] = bool(code and module in known and
        row["failure_summary"] == known[module]["failure_summary"] and row["tests"] == expected_tests and
        row["failure_cases"] == old_cases)
    (OUT / (module + ".json")).write_text(json.dumps(row, indent=2) + "\n")
    return row


started = time.monotonic()
rows = []
with ThreadPoolExecutor(max_workers=3) as pool:
    for future in as_completed([pool.submit(run, module) for module in modules]):
        rows.append(future.result())
        print(json.dumps(rows[-1]), flush=True)
        (E / "AFFECTED-REGRESSION-PROGRESS.json").write_text(json.dumps({"completed": len(rows), "total": len(modules), "latest": rows[-1]}, indent=2) + "\n")
unexpected = [r for r in rows if r["returncode"] and not r["same_known_upstream_failure"]]
report = {"schema": "photo-data-links-merge-affected-regression/v1", "modules": sorted(rows, key=lambda r: r["module"]),
          "module_count": len(modules), "tests": sum(r["tests"] for r in rows),
          "failed_modules": [r for r in rows if r["returncode"]], "unexpected_failures": unexpected,
          "status": ("FAIL" if unexpected else "PASS_WITH_KNOWN_UPSTREAM_FAILURES" if any(r["returncode"] for r in rows) else "PASS"),
          "duration_seconds": round(time.monotonic() - started, 3), "process_isolation": True,
          "workers": 3, "scope": "All historical boundary dispatch, current boundary, affected source guards, palette, and five known upstream failures"}
(E / "AFFECTED-REGRESSION-RESULT.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({k: v for k, v in report.items() if k != "modules"}), flush=True)
sys.exit(1 if unexpected else 0)
