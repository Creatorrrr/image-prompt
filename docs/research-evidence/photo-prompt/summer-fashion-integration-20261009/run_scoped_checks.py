"""Record scope-relevant contract and retrieval checks without changing fixtures."""
from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
MODULES = [
    "tests.test_photo_summer_fashion_semantics",
    "tests.test_photo_fashion_fit_semantics",
    "tests.test_photo_autumn_fashion_semantics",
    "tests.test_photo_swimwear_semantics",
    "tests.test_photo_clothing_terminology_semantics",
    "tests.test_photo_ornament_structure",
    "tests.test_photo_textile_opacity_effect_scope",
    "tests.test_photo_candidate_semantics",
    "tests.test_photo_visual_profile_retrieval",
    "tests.test_photo_visual_obligations",
    "tests.test_photo_semantic_index",
    "tests.test_photo_bm25f_retrieval",
    "tests.test_photo_visual_profile_shards",
    "tests.test_photo_runtime_freshness",
]


def main():
    suite = unittest.defaultTestLoader.loadTestsFromNames(MODULES)
    with (HERE / "scoped-tests.log").open("w") as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    summary = dict(modules=MODULES, tests_run=result.testsRun, failures=[str(t) for t, _ in result.failures],
                   errors=[str(t) for t, _ in result.errors], skipped=[str(t) for t, _ in result.skipped],
                   status="pass" if result.wasSuccessful() else "fail", scope="Data/retrieval/gate/freshness contracts; not native-image or requesting-user acceptance proof.")
    (HERE / "scoped-tests.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False))
    raise SystemExit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
