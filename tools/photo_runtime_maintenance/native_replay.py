"""Explicit, read-only replay of a run's original generation. Never publish or fall back."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

import checks
import state as maintenance

HASH = re.compile(r'[0-9a-f]{64}\Z')


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,
        separators=(',', ':'),allow_nan=False).encode()).hexdigest()


def regular(path):
    path = Path(path)
    require(path.is_file() and not path.is_symlink(),'missing_or_symlink_file: '+str(path))
    return path


def member(root, name):
    relative = PurePosixPath(name)
    require(bool(name) and not relative.is_absolute() and '..' not in relative.parts
            and '\\' not in name and str(relative) == name,'unsafe_member')
    path = Path(root)
    for part in relative.parts:
        path = path/part
        require(not path.is_symlink(),'symlink_member')
    return regular(path)


def read(path):
    return json.loads(regular(path).read_bytes())


def artifact(workflow, name):
    row = workflow['artifacts'][name]
    path = regular(row['path'])
    require(maintenance.sha(path) == row['sha256'],'artifact_changed: '+name)
    value = read(path)
    return value[0] if isinstance(value,list) and len(value) == 1 else value


def pack_bindings(pack):
    return {'tags_hash':(pack.get('provenance') or {}).get('tags_hash'),
        'authorial_core_sha256':(pack.get('authorial_core') or {}).get('canonical_sha256'),
        'global_retrieval_sha256':(pack.get('global_retrieval') or {}).get('canonical_sha256'),
        'corpus_sha256':(pack.get('global_retrieval') or {}).get('corpus_sha256'),
        'visual':{key:digest(pack.get(key)) for key in (
            'visual_obligations','visual_concept_candidates','semantic_clarification')}}


def inspect_run(run, *, full=False):
    """Verify original metadata/code, optionally every asset. No generation code imports."""
    workflow = read(Path(run)/'workflow.json')
    pack = artifact(workflow,'pack')
    receipt = artifact(workflow,'runtime_receipt')
    require(isinstance(pack,dict) and isinstance(receipt,dict),'invalid_pack_or_receipt')
    require(receipt.get('schema') == 'photo-runtime-receipt/v3','unsupported_receipt')
    require(digest({k:v for k,v in receipt.items() if k != 'canonical_sha256'})
            == receipt.get('canonical_sha256'),'receipt_checksum')
    require(receipt.get('pack_sha256') == digest(pack),'receipt_pack_mismatch')
    require(receipt.get('bindings') == pack_bindings(pack),'receipt_bindings_mismatch')
    binding = workflow['source_binding']
    store = Path(binding['runtime_store'])
    require(store.is_dir() and not store.is_symlink(),'store_missing_or_symlink')
    store = store.resolve()
    require(not (store/'generations').is_symlink(),'symlink_generation_directory')
    generation = receipt['generation_id']
    require(isinstance(generation,str) and HASH.fullmatch(generation),'invalid_generation')
    require(binding['generation_id'] == generation
            and binding['source_fingerprint'] == receipt['source_fingerprint'],'run_binding_mismatch')
    request = receipt['request_id']
    require(isinstance(request,str) and re.fullmatch('[0-9a-f]{32}',request),'invalid_request_id')
    require(read(member(store,'receipts/'+request+'.json')) == receipt,'original_issued_receipt_missing_or_changed')
    root = store/'generations'/generation
    require(root.is_dir() and not root.is_symlink(),'generation_missing_or_symlink')
    manifest = read(member(root,'manifest.json'))
    require(digest(manifest) == generation and manifest.get('schema') == 'photo-runtime-generation/v3',
            'generation_checksum_or_schema')
    require(digest(manifest['source']) == manifest['source_fingerprint'],'source_checksum')
    for name in ('source_fingerprint','algorithm_sha256'):
        require(manifest[name] == receipt[name],'receipt_generation_'+name)
    require(manifest['search_layout']['layout_sha256'] == receipt['search_layout_sha256'],
            'receipt_generation_layout')
    require(manifest['search_layout']['corpus_sha256'] == pack['global_retrieval']['corpus_sha256'],
            'receipt_generation_corpus')
    code = manifest['source']['code']
    actual = {str(p.relative_to(root)) for directory in ('scripts','precore')
              for p in (root/directory).glob('*.py')}
    require(actual == set(code),'executable_closure_changed')
    for name, expected in code.items():
        require(name in manifest['members'],'undeclared_code')
        require(maintenance.sha(member(root,name)) == expected,'code_checksum: '+name)
        require(manifest['members'][name]['sha256'] == expected,'member_code_binding')
    for name,row in manifest['members'].items():
        path = member(root,name)
        if full:
            require(path.stat().st_size == row['bytes'] and maintenance.sha(path) == row['sha256'],
                    'member_checksum: '+name)
    return {'status':'PASS','schema':'photo-explicit-native-replay/v1','run':str(Path(run).resolve()),
        'store':str(store),'generation_id':generation,'generation_root':str(root),
        'code_sha256':digest(code),'code_files':len(code),'members':len(manifest['members']),
        'full_member_hashes_verified':full,'receipt_sha256':receipt['canonical_sha256'],
        'source_fingerprint':manifest['source_fingerprint'],'algorithm_sha256':manifest['algorithm_sha256'],
        'scope':'original metadata/code verification; not semantic or runtime audit',
        'model_calls':0,'Gemini_calls':0,'CURRENT_writes':0}


WORKER = """
import hashlib,json,sys
from pathlib import Path
generation=Path(sys.argv[1]);run=Path(sys.argv[2])
manifest=json.loads((generation/'manifest.json').read_bytes())
def digest(value):return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
if digest(manifest)!=sys.argv[3]:raise ValueError('worker_generation_changed_before_import')
actual={str(p.relative_to(generation)) for d in ('scripts','precore') for p in (generation/d).glob('*.py')}
if actual!=set(manifest['source']['code']):raise ValueError('worker_executable_closure_changed')
for name,expected in manifest['source']['code'].items():
 path=generation/name
 if path.is_symlink() or path.parent.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:raise ValueError('worker_code_changed_before_import')
