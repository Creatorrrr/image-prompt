"""Lossless exact-value repetition view; no semantic grouping/classification."""
import pathlib,json,sys,hashlib
R=pathlib.Path(__file__).resolve().parents[1];B=json.loads((R/'native_batches/review08250-17437-03/BATCH.json').read_text())['records'][0];P=json.loads((R/'native-inputs/prepared/review08250-17437-03/PREPARED-PACKET.json').read_text());seen={}
def compact(v,path):
 key=json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
 if isinstance(v,(dict,list,str)) and len(key)>25:
  if key in seen:return {'exact_equal_to':seen[key],'canonical_sha256':hashlib.sha256(key.encode()).hexdigest()}
  seen[key]=path
 if isinstance(v,dict):return {k:compact(x,path+'/'+k) for k,x in v.items()}
 if isinstance(v,list):return [compact(x,path+'/'+str(i)) for i,x in enumerate(v)]
 return v
mode=sys.argv[1]
if mode=='historical':
 v=P['historical_compiled_rows'][B['candidate_id']];print(json.dumps(compact(v,'historical_compiled_row'),ensure_ascii=False))
elif mode=='common':
 v={k:({a:z for a,z in x.items() if a!='realization_content'} if k=='content' else x) for k,x in B['source_after'].items()};print(json.dumps(compact(v,'source_after'),ensure_ascii=False))
elif mode=='branches':
 # Always print baseline first so exact-common references have directly visible full antecedents.
 v=B['source_after']['content']['realization_content'];ids=list(v);compact(v['baseline'],'/content/realization_content/baseline');selected=[k for k in ids[int(sys.argv[2]):int(sys.argv[3])] if k!='baseline']
 for rid in selected:
  raw=v[rid];z=json.loads(json.dumps(raw));base='/content/realization_content/'+rid
  joined=' '.join(raw['concept_units'])
  for field in ['en','embedding_text']:
   assert raw[field]==joined;z[field]={'exact_space_join_of':[base+'/concept_units/'+str(j) for j in range(len(raw['concept_units']))],'string_sha256':hashlib.sha256(joined.encode()).hexdigest()}
  assert raw['semantics']['definition']==joined;z['semantics']['definition']={'exact_equal_to':base+'/en'}
  ko0=v['baseline']['ko'];assert raw['ko'].startswith(ko0)
  z['ko']={'exact_prefix':'/content/realization_content/baseline/ko','remaining_exact_suffix':raw['ko'][len(ko0):],'whole_string_sha256':hashlib.sha256(raw['ko'].encode()).hexdigest()}
  assert raw['semantics']['paraphrase_examples']==[raw['ko']];z['semantics']['paraphrase_examples']=[{'exact_equal_to':base+'/ko'}]
  print(json.dumps({rid:compact(z,base)},ensure_ascii=False))
