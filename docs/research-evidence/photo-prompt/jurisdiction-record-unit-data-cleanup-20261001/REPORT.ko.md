# 관할·기록 장면의 기존 의미를 최종 후보에 보존

spirit_jurisdiction_capture_context 한 행에 concept_units=[기존 영어 문장]만 추가했다. 영어·한국어 라벨, aliases, embedding_text, tags, facets, weights와 기존 guard는 바꾸지 않았다. 원래 문장은 비신성 번호·지도·인계 봉투·물질 흔적으로 관할과 기록 신뢰도를 표현하며, 실제 의례·신명·성물을 그 근거 체계로 쓰는 경우와 구분한다.

기존 영어는25단어였고 명시적 units나 keywords가 없어 semantic_source가 비어 있었다. 실제 production pack/detail에는 divine/sacred/rites/성물 같은 순서 없는 단어만 남아 원래 대비 관계가 전달되지 않았다. 편집 전 실제 builder로 제안을 확인한 결과, 같은 영어 문장을 명시적 unit 하나로 넣으면 최종 semantic overlay가 원래의 완전한 문장을 보존한다. 중간20-term helper만 보고 내린 결론이 아니다.

이 최종 unit은 영어다. 한국어 라벨은 source/localization/index에 남지만 최종 한국어 단어 coverage 증가를 주장하지 않는다. 별도 박물관 진열과 기록 판정 체계는 공존할 수 있으므로 성물이나 종교 어휘를 전역 금지하는 변경도 아니다. parser·한도·검색 로직·schema 확장은 없다.

## 고정 범위와 결과

10개 행 중 하나를 수정하고9개를 그대로 두었다. 장문이라는 이유만으로 일괄 수정하지 않았다. Punk7개는 기존 keyword units와 완전한 family bundle이 의미를 보존하며, 일반 capture-context2개는 통제군이다. 별도의 장문 narrative-core3개는 현재 범위에서 제외했다.

수정 전에 독립 검토자가 작성한6개 질의와 일반 capture control2개를 고정했다. 모두 검토 가능한 작성 진단이며 blind holdout은 아니다.

- Dense: 영어·한국어 양성, 공존 control, 일반 capture control은 모두1위 유지
- 실제 의례 대비 q03/q04:2→5위,2→6위로 하락
- q04에서는 대상이2위에서6위로 내려가며 cover_role_documentary_capture가5위로 들어왔다. 모든 교체 결과가 정답이라는 주장은 하지 않는다
- Lexical: 영어 양성88→81위로 조금 좋아졌지만 여전히 약하다. 한국어 양성1위 유지
- 의례 대비는 lexical에서 둘 다 여전히1위다. dense의 첫 결과도 다른 허구·주술 계열 후보여서 종교/기록 분류를 해결한 결과가 아니다
- 공존 control은 두 방식 모두1위지만 cosine은 .735839→.718343, .736367→.716891로 낮아졌다. 점수 불변을 주장하지 않는다
- 일반 capture control의 lexical 순위는6위와3위로 동일하다. 모든 lexical top5 ID 순서는 같다

채택 이유는 최종 public/detail에서 원래의 완전한 대비 의미가 실제로 복원되고, 고정 질의 target 순위의 역방향 변화가 없다는 점이다. 자연 질의의 실제 노출·채택이나 생성 이미지 품질은 검증하지 않았다.

## 독립 검증·테스트·비용

독립 read-only 검토가32개 method-query 결과, 실제 source/index/BM25/cache와 최종 unit/detail을 확인했다. 문서10,174개 중 새 벡터1개, 정확한 baseline 재사용10,173개다. Bundle 변경은 없다.

- DATA/public/background165개와 CJK/effect/bundle/profile43개: 총208개 통과
- 최초165개 실행에서는 역사적 capture artifact 부재로3개 subtest가 실패했다. 해당22개 파일은 sparse 선택 밖의 skip-worktree 경로였으며, 현재 HEAD의 원본 bytes로 복원해24개 hash 참조 모두 일치시켰다. 기대값·테스트를 바꾸거나 이미지를 새로 만들지 않았다
- 추가 role/projection11개:10개 통과, 기존 지역 평판 fixture1개 실패. 수정 전후 세 query의 top12 ID 순서는 같고 social-recognition 후보가7위라 요구 top6에 들지 못한다
- Dictionary metadata,1,385개 profile/3,305개 exact-term index와 저장 벡터 replay도 통과했다. 전체 저장소 green 또는 과거 렌더 품질 통과라는 주장은 아니다

9개 입력이 각각 한 번 성공했다. 전송량2,560 UTF-8 bytes, 추가 비용 보수적 상한$0.0147456, 추적 누적 상한$1.1665408이다. 청구서 실측이 아니며 별도 upstream 사용액은 대조하지 않았다. 추가 이미지 생성0회, 자동 retry0회다.

최신 main pull 이후 검사와 정상 push/remote 확인은 별도 publication 단계다. 해당 publication의 source/index 상태에서 evaluate_cycle.py --replay로 저장 결과를 API 없이 재현할 수 있다.
