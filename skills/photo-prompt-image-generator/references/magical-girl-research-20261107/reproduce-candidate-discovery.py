import json,csv,re,hashlib,collections
from pathlib import Path
p=Path(__file__).resolve().parent; a=p.parents[1]/'assets'
source=json.loads((p/'source-reconciliation.json').read_text())['rows']; m=json.loads((a/'photo_candidate_corpus_manifest.json').read_text())
queries={}
for r in source:
 label=r['source_cells'][0]; parts=label.split(' — ',1); terms=[]
 for part in parts:
  for x in re.split(r'[,/·]',part):
   x=x.strip().lower()
   if len(x)>=3 and len(x)<=80 and x not in ['type','pose','girls','magical','girl','socks','girl type']:
    terms.append(x)
 queries[r['id']]=list(dict.fromkeys(terms))
hits={r['id']:[] for r in source}; records=0; modules=0
for mod in m['modules']:
 if mod.get('kind')!='candidates':continue
 data=json.load(open(a/mod['file'])); modules+=1
 for cid,record in data.get('candidates',{}).items():
  records+=1;c=record.get('content',{}); sem=c.get('semantics',{})
  fields={'en':c.get('en',''),'ko':c.get('ko',''),'definition':c.get('definition',''),'aliases':c.get('aliases',[]),'semantic_definition':sem.get('definition',''),'concept_terms':c.get('concept_candidate',{}).get('concept_terms',[])}
  s=json.dumps(fields,ensure_ascii=False).casefold()
  for row in source:
   found=[]
   for q in queries[row['id']]:
    if q in s: found.append(q)
   if found: hits[row['id']].append({'candidate_id':cid,'module':mod['file'],'matched':found,'fields':fields,'record_kind':record.get('record_kind')})
print('modules',modules,'records',records,'rows with hits',sum(bool(v) for v in hits.values()))
with (p/'candidate-discovery-all.jsonl').open('w',encoding='utf-8') as f:
 for r in source:
  h=hits[r['id']]; h.sort(key=lambda x:(-max(map(len,x['matched'])),x['candidate_id']))
  json.dump({'term_id':r['id'],'queries_unverified':queries[r['id']],'total_phrase_matches':len(h),'hits':[{'candidate_id':v['candidate_id'],'module':v['module'],'matched':v['matched'],'record_kind':v['record_kind']} for v in h],'status':'unreviewed_lexical_leads_only'},f,ensure_ascii=False);f.write('\n')
