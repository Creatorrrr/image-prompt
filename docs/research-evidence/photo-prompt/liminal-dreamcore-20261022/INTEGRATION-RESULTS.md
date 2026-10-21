# 리미널 연구 데이터 반영과 독립 생성 테스트 결과

2026-10-22. 연구 결과를 운영 후보 모듈과 시각 의미 레지스트리에 반영했다.
독립 서브에이전트 3개가 최신 스킬로 서로 다른 복잡한 컨셉을 저술하고
이미지 생성을 각각 1회 실행했다. 실제 이미지 2장이 반환됐고, 1회는 출력
검토에서 차단됐다. 완성 장면 전체가 통과한 케이스는 없다. 따뜻한 드림코어
주제와 학교형 복도 후보는 실제 이미지에서 확인했지만, 각각 동작 접촉과
그림자의 연결 관계에 실패가 남았다.

## 반영한 데이터

| 구분 | 결과 |
|---|---:|
| 원 조사 용어의 한영 의미 카드·키워드 경로 | 200 |
| 완전한 한영 시각 후보 | 133 |
| 개념·음향·시간 맥락 진단 항목 | 72 |
| 추가된 운영 레코드 | 205 |
| 선택형 슬롯 연결 | 250 |
| 최종 전체 운영 레코드 | 19,006 |
| 최종 positive CID / RID | 18,808 / 18,810 |

초기 128개 시각 후보와 72개 맥락 항목을 반영한 후, 개발 질의에서 확인한
구체 대안 누락을 보완했다. 추가 대안은 R17 거대 꽃, R18 부유 지형,
R27 넓은 화각과 깊은 초점의 동시 가독성, R29 표시 영상에만 한정된 채널
오프셋, R30 표시 영상의 압축풍 블록이다. 거대 꽃과 부유 지형은 각각
독립된 선택지다. 포괄적인 부모 용어는 진단 항목으로 보존했다.

각 후보는 전체 영문·국문, 소유자, 방향 있는 관계, 필요한 관측 단서,
혼동 경계, 주장 한계, 적용 조건·영향 범위를 보존한다. 모든 필수 요소를
함께 선택해야 하며, 일부만 보이거나 가려지면 전체 사례의 통과가 아니다.
시각 의미 그래프는 검토 메타데이터다. `native_approval=false`,
`native_qualification=not_qualified`, 사용자 수용 pending 상태를 유지했다.
이미지 한 장으로 소리, 시간 경과, 실제 운영 상태 등을 확정하지 않는다.

기존 18,801개 후보, 12,629개 연결과 슬롯·정책은 변경하지 않았다.
원 조사에서 비교한 기존 23개 CID도 보존했다. 인용 출처는 용어와 주변
맥락의 근거이며, 구체적인 허구 장면은 저술한 실현안이다. 초기 모듈의
provenance digest는 조사 사양을 가리키며 인용 웹페이지 원문 해시를 뜻하지
않는다. 원 연구 스냅샷의 사후 검증 결과를 구현 후 결과로 덮어쓰지 않았다.

주요 파일:

- [200개 시각 의미 레지스트리](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_liminal_dreamcore_semantics_20261022.json)
- [초기 후보 200개](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_liminal_dreamcore_20261022.json)
- [구체 대안 5개](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_liminal_dreamcore_realizations_20261022.json)
- [구체 대안 의미 레지스트리](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_liminal_dreamcore_realization_semantics_20261022.json)
- [유지보수·사용 설명](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/liminal-dreamcore-visual-semantics.md)

## 실행본과 보호 범위

최신 스킬의 SHA-256은
`7fe5b6cfc2da6e65dd9b9dc999e46d70a1fac7dce8c47157e53c1cba43b00f35`이며,
세 실험에서 같은 버전을 사용했다. 컨셉과 기본 프롬프트는 후보 검색 전에
각각 고정했다. 동일한 사용자 문구·입력 이미지 해시를 coordinator가 준비해
에이전트의 지시문이 사용자 문구로 바뀌지 않도록 했다. A/B의 최초
prompt-only 초기화 오류는 같은 기본 프롬프트와 코어 해시를 유지한 image
모드 재생으로 바로잡았다.

| 용도 | H-F2 generation | native generation |
|---|---|---|
| 세 이미지 실험 S1 | `53f50c9033d5939f1e4f148156f8ba5e7fb3b4e3cc2765fdce587f97c0cf2d1c` | `a6f034003d123a4deb3ed2bae900093b5b5de55a8f4f4990545f21b86c1914ef` |
| 최종 설치 S2, 구체 대안 5개 추가 | `9e8b0409f1fd05aa419bd3577a65b98d4b51a243c39154146a7bc6772862151d` | `b12b73dbf6d73b551ca3fe9ce13796601351ea44ab4f77f129932ef0079af4b3` |

