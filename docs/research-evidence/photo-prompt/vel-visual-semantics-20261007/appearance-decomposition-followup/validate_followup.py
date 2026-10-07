#!/usr/bin/env python3
"""Validate source fidelity and research structure, never runtime or pixels."""
import collections, datetime, hashlib, json, re, subprocess
from pathlib import Path
from urllib.parse import urlparse, unquote
OUT=Path(__file__).resolve().parent
BASE=OUT.parent
ROOT=OUT.parents[4]
def read(name):return json.loads((OUT/name).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,ok,detail=None):checks.append({'name':name,'pass':bool(ok),'detail':detail})
src=read('SOURCE-DECOMPOSITION.json')
old=json.loads((BASE/'SOURCE-KEYWORDS.json').read_text())
receipt=read('SOURCE-DOWNLOAD-RECEIPT.json')
units=read('SEMANTIC-UNITS.json')['units']
cards=read('RESEARCH-CARDS.json')['cards']
drafts=read('CANDIDATE-DRAFTS.json')['drafts']
mapping=read('RUNTIME-MAPPING.json')['mapping']
inv=read('CURRENT-INVENTORY.json')
sources=read('SOURCES.json')['sources']
stats=read('RESEARCH-SUMMARY.json')
oldcards={c['id'] for c in json.loads((BASE/'RESEARCH-PROPOSALS.json').read_text())['cards']}
ids={e['id'] for e in src['entries']}
cids={c['id'] for c in cards}
sids={s['id'] for s in sources}
check('full217_and22categories',len(ids)==len(src['entries'])==217 and len({e['category'] for e in src['entries']})==22)
check('canonical_K_order',[e['id'] for e in src['entries']]==[f'K{n:03}' for n in range(1,218)])
check('download_JSON_hash_and_bytes',sha(OUT/'SOURCE-DECOMPOSITION.json')==receipt['sha256'] and (OUT/'SOURCE-DECOMPOSITION.json').stat().st_size==receipt['bytes'])
check('download_MD_hash_and_bytes',sha(OUT/'SOURCE-DECOMPOSITION.md')==receipt['markdown_attachment']['sha256'] and (OUT/'SOURCE-DECOMPOSITION.md').stat().st_size==receipt['markdown_attachment']['bytes'])
check('original_audit_hash',sha(BASE/'SOURCE-KEYWORDS.json')==src['summary']['source_audit_sha256']==receipt['source_audit_sha256'])
fieldmap={'id':'id','category':'category','phrase':'original_phrase','polarity':'original_polarity','meaning_ko':'original_meaning_ko','source_id':'source_id','source_kind':'source_kind','age_context':'age_context'}
drift=[{'id':o['id'],'field':a} for o,n in zip(old['entries'],src['entries']) for a,b in fieldmap.items() if o[a]!=n[b]]
check('eight_original_fields_preserved_all_rows',not drift,drift)
source_drift=[{'source_id':id,'field':k} for id,s in old['sources'].items() for k in ('title','kind','age','file_id') if s[k]!=src['sources'][id][k]]
check('19_original_source_metadata_preserved',len(src['sources'])==19 and not source_drift,source_drift)
check('polarity_counts',dict(collections.Counter(e['original_polarity'] for e in src['entries']))=={'긍정':100,'설명':97,'부정':20})
check('basis_counts',dict(collections.Counter(e['decomposition_basis'] for e in src['entries']))=={'직접 분해':128,'문맥 결합':36,'해석 예시':32,'제외 조건':20,'대상 조건':1})
check('units_keep_complete_decomposition_source',len(units)==217 and all(all(u[k]==v for k,v in s.items()) for s,u in zip(src['entries'],units)))
atoms=[a for u in units for a in u['visual_atoms']]
check('465_atoms_unique_preserved',len(atoms)==len({a['id'] for a in atoms})==465 and all([{k:a[k] for k in ('dimension_ko','description_ko')} for a in u['visual_atoms']]==s['visual_elements'] for s,u in zip(src['entries'],units)))
check('no_atom_hard_or_runtime_promotion',all(a['runtime_ready'] is False and a['is_hard_obligation'] is False for a in atoms))
check('28_cards_unique_and_scoped',len(cards)==len(cids)==28 and all(c['owner_scope'] and c['required_components_en'] and c['directed_relations'] and c['runtime_ready'] is False for c in cards))
check('card_keywords_priorcards_sources_slots_resolve',all(set(c['keyword_ids'])<=ids and set(c['prior_card_ids'])<=oldcards and set(c['research_source_ids'])<=sids and set(c['target_slots'])<=set(inv['slot_names']) for c in cards))
known=set(inv['entries'])|set(inv['profiles'])
unknown=sorted({k for c in cards for k in c['existing_ids_to_review'] if k not in known})
check('all_current_review_IDs_exist',not unknown,unknown)
check('217_rows_each_link_prior_plan',all(u['prior_card_ids'] and set(u['followup_card_ids'])<=cids for u in units))
check('192_extended_25_carried',sum(bool(u['followup_card_ids']) for u in units)==192 and sum(not u['followup_card_ids'] for u in units)==25)
check('source_case_negative_interpretation_authority_retained',all(u['adoption_policy'] and u['source_is_not_independent_observation'] and u['runtime_ready'] is False for u in units))
check('20_candidate_drafts_13new_7review',len(drafts)==20 and dict(collections.Counter(d['kind'] for d in drafts))=={'new_relation_trial':13,'extend_review':7} and all(d['runtime_ready'] is False and d['not_current_runtime_schema'] is True for d in drafts))
check('mapping_unexecuted_with_complete_effect_work',len(mapping)==20 and all(m['adapter_status']=='PROPOSED_NOT_RUN' and m['candidate_pack_exposure_proof'] is None and m['native_pixel_proof'] is None and m['required_adapter_work'] for m in mapping))
anchor_drift=[]
for m in mapping:
 for a in m['current_contract_anchors']:
  e=inv['entries'].get(a['example_id'],{}).get('entry',{})
  if a['affected_properties']!=e.get('affected_properties') or a['affected_dimensions']!=e.get('affected_dimensions',[]):anchor_drift.append(a['example_id'])
