# 플린트록 판타지 데이터 반영과 독립 이미지 시험

2026-10-23. 이 문서는 이미지 통합시험 시점의 소스 반영, 검색 검증, 실제 생성물 검토를 연결한다. 이후 Git 발행·병합 검증은 [PUBLICATION.md](PUBLICATION.md)에 별도로 기록한다. 원래 조사 내용은 [RESEARCH.md](RESEARCH.md), 카드별 반영 설계는 [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)에 있다.

**데이터 반영과 소스·인덱스 검증은 통과했다.** 독립 서브에이전트 세 개가 각각 다른 컨셉으로 첨부 사진을 실제 참조 입력에 넣어 한 장씩 생성했다. 공방 이미지에서는 격발부와 병 속 폭풍이 선명해 핵심 장르 표현을 확인했다. 다만 코디네이터의 엄격한 전체 복합 케이스는 **0/3 통과**다. 부품 경계, 화면 밖 총열, 손 접촉, 해자의 가려진 접점, 떠 있어야 할 도구의 고정 지지가 실패 원인이다. 이미지 생성 성공과 전체 의미 재현 성공을 구분한 결과다.

## 반영한 데이터

| 항목 | 결과 | 범위 |
|---|---:|---|
| 새 시각 후보 | 52 | 관찰할 수 있는 부품·재료·소유자·연결·장면 관계 |
| 새 문맥 진단 | 21 | 비시각적 의미와 혼동 경계. 긍정적 시각 후보로 취급하지 않음 |
| 슬롯 연결 | 99 | 실제 후보와 역할의 연결. 연결만으로 채택을 허가하지 않음 |
| 기존 후보 보강 | 5 CID / 6 카드 | 영어 원문의 관계를 한국어·검색문에 완전하게 보존 |
| 기존 후보 재사용 | 1 | 화장대·거울·문간·별도 침대의 기존 완전한 관계 |
| 보류 | 22 카드 | 상세 기구·표본의 도판 확인 전에는 새 긍정 후보로 등록하지 않음 |
| 의미 자료 | 102 카드 / 319 검색 경로 | 원본 관계 그래프, 출처, 관찰 한계, 혼동 사례, 평가 기준 |

반영 파일:

- [시각·문맥 후보](../../../../skills/photo-prompt-image-generator/assets/photo_candidate_flintlock_fantasy_20261023.json)
- [후보 연결](../../../../skills/photo-prompt-image-generator/assets/photo_candidate_flintlock_fantasy_bindings_20261023.json)
- [시각 의미 자료](../../../../skills/photo-prompt-image-generator/assets/photo_flintlock_fantasy_semantics_20261023.json)
- [스킬의 의미 해석 안내](../../../../skills/photo-prompt-image-generator/references/flintlock-fantasy-semantics.md)
- [카드별 실제 결정](integration-evidence/data-integration.json), [등록 검증](integration-evidence/registry-validation.json)

기존 후보는 높은 허리선, 대포 플랫폼·흉벽·개구부, 견장, 코트 안의 앞트임 조끼, 보루·해자·분리된 라블랭의 관계를 보강했다. 기존 조건·효과·출처와 영어 본문은 유지했다. 초기 반영 시 다섯 모듈의 비대상 부분을 원래 바이트와 대조한 [보존 증거](integration-evidence/source-preservation.json)가 있다. 다른 대화의 동시 변경은 되돌리지 않았다.

새 자료는 H-F2의 선택적 참고 재료다. 등록·출처 인용·관계 그래프는 typed native qualification이나 owner permission을 부여하지 않는다. `native_approval=false`와 비자격 상태를 유지했다. 장르 이름만으로 전쟁·계급·국적·유럽 복식·성적 의미를 강제하지 않는다.

## 출처 정정과 고정 시험판

