"""Register complete idol visual options and excluded contexts, preserving old records."""
from pathlib import Path
import collections,copy,hashlib,json,sys,uuid
H=Path(__file__).resolve().parent;ROOT=H.parents[3];SKILL=ROOT/'skills/photo-prompt-image-generator';A=SKILL/'assets';O=H/'integration-evidence'
sys.path.insert(0,str(SKILL/'scripts'))
import photo_candidate_corpus as corpus
read=lambda p:json.loads(p.read_bytes())
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
NS=uuid.UUID('39565d5e-3376-4c88-b227-a981023f4631')
ident=lambda prefix,key:prefix+uuid.uuid5(NS,'idol-fiction-20261023:'+key).hex
CONTRACT=('One complete optional authored idol-scene visual realization, not a genre definition or a mandatory bundle. '
 'Retain every stated actor, limb, garment, prop, floor support, display boundary, represented-image owner, count and directed endpoint in the selected English and Korean proposition. '
 'Review all whole-scene conditions and actual effects against independently frozen requester meaning and locked dimensions/properties; a role tag or lexical hit creates no owner or permission. '
 'Do not combine sibling alternatives or transfer a hand, garment, device, mark or represented face to another owner. '
 'The cited sources establish bounded domain context, not this authored whole-scene geometry or exact visual specimen. '
 'All selected distinguishing components and both relation endpoints must be observable together; hidden or partial required evidence cannot pass. '
 'Research metadata is not native typed-fact qualification. A still image does not establish identity, age beyond explicit fictional setting, consent, coercion, sexual orientation, actual romance, rank, skill, popularity, debut history, first victory, revenue, debt, medical state, repetition, timing, sound, live singing, lip sync, real-time tracking, AI autonomy, material chemistry or legal conclusions.')

# Additional dimensions declared conservatively for the complete literal, beyond its presentation role.
EXTRA={
 'training':['count','setting','composition','action','relationship'],
 'stage':['count','pose','composition','action'],
 'fan':['count','composition','action','relationship'],
 'camera':['count','composition','camera','setting'],
 'concept':['appearance','expression','pose','lighting','setting'],
 'wardrobe':['appearance'],
 'gesture':['pose','expression'],
 'appearance':['appearance'],
 'equipment':['appearance','composition'],
 'japan':['count','composition','appearance'],
 'virtual':['count','composition','setting'],
 'dark':['count','composition','setting','action','relationship'],
}

