"""Seal the human-readable report and a scoped, reproducible evidence inventory."""
from pathlib import Path
import json, hashlib, shutil, datetime

O = Path(__file__).resolve().parent
ROOT = Path('/Users/chasoik/Projects/image-prompt')
def read(p): return json.loads(Path(p).read_bytes())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')

final = read(O/'final-union-verification.json')
images = read(O/'image-evidence-verification.json')
assert final['status'] == images['status'] == 'pass'
assert read(O/'provider-original-equality.json')['status'] == 'pass'
active = final['active_config']; q = final['retrieval_qualification']
assert read(ROOT/'skills/photo-prompt-image-generator/retrieval-runtime.json') == active
master = read(O/'TEST-RESULTS.json')
master.update(state='completed',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    final_union=final,image_tests=images,provider_original_equality='provider-original-equality.json',
    verdict='New bounded source structures 2/3 PASS; complete authored scenes 0/3; automatic discovery of the new module 0/3.',
    acceptance='pending',paired_causal_improvement=False)
write(O/'TEST-RESULTS.json',master)

p = O/'REPORT.md'; s = p.read_text()
s = s.replace('현재 최신 부모를 기준으로 만든 `union-current/`의 데이터 전용 successor를 최종 검증하고 있다. 최종 기본 포인터와 보존 검증은 아래 실행 기록에 추가한다.',
    '최신 부모를 기준으로 만든 `union-current/`의 데이터 전용 successor 검증과 기본 버전 선택을 완료했다. 앞선 버전으로 되돌리지 않았다. 최종 기본 포인터와 보존 검증은 아래에 기록한다.')
marker = '<!-- final-union-result -->'
assert marker not in s, 'Report already finalized; inspect before rerunning.'
section = f'''{marker}
### 최종 기본 버전 반영

- H2: `{active['generation_id']}`
- Native: `{active['native_generation_id']}`
- 보존한 직전 기본 H2: `{final['parent_config']['generation_id']}`
- 기존 canonical 후보 {final['existing_canonical_records_preserved']:,}개와 모든 기존 source module·binding·catalog·policy를 보존했다. 커널 코드와 CPython 3.14.3/Unicode16 환경도 동일하다.
- 이미지 시험 버전과 최종 기본 버전의 신규 후보 module 및 binding module은 **byte-identical**이다. 원본 snapshot 24개, binding 35개가 모두 동일하다. 이미지 생성은 앞서 명시한 시험 pin에서 했다. 최종 글로벌 검색·표본이 그때와 동일하다고 주장하지 않는다.
- 최종 기본 검색은 positive {q['after_positive_CIDs']:,} CID다. source-derived 개발 질의 {q['target_at10']}/36 top10, 24개 control의 이전 top10 평균 중복 {q['control_mean_top10_overlap']:.3f}/10이다. 모든 배포 검증을 통과했고 CURRENT 쓰기는 0이다. 기본 선택용 설정 파일만 의도대로 바꿨다.
- 보호한 기존 파일 {final['protected_source_files_unchanged']}개가 그대로이며 HEAD `{final['HEAD']}`도 동일하다. 다른 dirty 파일을 되돌리거나 stage하지 않았다. 커밋·푸시·PR은 수행하지 않았다.

근거: [최종 통합본 대조](final-union-verification.json), [최종 60개 검색 검증](union-current/retrieval-qualification.json), [기본 선택 결과](union-current/install-active.json), [통합 결과](TEST-RESULTS.json).

'''
s = s.replace('## 세 독립 실행의 범위',section+'## 세 독립 실행의 범위')
s = s.replace('[부모 픽셀 판독](parent-pixel-reviews/)', '[제공 원본과 저장 이미지 동일성](provider-original-equality.json), [부모 픽셀 판독](parent-pixel-reviews/)')
p.write_text(s)

# Keep point-in-time source/config copies independent of future concurrent work.
snapshot = O/'source-snapshots'; snapshot.mkdir(exist_ok=True)
owned = ['assets/photo_candidate_court_palace_full_review_20261023.json',
    'assets/photo_candidate_court_palace_full_review_bindings_20261023.json',
    'assets/photo_court_palace_full_review_semantics_20261023.json',
    'assets/photo_court_palace_semantics_20261023.json',
    'assets/photo_candidate_corpus_manifest.json','retrieval-runtime.json',
    'references/court-palace-semantics.md']
source_rows = []
for rel in owned:
    origin = ROOT/'skills/photo-prompt-image-generator'/rel
    dest = snapshot/Path(rel).name
    shutil.copyfile(origin,dest)
    source_rows.append(dict(source=str(origin),snapshot=str(dest),sha256=sha(dest)))
write(O/'source-snapshot-inventory.json',dict(status='pass',files=source_rows,
    note='Point-in-time copies of this topic data, raw corpus registration and selected runtime. The global manifest contains preserved concurrent source modules.'))

# Exclude bulky rebuild/cache trees and transient locks. Include each run's exact
# managed bindings, reports, ledger and original saved image without changing it.
files = set()
for p in O.iterdir():
    if p.is_file() and p.name not in {'SCOPED-SHA256SUMS','evidence-inventory.json'} and not p.name.endswith('.LOCK'):
        files.add(p)
for d in ['parent-pixel-reviews','prompts','source-snapshots']:
    files.update(p for p in (O/d).rglob('*') if p.is_file() and not p.name.endswith('.LOCK'))
for d in ['union-final','union-latest','union-current']:
    files.update(p for p in (O/d).iterdir() if p.is_file() and not p.name.endswith('.LOCK'))
for arm in images['arms']:
    run=Path(arm['run']); w=read(run/'workflow.json')
    files.update(Path(x['path']) for x in w['artifacts'].values())
    files.update(p for p in run.iterdir() if p.is_file() and not p.name.endswith('.LOCK') and p.name!='.LOCK')
    files.add(Path(arm['image']))
files = sorted(files,key=str)
rows = [dict(path=str(p.resolve()),bytes=p.stat().st_size,sha256=sha(p)) for p in files]
write(O/'evidence-inventory.json',dict(schema='court-r2-scoped-evidence-inventory/v1',files=rows,
    excluded=['bulky build/cache/successor-store/successor-skill trees','transient *.LOCK files'],
    note='All listed paths are absolute. Hashes bind the saved report, final selected release evidence, source copies and three actual image attempts. Future concurrent global changes are not captured as immutable claims.'))
allrows = rows+[dict(path=str((O/'evidence-inventory.json').resolve()),sha256=sha(O/'evidence-inventory.json'))]
(O/'SCOPED-SHA256SUMS').write_text(''.join(f"{r['sha256']}  {r['path']}\n" for r in allrows))
print(json.dumps(dict(status='pass',evidence_files=len(allrows),report_sha256=sha(O/'REPORT.md'),
    active_h2=active['generation_id'],master_result=str(O/'TEST-RESULTS.json')),ensure_ascii=False))
