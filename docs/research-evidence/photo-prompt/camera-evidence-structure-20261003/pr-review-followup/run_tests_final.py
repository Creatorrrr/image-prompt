"""Complete unittest discovery, with a fresh offline process per module."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest


def flatten(suite):
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            yield from flatten(test)
        else:
            yield test


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--module")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(args.repo))
    for name in ("OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY", "ANTHROPIC_API_KEY"):
        os.environ.pop(name, None)
    if args.module:
        executed = []
        runtime_sources = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (args.repo / "skills/photo-prompt-image-generator/scripts").glob("*.py")}
        data_sources = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in (args.repo / "skills/photo-prompt-image-generator/assets").glob("*.json")}

        class RecordedResult(unittest.TextTestResult):
            def startTest(self, test):
                executed.append(test.id())
                super().startTest(test)

        suite = unittest.defaultTestLoader.loadTestsFromName(args.module)
        result = unittest.TextTestRunner(verbosity=2, resultclass=RecordedResult).run(suite)
        payload = {"module": args.module, "tests_run": result.testsRun, "executed_ids": executed,
            "runtime_sources": runtime_sources, "data_sources": data_sources,
            "failures": [{"id": t.id(), "traceback": trace} for t, trace in result.failures],
            "errors": [{"id": t.id(), "traceback": trace} for t, trace in result.errors],
            "skipped": [{"id": t.id(), "reason": reason} for t, reason in result.skipped],
            "expected_failures": [t.id() for t, _ in result.expectedFailures],
            "unexpected_successes": [t.id() for t in result.unexpectedSuccesses]}
        (args.output / f"{args.module}.json").write_text(json.dumps(payload, indent=2) + "\n")
        return 0 if result.wasSuccessful() else 1
    loader = unittest.TestLoader()
    suite = loader.discover(str(args.repo / "tests"), top_level_dir=str(args.repo))
    if loader.errors:
        raise RuntimeError("\n".join(loader.errors))
    ids = [t.id() for t in flatten(suite)]
    assert len(set(ids)) == len(ids), "duplicate discovery IDs"
    # Scheduling only: every discovered ID still runs in a fresh offline process.
    prior_seconds = {'tests.test_makeup_layer_dictionary': 0.369, 'tests.test_photo_acetate_distortion_alternative': 0.772, 'tests.test_photo_acting_expression_data': 39.857, 'tests.test_photo_action_context_effects_cleanup': 0.856, 'tests.test_photo_adult_appeal_scope': 71.505, 'tests.test_photo_adult_appeal_visual_semantics': 171.751, 'tests.test_photo_affect_visual_semantics': 80.044, 'tests.test_photo_aurora_anchor_alternative': 0.627, 'tests.test_photo_authorial_core': 355.704, 'tests.test_photo_authorial_core_v6': 106.124, 'tests.test_photo_authorial_direction_scope': 0.178, 'tests.test_photo_authorship_policy': 53.846, 'tests.test_photo_bm25f_retrieval': 0.163, 'tests.test_photo_body_aesthetic_semantics': 104.81, 'tests.test_photo_body_morphology_semantics': 92.332, 'tests.test_photo_body_shape_semantics': 269.471, 'tests.test_photo_bound_context_surfaces': 5.677, 'tests.test_photo_boundary_transition_visual_semantics': 2.809, 'tests.test_photo_camera_clause_polarity': 37.435, 'tests.test_photo_camera_evidence_structure': 38.646, 'tests.test_photo_camera_owned_clauses': 18.882, 'tests.test_photo_candidate_semantics': 35.931, 'tests.test_photo_capture_boundary_data': 0.554, 'tests.test_photo_capture_elements_visual_semantics': 1.851, 'tests.test_photo_capture_owner_data_cleanup': 0.745, 'tests.test_photo_capture_physics_alternatives': 0.493, 'tests.test_photo_character_render_review': 141.16, 'tests.test_photo_character_response_concepts': 21.177, 'tests.test_photo_clothing_terminology_semantics': 22.779, 'tests.test_photo_color_relations': 21.604, 'tests.test_photo_composer_view': 0.546, 'tests.test_photo_concept_candidate_expansion': 26.409, 'tests.test_photo_contextual_appeal': 0.539, 'tests.test_photo_control_assignment_punctuation': 0.3, 'tests.test_photo_control_span_ownership': 90.698, 'tests.test_photo_convoy_route_alternative': 0.892, 'tests.test_photo_core_retrieval': 12.336, 'tests.test_photo_costume_cosplay_semantics': 40.178, 'tests.test_photo_cumulonimbus_anvil_alternative': 0.872, 'tests.test_photo_current_boundary': 1.386, 'tests.test_photo_current_boundary_snapshot': 0.285, 'tests.test_photo_data_cleanup_public_surfaces': 1.431, 'tests.test_photo_data_semantic_corrections': 1.849, 'tests.test_photo_death_afterlife_semantics': 105.021, 'tests.test_photo_desire_visual_semantics': 2.963, 'tests.test_photo_dress_positive_paraphrase': 0.441, 'tests.test_photo_editing_effects_semantics': 87.641, 'tests.test_photo_embodiment': 74.147, 'tests.test_photo_emotional_place_visual_semantics': 28.934, 'tests.test_photo_environment_alternative_consistency': 0.661, 'tests.test_photo_era_visual_semantics': 18.126, 'tests.test_photo_everyday_scene_semantics': 12.775, 'tests.test_photo_face_shape_semantics': 251.012, 'tests.test_photo_fantasy_visual_semantics': 324.956, 'tests.test_photo_ghost_ship_gate_alternative': 0.648, 'tests.test_photo_glacier_surface_alternative': 0.68, 'tests.test_photo_hair_visual_semantics': 122.2, 'tests.test_photo_harem_visual_semantics': 26.146, 'tests.test_photo_historical_womenswear_semantics': 11.755, 'tests.test_photo_humanlike_semantics': 231.914, 'tests.test_photo_image_attempt_evidence': 2.208, 'tests.test_photo_imaginal_visual_semantics': 13.765, 'tests.test_photo_initial_creative_controls': 257.385, 'tests.test_photo_instrument_hand_roles': 1.397, 'tests.test_photo_instrument_semantics': 183.206, 'tests.test_photo_jurisdiction_record_unit_data_cleanup': 1.487, 'tests.test_photo_kebaya_material_alternative': 0.886, 'tests.test_photo_korean_emotional_visual_semantics': 41.583, 'tests.test_photo_krummholz_korean_alias_data_cleanup': 11.714, 'tests.test_photo_latest_metadata_boundary_history': 1.088, 'tests.test_photo_lattice_shadow_alternative': 0.811, 'tests.test_photo_leading_line_gate_alternatives': 0.749, 'tests.test_photo_legend_visual_semantics': 5.503, 'tests.test_photo_lighting_color_owner_data_cleanup': 1.475, 'tests.test_photo_lighting_composition_boundary_data': 1.028, 'tests.test_photo_lighting_visual_semantics': 37.063, 'tests.test_photo_liminal_active_use_korean_data_cleanup': 9.872, 'tests.test_photo_liminal_maintained_alternative': 0.428, 'tests.test_photo_loading': 0.167, 'tests.test_photo_luxury_semantics': 55.002, 'tests.test_photo_makeup_reference_balance': 52.36, 'tests.test_photo_makeup_visual_semantics': 166.5, 'tests.test_photo_material_data_cleanup': 1.121, 'tests.test_photo_model_editorial_semantics': 8.037, 'tests.test_photo_motion_artifact_owner_data_cleanup': 0.724, 'tests.test_photo_mythology_visual_semantics': 190.196, 'tests.test_photo_nape_effect_scope': 2.603, 'tests.test_photo_nape_metadata_boundary_history': 0.56, 'tests.test_photo_narrative_unit_data_cleanup': 1.199, 'tests.test_photo_natural_environment_semantics': 219.994, 'tests.test_photo_neutral_expression_alternatives': 125.625, 'tests.test_photo_next_slot_data_cleanup': 0.754, 'tests.test_photo_nonhuman_source_alternatives': 0.437, 'tests.test_photo_object_morphology_ownership': 0.479, 'tests.test_photo_occupation_korean_label_data_cleanup': 0.747, 'tests.test_photo_oneiric_anchor_alternative': 0.428, 'tests.test_photo_opening_era_semantics': 6.664, 'tests.test_photo_overhead_hand_alternative': 0.421, 'tests.test_photo_palace_fortification_semantics': 2.94, 'tests.test_photo_palace_korean_relation_alignment': 89.054, 'tests.test_photo_panning_direction_scope': 0.428, 'tests.test_photo_photorealism_elements_semantics': 7.196, 'tests.test_photo_photorealism_owner_data_cleanup': 0.741, 'tests.test_photo_portcullis_korean_state': 20.502, 'tests.test_photo_portrait_composition_semantics': 7.737, 'tests.test_photo_portrait_fashion_exposure': 14.617, 'tests.test_photo_pose_visual_semantics': 92.75, 'tests.test_photo_pose_vocabulary_semantics': 68.244, 'tests.test_photo_positive_retrieval': 0.171, 'tests.test_photo_poverty_visual_semantics': 40.437, 'tests.test_photo_precore_feature_selection': 0.494, 'tests.test_photo_prepack_isolation': 39.877, 'tests.test_photo_prop_conditional_contact': 0.726, 'tests.test_photo_protostar_korean_alias_data_cleanup': 1.934, 'tests.test_photo_punk_aesthetic_semantics': 1.122, 'tests.test_photo_rare_photo_visual_semantics': 77.589, 'tests.test_photo_reactorprompt_visual_relations': 72.933, 'tests.test_photo_realistic_background_semantics': 18.184, 'tests.test_photo_receiver_material_response': 0.463, 'tests.test_photo_reef_explicit_unit_data_cleanup': 6.462, 'tests.test_photo_religion_iconography_alternatives': 68.432, 'tests.test_photo_religion_iconography_boundary_history': 0.275, 'tests.test_photo_remaining_boundary_data': 0.9, 'tests.test_photo_render_repair': 21.693, 'tests.test_photo_research_integration': 0.376, 'tests.test_photo_residual_positive_guards': 0.695, 'tests.test_photo_retrieval_runtime_improvement': 58.927, 'tests.test_photo_role_garment_candidate_expansion': 0.459, 'tests.test_photo_run_manifest': 0.695, 'tests.test_photo_scene_data_cleanup': 5.7, 'tests.test_photo_semantic_guidance_data': 0.47, 'tests.test_photo_semantic_index': 2.763, 'tests.test_photo_shelf_return_korean_state_data_cleanup': 2.767, 'tests.test_photo_single_allocator_recovery': 0.427, 'tests.test_photo_slang_boundary_history': 0.2, 'tests.test_photo_slang_visual_alternatives': 82.75, 'tests.test_photo_slide_thickness_alternative': 0.661, 'tests.test_photo_slot_data_cleanup': 1.141, 'tests.test_photo_slot_query_fusion': 0.248, 'tests.test_photo_space_visual_semantics': 153.774, 'tests.test_photo_subculture_appearance_alternatives': 3.743, 'tests.test_photo_subculture_appearance_boundary_history': 0.28, 'tests.test_photo_suggestive_editorial_visual_semantics': 85.098, 'tests.test_photo_swimwear_semantics': 17.408, 'tests.test_photo_tactile_reality_semantics': 6.633, 'tests.test_photo_textile_opacity_effect_scope': 2.576, 'tests.test_photo_texture_data_cleanup': 1.729, 'tests.test_photo_traditional_clothing_semantics': 5.737, 'tests.test_photo_violence_crime_visual_semantics': 326.708, 'tests.test_photo_visual_obligations': 443.761, 'tests.test_photo_visual_profile_retrieval': 145.254, 'tests.test_photo_weapon_visual_semantics': 143.756, 'tests.test_photo_wet_hair_weight_alternative': 0.418, 'tests.test_photo_womens_activewear_visual_semantics': 108.945, 'tests.test_photo_womens_casualwear_visual_semantics': 76.999, 'tests.test_photo_womens_professional_uniform_visual_semantics': 1.189, 'tests.test_photo_womens_summer_trend_visual_semantics': 61.56, 'tests.test_photo_wrap_skirt_side_alternative': 0.706, 'tests.test_photo_wuxia_visual_semantics': 193.028, 'tests.test_photo_y2k_visual_semantics': 37.431, 'tests.test_subculture_illustration_contract_v1': 21.911, 'tests.test_subculture_illustration_moe_elements': 12.146, 'tests.test_subculture_illustration_photo_boundary': 0.778, 'tests.test_subculture_illustration_universal_scene_v3': 411.335, 'tests.test_universal_scene_directional_substitution': 2.863}
    modules = sorted({t.rsplit(".", 2)[0] for t in ids}, key=lambda m: (-prior_seconds.get(m, 0), m))
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=args.repo, text=True).strip()
    discovery = {"commit": commit, "discovered_ids": ids, "modules": modules,
        "method": "complete unittest discovery, isolated offline module processes", "workers": args.workers}
    (args.output / "discovery.json").write_text(json.dumps(discovery, indent=2) + "\n")
    environment = os.environ.copy()
    for name in ("OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY", "ANTHROPIC_API_KEY"):
        environment.pop(name, None)

    def run(module):
        started = time.monotonic()
        log = args.output / f"{module}.log"
        with log.open("w") as stream:
            proc = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--repo", str(args.repo),
                "--output", str(args.output), "--module", module], cwd=args.repo, env=environment,
                stdout=stream, stderr=subprocess.STDOUT)
        return {"module": module, "returncode": proc.returncode,
            "seconds": round(time.monotonic() - started, 3), "log_sha256": hashlib.sha256(log.read_bytes()).hexdigest()}

    started = time.monotonic()
    results = []
    print(f"Discovered {len(ids)} tests in {len(modules)} modules at {commit}.", flush=True)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run, module) for module in modules]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(f"Completed {len(results)}/{len(modules)}: {result['module']} rc={result['returncode']}", flush=True)
            (args.output / "progress.json").write_text(json.dumps(results, indent=2) + "\n")
    records = [json.loads((args.output / f"{r['module']}.json").read_text())
               for r in results if (args.output / f"{r['module']}.json").exists()]
    executed = [i for r in records for i in r["executed_ids"]]
    summary = {"commit": commit, "method": discovery["method"], "workers": args.workers,
        "discovered_tests": len(ids), "executed_tests": sum(r["tests_run"] for r in records),
        "module_count": len(modules), "missing_execution_ids": sorted(set(ids) - set(executed)),
        "unexpected_execution_ids": sorted(set(executed) - set(ids)),
        "duplicate_execution_ids": sorted({i for i in executed if executed.count(i) > 1}),
        "failures": [f for r in records for f in r["failures"]],
        "errors": [f for r in records for f in r["errors"]],
        "skipped": [f for r in records for f in r["skipped"]],
        "module_results": sorted(results, key=lambda r: r["module"]),
        "wall_seconds": round(time.monotonic() - started, 3)}
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: v for k, v in summary.items() if k != "module_results"}), flush=True)
    return 0 if all(r["returncode"] == 0 for r in results) and not summary["missing_execution_ids"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
