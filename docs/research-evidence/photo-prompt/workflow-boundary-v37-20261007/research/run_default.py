"""Research-only actual default photo boundary qualification, one approved runtime.

This does not publish a generation. The production default validator owns its
real CLI and all receipt/composed/render audits. Existing stores stay unchanged.
"""
from __future__ import annotations
import collections, datetime, hashlib, importlib.util, json, os, shutil, stat
import subprocess, sys, tempfile, time, traceback, unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = HERE.parent
ROOT = R / 'v37-integration'
VERSION = sys.argv[1]
assert VERSION in ('312', '314')
EXPECTED = {
 '312': ('/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12', 'fa67443527ed9647f760d807e2a38f26340757123e643c4639cf273ed15d5ea7', [3,12,14], '15.0.0'),
 '314': (str(R/'python314-preparation/runtime/python/bin/python3.14'), '3c5fd2caadada58c68c7ad95ca9003b32602aa81e5ea606caeb3e5da55bf7169', [3,14,3], '16.0.0'),
}[VERSION]
PRIVATE = HERE / ('private' + VERSION)
assert not PRIVATE.exists()
PRIVATE.mkdir()
TMP = PRIVATE/'temporary'; TMP.mkdir()
tempfile.tempdir = str(TMP)
STORE = R/('runtime'+VERSION+'-preparation/private/runtime-store')
ENV = {'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','LC_ALL':'C.UTF-8','TZ':'UTC','PHOTO_RUNTIME_STORE':str(STORE)}
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert dict(os.environ) == ENV
assert sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
assert str(Path(sys.executable).resolve()) == str(Path(EXPECTED[0]).resolve()) and sha(sys.executable) == EXPECTED[1]
assert sys.implementation.name == 'cpython' and list(sys.version_info[:3]) == EXPECTED[2] and unicodedata.unidata_version == EXPECTED[3]
if VERSION == '314': assert sys._is_gil_enabled()
RELEASE = json.loads((HERE/'REVIEW-RELEASE.json').read_bytes())
assert RELEASE['released'] is True and sha(__file__) == RELEASE['script_sha256']
for name, expected in RELEASE['code_files'].items(): assert sha(ROOT/name) == expected, ('code seal drift', name)

def write(name, value):
 p = PRIVATE/name
 with p.open('x') as f: json.dump(value,f,ensure_ascii=False,sort_keys=True,indent=2); f.write('\n'); f.flush(); os.fsync(f.fileno())
def inventory(base):
 return {str(p.relative_to(base)):{'sha256':sha(p),'bytes':p.stat().st_size,'mode':stat.S_IMODE(p.stat().st_mode)} for p in sorted(base.rglob('*')) if p.is_file()}
def event(row):
 row['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (PRIVATE/'EXECUTION-LEDGER.jsonl').open('a') as f: f.write(json.dumps(row,sort_keys=True)+'\n'); f.flush(); os.fsync(f.fileno())
BEFORE=inventory(STORE)
write('SOURCE-STORE-BEFORE.json', BEFORE)
CALLS=collections.Counter(); DENIALS=[]; AUDITS={}; CHILDREN=[]
original_run = subprocess.run

def invoke(argv, *args, **kwargs):
 kind = 'git' if argv[0]=='git' else 'actual_cli'
 if kind == 'git':
  assert argv[:4]==['git','--no-lazy-fetch','-c','protocol.allow=never'] and argv[4]=='cat-file'
 else:
  assert argv[0]==sys.executable and argv[1:5]==['-I','-S','-B','-c']
  assert argv[6]==str(ROOT) and argv[7]==str(ROOT/'skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py')
  assert Path(argv[8]).is_relative_to(TMP) and Path(argv[9]).is_relative_to(TMP)
 number=len(CHILDREN); label=kind+'-'+str(number); start=time.monotonic_ns()
 event({'event':'start','kind':kind,'label':label,'argv':argv,'cwd':str(kwargs.get('cwd','')),'environment':kwargs.get('env'), 'executable_sha256':sha('/usr/bin/git' if kind=='git' else sys.executable)})
 result=original_run(argv,*args,**kwargs)
 event({'event':'end','kind':kind,'label':label,'exit_code':result.returncode,'elapsed_ns':time.monotonic_ns()-start})
 CHILDREN.append({'kind':kind,'exit_code':result.returncode})
 if kind=='actual_cli':
  assert result.returncode==0, result.stdout+result.stderr
  (PRIVATE/'actual-cli.stdout.txt').write_text(result.stdout)
  (PRIVATE/'actual-cli.stderr.txt').write_text(result.stderr)
  shutil.copyfile(argv[8], PRIVATE/'candidate-pack.json')
  shutil.copyfile(str(argv[8])+'.runtime-receipt.json', PRIVATE/'runtime-receipt.json')
 return result
subprocess.run=invoke

def deny(reason): DENIALS.append(reason); raise RuntimeError('V37 research guard denied: '+reason)
def resolve(value): return Path(os.fsdecode(value)).resolve()
def writable(value):
 p=resolve(value)
 if not p.is_relative_to(PRIVATE): deny('write outside private qualification: '+str(p))
def audit(event,args):
 if event.startswith('socket.') or event in {'os.system','os.posix_spawn','os.fork','os.exec','pty.spawn'}: deny(event)
 if event=='subprocess.Popen':
  argv=args[1]
  if not (argv[0]=='git' and argv[:5]==['git','--no-lazy-fetch','-c','protocol.allow=never','cat-file'] or argv[0]==sys.executable and argv[1:5]==['-I','-S','-B','-c'] and argv[6]==str(ROOT)): deny('unapproved subprocess')
 if event=='import' and args[0].split('.')[0] in {'google','openai','requests','httpx','aiohttp','keyring','dotenv'}: deny('provider/credential import')
 if event=='open' and isinstance(args[0],(str,bytes)):
  p=resolve(args[0]); flags=args[2] if isinstance(args[2],int) else 0
  if p.name in {'.env','.netrc','.npmrc','credentials'} or '.ssh' in p.parts or '.aws' in p.parts: deny('credential read')
  if flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND): writable(args[0])
 if event in {'os.mkdir','os.remove','os.rmdir','os.chmod','os.utime','os.truncate'} and isinstance(args[0],(str,bytes)):
  if event=='os.mkdir' and resolve(args[0]).is_dir(): return
  value=args[0]
  if not Path(os.fsdecode(value)).is_absolute() and len(args)>1 and isinstance(args[-1],int) and args[-1]>=0: value=Path(os.readlink('/proc/self/fd/'+str(args[-1])))/os.fsdecode(value)
  writable(value)
 if event=='os.rename': writable(args[0]); writable(args[1])
 if event=='os.link':
  assert resolve(args[0]).is_relative_to(STORE); writable(args[1])
 if event=='os.symlink': deny('symlink creation')

