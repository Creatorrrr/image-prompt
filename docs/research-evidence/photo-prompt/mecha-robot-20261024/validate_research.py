"""Research integrity audit only. This is not runtime/native/pixel qualification."""
import hashlib,json
from pathlib import Path
from collections import Counter

P=Path(__file__).resolve().parent
ROOT=P.parents[3]
def read(name):return json.loads((P/name).read_text())
cards=read('semantic-cards.json')['cards']
drafts=read('candidate-drafts.json')['drafts']
terms=read('term-coverage.json')
contexts=read('context-boundaries.json')['contexts']
sources=read('source-registry.json')['sources']
slots=read('slot-proposals.json')
queries=read('retrieval-regression-plan.json')['cases']
cid={c['id']:c for c in cards};nid={n['id'] for n in contexts};sid={s['id'] for s in sources}
checks=[]
def check(name,ok,detail=''):
    checks.append({'name':name,'pass':bool(ok),'detail':detail})
check('unique_card_ids',len(cid)==len(cards))
check('original_table_322_and_extra_prose_one',len(terms['terms'])==323 and sum(len(s['terms']) for s in terms['sections'])==322)
expected=[15,14,18,18,20,14,21,19,14,14,23,15,24,16,16,18,19,16,8]
check('all_19_browser_section_counts',expected==[len(s['terms']) for s in terms['sections']])
check('term_routes_resolve',all(set(t['card_refs'])<=set(cid) and set(t['context_refs'])<=nid for t in terms['terms']))
check('no_term_equivalence_or_activation',all(t['equivalence'] is False and t['automatic_activation'] is False for t in terms['terms']))
check('source_references_resolve',all(set(c['source_ids'])<=sid for c in cards+contexts))
check('complete_bilingual_card_drafts',all(c['proposal_en'].strip() and c['proposal_ko'].strip() and c['claim_limit_ko'] and c['confusion_boundaries_ko'] for c in cards))
check('owner_relation_endpoints_resolve',all(e['from'] in c['owners'] and e['to'] in c['owners'] for c in cards for e in c['directed_relations']))
check('relation_gates_complete',all(len(c['render_gates'])==len(c['directed_relations'])+1 for c in cards))
check('no_research_native_or_runtime_approval',all(c['native_approval'] is False and c['runtime_registration'] is False and c['pixel_status']=='NOT_RUN' for c in cards))
check('context_excluded_from_positive_retrieval',all(n['positive_retrieval'] is False and n['classification_authority'] is False for n in contexts))
check('drafts_preserve_complete_card_languages_and_graphs',len(drafts)==len(cards) and all(d['content']=={'en':cid[d['card_id']]['proposal_en'],'ko':cid[d['card_id']]['proposal_ko']} and d['planned_owner_graph']['relations']==cid[d['card_id']]['directed_relations'] for d in drafts))
catalog_path=ROOT/'skills/photo-prompt-image-generator/assets/photo_candidate_slot_catalog.json'
catalog=json.loads(catalog_path.read_text())['slot_catalog']
check('all_proposed_slots_are_actual_catalog_ids',all(s in catalog for c in cards for s in c['proposed_slots']))
check('slot_catalog_snapshot_current',slots['catalog_sha256']==hashlib.sha256(catalog_path.read_bytes()).hexdigest())
check('slot_proposals_are_unapproved',all(p['status']=='manual_semantic_fit_review_pending' for p in slots['proposals']))
check('48_bilingual_queries_and_12_controls',Counter(q['kind'] for q in queries)=={'natural_query_pair':48,'negative_or_scope_control':12})
check('query_references_resolve_and_not_passed',all(set(q['expected_optional_card_refs'])<=set(cid) and q['pass_claim'] is False and q['installed_retrieval_status']=='NOT_RUN' for q in queries))
check('service_cable_both_endpoints',all(any(e['from']=='cable' and e['predicate']=='joins' and e['to']==end for e in cid['D01']['directed_relations']) for end in ['wall_socket','receptacle']))
check('both_controls_and_both_pedals_preserved',len(cid['C03']['directed_relations'])==4 and {e['to'] for e in cid['C03']['directed_relations']}=={'left_stick','right_stick','left_pedal','right_pedal'})
check('mechanical_hand_owner_not_human_palm',any(e=={'from':'robot_fingers','predicate':'part_of','to':'robot_hand'} for e in cid['H07']['directed_relations']))
check('explicit_holds_retained',{d['card_id'] for d in drafts if d['planned_action']=='hold_for_source_plate_review'}=={'G03','K06'})

before=read('protected-state.before.json')
changes=[]
for rel,h in before['hashes'].items():
    p=ROOT/rel
    now=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
    if now!=h:changes.append({'path':rel,'before':h,'after':now})
protection={'scope':before['scope'],'files_compared':len(before['hashes']),'changed_files':changes,'interpretation':'This research writes only inside its own directory. Concurrent changes, if any, are reported and never restored.'}
save=lambda n,v:(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
save('protected-state.after.json',protection)
result={'schema':'mecha-research-validation/v1','status':'PASS' if all(c['pass'] for c in checks) else 'FAIL','scope':'research artifact integrity and reference closure only','checks':checks,'counts':{'original_table_rows':322,'extra_prose_terms':1,'visual_cards':len(cards),'context_boundaries':len(contexts),'candidate_drafts':len(drafts),'directed_relations':sum(len(c['directed_relations']) for c in cards),'render_gate_definitions':sum(len(c['render_gates']) for c in cards),'proposed_slots':len(slots['slots']),'slot_proposals':len(slots['proposals']),'natural_query_pairs':48,'controls':12,'sources':len(sources),'partial_component_routes':sum(bool(t['card_refs']) for t in terms['terms']),'context_only_routes':sum(not t['card_refs'] for t in terms['terms'])},'source_access_counts':dict(Counter(s['access'] for s in sources)),'protected_snapshot':{'files_compared':len(before['hashes']),'changed_count':len(changes)},'not_established':['independent bilingual approval','full-corpus semantic deduplication','native source qualification','approved slot fit','operating registration','installed search exposure','prompt transport','saved pixels','requester acceptance']}
save('validation-results.json',result)
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(0 if result['status']=='PASS' else 1)
