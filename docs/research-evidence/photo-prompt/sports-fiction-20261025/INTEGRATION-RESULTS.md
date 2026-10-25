# 스포츠물 의미·후보 데이터 반영과 독립 이미지 검증

## 반영 범위

조사한 330개 원문 행을 문맥 진단 기록으로 보존하고, 102개 시각 의미 카드를 운영 의미 데이터에 반영했다. 사진 후보는 새 후보 100개와 기존 훈련 비브 후보 1개를 사용한다. 그림 매체의 오라 비유(X02)는 의미 데이터에 보존하고 사진의 양성 검색에서는 제외했다. 선택형 슬롯 연결 200개를 추가했다.

- 의미 데이터: `skills/photo-prompt-image-generator/assets/photo_sports_fiction_semantics_20261025.json`
- 후보: `skills/photo-prompt-image-generator/assets/photo_candidate_sports_fiction_20261025.json`
- 연결: `skills/photo-prompt-image-generator/assets/photo_candidate_sports_fiction_bindings_20261025.json`
- 회귀 검사: `skills/photo-prompt-image-generator/tests/test_sports_fiction_semantics.py`
- 실행·설치·원본 검증 근거: `generated/sports-integration-20261025/`

후보의 세 구성군, 사람·손·장비의 소유와 접점, 종목·동작 단계, 혼동 경계, 출처의 실제 검증 범위와 프레이밍 요구를 유지했다. 문맥 진단 기록은 양성 검색과 슬롯 연결에서 제외한다. 장르명, 심리, 기록, 도핑, 항복, 합법성, 동의 또는 경기 결과를 사진만으로 확정하지 않는다. 성인 설정을 요구하는 상호 시선 제안(X08)은 명시적인 성인 문맥 조건을 갖는다.

