"""Register reviewed mecha literals and diagnostics; preserve existing records."""
from pathlib import Path
import copy,hashlib,json,sys,uuid,collections,re
O=Path(__file__).resolve().parent;R=O.parents[3];ROOT=O.parents[4];S=ROOT/'skills/photo-prompt-image-generator';A=S/'assets';RESEARCH=O.parent
sys.path.insert(0,str(S/'scripts'))
import photo_candidate_corpus as corpus
read=lambda p:json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
NS=uuid.UUID('8b9ba548-98ca-4baa-9556-3ce444246ba6')
ident=lambda prefix,key:prefix+uuid.uuid5(NS,key).hex
def main():
 if (O/'data-integration.json').exists():raise SystemExit('Already integrated; preserve evidence.')
 before=corpus.load(A);cards=read(RESEARCH/'semantic-cards.json')['cards'];drafts={d['card_id']:d for d in read(RESEARCH/'candidate-drafts.json')['drafts']};contexts=read(RESEARCH/'context-boundaries.json')['contexts'];sources=read(RESEARCH/'source-registry.json')['sources'];src={s['id']:s for s in sources}
 write(O/'working-source-before.json',{'candidates':before['candidates'],'slot_bindings':before['slot_bindings'],'slot_catalog':before['slot_catalog'],'policies':before['policies']})
 hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in A.glob('*.json')}
 write(O/'source-hashes.before.json',hashes)
 existing={(r.get('content',{}).get('en',''),r.get('content',{}).get('ko','')):cid for cid,r in before['candidates'].items() if r['record_kind']!='diagnostic'}
 records={};bindings={};adoptions=[];enriched=[]
 for card in cards:
  c=copy.deepcopy(card);draft=drafts[c['id']];held=draft['planned_action']=='hold_for_source_plate_review';visual=not held
  cid=ident('cand_','mecha-robot:'+c['id']);dupe=existing.get((c['proposal_en'],c['proposal_ko']))
  if dupe:raise ValueError('Exact literal duplicate requires explicit reuse '+c['id']+' '+dupe)
  c.update(candidate_id=cid,registration_status='authored_source_module',runtime_registration=True,integration_status='held_diagnostic' if held else 'optional_visual_source',native_approval=False)
  if visual:
   content={'en':c['proposal_en'],'ko':c['proposal_ko'],'definition':'Optional complete authored visual realization: '+c['proposal_en'],'aliases':[c['title_ko']],'application_contract':draft['application_contract_draft'],'research_semantics':copy.deepcopy(c)}
   dims={d for slot in c['proposed_slots'] for d in before['slot_catalog'][slot]['dimensions']};dims.update(['subject','appearance'])
   if c['id'][0] in 'ACHIJ':dims.update(['action','relationship','pose'])
   effects={'dimensions':sorted(dims),'properties':[]}
  else:
   content={'definition':'Held source-specific diagnostic, excluded from positive retrieval: '+c['title_ko']+'. '+c['claim_limit_ko'],'research_semantics':copy.deepcopy(c)};effects={'dimensions':[],'properties':[]}
  records[cid]={'id':cid,'record_kind':'visual_option' if visual else 'diagnostic','content':content,'conditions':{},'effects':effects,'provenance':[{'source':'authored mecha research '+c['id']+'; bounded contextual citation '+src[x]['url'],'sha256':hashlib.sha256((RESEARCH/'semantic-cards.json').read_bytes()).hexdigest()} for x in c['source_ids']]}
  for slot in c['proposed_slots'] if visual else []:
   bid=ident('bind_',cid+':'+slot);bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional','semantic_role':before['slot_catalog'][slot]['semantic_role'],'conditions':{'subject_applicability':{}},'weight':2}
  adoptions.append({'card_id':c['id'],'candidate_id':cid,'action':'held_diagnostic' if held else 'new_specific_optional_realization','positive':visual,'existing_comparison_id':draft['existing_comparison_candidate_id'],'existing_source_mutated':False,'dedupe_scope':'all working positive EN/KO exact literal pairs; four prior full-record comparisons; no claim of exhaustive semantic equivalence review','reason':'Complete authored owner/count/topology or representation differs from broad existing labels. Generic existing options remain intact. Exact native qualification remains separate.'});enriched.append(c)
 for context in contexts:
  cid=ident('cand_','mecha-robot:context:'+context['id']);meta={**context,'candidate_id':cid,'native_approval':False,'registration_status':'context_diagnostic'}
  records[cid]={'id':cid,'record_kind':'diagnostic','content':{'definition':'Context-only, excluded from positive visual retrieval: '+context['title_ko']+'. '+context['claim_boundary_ko'],'research_semantics':meta},'conditions':{},'effects':{'dimensions':[],'properties':[]},'provenance':[{'source':src[x]['url'],'sha256':hashlib.sha256((RESEARCH/'context-boundaries.json').read_bytes()).hexdigest()} for x in context['source_ids']]}
 for filename,kind,body in [('photo_candidate_mecha_robot_20261024.json','candidates',records),('photo_candidate_mecha_robot_bindings_20261024.json','slot_bindings',bindings)]:
  p=A/filename
  if p.exists():raise ValueError('Never overwrite an existing module '+filename)
  write(p,{'schema':corpus.MODULE_SCHEMAS[kind],kind:body})
 manifest=read(A/corpus.MANIFEST_NAME)
 for f,k in [('photo_candidate_mecha_robot_20261024.json','candidates'),('photo_candidate_mecha_robot_bindings_20261024.json','slot_bindings')]:
  assert not any(m['file']==f for m in manifest['modules']);manifest['modules'].append({'file':f,'kind':k})
 write(A/corpus.MANIFEST_NAME,manifest)
 routes=read(RESEARCH/'term-coverage.json')['terms'];lookup={c['id']:c['candidate_id'] for c in enriched}
 for t in routes:t.update(candidate_ids=[lookup[x] for x in t['card_refs']],automatic_hard_activation=False)
 write(A/'photo_mecha_robot_semantics_20261024.json',{'schema':'photo-mecha-robot-visual-semantics/v1','cards':enriched,'context_boundaries':contexts,'term_routes':routes,'source_refs':sources,'native_approval':False,'automatic_activation':False})
 after=corpus.load(A)
 assert all(after['candidates'][cid]==record for cid,record in before['candidates'].items())
 assert all(after['slot_bindings'][bid]==record for bid,record in before['slot_bindings'].items())
 assert after['slot_catalog']==before['slot_catalog'] and after['policies']==before['policies']
 write(O/'new-native-records.json',records);write(O/'changed-native-records.json',{});write(O/'adoption-decisions.json',adoptions)
 report={'status':'source_data_integrated','new_records':len(records),'positive_records':sum(r['record_kind']=='visual_option' for r in records.values()),'diagnostic_records':sum(r['record_kind']=='diagnostic' for r in records.values()),'bindings':len(bindings),'semantic_cards':len(cards),'context_boundaries':len(contexts),'term_routes':len(routes),'held_cards':['G03','K06'],'existing_record_changes':0,'existing_records_bindings_catalog_policies_preserved':True,'before_candidates':len(before['candidates']),'after_candidates':len(after['candidates']),'native_approval':False,'index_runtime':'PENDING','candidate_mapping':{c['id']:c['candidate_id'] for c in enriched}}
 write(O/'data-integration.json',report);print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
