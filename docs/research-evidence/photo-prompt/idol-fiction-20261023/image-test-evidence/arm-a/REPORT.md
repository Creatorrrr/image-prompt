# 독립 이미지 테스트 A — 음악방송 리허설

실제 참고파일을 첨부해 네이티브 이미지 1장을 생성하고 저장했다. 넓은 아이돌 공연·제작 현장 주제와 참고 외형은 읽히지만 사전 strict 기준은 3 PASS / 2 FAIL이므로 완전 통과가 아니다. 신규 데이터는 검색에 노출되었으나 최종 프롬프트에는 사용하지 않았다. 따라서 이 결과로 데이터 반영에 따른 이미지 품질 향상을 입증할 수 없다.

## 산출물

- 실제 이미지: `images/idol-rehearsal-native.png` (1024×1536 RGB PNG)
- 최종 실제 전송 프롬프트: `final-prompt.txt`
- 도구 호출: `image_gen.imagegen`, 1회. 참고파일은 `referenced_image_paths`에 실제 첨부했다.
- 실제 returned 원본: `/Users/chasoik/.codex/generated_images/01a1691b-6b5e-7ca0-8414-7c355b199e0b/exec-47e9e986-ab0c-40e0-b5cb-fb47e25276af.png`; 원본을 남긴 채 arm 안으로 복사했다.
- 이미지 SHA256: `675930012322b27b668b91e659091d09cfbdb68788333d3bdf6c28b6cc4900e1`
- 실제 이미지 모델명은 도구 응답에서 관찰되지 않았다. transport의 요청 메타데이터를 관찰된 모델명으로 대체하지 않는다.

## 독립성과 controls

OS-backed seed `9522969309174889366`로 독립 작성한 네 라이브 방향 중 음악방송 리허설을 골랐다. `random-concept.json`, `independence.md`, `prefreeze-evidence-hashes.json`에 기록했다. 라이브 영역 배분과 리허설·crew·세 명의 그룹·의상·카메라는 agent-owned 선택이다. 다른 arm의 코어·프롬프트·후보·이미지를 읽지 않았다.

현재 요청의 원문 bytes와 coordinator envelope를 그대로 보존했다. 이전 실제 사용자 메시지의 긍정 주제 `아이돌물`은 topic-context/v1의 discovery 링크로만 사용했다. 에이전트 콘셉트를 사용자 정의나 원문으로 바꾸지 않았다. 참고 사진은 보이는 얼굴·헤어 외형만 사용했으며 실제 신원·나이·생애·성격을 추정하지 않았다. 허구 주인공의 24세 설정은 창작 선택이다.

저장 controls는 sensual 1 / fetish 0 / creativity 1 / surreal 0, emphasis auto→sensual_led, viewer_experience false, reference_edit_mode off, trend_layer off이다. snapshot canonical SHA256는 `323352cd19af1174b25db20c51b01119910294853fbe9235fb7e42125bdf2a2b`이다. 주인공의 매력은 표현·시선·조명·재킷의 질감이 작업 장면을 지지하는 정도로 설계했다. 실제 인상은 공연 사진의 글래머와 human appeal이 있으며, controls 수치와 사용자 선호를 픽셀에서 증명했다고 주장하지 않는다.

## 고정·검색·사용 구분

독립 baseline, core, feature selection 8개, embodiment review, 사전 픽셀 기준을 후보 접근 전에 freeze했다. neutral selection 감사는 경고 없이 통과했다. core canonical SHA256는 `4c024b30410142d7b6bcea70d81007e42ec7105fa2efeaeee7aa26402824ebfd`이다.

명시적으로 고정한 H-F2 generation은 `1d1802f68050e7c3034b0a4f55d3d3221575e81e343ee1433f2229225878d138`, native generation은 `a96224b17d1d894276583b0602462e39b3cde4bb80be8a35e0f2c58a956c894d`, store는 `/Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed`이다. 기본 포인터를 변경하지 않았다.

situation_context·visual_hierarchy 두 slot과 requester topic·baseline 두 whole-scene query, 총 4개의 독립 검색에서 32 occurrences / 27 distinct sources가 반환되었다. 모든 소스의 전체 명제·EN/KO 의미·조건·effects·소유자·끝점·claim limit을 검토하고 각 occurrence별 판단을 남겼다. `material-view.json`, `source-reviews.json`, `composed.authored.json`, `composition-comparison.md`에 원본과 판단이 있다.

신규 아이돌 데이터 노출은 다음 6 CID / 9 occurrences다.

| research ID | CID | 노출 query | 최종 사용 |
|---|---|---|---|
| I112 | cand_dcacd3baf99b5c78a52f459bf0b01362 | situation_context | skip |
| I013 | cand_e2f81522ccf653409d7c0ebf3ea75035 | situation_context | skip |
| I007 | cand_f47c8eb9d95154049a869b03d1a8c3c9 | situation_context, visual_hierarchy, __baseline_prompt__ | skip |
| I036 | cand_5b0c7ddd0be05ea0b01e7c7b904c13ef | visual_hierarchy, __baseline_prompt__ | skip |
| I006 | cand_257f80c76c65560985aa816848675a67 | __baseline_prompt__ | skip |
| I033 | cand_683c38a288185f42bcd337075fbf3469 | __baseline_prompt__ | skip |

