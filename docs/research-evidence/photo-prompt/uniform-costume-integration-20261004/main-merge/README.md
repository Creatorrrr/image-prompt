# 제복·코스튬 대체 표현과 최신 main 통합

원격 main `9544c624efee343e3c97ce428b4bec42fd1dfebb`에는 역이미지 프롬프트, 카메라 문장·관찰 축 처리, 목덜미·얇은 직물 속성 효과와 보컬로이드 반영 결과가 들어 있다. 공용 main 폴더의 미완성 연구를 보존하기 위해 분리한 작업 폴더에서 통합했다. 제복 원본 8개의 변경 전 스냅샷이 이 원격 원본과 모두 같음을 확인한 뒤, 제복 추가분만 적용했다. [원본 비교](AUTHORED-PRESERVATION.json), [양쪽 의도 보존](BOTH-INTENT-PRESERVATION.json).

기존 의미·후보 각각 29개를 보강하고 새 관계·후보 각각 38개, 완전한 한·영 대체 표현 266개와 선택형 묶음 3개를 유지했다. main의 카메라 처리 코드에 공통 구성요소 검색 연결만 더했다. 모든 구성요소·원본 opt-in·속성 잠금·제외 조건을 계속 요구하며 결과는 optional이다. 데이터 이름이나 테스트 ID 전용 분기는 없다. 기존 historical lexical oracle에는 봉인된 제복 추가분만 되돌리는 정확한 투영을 더하고, 원격의 Vocaloid·목덜미·직물 보존 투영을 그대로 유지했다.

두 인덱스는 합친 원본에서 다시 만들었다. 같은 ID·완전한 긍정 텍스트·provider·model·dimensions가 맞는 기존 벡터만 재사용했다. 의미 문서 9,939개, 시각 프로파일 1,728개와 exact term 4,049개다. 추가 임베딩 API와 native 이미지 호출은 모두 0회이고 과거 shard 세대는 유지했다. [재생성 기록](INDEX-REBUILD.json).

원격의 V1–V12와 pack 스냅샷 17개는 바이트 그대로 보존했다. 최초 로컬 uniform V11은 [별도 원본](local-photo-regression-baseline-v11.json)에 남겼다. 새 V13은 V12와 같은 동결 입력·64개 후보·순서·장면·코어·구성·부정 표현·비공개 경계를 유지한다. `provenance.tags_hash`, `core_retrieval.slot_corpus_sha256`, `core_retrieval.canonical_sha256`, `pack_id` 네 데이터 결합 필드만 바뀌었다. [전체 필드 비교](V13-FOUR-LEAF-PROOF.json), [역사 원본 해시](V1-V12-HISTORICAL-PRESERVATION.json).

V13은 일러스트 검증기의 명시적 후속 버전에 등록했다. 현재 validator 해시 메타데이터 하나만 갱신하고 universal V2의 나머지 필드와 모든 holdout을 보존했다. V10–V12 테스트는 각 당시 봉인된 입력과 데이터 정체성을 검사하고, V13과 production validation은 현재 실제 바이트를 검사한다. 변조·후보 변경·순서 변경·부정 표현·비공개 경계 변경에 대한 기존 거부 검사를 유지했다.

집중 제복·Vocaloid·역사 투영 검사 35개, V10–V13 이력·변조 방지 검사 28개, 사전 검증과 실제 시각 인덱스 검증은 통과했다. 병합된 전체 169개 모듈·1,464개 고유 테스트의 최종 결과는 모두 통과했다. 초기에는 분리 폴더의 `.venv/bin/python` 경로 미연결로 2개 검사가 실행되지 않았고, 기존 환경 연결 후 이 두 검사만 재실행해 통과했다. 소스·테스트 893개 파일은 전체 실행 중 바뀌지 않았으며 최초 오류 기록도 남겼다. [전체 결과](FULL-REGRESSION-SUMMARY.json). [전체 검사 계획](full-regression/PLAN.json), [소스 동결](FINAL-SOURCE-FREEZE.json).

기존 독립 3개 컨셉의 프롬프트·초기 누락·pixel 판정·생성 이미지 6장을 [qualification](../qualification)에 보존했다. 새 시각 의미 검사 6/6 통과와 전체 컨셉 A FAIL·B PASS·C FAIL 판정은 이전 동결 스냅샷의 결과다. 이번 Git 통합과 회귀 검사를 새로운 이미지 일반화나 사용자 수락 결과로 확대하지 않는다. 원본 업로드 사진과 중복된 전체 런타임 스냅샷은 공개 범위에서 제외했다. [원본 이미지·증거 해시 목록](QUALIFICATION-ARCHIVE.json).
