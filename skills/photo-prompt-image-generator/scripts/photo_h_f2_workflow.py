"""Managed H-F2 material retrieval, alongside unchanged native composition gates."""
from pathlib import Path
import uuid
import secrets
import photo_h_f2_sampling as sampling
import numpy as np
import photo_candidate_corpus as c
import photo_canonical_source as canonical
import photo_recall_first as rf
from photo_recall_generation import read,write,file_sha
from photo_workflow_state import WorkflowError,locked_state,value,encode,commit_stage,atomic_write
import photo_h_f2_queries as queries
from photo_h_f2_generation import Generation
from photo_h_f2_search import present_material

def cached_queries(generation,query_set,cache,skill=None):
 cache=Path(cache);cache.mkdir(parents=True,exist_ok=True);out={};missing=[]
 for slot,q in query_set['slots'].items():
  key=c.digest({'text':q['text'],'binding':generation.binding});path=cache/(key+'.json')
  if path.exists():
   item=read(path);rf.require(item['text']==q['text'] and item['binding']==generation.binding,'wrong cached input')
   rf.check_embedding(item['row'],generation.binding,q['text'],'query');out[slot]={'row':item['row'],'cache_hit':True}
  else:missing.append((slot,q,path))
 if missing:
  from photo_h_f2_encoder import LocalEncoder
  with LocalEncoder(skill or Path(__file__).resolve().parents[1]) as encoder:
   rf.require(encoder.binding==generation.binding,'installed local model differs from generation')
   rows=encoder.encode([q['text'] for _,q,_ in missing],'query')
  for (slot,q,path),row in zip(missing,rows,strict=True):
   rf.check_embedding(row,generation.binding,q['text'],'query')
   write(path,{'text':q['text'],'binding':generation.binding,'row':row});out[slot]={'row':row,'cache_hit':False}
 return out

def search_material(generation,query_set,cache,output,*,skill=None,creativity=1,sampling_seed=None):
 output=Path(output);output.mkdir(parents=True,exist_ok=True)
 journal=output/'transaction.json'
 rf.require(not journal.exists(),'incomplete or completed retrieval exists; reuse issued evidence, never restart it')
 seed = secrets.randbits(128) if sampling_seed is None else sampling_seed
 settings = sampling.policy(creativity)
 write(journal,{'state':'started','generation_id':generation.id,'query_set_sha256':c.digest(query_set),
                'sampling_seed':seed,'sampling_policy':settings})
 encoded=cached_queries(generation,query_set,cache,skill);index=generation.index();goals={};sources={};files={}
 for slot,q in query_set['slots'].items():
  result=index.search(q['text'],encoded[slot]['row'],generation.binding)
  p=output/(rf.sha(slot)+'.npz')
  positions={d['id']:i for i,d in enumerate(generation.metadata)}
  with p.open('wb') as stream:np.savez_compressed(stream,bm25=np.asarray(result['bm25']),bm25_raw=np.asarray(result['bm25_raw']),cosine=result['cosine'],order=np.asarray([positions[r['id']] for r in result['order']],dtype='<i4'))
  files[p.name]=file_sha(p);rows=[]
  window,projection=present_material(result['order'],result['query_scope']['event_phase'],literal=result['query_scope']['literal_text'],focus=result['query_scope']['primary_focus'],maximum=settings['rank_window'])
  presented,sample_evidence=sampling.sample(window,creativity,seed,slot,q['text_sha256'])
  for r in presented:
   source=generation.body.record(r['cid']);m=generation.metadata[positions[r['id']]]
   rf.require(c.digest(source)==m['source_sha256'],'returned source changed')
   sources[r['cid']]=source;rows.append({**r,'source_sha256':m['source_sha256'],'native_approval':False})
  goals[slot]={'candidates':rows,'sampling':sample_evidence,'material_projection':projection,'lane_calls':result['lane_calls'],'considered_RIDs':result['considered_RIDs'],
   'considered_CIDs':result['considered_CIDs'],'full_order_sha256':c.digest(result['order']),'query_scope':result['query_scope']}
 packet={'schema':'photo-h-f2-material-pack/v2','sampling_seed':seed,'sampling_policy':settings,'generation_id':generation.id,'query_set':query_set,'queries':encoded,
  'goals':goals,'sources':sources,'raw_files':files,'native_approval':False,'semantic_approval':False,
  'authority':'creative reference only; whole-source adoption requires the native selection contract'}
 packet['canonical_sha256']=c.digest(packet);write(output/'material.json',packet)
 write(journal,{'state':'completed','generation_id':generation.id,'material_sha256':packet['canonical_sha256']})
 return packet

