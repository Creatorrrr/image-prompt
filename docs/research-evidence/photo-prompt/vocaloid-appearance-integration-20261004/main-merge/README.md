# 보컬로이드 대체 표현과 최신 main 병합

로컬 main `b9b28a680b7db4c30f07fae780ae8b6fc8a9b031`의 역이미지 프롬프트 변경과 원격 main `0efc2dfde7de9693799d3c84618705332e59920c`를 함께 보존했다. 데이터 병합 커밋은 `d9640f98807cca08d8ddd69aacb903acb2ff562a`다.

원본 데이터 19개 파일을 ID별로 병합했다. 기존 프로파일 65개의 전체 대체 표현 134개·구성 요소 표현 154개, 기존 후보 55개의 보강, 새 관계 19개·후보 25개·선택형 bundle 3개를 유지했다. 여섯 기존 `ca_` 관계의 의존성인 외형 프로파일 원본 파일과 로드 목록도 포함했다. 별도로 진행하던 character-appearance·uniform-costume 연구 폴더와 미추적 테스트는 게시 범위에 넣지 않았다.

main의 카메라 해석·문장 소유자·부정 범위 처리 코드는 유지했고, 목덜미 길이와 얇은 직물 불투명도에 관한 후보·프로파일 여덟 곳의 속성 효과 추가도 보존했다. 출처 기록이 겹친 두 확장에는 양쪽 참조를 담은 새 후속 유지 기록을 추가했다. 기존 유지 기록은 바꾸지 않았다. [AUTHORED-MERGE-REVIEW.json](AUTHORED-MERGE-REVIEW.json), [UPSTREAM-EFFECT-ADDITIONS.json](UPSTREAM-EFFECT-ADDITIONS.json), [BOTH-PARENT-PRESERVATION.json](BOTH-PARENT-PRESERVATION.json)이 항목별 근거다.

양쪽의 정확한 긍정 텍스트와 provider·model·dimensions가 일치하는 벡터를 재사용해 두 인덱스를 다시 만들었다. 결과는 시각 프로파일 1,690개, 의미 문서 9,901개다. 임베딩 API와 네이티브 이미지 추가 호출은 모두 0회이며 기존 shard 세대도 유지했다. [INDEX-REBUILD.json](INDEX-REBUILD.json)에 재생성 근거가 있다.

양쪽에서 별도로 만든 v10 기록은 구분했다. main의 v1–v11 원본을 바이트 그대로 유지했고, 최초 로컬 Vocaloid v10은 상위 폴더의 `local-photo-regression-baseline-v10.json`에 보관했다. 최신 동결 입력으로 만든 v12는 기존 후보 64개·순서·코어·장면·구성·부정 표현·비공개 경계를 유지한다. 변한 것은 `provenance.tags_hash`, `core_retrieval.slot_corpus_sha256`, `core_retrieval.canonical_sha256`, `pack_id` 네 곳뿐이다. [V12-FOUR-LEAF-PROOF.json](V12-FOUR-LEAF-PROOF.json)이 전체 나머지 필드의 동등성을 확인한다.

일러스트 검증에는 이 v12를 명시적으로 등록하고 현재 validator 파일의 해시 메타데이터만 갱신했다. v10·v11 테스트는 당시의 저장된 입력과 데이터 정체성을 검증하고, v12 테스트와 실제 전체 자산 검사는 현재 파일을 검사한다. 과거 실패 판정과 oracle·holdout은 변경하지 않았다.

병합 검증은 전체 1,444개 unittest ID를 대상으로 진행했다. 역사적 픽셀·참조 검사에 필요한 Git 제외 파일 15개는 기존 작업 폴더의 저장된 해시와 대조해 복사했다. 새 생성이나 판정 완화는 없었다. 집중 v12·역사 비교 검사 30개는 통과했고, 전체 1,444개 고유 테스트의 최종 결과는 모두 통과했고 [FULL-REGRESSION-SUMMARY.json](FULL-REGRESSION-SUMMARY.json)에 각 실행의 근거를 기록했다. 분할 실행의 중간 실패 기록도 보존한다.

상위 보고서와 세 생성 컨셉의 픽셀 결과는 **병합 전 독립 동결 스냅샷의 기록**이다. A·B 출력 차단, C의 실제 이미지 두 장 전체 실패 판정은 그대로다. 이 Git 병합·회귀 통과를 새로운 이미지 품질 검증으로 해석하지 않는다. 당시 전체 런타임·인덱스 백업은 로컬에 보관하고 공개 파일에는 해시 manifest·원본 데이터·프롬프트·판정·실제 생성 결과를 남겼다.
