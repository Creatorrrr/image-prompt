"""Readable semantic cards; snapshots retain complete unmodified records."""
import collections,json,re,sys
from pathlib import Path
R=Path(__file__).parent;rows=[json.loads(x) for x in (R/'samples.jsonl').read_text().splitlines()];refs=json.loads((R/'REFERENCE-RECORDS.json').read_text());lookup={r['candidate']['id']:r['candidate'] for r in rows}|refs
def aslist(value):return [value] if isinstance(value,str) else list(value or [])
# Deduplicate repeated claim limits, never definitions or labels.
counts=collections.Counter()
for r in rows:
 co=r['candidate']['content'];limits=aslist(co.get('semantics',{}).get('claim_limits',[]))
 for ctx in co.get('contextual_usage',{}).get('contexts',[]):limits+=aslist(ctx.get('claim_limits',[]))+aslist(ctx.get('limits',[]))+aslist(ctx.get('application_conditions',[]))
 counts.update(set(limits))
common=sorted(s for s,n in counts.items() if n>=8);code={s:'C'+str(i+1) for i,s in enumerate(common)}
(R/'COMMON-LIMITS.json').write_text(json.dumps({code[s]:s for s in common},ensure_ascii=False,indent=2)+'\n')
def unique(items):
 result=[];seen=set()
 for x in items:
  if x in ('',None):continue
  key=json.dumps(x,ensure_ascii=False,sort_keys=True)
  if key not in seen:result.append(x);seen.add(key)
 return result
def effect(e):return {'d':e.get('dimensions',[]),'p':[p['target']+'.'+p['property']+':'+p['dimension'] for p in e.get('properties',[])]}
def short_record(co):
 if co.get('en'):return co['en']
 if 'semantics' in co:return co['semantics'].get('definition','')
 return co.get('definition','')
def card(r):
 c=r['candidate'];co=c['content'];m={'i':r['sample_number'],'kind':c['record_kind'],'KO':co.get('ko'),'EN':co.get('en')}
 if m['KO']==m['EN'] and m['KO']:m['same_KO_EN']=True;m.pop('EN')
 m={k:v for k,v in m.items() if v is not None}
 sem=co.get('semantics',{});act=co.get('activation',{})
 if act:m['activation']=act
 if sem.get('definition'):m['definition']=sem['definition']
 if co.get('definition'):m['definition']=co['definition']
 base=[str(m.get(k,'')) for k in ('KO','EN','definition')]
 additional=unique(co.get('concept_units',[])+co.get('concept_terms',[])+co.get('aliases',[])+co.get('paraphrases',[])+sem.get('paraphrase_examples',[])+sem.get('visual_components',[])+co.get('concept_candidate',{}).get('concept_terms',[]))
 extra=[x for x in additional if not any(x in b for b in base)]
 if extra:m['terms']=extra
 if co.get('embedding_text'):
  residue=co['embedding_text']
  for term in sorted(unique(base+additional),key=len,reverse=True):
   if len(term)>20:residue=residue.replace(term,'')
  residue=residue.strip(' ;,.\n')
  if residue and residue not in ('Selected visible color relation','Selected visible owner-bound relation','Source-owned visible relation'):m['embedding_extra']=residue
 if co.get('relations'):m['relations']=[{k:v for k,v in x.items() if k!='id'} for x in co['relations']]
 if co.get('components'):m['bundle_components']=[{'u':x['concept_units'],'min':x.get('minimum_realizations')} for x in co['components']]
 if co.get('member_candidates'):
  m['members']=[{'meaning':short_record(lookup[x['candidate_id']]['content']),'req':x.get('requirements')} for x in co['member_candidates']]
 if co.get('associated_profile_ids'):m['associated_profile_meanings']=[short_record(lookup[x]['content']) for x in co['associated_profile_ids']]
 if co.get('canonical_candidate_ref'):m['canonical_target']=short_record(lookup[co['canonical_candidate_ref']]['content'])
 contrasts=unique(sem.get('contrast_examples',[])+co.get('reject_substitutes',[])+co.get('confusion_boundaries',[])+co.get('research_confusions',[]))
 if contrasts:m['boundaries']=contrasts
 if sem.get('claim_limits'):m['limits']=[code.get(s,s) for s in aslist(sem['claim_limits'])]
 contexts=[]
 for ctx in co.get('contextual_usage',{}).get('contexts',[]):
  x={k:v for k,v in ctx.items() if k not in ('id','claim_limits','limits','application_conditions')}
  for key in ('claim_limits','limits','application_conditions'):
   if ctx.get(key):x[key]=[code.get(s,s) for s in aslist(ctx[key])]
  contexts.append(x)
 if contexts:m['context']=contexts
 for k in ('for_any','requires_any_tags','requires_all_tags','requires_primary_any_tags','primary_context_alternatives','facets','visual_relation','domain','role','axis_requirements','axis_exclusions','required_relations','confounders','research_view_requirement','research_source_urls'):
  if co.get(k):m[k]=co[k]
 m['effects']=effect(c['effects'])
 pc=co.get('concept_candidate',{})
 if pc.get('affected_dimensions') or pc.get('affected_properties'):m['profile_proposal_effects']={'d':pc.get('affected_dimensions',[]),'p':[p['target']+'.'+p['property']+':'+p['dimension'] for p in pc.get('affected_properties',[])]}
 m['slots']=[b['slot_id'] for b in r['bindings']]
 if r['bindings']:m['conditions']=[b['conditions'] for b in r['bindings']]
 return m
cards=[card(r) for r in rows]
for start in range(0,1000,25):
 (R/'views'/f'{start+1:04d}-{start+25:04d}.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in cards[start:start+25]))
if len(sys.argv)>1:
 start=int(sys.argv[1]);end=int(sys.argv[2]) if len(sys.argv)>2 else start+24
 for row in cards[start-1:end]:print(json.dumps(row,ensure_ascii=False,separators=(',',':')))
else:print(json.dumps({'review_card_bytes':sum(len(json.dumps(x,ensure_ascii=False)) for x in cards),'cards':len(cards),'common_limits':len(common)}))
