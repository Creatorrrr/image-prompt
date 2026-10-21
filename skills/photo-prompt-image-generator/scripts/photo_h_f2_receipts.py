"""Issued material evidence is separate from native adoption authority."""
from pathlib import Path
import uuid
import photo_candidate_corpus as c
import photo_recall_first as rf
from photo_recall_generation import read,write,file_sha
from photo_workflow_state import value
from photo_h_f2_generation import Generation
from photo_h_f2_query_scope import analyze, correct, compile_focus_contracts, order_focus
from photo_h_f2_search import fuse, known_row_contributions, present_material
from photo_h_f2_literal_text import compile_contracts, order_literal
from photo_h_f2_event_phase import compile_contracts as phase_contracts, order_phase

def issue(generation,packet,raw,native_pack,native_receipt):
 rf.require(packet['generation_id']==generation.id,'wrong material generation')
 audit_packet(generation,packet,raw)
 receipt={'schema':'photo-h-f2-receipt/v1','request_id':uuid.uuid4().hex,'generation_id':generation.id,
  'material_sha256':packet['canonical_sha256'],'raw_files':packet['raw_files'],
  'native_pack_sha256':c.digest(native_pack),'native_receipt_sha256':c.digest(native_receipt),'native_approval':False}
 receipt['canonical_sha256']=c.digest(receipt)
 write(generation.store/'h-f2-receipts'/(receipt['request_id']+'.json'),receipt)
 return receipt

def verify_bound(state):
 binding=state['h_f2_binding'];generation=Generation(binding['store'],binding['generation_id'])
 packet=value(state,'h_f2_material');receipt=value(state,'h_f2_receipt')
 issued=read(generation.store/'h-f2-receipts'/(receipt['request_id']+'.json'))
 rf.require(receipt==issued and receipt['schema']=='photo-h-f2-receipt/v1','receipt was not issued by this runtime')
 rf.require(receipt['canonical_sha256']==c.digest({k:v for k,v in receipt.items() if k!='canonical_sha256'}),'receipt checksum mismatch')
 rf.require(packet['canonical_sha256']==c.digest({k:v for k,v in packet.items() if k!='canonical_sha256'})==receipt['material_sha256'],'material checksum mismatch')
 rf.require(packet['generation_id']==receipt['generation_id']==generation.id,'mixed material generation')
 rf.require(c.digest(value(state,'pack'))==receipt['native_pack_sha256'] and c.digest(value(state,'runtime_receipt'))==receipt['native_receipt_sha256'],'native audit evidence changed')
 rf.require(packet['query_set']['core_sha256']==c.digest(value(state,'authorial_core_normalized')),'material core changed')
 for p,h in receipt['raw_files'].items():
  rf.require(Path(p).name==p and file_sha(Path(binding['raw_directory'])/p)==h,'raw scores changed')
 rf.require(packet['native_approval'] is False and receipt['native_approval'] is False,'material grants no native authority')
 from photo_h_f2_queries import prepare
 from photo_workflow import _sealed_slot_plan
 plan,material=_sealed_slot_plan(state)
 rf.require(packet['query_set']==prepare(material['core'],material['controls'],material['catalog'],plan),'bound goal or H input changed')
 rf.require(generation.manifest['native_generation_id']==value(state,'runtime_receipt')['generation_id'],'native generation changed')
 audit_packet(generation,packet,binding['raw_directory'])
 return packet

