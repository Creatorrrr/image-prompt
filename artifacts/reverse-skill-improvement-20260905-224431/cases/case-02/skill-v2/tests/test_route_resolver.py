#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import sys
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from module_metadata import ROOT, load_manifest, module_map  # noqa: E402
from anchor_catalog import CORE_ANCHOR_IDS  # noqa: E402
from route_resolver import (  # noqa: E402
    MAX_NON_CORE_MODULES,
    resolve_analysis_route,
    resolve_modules,
)


class RouteResolverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest(ROOT)

    def test_route_binds_actual_profile_instruction_views(self) -> None:
        facets = {"subjects": ["human"], "medium": ["photographic"]}
        prompt = resolve_analysis_route(facets, self.manifest, "prompt")
        audited = resolve_analysis_route(facets, self.manifest, "audited")
        prompt_inputs = {item["path"]: item for item in prompt["shared_instruction_inputs"]}
        audited_inputs = {item["path"]: item for item in audited["shared_instruction_inputs"]}
        path = "references/integration-contract.md"
        self.assertEqual(prompt_inputs[path]["source_sha256"], audited_inputs[path]["source_sha256"])
        self.assertNotEqual(prompt_inputs[path]["view_sha256"], audited_inputs[path]["view_sha256"])
        self.assertLess(prompt_inputs[path]["view_words"], audited_inputs[path]["view_words"])
        self.assertNotEqual(prompt["route_fingerprint"], audited["route_fingerprint"])
        for lane in prompt["lanes"]:
            self.assertEqual(len(lane["module_inputs"]), len(lane["module_ids"]))
            self.assertNotIn("content", lane["instruction_input"])

    def test_stale_manifest_content_is_not_an_instruction_snapshot(self) -> None:
        from copy import deepcopy
        manifest = deepcopy(self.manifest)
        module_map(manifest)["core.visual-evidence"]["content_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "stale manifest content"):
            resolve_analysis_route({"subjects": ["generic-object"]}, manifest)

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
        self.assertNotIn("detail.human-body-form", modules)
        self.assertNotIn("detail.color-tone-fidelity", modules)

    def test_material_color_tone_risk_selects_generic_fidelity_detail(self) -> None:
        modules = resolve_modules(
            {
                "subjects": ["generic-object"],
                "medium": ["photographic"],
                "relationships": ["ordinary"],
                "detail_risks": ["color-tone"],
            },
            self.manifest,
        )
        self.assertIn("detail.color-tone-fidelity", modules)
        self.assertIn("medium.photographic-capture", modules)
        self.assertIn("subject.generic-object", modules)

    def test_material_lighting_risk_selects_light_form_detail(self) -> None:
        modules = resolve_modules(
            {
                "subjects": ["generic-object"],
                "medium": ["photographic"],
                "relationships": ["ordinary"],
                "detail_risks": ["lighting-fidelity", "shadow-topology"],
            },
            self.manifest,
        )
        self.assertIn("detail.light-form-fidelity", modules)
        self.assertIn("medium.photographic-capture", modules)
        self.assertNotIn("detail.color-tone-fidelity", modules)

    def test_first_order_human_body_form_selects_dedicated_detail(self) -> None:
        modules = resolve_modules(
            {
                "subjects": ["human"],
                "medium": ["photographic"],
                "relationships": ["ordinary"],
                "detail_risks": [
                    "body-form",
                    "body-proportion",
                    "muscle-definition",
                    "skin-surface",
                ],
            },
            self.manifest,
        )
        self.assertIn("detail.human-body-form", modules)
        self.assertIn("subject.human", modules)
        self.assertIn("medium.photographic-capture", modules)

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
                "major_region_hierarchy",
                "dominant_fidelity_axis",
                "aesthetic_invariants",
                "flexible_dimensions",
                "appeal_render_separation",
                "invariant_salience_ledger",
                "aesthetic_salience_gate",
                "aesthetic_signature_early",
                "aesthetic_causal_signature",
                "direct_perceptual_appeal",
                "aggregate_prior_cluster_audit",
                "broad_color_descriptor_discipline",
                "color_metaphor_decomposition",
                "detail_not_sharpness",
                "attractiveness_polish_separation",
                "background_legibility_ceiling",
                "color_causality",
                "global_cast_consistency",
                "neutral_reference_anchor",
                "causal_origin_attribution",
                "semantic_salience_amplification",
                "semantic_claim_merge",
                "net_salience_audit",
                "replacement_correction",
                "cross_slot_perceptual_effect_audit",
                "color_tone_causal_consistency",
                "unowned_appearance_claim_audit",
                "causal_color_phrase_scope",
                "final_color_control_ledger",
                "light_form_causal_consistency",
                "unowned_lighting_claim_audit",
                "global_local_contrast_separation",
                "shadow_owner_coverage",
                "final_light_control_ledger",
                "module_evidence_not_prose",
                "clause_ownership",
                "diagnostic_render_separation",
                "color_tone_output_ownership",
                "light_form_output_ownership",
            }.issubset(CORE_ANCHOR_IDS)
        )

    def test_human_body_form_exposes_causal_form_anchors(self) -> None:
        body = module_map(self.manifest)["detail.human-body-form"]
        self.assertTrue(
            {
                "human_body_form_signature",
                "muscle_lighting_separation",
                "skin_surface_signature",
                "body_region_hierarchy",
                "persistent_induced_form_split",
                "skin_color_contract_handoff",
            }.issubset(body["provides_anchors"])
        )

    def test_color_tone_detail_exposes_generic_causal_anchors(self) -> None:
        color = module_map(self.manifest)["detail.color-tone-fidelity"]
        self.assertTrue(
            {
                "color_tone_contract",
                "color_causal_layers",
                "relative_color_calibration",
                "neutral_anchor_confidence",
                "aggregate_color_effect_budget",
                "tone_zone_response",
                "color_measurement_limits",
                "display_color_scope",
                "region_group_color_comparison",
            }.issubset(color["provides_anchors"])
        )

    def test_light_form_detail_exposes_generic_causal_anchors(self) -> None:
        light = module_map(self.manifest)["detail.light-form-fidelity"]
        self.assertTrue(
            {
                "light_form_contract",
                "observed_light_result",
                "source_geometry_fill_separation",
                "global_local_light_contrast",
                "shadow_ownership",
                "material_light_response",
                "pose_light_dependency",
                "lighting_color_contract_handoff",
                "light_control_ledger",
                "render_light_verification",
                "lighting_language_translation",
                "lighting_friendly_label_review",
                "lighting_label_external_source",
            }.issubset(light["provides_anchors"])
        )

    def test_photo_and_clothing_expose_contrast_and_material_anchors(self) -> None:
        modules = module_map(self.manifest)
        self.assertTrue(
            {
                "contrast_topology",
                "photographic_causal_decomposition",
                "color_light_decomposition",
                "light_to_form_strength",
                "white_balance_exposure_separation",
                "photographic_tone_response",
            }.issubset(modules["medium.photographic-capture"]["provides_anchors"])
        )
        self.assertTrue(
            {
                "material_role",
                "category_prior_disambiguation",
                "detail_role_ceiling",
            }.issubset(modules["detail.clothing-fashion"]["provides_anchors"])
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

    def test_manifest_advertises_adaptive_analysis_profiles(self) -> None:
        orchestration = self.manifest["analysis_orchestration"]
        self.assertEqual(orchestration["route_schema"], "reverse-image-analysis-route/v2")
        self.assertEqual(orchestration["default_profile"], "prompt")
        self.assertEqual(orchestration["supported_profiles"], ["prompt", "audited"])
        self.assertEqual(
            orchestration["prompt_report_schema"],
            "reverse-image-analysis-lane-report/compact-v2",
        )
        self.assertEqual(
            orchestration["prompt_set_schema"],
            "reverse-image-analysis-compact-set/v2",
        )
        self.assertEqual(
            orchestration["audited_bundle_schema"],
            "reverse-image-analysis-bundle/v2",
        )

    def test_analysis_route_activates_compact_portrait_lanes(self) -> None:
        route = resolve_analysis_route(
            {
                "subjects": ["human"],
                "medium": ["photographic"],
                "relationships": ["ordinary"],
                "detail_risks": ["face-detail", "color-tone", "lighting-fidelity"],
            },
            self.manifest,
        )
        self.assertEqual(route["schema_version"], "reverse-image-analysis-route/v2")
        self.assertEqual(route["analysis_profile"], "prompt")
        self.assertEqual(route["execution_budget"]["lane_waves"], 1)
        self.assertEqual(route["execution_budget"]["critic_passes"], 1)
        self.assertEqual(route["execution_budget"]["targeted_repairs"], 1)
        self.assertEqual(route["execution_budget"]["max_full_reroutes"], 1)
        self.assertFalse(route["execution_budget"]["full_precision_ledgers"])
        self.assertTrue(
            all(lane["analysis_depth"] == "compact" for lane in route["lanes"])
        )
        self.assertTrue(
            all(
                lane["report_schema"]
                == "reverse-image-analysis-lane-report/compact-v2"
                for lane in route["lanes"]
            )
        )
        self.assertEqual(
            set(route["required_lane_ids"]),
            {
                "lane.global-composition",
                "lane.spatial-topology",
                "lane.subject-appearance",
                "lane.color-light-material",
                "lane.medium-aesthetic-capture",
            },
        )
        self.assertNotIn("lane.information-layout", route["required_lane_ids"])

    def test_audited_analysis_profile_preserves_full_contract(self) -> None:
        route = resolve_analysis_route(
            {
                "subjects": ["human"],
                "medium": ["photographic"],
                "relationships": ["ordinary"],
                "detail_risks": ["face-detail", "color-tone", "lighting-fidelity"],
            },
            self.manifest,
            analysis_profile="audited",
        )
        self.assertEqual(route["analysis_profile"], "audited")
        self.assertTrue(route["execution_budget"]["full_precision_ledgers"])
        self.assertTrue(
            all(lane["analysis_depth"] == "audited" for lane in route["lanes"])
        )
        self.assertTrue(
            all(
                lane["report_schema"] == "reverse-image-analysis-lane-report/v2"
                for lane in route["lanes"]
            )
        )

    def test_unknown_analysis_profile_fails(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown analysis profile"):
            resolve_analysis_route({}, self.manifest, analysis_profile="exhaustive")

    def test_information_route_adds_information_lane_without_color_lane(self) -> None:
        route = resolve_analysis_route(
            {
                "subjects": ["document"],
                "medium": ["screenshot-ui"],
                "relationships": ["screen-frame-within-frame"],
                "detail_risks": ["text-logo"],
            },
            self.manifest,
        )
        self.assertIn("lane.information-layout", route["required_lane_ids"])
        self.assertIn("lane.spatial-topology", route["required_lane_ids"])
        self.assertNotIn("lane.color-light-material", route["required_lane_ids"])

    def test_analysis_route_fingerprint_is_alias_and_order_stable(self) -> None:
        left = resolve_analysis_route(
            {
                "subjects": ["human"],
                "medium": ["photographic"],
                "detail-risks": ["face-detail", "color-tone"],
            },
            self.manifest,
        )
        right = resolve_analysis_route(
            {
                "detail-risk": ["color-tone", "face-detail"],
                "subject": ["human"],
                "media": ["photographic"],
            },
            self.manifest,
        )
        self.assertEqual(left, right)

    def test_analysis_profile_changes_route_fingerprint(self) -> None:
        facets = {
            "subjects": ["human"],
            "medium": ["photographic"],
            "detail-risks": ["face-detail"],
        }
        prompt = resolve_analysis_route(facets, self.manifest)
        audited = resolve_analysis_route(
            facets, self.manifest, analysis_profile="audited"
        )
        self.assertNotEqual(prompt["route_fingerprint"], audited["route_fingerprint"])


if __name__ == "__main__":
    unittest.main()
