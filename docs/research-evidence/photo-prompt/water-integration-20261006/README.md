# 물 의미·후보 반영 및 독립 렌더 검증

[최종 보고서와 이미지 3장](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/REPORT.md), [기계 판독용 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/TEST-SUMMARY.json)를 작성했다. 독립 에이전트 3개의 최종 이미지에서 선택된 물 조건 21개와 신체·접촉·지지 조건 15개가 모두 통과했다. 실제 생성은 4회, 추가 장면 기대는 14/17, 관련 코드·계약 검사는 40개 통과했다. 과수원의 발판은 한 번 수정했으며 수정 전 이미지와 실패 기록도 보존했다.

117개 후보와 117개 시각 의미 프로필을 실제 skill에 등록하고, semantic index 10,284개와 visual index 2,081개를 갱신했다. 기존 원본 record는 유지하고 더 완전한 대상·접촉·광원·수면·장비 관계를 좁은 sibling으로 추가했다. 351개의 구성 요소별 native gate는 선택된 프로필에서만 의무가 된다.

- [반영 상태](INTEGRATION-STATUS.json), [채택 ledger와 효과 범위](ADOPTION-LEDGER.json), [설치와 보존 증거](INSTALLATION.json), [실제 경로와 독립 snapshot 일치](LIVE-FROZEN-PARITY.json)
- [추가 근거와 해석 한계](SOURCE-SUPPLEMENT.md), [연구 원본](../water-semantics-20261006/README.md)
- [물 회귀 검사](water-discovery-tests-final.log), [사전 검사](live-dictionary-discovery-final.log), [최종 local runtime 등록](live-runtime-final.json)
- 독립 arm: [1](arm-1/CASE.json), [2](arm-2/CASE.json), [3](arm-3/CASE.json)

각 arm은 동일한 실제 사용자 문장과 reference를 사용하지만, 독립 난수와 독립적인 기본 프롬프트/core를 후보 접근 전에 작성했다. 다른 arm의 프롬프트·후보팩·이미지는 전달하지 않았다. 컨셉·기대 관찰·표현의 구체화는 agent의 테스트 설정이며 요청자 정의로 바꾸지 않았다.

첫 검색에서 일반 물 후보는 노출됐지만, 새 visual profile의 component match terms가 전체 문장에 치우쳐 자연스러운 형태 설명을 찾지 못했다. 수정 전 pack/receipt를 각 arm에 보존했다. 36개 프로필의 검색용 짧은 양성 성분 표현을 보강했으며, 기존 필수 evidence와 모든 native gate는 유지했다. core와 CASE를 바꾸지 않고 같은 seed로 새 데이터 generation에서 최종 pack을 만들었다. source revision 때문에 기존 full-discovery 도중 나온 실패는 전체 PASS로 보고하지 않고 별도 재검증·분석한다.

프롬프트 감사, runtime input 감사, 생성 성공, 실제 native 픽셀 만족, 미적 판단, 요청자의 수용은 각각 구분한다. 이번 결과는 채택한 물 프로필 7개와 세 장면의 픽셀 검증이며 전체 117개 프로필의 검증이나 요청자의 수용을 뜻하지 않는다. 연구의 30개 비가시적 context와 45개 family는 서로 다른 변형을 고정된 필수 형상으로 뭉치지 않았다. 전체 검사 실행은 데이터 변경 시점이 섞여 중단했으며 전체 통과로 보고하지 않는다.
