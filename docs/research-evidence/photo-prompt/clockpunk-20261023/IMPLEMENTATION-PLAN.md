# Clockpunk 조사 결과 반영 계획

2026-10-23. 구현을 바로 시작할 수 있는 작업 단위·입출력·의존성·완료 조건을 기록한다. **현재는 연구 패키지만 작성했다. 아래 source/인덱스/런타임/이미지 단계는 계획이다.**

## 1. 목표와 우선순위

최종 목표는 Clockpunk 요청에서 **요청자가 원하는 기계·인물·생활 관계를 정확히 검색하고, 소유자와 효과 범위가 맞는 후보만 선택적으로 제시하며, 실제 생성물에서 그 관계를 확인**하는 것이다. 장르 단어가 있으면 모든 신규 카드를 적용하는 방식은 채택하지 않는다.

| 차수 | 대상 | 이유 | 종료 조건 |
|---|---|---|---|
| P0-교정 | 기존 6개 CID의 번역/과도한 기능·시간 주장·증기 배제 | 신규 추가 전 현재 오해를 줄임 | 한영·embedding·조건·효과·binding이 같은 전체 뜻을 보존; 보존 snapshot |
| P0-기계 | 태엽/추/기어/탈진/실태엽/퓨지, 캠·랙·웜·베벨·제네바 | 핵심 구별의 검색과 구조가 빈약 | 각 관계와 소유자의 직접 witness·자격 검토; 기구별 구분 사례 |
| P0-천문 | 아스트롤라베·환구의·오러리 | 실제 번역 혼동 확인 | 비교/단독 요청 모두에서 물건을 바꾸지 않음 |
| P0-생활 | 필기·감기·수리·의수·자격루/가라쿠리 | 기계를 노동·몸·생활과 연결 | 손/도구/접촉/몸 경계·지역 provenance 유지 |
| P1-확장 | 공방·가동 건축·복식·궁정·유물 성인 미학·기계 병사 | 조합의 장면 폭을 넓힘 | whole realization과 장르/신분/의도 해석 분리 |
| P1-문맥 | 자유의지·동의·예속·소유·고문/처형·빙의·역병 | 비가시 의미를 지우지 않고 오판 방지 | diagnostic/context 레코드와 시간 검증 요건 분리; positive 이미지 사실로 내보내지 않음 |

연구의 78개 초안을 모두 새 CID로 만드는 목표는 두지 않는다. 중복 제거·기존 재사용·문맥 분할·물리 관계 검토 뒤 실제 신규 CID 수와 binding 수를 확정한다. 모듈 크기나 카드 수가 의미 품질을 대신하지 않는다.

## 2. 단계 A: 재기준화와 입력 보존

입력은 `BASELINE.json`, `reference-dom.json`, `keyword-routes.json`, `existing-source-mapping.json`이다. 구현 시작 시 HEAD·dirty/untracked 목록·source manifest/module hash·slot catalog·설치된 세대를 다시 읽어 별도 `integration-evidence/BASELINE.json`으로 보존한다. 연구 시점 snapshot을 최신 증거로 덮어쓰지 않는다.

현재 작업 트리에는 SKILL·runtime·후보·인덱스 등 다른 변경이 많다. 연구 패키지는 새 폴더에만 썼다. 기존 6개 CID가 있는 모듈을 수정하기 전 원본/현재 diff/다른 작업의 변경을 대조한다. 게시가 나중에 요청되면 적합한 기존 checkout/worktree를 먼저 확인하고, 충돌 위험이 크면 별도 관리 worktree에 검토한 변경만 재구성한다.

완료 조건: 변경 allowlist·보호 파일 hash·최신 기준 상태가 분리되고, 연구 원본은 보존된다. 아직 어떤 후보도 채택되지 않는다.

## 3. 단계 B: 남은 원전·언어·물리 관계 검토

