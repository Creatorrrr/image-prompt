#!/usr/bin/env python3
"""Run final affected tests with exact IDs and machine-readable evidence."""
from pathlib import Path
import json,sys,unittest,time
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT))
name=sys.argv[1]
groups={
 'authored': ['tests.test_photo_religion_iconography_alternatives','tests.test_photo_religion_iconography_boundary_history','tests.test_photo_candidate_semantics.PhotoCandidateSemanticsTests.test_maintenance_prose_is_external_and_hash_bound'],
 'boundary': ['tests.test_subculture_illustration_universal_scene_v3.UniversalSceneDataContractTests.test_existing_render_manifests_keep_historical_failure_labels','tests.test_subculture_illustration_universal_scene_v3.UniversalSceneRuntimeContractTests.test_v1_v2_exact_replay_and_photo_baseline_remain_immutable','tests.test_subculture_illustration_universal_scene_v3.UniversalSceneCurrentOracleV2Tests.test_descriptive_baseline_cannot_override_module_or_manifest_authority','tests.test_subculture_illustration_contract_v1.SubcultureIllustrationContractV1Tests.test_aggregate_validator_does_not_hide_partial_pixel_qualification','tests.test_subculture_illustration_photo_boundary'],
 'retrieval': ['tests.test_photo_liminal_active_use_korean_data_cleanup','tests.test_photo_core_retrieval','tests.test_photo_mythology_visual_semantics','tests.test_photo_visual_profile_retrieval'],
}
suite=unittest.defaultTestLoader.loadTestsFromNames(groups[name])
def flatten(value):
 for item in value:
  if isinstance(item,unittest.TestSuite):yield from flatten(item)
  else:yield item
ids=[t.id() for t in flatten(suite)]
assert not any('._FailedTest.' in t for t in ids),ids
started=time.monotonic();result=unittest.TextTestRunner(verbosity=2).run(suite)
report={'group':name,'requested_names':groups[name],'test_ids':ids,'tests_run':result.testsRun,'elapsed_seconds':round(time.monotonic()-started,3),'failures':[t.id() for t,_ in result.failures],'errors':[t.id() for t,_ in result.errors],'skipped':[t.id() for t,_ in result.skipped],'successful':result.wasSuccessful()}
(HERE/f'final-verification-{name}.json').write_text(json.dumps(report,indent=2)+'\n')
sys.exit(0 if result.wasSuccessful() else 1)
