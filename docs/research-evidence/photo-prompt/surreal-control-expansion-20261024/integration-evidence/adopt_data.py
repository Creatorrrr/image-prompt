from pathlib import Path
import copy,hashlib,json,sys,uuid
R=Path('/Users/chasoik/Projects/image-prompt');O=Path(__file__).parent;Q=O.parent;S=R/'skills/photo-prompt-image-generator';A=S/'assets'
sys.path.insert(0,str(S/'scripts'));import photo_candidate_corpus as c
from photo_runtime_sources import source_update
rd=lambda p:json.loads(p.read_bytes())
def wr(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
EFFECTS={
'C01':'setting appearance count relationship lighting','C02':'subject age pose setting material appearance body_geometry relationship lighting','C03':'subject age pose action count setting material appearance relationship expression lighting',
'C04':'subject action pose material appearance body_geometry relationship camera setting','C05':'subject age pose action setting count material appearance relationship lighting atmosphere','C06':'subject age pose action setting lighting atmosphere appearance relationship',
'C08':'subject setting count material body_geometry appearance relationship camera','C09':'subject age pose action setting count material appearance body_geometry relationship composition','C10':'subject age count pose action setting appearance body_geometry relationship composition',
'R11':'setting count material appearance lighting relationship','R12':'setting count material appearance body_geometry relationship','R13':'setting material appearance body_geometry relationship','R14':'setting material appearance body_geometry relationship','R15':'setting material appearance body_geometry relationship','R16':'setting atmosphere appearance material lighting relationship','R17':'setting atmosphere material appearance relationship lighting','R18':'subject count pose action setting appearance body_geometry relationship','R19':'setting material appearance body_geometry relationship lighting','R20':'setting material appearance composition relationship'}
SLOTS={'C01':['surreal_concept','surreal_physics_detail'],'C02':['surface_material','surreal_physics_detail'],'C03':['surreal_concept','object_structure'],'C04':['object_structure','surreal_physics_detail'],'C05':['surreal_concept','surreal_physics_detail'],'C06':['surreal_concept','surreal_physics_detail'],'C08':['surreal_concept','surreal_physics_detail'],'C09':['surreal_concept','surreal_physics_detail'],'C10':['surreal_concept','surreal_physics_detail'],'R11':['surreal_concept','surreal_physics_detail'],'R12':['object_structure','surreal_concept'],'R13':['surface_material','object_structure'],'R14':['surreal_concept','surreal_physics_detail'],'R15':['object_structure','surreal_concept'],'R16':['surreal_concept','surreal_physics_detail'],'R17':['surface_material','surreal_concept'],'R18':['surreal_concept','surreal_physics_detail'],'R19':['object_structure','surreal_physics_detail'],'R20':['surreal_concept','surreal_physics_detail']}
DIAG_EN=[
'A clean circular area in dust shows a local surface difference. It does not establish a missing teacup, a handle imprint, who removed anything, chronology, supernatural disappearance or materialized memory.',
'A pool-like surface above visible people and furniture can suggest submersion. It does not establish water-filled space, underwater breathing, dry clothing, duration, physical impossibility or absence of glass, separate space, reflection or compositing.',
'A separated droplet has a visible position relative to the water and glass rim. A still image does not establish upward or downward motion, reversed gravity, sustained suspension, cause or temporal order.',
'Multiple colored shadows from multiple lights do not establish autonomous shadows or multiplied owners.',
'An aligned canvas edge and background support perceptual correspondence, not literal dimensional passage or landscape copying.',
'A mineral-looking surface with a dent is visible. Actual stone softness and the deformation process are not established.',
'A continuous road stripe with a lifted end may be ordinary road tape or peeling. Material transformation and living roads are not established.',
'Stone-to-grass contact or hands separated from a broom show momentary arrangements, not sustained support, absence of hidden supports or autonomous cleaning.',
'A ceiling opening, sky and indoor light can alter perception. They do not establish solid light or a different climate.',
'Sewn architectural surfaces and a normal structural reference do not establish residence history, the depicted person\'s memory or invisible load bearing.',
'A pool-like surface over a separate glass-bounded space can be physically realizable. Appearance does not establish underwater breathing or explain dry clothing.',
'Frost-like crystals, green leaves and their transition show local surface states, not actual temperature, elapsed time or supernatural protection.',
'A relationship gap too small to observe is unobservable evidence. Missing or unreadable realization is not proof of subtle surreal intensity one; no universal pixel threshold is established.',
'Surreal zero disables added agent treatment. It does not remove the requester\'s explicit dragon, fantasy person or impossible structure.',
'Ordinary reflections, contact shadows and perspective can support realism. They do not themselves establish a surreal effect.',
'One leading relationship and many secondary props differ in role. Counting unusual objects does not establish surreal intensity three.'
]
def main():
 old=c.load(A);cfg=rd(S/'retrieval-runtime.json');store=Path.home()/'.cache/image-prompt/photo-shared-runtime/h-f2-installed';native=store/'generations'/cfg['native_generation_id']
 before={'config':cfg,'store':str(store),'native':str(native),'corpus_sha256':c.digest(old),'working_counts':{k:len(old[k]) for k in ['candidates','slot_bindings','slot_catalog']},'source_files':{p.name:sha(p) for p in A.iterdir() if p.is_file() and p.suffix=='.json'}};wr(O/'before.json',before)
 cards=rd(Q/'candidate-proposals.json')['cards'];routes=rd(Q/'discovery-routes.json')['routes'];sources={s['source_id']:s for s in rd(Q/'sources.json')['sources']};records={};bindings={};registry=[];mapping={};decisions=[]
 assert set(EFFECTS)==set(SLOTS)=={v['research_id'] for v in cards if v['decision']=='new_complete_variant'}
 app='One complete optional authored visual arrangement. Preserve every positive English and Korean clause, owner, material appearance, state, count, contact, spatial boundary, normal comparison and same/different correspondence. Use only when all affected dimensions and properties permit the complete arrangement. All described endpoints and qualifiers must be legible together; partial or hidden evidence fails the complete case. Research relations, aliases, references and slot bindings establish no native approval or owner permissions. A still image does not prove actual material transformation, hidden-support absence, mass, chronology, mental state, supernatural causation or sustained motion. Intensity is an authorial role, never an intrinsic candidate level.'
 for card in cards:
  k=card['research_id'];kind=card['decision'];cid=None
  if kind=='new_complete_variant':
   cid='cand_'+uuid.uuid5(uuid.NAMESPACE_URL,'image-prompt/surreal-control-expansion/20261024/'+k).hex
   assert cid not in old['candidates'];en=card['proposal_en'];assert en not in [v.get('content',{}).get('en') for v in old['candidates'].values()]
   route=next(r for r in routes if r['research_card_id']==k)
   meta={**copy.deepcopy(card),'candidate_id':cid,'registration_status':'authored_source_module','native_qualification':'not_qualified','all_positive_clauses_required':True,'partial_is_fail':True,'unobservable_result':'UNOBSERVABLE_NOT_PASS','source_refs':[sources[i] for i in card['source_ids']],'graph_scope':'Research review only, not typed owner facts or native admission.','source_support':'Principle or counterexample only; concrete scene independently authored.'}
   records[cid]={'id':cid,'record_kind':'visual_option','content':{'en':en,'ko':card['proposal_ko'],'definition':'Optional complete surreal or perceptual relationship: '+en,'aliases':[card['title_ko'],route['en'],route['ko']],'application_contract':app,'research_semantics':meta},'conditions':{'requires_adult_context':True} if 'adult' in en.lower() else {},'effects':{'dimensions':sorted(EFFECTS[k].split()),'properties':[]},'provenance':[{'source':sources[i]['url'],'sha256':sha(Q/'candidate-proposals.json')} for i in card['source_ids']]}
   for slot in SLOTS[k]:
    assert slot in old['slot_catalog'];bid='bind_'+uuid.uuid5(uuid.NAMESPACE_URL,cid+'/'+slot).hex
    bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional','semantic_role':old['slot_catalog'][slot]['semantic_role'],'conditions':{'subject_applicability':{}},'weight':2}
  elif kind=='reuse_same_source':
   cid=card.get('reuse_candidate_id') or card['neighbor_sources'][0]['candidate_id']
   assert cid in old['candidates'];src=old['candidates'][cid];assert src['content']['en']==card['proposal_en'] and src['content']['ko']==card['proposal_ko'];meta={**copy.deepcopy(card),'candidate_id':cid,'registration_status':'same_source_reference_only','native_approval':False,'pixel_status':'NOT_RUN','source_record_sha256':c.digest(src)}
  else:meta={**copy.deepcopy(card),'candidate_id':None,'registration_status':'diagnostic_hold','positive_retrieval':False}
  mapping[k]=cid;registry.append(meta);decisions.append({'research_id':k,'candidate_id':cid,'decision':kind,'reason_ko':card['decision_reason_ko'],'native_approval':False})
 for d,en in zip(rd(Q/'diagnostics.json')['records'],DIAG_EN,strict=True):
  k=d['diagnostic_id'];cid='cand_'+uuid.uuid5(uuid.NAMESPACE_URL,'image-prompt/surreal-control-expansion/20261024/'+k).hex
  assert cid not in old['candidates'];meta={**d,'candidate_id':cid,'registration_status':'authored_diagnostic_module','native_approval':False,'pixel_status':'NOT_RUN'}
  records[cid]={'id':cid,'record_kind':'diagnostic','content':{'en':en,'ko':d['title_ko']+' 관측: '+'; '.join(d['observable'])+' 단정 불가: '+'; '.join(d['not_inferable'])+' 용도: '+d['use_ko'],'definition':'Context-only observability and confusion boundary, excluded from positive material retrieval.','aliases':[d['title_ko']],'application_contract':'Diagnostic only. Do not turn unobservable cause, chronology, mental state or normal competing interpretation into a fixed positive recipe.','research_semantics':meta},'conditions':{},'effects':{'dimensions':[],'properties':[]},'provenance':[{'source':sources[i]['url'],'sha256':sha(Q/'diagnostics.json')} for i in d['source_ids']] or [{'source':'skills/photo-prompt-image-generator/precore/creative_controls.json','sha256':sha(S/'precore/creative_controls.json')}]}
  registry.append(meta)
 nm='photo_candidate_surreal_control_expansion_20261024.json';bm='photo_candidate_surreal_control_expansion_bindings_20261024.json';sm='photo_surreal_control_expansion_semantics_20261024.json'
 assert not any((A/f).exists() for f in [nm,bm,sm]);manifest=rd(A/c.MANIFEST_NAME);manifest['modules'] += [{'file':nm,'kind':'candidates'},{'file':bm,'kind':'slot_bindings'}]
 with source_update(S):
  assert c.digest(c.load(A))==before['corpus_sha256'];wr(A/nm,{'schema':c.MODULE_SCHEMAS['candidates'],'candidates':records});wr(A/bm,{'schema':c.MODULE_SCHEMAS['slot_bindings'],'slot_bindings':bindings});wr(A/c.MANIFEST_NAME,manifest)
  now=c.load(A);assert all(now['candidates'][k]==v for k,v in old['candidates'].items());assert all(now['slot_bindings'][k]==v for k,v in old['slot_bindings'].items());assert all(now[k]==old[k] for k in ['slot_catalog','policies'])
 registrydata={'schema':'photo-surreal-control-expansion-registry/v1','cards':registry,'mechanisms':rd(Q/'mechanism-coverage.json')['mechanisms'],'keyword_routes':[{**r,'candidate_id':mapping[r['research_card_id']],'approval':'authored_source_reference' if mapping[r['research_card_id']] else 'diagnostic_hold'} for r in routes],'decisions':decisions,'sources':list(sources.values()),'native_approval':False,'intrinsic_level_mapping':False,'counts':{'new_positive':19,'diagnostics':16,'reused_sources':6,'held_proposals':1,'bindings':len(bindings),'mechanisms':12,'routes':26}}
 wr(A/sm,registrydata);wr(O/'new-native-records.json',records);wr(O/'changed-native-records.json',{});wr(O/'data-integration.json',registrydata);wr(O/'source-preservation.json',{'status':'pass','old_candidates_preserved':len(old['candidates']),'old_bindings_preserved':len(old['slot_bindings']),'catalog_policies_unchanged':True,'prior_file_hashes':before['source_files'],'new_modules':[nm,bm,sm],'counts':registrydata['counts'],'after_counts':{k:len(now[k]) for k in ['candidates','slot_bindings','slot_catalog']}});print(registrydata['counts'])
if __name__=='__main__':main()
