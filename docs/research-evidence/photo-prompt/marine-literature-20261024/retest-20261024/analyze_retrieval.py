"""Paired offline source-name ablation on an identical pool, policy and queries."""
from pathlib import Path
import gc;gc.disable()
import collections,copy,hashlib,json,sys
import numpy as np
T=Path(__file__).resolve().parent;Q=T.parent;R=T.parents[4]
read=lambda p:json.loads(Path(p).read_bytes())
def write(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')

def freeze_queries():
 rows=[]
 original=read(Q/'integration-evidence/independent-frozen-query-texts.json')
 for arm,data in original.items():
  for slot,text in data['slots'].items():rows.append({'id':'prior-'+arm+'-'+slot,'text':text,'origin':'previous actual frozen query'})
 for arm in 'abc':
  for slot,row in read(T/arm/'authored-intents.json')['slots'].items():
   if row['status']=='search':rows.append({'id':'retest-'+arm+'-'+slot,'text':'Photographic role: '+row['role_focus']+'\nScene context: '+row['scene_context'],'origin':'new independent pre-retrieval authored slot'})
  core=read(T/arm/'authorial_core.json')
  rows.append({'id':'retest-'+arm+'-baseline','text':core['baseline_prompt_en'],'origin':'new independently frozen baseline'})
 rows.append({'id':'clean-topic','text':'해병문학 용어 조사','origin':'exact current reviewed requester topic projection'})
 probes=read(Q/'integration-evidence/retrieval-qualification.json')['cases']
 low={'R12-ko','R24-ko','R25-en','R34-en','R37-ko','R38-en'}
 for row in probes:
  if row['id'] in low:rows.append({'id':'prior-low-'+row['id'],'text':row['query'],'target_candidate':row['target_candidate'],'origin':'previous low-ranked development query, retained unchanged'})
 write(T/'ablation-queries.frozen.json',rows)
 return rows

def main():
 rows=read(T/'ablation-queries.frozen.json');succ=read(T/'successor.json');N=Path(succ['store'])/'generations'/succ['native_generation_id'];sys.path.insert(0,str(N/'scripts'))
 from photo_h_f2_generation import Generation,WEIGHTS,configs
 from photo_h_f2_search import Index
 from photo_h_f2_encoder import LocalEncoder
 from photo_recall_generation import BodyReader,read as read_any,file_sha
 import photo_recall_first as rf
 import photo_candidate_corpus as corpus
 g=Generation(succ['store'],succ['generation_id'],full=True)
 oldroot=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed/h-f2-generations/3643bb6b2a4143f1a2f3ccccfacb63c5d98808319dac5753849304127f17e166')
 oldmanifest=read_any(oldroot/'manifest.json');assert corpus.digest(oldmanifest)==oldroot.name
 for name in ['indexed-documents.json.gz','documents.json.gz','field-documents.json.gz','vectors.f64']:
  assert file_sha(oldroot/name)==oldmanifest['files'][name]
 oldmeta=read_any(oldroot/'indexed-documents.json.gz');oldi={m['id']:i for i,m in enumerate(oldmeta)}
 olddocs={d['id']:d for d in read_any(oldroot/'documents.json.gz')['rows']}
 oldfields={d['id']:d for d in read_any(oldroot/'field-documents.json.gz')['rows']}
 positive=set(read(Q/'integration-evidence/new-visual-cids.json'))
 # This shadow is explicitly an offline counterfactual, not an installed release.
 shadow=copy.copy(g);shadow.body=BodyReader(oldroot);shadow.by_identity={m['id']:m for m in oldmeta}
 meta=[];docs=[];fdocs=[]
 current_docs=read_any(g.root/'documents.json.gz')['rows'];current_fields=read_any(g.root/'field-documents.json.gz')['rows']
 matrix=np.array(np.memmap(g.root/'vectors.f64',dtype='<f8',mode='r',shape=(len(g.metadata),768)))
 oldmatrix=np.memmap(oldroot/'vectors.f64',dtype='<f8',mode='r',shape=(len(oldmeta),768))
 for i,(m,d,f) in enumerate(zip(g.metadata,current_docs,current_fields,strict=True)):
  if m['cid'] in positive:
   assert m['id'] in oldi;meta.append(oldmeta[oldi[m['id']]]);docs.append(olddocs[m['id']]);fdocs.append(oldfields[m['id']]);matrix[i]=oldmatrix[oldi[m['id']]]
  else:meta.append(m);docs.append(d);fdocs.append(f)
 lengths={f:[] for f in WEIGHTS};counts={f:0 for f in WEIGHTS};posting={}
 for i,f in enumerate(fdocs):
  terms={}
  for name in WEIGHTS:
   bag=collections.Counter(t for v in f['fields'][name] for t in rf.tokens(v));size=sum(bag.values());lengths[name].append(size);counts[name]+=bool(size)
   for term,tf in bag.items():terms.setdefault(term,{})[name]=tf
  for term,tf in terms.items():posting.setdefault(term,[]).append([i,tf])
 cfg=configs();fields={'n':len(meta),'fields':cfg,'lengths':lengths,'nonempty_counts':counts,'postings':posting,'average_lengths':{f:(sum(lengths[f])/(counts[f] if 'normalization_population' in cfg[f] else len(meta)) if (counts[f] if 'normalization_population' in cfg[f] else len(meta)) else 0.) for f in WEIGHTS},'tokenizer':g.fields['tokenizer']}
 def owner(identity):return shadow if identity.split('|')[0] in positive else g
 before=Index(meta,fields,matrix,docs,source_units=lambda i:owner(i).primary_units(i),source_effects=lambda i:owner(i).effect_footprint(i),source_constraints=lambda i:owner(i).focus_constraints(i))
 after=g.index();cache=T/'ablation-query-embeddings.json'
 if cache.exists():e=read(cache);assert e['queries_sha256']==hashlib.sha256((T/'ablation-queries.frozen.json').read_bytes()).hexdigest();encoded=e['rows']
 else:
  with LocalEncoder(R/'skills/photo-prompt-image-generator') as encoder:
   assert encoder.binding==g.binding;encoded=encoder.encode([r['text'] for r in rows],'query')
  write(cache,{'queries_sha256':hashlib.sha256((T/'ablation-queries.frozen.json').read_bytes()).hexdigest(),'rows':encoded})
 out=[]
 for row,embedding in zip(rows,encoded,strict=True):
  a=before.search(row['text'],embedding,g.binding);b=after.search(row['text'],embedding,g.binding)
  result={**row,'before':{},'after':{}}
  for name,value in [('before',a),('after',b)]:
   result[name]={'new_in_top8':[{'rank':i+1,'cid':r['cid']} for i,r in enumerate(value['order'][:8]) if r['cid'] in positive],'new_in_top32':[{'rank':i+1,'cid':r['cid']} for i,r in enumerate(value['order'][:32]) if r['cid'] in positive],'top8':[r['cid'] for r in value['order'][:8]],'lane_calls':value['lane_calls']}
   if row.get('target_candidate'):result[name]['target_rank']=next(i+1 for i,r in enumerate(value['order']) if r['cid']==row['target_candidate'])
  out.append(result);write(T/'ablation-progress.json',{'complete':len(out),'total':len(rows)});print('searched',row['id'],flush=True)
 write(T/'retrieval-ablation.json',{'status':'complete','generation_id':succ['generation_id'],'native_generation_id':succ['native_generation_id'],'qualification':'Offline paired source-name ablation, identical current positive pool and kernel; only the 87 marine source names/documents/vectors differ. Not an installed counterfactual or independent holdout accuracy. Actual agent sampling/adoption is separate.','queries':out,'positive_pool':len(g.metadata),'sampling_or_policy_changes':False,'strict_claim_limit':'Clean topic vs previous polluted topic is an input-scope intervention; compare those rows separately from source naming.'})

if __name__=='__main__':
 if '--freeze-queries' in sys.argv:print(len(freeze_queries()))
 else:main()
