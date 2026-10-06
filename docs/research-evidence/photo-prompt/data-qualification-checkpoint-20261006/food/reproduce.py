"""Offline verifier; optional 24-call pure replay. See provenance for verification status."""
import argparse, collections.abc, copy, hashlib, json, os, sys, sysconfig
from pathlib import Path

def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(v): return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
def require(ok, message):
    if not ok: raise RuntimeError(message)

a = argparse.ArgumentParser(description=__doc__)
a.add_argument('--repo', required=True, type=Path)
a.add_argument('--evidence', required=True, type=Path, help='this package directory')
a.add_argument('--replay', action='store_true', help='explicitly opt into 24 pure retrieval calls')
a.add_argument('--out', type=Path, help='new output directory, outside source and package')
args = a.parse_args()
repo, package = args.repo.resolve(), args.evidence.resolve()
pin, manifest = read(package/'source-pin.json'), read(package/'manifest.json')
# Read only Git identity files: no Git subprocess, config, hook, or credential access.
git = repo/'.git'
if git.is_file():
    pointer = git.read_text().strip()
    require(pointer.startswith('gitdir: '), 'Invalid Git worktree pointer')
    git = (repo/pointer[8:]).resolve()
require(git.is_dir() and not git.is_symlink(), 'Missing Git identity directory')
common = (git/(git/'commondir').read_text().strip()).resolve() if (git/'commondir').is_file() else git
head = (git/'HEAD').read_text().strip()
if head.startswith('ref: '):
    ref = head[5:]
    require(ref.startswith('refs/') and '..' not in ref.split('/'), 'Invalid HEAD ref')
    target = (common/ref).resolve()
    require(target.is_relative_to(common.resolve()), 'Ref escapes checkout')
    if target.is_file(): head = target.read_text().strip()
    else:
        packed = (common/'packed-refs').read_text().splitlines()
        matches = [s.split()[0] for s in packed if s and not s.startswith(('#','^')) and s.split()[1] == ref]
        require(len(matches) == 1, 'Cannot resolve pinned HEAD')
        head = matches[0]
require(head == pin['commit'], 'Wrong pinned source commit')
source = repo/pin['base']
source_files = {(source/rel).resolve(): h for rel,h in pin['files'].items()}
for p,h in source_files.items():
    require(p.is_relative_to(repo) and sha(p) == h, 'Source hash mismatch: '+str(p))
for name,row in manifest['files'].items():
    p = (package/name).resolve()
    require(p.is_relative_to(package) and p.stat().st_size == row['bytes'] and sha(p) == row['sha256'], 'Package mismatch: '+name)
for p in package.rglob('*.json'): read(p)
verdict, expected, provenance = (read(package/n) for n in ('verdict.json','expected-replay.json','provenance.json'))
cases = ['case_'+c for c in 'abcdef']
require([verdict['cases'][c]['core_total'] for c in cases] == [64,64,57,56,64,64], 'Incorrect totals')
for row in provenance['original_receipts']:
    c = row['case_id']; folder = package/'inputs'/c
    require(sha(folder/'raw-request.txt') == row['raw_request_sha256'], 'Raw-request byte mismatch')
    require(read(folder/'request_envelope.json')['request_text'].encode() == (folder/'raw-request.txt').read_bytes(), 'Envelope differs from raw request')
print('PASS: pinned source, package hashes, JSON syntax, raw bytes and compact totals; no retrieval')
if not args.replay: raise SystemExit(0)
require(args.out is not None, '--out is required with --replay')
out = args.out.resolve()
require(not out.exists() and not out.is_relative_to(repo) and not out.is_relative_to(package), 'Output must be new and outside source/package')
require(not repo.is_relative_to(out) and not package.is_relative_to(out), 'Output cannot contain source/package')
out.mkdir(parents=True)
stdlib = Path(sysconfig.get_path('stdlib')).resolve()
package_files = {(package/n).resolve() for n in manifest['files']}
phase = 'initialize'
class NoEnvironment(collections.abc.Mapping):
    def __getitem__(self,k): raise PermissionError('Environment access denied')
    def __iter__(self): raise PermissionError('Environment enumeration denied')
    def __len__(self): return 0
    def get(self,k,default=None): raise PermissionError('Environment access denied')
os.environ.clear(); os.environ = NoEnvironment(); sys.dont_write_bytecode = True

