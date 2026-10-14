"""Lossless fresh source/reference/binding display for this worker's second block.

Only actually read earlier130 source records seed exact equality references.
"""
import json,sys,gzip
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=json.loads((R/'packets/12000-250.json').read_text());prior=json.loads((R/'packets/11870-130.json').read_text())
s=json.loads(gzip.decompress((R/'SOURCE.json.gz').read_bytes()))
objects={};strings={};start,stop=map(int,sys.argv[1:]);assert 12000<=start<stop<=12250

def display(v,path):
 key=json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
 if len(key)>45 and key in objects:return {'EXACT_OBJECT_AT':objects[key]}
 if len(key)>45:objects[key]=path
 if isinstance(v,str):
  if len(v)<45:return v
  if v in strings:return {'EXACT_STRING_AT':strings[v]}
  parts=[];tail=v
  while tail:
   matches=[(tail.find(old),-len(old),old,loc) for old,loc in strings.items() if len(old)>=45 and old in tail]
   if not matches:parts.append(tail);break
   at,_,old,loc=min(matches)
   if at:parts.append(tail[:at])
   parts.append({'EXACT_STRING_AT':loc});tail=tail[at+len(old):]
  strings[v]=path
  return {'LOSSLESS_CONCAT':parts} if any(isinstance(x,dict) for x in parts) else v
 if isinstance(v,dict):return {k:display(x,path+'/'+k) for k,x in v.items()}
 if isinstance(v,list):return [display(x,path+'/'+str(i)) for i,x in enumerate(v)]
 return v
for ordinal,cid in enumerate(prior['ids'],11870):display(prior['records'][cid],str(ordinal))
def bindings(v):
 if isinstance(v,dict):
  for k,x in v.items():
   if k=='binding_id':yield x
   yield from bindings(x)
 elif isinstance(v,list):
  for x in v:yield from bindings(x)
for ordinal,cid in enumerate(p['ids'],12000):
 if ordinal>=stop:break
 value=display(p['records'][cid],str(ordinal))
 refs=display(p['references'][cid],f'{ordinal}/COMPLETE_REFERENCE_CLOSURE')
 bids=sorted(set(bindings(p['records'][cid]))|set(bindings(p['references'][cid])))
 bvalue=display({b:s['slot_bindings'][b] for b in bids},f'{ordinal}/FROZEN_MEMBER_BINDINGS')
 if ordinal>=start:
  print('ORDINAL',ordinal,cid);print(json.dumps(value,ensure_ascii=False,separators=(',',':')))
  print('COMPLETE_REFERENCE_CLOSURE',json.dumps(refs,ensure_ascii=False,separators=(',',':')))
  print('FROZEN_MEMBER_BINDINGS',json.dumps(bvalue,ensure_ascii=False,separators=(',',':')))
