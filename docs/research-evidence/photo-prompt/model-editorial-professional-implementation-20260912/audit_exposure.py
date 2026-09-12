"""Read-only diagnostics on the three frozen packs; never injects candidates."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path.cwd();SKILL=ROOT/'skills/photo-prompt-image-generator';sys.path.insert(0,str(SKILL/'scripts'))
import prompt_generator as pg
from bm25f_retrieval import rank_bm25f
OUT=ROOT/'docs/research-evidence/photo-prompt/model-editorial-professional-implementation-20260912';RUN=ROOT/'artifacts/photo-runs/model-editorial-three-arm-20260912'
data=pg.load_json(SKILL/'assets/photo_prompt_tags.json');index=json.loads((SKILL/'assets/photo_prompt_visual_profile_index.json').read_text())
rows=[]
for a in 'abc':
 path=RUN/f'arm-{a}/candidate_pack.json';raw=json.loads(path.read_text());pack=raw[0] if isinstance(raw,list) else raw;core=pack['authorial_core'];query,_=pg.authorial_core_retrieval_text(core);tokens=pg.candidate_pack_v5_relevance_tokens(query);opened=set(core['intent_lock']['open_dimensions'])
 rank=rank_bm25f(index['bm25f'],pg.authorial_core_bm25f_query_fields(core),limit=1000)
 slots=[c['id'] for p in pack['slots'].values() for c in p['candidates'] if ':mep_' in c['id']]
 bundles=[]
 for b in data['candidate_bundles']:
  if not b['id'].startswith('mep_'):continue
  members=b['member_candidates'];dims={d for m in members for d in m['affected_dimensions']};units=[u for m in members for u in m['concept_units']];picked={m['slot']:pg.candidate_pack_slot_entry_by_id(data,m['slot'],m['entry_id']) for m in members}
  bundles.append({'id':b['id'],'required_dimensions':sorted(dims),'unopened_dimensions':sorted(dims-opened),'distinct_slots':len(picked)==len(members),'matching_multiword_units':[u for u in units if len(pg.candidate_pack_v5_relevance_tokens(u))>=2 and pg.intent_alias_matches(query,u)],'slot_context_failures':[s for s,e in picked.items() if not pg.compatible_with_slot_context(s,e,picked,data)],'missing_standalone_members':[m['id'] for m in members if m['id'] not in {c['id'] for p in pack['slots'].values() for c in p['candidates']}]})
 rows.append({'arm':a,'pack_id':pack['pack_id'],'pack_file_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'new_slot_ids':slots,'new_optional_profile_ids':[c['id'] for c in pack.get('visual_concept_candidates',{}).get('candidates',[]) if ':mep_' in c['id']],'new_public_bundle_ids':[c['id'] for c in pack.get('candidate_bundles',{}).get('candidates',[]) if ':mep_' in c['id']],'bm25f_only_diagnostic':{'not_actual_fused_ranking':True,'top_5':rank[:5],'new_profiles':[{'rank':i+1,**r} for i,r in enumerate(rank) if r['document_id'].startswith('mep_')]},'bundle_gate_diagnostics':bundles})
payload={'contract_version':'model-editorial-exposure-diagnostics/v1','read_only':True,'actual_pack_evidence_is_authoritative':True,'source_snapshot':'artifacts/photo-runs/model-editorial-three-arm-20260912/source_snapshot.json','limits':['BM25F-only ranks are diagnostics, not a reconstruction of the embedding and RRF final ranking.','Standalone sampler filtering has not been fully replayed.','Closed dimensions and context guards are preserved; no test core or source is rewritten to force exposure.'],'arms':rows}
(OUT/'exposure-diagnostics.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
for r in rows:print(r['arm'],r['new_slot_ids'],r['new_optional_profile_ids'],r['new_public_bundle_ids'],[(x['rank'],x['document_id']) for x in r['bm25f_only_diagnostic']['new_profiles'][:4]])
