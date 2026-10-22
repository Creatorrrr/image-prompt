"""Research integrity and source drift checks; no runtime/model execution."""
import collections,csv,hashlib,json,pathlib,re,subprocess
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(obj):return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def read(name):return json.loads((HERE/name).read_text())
def main():
    errors=[];checks={}
    def check(name,value):
        checks[name]=bool(value)
        if not value:errors.append(name)
    seed=read('reference-seeds.json')['seeds'];routes=read('keyword-routes.json')['routes']
    source=read('sources.json')['sources'];semantic=read('semantic-cards.json');cs=semantic['cards']
    drafts=read('candidate-drafts.json')['drafts'];audit=read('CORPUS-LEXICAL-AUDIT.json')
    mapping=read('existing-source-mapping.json');scenes=read('scene-blueprints.json')['blueprints']
    source_ids={s['source_id'] for s in source};card_ids={c['card_id'] for c in cs};by_card={c['card_id']:c for c in cs}
    check('reference_150_unique_complete',{s['seed_id'] for s in seed}==set(range(1,151)) and len(seed)==150)
    check('routes_150_unique_complete',{r['seed_id'] for r in routes}==set(range(1,151)) and len(routes)==150)
    check('sources_32_unique',len(source)==len(source_ids)==32)
    check('source_urls_and_read_scopes',all(s['url'].startswith('https://') and s['read_scope'] and s['supported_scope_and_limit_ko'] for s in source))
    check('cards_96_unique',len(cs)==len(card_ids)==96)
    check('source_and_seed_references',all(set(c['source_ids'])<=source_ids and set(c['seed_ids'])<=set(range(1,151)) for c in cs))
    check('all_keyword_route_references',all(set(r['card_ids'])<=card_ids and r['automatic_hard_activation'] is False for r in routes))
    check('every_card_has_a_route',all(c['routed_seed_ids'] for c in cs))
    current_catalog_raw=(ROOT/'skills/photo-prompt-image-generator/assets/photo_candidate_slot_catalog.json').read_bytes()
    catalog=json.loads(current_catalog_raw)['slot_catalog']
    check('slot_references_current',all(set(c['proposed_slots'])<=set(catalog) for c in cs))
    check('graphs_have_existing_distinct_endpoints',all(r['from'] in c['owners'] and r['to'] in c['owners'] and r['from']!=r['to'] for c in cs for r in c['directed_relations']))
    check('all_visible_owners_participate',all(set(c['owners'])=={x for r in c['directed_relations'] for x in (r['from'],r['to'])} for c in cs if c['observability']!='context'))
    context=[c for c in cs if c['observability']=='context'];visible=[c for c in cs if c['observability']!='context']
    check('12_context_no_positive_graph_or_gate',len(context)==12 and all(not c['owners'] and not c['directed_relations'] and not c['gates'] and c['context_scope'] for c in context))
    check('84_drafts_exact_visible_cards',len(drafts)==84 and {d['card_id'] for d in drafts}=={c['card_id'] for c in visible})
    check('draft_hashes_and_bilingual_payload',all(d['semantic_card_sha256']==sha(canonical(by_card[d['card_id']])) and d['proposal_en']==by_card[d['card_id']]['proposal_en'] and d['proposal_ko']==by_card[d['card_id']]['proposal_ko'] for d in drafts))
    check('drafts_inert',all(d['native_approval'] is False and d['runtime_registration']=='none' and d['candidate_id'] is None and d['realization_id'] is None for d in drafts))
    gates=[g for c in cs for g in c['gates']]
    check('217_unique_relation_gates',len(gates)==len({g['gate_id'] for g in gates})==217)
    check('strict_observability_gates',all(g['partial_is_fail'] and not g['unobservable_is_pass'] and g['pixel_status']=='NOT_RUN' and g['both_endpoints_required'] for g in gates))
    check('gate_graph_correspondence',all([g['required_relation'] for g in c['gates']]==c['directed_relations'] for c in visible))
    check('claim_and_confusion_and_bilingual_fields',all(c['claim_limit_ko'] and c['nearest_confusion_ko'] and c['proposal_en'] and c['proposal_ko'] and c['native_approval'] is False for c in cs))
    check('24_unique_full_existing_snapshots',len(mapping)==len({m['candidate_id'] for m in mapping})==24 and all(m['record']['id']==m['candidate_id'] and m['source_sha256']==sha(canonical(m['record'])) and 'bindings' in m and m['native_adoption']=='NOT_RUN' for m in mapping))
    with (HERE/'EVALUATION-CASES.tsv').open() as f:cases=list(csv.DictReader(f,delimiter='\t'))
    check('68_bilingual_not_run_development_cases',len(cases)==68 and dict(collections.Counter(c['cohort'] for c in cases))=={'development':32,'boundary':16,'ordinary':12,'nonvisual':8} and all(c['query_en'] and c['query_ko'] and c['execution_status']=='NOT_RUN' and c['gold_cid_rid']=='PENDING' for c in cases))
    check('evaluation_card_and_slot_references',all(set(c['target_cards'].split(','))<=card_ids and set(c['slots'].split(','))<=set(catalog) for c in cases))
    check('12_scene_blueprints',len(scenes)==12 and all(set(s['optional_cards'])<=card_ids and s['authored_scene_proposal_ko'] for s in scenes))
    links=[]
    for file in HERE.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',file.read_text()):
            if not target.startswith(('http:','https:','#')):
                links.append((file.name,target,(file.parent/target.split('#')[0]).exists()))
    # These two output files are created below on the first validation run.
    check('local_markdown_links_resolve',all(x[2] or x[1] in {'VALIDATION.json','SHA256SUMS'} for x in links))
    baseline=read('BASELINE.json');tracked_drift=[]
    for rel,expected in baseline['tracked_sha256'].items():
        f=ROOT/rel
        if not f.is_file() or sha(f.read_bytes())!=expected:tracked_drift.append(rel)
    module_drift=[rel for rel,expected in audit['source_module_sha256'].items() if not (ROOT/'skills/photo-prompt-image-generator/assets'/rel).is_file() or sha((ROOT/'skills/photo-prompt-image-generator/assets'/rel).read_bytes())!=expected]
    current_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
    drift={'tracked_files_changed_since_baseline':tracked_drift,'source_modules_changed_since_audit':module_drift,
      'catalog_changed_since_build':sha(current_catalog_raw)!=semantic['catalog_sha256'],
      'head_changed':current_head!=baseline['head'],'baseline_head':baseline['head'],'current_head':current_head,
      'interpretation':'Observational drift, not attribution. Never revert concurrent work. Rebaseline before implementation if any protected identity changed.'}
    is_drift=bool(tracked_drift or module_drift or drift['head_changed'] or drift['catalog_changed_since_build'])
    manifest=[]
    for f in sorted(HERE.iterdir()):
        if f.is_file() and f.name not in {'SHA256SUMS','VALIDATION.json'}:manifest.append(f'{sha(f.read_bytes())}  {f.name}')
    (HERE/'SHA256SUMS').write_text('\n'.join(manifest)+'\n')
    # The hash manifest includes source scripts and documents but excludes itself and this changing report.
    result={'schema':'genre-fusion-research-validation/v1','date_kst':'2026-10-22',
      'status':'FAIL' if errors else ('STRUCTURE_PASS_SOURCE_DRIFT_REQUIRES_REBASELINE' if is_drift else 'RESEARCH_STRUCTURE_PASS'),
      'checks':checks,'errors':errors,'counts':{'seeds':len(seed),'sources':len(source),'cards':len(cs),'positive_drafts':len(drafts),'context_cards':len(context),'relation_gates':len(gates),'existing_snapshots':len(mapping),'evaluation_cases':len(cases),'bilingual_queries':len(cases)*2,'scene_blueprints':len(scenes),'hashed_package_files':len(manifest)},
      'source_drift':drift,'calls':{'embedding':0,'retrieval':0,'image':0},
      'not_performed':['runtime registration','index build/publication','native source qualification','retrieval evaluation','image/pixel evaluation','independent translation review','independent holdout evaluation','user acceptance','commit','push'],
      'proof_boundary':'Research integrity and read-only source snapshots only. This does not validate literary definitions exhaustively, role fit, operating code, rankings, native pixels or user preference.'}
    (HERE/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'checks':len(checks),'errors':errors,'counts':result['counts'],'tracked_drift':len(tracked_drift),'module_drift':module_drift,'head_changed':drift['head_changed']},ensure_ascii=False))
    return 1 if errors else 0
if __name__=='__main__':raise SystemExit(main())
