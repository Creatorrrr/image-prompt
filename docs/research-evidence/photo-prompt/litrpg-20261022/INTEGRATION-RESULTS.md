# LitRPG 데이터 반영과 독립 이미지 검증

2026-10-22~23 KST. 연구의 78개 의미 카드와 297개 어휘 경로를 운영 소스와 설치 검색 버전에 반영했다. 시각 실현 60개, 문맥/연속 증거 진단 18개, 선택적 바인딩 128개다. 최신 스킬을 사용하는 독립 서브에이전트 3개가 첨부 사진을 실제 전달해 각 1회씩 이미지를 생성했다. 공원·공방의 핵심 LitRPG 관계는 통과했고 광산의 전체 전술 관계는 부분 실패했다. 정확한 동작·끝점까지 포함한 전체 사전 테스트는 **0/3 통과**다. 실패를 보존하고 재생성하지 않았다.

## 실제 변경 범위

- `assets/photo_litrpg_system_semantics_20261022.json`: 의미·출처·한계·전체 원문 반영 판단.
- `assets/photo_candidate_litrpg_system_20261022.json`: 완전한 양언어 시각 실현과 진단 78개.
- `assets/photo_candidate_litrpg_system_bindings_20261022.json`: 실제 catalog 슬롯에 맞춘 128개 바인딩.
- `assets/photo_candidate_corpus_manifest.json`: 위 두 모듈만 추가. 다른 기존 모듈·조건·효과·정책·바인딩은 보존.
- `references/litrpg-system-semantics.md`와 `references/maintenance.md`: 매체·소유자·표시 내용·인지·시간 증거 구분.
- `retrieval-runtime.json`: 검증된 새 설치 세대를 선택.

경로의 기준은 `skills/photo-prompt-image-generator/`이다. 검색 코드와 임베딩 모델을 이번 변경에서 수정하지 않았다. 원전/typed native 적격성은 미승인 상태를 유지한다. 연구 그래프는 조건·권한·사실을 생성하지 않는다.

## 원문과 설치 스냅샷을 구분한 검증

아래 작업 원문의 수와 보존 검사는 이번 반영 시점의 기록이다. 독립 실험 이후 공유 manifest·maintenance에 다른 추가 변경이 관찰됐으며, 이를 되돌리지 않았다. LitRPG 전용 파일과 설치 config는 그대로이고 manifest의 두 LitRPG 모듈 등록도 각각 정확히 1개 유지된다. [최종 hash 관찰](integration-evidence/FINAL-SOURCE-HASH-OBSERVATION.json)에 이를 분리했다. 세 런의 고정 설치 세대는 바뀌지 않았다.

| 대상 | 이전 | 반영 후 | 검증 |
|---|---:|---:|---|
| 작업 원문 레코드 | 19,813 | 19,891 | 기존 19,813개 전체 레코드 보존 |
| 작업 원문 바인딩 | 14,287 | 14,415 | 기존 14,287개 보존, catalog·policy 보존 |
| 시작 시점 설치 원문 | 19,801 | 19,879 | 기존 설치 원문 전체 보존, 신규 78개 추가 |
| 설치 양성 CID | 19,438 | 19,498 | 진단을 양성 검색에 추가하지 않음 |
| 설치 양성 RID | 19,440 | 19,500 | 전체 source·index·vector·실행 proof 검증 |

작업 원문에는 시작 시점 설치 버전에 없는 다른 작업의 12개가 있었다. 이번 설치는 시작 시점의 검증된 설치 버전과 LitRPG 변경만으로 구성했으며, 다른 작업의 미발행 12개를 함께 활성화하지 않았다. 그 12개를 작업 원문에서 삭제하거나 바꾸지도 않았다. 따라서 작업 원문 수와 설치 수가 다른 이유를 신규 데이터 누락으로 해석하지 않는다. LitRPG 78개는 양쪽에 완전히 포함된다.

새 H-F2 세대는 `ef02180fc06f390a079ecb7727ece11c2dd30e54394f9e1ae8b9112217bd29ac`, native 세대는 `f3d402db654117a13c83f52df5228ccafdc93969b606550cd88f4f747c751b57`이다. 설치·실행 recorder 확인이 통과했고 default config를 활성화했다. 기존 CURRENT는 쓰지 않았다. 이전 세대와 기존 런은 보존했다.

