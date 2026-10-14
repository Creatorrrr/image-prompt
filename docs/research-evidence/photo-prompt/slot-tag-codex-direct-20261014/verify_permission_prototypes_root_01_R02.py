"""Complete staging without altering a valid immutable unified-diff artifact."""
import ast,difflib,hashlib,json,subprocess
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
 with p.open('xb') as f:f.write(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()+b'\n')
previous=R/'ROOT-PERMISSION-PROTOTYPE-INTEGRATION-02.json';report=json.loads(previous.read_bytes())
for name,h in report['files'].items():assert sha(ROOT/name)==h
for name,h in report['protected_files'].items():assert sha(ROOT/name)==h
expected=set(report['files'])|{str(previous.relative_to(ROOT))}
assert set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())==expected
patch=R/'permission-envelope-prototype-02/IMPLEMENTATION-DIFF-V2.patch'
actual=''.join(difflib.unified_diff((R/'permission-envelope-prototype-01/envelope.py').read_text().splitlines(keepends=True),(R/'permission-envelope-prototype-02/envelope.py').read_text().splitlines(keepends=True),fromfile='prototype01/envelope.py',tofile='prototype02/envelope.py'))
assert patch.read_text()==actual
lines=[i+1 for i,line in enumerate(actual.splitlines()) if line.rstrip()!=line]
assert lines==[26,27] and all(actual.splitlines()[i-1]==' ' for i in lines)
failure=R/'ROOT-PERMISSION-PROTOTYPE-STAGING-FAILED-ATTEMPT-01.json'
save(failure,dict(schema='photo-root-staging-failure/v1',actor='/root',helper='verify_permission_prototypes_root_01.py',helper_sha256=sha(R/'verify_permission_prototypes_root_01.py'),command=['git','diff','--cached','--check'],exit_code=2,
 reported_path=str(patch.relative_to(ROOT)),reported_lines=lines,reason='Unified diff context records for unchanged blank source lines consist of a required single leading space. Git treats these serialized context markers as trailing whitespace when adding the patch artifact.',
 implementation_or_test_failure=False,original_artifact_changed=False,root_rerun_tests=64,root_rerun_scenarios=222))
ast.parse(Path(__file__).read_bytes())
out=R/'ROOT-PERMISSION-PROTOTYPE-STAGING-R02.json'
save(out,dict(schema='photo-root-staging-verification/v1',actor='/root',semantic_and_test_report=str(previous.relative_to(ROOT)),semantic_and_test_report_sha256=sha(previous),failure=str(failure.relative_to(ROOT)),failure_sha256=sha(failure),
 helper=str(Path(__file__).relative_to(ROOT)),helper_sha256=sha(Path(__file__)),
 exact_whitespace_exception=str(patch.relative_to(ROOT)),valid_unified_diff_bytes_recomputed_from_complete_before_after=True,only_allowed_context_space_lines=lines,
 exception_scope='Only this exact immutable serialized patch is excluded from Git whitespace scanning; every other staged file uses the unchanged normal check. Its exact complete diff bytes and staged bytes are independently verified.',
 native_approvals=0,operating_changes=0,Gemini_calls=0))
added=[str(p.relative_to(ROOT)) for p in [Path(__file__),failure,out]];subprocess.run(['git','add','--',*added],check=True)
subprocess.run(['git','diff','--cached','--check','--','.',':(exclude)'+str(patch.relative_to(ROOT))],check=True)
names=expected|set(added);assert set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())==names
for name in names:assert subprocess.check_output(['git','show',':'+name])==(ROOT/name).read_bytes()
print(json.dumps(dict(files=len(names),normal_whitespace_checks_pass=True,exact_valid_serialized_patch_exception=1,tests=64,scenarios=222,native_approvals=0,operating_changes=0)))
