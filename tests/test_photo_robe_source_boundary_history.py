"""Route unchanged original assertions through an authenticated source tree."""
from pathlib import Path
import tempfile
import unittest
from tests import photo_ethereal_history_v35 as history

ROOT = Path(__file__).resolve().parents[1]


class OriginalBoundaryReplayTests(unittest.TestCase):
    def test_original_assertions_replay_without_revision(self):
        with tempfile.TemporaryDirectory(prefix="photo-original-tests-", dir=ROOT) as temporary:
            tree = Path(temporary).resolve() / "tree"
            history.materialize_original(tree, source_root=ROOT, link_verified=True)
            history.replay_original(tree, source_root=ROOT, test_module='tests.test_photo_robe_source_boundary_history')


if __name__ == "__main__":
    unittest.main()
