"""Check tracked bytes and the scoped application, without changing files."""
import concurrent.futures,hashlib,json,subprocess
from pathlib import Path
P=Path('/Users/chasoik/Projects/image-prompt');OUT=P/'docs/research-evidence/photo-prompt/selfie-pose-integration-20261008'
baseline=json.loads((OUT/'primary-before.json').read_text())
application=json.loads((OUT/'primary-application-revision-3.json').read_text())
owned={r['path']:r['after_sha256']for r in application['copied']}
def sha(path):
    if not path.is_file():return None
    h=hashlib.sha256()
    with path.open('rb')as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()
def check(row):
    rel,before=row;after=sha(P/rel)
    return None if after==before else {'path':rel,'before_sha256':before,'after_sha256':after,'classification':'owned_application'if rel in owned else'concurrent_external_change'}
with concurrent.futures.ThreadPoolExecutor(max_workers=8)as pool:
    differences=[r for r in pool.map(check,baseline['tracked_file_hashes'].items())if r]
owned_checks=[{'path':r,'matches_application':sha(P/r)==h}for r,h in owned.items()]
assert all(r['matches_application']for r in owned_checks)
report={'scope':'All initially inventoried tracked paths plus 40 scoped application artifacts. Initial ignored and untracked files were not comprehensively fingerprinted. No reset, staging or deletion was performed.',
    'head_before':baseline['head'],'head_after':subprocess.check_output(['git','rev-parse','HEAD'],cwd=P).decode().strip(),
    'tracked_paths_checked':len(baseline['tracked_file_hashes']),'differences':differences,'owned_artifacts':owned_checks,
    'unrelated_differences':[r for r in differences if r['classification']=='concurrent_external_change']}
(OUT/'preservation-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'tracked_paths_checked':report['tracked_paths_checked'],'head_unchanged':report['head_before']==report['head_after'],'owned_artifacts_match':len(owned_checks),'unrelated_differences':report['unrelated_differences']},ensure_ascii=False))
