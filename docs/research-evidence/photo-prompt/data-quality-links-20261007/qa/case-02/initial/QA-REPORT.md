case-02 독립 검증은 기술 audit·구조 그래프·freshness·요청 의미에 PASS, 영어 초안의 예술적 판단에 PARTIAL을 부여했다. 확인한 범위에서 구현 버그는 발견하지 않았다. 이미지 픽셀과 사용자 수용 증거는 없다.

입력은 coordinator가 만든 synthetic QA 주제이며 실제 인간이 이 사진 주제를 직접 요청했다고 간주하지 않았다. 원문은 다음과 같다.

> 오래된 구리 주전자와 접힌 리넨을 이른 아침 자연광으로 찍은 사진. 사람은 없음.

| 구분 | 판정 | 독립 근거 |
| --- | --- | --- |
| technical audit | PASS | 공식 pre-core validator 통과, composed audit failures=[], baseline 116단어 바이트 보존 |
| graph accuracy | PASS | 노출 64개: 연결 17개·정상 미연결 47개, 원본 재구성 2,971개 간선 및 13,517개 노드 양방향 목록 일치 |
| freshness | PASS | --require-current 3건 성공, 복사 보고서 checksum 손상과 잘못된 root 각각 실제 거부 |
| request/meaning fidelity | PASS | 구리·리넨·접힘·이른 아침·자연광·사람 제외 보존, 카메라 unprescribed/open/open 및 빈 evidence |
| artistic judgement | PARTIAL | 재질과 형태 관계는 일관되나 천에 이어지는 창문 반사의 광학적 표현이 모호하며 실제 화면 검증 없음 |

원본 동결은 2026-10-06T16:40:56+00:00에 이루어졌다. 이후 원본 파일은 바꾸지 않고 사본에서 catalog_path의 canonical identifier와 user_exclusions의 people → 사람만 기술적으로 교정했다. 첫 생성 시도의 exclusion 거부는 DATA를 읽기 전 발생했다. 의미·영어 baseline·anchor·assertion은 보존되었고 normalizer가 추가한 request_binding/core_id/hash를 별도로 기록했다. 교정의 시각·이유·원본/사본 해시는 SCHEMA-CORRECTIONS.json에 있다.

실제 pack은 자체 로컬 runtime에서 lexical BM25F 방식으로 생성했다. generation_id는 `2135faf8f2451eac73b90c447edbd496545d20d974c158f44ec67d98e9107f2a`, pack_id는 `7f3c7b8e9d3f7b53`이다. 동일 receipt generation으로 관리 보고서를 build했으며 보고서가 가리키는 source_root와 runtime_store는 모두 이 case-02 폴더 안에 있다.

그래프 검사는 관리 링크 모듈을 import하지 않고 원본 JSON의 candidate_ids/candidate_slots 및 hard_profile_ids/hard_profile_id 선언으로 재구성했다. 원본과 보고서 inputs의 바이트 해시 96개도 대조했다. 최초 독립 검사에서 빠졌던 단수 hard_profile_id 형식 71건은 검사기의 입력 형식 범위를 보완해 재검사했으며, 최초 결과와 보완 기록을 보존했다. 보고서 오류로 오인하여 숨기거나 관계를 임의 생성하지 않았다.

리넨 후보 `slot:surface_material:linen_fabric_surface`는 원본에도 번들 연결이 없고 현재 조회는 path_count=0으로 정상 성공했다. 연결 후보 `slot:prop:mg_collage_edges`와 반대 방향의 `profile:mg_collage_edges_relation` 조회는 동일한 3노드 경로를 돌려준다. 조회는 meaning_support=not_inferred, review=unreviewed, profile_activation=independent_request_evidence_only를 보존한다. 번들 경유 연관은 모든 component/relation의 의미 충족이나 필수 profile 활성화 근거가 아니며 optional 후보·bundle·visual concept은 모두 비채택했다. composed audit의 effective_visual_contract_sha256도 null이다.

freshness의 실패 대조는 scratch 보고서 사본에만 수행했다. JSON의 의미는 같은 상태에서 links.json 끝에 줄바꿈을 추가하자 `report_invalid: report member checksum mismatch: links.json`으로 거부했다. 다른 scratch root를 지정한 정상 보고서 조회도 `report_not_current: report authority/root differs from requested source`로 거부했다. 정상 보고서와 sealed skill의 원본 바이트는 유지했다.

공식 composed audit의 8개 경고는 candidate pack이 알고 있는 표현에 없던 필수 의미가 최종 자유 서술/assertion으로 보존되었다는 내용이다. 최종 필수 의미가 빠졌다는 증거나 예술적 성공의 증거로 해석하지 않았다. 관리 보고서의 review 46건도 이 장면의 실패 판정으로 자동 전환하지 않았다.

예술적 검토에서는 구리의 곡면과 리넨의 평평한 층, 사용 흔적과 건조한 결, 조용한 빛이 연결되는 점을 긍정적으로 보았다. 틴트·노이즈·세탁 바구니·콜라주를 더하지 않은 선택은 요청의 정적 성격에 맞는다. 다만 창문 반사가 천의 윗 접힘으로 이어지는 구절은 확산광인지 반사광인지 다소 모호하고, 익숙한 창가 정물 이상의 독창성을 강하게 입증하지 않는다. 픽셀·사용자 수용 검증 없이 예술적 완성을 PASS로 단정하지 않았다.

최종 영어 프롬프트는 동결 baseline과 동일하다.

An object-only still-life photograph of an old copper kettle beside a length of linen that lies folded, lit by natural light in the early morning. Both rest on a pale stone windowsill. The kettle's curved flank carries small rubbed patches and darkened seams; the linen's stacked folds reveal a coarse, dry weave. A soft window reflection runs along the copper curve and falls across the upper fold, making the metal's rounded volume answer the fabric's flat layers. The kettle holds the visual center, with a small interval of stone separating it from the linen. Cool, quiet shadows remain readable against a plain, dim interior background, while the warm copper and off-white cloth retain their natural colors.

주요 증거 파일: QA-RESULT.json, composed_audit.json, independent-graph-check.json, normalization-preservation-check.json, freshness-mutation.json, SCHEMA-CORRECTIONS.json, 각 *-command.json 및 *-stdout.log/*-stderr.log. 상세 절대 경로와 SHA-256은 QA-RESULT.json에 기록했다.
