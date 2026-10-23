"""Research structure validation only. Does not validate natural-language truth."""
from pathlib import Path
import collections, csv, hashlib, json, re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]

def read(n):return json.loads((HERE/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    failures=[];checks=[]
    def check(name,condition):
        checks.append({'check':name,'pass':bool(condition)})
        if not condition:failures.append(name)
    seed=read('seed-keywords.json');rows=read('conversation-table-rows.json')
    expected=[r['cells'][:2] for r in rows if r['cells'][0] not in ['용어','방향']][:-9]
    check('all_325_seed_rows_preserved',len(seed)==325 and [[s['term'],s['seed_description']] for s in seed]==expected)
    cards=read('semantic-cards.json');contexts=read('context-distinctions.json');routes=read('keyword-routes.json');sources=read('sources.json');holds=read('holds.json')
    ids=lambda rs:{r['id'] for r in rs}
    ci,ni,ki,si,hi=map(ids,[cards,contexts,seed,sources,holds])
    check('unique_ids',all(len(ids(x))==len(x) for x in [cards,contexts,seed,sources,holds,routes]))
    check('route_set_exactly_seed_set',ids(routes)==ki)
    check('each_route_has_explicit_disposition',all(r['optional_component_card_ids'] or r['context_card_ids'] or r['hold_ids'] for r in routes))
    check('all_route_refs_exist',all(set(r['optional_component_card_ids'])<=ci and set(r['context_card_ids'])<=ni and set(r['hold_ids'])<=hi for r in routes))
    check('card_seed_and_source_refs_exist',all(set(c['seed_ids'])<=ki and set(c['source_ids'])<=si for c in cards+contexts))
    check('no_whole_compound_equivalence_or_authority',all(not r['equivalence'] and not r['whole_compound_term_qualified'] and not r['adoption_authority'] for r in routes))
    check('120_complete_bilingual_visual_drafts',len(cards)==120 and all(c['phrase_en'].strip().endswith('.') and c['phrase_ko'].strip().endswith('다.') for c in cards))
    check('360_explicit_observations',sum(len(c['observable_components']) for c in cards)==360)
    check('all_owner_literals_bound_to_card',all(c['owner_relation_contract']['complete_proposition_en']==c['phrase_en'] and c['owner_relation_contract']['complete_proposition_ko']==c['phrase_ko'] for c in cards))
    check('all_cards_research_only',all(not c['runtime_importable'] and not c['native_approval'] and c['native_qualification']=='not_attempted' for c in cards))
    check('all_contexts_positive_excluded',len(contexts)==45 and all(not c['positive_retrieval'] and not c['runtime_importable'] for c in contexts))
    check('unverified_high_stakes_contexts_do_not_borrow_sources',all(not c['source_ids'] for c in contexts if c['id'] in ['N33','N40','N41','N42']))
    check('held_terms_retained',all(set(h['seed_ids'])<=ki and h['reason'] and h['next'] for h in holds))
    check('source_scopes_and_access_limits_present',len(sources)==27 and all(s['verified_scope_ko'] and s['limits_ko'] and s['access_status'] and s['remote_content_hash'] is None for s in sources))
    proposals=read('candidate-drafts.json')
    check('proposals_cannot_import_as_native',proposals['not_native_corpus_schema'] and not proposals['runtime_importable'] and len(proposals['proposals'])==120 and all(p['native_candidate_id'] is None and not p['native_approval'] for p in proposals['proposals']))
    ev=read('evaluation-cases.json')
    check('76_development_cases_not_executed',len(ev['cases'])==76 and all(c['split']=='development' and c['execution_status']=='not_run' for c in ev['cases']))
    check('evaluation_refs_exist',all(set(c.get('context_ids',[]))<=ni and set(c.get('relevant_card_ids',[])+c.get('insufficient_static_proxy_card_ids',[]))<=ci for c in ev['cases']))
    assets=ROOT/'skills/photo-prompt-image-generator/assets'
    manifest=json.loads((assets/'photo_candidate_corpus_manifest.json').read_text())
    slots=set()
    for m in manifest['modules']:
        if m['kind']=='slot_bindings':
            slots|={b['slot_id'] for b in json.loads((assets/m['file']).read_text())['slot_bindings'].values()}
    check('suggested_slot_names_exist',all(set(c['proposed_slots'])<=slots for c in cards))
    audit=read('CORPUS-AUDIT.json');changed=[n for n,h in audit['source_hashes'].items() if sha(assets/n)!=h]
    check('working_source_hashes_match_baseline',not changed)
    links=[]
    for file in HERE.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',file.read_text()):
            if not re.match(r'\w+://',target) and not target.startswith('#'):
                links.append((file.name,target,(file.parent/target.split('#')[0]).exists()))
    check('local_markdown_links_resolve',all(x[2] for x in links))
    summary=read('SUMMARY.json')
    check('published_summary_counts_match',summary['visual_cards']==len(cards) and summary['context_distinctions']==len(contexts) and summary['keyword_routes']==len(routes) and summary['proposed_slot_links']==sum(len(c['proposed_slots']) for c in cards))
    result={'schema':'idol-research-structure-validation/v1','status':'pass' if not failures else 'fail',
            'checks':checks,'failures':failures,'source_changes_since_baseline':changed,
            'evidence_boundary':'Structure/reference/status validation only. No semantic truth, exact visual specimen, native qualification, retrieval, image-quality or user-acceptance claim.',
            'not_run':['native source qualification','installed retrieval evaluation','independent holdout','image generation','saved pixel review'],
            'evaluations_authored':len(ev['cases']),'image_calls':0}
    (HERE/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'checks':len(checks),'failures':failures,'source_changes':changed},ensure_ascii=False))
    return bool(failures)

if __name__=='__main__':raise SystemExit(main())
