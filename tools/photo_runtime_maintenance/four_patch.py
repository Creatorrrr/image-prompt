"""Construct exact function-only patches and independent private test projects."""
import argparse
import ast
import difflib
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

import checks
import four_state as scope
from history_state import new
from logic_pilot import remove
import state


SMOKE = r'''
import hashlib,json,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve();removed=json.loads(sys.argv[2]);sys.path.insert(0,str(root/'scripts'))
import bm25f_retrieval as bm,photo_native_pack as pack,photo_camera_evidence as camera,photo_runtime_sources as runtime
assert '모에' not in bm.tokenize_bm25f_text('외모에 어울리는',lexicon=['모에'])
assert '모에' in bm.tokenize_bm25f_text('모에',lexicon=['모에'])
roles={'lighting':{'candidates':[{'id':'same'}]}}
assert pack.role_cards(pack.WorkingPack({},roles)) is roles
wire={'contract_version':pack.CONTRACT,'candidate_pool':{},'role_proposals':{},'role_views':{'lighting':{'candidate_refs':[]}}}
assert pack.role_cards(json.loads(json.dumps(wire)))=={'lighting':{'candidates':[]}}
assert camera.camera_authoring_declaration({}) is None
assert set(camera.CAMERA_AXES)=={'direction','height'}
runtime._require_implementation({'code':runtime.LOADED_CODE,'environment':runtime.LOADED_ENVIRONMENT},None)
bad={'code':{**runtime.LOADED_CODE,'scripts/changed.py':'wrong'},'environment':runtime.LOADED_ENVIRONMENT}
try:runtime._require_implementation(bad,None)
except runtime.FreshnessError as error:assert error.state=='runtime_restart_required'
else:raise AssertionError('implementation guard weakened')
loaded={}
for module in (bm,pack,camera,runtime):
 p=Path(module.__file__).resolve();assert p.is_relative_to(root)
 loaded[module.__name__]={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
for name,filename in removed.items():
 module=next(m for m in (bm,pack,camera,runtime) if Path(m.__file__).name==filename)
 assert not hasattr(module,name)
print(json.dumps({'status':'PASS','loaded_modules':loaded,'removed_functions':sorted(removed),
 'functional_checks':['lexicon_boundaries','working_and_wire_role_cards','camera_empty_core','matched_and_mismatched_implementation'],
 'model_calls':0,'Gemini_calls':0,'CURRENT_writes':0}))
'''


def policy():
    live = scope.SKILL
    return checks.profile()+'(deny file-read* '+ ' '.join(
        '(subpath '+json.dumps(str(live/p))+')' for p in ('scripts','precore'))+')'


def copy_code(project):
    skill = project/'skills/photo-prompt-image-generator'
    for part in ('scripts','precore'):
        (skill/part).mkdir(parents=True)
        for source in (scope.SKILL/part).glob('*.py'):
            shutil.copy2(source,skill/part/source.name)
        for source in (scope.SKILL/part).rglob('*'):
            if source.is_file() and source.suffix not in {'.py','.pyc','.pyo'} and '__pycache__' not in source.parts:
                destination=skill/part/source.relative_to(scope.SKILL/part)
                destination.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(source,destination)
    for filename in ('retrieval-runtime.json','embedding-default.json','embedding-runtime.lock.json'):
        shutil.copy2(scope.SKILL/filename,skill/filename)
    return skill


