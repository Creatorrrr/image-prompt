"""Reconcile completed full discovery, clean-main replay and unchanged source."""
import hashlib
import json
from pathlib import Path
import subprocess

PUB=Path(__file__).resolve().parent
ROOT=PUB.parents[3]


def load(path): return json.loads(path.read_text())


def selector(identity):
    if identity.startswith('setUpClass ('):return identity[len('setUpClass ('):-1]
    if identity.startswith('unittest.loader._FailedTest.'):
        name=identity.removeprefix('unittest.loader._FailedTest.')
        return name if name.startswith('tests.') else 'tests.'+name
    return identity.split(' (',1)[0]


full=load(PUB/'full-tests/FULL-RESULT.json')
assert full['discovery_complete'] and full['every_discovered_id_assigned_exactly_once']
workers=[load(path) for path in sorted((PUB/'full-tests').glob('worker-*-result.json'))]
assert len(workers)==full['workers']
started=[identity for worker in workers for identity in worker['started_ids']]
assigned=[identity for worker in workers for identity in worker['selected_ids']]
assert len(started)==len(set(started))==full['tests_run']
missing=sorted(set(assigned)-set(started))
blocked_classes=[row['id'][len('setUpClass ('):-1] for row in full['errors'] if row['id'].startswith('setUpClass (')]
assert all(any(identity.startswith(owner+'.') for owner in blocked_classes) for identity in missing),missing
baseline={}; baseline_groups=[]
for path in sorted(PUB.glob('BASELINE-RESULT-*.json')):
    report=load(path)
    assert report['source_commit']=='a7c8f7fb0c09a989957b2d2e658df9b2d7aaf101'
    outcomes={selector(row['id']):row for row in report['failures']+report['errors']}
    assert set(report['selections'])<=outcomes.keys()
    baseline.update(outcomes)
    baseline_groups.append({'report':path.name,'selections':len(report['selections']),'tests_run':report['tests_run']})
current={selector(row['id']):row for row in full['failures']+full['errors']}
new_failed=sorted(current.keys()-baseline.keys())
assert not new_failed,new_failed
comparisons=[{'selector':identity,'reproduced_on_clean_main':True,
    'publication_traceback':current[identity]['traceback'],
    'baseline_traceback':baseline[identity]['traceback']} for identity in sorted(current)]
source=load(PUB/'TESTED-SOURCE-SEAL.json')
assert all(hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['sha256'] for row in source['files'])
assert not subprocess.check_output(['git','diff','--name-only','--','skills','tests'],cwd=ROOT).strip()
result={'schema_version':'wardrobe-publication-final-validation/v1',
    'status':'VALIDATED_WITH_REPRODUCED_BASELINE_SUITE_FAILURES',
    'tested_source_commit':full['source_commit'],'tested_production_bytes_unchanged':True,
    'dictionary':load(PUB/'INITIAL-VALIDATION.json')['results']['dictionary'],
    'visual_index':load(PUB/'INITIAL-VALIDATION.json')['results']['visual-index'],
    'runtime_publication':load(PUB/'INITIAL-VALIDATION.json')['results']['runtime'],
    'focused_tests':load(PUB/'INITIAL-VALIDATION.json')['results']['focused-tests'],
    'full_discovery':{'status':full['status'],'discovered_tests':full['discovered_tests'],
        'tests_run':full['tests_run'],'failure_assertions':len(full['failures']),'errors':len(full['errors']),
        'skipped':full['skipped'],'expected_failures':full['expected_failures'],
        'unexpected_successes':full['unexpected_successes'],'seconds':full['seconds'],
        'fixture_setup_blocked_tests':missing,'fixture_setup_blocked_count':len(missing),
        'every_discovered_id_assigned_exactly_once':True},
    'baseline_comparison':{'clean_main_commit':'a7c8f7fb0c09a989957b2d2e658df9b2d7aaf101',
        'distinct_failed_selectors':len(current),'all_failed_selectors_reproduced':True,
        'new_failing_selectors':new_failed,'groups':baseline_groups,
        'boundary':'Matching failed test IDs is evidence of existing failures. Historical setup/import failures still block their assertions; this is not a fully passing suite or a proof against every masked regression.'},
    'authored_preservation':load(PUB/'MAIN-INTEGRATION-AUDIT.json'),
    'indexes':load(PUB/'scoped-index-build.json'),
    'image_qualification':{'historical_latest_all_required_pass':1,'cases':3,'user_acceptance':'pending',
        'boundary':'Git publication and passing source contracts do not promote partial native pixel evidence.'},
    'publication_embedding_calls':0,'publication_image_calls':0}
(PUB/'BASELINE-FAILURE-COMPARISON.json').write_text(json.dumps({'comparisons':comparisons},ensure_ascii=False,indent=2)+'\n')
(PUB/'FINAL-VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
text=(PUB/'PUBLICATION.md').read_text()
text=text.replace('Full unittest discovery is required on the final source after pulling origin/main; its separate report records the actual result.',
    f"Full unittest discovery completed after the pull: {full['discovered_tests']} discovered, {full['tests_run']} run, {len(missing)} blocked by failing class setup. It reports {len(full['failures'])} failure assertions and {len(full['errors'])} errors. All {len(current)} distinct failing selectors reproduced on clean origin/main; there are no newly failing selectors among the executed comparisons. This remains a failing broad suite, with its unexecuted historical assertions explicitly listed in FINAL-VALIDATION.json.")
(PUB/'PUBLICATION.md').write_text(text)
print(json.dumps({'status':result['status'],'discovered':full['discovered_tests'],'run':full['tests_run'],'blocked':len(missing),'distinct_baseline_failures':len(current),'new_failing_selectors':new_failed}),flush=True)
