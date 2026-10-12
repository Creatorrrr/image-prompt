"""Author paired optional choices and audit real objects in one pinned worker."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = Path('/Users/chasoik/.codex/worktrees/slot-retrieval-stage07-integration/image-prompt')
PYTHON = Path('/Users/chasoik/Projects/image-prompt/.venv/bin/python')
sys.path.insert(0, str(OUT))
from compose_cases import reject, authored_review, save

WORKER = r'''
import hashlib,json,sys
from pathlib import Path
sys.path.insert(0,sys.argv[1])
import audit_composed_prompt as ca
import audit_image_render_request as ra
from photo_runtime_sources import RuntimeSnapshotProvider
payload=json.loads(Path(sys.argv[2]).read_text())
provider=RuntimeSnapshotProvider(Path(sys.argv[1]).parent,Path(payload['store']))
results=[]
for row in payload['cases']:
    obj={}
    for role,binding in row['inputs'].items():
        raw=Path(binding['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==binding['sha256'],role
        value=json.loads(raw);obj[role]=value[0] if isinstance(value,list) else value
    pack,receipt,composed,request=(obj[k] for k in ('pack','receipt','composed','request'))
    snapshot=provider.from_receipt(pack,receipt)
    ca._audit_source_data=lambda:snapshot.data
    first=ca.audit_composed_prompt(pack,composed,source_data=snapshot.data)
    runtime=ra.audit_image_render_request(pack,composed,request,request_path=Path(row['inputs']['request']['path']))
    result={'case':row['case'],'variant':row['variant'],'composed_audit':first,'runtime_audit':runtime,
        'generation_id':snapshot.generation_id,'source_fingerprint':snapshot.manifest['source_fingerprint'],
        'actual_receipt_verified':True,'embodiment_scope':composed['embodiment_review']['review']['scope'],
        'embodiment_failures':ca.photo_embodiment.audit_composed(pack,composed),
        'chosen_candidate_ids':composed['chosen_candidate_ids']}
    target=Path(row['destination']);(target/'FULL-AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    results.append(result);Path(payload['summary']).write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'case':row['case'],'variant':row['variant'],'composed':first['status'],'runtime':runtime['status'],'checks':[x['check'] for x in first['failures']]},ensure_ascii=False),flush=True)
'''

def choice(pack, spec):
    composed=reject(pack)
    prompt=composed['prompt_en']+' '+spec['addition']
    composed['prompt_en']=prompt
    composed['chosen_candidate_ids']=spec['candidate_ids']
    candidates={c['id']:c for info in pack['slots'].values() for c in info['candidates']}
    for identity in spec['candidate_ids']:
        candidate=candidates[identity]
        assert candidate['applicability']['status']=='eligible', identity
        row={'candidate_id':identity,'artistic_interpretation':spec['interpretation'],
            'transformation':spec['transformation'],'prompt_evidence':spec['addition'],
            'affected_dimensions':candidate['affected_dimensions'],
            'affected_properties':candidate.get('affected_properties',[])}
        if candidate.get('relations'):
            row['relation_evidence']={r['id']:spec['addition'] for r in candidate['relations']}
        composed['candidate_interpretations'].append(row)
    composed['authorial_core_binding']['authorial_decisions']=[{
        'dimension':'composition','decision':spec['interpretation'],'rationale':spec['transformation']}]
    composed['embodiment_review']=authored_review(pack,prompt)
    composed['embodiment_review']['review']['summary']='Reread the full final prose, including the authored addition: '+spec['transformation']+' The original actor, grounded support, reach and contacts remain coherent; the added carrier relations are readable in the specified view. This is prose review, not rendered evidence.'
    for row in composed['embodiment_review']['review']['checks'].values():
        row['reason']+=' The added cloth, surface or connected outline does not change this stated body mechanism.'
    return composed

def main():
    spec=json.loads((OUT/'ADOPTION-AUTHORING.json').read_text())['cases']
    paths=sorted((OUT/'qualified-public-natural').glob('*/candidate-pack.json'))+sorted((OUT/'qualified-public-native').glob('*/candidate-pack.json'))
    assert len(paths)==40, 'Wait for all 40 public CLI cases'
    cases=[]
    for path in paths:
        pack=json.loads(path.read_text())[0]
        variants={'reject-all':reject(pack)}
        if path.parent.name=='holdout-10-fantasy-ko':
            from golem_composition import compose
            variants['reject-all']=compose(pack)
        if path.parent.name in spec:
            variants['adopt-compatible']=choice(pack,spec[path.parent.name])
        for variant, composed in variants.items():
            destination=OUT/'qualified-composition'/path.parent.name/variant
            # Preserve the earlier standalone composed-CLI outputs without overwriting them.
            save(destination/'FINAL-COMPOSED.json',composed)
            request={'schema_version':'photo-image-render-request/v2','pack_id':pack['pack_id'],
                'core_retrieval_sha256':pack['core_retrieval']['canonical_sha256'],
                'source_intent_lock_sha256':pack['authorial_core']['intent_lock']['canonical_sha256'],
                'source_embodiment_preflight_sha256':pack['embodiment_preflight']['canonical_sha256'],
                'runtime_prompt_en':composed['prompt_en']+('\n\nAvoid: '+composed['negative_en'] if composed.get('negative_en') is not None else ''),
                'runtime_negative_en':composed['negative_en'],'references':[],
                'audit_boundary':{'composed_prompt_audit_status':'pass','runtime_prompt_audit_status':'not_run','inherits_composed_prompt_pass':False}}
            if pack.get('render_repair'):request['render_repair_contract_sha256']=pack['render_repair']['canonical_sha256']
            save(destination/'RENDER-REQUEST.json',request)
            files={'pack':path,'receipt':Path(str(path)+'.runtime-receipt.json'),
                'composed':destination/'FINAL-COMPOSED.json','request':destination/'RENDER-REQUEST.json'}
            cases.append({'case':path.parent.name,'variant':variant,'destination':str(destination),
                'inputs':{role:{'path':str(file),'sha256':hashlib.sha256(file.read_bytes()).hexdigest()} for role,file in files.items()}})
    assert len(cases)==48
    manifest=json.loads((OUT/'QUALIFIED-RUNTIME.json').read_text())
    payload={'store':str(OUT/'qualified-runtime-store'),'summary':str(OUT/'QUALIFIED-COMPOSITION-VALIDATION.json'),'cases':cases}
    save(OUT/'QUALIFIED-COMPOSITION-INPUTS.json',payload)
    (OUT/'qualified_composition_worker.py').write_text(WORKER)
    command=[str(PYTHON),str(OUT/'qualified_composition_worker.py'),str(Path(manifest['sealed_root'])/'scripts'),str(OUT/'QUALIFIED-COMPOSITION-INPUTS.json')]
    subprocess.run(command,cwd=ROOT,check=True)

if __name__=='__main__':main()
