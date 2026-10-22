"""Freeze scoped source evidence, three actual attempts and two returned images."""
from pathlib import Path
import hashlib, json, shutil, datetime

O = Path(__file__).resolve().parent
ROOT = O.parents[2]
D = ROOT / 'docs/research-evidence/photo-prompt/lovecraftian-horror-20261022'
E = D / 'integration-evidence'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_bytes())
write = lambda p, v: p.write_text(json.dumps(v, ensure_ascii=False, indent=2)+'\n')
def copy(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    assert sha(src) == sha(dst)

arms = {
    'archive': ('lovecraftian-archive-20261022-c7e194-r2', 'execution-summary.json'),
    'science': ('lovecraftian-science-20261022-c84a7b-final', 'run-summary.json'),
    'encounter': ('lovecraftian-encounter-20261022-c8e24b', 'test-report.json'),
}
G = read(O/'successor.json')['generation_id']
ref = Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg')
assert sha(ref) == read(D/'IMAGE-TEST-CASES.json')['reference']['sha256']
cases = []
for arm, (name, summary_name) in arms.items():
    run = ROOT/'generated/photo-runs'/name
    summary = read(run/summary_name)
    state = read(run/'workflow.json')
    expected_operation = 'provider_blocked' if arm == 'archive' else 'complete'
    assert len(state['operations']) == 1 and state['operations'][0]['status'] == expected_operation
    ledger = [json.loads(line) for line in (run/'image_runs.ndjson').read_text().splitlines() if line.strip()]
    assert len(ledger) == 1
    composed = read(run/('composed-authored.json' if arm=='archive' else 'authored/composed.json' if arm=='encounter' else 'composed.json'))
    assert composed['chosen_candidate_ids'] == [] and composed['chosen_visual_concept_ids'] == []
    for n in [summary_name, 'final-prompt.txt', 'run_manifest.json', 'image_runs.ndjson',
              'native-result.json', 'native-output-provenance.json', 'pixel-observations.json',
              'pixel-assessment-independent.json', 'review-execution-wrapper.json',
              'verified-review-wrapper.py', 'composition-comparison.md']:
        if (run/n).is_file(): copy(run/n, E/arm/n)
    for p in run.glob('native-tool-error*.json'): copy(p, E/arm/p.name)
    # Bound final render request and any review audit, retained exactly.
    for role in ['freeze_receipt','render_request','runtime_audit','composed_audit','review_audit','native_plan']:
        if role in state['artifacts']:
            item = state['artifacts'][role]; p = Path(item['path'])
            if not p.is_absolute(): p = run/p
            assert sha(p) == item['sha256']
            copy(p, E/arm/(role+'.json'))
    image_path = summary.get('image_path')
    image_sha = None
    if image_path:
        image_path = Path(image_path)
        image_sha = sha(image_path)
        assert image_sha == summary['image_sha256']
        copy(image_path, D/'test-images'/(arm+'.png'))
    result = {'arm':arm, 'summary':str(run/summary_name), 'prompt':str(run/'final-prompt.txt'),
              'prompt_sha256':sha(run/'final-prompt.txt'), 'image':str(image_path) if image_path else None,
              'image_sha256':image_sha, 'image_calls':len(ledger), 'source_adopted_new':0,
              'source_adopted_updated':0, 'source_adopted_legacy':0,
              'new_data_to_image':'NOT_DEMONSTRATED',
              'pixel_verdict':'BLOCKED_UNSCORED' if arm=='archive' else 'PARTIAL_NOT_FULL_PASS',
              'workflow_phase':state['phase'], 'ledger_run_id':ledger[0]['run_id']}
    cases.append(result)

fresh = read(O/'new-native-records.json')
A = ROOT/'skills/photo-prompt-image-generator/assets'
assert read(A/'photo_candidate_lovecraftian_horror_20261022.json')['candidates'] == fresh
changed = read(O/'changed-native-records.json')
cosmic = read(A/'photo_candidate_cosmic_horror_20261021.json')['candidates']
assert all(cosmic[cid] == record for cid, record in changed.items())
for name in ['photo_candidate_lovecraftian_horror_20261022.json',
             'photo_candidate_lovecraftian_horror_bindings_20261022.json',
             'photo_lovecraftian_horror_semantics_20261022.json']:
    copy(A/name, E/'source'/name)
for name in ['before.json','data-integration.json','source-preservation.json','focused-data-checks.json',
             'final-scoped-source-check.json','canonical-source-validation.json','native-index-build.json',
             'native-staged.json','successor.json','install.log','runtime-check.json',
             'retrieval-qualification.json','qualification-query-evidence.json',
             'semantic-boundaries-tests.log','literal-text-tests.log',
             'historical-research-integrity.json','changed-native-records.json','resume-execution.json',
             'encounter-review-coordination-disclosure.json','coordinator-pixels-science.json',
             'coordinator-pixels-encounter.json','adopt_data.py','build_release.py','resume_release.py',
             'qualify_release.py','finalize_evidence.py']:
    copy(O/name, E/'maintenance'/name)

result = {'schema':'lovecraftian-integration-image-test-results/v1',
          'completed_at':datetime.datetime.now().isoformat(), 'generation_id':G,
          'source_counts':{'semantic_cards':84,'new_visual':57,'new_context_diagnostic':27,
                           'updated_existing':6,'new_bindings':158,'keyword_routes':185},
          'reference_sha256':sha(ref), 'actual_image_calls':sum(x['image_calls'] for x in cases),
          'returned_images':sum(x['image'] is not None for x in cases), 'blocked_unscored':1,
          'new_or_updated_source_adoptions':0, 'pixel_whole_case_passes':0,
          'source_registration':'PASS','sealed_release_and_install':'PASS',
          'managed_record_integrity':'PASS','augmentation_contribution':'NOT_DEMONSTRATED',
          'default_activation':'HOLD','CURRENT_writes_by_task':0,'commits_by_task':0,'pushes_by_task':0,
          'user_acceptance':'pending','cases':cases,
          'limits':['3 independent concept arms, not a causal before/after image comparison',
                    'initial setup/authoring/review timing deviations disclosed in INTEGRATION-RESULTS.md',
                    'provider_blocked rerender contract prevented proposed safe-alternative retry',
                    'working global dictionary index remains outside this isolated release qualification']}
assert result['actual_image_calls'] == 3 and result['returned_images'] == 2
write(D/'IMAGE-TEST-RESULTS.json', result)
status = read(O/'evidence-status.json')
status.update(image_tests={'attempts':3,'images':2,'blocked_unscored':1,'partial_not_full_pass':2,
                          'new_or_updated_source_adoptions':0,'augmentation':'NOT_DEMONSTRATED'})
write(O/'evidence-status.json',status)
copy(O/'evidence-status.json',E/'maintenance/evidence-status.json')
files = sorted([p for p in E.rglob('*') if p.is_file()]+[p for p in (D/'test-images').glob('*.png')]+
               [D/n for n in ['INTEGRATION-RESULTS.md','FOLLOWUP-INDEX.md','IMAGE-TEST-CASES.json','IMAGE-TEST-RESULTS.json']])
(D/'INTEGRATION-SHA256SUMS').write_text(''.join(sha(p)+'  '+str(p.relative_to(D))+'\n' for p in files))
print(json.dumps({'status':'pass','evidence_files':len(files),'image_calls':3,'images':2,
                  'case_results':[x['pixel_verdict'] for x in cases]}))
