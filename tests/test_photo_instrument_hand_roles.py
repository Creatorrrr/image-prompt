"""Guard authored playing roles before optional candidate wording reaches a prompt."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
import prompt_generator as pg


class InstrumentHandRoleDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = pg.load_json(SKILL / "assets/photo_prompt_tags.json")

    def entry(self, slot, entry_id):
        return next(row for row in self.data["slots"][slot] if row["id"] == entry_id)

    def test_shared_wind_pose_preserves_support_as_a_hand_role(self):
        row = self.entry("body_pose", "wind_embouchure_two_hand_key_pose")
        for field in ("en", "embedding_text"):
            self.assertIn("support", row[field])
            self.assertIn("each hand", row[field])
            self.assertNotIn("both hands operat", row[field])
        self.assertIn("지지", row["ko"])

    def test_trumpet_public_action_preserves_handedness(self):
        row = self.entry("action", "trumpet_lip_valve_action")
        candidate, _ = pg.candidate_pack_summarize_slot_candidate(
            self.data, "action", {"id": row["id"], "applicability_status": "eligible"}
        )
        self.assertEqual(candidate["label_en"], row["en"])
        self.assertEqual(candidate["label_ko"], row["ko"])
        self.assertIn("left-hand support", candidate["label_en"])
        self.assertIn("right-hand valve", candidate["label_en"])
        self.assertIn("왼손", candidate["label_ko"])
        self.assertIn("오른손", candidate["label_ko"])
        self.assertIn("note-appropriate combination", row["embedding_text"])
        self.assertNotIn("pressing three piston valves", candidate["label_en"])


if __name__ == "__main__":
    unittest.main()