def prepare():
    if (scope.E/'PRIVATE-PROJECTS.json').exists():raise FileExistsError('private projects already prepared')
    targets = state.read(scope.E/'TARGETS.json')['targets']
    approved = {r['name'] for r in state.read(scope.E/'REFERENCE-REVIEW.json')['rows'] if r['decision']=='REMOVE_CANDIDATE'}
    if approved!=set(scope.FUNCTIONS):raise ValueError('reference-deferred candidate; prepare a narrower reviewed scope')
    parent = Path(tempfile.mkdtemp(prefix='photo-four-private-'))
    original = {r['path']:(scope.ROOT/r['path']).read_bytes() for r in targets}
    smoke_results = {};patches = {};projects = {}
    cases = [('control',{}),*[(n,{n:f}) for n,f in scope.FUNCTIONS.items()],('combined',scope.FUNCTIONS)]
    python = scope.SKILL/'.runtime/embedding-python/bin/python'
    for label,functions in cases:
        project = parent/label;skill = copy_code(project);projects[label]=str(project)
        patch = []
        for name,filename in functions.items():
            relative = 'skills/photo-prompt-image-generator/scripts/'+filename
            before = original[relative];after = remove(before,[name]);(project/relative).write_bytes(after)
            old_tree=ast.parse(before);old_tree.body=[n for n in old_tree.body if not (isinstance(n,ast.FunctionDef) and n.name==name)]
            if ast.dump(old_tree,include_attributes=False)!=ast.dump(ast.parse(after),include_attributes=False):
                raise ValueError('change outside approved function')
            patch.extend(difflib.unified_diff(before.decode().splitlines(True),after.decode().splitlines(True),
                fromfile='a/'+relative,tofile='b/'+relative))
        raw=''.join(patch).encode();patch_path=scope.E/('PATCH-'+label+'.patch.gz')
        executable_patch=parent/('PATCH-'+label+'.patch')
        if functions:
            patch_path.write_bytes(gzip.compress(raw,mtime=0));executable_patch.write_bytes(raw)
            subprocess.run(['git','-C',str(project),'apply','--reverse','--check',str(executable_patch)],check=True)
            subprocess.run(['git','-C',str(project),'apply','--reverse',str(executable_patch)],check=True)
            for filename in functions.values():
                rel='skills/photo-prompt-image-generator/scripts/'+filename
                if (project/rel).read_bytes()!=original[rel]:raise ValueError('inverse patch did not restore bytes')
            subprocess.run(['git','-C',str(project),'apply',str(executable_patch)],check=True)
            patches[label]={'path':str(patch_path.relative_to(scope.ROOT)),'sha256':state.sha(patch_path),
                'raw_sha256':hashlib.sha256(raw).hexdigest(),
                'functions':list(functions),'inverse_exact':True,
                'candidate_files':{'skills/photo-prompt-image-generator/scripts/'+f:state.sha(skill/'scripts'/f) for f in functions.values()}}
        process = subprocess.run(['/usr/bin/sandbox-exec','-p',policy(),str(python),'-I','-c',SMOKE,
            str(skill),json.dumps(functions)],env=checks.environment(),capture_output=True,text=True,timeout=60)
        if process.returncode:raise ValueError(label+' smoke failed: '+process.stderr+process.stdout)
        smoke_results[label]=json.loads(process.stdout)
        print('private function smoke PASS:',label,flush=True)
    candidate = Path(projects['combined']);skill=candidate/'skills/photo-prompt-image-generator'
    # APFS clones are independent regular files, never source hardlinks.
    subprocess.run(['/bin/cp','-c','-R','-p',str(scope.SKILL/'assets'),str(skill/'assets')],check=True)
    shutil.copytree(scope.ROOT/'tests',candidate/'tests',ignore=shutil.ignore_patterns('__pycache__'))
    (candidate/'docs').symlink_to(scope.ROOT/'docs',target_is_directory=True)
    lock=state.read(scope.SKILL/'embedding-runtime.lock.json');package=skill/lock['package']
    package.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['/bin/cp','-c','-R','-p',str(scope.SKILL/lock['package']),str(package)],check=True)
    (skill/'.runtime/embedding-python').symlink_to(scope.SKILL/'.runtime/embedding-python',target_is_directory=True)
    control=Path(projects['control'])/'skills/photo-prompt-image-generator'
    (control/'.runtime').symlink_to(scope.SKILL/'.runtime',target_is_directory=True)
    new(scope.E/'PATCHES.json',{'schema':'photo-four-private-patches/v1','patches':patches,
        'combined_source_lines_removed':sum(r['lines'] for r in targets)})
    new(scope.E/'PRIVATE-PROJECTS.json',{'schema':'photo-four-private-projects/v1','projects':projects,
        'private_parent':str(parent),'source_code_files':77,'tests_copied':True,'assets_independent_APFS_clones':True,
        'model_files':len(lock['files']),'model_package_independent':True,'docs_readonly_original_inputs':True,
        'private_paths_are_execution_scratch_not_recovery_sources':True})
    new(scope.E/'SOURCE-SMOKE-03.json',{'status':'PASS','cases':smoke_results,
        'live_source_reads_denied':True,'original_writes_denied':True,'network_denied':True})
    new(scope.E/'STAGE03.json',{'status':'PASS','functions':4,'removed_lines_in_private_only':50,
        'control_and_each_function_and_combined_cases':6,'inverse_exact':True,'original_source_changes':0,
        'Gemini_calls':0,'CURRENT_writes':0})


