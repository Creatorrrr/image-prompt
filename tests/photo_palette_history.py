"""Authenticated V33 DATA successor and exact offline V32 recovery."""
from __future__ import annotations

import builtins
import errno
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

PROOF=Path('docs/research-evidence/photo-prompt/color-palette-main-merge-20261007/V33-PALETTE-DATA-PROOF.json')
PARENT=PROOF.parent/'V32-PARENT-SOURCE.json'
PROOF_SHA256='9fe462ebda03f4dedb4038390f8d4b56929bd19157562d32f34b7529f9010eb0'
PARENT_SHA256='07d295cf839e2b21030bb0d2ca8d90b7e826f64f01ae4f4be9a57997bc77c30d'
PARENT_PIN='96e20422316276a4e0b5ed97f44152e4931e7504'
PARENT_TREE='ae809d09bc01042c15b77271764036871d28949d'
PHOTO=Path('skills/photo-prompt-image-generator/assets')
ILLUSTRATION=Path('skills/subculture-illustration-image-generator')
EVOLVING=frozenset((PHOTO/n).as_posix() for n in (
    'photo_prompt_source_manifest.json','photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json'))
ADDED=frozenset((PHOTO/n).as_posix() for n in (
    'photo_prompt_palette_applications_extension.json','photo_prompt_visual_obligations_palette_applications.json'))
PACK_POINTERS=frozenset({
    '/0/core_retrieval/canonical_sha256','/0/core_retrieval/slot_corpus_sha256','/0/core_retrieval/slot_ownership_sha256','/0/pack_id','/0/provenance/tags_hash',
    '/0/creative_augmentation/candidates','/0/creative_augmentation/hard_eligible_pool_sha256','/0/semantic_clarification/candidates','/0/visual_concept_candidates/candidates',
    '/0/slots/color/candidate_count','/0/slots/color_grading/candidate_count','/0/slots/lighting/candidate_count','/0/slots/texture/candidate_count',
    '/0/slots/color_grading/candidates/1','/0/slots/texture/candidates/0',
})

def _fixtures():
    from tests import photo_prompt_fixtures
    return photo_prompt_fixtures

def _sha(raw):return hashlib.sha256(raw).hexdigest()

def _exact_payload(root,row):
    """A sealed V32 backing is never repaired through mutable successor data."""
    path=_fixtures()._v24_regular_path(root,row['source_path'])
    raw=path.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode('ascii')+b'\0'+raw).hexdigest()
    if (path.stat().st_mode&0o7777!=int(row['mode'][-3:],8)
            or len(raw)!=row['bytes'] or _sha(raw)!=row['sha256'] or blob!=row['git_blob']):
        raise AssertionError('Frozen V32 exact historical source payload or mode drift: '+row['path'])
    return raw

def context(root):
    return any((root/p).exists() or (root/p).is_symlink() for p in (
        PROOF,PARENT,ILLUSTRATION/'assets/photo_regression_baseline_v33.json'))

