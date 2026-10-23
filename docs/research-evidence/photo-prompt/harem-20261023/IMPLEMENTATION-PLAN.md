# 시각 의미·후보 데이터 반영 계획

2026-10-23. 이 계획은 구현 가능한 변경 단위와 판정 기준이다. 현재 운영 source/manifest/index/설치본은 수정하지 않았다. 연구 초안에 CID를 붙이는 것만으로 반영·검색 개선·생성 품질 확보가 되지 않는다.

## 1. 우선순위와 변경 단위

|단계|우선순위|내용|완료 기준|
|---|---|---|---|
|A: 기준 재확인|P0|현재 HEAD·dirty 파일·manifest·95개 모듈 closure·설치 선택·149-slot 정의를 다시 읽는다. 연구 snapshot은 보존한다.|새 source/binding의 정확한 버전과 충돌 범위가 정해짐|
|B: 의미 경계|P0|X01–X14를 기준으로 장르/인원/성별/경쟁/교제/동의/혼인/결말/매체/시간/성격을 분리한다.|하렘·역하렘·CNM·why-choose·NTR의 비동치가 유지되고 일반 집단에 관계를 발명하지 않음|
|C: 기존 정밀화|P0|18개 CID의 전체 원문·조건·효과·역할을 재심사한다. OR/AND 번역, 자기/상대 손, 진행 상태/aftermath, 3명 이상·제한 선택의 범위를 처리한다.|기존 의미를 바꾼 수정과 별도 대안을 구분; 모든 추가 속성의 owner/effect 검토|
|D: 접촉·관계 대안|P1|H01–H26의 제안 방향·손·옷·머리·팔·시선·지지점을 후보화한다. 같은 뜻의 기존 완결 대안을 먼저 찾는다.|필수 접점과 주인이 한영에서 동일; 동기·사랑·동의를 시각 증거로 승격하지 않음|
|E: 외형·복식·구도|P1|P/A/W/C 카드 50개를 기존 source와 비교한다. 귀 장식/해부학·레이어·개구·클립·화면 경계를 별도 대안으로 유지한다.|전체 의미·조건·효과가 맞는 reuse/refine/new/context/defer 판정 완료|
|F: 잔여 외형|P2|미연결 외형 36개: 세부 재단·시대·용도·의복/몸/소재를 구체 도판으로 확인한다.|각 표제의 정확한 claim-level 근거와 통용도, 필요한 owner별 실현이 확보됨|
|G: 잔여 문맥|P2|문맥의 세부 정의가 남은 38개: 팬덤 용례, 서사적 기능, 지역/언어 차이를 확인한다.|출처의 실제 정의 범위와 pending를 기록; 무근거 동의어 병합 없음|
|H: 검증·활성화|P1 이후|source 검사→native qualification→별도 index→검색·선택→픽셀→설치 활성화를 분리한다.|각 단계의 실제 증거와 실패·차단 상태가 독립 기록됨|

‘P1 이후’는 중요도가 낮다는 뜻이 아니라 데이터 확정 후라는 의존 순서다. 새 후보 수는 미리 76개로 약속하지 않는다. 중복 재사용·분기·미확인 보류로 달라질 수 있다.

## 2. 구체 파일과 두 생성 경로

사진 데이터의 제안 경로는 다음과 같다.

- `skills/photo-prompt-image-generator/assets/photo_harem_semantics_20261023.json`: 의미 경계, 정확한 한영 표제, 정의의 범위·불확실성, keyword→선택적 실현의 관계, 출처.
- `skills/photo-prompt-image-generator/assets/photo_candidate_harem_20261023.json`: 승인한 완결 시각 대안만. 문맥 진단은 현행 제외/진단 규약에 맞게 분리한다.
- `skills/photo-prompt-image-generator/assets/photo_candidate_harem_bindings_20261023.json`: 실제 slot·owner·property·조건을 심사한 optional binding만.
- `skills/photo-prompt-image-generator/references/harem-visual-semantics.md`: 등록 범위·재사용/수정 이유·검증 결과·남은 한계.
- `photo_candidate_corpus_manifest.json`: 최종 심사를 마친 실제 모듈만 등록. 기존 모듈 수정은 별도 allowlist에 기재한다.

