# 첩보물 데이터 반영과 독립 이미지 테스트 결과

2026-10-23. 데이터 반영·기본 설치 갱신·독립 에이전트 3개의 참조 이미지 생성과 실제 픽셀 검토를 수행했다. 신규 표현 1개의 완전한 시각 실현은 확인했다. 최초에 고정한 세 장면의 모든 관찰 기준을 동시에 만족한 결과는 0/3이다. 이것을 세 장 모두 첩보 장면을 표현하지 못했다는 뜻으로 해석하지 않는다. 특히 A는 선택 가능한 작가 소유의 동작을 ‘접촉 전’으로 발전시켜, 원래의 동시 접촉 검사와 다른 순간을 의도적으로 선택했다.

## 데이터와 실제 설치

시각 카드 138개 중 111개를 한영 optional 후보로 추가하고, 17개는 기존 소스·조건·효과·연결을 그대로 재사용했다. 세부 표본 검토를 보류한 10개와 문맥 구분 172개, 합계 182개는 diagnostic으로 분리해 positive 검색에서 제외했다. optional 연결 158개를 추가했다. 아직 개별 검토·매핑이 남은 외형 용어 65개와 보류 카드 10개의 검증은 완료로 바꾸지 않았다.

[반영 상세](integration-evidence/DATA-REFLECTION.md), [경계 검사 11개](integration-evidence/focused-tests.log), [사전 검증](integration-evidence/dictionary-validation.final.json), [원본 보존 검사](integration-evidence/protected-source-review.json).

최신 기본 설치본은 H-F2 `587f77950e648994525a9066e8757e9fbaa55b38c3d9312f0b5ef517fdaece28` / native `489839d65a789793d41a60e11d83965132f2030d23f69032ff35e7d8a5ab51f4`다. 동시 작업의 직전 후보 20,782개를 모두 보존하고 이번 293개 기록을 합쳤다. 배포 코드의 source/embedding/seal 검증을 통과했으며 native 커널은 수정하지 않았다. positive 전체 20,268 CID에서 신규 시각 후보 111개 전부 존재, diagnostic 182개 전부 제외, 재사용 17개 전부 존재를 확인했다. [실제 활성화](integration-evidence/final-install-active.json), [전체 CID 포함/제외](integration-evidence/final-positive-closure.json).

최종 설치본에서 한영 412개 질의를 실행했다. literal smoke는 gold가 있는 256개 중 top8 251개, top32 254개를 찾았다. 카드 작성자의 자연어 표현 48개는 top8 39개, top32 45개였다. 경계·일반·비시각 대조 88개에는 exact-CID gold가 없어 성공률을 매기지 않았다. 이 질의들은 독립 holdout이 아니며, 후보 노출은 선택·의미 승인·픽셀 성공을 뜻하지 않는다. [최종 검색 집계](integration-evidence/final-active-retrieval-summary.json), [대조군의 실제 노출과 한계](integration-evidence/retrieval-findings.md).

## 독립 실행과 참조 경계

각 에이전트는 실제 사용자 요청과 첨부 사진, 같은 최신 SKILL.md 및 허용된 중립 precore 자료로 독립 랜덤 콘셉트·초안을 고정한 뒤 후보를 읽었다. 다른 arm의 프롬프트·이미지를 보지 않았다. 세 arm의 최초 core 해시는 서로 다르며 최신 skill SHA256은 `f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089`다. A/C의 검색 준비 오류는 같은 입력 바이트를 보존한 exec 하위 run으로 복구했고, 최초 기록을 삭제하지 않았다.

세 이미지 테스트는 같은 검증된 H-F2 `3300bd369483c394610b29a53b8421934dacba4a9039e6cdd017deec7c4c26b7`에 고정했다. 작업 중 기본 설치가 바뀌어 그 변경을 보존한 재기반 설치본을 따로 만들었기 때문이다. 이미지에 사용한 주제 모듈 2개는 최종 설치본에서도 바이트가 같다. 전체 후보 집합은 다르므로 세 이미지의 검색·픽셀 결과를 최종 기본 설치본에서 실행한 것으로 바꾸어 보고하지 않는다. [모듈 동등성](integration-evidence/test-source-rebase-equivalence.json).

첨부 JPEG SHA256 `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`을 세 native 호출에 실제로 첨부했다. 얼굴·짧은 검은 보브·앞머리의 외관 안내로 사용했으며 실제 신원이나 나이를 단정하지 않았다. 각 arm native 1회, 총 3회/3장이고 API fallback·재생성은 없었다. 세 원본은 모두 1536×1024 PNG다. 저장 이미지·최종 prompt·원장·manifest·참조·skill·generation의 연결을 검사했다. [완료 자산 검증](integration-evidence/completed-image-closure.json), [재검증 스크립트](integration-evidence/validate_completed_images.py).

## 실제 이미지 판정

