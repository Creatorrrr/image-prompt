"""Close the current merged-source verification and preserve failure history."""
import hashlib
import json
from pathlib import Path
import re

OUT=Path(__file__).resolve().parent
STAGE=OUT.parent


def read(name):return json.loads((OUT/name).read_text())
def save(name,value):(OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def main():
    public=[row for i in range(4) for row in read('REPAIRED-PUBLIC-ENTRYPOINTS-'+str(i)+'.json')['cases']]
    assert len(public)==40 and len({r['case'] for r in public})==40
    meta=read('REPAIRED-RUNTIME.json')
    assert {r['generation_id'] for r in public}=={meta['generation_id']}
    assert all(r['cli_exit']==r['view_exit']==0 and not r['recomputation_errors'] and r['omission_detected'] for r in public)
    targets=json.loads((STAGE/'CRITERIA-FROZEN.json').read_text())['natural_targets']
    positives=negatives=0;target_rows=[];changed=[]
    before_subject=json.loads((STAGE/'CRITERIA-FROZEN.json').read_text())['subject_adjudication']['cases']
    for lane,old_lane in [('repaired-public-natural','qualified-public-natural'),('repaired-public-native','qualified-public-native')]:
        for path in (OUT/lane).glob('*/candidate-pack.json'):
            pack=json.loads(path.read_text())[0];old=json.loads((STAGE/old_lane/path.parent.name/'candidate-pack.json').read_text())[0]
            assert pack['authorial_core']==old['authorial_core'] and pack['creative_controls']==old['creative_controls'] and pack['negative_en']==old['negative_en']
            ids={c['id'] for slot in pack['slots'].values() for c in slot['candidates']};old_ids={c['id'] for slot in old['slots'].values() for c in slot['candidates']}
            assert len(ids)<=64 and all(len(s['candidates'])<=s['candidate_limit'] for s in pack['slots'].values())
            if ids!=old_ids:changed.append(dict(case=path.parent.name,added=sorted(ids-old_ids),removed=sorted(old_ids-ids)))
            for identity in targets.get(path.parent.name,{}).get('required_compatible',[]):
                candidate=next((c for slot in pack['slots'].values() for c in slot['candidates'] if c['id']==identity),None);assert candidate
                target_rows.append(dict(case=path.parent.name,id=identity,applicability=candidate['applicability']['status']))
            if lane=='repaired-public-natural':
                frozen=next(r for r in before_subject if r['key']==path.parent.name)
                actual={c['entry_id'] for c in pack['slots'].get('subject',{}).get('candidates',[])}
                assert actual=={r['id'] for r in frozen['after_subject']},(path.parent.name,actual)
            else:
                spec=next(r for r in json.loads((STAGE/'CASES-FROZEN.json').read_text()) if r['key']==path.parent.name)
                expected=next(r for r in json.loads((STAGE/'EXPECTATIONS.json').read_text()) if r['native_alias']==spec['native_alias'])['source_candidates'][0]['document_id']
                hit=expected in ids
                if spec['mode']=='positive':positives+=int(hit);assert hit,path.parent.name
                else:negatives+=int(hit);assert not hit,path.parent.name
    assert len(target_rows)==13 and positives==10 and negatives==0
    audits=read('REPAIRED-COMPOSITION-VALIDATION.json');assert len(audits)==9
    assert all(r['actual_receipt_verified'] and r['generation_id']==meta['generation_id'] and r['composed_audit']['status']==r['runtime_audit']['status']=='pass' and not r['embodiment_failures'] for r in audits)
    all_inputs=read('REPAIRED-COMPOSITION-ALL-INPUTS.json')['cases'];assert len(all_inputs)==48
    old_inputs=json.loads((STAGE/'QUALIFIED-COMPOSITION-INPUTS.json').read_text())['cases'];old_map={(r['case'],r['variant']):r for r in old_inputs}
    for row in all_inputs:
        value=json.loads(Path(row['inputs']['composed']['path']).read_text());before=json.loads(Path(old_map[(row['case'],row['variant'])]['inputs']['composed']['path']).read_text())
        assert value['prompt_en']==before['prompt_en'] and value['negative_en']==before['negative_en'] and value['chosen_candidate_ids']==before['chosen_candidate_ids']
    selectors=set()
    for lane in ['merge-focused','repaired-animal-context','repaired-bird-negative-recheck']:
        selectors.update(re.findall(r'\((tests\.[^)]+)\)',(OUT/(lane+'-tests.log')).read_text()))
    assert read('merge-focused-tests.json')['successful'] and read('repaired-bird-negative-recheck-tests.json')['successful']
    initial=read('repaired-animal-context-tests.json');assert not initial['failures'] and len(initial['errors'])==2
    assert all('setting needs at least 3 concrete content words' in r['traceback'] for r in initial['errors'])
    result=dict(runtime=meta,public_entrypoint_cases=40,cli_view_recomputation_errors=0,native_hits=10,native_false_hits=0,
        required_target_exposures=target_rows,adoption_eligible_targets=12,changed_candidate_sets=changed,
        original_subject_meaning_preserved=True,current_full_composed_runtime_audits=9,all_current_critical_audits_pass=True,
        final_prose_negative_choices_unchanged=48,original_full_48_audits='Sealed stage07 history, not 48 current-source reaudits.',
        tests_unique=len(selectors),all_latest_selectors_pass=True,
        harness_error='One new bird negative fixture initially had only two setting content words. Expanded its new setting, then reran that selector; raw failed result retained. Frozen benchmark/holdout unchanged.',
        exact=read('merged-exact/exact-recall-summary.json')['totals'],exact_reuse=read('REPAIRED-RETRIEVAL-INVARIANCE.json'),
        animal_scope_repair=read('ANIMAL-SCOPE-REPAIR.json'),embedding_api_calls=0,image_calls=0,
        whole_suite='Not rerun; no full-suite green claim.',core_controls_negative_and_caps_preserved=True)
    save('FINAL-MERGE-VALIDATION.json',result)
    print(json.dumps({k:result[k] for k in ['public_entrypoint_cases','current_full_composed_runtime_audits','tests_unique','native_hits','native_false_hits']}))


if __name__=='__main__':main()
