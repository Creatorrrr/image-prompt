arm A는 네이티브 이미지 1장을 생성·저장했고, 전체 의미 검증은 실패로 기록했다. 구성·생성 요청 감사는 PASS지만, 저장된 원본 픽셀에서 핵심 형태 3개 중 위팔 살집만 분명히 확인됐다. 사용자 수락은 아직 받지 않았다.

| 합성 시험 의미 | 영역 | 원본 픽셀 판정 |
| --- | --- | --- |
| plump | 배꼽 아래의 작은 둥근 볼륨 | FAIL — 작은 돌출은 암시되지만 니트 주름·처짐과 신체 볼륨을 충분히 구별할 수 없다. |
| curvaceous | 하부 갈비뼈→옆허리→아래배의 연속 곡선 | FAIL — 가까운 위팔이 옆몸통 경계를 가려 들어간 선과 나온 선 및 연속성을 모두 확인할 수 없다. |
| fleshy | 드러난 위팔의 둥근 살집 | PASS — 가까운 위팔의 부드러운 두께·완만한 테이퍼·팔꿈치 접힘이 보인다. |

초기 보조 게이트는 6개 중 3 PASS / 3 FAIL이다. 선택한 윤곽 프로필의 게이트와 embodiment 게이트를 합친 정확한 hard set은 8개 중 5 PASS / 3 FAIL이며, 리뷰 스키마 오류는 0개다. partial·unobservable은 FAIL로 처리했다.

실패한 hard gate는 vo_ne_regional_contour_transition_2, vo_ne_regional_contour_transition_3, embodiment_visibility_and_projection이다. 얼굴·머리 외관, 위팔 살집, 책·제본실 접촉, 젖은 출입구가 있는 책 수선 장면은 확인됐다. 원본 사진의 실제 나이·정체성·체형은 추론하지 않았다.

normal V6 CLI의 실제 선택 모드는 core_bm25f다. 후보팩에서 직접 노출된 ne_regional_soft_volume와 ne_regional_contour_transition을 독립 검토 후 선택했고, 선택한 visual-concept:ne_regional_contour_transition의 전체 3-component 계약을 묶었다. 전신 볼륨·엉덩이·입술·오버헤드 팔·행동 archetype 후보는 국소 시험에 맞지 않아 거절했다. Gemini 인덱스가 존재한다는 사실을 이 arm의 embedding 검색 성공으로 대체하지 않았다.

344단어의 standalone prompt는 prompt_en.txt, 정확한 네이티브 입력은 native_tool_args.json과 native_render_request.json에 있다. 이미지 도구는 image_gen.imagegen이며, 전달된 파일을 arm의 generated_images/arm-a-book-repair-20261003T032108Z/native.png로 바이트 그대로 복사했다. 생성 모델 식별자는 도구가 노출하지 않았다. native result 1237×1272 PNG의 SHA-256은 7a2979a4cd3d3a4ce1f6cbb81bf87c33d8fac2caf7589c43ac45f1bb70361bbb다.

원본 authorial_core.json·baseline과 92개 운영 입력은 시작·종료 hash 검증에서 변하지 않았다. CLI normalizer가 request binding과 canonical metadata를 추가해 파생한 core hash는 별도로 기록했다. 실제 사용자 권한 원문과 arm이 작성한 합성 몸통/팔 정의는 분리되어 있으며, 다른 arm의 출력은 읽지 않았다. run_manifest.json은 photo-independent-run-manifest/v2, ledger는 runs/image_runs.ndjson이고 실제 이미지 호출 수는 1이다. 생성 결과 status=success는 픽셀 qualification=failed와 별개다.

단일 이미지로 데이터 보강의 인과적 효과나 일반적 렌더 신뢰도는 검증할 수 없다. 이 기록은 후보 노출·정확한 감사 바이트·이 시도의 원본 픽셀 결과를 보존한다. 재생성은 수행하지 않았다.