def transition(root):
    """Pin shape, Git identity, backing paths and complete member identity."""
    f=_fixtures()
    raw=f._v24_regular_path(root,PROOF.as_posix()).read_bytes()
    parent_raw=f._v24_regular_path(root,PARENT.as_posix()).read_bytes()
    if _sha(raw)!=PROOF_SHA256 or _sha(parent_raw)!=PARENT_SHA256:
        raise AssertionError('Frozen V33 palette proof or V32 parent manifest drift')
    proof,parent=json.loads(raw),json.loads(parent_raw)
    rows=parent.get('members') or []
    if (proof.get('schema')!='photo-palette-application-data-transition/v33'
            or proof.get('parent_manifest')!=PARENT.as_posix()
            or proof.get('parent_manifest_sha256')!=PARENT_SHA256
            or proof.get('previous_qualified_commit')!=PARENT_PIN
            or proof.get('previous_qualified_tree')!=PARENT_TREE
            or proof.get('parent_member_count')!=1369
            or parent.get('schema')!='photo-v32-parent-source-manifest/v1'
            or parent.get('source_pin')!=PARENT_PIN or parent.get('source_tree')!=PARENT_TREE
            or parent.get('member_count')!=len(rows) or len(rows)!=1369
            or parent.get('total_member_bytes')!=2599273290
            or len(proof.get('source_files_after',{}))!=150
            or len(proof.get('source_inventory_after',{}))!=101
            or set(proof.get('preserved_source_paths',[]))!=EVOLVING):
        raise AssertionError('Frozen V33 source lineage or inventory drift')
    paths,backings=set(),{}
    for row in rows:
        name=f._v17_safe_path(row['path']).as_posix()
        source=f._v17_safe_path(row['source_path']).as_posix()
        identity=tuple(row.get(k) for k in ('git_blob','mode','bytes','sha256'))
        if (name in paths or row.get('git_commit')!=PARENT_PIN or row.get('git_path')!=name
                or row.get('mode') not in ('100644','100755')
                or type(row.get('bytes')) is not int or row['bytes']<0
                or not isinstance(row.get('sha256'),str) or len(row['sha256'])!=64
                or not isinstance(row.get('git_blob'),str) or len(row['git_blob'])!=40
                or any(c not in '0123456789abcdef' for c in row['sha256']+row['git_blob'])
                or (source in backings and backings[source]!=identity)):
            raise AssertionError('Frozen V32 historical source provenance drift')
        paths.add(name);backings[source]=identity
    if (sum(r['bytes'] for r in rows)!=parent['total_member_bytes']
            or any(p.as_posix() in paths for n in paths for p in Path(n).parents)
            or any(p.as_posix() in backings for n in backings for p in Path(n).parents)):
        raise AssertionError('Frozen V32 historical source member overlap drift')
    originals={r['path']:r for r in rows}
    if any(originals[n]['source_path']==n or originals[n]['sha256']==proof['source_files_after'][n] for n in EVOLVING):
        raise AssertionError('Frozen V33 preserved source mapping drift')
    return proof,parent

def previous_payload(root,name,current):
    """Validate the live successor, then normalize only its three known edits."""
    if name not in EVOLVING or not context(root):return current
    f=_fixtures();proof,parent=transition(root)
    row=next(r for r in parent['members'] if r['path']==name)
    live=f._v24_regular_path(root,name)
    if (_sha(live.read_bytes())!=proof['source_files_after'][name]
            or live.stat().st_mode & 0o7777 != int(row['mode'][-3:],8)):
        raise AssertionError('Frozen V33 retained live source payload or mode drift: '+name)
    original=_exact_payload(root,row)
    if _sha(current) not in {proof['source_files_after'][name],row['sha256']}:
        raise AssertionError('Frozen V33 supplied source payload drift: '+name)
    return original

def preserved_payload(root,row,current):
    if row['source_path']!=row['path'] or row['path'] not in EVOLVING or not context(root):return None
    f=_fixtures();_,parent=transition(root)
    original=next(r for r in parent['members'] if r['path']==row['path'])
    prior=previous_payload(root,row['path'],current)
    if _sha(current)==original['sha256']:return None
    if all(row[k]==original[k] for k in ('sha256','git_blob','bytes','mode')):return prior
    for restore in (f._v32_preserved_retained_payload,f._v31_preserved_retained_payload,
                    f._v30_preserved_retained_payload,f._v29_preserved_retained_payload,
                    f._v28_preserved_retained_payload,f._v27_preserved_retained_payload):
        raw=restore(root,row,prior)
        if raw is not None:return raw
    return None

