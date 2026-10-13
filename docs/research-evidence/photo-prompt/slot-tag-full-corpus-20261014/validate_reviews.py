"""Mechanical review provenance checks are not a second semantic judgement."""
from pathlib import Path
import gzip,json,sys,collections
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'))
import photo_candidate_corpus as c
from photo_contracts import AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS as DIMENSIONS
NEGATIVE={'confusion_boundaries','research_confusions','confounders','failure_modes','excluded','exclusions','forbidden','avoid','negative','research_source_urls','tags','facets'}

def pointer(record,p):
 if not isinstance(p,str) or not p.startswith('/content/'):raise ValueError('quote must point into primary positive content: '+str(p))
 value=record
 if p.startswith('/content/activation/') and not any(p.startswith('/content/activation/'+key+'/') for key in ['exact_terms','project_glossary_aliases']):raise ValueError('activation policy is not visual evidence: '+p)
 for raw in p[1:].split('/'):
  key=raw.replace('~1','/').replace('~0','~')
  if key in NEGATIVE:raise ValueError('negative, routing or origin field used as a visual fact: '+p)
  value=value[int(key)] if isinstance(value,list) else value[key]
 if not isinstance(value,str):raise ValueError('quote target is not a source string: '+p)
 return value

def check_fact(record,fact):
 if not isinstance(fact,dict):raise ValueError('fact is not an object')
 value=pointer(record,fact['pointer']);quote=fact['quote']
 if not isinstance(quote,str) or not quote.strip() or quote not in value:raise ValueError('quote differs from source: '+str(quote)[:100])
 if fact['dimension'] not in DIMENSIONS:raise ValueError('unknown dimension: '+fact['dimension'])
 for key in ['target','property']:
  if not isinstance(fact[key],str) or not fact[key].strip() or '*' in fact[key] or fact[key].endswith('.') or fact[key].casefold() in {'unknown','unspecified'}:raise ValueError('unspecific owned property')
 return {k:fact[k] for k in ['dimension','target','property']}

def validate(review,record,catalog):
 errors=[]
 if review['id']!=record['id'] or review.get('all_roles_considered') is not True:errors.append('coverage')
 if review.get('recommended_kind') not in c.KINDS:errors.append('kind')
 slots=[]
 for role in review['roles']:
  tag=role['slot_id'];slots.append(tag)
  try:
   spec=catalog[tag]
   if role['semantic_role']!=spec['semantic_role']:raise ValueError('wrong direct/contextual role')
   if role['scope'] not in {'whole_record','positive_alternative'}:raise ValueError('unknown scope')
   if not role['evidence']:raise ValueError('empty role evidence')
   for f in role['evidence']:
    p=check_fact(record,f)
    if p['dimension'] not in spec['dimensions']:raise ValueError('property outside role dimensions')
    if not any(p['property']==prefix.rstrip('.') or p['property'].startswith(prefix if prefix.endswith('.') else prefix+'.') for prefix in spec['property_prefixes']):raise ValueError('property outside role meaning path')
  except (ValueError,KeyError,TypeError,IndexError) as e:errors.append('role '+tag+': '+str(e))
 if len(slots)!=len(set(slots)):errors.append('duplicate role')
 for f in review['facts']:
  try:check_fact(record,f)
  except (ValueError,KeyError,TypeError,IndexError) as e:errors.append('fact: '+str(e))
 for fix in review['corrections']:
  try:
   if pointer(record,fix['pointer'])!=fix['before']:raise ValueError('correction is not exact source string')
   if not isinstance(fix['after'],str) or not fix['after'].strip():raise ValueError('empty replacement')
  except (ValueError,KeyError,TypeError,IndexError) as e:errors.append('correction: '+str(e))
 return errors

def main():
 source=json.loads(gzip.decompress((HERE/'REVIEW-SOURCE.json.gz').read_bytes()));seen={};issues={}
 for file in sorted((HERE/'model-reviews').glob('*.json')):
  if file.name.endswith('.errors.json') or '.attempt-' in file.name:continue
  envelope=json.loads(file.read_text())
  for review in envelope['reviews']:
   cid=review['id'];assert cid not in seen,cid;seen[cid]=str(file.relative_to(HERE))
   problems=validate(review,source['candidates'][cid],source['slot_catalog'])
   if problems:issues[cid]=problems
 result={'schema':'photo-model-review-integrity/v1','reviewed_records':len(seen),'source_records':len(source['candidates']),'mechanically_valid_records':len(seen)-len(issues),'invalid_records':len(issues),'issues':issues,'boundary':'Quote, schema and coverage checks only; not independent semantic accuracy.'}
 (HERE/'REVIEW-INTEGRITY.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
