"""Run a named existing regression against base scripts/data without changing the checkout."""
import argparse
import hashlib
import importlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
BASE = "766c327d23d721bfc4bc459e4d596a4563fa7264"
SKILL_REL = Path("skills/photo-prompt-image-generator")


def base_bytes(path):
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--routing-case", action="append", default=[])
    parser.add_argument("--reported-routing-cases", action="store_true")
    parser.add_argument("--current", action="store_true")
    args = parser.parse_args()
    if args.reported_routing_cases:
        log = (HERE / "related-regression.log").read_text()
        args.routing_case = list(dict.fromkeys(re.findall(r"case='([^']+)'\) \.\.\. FAIL", log)))
        assert args.routing_case, "No reported routing failures"
    name = "test_registry_and_request_scoped_routing_fixture" if args.routing_case else "test_prepack_visual_intent_is_hash_bound_and_source_grounded"
    output_stem = ("baseline-routing-" + args.routing_case[0] if len(args.routing_case) == 1 else
                   "baseline-routing-reported-cases") if args.routing_case else "baseline-visual-intent-failure"
    if args.current:
        output_stem = output_stem.replace("baseline-", "current-", 1)
    fixture_rel = Path("tests/fixtures/photo_prompt/visual_obligation_routing_v1.jsonl")
    fixture = base_bytes(fixture_rel) if args.routing_case else None
    if fixture is not None:
        assert (ROOT / fixture_rel).read_bytes() == fixture, "Existing routing fixture changed"
        retained_rows = [line for line in fixture.decode().splitlines() if json.loads(line)["id"] in args.routing_case]
        assert len(retained_rows) == len(set(args.routing_case)), "Every routing case must name exactly one existing row"
    test_rel = Path("tests/test_photo_visual_obligations.py")
    assert (ROOT / test_rel).read_bytes() == base_bytes(test_rel), "Existing test changed"
    with tempfile.TemporaryDirectory(prefix="portrait-fashion-baseline-") as tmp:
        baseline_root = Path(tmp)
        baseline_skill = baseline_root / SKILL_REL
        scripts = baseline_skill / "scripts"
        assets = baseline_skill / "assets"
        scripts.mkdir(parents=True)
        assets.mkdir()
        # Every tracked script is copied from the recorded base revision.
        tracked_scripts = subprocess.check_output(
            ["git", "ls-tree", "-r", "--name-only", BASE, str(SKILL_REL / "scripts")], cwd=ROOT, text=True
        ).splitlines()
        for entry in tracked_scripts:
            source = Path(entry)
            destination = baseline_root / source
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(base_bytes(source))
        # Current unchanged assets are linked; changed top-level assets are restored
        # from base bytes, including manifests referencing preserved historical shards.
        changed = set(subprocess.check_output(
            ["git", "diff", BASE, "--name-only", "--", str(SKILL_REL / "assets")], cwd=ROOT, text=True
        ).splitlines())
        base_top_files = subprocess.check_output(
            ["git", "ls-tree", "--name-only", BASE, str(SKILL_REL / "assets") + "/"], cwd=ROOT, text=True
        ).splitlines()
        for entry in base_top_files:
            source = Path(entry)
            destination = baseline_root / source
            current = ROOT / source
            if entry in changed and current.is_file():
                destination.write_bytes(base_bytes(source))
            else:
                destination.symlink_to(current, target_is_directory=current.is_dir())
        (baseline_root / "docs").symlink_to(ROOT / "docs", target_is_directory=True)
        if args.current:
            baseline_root = ROOT
            baseline_skill = ROOT / SKILL_REL
            scripts = baseline_skill / "scripts"
            assets = baseline_skill / "assets"
        # Import the unmodified test with base modules ahead of project modules.
        sys.path[:0] = [str(scripts), str(ROOT)]
        module = importlib.import_module("tests.test_photo_visual_obligations")
        module.ROOT = baseline_root
        module.SKILL_DIR = baseline_skill
        module.SCRIPT_DIR = scripts
        module.WRAPPER_PATH = scripts / "generate_photo_prompt.py"
        module.REGISTRY_PATH = assets / "photo_prompt_visual_obligations.json"
        module.TAGS_PATH = assets / "photo_prompt_tags.json"
        if fixture is not None:
            case_file = Path(tmp) / "routing-case.jsonl"
            case_file.write_text("\n".join(retained_rows) + "\n")
            module.ROUTING_FIXTURE_PATH = case_file
        suite = unittest.TestSuite([module.PhotoVisualObligationTests(name)])
        with (HERE / (output_stem + ".log")).open("w") as stream:
            result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
        report = {
            "base_revision": BASE, "test": name, "tests_run": result.testsRun,
            "mode": "current_checkout" if args.current else "base_revision",
            "failed_tests": len(result.failures), "errors": len(result.errors),
            "unchanged_test_sha256": hashlib.sha256(base_bytes(test_rel)).hexdigest(),
            "scope": ("Current checkout; only the reported failed rows, using unchanged assertions." if args.current else
                      "Base-revision scripts and changed assets; unchanged assets linked. No current data or code was edited."),
            "failures": [trace for _, trace in result.failures],
            "error_traces": [trace for _, trace in result.errors],
        }
        if fixture is not None:
            report["routing_cases"] = args.routing_case
            report["unchanged_fixture_sha256"] = hashlib.sha256(fixture).hexdigest()
            report["fixture_scope"] = "Only the named original frozen rows, with their unchanged assertions."
        (HERE / (output_stem + ".json")).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
