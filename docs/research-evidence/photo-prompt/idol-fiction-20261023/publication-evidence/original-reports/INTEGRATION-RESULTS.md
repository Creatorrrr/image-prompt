# 아이돌물 데이터 반영 결과

2026-10-23 KST. 최초 연구 패키지의 미실행 표시는 당시 스냅샷이다. 이 문서는 그 후 실제 등록·설치·검색 결과이며, 이미지는 `IMAGE-TEST-RESULTS.md`에서 별도 판정한다.

## 실제 등록

| 구분 | 추가 | 처리 |
|---|---:|---|
| 완전한 한영 시각 선택 명제 | 120 | positive visual_option |
| 시간·역할·맥락 구별 | 45 | diagnostic, positive 검색 제외 |
| 선택형 역할 binding | 219 | 기존 역할 정책 보존 |
| 원문 용어별 연결 | 325 | 자문용 경로; 강제 활성화 없음 |
| 추가 출처 보류 | 9주제·46용어 | 보류 유지 |

범위는 의상24, 콘셉트16, 제스처14, 팬 상호작용12, 외형12, 훈련10, 무대10, 카메라10, 어두운 서사5, 가상 퍼포머3, 장비2, 일본 공연 맥락2다. 인물·손·의복·장비·거울상·화면 속 인물의 소유와 연결 끝점을 문장 전체로 보존했다. 정지 이미지로 라이브 가창·인기·실제 연애·반복 행위·성공 이력·시간 순서를 확정하지 않는다.

추가 작업 소스:

- `skills/photo-prompt-image-generator/assets/photo_candidate_idol_fiction_20261023.json`
- `skills/photo-prompt-image-generator/assets/photo_candidate_idol_fiction_bindings_20261023.json`
- `skills/photo-prompt-image-generator/assets/photo_idol_fiction_semantics_20261023.json`
- `skills/photo-prompt-image-generator/references/idol-fiction-semantics.md`

앞의 두 모듈을 corpus manifest에 등록하고 maintenance 문서에 연결했다. `integrate_data.py`는 이미 등록된 상태에서 재실행을 거부한다. 첫 시도의 미지원 조건명 오류는 `integration-evidence/failed-source-attempt/`에 보존했고, 지원되는 `requires_adult_context`로 수정한 후 성공했다. source 등록은 native 의미·역할 자격 승인이 아니다. 그런 승인이나 typed fact를 만들어 넣지 않았다.

## 보존과 설치

등록 트랜잭션에서 기존 후보21,252개와 binding16,069개, catalog와 policy를 그대로 유지했다. 당시 작업 소스는 등록 후 후보21,417개·binding16,288개다. 구조8개 점검과 dictionary validator가 통과했다.

기존 설치 후보21,075개 전부와 코드·벡터·정책을 보존하고 이번165개만 더한 별도 설치 후속 버전을 만들었다. 설치 후 후보21,240개, positive CID20,388개·검색 RID20,390개다. 기존 검증 코드 SHA `ec29f441dbfc26930e7f4fb71ced759bf5ae271e672176110b21d2a7f6c846ef`는 그대로다. 이번 작업 외의 미게시 작업 소스를 함께 설치하지 않았다.

설치·완전 검증·기본 설정 활성화가 통과했다. `CURRENT` 쓰기0회이며 기본 설정은 전용 installer로 갱신했다. 세 이미지 실험은 아래 버전에 고정했다.

```text
store: /Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed
generation: 1d1802f68050e7c3034b0a4f55d3d3221575e81e343ee1433f2229225878d138
native: a96224b17d1d894276583b0602462e39b3cde4bb80be8a35e0f2c58a956c894d
```

종료 직전 다른 작업이 기본 버전을 `1d3013b5e422e72eb80bdd75189ebe25575ffa92aecc3378ed8ba79358b897bd`로 갱신했다. 새 기본 버전에서도 이번165개 후보와219개 binding이 원문 그대로 유지됐고 코드 SHA도 동일함을 확인했다. 원래 이미지/검색 실험의 고정 버전을 바꾸거나 새 기본 버전의 검색 순위까지 같은 결과라고 간주하지 않았다. 후속 기본 버전 확인은 `integration-evidence/later-default-source-check.json`과 `later-default-validation.json`에 있다.

작업 소스 인덱스의 빌드 자체 검증도 후보21,417개·positive20,515개로 통과했다. 이후 동시 작업이 기존 candidate shard들과90개 추가 레코드를 변경하여, 나중의 작업 소스 인덱스 재검증은 source digest 불일치로 실패했다. 그 변경을 덮어쓰거나 되돌리지 않았다. 동시 변경 이후 전체 작업 트리의 최종 index 일치까지 검증했다고 주장하지 않는다. 이번 이미지 테스트가 고정한 독립 설치 버전은 완전 검증을 통과했다. 해시 차이는 `integration-evidence/concurrent-source-drift.json`에 보존했다.

## 실제 검색 점검

