"""Finish staging after an already-committed evidence file made set equality fail.

The acceptance and semantic verification are unchanged. Preserve the failed
helper and its report, and compare cached paths to actual differences from HEAD.
"""
import ast, hashlib, json, subprocess
from pathlib import Path
ROOT=Path.cwd(); R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
def read(p): return json.loads(p.read_bytes())
def raw(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
 with p.open('x') as f: json.dump(v,f,ensure_ascii=False,sort_keys=True,indent=2); f.write('\n')
report_path=R/'ROOT-FIRST20-149-INTEGRATION-02.json'; report=read(report_path)
names=set(report['files'])|{str(report_path.relative_to(ROOT))}
for name,pin in report['files'].items():
 p=ROOT/name; assert raw(p)==pin
 if p.suffix=='.json': read(p)
 if p.suffix=='.py': ast.parse(p.read_bytes())
for name,pin in report['protected_files'].items(): assert raw(ROOT/name)==pin
actual=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())
assert actual<names
unchanged=names-actual
assert unchanged=={str((R/'authored/native_06250_first20_149_03.guard-source-proposals.json').relative_to(ROOT))}
for name in unchanged: assert subprocess.check_output(['git','show','HEAD:'+name])==(ROOT/name).read_bytes()
failure=R/'ROOT-FIRST20-149-STAGING-FAILED-ATTEMPT-01.json'
save(failure,dict(schema='photo-root-staging-failure/v1',action='accept_first20_149_04_root_01.py final cached-set assertion',reason='The explicit allowlist also includes one byte-identical already committed source-proposal artifact. git add correctly omits it from the actual diff. Semantic verification and acceptance succeeded; no unexpected cached path exists.',expected_allowlist=len(names),actual_cached=len(actual),already_committed_unchanged=sorted(unchanged),unexpected_cached=[],meaning_or_proof_changes=0))
staging=R/'ROOT-FIRST20-149-STAGING-R02.json'
save(staging,dict(schema='photo-root-staging-correction/v1',report=str(report_path.relative_to(ROOT)),report_raw_sha256=raw(report_path),all_report_raw_hashes_verified=True,json_and_python_ast_valid=True,protected_files_verified=True,already_committed_unchanged=sorted(unchanged),cached_expected_method='Exact allowed paths whose working bytes differ from HEAD; new files count as differences. No repository-wide staging.',semantic_acceptance_changed=False,Gemini_calls=0))
names|={str(p.relative_to(ROOT)) for p in (failure,staging,Path(__file__).resolve())}
subprocess.run(['git','add','--',*sorted(names)],check=True)
expected=set()
for name in names:
 result=subprocess.run(['git','show','HEAD:'+name],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
 if result.returncode or result.stdout!=(ROOT/name).read_bytes(): expected.add(name)
assert set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())==expected
subprocess.run(['git','diff','--cached','--check'],check=True)
for name in names: assert subprocess.check_output(['git','show',':'+name])==(ROOT/name).read_bytes()
print(json.dumps(dict(cached_files=len(expected),allowed_unchanged=len(unchanged),research_approved_in_batch=20,newly_accepted_in_batch=13,operating_changes=0)))
