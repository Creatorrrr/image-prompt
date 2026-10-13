"""First-pass cards: meaning, relations, tags, scope. Deep cards remain separate."""
import json
from pathlib import Path
R=Path(__file__).parent;cards=[]
def add(items,value):
 if not isinstance(value,str) or not value:return
 if any(value.rstrip('.;') in x for x in items):return
 items[:]=[x for x in items if x.rstrip('.;') not in value];items.append(value)
for path in sorted((R/'views').glob('[0-9]*.jsonl')):
 for line in path.read_text().splitlines():
  x=json.loads(line);v=[]
  for key in ('KO','EN','definition'):add(v,x.get(key))
  for text in x.get('activation',{}).get('exact_terms',[]):add(v,text)
  for text in x.get('terms',[]):add(v,text)
  for c in x.get('bundle_components',[]):
   for text in c['u']:add(v,text)
  for c in x.get('members',[]):add(v,c['meaning'])
  for text in x.get('associated_profile_meanings',[]):add(v,text)
  if x.get('canonical_target'):add(v,x['canonical_target'])
  y={'i':x['i'],'k':x['kind'].replace('visual_',''),'v':v,'s':x['slots']}
  if x.get('embedding_extra') and len(x['embedding_extra'])>35:y['embed_extra']=x['embedding_extra']
  if x.get('relations'):y['rel']=[r['type']+': '+r['subject']+' -> '+r['object'] for r in x['relations']]
  e=x['effects'];y['scope']=e['p'] or e['d']
  if x.get('profile_proposal_effects'):y['profile_scope']=x['profile_proposal_effects']['p'] or x['profile_proposal_effects']['d']
  for key in ('for_any','requires_primary_any_tags','requires_any_tags','requires_all_tags','boundaries','definition','role'):
   if x.get(key) and key!='definition':y[key]=x[key]
  for ctx in x.get('context',[]):
   texts=[]
   for key in ('observable_interpretation','definition','ordinary','expressive'):
    value=ctx.get(key)
    if isinstance(value,str):add(texts,value)
    elif isinstance(value,dict):
     for val in value.values():add(texts,val)
   if texts:y.setdefault('ctx',[]).extend(texts)
  if x.get('conditions'):
   guards=[r['subject_applicability'] for r in x['conditions'] if r.get('subject_applicability')]
   if guards:y['guard']=guards
  if x.get('activation',{}).get('requires_adult_character'):y['adult_required']=True
  cards.append(y)
for start in range(0,1000,25):
 (R/'views'/f'compact-{start+1:04d}-{start+25:04d}.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in cards[start:start+25]))
print({'cards':len(cards),'bytes':sum(len(json.dumps(x,ensure_ascii=False)) for x in cards)})