전체 positive pool에서 질의별 BM25F1회·로컬 cosine1회를 실행했다. 같은 모델·query 벡터로 대조·시간 문맥28개는 이전 설치 버전도 실행했다. 총76개는 카드 작성자가 만든 개발 질의이며 독립 holdout이 아니다.

| 질의 | 수 | 기대 선택지 top8 | top32 |
|---|---:|---:|---:|
| 한영 positive | 40 | 35/40 | 40/40 |
| 한국어 positive | 20 | 17/20 | 20/20 |
| 영어 positive | 20 | 18/20 | 20/20 |
| 조합 | 8 | 하나 이상6/8 | 하나 이상8/8, 전부5/8 |
| 대조 | 20 | 정답 recall로 채점하지 않음 | 전후 결과 보존 |
| 시간·문맥 | 8 | 정답 recall로 채점하지 않음 | 전후 결과 보존 |

45개 diagnostic은 모든 검색 결과의 positive population에서 제외됐다. 위 수치는 선택형 원문의 노출 지표다. 문장 전체 적합성·동시 조합·채택·native 승인·픽셀 품질·인과적 개선을 뜻하지 않는다. 조합 M02처럼 두 원문이 같은 손을 요구하면 함께 검색되어도 그대로 동시 채택할 수 없다.

대조·시간 질의28개의 top1도 읽었다. 중앙 배치·트로피 집단·단체 팔 배열에는 관련 새 선택지가 노출되지만, 요청에 없던 인원수·배치를 추가할 근거는 아니다. `걸크러시 룩`, `지뢰계 리본 의상`, `헤드셋 쓴 가수`, `립싱크·백킹 트랙`의 상위 결과에는 무관하거나 의미가 부족한 원문이 남는다. `군무의 정밀 타이밍`에서 정지된 팔 배열이 검색되어도 타이밍을 증명하지 못한다. 이28개를 일괄 의미 PASS로 처리하지 않았다. 장르 단축어 검색과 오디오·시간 구별은 후속 개선 대상으로 남긴다.

## 이번 실행이 드러낸 후속 반영 우선순위

1. **실제 선택 경로의 의미 자격 검토.** 세 독립 실행에 노출된 신규11개 source부터 전체 한영 원문·주체·소유·조건·효과를 직접 검토한다. 필요한 native 의미/역할 증거를 실제로 갖춘 경우에만 자격을 추가한다. 등록 해시·연구 카드·출처 URL만으로 승인하지 않는다. 자격 확보 뒤에도 frozen core와 맞지 않으면 선택하지 않는다.
2. **조합 가능한 관계 단위 보강.** 거대한 장면 전체를 끼워 넣기 어려운 경우, 원문을 임의로 잘라 채택하는 대신 독립적으로 완결된 관계 명제를 새 source로 작성한다. 예컨대 장비 접촉·화면 경계·가시적 큐의 소유를 각각 완결시키되, 원 source와 ID·provenance를 보존한다. 같은 손을 요구하는 대안의 충돌도 유지한다.
3. **짧은 장르 질의의 발견성 보강.** `아이돌물` 단독 질의와 걸크러시·지뢰계 등 현재 부족한 한국어 질의를 별도 검토한다. 동의어로 뭉개지 않고 가능한 표현과 의미 경계를 함께 기록한다. 발견용 query/label 개선이 사용자 의미나 필수 장면을 자동 확장하지 않도록 한다.
4. **새로운 독립 평가.** 이번76개 개발 질의와 세 이미지 장면은 회귀 평가로 보존한다. 이를 다시 독립 holdout으로 부르지 않는다. 다음에는 source 내용을 보지 않은 작성자가 만든 새 질의·새 장면으로 선택/소유 관계와 픽셀 재현을 확인한다.
5. **정지 이미지의 한계 유지.** 오디오·타이밍·반복 행위·실제 이력은 계속 별도 증거로 남긴다. 정지 포즈나 장비가 나타난 것을 그 사실의 성공으로 치환하지 않는다.

위 항목은 이번 결과에 근거한 다음 단계 계획이다. 이번 등록에서 native 자격 확보나 새 독립 holdout까지 완료한 것으로 해석하지 않는다.

## 증거

- `integration-evidence/data-integration.json`, `scoped-source-validation.json`, `dictionary-validation.log`
- `generated/photo-runs/idol-fiction-20261023-integration/working-index-cache/BUILD-REPORT.json`
- 같은 run의 `maintenance/canonical-source-validation.json`, `successor.json`, `install.json`, `install-active.json`
- 같은 run의 `maintenance/frozen-query-cases.json`, `query-embeddings.json`, `retrieval-qualification.json`, `control-source-excerpts.json`

출처의 확인 범위와 저자 작성 장면의 경계는 기존 `SOURCES.md`와 `REPORT.md`를 따른다. 공개 출처27개가 이120개 장면의 모든 기하·연기·인원수를 승인한다는 뜻은 아니다.
