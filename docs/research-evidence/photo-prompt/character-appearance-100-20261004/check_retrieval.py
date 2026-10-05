#!/usr/bin/env python3
"""Real-vector retrieval diagnostics, with evidence admission reported apart."""
import hashlib
import json
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
import prompt_generator as pg
from build_visual_profile_index import load_project_env

def main():
    source=HERE/'RETRIEVAL-HOLDOUT.json';holdout=json.loads(source.read_text())
    registry=pg.load_visual_obligation_registry(SKILL/'assets/photo_prompt_visual_obligations.json')
    index=pg.load_visual_profile_index(SKILL/'assets/photo_prompt_visual_profile_index.json',registry)
    profiles={p['id']:p for p in registry['profiles']}
    load_project_env();records=[]
    cache_path=Path('/tmp/image-prompt-character-appearance-100-20261004/retrieval-query-vectors.json')
    cache=json.loads(cache_path.read_text()) if cache_path.exists() else {}
    def embed(query):
        key=hashlib.sha256((index['embedding_model']+'|'+str(index['embedding_dimensions'])+'|'+query).encode()).hexdigest()
        if key not in cache:
            cache[key]=pg.embed_texts_with_gemini([query],model=index['embedding_model'],dimensions=index['embedding_dimensions'])[0]
            cache_path.write_text(json.dumps(cache))
        return cache[key]
    for row in holdout['positives']:
        query=row['query'];pid=row['profile_id']
        vector=embed(query)
        ranks=sorted(((pg.cosine_similarity(vector,e['vector']),key) for key,e in index['entries'].items()),reverse=True)
        rank=next(n for n,(_,key) in enumerate(ranks,1) if key==pid)
        evidence=profiles[pid]['semantics']['paraphrase_examples'][-1]
        routed=pg.resolve_visual_profile_hits(registry,[{'source':'authorial_core_interpretation','text':evidence,'polarity':'advisory'}],
            visual_profile_index=index,query_text=query,query_vector=vector,adult_context=False)
        hybrid=pg.resolve_visual_profile_hits(registry,[{'source':'authorial_core_interpretation','text':evidence,'polarity':'advisory'}],
            visual_profile_index=index,query_text=query,query_vector=vector,
            query_fields={'active_request':query,'visual_priorities':[evidence]},adult_context=False)
        free=pg.resolve_visual_profile_hits(registry,[{'source':'user_requirement','text':query,'polarity':'required'}],
            visual_profile_index=index,query_text=query,query_vector=vector,adult_context=False)
        hit=next((h for h in routed['hits'] if h['profile_id']==pid),None)
        hybrid_hit=next((h for h in hybrid['hits'] if h['profile_id']==pid),None)
        records.append({'profile_id':pid,'query':query,'all_profiles_vector_rank':rank,
            'all_profiles_count':len(ranks),'top_five':[{'profile_id':key,'similarity':round(score,6)} for score,key in ranks[:5]],
            'conditioned_component_evidence':evidence,'conditioned_hit':hit,'conditioned_hybrid_hit':hybrid_hit,
            'free_query_hits':free['hits'],
            'prototype_top_10':rank<=10,
            'conditioned_optional_only':bool(hit and hit['optional_eligible'] and not hit['hard_eligible']),
            'conditioned_hybrid_optional_only':bool(hybrid_hit and hybrid_hit['optional_eligible'] and not hybrid_hit['hard_eligible']),
            'free_query_has_no_hard_hits':not any(h['hard_eligible'] for h in free['hits'])})
        print(pid,'rank',rank,'optional_only',records[-1]['conditioned_optional_only'],flush=True)
    negative_records=[]
    new_ids={p['id'] for p in json.loads((SKILL/'assets/photo_prompt_visual_obligations_character_appearance.json').read_text())['profiles']}
    for query in holdout['negatives']:
        vector=embed(query)
        result=pg.resolve_visual_profile_hits(registry,[{'source':'user_requirement','text':query,'polarity':'required'}],
            visual_profile_index=index,query_text=query,query_vector=vector,adult_context=True)
        hits=[h for h in result['hits'] if h['profile_id'] in new_ids]
        negative_records.append({'query':query,'new_profile_hits':hits,'no_new_hard_hits':not any(h['hard_eligible'] for h in hits)})
    output={'schema_version':'character-appearance-real-retrieval-diagnostic/v1',
        'holdout_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'index_registry_sha256':index['registry_sha256'],
        'vector_provider':index['provider'],'vector_model':index['embedding_model'],
        'positives':records,'negatives':negative_records,
        'counts':{'positive_queries':len(records),'prototype_top_10':sum(r['prototype_top_10'] for r in records),
            'conditioned_optional_only':sum(r['conditioned_optional_only'] for r in records),
            'conditioned_hybrid_optional_only':sum(r['conditioned_hybrid_optional_only'] for r in records),
            'free_paraphrase_target_admission':sum(any(h['profile_id']==r['profile_id'] for h in r['free_query_hits']) for r in records),
            'no_free_query_hard_hits':sum(r['free_query_has_no_hard_hits'] for r in records),
            'negative_queries':len(negative_records),'no_negative_hard_hits':sum(r['no_new_hard_hits'] for r in negative_records)}}
    (HERE/'RETRIEVAL-RESULTS.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(output['counts']),flush=True)
    assert all(r['prototype_top_10'] and r['conditioned_hybrid_optional_only'] and r['free_query_has_no_hard_hits'] for r in records)
    assert all(r['no_new_hard_hits'] for r in negative_records)

if __name__=='__main__':main()
