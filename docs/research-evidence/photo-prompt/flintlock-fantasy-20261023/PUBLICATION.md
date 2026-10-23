# Flintlock Fantasy 발행 범위와 검증

이번 발행은 52개 시각 후보, 21개 문맥 진단, 99개 연결과 의미 자료·조사·시험 증거를 포함한다. 공용 모듈 다섯 개에서는 해당 CID의 `content.ko`와 `content.embedding_text`만 바꿨다. 기존 영어, 조건, 효과, 출처와 다른 CID는 보존했다. 원래 57개 조사 출처와 현재 F02 정정에 추가한 두 출처의 시점을 구분한다.

더러운 기본 체크아웃의 다른 도메인·스킬 코드·런타임 설정과 혼합 인덱스는 발행에 가져오지 않았다. `ef1fadef6b2f719db49e71a72cca7aea15341ebb`에서 분리한 워크트리의 정확한 발행 소스로 인덱스를 다시 만들었다. 기준판의 20,149 CID에 이번 73개를 더해 20,222 CID이며 긍정 검색 대상은 19,752개다. 원래 벡터 19,695개를 재사용했고 변경 문서 57개는 동일한 실제 임베딩 공간·레시피의 검증된 캐시에서 읽었다. 외부 이미지나 임베딩을 새로 호출하지 않았다. 병합 중 소스가 바뀌면 그 합집합에서 다시 검증한다.

- [필드 단위 추출](publication-evidence/source-extraction.json)
- [인덱스 전체 검증](publication-evidence/index-build.json)
- [사전·인덱스 검사](publication-evidence/dictionary-validation.json)
- [회귀 검사](publication-evidence/focused-tests.json)
- [회귀 검사 환경과 설정 복원](publication-evidence/focused-tests-runtime.json)
- [실제 이미지 시험 결과](INTEGRATION-RESULTS.md)

회귀 검사는 소스 문맥, primary proof 경계, 샘플링의 68개 테스트 및 40개 하위 검사를 통과했다. 저장소가 원래 선택한 과거 설치판은 이 호스트에 없어 최초 수집은 실패했다. 검증된 시험용 설치판을 워크트리에서만 잠시 지정해 미변경 테스트를 실행한 뒤 원래 설정 바이트를 복원했다. 기본 체크아웃이나 전역 런타임 선택은 바꾸지 않았다. 이 검사는 로컬에 없는 과거 설치판 자체의 검증을 뜻하지 않는다.

독립 이미지 생성은 앞선 통합시험의 각 1회, 총 3회뿐이다. 전체 복합 케이스는 0/3 통과이며, B02는 개별 1/3, A01은 0/2, H08은 비채택으로 전달 시험을 하지 않았다. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`, 사용자 판단 대기와 native qualification 부재를 유지한다. 발행 검사는 픽셀 판정을 바꾸지 않는다.

`image-test-evidence/`에는 실제 프롬프트, frozen 기준, 결과, 감사·ledger·해시를 보관한다. 원본 참조와 생성 래스터 및 완전한 관리 실행 이력은 로컬에 보존하고 Git에 추가하지 않았다. 모델 복사본, 인덱스 staging, 임시 설치 스토어, 요청 캐시는 커밋 대상에서 제외했다.

커밋 뒤 `git pull --no-rebase origin main`으로 원격 변경을 병합하고, 공용 manifest는 파일·종류의 합집합을 유지하며 겹치는 소스 의미를 검토한다. 파생 인덱스는 해당 최종 소스에서 재구축한다. push는 강제 옵션 없이 수행하고, 실제 `git ls-remote` SHA 및 로컬 main과 일치를 확인한 뒤 전용 워크트리와 이 작업의 임시·캐시만 정리한다. 원격 확인과 정리의 최종 영수증은 로컬 `generated/maintenance/flintlock-publication-20261023/`에 보존한다.

원래 조사 TSV 두 개의 CRLF와 VISUAL-CARDS.md의 마지막 빈 줄은 원본 SHA가 같은 증거로 보존했다. [공백 검사 예외](publication-evidence/whitespace-preservation.json)에 정확한 파일·라인·해시를 기록했고 나머지 파일은 엄격한 공백 검사를 통과했다.
