import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
WRAPPER_PATH = SKILL_DIR / "scripts" / "generate_photo_prompt.py"

NEW_LAYER_SLOTS = {
    "brow_style",
    "lip_finish",
    "eye_makeup_line",
}
FORCED_LAYER_IDS = {
    "brow_style": "soft_brushed_up_brow",
    "lip_finish": "blurred_edge_lip_tint",
    "eye_makeup_line": "graphic_floating_eyeliner",
}
EXPECTED_RENDER_TERMS = {
    "brow_style": "soft brushed-up natural brows",
    "lip_finish": "muted blurred-edge lip tint with a soft diffused outline",
    "eye_makeup_line": "graphic floating eyeliner with clean negative space",
}


def load_tags():
    return json.loads(TAGS_PATH.read_text())


class MakeupLayerDictionaryTests(unittest.TestCase):
    def setUp(self):
        self.tags = load_tags()

    def test_makeup_layer_slots_are_human_only_surface_controls(self):
        for slot in NEW_LAYER_SLOTS:
            with self.subTest(slot=slot):
                entries = self.tags["slots"][slot]
                self.assertGreaterEqual(len(entries), 5)
                self.assertIn(slot, self.tags["slot_pick_order"])
                self.assertEqual(
                    self.tags["slot_applicability"]["slots"][slot]["subject_categories"],
                    ["human"],
                )
                self.assertTrue(
                    {"product", "jewelry", "food", "wildlife"}.issubset(
                        self.tags["slot_applicability"]["slots"][slot]["deny_domains"]
                    )
                )
                self.assertTrue(all(entry.get("for_any") == ["human"] for entry in entries))

    def test_new_makeup_layer_render_terms_are_not_demographic_shortcuts(self):
        forbidden = (
            "for men",
            "for women",
            "male",
            "female",
            "masculine",
            "feminine",
            "genderless",
            "gender-neutral",
        )

        checked_entries = []
        for slot in NEW_LAYER_SLOTS:
            checked_entries.extend(self.tags["slots"][slot])
        checked_entries.extend(
            entry
            for entry in self.tags["slots"]["skin_finish"]
            if entry["id"] in {"cloud_blurred_skin_finish", "skincare_hybrid_second_skin_glow"}
        )

        for entry in checked_entries:
            with self.subTest(entry_id=entry["id"]):
                rendered = entry["en"].lower()
                self.assertFalse(any(term in rendered for term in forbidden))

    def test_inclusive_makeup_family_routes_layered_slots_and_preset(self):
        family = self.tags["semantic_policy"]["families"]["inclusive_makeup_beauty"]

        self.assertIn("gender_neutral_makeup_editorial_closeup", family["preset_policy"]["allow_ids"])
        self.assertTrue(NEW_LAYER_SLOTS.issubset(set(family["routed_slots"])))
        self.assertTrue(NEW_LAYER_SLOTS.issubset(set(family["steering_slots"])))
        self.assertIn("inclusive_makeup_beauty", self.tags["semantic_policy"]["steering_priority"])
        self.assertIn("inclusive_makeup_beauty", self.tags["coherence_rules"]["family_strength"])

    def test_makeup_family_slot_signals_reference_known_slot_entries(self):
        slots = self.tags["slots"]
        family = self.tags["semantic_policy"]["families"]["inclusive_makeup_beauty"]

        for slot, signal_groups in family["slot_signals"].items():
            slot_ids = {entry["id"] for entry in slots[slot]}
            for group_name in ("core", "support"):
                for entry_id in signal_groups.get(group_name, []):
                    with self.subTest(slot=slot, group=group_name, entry_id=entry_id):
                        self.assertIn(entry_id, slot_ids)

    def test_makeup_layer_preset_uses_new_layer_slots(self):
        preset = next(
            entry
            for entry in self.tags["presets"]
            if entry["id"] == "gender_neutral_makeup_editorial_closeup"
        )

        optional_slots = {entry["slot"] for entry in preset["optional_slots"]}
        self.assertIn("subject", optional_slots)
        self.assertTrue(NEW_LAYER_SLOTS.issubset(optional_slots))
        self.assertNotIn("adult_woman_lifestyle_subject", preset["filters"]["subject"]["ids"])
        for slot in NEW_LAYER_SLOTS:
            with self.subTest(slot=slot):
                self.assertGreaterEqual(len(preset["filters"][slot]["ids"]), 5)

    def test_forced_makeup_layers_render_exactly_once_in_every_detail_level(self):
        for detail_level in ("standard", "detailed", "compact"):
            argv = [
                sys.executable,
                str(WRAPPER_PATH),
                "--preset",
                "gender_neutral_makeup_editorial_closeup",
                "--selection-mode",
                "rule",
                "--seed",
                "42",
                "--lang",
                "en",
                "--detail-level",
                detail_level,
                "--json-output",
            ]
            for slot, entry_id in FORCED_LAYER_IDS.items():
                argv.extend(["--set", f"{slot}={entry_id}"])

            completed = subprocess.run(
                argv,
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            result = json.loads(completed.stdout)[0]
            prompt = result["prompt_en"].lower()

            self.assertEqual(result["quality"]["verdict"], "pass")
            for slot, phrase in EXPECTED_RENDER_TERMS.items():
                with self.subTest(detail_level=detail_level, slot=slot):
                    self.assertEqual(prompt.count(phrase.lower()), 1)


if __name__ == "__main__":
    unittest.main()
