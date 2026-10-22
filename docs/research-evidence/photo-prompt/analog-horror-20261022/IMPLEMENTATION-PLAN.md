# 아날로그 호러 연구 결과 반영 계획

상태: **계획 수립 완료 / 운영 반영 NOT_RUN**. 연구 자료의 72개 초안을 그대로 72개 운영 후보로 추가하는 계획은 아니다. 현재 원문 의미를 보존하면서 재사용·수정·신규·문맥·보류를 먼저 결정한다.

## 0. 구현 직전의 기준 고정

`BASELINE.json`은 시작 HEAD와 추적 파일 해시, dirty 상태를 보존한다. 이 저장소는 다른 작업이 진행 중이므로 구현 직전에 HEAD·manifest·각 source module·index·installed generation을 다시 고정한다. 연구 당시 후보 수나 source hash를 구현 시점의 값이라고 가정하지 않는다.

고정할 항목은 `assets/photo_candidate_corpus_manifest.json`, 그 manifest가 선언한 모듈 전체, `assets/photo_candidate_search.json`의 전체 closure, `retrieval-runtime.json`, 설치된 H-F2 generation과 bound Python이다. source read 중 변화를 발견하면 그 묶음을 채택하지 않고 다시 snapshot한다. 옛 연구 증거를 새 결과로 덮어쓰지 않는다.

이번에 읽기 전용 `photo_installed_h_f2.py --check-runtime`은 pass였다. 이는 설치된 recorder·의존성 점검이며 연구 카드의 등록·검색·native 승인이 아니다. 이미지 호출과 source write는 0이었다. 구현 전 동일 검사를 새로 수행한다.

산출물: `integration-evidence/baseline-<time>.json`, 보호할 dirty 파일의 해시, 명시적 수정 allowlist. 중단 기준: 해시 혼합·manifest read drift·누락된 source·현재 backend 불명. 기존 미완료 작업을 되돌리는 방식으로 해결하지 않는다.

## 1. 원문별 채택 심사

순서대로 `existing-source-mapping.json`의 19개 전체 레코드를 최신 source에 재대조한다. 표본 순서는 relevance rank가 아니다. 아래는 우선 판단이며 최종 native 승인은 아니다.

|대상|권장 판단|구현 시 검토할 정확한 변화|
|---|---|---|
|VHS 홈비디오 거실|reuse|설정으로만 재사용. 카세트 물체·결함 전체로 확장하지 않음|
|VHS scanlines and color bleed|refine|display raster의 주사선과 playback color spread를 독립 선택 가능하게 분리; 기존 material effect와 새 image effect 범위 재검토|
|조건부 dropout 분기|reuse/refine|물리 carrier와 이미 선언된 playback image의 경계·분기 조건 보존|
|렌즈 ghosting|기존 source 보존|방송 echo 의미로 재태깅하지 않음; 별도 relation이 없을 때 신규 생성|
|천체/VTuber tracking|오탐 대조|테이프 트래킹 source로 채택하지 않음|
|저채도·고채도 대비 chroma|오탐 대조|Y/C delay·색 번짐 source로 채택하지 않음|
|애니매트로닉 subject·무대|reuse|기존 외형·설정 사용, 기구 접점이 필요할 때만 보완|
|유기 건축|reuse complete|기존 wall/membrane/conduit와 directed relation 전체를 보존|
|고유 작품·시간·소리·동의·의도|context/defer|장르·외형 후보의 하드 픽셀 의무로 전환하지 않음|

장르의 표현성을 높이기 위해 기존 인물·장소·소품을 임의로 추가하지 않는다. 독립적으로 정한 장면의 주제·행동·관계·중심 사건을 고정한 뒤, 그 장면에 맞는 완전한 후보만 선택한다. 기술 결함은 대체재이며 여러 결함을 모두 필수로 합치지 않는다.

산출물: `adoption-decisions.json`에 각 source ID, 선택 branch/RID, reuse/refine/new/context/defer, 변경 전후 field와 해시, 보존할 조건·effects·원전 위치, 검토 이유. 통과 기준: 200개 route에 반영/비반영의 이유가 있고, 신규 순증 수가 결정되며, 기존 관계의 무단 축소가 없다.

## 2. 데이터 형태로 이식

예정 신규 파일은 아래와 같다. 실제 순증이 필요할 때만 만든다.

- `skills/photo-prompt-image-generator/assets/photo_analog_horror_semantics_20261022.json`: 연구 의미·출처·처리 경로 sidecar. 현재 loader가 이를 자동 소비한다고 가정하지 않는다.
- `skills/photo-prompt-image-generator/assets/photo_candidate_analog_horror_20261022.json`: 검토를 마친 native `photo-candidate-module/v3` 레코드만 포함.
- `skills/photo-prompt-image-generator/assets/photo_candidate_analog_horror_bindings_20261022.json`: 독립 검토한 native slot binding만 포함.
- `skills/photo-prompt-image-generator/references/analog-horror-visual-semantics.md`: 범위·혼동·관찰 한계·예시.

