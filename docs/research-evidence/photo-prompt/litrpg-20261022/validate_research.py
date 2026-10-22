"""Research integrity and preservation checks; no runtime/pixel qualification."""
import collections, hashlib, json
from pathlib import Path
from urllib.parse import urlparse
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def read(n):return json.loads((HERE/n).read_text())
def sha(raw):return hashlib.sha256(raw).hexdigest()
errors=[];checks={}
def check(k,ok,detail=None):
 checks[k]={'passed':bool(ok),'detail':detail}
 if not ok:errors.append(k)
cards=read('semantic-cards.json');sources=read('sources.json');routes=read('keyword-routes.json');drafts=read('candidate-drafts.json');cases=read('evaluation-cases.json');counts=read('COUNTS.json');ref=read('reference-register.json')
cardmap={c['id']:c for c in cards};sids={s['id'] for s in sources};rids={r['id'] for r in routes}
check('unique_identifiers',len(cardmap)==len(cards) and len(sids)==len(sources) and len(rids)==len(routes) and len({d['id'] for d in drafts})==len(drafts))
check('reference_table_counts',[len(t['labels']) for t in ref['tables']]==ref['table_counts'])
check('reference_coverage',len(routes)==sum(ref['table_counts'])==297 and sum(r['kind']=='term' for r in routes)==255)
check('exact_transcribed_labels',all(r['label']==ref['tables'][r['table']]['labels'][r['row']-1] for r in routes))
check('all_routes_resolve',all(r['card_ids'] and set(r['card_ids'])<=set(cardmap) for r in routes))
check('all_cards_discoverable',all(c['keyword_route_ids'] and set(c['keyword_route_ids'])<=rids for c in cards))
check('source_references_resolve',all(set(c['source_ids'])<=sids and c['source_ids'] for c in cards))
check('sources_have_access_scope',all(s['access'] and s['supported_claim_and_limit_ko'] and urlparse(s['url']).scheme=='https' and s['checked_on_kst']=='2026-10-22' for s in sources))
check('blocked_sources_not_positive_authority',all(not set(c['source_ids'])&{'S23','S24','S25','S26','S27'} for c in cards))
visual=[c for c in cards if c['evidence_mode'] in ('still','displayed')]
check('visual_context_separation',len(visual)==len(drafts)==60 and all(not c['owners'] and not c['relations'] and not c['pixel_gates'] and c['context_requirement'] for c in cards if c['evidence_mode'] in ('context','sequence')))
check('research_counts',counts['semantic_cards']==len(cards)==78 and counts['routes']==len(routes) and counts['sources']==len(sources))
bad_endpoints=[];unused=[]
for c in visual:
 endpoints={r[k] for r in c['relations'] for k in ('subject','object')}
 if not endpoints<=set(c['owners']):bad_endpoints.append(c['id'])
 if set(c['owners'])-endpoints:unused.append(c['id'])
check('relation_endpoints_declared',not bad_endpoints,bad_endpoints)
check('every_visual_owner_connected',not unused,unused)
catalog=json.loads((ROOT/'skills/photo-prompt-image-generator/assets/photo_candidate_slot_catalog.json').read_text())['slot_catalog']
check('proposed_slots_exist',all(c['proposed_slots'] and set(c['proposed_slots'])<=set(catalog) for c in visual))
check('drafts_preserve_whole_research_unit',all(d['content']=={'en':cardmap[d['card_id']]['phrase_en'],'ko':cardmap[d['card_id']]['phrase_ko']} and d['owners']==cardmap[d['card_id']]['owners'] and d['relations']==cardmap[d['card_id']]['relations'] and d['source_ids']==cardmap[d['card_id']]['source_ids'] for d in drafts))
check('no_duplicate_bilingual_drafts',len({(d['content']['en'],d['content']['ko']) for d in drafts})==len(drafts))
check('research_not_runtime_approval',all(c['native_approval'] is False and c['failure_policy']=='partial_is_fail; UNOBSERVABLE_NOT_PASS' for c in cards) and all(d['native_approval'] is False and d['index_registered'] is False for d in drafts) and all(r['advisory_only'] and not r['auto_obligation'] for r in routes))
case_counts=dict(collections.Counter(c['set'] for c in cases))
check('evaluation_matrix',case_counts=={'development_positive':12,'development_near_negative':12,'bilingual_paraphrase':12,'ordinary_control':6,'context_boundary':6},case_counts)
check('evaluation_card_references',all(set(c.get('expected_cards',[])+c.get('confusable_cards',[]))<=set(cardmap) for c in cases))
audit=read('CORPUS-AUDIT.json')
check('audit_read_stable',not audit['changes_during_read'] and not audit['manifest_changed_during_read'] and not audit['duplicate_ids'])
check('source_audit_not_search',audit['runtime_search_performed'] is False)
baseline=read('BASELINE.json');drift=[]
for f,h in baseline['skill_file_sha256'].items():
 p=ROOT/f
 if not p.is_file() or sha(p.read_bytes())!=h:drift.append(f)
drift_report={'checked_files':len(baseline['skill_file_sha256']),'matching_files':len(baseline['skill_file_sha256'])-len(drift),'changed':[{'path':f,'before_sha256':baseline['skill_file_sha256'][f],'observed_sha256':sha((ROOT/f).read_bytes()) if (ROOT/f).is_file() else None} for f in drift],'all_snapshotted_files_unchanged':not drift,'interpretation':'Concurrent workspace changes observed. This task writes only the litrpg research directory; no restoration or edit of these operating paths was performed. Rebase source comparisons before implementation.','excluded':'generated search/index shards and embedding directories were not snapshotted'}
(HERE/'WORKSPACE-DRIFT.json').write_text(json.dumps(drift_report,ensure_ascii=False,indent=2)+'\n')
check('baseline_drift_observation_recorded',all((ROOT/f).is_file() for f in drift),drift_report)
check('declared_scope',counts['operating_data_modified'] is False and counts['index_built'] is False and counts['image_calls']==0)
required=['RESEARCH.md','IMPLEMENTATION-PLAN.md','CORPUS-FINDINGS.md','SOURCES.md','KEYWORD-ATLAS.md','VISUAL-CARDS.md','CANDIDATE-ATLAS.md','EVALUATION-PLAN.md','README.md','reviewed-litrpg-sources.json']
check('deliverables_present',all((HERE/f).is_file() for f in required))
result=dict(status='pass' if not errors else 'fail',checked_on_kst='2026-10-22',checks=checks,errors=errors,workspace_drift_observed=bool(drift),all_snapshotted_operating_files_unchanged=not drift,proof_scope='Research integrity and explicit baseline-drift accounting only. Does not claim unchanged operating files when drift exists. No web exhaustiveness, runtime exposure, native qualification, image quality or requester acceptance proof.',counts=counts)
(HERE/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
members=sorted(p for p in HERE.iterdir() if p.is_file() and p.name!='SHA256SUMS')
(HERE/'SHA256SUMS').write_text(''.join(f'{sha(p.read_bytes())}  {p.name}\n' for p in members))
print(json.dumps({'status':result['status'],'checks':len(checks),'errors':errors,'skill_drift':drift,'package_members':len(members)},ensure_ascii=False))
raise SystemExit(bool(errors))
