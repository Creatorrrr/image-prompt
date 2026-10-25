from pathlib import Path
import gc,json,sys,hashlib
gc.disable();O=Path(__file__).resolve().parent;ROOT=O.parents[5];S=ROOT/'skills/photo-prompt-image-generator'
read=lambda p:json.loads(p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
base=read(O/'release-base-before-concurrent-rebase.json');stage=read(O/'successor.json');N=Path(stage['store'])/'generations'/stage['native_generation_id'];sys.path.insert(0,str(N/'scripts'))
from photo_h_f2_generation import Generation
from photo_h_f2_encoder import LocalEncoder
from photo_h_f2_search import present_material
import photo_recall_first as rf
queries=read(O/'qualification-queries.frozen.json');qsha=hashlib.sha256((O/'qualification-queries.frozen.json').read_bytes()).hexdigest();mapping=read(O/'card-candidate-map.json');records=read(O/'new-native-records.json');diagnostic={cid for cid,r in records.items() if r['record_kind']=='diagnostic'};positive=set(records)-diagnostic;binding=read(Path(stage['store'])/'h-f2-generations'/stage['generation_id']/'manifest.json')['binding'];cache=O/'qualification-query-evidence.json'
if cache.exists():
 encoded=read(cache);assert encoded['query_sha256']==qsha and encoded['binding']==binding
else:
 encoded={'query_sha256':qsha,'binding':binding,'rows':[]}
 with LocalEncoder(S) as enc:
  assert enc.binding==binding
  for i in range(0,len(queries),12):
   batch=queries[i:i+12]
   for q,e in zip(batch,enc.encode([r['text'] for r in batch],'query'),strict=True):rf.check_embedding(e,binding,q['text'],'query');encoded['rows'].append({'id':q['id'],'embedding':e})
 write(cache,encoded)
rows=[]
for label,store,gid in [('baseline',base['store'],base['config']['generation_id']),('stage',stage['store'],stage['generation_id'])]:
 generation=Generation(store,gid,full=True);index=generation.index()
 for q,e in zip(queries,encoded['rows'],strict=True):
  assert q['id']==e['id'];out=index.search(q['text'],e['embedding'],binding);assert out['lane_calls']=={'BM25F':1,'local_cosine':1};order=out['order'];assert not any(r['cid'] in diagnostic for r in order)
  targets={mapping[c] for c in q['target_research_cards']};rank=next((i+1 for i,r in enumerate(order) if r['cid'] in targets),None);scope=out['query_scope'];material,projection=present_material(order,scope['event_phase'],literal=scope['literal_text'],focus=scope['primary_focus'],maximum=8)
  if q.get('expected_material')=='empty_restriction_projection_preserved':assert not material,(label,q['id'],projection)
  if q.get('expected_material')=='ordinary_positive_discovery':assert material,(label,q['id'],projection)
  rows.append({**q,'build':label,'generation_id':gid,'population':out['considered_CIDs'],'target_rank':rank,'raw_top8':order[:8],'projected_material_count':len(material),'projected_new_CIDs':[r['cid'] for r in material if r['cid'] in positive],'material_projection':projection,'native_approval':False});print(label,q['id'],rank,'material',len(material),flush=True)
 del index,generation;gc.collect()
summary={'status':'pass','queries_per_build':len(queries),'whole_pool_searches':len(rows),'exposed_repair_development':18,'ordinary_controls':6,'scope_boundary_controls':6,'holdout_cases':0,'new_positive_records':len(positive),'new_diagnostics_excluded':len(diagnostic),'restrictions_unchanged':True,'positive_goal_query_admitted':True,'counts':{label:{'target_at8':sum(r['target_rank'] is not None and r['target_rank']<=8 for r in rows if r['build']==label and r['kind']=='exposed_repair_development'),'ordinary_controls_with_new_material':sum(bool(r['projected_new_CIDs']) for r in rows if r['build']==label and r['kind']=='ordinary_control')} for label in ['baseline','stage']},'limits':'Research-exposed development, raw rank and first-eight projection are not actual managed random samples, native approval, adoption or pixels. New target CIDs are absent from baseline by construction; rank change is source exposure, not semantic recall or causal quality improvement.'}
write(O/'retrieval-qualification.json',{'summary':summary,'rows':rows});print(json.dumps(summary,ensure_ascii=False,indent=2))