sys.path.insert(0,str(generation/'scripts'))
import photo_local_embedding as local,photo_embedding_provider as provider
def forbidden(*args,**kwargs):raise RuntimeError('replay_forbids_new_embedding_calls')
local.infer=forbidden
provider.embed=forbidden;provider.embed_many=forbidden
from photo_workflow_state import load_state,value
from photo_workflow_worker import audit_bound
from photo_runtime_sources import RuntimeSnapshotProvider
state=load_state(run)
snapshot=RuntimeSnapshotProvider(store=Path(state['source_binding']['runtime_store'])).from_receipt(value(state,'pack'),value(state,'runtime_receipt'))
result=audit_bound(state)['composed_audit']
if result['status']!='pass' or result['failures']:raise ValueError('original_frozen_audit_failed')
print(json.dumps({'status':'PASS','generation_id':snapshot.generation_id,'audit_status':result['status'],
 'code_root':str(generation),'model_calls':0,'Gemini_calls':0,'CURRENT_writes':0}))
"""


def audit(run):
    verified = inspect_run(run,full=True)
    python = maintenance.ROOT/'skills/photo-prompt-image-generator/.runtime/embedding-python/bin/python'
    # Root itself stays readable for bound input files, never for executable source fallback.
    live = maintenance.ROOT/'skills/photo-prompt-image-generator'
    policy = checks.profile()+'(deny file-read* '+ ' '.join(
        '(subpath '+json.dumps(str(live/p))+')' for p in ('scripts','precore'))+')'
    process = subprocess.run(['/usr/bin/sandbox-exec','-p',policy,str(python),'-I','-c',WORKER,
        verified['generation_root'],verified['run'],verified['generation_id']],capture_output=True,text=True,
        env=checks.environment(),timeout=240)
    if process.returncode:
        return {**verified,'status':'DEFER','reason':'original_frozen_audit_unavailable',
            'exit_code':process.returncode,'stdout':process.stdout,'stderr':process.stderr,
            'network_denied':True,'live_source_fallback_denied':True}
    result = json.loads(process.stdout)
    require(result['generation_id'] == verified['generation_id'],'worker_generation_mismatch')
    return {**verified,'runtime_audit':result,'scope':'original frozen receipt and composition audit',
        'network_denied':True,'live_source_fallback_denied':True}


def main():
    parser = argparse.ArgumentParser(description=__doc__,allow_abbrev=False)
    parser.add_argument('command',choices=('inspect','verify','audit'))
    parser.add_argument('--run',type=Path,required=True)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    if args.output and args.output.exists():
        raise FileExistsError('never overwrite evidence')
    try:
        result = audit(args.run) if args.command == 'audit' else inspect_run(args.run,full=args.command == 'verify')
    except (ValueError,KeyError,TypeError,OSError,subprocess.TimeoutExpired) as error:
        result = {'status':'DEFER','reason':str(error),'Gemini_calls':0,'CURRENT_writes':0}
    if args.output:
        from history_state import new
        new(args.output,result)
    print(json.dumps(result,ensure_ascii=False),flush=True)
    return 0 if result['status'] == 'PASS' else 2


if __name__ == '__main__':
    sys.exit(main())
