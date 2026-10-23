"""Validate research integrity, not native/source/search/pixel qualification."""
from pathlib import Path
import collections, hashlib, json
BASE=Path(__file__).resolve().parent; ROOT=BASE.parents[3]
def read(name):return json.loads((BASE/name).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
errors=[]
def check(condition,message):
 if not condition:errors.append(message)
terms=read('conversation-keywords.json');routes=read('keyword-routes.json');cards=read('semantic-cards.json');drafts=read('candidate-drafts.json');sources=read('sources.json');cases=read('evaluation-cases.json');refs=read('reference-work-mapping.json');combos=read('combination-mapping.json');recovery=read('browser-supplement.json')
visual=cards['visual'];context=cards['context'];allcards=visual+context
ids={c['card_id'] for c in allcards};sids={s['source_id'] for s in sources};tids={t['seed_id'] for t in terms}
check(len(terms)==154 and len(tids)==154,'154 distinct original term rows required')
check(all(t['description_complete'] for t in terms),'partial descriptions remain')
check(recovery['browser_recovery_complete'] and sum(recovery['table_data_row_counts'])==179,'browser table accounting does not close')
check(len(visual)==64 and len(context)==29 and len(ids)==93,'unexpected card counts or duplicate ids')
check(len(drafts)==64 and len({d['draft_id'] for d in drafts})==64,'draft count or uniqueness mismatch')
check(len(sources)==47 and len(sids)==47,'source count or uniqueness mismatch')
check(len(refs)==19 and len(combos)==6,'all works/combinations required')
check(len(routes)==154 and {r['seed_id'] for r in routes}==tids,'keyword routes are incomplete')
for r in routes:
 check(bool(r['visual_card_ids'] or r['context_card_ids']),'unmapped seed '+r['seed_id'])
 check(set(r['visual_card_ids']+r['context_card_ids'])<=ids,'unknown route target '+r['seed_id'])
 check(r['activation']=='advisory_only','hard activation in keyword route')
for c in allcards:
 check(set(c['source_ids'])<=sids,'unknown source '+c['card_id'])
 check(set(c['seed_ids'])<=tids,'unknown seed '+c['card_id'])
 check(not c['native_approval'] and not c['automatic_hard_activation'],'unearned qualification '+c['card_id'])
for c in visual:
 check(c['proposal_en'].strip() and c['proposal_ko'].strip(),'missing bilingual prose '+c['card_id'])
 check(len(c['relations'])>=2,'insufficient relation description '+c['card_id'])
 for rel in c['relations']:
  check(rel['from'] in c['owners'] and rel['to'] in c['owners'],'unknown owner endpoint '+c['card_id'])
 check(len(c['gates'])==len(c['relations']),'gate/graph mismatch '+c['card_id'])
 check(all(g['partial_is_fail'] and g['both_endpoints_required'] and g['pixel_status']=='NOT_RUN' and g['unobservable_status']=='UNOBSERVABLE_NOT_PASS' for g in c['gates']),'invalid pixel status '+c['card_id'])
 check(c['confusion_boundary_ko'] and c['claim_limit_ko'],'missing boundary '+c['card_id'])
for c in context:check(not c['positive_retrieval'],'context admitted as positive '+c['card_id'])
for d in drafts:
 c=next(c for c in visual if c['card_id']==d['card_id'])
 check(d['content']['en']==c['proposal_en'] and d['content']['ko']==c['proposal_ko'],'draft semantic drift '+d['card_id'])
for r in refs+combos:check(set(r['card_ids'])<=ids,'unknown reference/combination card '+str(r))
for e in cases:
 check(e['query_en'].strip() and e['query_ko'].strip(),'missing query text '+e['case_id'])
 check(set(e['expected_card_ids'])<=ids,'unknown evaluation target '+e['case_id'])
 check(e['retrieval_status']=='NOT_RUN' and e['pixel_status']=='NOT_RUN','unearned evaluation result '+e['case_id'])
check(len(cases)==113 and len({c['case_id'] for c in cases})==113,'case count/uniqueness mismatch')
slot=read('slot-mapping.json');dimensions={s for c in visual for s in c['proposed_slots']}
check(dimensions<=set(slot['research_dimension_to_possible_existing_slot_ids']),'research dimensions missing slot review mapping')
audit=read('corpus-audit.json');snaps=read('existing-source-snapshots.json')
check(len(snaps)==15 and all(s['candidate_id']==s['record']['id'] for s in snaps),'source snapshot closure mismatch')
check(all(s['native_qualification']=='NOT_ASSESSED_BY_THIS_RESEARCH' for s in snaps),'research granted existing-source qualification')
baseline=read('source-baseline.json');drift=[]
for row in baseline['modules']:
 p=ROOT/row['file']
 if not p.exists() or sha(p)!=row['sha256']:drift.append(row['file'])
for p,h in baseline['protected_files'].items():
 path=ROOT/p
 if not path.exists() or sha(path)!=h:drift.append(p)
audit_drift=[p for p,h in audit['module_hashes'].items() if not (ROOT/p).exists() or sha(ROOT/p)!=h]
# Owned research files are checked independently from concurrently modified sources.
files=sorted(p for p in BASE.iterdir() if p.is_file() and p.name not in ['VALIDATION.json','SHA256SUMS'])
for p in files:
 if p.suffix in ['.md','.py','.json','.tsv']:
  for n,line in enumerate(p.read_text().splitlines(),1):
   check(line==line.rstrip(),f'trailing whitespace {p.name}:{n}')
checksums={p.name:sha(p) for p in files}
(BASE/'SHA256SUMS').write_text(''.join(f'{h}  {name}\n' for name,h in checksums.items()))
result=dict(research_integrity='PASS' if not errors else 'FAIL',errors=errors,counts=dict(term_rows=len(terms),visual_cards=len(visual),context_cards=len(context),candidate_drafts=len(drafts),sources=len(sources),mapped_existing_sources=len(snaps),relation_gates=sum(len(c['gates']) for c in visual),evaluation_cases=len(cases)),checked_research_file_count=len(files),source_drift_since_initial_snapshot=sorted(set(drift)),source_drift_since_corpus_audit=audit_drift,source_drift_interpretation='observation only; this task writes research-folder files only; concurrent differences must not be overwritten',native_status='NOT_RUN',retrieval_status='NOT_RUN',image_status='NOT_RUN',pixel_status='NOT_RUN',user_acceptance='NOT_ASSESSED',scope_limit='checks structural research integrity, references, graph endpoints and artifact hashes; does not establish natural-language truth or source/native qualification')
(BASE/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