독립 검토 중 F02 저장실 카드가 인용한 보루·글라시 자료는 화약고 저장을 뒷받침하지 않는다는 문제가 발견됐다. 현재 후보와 의미 자료의 근거를 [Fort Moultrie의 화약고 설명](https://www.nps.gov/places/1809-powder-magazine-in-fort-moultrie.htm), [Fort Point의 화약고 설명](https://www.nps.gov/places/000/powder-magazines-fort-point-tour.htm)으로 정정했다. 두 자료는 화약고와 통의 문맥을 뒷받침한다. 높인 목재 플랫폼 배치는 저작한 장면이며 보편적 역사 설계나 통 내용물의 증거로 삼지 않았다. 원래 조사 스냅샷 57개 출처는 보존했고 현재 자료는 59개다. 출처 이미지의 픽셀을 검토한 것으로 계산하지 않는다.

[정정 기록](integration-evidence/source-correction-F02.json)과 [현재 소스 적용 기록](integration-evidence/source-correction-application.json)에 변경 범위가 있다. 이미 봉인한 첫 시험판에는 이전 F02 메타데이터가 남아 있다. 세 이미지 시험 모두 F02를 제외했다. 해당 시험판을 현재 수정본 전체와 동일하다고 주장하지 않는다.

세 에이전트는 다음 동일한 설치판을 명시해 사용했다.

사용한 최신 [photo-prompt-image-generator 스킬](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/SKILL.md)의 본문 해시는 `f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089`다. 설치판 커널 코드 해시 `ec29f441dbfc26930e7f4fb71ced759bf5ae271e672176110b21d2a7f6c846ef`는 작업 시작과 현재 기본판에서 동일하다. 데이터 시험판만 명시적으로 고정했다.

- H-F2: `87ba6e2c8e0fbeabc22e20946ce4396a2f6d54c153f4c3e9bd5a3cdd079beaa5`
- native: `6616c889a59a1122a312897ea77fbe700c9e7c243b8c91b3a0952d45dc6d8c41`
- 기존 20,329 CID + 이번 73 CID = 20,402 CID, 긍정 후보 19,898개.
- 기존 코드와 임베딩 공간을 보존했다. 기존 벡터 19,841개를 재사용하고 실제 변경 문서 57개를 계산했다. [소스 검증](integration-evidence/canonical-source-validation.json), [인덱스 검증](integration-evidence/native-index-build.json), [설치 결과](integration-evidence/install-for-image-tests.json).
- 전역 기본 선택을 활성화하지 않았다. `CURRENT` 기록도 이번 설치에서 변경하지 않았다. 각 실행이 이 시험판을 명시하므로 다른 대화가 작업하는 기본 선택과 분리된다.

실제로 동시 작업 중 기본 generation은 변경됐으며, 이를 이번 확장의 기본 활성화나 시험판과의 동일성으로 간주하지 않았다. [기본 설정 관찰](integration-evidence/default-config-observation.json)에 작업 전후의 값과 코드 해시를 남겼다. 이번 반영 범위는 작업 소스·현재 소스 검색 인덱스·명시한 시험용 설치판이다.

작업 소스의 원래 인덱스와 설치판의 canonical 인덱스는 다른 표현이다. 벡터의 레시피 이름만 바꿔 섞지 않고 각각 해당 소스에서 검증한다.

## 독립 시험 설계

세 서브에이전트는 부모의 작업 내역을 넘겨받지 않고 시작했다. 공통 입력은 실제 사용자 요청, 참조 이미지, 이전 사용자의 주제 문구와 넓은 추첨 영역뿐이다. 각자 무작위 선택, 독립 초안, 코어, 검사 기준을 후보 검색 전에 고정했다. 서로의 프롬프트·후보 목록·이미지를 전달하지 않았다. 이후 공통 출처 오류 정정은 공유했으므로 완전히 눈가림한 실험으로 부르지 않는다. [고정 입력 기록](integration-evidence/independent-arms-before-retrieval.json).

| 시험 | 독립 컨셉 | 이번 새 후보 노출 | 프롬프트 사용 |
|---|---|---|---|
| A | 공방에서 권총 격발부와 병 속 작은 폭풍을 함께 살피는 장면 | B02 권총의 짧은 총열·굽은 손잡이·외부 격발장치 | 일반 구조의 `inspiration_only` |
| B | 해자 건너편의 불빛을 바라보며 신호등을 여닫는 성벽 위 전달자 | A01 부싯돌·물림쇠·프리즌·화약접시 | 일반 기계 구조의 `inspiration_only` |
| C | 공중에 떠 있는 황동 도구를 사용해 항구 신호 깃발을 수선하는 장면 | H08 작업자·구체·집게·별도 받침 관계 | 조건과 사물 관계가 맞지 않아 비채택 |

`inspiration_only`는 실제 노출된 원문에서 일반 속성을 참고한 기록이며 native 후보의 정식 채택·자격 통과가 아니다. C는 이미 고정된 수선 장면을 구체 검사로 바꾸거나 연령 조건을 사후 삽입하지 않았다. 새 데이터가 노출됐다는 사실과 새 데이터의 이미지 전달 성공을 구분한다.

첨부 사진은 세 실행 모두 실제 native 참조 입력으로 전달하며 얼굴 비례·짧은 검정 단발·앞머리의 외형 지침으로 사용한다. 정확한 신원·연령·성격을 추정하지 않는다. 프롬프트와 실제 생성 결과를 별도로 보존한다. 각 arm의 허용 이미지 호출은 1회이며, baseline/ablation 생성은 없다.

검사 기준은 생성 전에 고정했다. 모든 부품·끝점·접촉·갯수·연결이 함께 보여야 복합 기준을 통과한다. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`를 유지한다. 없는 이미지나 차단 결과는 `BLOCKED_UNSCORED`다. 정지 화면의 빛·공중 간격은 실제 점화 성공·정보 전달·마법의 인과관계를 증명하지 않는다. 사용자 평가는 별도 대기 상태다.

## 실제 이미지 및 검색 검증 결과

### 소스와 검색

이미지 통합시험 종료 시 작업 소스에는 동시 작업을 포함한 20,703 CID와 15,628 연결이 있다. 이 소스의 긍정 후보 20,111개에서 별도 인덱스를 재구성·완전 검증한 뒤, 현재 소스와 정확히 같은지 확인하고 836개 파일을 바이트 대조해 적용했다. 레이아웃은 `98f029cffe5ba23c420acd71f15ca754192e4083016db44c8846df45f1f00190`이다. 기존 샤드는 보존했다. [검증·적용 기록](integration-evidence/working-index-install.json).

그 뒤 실제 작업 디렉터리에서 정규 사전 검증기의 모든 소스·인덱스 검사를 실행했다. 결과는 `native_candidates=20703`, `bindings=15628`, `errors=[]`다. [최종 검증 출력](integration-evidence/dictionary-validation.final.json).

이번 73개 새 소스와 다섯 수정 소스가 현재 작업 파일에 정확히 남아 있고, 다섯 기존 소스의 조건·효과·출처·영어 본문은 보존됐음을 [최종 소스 대조](integration-evidence/source-preservation.final.json)에서 확인했다. 시험판과 현재 새 소스의 유일한 차이는 F02 출처 메타데이터 정정이다. 세 arm에 실제 노출된 A01·B02·H08은 시험판과 현재 자료가 같다. [시험 소스 대조](integration-evidence/image-tested-source-consistency.json).

고정한 첫 시험판으로 한국어·영어 226개 질의를 실행했다. 카드에서 만든 개발 질의 162개 중 등록 후보를 기대할 수 있는 것은 118개, 보류·문맥에 해당하는 것은 44개다. 등록 후보의 목표 CID는 **117/118개에서 상위 10위, 118/118개에서 상위 32위**에 나왔다. 유일한 상위 10위 밖 사례는 분리된 삼각형 라블랭을 묻는 영어 DEV-D06으로 16위였다. 혼동 경계 64개는 이전판과 새 판에서 각각 실행했고, 기존 상위 10개 교집합의 평균은 9.0625개였다. 64개 중 35개에서 새 후보가 상위 10개에 노출됐다. 이 노출을 곧 오탐이나 채택으로 계산하지 않았다. [전체 질의·결과](integration-evidence/retrieval-qualification.json).

이 수치는 소스에서 파생한 개발 검색의 도달성과 순위 자료다. 독립 holdout의 정확도, 혼동 질의의 수동 적합성, 새 후보가 없는 이전판 대비 의미 개선, typed native qualification, 이미지의 인과적 개선은 측정하지 않았다. F02의 이전 메타데이터도 이 고정 검색 스냅샷에 포함되며, 현재 정정본 전체의 검색 검증과 동일시하지 않는다.

### 이미지

실제 저장 이미지와 원본 해시를 기준으로 판정한다. 사전감사 통과를 픽셀 성공으로 대체하지 않는다.

| Arm | 실제 생성 | 기본 장면 기준: 에이전트 | 기본 장면 기준: 코디네이터 | 이번 새 소스의 전체 관계 |
|---|---:|---:|---:|---|
| A | 1회 | 5/6 | 5/6 | B02 실패, 개별 기준 1/3 |
| B | 1회 | 4/6 | 3/6 | A01 실패, 개별 기준 0/2 |
| C | 1회 | 3/5 | 3/5 | H08 비채택, 전달 시험 미실행 |

이번 새 후보를 프롬프트에서 참고한 두 실행의 완전한 소스 관계는 0/2 통과다. C의 유효한 비채택을 소스 채택 실패로 계산하지 않았다. 개별 기준 수가 다른 세 장면의 통과 비율을 하나의 일반 품질 지표로 합산하지 않는다. 재생성·baseline/ablation 생성은 모두 0회이며, 세 결과의 사용자 수용은 대기 상태다. [파일 무결성·참조 해시](integration-evidence/image-file-validation.json).

**A — 병 속 폭풍을 시험하는 공방**

[최종 프롬프트](image-test-evidence/a/authoring/final-prompt.txt), [사전 검사 기준](image-test-evidence/a/authoring/prospective_pixel_gates.json), [저장 이미지](/Users/chasoik/Projects/image-prompt/generated/photo-runs/flintlock-fantasy-20261023-a/returned-image.png), [코디네이터 독립 검토](integration-evidence/coordinator-pixel-review-a.json).

실제 참조를 첨부한 native 생성 1회가 성공했다. 1536×1024, SHA-256 `3719e798f46f1d7e48b211ecd150305d31e053af65dd4c1e0fa92338dfd6001e`다. 실제 모델은 응답에 없어 `unknown`이다.

참조 얼굴·단발, 부싯돌을 무는 물림쇠, 열린 프리즌, 별도 오목한 화약접시, 병 안의 작은 구름·번개가 선명하다. 손·시험 장치·불꽃·폭풍 병이 한 작업대 장면을 이뤄 **이번 장르의 핵심 표현은 확인했다.** 다만 오른손 손가락은 레버 뒤의 작업대 위에 펴진 상태 대신 레버 장치에 닿아 있고, 왼손과 병 지지 고리의 정확한 접촉도 완전하게 구별되지 않는다. 기본 5/6개 통과, 전체 케이스는 실패다.

B02의 세 소스 기준 중 외부 부싯돌 격발장치가 같은 총열 옆에 붙는 관계는 통과했다. 그러나 **총열 끝이 오른쪽 프레임 밖으로 이어져 완전한 짧은 총열의 형태와 갯수 조건을 확인할 수 없다.** 소스 기준은 1/3개 통과다. 보이는 총열이 하나라는 사실을 전체의 짧은 총열 조건 통과로 올리지 않았다.

[A 정식 검토 감사](image-test-evidence/a/authoring/review-audit-output.json)는 `record_valid=true`, `technical_qualification=fail`이다. 신체·배치 검토는 3개 통과·2개 실패로 기록됐다. 독립 장면 기준 5/6과 신규 B02 기준 1/3은 별도의 집계다.

**B — 성벽 위 신호 전달자**

[최종 프롬프트](image-test-evidence/b/final_prompt.txt), [사전 검사 기준](image-test-evidence/b/prospective_testcase.json), [저장 이미지](/Users/chasoik/Projects/image-prompt/generated/photo-runs/flintlock-fantasy-20261023-b/flintlock-signal-courier.png), [코디네이터 독립 검토](integration-evidence/coordinator-pixel-review-b.json).

실제 참조를 첨부한 native 생성 1회가 성공했다. 1536×1024, SHA-256 `b90bb01d7658b9cab040d53fd6a24b31f8d7f483190c4e50c9f7f70748863de2`다. 실제 모델은 응답에 없어 `unknown`이다.

참조 외형, 등불을 지지하고 문틀에 닿는 손, 가까운 등불과 반대편 탑의 별도 불빛은 확인했다. 그러나 **부싯돌과 금속 물림쇠의 경계, 별도 화약접시가 명확하지 않고, 앞쪽 흉벽이 가까운 벽 바닥·물 접점을 가린다.** 따라서 격발부와 해자 양안의 복합 기준은 부분 관찰로 실패다. A01의 두 신규 소스 관계도 0/2 통과다. 프롬프트 참고가 실제 부품 관계의 완전한 재현으로 이어지지는 못했다.

장면 전체는 해질녘 성곽 인물 사진으로 설득력이 있다. 마법 기준은 검토자 간 차이를 그대로 남겼다. B 에이전트는 빛나는 원판과 무늬 투사를 통과로 봐 기본 4/6개를 통과시켰다. 코디네이터는 같은 사전 기준에서 일반 역광·구멍을 통한 투사와 초자연적 전달 매체를 충분히 구별할 수 없다고 보아 부분 관찰로 판정했다. 코디네이터 기본 판정은 3/6개 통과다. 두 검토 모두 전체 케이스와 A01 전달은 실패이며, 기준이나 이미지를 바꾸지 않았다.

[B 실행 요약](image-test-evidence/b/arm-result-summary.json)의 정식 검토 기록은 유효하고 신체 동작 5개 항목은 통과했다. 그 범위의 `technical_qualification=pass`가 이번 격발부·해자 연구 케이스 통과를 뜻하지는 않는다.

**C — 항구의 깃발 수선**

[최종 프롬프트](image-test-evidence/c/final-prompt.txt), [사전 검사 기준](image-test-evidence/c/prospective-testcase.json), [저장 이미지](/Users/chasoik/Projects/image-prompt/generated/photo-runs/flintlock-fantasy-20261023-c/images/flintlock-harbor-mender-native.png), [코디네이터 독립 검토](integration-evidence/coordinator-pixel-review-c.json).

실제 참조를 첨부한 native 생성 1회가 성공했다. 원본은 1237×1272이며 SHA-256은 `ac84a6196cba686ee0383076784ec52335898c055d98b188f22420ad86f0af3d`이다. 도구 응답에 모델명이 없어 실제 모델은 `unknown`으로 남겼다.

햇빛이 드는 항구의 수선대, 인물의 얼굴과 짧은 단발, 깃발 패치와 바느질, 기다리는 무장 인물의 관계는 읽힌다. 얼굴·민간 노동·수선 접촉은 통과했다. 원본 크기의 부분 화면을 원본 픽셀과 대조해 실과 바늘의 접촉을 확인했다. 그러나 **황동 집게의 수평 팔이 오른쪽 고정 기둥에 연결되어 있어 공중 부양 기준은 실패**다. 외부 물림쇠·세워진 강철 부품은 보이지만 별도 화약접시 경계가 명확하지 않아 격발부 복합 기준도 부분 관찰로 실패했다. 픽셀 기준 3/5개 통과, 전체 케이스는 실패다. H08은 생성 전에 비채택했으므로 새 후보의 프롬프트→픽셀 전달은 시험하지 못했다.

[C 정식 검토 감사](image-test-evidence/c/review-audit-result.json)는 `record_valid=true`, `technical_qualification=fail`이다. 유효한 실패 기록이며 사용자 수용은 `pending`이다.

## 다음 데이터 반영 원칙

1. 생성 결과에서 부품이 뭉개지거나 손·도구 연결이 모호하면 해당 기준을 실패로 남긴다. 그 결과만으로 후보 자체의 출처 정확성이 틀렸다고 단정하지 않는다.
2. H08처럼 장면·소유자·조건이 맞지 않는 자료는 강제 채택하지 않는다. 별도 요청에서 그 완전한 장면이 실제로 필요할 때 독립 코어를 작성하고 평가한다.
3. 22개 보류 카드는 기관의 실제 표본·도판을 검토한 뒤 위치·갯수·부품 경계를 확정하고 필요한 후보만 등록한다. 이번 세 이미지가 그 도판 검토를 대체하지 않는다.
4. 검색 개발 질의와 혼동 경계 질의의 결과는 노출·재현성 자료로 사용한다. 독립 holdout이나 이미지 품질의 인과적 개선으로 주장하지 않는다.
5. 전역 기본판 갱신이나 배포는 이번 변경·동시 소스의 합집합에서 새 검증을 거친 별도 단계다. 이미지 통합시험 당시에는 커밋·푸시·PR을 만들지 않았다. 후속 발행은 [PUBLICATION.md](PUBLICATION.md)에 기록한다.

관찰된 실패를 다음 평가에 사용할 때는 아래처럼 장면의 관찰 가능성을 먼저 개선한다. 아래 제안은 아직 새 이미지를 생성해 검증한 결과가 아니다.

| 관찰된 문제 | 다음 장면 설계 | 유지할 통과 조건 |
|---|---|---|
| 작은 격발부에서 돌·금속·화약접시 경계가 합쳐짐 | 얼굴과 장면을 유지하면서 해당 격발부가 전경에서 충분한 원본 픽셀을 차지하도록 거리·측면 각도·초점면을 조정 | 동일 총기의 부품과 연결을 한 화면에서 모두 구별 |
| 흉벽이 가까운 벽·물 접점을 가림 | 두 벽의 바닥 접점과 그 사이 물을 동시에 볼 수 있는 관찰 위치부터 정함 | 가까운 접점·먼 접점·연속된 물 구간을 함께 확인 |
| 떠 있는 도구가 고정 장치로 바뀜 | 집게 주변 공기 간격과 천의 장력이 함께 보이는 단순한 배치를 계획 | 접촉·간격·장력 및 전체 지지 관계 확인. 푸른 무늬만으로 통과시키지 않음 |
| 새 후보가 현재 장면의 조건·소유자와 맞지 않음 | 그 후보의 완전한 작업이 필요한 별도 요청에서 독립 코어와 검사를 설계 | 기존 장면의 나이·사물·행동을 사후 바꾸지 않고 정당한 조건을 먼저 확보 |

## 재현과 최종 상태

[최종 검증 묶음](integration-evidence/FINAL-VERIFICATION.json)은 세 실행의 frozen core 유지, exact prompt와 ledger의 일치, 참조 해시, 저장 이미지 해시, 이미지 호출 각 1회, `review_record_validated` 상태를 대조한다. [최종 소스·인덱스 신선도](integration-evidence/final-source-index-freshness.json)는 완전 검증 당시 소스 90개 파일 및 적용한 인덱스 포인터와 현재 파일의 바이트 일치를 확인한다.

환경 재시작으로 중단된 소스 인덱스 빌드·검색 평가와 미완료 사전감사만 복구했다. 생성 전에는 ledger·작업 상태·실행 중 프로세스를 확인해 미호출을 검증했고, 실제 이미지 생성은 이후 각 한 번씩만 수행했다. task 소유의 중단된 staging revision만 복구했으며 다른 작업의 프로세스나 소스는 중지·초기화하지 않았다. [자원 순서·복구 기록](integration-evidence/resource-sequencing.json), [staging revision 복구](integration-evidence/working-index-abandoned-revision-recovery.json).

소스·인덱스 반영 및 명시한 시험용 설치판 사용은 완료했다. 이미지 통합시험 종료 시에는 전역 기본판 활성화, 커밋, 푸시, PR, 배포를 실행하지 않았다. 후속 Git 발행 상태는 [PUBLICATION.md](PUBLICATION.md)를 따른다. 세 이미지의 실제 모델명은 응답에서 관측되지 않았고, 사용자 수용 판단은 받지 않았다.

생성 이미지와 원본 참조는 로컬 전달 결과로 보존하며 Git에 추가하지 않았다. 저장소의 `image-test-evidence/`에는 실제 프롬프트, 고정 기준, 판정, 감사 및 해시 증거를 보존했다.
