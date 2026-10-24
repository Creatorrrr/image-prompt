"""Research integrity and protected-state observation; not native/pixel qualification."""
import collections
import csv
import hashlib
import json
import pathlib
import re
import subprocess

HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def read(n): return json.loads((HERE/n).read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None

checks=[]
def check(name,condition): checks.append({'name':name,'passed':bool(condition)})

dom=read('reference-browser.json')
routes=read('keyword-routes.json')['routes']
cards=read('semantic-cards.json')['cards']
drafts=read('candidate-drafts.json')['drafts']
sources=read('sources.json')
summary=read('PACKAGE-SUMMARY.json')
scan=read('corpus-scan.json')
baseline=read('BASELINE.json')
existing=read('existing-records.json')
triage=read('existing-source-triage.json')
with (HERE/'BOUNDARY-CASES.tsv').open() as f: boundaries=list(csv.DictReader(f,delimiter='\t'))
cid={c['id'] for c in cards}
sid={s['id'] for s in sources}
slots=set(scan['slots'])
check('chrome_full_tail_and_all_17_sections', all(any(h.startswith(str(i)+'. ') for h in dom['headings']) for i in range(1,18)) and '같은 도면 위로 몸을 기울이며' in dom['text'])
check('26_tables_364_rows',len(dom['tables'])==26 and sum(len(t['rows'])-1 for t in dom['tables'])==364)
refrows=[r for t in dom['tables'] if not t['precedingHeading'].startswith('16.') for r in t['rows'][1:]]
check('356_reference_labels_and_descriptions_preserved',len(routes)==356 and [(r['term'],r['reference_explanation']) for r in routes]==[(r[0],r[1]) for r in refrows])
check('8_concepts_separate_from_terms',len(read('reference-concept-examples.json'))==8)
check('unique_card_and_route_ids',len(cid)==len(cards) and len({r['id'] for r in routes})==len(routes))
check('all_route_card_targets_exist',all(r['card_ids'] and set(r['card_ids'])<=cid for r in routes))
check('all_routes_inactive_and_not_definitional_equivalence',all(r['runtime_activation'] is False and r['definition_status']=='reference_retained_not_blanket_independently_verified' for r in routes))
check('all_card_source_targets_exist',all(c['source_ids'] and set(c['source_ids'])<=sid for c in cards))
check('all_suggested_slots_exist_in_snapshot',all(set(c['suggested_slots'])<=slots for c in cards))
check('all_graphs_have_endpoints',all(c['relations'] and all(r['from'] in {n['id'] for n in c['owner_nodes']} and r['to'] in {n['id'] for n in c['owner_nodes']} for r in c['relations']) for c in cards))
check('declared_owner_namespaces_have_explicit_links',all(all(any(r=={'from':n['id'],'relation':'belongs_to','to':n['id'][0]} for r in c['relations']) for n in c['owner_nodes'] if re.match(r'^[ABCD]_(?!and_)',n['id'])) for c in cards))
visual=[c for c in cards if c['mode'] in ('observable','staged_proxy')]
nonvisual=[c for c in cards if c['mode'] not in ('observable','staged_proxy')]
check('all_visible_cards_bilingual',all(c['positive_en'] and c['positive_ko'] for c in visual))
check('nonvisual_cards_have_no_positive_candidate',all(c['positive_en'] is None and c['positive_ko'] is None and c['activation']=='context_only_no_positive_candidate' for c in nonvisual))
check('one_draft_per_visual_card_only',len(drafts)==len(visual)==101 and {d['card_id'] for d in drafts}=={c['id'] for c in visual})
cby={c['id']:c for c in cards}
check('drafts_preserve_full_bilingual_owner_and_gate_contract',all(all(d[k]==cby[d['card_id']][k] for k in ('positive_en','positive_ko','owner_nodes','relations','confusion_boundary','observable_gate','source_ids')) for d in drafts))
check('all_cards_and_drafts_not_runtime_approved',all(c['runtime_importable'] is False and c['native_approval'] is False and c['pixel_status']=='NOT_RUN' for c in cards+drafts))
check('all_cards_have_source_scope_boundary_and_pixel_policy',all(c['source_evidence_scope'] and c['confusion_boundary'] and c['observable_gate'] and c['unobservable_policy']=='UNOBSERVABLE_NOT_PASS' and c['partial_policy']=='partial_is_fail' for c in cards))
check('source_statuses_and_image_limits_explicit',len(sources)==30 and all(s['url'].startswith('https://') and s['access_status'] and s['claim_scope'] and not s['image_reviewed'] for s in sources))
check('source_access_counts_reproduce',dict(collections.Counter(s['access_status'] for s in sources))==summary['source_access'])
check('14_original_records_and_triage_closure',len(existing)==len(triage)==14 and {t['candidate_id'] for t in triage}==set(existing))
check('triage_records_have_conditions_effects_bindings',all(all(k in r['record'] for k in ('content','conditions','effects')) and r['bindings'] for r in existing.values()))
check('triage_canonical_hashes',all(t['source_record_sha256']==hashlib.sha256(json.dumps(existing[t['candidate_id']]['record'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest() for t in triage))
check('36_bilingual_boundary_cases_and_valid_card_links',len(boundaries)==36 and all(r['query_ko'] and r['query_en'] and r['expected'] and r['forbidden'] and set(r['card_ids'].split(','))<=cid for r in boundaries))
check('development_cases_explicitly_not_holdout',len(read('development-cases.json'))==124 and all(not r['executed'] and r['independence']=='derived_from_authored_cards_not_holdout' for r in read('development-cases.json')))
check('no_execution_counts_inflated',summary['executed_search_queries']==summary['generated_images']==summary['native_candidates_added']==0)
required=['RESEARCH.md','IMPLEMENTATION-PLAN.md','PIXEL-PLAN.md','GAPS.md','CORPUS-FINDINGS.md','SOURCES.md','README.md']
check('required_review_documents_exist',all((HERE/p).is_file() for p in required))
broken=[]
for p in HERE.glob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        # These two validation outputs are created after checks in this invocation.
        if target in {'VALIDATION.json','SHA256SUMS'}:continue
        if not re.match(r'^[a-z]+:',target) and not (p.parent/target.split('#')[0]).exists():broken.append([p.name,target])
check('relative_document_links_exist',not broken)
drift=[p for p,h in baseline['protected_files'].items() if sha(ROOT/p)!=h]
runtime_drift=[p for p,h in baseline['runtime_pointer_hashes'].items() if sha(pathlib.Path(p))!=h]
module_drift=[p for p,h in scan['module_hashes'].items() if sha(ROOT/p)!=h]
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
passed=all(c['passed'] for c in checks)
status='RESEARCH_STRUCTURE_PASS' if passed else 'RESEARCH_STRUCTURE_FAIL'
if passed and (drift or runtime_drift or head!=baseline['head']):status='STRUCTURE_PASS_WORKSPACE_DRIFT_REQUIRES_REBASELINE'
report={'status':status,'checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'broken_links':broken,'source_snapshot_counts':scan['counts'],'package_counts':summary,'boundary_cases':36,'boundary_queries':72,'boundary_independence':'hand_authored_after_research_development_not_sealed_holdout','baseline_head':baseline['head'],'current_head':head,'protected_file_count':len(baseline['protected_files']),'protected_file_drift':drift,'module_drift':module_drift,'runtime_pointer_drift':runtime_drift,'protection_scope':baseline['scope'],'limits':['Custom structural checks do not verify scholarly correctness or complete term-specific visual coverage.','No native source validation, retrieval, embedding, index closure verification, install, generation, pixel review, acceptance, commit or push was performed.','Large generated search shards excluded from protected-byte scan; initial untracked paths are listed in git_status but their bytes were not snapshotted.','Shared-workspace drift is observed and preserved, never reverted by this validator.']}
(HERE/'VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
manifest=[]
for p in sorted(HERE.rglob('*')):
    if p.is_file() and p.name!='SHA256SUMS' and '__pycache__' not in p.parts:manifest.append(f'{sha(p)}  {p.relative_to(HERE)}')
(HERE/'SHA256SUMS').write_text('\n'.join(manifest)+'\n')
print(json.dumps({'status':status,'passed':report['passed'],'total':report['total'],'failed':[c['name'] for c in checks if not c['passed']],'protected_drift':len(drift),'module_drift':module_drift,'runtime_pointer_drift':runtime_drift},ensure_ascii=False))
raise SystemExit(0 if passed else 1)
