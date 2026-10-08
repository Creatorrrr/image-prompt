"""Retain the pulled front-zip correction and authenticate its successor record."""
from pathlib import Path
import copy
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[4]
SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
from photo_candidate_semantics import digest
from photo_runtime_sources import source_update

def main():
    source=SKILL/'assets/photo_prompt_swimwear_extension.json'
    incoming=json.loads(subprocess.check_output(['git','show','HEAD:'+str(source.relative_to(ROOT))],cwd=ROOT))
    assert json.loads(source.read_text())==incoming
    prior=incoming['maintenance_ref'];raw=copy.deepcopy(incoming);raw.pop('maintenance_ref')
    records=ROOT/'docs/research-evidence/photo-prompt/extension-maintenance'
    old=json.loads((records/(prior['record_id']+'.json')).read_text())
    assert digest(old)==prior['sha256']
    assert old['authored_source_sha256']!=digest(raw)
    record={
        'schema_version':'photo-extension-maintenance/v1',
        'record_id':'swimwear-front-zip-binding-20261008',
        'source_filename':source.name,
        'authored_source_sha256':digest(raw),
        'prior_maintenance_ref':prior,
        'upstream_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'scope':'Authenticate the already-pulled front-zip source after removal of incompatible rear-zip aliases. Preserve the prior record and all authored source fields except maintenance_ref.',
        'visual_semantic_change_in_this_successor':False,
    }
    updated={**incoming,'maintenance_ref':{'contract_version':'photo-extension-maintenance-ref/v1',
                                         'record_id':record['record_id'],'sha256':digest(record)}}
    with source_update(SKILL):
        (records/(record['record_id']+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
        source.write_text(json.dumps(updated,ensure_ascii=False,indent=2)+'\n')
    proof={
        'upstream_failure_reproduced':'upstream-binding-baseline.log',
        'prior_record_sha256':prior['sha256'],
        'prior_bound_source_digest':old['authored_source_sha256'],
        'current_authored_source_digest':digest(raw),
        'successor_record_ref':updated['maintenance_ref'],
        'all_upstream_fields_except_maintenance_ref_unchanged':{k:v for k,v in updated.items() if k!='maintenance_ref'}==raw,
        'original_maintenance_record_preserved':digest(json.loads((records/(prior['record_id']+'.json')).read_text()))==prior['sha256'],
    }
    (Path(__file__).parent/'SWIMWEAR-BINDING-REPAIR.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(proof,ensure_ascii=False))

if __name__=='__main__':main()
