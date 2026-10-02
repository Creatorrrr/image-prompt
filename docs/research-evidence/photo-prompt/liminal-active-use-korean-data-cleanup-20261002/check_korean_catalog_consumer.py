#!/usr/bin/env python3
"""Replay the real Korean action catalog; no source/index/runtime writes or API.

Temporary complete merged input files exercise the production CLI loader. Both
saved catalogs are immutable. --require-live-proposal additionally verifies the
owner has applied the proposal; default permits the verified baseline at prep.
"""
import argparse
import contextlib
import io
import json
import socket
import tempfile
import urllib.request
from pathlib import Path
from unittest.mock import patch
from cycle_common import A,E,SLOT,TARGET,g,load_freeze,read_json,require,states_from_freeze


def check(require_live_proposal=False):
    frozen=load_freeze();states=states_from_freeze(frozen)
    blocked=AssertionError('API/network forbidden in Korean catalog replay')
    def catalog(path):
        stream=io.StringIO()
        with contextlib.redirect_stdout(stream),patch.object(g,'embed_texts_with_gemini',side_effect=blocked),patch.object(urllib.request,'urlopen',side_effect=blocked),patch.object(urllib.request.OpenerDirector,'open',side_effect=blocked),patch.object(socket,'create_connection',side_effect=blocked):
            code=g.main(['--tags',str(path),'--quality-layers',str(A/'photo_prompt_quality_layers.json'),'--visual-obligation-registry',str(A/'photo_prompt_visual_obligations.json'),'--visual-profile-index',str(A/'photo_prompt_visual_profile_index.json'),'--lang','ko','--list-tags',SLOT])
        require(code==0,'Actual catalog CLI failed')
        return stream.getvalue()
    outputs={}
    with tempfile.TemporaryDirectory() as temporary:
        for state,data in states.items():
            path=Path(temporary)/(state+'-tags.json')
            path.write_text(json.dumps(data,ensure_ascii=False))
            require(g.load_json(path)==data,'Actual CLI input differs from complete frozen state')
            before=path.read_bytes();outputs[state]=catalog(path)
            require(path.read_bytes()==before,'CLI input changed')
            require(outputs[state]==(E/('catalog-'+state+'.txt')).read_text(),'Saved full catalog differs: '+state)
    live=catalog(A/'photo_prompt_tags.json')
    live_states=[state for state,output in outputs.items() if output==live]
    require(len(live_states)==1,'Live catalog exceeds frozen source scope')
    if require_live_proposal:
        require(live_states==['proposal'],'Actual live catalog must equal proposal')
    lines={state:output.splitlines() for state,output in outputs.items()}
    require(len(lines['baseline'])==len(lines['proposal'])==frozen['full_action_corpus_size']==963,'Complete action catalog count differs')
    changed=[{'before':before,'proposal':after} for before,after in zip(lines['baseline'],lines['proposal']) if before!=after]
    report=read_json(E/'korean-catalog-consumer.json')
    require(changed==report['changed_display_rows'] and len(changed)==1,'Catalog must change exactly the frozen Korean clause')
    selected=TARGET.split(':')[-1]
    for label,key in [('baseline','before'),('proposal','proposal')]:
        row=next(r for r in states[label]['slots'][SLOT] if r['id']==selected)
        require(changed[0][key]==f"{selected}: {row['ko']} / {row['en']}",'Selected catalog line incorrect')
    return {'status':'pass','source_rows':963,'changed_display_rows':1,'all_other_catalog_lines_exact':True,'actual_live_state':live_states[0],'api_calls':0,'source_index_runtime_writes':0}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-live-proposal',action='store_true')
    print(check(parser.parse_args().require_live_proposal))