def materialize_v32_parent_source(directory,*,source_root,link_verified=False):
    """Publish an offline exact tree atomically; optional test links are verified."""
    f=_fixtures();f._v24_empty_destination(directory)
    _,parent=transition(source_root)
    directory.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.sealed-v32-',dir=directory.parent) as temporary:
        staged=Path(temporary)/'tree';staged.mkdir()
        for row in parent['members']:
            raw=_exact_payload(source_root,row)
            target=staged/f._v17_safe_path(row['path']);target.parent.mkdir(parents=True,exist_ok=True)
            if link_verified:
                try:os.link(f._v24_regular_path(source_root,row['source_path']),target)
                except OSError as exc:
                    if exc.errno!=errno.EXDEV:raise
                    target.write_bytes(raw);target.chmod(int(row['mode'][-3:],8))
            else:target.write_bytes(raw);target.chmod(int(row['mode'][-3:],8))
        # V32 validates V31's original backing paths as well as logical files.
        # Their mapping and payload identity are already sealed by V32's proof.
        _, original_v31 = f._v32_transition(source_root)
        for row in original_v31['members']:
            if row['source_path'] == row['path']:
                continue
            raw = f._v24_verified_payload(source_root, row)
            target = staged / f._v17_safe_path(row['source_path'])
            if target.exists():
                if target.read_bytes() != raw or target.stat().st_mode & 0o7777 != int(row['mode'][-3:], 8):
                    raise AssertionError('Frozen V32 archived backing collision: ' + row['source_path'])
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            if link_verified:
                try:
                    os.link(f._v24_regular_path(source_root, row['source_path']), target)
                except OSError as exc:
                    if exc.errno != errno.EXDEV:
                        raise
                    target.write_bytes(raw); target.chmod(int(row['mode'][-3:], 8))
            else:
                target.write_bytes(raw); target.chmod(int(row['mode'][-3:], 8))
        f._v24_empty_destination(directory);staged.replace(directory)
    return parent

def pinned_v32_validator(directory,*,source_root):
    """Use exact V32 code and imports, never a live same-named module."""
    f=_fixtures();_,parent=transition(source_root)
    rows={r['path']:r for r in parent['members']}
    scripts=directory/ILLUSTRATION/'scripts'
    prefix='_archived_photo_v32_'+hashlib.sha256(str(directory).encode()).hexdigest()[:16]
    modules,payloads={},{}
    for name in ('illustration_runtime','illustration_audit','universal_scene_runtime','validate_illustration_assets'):
        path=scripts/(name+'.py');row=rows[path.relative_to(directory).as_posix()]
        payloads[name]=_exact_payload(directory,dict(row,source_path=row['path']))
        spec=importlib.util.spec_from_file_location(prefix+'_'+name,path)
        modules[name]=importlib.util.module_from_spec(spec)
    def historical_import(name,globals=None,locals=None,fromlist=(),level=0):
        if level==0 and name in modules:return modules[name]
        return builtins.__import__(name,globals,locals,fromlist,level)
    previous={m.__name__:sys.modules.get(m.__name__) for m in modules.values()}
    try:
        for m in modules.values():
            m.__dict__['__builtins__']=dict(vars(builtins),__import__=historical_import);sys.modules[m.__name__]=m
        for name,m in modules.items():exec(compile(payloads[name],m.__file__,'exec'),m.__dict__)
    finally:
        for name,original in previous.items():
            if original is None:sys.modules.pop(name,None)
            else:sys.modules[name]=original
    return modules['validate_illustration_assets']

