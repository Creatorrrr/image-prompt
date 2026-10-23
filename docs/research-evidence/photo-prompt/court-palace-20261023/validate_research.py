"""Reference/ownership/scope integrity, not historical truth or runtime quality."""
import collections,csv,hashlib,json,pathlib,re,subprocess
H=pathlib.Path(__file__).resolve().parent;ROOT=H.parents[3]
def read(n):return json.loads((H/n).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def main():
    checks=[]
    def check(name,ok,detail=None):
        checks.append({'name':name,'pass':bool(ok),'detail':detail})
    cards=read('semantic-cards.json')['cards'];sources=read('sources.json')['sources'];drafts=read('candidate-drafts.json')['drafts'];routes=read('keyword-routes.json')['rows'];ref=read('reference-rows.json');counts=read('PACKAGE-COUNTS.json');mapping=read('existing-source-mapping.json');snap=read('corpus-snapshot.json')
    cs={c['id']:c for c in cards};ss={s['id']:s for s in sources}
    check('unique IDs',len(cs)==len(cards) and len(ss)==len(sources) and len({r['id'] for r in routes})==len(routes))
    check('expected package scope',len(cards)==88 and len(drafts)==73 and len(sources)==40 and len(routes)==623 and len(ref['rows'])==622 and len(ref['sections'])==34)
    check('all source references exist',all(set(c['source_ids'])<=ss.keys() for c in cards))
    check('directed graph endpoints and relation IDs',all({r[k] for r in c['relations'] for k in ['subject','object']}<={n['id'] for n in c['components']} and len({r['id'] for r in c['relations']})==len(c['relations']) and all(r['type'] and r['subject']!=r['object'] for r in c['relations']) for c in cards))
    check('KO EN boundary and gate present',all(c['visible_ko'] and c['visible_en'] and c['confusion_boundary'] and c['pixel_gate'] and c['source_scope'] for c in cards))
    check('optional and strict observation policies',all(c['adoption']=='optional_post_core_only' and c['unobservable_policy']=='UNOBSERVABLE_NOT_PASS' and c['partial_policy']=='partial_is_fail' for c in cards))
    check('context cannot become positive draft',set(d['card_id'] for d in drafts)=={c['id'] for c in cards if c['kind']!='context_only'})
    check('drafts are not operating records',all(d['actual_candidate_id'] is None and d['actual_slot_bindings']==[] and d['native_approval'] is False and d['registration_status']=='NOT_ADOPTED' for d in drafts))
    check('unverified artifact stays deferred',cs['D06']['historical_review_required'] and next(d for d in drafts if d['card_id']=='D06')['proposed_disposition'].startswith('defer'))
    check('all pending artifact reviews remain pending',all(d['proposed_disposition'].startswith('defer') for d in drafts if cs[d['card_id']]['historical_review_required']))
    check('reference rows preserved in order',all(all(routes[i][k]==r[k] for k in ['part','section','term','definition']) for i,r in enumerate(ref['rows'])))
    check('route references and no automatic visual obligation',all(set(r['related_card_ids']+r.get('family_reference_ids',[]))<=cs.keys() and r['visual_obligation'] is False for r in routes))
    check('deferred term has only family guidance',all(not r['related_card_ids'] and r.get('family_reference_ids') and r['coverage_level']=='family_only_exact_definition_deferred' for r in routes if r['disposition']=='defer_term_specific_research'))
    # False reverse substring matches would map 군주 to 군주 시해. Test the preserved input.
    monarch=next(r for r in routes if r['term']=='군주')
    check('no reverse-substring regicide inference','K08' not in monarch['related_card_ids'])
    check('counts agree',counts['cards']==len(cards) and counts['drafts']==len(drafts) and counts['historical_review_required']==sum(c['historical_review_required'] for c in cards) and counts['route_dispositions']==dict(collections.Counter(r['disposition'] for r in routes)))
    slots=json.loads((ROOT/'skills/photo-prompt-image-generator/assets/photo_candidate_slot_catalog.json').read_text())['slot_catalog']
    check('proposed role names exist',all(set(d['proposed_role_review'])<=slots.keys() for d in drafts),{'catalog_slot_count_observed':len(slots),'binding_approval':False})
    check('frozen corpus record and binding hashes',all(x['record_sha256']==sha(canonical(x['record'])) and x['bindings_sha256']==sha(canonical(x['bindings'])) for x in mapping['records']))
    snapshot_by_id={x['cid']:x for x in snap['records']}
    check('mapping preserved whole source and bindings',all(x['record']==snapshot_by_id[x['cid']]['record'] and x['bindings']==snapshot_by_id[x['cid']]['bindings'] for x in mapping['records']))
    check('manual decisions real existing IDs',sum(x['proposed_disposition']!='lexical_adjacent_unreviewed' for x in mapping['records'])==mapping['manual_decision_count']==19)
    cases=read('evaluation-cases.json')['cases'];pairs=list(csv.DictReader((H/'CONFUSION-CASES.tsv').open(),delimiter='\t'))
    check('evaluation references and NOT_RUN',len(cases)==88 and all(set(c['expected_card_ids'])<=cs.keys() and c['retrieval_status']==c['pixel_status']==c['prompt_status']==c['acceptance_status']=='NOT_RUN' for c in cases))
    check('contrast pairs complete',len(pairs)==24 and all(all(p[k] for k in ['pair_id','query_a_ko','query_a_en','query_b_ko','query_b_en','expected_boundary']) and p['status']=='NOT_RUN' for p in pairs))
    check('raw reference excludes unrelated sidebar',(H/'reference-ax.txt').read_text().startswith('148 heading') and '앱 탐색' not in (H/'reference-ax.txt').read_text())
    missing_links=[]
    for p in H.glob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            # These two outputs are emitted below, including on the first clean run.
            if '://' not in link and link not in {'VALIDATION.json','SHA256SUMS'} and not (p.parent/link.split('#')[0]).exists():missing_links.append((p.name,link))
    check('local document links resolve',not missing_links,missing_links)
    base=read('BASELINE.json');drift=[]
    for name,old in base['protected'].items():
        p=ROOT/name;now=sha(p.read_bytes()) if p.exists() else None
        if now!=old:drift.append({'path':name,'baseline':old,'current':now})
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    # Preserve external changes as observations, never a reason to restore shared files.
    result={'schema':'court-palace-research-validation/v1','research_structure':'PASS' if all(c['pass'] for c in checks) else 'FAIL','checks':checks,'counts':counts,'corpus_snapshot':{'candidates':snap['record_count'],'bindings':snap['binding_count'],'lexical_hits':len(snap['records']),'manual_decisions':19},'evaluation_plan':{'cases':len(cases)+len(pairs)*2,'language_queries':len(cases)*2+len(pairs)*4,'retrieval':'NOT_RUN','images':'NOT_RUN'},'workspace_observation':{'baseline_head':base['head'],'current_head':head,'head_changed':base['head']!=head,'protected_count':len(base['protected']),'protected_hashes_equal':not drift,'protected_drift':drift,'scope_of_agent_writes':'Only new court-palace-20261023 research directory; external drift is not reverted.','all_repository_files_unchanged_claim':False},'not_proven':['Independent historical correctness of all original terms','Native semantic approval','Index source closure or embedding compatibility','Actual retrieval rank and semantic adoption','Prompt transport','Generated native pixels','User acceptance','Commit or push']}
    (H/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    sums=[]
    for p in sorted(H.iterdir()):
        if p.is_file() and p.name!='SHA256SUMS':sums.append(f'{sha(p.read_bytes())}  {p.name}')
    (H/'SHA256SUMS').write_text('\n'.join(sums)+'\n')
    print(json.dumps({'research_structure':result['research_structure'],'checks':len(checks),'failed':[c for c in checks if not c['pass']],'protected_drift_count':len(drift),'head_changed':head!=base['head'],'sha_files':len(sums)},ensure_ascii=False,indent=2))
    if result['research_structure']!='PASS':raise SystemExit(1)
if __name__=='__main__':main()
