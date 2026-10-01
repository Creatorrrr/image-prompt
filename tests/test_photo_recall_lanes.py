from __future__ import annotations
import unittest
from tests import photo_prompt_fixtures
from recall_lanes import reserve_lane_leaders

class RecallLaneReservationTests(unittest.TestCase):
    def test_preserves_budget_and_lane_leaders(self):
        self.assertEqual(reserve_lane_leaders(['a','b','c','d','e'], [['b','a'],['d','c'],['e']], 3), ['b','d','e'])
    def test_never_broadens_eligibility(self):
        self.assertEqual(reserve_lane_leaders(['a','b'], [['outside','b']], 3), ['b','a'])
    def test_small_budget_and_duplicates_are_deterministic(self):
        self.assertEqual(reserve_lane_leaders(['a','b','c'], [['b'],['b'],['c']], 1), ['b'])
        self.assertEqual(reserve_lane_leaders(['a'], [['a']], 0), [])
