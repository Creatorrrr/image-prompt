import json,gzip,pathlib,sys
R=pathlib.Path(__file__).resolve().parents[1]
P=R/'native-inputs/prepared/review11870-01250-01300-03'
I=json.loads((P/'INPUT.json').read_text());PK=json.loads((P/'PREPARED-PACKET.json').read_text());B=json.loads((R/'native_batches/review11870-01250-01300-03/BATCH.json').read_text())
O=json.loads(gzip.decompress(pathlib.Path(I['original_snapshot']['file']).read_bytes()));C=json.loads(gzip.decompress(pathlib.Path(I['current_snapshot']['file']).read_bytes()))
start,stop=int(sys.argv[1]),int(sys.argv[2]);mode=sys.argv[3]
for x in B['records']:
 if not start<=x['ordinal']<stop:continue
 cid=x['candidate_id']
 if mode=='sources':
  seen=[];z={'ordinal':x['ordinal'],'candidate_id':cid}
  for field,value in [('original',PK['original_records'][cid]),('current',PK['current_records'][cid]),('native_before',x['source_before']),('native_after',x['source_after'])]:
   match=next((a for a,b in seen if b==value),None);z[field]=('EXACT_EQUAL_TO_'+match if match else value);seen.append((field,value))
  z['original_ownbindings']={k:v for k,v in O['slot_bindings'].items() if v.get('candidate_id')==cid}
  cb={k:v for k,v in C['slot_bindings'].items() if v.get('candidate_id')==cid};z['current_ownbindings']='EXACT_EQUAL_TO_ORIGINAL_OWNBINDINGS' if cb==z['original_ownbindings'] else cb
  z.update({k:x[k] for k in ['delta','rationale','status','dependency_records','reference_bindings','original_compiled']});z['required_closure']=PK['references'][cid];z['required_refbindings']=PK['reference_bindings'][cid]
 elif mode=='old':z={'ordinal':x['ordinal'],'old5B':PK['historical_compiled_rows'][cid]}
 elif mode=='proof':z={'ordinal':x['ordinal'],'candidate_id':cid,'proof':x['proof']}
 else:raise ValueError(mode)

 # Exact duplicate prose aliases only; no semantic field dropped or summarized.
 known=x['rationale']
 def aliases(v):
  if isinstance(v,dict):return {k:aliases(w) for k,w in v.items()}
  if isinstance(v,list):return [aliases(w) for w in v]
  if isinstance(v,str) and known and v==known:return {'exact_text_alias':'row_rationale_already_shown_in_sources'}
  if isinstance(v,str) and known and v.endswith(known):return {'exact_prefix':v[:-len(known)],'exact_suffix_alias':'row_rationale_already_shown_in_sources'}
  return v
 if mode=='sources':
  z['delta']=aliases(z['delta'])
 elif mode=='proof':z['proof']=aliases(z['proof'])
 print(json.dumps(z,ensure_ascii=False))