def audit(event, values):
    if event.startswith('socket.') or event in {'subprocess.Popen','os.system','os.posix_spawn','os.fork','os.exec','ctypes.dlopen','os.remove','os.rename','os.rmdir','os.symlink','os.link'}:
        raise PermissionError('Offline replay denies '+event)
    if event == 'import' and str(values[0]).split('.')[0] in {'openai','google','anthropic','requests','httpx','urllib','boto3','botocore','keyring'}:
        raise PermissionError('Provider/network import denied')
    if event != 'open': return
    name,mode,flags = values
    require(not isinstance(name,int), 'Raw file descriptors denied')
    p = Path(name).resolve()
    if flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):
        require(p.is_relative_to(out), 'Write outside evidence denied'); return
    require(phase != 'retrieve', 'Filesystem read during pure retrieval denied')
    if p.is_relative_to(repo) and p.suffix in {'.pyc', '.pyo'}:
        raise PermissionError('Unsealed repository bytecode read denied')
    require(p in source_files or p in package_files or (p.is_relative_to(stdlib) and p.suffix in {'.py','.pyc','.so'}), 'Unapproved read: '+str(p))
sys.addaudithook(audit)
sys.path.insert(0,str(source/'scripts'))
import prompt_generator as pg
import photo_camera_evidence as camera
import photo_embodiment as embodiment

data = pg.load_json(source/'assets/photo_prompt_tags.json')
data[pg.QUALITY_LAYERS_DATA_KEY] = pg.load_quality_layers(source/'assets'/pg.QUALITY_LAYERS_FILENAME)
require(digest(data) == expected['source_data_sha256'], 'Loaded baseline data differs')
prototype = read(package/'prototype-extension.json')
pg.photo_candidate_semantics.validate_extension_keys(prototype)
pg.photo_candidate_semantics.validate_candidate_entries(prototype,pg.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)
inputs = {}
for row in provenance['original_receipts']:
    c = row['case_id']; folder = package/'inputs'/c
    envelope = pg.normalize_request_envelope(read(folder/'request_envelope.json'))
    controls = read(folder/'creative_controls.json')
    pg.creative_controls.validate(controls,envelope['request_text'])
    core = pg.normalize_authorial_core(read(folder/'authorial_core.json'),request_envelope=envelope,creative_control_snapshot=controls)
    camera.camera_authoring_declaration(core,required=True)
    policy = embodiment.build_policy(core,read(folder/'embodiment_review.json'))
    actual = {'request_envelope_sha256':envelope['canonical_sha256'],'creative_controls_sha256':controls['canonical_sha256'],'authorial_core_sha256':core['canonical_sha256'],'intent_lock_sha256':core['intent_lock']['canonical_sha256'],'embodiment_policy_sha256':policy['canonical_sha256']}
    require(all(v == (row.get(k) or row['attempt_02'][k]) for k,v in actual.items()), 'Original final input binding mismatch')
    inputs[c] = core,controls
results = {}
for arm,selected in [('before',[]),('combined',prototype['slots']['texture']),('bread_only',[prototype['slots']['texture'][0]]),('pastry_only',[prototype['slots']['texture'][1]])]:
    current = copy.deepcopy(data)
    if selected:
        extension = copy.deepcopy(prototype); extension['slots']['texture'] = copy.deepcopy(selected)
        current = pg.merge_research_extension(current,extension)
        pg.photo_candidate_semantics.validate_candidate_entries(current,pg.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)
    results[arm] = {}
    for c,(core,controls) in inputs.items():
        phase = 'retrieve'
        try: slots,binding,contract = pg.retrieve_core_slots(current,core,controls)
        finally: phase = 'project'
        mini = {'slots':copy.deepcopy(slots),'provenance':{'seed':0,'batch_index':0}}
        meanings = {}
        for slot,payload in mini['slots'].items():
            for candidate in payload['candidates']:
                entry = pg.candidate_pack_slot_entry_by_id(current,slot,candidate['entry_id'])
                meaning = pg.photo_candidate_semantics.semantic_source(entry,slot,current['candidate_semantic_policy'])
                meanings[candidate['id']] = meaning
                if not pg.property_effects_allowed(core['intent_lock'],meaning['affected_dimensions'],meaning.get('affected_properties',[])):
                    candidate['applicability'] = {'status':'ineligible','source':'authored_property_scope','reason':'effect overlaps a protected requester property'}
        pg.candidate_pack_prepare_authorial_surfaces(mini)
        pg.photo_candidate_semantics.apply_public_semantics(mini,meanings)
        actual = {'public_slots_sha256':digest(mini['slots']),'binding_sha256':digest(binding)}
        require(actual == expected['cases'][c][arm], 'Replay differs: '+arm+'/'+c)
        results[arm][c] = actual
(out/'replay-result.json').write_text(json.dumps({'pure_calls':24,'exact_hashes':results},indent=2)+'\n')
print('PASS: 24 pure core-slot calls match archived public-slot/binding hashes; no full CLI or non-core replay')
