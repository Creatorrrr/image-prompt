# 캠퍼스물 검색·코어 잠금 개선 및 독립 3개 재시험

검색과 코어 소유권 개선은 적용됐다. 신규 후보는 **3개 중 2개 최종 프롬프트에 새 문구로 들어갔고, 두 이미지에도 일부 구성 요소가 보인다. 전체 관계를 동시에 충족한 신규 후보의 엄격한 픽셀 통과는 0/3**이다. 생성 성공이나 프롬프트 감사 통과를 이미지 전체 성공으로 세지 않았다.

## 3개 실제 이미지와 프롬프트

| 실험 | 독립 추첨 기본안 → 후보 이후 최종안 | 신규 소스 노출 | 새 후보 문구 | 전체 픽셀 판정 | 산출물 |
|---|---|---:|---|---|---|
| A | 구내식당에서 노트 정리 → 강의실에서 노트 정리 | 9개 | S01 강의실 공간 관계 1건 | FAIL: 단차 좌석·스크린은 보이나 강연대 식별과 모든 좌석 열↔통로 접점이 불완전 | [이미지](arms/a/image.png) · [프롬프트](arms/a/prompt.txt) |
| B2 | 비를 기다리는 지붕 보행로 → 기숙사 문턱에서 잠깐 멈춤 | 4개 | S11 침대·책상·수납 구역 1건 | FAIL: 침대 둘·책상 둘은 보이나 완전한 침대 형태와 두 별도 수납↔해당 생활 구역 연결이 불완전 | [이미지](arms/b2/image.png) · [프롬프트](arms/b2/prompt.txt) |
| C | 자전거 바구니에 노트 넣기 → 카페에서 잡지 읽기 중 시선 들기 | 7개 | 신규 소스 0건; 호환 가능한 기존 소스 2건 사용 | 신규 데이터 성공으로 세지 않음. 별도로 왼손이 빈 탁자 대신 페이지 위에 놓인 오류 | [이미지](arms/c/image.png) · [프롬프트](arms/c/prompt.txt) |

세 에이전트는 이전 실험이나 다른 arm을 보지 않는 새 세션으로 시작했다. 후보 접근 전에 각자의 무작위 추첨, baseline, feature selection, ownership review, embodiment review를 동결했다. B가 broad campus 주제 자체까지 열어둔 것은 부모가 후보 접근 전에 발견했다. 기존 B를 보존하고 동일 추첨·동일 baseline으로 B2를 만들어 주제만 보호했다. 후보 재추첨이나 채택 quota는 없었다.

실제 `image_gen` 호출은 **각 1회, 총 3회**다. 같은 참고 파일 SHA `06d6c6fe...ece7`을 사용했다. 전달한 프롬프트·원본 참조·저장 이미지 해시, ledger 각1행, manifest와 관리형 리뷰를 확인했다. 이미지 사본은 원본과 byte-identical이다. 실제 출력은 A1536×1024, B/C1237×1272다. 도구 응답에 모델 식별자가 없어 observed model은 unknown으로 기록했다. 사용자 평가는 pending이다.

## 신규 소스 전달 근거

| 실험 | CID / RID | 최종 프롬프트의 새로운 근거 | 적용 범위 |
|---|---|---|---|
| A | `cand_72ff5a0952cc5691bb09a90532c58937` / `base` | Tiered rows of long seats face a front lectern and screen, with a side aisle reaching each row. | composition/count/relationship/setting: 전부 open |
| B2 | `cand_6ca2cafe37485166ab079d5f75367a5a` / `base` | one room with exactly two beds and two personal desks in separate zones + 각 침대·책상·별도 수납의 연결 문구 | composition/count/relationship/setting: 전부 open |

두 새 관계는 baseline에 없었다. source hash·conditions·전체 declared effects, 실제 renderer 문구와 동일한 prompt hash를 [부모 전달성 검사](PARENT-PROMPT-TRANSMISSION.json)로 확인했다. source별 조건이나 효과를 잘라내지 않았다. 세 실험 모두 native chosen ID는 빈 배열이며, 이 표는 H-F2 material의 `inspiration_only` 전달 근거다. whole-source native qualification으로 승격하지 않는다.

A는 신규 소스 5개 게이트 중 강연대·모든 통로 접점이 partial/unobservable였다. B는 두 desk가 보이나 preauthored complete-bed-shape와 두 bedside-storage 구역 연결이 partial이었다. C의 기존 café/잡지 구성은 보이지만 신규 source 기여는0이다. 부모도 원본 픽셀을 직접 별도 검토했다. [부모 픽셀 판정](PARENT-PIXEL-REVIEW.json), [생성 전 게이트 해시](PRE-RENDER-TESTCASE-BINDINGS.json), [B2 생성 전 inline 게이트](PRE-RENDER-B2-INLINE-GATES.json) 참조.

관리형 리뷰 기록은3/3 유효하다. 그 안의 신체/접촉 기술 판정은 AFAIL(가방 바닥 지지가 가림), BPASS, CFAIL(왼손 목표 면 불일치)이다. B의 신체 판정 PASS는 신규 S11 관계의 부분 실패를 대신하지 않는다. 참고 얼굴·단발의 보이는 특성은 세 이미지에서 유지됐으며 실제 신원을 증명하지 않는다.

## 수정과 검색 검증

실행·연구·위임 문구가 주제 검색으로 섞이던 경로에 `photo-request-query-scope/v1`을 추가했다. 원문과 활성 구간은 보존하고 exact visual/topic_reference/reference_use/workflow 용도를 검토한다. 세 실제 주제 질의는 모두 **캠퍼스물**이었다. 기본 프롬프트 질의·슬롯 질의·부정 및 설정값 firewall은 유지했다.

