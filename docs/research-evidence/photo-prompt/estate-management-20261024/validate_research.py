#!/usr/bin/env python3
"""Research integrity checks, not historical/translation/retrieval/pixel tests."""
import collections,hashlib,json,pathlib,sys
sys.dont_write_bytecode=True
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def read(name):return json.loads((HERE/name).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
inv=read('reference-inventory.json')
source=read('sources.json')['sources']
semantic=read('semantic-cards.json')
visual=semantic['cards'];context=semantic['context_diagnostics']
drafts=read('candidate-drafts.json')['drafts']
cases=read('regression-cases.json')['cases']
base=read('BASELINE.json')
mapping=read('existing-source-mapping.json')
allcards=visual+context
ids=[x['id'] for x in allcards]
assert len(ids)==len(set(ids)), 'Duplicate card ID'
sources={x['id']:x for x in source}
assert len(sources)==len(source), 'Duplicate source ID'
counts=[sum(r['section']==n for r in inv['rows']) for n in range(1,21)]
assert counts==inv['chrome_counts'], 'Original Chrome section row counts changed'
assert len(inv['rows'])==inv['row_count']==sum(counts)
assert len({r['row_id'] for r in inv['rows']})==len(inv['rows'])
assert inv['rows'][-1]['original_label']=='전쟁 후 영지 재건'
catalog=json.loads((ROOT/'skills/photo-prompt-image-generator/assets/photo_candidate_slot_catalog.json').read_text())['slot_catalog']
for c in allcards:
    assert c['source_ids'] and set(c['source_ids'])<=sources.keys(),c['id']
    assert not any(sources[i]['access'].startswith('unavailable') for i in c['source_ids']),f"{c['id']}: unavailable source cannot support a card"
    assert c['automatic_activation'] is False and c['native_approval'] is False,c['id']
    assert c['runtime_registration']=='none',c['id']
for c in visual:
    assert c['visible_en'].strip() and c['visible_ko'].strip() and c['confusion_boundary_ko'],c['id']
    nodes={n['id'] for n in c['components']}
    assert len(nodes)==len(c['components']),c['id']
    assert all(n['owner'] in nodes for n in c['components']),f"{c['id']}: dangling owner"
    assert all(r['subject'] in nodes and r['object'] in nodes for r in c['relations']),f"{c['id']}: dangling graph endpoint"
    assert c['relations'] and len(c['pixel_gates_ko'])>=3,c['id']
    assert set(c['proposed_slots'])<=catalog.keys(),c['id']
    assert c['pixel_status']=='NOT_RUN' and c['source_image_review']=='NOT_RUN',c['id']
    assert c['historical_reconstruction_approved'] is False,c['id']
for c in context:
    assert c['positive_visual_candidate'] is False and c['not_proven_by_pixels'],c['id']
assert {d['card_id'] for d in drafts}=={v['id'] for v in visual}
for d in drafts:
    assert d['canonical_candidate_id'] is None and d['runtime_registration']=='none',d['draft_id']
    assert d['partial_is_fail'] and d['unobservable_policy']=='UNOBSERVABLE_NOT_PASS',d['draft_id']
    assert all(b['status']=='REVIEW_REQUIRED' and b['role_authority'] is False for b in d['binding_proposals'])
for r in inv['rows']:
    assert set(r['visual_card_ids']+r['context_card_ids'])<=set(ids),r['row_id']
    assert not r['exact_definition_verified'] and not r['compound_label_fully_covered'],r['row_id']
assert len({c['id'] for c in cases})==len(cases)
assert all(c['execution']=='NOT_RUN' for c in cases), 'A planned case was mislabeled as executed'
assert all(c.get('card_id') in ids for c in cases if 'card_id' in c)
assert len(mapping['manual_source_reviews'])==8
for r in mapping['manual_source_reviews']:
    b=json.dumps(r['record'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
    assert hashlib.sha256(b).hexdigest()==r['canonical_sha256'],r['candidate_id']
assert mapping['snapshot_manifest_sha256']==base['source_manifest_sha256'],'Research was rebuilt on a different source without preserving a new snapshot'
changed=[]
for m in base['source_modules']:
    f=ROOT/'skills/photo-prompt-image-generator/assets'/m['file']
    if not f.exists() or sha(f)!=m['sha256']:changed.append(str(f.relative_to(ROOT)))
for path,expected in base['existing_dirty_tracked_file_hashes'].items():
    f=ROOT/path
    if not f.exists() or sha(f)!=expected:changed.append(path)
report=dict(integrity='PASS',reference_rows=len(inv['rows']),visual_cards=len(visual),
    context_diagnostics=len(context),candidate_drafts=len(drafts),source_entries=len(source),
    evaluation_cases_defined=len(cases),evaluation_cases_executed=0,
    source_or_protected_snapshot_drift=sorted(set(changed)),
    scope='Checks graph/link/count/role-name integrity and truthful status markers only. Does not certify historical facts, bilingual equivalence, native effects/roles, retrieval, saved pixels, or user acceptance.')
(HERE/'validation-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
