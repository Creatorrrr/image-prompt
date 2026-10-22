"""Research integrity validation, separate from source qualification and quality."""
import collections,csv,hashlib,json,pathlib,re,subprocess,sys
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def read(n):return json.loads((HERE/n).read_text())
def main():
    checks={};errors=[]
    def check(n,b):
        checks[n]=bool(b)
        if not b:errors.append(n)
    seeds=read('reference-seeds.json')['seeds'];routes=read('keyword-routes.json')['routes']
    ss=read('sources.json')['sources'];cs=read('semantic-cards.json')['cards'];ds=read('candidate-drafts.json')['drafts']
    mapping=read('existing-source-mapping.json');audit=read('CORPUS-LEXICAL-AUDIT.json');baseline=read('BASELINE.json')
    cids={c['card_id'] for c in cs};sids={s['source_id'] for s in ss};by_card={c['card_id']:c for c in cs}
    expected_seeds=set(range(1,190));catalog=json.loads((ROOT/'skills/photo-prompt-image-generator/assets/photo_candidate_slot_catalog.json').read_text())['slot_catalog']
    check('189_unique_recovered_rows',len(seeds)==189 and {s['seed_id'] for s in seeds}==expected_seeds)
    check('189_complete_rows_with_browser_supplement',len(seeds)==189 and all(s['reference_row_complete'] for s in seeds) and read('REFERENCE-BROWSER-SUPPLEMENT.json')['total_data_rows']==189)
    check('bounded_reference_notice',read('REFERENCE-THREAD-BOUNDED.json')['truncated'] is True and len(read('REFERENCE-THREAD-BOUNDED.json')['answer_text'])==20000)
    check('189_routes_without_automatic_activation',len(routes)==189 and {r['seed_id'] for r in routes}==expected_seeds and all(not r['automatic_hard_activation'] for r in routes))
    check('route_source_references_exist',all(set(r['related_source_ids'])<=sids for r in routes))
    check('reference_kinds_reconcile',sum(s['kind']=='authored_combination' for s in seeds)==8 and sum(s['kind']=='reference_work' for s in seeds)==8 and sum(s['kind']=='combination_axis' for s in seeds)==3 and len(seeds)-19==170)
    check('routes_have_valid_cards',all(r['optional_visual_card_ids'] or r['context_card_ids'] for r in routes) and all(set(r['optional_visual_card_ids']+r['context_card_ids'])<=cids for r in routes))
    check('61_unique_sources',len(ss)==len(sids)==61 and all(s['url'].startswith('https://') and s['read_scope'] and s['limits_ko'] and s['supports_ko'] for s in ss))
    check('108_unique_cards',len(cs)==len(cids)==108)
    check('all_source_and_seed_references_exist',all(set(c['source_ids'])<=sids and set(c['reference_seed_ids'])<=expected_seeds for c in cs))
    check('all_slots_exist_current_catalog',all(set(c['proposed_slots'])<=set(catalog) for c in cs))
    check('all_cards_have_route',{c for r in routes for c in r['optional_visual_card_ids']+r['context_card_ids']}==cids)
    check('source_links_not_canonical_design_claims',all(c['source_support_scope']=='concept_or_material_boundary; exact arrangement is newly authored' for c in cs))
    context=[c for c in cs if c['observability']=='context'];visible=[c for c in cs if c['observability']!='context']
    check('22_context_cards_no_positive_graphs',len(context)==22 and all(not c['owners'] and not c['relations'] and not c['gates'] for c in context))
    check('86_visible_cards_with_bilingual_proposals',len(visible)==86 and all(c['proposal_en'] and c['proposal_ko'] and c['confusion_boundary_ko'] and c['claim_limit_ko'] for c in cs))
    check('graphs_have_existing_distinct_endpoints',all(r['from'] in c['owners'] and r['to'] in c['owners'] and r['from']!=r['to'] for c in visible for r in c['relations']))
    check('every_owner_participates',all(set(c['owners'])=={x for r in c['relations'] for x in (r['from'],r['to'])} for c in visible))
    gates=[g for c in visible for g in c['gates']]
    check('252_unique_gates',len(gates)==len({g['gate_id'] for g in gates})==252)
    check('gate_relation_bijection',all([g['required_relation'] for g in c['gates']]==c['relations'] for c in visible))
    check('strict_unobservable_partial_and_not_run',all(g['both_endpoints_required'] and g['owner_continuity_required'] and g['partial_is_fail'] and g['unobservable_status']=='UNOBSERVABLE_NOT_PASS' and g['pixel_status']=='NOT_RUN' for g in gates))
    check('86_drafts_exact_visible_card_set',len(ds)==86 and {d['card_id'] for d in ds}=={c['card_id'] for c in visible})
    check('draft_hashes_and_text_binding',all(d['card_sha256']==sha(canonical(by_card[d['card_id']])) and d['proposal_en']==by_card[d['card_id']]['proposal_en'] and d['proposal_ko']==by_card[d['card_id']]['proposal_ko'] for d in ds))
    check('research_not_native_or_runtime_approved',all(d['candidate_id'] is None and d['realization_id'] is None and not d['native_approval'] and not d['source_is_executable'] and d['runtime_registration']=='none' for d in ds) and all(not c['native_approval'] and not c['automatic_hard_activation'] for c in cs))
    check('28_full_source_snapshots',len(mapping)==len({m['candidate_id'] for m in mapping})==28 and all(m['record']['id']==m['candidate_id'] and m['record_sha256']==sha(canonical(m['record'])) and 'bindings' in m for m in mapping))
    check('mapping_refs_and_no_native_rank_claim',all(set(m['related_cards'])<=cids and m['actual_rank'] is None and m['native_source_qualification']=='NOT_RUN' for m in mapping))
    with (HERE/'EVALUATION-CASES.tsv').open() as f:es=list(csv.DictReader(f,delimiter='\t'))
    check('88_unique_bilingual_development_cases',len(es)==len({e['case_id'] for e in es})==88 and all(e['query_ko'] and e['query_en'] and e['required_evidence'] and e['forbidden_inference'] for e in es))
    check('cohorts_36_26_12_14',dict(collections.Counter(e['cohort'] for e in es))=={'development':36,'boundary':26,'ordinary':12,'nonvisual':14})
    check('evaluation_refs_and_not_run',all(set(e['target_cards'].split(','))<=cids and set(e['slots'].split(','))<=set(catalog) and e['execution_status']=='NOT_RUN' and e['gold_cid_rid']=='PENDING_SOURCE_ADJUDICATION' for e in es))
    check('lexical_count_reconciles',sum(audit['record_kinds'].values())==audit['candidate_count'] and audit['positive_count']+audit['record_kinds']['diagnostic']==audit['candidate_count'])
    check('no_drift_during_corpus_snapshot',not audit['changed_during_read'])
    broken=[]
    for p in HERE.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if not target.startswith(('https:','http:','#')) and not (p.parent/target.split('#')[0]).exists() and target not in {'VALIDATION.json','SHA256SUMS'}:broken.append([p.name,target])
    check('local_markdown_links_resolve',not broken)
    drift=[]
    for path,h in baseline['protected_tracked_sha256'].items():
        p=ROOT/path
        if not p.is_file() or sha(p.read_bytes())!=h:drift.append(path)
    module_drift=[p for p,h in audit['source_module_sha256'].items() if not (ROOT/'skills/photo-prompt-image-generator/assets'/p).is_file() or sha((ROOT/'skills/photo-prompt-image-generator/assets'/p).read_bytes())!=h]
    manifest_drift=sha((ROOT/'skills/photo-prompt-image-generator/assets/photo_candidate_corpus_manifest.json').read_bytes())!=audit['source_manifest_sha256']
    current_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    drift_data={'tracked_changed_since_research_start':drift,'source_modules_changed_since_audit':module_drift,'source_manifest_changed_since_audit':manifest_drift,'head_changed':current_head!=baseline['head'],'baseline_head':baseline['head'],'observed_head':current_head}
    result={'status':'pass' if not errors else 'fail','scope':'research integrity only; no runtime source/native qualification, retrieval or pixel verification','checks':checks,'errors':errors,'broken_links':broken,'counts':{'reference_rows':189,'complete_reference_rows':189,'semantic_cards':len(cs),'candidate_drafts':len(ds),'context_cards':len(context),'relation_gates':len(gates),'sources':len(ss),'existing_snapshots':len(mapping),'evaluation_cases':len(es),'bilingual_queries':2*len(es)},'protected_tracked_file_count':len(baseline['protected_tracked_sha256']),'source_drift':drift_data,'adoption_rebaseline_required':bool(drift or module_drift or manifest_drift or current_head!=baseline['head']),'not_run':['runtime_registration','source_native_qualification','index_build_publish','embedding','retrieval','image_generation','pixel_evaluation','installation_activation','user_acceptance','commit_push']}
    (HERE/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    files=sorted(p for p in HERE.iterdir() if p.is_file() and p.name!='SHA256SUMS')
    (HERE/'SHA256SUMS').write_text(''.join(sha(p.read_bytes())+'  '+p.name+'\n' for p in files))
    print(json.dumps({'status':result['status'],'checks':len(checks),'errors':errors,'source_drift':drift_data,'counts':result['counts']},ensure_ascii=False))
    return 1 if errors else 0
if __name__=='__main__':sys.exit(main())
