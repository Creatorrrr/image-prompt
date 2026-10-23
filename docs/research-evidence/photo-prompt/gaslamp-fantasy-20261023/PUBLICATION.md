# Gaslamp Fantasy main 게시 검증

이번 게시 범위는 Gaslamp 의미/후보/선택적 연결, 217개 원문 경로의 연구, 세 독립 이미지 실험의 원본·프롬프트·실패 판정, 그리고 정확한 병합 소스의 호환 검색 인덱스다. 기존 main의 코드·후보·조건·효과·정책과 다른 작업은 보존한다.

최초 main 소스의 후보 20,149개와 연결 14,810개를 바이트 의미가 같은 상태로 보존하고, 107개 후보(시각72/진단35)와 144개 연결만 더했다. 기존 여섯 재사용 source도 원문과 같다. 의미 카드113/경로217/성분·관계 검사445는 최초 연구대로 유지한다.

호환 검색 레이아웃은 저장소의 `photo-global-visual-text/v1` 및 phrase/profile별 기존 recipe를 따른다. 기존 벡터19,700개를 재사용하고 새72개만 실제 로컬 임베딩으로 생성했다. 이전 실험의 다른 recipe 벡터에 새 이름을 붙이지 않았다. merged origin/main이 바뀌면 그 소스와 기존 recipe에서 다시 검증한다.

구조/의미 source 검증, 전체 index/source closure 및 회귀68개를 확인한다. 테스트 부트스트랩에 필요한 로컬 모델 환경과 현재 설치본은 실행 의존성이며 Git의 `retrieval-runtime.json`은 원격 버전을 보존한다. 기본 작업 폴더의 활성2aaccb50 계열 runtime과 다른 작업의 변경도 보존한다.

세 이미지의 생성은 각1회이며 장르 가시성3/3, 엄격 전체 관계0/3이다. 생성 성공과 검토 기록의 유효성은 이미지 관계 성공이나 native 후보 자격, 사용자 수용을 의미하지 않는다. 새 이미지나 추가 원격 모델 호출 없이 기존 결과를 보존한다.

- [최초 소스 보존](publication-evidence/source-preservation.initial.json)
- [인덱스 빌드/전체 검증](publication-evidence/index-build.initial.json)
- [사전/인덱스 검사](publication-evidence/dictionary-validation.initial.json)
- [회귀68개](publication-evidence/focused-tests.initial.json)
- [원본 경로/무손실 압축 매핑](publication-evidence/PATH-MAP.json)
- [최종 세 이미지 검증표](integration-evidence/FINAL-TEST-MATRIX.json)
- [가스등 점검](image-test-evidence/a/arm-report.md)
- [유리 영혼종 수리](image-test-evidence/b/arm-report.json)
- [통행증 교섭](image-test-evidence/c/final-summary.json)

원본 연구와 실험 JSON의 절대 경로와 해시는 역사 기록으로 그대로 보존했다. 읽기용 통합 보고서는 저장소 내부 경로를 사용한다. 5MB를 넘는 두 임시 원문 snapshot은 무손실 gzip으로 보관하며 원본 SHA를 매핑에 유지한다. 외부 Downloads의 참조 인물 원본은 Git에 복사하지 않았다. 임시 모델 복제·빌드·인코딩 캐시와 이 작업의 전용 워크트리는 실제 원격 main SHA를 확인한 다음 제거한다. 운영 중인 설치 runtime/공유 모델과 최종 이미지·프롬프트·증거는 보존한다.

실제 commit/push 및 cleanup 완료 SHA는 로컬 `generated/publication-receipts/gaslamp-fantasy-20261023.json`의 최종 원격 조회 결과로 확인한다. 이 문서는 미래 SHA를 미리 만들어 적지 않는다.

초기 작성 형식/소유권을 고치면서 교체한 세 draft run은 실제 이미지 호출0회다. [검증한 압축 이력](publication-evidence/ABANDONED-AUTHORING.json)과 tar.gz에 원문을 보존한 뒤 임시 원본 폴더를 정리한다. 세 최종 이미지 run과 그 산출물은 유지한다.

최종 병합 대상은 `a8732e20dc681c5827e05db5352782d075fe422b`다. Flintlock·Art Horror 등 기존 후보20,314개/연결15,035개와 87개 모듈 파일을 원문 그대로 보존하고, 총20,421개/15,179개로 확장했다. 최종 레이아웃 `a941304f7180dd443b016025e0d402813af9165426c3018579725f9eb7c8339a`는 양쪽 소스에서 검증했으며 기존 벡터19,815개와 새72개로 구성된다.

- [최종 소스 보존](publication-evidence/source-preservation.final.json)
- [최종 인덱스 빌드·전체 검증](publication-evidence/index-build.final.json)
- [최종 사전 검증](publication-evidence/dictionary-validation.final.json)
- [고정 SHA 기반 병합 규칙](publication-evidence/merge-resolution.json)