원래 주제가 일러스트레이션/키아트/CG인 경우에는 별도 경로를 택한다. `skills/subculture-illustration-image-generator/assets/research_evidence_moe_elements/`의 NTR/얀데레 의미 계약과 `illustration_universal_scene_candidates_v1.json`, `illustration_universal_semantic_bindings_v1.json`, 현행 grammar/compatibility 생성 규약을 읽는다. 사진 CID/binding 구조를 그곳에 복사하지 않는다. 기존 불변 의미·typed alias·명시적 활성화를 보존하는 확장 설계를 먼저 작성한다. 실제 파일명·버전은 그 시점의 소유 스키마에 맞춘다. 이번에는 양쪽 어느 것도 변경하지 않았다.

## 3. 기존 source별 결정 규칙

[18개 구체 판정](existing-source-decisions.json)을 출발점으로 현재 원문을 다시 읽는다.

- **reuse**: 전체 영어·한국어·선택 분기·개수·소유자·매체·조건·효과·의무가 같은 경우만 기존 ID를 유지한다.
- **refine**: 실제 번역·owner·효과·전제가 불완전할 때 수정 이유와 영향받는 기존 문맥을 기록한다. 원래 3명 이상 대안을 몰래 2명으로 바꾸지 않는다.
- **new**: 전체 기존 corpus를 의미 단위로 비교해 완결 대안이 없을 때 CID/RID를 만든다. 단어 검색 0건은 신규성의 근거가 아니다.
- **context**: 신분·의도·진심·동의·친족·과거·미래·게임 상태 등은 문맥으로 유지한다. 다만 요청한 의미 자체를 지우거나 다른 장르로 약화하지 않는다.
- **defer**: 불충분한 출처·표본·native 증거·가시성이 있으면 구체 보류 사유를 남긴다. 보류는 원 어휘 삭제를 뜻하지 않는다.

예: `cand_d283…`는 자기 두 손의 깍지이므로 H07 두 사람 손깍지에 그대로 연결하지 않는다. `cand_ae856…`의 허리끈/클립/스타킹 경계는 재사용 우선이지만 원래 adult/primary 조건·한글 정보량·W17 두 끈의 개수 차이를 심사한다. `cand_522c…`는 OR/AND와 전달 행동의 한영 불일치를 고친다. 현재 source의 원뜻을 보존하지 못하면 별도 완결 대안이 필요하다.

## 4. 운영 source와 역할 심사

연구의 A/B/C와 그래프는 심사 메모다. 이를 frozen requester fact나 허용된 신체 접촉·동의·새 인물 생성 권한으로 쓰지 않는다. 실제 독립 core의 존재하는 owner와 정확한 property 경로에 bind한다. 모든 도입/변경 인물·소품·개수·의복 층·자세·접촉·시선·배경·카메라·매체를 intrinsic effects와 맞춘다. 빈 effects나 인용 URL은 보존 증거가 아니다.

현행 149-slot의 실제 명칭을 사용한다. 접촉은 `contact_point`, 신체 자세는 `body_pose`, 시선은 `gaze_target`, 의복 연결은 `garment_detail`, 몸/의복의 여유는 `garment_fit`, 겹침은 `wardrobe_layering`, 눈 구조/색은 `eye_detail`, 귀 신체 구조는 `species_marker`, 표면은 `surface_material`이 검토 출발점이다. 화면 속 패널은 `composition`/`object_structure`의 적합 속성인지 심사한다. 카드를 여러 role에 추천했다는 사실로 전 role을 일괄 승인하지 않는다.

필요한 기존 의복/사람/물건의 전제, source guard, 선택 branch, 전체 조건·효과·의무를 같은 CID/RID에서 검토한다. 다른 후보의 미선택 대안에서 사실을 빌리지 않는다. context를 direct로 승격하거나 discovery tag를 사실로 쓰지 않는다. 원문 전체의 positive field-local anchor와 native proof를 현재 도구로 따로 심사한다. 연구 graph/source hash는 그 proof를 대체하지 않는다.

## 5. source 검사와 인덱스

구현 직전 [현행 유지보수 문서](../../../../skills/photo-prompt-image-generator/references/maintenance.md)와 CLI 지원을 다시 확인한다. 조사 당시 다음 entrypoint/옵션이 실제 존재했다. 아래 명령은 이 연구에서 실행하지 않았다.

```sh
python3 skills/photo-prompt-image-generator/scripts/photo_installed_h_f2.py --check-runtime
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_shared_candidate_index.py --verify
```

