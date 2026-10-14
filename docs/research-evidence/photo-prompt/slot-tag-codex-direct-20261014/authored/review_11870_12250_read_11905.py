"""Lossless source display; references denote exact canonical object/string equality.

Earlier ordinals are seeded only because this worker has already read them
completely. Call increasing contiguous windows, beginning at11905.
"""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=json.loads((R/'packets/11870-130.json').read_text());objects={};strings={}
start,stop=map(int,sys.argv[1:]);assert 11905<=start<stop<=12000

def display(v,path,emit):
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
 if isinstance(v,dict):return {k:display(x,path+'/'+k,emit) for k,x in v.items()}
 if isinstance(v,list):return [display(x,path+'/'+str(i),emit) for i,x in enumerate(v)]
 return v
for ordinal,cid in enumerate(p['ids'],11870):
 if ordinal>=stop:break
 value=display(p['records'][cid],str(ordinal),ordinal>=start)
 if ordinal>=start:
  print('ORDINAL',ordinal,cid)
  print(json.dumps(value,ensure_ascii=False,separators=(',',':')))
  print('COMPLETE_REFERENCE_CLOSURE',json.dumps(p['references'][cid],ensure_ascii=False,separators=(',',':')))