native index에서는 기존 벡터 19,438개를 재사용하고 신규 60개를 로컬 모델로 계산했다. H-F2 문서 벡터도 기존 19,440개를 그대로 재사용하고 신규 60개를 로컬에서 계산했다. 원격 임베딩 API를 사용하지 않았다. local execution과 원문·vector hash 검증을 유지했다. Python의 큰 비순환 JSON 검증에서 cyclic GC를 비활성화한 실행 설정을 기록했으며, 원래 deployed validator와 모든 assertion은 그대로 수행했다. 검증을 생략하거나 kernel을 바꾸지 않았다.

## 검색 평가

기록은 [retrieval-qualification.json](integration-evidence/maintenance/retrieval-qualification.json)과 질의별 실행 증거에 있다. 개발용 48개를 현재 설치된 전체 양성 풀에서 실제 검색했다.

| 구분 | 질의 수 | 관찰 |
|---|---:|---|
| 개발 양성 | 12 | 지정 후보 상위 10개 이내 노출 |
| 무키워드 양언어 | 12 | 지정 후보 상위 10개 이내 노출 |
| 근접 음성 | 12 | 결과 보존; 노출을 자동 채택 오류로 간주하지 않음 |
| 일반 장면 | 6 | 신규 후보 상위 10개 노출 0건 |
| 비시각 문맥 경계 | 6 | 결과 보존; 진단은 양성 검색 외부에 유지 |

24/24는 소스와 함께 설계한 개발 질의의 목표 CID 노출이다. 독립 holdout·실제 managed sampling·전체 정밀도/재현율·원전 적격성·이미지 품질 개선을 입증한 수치는 아니다. baseline 검색은 실행하지 않았으며 신규 CID가 이전에 없었다는 사실로 성능 향상을 계산하지 않았다. 개별 관리 런의 노출과 실제 사용은 이미지 실험과 함께 별도로 보고한다.

관련 source context·primary proof·sampling 회귀 검사 68개가 통과했다. 초기 연구의 24개 검사 결과는 당시 연구 단계의 기록이며 현재 운영 반영 상태와 혼동하지 않는다.

## 독립 실험 설계

세 child는 `fork_turns=none`으로 시작했고 다른 arm의 prompt/pack/image를 받지 않았다. 각각 현재 스킬과 허용 중립 파일, 사용자 실제 요청, 같은 사진만으로 독립 난수 컨셉과 baseline을 작성한 뒤 core를 동결했다. 기본 제어는 각 resolver의 saved 값 sensual=1, fetish=0, creativity=1, surreal=0이며 override를 주입하지 않았다.

| arm | 독립 컨셉 | 런 |
|---|---|---|
| A | 미완의 뿌리 제거 작업 앞 공원 관리원의 개인 자원·기술 상태 | `generated/photo-runs/litrpg-20261022-arm-a/` |
| B | 유리공예사의 랜턴 바이알 감정과 거래 | `generated/photo-runs/litrpg-20261022-arm-b/` |
| C | 소금광산 던전에서 카드 선택과 경로 유인·통과 | `generated/photo-runs/litrpg-20261022-arm-c/managed/` |

coordinator envelope는 dispatch 직후, 모든 child init/core 이전에 작성됐다. 실제 사용자 원문 provenance는 지켰으나 스킬의 pre-dispatch 생성 순서까지 준수했다고 주장하지 않는다. children은 task brief를 requester text로 만들지 않았다. C의 첫 slot 준비에서 잘못된 슬롯명과 전체 scope 바인딩이 생겨 검색 전 별도 관리 런으로 같은 authoring 입력을 다시 동결했다. 실패 기록과 정상 런을 모두 보존한다. `prepare-slot-intents`에 pin 인자가 없다는 CLI 차이로 거절된 호출도 보존하고, 실제 첫 retrieve에서 같은 generation/store를 명시했다.

첨부 사진은 외형 참고로만 사용했다. 실제 인물의 나이·성격·동의·허구적 이력을 판단하지 않는다. 생성 입력의 `referenced_image_paths`에 실제 첨부 경로가 있고, 세 ledger/manifest의 참고 사진 SHA-256은 모두 `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`이다. 세 런이 사용한 현재 `SKILL.md` SHA-256은 `f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089`로 동일하다. 이미지 모델의 구체적 이름/버전은 도구가 반환하지 않아 추정하지 않았다.

## 실제 원본의 픽셀 판정