기존 source 수정은 심사에서 확정한 payload owner 파일만 allowlist에 넣는다. 현재 manifest에 `candidates`와 `slot_bindings` 모듈을 추가할 수 있지만, 지원하지 않는 `semantic_registry` 같은 module kind를 임의로 만들지 않는다. 위 sidecar는 manifest의 임의 kind로 등록하는 파일이 아니다.

각 연구 카드를 native 후보로 옮길 때 다음을 채운다.

|연구 필드|운영 반영 방식|필수 검토|
|---|---|---|
|positive_en / positive_ko|기존 content의 정식 한영 표현·발견 텍스트|모든 owner·동일 방향 관계·조건·한계의 번역 대응|
|owners / relations|현재 방식과 호환되는 `content.authored_components` 및 선택된 evidence obligation|끝점·carrier·좌표계·동일 객체 여부를 빠짐없이 유지|
|layer|원래 source 의미와 맞는 명시적 owner/scope로 표현|신호 결함이 피부·벽·플라스틱 재질로 새지 않음|
|render_gate_proposals|선택한 realization의 가시 의무|부분·가려짐·병합·반전은 fail; 소리·시간 의미를 포함하지 않음|
|source_ids|제목·URL·실제 읽은 위치·주장 범위의 provenance|저술한 장면을 원작의 사실로 인용하지 않음|
|proposed_slots|현재 slot catalog의 역할 관계로 매핑|연구의 text_carrier는 `visible_text`; spatial relation은 필요에 맞는 기존 slot|
|effects|선택이 바꾸는 실제 dimension과 owner target만 기록|전체 카드의 effects를 합집합으로 강제하지 않음|
|conditions|carrier·디지털 전송·주제·선택 branch 조건|장르 태그 하나가 기존 intrinsic 조건을 무효화하지 않음|

`image_artifact` 역할의 신호/표시 효과를 모든 물체의 `material` 변화로 처리하지 않는다. 반대로 CRT 외함·유리·물리 테이프 표면의 재질은 별도 물체 의미다. 후보 내용과 binding 역할은 분리한다. 같은 source가 다른 slot에서 제시되더라도 source의 고유 의미와 조건을 유지한다.

ID 정책: 단순 발견 표현 보강은 동일 의미 범위 안에서 수행한다. 실질 의미·필수 성분·분기가 달라지면 기존 결과를 새 성공으로 재해석하지 않는다. 기존 증거는 보존하고 successor·명시적 변경 기록과 새 qualification을 만든다. 연구용 `draft_Axxx`는 운영 CID/RID가 아니다.

## 3. 출처 공백을 채우는 작업

이번에 후보 초안으로 만들지 않은 6개는 A002 VHS-C/어댑터, A012 시험 컬러바, A015 텔레텍스트 격자, A058 형상 지각, A061 기구 접점, A076 모스 부호다. 각각 실물/규격/원전/정확한 문자열을 확보하고 카드의 범위를 재검토한다. P0에 관련 카드가 있어도 공백을 해결하기 전에는 그 초안을 운영 채택하지 않는다.

고유 설정은 183~200번 각각의 상태를 따른다. 우선순위는 M.A.D. 원전 정의, Walten 원작/당사자 인터뷰 본문, Vita Carnis 공식 자료, Kane Pixels판 ASYNC/Complex의 원전 에피소드·시각 시점이다. creator, work, episode, publication/version, timecode, visible claim, inferred claim, fan interpretation을 기록한다. 조회 실패를 팬 위키로 조용히 대체하지 않는다.

## 4. 독립 인덱스와 실제 검색 평가

읽은 현재 빌더는 `build_shared_candidate_index.py`의 `--output-assets`를 지원한다. 예시는 **후속 단계 실행용**이며 이번에는 실행하지 않았다.

```sh
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_shared_candidate_index.py \
  --backend embeddinggemma2-local \
  --output-assets /absolute/analog-staged/assets \
  --cache /absolute/analog-build-cache --batch-size 32

.venv/bin/python skills/photo-prompt-image-generator/scripts/build_shared_candidate_index.py \
  --assets /absolute/analog-staged/assets --verify
```

backend는 구현 시점의 활성 설정·고정 모델·실행 증거를 확인한 뒤 정한다. 이 예시가 backend 변경의 권한이나 필요성을 뜻하지 않는다. 로컬 모델이 없거나 unsafe이면 해당 hybrid 검증을 중단한다. 다른 provider나 keyword_only로 조용히 바꾸어 통과시키지 않는다. 빌더의 `--publish`는 이 평가 단계에서 쓰지 않는다. 별도 output에서 생성되는 manifest도 운영 manifest와 구분한다.

