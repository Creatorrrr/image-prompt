"""Evaluate unchanged frozen queries on the integrated corpus, with saved vectors only."""
from pathlib import Path
import json,hashlib,math,sys
ROOT=Path(__file__).resolve().parents[4];E=Path(__file__).resolve().parent;C=E.parent/'action-context-effects-cleanup-20261001';A=ROOT/'skills/photo-prompt-image-generator/assets'
sys.path.insert(0,str(A.parent/'scripts'));import prompt_generator as g
from bm25f_retrieval import rank_bm25f
D=g.load_json(A/'photo_prompt_tags.json');index=g.load_semantic_index(A/'photo_prompt_semantic_index.json',D);bm=g.semantic_bm25f_payload_from_index(index);f=json.loads((C/'frozen-inventory-queries.json').read_text());cache=json.loads((C/'new-vector-cache.json').read_text());dense=[];lexical=[]
def cosine(a,b):return sum(x*y for x,y in zip(a,b))/(math.sqrt(sum(x*x for x in a))*math.sqrt(sum(x*x for x in b)))
for q in f['queries']:
 v=cache[hashlib.sha256(q['query'].encode()).hexdigest()]['vector'];scores=[{'id':k,'score':round(cosine(v,e['vector']),12)}for k,e in index['entries'].items()if e['kind']=='slot'and e['slot']==q['slot']];scores.sort(key=lambda x:(-x['score'],x['id']));rank=next(i for i,x in enumerate(scores,1)if x['id']==q['target']);dense.append({**q,'rank':rank,'corpus_size':len(scores),'target_score':scores[rank-1]['score'],'top5':scores[:5]})
 ids=['slot:'+q['slot']+':'+e['id']for e in D['slots'][q['slot']]];ranks=rank_bm25f(bm,{'query':q['query']},allowed_ids=ids,limit=len(ids));lexical.append({**q,'rank':next((i for i,x in enumerate(ranks,1)if x['document_id']==q['target']),None),'corpus_size':len(ids),'top5':ranks[:5]})
for name,rows in [('dense',dense),('lexical',lexical)]:(E/f'{name}-merged.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
comparison=[]
for name,rows in [('dense',dense),('lexical',lexical)]:
 old=json.loads((C/f'{name}-final.json').read_text())
 comparison.append({'method':name,'positive_top1_pre_pull':sum(x['kind']=='positive'and x['rank']==1 for x in old),'positive_top1_post_pull':sum(x['kind']=='positive'and x['rank']==1 for x in rows),'rank_changes':[{'query_id':a['id'],'kind':a['kind'],'before':a['rank'],'after':b['rank']}for a,b in zip(old,rows)if a['rank']!=b['rank']],'corpus_size_changes':[{'query_id':a['id'],'before':a['corpus_size'],'after':b['corpus_size']}for a,b in zip(old,rows)if a['corpus_size']!=b['corpus_size']]})
summary={'dictionary_hash':g.dictionary_hash(D),'documents':len(index['entries']),'new_api_calls':0,'same_32_frozen_queries':True,'comparison_to_cleanup_checkpoint':comparison,'limitation':'Candidate-derived within-slot diagnostic, not image quality or independent holdout. Original full before/after results remain in cleanup checkpoint.'};(E/'retrieval-comparison.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False,indent=2))