서브에이전트의 원본 리뷰와 coordinator의 원본 직접 관찰을 교차 확인했다. coordinator는 child의 관찰을 전달받았으므로 맹검 리뷰라고 주장하지 않는다. 생성 전 게이트 hash는 변경되지 않았다. 프롬프트 export 파일은 실제 payload 문자열에 마지막 줄바꿈 한 개만 추가한 파일이며 두 hash를 따로 저장했다.

| arm | 같은 원본에서 확인한 주제 표현 | 엄격한 실패 근거 | 전체 판정 |
|---|---|---|---|
| A 공원 관리원 | `GARDENER LV 12`, `STAMINA 8/100`, 짧은 바, `ROOTBREAK 00:42`; 패널-손목 연결과 시선; 쉬는 인물·지면의 도구·남은 뿌리 모두 보임 | 지정한 왼손 도구/오른팔 무릎 대신 오른손 도구/왼팔 무릎으로 좌우가 반전 | FAIL, 6개 중 5개 통과 |
| B 유리 공방 | 바이알과 연결된 아이템 평가, 제작자 `GLASSCRAFT Lv.7`/`XP 84/100`, 구매자 지불; 같은 카드의 이름·속성 행·별도 `CHARGE 6/6` 블록 | 생성 전 검토한 엄지·검지의 넓은 받침 지지가 하부 몸통을 감싸는 접촉으로 변경 | B1–B5 PASS, 신규 구조 B6 PASS, 정확한 관리형 접촉 FAIL → 전체 FAIL |
| C 광산 탐험 | 선택 카드와 미사용 카드 두 장, `ECHO STEP`, `MP 0/2`, 카드-청록 선-왼쪽 발자국, 두 통로 | 감시자의 머리/나팔이 같은 발자국을 향하는지 불명확; 앞쪽 부츠가 하단에 잘려 문턱 통과와 양발 지지가 비관측 | FAIL, 5개 중 3개 통과 |

A의 동작은 물리적으로 자연스럽지만 사전 지정한 좌우가 다르다. B의 일반 접촉과 지지도 자연스러워 B5는 통과한다. 정확한 받침 접촉만 별도 관리형 게이트에서 실패하며 같은 결함을 일반 물리 오류로 중복 계산하지 않았다. C는 핵심 관계 끝점 자체가 빠졌으므로 카드·수치가 보인다는 이유로 전체 전술 관계를 통과시키지 않았다.

정규 리뷰 기록 검사는 세 런 모두 `record_valid=true`로 통과했다. 이는 기록 형식과 증거 바인딩의 유효성이다. 세 런의 `technical_qualification=fail`과 전체 픽셀 실패를 대신하지 않는다. 실제 호출 3회, 반환 원본 3개, 재시도 0회이며 원본·ledger·manifest·봉인 native plan의 hash를 대조했다. B는 결과 기록 호출의 잘못된 skill SHA를 올바른 동결 SHA로 복구했고, 이미지 호출은 늘리지 않았다. A의 결과 기록 필수 인자 누락 복구도 같은 원본의 기록 작업이다.

| arm | 원본 / 프롬프트 / 사전 케이스 / 리뷰 |
|---|---|
| A, 1312×1199 | [원본](/Users/chasoik/Projects/image-prompt/generated/photo-runs/litrpg-20261022-arm-a/image.png) · [프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/litrpg-20261022-arm-a/final-prompt.txt) · [사전 케이스](/Users/chasoik/Projects/image-prompt/generated/photo-runs/litrpg-20261022-arm-a/testcase-preimage-final.json) · [리뷰](/Users/chasoik/Projects/image-prompt/generated/photo-runs/litrpg-20261022-arm-a/litrpg-pixel-review.json) |
| B, 1448×1086 | [원본](/Users/chasoik/Projects/image-prompt/generated/photo-runs/litrpg-20261022-arm-b/generated-original.png) · [프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/litrpg-20261022-arm-b/final-prompt.txt) · [사전 케이스](/Users/chasoik/Projects/image-prompt/generated/photo-runs/litrpg-20261022-arm-b/registered-scene-testcase.json) · [리뷰](/Users/chasoik/Projects/image-prompt/generated/photo-runs/litrpg-20261022-arm-b/scene-pixel-review.json) |
| C, 1374×1145 | [원본](/Users/chasoik/Projects/image-prompt/generated/photo-runs/litrpg-20261022-arm-c/image-original.png) · [프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/litrpg-20261022-arm-c/final-prompt.txt) · [사전 케이스](/Users/chasoik/Projects/image-prompt/generated/photo-runs/litrpg-20261022-arm-c/testcase-precall.json) · [리뷰](/Users/chasoik/Projects/image-prompt/generated/photo-runs/litrpg-20261022-arm-c/pixel-testcase-review.json) |

