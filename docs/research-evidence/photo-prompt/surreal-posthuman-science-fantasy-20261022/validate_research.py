"""Research package integrity checks. PASS does not qualify semantics, retrieval or pixels."""
from pathlib import Path
from collections import Counter
import csv, hashlib, json, re, sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
load=lambda n:json.loads((HERE/n).read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,condition,detail=None):checks.append(dict(check=name,pass_=bool(condition),detail=detail))

sources=load('sources.json')['sources']; source_ids={s['source_id'] for s in sources}
keywords=load('keyword-register.json')['keywords'];cards=load('semantic-cards.json')['cards']
proposals=load('candidate-drafts.json')['proposals'];contexts=load('context-records.json')['records']
counts=load('COUNTS.json')
check('source_identity',len(source_ids)==len(sources)==33)
check('reference_keyword_inventory',len(keywords)==182 and len({k['label'] for k in keywords})==182)
check('all_keyword_definitions_have_origin',all(k['definition_ko'] and k['definition_origin'] for k in keywords))
check('no_keyword_automatic_visual_obligation',all(k['automatic_visual_obligations']==[] and k['native_approval'] is False for k in keywords))
check('keyword_source_refs',all(set(k['direct_source_ids']+k['family_background_source_ids'])<=source_ids for k in keywords))
check('72_unique_cards_12_families',len(cards)==len({c['card_id'] for c in cards})==72 and Counter(c['card_id'][0] for c in cards)==dict.fromkeys('ABCDEFGHIJKL',6))
check('24_priority_review_cases',sum(c['priority']=='P0' for c in cards)==24)
catalog=json.loads((ROOT/'skills/photo-prompt-image-generator/assets/photo_candidate_slot_catalog.json').read_text())['slot_catalog']
for c in cards:
    cid=c['card_id'];endpoints=set(c['owners'])
    check(cid+'-source_refs',bool(c['source_ids']) and set(c['source_ids'])<=source_ids)
    check(cid+'-owned_endpoints',all(r['from'] in endpoints and r['to'] in endpoints and r['from']!=r['to'] for r in c['directed_relations']))
    check(cid+'-all_owners_referenced',endpoints=={r[e] for r in c['directed_relations'] for e in ['from','to']})
    check(cid+'-catalog_vocabulary_only',set(c['proposed_slots'])<=set(catalog))
    check(cid+'-literal_meaning_gate',c['whole_positive_meaning_gate']['proposal_en']==c['proposal_en'] and c['whole_positive_meaning_gate']['proposal_ko']==c['proposal_ko'])
    check(cid+'-components',set(g['owner'] for g in c['component_gates'])==endpoints)
    check(cid+'-relation_gates',len(c['render_gates'])==len(c['directed_relations']) and all(g['relation']==r and g['partial_is_fail'] and g['both_endpoints_required'] and g['status']=='NOT_RUN' for g,r in zip(c['render_gates'],c['directed_relations'])))
    check(cid+'-no_quality_claim',c['native_approval'] is False and c['pixel_status']=='NOT_RUN')
check('drafts_are_not_registered',len(proposals)==72 and all(p['candidate_id'] is None and p['realization_id'] is None and p['conditions_effects_native_proof'].startswith('UNAUTHORED') for p in proposals))
check('context_is_not_positive_effect',len(contexts)==16 and all(x['positive_visual_effects']==[] and x['native_approval'] is False and set(x['source_ids'])<=source_ids for x in contexts))
with (HERE/'EVALUATION-CASES.tsv').open() as f:cases=list(csv.DictReader(f,delimiter='\t'))
check('evaluation_design_not_results',len(cases)==112 and all(x['status']=='NOT_RUN' for x in cases) and Counter(x['cohort'] for x in cases)=={'development':72,'boundary':16,'ordinary':12,'nonvisual':12})
check('bilingual_case_queries',all(x['query_ko'] and x['query_en'] for x in cases) and counts['bilingual_queries']==len(cases)*2)

snapshots=load('existing-source-snapshots.json')['snapshots'];audit=load('CORPUS-AUDIT.json')
check('36_unique_whole_source_snapshots',len(snapshots)==len({s['candidate_id'] for s in snapshots})==36)
for s in snapshots:
    digest=hashlib.sha256(json.dumps(s['record'],sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    check(s['candidate_id']+'-snapshot_digest',digest==s['record_sha256'] and s['module_sha256']==audit['module_sha256'][s['owner_module']])
links=[]
for p in HERE.glob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if re.match(r'^[a-z][a-z0-9+.-]*:',target) or target.startswith('#'):continue
        resolved=(p.parent/target.split('#')[0]).resolve()
        if resolved.name in ['VALIDATION.json','SHA256SUMS']:continue
        links.append((p.name,target,resolved.exists()))
check('local_document_links',all(x[2] for x in links),[x for x in links if not x[2]])

baseline=load('BASELINE.json')
tracked_drift=[]
for rel,digest in baseline['tracked_sha256'].items():
    path=ROOT/rel
    if not path.is_file() or sha(path)!=digest:tracked_drift.append(rel)
source_drift=[rel for rel,digest in audit['module_sha256'].items() if not (ROOT/rel).is_file() or sha(ROOT/rel)!=digest]
runtime=load('RUNTIME-OBSERVATION.json')
runtime_drift=[rel for rel,rec in runtime['declarations'].items() if sha(ROOT/rel)!=rec['sha256']]
# Concurrent drift is reported independently; it is never silently restored.
check('research_scope_protected_tracked_files',not tracked_drift,tracked_drift)
check('corpus_snapshot_still_matches',not source_drift,source_drift)
check('runtime_declarations_still_match',not runtime_drift,runtime_drift)
check('installed_read_only_check',runtime['check_exit_code']==0 and runtime['installed_check']['image_calls']==0 and runtime['installed_check']['source_writes']==0)

failed=[c for c in checks if not c['pass_']]
result=dict(schema='research-package-integrity/v1',status='PASS' if not failed else 'CHECK_REQUIRED',
            scope='Artifact structure, internal references and protected-file hashes only. No independent semantic, translation, native qualification, search or image proof.',
            counts=counts,checks=len(checks),failed=failed,tracked_drift=tracked_drift,source_drift=source_drift,runtime_drift=runtime_drift,
            unrun=['runtime registration','embedding/index build/publication','retrieval evaluation','native source qualification','image generation','native-pixel review','independent bilingual review','user acceptance','commit/push'])
(HERE/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
files=sorted(p for p in HERE.iterdir() if p.is_file() and p.name!='SHA256SUMS')
(HERE/'SHA256SUMS').write_text(''.join(f'{sha(p)}  {p.name}\n' for p in files))
print(json.dumps({'status':result['status'],'checks':len(checks),'failures':len(failed),'tracked_drift':tracked_drift,'source_drift':source_drift,'runtime_drift':runtime_drift},ensure_ascii=False))
sys.exit(1 if failed else 0)
