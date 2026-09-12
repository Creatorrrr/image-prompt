"""Validate research integrity, not generator quality. Does not mutate runtime assets."""
import hashlib
import json
import re
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def read(name):return json.loads((HERE/name).read_text())
def unique_ids(rows):
    ids=[r['id'] for r in rows]
    assert len(ids)==len(set(ids)), 'duplicate id'
    return set(ids)
sources=read('sources.json')['sources'];sids=unique_ids(sources)
props=read('visual-proposals.json')['proposals'];pids=unique_ids(props)
bundles=read('candidate-bundles.json')['bundles'];unique_ids(bundles)
cases=[json.loads(x) for x in (HERE/'evaluation-cases.jsonl').read_text().splitlines()];unique_ids(cases)
inv=read('keyword-inventory.json');audit=read('repo-audit.json')
assert len(sources)==19 and len(props)==37 and len(bundles)==20 and len(cases)==98
original=read('source-conversation.json')['turns'][0]['items'][1]['text']
spans=re.findall(r'`([^`]+)`',original)
assert spans==[x['text'] for x in inv['occurrences']]
assert set(spans)=={x['text'] for x in inv['terms']}
assert len(spans)==inv['occurrence_count']==253
assert len(set(spans))==inv['unique_span_count']==233
core=read('core-keyword-map.json')['rows']
assert len(core)==20 and len({x['term'] for x in core})==20
assert all(set(x['proposal_ids'])<=pids and x['term'] in spans and not x['hard_activation'] for x in core)
existing={x['record']['id'] for x in audit['selected_existing_records']}
design_count=0
for p in props:
    assert not p['runtime_registered'] and p['status']=='research_draft'
    assert not p['activation']['broad_realism_keyword_is_hard_trigger']
    assert len(p['required_visible_components'])>=3
    assert p['owner'] and p['prerequisites'] and p['confusion_boundaries']
    assert set(p['source_ids'])<=sids
    assert set(p['existing_profile_ids'])<=existing
    if not p['source_ids']:
        design_count+=1
        assert p['evidence_level']=='authored_design_hypothesis_without_direct_empirical_source'
    assert p['evaluation']['generated_image_test']=='not_run'
    for suffix in ['positive','near_miss']:
        assert any(x['id']==p['id']+'_'+suffix for x in cases)
assert design_count==6
for b in bundles:
    assert set(b['required_if_this_bundle_is_explicitly_selected']+b['optional_proposal_ids'])<=pids
    assert not b['runtime_registered'] and b['candidate_pack_exposure']=='not_run'
for t in inv['terms']:
    assert not t['hard_activation']
    assert set(t['related_proposal_ids'])<=pids
assert all(x['execution_status']=='not_run' for x in cases)
assert all(x['id'] in sids and x['url'].startswith('https://') and x['limit'] for x in sources)
assert len(audit['exact_match_diagnostics'])==22
changed=[]
for x in audit['source_files']:
    if hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()!=x['sha256']:changed.append(x['path'])
assert not changed, 'authored source changed since read-only audit: '+str(changed)
for suffix in ['.json','.jsonl']:
    for p in HERE.glob('*'+suffix):
        if p.name=='validation.json':continue
        if suffix=='.json':json.loads(p.read_text())
        else:
            for line in p.read_text().splitlines():json.loads(line)
report=(HERE/'report.md').read_text()
assert '<!-- SOURCES -->' not in report
for sid in sids: assert '['+sid+'](' in report
out={'schema_version':'photo-research-validation/v1','status':'passed','verified_at':'2026-09-12',
 'counts':{'sources':len(sources),'proposals':len(props),'design_only_proposals':design_count,
 'bundles':len(bundles),'specification_cases':len(cases),'unique_input_spans':len(set(spans)),
 'input_occurrences':len(spans),'existing_exact_diagnostics':22,'source_files_unchanged':len(audit['source_files'])},
 'checks':['JSON parse','unique IDs','complete input-span preservation','source and proposal references',
  'existing reuse IDs observed in current authored sources','all research-only flags',
  'positive and near-miss specification coverage','existing authored source SHA-256 unchanged',
  'source inventory present in report'],
 'not_verified':['new runtime integration','index generation','candidate exposure or selection',
 'prompt audit','image generation','pixel quality','causal improvement','user preference'],
 'artifact_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.iterdir())
    if p.is_file() and p.name!='validation.json'}}
(HERE/'validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'passed','counts':out['counts']},ensure_ascii=False))