모든 반영은 선택 가능한 저작 재료다. 주제명만으로 장면이 활성화되거나, 전체 원문이 검증되거나, 원생 의미·픽셀 승인을 받은 것으로 취급하지 않는다. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`, `BLOCKED_UNSCORED`를 유지한다.

## 소스와 실행 데이터 검증

이전 설치본과 작업 소스의 차이는 스포츠 외 변경도 포함한다. 기존 설치본 22,388개 후보를 유지하며, 최신 작업 소스의 추가 기록과 번역 갱신을 합쳐 데이터 전용 후속 실행본을 구성한다. 실행 코드·랭킹은 이전 설치본을 유지한다. V3 저작 소스는 문자의 정확한 소유를 유지하는 V4 리터럴 표현으로 옮긴다. 중복 문구를 공유하던 필드는 필요한 참조만 분리하며, 이전의 관련 없는 의미·효과·조건을 재작성하지 않는다.

의미 회귀 검사 12개가 통과했다. 이는 소유·단계·해석 경계의 데이터 검사이며 생성 픽셀 검사와 별도다. 조사 단계의 64개 회귀 계획 전체를 실행한 것으로 간주하지 않는다.

## 독립 이미지 검증 설계

동일한 사용자 요청과 첨부 사진을 사용하며, 중립적인 종목 목록에서 시드를 고정한 샘플로 서로 다른 세 분야를 배정했다. 각 서브에이전트는 다른 팔의 이력·컨셉·후보를 받지 않고 최신 스킬을 읽어 컨셉, 특징 선택, 구현 계획, 평가 기준과 코어를 확정했다. 세 팔의 코어가 확정된 뒤 새 실행 데이터를 검색하도록 한다.

- A: 리커브 양궁
- B: 수영 스타트
- C: 육상 계주

사진의 얼굴·머리 외관을 참조해 각기 다른 스포츠 장면을 작성하고, 각 팔에서 네이티브 이미지 생성 1회를 시행한다. 반환된 원본의 실제 접점·지지·단계·형태를 검사한다. 프롬프트 감사 통과와 픽셀 통과를 구별하며 가려진 필수 접점은 합격으로 처리하지 않는다. 주제 반영의 픽셀 성공은 평가한 장면과 항목에만 한정한다. 세 이미지로 전체 스포츠 데이터의 픽셀 품질을 보증하지 않는다.

## 설치 결과

- 작업 소스: 후보 23,596개, 연결 18,538개, 소스 모듈 127개. 전체 로드 검증 통과.
- 기존 저작 모듈 125개: 바이트 보존 확인.
- 작업 저장소 검색 인덱스: `8c5fec1babfa95021165cb15aac9354802d170e41ef03ddfe59eea0673d9677a`. 전체 검증 후 활성화, 기존 샤드 삭제 0개.
- 설치 H-F2: `d75d1546f9bdb3537d1316c0e14a5a04903fd29b1cedcfc63caefa328b690cd1`.
- 설치 native source: `f3e06322413adee3264fb44778c3264cee5491f9672236896497edd246707da7`.
- 설치·실행 의존성·recorder 버전 검사 통과. 기본 설정 갱신 완료. `CURRENT` 쓰기 0회.
- 설치 중 다른 작업이 기본 실행본을 갱신한 것이 감지되어, 즉시 덮어쓰지 않고 후보 22,501개와 모든 연결의 보존을 비교했다. 공통 후보 10개의 리터럴 식별자와 번역 차이는 해석된 원문·검색 필드·기존 의미의 동등성 및 최신 저작 소스와의 일치로 확인했다. 통합본에는 동시 갱신의 의미가 보존돼 있다.
- 기존 문서 벡터 21,078개를 정확하게 재사용하고 새 문서 벡터 512개를 계산했다. 실행 코드와 랭킹 변경은 없다.

아래 이미지 검증 결과는 별도 기록한다.


## 검색 증거의 구분

검색 순위 창과 실제 제시 샘플은 다르다. 새 카드가 순위 창에 포함됐다는 사실만으로 프롬프트 작성자에게 제시됐다고 간주하지 않는다. `generated/sports-integration-20261025/arm-material-exposure.json`은 두 집합을 별도 보존한다.

| 팔 | 새 카드가 순위 창에 포함 | 새 카드가 실제 제시됨 | 제시된 전체 고유 소스 수 |
|---|---|---|---:|
| A 양궁 | R01, R02, R03, M08 | R02, R03 | 21 |
| B 수영 | A01, A02, S01, S02, S03, S04 | S01, S03, S04 | 31 |
| C 계주 | A02, A04, L03, L05 | 없음 | 30 |

계주 A04는 동작·접점·기본 프롬프트 검색에서 순위 창에 들어갔지만 실제 발행 샘플에는 뽑히지 않았다. 기존 계주 관련 소스는 제시됐다. 샘플링 시드나 쿼리를 바꿔 원하는 새 카드를 강제로 제시하지 않는다. 따라서 C는 계주 주제와 접점의 픽셀 실현 테스트이며, 새 스포츠 후보의 직접 활용 증거를 제공하지 않는다.

A와 B에서도 새 카드가 독립 기본 구상과 겹칠 수 있으므로 실제 제시·검토·선택과 추가 기여를 구분한다. 이 세 장은 데이터 추가 전후 효과를 추정하는 대조 실험이 아니다.

## 원본 픽셀 결과

세 독립 서브에이전트가 최신 스킬 `e26f7fbefab8a3385ceb1780909513544d8deb011efd390cbb545e43b0b49cf9`와 동일한 참조 이미지 바이트를 사용했다. 각 팔은 `image_gen`을 네이티브 환경에서 정확히 한 번 호출했다. 원본 2장과 출력 차단 1건을 보존했다. 각 팔의 ledger는 1행이며, 독립 manifest는 `photo-independent-run-manifest/v2`, 실제 팩 버전은 `h-f2-v2`다. 세 팔 모두 `cross_arm_inputs_used=false`다. 부모도 반환 원본 두 장을 직접 확인했다.

| 팔 | 컨셉 | 주제·참조 외관 | 엄격한 전체 테스트 | 핵심 근거 |
|---|---|---|---|---|
| A | 조용한 야외 연습장의 리커브 풀 드로 | 육안상 확인 | FAIL, 독립 게이트 2/5 통과 | 활 상단 끝이 프레임 밖. 드로 손가락·턱 아래 앵커·화살 받침·노크/시위 직접 접점은 일부 가림 |
| B | 실내 풀 출발대의 정지된 트랙 스타트 | 미평가 | BLOCKED_UNSCORED | 출력 단계 `moderation_blocked`, 반환 픽셀 없음 |
| C | 계주 배턴 인계 | 육안상 확인, A04 구성군 3/3 관찰 | FAIL, 독립 게이트 5/6 통과 | 하나의 배턴과 두 손·두 팔의 소유는 명확. 앞선 주자의 발바닥/지면 접점이 하단 밖 |

전체 엄격 통과 0건, 부분 관찰로 실패 2건, 차단·미평가 1건이다. 소스·프롬프트·실행 감사 통과는 이미지 품질 통과가 아니다. 사용자 판단은 모두 pending이다.

양궁 R01의 넓은 얼굴 옆 앵커 의미와 엄격 testcase의 턱 아래 직접 접점은 구분한다. 얼굴 옆 손 배치는 보이지만, testcase의 정확한 턱 아래 접촉과 노크-시위 직접 결합까지 보인다고 승격하지 않는다. 계주 A04의 세 의미 구성군은 같은 원본에서 관찰되지만, 이는 제시되지 않은 새 CID의 채택이나 전체 코퍼스 원생 승인이 아니다.

수영의 실제 도구 증거는 `error_code=moderation_blocked`, `moderation_stage=output`, `categories=[sexual]`, request ID `50c1e018-41aa-419e-bba3-05838004072b`다. 이 분류는 도구가 반환한 관찰값이며 사용자의 요청이나 데이터 전체에 대한 판정으로 확장하지 않는다. 픽셀이 없어 주제·의복·접점·참조 외관을 평가하지 않았다. 세 팔 모두 이번 1회 호출 계획을 사용하고 추가 호출은 하지 않았다. 최신 스킬에 있는 기존 예산 내 증명된 동일 입력 재시도 경로를 보편적으로 금지한다고 해석하지 않는다.

각 팔의 대안·전체 소스 검토 결과는 모두 독립 기본 구상 유지, 최종 후보 영감 추가 0, native 채택 0이다. 따라서 새 자료가 직접 생성 품질을 개선했다고 주장하지 않는다. 새 자료의 등록·검색과 관찰 기준의 구체화, 두 실제 스포츠 장면의 의미 실현 및 프레이밍 한계까지 검증했다.

### 결과와 프롬프트

- A: [원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/initial-tests/a/original.png), [프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/initial-tests/a/final_prompt.txt), [평가](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/initial-tests/a/pixel-evaluation.json), [개별 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/initial-tests/a/REPORT.md).
- B: [프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/initial-tests/b/final-prompt.txt), [차단 원본 증거](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/initial-tests/b/native-attempt-1-error.json), [평가](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/initial-tests/b/pixel-evaluation.json), [개별 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/initial-tests/b/RESULT.md).
- C: [원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/initial-tests/c/original.png), [프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/initial-tests/c/final-prompt.txt), [평가](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/initial-tests/c/pixel-evaluation.json), [개별 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/initial-tests/c/RESULT.md).

[통합 실행 증거](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/archived-generated/sports-integration-20261025/test-evidence.json)와 [운영 픽셀 근거 레지스트리](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/registries/photo_sports_fiction_pixel_evidence_20261025.json)는 원본 해시·의미 카드 매핑·평가 범위를 보존한다. 이 레지스트리는 양성 검색 인덱스나 native 승인에 영향을 주지 않는다.

## 결과를 다음 보강에 반영하는 계획

1. **활의 전체 경로와 국소 접점을 분리해 관찰한다.** 상단 끝이 없는 경우 아래 시위가 보여도 전체 경로는 실패다. 다음 관련 구현에서는 기존 동작과 얼굴 외관을 보존하면서 전체 활의 외곽 여백을 먼저 확보하고, 드로 손·노크·받침의 직접 경계가 한 시점에 보이는 시점을 선택하는 국소 수선으로 다룬다. 사진 분위기만 더 강화하는 것으로 대체하지 않는다.
2. **주자의 지지점은 별도의 동시 프레이밍 요구로 유지한다.** 배턴 인계의 세 구성군이 맞아도 발·지면 지지가 필수인 테스트는 별도 실패다. 다음 관련 구현에서는 앞 주자의 원근상 크기를 조절하고 모든 신발 바깥에 트랙 여백을 확보하는 구도를 우선한다.
3. **차단을 픽셀 수선으로 위장하지 않는다.** 수영은 이미지 근거가 없으므로 신체·접점의 성공/실패 예시로 학습하거나 후보를 비활성화하지 않는다. 그대로 차단·미평가 근거로 남긴다.
4. **검색 성능과 생성 품질을 별도로 평가한다.** 새 카드의 순위 창 포함, 실제 제시, 검토, 활용을 각각 집계한다. 새 카드의 직접 개선 효과를 주장하려면 별도의 사전 설계된 대조 평가가 필요하다. 이번 시드를 바꿔 새 카드를 억지로 뽑지는 않는다.
5. **승인 범위를 넓히지 않는다.** 64개 조사 단계 회귀 계획과 미평가 카드들은 남아 있다. 이번 관찰을 전체 102개 의미 카드·100개 새 후보의 완전한 픽셀 승인으로 승격하지 않는다.


## 실제 활용 후속 재검증

최초 세 팔의 새 후보 활용 0을 확인한 후, 시각 후보 100개의 실제 의미 검색 필드를 보강하고 국소 장비 후보 6개를 추가했다. 새 독립 세 팔에서는 최종 프롬프트 활용 3/3, 원본의 전체 엄격 통과는 피겨 1/3이다. 사이클·배드민턴의 가시성/공간 실패도 보존했다. [상세 후속 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/REPORT.md)


## 게시 전 전체 스키마 보완

전체 운영 사전 검사에서 검색용 관계 328개의 필수 ID 누락을 발견해 안정적인 ID를 부여했다. ID를 제외하면 원문·조건·효과·출처·검색 필드는 정확히 같으며, 106개 시각 후보 전체에 실제 관계 스키마 검사를 추가했다. 최종 회귀 검사는 23개다. 이 보완은 기존 이미지 실행본을 새 실행본의 픽셀 승인으로 바꾸지 않는다. 게시 검증과 보존 근거는 [PUBLICATION.md](PUBLICATION.md)에 기록한다.
