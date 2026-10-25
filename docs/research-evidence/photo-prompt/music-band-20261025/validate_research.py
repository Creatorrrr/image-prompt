"""Check research integrity. Does not verify factual truth, native or pixel quality."""
from pathlib import Path
import json,hashlib,re,collections
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,condition,detail=None):
 checks.append({'check':name,'status':'pass' if condition else 'fail','detail':detail})
cards=read('semantic-cards.json');keywords=read('keyword-atlas.json');contexts=read('context-distinctions.json');sources=read('sources.json');holds=read('remaining-research.json');summary=read('PACKAGE-SUMMARY.json');tables=read('conversation-tables.json')
lookup=lambda rows:{x['id']:x for x in rows}
cc,kk,nn,ss,qq=map(lookup,[cards,keywords,contexts,sources,holds])
check('unique_ids',all(len(lookup(rows))==len(rows) for rows in [cards,keywords,contexts,sources,holds]))
check('counts',(len(tables),len(keywords),len(cards),len(contexts),len(sources),len(holds))==(25,392,124,20,52,12))
actual=[(t['table_index'],i+1,t['section'],r[0],r[1]) for t in tables for i,r in enumerate(t['rows'])]
recovered=[(k['table_index'],k['row_index'],k['section'],k['term'],k['seed_definition']) for k in keywords]
check('every_seed_cell_preserved_exactly',actual==recovered)
check('all_14_sections_and_ending_present',all(f'{i}. ' in (ROOT/'conversation.browser.txt').read_text() for i in range(1,15)) and '창작용 조합 예시' in (ROOT/'conversation.browser.txt').read_text())
check('all_keyword_routes_resolve',all(all(i in cc for i in k['optional_visual_components']+k['contrast_visual_cards']) and all(i in nn for i in k['context_ids']) and all(i in qq for i in k['hold_ids']) and all(i in ss for i in k['source_ids']) for k in keywords))
check('all_cards_have_seeds',all(c['seed_ids'] for c in cards),[c['id'] for c in cards if not c['seed_ids']])
check('bidirectional_routes',all(k['id'] in cc[cid]['seed_ids'] for k in keywords for cid in k['optional_visual_components']+k['contrast_visual_cards']) and all(cid in kk[kid]['optional_visual_components']+kk[kid]['contrast_visual_cards'] for cid,c in cc.items() for kid in c['seed_ids']))
check('three_positive_components_each',all(len(c['observable_components'])==3 and all(g['required_if_selected'] and g['requirement_ko'].strip() for g in c['observable_components']) for c in cards))
check('bilingual_owner_contract_bound',all(c['phrase_ko']==c['owner_contract']['source_proposition_ko'] and c['phrase_en']==c['owner_contract']['source_proposition_en'] for c in cards))
check('research_only_flags',all(c['runtime_importable'] is False and c['native_approval'] is False and c['automatic_hard_activation'] is False for c in cards) and all(not k['adoption_authority'] and not k['equivalence'] for k in keywords))
check('source_references_resolve',all(all(i in ss for i in row['source_ids']) for row in cards+contexts))
check('publisher_urls_have_evidence',all(s['url'] in (ROOT/s['evidence_file']).read_text() for s in sources))
check('source_limit_fields_present',all(s['visual_specimen_reviewed'] is False and s['verified_scope_ko'] and s['limits_ko'] for s in sources))
check('source_access_summary_matches',dict(collections.Counter(s['access_status'] for s in sources))==summary['source_access_counts'])
slots=json.loads((REPO/'skills/photo-prompt-image-generator/assets/photo_candidate_slot_catalog.json').read_text())['slot_catalog']
check('proposed_slots_exist',all(s in slots for c in cards for s in c['proposed_slots']),{'actual_slot_count':len(slots)})
check('followup_cards_resolve',all(cid in cc for h in holds for cid in h['card_ids']))
dev=read('evaluation-cases.json');smoke=read('card-derived-smoke.json');pixels=read('prospective-pixel-cases.json');triage=read('existing-triage.json');existing=read('existing-records.json')
check('planned_evaluation_counts',(len(dev),len(smoke),len(pixels),len(triage))==(44,124,16,9))
check('evaluation_ids_resolve',all(cid in cc for d in dev for cid in d['expected_research_card_ids']) and all(p['card_id'] in cc for p in pixels))
check('evaluation_not_reported_as_executed',all(d['status']=='planned_not_executed' for d in dev+smoke) and all(p['status']=='planned_not_generated' for p in pixels))
check('pixel_gates_match_current_cards',all(p['gates']==cc[p['card_id']]['observable_components'] and p['whole_proposition_en']==cc[p['card_id']]['phrase_en'] for p in pixels))
check('triage_source_snapshot_bound',all(t['candidate_id'] in existing and hashlib.sha256(json.dumps(existing[t['candidate_id']]['record'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()==t['current_record_sha256'] for t in triage))
snapshot=read('corpus-audit.json');changes=[]
for path,expected in snapshot['source_hashes'].items():
 p=REPO/path
 if not p.exists() or sha(p)!=expected:changes.append(path)
check('audited_source_files_unchanged_since_snapshot',not changes,changes)
manifest=REPO/'skills/photo-prompt-image-generator/assets/photo_candidate_corpus_manifest.json'
check('manifest_unchanged_since_snapshot',sha(manifest)==snapshot['manifest_sha256'])
check('runtime_check_is_read_only_pass',read('runtime-check.json')['status']=='pass' and read('runtime-check.json')['image_calls']==0 and read('runtime-check.json')['source_writes']==0)
check('adult_and_dark_seed_tables_preserved',sum(k['table_index'] in [21,22] for k in keywords)==27)
check('rimshot_and_acoustic_device_boundary_preserved','오픈' in cc['A19']['name_ko'] and '어쿠스틱' in cc['A20']['phrase_ko'] and '전자패드' in cc['A20']['confusion_boundary_ko'])
check('report_files_present',all((ROOT/f).exists() for f in ['README.md','RESEARCH.md','IMPLEMENTATION-PLAN.md','EVALUATION-PLAN.md','SOURCES.md','KEYWORD-ATLAS.md','VISUAL-CARDS.md','CONTEXT-DISTINCTIONS.md','GAPS.md']))
result={'status':'pass' if all(c['status']=='pass' for c in checks) else 'fail','scope':'research_structure_provenance_and_snapshot_integrity_only','checks':checks,'check_count':len(checks),'not_verified':['Full truth of all seed definitions','Visual source specimens','Native qualification and role eligibility','Search exposure or search quality','Prompt transport or saved-image compliance','Causal artistic quality or requester acceptance'],'counts':{'source_modules_hashed':len(snapshot['source_hashes']),'slots_read':len(slots),'seed_rows':len(keywords),'cards':len(cards),'sources':len(sources),'manual_development_queries':2*len(dev),'smoke_queries':2*len(smoke),'planned_pixel_cases':len(pixels)},'images_generated':0}
(ROOT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(0 if result['status']=='pass' else 1)