검증할 것은 전체 source/벡터/통계/샤드 closure, source text hash와 embedding recipe, 모델 공간 일치다. 전역 BM25F·실제 query embedding·exact cosine·RRF의 증거를 보존한다. role tag는 source의 의미·순위를 보장하지 않는다. `keyword_only` 결과가 필요하면 별도 진단으로 표기한다.

`EVALUATION-CASES.tsv`의 80개 사례/160개 한영 질의를 사용한다. 개발 양성 24, 별도 경계 제안 32, 일반 대조 16, 비가시 대조 8이다. 이번에 작성한 holdout은 이제 공개된 제안이므로 최종 평가에서는 **검토자가 별도의 비공개 표현 변형**을 추가한다. 후보 ID·원문 문장을 질의에 주입하지 않는다.

연구 카드 ID를 실제 채택 CID/RID로 연결한 relevance 표를 먼저 만든다. 긍정 후보 노출 recall@8, 기술 sense 오탐, carrier 누출, EN/KO 격차, 일반 요청의 불필요한 장르 추가를 baseline/staged에서 따로 측정한다. top8 노출과 최종 선택을 혼동하지 않는다.

제안하는 채택 문턱은 다음과 같다. 실행 전 기준을 고정하고 결과를 보고 완화하지 않는다.

- P0 핵심 구분 사례: 잘못된 sense·owner·branch 선택 0건.
- 일반 대조 16건: 요청하지 않은 공포·괴물·피해·신호 결함의 최종 추가 0건. 카세트·TV 자체처럼 요청된 관련 source는 허용.
- 비가시 대조 8건: 정지 외형을 원래 음성·시간·동의·초자연 효과의 성공으로 표시 0건.
- 한영 양성 recall@8은 각각 baseline 이상. 작은 고정 집합의 개선만으로 일반 품질 향상이라 주장하지 않음.
- 각 실패는 전체 레코드·선택 branch·query lane·필터·결과 순위까지 원인을 기록. 미해결 P0 오류가 있으면 채택 중단.

## 5. 장면·생성·픽셀 검증

12개 장면 × baseline/기존 의미 보완/최소 신규의 3 arms × 반복 2개 = 최대 72장으로 1차 계획했다. provider가 seed를 보장하지 않으면 같은 조건의 paired 반복으로 기록하고 동일 난수 통제라고 주장하지 않는다. 연구의 6개 보류 카드는 각각 source 근거를 채운 뒤 포함한다. 상세는 [PIXEL-PLAN.md](PIXEL-PLAN.md).

순서: 독립 authorial core → 후보 없는 자연 질의 → 후보 노출 → 전체 source/조건 심사 → 선택 → 정확한 prompt evidence → render request audit → 실제 생성 → 파일·native 픽셀 판정 → 사용자 판단. 각 단계의 통과는 다음 단계의 통과가 아니다. blocking·moderation·불가시는 이미지 성공률의 분모와 별도 상태로 보존한다.

문자/컬러바 후처리는 생성 원본을 덮지 않고 독립 파생물로 저장한다. 후처리 전후와 합성 위치·문자열·색값을 남긴다. 합성한 글자의 정확성을 원래 생성기의 능력으로 계산하지 않는다.

## 6. 설치·공개·롤백

source·native 검증·retrieval·픽셀 근거가 준비된 뒤 현재 설치 도구의 허용 allowlist로 새 release를 stage하고 검토한다. working source 수정만으로 installed code가 바뀌었다고 보고하지 않는다. CURRENT·기존 source/index manifest·backend default·실행 이력을 백업하고 새 source/index/generation의 일치를 확인한 뒤 전환한다.

롤백은 단일 옛 manifest만 복사하는 방식이 아니라, 서로 호환되는 source/index/runtime generation 묶음으로 복구한다. 다른 작업이 추가한 source를 누락시키지 않도록 현재 corpus와의 호환성을 검사한다. 이전 실행 증거·shard를 삭제하지 않는다. 커밋·push·PR은 별도 요청과 범위에 맞춰 수행하고, 명시적 파일 allowlist와 staged 이름·해시를 대조한다.

## 완료 조건과 규모

이번 연구의 완료 조건은 200개 키워드의 경로, 78개 카드, 72개 비운영 초안, 근거 한계, 실제 source 표본 판단, 80개 평가 계획, 구현·중단·롤백 절차가 재현 가능하게 남는 것이다. 실제 운영 반영 완료 조건은 각 단계의 실행 증거가 별도로 충족되는 것이다.

구현 규모는 원전 추가 조사·19개 기존 source 재심사·필요한 신규 순증 수·현재 인덱스 재사용률에 따라 달라진다. 72개 초안을 기계적으로 모두 등록하거나 예측 불가능한 이미지 품질을 일정으로 보장하지 않는다. 먼저 P0 데이터와 검색 비교를 수행하고, 그 결과로 P1의 후보 범위와 생성 비용을 확정하는 순서다.
