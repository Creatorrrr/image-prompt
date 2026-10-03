arm_b 최종 결과는 **FAIL**이다. 네이티브 이미지 2개를 실제 생성·저장했고 두 원본을 전체 화면과 native original로 직접 검사했다. 세이렌의 사람–새 연결과 키마이라의 사자–염소–뱀 연결은 읽히지만, 두 번째 이미지에서도 세이렌 왼쪽 날개 일부가 프레임 밖으로 이어졌다. 사전 `whole_structure_visibility` 기준을 확인할 수 없으므로 `partial_is_fail=true`에 따라 전체 통과로 올리지 않았다.

컨셉은 현대 박물관 블랙박스의 정교한 애니매트로닉 무대다. 노래가 멎은 가상 성인 사람 머리의 새 세이렌과 사자 몸·등의 염소 머리·뱀으로 끝나는 꼬리를 가진 키마이라가 같은 바닥 위에서 독립된 몸을 드러낸다. 이 라벨·형태 변형·수량·무대·카메라는 사용자 의미 정의가 아닌 이 arm의 독립적인 구체 시험 선택이다.

난수 절차는 저장된 `1817895734`를 사용한 CPython `random.Random(seed)` → `randint(2,3)` → `sample(term_pool,n)`이며 재추첨하지 않았다. 선택 수는 2, 순서는 **그리스 세이렌 → 키마이라**였다. 원문 `request_envelope.json`은 수정하지 않았으며 요청 UTF-8 SHA-256은 `3b1ed5fc3c3b175976aedc3a3860a11e9e6c563a55ebab85c1c10b2ad1cd697a`다.

