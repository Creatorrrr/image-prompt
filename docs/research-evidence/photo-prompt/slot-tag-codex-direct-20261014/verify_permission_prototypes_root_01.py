"""Preserve independently reviewed prototype correction and its explicit limits."""
import ast,hashlib,json,subprocess
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
one=R/'permission-envelope-prototype-01';two=R/'permission-envelope-prototype-02';peer=R/'permission-envelope-review11870-01'
assert sha(two/'envelope.py')=='94e88fd3ac20a350560b040eb7e6f126be40ff040d9a333eda8b1b75f0979091'
assert sha(two/'REPORT-V2.json')=='4e629f9fb5162451991f3e1bd248489f19651bda71f35feb34fc7944ad83564f'
assert sha(peer/'REPORT-v1.json')=='8fdcc898356656c37636f821ca3823cfc0861bc6b55d017a1e100572d204bd69'
assert (one/'fixtures.py').read_bytes()==(two/'fixtures.py').read_bytes() and (one/'test_envelope.py').read_bytes()==(two/'test_envelope.py').read_bytes()
first=read(one/'ROOT-RERUN-01.json');second=read(two/'ROOT-RERUN-V2-01.json')
assert (first['tests'],first['explicit_scenarios'])==(55,141) and (second['tests'],second['explicit_scenarios'])==(64,222)
for result in (first,second):
 assert result['failures']==result['errors']==result['skipped']==result['native_approvals']==result['operating_changes']==result['Gemini_calls']==0
 assert result['network_denied'] and result['model_API_imports_forbidden'] and not result['consumer_integrated']
assert all(x['expected']==x['actual'] for x in second['new_cases'])
assert len(second['new_cases'])==81 and len(second['old_cases'])==141
for group in (one,two):
 for p in group.iterdir():
  if p.name.startswith('ROOT-RERUN'):
   report=read(p)
   for name,h in report.get('pinned_files',{}).items():
    # Copied v1 reports are explicitly historical and bind prototype01 bytes.
    owner=one if p.name=='ROOT-RERUN-01.json' else two
    assert sha(owner/name)==h,(owner,name)
protected={'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md':'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359','docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md':'0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b'}
for name,h in protected.items():assert sha(ROOT/name)==h
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
paths=[Path(__file__),ROOT/'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md']
for group in (one,two,peer):paths += [p for p in sorted(group.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
pins={}
for p in paths:
 if p.suffix=='.json':read(p)
 elif p.suffix=='.py':ast.parse(p.read_bytes())
 pins[str(p.relative_to(ROOT))]=sha(p)
out=R/'ROOT-PERMISSION-PROTOTYPE-INTEGRATION-02.json'
value=dict(schema='photo-root-research-permission-prototype-integration/v1',actor='/root',status='research_primitive_correction_verified_not_native_or_operating',
 original_tests=55,original_scenarios=141,corrected_tests=64,corrected_scenarios=222,
 independent_finding='Eight actual B1 joint parent/child path false accepts despite unchanged source E/Rx. V2 compares both actual target/Rx unions using the same frozen property primitive.',
 new_scenario_boundary=dict(actual_B1_permission=31,direct_permission_primitive=47,actual_B1_wildcard_rejections=3),
 root_review='Whole prototype01 implementation/spec/fixtures/tests, exact V2 implementation diff, whole new9 tests/spec, independent review and correction reports directly read. Root reran both authored suites, not newly independent222 expectations.',
 historical_failures_preserved=True,original_source_and_prototypes_immutable=True,
 unresolved=['The native visibility tuple has no image component. A wrong trusted two-image annotation remains a documented pending PR limitation outside222 passing scenarios.',
 'Source1299/native qualification, B2 P/PR/guard matching, compact/full consumer and final-state preservation, runtime publication and operating activation remain unimplemented.'],
 native_approvals=0,operating_changes=0,Gemini_calls=0,files=pins,protected_files=protected)
with out.open('xb') as f:f.write(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()+b'\n')
names=sorted(set(pins)|{str(out.relative_to(ROOT))});subprocess.run(['git','add','--',*names],check=True);subprocess.run(['git','diff','--cached','--check'],check=True)
assert set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())==set(names)
for name in names:assert subprocess.check_output(['git','show',':'+name])==(ROOT/name).read_bytes()
print(json.dumps(dict(files=len(names),tests=64,scenarios=222,native_approvals=0,operating_changes=0,Gemini_calls=0)))
