from pathlib import Path
import json,re,unicodedata
from collections import defaultdict,Counter
R=Path('/Users/chasoik/Projects/image-prompt'); O=Path(__file__).parent; A=R/'skills/photo-prompt-image-generator/assets'
inv=json.loads((O/'inventory.json').read_text()); m=json.loads((A/'photo_candidate_corpus_manifest.json').read_text())
en={}
for line in (O/'aliases-en.txt').read_text().splitlines():
 sec,items=line.split('\t');en[sec]=items.split('|')
corpus=[]
def norm(s):return unicodedata.normalize('NFKC',s).casefold().replace('‐','-').replace('–','-').replace('’',"'")
for mod in m['modules']:
 if mod['kind']!='candidates':continue
 for cid,r in json.loads((A/mod['file']).read_text()).get('candidates',{}).items():
  c=r.get('content',{}); fields={k: c.get(k) for k in ('en','ko','definition','aliases')}; text=norm(' '.join(str(fields[k]) for k in fields))
  corpus.append({'id':cid,'module':mod['file'],'kind':r.get('record_kind'),'fields':fields,'text':text,'conditions':r.get('conditions',{}),'effects':r.get('effects',{})})
post=defaultdict(set)
for i,r in enumerate(corpus):
 for token in set(re.findall(r'[a-z0-9]+|[가-힣]+',r['text'])):
  if len(token)>1:post[token].add(i)
out=[]
for row in inv['rows']:
 sec=row['id'][5:].rsplit('-',1)[0]; idx=int(row['id'].rsplit('-',1)[1])-1;eng=en[sec][idx]
 aliases=[row['term_from_research_plan']]+[x.strip() for x in eng.split(' / ')];aliases += [x.strip() for x in row['term_from_research_plan'].split('·')]
 aliases=list(dict.fromkeys(x for x in aliases if len(x)>=3)); hits={}
 for alias in aliases:
  q=norm(alias).strip();tokens=re.findall(r'[a-z0-9]+|[가-힣]+',q);poss=[post[t] for t in tokens if t in post and len(t)>1]
  if not poss:continue
  ids=set.intersection(*poss)
  for i in ids:
   rec=corpus[i]; pattern=r'(?<![a-z0-9가-힣])'+re.escape(q)+r'(?![a-z0-9가-힣])'
   if not re.search(pattern,rec['text']):continue
   hit=hits.setdefault(rec['id'],{'candidate_id':rec['id'],'module':rec['module'],'record_kind':rec['kind'],'fields':rec['fields'],'conditions':rec['conditions'],'effects':rec['effects'],'matched_aliases':[]})
   hit['matched_aliases'].append(alias)
 ordered=sorted(hits.values(),key=lambda h:(h['record_kind']!='visual_option',h['module']!='photo_candidate_cosplay_20261106.json',-max(map(len,h['matched_aliases'])),h['candidate_id']))
 out.append({**row,'english_label':eng,'searched_aliases':aliases,'lexical_match_count':len(ordered),'shortlist':ordered[:8], 'search_interpretation':'Unreviewed literal matches; not proof of semantic equivalence, applicability, completeness, or absence.'})
summary={'rows':len(out),'rows_with_match':sum(bool(x['lexical_match_count']) for x in out),'rows_without_match':sum(not x['lexical_match_count'] for x in out),'records_searched':len(corpus)}
(O/'term-lexical-comparison.json').write_text(json.dumps({'summary':summary,'rows':out},ensure_ascii=False,indent=2)+'\n'); print(json.dumps(summary,ensure_ascii=False));
for sec in en:
 group=[x for x in out if x['id'][5:].rsplit('-',1)[0]==sec];miss=[x['term_from_research_plan'] for x in group if not x['lexical_match_count']];print(sec,'matches',len(group)-len(miss),'/',len(group),'no exact:',', '.join(miss))