1. `additional_engineering_review_required` 7개 카드의 실제 기구/복식 원전·도판을 추가한다. 현대 공학과 특정 시대의 제작 가능성을 별도 판단한다. 색인만 읽은 8개 자료는 가능하면 본문/대체 공식 자료로 보완하고 실패 시 그대로 제한을 남긴다.
2. M03의 수운의상대/자격루, M04의 가라쿠리/터크, F07의 수레/트레드휠, G03의 양식, H04/L02/J05/K04의 문맥을 서로 다른 레코드로 분할한다. 한 장면에서 여러 물건을 비교하는 선택지는 별도 완전 bundle로 저술한다.
3. EN/KO의 명사·수량·부품·연결·작용점·부정·표현 층을 항목별 대조한다. `orrery=오러리/태양계 운동 모형`, `armillary sphere=환구의/혼천의형 천구 기구`, `plane astrolabe=평면 아스트롤라베`를 자동 동의어 병합하지 않는다.
4. A01 태엽통 내부 노출, A07 체인 양끝, C01 펜촉, F03 감는 손, I01 의수 소켓, J02 그림/종이/현실 손의 종단을 도판과 대조한다. 사람이 있는 실현은 reach·관절·하중·지지·가림을 검토한다.

완료 조건: 각 등록 예정 레코드마다 출처 지원 범위, 저술한 허구 범위, 명확한 owner graph, 재료/수량/연결/행위 전체가 양 언어에서 일치한다. `아직 검토 안 됨`은 보류로 남으며 교정용 alias로 숨기지 않는다.

## 4. 단계 C: 실제 데이터 저술 위치

| 경로 | 반영할 내용 | 권위 범위 |
|---|---|---|
| `skills/photo-prompt-image-generator/assets/photo_clockpunk_semantics_20261023.json` (신규 제안) | 검토한 카드·키워드 경로·혼동·출처·기존 CID 결정 | 연구/유지보수 sidecar; 자동 사실/역할 권위 아님 |
| `assets/photo_candidate_clockpunk_20261023.json` (신규 제안) | 승인된 완전 시각 대안과 분리된 context/diagnostic 레코드 | canonical candidate 한 개당 하나의 소유 원본 |
| `assets/photo_candidate_clockpunk_bindings_20261023.json` (신규 제안) | 실제 검토한 CID→slot 관계와 적용 조건 | 역할 적합성; intrinsic effect 복제 금지 |
| `assets/photo_candidate_corpus_manifest.json` | 후보/binding 모듈만 명시 등록 | authored source 진입점 |
| `references/clockpunk-visual-semantics.md` (신규 제안) | 입력 의미·기계 기능 구분·비가시 경계·검증 상태 | 사람용 조사/실행 안내 |
| `references/maintenance.md` | 새 확장 문서 링크와 정확한 증거 상태 | 유지보수 안내 |
| 기존 `_000/_001/_002/_014/_015` module 중 실제 해당 CID | snapshot의 6개 보정 결정만 최신 문맥에 맞춰 수정 | 기존 조건/효과/다른 CID 보호 |

위 표의 `assets/`와 `references/`는 모두 `skills/photo-prompt-image-generator/` 기준이다. 실제 작업 시 diff는 절대 경로 allowlist로 관리한다. 연구 파일을 operating manifest에 그대로 등록하거나, sidecar를 별도 sampler/새 의미 엔진으로 연결하지 않는다. SKILL의 기본 controls·pre-core 접근 규칙·관계 engine은 이번 데이터 보강 때문에 변경하지 않는다.

기존 CID 수정은 원래 의미를 유지하는 번역 정정과 의미 변경을 구별한다. 허구 포켓워치처럼 본래 복합 의미를 해체하면 기존 ID를 억지로 역사 기구로 바꾸지 말고, 기존 허구 대안을 보존한 채 별도 ID와 명시 disposition을 둔다. `without steam` 수정도 요청자가 지정한 순수 동력 조건을 지우는 일반 완화가 되어서는 안 된다.

## 5. 단계 D: owner·guard·effect·native 자격

현재 `photo_candidate_corpus_manifest.json`의 V3 candidate/binding, 실제 V10 pack, V3 generation/receipt 계약을 따른다. 옛 메모의 pack 버전이나 다른 실험의 proof를 가져오지 않는다. 실현의 모든 긍정 필드가 동일 CID/RID의 실제 source quotation에 의해 검토되도록 `photo_semantic_evidence.py`와 `photo_native_owner_resolution.py`의 현행 계약을 사용한다.

