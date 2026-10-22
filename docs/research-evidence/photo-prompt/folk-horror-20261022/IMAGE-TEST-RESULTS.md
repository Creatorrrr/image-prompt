# 독립 3개 arm의 참조 이미지 생성 테스트

2026-10-22. 세 서브에이전트가 서로 다른 컨셉을 독립 난수로 선택하고 최신 작업 스킬로 프롬프트·이미지를 작성했다. 각 arm에서 native `image_gen` 1회씩, 총 3회 성공했다. 추가 생성·API/CLI 대체 호출은 없었다. 각 원본을 담당 arm과 coordinator가 직접 확인했다.

**참조 얼굴·헤어 표현은 3/3에서 확인했다. 모든 엄격 기준을 통과한 arm은 0/3이다.** 겨울 장면은 새 L03 후보의 실내/실외·문턱·그릇 관계가 실제로 나타났으나 전체 문턱 가시 기준에서 부분 실패했다. 나머지 두 arm은 신규 후보를 실제 사용하지 않아 신규 데이터의 프롬프트→픽셀 전달을 검증한 것으로 세지 않는다.

## 실행 방법과 독립성

- 요청문과 첨부 이미지가 공통 입력이다. 사진은 가시 얼굴·헤어의 외형 참조로 사용하고 장면의 인물은 허구의 성인 역할로 저술했다. 참조 인물의 실제 정체·나이·이력을 추정하지 않았다.
- 참조 경로: `/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg`, SHA-256 `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`.
- 각 arm은 다른 arm의 프롬프트·pack·이미지를 입력으로 사용하지 않았다. 각자 컨셉 후보를 만든 뒤 OS 난수 `secrets.randbelow`로 하나를 뽑았다. 독립 baseline/core를 먼저 freeze하고 후보를 검색했다. 검색 결과에 맞춰 난수 컨셉을 다시 뽑지 않았다.
- 스킬 SHA-256은 세 arm 모두 `7fe5b6cfc2da6e65dd9b9dc999e46d70a1fac7dce8c47157e53c1cba43b00f35`. 각자 기존 저장 설정을 해석해 sensual=1, fetish=0, surreal=0, creativity=1을 고정했다. 각 arm의 controls seed와 core 해시는 다르다.
- 새 설치 세대 `0ad30ffe246d77f7c711ea49244b407b71ff747cbc33b380f6f12aaacd657cf2` 및 native `4cf1bf4117010c240ccb49148e2ee1bd5be2ca58d79c1f1521888aa16f9c0b20`에 각각 binding됐다.
- 실제 반환된 source 전체·조건·effects를 검토하고 query/CID/RID occurrence마다 skip 또는 inspiration_only를 기록했다. 새 CID를 강제로 주입하지 않았다. 후보와 baseline의 완전한 대안을 비교한 뒤 최종 프롬프트를 정했다.
- 장면 테스트는 검색 전, 실제 사용 source의 추가 테스트는 이미지 호출 전에 고정했다. 원본을 보고 기준을 약하게 바꾸거나 실패를 없애기 위해 다시 생성하지 않았다. coordinator의 [별도 검토 계획](integration-evidence/coordinator-pixel-plan.json)도 생성 원본을 보기 전에 기록했다.

| arm | 독립 난수 컨셉 | 실제 검색·전체 source 검토 | 새 카드 노출 / 실제 사용 |
|---|---|---|---|
| Korea | 닫힌 공동 우물에서 시작된 젖은 발자국 | 5 queries, 40 occurrences / 38 distinct | 신규 CID 0개. 기존 재사용 R01 관련 실현은 노출됐으나 최종은 baseline 유지 |
| Harvest | 씨앗 공납: 빈 그릇 위의 씨앗을 공동체가 지켜봄 | 5 queries, 40 occurrences / 39 distinct | 새 O01·R06 노출, 둘 다 미사용. 기존 task-gaze source 1개만 영감 사용 |
| Winter | 겨울 과수원 wassail에서 돌아온 인물의 문턱 | 3 queries, 24 occurrences / 24 distinct | 새 L03·R02 노출, L03만 영감 사용 |

세 arm 합계 13개 H-F2 질의와 104개 반환 occurrence다. arm 사이에 같은 source가 있을 수 있으므로 distinct 수를 합쳐 전체 unique라고 부르지 않는다. 이 검색은 데이터 검증의 별도 104개 한영 질의/208회 실행과 다른 실행이다.

Korea arm은 첫 관리용 초기화에서 기본 전체 슬롯 범위를 확인한 후 후보 접근 전에 3개 슬롯 범위로 다시 초기화했다. 난수 컨셉·request·controls·독립 core/baseline은 유지했다. 실제 테스트 run은 `folk-korea-20261022-6e9460-s3`이며 초기화 횟수를 독립 실험이나 추가 생성으로 세지 않았다.

