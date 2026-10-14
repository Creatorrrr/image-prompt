"""Lossless display of exact input rows; not a semantic classifier or read counter."""
from pathlib import Path
import json,sys,hashlib
P=Path(__file__).with_name('native_06250_08250_09250.inputs.json')
data=json.loads(P.read_text());start,stop=map(int,sys.argv[1:3]);assert 8250<=start<stop<=9250
sha=lambda x:hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
for row in data['records'][start-8250:stop-8250]:
 print('WHOLE',row['ordinal'],row['candidate_id'],'actualRIDs',row['actual_current_realization_ids'])
 print('ORIGINAL',json.dumps(row['original_source'],ensure_ascii=False,separators=(',',':')))
 for key in ['five_b_source_after','current_source']:
  print(key, 'EXACT canonical equality to ORIGINAL '+row[key+'_sha256'] if row[key]==row['original_source'] else json.dumps(row[key],ensure_ascii=False,separators=(',',':')))
 # Exact equal whole-string references, never summary/keywords/substrings.
 strings={}
 def remember(value,pointer):
  if isinstance(value,str):strings.setdefault(value,pointer)
  elif isinstance(value,dict):
   for key,child in value.items():remember(child,pointer+'/'+key.replace('~','~0').replace('/','~1'))
  elif isinstance(value,list):
   for i,child in enumerate(value):remember(child,pointer+'/'+str(i))
 remember(row['original_source'],'original_source')
 def lossless(value):
  if isinstance(value,str) and len(value)>40 and value in strings:
   return {'EXACT_STRING_EQUAL_TO':strings[value],'sha256':sha(value)}
  if isinstance(value,dict):return {k:lossless(v) for k,v in value.items()}
  if isinstance(value,list):return [lossless(v) for v in value]
  return value
 print('REGISTERED5B',json.dumps(lossless(row['original_compiled']),ensure_ascii=False,separators=(',',':')))
 print('ORIGINAL_OWN',json.dumps(row['original_own_bindings'],ensure_ascii=False,separators=(',',':')))
 print('CURRENT_OWN','EXACT canonical equality to ORIGINAL_OWN' if row['current_own_bindings']==row['original_own_bindings'] else json.dumps(row['current_own_bindings'],ensure_ascii=False,separators=(',',':')))
 print('ORIGINAL_CLOSURE',json.dumps(row['original_closure'],ensure_ascii=False,separators=(',',':')))
 print('CURRENT_CLOSURE','EXACT canonical equality to ORIGINAL_CLOSURE' if row['current_closure']==row['original_closure'] else json.dumps(row['current_closure'],ensure_ascii=False,separators=(',',':')))