def profile(frame,event,arg):
 module=frame.f_globals.get('__name__',''); name=frame.f_code.co_name
 if event=='call':
  if module in {'build_semantic_index','build_visual_profile_index','generate_images_via_api','photo_api_render','sync_photo_runtime_source'} and name not in {'<module>','<dictcomp>','<listcomp>','<lambda>'}: deny('provider function')
  if name in {'get_gemini_api_key','cached_gemini_client','embed_texts_with_gemini','embed_single_semantic_text','load_api_key','call_api'}: deny('credential/provider function')
  if module=='photo_runtime_sources' and name in {'publish','fetch','source_update','complete_source_update'}: deny('publisher/fetch fallback')
  if module=='core_slot_index_storage' and name=='create': deny('cache creation')
  if module in {'photo_runtime_sources','prompt_generator','audit_composed_prompt','audit_image_render_request'} and name in {'capture_sources','load_generation','from_receipt','verify_pack_bindings','acquire','receipt','generate_candidate_pack','prepare_candidate_source','retrieve_core_slots','build_core_slot_index','audit_composed_prompt','audit_image_render_request','audit_authorial_core','audit_core_retrieval'}: CALLS[module+'.'+name]+=1
 if event=='return' and module in {'audit_composed_prompt','audit_image_render_request'} and name in {'audit_composed_prompt','audit_image_render_request','audit_authorial_core','audit_core_retrieval'}:
  AUDITS.setdefault(module+'.'+name,[]).append(arg)
sys.addaudithook(audit); sys.setprofile(profile)
validator_path=ROOT/'skills/subculture-illustration-image-generator/scripts/validate_illustration_assets.py'
sys.path[:0]=[str(ROOT),str(ROOT/'tests'),str(validator_path.parent)]
code=0
try:
 spec=importlib.util.spec_from_file_location('_actual_v37_public_validator',validator_path)
 validator=importlib.util.module_from_spec(spec);spec.loader.exec_module(validator)
 result=validator.validate_photo_regression_baseline(ROOT/'skills/subculture-illustration-image-generator/assets')
 receipt=result.pop('private_runtime_receipt')
 assert receipt==json.loads((PRIVATE/'runtime-receipt.json').read_bytes())
 pack_raw=(PRIVATE/'candidate-pack.json').read_bytes()
 assert pack_raw==(R/('runtime'+VERSION+'-preparation/private/candidate-pack.json')).read_bytes()
 assert pack_raw==(ROOT/'skills/subculture-illustration-image-generator/assets/photo_regression_baseline_v36_pack.json').read_bytes()
 assert result['status']=='pass' and result['schema']=='photo_regression_baseline/v37'
 assert len([c for c in CHILDREN if c['kind']=='actual_cli'])==1 and all(c['exit_code']==0 for c in CHILDREN)
 assert not DENIALS
 assert inventory(STORE)==BEFORE, 'original runtime store changed'
 for name, expected in RELEASE['code_files'].items(): assert sha(ROOT/name)==expected, ('code changed during execution',name)
 write('RESULT.json',{'status':'pass','public_default_result':result,'environment':{'implementation':'cpython','python':EXPECTED[2],'unicode':EXPECTED[3]},'same_runtime_doc_only_full_bytes_equal':True,'oracle_full_bytes_equal':True,'full_pack_sha256':hashlib.sha256(pack_raw).hexdigest(),'source_store_unchanged':inventory(STORE)==BEFORE,'actual_cli_count':1,'audits':AUDITS,'production_calls':dict(CALLS),'denials':DENIALS,'data_improvement_count_delta':0})
 print(json.dumps({'status':'pass','version':VERSION,'result_sha256':sha(PRIVATE/'RESULT.json'),'pack_sha256':sha(PRIVATE/'candidate-pack.json')}))
except BaseException:
 traceback.print_exc(); code=1
finally:
 sys.setprofile(None)
 write('EXECUTION-END.json',{'exit_code':code,'denials':DENIALS,'children':CHILDREN,'source_store_unchanged':inventory(STORE)==BEFORE})
raise SystemExit(code)
