#!/usr/bin/env python3
"""Portable, read-only replay of cycle15 source-context and cache-boundary evidence."""
import copy
import socket
import urllib.request
from decimal import Decimal
from unittest.mock import patch
from cycle_common import A,E,R,TARGET,g,load_freeze,states_from_freeze,read_json,require,sha,load_baseline_index,validate_vector
from bm25f_retrieval import rank_bm25f


def check():
    f=load_freeze();states=states_from_freeze(f)
    q=next(x for x in f['queries'] if x['id']=='coexistence_en')
    require(sha(q['query'].encode())==q['query_sha256'],'Full query changed')
    original=E/'supplemental-review/original'
    raw_report=read_json(original/'result.json')
    base_conditional=read_json(original/'compatible-lexical.json')
    quality_report=read_json(original/'quality-overlay-lexical.json')
    require(raw_report['query']==q['query']==base_conditional['query']==quality_report['query'],'Review query mismatch')
    quality=g.load_quality_layers(A/'photo_prompt_quality_layers.json')
    require(sha((A/'photo_prompt_quality_layers.json').read_bytes())==quality_report['quality_sha256'],'Quality overlay changed')
    flame='slot:aftermath_trace:localized_extinguished_flame_trace'
    outputs={}
    for state,data in states.items():
        data[g.QUALITY_LAYERS_DATA_KEY]=quality
        subject=next(x for x in data['slots']['subject'] if x['id']=='pov_food_budget_adult_subject')
        pool=data['slots']['aftermath_trace']
        compatible=g.compatible_with_picked(pool,{'subject':subject},forced=False,slot='aftermath_trace',source=data)
        ids=['slot:aftermath_trace:'+x['id'] for x in compatible]
        require(ids==quality_report['states'][state]['compatible_ids'],'Compatible pool changed')
        require(len(ids)==12 and TARGET in ids and flame not in ids,'Source-context eligibility changed')
        bm=g.build_semantic_bm25f_payload(data)
        all_ids=['slot:aftermath_trace:'+x['id'] for x in pool]
        raw=rank_bm25f(bm,{'query':q['query']},allowed_ids=all_ids,limit=len(all_ids))
        require(raw==raw_report['states'][state]['lexical_full_ranking'],'Raw full ranking changed')
        ranked=rank_bm25f(bm,{'query':q['query']},allowed_ids=ids,limit=len(ids))
        shortlist=rank_bm25f(bm,{'query':q['query']},allowed_ids=ids)
        require(ranked==quality_report['states'][state]['full_ranking'],'Conditional full ranking changed')
        require(shortlist==quality_report['states'][state]['default_shortlist'],'Default lexical shortlist changed')
        require(shortlist[0]['document_id']==TARGET,'Conditional target is not first')
        outputs[state]=[row['document_id'] for row in ranked]
    require(outputs['baseline']==outputs['proposal'],'Conditional order changed')
    # Reproduce why raw-query cache alone cannot establish default hybrid retrieval.
    clean=states_from_freeze(f)
    baseline,_=load_baseline_index(f,clean['baseline'])
    proposal=g.load_semantic_index(A/'photo_prompt_semantic_index.json',clean['proposal'])
    cache=read_json(E/'new-vector-cache.json')
    attempts={}
    def deny(*args,**kwargs):raise AssertionError('Network/API/credential fallback forbidden')
    for state,index in [('baseline',baseline),('proposal',proposal)]:
        data=clean[state];data[g.QUALITY_LAYERS_DATA_KEY]=quality
        for mode in ('auto','off'):
            requested=[]
            def exact_only(text,model,dimensions,api_key):
                h=sha(text.encode());requested.append({'text':text,'sha256':h})
                if h not in cache:raise RuntimeError('NO_EXACT_CACHED_VECTOR: '+h)
                record=cache[h];validate_vector(record,text)
                require(record['model']==model and record['dimensions']==dimensions,'Cached request mismatch')
                return record['vector']
            with patch.object(g,'embed_single_semantic_text',side_effect=exact_only),patch.object(g,'embed_texts_with_gemini',side_effect=deny),patch.object(g,'get_gemini_api_key',side_effect=deny),patch.object(g,'cached_gemini_client',side_effect=deny),patch.object(socket,'create_connection',side_effect=deny),patch.object(socket.socket,'connect',side_effect=deny),patch.object(urllib.request,'urlopen',side_effect=deny),patch.object(urllib.request,'build_opener',side_effect=deny):
                try:
                    g.make_semantic_context(data,q['query'],'hybrid','medium',semantic_index=index,semantic_axis_mode=mode)
                except RuntimeError as error:
                    reference=raw_report['default_hybrid_context_attempt' if mode=='auto' else 'supported_axis_off_attempt']
                    require(str(error)==reference['error'],'Different cache boundary')
                    require(requested[0]['text']==q['query'],'Raw full query was changed')
                    require([x['text'] for x in requested]==[x['text'] for x in reference['embedding_requests']],'Derived production request changed')
                    attempts[state+':'+mode]={'status':'blocked_before_shortlist','missing':str(error),'requests':requested}
                else:raise AssertionError('Unexpected hybrid success without missing vectors')
    return {'status':'pass','conditional_compatible_count':12,'conditional_target_ranks':[1,1],
            'conditional_full_order_exact':True,'flame_excluded_by_existing_context_guard':True,
            'actual_quality_overlay_checked':True,'raw_lexical_target_ranks':[5,6],
            'raw_lexical_flame_ranks':[6,5],'raw_margins':[raw_report['states'][s]['target_minus_flame_margin'] for s in ('baseline','proposal')],
            'cache_boundary_attempts':attempts,'api_calls':0,'writes':0,
            'scope':'Conditional source-compatible lexical evidence only. Natural hybrid/V6 retrieval and subject selection are not established.'}


if __name__=='__main__':
    report=check()
    print('PASS: exact raw harm retained, conditional 12-row order stable, missing-axis hybrid attempts blocked, no API or writes')
