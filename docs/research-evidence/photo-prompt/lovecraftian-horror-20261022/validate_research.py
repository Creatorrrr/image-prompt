"""Offline research integrity checks. Does not qualify runtime or natural-language truth."""
import ast,collections,copy,hashlib,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def read(n):return json.loads((HERE/n).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def require(ok,msg):
    if not ok:raise ValueError(msg)
def unique(xs,key):
    require(len(xs)==len({x[key] for x in xs}),'duplicate '+key)
def validate(data):
    sources,cards,drafts,routes,cases,mappings,audit,dom=data
    for rows,key in [(sources,'source_id'),(cards,'card_id'),(drafts,'draft_id'),(routes,'seed_id'),(cases,'case_id'),(mappings,'existing_card_id')]:unique(rows,key)
    ss={s['source_id']:s for s in sources};cc={c['card_id']:c for c in cards}
    require(len(routes)==sum(len(t)-1 for t in dom['tables'][:16])==185,'seed closure')
    for r in routes:
        row=dom['tables'][r['table_index']][r['row_index']]
        require(r['original_term']==row[0] and r['conversation_definition']==row[1],'seed source mismatch')
        require(r['card_refs'] and set(r['card_refs'])<=cc.keys(),'route card reference')
        require(r['hard_visual_obligation'] is False,'broad route cannot hard activate')
    for c in cards:
        require(c['source_refs'] and set(c['source_refs'])<=ss.keys(),'card source reference')
        require(all(ss[s].get('review_level') not in ('pending','availability_only',None) for s in c['source_refs']),'unreviewed source used as support')
        require(c['native_approval'] is False,'research cannot native-approve')
        require(c['seed_refs'],'unrouted semantic card')
        require(c['confusion_boundary_ko'] and c['claim_limit_ko'],'missing semantic boundary')
        if c['card_id'].startswith('R'):
            require(c.get('candidate_eligible') is True,'visual proposal classification')
            require(c.get('proposal_en') and c.get('proposal_ko'),'bilingual phrase missing')
            require(c['owners'] and c['relations'],'visible graph missing')
            for e in c['relations']:
                require(e['from'] in c['owners'] and e['to'] in c['owners'],'dangling relation endpoint')
                require(e['predicate'].strip(),'blank predicate')
            require(c['evidence_policy']=={'unobservable':'UNOBSERVABLE_NOT_PASS','whole_case':'partial_is_fail'},'pixel boundary missing')
            require(len([g for g in c['gates'] if '.relation' in g['gate_id']])==len(c['relations']),'gate relation closure')
        else:
            require(not c.get('candidate_eligible',False) and not c['owners'] and not c['relations'],'nonvisual promoted to visible proposal')
    visual={c['card_id'] for c in cards if c.get('candidate_eligible')}
    require({d['card_ref'] for d in drafts}==visual and len(drafts)==len(visual),'draft closure')
    for d in drafts:
        require(d['native_approval'] is False and d['runtime_candidate_id'] is None and d['runtime_realization_id'] is None,'native identity leakage')
        require(d['registration_status']=='research_only_not_in_operating_manifest','research registration')
        c=cc[d['card_ref']]
        require(d['phrase_en']==c['proposal_en'] and d['phrase_ko']==c['proposal_ko'],'draft text drift')
        require(d['owner_components']==c['owners'] and d['directed_relations']==c['relations'],'draft graph drift')
    catalog=json.loads((ROOT/'skills/photo-prompt-image-generator/assets/photo_candidate_slot_catalog.json').read_text())['slot_catalog']
    require(all(s in catalog for c in cards for s in c['proposed_slots']),'unknown current slot')
    for m in mappings:
        require(sha(canonical(m['existing_semantics']))==m['semantic_record_sha256'],'semantic snapshot hash')
        for r in m['source_records']:
            require(sha(canonical(r['record']))==r['source_record_sha256'],'candidate snapshot hash')
            require(r['candidate_id']==r['record']['id'],'CID mismatch')
            require(all(b.get('candidate_id')==r['candidate_id'] for b in r['bindings'].values()),'foreign binding')
    require(audit['snapshot_consistency']=='COHERENT','corpus changed during audit')
    require(len(audit['routes'])==len(routes),'lexical audit closure')
    require(all(c['status']=='NOT_RUN' and c['query_ko'] and c['query_en'] for c in cases),'unrun evaluation claimed run')
    require(all(set(c['card_refs'])<=cc.keys() for c in cases),'evaluation reference')
    require(dict(collections.Counter(c['kind'] for c in cases))=={'positive':30,'boundary':26,'ordinary_control':12,'nonvisual_or_unresolved':12},'evaluation balance')
    require(not ({'K09','K10','K11','K12','K19','K26'}-cc.keys()),'deferred scope missing')

def main():
    data=[read(n) for n in ['sources.json','semantic-cards.json','candidate-drafts.json','keyword-routes.json','evaluation-cases.json','existing-source-mapping.json','CORPUS-LEXICAL-AUDIT.json','conversation-dom.json']]
    validate(data)
    mutations=[
        ('dangling endpoint',lambda d:d[1][0]['relations'][0].update(to='missing_owner')),
        ('missing source',lambda d:d[1][0].update(source_refs=['MISSING'])),
        ('broad hard obligation',lambda d:d[3][0].update(hard_visual_obligation=True)),
        ('native approval',lambda d:d[1][0].update(native_approval=True)),
        ('runtime CID',lambda d:d[2][0].update(runtime_candidate_id='cand_fake')),
        ('nonvisual promotion',lambda d:d[1][-1].update(candidate_eligible=True)),
        ('missing translation',lambda d:d[1][0].update(proposal_ko='')),
        ('false executed evaluation',lambda d:d[4][0].update(status='PASS')),
        ('stale source snapshot hash',lambda d:d[5][0].update(semantic_record_sha256='0'*64)),
        ('duplicate route',lambda d:d[3][1].update(seed_id=d[3][0]['seed_id'])),
    ]
    rejected=[]
    for name,mutate in mutations:
        damaged=copy.deepcopy(data);mutate(damaged)
        try:validate(damaged)
        except ValueError:rejected.append(name)
        else:raise ValueError('Mutation was accepted: '+name)
    for f in HERE.glob('*.py'):ast.parse(f.read_text(),filename=str(f))
    baseline=read('BASELINE.json');changed=[];missing=[]
    for name,expected in baseline['protected_sha256'].items():
        p=ROOT/name
        if not p.exists():missing.append(name)
        elif sha(p.read_bytes())!=expected:changed.append(name)
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    audit=data[6]
    newer=[]
    for name,expected in audit['module_sha256'].items():
        path=ROOT/'skills/photo-prompt-image-generator/assets'/name
        if not path.exists() or sha(path.read_bytes())!=expected:newer.append(name)
    drift=dict(initial_head=baseline['head'],current_head=head,head_changed=head!=baseline['head'],
        protected_file_count=len(baseline['protected_sha256']),changed_paths=changed,missing_paths=missing,
        modules_changed_after_corpus_snapshot=newer,
        note='This task writes only its research directory. Concurrent source differences are observations, not attributed edits or a reason to revert other work. Rebaseline before implementation.')
    (HERE/'SOURCE-DRIFT.json').write_text(json.dumps(drift,ensure_ascii=False,indent=2)+'\n')
    status='STRUCTURE_PASS_SOURCE_DRIFT_REQUIRES_REBASELINE' if changed or missing or head!=baseline['head'] or newer else 'RESEARCH_STRUCTURE_PASS'
    result=dict(status=status,structure_status='PASS',counts=read('COUNTS.json'),
        source_review_counts=dict(collections.Counter(s['review_level'] for s in data[0])),
        existing_semantic_mappings=len(data[5]),existing_candidate_snapshots=sum(len(m['source_records']) for m in data[5]),
        corpus_snapshot_consistency=audit['snapshot_consistency'],corpus_candidate_count=audit['candidate_count'],
        planned_evaluation_cases=len(data[4]),planned_bilingual_inputs=2*len(data[4]),evaluation_status='NOT_RUN',
        mutation_rejections=rejected,mutation_rejections_count=len(rejected),
        observed_source_drift_count=len(changed),missing_protected_count=len(missing),
        checks=['seed closure/order','source review scope','owner/edge endpoint closure','draft/card closure','current slot names','saved source hashes','research authority boundary','evaluation NOT_RUN','Python syntax'],
        not_established=['natural-language completeness','full original artwork fidelity','runtime registration of these drafts','native qualification','actual retrieval performance','new embeddings','generated pixels','artistic preference','user acceptance','commit or push'])
    (HERE/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    (HERE/'FINAL-STATE.json').write_text(json.dumps(dict(head=head,status=subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True),scope='research directory only'),ensure_ascii=False,indent=2)+'\n')
    sums=[f'{sha(p.read_bytes())}  {p.relative_to(HERE)}' for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='SHA256SUMS' and '__pycache__' not in p.parts]
    (HERE/'SHA256SUMS').write_text('\n'.join(sums)+'\n')
    print(json.dumps({k:result[k] for k in ['status','structure_status','existing_semantic_mappings','existing_candidate_snapshots','mutation_rejections_count','observed_source_drift_count','missing_protected_count','planned_evaluation_cases','planned_bilingual_inputs']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
