# 음악물 데이터와 검증 기록 게시

음악물 시각 카드 124개, 새 완전한 선택형 후보 122개와 진단 32개, 바인딩 370개, 원문 재사용 2개를 게시 범위로 정했다. 후보/의미 원문 세 파일, 음악 테스트, 음악 안내, 음악 리서치·실제 이미지·프롬프트·리뷰 기록을 포함한다. 공유 SKILL과 composition-contract에서는 이번 재시험에서 추가한 일반 조언/원문 계약 구분 세 문단만 옮겼다.

다른 주제의 미완료 변경은 가져오지 않았다. 공유 corpus manifest는 게시 기준의 기존 목록을 유지하고 음악 모듈 두 항목만 추가했다. 기존 후보·바인딩·카탈로그·정책 보존과 전체 사전/인덱스를 검증했다. 기본 runtime selector를 이 작업의 임시 빌드로 교체하지 않는다.

첫 실험과 재시험의 원본과 판정은 역사적 기록으로 보존했다. 재시험의 부모 보수 판정은16/21, 독립 판정17/21, 엄격 전체 장면 통과0/3이며 신규 음악 source의 최종 추가 기여는0이다. 게시가 픽셀 실패를 성공으로 바꾸거나 native 자격을 부여하지 않는다.

`publication-evidence/source-preservation.json`, `focused-tests.log`, `dictionary-validation.json`, `index-build.json`이 게시 전 검증이다. `historical-evidence-validation.json`은 원래 연구 및 재시험 해시를 확인한다. 빈 LOCK 파일은 일시적 동시 실행 파일이므로 게시에서 제외했으며 실질적인 재시험286개 파일은 일치했다.

`publication-evidence/run-snapshots/`와 `run-snapshot-inventory.json`은6개 이미지 실행의 관리 기록을 원문 바이트와 함께 보존한다. 기존 경로/영수증을 바꾸지 않고 원래 경로와 보존 위치의 해시 대응을 기록했다. 원본 사진과 실제 native 반환 이미지는 보존 대상이다.

작업 커밋 이후 `origin/main`을 pull하여 원격 변경과 통합하고 최종 사전/인덱스 검증을 거친 뒤 main을 푸시한다. 원격 SHA 일치 확인 뒤에만 관리 워크트리와 이번 작업의 빌드·successor·벡터 요청 캐시, 보존 완료된 generated run 임시 원본을 제거한다. 공용 실행 runtime/model과 다른 작업의 캐시는 유지한다. 실제 푸시·정리 완료 결과는 대화의 최종 응답과 별도 마감 영수증으로 확인한다.