두 실행본 모두 봉인·배포 실행본 검증을 통과했다. 검색·렌더링 엔진 코드
SHA는 기존 `96b67dedcfea019115cd46c6542287d7102e46cd12a486f1e817d79f3c634d0e`
그대로다. S2는 S1의 모든 기존 소스와 벡터를 보존한다. 이미지 실험은
S1에 고정되어 있으며 S2 추가 대안 5개는 이번에 픽셀 검증하지 않았다.

기존 보호 파일 3,638개에서 변경된 기존 파일은 모듈 목록, 검색 색인,
`retrieval-runtime.json` 세 개다. 모든 `CURRENT`와 참조 원본을 보존했다.
HEAD는 `ffa6f724324bfe0256208fb202568ce00cd9f040` 그대로이며 커밋·푸시는 하지 않았다.

## 검색 검증

원 연구의 개발·경계 사례 48개를 한국어와 영어로 각각 실행했다. 같은 로컬
임베딩 공간과 같은 전체 후보 풀 검색 엔진에서 총 96개 질의를 전후 비교했다.

| 지표 | 초기 반영 S1 | 구체 대안 보완 S2 |
|---|---:|---:|
| 개발 질의 64개에서 정확한 대상이 상위 8위 안에 존재 | 54 / 64 | 62 / 64 |
| 개발 질의에서 대상이 상위 96위 안에 존재 | 56 / 64 | 64 / 64 |

남은 상위 8위 밖 사례는 한국어의 불투명한 어두운 수면(E08, 40위)과
수면 아래 성인 인체(E32, 62위)다. 32개 경계 질의 중 17개에서는 전체 신규
후보 133개 중 인접 후보가 상위 8위에 노출됐다. 이번 추가 대안 5개는 그
경계 질의 상위 8위에 노출되지 않았다. 원문 적합성 판단과 실제 채택은
별도 절차다. 순위 범위 안에 있다는 사실은 샘플에 반드시 뽑힌다는 뜻이 아니다.

이 질의들은 같은 연구 패키지에서 작성한 개발 자료다. 독립 홀드아웃,
상위 8개 전체의 정확도, 채택 승인, 픽셀 품질을 입증하는 점수로 사용하지 않았다.

[검색 실행 결과와 남은 사례](/Users/chasoik/Projects/image-prompt/generated/maintenance/liminal-dreamcore-20261022-realization-gaps/combined-retrieval-results.json)

## 독립 이미지 테스트

세 에이전트가 서로 다른 영역에서 난수 조합으로 사건과 순간을 정했다.
모두 첨부 사진의 얼굴 외형·짧은 어두운 보브를 참고하는 허구의 성인 장면이다.
실제 인물의 나이·정체성·성격을 확정하지 않았다. 생성 전에 관측 기준과
최종 프롬프트 해시를 고정했고, partial은 완전 통과로 처리하지 않았다.

| 실험 | 독립 컨셉 | 신규 데이터 사용 | 실제 결과 |
|---|---|---|---|
| A | 침수된 심야 페리 터미널의 마른 문턱에서 끈으로 떠 있는 여행가방을 회수 | 신규 3개 노출. L043 두 계단·공유 계단참·닫힌 방화문 전체를 inspiration으로 반영 | 출력 검토 차단. 이미지 없음. 주제와 L043 픽셀 모두 관측 불가 |
| B | 빈 시골 학교 옷걸이실에서 과수원과 하늘 바닥으로 이어지는 문을 붙잡는 순간 | 신규 L111 노출. 닫힌 문·특정 문구가 현 장면과 충돌해 미채택 | 따뜻한 드림코어·경계·참조 외형 확인. 황동 추의 문 지지 접촉은 partial/fail. 전체 fail |
| C | 학교 기록 반환 창구에서 기록 속 외투가 현재 장부와 손에 그림자를 드리우는 순간 | 신규 3개 노출. L053 사물함 복도·어두운 창·불 켜진 게시함 전체를 inspiration으로 반영 | L053 배경 관계는 visible/pass. 그림자가 장부에만 있고 손을 가로지르지 않아 핵심 관계 partial/fail. 전체 주제 fail |

