"""Adopt the military research as scoped optional authored data, not native proof."""
from pathlib import Path
import collections,copy,gc,hashlib,json,os,sys,uuid
gc.disable()
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3];S=ROOT/'skills/photo-prompt-image-generator';A=S/'assets';O=HERE/'integration-evidence'
sys.path.insert(0,str(S/'scripts'))
import photo_candidate_corpus as corpus
from photo_runtime_sources import source_update
NS=uuid.UUID('68490886-7900-4f42-8fd7-0f991ae1cb8c')
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(prefix,key):return prefix+uuid.uuid5(NS,'military-fiction-20261024:'+key).hex
def write(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_name(p.name+'.military.tmp');tmp.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');os.replace(tmp,p)
CONTRACT=('One complete optional authored military-fiction-compatible visual realization, not a genre definition, official uniform regulation, tactical instruction or legal/clinical assessment. '
 'Retain all positive English and Korean clauses, actual actors, counts, body owners, connected articulations, garment layers, supports, attachment surfaces, strap and cable endpoints, '
 'object states, shared attention endpoints, representation boundaries and explicit specimen or fictional modes. Review the complete source and every intrinsic effect against independently frozen '
 'requester meaning and whole-dimension/property locks. A keyword, role tag, research graph or source URL creates no owner, prerequisite, permission or native qualification. '
 'Do not borrow an unselected alternative, move a hand or device to another owner, merge a depicted figure into the real people count, or combine raised/lowered or worn/removed states. '
 'Distinguishing connected parts must read together at useful scale. partial_is_fail; UNOBSERVABLE_NOT_PASS. '
 'External appearance alone does not establish real identity, age, experience, service status, actual rank or billet, affiliation, training, competence, consent, romance, sexual intent, coercion, '
 'hostility, injury cause, diagnosis, administrative casualty status, legal status, war crimes, internal hidden armour, protective performance, sensor accuracy, communication success, chronology or sound. '
 'An explicitly authored adult fictional/styled subject remains that source choice, not inferred age or biography of a reference person. '
 'Displays, photographs and painted figures show claims within their own carriers. Sources support bounded terminology; scene geometry is authored, not an observation of a source photograph.')

# Whole-proposition footprints, deliberately independent of presentation slots.
EFFECT_TEXT='''
1 setting composition
2 subject count appearance pose action setting relationship composition
3 subject count pose action setting lighting composition
4 subject count pose action setting appearance relationship
5 subject count pose action setting relationship
6 subject appearance pose action setting relationship
7 subject count pose action setting relationship format
8 appearance pose body_geometry
9 subject count appearance pose action setting relationship
10 subject count pose action setting relationship
11 appearance material
12 appearance material setting
13 appearance color
14 appearance
15 appearance color pose
16 appearance material
17 appearance
18 appearance color material
19 subject appearance pose setting
20 appearance
21 appearance
22 appearance material
23 appearance material
24 appearance count composition format
25 appearance count setting composition
26 appearance
27 appearance
28 appearance count composition format material
29 appearance pose action count
30 appearance setting relationship
31 appearance
32 appearance material composition format
33 appearance relationship
34 appearance relationship
35 appearance pose relationship
36 appearance
37 appearance relationship
38 appearance relationship
39 appearance relationship
40 appearance relationship
41 appearance format relationship color setting
42 appearance
43 appearance pose
44 appearance
45 appearance color
46 material color composition format count
47 appearance material
48 appearance
49 pose action
50 pose
51 pose
52 subject count pose action setting composition
53 appearance pose action
54 appearance pose action relationship
55 pose body_geometry setting
56 pose body_geometry setting
57 appearance pose action
58 appearance pose action relationship
59 subject count pose action setting relationship
60 subject pose appearance setting relationship
61 subject pose appearance setting relationship
62 subject pose action setting relationship
63 subject pose action setting relationship
64 subject pose appearance setting
65 appearance pose
66 subject count pose action relationship setting
67 subject count pose action relationship appearance setting
68 subject pose action appearance
69 subject count appearance pose action relationship setting
70 subject count pose action setting relationship format
71 subject pose setting
72 subject pose setting lighting
73 setting
74 subject pose setting relationship
75 subject setting composition
76 subject count appearance pose action setting relationship
77 setting count composition
78 subject pose appearance setting relationship
79 subject count setting composition
80 subject pose lighting setting
81 appearance material
82 subject pose
83 subject count appearance setting format relationship
84 appearance format
85 subject age appearance pose action style
86 subject age appearance
87 subject age appearance relationship
88 subject age appearance relationship style
89 subject age appearance pose
90 subject age appearance material style
91 subject age appearance pose
92 subject age appearance material
93 subject appearance pose body_geometry
94 appearance
95 subject count appearance pose action setting relationship style
96 subject age appearance style body_geometry
97 appearance material
98 subject pose action setting relationship
99 appearance setting
100 appearance setting composition
101 subject pose setting relationship
102 subject appearance pose relationship
103 appearance material
104 appearance color material
'''
EFFECTS={f'V{int(row.split()[0]):02}':row.split()[1:] for row in EFFECT_TEXT.strip().splitlines()}
REUSE={'V20':'cand_5ccf05cc8bd152caaf61d576b37698b8'}
def main():
 O.mkdir(exist_ok=True)
 if (O/'data-integration.json').exists():raise SystemExit('Already integrated; retain evidence.')
 before=corpus.load(A);manifest_path=A/corpus.MANIFEST_NAME;manifest=read(manifest_path)
 protected={str(p.relative_to(ROOT)):sha(p) for p in [S/'SKILL.md',S/'retrieval-runtime.json',*A.glob('*.json')]}
 write(O/'integration-baseline.json',{'head':os.popen('git rev-parse HEAD').read().strip(),'protected':protected,
  'manifest':manifest,'candidate_sha256':{cid:digest(r) for cid,r in before['candidates'].items()},
  'binding_sha256':{bid:digest(r) for bid,r in before['slot_bindings'].items()},
  'catalog_sha256':digest(before['slot_catalog']),'policies_sha256':digest(before['policies'])})
 cards=read(HERE/'semantic-cards.json');contexts=read(HERE/'context-distinctions.json');gaps=read(HERE/'remaining-research.json')
 mapping={};records={};bindings={};decisions=[]
 exact={(c['content'].get('en'),c['content'].get('ko')):cid for cid,c in before['candidates'].items() if c['record_kind']!='diagnostic'}
 for card in cards:
  key=card['id'];cid=REUSE.get(key) or exact.get((card['positive_en'],card['positive_ko']))
  if cid:
   mapping[key]=cid;decisions.append({'card_id':key,'candidate_id':cid,'decision':'reuse_complete_existing_source','native_approval':False});continue
  cid=ident('cand_',key);mapping[key]=cid
  meta={**copy.deepcopy(card),'runtime_registration':True,'runtime_importable':True,'candidate_id':cid,'native_approval':False,
   'native_qualification':'not_qualified','graph_scope':'review metadata only, not native facts or source/role proof'}
  dims=EFFECTS[key];props=[]
  if set(dims)<= {'appearance','material','color'}:
   props=[{'dimension':'appearance','target':'main_subject','property':'wardrobe'}] if 'appearance' in dims else []
  if key=='V81':props=[{'dimension':'appearance','target':'main_subject','property':'body.face.surface_applied_material'},{'dimension':'appearance','target':'main_subject','property':'wardrobe'}]
  record={'id':cid,'record_kind':'visual_option','content':{'en':card['positive_en'],'ko':card['positive_ko'],
   'definition':card['positive_en'],'aliases':[card['title_ko']],'application_contract':CONTRACT,'research_semantics':meta},
   'conditions':{'requires_adult_context':True} if 'adult' in card['positive_en'].lower() else {},
   'effects':{'dimensions':dims,'properties':props},'provenance':[{'source':'authored research docs/research-evidence/photo-prompt/military-fiction-20261024/semantic-cards.json#'+key,'sha256':sha(HERE/'semantic-cards.json')}]}
  records[cid]=record
  for slot in card['suggested_slots']:
   assert slot in before['slot_catalog'];bid=ident('bind_',cid+':'+slot)
   bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional','semantic_role':before['slot_catalog'][slot]['semantic_role'],
    'conditions':{'subject_applicability':{}},'weight':1}
  decisions.append({'card_id':key,'candidate_id':cid,'decision':'new_complete_authored_visual','native_approval':False})
 for row in contexts+gaps:
  key=row.get('id') or 'held_'+row['keyword_id'];cid=ident('cand_',key);mapping[key]=cid
  label=row.get('terms') or row['term'];meaning=row.get('boundary_ko') or row['next_research_ko']
  records[cid]={'id':cid,'record_kind':'diagnostic','content':{'definition':'Context or held diagnostic, excluded from positive visual retrieval: '+label+'. '+meaning,
   'research_semantics':{**copy.deepcopy(row),'native_approval':False,'runtime_registration':True,'graph_scope':'diagnostic only'}},
   'conditions':{},'effects':{'dimensions':[],'properties':[]},
   'provenance':[{'source':'research military-fiction-20261024 '+key,'sha256':sha(HERE/('context-distinctions.json' if 'id' in row else 'remaining-research.json'))}]}
 changed={};changed_prior={}
 salute='cand_59849d02f9cc501bb453ac8d42a8ede7';flight='cand_7c21122f9000531c8cc8f8ad22e90b35'
 for cid in [salute,flight]:changed_prior[cid]=copy.deepcopy(before['candidates'][cid]);changed[cid]=copy.deepcopy(changed_prior[cid])
 changed[salute]['content']['ko']='펴서 모은 손가락들이 이마 가장자리 옆에 놓이고, 손바닥 방향은 지정된 경례 변형을 따르며, 팔꿈치는 같은 어깨에서 바깥쪽으로 굽는다.'
 changed[flight]['content']['ko']='주 조종석·계기판·외부 시야가 함께 보이는 항공기 조종실'
 changed[flight]['content']['aliases']=[x for x in changed[flight]['content']['aliases'] if x!='비행갑판']
 changed[flight]['content']['aliases'].append('항공기 flight deck 조종실')
 for cid in changed:assert all(changed[cid][k]==changed_prior[cid][k] for k in ['id','record_kind','conditions','effects','provenance'])
 cm='photo_candidate_military_fiction_20261024.json';bm='photo_candidate_military_fiction_bindings_20261024.json';sm='photo_military_fiction_semantics_20261024.json'
 for name in [cm,bm,sm]:assert not (A/name).exists(),name
 registry={'schema':'photo-military-fiction-visual-semantics/v1','cards':[{**copy.deepcopy(x),'candidate_id':mapping[x['id']],'registration':'reused' if x['id'] in REUSE else 'authored_optional_visual','native_approval':False} for x in cards],
  'context_distinctions':contexts,'held_visual_terms':gaps,'keyword_routes':[{**copy.deepcopy(x),
   'component_candidate_ids':[mapping[y] for y in x['component_card_ids']],
   'context_candidate_ids':[mapping[y] for y in x['section_context_ids']],
   'automatic_hard_activation':False} for x in read(HERE/'keyword-atlas.json')],
  'sources':read(HERE/'sources.json'),'native_approval':False,'automatic_activation':False,'research_sha256':sha(HERE/'semantic-cards.json')}
 assert set(records).isdisjoint(before['candidates']) and set(bindings).isdisjoint(before['slot_bindings'])
 with source_update(S):
  assert sha(manifest_path)==protected[str(manifest_path.relative_to(ROOT))]
  write(A/cm,{'schema':corpus.MODULE_SCHEMAS['candidates'],'candidates':records});write(A/bm,{'schema':corpus.MODULE_SCHEMAS['slot_bindings'],'slot_bindings':bindings});write(A/sm,registry)
  for mod in manifest['modules']:
   if mod['kind']!='candidates':continue
   path=A/mod['file'];body=read(path);owned=set(body['candidates'])&changed.keys()
   if owned:
    assert sha(path)==protected[str(path.relative_to(ROOT))]
    for cid in owned:body['candidates'][cid]=changed[cid]
    write(path,body)
  manifest['modules'] += [{'file':cm,'kind':'candidates'},{'file':bm,'kind':'slot_bindings'}];write(manifest_path,manifest)
 after=corpus.load(A)
 assert all(after['candidates'][cid]==r for cid,r in before['candidates'].items() if cid not in changed)
 assert all(after['slot_bindings'][bid]==r for bid,r in before['slot_bindings'].items())
 assert all(after[k]==before[k] for k in ['slot_catalog','policies'])
 for name,data in [('card-candidate-map.json',mapping),('new-native-records.json',records),('changed-native-records.json',changed),('changed-native-prior.json',changed_prior)]:write(O/name,data)
 report={'status':'authored_source_integrated','positive_new':sum(x['record_kind']=='visual_option' for x in records.values()),'context_and_held_new':sum(x['record_kind']=='diagnostic' for x in records.values()),
  'bindings_new':len(bindings),'reused_complete_sources':len(REUSE),'narrow_existing_updates':len(changed),'semantic_cards':len(cards),'context_distinctions':len(contexts),'keyword_routes':len(registry['keyword_routes']),
  'before_candidates':len(before['candidates']),'after_candidates':len(after['candidates']),
  'existing_unrelated_records_bindings_catalog_policies_preserved':True,'native_approval':False,'decisions':decisions,
  'source_only_not_installed_yet':True,'image_calls':0}
 write(O/'data-integration.json',report);print(json.dumps({k:v for k,v in report.items() if k!='decisions'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
