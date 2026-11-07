import json,re,sys,collections
from pathlib import Path
R=Path('/Users/chasoik/Projects/image-prompt');O=R/'docs/research-evidence/photo-prompt/nurse-uniform-20261107';A=R/'skills/photo-prompt-image-generator/assets';sys.path.insert(0,str(R/'skills/photo-prompt-image-generator/scripts'))
import photo_candidate_corpus as c
corpus=c.load(A); terms=collections.defaultdict(set); snippets={};rx=re.compile(r'[a-z0-9]+|[가-힣]{2,}|[\u3040-\u30ff\u4e00-\u9fff]{2,}',re.I)
def tokenize(s):return set(x.lower() for x in rx.findall(s) if len(x)>2 and x.lower() not in {'the','and','with','nurse','nursing','medical','uniform','간호사','간호복'})
for cid,rec in corpus['candidates'].items():
 if rec.get('record_kind')!='visual_option':continue
 cont=rec.get('content',{}); parts=[cont.get(k,'') for k in ('en','ko','definition')];parts=[x for x in parts if isinstance(x,str)];snippets[cid]=' | '.join(parts)[:500]
 for t in tokenize(' '.join(parts)):terms[t].add(cid)
rows=json.loads((O/'source-rows.json').read_text());out=[]
for i,row in enumerate(rows):
 ts=tokenize(row['label']); scores=collections.Counter()
 for t in ts:
  for cid in terms.get(t,()):scores[cid]+=1
 top=scores.most_common(6);out.append({'row_id':f'NURSE-ROW-{i+1:03d}','label':row['label'],'tokens':sorted(ts),'lexical_neighbors':[{'candidate_id':cid,'token_hits':score,'preview':snippets[cid]} for cid,score in top],'status':'lexical_shortlist_only_not_semantic_review'})
(O/'lexical-shortlists.json').write_text(json.dumps({'scope':'working source corpus; lexical hints only; no equivalence, ranking or installed-release claim','source_rows':len(rows),'candidate_count':len(snippets),'rows':out},ensure_ascii=False,indent=2)+'\n');print('rows',len(out),'with hints',sum(bool(x['lexical_neighbors']) for x in out),'candidate records',len(snippets))