def retrieve(args):
 import photo_workflow as workflow
 import photo_slot_expression as expression
 from photo_runtime_sources import RuntimeSnapshotProvider
 import prompt_generator as g
 with locked_state(args.run) as state:
  workflow.ensure(state)
  if not args.generation_id or not args.runtime_store:raise WorkflowError('h_f2_requires_explicit_generation_and_store')
  if args.seed not in (None,0) or args.visual_intent or args.source_remote or args.embedding_env_file:raise WorkflowError('h_f2_unsupported_override')
  if args.precap or args.retrieval_mode!='hybrid_required' or args.source_mode!='local_current':raise WorkflowError('h_f2_requires_local_hybrid_without_precap')
  if 'slot_expression_plan' not in state['artifacts']:
   material=workflow._slot_material(args.run,state,args.slot)
   return {'status':'needs_slot_intent_authoring','material':material}
  plan,material=workflow._sealed_slot_plan(state,args.slot)
  if 'h_f2_receipt' in state['artifacts']:
   from photo_h_f2_receipts import verify_bound
   verify_bound(state)
   if args.generation_id!=state['h_f2_binding']['generation_id'] or str(args.runtime_store.resolve())!=state['h_f2_binding']['store']:raise WorkflowError('h_f2_reuse_binding_changed')
   return {'status':'pass','reused':True,'additional_lane_calls':0}
  if 'pack' in state['artifacts'] or state['phase']!='slot_intents_authored':raise WorkflowError('h_f2_requires_unretrieved_authored_run')
  generation=Generation(args.runtime_store,args.generation_id)
  native_id=generation.manifest.get('native_generation_id')
  if not native_id:raise WorkflowError('h_f2_requires_pinned_native_audit_generation')
  provider=RuntimeSnapshotProvider(store=args.runtime_store);snapshot=provider.load_generation(native_id)
  rf.require(snapshot.manifest['search_layout']['corpus_sha256']==read(generation.root/'source-manifest.json')['source_sha256'],'native and H-F2 source differ')
  native_catalog=snapshot.data['slot_catalog']
  if expression.specification(native_catalog)!=material['catalog']:raise WorkflowError('h_f2_catalog_generation_mismatch')
  from photo_validation_context import build as build_validation_context
  validation_context=build_validation_context(snapshot.data,material['core'],material['controls'],value(state,'embodiment_review'))
  validation_receipt=provider.receipt(snapshot,validation_context)
  queryset=queries.prepare(material['core'],material['controls'],material['catalog'],plan)
  output=Path(args.run).resolve()/'.staging/h-f2'
  packet=search_material(generation,queryset,args.query_cache or Path(args.runtime_store)/'h-f2-query-cache',output,skill=getattr(args,'local_embedding_skill',None),creativity=g.creative_controls.runtime_values(material['controls'])['creativity'])
  from photo_h_f2_receipts import issue
  receipt=issue(generation,packet,output,validation_context,validation_receipt)
  commit_stage(args.run,state,'pack_bound',{'pack':encode(validation_context),'runtime_receipt':encode(validation_receipt),
   'h_f2_material':encode(packet),'h_f2_receipt':encode(receipt)},metadata={
    'source_binding':{'generation_id':native_id,'source_fingerprint':validation_receipt['source_fingerprint'],'runtime_store':str(args.runtime_store.resolve()),'slot_expression_plan_sha256':plan['canonical_sha256']},
    'h_f2_binding':{'generation_id':generation.id,'store':str(args.runtime_store.resolve()),'raw_directory':str(output)},'retrieval_seed':packet['sampling_seed']})
  return {'status':'pass','phase':'pack_bound','policy':queries.RECIPE,
   'searched_slots':sum(scope=='slot' for scope in queryset['query_scopes'].values()),
   'searched_whole_scene_queries':sum(scope!='slot' for scope in queryset['query_scopes'].values()),
   'searched_queries':len(queryset['slots']),'native_candidates_automatically_adopted':0}

def view(state,candidate_ids=None,page=0):
 from photo_h_f2_receipts import verify_bound
 packet=verify_bound(state);requested=set(candidate_ids or [])
 rf.require(type(page) is int and page>=0,'nonnegative material page required')
 ordered=[]
 for position in range(max((len(sampling.candidates(g)) for g in packet['goals'].values()),default=0)):
  for slot in sorted(packet['goals']):
   rows=sampling.candidates(packet['goals'][slot])
   if position<len(rows) and rows[position]['cid'] not in ordered:ordered.append(rows[position]['cid'])
 rf.require(len(requested)<=64,'detail view budget is64 unique sources')
 displayed=set(ordered[page*64:(page+1)*64]) if not requested else requested
 rf.require(not requested or requested<=set(packet['sources']),'candidate not in material pack')
 goals={}
 for slot,result in packet['goals'].items():
  rows=[]
  for row in sorted(sampling.candidates(result),key=lambda r:r['cid']):
   if row['cid'] not in displayed:continue
   source=packet['sources'][row['cid']]
   rows.append({'candidate_id':row['cid'],'realization_id':row['rid'],'native':canonical.native(source),
    'meaning':canonical.units(source,row['rid']),'conditions':source['conditions'],'effects':source['effects'],
    'source_sha256':row['source_sha256'],'native_approval':False,'application':'unreviewed;preserve complete source and requester constraints'})
  goals[slot]=rows
 from compose_pack_view import build_view
 return {'schema':'photo-h-f2-material-view/v1','material_page':page,'total_unique_materials':len(ordered),'displayed_unique_materials':len(displayed),'additional_search_calls':0,'materials':goals,
  'query_scopes':packet['query_set']['query_scopes'],
  'material_projections':{slot:goal['material_projection'] for slot,goal in packet['goals'].items()},('validation_context' if value(state,'pack').get('contract_version')=='photo-validation-context/v1' else 'native_guard_contract'):build_view(value(state,'pack')),
  'authority':'inspiration is separate from complete native adoption','native_approval':False}
