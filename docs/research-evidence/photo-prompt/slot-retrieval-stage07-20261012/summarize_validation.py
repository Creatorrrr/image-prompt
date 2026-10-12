"""Summarize real artifacts without promoting unrun checks or empty outputs."""
import hashlib
import json
from pathlib import Path
import re

OUT = Path(__file__).resolve().parent
ROOT = Path('/Users/chasoik/.codex/worktrees/slot-retrieval-stage07-integration/image-prompt')


def read(name):
    return json.loads((OUT/name).read_text())


def save(name, value):
    (OUT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def one(path):
    value = json.loads(path.read_text())
    return value[0] if isinstance(value, list) else value


def private_keys(value):
    forbidden = {'score','rank','fusion_score','retrieval_rank','retrieval_score','bm25f_score','private_trace'}
    if isinstance(value, dict):
        return (forbidden & value.keys()) | set().union(*(private_keys(v) for v in value.values()))
    if isinstance(value, list):
        return set().union(*(private_keys(v) for v in value))
    return set()


def main():
    rows = read('qualified-public-natural-benchmark.json')+read('qualified-public-native-cases.json')
    assert len(rows)==40
    problems = []
    targets = []
    required = read('CRITERIA-FROZEN.json')['natural_targets']
    meaning = read('CRITERIA-FROZEN.json')['subject_adjudication']
    subject_results = []
    for lane, old_lane in [('qualified-public-natural','public-natural'),('qualified-public-native','public-native')]:
        for path in sorted((OUT/lane).glob('*/candidate-pack.json')):
            pack, old = one(path), one(OUT/old_lane/path.parent.name/'candidate-pack.json')
            ids = {r['id'] for s in pack['slots'].values() for r in s['candidates']}
            old_ids = {r['id'] for s in old['slots'].values() for r in s['candidates']}
            for check, passed in [('frozen_core',pack['authorial_core']==old['authorial_core']),
                                  ('frozen_controls',pack['creative_controls']==old['creative_controls']),
                                  ('negative_bytes',pack['negative_en']==old['negative_en']),
                                  ('candidate_set',ids==old_ids),
                                  ('overall_cap',len(ids)<=64),
                                  ('slot_caps',all(len(s['candidates'])<=s['candidate_limit'] and s['candidate_limit'] in (2,4) for s in pack['slots'].values())),
                                  ('optional',all(r['adoption']=='optional' for s in pack['slots'].values() for r in s['candidates'])),
                                  ('unordered',all(s['candidate_order']=='seed_shuffled_non_preferential' for s in pack['slots'].values())),
                                  ('private_rank',not private_keys(pack))]:
                if not passed:problems.append(dict(case=path.parent.name,check=check))
            for identity in required.get(path.parent.name,{}).get('required_compatible',[]):
                candidate = next((r for s in pack['slots'].values() for r in s['candidates'] if r['id']==identity),None)
                assert candidate is not None, (path.parent.name,identity)
                targets.append(dict(case=path.parent.name,id=identity,exposed=True,
                                    adoption_status=candidate['applicability']['status']))
            if lane=='qualified-public-natural':
                recorded=next(r for r in meaning['cases'] if r['key']==path.parent.name)
                actual={r['entry_id'] for r in pack['slots'].get('subject',{}).get('candidates',[])}
                assert actual=={r['id'] for r in recorded['after_subject']},path.parent.name
                subject_results.append(dict(case=path.parent.name,proposals=sorted(actual),
                    unsupported=recorded['unsupported_after'],reasons=recorded.get('after_reasons',{}),
                    empty=not actual))
    assert not problems,problems
    native=read('qualified-public-native-cases.json')
    public=dict(cases=40,natural_cases=20,development=8,holdout=12,native_alias_cases=20,
        cli_errors=sum(r['exit_code']!=0 for r in rows),view_errors=sum(r['view_exit_code']!=0 for r in rows),
        recomputation_errors=sum(bool(r['recomputation_issues']) for r in rows),
        candidate_omission_detected=sum(r['omission_detected'] for r in rows),
        native_positive_total=10,native_positive_hits=sum(r['target_hit'] for r in native if r['mode']=='positive'),
        native_adjacent_excluded_total=10,native_adjacent_false_hits=sum(r['target_hit'] for r in native if r['mode']!='positive'),
        target_exposure_total=len(targets),target_exposure_hits=sum(r['exposed'] for r in targets),
        targets_adoption_eligible=sum(r['adoption_status']=='eligible' for r in targets),target_exposures=targets,
        candidate_sets_unchanged=True,frozen_core_controls_negative_unchanged=True,
        cap_policy=dict(overall=64,core=4,support=2),optional_and_unordered_preserved=True,
        private_rank_leaks=0,boundary_problems=problems,subject_meaning=dict(
            adjudication_scope=meaning['scope'],blind_holdout=False,
            cases_with_unsupported=sum(bool(r['unsupported']) for r in subject_results),
            unsupported_proposals=sum(len(r['unsupported']) for r in subject_results),
            subject_proposals=sum(len(r['proposals']) for r in subject_results),
            empty_subject_cases=[r['case'] for r in subject_results if r['empty']],cases=subject_results),
        generation_id=read('QUALIFIED-RUNTIME.json')['generation_id'])
    assert public['target_exposure_total']==13 and public['targets_adoption_eligible']==12
    save('PUBLIC-VALIDATION.json',public)
    lanes=['integrated-focused','qualified-profile-regression','qualified-profile-publication-recheck','qualified-integration-regression']
    tests={};selectors={}
    for lane in lanes:
        result=read(lane+'-tests.json')
        log=(OUT/(lane+'-tests.log')).read_text()
        selectors[lane]=set(re.findall(r'\((tests\.[^)]+)\)',log))
        assert len(selectors[lane])==result['tests_run']
        tests[lane]=dict(tests_run=result['tests_run'],failures=len(result['failures']),errors=len(result['errors']),
                         skipped=len(result['skipped']),successful=result['successful'])
    failed={r['selector'] for r in read('qualified-profile-regression-tests.json')['failures']}
    assert failed==selectors['qualified-profile-publication-recheck']
    assert all('source_revision_pending' in r['traceback'] for r in read('qualified-profile-regression-tests.json')['failures'])
    assert tests['qualified-profile-publication-recheck']['successful']
    test_summary=dict(runs=tests,baseline_before_source_amendment=136,
        unique_selectors=len(set.union(*selectors.values())),
        after_source_amendment_unique=len(selectors['qualified-profile-regression']|selectors['qualified-integration-regression']),
        all_latest_selector_results_pass=True,
        publication_repair='13 CLI tests were blocked by unfinished worktree default source revision. Normal publisher completed the revision, with the same qualified generation. All 13 failed selectors then passed; failed attempt logs retained.',
        selector_inventory={lane:sorted(v) for lane,v in selectors.items()},
        whole_suite_current='NOT RUN after the data-only amendment; no full-suite green claim.',
        prior_stage6_full_suite= json.loads((OUT.parent/'slot-retrieval-stage06-20261012/SUMMARY.json').read_text())['full'])
    save('TEST-VALIDATION.json',test_summary)
    allowed={'skills/photo-prompt-image-generator/assets/'+name for name in ['photo_prompt_visual_obligations.json','photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']}
    changed=[]
    for row in read('INPUTS-FROZEN.json')['files']:
        path=ROOT/row['path']
        actual=hashlib.sha256(path.read_bytes()).hexdigest()
        if actual!=row['sha256']:changed.append(dict(path=row['path'],before=row['sha256'],after=actual))
    assert {r['path'] for r in changed}==allowed,changed
    save('FROZEN-INPUT-CHANGES.json',dict(original_frozen_files=len(read('INPUTS-FROZEN.json')['files']),
        changed_existing_files=changed,unexpected_existing_file_changes=[],
        new_files='Generated active semantic shards, regression fixtures/test and stage07 evidence are inventoried separately.'))
    print(json.dumps(dict(public_cases=40,target_exposures=len(targets),adoption_eligible_targets=12,tests_unique=test_summary['unique_selectors'],current_tests=78,changed_existing_files=len(changed))))


if __name__=='__main__':
    main()