코어에는 새 managed freeze의 `ownership_review`를 요구한다. 모든 requester anchor와 agent_visual_choice의 원자적 문구를 검토하고, 긴 필수 문구 속에 끼어든 저자 선택도 거절한다. 정의·required assertion도 검사한다. 부모가 의미 소유권을 직접 검토했으며, 이 구조 검사가 임의 자연어 소유권을 자동 증명한다고 주장하지 않는다. 과거 기록은 그대로 검증할 수 있다.

집중 회귀 **64/64 PASS**, 실제 freeze 경로에서도 review 누락·짧은 저자 문구를 숨긴 anchor를 거절하고 같은 baseline의 좁은 anchor를 통과시켰다. 생성기와 독립 감사기가 query scope를 같은 hash로 재구성하며 변조를 거절했다. [테스트](FOCUSED-TESTS.json) · [실제 freeze 회귀](REAL-FREEZE-REGRESSION.json) · [코어 검토](PARENT-CORE-REVIEW.json).

동일21,053CID/21,055RID 풀·난수·알고리즘에서 질의 scope만 바꾼 별도 비교는 다음과 같다. 이 비교를 arm의 창작 입력으로 주지 않았다.

| 측정 | 구 projection: 신규 후보 + 같은 첨부 이미지 + 캠퍼스물 | 새 projection: 캠퍼스물 |
|---|---:|---:|
| 상위20 안 신규 CID | 1 | 11 |
| 상위100 안 신규 CID | 8 | 50 |
| A와 같은 난수의 제공 표본 안 신규 CID | 1 | 8 |

수정 후 표본이 실제 A receipt와 일치한다. 이는 이번 질의의 비교이며 일반적인 검색 정확도나 이미지 성공률 통계는 아니다. [질의 비교](QUERY-ABLATION.json) · [세 receipt 재검증](PARENT-RECEIPT-VERIFICATION.json).

## 적용 버전과 보존

검토한 Python8개 멤버만 기존 sealed 데이터 위에 교체했다. native 데이터 멤버 변경0, H-F2 데이터4,087개 file manifest 동일. 작업 중인 별도 변경은 함께 배포하지 않았다. 세 실험은 H-F2 `4a05dd82...` / native `987f0648...`에 고정됐다. 이후 동시 데이터 후속 release가 기본값을 갱신했지만 같은8개 코드 SHA를 유지함을 확인했고 되돌리지 않았다. 캠퍼스 candidate/bindings/semantics 세 파일은 시작 SHA 그대로다. working corpus manifest의 동시 변경도 보존했다. [구현·경계](IMPLEMENTATION.md) · [검토 patch](REVIEWED-CODE-PATCH.diff) · [closure 검사](RELEASE-CLOSURE-AUDIT.json).

실험 시작 시 최신 SKILL SHA는 `8c82b646...`였고 세 manifest에 그대로 남았다. 실험 도중 live 문서가 `83b3239e...`로 바뀐 것은 **혼합된 대화 제목에서 exact topic 부분만 고르라는 설명 추가**다. 본 실험은 처음부터 정확한 캠퍼스물 부분만 인용해 이미 이 기준을 준수했다. 실행한 내용의 byte-exact snapshot을 초기 SHA와 대조해 복원·보관했고, 새 문서로 과거 실행 메타데이터를 바꾸지 않았다. [버전 대조](SKILL-PROVENANCE-RECONCILIATION.json) · [실행 스킬](SKILL-EXECUTED.md) · [설명 추가 diff](SKILL-AFTER-EXECUTION-DELTA.diff).

## 다음 반영 계획

1. 신규 positive100건 중 broad subject effect가 있는94건을 **전체 양국어 명제·소유자·대상·속성 기준으로 재검토**한다. 반영률을 높이려고 subject 잠금이나 source effect를 지우지 않는다. 배경 물체와 참조 인물에 대한 실제 변경 범위를 분리할 수 있는 경우에만 근거 있는 owner/property 표현을 만든다.
2. 그 수정은 소스 전체의 count·접촉·관계를 유지한 독립된 계약으로 검증한다. 참조 얼굴·신원 범위와의 충돌/호환 양쪽 회귀를 만들고 새 source/index release를 발행한다. 기존 발행 기록은 변경하지 않는다.
3. 렌더링 단계에서는 A의 distinct 강연대와 **모든** 좌석↔통로 접점, B의 두 완전한 침대/책상/옆 수납 구역, C의 빈 탁자 위 왼손 접촉을 먼저 한 화면에서 검토한다. 더 강한 문구만 덧붙이지 않고 열린 구도·위치·정보량을 조정한다. 얼굴 강조와 연결 지점 가시성이 함께 성립하지 않으면 그 optional 대안을 거절한다.
4. 다음 재시험도 새 독립 core와 사전 게이트를 사용하고 실패한 기준을 그대로 유지한다. source 노출, 새 문구 전달, 픽셀 전체 충족, 기술 판정, 사용자 선호를 분리한다.

현재 결과로는 검색과 문구 전달 경로의 개선을 확인했으며, 신규 소스 전체의 픽셀 충족은 남은 과제다. baseline 이미지는 생성하지 않았으므로 source 기여 경로는 동결 텍스트 대비/원본 source/최종 문구/관찰 픽셀로 추적한 것이며, 이미지 간 인과 A/B 실험으로 일반화하지 않는다.

[최종 기계 검증](FINAL-VALIDATION.json)
