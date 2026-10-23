"""Register harem research as reviewed optional source, keeping prior work intact."""
from pathlib import Path
import json, hashlib, uuid, copy, sys
O=Path(__file__).resolve().parent; Q=O.parent; R=O.parents[4]; S=R/'skills/photo-prompt-image-generator'; A=S/'assets'
sys.path.insert(0,str(S/'scripts'))
import photo_candidate_corpus as corpus
read=lambda p:json.loads(p.read_bytes())
def write(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
NS=uuid.UUID('64073ca7-b2cc-4af5-a476-510ff7614747')
def ident(prefix,key):return prefix+uuid.uuid5(NS,key).hex
CONTRACT=('One optional complete authored visual realization. Preserve the entire bilingual proposition, every stated person and object count, owner, anatomical connection, contact target, support, gap, layer, garment boundary, gaze direction and depicted-media boundary together. '
 'Apply only within independently frozen requester meaning, actual existing owner prerequisites and permitted dimensions/properties. A genre, tag, source citation or research graph creates no facts, people, age, consent or permission. '
 'All distinguishing endpoints and qualifiers must be observable together; partial evidence is not a full pass. '
 'A still image does not establish romantic feelings, diagnosis, personality history, kinship, profession, identity, consent, coercion, chronological cause, game state, an ending or material composition. '
 'Fictional adults and reference appearance remain separate from any inferred real-person biography. Research metadata is not native source qualification.')

# Complete-source effect review, not a claim that every named role is approved.
DIMENSIONS={
 'H':['subject','action','pose','expression','composition'],
 'P':['subject','pose','expression','composition'],
 'A':['subject','appearance','composition'],
 'W':['subject','appearance'],
 'C':['subject','composition','setting','action','appearance'],
}
TRANSLATIONS={
 'cand_522c907a6a97547886a2d207a4138b03':'무심하게 내민 자수 손수건 또는 작은 참 장식',
 'cand_d2834908636b578489498652230bafd9':'같은 인물의 양손 손가락이 번갈아 맞물리고 각 엄지와 손가락의 주인 및 손목 연결이 구분되는 손깍지',
 'cand_ae856dfccef0599eb2db1c6ba565e112':'성인의 허리 지지부에서 같은 스타킹 윗단으로 끈이 내려오고 끈 아래의 여밈쇠가 그 스타킹 윗단에 눈에 보이게 붙으며 벨트 끈과 스타킹의 천 가장자리가 각각 연속되고 분리되어 있다',
}

def main():
 assert not (O/'data-integration.json').exists()
 before=corpus.load(A); manifest=read(A/corpus.MANIFEST_NAME); manifest_sha=sha(A/corpus.MANIFEST_NAME)
 cards=read(Q/'semantic-cards.json')['cards']; routes=read(Q/'keyword-routes.json')['keywords']; sources=read(Q/'sources.json')['sources']
 src={x['id']:x for x in sources}; fresh={}; bindings={}; registry=[]; decisions=[]; existing_pairs={}
 for cid,record in before['candidates'].items():existing_pairs.setdefault((record['content'].get('en'),record['content'].get('ko')),[]).append(cid)
 for card in cards:
  key=card['id'];visual=card['mode']!='context';metadata=copy.deepcopy(card)
  metadata.update(registration_status='authored_optional_source' if visual else 'context_diagnostic',runtime_importable=visual,
    native_qualification='not_qualified',native_approval=False,automatic_hard_activation=False,
    graph_scope='Research review metadata; never a frozen fact, owner selection, effect permission or native proof.',
    source_details=[src[x] for x in card['source_ids']])
  pair=(card['positive_en'],card['positive_ko']); reused=existing_pairs.get(pair,[]) if visual else []
  # Exact bilingual text alone is insufficient for reuse. Keep each complete
  # newly authored count/owner/state alternative scoped for individual review.
  cid=ident('cand_','harem:'+key);assert cid not in before['candidates']
  metadata['candidate_id']=cid
  if visual:
   content={'en':pair[0],'ko':pair[1],'definition':'Complete optional authored visual realization: '+pair[0],
    'aliases':[card['label_ko']],'application_contract':CONTRACT,'research_semantics':metadata}
   dimensions=list(DIMENSIONS[key[0]])
   # Every complete clause changes its actual named world/geometry, even where
   # a role tag only describes one facet. There are no empty effect claims.
   if key in ['H14','H22','H26','P06','P07']:dimensions=sorted(set(dimensions+['setting']))
   conditions={'for_any':['human']}
  else:
   content={'definition':'Context-only diagnostic, excluded from positive visual retrieval: '+card['context_en']+' '+card['context_ko'],
    'research_semantics':metadata};dimensions=[];conditions={}
  fresh[cid]={'id':cid,'record_kind':'visual_option' if visual else 'diagnostic','content':content,
    'conditions':conditions,'effects':{'dimensions':dimensions,'properties':[]},
    'provenance':[{'source':str((Q/'semantic-cards.json').relative_to(R))+'#'+key,'sha256':sha(Q/'semantic-cards.json')}]}
  if visual:
   for slot in card['suggested_slots']:
    assert slot in before['slot_catalog'],slot
    bid=ident('bind_',cid+':'+slot)
    bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional',
      'semantic_role':before['slot_catalog'][slot]['semantic_role'],'conditions':{'subject_applicability':{}},'weight':1.0}
  metadata['actual_slot_suggestions']=card['suggested_slots'] if visual else []
  registry.append(metadata);decisions.append({'card_id':key,'candidate_id':cid,'decision':'new_scoped_visual' if visual else 'diagnostic',
    'exact_bilingual_neighbours':reused,'reason':'Full authored owners/counts/contacts/state retained as one optional alternative; native role/source qualification remains separate.' if visual else 'Nonvisual meaning retained without positive visual retrieval.',
    'effects_review':dimensions,'native_approval':False})
 # Reversible translation refinements, preserving every intrinsic guard/effect.
 changed={};updates={};source_files={}
 for mod in manifest['modules']:
  if mod['kind']!='candidates':continue
  p=A/mod['file'];body=read(p)
  for cid,new in TRANSLATIONS.items():
   if cid not in body.get('candidates',{}):continue
   old=copy.deepcopy(body['candidates'][cid]); record=copy.deepcopy(old)
   record['content']['ko']=new
   body['candidates'][cid]=record;changed[cid]=record;updates[cid]={'file':mod['file'],'before':old,'after':record,
     'reason':'Restore complete source proposition in Korean; OR remains OR, self hands remain self-owned, garter clip and welt endpoints stay explicit. All English, guards, effects, provenance and other content remain unchanged.'}
   source_files[p]=(sha(p),body)
 assert set(changed)==set(TRANSLATIONS)
 newmods=[('photo_candidate_harem_20261023.json','candidates',fresh),('photo_candidate_harem_bindings_20261023.json','slot_bindings',bindings)]
 for name,kind,data in newmods:
  assert not (A/name).exists();manifest['modules'].append({'file':name,'kind':kind})
 for p,(h,body) in source_files.items():assert sha(p)==h,'Source changed concurrently; rebaseline before mutation'
 assert sha(A/corpus.MANIFEST_NAME)==manifest_sha,'Manifest changed concurrently; rebaseline before mutation'
 for p,(_,body) in source_files.items():write(p,body)
 for name,kind,data in newmods:write(A/name,{'schema':corpus.MODULE_SCHEMAS[kind],kind:data})
 write(A/corpus.MANIFEST_NAME,manifest)
 lookup={c['id']:c['candidate_id'] for c in registry}
 for route in routes:
  route.update(candidate_ids=[lookup[x] for x in route['card_ids']],automatic_hard_activation=False,
    discovery_only=True,definition_status='Source-scoped research route; original title is not an approved exact synonym or image recipe.')
 write(A/'photo_harem_semantics_20261023.json',{'schema':'photo-harem-visual-semantics/v1','cards':registry,'keyword_routes':routes,'sources':sources,
    'native_approval':False,'automatic_hard_activation':False,'research_sha256':sha(Q/'semantic-cards.json'),
    'scope':'314 term rows and 6 authored combinations; 76 complete visual/proxy alternatives and 14 context diagnostics. Pending meanings remain pending.'})
 after=corpus.load(A)
 assert all(after['candidates'][cid]==record for cid,record in before['candidates'].items() if cid not in changed)
 assert all(after[k]==before[k] for k in ['slot_bindings','slot_catalog','policies'] if k!='slot_bindings')
 assert all(after['slot_bindings'][k]==v for k,v in before['slot_bindings'].items())
 for cid in changed:
  assert all(after['candidates'][cid][k]==before['candidates'][cid][k] for k in ['conditions','effects','provenance'])
 write(O/'new-native-records.json',fresh);write(O/'changed-native-records.json',changed);write(O/'translation-review.json',updates);write(O/'adoption-review.json',decisions)
 write(O/'data-integration.json',{'status':'source_registered','new_visual_sources':76,'new_context_diagnostics':14,'new_bindings':len(bindings),
  'keyword_rows':320,'translation_refinements':len(changed),'before_CIDs':len(before['candidates']),'after_CIDs':len(after['candidates']),
  'other_candidates_and_all_existing_bindings_catalog_policies_unchanged':True,'native_approval':False,'index_status':'NOT_RUN'})
 print(json.dumps(read(O/'data-integration.json'),ensure_ascii=False))

if __name__=='__main__':main()