- 부품은 object_structure, 상호작용은 relational_action/contact_point, 재료 정체는 surface_material, 탄성 반응은 material_mechanics, 광학 흐림은 motion_rendering으로 각각 소유자/속성을 검토한다. 같은 사실을 이웃 역할에 태그만 바꿔 중복 승인하지 않는다.
- 새 사람·손·장치·의복·수량·표면·텍스트·배치·행동이 문구에 포함되면 실제 전체 effects에 반영한다. 연구의 `affected_dimension_proposal`과 catalog descriptor는 완전 effects 목록이 아니다.
- intrinsic guards와 role guards는 분리한다. `requires_primary_any_tags` 같은 기존 guard를 새 binding으로 우회하지 않는다. 선택적 관찰 구조가 새로운 소유자·신체·제도·성적 맥락을 만들 권한을 주지 않는다.
- alternative와 conditional branch는 실제 선택 RID별로 완전하게 분리한다. 태엽/수력/인력 대안, 서로 다른 시대 의복, 좌우 의수, 서로 다른 그림 층을 합집합으로 섞지 않는다.
- `context_only`의 철학/동의/신분/이력은 가시 사실로 승격하지 않는다. 양성 전체 소스에서 지원되지 않는 qualifier를 metadata·alias·인용 URL로 보충하지 않는다.
- native 미자격은 `review_required`/보류로 남긴다. 정합한 JSON·후보 등록·검색 노출·연구 graph는 source 자격 승인과 별개다.

완료 조건: 각 예정 CID/RID의 완전 원문·conditions·effects·owner endpoints·실제 role를 직접 검토한 증거와 qualification 결과가 있다. 하나라도 미확정이면 등록/검색 실험의 상태와 채택 가능 상태를 분리한다.

## 6. 단계 E: 구조 검사와 필요한 회귀

먼저 새 데이터 모듈에 대해 `scripts/validate_photo_prompt_dictionary.py --assets <staged-assets>`를 실행한다. 실제 schema와 현행 로더가 source/binding/중복 ID/참조를 통과하는지 확인한다. 그 뒤 변경에 맞는 기존 semantic boundary·source context·gap source 테스트를 선택한다. 등록되지 않은 이 연구 패키지만 작성한 현재 턴에는 runtime 테스트를 실행할 이유가 없다.

새 의미 회귀는 다음 위험에 집중한다: 동력 태엽/실태엽, 세 천문기구, 웜 자기잠김, 그림/실물/의수의 owner, 전후/측정/음향 claim, EN/KO 범위 차이, 장르명→성적/폭력/신분 자동 활성화, `no_people`와 고정 인물 수·기존 소유자·동력/시대 lock. 단순 JSON을 다시 읽는 테스트나 구현 문장을 그대로 되풀이하는 테스트는 추가하지 않는다.

완료 조건: 변경 관련 회귀의 결과·미실행 범위·실패 원인이 기록된다. 일반 손목시계·보철·재료 사진에 장르나 신분을 억지로 붙이지 않는다.

## 7. 단계 F: 별도 인덱스와 runtime 경계

`scripts/build_shared_candidate_index.py`의 현행 옵션으로 staging generation을 만든다. embeddings와 BM25F를 실제 recipe/model/space/source fingerprint에 맞춰 검증하고, changed text만 적절한 재계산 대상으로 삼는다. 새 en/ko/embedding 문구인데 예전 vector/proof를 그대로 유지하지 않는다.

초기 단계는 active manifest·installed CURRENT를 바꾸지 않는 별도 생성물로 비교한다. `--verify` 통과는 source/index/extent 무결성 증거이며 의미 적합성이나 픽셀 증거는 아니다. runtime 게시가 후속 실행 범위에 포함될 때 검토한 code/data allowlist로 sealed release를 만들고 설치/활성화 검증을 별도로 수행한다. working-source 변경만으로 installed code가 바뀌었다고 보고하지 않는다.

