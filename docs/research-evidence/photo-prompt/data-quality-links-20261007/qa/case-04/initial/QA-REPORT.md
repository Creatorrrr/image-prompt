사례 04의 독립 검증을 완료했다. coordinator가 만든 synthetic 요청을 원문 envelope에 바인딩한 사례이며, 인간이 직접 이 사진을 요청한 것으로 보고하지 않는다.

요청: 겨울 저녁 작은 기차역 플랫폼의 지붕과 빗물 자국을 찍은 사진. 사람은 없음.

| 구분 | 결과 | 근거와 한계 |
| --- | --- | --- |
| 기술 감사 | PASS | current-catalog feature validator와 runtime receipt를 사용한 composed audit가 성공했다. 실패 0개, 요청 앵커의 자유 서술 보존 경고 6개. |
| 관리 graph | PASS | 실제 원본 JSON에서 독립 복원한 2,971개 edge가 일치했다. 노출 후보 64개, 관련 프로필 32개, bundle 3개의 query 경로와 source_refs를 대조했다. |
| Freshness | PASS | --require-current는 current_verified로 성공했다. scratch report의 links.json 손상과 잘못된 source root는 실제 CLI에서 거부됐다. |
| 요청 의미 보존 | PASS | baseline 영어를 byte-identical로 유지하고 겨울 저녁·작은 역 플랫폼·지붕·빗물 자국·사람의 부재를 보존했다. |
| 작품 판단 | PARTIAL | 텍스트의 사진 방향은 일관되지만 이미지의 가시성·광학적 설득력·전체 작품 효과는 확인하지 않았다. |

pack_id는 `136870243d1ab4c2`, generation_id는 `2135faf8f2451eac73b90c447edbd496545d20d974c158f44ec67d98e9107f2a`, report_id는 `05adc9646d6aecab4c21571e9734e9262838e117de41c815f4f287de680a2a35`이다. 로컬 `core_bm25f` 검색으로 하나의 pack만 만들었고 이미지·embedding API를 호출하지 않았다.

저장된 sensual 1과 fetish 0을 override하지 않았다. 명시적 `no_people=true`로 두 축의 실효값은 0이며 creativity 1, surreal 0을 사용했다. `explicit_nonsexual=false`는 성적 내용 금지를 별도로 요청하지 않았다는 뜻이다. 카메라 방향·높이는 요청되지 않았으므로 advisory의 `unprescribed/open`, evidence `{}`를 유지했고 `--new-author-camera-evidence` 검사를 통과했다. 인체 메커니즘은 해당 없음이다.

동결 원본은 모두 같은 해시로 남아 있다. 입력 교정은 별도 파일에서 selection.catalog_path를 canonical wire 문자열로 바꾸고, user_exclusions의 영어 번역 people을 원문의 literal 사람으로 바꾼 두 건이다. baseline·앵커·assertion·요청 의미를 바꾸지 않았다. 교정 이유, 전후 해시, DATA 접근 이전 순서는 [INPUT-SCHEMA-CORRECTIONS.json](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-04/run/INPUT-SCHEMA-CORRECTIONS.json)에 있다. 독립 graph 해석기에서 단수 `hard_profile_id`까지 포함한 과정은 scratch 진단 교정이며 sealed skill이나 관리 코드는 수정하지 않았다.

graph에서 18개 노출 후보는 경로가 있었고 46개는 원본에도 bundle 참조가 없는 정상 미연결이었다. 후보→bundle→profile과 profile→bundle→후보는 source reference 경로를 뜻한다. 모든 실제 조회의 `meaning_support`는 `not_inferred`, `profile_activation`은 `independent_request_evidence_only`였다. raw JSON의 `hard_profile_id(s)` 이름만으로 전체 의미 충족이나 필수 활성화를 추론하지 않았다. 세 pack bundle과 다섯 optional visual concept를 모두 선택하지 않았으므로 opt-in obligation이 생기지 않았다. [독립 대조](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-04/run/independent_graph_comparison.json)와 [실제 query 결과](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-04/run/management_queries.json)에 원본 경로·출처 해시를 보존했다.

기존 retrieval 문제를 새 관리 도구 결과와 구분한다. `small_friend_group`와 `tight_elevator_group`은 실제 ineligible이므로 no_people guard 누락으로 확정하지 않았다. 반면 `slot:platform_framing:pr_casual_crop_subject_legibility_candidate`는 원본 en과 concept_units가 adult와 task-bearing action을 전제하며 for_any/guards/requires가 없는데, 이 객체·no_people core에서 eligible로 노출되고 near augmentation에 샘플됐다. 즉시 coordinator에게 알렸으며 채택하지 않았다. 원본 JSON pointer, 실제 concept_terms, applicability, compiled 조건은 [RETRIEVAL-EXPOSURE-ISSUE.json](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-04/run/RETRIEVAL-EXPOSURE-ISSUE.json)에 있다. 별도의 물체·상품 scope가 있는 손 작업 후보 등은 이 직접적인 인물 전제 누락과 구별했다.

최종 사진 방향은 지붕의 직선 구조와 누적된 불규칙한 물 흔적의 대비다. 작고 따뜻한 플랫폼 조명은 표면 흔적을 드러내고, 차가운 저녁광과 부차적인 선로·포장은 장소를 읽게 한다. 가까운 의미 검색 결과가 제안한 신체·군중·CCTV 인물·의복·신발·별개 장면은 이 물질 관찰을 강화하지 않아 제외했다. 겨울의 계절 식별성은 텍스트 지시와 차가운 저녁 분위기에 의존하며 실제 이미지에서의 충분성은 확인하지 않았다.

최종 영어 프롬프트:

An architectural photograph of the roof canopy of a small railway station platform on a winter evening. The roof and its rainwater stains are the main subject: dark, uneven runoff streaks descend along the fascia and spread beneath the roof seams, with pale dried tide lines edging the dampened patches. The canopy occupies most of the frame, while a narrow strip of platform paving, one supporting post, and the parallel rails establish its modest station setting. A single warm platform lamp draws out the overlapping stain edges and the slight roughness of the roof surface against the cold blue-gray dusk. The platform is empty, its paving carrying a subdued wet glimmer. Preserve the quiet difference between a working shelter's straight structure and the irregular water traces that have accumulated on it. Natural tonal transitions and legible surface texture make the photograph feel observed and still, with the surrounding station kept subordinate to the stained roof.

영어 prompt 본문 SHA-256: `8a464da6bae94ed8bdb2dc8039d80136f7fbcd6b08674056b254ce1f295ccf2c`. [composed_prompt.json](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-04/run/composed_prompt.json) 및 [최종 영어 파일](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-04/run/final_prompt_en.txt)에 저장했다.

이미지 픽셀과 사용자 수용은 검증하지 않았다. 기술 PASS나 graph 연결은 이미지 품질·요청 의미의 전체 충족·사용자 선호를 증명하지 않는다.
