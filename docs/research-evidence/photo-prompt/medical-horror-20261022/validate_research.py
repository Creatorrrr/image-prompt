"""Research integrity and protected-state observation. Never mutates runtime."""
import csv,datetime,hashlib,json,re,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
def read(name):return json.loads((P/name).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
cards=read('semantic-cards.json');drafts=read('candidate-drafts.json');routes=read('keyword-routes.json')
sources=read('sources.json');cases=read('evaluation-cases.json');summary=read('SUMMARY.json')
ids={x['id'] for x in cards};sids={x['id'] for x in sources}
assert len(cards)==len(ids)==86
assert len(drafts)==64 and len(sources)==51 and len(cases)==64 and len(routes)==181
assert len({x['en'] for x in routes})==181
for c in cards:
    assert set(c['source_refs'])<=sids
    assert c['runtime_registration'] is False and c['native_approval'] is False
    assert c['unobservable_policy']=='UNOBSERVABLE_NOT_PASS' and c['whole_case_policy']=='partial_is_fail'
    if c['id'].startswith('X'):
        assert not c['observable_components'] and not c['relations'] and not c['render_gates']
    else:
        assert c['phrase_en'].strip() and c['phrase_ko'].strip() and c['relations'] and c['render_gates']
        assert all(set(r)=={'subject','predicate','object'} and all(r.values()) for r in c['relations'])
        assert c['confusion_boundaries'] and c['claim_limit_ko']
for r in routes:
    assert r['visual_card_ids'] or r['boundary_card_ids']
    assert set(r['visual_card_ids']+r['boundary_card_ids'])<=ids
    for i in r['visual_card_ids']+r['boundary_card_ids']:
        assert r['en'] in next(c['seed_terms'] for c in cards if c['id']==i)
for d in drafts:
    c=next(c for c in cards if c['id']==d['card_id'])
    assert d['phrase_en']==c['phrase_en'] and d['phrase_ko']==c['phrase_ko']
    assert d['runtime_eligible'] is False and d['native_approval'] is False
    assert not d['id'].startswith('cand_')
for c in cases:
    assert c['status']=='NOT_RUN' and c['query_en'] and c['query_ko']
    assert c['reference_card_ids']=='NONE' or set(c['reference_card_ids'].split(','))<=ids
with (P/'EVALUATION-CASES.tsv').open() as f:assert list(csv.DictReader(f,delimiter='\t'))==cases
broken=[]
future={'VALIDATION.json','VALIDATION.md','SHA256SUMS'}
for f in P.glob('*.md'):
    for dest in re.findall(r'\]\(([^)]+)\)',f.read_text()):
        if '://' in dest or dest.startswith('#'):continue
        name=dest.split('#')[0]
        if name not in future and not (f.parent/name).exists():broken.append([f.name,dest])
assert not broken,broken
baseline=read('BASELINE.json')
changes=[]
for name,h in baseline['protected_files'].items():
    f=ROOT/name
    if not f.exists():changes.append(dict(path=name,status='missing_since_baseline'))
    elif sha(f)!=h:changes.append(dict(path=name,status='changed_since_baseline'))
audit=read('CORPUS-LEXICAL-AUDIT.json')
module_drift=[name for name,h in audit['module_hashes'].items()
              if not (ROOT/'skills/photo-prompt-image-generator/assets'/name).exists()
              or sha(ROOT/'skills/photo-prompt-image-generator/assets'/name)!=h]
manifest=ROOT/'skills/photo-prompt-image-generator/assets/photo_candidate_corpus_manifest.json'
manifest_drift=sha(manifest)!=audit['manifest_sha256']
for row in read('existing-source-mapping.json'):
    assert hashlib.sha256(json.dumps(row['record'],ensure_ascii=False,sort_keys=True).encode()).hexdigest()==row['record_sha256']
    assert row['record']['id']==row['cid']
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
result=dict(checked_at_kst=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(),
 status='STRUCTURE_PASS_REBASELINE_REQUIRED' if changes or module_drift or manifest_drift or head!=baseline['head'] else 'STRUCTURE_PASS',
 structure_pass=True,counts=summary,checks=['181 unique routes and live card links','86 cards with source/limit/gate boundaries',
 '64 exact bilingual draft counterparts; all inert','64 NOT_RUN cases and TSV/JSON equality','local Markdown links',
 'full-source snapshot hashes','protected baseline and audit generation observations'],
 source_changes_since_baseline=changes,audit_module_drift=module_drift,audit_manifest_drift=manifest_drift,
 head_at_baseline=baseline['head'],head_now=head,
 scope='This task authored only this research folder. Concurrent external changes are observed, not reverted or claimed as ours.',
 not_verified=['complete clinical definitions for every term','historical/film pixels','runtime schema qualification',
 'native semantic approval','hybrid retrieval and source exposure','prompt transport','generated pixels','artistic improvement',
 'user acceptance','runtime registration/index/installation/activation','commit/push'])
(P/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(P/'VALIDATION.md').write_text('# 연구 산출물 검증\n\n'+result['status']+'\n\n'+
 '181개 용어 연결, 카드·초안·출처·평가 사례 참조와 파일 무결성 검사를 통과했다. 이는 의학적 정확성 전체·native 의미 승인·검색·이미지 성공의 검증이 아니다.\n\n'+
 f'BASELINE 이후 보호 파일 변화 {len(changes)}개, audit 모듈 변화 {len(module_drift)}개, manifest 변화 {manifest_drift}. 동시 작업을 보존했으며 실제 반영 전에 최신 소스·인덱스·설치 상태를 재기준화한다. 상세 경로와 SHA는 VALIDATION.json을 본다.\n\n'+
 '운영 등록·인덱스 발행·임베딩/이미지 호출·설치 활성화·commit/push는 이번 작업에서 수행하지 않았다. 연구 질의 128개와 초기 이미지 비교 36 arms는 계획이며 모두 미실행이다.\n')
files=sorted(f for f in P.iterdir() if f.is_file() and f.name!='SHA256SUMS')
(P/'SHA256SUMS').write_text(''.join(f'{sha(f)}  {f.name}\n' for f in files))
print(json.dumps(dict(status=result['status'],files=len(files),protected_changes=len(changes),
 audit_module_drift=module_drift,audit_manifest_drift=manifest_drift,counts=summary),ensure_ascii=False))
