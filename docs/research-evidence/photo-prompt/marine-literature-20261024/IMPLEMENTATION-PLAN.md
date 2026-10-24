# 데이터 반영 계획

> 후속 실행: 아래는 최초 연구 시점의 계획이다. 실제 등록·검색·생성 결과와 남은 한계는 [반영 및 이미지 검증 결과](INTEGRATION-RESULTS.md)에 별도로 기록한다.

상태: 연구 완료, 운영 데이터 반영 전. 모든 경로는 `/Users/chasoik/Projects/image-prompt` 기준이다. 이 문서의 명령은 후속 구현 예시이며 이 연구에서 실행한 결과가 아니다.

## 단계 0 — 최신 기준선과 의미 중복 확인

현재 작업 트리는 연구 시작 때 이미 2,649개 dirty 항목을 가졌다. `BASELINE.json`에 당시 HEAD와 manifest 모듈·검색 manifest·슬롯 카탈로그·스크립트 등 197개 해시를 기록했다. 현재 연구 폴더만 수정한다. 구현 직전에 HEAD·dirty 상태·staged 목록·전체 source closure·CURRENT를 다시 읽는다. 다른 연구와 파일 변경을 되돌리거나 넓게 stage하지 않는다.

`audit_corpus.py`는 현재 저장소의 긍정 projection을 사용하는 읽기 전용 발견 도구다. 이를 다시 실행하고 `existing-source-mapping.json`의 원문·conditions·effects·모든 binding을 대조한다. 특히 `new`는 아직 의미 중복을 모두 제거했다는 선언이 아니다. 새 후보 작성 전에 85개 잠정 새 정의 각각을 실제 검색과 전체 레코드로 확인한다.

완료 조건: 모든 카드가 `reuse/refine/new/context/defer` 중 하나로 최종 분류되고, 해당 근거·기존 ID·변경 범위·우선순위가 설명된다. 이름 일치·0건·가짜 부분문자열로 분류하지 않는다.

## 단계 1 — P0: 일반 형태와 접점

먼저 의복과 패치 운반체, 모자 모체/챙, 식별표 연결, 공구·식판의 형태, 일반 포즈의 팔·손·지지점, 카메라 방향을 반영한다. V001–V022·V027–V058·V071–V073·V075–V081에서 기존 재사용 가능 자료를 먼저 고른다. 이 범위 내에서도 자료가 약하거나 매체·판본 선택이 필요한 것은 미루며 번호 범위 전체를 일괄 승인하지 않는다.

조건은 사람/성인·선택된 옷 형태·매체·원래 인물 수·특정 대상의 소유를 유지한다. 등장인물이 성인이라는 사실을 adult_presentation_context 또는 성적 표현 활성화의 근거로 쓰지 않는다. 가슴 패치·군복 체계·군인 subject는 효과 범위가 다르므로 하나의 빈 binding으로 우회하지 않는다.

새 데이터의 예상 구조는 `photo_candidate_marine_literature_20261024.json`의 후보, 대응 binding 모듈, 선택형 의미 sidecar다. 이 이름들은 계획이며 파일을 아직 생성하지 않았다. `candidate-drafts.json`의 D_Vxxx는 native CID/RID가 아니다. 기존 ID 생성·source guard·검증 규약으로 컴파일해야 한다.

기존 후보 전체를 재사용할 때 손바닥 방향·필수 TV·탁자·타깃·성인 조건·효과·매체·native qualification을 잘라내지 않는다. 새 의미를 넣으려고 조건을 지우지 않는다. 재사용 후보의 추가 관찰 게이트는 연구 장면의 요구이며 기존 소스가 그것을 이미 보장한다고 재표시하지 않는다.

## 단계 2 — P1: 공간·차량·판본과 그래픽

컨테이너 층·생활관 통로·창/문·차량 승객실·화물칸·운전대 접점·기계 머리 등은 연결과 규모의 검증이 필요하다. 17층 카드와 일반 적층 카드를 구분하고, 17이라는 글자를 층수의 대용으로 사용하지 않는다. 운전자·동승자·외부 인물의 손과 차량이 섞이지 않게 한다.

