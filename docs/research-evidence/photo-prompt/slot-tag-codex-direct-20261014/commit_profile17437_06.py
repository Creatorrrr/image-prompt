"""Commit exact reviewed profile research history and focused149 acceptance only."""
import ast,hashlib,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[3];paths={Path(__file__).resolve(),R/'root_accept_profile17437_06.py'}
for pat in ['authored/native_fresh_08250_17437_05*','authored/native_fresh_08250_17437_06*','worker-notes/native-08250-special17437-05*','worker-notes/native-08250-special17437-06*','worker-notes/native-09250-special17437-05*']:paths.update(p for p in R.glob(pat)if p.is_file())
for name in ['review08250-17437-05','review08250-17437-06']:paths.update(p for p in (R/'native_batches'/name).iterdir()if p.is_file())
assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT)
for p in paths:
 assert p.is_file()and not p.is_symlink()
 if p.suffix=='.py':ast.parse(p.read_bytes())
 if p.suffix=='.json':json.loads(p.read_bytes())
for name in ['worker-notes/native-08250-special17437-06-handoff-20261015.json','worker-notes/native-09250-special17437-05-peer-20261015.review.json']:
 h=json.loads((R/name).read_bytes())
 for a in h['artifacts']:
  p=Path(a.get('file',a.get('path','')));p=p if p.is_absolute()else R/p
  assert p.is_file()and hashlib.sha256(p.read_bytes()).hexdigest()==a['raw_sha256'];paths.add(p)
  subprocess.run(['git','ls-files','--error-unmatch',str(p.relative_to(ROOT))],cwd=ROOT,capture_output=True)
v=json.loads((R/'native_batches/review08250-17437-06/ROOT-VERIFICATION-01.json').read_bytes());assert v['other_semantic_payload_exactly_preserved']and v['root_full_batch_and_acceptance_verified']and v['operating_native_qualified']==0
allow=R/'ROOT-PROFILE17437-06-COMMIT-ALLOWLIST.json';assert not allow.exists();allow.write_text(json.dumps({'schema':'photo-root-exact-commit-allowlist/v1','files':sorted(str(p.relative_to(ROOT))for p in paths)+[str(allow.relative_to(ROOT))],'file_byte_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(paths)},'scope':'Exact original05 worker/peer/failure history plus fresh06 direct repair proof and separate root scoped149 research acceptance. No operating native qualification or source/index/runtime mutation.','new_model_or_Gemini_calls':0},sort_keys=True,indent=2)+'\n');paths.add(allow);names=sorted(str(p.relative_to(ROOT))for p in paths);subprocess.run(['git','add','--',*names],cwd=ROOT,check=True);subprocess.run(['git','diff','--cached','--check'],cwd=ROOT,check=True)
for name in names:assert subprocess.check_output(['git','show',':'+name],cwd=ROOT)==(ROOT/name).read_bytes(),name
print('PASS exact stagedfiles',len(paths))
