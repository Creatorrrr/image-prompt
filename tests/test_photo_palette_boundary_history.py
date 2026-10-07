"""Replay unchanged predecessor assertions through exact committed V34 bytes."""
from pathlib import Path
import tempfile
import unittest
from tests import photo_ethereal_history_v35 as history
ROOT=Path(__file__).resolve().parents[1]

class OriginalBoundaryReplayTests(unittest.TestCase):
    def test_original_assertions_replay_without_revision(self):
        with tempfile.TemporaryDirectory(prefix='photo-original-v34-tests-') as temporary:
            tree=Path(temporary).resolve()/'tree'
            history.materialize_original(tree,source_root=ROOT,link_verified=True)
            result=history.replay_original(tree,source_root=ROOT,test_module='tests.test_photo_palette_boundary_history')
            self.assertEqual(0,result.returncode)

if __name__=='__main__':unittest.main()
