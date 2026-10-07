"""Run immutable aa5 assertions on their exact historical fixture closure."""
from pathlib import Path
import unittest
from tests.photo_workflow_boundary_v37 import historical_test_suite


def load_tests(loader, tests, pattern):
    return historical_test_suite("tests.test_photo_camera_authoring_guidance_contract", source_root=Path(__file__).resolve().parents[1], loader=loader)


if __name__ == "__main__":
    unittest.main()
