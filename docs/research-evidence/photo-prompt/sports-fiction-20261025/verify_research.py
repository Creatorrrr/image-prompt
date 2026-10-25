"""Check research artifact integrity; this is not a runtime or image test."""
from pathlib import Path
import json, re, hashlib

ROOT=Path(__file__).resolve().parent
def read(name):return json.loads((ROOT/name).read_text())
def unique(rows,key='id'):
    values=[r[key] for r in rows]
    assert len(values)==len(set(values)),key

tables=read('conversation-tables.json')['tables']
routes=read('keyword-routes.json')['routes']
cards=read('semantic-cards.json')['cards']
sources=read('sources.json')['sources']
drafts=read('candidate-drafts.json')['drafts']
bindings=read('binding-drafts.json')['bindings']
cases=read('regression-cases.json')['cases']
unique(routes);unique(cards);unique(sources);unique(drafts,'draft_id');unique(bindings,'draft_id');unique(cases)
source_ids={x['id'] for x in sources};card_ids={x['id'] for x in cards};draft_ids={x['draft_id'] for x in drafts}
original={(t['table_index'],ri):cells for t in tables for ri,cells in enumerate(t['rows'][1:],1)}
assert len(routes)==len(original)==330
assert len({(r['table_index'],r['row_index']) for r in routes})==330
for r in routes:
    assert [r['term'],r['original_definition']]==original[(r['table_index'],r['row_index'])]
    assert set(r['optional_realization_ids'])<=card_ids
    assert set(r['source_ids'])<=source_ids
    assert r['hard_activation'] is False and r['automatic_bundle'] is False
for c in cards:
    assert len(c['components'])==3
    assert c['proposal_en']=='; '.join(g['en'] for g in c['components'])+'.'
    assert c['proposal_ko']=='; '.join(g['ko'] for g in c['components'])+'.'
    assert all(g['pixel_gate'] and g['required_if_selected'] for g in c['components'])
    assert set(c['source_ids'])<=source_ids
    assert not c['runtime_registered'] and c['native_pixel_status']=='NOT_RUN'
    owners={o['id'] for o in c['owners']}
    assert all(r['subject'] in owners and r['object'] in owners for r in c['relations'])
    assert c['review_policy']['partial_is_fail'] and c['review_policy']['unobservable']=='UNOBSERVABLE_NOT_PASS'
for d in drafts:
    assert d['semantic_card_id'] in card_ids and not d['runtime_registered']
    if d['semantic_card_id'] in ('X04','X05','X07','X08'):
        assert not d['content']['aliases'], 'Context/diagnosis/outcome seeds must not become positive synonyms.'
for b in bindings:
    assert b['candidate_draft_id'] in draft_ids and b['role']=='optional'
    assert b['native_schema_verified'] is False
for c in cases:
    assert set(c['linked_card_ids'])<=card_ids
    assert c['execution_status']=='PLANNED_NOT_RUN'
atoms=read('technique-atoms.json')['atoms'];unique(atoms)
assert len(atoms)==70 and all(a['parent_row_id'] in {r['id'] for r in routes} for a in atoms)
assert sum(bool(a['optional_realization_ids']) for a in atoms)==50

# Concrete lexical collision concerns found during this research.
for term in ('스포콘 — スポ根, Spokon','업셋 — Upset','자이언트 킬링 — Giant-killing','승강제 — Promotion and relegation','세트 플레이 — Set play'):
    assert next(r for r in routes if r['term']==term)['optional_realization_ids']==[],term
by_id={c['id']:c for c in cards}
assert by_id['W06']['source_ids']==['S35','S38']
assert 'hips to ankles' in by_id['W06']['proposal_en']
assert 'W14' in next(r for r in routes if r['term']=='원피스 수영복·니 스킨 — One-piece / Kneeskin')['optional_realization_ids']
assert 'W09' not in next(r for r in routes if r['term']=='원피스 수영복·니 스킨 — One-piece / Kneeskin')['optional_realization_ids']

link_errors=[]
for p in ROOT.glob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if target.startswith(('https://','http://','#')):continue
        if target=='research-integrity.json':continue  # This check writes the linked report below.
        if not (ROOT/target.split('#')[0]).exists():link_errors.append((p.name,target))
assert not link_errors,link_errors
report={'status':'PASS','proof_scope':'Local research JSON integrity, original-row preservation, references, draft-only flags, selected lexical boundaries, and local document links only.',
 'counts':{'original_rows':len(original),'cards':len(cards),'components':sum(len(c['components']) for c in cards),'sources':len(sources),'candidate_drafts':len(drafts),'binding_drafts':len(bindings),'regression_cases_planned':len(cases),'technique_atoms':len(atoms),'mapped_technique_atoms':50},
 'not_proven':['All definitions independently verified','Sport-specific biomechanics correctness','Native schema acceptance','Actual retrieval ranking or pack exposure','Composed prompt quality','Returned native image quality','Requester acceptance'],
 'runtime_changes_performed':False,'image_generation_performed':False,
 'hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.glob('*.json')) if p.name!='research-integrity.json'}}
(ROOT/'research-integrity.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='hashes'},ensure_ascii=False,indent=2))
