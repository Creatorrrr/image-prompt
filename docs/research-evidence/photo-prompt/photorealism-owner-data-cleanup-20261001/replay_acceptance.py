"""Rebuild/replay the accepted scope using saved vectors only; no API code."""
from pathlib import Path
import argparse,copy,gzip,hashlib,json,math,sys,tempfile
R=Path(__file__).resolve().parents[4];E=Path(__file__).resolve().parent;A=R/'skills/photo-prompt-image-generator/assets'
sys.path.insert(0,str(A.parent/'scripts'));import prompt_generator as g
import build_semantic_index as builder
from bm25f_retrieval import rank_bm25f
p=argparse.ArgumentParser();p.add_argument('--build',action='store_true');args=p.parse_args()
F=json.loads((E/'frozen-inventory-queries.json').read_text());C=json.loads((E/'acceptance-decisions.json').read_text());cache=json.loads((E/'new-vector-cache.json').read_text());attempts=json.loads((E/'api-attempts.json').read_text())
assert hashlib.sha256((E/'frozen-inventory-queries.json').read_bytes()).hexdigest()==(E/'frozen-sha256.txt').read_text().split()[0]
assert hashlib.sha256((E/'acceptance-decisions.json').read_bytes()).hexdigest()==(E/'acceptance-sha256.txt').read_text().split()[0]
assert len(attempts)==len({a['sha256']for a in attempts})==22 and all(a['status']=='completed'for a in attempts)
assert sum(len(cache[a['sha256']]['text'].encode())for a in attempts)==5707
for a in attempts:
 v=cache[a['sha256']];assert hashlib.sha256(v['text'].encode()).hexdigest()==a['sha256'];assert v['model']=='gemini-embedding-2'and v['dimensions']==768 and len(v['vector'])==768 and all(math.isfinite(x)for x in v['vector'])
B=json.loads(gzip.decompress((E/'baseline-merged-data.json.gz').read_bytes()));assert g.dictionary_hash(B)==F['baseline_dictionary_hash']
with tempfile.NamedTemporaryFile(dir=A,suffix='.json',delete=False)as handle:temp=Path(handle.name);handle.write((E/'baseline-index-manifest.json').read_bytes())
try:old=g.load_semantic_index(temp,B)
finally:temp.unlink()
proposal=copy.deepcopy(B)
for row in F['inventory']:
 rows=proposal['slots'][row['slot']];i=next(i for i,x in enumerate(rows)if x['id']==row['id']);assert rows[i]==row['before'];rows[i]=row['proposed_after']
derived=json.loads((E/'derived-bundle-owner-changes.json').read_text())['derived_changes']
for row in derived:
 owner=proposal['candidate_bundles'];parts=row['path'].split('/')
 for part in parts[:-1]:owner=owner[int(part)]if isinstance(owner,list)else owner[part]
 assert owner[parts[-1]]==row['before'];owner[parts[-1]]=row['after']
assert g.dictionary_hash(proposal)=='3037337ebe3bb06ed2e748802966b4ade9fb528340724b0802ab24b6c0069be4'
accepted=copy.deepcopy(proposal)
for row in F['inventory']:
 if row['id']in C['reverted_to_baseline']:
  rows=accepted['slots'][row['slot']];i=next(i for i,x in enumerate(rows)if x['id']==row['id']);rows[i]=row['before']
assert g.dictionary_hash(accepted)==C['accepted_dictionary_hash']
D=g.load_json(A/'photo_prompt_tags.json');assert D==accepted

def index_for(data):
 bm=g.build_semantic_bm25f_payload(data);entries={}
 for key,kind,row,slot in g.iter_semantic_entries(data):
  text=g.semantic_text_for_entry(row,slot,kind=kind);vector=old['entries'][key]['vector']if old['entries'][key]['text']==text else cache[hashlib.sha256(text.encode()).hexdigest()]['vector'];entries[key]={'kind':kind,'slot':slot,'id':row['id'],'text':text,'vector':vector,'bm25f_document':bm['documents'][key]}
 result={'provider':g.SEMANTIC_PROVIDER,'dictionary_hash':g.dictionary_hash(data),'semantic_text_recipe':g.SEMANTIC_TEXT_RECIPE_VERSION,'embedding_model':g.SEMANTIC_MODEL_ID,'embedding_dimensions':768,'bm25f':{k:v for k,v in bm.items()if k!='documents'},'entries':entries};g.validate_semantic_index_metadata(result,data);return result

final=index_for(accepted)
if args.build:builder.write_sharded_payload(A/'photo_prompt_semantic_index.json',final,keep_stale_generations=True)
actual=g.load_semantic_index(A/'photo_prompt_semantic_index.json',D);assert actual['entries']==final['entries']
assert sum(old['entries'][key]['vector']==row['vector']for key,row in actual['entries'].items())==10174-len(C['accepted_ids'])
def cosine(a,b):return sum(x*y for x,y in zip(a,b))/(math.sqrt(sum(x*x for x in a))*math.sqrt(sum(x*x for x in b)))
for name,data,index in [('baseline',B,old),('proposal',proposal,index_for(proposal)),('accepted',accepted,final)]:
 dense=[];lexical=[];bm=g.semantic_bm25f_payload_from_index(index)
 for q in F['queries']:
  vector=cache[hashlib.sha256(q['query'].encode()).hexdigest()]['vector'];rs=[{'id':key,'score':round(cosine(vector,row['vector']),12)}for key,row in index['entries'].items()if row['kind']=='slot'and row['slot']==q['slot']];rs.sort(key=lambda x:(-x['score'],x['id']));rank=next(i for i,x in enumerate(rs,1)if x['id']==q['target']);dense.append({**q,'rank':rank,'corpus_size':len(rs),'target_score':rs[rank-1]['score'],'top5':rs[:5]})
  ids=['slot:'+q['slot']+':'+row['id']for row in data['slots'][q['slot']]];ls=rank_bm25f(bm,{'query':q['query']},allowed_ids=ids,limit=len(ids));lexical.append({**q,'rank':next((i for i,x in enumerate(ls,1)if x['document_id']==q['target']),None),'corpus_size':len(ids),'top5':ls[:5]})
 for method,rows in [('dense',dense),('lexical',lexical)]:
  path=E/f'{method}-{name}.json'
  if args.build and name=='accepted':path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
  else:assert json.loads(path.read_text())==rows,(method,name)
 print(name+': all 38 method/query result rows verified',flush=True)
print('Accepted index verified; all22 original attempts retained; zero API calls',flush=True)
