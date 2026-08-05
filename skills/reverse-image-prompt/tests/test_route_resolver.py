#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import sys
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from module_metadata import ROOT, load_manifest, module_map  # noqa: E402
from anchor_catalog import CORE_ANCHOR_IDS  # noqa: E402
from route_resolver import MAX_NON_CORE_MODULES, resolve_modules  # noqa: E402


class RouteResolverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest(ROOT)

    def test_capture_quality_can_select_photo_medium(self) -> None:
        modules = resolve_modules(
            {
                "subjects": ["human"],
                "relationships": ["ordinary"],
                "capture_quality": ["flash", "casual-phone"],
            },
            self.manifest,
        )
        self.assertIn("medium.photographic-capture", modules)
        self.assertNotIn("medium.unspecified-visual", modules)
        self.assertNotIn("detail.human-face-likeness", modules)

    def test_readable_face_selects_likeness_detail(self) -> None:
        modules = resolve_modules(
            {
                "subjects": ["human"],
                "medium": ["photographic"],
                "relationships": ["ordinary"],
                "detail_risks": ["face-detail"],
            },
            self.manifest,
        )
        self.assertIn("detail.human-face-likeness", modules)

    def test_human_without_readable_face_keeps_likeness_module_out(self) -> None:
        modules = resolve_modules(
            {
                "subjects": ["human"],
                "medium": ["photographic"],
                "relationships": ["ordinary"],
            },
            self.manifest,
        )
        self.assertIn("subject.human", modules)
        self.assertNotIn("detail.human-face-likeness", modules)

    def test_mixed_media_allows_photo_and_render_layers(self) -> None:
        modules = resolve_modules(
            {
                "subjects": ["human"],
                "medium": ["photographic", "non-photographic"],
                "relationships": ["mixed-media"],
            },
            self.manifest,
        )
        self.assertIn("medium.photographic-capture", modules)
        self.assertIn("medium.non-photographic-rendering", modules)
        self.assertIn("concept.mixed-media-illusion", modules)

    def test_core_handled_values_do_not_fail(self) -> None:
        modules = resolve_modules(
            {
                "subjects": ["generic-object"],
                "medium": ["unspecified"],
                "relationships": ["ordinary"],
                "detail_risks": ["small props", "cropped edges"],
            },
            self.manifest,
        )
        self.assertIn("subject.generic-object", modules)

    def test_major_spatial_relationship_anchors_are_core(self) -> None:
        self.assertTrue(
            {
                "major_component_relation_graph",
                "major_component_topology",
                "interaction_geometry_sentence",
                "image_scene_space_distinction",
            }.issubset(CORE_ANCHOR_IDS)
        )

    def test_adaptive_aesthetic_anchors_are_core(self) -> None:
        self.assertTrue(
            {
                "subject_environment_balance",
                "aesthetic_salience_gate",
                "aesthetic_signature_early",
                "detail_not_sharpness",
                "attractiveness_polish_separation",
                "background_legibility_ceiling",
            }.issubset(CORE_ANCHOR_IDS)
        )

    def test_human_subject_exposes_broad_person_gestalt_anchor(self) -> None:
        human = module_map(self.manifest)["subject.human"]
        self.assertIn("broad_person_gestalt_anchor", human["provides_anchors"])

    def test_unknown_value_fails_instead_of_being_ignored(self) -> None:
        with self.assertRaisesRegex(ValueError, "unmapped detail-risk value"):
            resolve_modules(
                {
                    "subjects": ["generic-object"],
                    "medium": ["photographic"],
                    "detail_risks": ["glossy-mystery"],
                },
                self.manifest,
            )

    def test_module_budget_is_enforced(self) -> None:
        with self.assertRaisesRegex(ValueError, "module budget exceeded"):
            resolve_modules(
                {
                    "subjects": [
                        "human",
                        "animal",
                        "product",
                        "food",
                        "architecture",
                        "landscape",
                        "vehicle",
                        "document",
                    ],
                    "medium": ["photographic"],
                    "relationships": ["ordinary"],
                },
                self.manifest,
            )

    def test_declared_budget_matches_contract(self) -> None:
        self.assertEqual(MAX_NON_CORE_MODULES, 8)


if __name__ == "__main__":
    unittest.main()
