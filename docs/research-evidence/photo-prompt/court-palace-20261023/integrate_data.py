"""Narrow authored-data adoption. No index, runtime activation or image calls."""
from pathlib import Path
import copy,hashlib,json,sys,uuid,collections
H=Path(__file__).resolve().parent;ROOT=H.parents[3];S=ROOT/'skills/photo-prompt-image-generator';A=S/'assets';O=H/'integration-evidence'
sys.path.insert(0,str(S/'scripts'))
import photo_candidate_corpus as corpus
def read(p):return json.loads(p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
def digest(x):return sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
NS=uuid.UUID('ebeece53-1231-4cff-ae9f-c48d5b8ba236')
def ident(prefix,text):return prefix+uuid.uuid5(NS,text).hex
CONTRACT=('One optional complete authored visual realization. Keep every named owner, body part, garment panel, accessory, count, attachment, support, contact, material boundary and representation layer coherent. '
 'Use only within independently frozen requester meaning and actual permitted dimensions/properties; a family label is not a permission. Sibling variants are not automatically combined. '
 'Distinguishing endpoints and the connecting path must be simultaneously visible at useful scale. UNOBSERVABLE_NOT_PASS; partial_is_fail. '
 'Source provenance and research graphs are review metadata, not native typed-fact qualification, owner permission or historical authenticity. '
 'A still image does not establish identity, age, kinship, rank, lawful succession, consent, coercion, motive, guilt, poisoning, death, chronology, repetition, sound or a supernatural cause.')
PATCHES={
'cand_89be8a1c4fd95159bbee8c848ed56b58':('긴 둥근 앞뒤 자락을 가진 당의 겉저고리',None),
'cand_e855260164c15d79b266c9725a770089':('좁은 당의 소매 끝을 마감하는 밝은 색 거들지',None),
'cand_de6bae158e86581ebf5e215af9eb6335':('치마 위에서 당의 앞뒤 자락을 갈라놓는 옆트임',None),
'cand_412c5d71d396544d9e62f544bd7bf0cb':(None,'empty throne behind the subject; 인물 뒤 빈 왕좌 구도'),
}
def main():
 O.mkdir(exist_ok=False)
 before=corpus.load(A)
 write(O/'BASELINE.json',{'source_files':{str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in [S/'SKILL.md',S/'retrieval-runtime.json',*A.glob('*.json')]},'candidates':len(before['candidates']),'bindings':len(before['slot_bindings']),'candidate_hashes':{k:digest(v) for k,v in before['candidates'].items()},'binding_hashes':{k:digest(v) for k,v in before['slot_bindings'].items()},'slot_catalog_sha256':digest(before['slot_catalog']),'policies_sha256':digest(before['policies'])})
 cards=read(H/'semantic-cards.json')['cards'];drafts={x['card_id']:x for x in read(H/'candidate-drafts.json')['drafts']};sources=read(H/'sources.json')['sources'];lookup={};new={};bindings={};decisions=[]
 for card in cards:
  cid=ident('cand_','court-palace-20261023:'+card['id']);lookup[card['id']]=cid;positive=card['kind']!='context_only' and not card['historical_review_required'];meta={**copy.deepcopy(card),'candidate_id':cid,'native_approval':False,'integration_status':'optional_visual_source' if positive else 'held_diagnostic' if card['historical_review_required'] else 'context_diagnostic'}
  if positive:
   content={'en':card['visible_en'],'ko':card['visible_ko'],'definition':'Optional court-scene visual realization: '+card['visible_en'],'aliases':[card['terms'][0]],'application_contract':CONTRACT,'research_semantics':meta}
   slots=drafts[card['id']]['proposed_role_review'];dims=set(d for slot in slots for d in before['slot_catalog'][slot]['dimensions'])
   # Garment/accessory forms alter wardrobe, not reference face/hair or biology.
   wardrobe=(card['id'][0] in 'BDEFH' or card['id'] in ['G04'])
   if wardrobe and dims<=set(['appearance','role']):effects={'dimensions':['appearance'],'properties':[{'dimension':'appearance','target':'main_subject','property':'wardrobe'}]}
   else:effects={'dimensions':sorted(dims),'properties':[]}
  else:
   content={'definition':('Held for additional artifact and historical review: ' if card['historical_review_required'] else 'Context diagnostic excluded from positive visual retrieval: ')+' / '.join(card['terms'])+'. '+card['confusion_boundary'],'research_semantics':meta};slots=[];effects={'dimensions':[],'properties':[]}
  new[cid]={'id':cid,'record_kind':'visual_option' if positive else 'diagnostic','content':content,'conditions':{},'effects':effects,'provenance':[{'source':'authored research '+str((H/'semantic-cards.json').relative_to(ROOT))+'#'+card['id']+'; bounded citation '+next(x['url'] for x in sources if x['id']==sid),'sha256':sha((H/'semantic-cards.json').read_bytes())} for sid in card['source_ids']]}
  for slot in slots:
   bid=ident('bind_',cid+':'+slot);bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional','semantic_role':before['slot_catalog'][slot]['semantic_role'],'conditions':{'subject_applicability':{}},'weight':2}
  decisions.append({'card_id':card['id'],'candidate_id':cid,'positive':positive,'status':meta['integration_status'],'slots':slots,'historical_review_required':card['historical_review_required']})
 assert set(new).isdisjoint(before['candidates'])
 manifest=read(A/corpus.MANIFEST_NAME);patches=[];files=[]
 for mod in manifest['modules']:
  if mod['kind']!='candidates':continue
  p=A/mod['file'];data=read(p);owned=set(data['candidates'])&set(PATCHES)
  if not owned:continue
  for cid in sorted(owned):
   old=copy.deepcopy(data['candidates'][cid]);co=data['candidates'][cid]['content'];ko,embedding=PATCHES[cid]
   if ko:co['ko']=ko;co['embedding_text']=co.get('en','')+'; '+ko
   if embedding:co['embedding_text']=embedding
   patches.append({'candidate_id':cid,'module':mod['file'],'before':old,'after':copy.deepcopy(data['candidates'][cid]),'conditions_effects_provenance_preserved':all(data['candidates'][cid][k]==old[k] for k in ['conditions','effects','provenance'])})
  write(p,data);files.append(str(p.relative_to(ROOT)))
 assert len(patches)==4 and all(x['conditions_effects_provenance_preserved'] for x in patches)
 for name,kind,field,values in [('photo_candidate_court_palace_20261023.json','candidates','candidates',new),('photo_candidate_court_palace_bindings_20261023.json','slot_bindings','slot_bindings',bindings)]:
  assert not any(m['file']==name for m in manifest['modules']);write(A/name,{'schema':corpus.MODULE_SCHEMAS[kind],field:values});manifest['modules'].append({'file':name,'kind':kind});files.append(str((A/name).relative_to(ROOT)))
 write(A/corpus.MANIFEST_NAME,manifest);files.append(str((A/corpus.MANIFEST_NAME).relative_to(ROOT)))
 routes=read(H/'keyword-routes.json')['rows']
 for route in routes:route.update(candidate_ids=[lookup[x] for x in route['related_card_ids']],automatic_hard_activation=False)
 enriched=[{**c,'candidate_id':lookup[c['id']],'native_approval':False,'integration_status':next(x['status'] for x in decisions if x['card_id']==c['id'])} for c in cards]
 write(A/'photo_court_palace_semantics_20261023.json',{'schema':'photo-court-palace-visual-semantics/v1','cards':enriched,'keyword_routes':routes,'source_refs':sources,'native_approval':False,'automatic_activation':False,'research_sha256':sha((H/'semantic-cards.json').read_bytes())});files.append(str((A/'photo_court_palace_semantics_20261023.json').relative_to(ROOT)))
 after=corpus.load(A)
 assert all(after['candidates'][k]==v for k,v in before['candidates'].items() if k not in PATCHES)
 assert all(after['slot_bindings'][k]==v for k,v in before['slot_bindings'].items()) and after['slot_catalog']==before['slot_catalog'] and after['policies']==before['policies']
 write(O/'new-native-records.json',new);write(O/'changed-native-records.json',{x['candidate_id']:x['after'] for x in patches});write(O/'existing-source-patches.json',patches)
 result={'status':'authored_source_integrated','research_cards':len(cards),'keyword_routes':len(routes),'new_records':len(new),'new_positive_records':sum(x['positive'] for x in decisions),'diagnostic_records':sum(not x['positive'] for x in decisions),'historical_review_held':sum(x['historical_review_required'] for x in decisions),'bindings':len(bindings),'existing_updated_CIDs':4,'before_CIDs':len(before['candidates']),'after_CIDs':len(after['candidates']),'old_unmodified_records_preserved':True,'old_bindings_catalog_policies_preserved':True,'native_approval':False,'index_status':'NOT_RUN','cards':decisions,'authored_file_allowlist':files}
 write(O/'data-integration.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ['cards','authored_file_allowlist']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