## 1. 닫힌 공동 우물과 발자국

![닫힌 공동 우물과 발자국](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/folk-horror-20261022/images/korea-closed-well.png)

[실제 도구 전달 프롬프트](integration-evidence/arms/korea/actual-tool-prompt.txt) · [도구 payload](integration-evidence/arms/korea/actual-tool-payload.json) · [독립 manifest](integration-evidence/arms/korea/run_manifest.json) · [coordinator 원본 판정](integration-evidence/coordinator-review-korea.json)

| 확인할 것 | 원본 판정 |
|---|---|
| 참조 얼굴·단발·분리된 앞머리 | PASS: 환경 인물 사진 크기에서도 비교 가능 |
| 우물·맨발 자국·문턱의 주민 | 가시 확인. 주인공의 내려다보는 시선과 지켜보는 주민들이 농촌 금기의 분위기를 만듦 |
| 우물에서 시작해 인물까지 이어지는 완전한 흔적 | **UNOBSERVABLE_NOT_PASS**: 우물 덮개 왼쪽이 프레임 밖이며 전체 시작점·연결 경로가 충분히 확정되지 않음 |
| 신체 소유·발의 지면 접촉 | 가시 범위에서 확인. 신체 결함을 관측하지 않음 |
| 이번 새 후보의 직접 전달 | **NOT_TESTED**: 신규 CID가 노출·사용되지 않았고 최종 프롬프트가 독립 baseline과 동일 |

이미지는 농촌의 이상한 흔적과 집단의 주시를 표현한다. 완전한 사건의 연결까지 성공했다고 주장하지 않는다. 실제 한국 의례나 초자연 원인의 증거가 아니다.

## 2. 씨앗 공납

![씨앗 공납](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/folk-horror-20261022/images/harvest-seed-levy.png)

[실제 도구 전달 프롬프트](integration-evidence/arms/harvest/actual-tool-prompt.txt) · [도구 payload](integration-evidence/arms/harvest/actual-tool-payload.json) · [독립 manifest](integration-evidence/arms/harvest/run_manifest.json) · [coordinator 원본 판정](integration-evidence/coordinator-review-harvest.json)

| 확인할 것 | 원본 판정 |
|---|---|
| 참조 얼굴·헤어 | PASS |
| 동일 인물의 연결된 양팔·씨앗을 받친 양손·그 아래 완전한 빈 그릇 | **PASS**. 다른 그릇들은 곡식이 차 있으며 주인공의 그릇은 비어 있음 |
| 밝은 수확 환경·공동체의 작업 지향 시선 | PASS. 기존 task-gaze 영감이 실제 화면에 보임 |
| 공동체의 규칙이 강압적인 공포로 읽힘 | **부분 반영/FAIL**: 표정이 우호적이고 평범한 축제 참여로도 읽혀 포크 호러의 압박이 약함 |
| 발과 지면의 전체 지지 | **UNOBSERVABLE_NOT_PASS**: crop 밖. 해부학적 오류를 발견했다는 의미가 아님 |
| 새 O01·R06의 전체 의미 | **NOT_TESTED**: O01은 곡식단/비워진 작업대, R06은 빈 의자/그릇 원/바깥 참여자의 전체 배치가 필요. 이번에는 미사용이므로 수확 소품이 보인다는 이유로 통과시키지 않음 |

참조·손 소유·물체 배치의 성공과 공포감의 부분 실패가 함께 나온 사례다. 예쁜 농촌 사진이 생성됐다는 사실만으로 장르 테스트를 통과시키지 않았다.

## 3. 겨울 과수원에서 돌아온 문턱

![겨울 과수원과 문턱 바깥 그릇](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/folk-horror-20261022/images/winter-threshold.png)

[실제 도구 전달 프롬프트](integration-evidence/arms/winter/actual-tool-prompt.txt) · [도구 payload](integration-evidence/arms/winter/actual-tool-payload.json) · [독립 manifest](integration-evidence/arms/winter/run_manifest.json) · [coordinator 원본 판정](integration-evidence/coordinator-review-winter.json)

사용한 새 source는 **L03 / `cand_dfc1906f2832572d9f6678c5024d7536` / base**다. 정상 검색에서 나타난 전체 source를 읽고, 허리 높이에서 그릇을 들던 baseline을 ‘몸은 실내에 두고 문턱 바깥 돌바닥에 내려놓은 순간’으로 국소 재구성했다. 최종 프롬프트에는 다음 source의 완전한 문장을 그대로 담았다.

> A raised wooden sill separates a lit interior from the dark exterior; a bowl rests outside the sill.

