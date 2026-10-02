"""Conditional source-compatible lexical replay. No natural selection/adoption claim."""
from pathlib import Path
import sys,json,socket,urllib.request
R=Path('/workspace/scratch/ce8f20680f5a/image-prompt');E=R/'docs/research-evidence/photo-prompt/shelf-return-korean-state-data-cleanup-20261001';O=Path(__file__).parent
sys.path.insert(0,str(E))
def deny(*a,**k):raise AssertionError('No network, API, credentials or repo writes')
socket.create_connection=deny;socket.socket.connect=deny;urllib.request.urlopen=deny;urllib.request.build_opener=deny
import cycle_common as c
from bm25f_retrieval import rank_bm25f
g=c.g;c.write_json=deny;g.embed_texts_with_gemini=deny;g.embed_single_semantic_text=deny;g.get_gemini_api_key=deny;g.cached_gemini_client=deny
f=c.load_freeze();D=c.states_from_freeze(f);q=next(x for x in f['queries']if x['id']=='coexistence_en');assert c.sha(q['query'].encode())==q['query_sha256'];S='aftermath_trace';T=c.TARGET;F='slot:'+S+':localized_extinguished_flame_trace'
r={'freeze_sha256':c.sha((E/'frozen-inventory-queries.json').read_bytes()),'query':q['query'],'query_sha256':q['query_sha256'],'scope':'Conditional source-compatible lexical ranking, with the existing authored food-budget adult subject already picked. No new guards or forced choices. Not natural hybrid, V6 full-pipeline retrieval or adoption evidence.','api_calls':0,'states':{},'runtime_sha256':c.sha((R/'skills/photo-prompt-image-generator/scripts/prompt_generator.py').read_bytes())}
for label,data in D.items():
 subject=next(x for x in data['slots']['subject']if x['id']=='pov_food_budget_adult_subject');picked={'subject':subject};pool=data['slots'][S];whole=g.compatible_with_picked(pool,picked,forced=False,slot=S,source=data);ids=['slot:'+S+':'+x['id']for x in whole];audit=[]
 for x in pool:
  allowed=g.compatible_with_picked([x],picked,forced=False,slot=S,source=data)
  assert bool(allowed)==(x in whole)
  audit.append({'id':'slot:'+S+':'+x['id'],'compatible':bool(allowed),'raw_requires_primary_any_tags':x.get('requires_primary_any_tags',[]),'quality_layer_primary_requirements':sorted(g.quality_layer_primary_context_requirements(data,S,x))})
 assert T in ids and F not in ids
 target=next(x for x in pool if x['id']==T.split(':')[-1]);flame=next(x for x in pool if x['id']==F.split(':')[-1]);primary=g.picked_core_context_tokens(picked);assert set(flame['requires_primary_any_tags']).isdisjoint(primary);assert set(target['requires_primary_any_tags'])&primary
 bm=g.build_semantic_bm25f_payload(data);ranked=rank_bm25f(bm,{'query':q['query']},allowed_ids=ids,limit=len(ids));default=rank_bm25f(bm,{'query':q['query']},allowed_ids=ids);assert default==ranked[:bm['policy']['candidate_limit']]
 raw=next(x for x in c.read_json(E/'ranking-results.json')if(x['state'],x['method'],x['query_id'])==(label,'lexical',q['id']))['full_ranking'];assert ranked==[x for x in raw if x['document_id']in ids]
 rank=next(i for i,x in enumerate(ranked,1)if x['document_id']==T)
 r['states'][label]={'dictionary_hash':g.dictionary_hash(data),'picked_subject':subject,'primary_context_tokens':sorted(primary),'input_pool_count':len(pool),'compatible_pool_count':len(ids),'compatible_ids':ids,'all_53_row_guard_audit':audit,'target':target,'flame':flame,'target_rank':rank,'target_score':ranked[rank-1]['score'],'flame_excluded':True,'policy_candidate_limit':bm['policy']['candidate_limit'],'default_shortlist':default,'full_ranking':ranked}
 print(label,'compatible',len(ids),'target rank',rank,'score',ranked[rank-1]['score'],'flame excluded; full order',[x['document_id'].split(':')[-1]for x in ranked],flush=True)
b,a=r['states']['baseline'],r['states']['proposal'];assert b['compatible_ids']==a['compatible_ids'];assert b['picked_subject']==a['picked_subject'];assert b['flame']==a['flame'];assert b['all_53_row_guard_audit']==a['all_53_row_guard_audit'];r['comparison']={'compatible_pool_and_guards_exact':True,'target_rank_before_after':[b['target_rank'],a['target_rank']],'full_lexical_order_exact':[x['document_id']for x in b['full_ranking']]==[x['document_id']for x in a['full_ranking']],'default_shortlist_order_exact':[x['document_id']for x in b['default_shortlist']]==[x['document_id']for x in a['default_shortlist']],'top5_order_exact':[x['document_id']for x in b['full_ranking'][:5]]==[x['document_id']for x in a['full_ranking'][:5]],'remaining_cost':'Raw full-corpus 5->6 and score decline remain factual; this guard-bound lexical diagnostic only limits applicability of the flame promotion when this exact subject context is present.','limits':['Natural selection of this subject is unproven.','Different picked primary contexts or forced choices can change compatibility.','No default-hybrid axes or full-query V6 core were synthesized.','No guard, source, query, candidate weight or acceptance criteria were altered.']}
(O/'compatible-lexical.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print('PASS',json.dumps(r['comparison'],ensure_ascii=False),flush=True)