| arm / 독립 콘셉트 | 새 데이터의 실제 사용 | 실제 픽셀 | 최초 전체 사례 |
|---|---|---|---|
| A · 비 오는 역 꽃가게 | 2개 신규 소스 노출, suspended_handoff 전체 문장을 inspiration_only로 사용. native chosen=[] | 봉투를 든 남성의 손, 여성의 빈 손바닥, 둘 사이의 간격과 양쪽 소유 관계가 함께 보임. 선택한 신규 표현의 국소 검사 PASS | FAIL · 최초 기준의 양손 동시 접촉은 없음. 남성의 정확한 눈 시선도 프레임 밖이라 확증 불가 |
| B · 미술관 보존 프리뷰 리셉션 | 신규 사진 제시 소스 1개 노출, 기존 photo/table/owner 근거와 맞지 않아 미채택 | 공개 역할·카탈로그 아래 같은 카드의 두 접점·별도 손목은 보임. 제3 방문객 환대와 카드로 향한 시선의 분리는 모호 | FAIL · public_hidden_attention partial |
| C · 비 오는 화물역 현장 관찰 | 신규 분석 비교 소스 1개 노출, 두 보고서/기존 소유자 근거가 없어 미채택 | 차량의 붉은 표식이 LCD/기록 사진에 반복되고 연필 접촉은 보임. 렌즈의 특정 표적 방향과 마이크–무전기 전체 배선은 확증 불가 | FAIL · observation_chain 및 communication_apparatus partial |

A의 신규 소스는 `cand_e8f9f772b82355b7bbe1c2a949161eab`다. 정확한 문장은 “One person extends an envelope while the other person's open hand remains separated from it by a visible gap.”이며 최종 프롬프트와 픽셀에 모두 있다. 이 1개의 완전한 시각 실현 관찰은 다른 신규 110개의 검증이나 formal native whole-source 승인으로 확장하지 않는다. B/C는 새 소스를 채택하지 않았으므로 새 소스 자체의 픽셀 품질은 미검증이다. C의 arm 기록에 있는 BLOCKED_UNSCORED는 이 미채택 소스에 대한 upstream 판정이고, 생성 이미지 자체가 차단됐다는 뜻이 아니다.

| 산출물 | A | B | C |
|---|---|---|---|
| 프롬프트 | [A 최종](/Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-20261023-integration-a/exec/final-prompt.txt) | [B 최종](/Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-20261023-integration-b/final-prompt.txt) | [C 최종](/Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-20261023-integration-c/exec/final-prompt.txt) |
| 이미지 | [A PNG](/Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-20261023-integration-a/exec/images/espionage-a-native-1.png) | [B PNG](/Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-20261023-integration-b/results/museum-liaison.png) | [C PNG](/Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-20261023-integration-c/exec/results/espionage-c.png) |
| root 원본 픽셀 재검토 | [A](integration-evidence/root-pixel-review-a.json) | [B](integration-evidence/root-pixel-review-b.json) | [C](integration-evidence/root-pixel-review-c.json) |
| 독립 manifest | [A](/Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-20261023-integration-a/exec/run_manifest.json) | [B](/Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-20261023-integration-b/native-manifest.json) | [C](/Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-20261023-integration-c/exec/independent-manifest.json) |

root도 세 원본을 직접 열어 최초 사례와 선택한 전체 source 문장에 대조했다. B의 시선 판정과 C의 광학/배선 판정은 arm과 일치했다. C의 두 손·앉은 자세 자체는 타당하지만, root는 최초 body_scene_integrity에 포함된 광학 경로까지 묶어 partial로 기록했다. 검사 범위가 다른 이 차이를 손 구조 실패로 바꾸어 보고하지 않는다. 기술적 기록 검사가 통과해도 주제 전체의 픽셀 검사가 통과하는 것은 아니다. 사용자 선호·수용은 미확인이다.

## 남은 범위와 반영 계획

1. 이번 소스·연결·진단 경계는 설치된 상태를 유지한다. 한 장의 국소 관찰을 전체 사전의 native 승인이나 자동 장르 강제 규칙으로 승격하지 않는다.
2. 다음 검색 회귀에서는 한국어 신발 여밈·스타킹 지지 등의 누락을 독립 작성자가 만든 질의로 재검증한다. 동의어를 대량 추가하기 전에 전체 소스의 효과·소유 관계를 재검토한다. 일반 보고서나 사람 없는 저장 공간에 사람/동작 후보가 노출되는 대조 사례도 요청 단위의 조건·선택 검토에서 확인한다.
3. 다음 픽셀 사례에서는 A의 동시 접촉/접촉 전 순간을 별도 사례로 고정하고, B의 제3 방문객과 각 시선 표적을 같은 프레임에 두며, C의 렌즈 축·특정 차량·라디오 연결점을 한 화면에서 읽을 수 있는 배치로 비교한다. 이번 세 이미지를 고치거나 추가 생성하지 않았다.
4. 표본 동등성 보류 10개와 미연결 외형 용어 65개는 원문·표본 검토를 마친 항목부터 별도 반영한다. 비시각 문맥을 외관의 사실로 바꾸지 않는다.

초기 연구 34개 파일의 해시와 초기 상태 표시는 보존했다. 이 문서와 integration-evidence가 후속 실행 결과다. 커밋·푸시는 수행하지 않았다.
