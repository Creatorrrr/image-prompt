"""Root-requested exact one-sentence revision; original proposal immutable."""
import json,copy,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def digest(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
p=R/'authored/catalog_expression_artificial_face_12250.proposal.json';old=json.loads(p.read_text());new=copy.deepcopy(old)
before='Eye or iris direction, a named gaze target, camera/participant engagement or eye closure alone without a separately stated facial response; these properties require their own evidence and roles.'
after='Eye or iris direction, a named gaze target or camera/participant engagement alone; these properties require their own evidence and roles.'
assert old['after']['excludes'][1]==before;new['after']['excludes'][1]=after
assert [k for k in old['after'] if old['after'][k]!=new['after'][k]]==['excludes'];assert [i for i,(a,b) in enumerate(zip(old['after']['excludes'],new['after']['excludes'])) if a!=b]==[1]
new['delta']=[dict(pointer='/expression/'+key,before=new['before'][key],after=new['after'][key]) for key in new['before'] if new['before'][key]!=new['after'][key]];new['after_spec_sha256']=digest(new['after']);C=json.loads((R/'CATALOG-FINAL-144-V3.json').read_text());C['expression']=new['after'];new['hypothetical_catalog_sha256']=digest(C)
new['revision']=dict(previous_proposal=str(p),previous_proposal_sha256=digest(old),requested_by='root',reason='Preserve existing observable eye-area-response scope. Machine-face clarification does not authorize a new eye-closure/eyelid-aperture exclusion; no complete existing closure treatment audit was performed.',exact_delta_from_previous_after=[dict(pointer='/expression/excludes/1',before=before,after=after)],other_fields_of_after_exactly_equal=True,no_new_eye_closure_role_part_effect=True)
out=R/'authored/catalog_expression_artificial_face_12250.proposal_v2.json';assert not out.exists();out.write_text(json.dumps(new,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps(dict(path=str(out),sha256=digest(new),after_spec_sha256=new['after_spec_sha256'],hypothetical_catalog_sha256=new['hypothetical_catalog_sha256'])));print('WHOLE_AFTER',json.dumps(new['after'],ensure_ascii=False,separators=(',',':')))
