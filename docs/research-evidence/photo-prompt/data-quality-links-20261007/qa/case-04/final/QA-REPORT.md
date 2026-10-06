사례 04의 round-2 독립 재검증을 완료했다. 새 분리 root에서 같은 동결 요청·baseline·core 의미·creative controls·feature selection·embodiment review를 사용했다. 초기 run 증거, ISOLATION.json과 precore-frozen snapshot은 보존했다.

요청: 겨울 저녁 작은 기차역 플랫폼의 지붕과 빗물 자국을 찍은 사진. 사람은 없음.

| 구분 | 결과 | 확인 내용 |
| --- | --- | --- |
| 공식 기술 감사 | PASS | feature validator 및 새 runtime receipt를 사용한 composed audit 성공. 실패 0개, 앵커 자유 서술 보존 경고 6개. |
| 관리 graph | PASS | 원본에서 독립 복원한 2,971개 edge, 노출 후보 64개·관련 프로필 29개·번들 3개의 실제 양방향 query 경로와 source_refs가 일치. |
| Freshness·거부 | PASS | --require-current는 current_verified. scratch report의 links.json 손상과 wrong source root를 실제 CLI에서 거부. |
| 요청 의미·영어 보존 | PASS | baseline과 final prompt byte-identical. 지붕·물자국·작은 역·겨울 저녁·사람 부재 및 unprescribed/open 카메라 검토 유지. |
| 수정 대상 no_people guard | PASS | 두 후보 모두 exact frozen 문맥에서 explicit_no_people, eligible=False, public pack 전체에서 미노출. |
| 작품 판단 | PARTIAL | 텍스트의 방향은 일관되지만 이미지가 없어 실제 가시성·계절·빛·작품 효과 미검증. |
| 다른 기존 advisory 노출 | PARTIAL | 다른 adult actor 전제 후보의 의미 불일치를 별도 기록하고 전부 미채택. 관리 graph 오류와 구분. |

pack_id는 `a997327a635ba1dd`, generation_id는 `db193081d04dba97d754e8809cebfb67a97133c7162a5429da965d53e9c88462`, report_id는 `79e7c2d2309d5d66fa01d46cb396719c88bdbed3116338d3138d894815faa262`이다. 새 runtime generation은 staged generation과 같은 값이었다. 로컬 lexical 검색만 사용했으며 API·이미지·네트워크 호출은 없었다.

`pr_casual_crop_subject_legibility_candidate`와 `rb_shared_wind_response_candidate`의 실제 원본·compiled `kind`와 `for_any`는 각각 human이다. frozen primary object/no_people 계약으로 실행한 실제 guard는 둘 다 `explicit_no_people`를 반환하고 `core_slot_entry_eligible=False`였다. slots·creative augmentation·bundle member·public pack 어느 곳에도 두 ID가 남지 않았다. [guard 증거](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-04/round-2/run/human_candidate_guard_verification.json)에 원본 pointer·hash·조건과 실제 결과를 저장했다. 이 확인은 두 대상의 수정 성공 범위이며 전체 후보 사전의 모든 인물 조건이 완성됐다는 주장으로 확대하지 않는다.

관리 보고서는 source reference 경로를 공개한다. 원본 JSON의 candidate_ids/candidate_slots와 단수·복수 hard_profile_id(s)를 독립 해석해 모든 2,971개 edge를 확인했다. 이번 노출 후보는 경로 있음 17개, 원본에도 bundle 참조가 없는 정상 미연결 47개다. 실제 query의 `meaning_support=not_inferred`와 `profile_activation=independent_request_evidence_only`는 유지된다. bundle 연관을 전체 의미 충족·필수 활성화·현재 요청에서의 후보 적합성으로 승격하지 않았다. 세 bundle과 다섯 optional visual concept를 모두 미채택했으므로 추가 hard obligation은 생기지 않았다. [원본 대조](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-04/round-2/run/independent_graph_comparison.json)와 [query 결과](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-04/round-2/run/management_queries.json)를 보존했다.

잔여 기존 검색 품질은 별도다. `hr_horror_comedy_task_contrast`의 adult actor와 `hr_mockumentary_evidence_display`의 adult interview subject는 현재 객체/no_people 사진과 맞지 않지만 kind/for_any가 없는 eligible 후보로 보인다. `hr_vampire_identity_variant`도 adult 둘의 관계를 전제하는 다른 장면이다. 모두 채택하지 않았으며 원본 pointer·조건·concept_units·applicability는 [잔여 노출](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-04/round-2/run/residual_advisory_exposure.json)에 있다. cello-specific 동작 계약은 이 건축 사례에서 실제 요청으로 실행하지 않았으므로 별도 의미 검증의 성공을 주장하지 않는다.

작성 판단은 이전과 같다. 지붕의 직선 구조와 누적된 불규칙한 물 흔적을 주된 관계로 읽고, 따뜻한 작은 플랫폼 조명과 차가운 저녁광으로 표면을 드러내며, 포장·기둥·선로는 장소를 설명하는 부차적 요소로 남긴다. 새 후보가 제안한 중앙 안전 크롭·필름 입자는 가능하지만 현재 표면 관찰을 개선한다는 근거가 약하다. 영상 시간 단서·fresh-use mystery·유리 접촉 얼룩은 다른 목적이나 trace owner를 추가하므로 선택하지 않았다.

최종 영어 프롬프트:

An architectural photograph of the roof canopy of a small railway station platform on a winter evening. The roof and its rainwater stains are the main subject: dark, uneven runoff streaks descend along the fascia and spread beneath the roof seams, with pale dried tide lines edging the dampened patches. The canopy occupies most of the frame, while a narrow strip of platform paving, one supporting post, and the parallel rails establish its modest station setting. A single warm platform lamp draws out the overlapping stain edges and the slight roughness of the roof surface against the cold blue-gray dusk. The platform is empty, its paving carrying a subdued wet glimmer. Preserve the quiet difference between a working shelter's straight structure and the irregular water traces that have accumulated on it. Natural tonal transitions and legible surface texture make the photograph feel observed and still, with the surrounding station kept subordinate to the stained roof.

영어 본문 SHA-256: `8a464da6bae94ed8bdb2dc8039d80136f7fbcd6b08674056b254ce1f295ccf2c`. [최종 영어 파일](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-04/round-2/run/final_prompt_en.txt)과 [composed_prompt.json](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-04/round-2/run/composed_prompt.json)에 저장했다.

이미지 픽셀과 사용자 수용은 검증하지 않았다. [초기 증거 보존 확인](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-04/round-2/run/initial_run_evidence_preservation.json)에는 기존 QA의 26개 artifact 해시와 ISOLATION/precore-frozen/새 sealed source 보존 결과가 있다.
