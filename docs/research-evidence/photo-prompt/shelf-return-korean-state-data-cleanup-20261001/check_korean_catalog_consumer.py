#!/usr/bin/env python3
"""Replay the real --list-tags CLI consumer; no API or source/index writes."""
import argparse
import contextlib
import copy
import io
import json
import socket
import tempfile
import urllib.request
from pathlib import Path
from unittest.mock import patch
from cycle_common import A,E,R,TARGET,g,load_freeze,states_from_freeze,read_json,require,sha,write_json


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record',action='store_true')
    args=parser.parse_args()
    frozen=load_freeze()
    states=states_from_freeze(frozen)
    runtime_sha=sha((R/'skills/photo-prompt-image-generator/scripts/prompt_generator.py').read_bytes())
    selected_id=TARGET.split(':')[-1]
    def catalog(path):
        stream=io.StringIO()
        argv=['--tags',str(path),'--quality-layers',str(A/'photo_prompt_quality_layers.json'),
              '--visual-obligation-registry',str(A/'photo_prompt_visual_obligations.json'),
              '--visual-profile-index',str(A/'photo_prompt_visual_profile_index.json'),
              '--lang','ko','--list-tags','aftermath_trace']
        with contextlib.redirect_stdout(stream), patch.object(g,'embed_texts_with_gemini',side_effect=AssertionError('API forbidden')), patch.object(urllib.request,'urlopen',side_effect=AssertionError('Network forbidden')), patch.object(urllib.request.OpenerDirector,'open',side_effect=AssertionError('Network forbidden')), patch.object(socket,'create_connection',side_effect=AssertionError('Network forbidden')):
            code=g.main(argv)
        require(code==0,'Actual catalog CLI returned failure')
        return stream.getvalue()
    outputs={}
    with tempfile.TemporaryDirectory() as temporary:
        for state,data in states.items():
            path=Path(temporary)/(state+'-tags-snapshot.json')
            path.write_text(json.dumps(data,ensure_ascii=False))
            require(g.load_json(path)==data,'CLI input snapshot differs from frozen complete state')
            before=sha(path.read_bytes())
            outputs[state]=catalog(path)
            require(before==sha(path.read_bytes()),'Catalog mutated input snapshot')
    live=catalog(A/'photo_prompt_tags.json')
    require(live==outputs['proposal'],'Live current CLI differs from exact proposed catalog')
    lines={state:text.splitlines() for state,text in outputs.items()}
    require(len(lines['baseline'])==len(lines['proposal'])==len(states['baseline']['slots']['aftermath_trace']),'Catalog row count differs')
    changed=[{'baseline':before,'proposal':after} for before,after in zip(lines['baseline'],lines['proposal']) if before!=after]
    require(len(changed)==1,'More than the selected catalog row changed')
    for state,data in states.items():
        row=next(r for r in data['slots']['aftermath_trace'] if r['id']==selected_id)
        require(changed[0][state]==f"{selected_id}: {row['ko']} / {row['en']}",'CLI did not display exact selected bilingual label')
    for filename,text in [('catalog-baseline.txt',outputs['baseline']),('catalog-proposal.txt',outputs['proposal'])]:
        if args.record:
            (E/filename).write_text(text)
        else:
            require((E/filename).read_text()==text,'Saved catalog replay mismatch')
    report={'status':'pass','consumer':'Production prompt_generator.main --list-tags aftermath_trace -> list_tags -> localize(ko/en)',
            'baseline_input':'Exact complete frozen baseline serialized to a temporary --tags file; real CLI loader and output path, no loader/formatter mocking',
            'proposal_input':'Exact complete frozen proposal serialized to a temporary --tags file; independently equal to the actual live repository CLI output',
            'source_rows':len(lines['baseline']),'changed_display_rows':changed,
            'all_other_catalog_lines_exact':True,'current_live_cli_equals_proposal':True,
            'source_and_runtime_written':False,'api_calls':0,'network_calls':0,
            'prompt_generator_sha256':runtime_sha,
            'catalog_sha256':{state:sha(text.encode()) for state,text in outputs.items()},
            'limits':['This is a real Korean source/catalog display correction, not Korean generated-prompt improvement.',
                      'The current prompt section/template path does not include aftermath_trace; build_fields alone is not evidence of final prompt usage.',
                      'Selected-choice JSON serializes localized labels when an entry is selected; natural selection or adoption is not established here.',
                      'Final English V6 surfaces are independently identical; that unchanged output is not an offset for retrieval harm.']}
    if args.record:
        write_json(E/'korean-catalog-consumer.json',report)
    else:
        require(read_json(E/'korean-catalog-consumer.json')==report,'Saved consumer report mismatch')
    print('PASS: real CLI catalog changes exactly one Korean display row; all other lines exact; live current output matches; zero API')
    print(json.dumps(changed[0],ensure_ascii=False))


if __name__=='__main__':
    main()