집계 증거는 [IMAGE-TEST-SUMMARY.json](integration-evidence/IMAGE-TEST-SUMMARY.json), 루트의 직접 관찰은 [ROOT-PIXEL-REVIEW.json](integration-evidence/ROOT-PIXEL-REVIEW.json)에 있다. `finalize_image_evidence.py`는 바이트·설치 세대·참고 사진·프롬프트·사전 게이트 일치를 검증하며 시각 판단을 자동 계산하지 않는다.

## 신규 데이터가 실제 기여한 범위

| arm | 반환 occurrence / 런 내 고유 원문 | 신규 노출 | 최종 사용 | 실제 픽셀 증거 |
|---|---:|---|---|---|
| A | 32 / 30 | 0 | 신규 0, 기존 깊이 표현 1개를 일반 영감으로 사용 | 핵심 게임 시스템은 검색 전 독립 baseline에 이미 존재 |
| B | 32 / 32 | I01 1개 | 머리글·속성 행·현재/최대 자원 블록을 일반 정보 구조 영감으로 사용 | B6의 완전한 같은 카드 구조와 `CHARGE 6/6`이 선명하게 구현됨 |
| C | 40 / 40 | Q11 1개 | 미사용. draw/hand/discard 완성 대안을 비교한 뒤 다른 관계와 경쟁한다고 판단 | 원본을 Q11의 draw/discard 구현 증거로 계산하지 않음 |

I01 CID는 `cand_821f6992d66a5e5bbc1fc22ad7ac9191`, Q11 CID는 `cand_e4cb826520795860bac4494c97427c1c`다. 세 런 모두 `chosen_visual_concept_ids=[]`, native 전체 원문 채택은 0개다. 선택적 후보를 억지로 채택할 할당량은 부과하지 않았다. 노출·완성 대안에서의 실현 가능성·선호에 따른 선택·최종 일반 영감·픽셀 생존을 분리했다.

데이터 등록과 실제 사용 경로는 확인했다. 그러나 세 장 중 신규 데이터의 보존된 의미가 직접 보이는 것은 B의 I01 구조이며, A/C까지 신규 데이터의 성공 사례로 합산할 수 없다. 동일 조건의 baseline 이미지가 없어 **데이터 추가가 이미지 품질을 인과적으로 향상시켰다는 결론은 미입증**이다. 정지 화면의 수치·거래·시선은 표시와 현재 배치의 증거이며 실제 자원 감소, 기술 실행 이력, 구매자의 마음 변화나 감시자가 돌아선 시간적 인과는 입증하지 않는다. 사용자 수락도 아직 받지 않았다.

## 후속 개선 우선순위

현 단계에서 새 의미 카드의 오류로 확인된 것은 없다. 관찰된 문제는 정확한 동작 지정과 복잡한 관계를 프레임 안에 보존하는 생성 단계에 있다. 다음 회귀에서는 A의 좌우 표현을 인물 기준/화면 기준으로 함께 명시하고, B의 넓은 받침과 손가락 접촉을 크게 확보하며, C의 앞쪽 부츠·문턱·나팔 방향을 동시에 볼 수 있는 더 넓은 시점을 우선한다. 이때 기존 실패 원본과 사전 기준을 유지하고 별도 런으로 비교해야 한다. 이번 실험의 결과를 바꾸는 재생성은 하지 않았다.

커밋·push는 수행하지 않았다. 다른 작업의 원문·공유 파일 추가 변경과 이전 설치 세대는 보존했다.

최종 정리에서 임시 설치 준비본과 실제 설치본의 비캐시 파일 5,073개를 대조해 누락/차이 0개를 확인했다. 이후 이번 작업의 중복 build/staging 디렉터리 3개만 제거했다. 새·이전 설치 세대, 생성 원본, 모든 arm의 증거, 재생성 스크립트와 검증 결과는 유지했다. [대조](integration-evidence/maintenance/staged-installed-comparison.json)와 [정리 범위](integration-evidence/maintenance/build-cleanup.json)에 기록했다.