def resolve_v32_python(source_root):
    """Require the sealed interpreter binding; never rewrite receipt hashes."""
    _, parent = transition(source_root)
    name = 'docs/research-evidence/photo-prompt/robe-back-source-consistency-20261006/CURRENT-GENERATION.json'
    row = next(r for r in parent['members'] if r['path'] == name)
    expected = json.loads(_exact_payload(source_root, row))['source']['environment']
    configured = os.environ.get('PHOTO_V32_PYTHON')
    candidates = [configured] if configured else [
        sys.executable,
        str(Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'),
        shutil.which('python3.' + str(expected['python'][1])),
    ]
    probe = (
        "import json,sys,unicodedata; print(json.dumps({"
        "'implementation':sys.implementation.name,'python':list(sys.version_info[:3]),"
        "'unicode':unicodedata.unidata_version}))"
    )
    for candidate in dict.fromkeys(p for p in candidates if p):
        try:
            result = subprocess.run([candidate, '-c', probe], capture_output=True,
                                    text=True, timeout=10, check=True)
            if json.loads(result.stdout) == expected:
                return Path(candidate).resolve()
        except (OSError, ValueError, subprocess.SubprocessError):
            continue
    raise AssertionError('Exact V32 Python/Unicode binding unavailable; set PHOTO_V32_PYTHON: '
                         + json.dumps(expected, sort_keys=True))

def replay_v32(directory, *, source_root):
    """Run the original publisher and validator in their exact Python version."""
    interpreter = resolve_v32_python(source_root)
    executable = directory / '.venv/bin/python'
    executable.parent.mkdir(parents=True, exist_ok=True)
    if executable.exists() or executable.is_symlink():
        if executable.resolve() != interpreter:
            raise AssertionError('Original V32 replay interpreter path drift')
    else:
        executable.symlink_to(interpreter)
    code = (
        "import json,sys; from pathlib import Path; "
        "sys.path.insert(0,'skills/photo-prompt-image-generator/scripts'); "
        "from photo_runtime_sources import SnapshotPublisher; SnapshotPublisher().publish(); "
        "sys.path.insert(0,'skills/subculture-illustration-image-generator/scripts'); "
        "import validate_illustration_assets as v; "
        "print(json.dumps(v.validate_photo_regression_baseline("
        "Path('skills/subculture-illustration-image-generator/assets'),baseline_version=32)))"
    )
    with tempfile.TemporaryDirectory(prefix='photo-v32-runtime-') as store:
        environment = os.environ.copy()
        environment['PHOTO_RUNTIME_STORE'] = store
        environment['GEMINI_API_KEY'] = ''; environment['GOOGLE_API_KEY'] = ''
        result = subprocess.run([str(interpreter), '-c', code], cwd=directory,
                                env=environment, capture_output=True, text=True, timeout=300)
    if result.returncode:
        raise AssertionError('Original V32 replay failed: ' + (result.stderr or result.stdout))
    return json.loads(result.stdout.strip().splitlines()[-1])

def qualify_current(v,asset_dir,repo_root,baseline,pack,raw,receipt=None):
    """Check every source and exact reviewed optional delta; preserve hard duties."""
    require=v._require
    try:proof,parent=transition(repo_root)
    except (AssertionError,OSError,ValueError) as exc:require(False,str(exc))
    require(baseline.get('palette_data_transition')=={
        'evidence_path':PROOF.as_posix(),'evidence_sha256':PROOF_SHA256,
        'previous_qualified_commit':PARENT_PIN,'parent_manifest_sha256':PARENT_SHA256},'photo V33 lineage drift')
    previous_raw=(asset_dir/'photo_regression_baseline_v32_pack.json').read_bytes()
    require(v._sha256(asset_dir/'photo_regression_baseline_v32.json')==proof['previous_manifest_sha256']
            and _sha(previous_raw)==proof['previous_pack_sha256']
            and _sha(raw)==proof['current_pack_sha256']==baseline['sha256']
            and raw==(asset_dir/'photo_regression_baseline_v33_pack.json').read_bytes()
            and json.loads(raw)==[pack] and pack['pack_id']==proof['current_pack_id'],'photo V33 frozen pack bytes drift')
    expected=json.loads(previous_raw)
    changes=proof['reviewed_pack_delta']
    require(len(changes)==15 and {r['pointer'] for r in changes}==PACK_POINTERS
            and proof['allowed_pack_delta_pointers']==sorted(PACK_POINTERS),'photo V33 unregistered pack delta')
    for row in changes:
        target=expected;parts=[p.replace('~1','/').replace('~0','~') for p in row['pointer'].split('/')[1:]]
        for part in parts[:-1]:target=target[int(part)] if isinstance(target,list) else target[part]
        key=int(parts[-1]) if isinstance(target,list) else parts[-1]
        require(target[key]==row['before'],'photo V33 original optional catalog drift');target[key]=row['after']
    require(expected==[pack],'photo V33 unreviewed request, candidate, scene or hard duty changed')
    require(v._public_photo_candidate_count(pack)==64==proof['preserved_public_candidate_count']
            and baseline['frozen_inputs']==proof['frozen_inputs']
            and all(v._sha256(v._photo_v28_regular_path(repo_root,n))==s for n,s in proof['frozen_inputs'].items()),'photo V33 frozen input or public count drift')
    priorproof,_=_fixtures()._v32_transition(repo_root)
    changed=EVOLVING|ADDED
    inventory={p.name:v._sha256(v._photo_v28_regular_path(repo_root,p.relative_to(repo_root).as_posix())) for p in (repo_root/PHOTO).glob('*.json')}
    require(proof['source_inventory_before']==priorproof['source_inventory_after']
            and inventory==proof['source_inventory_after']
            and set(inventory)==set(proof['source_inventory_before'])|{Path(p).name for p in ADDED}
            and all(inventory[n]==s for n,s in proof['source_inventory_before'].items() if (PHOTO/n).as_posix() not in EVOLVING)
            and set(proof['source_files_after'])==set(priorproof['source_files_after'])|ADDED
            and all(proof['source_files_after'][n]==s for n,s in priorproof['source_files_after'].items() if n not in changed),'photo V33 unrelated authored DATA or runtime changed')
    for group in ('source_files_after','active_shards_after','retained_shards_before','evidence_files'):
        require(all(v._sha256(v._photo_v28_regular_path(repo_root,n))==s for n,s in proof[group].items()),'photo V33 source, shard or evidence drift: '+group)
    require(proof['retained_shards_before']==priorproof['active_shards_after'],'photo V33 retained main shard inventory drift')
    maintenance=proof['maintenance_successor']
    require(v._sha256(v._photo_v28_regular_path(repo_root,maintenance['path']))==maintenance['sha256'],'photo V33 palette maintenance receipt drift')
    manifest=(PHOTO/'photo_prompt_source_manifest.json').as_posix()
    descriptor=(ILLUSTRATION/'assets/universal_scene_baseline_v2.json').as_posix()
    originals={}
    for row in parent['members']:
        payload=_exact_payload(repo_root,row)
        if row['path'] in {manifest,descriptor}:originals[row['path']]=payload
    old_rows=json.loads(originals[manifest])['sources'];new_rows=json.loads((repo_root/manifest).read_bytes())['sources']
    require(new_rows[:-2]==old_rows and {r['file'] for r in new_rows[-2:]}=={Path(p).name for p in ADDED}
            and all(r['required'] is True and r['load_order']==max(o['load_order'] for o in old_rows if o['kind']==r['kind'])+1 for r in new_rows[-2:]),'photo V33 replaced existing registration or added an unrelated source')
    old_descriptor=originals[descriptor];old_hash=proof['previous_validator_sha256'].encode('ascii')
    require(_sha(old_descriptor)==proof['previous_universal_descriptor_sha256']
            and old_descriptor.count(old_hash)==1
            and (repo_root/descriptor).read_bytes()==old_descriptor.replace(old_hash,v._sha256(Path(v.__file__)).encode('ascii'),1),'photo V33 universal descriptor changed beyond validator binding')
    if receipt is not None:
        require(receipt.get('generation_id')==proof['generation_id'] and receipt.get('source_fingerprint')==proof['source_fingerprint']
                and receipt.get('algorithm_sha256')==proof['algorithm_sha256'],'photo V33 receipt source generation drift')
        scripts=str(repo_root/'skills/photo-prompt-image-generator/scripts')
        if scripts not in sys.path:sys.path.insert(0,scripts)
        from photo_runtime_sources import RuntimeSnapshotProvider
        RuntimeSnapshotProvider().from_receipt(pack,receipt)
