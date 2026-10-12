
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
