"""Replay selected failures against actual pre-Y2K source and indexes."""
import json
import hashlib
import importlib
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE / "baseline-source"
sys.path.insert(0, str(BASE))
names_file = Path(sys.argv[1])
output_file = Path(sys.argv[2])
names = json.loads(names_file.read_text())
selection = None
if len(sys.argv) > 3:
    selected_ids = set(json.loads(Path(sys.argv[3]).read_text()))
    module = importlib.import_module("tests.test_photo_visual_obligations")
    original = module.ROUTING_FIXTURE_PATH
    selected_lines = [line for line in original.read_text().splitlines() if line.strip() and json.loads(line)["id"] in selected_ids]
    assert {json.loads(line)["id"] for line in selected_lines} == selected_ids
    selected_path = HERE / "baseline-visual-selected-fixtures" / original.name
    selected_path.parent.mkdir(exist_ok=True)
    selected_path.write_text("\n".join(selected_lines) + "\n")
    module.ROUTING_FIXTURE_PATH = selected_path
    selection = {"case_ids": sorted(selected_ids), "original_fixture": str(original), "original_sha256": hashlib.sha256(original.read_bytes()).hexdigest(), "selected_fixture": str(selected_path), "selected_sha256": hashlib.sha256(selected_path.read_bytes()).hexdigest(), "rows_and_expectations": "Verbatim existing rows; unchanged test assertions and runtime source. Only case selection is narrowed to observed failures."}
suite = unittest.TestLoader().loadTestsFromNames(names)
result = unittest.TextTestRunner(verbosity=2).run(suite)
summary = {
    "tests_run": result.testsRun,
    "failed_test_ids": [case.id() for case, _ in result.failures],
    "error_test_ids": [case.id() for case, _ in result.errors],
    "failure_evidence": [{"id": case.id(), "traceback": trace} for case, trace in result.failures],
    "error_evidence": [{"id": case.id(), "traceback": trace} for case, trace in result.errors],
    "source_root": str(BASE),
    "source": "clean HEAD generator/tags and saved original indexes; subprocess paths also isolated",
    "routing_case_selection": selection,
}
output_file.write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps({"tests_run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors)}))
raise SystemExit(not result.wasSuccessful())
