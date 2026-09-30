from __future__ import annotations

import unittest

from tests import photo_prompt_fixtures as fixtures
import photo_creative_controls as controls


class PhotoControlAssignmentPunctuationTests(unittest.TestCase):
    def split(self, text, overrides):
        envelope = fixtures.envelope(text)
        snapshot = controls.resolve(
            text, context={"subject_category": "human"}, overrides=overrides, seed=19,
        )
        return controls.split_request_spans(envelope, snapshot)

    def test_sentence_period_is_not_part_of_a_control_value(self):
        text = "Two adult friends. sensual=1, fetish=0, creativity=3, surreal=0. 프롬프트만 작성해줘."
        visual, assignments = self.split(text, {
            "sensual": 1, "fetish": 0, "creativity": 3, "surreal": 0,
        })
        self.assertEqual([(row["name"], row["value"]) for row in assignments], [
            ("sensual", 1), ("fetish", 0), ("creativity", 3), ("surreal", 0),
        ])
        self.assertEqual(assignments[-1]["text"], "surreal=0")
        self.assertIn("프롬프트만 작성해줘.", visual[-1]["text"])
        for row in [*visual, *assignments]:
            self.assertEqual(text[row["start"]:row["end"]], row["text"])

    def test_enum_and_quoted_image_text_keep_their_own_boundaries(self):
        text = 'Show the sign "surreal=0.". adult_appeal_emphasis=auto.'
        visual, assignments = self.split(text, {"adult_appeal_emphasis": "auto"})
        self.assertEqual([row["name"] for row in assignments], ["adult_appeal_emphasis"])
        self.assertIn('"surreal=0."', visual[0]["text"])

    def test_invalid_numeric_values_are_not_truncated_to_valid_integers(self):
        for value in ("0.5.", "0.0", ".5", "0..5", "0oops", "1e0."):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.split(f"A portrait; surreal={value}", {"surreal": 0})


if __name__ == "__main__":
    unittest.main()
