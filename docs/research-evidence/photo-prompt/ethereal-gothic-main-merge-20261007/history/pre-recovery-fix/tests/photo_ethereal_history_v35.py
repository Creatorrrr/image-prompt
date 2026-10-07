"""Authenticated additive DATA boundary and exact original V34 replay."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

BASE=Path('docs/research-evidence/photo-prompt/ethereal-gothic-main-merge-20261007/history')
PARENT=BASE/'V34-PARENT-SOURCE.json'
PARENT_SHA256='58e9066a9e934413e1dccd103414098b113f76d8a3165139d434024eeb6a68f0'
PIN='f6b2f88fc9adeae0dfe59b78a7a0ecafc7b4c03a'
TREE='96a47e6e88cbf902878081f82ceb4d0013bc7e21'
PROOF=BASE/'V35-ETHEREAL-DATA-PROOF.json'
PROOF_SHA256='d485dd85f129291b35669733f98931336cf70cf57bedf04422b3c8b61a69bccb'
PHOTO=Path('skills/photo-prompt-image-generator/assets')
ILL=Path('skills/subculture-illustration-image-generator')
ADDED=frozenset((PHOTO/n).as_posix() for n in ('photo_prompt_ethereal_gothic_scene_extension.json','photo_prompt_visual_obligations_ethereal_gothic_scene.json'))
CHANGED=frozenset((PHOTO/n).as_posix() for n in ('photo_prompt_source_manifest.json','photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json'))
PACK_POINTERS=['/0/core_retrieval/canonical_sha256','/0/core_retrieval/slot_corpus_sha256','/0/core_retrieval/slot_ownership_sha256','/0/creative_augmentation/hard_eligible_pool_sha256','/0/pack_id','/0/provenance/tags_hash','/0/slots/light_shape/candidates/1']

def digest(raw):return hashlib.sha256(raw).hexdigest()
def _fixtures():
    from tests import photo_prompt_fixtures
    return photo_prompt_fixtures
def regular(root,name):return _fixtures()._v24_regular_path(root,str(name))
def context(root):return any((root/p).exists() or (root/p).is_symlink() for p in (PROOF,PARENT,ILL/'assets/photo_regression_baseline_v35.json'))

def parent_manifest(root):
    raw=regular(root,PARENT).read_bytes()
    if digest(raw)!=PARENT_SHA256:raise AssertionError('Frozen V35 parent manifest drift')
    parent=json.loads(raw);rows=parent.get('members') or []
    if (parent.get('schema')!='photo-ethereal-parent-source/v1' or parent.get('source_pin')!=PIN or parent.get('source_tree')!=TREE or parent.get('member_count')!=1522 or len(rows)!=1522 or parent.get('total_member_bytes')!=2962793144):raise AssertionError('Frozen V35 parent lineage drift')
    names=set();backings={}
    for row in rows:
        name=_fixtures()._v17_safe_path(row['path']).as_posix();source=_fixtures()._v17_safe_path(row['source_path']).as_posix();identity=tuple(row.get(k) for k in ('git_blob','mode','bytes','sha256'))
        if (name in names or row.get('git_commit')!=PIN or row.get('git_path')!=name or row.get('mode') not in {'100644','100755'} or type(row.get('bytes')) is not int or row['bytes']<0 or len(row.get('git_blob',''))!=40 or len(row.get('sha256',''))!=64 or any(c not in '0123456789abcdef' for c in row['git_blob']+row['sha256']) or (source in backings and backings[source]!=identity)):raise AssertionError('Frozen V35 parent provenance drift')
        names.add(name);backings[source]=identity
    if sum(r['bytes'] for r in rows)!=parent['total_member_bytes'] or any(p.as_posix() in names for n in names for p in Path(n).parents) or any(p.as_posix() in backings for n in backings for p in Path(n).parents):raise AssertionError('Frozen V35 parent path overlap drift')
    return parent

def exact_payload(root,row):
    path=regular(root,row['source_path']);raw=path.read_bytes();blob=hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()
    if path.stat().st_mode&0o7777!=int(row['mode'][-3:],8) or len(raw)!=row['bytes'] or digest(raw)!=row['sha256'] or blob!=row['git_blob']:raise AssertionError('Frozen V35 original source payload or mode drift: '+row['path'])
    return raw

def transition(root):
    raw=regular(root,PROOF).read_bytes()
    if digest(raw)!=PROOF_SHA256:raise AssertionError('Frozen V35 DATA proof drift')
    proof=json.loads(raw);parent=parent_manifest(root)
    if (proof.get('schema')!='photo-ethereal-data-transition/v35' or proof.get('parent_manifest')!=PARENT.as_posix() or proof.get('parent_manifest_sha256')!=PARENT_SHA256 or proof.get('previous_qualified_commit')!=PIN or proof.get('previous_qualified_tree')!=TREE or proof.get('parent_member_count')!=parent['member_count'] or set(proof.get('added_source_paths') or [])!=ADDED or set(proof.get('changed_source_paths') or [])!=CHANGED):raise AssertionError('Frozen V35 DATA lineage drift')
    return proof,parent

def previous_path(root,name,supplied=None):
    """Recover original V32 inputs only after verifying the exact V35 live side."""
    from tests import photo_data_scope_history_v34 as v34
    if not context(root):return v34.previous_path(root,name,supplied)
    if name not in v34.RECOVERY:return regular(root,name)
    proof,parent=transition(root);path=regular(root,name);current=path.read_bytes();row=next(r for r in parent['members'] if r['path']==name)
    if digest(current)!=proof['source_files_after'][name] or path.stat().st_mode&0o7777!=int(row['mode'][-3:],8):raise AssertionError('Frozen V35 retained live source payload or mode drift: '+name)
    original_row=next(r for r in v34.source_manifest('v32',root)['members'] if r['path']==name)
    original=v34.exact_payload(root,original_row);parent_raw=exact_payload(root,row)
    if supplied is not None and digest(supplied) not in {digest(current),digest(original),digest(parent_raw)}:raise AssertionError('Frozen V35 supplied source payload drift: '+name)
    return regular(root,original_row['source_path'])

def previous_payload(root,name,current):return previous_path(root,name,current).read_bytes() if context(root) else current

def materialize_original(directory,*,source_root,link_verified=False):
    f=_fixtures();f._v24_empty_destination(directory);parent=parent_manifest(source_root)
    for row in parent['members']:exact_payload(source_root,row)
    directory.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.sealed-v34-',dir=directory.parent) as temporary:
        staged=Path(temporary)/'tree';staged.mkdir()
        for row in parent['members']:
            target=staged/f._v17_safe_path(row['path']);target.parent.mkdir(parents=True,exist_ok=True)
            if link_verified:os.link(regular(source_root,row['source_path']),target)
            else:target.write_bytes(exact_payload(source_root,row));target.chmod(int(row['mode'][-3:],8))
        f._v24_empty_destination(directory);staged.replace(directory)
    return parent

def replay_original(directory,*,source_root,baseline_version=34,test_module=None):
    parent=parent_manifest(source_root);environment=parent['environment'];probe="import json,sys,unicodedata; print(json.dumps({'implementation':sys.implementation.name,'python':list(sys.version_info[:3]),'unicode':unicodedata.unidata_version}))"
    actual=json.loads(subprocess.check_output([sys.executable,'-c',probe],text=True))
    if actual!=environment:raise AssertionError('Exact V34 Python/Unicode environment unavailable')
    executable=directory/'.venv/bin/python';executable.parent.mkdir(parents=True,exist_ok=True);executable.symlink_to(Path(sys.executable).absolute())
    env=os.environ.copy();env.update(GEMINI_API_KEY='',GOOGLE_API_KEY='',PYTHONPATH=str(directory)+os.pathsep+str(directory/'tests'))
    with tempfile.TemporaryDirectory(prefix='original-v34-runtime-') as store:
        env['PHOTO_RUNTIME_STORE']=store
        setup="import sys; sys.path.insert(0,'skills/photo-prompt-image-generator/scripts'); from photo_runtime_sources import SnapshotPublisher; SnapshotPublisher().publish()"
        prepared=subprocess.run([str(executable),'-c',setup],cwd=directory,env=env,capture_output=True,text=True,timeout=300)
        if prepared.returncode:raise AssertionError('Original V34 publisher failed: '+prepared.stderr)
        if test_module:cmd=[str(executable),'-m','unittest','-v',test_module]
        else:
            code="import json,sys; from pathlib import Path; sys.path.insert(0,'skills/subculture-illustration-image-generator/scripts'); import validate_illustration_assets as v; print(json.dumps(v.validate_photo_regression_baseline(Path('skills/subculture-illustration-image-generator/assets'),baseline_version="+str(baseline_version)+")))"
            cmd=[str(executable),'-c',code]
        result=subprocess.run(cmd,cwd=directory,env=env,capture_output=True,text=True,timeout=900)
    if result.returncode:raise AssertionError('Original V34 replay failed: '+result.stdout+result.stderr)
    return result if test_module else json.loads(result.stdout.strip().splitlines()[-1])

def qualify_current(v,asset_dir,root,baseline,pack,raw,receipt=None):
    require=v._require
    try:proof,parent=transition(root)
    except (AssertionError,OSError,ValueError) as exc:require(False,str(exc))
    require(baseline.get('ethereal_data_transition')==dict(evidence_path=PROOF.as_posix(),evidence_sha256=PROOF_SHA256,previous_qualified_commit=PIN,parent_manifest_sha256=PARENT_SHA256),'photo V35 successor lineage drift')
    previous_raw=(asset_dir/'photo_regression_baseline_v34_pack.json').read_bytes();old_baseline=json.loads((asset_dir/'photo_regression_baseline_v34.json').read_bytes())
    require(v._sha256(asset_dir/'photo_regression_baseline_v34.json')==proof['previous_manifest_sha256'] and digest(previous_raw)==proof['previous_pack_sha256'] and digest(raw)==proof['current_pack_sha256']==baseline['sha256'] and raw==(asset_dir/'photo_regression_baseline_v35_pack.json').read_bytes() and json.loads(raw)==[pack] and pack['pack_id']==proof['current_pack_id'],'photo V35 frozen pack bytes drift')
    changes=proof['reviewed_pack_delta'];require([r['pointer'] for r in changes]==PACK_POINTERS==proof['allowed_pack_delta_pointers'] and all(r['operation']=='replace' for r in changes),'photo V35 unregistered pack delta')
    before,after=changes[-1]['before'],changes[-1]['after']
    require(before['entry_id']=='monitor_rectangle_glow' and after['entry_id']=='sparkling_water_reflection_highlights' and before['slot']==after['slot']=='light_shape','photo V35 unrelated advisory candidate change')
    expected=json.loads(previous_raw)
    from tests import photo_data_scope_history_v34 as v34
    v34._apply(expected,changes,require);require(expected==[pack],'photo V35 changed unreviewed scene, candidate or hard duty')
    old_proof_path=regular(root,proof['previous_proof']);require(v._sha256(old_proof_path)==proof['previous_proof_sha256']==v34.PROOF_SHA256,'photo V35 predecessor proof drift');old_proof=json.loads(old_proof_path.read_bytes())
    inventory={p.name:v._sha256(regular(root,p.relative_to(root).as_posix())) for p in (root/PHOTO).glob('*.json')}
    require(proof['source_inventory_before']==old_proof['source_inventory_after'] and inventory==proof['source_inventory_after'] and set(inventory)==set(proof['source_inventory_before'])|{Path(p).name for p in ADDED} and all(inventory[n]==s for n,s in proof['source_inventory_before'].items() if (PHOTO/n).as_posix() not in CHANGED) and set(proof['source_files_after'])==set(old_proof['source_files_after'])|ADDED and all(proof['source_files_after'][n]==s for n,s in old_proof['source_files_after'].items() if n not in CHANGED),'photo V35 unrelated authored source or runtime changed')
    for group in ('source_files_after','evidence_files','active_shards_after','retained_shards_before'):require(all(v._sha256(regular(root,n))==s for n,s in proof[group].items()),'photo V35 source, shard or evidence drift: '+group)
    require(proof['retained_shards_before']==old_proof['active_shards_after'],'photo V35 prior active shard inventory drift')
    require(baseline['frozen_inputs']==old_baseline['frozen_inputs']==proof['frozen_inputs'] and all(v._sha256(regular(root,n))==s for n,s in proof['frozen_inputs'].items()) and v._public_photo_candidate_count(pack)==proof['preserved_public_candidate_count']==64,'photo V35 frozen request or public count drift')
    for field in ('preserved_contract_sha256','negative_en','private_fields_absent'):require(baseline[field]==old_baseline[field],'photo V35 preserved baseline contract drift: '+field)
    records={r['path']:r for r in parent['members']};manifest=(PHOTO/'photo_prompt_source_manifest.json').as_posix();old=json.loads(exact_payload(root,records[manifest]))['sources'];new=json.loads(regular(root,manifest).read_bytes())['sources']
    require(new[:-2]==old and {r['file'] for r in new[-2:]}=={Path(p).name for p in ADDED} and all(r['required'] is True and r['load_order']==max(x['load_order'] for x in old if x['kind']==r['kind'])+1 for r in new[-2:]),'photo V35 registration replaced prior meaning')
    candidate=json.loads(regular(root,PHOTO/'photo_prompt_ethereal_gothic_scene_extension.json').read_bytes());profiles=json.loads(regular(root,PHOTO/'photo_prompt_visual_obligations_ethereal_gothic_scene.json').read_bytes())
    require(sum(len(rows) for rows in candidate['slots'].values())==60 and len(profiles['profiles'])==41 and len(candidate['visual_semantics'])==68 and sum(len(rows) for rows in candidate['existing_slot_context_extensions'].values())==5,'photo V35 authored DATA count drift')
    ref=candidate['maintenance_ref'];record=json.loads(regular(root,'docs/research-evidence/photo-prompt/extension-maintenance/'+ref['record_id']+'.json').read_bytes())
    require(ref['record_id']=='ethereal-gothic-20261007-v2' and record['maintenance_only'] is True and digest(json.dumps(record,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())==ref['sha256'],'photo V35 maintenance record drift')
    for row in parent['members']:exact_payload(root,row)
    descriptor=(ILL/'assets/universal_scene_baseline_v2.json').as_posix();old_descriptor=exact_payload(root,records[descriptor]);old_hash=proof['previous_validator_sha256'].encode()
    require(digest(old_descriptor)==proof['previous_universal_descriptor_sha256'] and old_descriptor.count(old_hash)==1 and regular(root,descriptor).read_bytes()==old_descriptor.replace(old_hash,v._sha256(Path(v.__file__)).encode(),1),'photo V35 universal descriptor changed beyond validator binding')
    if receipt is not None:
        require(all(receipt.get(k)==proof[k] for k in ('generation_id','source_fingerprint','algorithm_sha256')),'photo V35 receipt source generation drift')
        from photo_runtime_sources import RuntimeSnapshotProvider
        RuntimeSnapshotProvider().from_receipt(pack,receipt)
