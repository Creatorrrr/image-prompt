"""Route unchanged original assertions through an authenticated source tree."""
from pathlib import Path
import tempfile
import unittest
from tests import photo_data_scope_history_v34 as history

ROOT = Path(__file__).resolve().parents[1]


class OriginalBoundaryReplayTests(unittest.TestCase):
    def test_original_assertions_replay_without_revision(self):
        with tempfile.TemporaryDirectory(prefix="photo-original-tests-", dir=ROOT) as temporary:
            tree = Path(temporary).resolve() / "tree"
            history.materialize('local-v33', tree, source_root=ROOT, link_verified=True)
            history.replay('local-v33', tree, source_root=ROOT, test_module='tests.test_photo_data_scope_boundary_history', log_name='LOCAL-V33-ORIGINAL-TESTS.log')


if __name__ == "__main__":
    unittest.main()
