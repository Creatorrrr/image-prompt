arm_c 결과는 **FAIL**입니다. native 이미지 호출 2회는 모두 저장에 성공했지만, 최종 원본의 12개 ALL_OF 조건은 PASS 7 / FAIL 3 / UNOBSERVABLE 2였습니다. `partial_is_fail=true`이며 두 시도의 요소를 합쳐 통과로 처리하지 않았습니다.

컨셉은 **생명실이 끊어진 뒤 열린 문 / The Gate After the Thread**입니다. 현대 가상 극장 설치에서 한 가상 성인 고인의 계량·기록·입장 판결과, 세 모이라이가 다루는 같은 생명실, 지하·지상·천상을 잇는 단일 세계축을 한 프레임에 배치했습니다. 서로 다른 전통을 합친 현대 허구 설치라는 범위를 명시했습니다. 참조는 가상 28세 성인 역할의 가시적 눈·얼굴·단발 외형에만 활용했고, 실제 나이·신원·종교·동의·인격·체형이나 사용자 선호 및 신원매칭을 평가하지 않았습니다.

저장된 seed `600376509`에 CPython `random.Random(seed)`, `randint(2,3)`, `sample(range(4), count)`를 적용해 count=3, index=[2,1,3]을 얻었습니다. 선택 라벨은 아래 세 개이며 coordinator 실험 자극입니다. 인간이 의미를 새로 정의한 것으로 바꾸지 않았습니다.

| 선택 키워드 | 최종 픽셀 판정 | 근거 |
| --- | --- | --- |
| 세계축 삼계 연결 | PASS 2/2 | 배경의 같은 나무가 어두운 뿌리 영역, 사람이 있는 지상, 별과 구름의 천상 층을 연결합니다. 다만 실제 조각 설치보다 회화적 무대 배경으로 렌더되어 전체 예술 방향의 제한을 별도 기록했습니다. |
| 아누비스의 계량과 토트의 기록 | PASS 3 / UNOBSERVABLE 2 | 같은 저울의 심장·깃털, 아누비스의 관여, 열린 상향 입장 경로는 보입니다. 심장의 파란 표시를 추가했지만 내부 도상이 고인·관과 달라 동일 소유를 확정하기 어렵고, 토트의 필기 접점은 종이 윗 경계에 가려 확인할 수 없습니다. |
| 하나의 생명실을 뽑고 재고 자르는 모이라이 | PASS 2 / FAIL 3 | 세 역할의 개별 인물·기구와 측정 접점은 보입니다. 방적은 이미 감긴 릴을 당기는 모습이고, 가위 앞뒤 수평 실은 끊어지지 않았습니다. 수정으로 추가한 주인공행 대각선은 계속된 수평 실에 분기처럼 붙어 같은 한 실의 절단 후 연속 경로가 아닙니다. |

8개 중립 범주, 독립 baseline·controls·embodiment·core와 12개 판정 조건을 동결한 뒤 pre-core validator를 통과했습니다. freeze 시점 이전에 후보/프로필/과거 프롬프트/타 arm 자료를 열지 않았습니다. 원문 envelope bytes는 그대로이며 사후 무결성 검사에서 모든 동결 파일의 SHA256이 유지됐습니다.

현행 HEAD `900848816f88a494e5bf16ea475a25074d584911`에서 코어 기반 v6 pack **한 개**, `37dc2140e374ad65`를 생성했습니다. 실제 compose 상세 조회 후 아래 보강된 기존 후보 두 개를 완전한 의미로 채택했습니다.

- `augmentation:adult_appeal:sensual:action:moirai_spin_measure_cut_action`
- `augmentation:adult_appeal:sensual:aesthetic_trend:axis_mundi_connection_aesthetic`

`slot:composition:ri_heart_maat_figure_readable_composition`은 반대 저울판에 마아트 소상을 놓고 그 머리에 깃털을 두는 변형입니다. 사전에 고정한 깃털 계량 장면과 달라 거절했고, 그 복합 의미를 일부만 빌려 독립 작성으로 재표시하지 않았습니다. `bundle:ri_heart_maat_figure`도 선택하지 않았습니다. unrelated `ri_chakra_white2` 등 8개 프로필은 노출됐지만 선택한 프로필과 visual-concept ID는 0개입니다. 전체 노출 105개 후보 ID, 상세 열람·선택·거절은 [exposure_adoption_ledger.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/exposure_adoption_ledger.json)과 [candidate_adoption_review.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/candidate_adoption_review.json)에 기록했습니다.