캐릭터 문맥에는 출처·게시 시점·작품/팬아트 판본·원작자 확인 상태·참조 이미지·관찰 가능한 외형을 둔다. 단일 공식 캐릭터 외형·정확한 봉고 연식·실제 도시가 변형된 것 같은 주장은 자동 생성하지 않는다. 이번에 원본 이미지를 읽지 못한 외형은 팬아트 픽셀 자료 확인 전 `defer`로 남길 수 있다.

만화 그래픽 9개 카드는 medium을 명시적으로 고른 뒤에만 검토한다. 효과선·큰 문자·먹선·눈물·반응 컷을 사진의 일반 꾸밈으로 활성화하지 않는다. 말풍선·표어판·메뉴 카드·자막의 서로 다른 운반체를 보존한다.

## 단계 3 — P2: 문맥과 관찰 불가능한 주장

30개 성적·폭력적·배설 관련 입력은 원뜻과 다의성을 보존하는 diagnostic 자료로 검토한다. `diagnostic`은 현재 코퍼스에서 허용되는 kind이며 `photo_global_index.POSITIVE_KINDS`는 이를 제외한다. 문맥 레코드를 만드는 경우에도 네이티브 스키마·키·source guard를 지켜야 한다. 파일을 단순 sidecar로 놓는 것만으로 로더가 의미를 실행한다고 가정하지 않는다.

위계 평가·동성사회성·지향·합의/강요·피해 이력·실제 물질·소리·부활·드리프트·시간 경과는 시각 명제의 필수 증거로 사용하지 않는다. 장르명·인물 이름으로 맨상체·빨강·고어·성적 장면을 자동 추가하지 않는다. 원뜻을 평범한 단어로 치환해 포괄했다고 표시하지 않는다.

순서형 T001–T004, 문패 V064, 내용물 미확정 메뉴 V074는 이번 90개 긍정 초안에서 제외했다. 연속 이미지/문자/음향이 명시된 작업에서 별도로 설계한다.

## 단계 4 — 독립된 소스·인덱스 제작

현재 확인한 경계는 다음과 같다.

- 소스 manifest: `skills/photo-prompt-image-generator/assets/photo_candidate_corpus_manifest.json`, 모듈형 `photo-candidate-corpus/v3`.
- 역할: `photo_candidate_slot_catalog.json`의 149개 슬롯과 직접/문맥 역할. 후보에 붙는 slot ID와 effects는 독립 검토한다.
- 검색: `photo_candidate_search.json`의 `photo-candidate-search-layout/v1`. 이번 관찰은 `embeddinggemma2-local`, `google/embeddinggemma-2`, 768차원, `embeddinggemma2-retrieval/v1`이었다. 과거 Gemini 메모를 현재 값으로 쓰지 않는다.
- 실제 코드: `photo_candidate_corpus.py`, `photo_semantic_evidence.py`, `photo_global_index.py`, `photo_visual_retrieval.py`, `photo_global_retrieval.py` 및 slot/global lane.
- 빌더: `build_shared_candidate_index.py`; 검증: `validate_photo_prompt_dictionary.py`; 스냅샷: `publish_photo_runtime_snapshot.py`.

후속 작업은 별도 완전한 skill root를 준비한다. 원래 소스를 통째로 보호 복사한 staging root에 검토된 후보만 적용하고, 그 root의 assets에 새 인덱스를 만든다. 기본 assets에 빌더를 실행하면 검색 manifest가 바뀌므로 피한다. `--output-assets`는 출력 소스와 입력 소스의 일치 검사를 하므로 이미 수정된 다른 assets를 복잡하게 resume하는 우회로 쓰지 않는다.

아래는 후속 구현 때 사용할 실제 CLI 형식이다. 경로의 `/absolute/staging/...`는 준비한 별도 root로 바꾼다.

```sh
python3 /absolute/staging/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py --assets /absolute/staging/photo-prompt-image-generator/assets
python3 /absolute/staging/photo-prompt-image-generator/scripts/build_shared_candidate_index.py --assets /absolute/staging/photo-prompt-image-generator/assets --backend embeddinggemma2-local --cache /absolute/staging/build-cache
python3 /absolute/staging/photo-prompt-image-generator/scripts/build_shared_candidate_index.py --assets /absolute/staging/photo-prompt-image-generator/assets --verify
python3 /absolute/staging/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py --assets /absolute/staging/photo-prompt-image-generator/assets
```