신규 데이터의 네이티브 승인 채택은 세 실험 모두 0개다. A/C는 H-F2
`inspiration_only`로 전체 의미를 사용했다. B의 새 데이터 직접 적용 효과는
입증되지 않았다. C에서는 선택한 신규 배경 후보의 실현을 확인했지만,
장면 전체와 네이티브 의미 승인으로 일반화하지 않았다. 이전 버전으로
생성한 비교 이미지가 없으므로 이미지 품질의 인과적 개선율도 계산하지 않았다.

| 실험 | 최종 영문 프롬프트 | 원 테스트·평가 자료 |
|---|---|---|
| A | [412단어 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/liminal-20261022-a-image/final_prompt_en.txt) | [보고서](/Users/chasoik/Projects/image-prompt/generated/photo-runs/liminal-20261022-a-image/report.json), [주제 기준](/Users/chasoik/Projects/image-prompt/generated/photo-runs/liminal-20261022-a-image/testcase.json), [L043 기준](/Users/chasoik/Projects/image-prompt/generated/photo-runs/liminal-20261022-a-image/source_testcase.json) |
| B | [영문 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/liminal-20261022-b-image/prompt_en.txt) | [국문 보고서](/Users/chasoik/Projects/image-prompt/generated/photo-runs/liminal-20261022-b-image/report_ko.md), [픽셀 평가](/Users/chasoik/Projects/image-prompt/generated/photo-runs/liminal-20261022-b-image/pixel-test-results.json) |
| C | [499단어 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/liminal-20261022-c-image/final_prompt_en.txt) | [국문 보고서](/Users/chasoik/Projects/image-prompt/generated/photo-runs/liminal-20261022-c-image/report.ko.md), [사전 기준](/Users/chasoik/Projects/image-prompt/generated/photo-runs/liminal-20261022-c-image/testcase.json), [픽셀 평가](/Users/chasoik/Projects/image-prompt/generated/photo-runs/liminal-20261022-c-image/pixel-review.json) |

부모 에이전트도 B/C의 실제 반환 파일을 열어 사전 기준으로 재검토했다.
평가 결과는 [B](/Users/chasoik/Projects/image-prompt/generated/maintenance/liminal-dreamcore-20261022/root-pixel-review-b.json)와
[C](/Users/chasoik/Projects/image-prompt/generated/maintenance/liminal-dreamcore-20261022/root-pixel-review-c.json)에 보존했다.
모든 사용자 수용 상태는 pending이다.

### 반환 이미지 B

![따뜻한 드림코어 B](/Users/chasoik/Projects/image-prompt/generated/photo-runs/liminal-20261022-b-image/image.png)

### 반환 이미지 C

![위어드코어 기록 창구 C](/Users/chasoik/Projects/image-prompt/generated/images/liminal-c-20261022/liminal-c.png)

## 오류와 다음 보완 지점

A는 `moderation_blocked`, `moderation_stage=output`, `categories=[other]`로
거부됐다. request ID는 `01810089-3933-4be2-b541-4e6041da04f1`이다. 도구가
구체적인 차단 요소를 제공하지 않아 원인을 추정하지 않았다. 오류 원문과
거절 시도 manifest를 보존했고 추가 생성이나 다른 제공자 호출은 하지 않았다.

C는 실제 이미지가 반환됐으나 이번 실험에서 C가 작성한 관찰 콜백이 출력 힌트의 디렉터리와 파일
경로를 합쳐 잘못 해석해 `preview_only`로 등록했다. 이미 종료된 operation에
실제 경로를 다시 등록하는 요청은 `native_operation_not_started`로 거절됐다.
원 관측, 정정 요청·거절, 실제 파일과 해시를 함께 남겼다. 생성 성공과
관리 기록 오류를 구분하며, ledger를 수동으로 고치지 않았다.

B의 문고정추는 문 하단·추·실내 바닥·문턱의 접촉과 지지 방향이 한 구역에
보이도록 연출할 필요가 있다. C의 그림자는 화면 가장자리에서 나오는 경로,
같은 손의 표면을 덮는 지점, 장부의 그림자를 하나의 연속된 연결로 보여야 한다.
현재 결과는 어울리는 사물과 분위기만으로 복잡한 접촉 관계를 보증할 수
없다는 점을 확인했다. 이 보고서에서 해당 실패를 통과로 승격하지 않았다.

후속 보완 후보는 한국어 검색 순위 2건, 소유자 사이 접촉의 화면 비중,
도구 관찰 콜백의 다중 경로 처리다. 이번 구현에서 검색·렌더링 엔진을
수정하거나 추가 이미지를 생성하지 않았다.