def apply_qualified():
    """Apply the already qualified exact patch once; never publish a generation."""
    if (scope.E/'APPLICATION.json').exists() or (scope.E/'APPLY-INTENT.json').exists():
        raise FileExistsError('application already started; inspect instead of repeating')
    for number in range(1,7):
        if state.read(scope.E/('STAGE'+str(number).zfill(2)+'.json'))['status']!='PASS':
            raise ValueError('required stage did not pass')
    targets=state.read(scope.E/'TARGETS.json')['targets']
    current=state.status(scope.ROOT)
    if state.git(scope.ROOT,'diff','--cached','--name-only'):
        raise ValueError('preserve original staging')
    originals={}
    for target in targets:
        path=scope.ROOT/target['path']
        if target['path'] in current or state.sha(path)!=target['source_sha256']:
            raise ValueError('target changed; defer before application')
        originals[target['path']]=path.read_bytes()
    patch=state.read(scope.E/'PATCHES.json')['patches']['combined']
    archive=scope.ROOT/patch['path']
    if state.sha(archive)!=patch['sha256']:raise ValueError('patch archive changed')
    raw=gzip.decompress(archive.read_bytes())
    if hashlib.sha256(raw).hexdigest()!=patch['raw_sha256']:raise ValueError('raw patch changed')
    with tempfile.TemporaryDirectory(prefix='four-apply-') as temp:
        file=Path(temp)/'qualified.patch';file.write_bytes(raw)
        subprocess.run(['git','-C',str(scope.ROOT),'apply','--check',str(file)],check=True)
        new(scope.E/'APPLY-INTENT.json',{'original_files':{t['path']:t['source_sha256'] for t in targets},
            'candidate_files':patch['candidate_files'],'patch_raw_sha256':patch['raw_sha256'],
            'gate_evidence':{str(n):state.sha(scope.E/('STAGE'+str(n).zfill(2)+'.json')) for n in range(1,7)}})
        subprocess.run(['git','-C',str(scope.ROOT),'apply',str(file)],check=True)
        try:
            for target in targets:
                rel=target['path'];path=scope.ROOT/rel
                if state.sha(path)!=patch['candidate_files'][rel]:raise ValueError('applied bytes differ from tested copy')
                tree=ast.parse(originals[rel]);tree.body=[n for n in tree.body if not (isinstance(n,ast.FunctionDef) and n.name==target['name'])]
                if ast.dump(tree,include_attributes=False)!=ast.dump(ast.parse(path.read_bytes()),include_attributes=False):
                    raise ValueError('unapproved AST change')
        except Exception:
            subprocess.run(['git','-C',str(scope.ROOT),'apply','--reverse','--check',str(file)],check=True)
            subprocess.run(['git','-C',str(scope.ROOT),'apply','--reverse',str(file)],check=True)
            raise
    stat=state.git(scope.ROOT,'diff','--numstat','--',*sorted(scope.SOURCE_PATHS)).decode().splitlines()
    if sum(int(s.split('\t')[0]) for s in stat)!=0 or sum(int(s.split('\t')[1]) for s in stat)!=50:
        raise ValueError('diff exceeds exact 50-line removal')
    new(scope.E/'APPLICATION.json',{'status':'APPLIED_PENDING_POSTCHECKS','applied':patch['candidate_files'],
        'functions':list(scope.FUNCTIONS),'removed_lines':50,'raw_patch_sha256':patch['raw_sha256'],
        'remaining_AST_equal':True,'source_publish_calls':0,'Gemini_calls':0,'CURRENT_writes':0})
    print('Applied qualified four-function patch; exactly 50 removed source lines',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('prepare','apply'),nargs='?',default='prepare')
    args=parser.parse_args()
    prepare() if args.command=='prepare' else apply_qualified()