세이렌의 인간 머리와 새 몸·발이라는 선택 범위는 [Met 큐레이터 인터뷰](https://www.metmuseum.org/ko/perspectives/dangerous-beauty-interview-with-kiki-karoglou)의 고대 유형 설명을 확인했다. 키마이라의 사자 몸·등 가운데 염소 머리·뱀 머리로 끝나는 꼬리는 [Getty 도상 레코드](https://www.getty.edu/cona/CONAIconographyRecord.aspx?iconid=901000661)를 확인했다. 이 공개 자료는 용어의 형태 경계를 확인하는 데만 썼고 박물관 무대 컨셉을 공급받는 검색에는 쓰지 않았다.

참조 사진은 `view_image`로 보고 가상의 명시적 성인 세이렌에 보이는 짙은 눈, 얼굴 외형, 짧은 검은 단발과 잔 앞머리의 외형 단서로만 연결했다. 실제 신원·나이·종교·동의·인격·체형 및 사용자 선호를 추론하거나 판정하지 않았다.

사전에는 요청/참조/시험 라벨, 두 SKILL.md, 중립 카탈로그·controls 정의와 resolver, 필요한 1차 공개 자료만 접근했다. 8개 중립 범주를 baseline 전에 선택했다. core, controls, embodiment와 범주·관찰 기준을 동결한 다음 precore validator가 `valid=true`, `warnings=[]`를 반환했다. 동결 완료를 root에 전달한 뒤 data ready 조건이 충족되어 post-core에 접근했다. 타 arm 프롬프트·이미지·후보 파일은 읽지 않았다.

하나의 현행 v6 pack `2983d23e47c6eac8`에서 실제 상세를 읽고 다음을 채택했다.

- 구도: `slot:composition:ri_chimera_topology_readable_composition`
- 구도: `slot:composition:ri_siren_human_bird_readable_composition`
- opt-in 시각 프로파일: `visual-concept:ri_chimera_topology`
- opt-in 시각 프로파일: `visual-concept:ri_siren_human_bird`

다른 종교 인물, 스핑크스, 거울, 성격 반응, 의상·발·손 후보는 장면에 맞지 않아 거절했다. 후보명 출현을 픽셀 성공으로 취급하지 않았고, 선택한 프로파일의 구성요소와 렌더 게이트 전체를 적용했다. 노출된 후보/프로파일과 채택 목록은 `candidate_exposure_adoption.json`, 상세 읽기는 `composer_details_ri.json`과 `composer_details_profiles.json`에 남았다.

| 단계/시도 | 결과 |
| --- | --- |
| precore validator | PASS, 경고 없음 |
| 시도 1 composed/runtime 감사 | PASS/PASS |
| 시도 1 native 생성 | 성공한 원본 파일 보존; 픽셀 전체 FAIL |
| 시도 1 결함 | 왼쪽 날개와 꼬리 끝이 프레임에서 잘림 |
| 시도 2 composed/runtime 감사 | PASS/PASS; 366단어에 대한 권고 예산 경고 보존 |
| 시도 2 native 생성 | 성공한 원본 파일 보존; 픽셀 전체 FAIL |
| 시도 2 개선/잔여 결함 | 꼬리 끝과 바닥 여백 개선; 왼쪽 날개 외곽 잘림 잔여 |

두 번째 독립 원본의 custom 관찰 기준은 11개 중 **10 PASS / 1 UNOBSERVABLE**, 표준 effective 렌더 게이트는 11개 중 **9 pass / 2 fail**이다. 실패 게이트는 `vo_ri_siren_human_bird_2`, `embodiment_visibility_and_projection`이며 표준 리뷰 감사의 `schema_failures=[]`이다. 세 개의 키마이라 도상 게이트는 같은 두 번째 이미지에서 모두 pass다. 첫 이미지의 구성요소를 두 번째 이미지와 합쳐 통과시키지 않았다.

수정은 한 번만 했다. 요청·core·intent·pack·negative·채택 IDs·모든 통과 접합을 유지한 채 camera/framing 여백 문장만 바꾸었다. 원래 시도와 정확한 변경 범위는 `retry_lineage_attempt_2.json`에 보존했다. 실제 도구 호출은 총 **2회**, 도구는 모두 `image_gen.imagegen`이고 fallback이나 모델 변경은 없었다. 도구 생성 성공과 렌더 충족을 분리했다.

최종 검토 대상 파일은 다음과 같다.

- 이미지: [image_attempt_2.png](image_attempt_2.png), SHA-256 `cd31b2e4e1e6bf97fcdde52207b756e040231ea764bdfcd472039dfda869f5ba`
- 첫 이미지: [image_attempt_1.png](image_attempt_1.png), SHA-256 `e0dabc87014a6d39445531d6164e5dcde1d188745100b417160a6548e25e5561`
- 독립 테스트 기준: [test_case.json](test_case.json)
- 최종 standalone prompt: [standalone_prompt.txt](standalone_prompt.txt); 두 시도별 prompt도 보존
- negative bytes: [negative_prompt.txt](negative_prompt.txt)
- 최종 픽셀 리뷰: [pixel_review.json](pixel_review.json)
- 최종 표준 리뷰 감사: [render_review_audit_attempt_2.json](render_review_audit_attempt_2.json)
- 최종 runtime 요청: [final_runtime_request.json](final_runtime_request.json)
- 원본·수정 composed/runtime 감사: `composed_audit.json`, `runtime_audit.json`, `composed_audit_attempt_2.json`, `runtime_audit_attempt_2.json`
- 두 native 원본의 source/save/hash metadata: `native_result_attempt_1.json`, `native_result_attempt_2.json`
- arm 내부 원장·manifest: [image_runs.ndjson](image_runs.ndjson), [run_manifest.json](run_manifest.json), 원래 시도의 `run_manifest_attempt_1.json`

핵심 binding은 core `689b212aefa05d45b7cf1f5f1e5b4c213f65d6d1a1f8918e52f72879c8d2fe70`, intent `c502a7f3f384c486a3dca7accd1f35cc34512d4ab3ed5e8d5bec3e0a5f21243e`, retrieval `4aa2581f1b534affdec2d26c184f06c6382944641b1ec515f9f5a6e6366eeaa9`, effective visual contract `9d5fbc1c8cabe6ce7d9e250e0385e0bacfc08cc220a80a3b45e2eea4d855f3fe`이다. `artifact_integrity_check.json`에서 동결한 모든 파일의 원래 해시, 원본/최종 prompt, negative bytes, 두 image hashes와 시도 간 동일 binding·채택 IDs를 확인했다.
