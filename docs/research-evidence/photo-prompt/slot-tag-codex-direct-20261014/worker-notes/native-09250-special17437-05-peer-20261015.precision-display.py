# Mechanical reversible ID/RID factoring only. Does not judge meaning.
import json,hashlib,copy,importlib.util
from pathlib import Path
R=Path(__file__).resolve().parents[1]
S=importlib.util.spec_from_file_location('disp',R/'worker-notes/native-09250-special17437-05-peer-20261015.read.py');M=importlib.util.module_from_spec(S);S.loader.exec_module(M)
b=json.loads((R/'native_batches/review08250-17437-05/BATCH.json').read_text())['records'][0];p=b['proof'];d=json.loads((R/'authored/native_fresh_08250_17437_05_precision.json').read_text());n=json.loads((R/'worker-notes/native-09250-special17437-05-peer-20261015.proof-normalized.json').read_text());lookup={k:{json.dumps(x,sort_keys=True,ensure_ascii=False):i for i,x in enumerate(p[k])} for k in ['facts','source_units']};tm={k:{i:t for i,r,t in n[k]['occurrences']} for k in ['facts','source_units']}
def ptr(v,s):
 for k in s.strip('/').split('/'):v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
def norm(v,rid,hid):
 if isinstance(v,dict):return {k:norm(x,rid,hid) for k,x in v.items()}
 if isinstance(v,list):return [norm(x,rid,hid) for x in v]
 if isinstance(v,str):
  if v==hid:return '$HISTORICAL_ID'
  if v==rid:return '$RID'
  if v.startswith(rid+'_'):return '$RID_'+v[len(rid)+1:]
  return v.replace('/realization_content/'+rid+'/', '/realization_content/$RID/')
 return v
def den(v,rid,hid):
 if isinstance(v,dict):return {k:den(x,rid,hid) for k,x in v.items()}
 if isinstance(v,list):return [den(x,rid,hid) for x in v]
 if isinstance(v,str):
  if v=='$HISTORICAL_ID':return hid
  if v=='$RID':return rid
  if v.startswith('$RID_'):return rid+'_'+v[len('$RID_'):]
  return v.replace('/realization_content/$RID/', '/realization_content/'+rid+'/')
 return v
out={'method':'All new facts and units are exact-equality references to the reviewed proof templates with actual occurrence index retained. Local whole field exact matches current source. Old ID and RID prefix normalization is reversed and equality checked; old requires are retained. No semantic field deleted.' ,'templates':[],'occurrences':[]};seen={}
for i,x in enumerate(d['resolutions']):
 rid=x['realization_id'];hid=x['historical_fact_id'];v=copy.deepcopy(x);env={k:v.pop(k) for k in ['reviewed_occurrence_index','historical_fact_id','historical_fact_sha256']};actual={}
 for k,kind in [('fresh_canonical_fact','facts'),('fresh_normal_anchor','source_units'),('fresh_local_reference','source_units')]:
  ix=lookup[kind][json.dumps(v[k],sort_keys=True,ensure_ascii=False)];actual[k]=ix;v[k]={'exact_proof_kind':kind,'exact_proof_template':tm[kind][ix]}
 assert v['exact_local_full_text']==ptr(b['source_after'],v['exact_local_pointer']);v['exact_local_full_text']={'exact_current_field':v['exact_local_pointer']}
 z=norm(v,rid,hid);assert den(z,rid,hid)==v
 key=json.dumps(z,sort_keys=True,ensure_ascii=False)
 if key not in seen:seen[key]=len(out['templates']);out['templates'].append(z)
 ti=seen[key];env.update(realization_id=rid,template=ti,proof_occurrences=actual);out['occurrences'].append(env)
 # independently reconstruct all replaced values
 back=den(out['templates'][ti],rid,hid);back['exact_local_full_text']=ptr(b['source_after'],back['exact_local_pointer'])
 for k,kind in [('fresh_canonical_fact','facts'),('fresh_normal_anchor','source_units'),('fresh_local_reference','source_units')]:back[k]=p[kind][actual[k]]
 back.update({k:env[k] for k in ['reviewed_occurrence_index','historical_fact_id','historical_fact_sha256']});assert back==x
out['templates']=M.compact(out['templates']);q=R/'worker-notes/native-09250-special17437-05-peer-20261015.precision-normalized.json';assert not q.exists();q.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'templates':len(out['templates']),'occurrences':len(out['occurrences']),'roundtrip_exact':True,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()}))
