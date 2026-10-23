"""Integrity checks for the research package, not runtime or semantic qualification."""
from pathlib import Path
import collections, hashlib, json, re, subprocess
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def read(n):return json.loads((HERE/n).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    sources=read('sources.json')['sources'];cards=read('semantic-cards.json')['cards'];drafts=read('candidate-drafts.json')['drafts'];route_doc=read('keyword-routes.json');routes=route_doc['routes'];cases=read('evaluation-cases.json')['cases'];counts=read('PACKAGE-COUNTS.json')
    source_ids={s['source_id'] for s in sources};by_id={c['card_id']:c for c in cards};visual=[c for c in cards if c['kind']!='context_only'];contexts=[c for c in cards if c['kind']=='context_only'];gates={}
    assert len(source_ids)==len(sources)==len({s['url'] for s in sources})
    assert len(by_id)==len(cards)
    assert all(s['url'].startswith('https://') and s['source_image_review']=='NOT_RUN' for s in sources)
    catalog=json.loads((ROOT/'skills/photo-prompt-image-generator/assets/photo_candidate_slot_catalog.json').read_text())['slot_catalog']
    for c in cards:
        assert set(c['source_ids'])<=source_ids and c['source_ids'],c['card_id']
        assert c['native_approval'] is False and c['automatic_activation'] is False and c['runtime_registration']=='none'
        if c['kind']=='context_only':assert not c['gates'] and c['proposal_en'] is None;continue
        assert c['proposal_en'] and c['proposal_ko'] and c['owners']
        assert set(c['proposed_slots'])<=set(catalog)
        for r in c['directed_relations']:assert r['from'] in c['owners'] and r['to'] in c['owners'],(c['card_id'],r)
        for owner,n in c['count_constraints'].items():assert owner in c['owners'] and isinstance(n,int) and n>0
        for g in c['gates']:
            assert g['gate_id'] not in gates
            assert g['status']=='NOT_RUN' and g['partial_is_fail'] and g['unobservable_status']=='UNOBSERVABLE_NOT_PASS'
            gates[g['gate_id']]=g
    assert len(drafts)==len(visual)==len({d['draft_id'] for d in drafts})
    for d in drafts:
        c=by_id[d['card_id']]
        assert d['candidate_id'] is None and d['rid'] is None and d['status']=='research_draft_only'
        assert d['content']=={'en':c['proposal_en'],'ko':c['proposal_ko']}
        assert d['required_gates']==[g['gate_id'] for g in c['gates']]
        assert d['proposed_disposition']==c['proposed_disposition']
        assert d['native_approval'] is False and d['automatic_activation'] is False
    assert len({r['route_id'] for r in routes})==len(routes)
    for r in routes:assert set(r['target_card_ids'])<=set(by_id) and r['target_card_ids']
    sections={int(re.match(r'\d+',r['original_section']).group()) for r in routes if r['original_section']}
    assert sections==set(range(1,18)) and route_doc['chrome_recovery_complete']
    assert read('REFERENCE-ACCESS.json')['chrome_recovery']['status']=='complete'
    assert len({c['case_id'] for c in cases})==len(cases)
    for c in cases:
        assert c['query_en'] and c['query_ko'] and c['result']=='NOT_RUN'
        assert set(c['expected_card_ids']+c.get('confusion_card_ids',[]))<=set(by_id)
        if c['cohort']=='authored_boundary_control':assert c['expected_card_ids']==[] and c['confusion_card_ids']
    assert not read('evaluation-cases.json')['independent_holdout']
    actual=dict(visual_cards=len(visual),context_cards=len(contexts),candidate_drafts=len(drafts),keyword_routes=len(routes),sources=len(sources),development_cases=sum(c['cohort']=='card_derived_development' for c in cases),boundary_cases=sum(c['cohort']=='authored_boundary_control' for c in cases),bilingual_queries_planned=2*len(cases),relation_gates=sum(len(c['directed_relations']) for c in visual),count_gates=sum(len(c['count_constraints']) for c in visual))
    assert all(counts[k]==v for k,v in actual.items())
    # A record snapshot proves what was read, never current native approval.
    reviewed={};matched=set()
    for f in ['existing-source-mapping.json','existing-source-supplement.json']:
        for r in read(f)['records']:
            matched.add(r['candidate_id']);record_hash=sha(json.dumps(r['record'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
            assert record_hash==r['record_sha256'] and r['native_approval'] is False
            assert set(r['related_card_ids'])<=set(by_id)
            if r['manual_review']:reviewed[r['candidate_id']]=r
    assert counts['unique_manually_reviewed_existing_sources']==len(reviewed)
    baseline=read('BASELINE.json');drift=[]
    manifest=ROOT/'skills/photo-prompt-image-generator/assets/photo_candidate_corpus_manifest.json'
    current_manifest_hash=sha(manifest.read_bytes())
    if current_manifest_hash!=baseline['manifest_sha256']:drift.append({'path':str(manifest.relative_to(ROOT)),'before':baseline['manifest_sha256'],'after':current_manifest_hash})
    for name,h in baseline['module_sha256'].items():
        p=ROOT/'skills/photo-prompt-image-generator/assets'/name
        now=sha(p.read_bytes()) if p.exists() else None
        if now!=h:drift.append({'path':str(p.relative_to(ROOT)),'before':h,'after':now})
    for name,h in baseline['protected_files'].items():
        p=ROOT/name;now=sha(p.read_bytes()) if p.exists() else None
        if now!=h:drift.append({'path':name,'before':h,'after':now})
    result=dict(status='PASS',scope='Research integrity and snapshot consistency only; no runtime/retrieval/native/pixel tests',counts=counts,source_sections_covered=sorted(sections),unique_lexically_matched_sources=len(matched),unique_manually_reviewed_sources=len(reviewed),protected_authored_and_runtime_files_checked=1+len(baseline['module_sha256'])+len(baseline['protected_files']),protected_drift=drift,head_before=baseline['head'],head_after=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),native_review='NOT_RUN',retrieval='NOT_RUN',images='NOT_RUN',user_acceptance='PENDING',commit_push='NOT_RUN_BY_THIS_TASK')
    (HERE/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    # Own package files only. No cleanup or writes outside HERE.
    files=sorted(p for p in HERE.iterdir() if p.is_file() and p.name!='SHA256SUMS')
    (HERE/'SHA256SUMS').write_text(''.join(f'{sha(p.read_bytes())}  {p.name}\n' for p in files))
    print(json.dumps({k:result[k] for k in ['status','unique_lexically_matched_sources','unique_manually_reviewed_sources','protected_drift','head_before','head_after']},ensure_ascii=False))
if __name__=='__main__':main()