첫 검증에서 새 소스와 옛 파생 인덱스의 불일치가 예상되면 source-only 검사와 index 검사 결과를 따로 기록한 뒤 재구축한다. 검증 실패를 숨기거나 recipe 이름만 바꾸지 않는다. 벡터는 모델 패키지/리비전/공간·차원·정규화·실행 recipe와 텍스트 recipe·해시가 정확히 같은 경우만 재사용한다. 새 긍정 텍스트에는 실제 임베딩이 필요하다. 구성 파일 확인은 임베딩 서비스의 실제 가용성 증명이 아니다.

완료 조건: 소스·owner guard·binding·검색 파생물의 정확한 closure가 일치하고, source drift가 없으며, 기존 후보가 손실되지 않는다. 이 단계는 이미지 품질 합격이 아니다.

## 단계 5 — 실제 검색과 회귀

`evaluation-cases.json`에 40개 사례와 한영 질의 80개를 마련했다. 아직 실행 결과가 아니다. 동일 frozen core에서 독립 slot 검색과 주제/기본 프롬프트 기반 whole-scene 검색을 모두 확인한다. lane을 합쳐 한 lane의 누락을 가리지 않는다.

일반 경례·뒷짐·로우앵글, 삼각/사각·패치/목줄·승합/트럭·물체색/조명·그래픽/현상·공간/매체의 양성·음성 대조를 실행한다. 각 결과는 순위·CID·RID·선택 realization·조건 통과·소유자 바인딩·실제 전달된 문구까지 기록한다. `NONE`, `context`, `UNOBSERVABLE` 기대값 사례를 top-k 노출률에 억지로 포함하지 않는다.

제안된 종료 기준은 시각 양성 사례의 적절 후보 top-8 노출 95% 이상을 개발 목표로 쓰되, 소유자 뒤집힘·원뜻 덮어쓰기·민감 문맥 자동 활성화·locked dimension 위반은 0건이어야 한다. 수치는 사전 제안이며 관측 결과가 아니다. 단일 사례의 필수 구분이 실패하면 해당 후보는 노출률과 무관하게 채택 보류다. 기존 일반 군복·군인이 아닌 패션·음식·제품·야생동물·일반 포즈 회귀도 실행한다.

## 단계 6 — 원본 픽셀과 채택

[픽셀 계획](PIXEL-PLAN.md)의 12개 검증군에서 요청 의미를 먼저 동결하고, 그 뒤 후보를 검색·채택한다. 새 이미지 생성은 이 연구의 실행 범위가 아니며 0건이다. 세 독립 전체 장면 A/B/C는 복식 접점, 다인 포즈와 차량, 적층과 문자로 분리해 실패 원인을 읽을 수 있게 한다.

원본 픽셀에서 모든 필수 그룹과 방향 관계가 같은 arm에 보여야 한다. 소스·검색·프롬프트 감사의 PASS는 픽셀 PASS가 아니다. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`, `BLOCKED_UNSCORED`를 유지한다. 차단으로 파일이 없으면 무점수이며 같은 프롬프트를 그대로 반복하지 않는다. 사용자 수락은 별도다.

각 카드의 출처 의미검토, 실제 검색, 픽셀 qualification이 충족된 범위만 운영 채택한다. 스냅샷 게시·설치와 저장소 commit/push는 별도 결과로 기록한다. 게시 단계는 준비한 소스 root와 runtime store를 명시하며 기존 CURRENT를 먼저 보존한다. 현재 연구 산출물을 즉시 운영 데이터로 등록하거나 commit/push하지 않았다.

## 우선 완료 단위

1. 일반 경례·뒷짐·로우앵글의 기존 ID 재사용 범위와 상속 조건 확정.
2. 팔각모·패치·부츠·식판·스패너의 새 관찰 계약과 기존 의미 중복검토.
3. 두 성인의 팔/손·시선·문틀·차량 접점 회귀.
4. 성채와 차량의 판본 및 관찰 가능성 검토.
5. 인물별 팬아트 외형의 실제 픽셀 출처 보완.
6. 만화 매체와 문맥 자료의 선택적 등록, 별도 네이티브 검증.
