"""Repair representation errors without calling the repair independent review.

Unresolved ownership/meaning/quotes are queued for a fresh source-based model
adjudication. No unvalidated response becomes a native source or binding.
"""
from pathlib import Path
import copy,gzip,json,sys
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from validate_reviews import validate,pointer,NEGATIVE

def strings(value,path=''):
 if isinstance(value,str):yield path,value
 elif isinstance(value,dict):
  for key,x in value.items():yield from strings(x,path+'/'+str(key).replace('~','~0').replace('/','~1'))
 elif isinstance(value,list):
  for n,x in enumerate(value):yield from strings(x,path+'/'+str(n))

def normalize(raw,record,catalog):
 review=copy.deepcopy(raw);changes=[]
 available=[]
 for p,s in strings(record['content'],'/content'):
  try:pointer(record,p);available.append((p,s))
  except ValueError:pass
 def quote(f):
  try:
   if f['quote'] in pointer(record,f['pointer']):return
  except (ValueError,KeyError,TypeError,IndexError):pass
  matches=[(p,s) for p,s in available if f['quote'] in s]
  if matches:
   p,_=min(matches,key=lambda x:(len(x[0]),x[0]));old=f['pointer'];f['pointer']=p;changes.append({'type':'same_exact_positive_quote_pointer','before':old,'after':p,'quote':f['quote']})
 for role in review['roles']:
  spec=catalog[role['slot_id']]
  if role['semantic_role']!=spec['semantic_role']:
   changes.append({'type':'catalog_contract_semantic_role','slot':role['slot_id'],'before':role['semantic_role'],'after':spec['semantic_role']});role['semantic_role']=spec['semantic_role']
  for f in role['evidence']:
   quote(f)
   if f['dimension'] not in spec['dimensions'] and len(spec['dimensions'])==1:
    changes.append({'type':'catalog_contract_dimension','slot':role['slot_id'],'property':f['property'],'before':f['dimension'],'after':spec['dimensions'][0]});f['dimension']=spec['dimensions'][0]
 for f in review['facts']:quote(f)
 corrections=[];metadata=[]
 for fix in review['corrections']:
  if fix['pointer'].startswith('/content/'):
   corrections.append(fix)
  elif fix['pointer']=='/record_kind' and fix['before']==record['record_kind'] and fix['after']==review['recommended_kind']:
   metadata.append(fix);changes.append({'type':'kind_correction_already_in_recommended_kind','pointer':fix['pointer']})
  elif fix['pointer'].startswith('/effects/'):
   metadata.append(fix);changes.append({'type':'effect_suggestion_is_metadata_not_text_replacement','pointer':fix['pointer']})
  else:corrections.append(fix)
 review['corrections']=corrections
 return review,changes,metadata

def main():
 source=json.loads(gzip.decompress((HERE/'REVIEW-SOURCE.json.gz').read_bytes()));out=HERE/'normalized-reviews';out.mkdir(exist_ok=True);count=0;invalid={}
 for file in sorted((HERE/'model-reviews').glob('*.json')):
  if file.name.endswith('.errors.json') or '.attempt-' in file.name:continue
  original=json.loads(file.read_text());rows=[]
  for raw in original['reviews']:
   cid=raw['id'];r,changes,metadata=normalize(raw,source['candidates'][cid],source['slot_catalog']);problems=validate(r,source['candidates'][cid],source['slot_catalog']);count+=1
   rows.append({'review':r,'original_response_file':str(file.relative_to(HERE)),'representation_repairs':changes,'metadata_suggestions':metadata,'mechanical_errors':problems,'mechanical_validation':'fail' if problems else 'pass','independent_semantic_review':False})
   if problems:invalid[cid]=problems
  target=out/file.name;target.write_text(json.dumps({'ids':original['ids'],'source_sha256':original['source_sha256'],'rows':rows},ensure_ascii=False,indent=2)+'\n')
 (HERE/'ADJUDICATION-QUEUE.json').write_text(json.dumps({'reviewed':count,'invalid_count':len(invalid),'invalid':invalid},ensure_ascii=False,indent=2)+'\n');print(json.dumps({'reviewed':count,'invalid_count':len(invalid)}))
if __name__=='__main__':main()
