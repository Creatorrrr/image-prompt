"""Validate one authored rewrite per frozen zero-goal, then encode locally once."""
from pathlib import Path
import argparse
import importlib
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[4];E=Path(__file__).parent
S=ROOT/'skills/photo-prompt-image-generator';CACHE=Path.home()/'.cache/image-prompt/candidate-recall-followup-20261019'
sys.path.insert(0,str(S/'scripts'))
from photo_candidate_authoring import read,write,file_sha
from photo_candidate_lane_generation import Generation,kernel
from build import verify_freeze


def require(value,reason):
    if not value:raise ValueError(reason)


def validate_authored(auth,packet,expected,packet_sha):
    require(auth['schema']=='photo-candidate-query-rewrite/v1' and auth['source_packet_sha256']==packet_sha,'query authoring source changed')
    require(auth['rewrites_per_goal']==1 and auth['scores_seen_for_this_query'] is False,'query was revised after scores')
    require(set(auth['goals'])==set(expected)==set(packet['goals']) and len(expected)==12,'fixed A-zero-goal scope changed')
    texts={}
    for goal,row in auth['goals'].items():
        require(set(row)=={'role_focus','scene_context','interpretation_ko','clauses'},'extra query variant or missing authored field')
        require(not re.search(r'cand_[0-9a-f]{32}',str(row)),'candidate identifier in source-only query')
        seen=set()
        for clause in row['clauses']:
            component=clause['component']
            require(component in {'role_focus','scene_context'} and component not in seen,'duplicate or unknown query component')
            seen.add(component)
            require(clause['text']==row[component] and bool(clause['rationale'].strip()) and bool(clause['grounds']),'query clause not completely grounded')
            for ground in clause['grounds']:
                pointer=ground['pointer'];require(pointer.startswith(('/core/','/plan/')),'foreign authoring source')
                value=packet['goals'][goal]
                for part in pointer.strip('/').split('/'):
                    value=value[part.replace('~1','/').replace('~0','~')]
                require(isinstance(value,str) and value==ground['quote'],'query source quote changed')
        require(seen=={'role_focus','scene_context'},'unmapped query component')
        require(isinstance(row['role_focus'],str) and 0<len(row['role_focus'])<=1200 and len(row['scene_context'])<=800,'query text budget exceeded')
        texts[goal]='Photographic role: '+row['role_focus']+('\nScene context: '+row['scene_context'] if row['scene_context'] else '')
    return texts


def check(name):
    for relative,sha in read(E/name)['files'].items():
        require(file_sha(ROOT/relative)==sha,'frozen query artifact changed: '+relative)


def prepare():
    verify_freeze();check('Q1-AUTHOR-FREEZE.json')
    require(read(E/'SELECTED-DOCUMENTS.json')['run_Q1'],'conditional Q1 is not authorized by its criterion')
    require(not (E/'Q1-QUERIES.json').exists(),'query vectors already created; no repeat inference')
    auth=read(E/'Q1-AUTHORED.json');packet=read(E/'QUERY-AUTHORING-INPUTS.json')
    texts=validate_authored(auth,packet,read(E/'CRITERIA.json')['Q1_goals'],file_sha(E/'QUERY-AUTHORING-INPUTS.json'))
    write(E/'QUERY-PROVENANCE.json',{'status':'STRUCTURAL_PASS','semantic_author':'Codex','semantic_review':'each paraphrase compared with the fixed requester/core/slot intent; historical exposure disclosed',
        'source_packet_sha256':file_sha(E/'QUERY-AUTHORING-INPUTS.json'),'clauses':{g:r['clauses'] for g,r in auth['goals'].items()},
        'query_texts':texts,'before_embedding_or_search':True,'no_candidate_labels_or_rank_inputs':True})
    selected=read(E/'SELECTED-DOCUMENTS.json')['selected'];gid=read(E/('BUILD-'+selected+'.json'))['generation_id']
    generation=Generation(CACHE/'store',gid);kernel(generation.root)
    render=importlib.import_module('photo_h_f2_queries').text
    for goal,row in auth['goals'].items():require(render(row['role_focus'],row['scene_context'])==texts[goal],'H wire rendering changed')
    from photo_h_f2_encoder import LocalEncoder
    with LocalEncoder(S) as encoder:
        require(encoder.binding==generation.binding,'foreign query model')
        goals=sorted(texts);rows=encoder.encode([texts[g] for g in goals],'query')
    write(E/'Q1-QUERIES.json',{'binding':generation.binding,'goals':{g:{'text':texts[g],'row':row} for g,row in zip(goals,rows,strict=True)},
        'new_local_query_inputs':len(rows),'new_document_inputs':0,'Gemini_calls':0})
    paths=[E/n for n in ['Q1-AUTHOR-FREEZE.json','Q1-AUTHORED.json','Q1-POLICY.json','QUERY-PROVENANCE.json','Q1-QUERIES.json','QUERY-AUTHORING-INPUTS.json']]
    write(E/'Q1-EXECUTION-FREEZE.json',{'files':{str(p.relative_to(ROOT)):file_sha(p) for p in paths},'query_results_seen':False})
    print('validated and locally encoded',len(rows),'fixed single queries',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=['prepare','run']);args=parser.parse_args()
    if args.command=='prepare':prepare()
    else:
        verify_freeze();check('Q1-AUTHOR-FREEZE.json');check('Q1-EXECUTION-FREEZE.json')
        subprocess.run([sys.executable,str(E/'evaluate.py'),'Q1'],check=True)
        check('Q1-EXECUTION-FREEZE.json')