현재 build는 `--output-assets`, `--runtime-store`, `--backend` 옵션을 지원한다. 검증된 최종 source union에서 별도 출력 경로로 build하고 활성 manifest를 먼저 옮기지 않는다. `--publish`는 실제 게시 단계에서만 사용한다. ID·전체 텍스트 hash·text recipe·provider/model·차원·vector integrity가 모두 일치하는 벡터만 재사용한다. 의미/영문/한글 변경분을 이전 벡터로 새 recipe인 것처럼 재표기하지 않는다.

먼저 후보/owner/역할/효과/조건에 영향을 받는 focused tests를 실행한다. 실패나 변경 범위가 새로운 회귀 위험을 보일 때만 범위를 확장한다. 전체 source/index closure·통계·문서/vector 범위와 native qualification을 별도 검증한다. 연구 validator의 PASS를 해당 검사로 대체하지 않는다.

## 6. 검색·선택 평가

90개 카드 파생 180질의와 36개 경계쌍 144질의, 총 **324개 개발 질의**가 있다. 검색은 미실행이다. 카드 문장을 그대로 쓴 개발 질의에는 데이터 작성과 겹치는 편향이 있다. 독립 holdout은 별도 작성자가 카드 문장을 보지 않고 자연어 요청을 작성하고 기대 관계·혼동 기준을 먼저 동결한 뒤 구성한다. 현재 holdout은 PENDING이다.

baseline과 stage는 같은 독립 요청, 같은 언어·slot 의미, 같은 전체 공통 pool에서 비교한다. 슬롯별 독립 candidate-free query, BM25F·실제 query embedding·cosine·RRF와 최종 CID/RID·rank·lane·source hash를 보존한다. 주제 전용 pool·slot 선필터·키워드 강제 승격으로 성능을 만들지 않는다.

평가를 **노출 → 실제로 허용되는 선택 → 최종 프롬프트의 전체 의미 보존 → 픽셀**로 나눠 기록한다. context 레코드의 positive visual 침투, 자기/상대 owner 교체, count/성별/매체 변경, 원치 않는 성적/폭력적 의미 추가를 각각 세어야 한다. 일반 집단·업무·운동·코스튬·장비 요청에서도 비교한다. 같은 소재 후보가 노출되는 것과 부적합한 구애/성적 의미를 채택하는 것은 별개다. 한국어/영어, 원 용어/자연어를 분리 보고한다.

## 7. 실제 이미지 검증

[PIXEL-PLAN.md](PIXEL-PLAN.md)의 12장면×baseline/stage=24장 비교를 첫 묶음으로 제안한다. 현재 생성·선택·전송·픽셀 검토는 모두 NOT_RUN이다. 각 요청의 정확한 envelope·독립 core·잠긴 의미·owner·최종 prompt·실제 선택·runtime receipt를 고정하고 같은 생성 환경을 사용한다. stage에만 임의로 길고 정밀한 사용자 요청을 주지 않는다.

명시된 필수 접점·개수·연결·틈·반사/화면 경계는 한꺼번에 판정한다. 일부만 성공하면 partial 실패, 숨거나 너무 작으면 판정 불가이며 PASS로 계산하지 않는다. 차단은 BLOCKED_UNSCORED로 남기고 의미를 바꿔 재시도한 결과를 같은 비교에 섞지 않는다. seed·모델 버전·비결정성이 통제되지 않으면 1쌍 결과에서 데이터의 원인 효과를 단정하지 않는다.

## 8. 완료 판정·활성화·복구

연구 → source 등록 → native qualification → index 무결성 → 검색 → 실제 선택/compose → 정확한 이미지 요청 전송 → 저장 픽셀 → 사용자 수용을 독립 상태로 기록한다. 앞 단계의 PASS를 뒤 단계에 복사하지 않는다. 중요한 관계 하나라도 실패한 케이스는 전체 장면 성공에 포함하지 않는다.

새 sealed generation과 설치본을 비활성 별도 경로에서 확인한 뒤 현재 사용 경로를 전환한다. assets 편집·인덱스 build 성공은 설치된 H-F2 변경을 뜻하지 않는다. 이전 generation·선택 config를 복구 가능하게 남기고 활성화에 문제가 있으면 이전 선택으로 복구하되 실패 증거를 보존한다.

후속 버전 관리가 요청되면 정확한 allowlist로 변경한 파일만 stage한다. 기존 dirty/deleted/untracked 작업을 정리하거나 섞지 않는다. 이번 연구는 commit/push/설치 활성화를 하지 않았다.
