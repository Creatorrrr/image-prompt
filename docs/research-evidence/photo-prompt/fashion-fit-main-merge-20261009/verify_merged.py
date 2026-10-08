"""Run the focused fit and relevant existing regression suites; save exact failures."""
from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(ROOT))
modules = json.loads((ROOT / "docs/research-evidence/photo-prompt/fashion-fit-integration-20261008/related-tests-final.json").read_text())["modules"]
suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(name[:-3]) for name in modules)
with (HERE / "focused-tests.log").open("w") as log:
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
receipt = {
    "modules": modules,
    "tests_run": result.testsRun,
    "failures": [{"test": str(test), "traceback": trace} for test, trace in result.failures],
    "errors": [{"test": str(test), "traceback": trace} for test, trace in result.errors],
    "skipped": [{"test": str(test), "reason": reason} for test, reason in result.skipped],
    "result": "PASS" if result.wasSuccessful() else "FAIL",
}
(HERE / "focused-tests.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(receipt, ensure_ascii=False))
raise SystemExit(0 if result.wasSuccessful() else 1)
