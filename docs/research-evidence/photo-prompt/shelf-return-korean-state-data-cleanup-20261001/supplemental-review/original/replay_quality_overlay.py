"""Verify the same conditional lexical pool with the real runtime quality overlay."""
from pathlib import Path
import sys,json,socket,urllib.request
R=Path('/workspace/scratch/ce8f20680f5a/image-prompt');E=R/'docs/research-evidence/photo-prompt/shelf-return-korean-state-data-cleanup-20261001';O=Path(__file__).parent;sys.path.insert(0,str(E))
def deny(*a,**k):raise AssertionError('No network/API/credentials/repo writes')
socket.create_connection=deny;socket.socket.connect=deny;urllib.request.urlopen=deny;urllib.request.build_opener=deny
import cycle_common as c
from bm25f_retrieval import rank_bm25f
g=c.g;c.write_json=deny;g.embed_texts_with_gemini=deny;g.embed_single_semantic_text=deny;g.get_gemini_api_key=deny;g.cached_gemini_client=deny
f=c.load_freeze();D=c.states_from_freeze(f);q=next(x for x in f['queries']if x['id']=='coexistence_en');parent=c.read_json(O/'compatible-lexical.json');P=c.A/'photo_prompt_quality_layers.json';qual=g.load_quality_layers(P)
r={'kind':'Conditional source-compatible lexical ranking with unchanged production runtime quality overlay, not natural hybrid/adoption.','query':q['query'],'query_sha256':q['query_sha256'],'quality_path':str(P),'quality_sha256':c.sha(P.read_bytes()),'base_diagnostic_sha256':c.sha((O/'compatible-lexical.json').read_bytes()),'states':{},'api_calls':0}
for label,data in D.items():
 data[g.QUALITY_LAYERS_DATA_KEY]=qual;subject=next(x for x in data['slots']['subject']if x['id']=='pov_food_budget_adult_subject');picked={'subject':subject};pool=data['slots']['aftermath_trace'];allowed=g.compatible_with_picked(pool,picked,forced=False,slot='aftermath_trace',source=data);ids=['slot:aftermath_trace:'+x['id']for x in allowed];assert c.TARGET in ids;assert 'slot:aftermath_trace:localized_extinguished_flame_trace'not in ids
 bm=g.build_semantic_bm25f_payload(data);ranked=rank_bm25f(bm,{'query':q['query']},allowed_ids=ids,limit=len(ids));default=rank_bm25f(bm,{'query':q['query']},allowed_ids=ids);raw=next(x for x in c.read_json(E/'ranking-results.json')if(x['state'],x['method'],x['query_id'])==(label,'lexical',q['id']))['full_ranking'];assert ranked==[x for x in raw if x['document_id']in ids]
 r['states'][label]={'compatible_count':len(ids),'compatible_ids':ids,'excluded_by_quality_overlay':sorted(set(parent['states'][label]['compatible_ids'])-set(ids)),'all_53_rows':[{'id':x['id'],'compatible':x in allowed,'quality_primary_requirement_sources':g.quality_layer_primary_context_requirement_sources(data,'aftermath_trace',x)}for x in pool],'target_rank':next(i for i,x in enumerate(ranked,1)if x['document_id']==c.TARGET),'full_ranking':ranked,'default_shortlist':default}
 print(label,len(ids),r['states'][label]['target_rank'],r['states'][label]['excluded_by_quality_overlay'],flush=True)
b,a=r['states']['baseline'],r['states']['proposal'];assert b['compatible_ids']==a['compatible_ids'];assert b['all_53_rows']==a['all_53_rows'];assert [x['document_id']for x in b['full_ranking']]==[x['document_id']for x in a['full_ranking']];r['comparison']={'compatible_ids_and_guards_exact':True,'full_order_exact':True,'target_rank_before_after':[b['target_rank'],a['target_rank']]}
(O/'quality-overlay-lexical.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print('PASS',r['comparison'],flush=True)