| 호출 전 고정 source 테스트 | 원본 판정 |
|---|---|
| 나무 문턱의 전체 폭과 양쪽 접점을 가림 없이 확인 | **FAIL/partial**: 나무·솟은 구조·양쪽 문설주는 보이나 팔과 그릇이 폭 일부를 가림 |
| 같은 문턱이 밝은 실내와 어두운 실외를 나눔 | **PASS** |
| 그릇이 문턱 바깥에 완전히 있고 바깥 돌바닥과 닿음 | **PASS** |
| 모든 조건을 동시에 완전히 관측 | **FAIL/UNOBSERVABLE_NOT_PASS**: 앞서 정한 전체 폭 기준을 그대로 적용 |

가시 형태로는 L03의 핵심 구성요소와 관계를 확인했다. 사전에 추가한 ‘전체 문턱 폭을 가림 없이 관측’ 기준은 통과하지 못했으므로 완전 충족으로 보고하지 않는다. source 문장이 표현된 사실과 엄격한 전체 가시성 판정을 구분한다.

참조 외형, 연결된 두 팔·양손의 같은 그릇 접점, 나뭇가지에 직접 묶인 리본, 횃불 인물 두 명은 확인된다. 한 발의 전체 지지는 가려져 미관측이다. 따뜻한 실내와 차가운 과수원, 그릇을 바깥에 둔 행동, 기다리는 인물의 연결이 세 사례 중 가장 명확한 포크 호러 분위기를 만든다. 실제 wassail의 역사적 재현·초자연 효과를 증명한 것으로 세지 않는다.

## 결과의 범위와 다음 검증 설계

새 자료의 source→자연 검색→전체 비교→프롬프트→가시 관계 연결은 겨울 L03에서 부분적으로 확인했다. 새 source 69개 전체, 문화별 정확성, 독립 holdout, 이전 데이터와의 생성 A/B, 사용자 선호는 이번 3장으로 검증되지 않았다. 실패한 일부 조건을 기록한 채 이미지 생성 실험 자체는 마쳤다.

후속 개선은 다음 순서가 적합하다. 이번 결과를 덮지 않고 별도 case로 분리해야 한다.

1. **카메라와 관측 범위**: L03는 문턱 전체 폭을 가리지 않는 외부 사선 구도, 우물 사례는 전체 덮개·첫 발자국·최종 접점이 함께 들어오는 높은 사선 구도를 설계한다. 전신 지지를 검증 조건으로 삼으면 실제 구도에도 두 발/지면을 포함한다. 사진에 필요하지 않은 지지 조건은 다음 core 작성 때부터 적용 이유를 재검토하고 이미 고정한 테스트에는 소급하지 않는다.
2. **관계로 만드는 압박**: 수확 장면은 ‘주변 모두가 미소 짓는다’만으로 강제를 대신하지 않고, 내밀었지만 받아주지 않는 손·비워진 유일한 자리·차단된 이동처럼 함께 관측할 행동과 대응을 선택한다. 각 새 source를 사용한다면 그 전체 배치를 유지한다.
3. **신규 source 전용 픽셀 세트**: 자연스러운 무작위 저작 평가와 별도로, 완전한 카드 의미 자체를 요구하는 독립 테스트 입력을 만든다. 12개 필수 사례의 source별 gate를 고정한 뒤 기존 계획의 A/B/C 비교를 수행한다. 이번 미사용 O01/R06나 미노출 한국 카드의 성공을 추정해서 채우지 않는다.
4. **검색 잡음**: [대조 37건](integration-evidence/control-semantic-review.json)의 충돌·문맥 문의를 별도 holdout으로 검증한다. 모델이 불필요한 source를 실제로 skip하는지 확인한 뒤에만 순위/배제 처리 변경을 검토한다. source 원문을 잘라 조건을 약화하지 않는다.

모든 새 source의 native approval은 false이며 세 arm의 native chosen list는 빈 배열이다. 이번 사용은 현재 H-F2의 저작 영감 경로다. compose/runtime와 review-record 검사 PASS는 입력·기록 유효성에 관한 결과이며, 이미지의 엄격 technical qualification FAIL을 덮지 않는다. 사용자 수락은 아직 받지 않았다.

원본 이미지 해시:

| arm | SHA-256 |
|---|---|
| Korea | `bcf4e46d1be21096bda18d164218c984691bbce915eecfcf14c7ce5daf05da95` |
| Harvest | `81f035fd601aed9f4689af31dd13243c58aa14a52edf431b69f721626527e387` |
| Winter | `31e9c4e6c72de37041a5bcce4b9af9c897f0db338e4fab44068606b88f2a830d` |

원본 파일을 동일 바이트로 보존했다. [FINAL-INTEGRITY.json](integration-evidence/FINAL-INTEGRITY.json)은 참조·프롬프트·source 세대·원본 이미지·독립 manifest와 기존 파일 보존을 검증한다. 실제 픽셀 판정은 각 arm 및 coordinator의 별도 원본 검토 기록에 있다.
