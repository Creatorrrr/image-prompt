#!/usr/bin/env python3
"""Correct an observed graph/text mismatch without rewriting initial evidence."""
import argparse
import copy
import json
import sys
from pathlib import Path

parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,required=True);args=parser.parse_args()
root=args.root.resolve();skill=root/'skills/photo-prompt-image-generator';sys.path.insert(0,str(skill/'scripts'))
from photo_candidate_semantics import digest
from photo_runtime_sources import source_update

candidate_path=skill/'assets/photo_prompt_fire_relations_extension.json'
profile_path=skill/'assets/photo_prompt_visual_obligations_fire_relations.json'
candidate=json.loads(candidate_path.read_text());profiles=json.loads(profile_path.read_text())
entry=next(c for rows in candidate['slots'].values() for c in rows if c['id']=='fire_f097')
relation=next(r for r in entry['relations'] if r['type']=='directed_at')
assert relation['subject']=='outlet' and relation['object']=='forge'
assert 'the same fire bed' in entry['en']
old_ref=copy.deepcopy(candidate['maintenance_ref'])
relation['object']='declared_fire_bed'
profile=next(p for p in profiles['profiles'] if p['id']=='fire_rel_f097')
gate=next(g for g in profile['authored_components']['obligations'][0]['render_gates'] if g['id']=='vo_fire_f097_owned_relation')
assert 'outlet directed_at forge' in gate['description']
gate['description']=gate['description'].replace('outlet directed_at forge','outlet directed_at declared_fire_bed')
record={'schema_version':'photo-extension-maintenance/v1','record_id':'fire-bellows-owner-correction-20261008',
  'source_filename':candidate_path.name,'prior_maintenance_ref':old_ref,
  'scope':'one graph endpoint and the corresponding same-owner gate; no slot, tag, alias, effect, baseline or observed image change',
  'changes':[{'unit_id':'F097','candidate_id':'fire_f097','profile_id':'fire_rel_f097',
    'from':'forge','to':'declared_fire_bed','reason':'The authored component explicitly says the same fire bed. A forge endpoint silently narrowed the declared domestic-hearth realization.',
    'discovered_by':'arm 3 rejected the unselected candidate during post-core review',
    'pixel_status':'not_selected_or_rendered; no image-success claim for this corrected candidate'}]}
candidate['maintenance_ref']={'contract_version':'photo-extension-maintenance-ref/v1','record_id':record['record_id'],'sha256':digest(record)}
evidence=root/'docs/research-evidence/photo-prompt/extension-maintenance'/f'{record["record_id"]}.json'
evidence.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
with source_update(skill):
  candidate_path.write_text(json.dumps(candidate,ensure_ascii=False,indent=2)+'\n')
  profile_path.write_text(json.dumps(profiles,ensure_ascii=False,indent=2)+'\n')
out=root/'docs/research-evidence/photo-prompt/fire-semantics-20261008/integration/BELLOWS-OWNER-CORRECTION.json'
out.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'changed_unit':'F097','current_maintenance_record':record['record_id'],'prior_record_preserved':old_ref['record_id']}))