def main():
 if (O/'data-integration.json').exists():raise SystemExit('Already integrated; preserve evidence')
 O.mkdir(exist_ok=True)
 before=corpus.load(A);manifest_path=A/corpus.MANIFEST_NAME
 protected={p.name:sha(p) for p in A.glob('*.json')}
 write(O/'BASELINE.json',{'manifest':read(manifest_path),'source_hashes':protected,'candidate_count':len(before['candidates']),'binding_count':len(before['slot_bindings']),'retrieval_config':read(SKILL/'retrieval-runtime.json')})
 cards=read(H/'semantic-cards.json');contexts=read(H/'context-distinctions.json');sources=read(H/'sources.json');routes=read(H/'keyword-routes.json')
 new={};bindings={};mapping={};decisions=[]
 exact={(v.get('content',{}).get('en'),v.get('content',{}).get('ko')) for v in before['candidates'].values() if v['record_kind']!='diagnostic'}
 for card in cards:
  assert (card['phrase_en'],card['phrase_ko']) not in exact
  cid=ident('cand_',card['id']);mapping[card['id']]=cid
  meta={**copy.deepcopy(card),'candidate_id':cid,'registration_status':'authored_optional_source','runtime_importable':True,'native_qualification':'not_qualified','native_approval':False}
  roles=card['proposed_slots'];dims=sorted(set(EXTRA[card['family']])|{d for role in roles for d in before['slot_catalog'][role]['dimensions']})
  # Specific wardrobe carrier footprint; full authorial scenes retain conservative broad dimensions.
  wardrobe_only=(card['family']=='wardrobe' and set(dims)=={'appearance'})
  if card['id']=='I059':dims=sorted(set(dims)|{'count'})
  effects={'dimensions':dims,'properties':[]}
  if wardrobe_only:effects={'dimensions':['appearance'],'properties':[{'dimension':'appearance','target':'main_subject','property':'wardrobe'}]}
  cond={'for_any':['human']}
  if 'adult' in card['phrase_en'].lower():cond['requires_adult_context']=True
  new[cid]={'id':cid,'record_kind':'visual_option','content':{'en':card['phrase_en'],'ko':card['phrase_ko'],'definition':card['phrase_en'],'aliases':[card['name_ko']],'application_contract':CONTRACT,'research_semantics':meta},'conditions':cond,'effects':effects,'provenance':[{'source':'authored optional proposition docs/research-evidence/photo-prompt/idol-fiction-20261023/semantic-cards.json#'+card['id'],'sha256':sha(H/'semantic-cards.json')}]}
  for role in roles:
   bid=ident('bind_',cid+':'+role);bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':role,'role':'optional','semantic_role':before['slot_catalog'][role]['semantic_role'],'conditions':{'subject_applicability':{}},'weight':1}
  decisions.append({'card_id':card['id'],'candidate_id':cid,'status':'authored_visual_source_not_native_qualified','slots':roles,'source_support':card['source_support'],'all_old_sources_unchanged':True})
 for ctx in contexts:
  cid=ident('cand_',ctx['id']);mapping[ctx['id']]=cid
  meta={**copy.deepcopy(ctx),'candidate_id':cid,'registration_status':'excluded_context_diagnostic','runtime_importable':True}
  new[cid]={'id':cid,'record_kind':'diagnostic','content':{'definition':'Context diagnostic excluded from positive visual retrieval: '+ctx['name_ko']+'. '+ctx['meaning_boundary_ko']+' '+ctx['required_evidence_ko'],'research_semantics':meta},'conditions':{},'effects':{'dimensions':[],'properties':[]},'provenance':[{'source':'research context docs/research-evidence/photo-prompt/idol-fiction-20261023/context-distinctions.json#'+ctx['id'],'sha256':sha(H/'context-distinctions.json')}]}
 assert set(new).isdisjoint(before['candidates'])
 cm='photo_candidate_idol_fiction_20261023.json';bm='photo_candidate_idol_fiction_bindings_20261023.json';sm='photo_idol_fiction_semantics_20261023.json'
 for name in [cm,bm,sm]:assert not (A/name).exists()
 write(A/cm,{'schema':corpus.MODULE_SCHEMAS['candidates'],'candidates':new})
 write(A/bm,{'schema':corpus.MODULE_SCHEMAS['slot_bindings'],'slot_bindings':bindings})
 enriched_routes=[{**copy.deepcopy(r),'visual_candidate_ids':[mapping[c] for c in r['optional_component_card_ids']],'context_candidate_ids':[mapping[c] for c in r['context_card_ids']],'automatic_hard_activation':False} for r in routes]
 write(A/sm,{'schema':'photo-idol-fiction-visual-semantics/v1','cards':[{**copy.deepcopy(c),'candidate_id':mapping[c['id']],'runtime_importable':True,'registration_status':'authored_optional_source','native_qualification':'not_qualified','native_approval':False} for c in cards], 'context_distinctions':[{**copy.deepcopy(c),'candidate_id':mapping[c['id']],'runtime_importable':True,'registration_status':'excluded_context_diagnostic'} for c in contexts],'keyword_routes':enriched_routes,'sources':sources,'holds':read(H/'holds.json'),'native_approval':False,'automatic_hard_activation':False,'research_snapshot_sha256':sha(H/'semantic-cards.json')})
 assert sha(manifest_path)==protected[corpus.MANIFEST_NAME], 'Concurrent manifest update; reconcile before append'
 manifest=read(manifest_path)
 for fn,kind in [(cm,'candidates'),(bm,'slot_bindings')]:manifest['modules'].append({'file':fn,'kind':kind})
 write(manifest_path,manifest)
 after=corpus.load(A)
 assert all(after['candidates'][cid]==r for cid,r in before['candidates'].items())
 assert all(after['slot_bindings'][bid]==r for bid,r in before['slot_bindings'].items())
 assert all(after[k]==before[k] for k in ['slot_catalog','policies'])
 assert all(sha(A/name)==h for name,h in protected.items() if name!=corpus.MANIFEST_NAME)
 write(O/'new-native-records.json',new);write(O/'changed-native-records.json',{})
 write(O/'card-candidate-map.json',mapping)
 result={'status':'source_data_integrated','new_visual':len(cards),'new_diagnostics':len(contexts),'new_bindings':len(bindings),'keyword_routes':len(routes),'before_candidates':len(before['candidates']),'after_candidates':len(after['candidates']),'before_bindings':len(before['slot_bindings']),'after_bindings':len(after['slot_bindings']),'existing_records_bindings_catalog_policies_preserved':True,'old_asset_hashes_preserved_except_manifest':True,'source_files':[cm,bm,sm],'native_approval':False,'index_status':'not_run','decisions':decisions}
 write(O/'data-integration.json',result)
 print(json.dumps({k:v for k,v in result.items() if k!='decisions'},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