def audit_packet(generation,packet,raw):
 """Reconstruct saved rankings, without querying the corpus or invoking a model."""
 import numpy as np
 rf.require(set(packet['goals'])==set(packet['queries'])==set(packet['query_set']['slots']),'goal/query scope changed')
 sources=set();ids=[m['id'] for m in generation.metadata]
 documents={d['id']:d['text'] for d in read(generation.root/'documents.json.gz')['rows']}
 contracts=compile_contracts(documents,rf.tokens,source_units=generation.primary_units)
 phases=phase_contracts(documents,rf.tokens,source_units=generation.primary_units)
 focuses=compile_focus_contracts(documents,source_units=generation.primary_units,source_effects=generation.effect_footprint,source_constraints=generation.focus_constraints)
 for slot,goal in packet['goals'].items():
  q=packet['query_set']['slots'][slot];row=packet['queries'][slot]['row']
  rf.check_embedding(row,generation.binding,q['text'],'query')
  rf.require(goal['lane_calls']=={'BM25F':1,'local_cosine':1},'extra or missing search invocation')
  rf.require(goal['considered_RIDs']==len(ids) and goal['considered_CIDs']==generation.manifest['CID_count'],'not whole positive pool')
  path=Path(raw)/(rf.sha(slot)+'.npz')
  rf.require(path.name in packet['raw_files'] and file_sha(path)==packet['raw_files'][path.name],'raw data not bound')
  with np.load(path) as saved:
   sparse=saved['bm25'];raw_sparse=saved['bm25_raw'];dense=saved['cosine'];order=list(saved['order'])
   rf.require(raw_sparse.shape==sparse.shape and np.isfinite(raw_sparse).all() and (raw_sparse>=0).all(),'invalid original lexical scores')
   analysis=analyze(q['text'],rf.tokens)
   corrected,_order,correction=correct(generation.metadata,raw_sparse,dense,analysis,rf.tokens,fuse,
    lambda i:known_row_contributions(generation.fields,q['text'],rf.tokens,i),lambda i:documents[ids[i]],
    lambda term:len(generation.fields['postings'].get(term,())))
   rf.require(np.array_equal(np.asarray(corrected),sparse),'bounded lexical correction changed')
   rf.require(sparse.shape==dense.shape==(len(ids),),'wrong raw score population')
   rf.require(np.isfinite(sparse).all() and (sparse>=0).all() and np.isfinite(dense).all(),'invalid saved scores')
   lr={i:r for r,i in enumerate(sorted((i for i,s in enumerate(sparse) if s>0),key=lambda i:(-float(sparse[i]),ids[i])),1)}
   dr={i:r for r,i in enumerate(sorted(range(len(ids)),key=lambda i:(-float(dense[i]),ids[i])),1)}
   scores=[(1/(10+lr[i]) if i in lr else 0.)+1/(10+dr[i]) for i in range(len(ids))]
   seen=set();expected=[]
   for i in sorted(range(len(ids)),key=lambda i:(-scores[i],ids[i])):
    cid=generation.metadata[i]['cid']
    if cid not in seen:seen.add(cid);expected.append(i)
   full=[]
   for i in expected:
    d=generation.metadata[i]
    full.append({'id':d['id'],'cid':d['cid'],'rid':d['rid'],'bm25':float(sparse[i]),'cosine':float(dense[i]),'bm25_rank':lr.get(i),'dense_rank':dr[i],'rrf':scores[i]})
   full,focus=order_focus(full,q['text'],focuses)
   full,literal=order_literal(full,q['text'],analysis,contracts,rf.tokens)
   full,phase=order_phase(full,q['text'],analysis,phases,rf.tokens)
   rf.require([ids[i] for i in order]==[row['id'] for row in full],'saved full order is not witnessed phase/literal/RRF10 order')
   rf.require(goal.get('query_scope')=={'analysis':analysis,'correction':correction,'literal_text':literal,'primary_focus':focus,'event_phase':phase},'lexical, literal or event-phase scope changed')
   rf.require(c.digest(full)==goal['full_order_sha256'],'full order trace changed')
   presented,projection=present_material(full,phase,literal=literal,focus=focus)
   rf.require(goal.get('material_projection')==projection,'material source-witness projection changed')
   rf.require(len(goal['top8'])==len(presented),'source-witnessed top8 budget changed')
   for row,expected in zip(goal['top8'],presented,strict=True):
    rf.require(all(row[k]==v for k,v in expected.items()),'top8 CID/RID/score changed')
    source=packet['sources'][row['cid']];record=generation.body.record(row['cid'])
    rf.require(source==record and row['source_sha256']==c.digest(record),'mixed candidate source')
    rf.require(row['rid'] in record['meaning']['primary'] and row['native_approval'] is False,'foreign realization or authority')
    sources.add(row['cid'])
 rf.require(sources==set(packet['sources']),'extra unreturned source in material pool')
 return {'status':'pass','goals':len(packet['goals']),'additional_search_calls':0,'model_calls':0}

def audit_decisions(state,composed):
 packet=verify_bound(state)
 rows=composed.get('h_f2_material_decisions',[])
 rf.require(isinstance(rows,list),'material decisions must be an authored list')
 seen=set()
 for row in rows:
  rf.require(isinstance(row,dict) and set(row)=={'slot','candidate_id','realization_id','source_sha256','use','rationale'},'explicit material decision fields required')
  key=(row['slot'],row['candidate_id'],row['realization_id'])
  rf.require(key not in seen,'duplicate material decision');seen.add(key)
  goal=packet['goals'].get(row['slot'],{})
  source=next((r for r in goal.get('top8',[]) if r['cid']==row['candidate_id'] and r['rid']==row['realization_id']),None)
  rf.require(source is not None and source['source_sha256']==row['source_sha256'],'decision refers to foreign material')
  rf.require(row['use'] in ('skip','inspiration_only') and isinstance(row['rationale'],str) and row['rationale'].strip(),'material is not a native adoption authority')
 return packet