requester topic query에서는 신규 CID가 0개였다. 일반적인 테스트·컨셉 표현의 noise가 컸고, 신규 노출은 slot 또는 baseline query에서 일어났다. 신규 소스 모두 `native_approval:false` / `not_qualified`를 보존했다. 이 표는 discovery 노출이며 native whole-source 채택 자격이나 이미지 사용을 뜻하지 않는다.

완전한 프롬프트 대안 두 개(가까운 press형 프레이밍, I112의 색 구분 counterfactual)를 baseline과 비교했다. 가까운 구도는 외형을 키우지만 바닥·지지 관계를 잃고, 세 담당색과 개별 마이크는 멤버 구분을 늘리는 대신 손 큐·주인공의 우선순위를 분산시킨다. native 권한이 부여되었다고 간주하지 않고 원안을 선택했다. `used_new_CIDs=[]`, 모든 material use는 skip, `chosen_candidate_ids=[]`, `chosen_visual_concept_ids=[]`다. final prompt는 독립 baseline과 bytes가 동일하고 SHA256 `102a474b4f0c3d58a23b9f988e24521b0cb7f12e5c9e2dbdbfe844964937bbd3`이다.

compose-audit와 prepare-render는 PASS였다. compose의 quality warning 네 개는 frozen intent가 후보 선택 없이 authored evidence로 보존된다는 uncovered_intent 경고다. 이 PASS는 입력·문구·binding 감사이며 픽셀 성공 판정이 아니다.

## 실제 픽셀 평가

원본 저장 이미지, 전체 thumbnail, 무보간 native crop(얼굴·마이크, 손 큐, 지지발)을 직접 view_image로 확인했다. crop은 평가용 파생파일이며 원본을 편집하지 않았다. 최초 독립 평가를 `strict-pixel-review.json`에 그대로 남겼다.

| 사전 기준 | 판정 | 실제 픽셀 근거 |
|---|---|---|
| A1 아이돌 working life | PASS | 세 공연자·matching stage wardrobe·마이크·floor mark·헤드셋 crew가 같은 제작 공간에 보임 |
| A2 연결된 count-in | FAIL / partial | 큐 손과 lead mic는 보이나 eye-line이 아래쪽 손 큐 위치로 명확히 수렴하지 않아 정확한 endpoint 관계가 불명확 |
| A3 참고 외형 | PASS | dark bob·wispy fringe·dark eyes·soft oval face 등 major cues를 native crop에서 대조 가능; identity 증명 아님 |
| A4 전체 지지·동작 상태 | FAIL | support boot는 X 위에 있으나 뒤 boot의 발끝과 뒤꿈치가 함께 떠 있어 light heel-lift waiting stance보다 큰 동작임 |
| A5 사진 위계 | PASS | lead 전신·얼굴, 분리된 손 큐, rear group 및 stage work context가 함께 읽힘 |

A4는 해부학적 기괴함이나 불가능한 균형을 주장하는 실패가 아니다. 한 발로 선 신체 자체는 개연적이지만, 사전에 의도한 특정 발 지지·동작 상태가 완전히 재현되지 않았다. A2의 일부 visible evidence만으로 전체 관계 PASS를 만들지 않았다. 한 장의 사진은 이전 실수·실제 재시작 시점·노래 소리·직업·정확한 나이 등을 입증하지 못한다.

관리형 embodiment review도 exact saved image에서 다시 기록했다. 의도한 support state 불일치를 숨기지 않고 `embodiment_support_and_balance=fail`, 나머지 네 gate는 visible/pass로 제출했다. 최종 review-audit는 `status=pass / record_valid=true`로 실패 관찰 기록의 형식을 검증했고, `technical_qualification=fail`을 보존했다. 4 gate PASS / support-and-balance 1 gate FAIL이며, workflow는 `review_record_validated`와 `stale_roles=[]` 상태다. `review-audit-output.json`에 실제 결과가 있다.

## Recorder와 결론 경계

최신 sealed recorder가 `image_runs.ndjson`와 `run_manifest.json`에 `candidate_pack_version=h-f2-v2`, 실제 call_count 1, cross_arm_inputs_used false, exact core/lock/prompt/reference/image hashes를 기록했다. ledger run ID는 `ae53ec23565e440f`다. `recorder-evidence-validation.json`의 10개 binding·hash·version·독립선언 검증은 PASS다. manifest의 success는 실행과 저장 성공이며 scene 합격이나 사용자 수락이 아니다.

사용자 선호·수락은 `pending / not_yet_received`다. 실제 생성 baseline 비교가 없고 최종 prompt가 신규 소스를 사용하지 않았으므로 데이터에 의한 품질 향상, native qualification 또는 사용자 선호 향상을 주장하지 않는다. 재시도·우회·추가 image call은 하지 않았다.