check('property_anchors_exact_native_snapshot',not anchor_drift,anchor_drift)
bundles=read('BUNDLE-DRAFTS.json')['bundles']
check('6_optional_menus',len(bundles)==6 and all(set(b['card_ids'])<=cids and b['required_all_members'] is False and b['runtime_ready'] is False for b in bundles))
corrections=read('FIDELITY-CORRECTIONS.json')['corrections']
check('46_review_notes_resolve',len(corrections)==len({r['keyword_id'] for r in corrections})==46 and all(r['keyword_id'] in ids for r in corrections))
check('11_new_12_inherited_sources',len(sources)==len(sids)==23 and sum(s['origin']=='additional_web_research' for s in sources)==11 and sum(s['origin']=='inherited_initial_research' for s in sources)==12)
check('URLs_and_new_source_access_limits',all(urlparse(s['url']).scheme=='https' for s in sources) and all(s.get('access_scope') and s.get('claim_limit_ko') for s in sources if s['origin']=='additional_web_research'))
reg=read('REGRESSION-PLAN.json')['cases']
check('193_future_regression_specs',len(reg)==len({c['id'] for c in reg})==193 and all(c['status']=='PROPOSED_NOT_RUN' for c in reg))
pix=read('PIXEL-QUALIFICATION-PLAN.json')
check('14_pixel_groups_5pilot_45planned_0actual',len(pix['groups'])==14 and sum(g['pilot'] for g in pix['groups'])==5 and pix['pilot_design']['planned_images']==45 and pix['pilot_design']['actual_images']==0)
check('zero_runtime_API_image_adoption_claims',all(stats[k]==0 for k in ('actual_generation_calls','live_pack_calls','embedding_calls','runtime_adoptions')) and inv['summary']['embedding_calls']==inv['summary']['live_pack_calls']==inv['summary']['generation_calls']==0)
check('manifest_and_native_counts',len(inv['manifest']['sources'])==inv['summary']['manifest_source_count']==100 and inv['summary']['slot_entry_count']==10518 and inv['summary']['profile_count']==2308)
baseline=read('BASELINE-SNAPSHOT.json')
active_drift=[p for p,h in baseline['hashes'].items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
inventory_drift=[p for p,h in inv['source_hashes'].items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
allowed_parent_changes={'README.md','RESEARCH.md','IMPLEMENTATION-PLAN.md'}
parent_drift=[p for p,h in baseline['existing_research_hashes'].items() if not (BASE/p).is_file() or sha(BASE/p)!=h]
check('original_research_data_preserved',set(parent_drift)<=allowed_parent_changes,parent_drift)
check('native_source_revision_still_matches_snapshot',not inventory_drift,inventory_drift)
check('protected_active_baseline_unchanged',not active_drift,active_drift)
missing=[]
for name in ('README.md','RESEARCH.md','IMPLEMENTATION-PLAN.md','SEMANTIC-CARDS.md','KEYWORD-CROSSWALK.md','SOURCES.md'):
 for target in re.findall(r'\]\(([^\)]+)\)',(OUT/name).read_text()):
  if urlparse(target).scheme or target.startswith('#'):continue
  target=unquote(target.split('#')[0])
  if target=='VALIDATION.json':continue
  if not (OUT/target).is_file():missing.append({'document':name,'target':target})
check('authored_markdown_local_links_resolve',not missing,missing)
thread=read('REFERENCED-CONVERSATION.json')
def message_text(i):return i.get('text') or '\n'.join(p.get('text','') for p in i.get('content',[]) if p.get('type')=='text')
check('followup_thread_and_complete_assistant_text',thread['thread']['id']==receipt['conversation_id'] and any('외형적인 특징' in message_text(i) for t in thread['turns'] for i in t['items']) and any('K214' in message_text(i) and 'K010' in message_text(i) and len(message_text(i))>18000 for t in thread['turns'] for i in t['items']))
result={'status':'PASS_RESEARCH_INTEGRITY' if all(c['pass'] for c in checks) else 'RESEARCH_VALIDATION_FAILED','checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'passed_checks':sum(c['pass'] for c in checks),'total_checks':len(checks),'protected_active_files':len(baseline['hashes']),'protected_active_drift':active_drift,'native_source_drift':inventory_drift,'intentional_parent_document_updates':parent_drift,'historical_initial_audit_drift_at_followup_start':baseline['historical_baseline_drift'],'head_at_followup_start':baseline['head'],'head_at_validation':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'counts':stats,'claim_boundary':'Research-source preservation and structure only. Runtime integration, pack exposure, image fidelity, causal improvement and user acceptance are not scored.'}
(OUT/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':result['status'],'checks':f"{result['passed_checks']}/{result['total_checks']}",'protected_active_drift':active_drift,'native_source_drift':inventory_drift,'intentional_parent_document_updates':parent_drift,'failed_checks':[c for c in checks if not c['pass']]},ensure_ascii=False,indent=2))
raise SystemExit(0 if all(c['pass'] for c in checks) else 1)
