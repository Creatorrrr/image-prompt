#!/usr/bin/env python3
"""Validate research integrity and explicit proof limits. No external calls."""
import collections,hashlib,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def get(n):return json.loads((HERE/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
errors=[];checks={}
def check(name,condition):
    checks[name]=bool(condition)
    if not condition:errors.append(name)

cards=get('semantic-cards.json')['cards'];drafts=get('candidate-drafts.json')['drafts'];routes=get('keyword-routes.json')['routes'];contexts=get('context-records.json')['records'];sources=get('sources.json')['sources'];cases=get('evaluation-cases.json')['cases'];counts=get('COUNTS.json')
ci={c['card_id']:c for c in cards};si={s['source_id']:s for s in sources};di={c['context_id']:c for c in contexts}
slots=get('../../../../skills/photo-prompt-image-generator/assets/photo_candidate_slot_catalog.json')['slot_catalog']
check('200_distinct_contiguous_source_routes',[r['source_number'] for r in routes]==list(range(1,201)))
check('exact_card_and_draft_counts',len(cards)==64 and len(drafts)==61 and len(ci)==64)
check('context_records_and_source_counts',len(contexts)==20 and len(sources)==36)
check('all_source_contexts_cover_all_keywords',set().union(*(set(x['seed_ids']) for x in contexts))==set(range(1,201)))
check('all_routes_have_valid_cross_references',all(set(r['visual_card_ids'])<=ci.keys() and set(r['context_ids'])<=di.keys() and r['context_ids'] and r['automatic_hard_profile'] is False for r in routes))
check('valid_source_references',all(set(x['source_ids'])<=si.keys() and all(si[s]['access']!='inaccessible' for s in x['source_ids']) for x in cards+contexts))
check('valid_provisional_slots',all(set(c['proposed_slots'])<=slots.keys() for c in cards))
check('all_graph_endpoints_owned',all(r['from'] in c['owners'] and r['to'] in c['owners'] for c in cards for r in c['directed_relations']))
check('relation_graphs_nontrivial',all(len(c['owners'])>=3 and len(c['directed_relations'])>=2 for c in cards))
check('every_relation_has_matching_unexecuted_gate',all([g['required_visible_relation'] for g in c['review_gates']]==c['directed_relations'] and all(g['status']=='NOT_RUN' and g['partial_is_fail'] is True and g['unobservable_is_pass'] is False for g in c['review_gates']) for c in cards))
check('every_card_has_limits_and_bilingual_proposal',all(c['claim_limit'] and c['nearest_confusion'] and c['proposal_en'] and c['proposal_ko'] and c['native_approval'] is False for c in cards))
check('drafts_are_not_native_candidates',all(d['candidate_id'] is None and d['realization_id'] is None and d['native_approval'] is False and d['stage']=='research_draft_not_loader_input' for d in drafts))
check('drafts_retain_complete_bilingual_and_graph_meaning',all(d['en']==ci[d['card_id']]['proposal_en'] and d['ko']==ci[d['card_id']]['proposal_ko'] and d['owners']==ci[d['card_id']]['owners'] and d['relations']==ci[d['card_id']]['directed_relations'] for d in drafts))
check('withheld_cues_are_not_positive_drafts',not {'V41','V47','V61'}&{d['card_id'] for d in drafts})
check('iconography_remains_deferred',next(d for d in drafts if d['card_id']=='V45')['adoption']=='defer_iconography_review')
check('physical_projection_drafts_remain_deferred',all(next(d for d in drafts if d['card_id']==cid)['adoption']=='defer_physical_or_projection_review' for cid in ['V56','V57']))
matrix=get('adoption-matrix.json')['records']
check('all_cards_have_provisional_adoption_decisions',{r['card_id'] for r in matrix}==ci.keys() and all(r['proposed_decision'] in {'reuse','refine','new','context','defer'} and r['native_approval'] is False for r in matrix))
check('speculative_geometry_registration_deferred',all(next(r for r in matrix if r['card_id']==cid)['proposed_decision']=='defer' for cid in ['V45','V56','V57']))
check('context_diagnostics_not_material_authority',all(c['material_retrieval'] is False and c['native_approval'] is False for c in contexts))
check('200_raw_original_labels_preserved',len((HERE/'reference-keywords.txt').read_text().splitlines())==180 and all(r['en'] and r['ko'] for r in routes))
check('148_cases_and_296_queries_unexecuted',len(cases)==148 and all(c['query_en'] and c['query_ko'] and c['execution']=='NOT_RUN' and c['holdout'] is False for c in cases))
check('evaluation_splits',collections.Counter(c['split'] for c in cases)==dict(development_exact_realization=64,natural=32,boundary=24,context=12,control=16))
check('source_access_limits_match',sum(s['access']=='search_excerpt_only' for s in sources)==5 and sum(s['access']=='inaccessible' for s in sources)==2)
check('counts_match',counts['relation_gates']==sum(len(c['review_gates']) for c in cards)==211 and counts['sources']==len(sources) and counts['candidate_drafts']==len(drafts))
check('no_retrieval_images_or_runtime_adoption_claim',all(counts[k]==0 for k in ['image_calls','retrieval_calls','operating_source_writes']) and counts['implementation_status']=='NOT_RUN')
audit=get('CORPUS-AUDIT.json')
check('corpus_snapshot_stable_during_read',not audit['changes_during_read'] and not audit['manifest_changed'] and not audit['duplicate_candidate_ids'])
snap=get('existing-source-snapshots.json')
check('source_snapshot_hashes',all(hashlib.sha256(json.dumps(r['record'],sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()==r['canonical_sha256'] for r in snap))
broken=[]
for p in HERE.glob('*.md'):
    for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if '://' in link or link.startswith('#'):continue
        target=p.parent/link.split('#')[0]
        if target.parent==HERE and target.name in {'VALIDATION.json','SHA256SUMS'}:continue
        if not target.exists(): broken.append((p.name,link))
check('local_markdown_links_resolve',not broken)
check('runtime_read_only_check_passes',get('RUNTIME-CHECK.json').get('status')=='pass' and get('RUNTIME-CHECK.json').get('image_calls')==0 and get('RUNTIME-CHECK.json').get('source_writes')==0)
pres=get('PRESERVATION.json')
check('head_unchanged_during_research',pres['head_before']==pres['head_after'])

report=dict(status='pass' if not errors else 'fail',checks=checks,failed=errors,broken_links=broken,counts=dict(keywords=len(routes),cards=len(cards),drafts=len(drafts),contexts=len(contexts),sources=len(sources),relation_gates=counts['relation_gates'],evaluation_cases=len(cases),bilingual_queries=len(cases)*2,source_snapshots=len(snap)),observed_protected_drift=pres['changes'],proof_scope='research integrity only; no operating source qualification, material retrieval, image generation, native pixels, artistic improvement or user acceptance',required_followup='rebaseline current source and installed generation before applying; inspect reported concurrent drift')
(HERE/'VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))
if errors: raise SystemExit(1)
files=sorted(p for p in HERE.iterdir() if p.is_file() and p.name!='SHA256SUMS')
(HERE/'SHA256SUMS').write_text(''.join(f'{sha(p)}  {p.name}\n' for p in files))
