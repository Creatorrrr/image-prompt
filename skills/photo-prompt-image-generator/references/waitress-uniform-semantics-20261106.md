# 웨이트리스·식음료 서비스 유니폼 시각 의미

연구 계획과 실행 기록은 로컬 전용 Git 무시 경로 `docs/research-evidence/photo-prompt/waitress-uniform-20261106/`에 있으며 다른 체크아웃에는 없을 수 있다. 관련 데이터는 `photo_waitress_uniform_semantics_20261106.json`, `photo_candidate_waitress_uniform_20261106.json`, `photo_candidate_waitress_uniform_bindings_20261106.json`, `photo_candidate_retrieval_views_waitress_uniform_20261106.json`이다.

44개의 한영 시각 선택지와 8개의 맥락 진단은 업무복의 구성·앞치마 구조·시대별 사례·소품과 손의 접점·코스튬·상태·장면을 구분한다. 각각의 시각 선택지는 완전한 선택적 명제이며 관련된 별도 후보를 합쳐 새로운 사실이나 요구를 만들지 않는다. 진단은 positive image material이 아니다. 한영 뷰는 원본이 허용하는 의미와 source quote/hash를 유지하며 검색을 지원할 뿐 native role·owner·effect 승인이나 채택 허가를 부여하지 않는다.

직업과 복장은 동의어가 아니다. 비브와 크로스백, 의상과 앞치마의 층, 역사적 실물과 현대 코스튬, 일반 서버와 메이드 카페, carhop과 스케이팅 carhop을 구분한다. 성인·페티시·노출·고딕·혈흔·무기·상처·행동은 각각 요청된 범위와 실제 후보 조건에 따라 개별 검토한다. 사진의 시각적 단서만으로 연령·직업·동의·성적 의도·물질의 화학 성분·사건 원인을 확정하지 않는다. 숨은 구조·가려진 접점은 미관찰로 남긴다.

후보 source 등록, 색인 포함, 검색 노출, native 적격성과 최종 채택, 저장된 이미지에서의 관찰은 서로 다른 상태다. 연구용 관찰 게이트와 `native_approval: false`는 픽셀이나 실제 역할 승인 검증이 아니다. 구체 설치 상태와 평가 결과는 해당 실행 기록에서 확인한다.

## 소스 무결성과 검증 범위

- `photo_waitress_uniform_semantics_20261106.json`: SHA-256 `d2cc3db84ebe67d7796e8877939a28bcd8f4d876e8a437f56d7c918f8ee92b2c`.
- `photo_candidate_waitress_uniform_20261106.json`: SHA-256 `a0a4ae7dfa1a8a8283e7a487ceca59bbfac27cd25c8013a02b9e781be2e08e33`.
- `photo_candidate_waitress_uniform_bindings_20261106.json`: SHA-256 `970ea63aad3f2aa3ebc71bb8563f00f6b1eae6f652620ecd535c3800cbd73759`.
- `photo_candidate_retrieval_views_waitress_uniform_20261106.json`: SHA-256 `fc39eb391d5219beb76ed52166368cca9633ba84b53300d5c563250930922e20`.

개발용 한국어·영어 질의 8개에서 지정 신규 후보가 1위였고 비관련 대조 2개의 top 8은 이전 릴리스와 같았다. 저자가 후보를 알고 만든 소규모 시험이므로 독립 holdout이나 이미지 품질 개선의 증거가 아니다. 참조 이미지를 사용한 세 독립 실행은 웨이트리스 주제의 복식·소품을 보여줬지만 주요 동작은 검색 전 baseline에 이미 있었고, 선택 가능한 완전한 신규 후보 채택은 없었다. 다이너와 카홉의 신체 지지·연결 게이트는 가림 또는 프레임 밖으로 기술 판정에 실패했고, 카페의 다섯 게이트는 통과했다. 한 장의 시각 관찰은 인과적 기여나 사용자 수용을 입증하지 않는다. 자세한 로컬 증거는 위 실행 기록을 확인한다.

소스 등록만으로 다른 장치에서 인덱스나 임베딩이 준비되는 것은 아니다. 각 환경은 실제 선택된 봉인 검색 릴리스와 모델 공간을 별도로 검증해야 한다.
