"""Maintenance diagnosis against unchanged independently frozen arm inputs."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'))
import prompt_generator as g
A=ROOT/'skills/photo-prompt-image-generator/assets'
data=g.load_json(A/'photo_prompt_tags.json')
rows=[]
for arm in ['mirror','ultrawide','fixed']:
    directory=OUT/'arms'/arm
    cp=next(directory.glob('run/revisions/*/authorial_core_normalized.json'))
    ct=next(directory.glob('run/revisions/*/creative_controls.json'))
    core=json.loads(cp.read_text());controls=json.loads(ct.read_text())
    contract,picked=g.frozen_core_context(data,core,controls)
    slots={}
    for slot in ['capture_context','camera_type','capture_mode']:
        entries=[e for e in data['slots'].get(slot,[])if e['id'].startswith('sf_')]
        slots[slot]={'slot_block_reason':g.slot_block_reason(data,slot,contract),
            'focus_fields':g.core_slot_focus_queries(data,core,slot)[1],
            'new_candidates':[{'id':e['id'],'eligible':g.core_slot_entry_eligible(data,core,contract,picked,slot,e)}for e in entries]}
    rows.append({'arm':arm,'core_sha256':core['canonical_sha256'],'domains':contract['domains'],'slots':slots})
report={'scope':'Maintenance diagnostics only; frozen core and existing packs unchanged.','arms':rows}
(OUT/'exposure-diagnosis.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