첫 시도는 357단어 생성 프롬프트, 마지막 시도는 383단어 native 국소 수정 프롬프트입니다. 둘 다 composed/runtime 감사는 PASS입니다. 두 번째의 360단어 권장 길이 초과는 advisory warning이며 640단어 상한 이내입니다. `negative_en` exact bytes는 두 시도에서 같습니다. 최초의 coverage-assertion key 준비 오류는 원문이나 코어를 바꾸지 않고 mandatory key 바인딩만 바로잡았으며 실패 감사도 보존했습니다.

native `image_gen.imagegen`만 사용했습니다. 1회 생성과 1회 국소 수정으로 승인된 재시도 한도를 소진했습니다. 수정은 자신의 첫 이미지와 원래 참조를 첨부하고, 통과한 저울·세계축·입장 경로·인물 배치·측정을 보존하며 다섯 실패/확인 불가 접점만 대상으로 했습니다. 반환된 구체 원본 경로를 그대로 복사했고, 파일 SHA256·1374×1145 치수와 native 반환/저장 원본의 같은 PNG 픽셀 payload를 확인했습니다. 모델 ID는 도구가 반환하지 않아 unknown입니다.

| 시도 | run_id | 저장 원본 SHA256 | 픽셀 결과 |
| --- | --- | --- | --- |
| 1 | `c47d6abb99a4e350` | `0dc374a92221887cb959bce025bc76af3330216980ff0ace03ea4c843331150b` | FAIL: 7 PASS / 3 FAIL / 2 UNOBSERVABLE |
| 2 | `2c61db8d448f5b76` | `1a2ea776cfe0459c9df41762a991acf521654f98c5d2a8088bb95717394d3a70` | FAIL: 7 PASS / 3 FAIL / 2 UNOBSERVABLE |

composed/runtime PASS는 정확한 프롬프트·참조·코어·retrieval binding의 사전 검증입니다. 원본 픽셀 증거를 대신하지 않습니다. 두 render-review 감사는 schema_failures=[]를 유지하면서 `embodiment_contact_and_space`, `embodiment_visibility_and_projection`의 실제 실패 때문에 `failed_technical_hard_gates`를 반환했습니다.

주요 산출물:

- [첫 원본 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/attempt_01/image.png) · [첫 생성 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/attempt_01/standalone_prompt.txt) · [첫 픽셀 리뷰](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/attempt_01/pixel_review.json) · [첫 composed 감사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/attempt_01/composed_audit.json) · [첫 runtime 감사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/attempt_01/runtime_audit.json)
- [최종 수정 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/attempt_02/image.png) · [실제 마지막 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/standalone_prompt.txt) · [negative exact bytes](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/negative_prompt.txt) · [runtime_request.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/runtime_request.json)
- [최종 픽셀 리뷰](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/pixel_review.json) · [composed 감사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/composed_audit.json) · [runtime 감사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/runtime_audit.json) · [render-review 감사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/attempt_02/render_review_audit.json)
- [동결 판정 조건](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/test_case.json) · [무작위 선택 원장](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/random_selection.json) · [동결 manifest](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/freeze_manifest.json) · [pre-core 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/precore_validation.json) · [최종 무결성](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/final_integrity.json)
- [재시도 lineage](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/attempt_02/retry_plan.json) · [arm 전용 실제 호출 원장](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/image_runs.ndjson) · [시도 준비/결과 원장](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/attempt_ledger.json) · [run_manifest.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/run_manifest.json) · [qualification_manifest.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/qualification_manifest.json)

정규화된 authorial core SHA256은 `59bfec40eafeea1833a37cb332b42e1c5dbf7fae16b88c89aacebe6db5b48c01`, intent lock은 `b212b99f7223e9f3dd4c0d5d4689b5caca2dbeea487b7f7327aae1dea687f5ba`, core retrieval은 `223e54d9fb5a0c730602a209ff0ebe6dacd39773534d196b550049efdbb82936`입니다. 작성 산출물은 arm_c에만 저장했고 자산·코드·테스트·공용 원장은 수정하지 않았습니다.

의미 검토의 공개 출처는 [British Museum Hunefer 파피루스](https://www.britishmuseum.org/collection/object/Y_EA9901-3), [Met 모이라이 소장품 설명](https://www.metmuseum.org/art/collection/search/373996), [Prose Edda 원문 번역](https://www.gutenberg.org/cache/epub/18947/pg18947-images.html)입니다. BM 직접 열기는 403이었고 검색에 반환된 해당 박물관 객체 설명을 사용했습니다. Edda의 뿌리-천상 연결은 일반 세계축 해석의 출처이며, 이번 삼계 무대는 독립적인 가상 설치 선택이지 북유럽 세계가 셋뿐이라는 주장이 아닙니다.