완료 조건: 기존/신규 세대·model/recipe·corpus hash·검색 execution receipt를 재현할 수 있다. 구체 명령 옵션은 구현 시 현행 CLI `--help`로 확인하고 미래 옵션을 가정하지 않는다.

## 8. 단계 G: 실제 검색 비교

입력은 `EVALUATION-CASES.tsv` 120사례×2언어=240질의다. 88개 개발 사례와 32개 경계/일반 사례로 구성했으며 독립 holdout이 아니다. 별도 작성자가 source 문구를 보지 않고 만든 최소 24개 자연 요청(각 언어 12개)을 잠근 뒤 별도 holdout으로 추가한다. 이번 조사에서 그 holdout의 성공을 가정하지 않는다.

같은 query/spec/core와 기존/신규 세대로 아래 항목을 기록한다.

| 지표 | 계산/판정 |
|---|---|
| 의미 recall@5/@10 | 요청에 맞는 소유자·관계·부품의 최소 허용 집합이 노출됐는지; 장르 태그만 맞는 후보는 정답 아님 |
| precision@5 | 실제 전체 문구가 요청/role/effect 범위에 맞는지 직접 판정; 관련 단어만으로 정답 처리 금지 |
| 언어 차이 | 같은 의미의 EN/KO 요청에서 천문기구/부품/관계가 바뀌는지 |
| 부당 활성화 | 일반 control에서 강제되는 기계·성적·폭력·직업·신분 의미가 있는지 |
| 보류율·원인 | 자격·소유자·효과·가시성·번역 때문에 decline한 사유 |
| 실제 채택 | 단순 노출/검토/선택/완전 채택을 별도 수치로 보고 |

시작 전 합의할 제안 목표는 개발 P0의 최소 허용 노출 recall@10≥90%, 독립 자연 요청≥80%, hard lock/비가시 주장의 잘못된 승격 0건이다. 이 수치는 계획 목표이며 성과가 아니다. 임계값을 맞추기 위해 동의어를 과확장하거나 실패 질의를 개발 집합으로 옮기지 않는다. 일반 후보가 관련 부품으로 노출되는 일과 부당한 장르/의미 활성화도 구분한다.

## 9. 단계 H: 프롬프트·이미지 비교와 채택

[PIXEL-PLAN.md](PIXEL-PLAN.md)의 첫 12군×3 arm=36장을 제안한다. 이미지 생성은 이번 요청의 실행 내용에 포함시키지 않았고 미실행이다. 향후 실행 시 실제 허가된 범위와 사용 가능한 generator/runtime를 확인한다.

독립 요청 의미→baseline freeze→선택적 retrieval→authorial decision 순서를 지킨다. 원 대화의 예시 소품을 requester-owned anchor로 고정하지 않는다. 동일 의미/controls/대상 버전을 비교하고 최종 staging·owner/effect changes·declines를 남긴다. 중요한 연결의 양끝·접촉·크기·대비·깊이·가림이 실제 저장된 픽셀에서 읽혀야 완전 통과다. 비교식 원전 검증·native source 자격과 실제 이미지 결과를 혼동하지 않는다.

완료 조건: 구조별 saved image와 exact prompt/transport hash가 연결되고, 부분·가림·비가시는 전체 의미 PASS에서 제외된다. 정지 이미지로 작동 성공·동의·인격·반복을 판정하지 않는다. 생성 차단/실패는 픽셀 점수의 0점 표본으로 섞지 않고 `blocked_unscored`로 별도 보고한다.

## 10. 게시·보존·최종 보고

커밋/푸시/배포가 후속 작업 범위라면 검토한 allowlist만 stage하고 staged 이름·hash·diff와 제외한 dirty 파일 hash를 비교한다. local/tracking/remote SHA를 별도 확인한 뒤 임시 worktree를 정리한다. 이번 연구는 커밋/푸시하지 않았다.

최종 표는 **연구 → 원본 반영 → native 자격 → 인덱스 → 실제 검색 → installed 활성화 → exact prompt 전송 → 저장 픽셀 → 사용자 수용 → commit/push**를 각각 완료/미실행/보류로 보여 준다. 어떤 단계의 PASS도 다음 단계의 성공을 대신하지 않는다.
