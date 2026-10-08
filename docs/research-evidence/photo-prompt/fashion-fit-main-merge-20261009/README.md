# 패션 핏 데이터 main 통합

패션 핏 연구 카드 64개 중 60개를 후보 114개·시각 의미 프로필 114개·선택 번들 114개로 등록하고 기존 후보 4개의 동등 표현을 보강했다. 같은 의복의 소유·관계·영향 속성과 관찰 기준을 유지했다. 기존 main의 셀피·일식 데이터와 등록 항목 112개는 보존했고 패션 핏 source 두 개만 추가했다. 별도 지적 활동 데이터와 다른 미커밋 작업은 로컬에 유지한다.

독립 세 native 실험의 프롬프트·코어·receipt·검사·반환 이미지 기록 618개를 원본 해시로 대조해 복사했다. 실제 생성 5회, 전체 사례 통과 0/3이라는 원래 결과와 관리형 리뷰 연결 오류를 그대로 보존했다. 이번 Git 통합에서 이미지를 새로 생성하지 않았다. 역사적 실험 세대를 최신 main 데이터 세대로 대체하지 않는다.

실행 캐시와 lock 파일 1,935개는 원래 작업 공간에 보존하며 파일별 해시를 기록했다. 검색 인덱스는 동일 ID·전체 텍스트·provider/model/dimensions/recipe의 캐시 벡터만 재사용하고 BM25F와 메타데이터를 다시 계산한다. 원본 수정·충돌 해결과 파생 인덱스 재생성을 구분한다.

- [복사·제외 범위](EVIDENCE-COPY.json), [로컬 캐시 목록](LOCAL-RUNTIME-CACHE-INVENTORY.json)
- [기존 main 및 신규 원본 보존](LOCAL-INTENT-VERIFICATION.json), [최초 인덱스 재생성](LOCAL-INDEX-REBUILD.json)
- [최초 검증](LOCAL-CHECKS.json), [원래 이미지 테스트 보고서](../../../analysis/2026-10-08-fashion-fit-integration-and-native-tests.md)

origin/main을 pull한 결과 이미 최신이어서 충돌은 없었다. 기존 원본 112개 등록과 패션 핏 원본 두 파일의 바이트 보존을 확인했다. 관련 회귀 81개, 최초 패션 핏 검사 10개, 사전 검증과 시각 인덱스 deep check가 통과했다. 게시 코퍼스는 semantic 11,181개와 시각 프로필 2,934개이며 임베딩 호출은 0회다. 전체 테스트 모음과 이미지 검증은 이 Git 작업에서 다시 실행하지 않았다.

[원격 pull](pull.log), [양쪽 원본 의도 보존](MERGE-INTENT-VERIFICATION.json), [81개 회귀](focused-tests.json), [로컬 추가 데이터 캐시 검증](PRIMARY-VECTOR-PREFLIGHT.json)에 근거를 기록했다. 실제 push/main 일치와 원래 작업 공간 보존, 워크트리 제거는 완료 후 별도 영수증으로 남긴다.
