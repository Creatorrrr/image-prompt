# Neutral expression data merge

로컬의 neutral 대체 표현·후보·회귀·세 독립 native 사례와 원격의 문맥 대체 표현·회귀·연구 증거를 함께 병합한다. 로컬 작성 결과는 `96f938e264a3ce4fdfc22bbc3d9548583059c5b0`, 실제 pull로 받은 원격 parent는 `7307343d59bcd09624c2ea2aad461d8d5d9dd026`, 공통 기준은 `10937f9553f02ce75d3244abc11286ff45412ea9`다.

## 양쪽 의도 보존

- 로컬: 44개 시각 의미의 대체 표현 176개, 구성요소·소유자 대체 표현 114개, 기존 후보 42개의 대체 표현 154개, 새 시각 의미 3개와 일반 후보 2개, 도덕적 타락과 신체 변형의 구별, 실제 native 이미지·프롬프트·실패 기록을 유지했다.
- 원격: 독립 biohybrid 몸체의 소유권 근거, 소환 사건의 이미 선언된 국소 결과 대안, liminal 공간의 이미 선언된 유지·운영 단서 대안과 그 회귀·출처 조사·기존 범위 유지 기록을 유지했다.
- 같은 base 파일에서 로컬이 바꾼 12개 profile과 원격이 바꾼 3개 profile의 ID는 겹치지 않았다. 병합된 각 profile이 해당 작성 parent와 완전히 같은지 검사했다.
- 로컬의 변경 파일 688개와 원격의 변경 파일 32개 중 겹친 파일은 원본 base registry와 파생 visual index 두 파일뿐이다. 나머지 파일은 각 parent의 Git blob과 동일함을 확인했다.

실제 충돌은 파생 `photo_prompt_visual_profile_index.json` 하나였다. 어느 parent의 인덱스 해시를 고르는 방식 대신 합친 원본 registry에서 builder를 실행했다. 양쪽의 호환 캐시를 사용했고 추가 임베딩 호출은 0회다. 1,510개 entry의 문장·벡터·메타데이터, exact lookup과 BM25F는 로컬 검증본과 같으며 전체 인덱스 차이는 `registry_sha256` 하나다.

합친 registry 해시는 `e536af9904e7da752552ddbee04b590be3ebbb9a8803b640510f1f4c4e97d2d8`다. ordinary corpus는 기존 `0620af2ed2904452df6cf761e1f1825a527777f08720dc82bd760f92e501d83e`를 유지해 9,703개 후보/112개 슬롯, semantic index 9,739개 entry/16개 shard의 metadata 검사가 통과했다.

## 병합 후 확인

dictionary validator, visual profile index check, semantic index metadata, staged diff whitespace 검사가 통과했다. 기존 세 arm의 실제 초기 core·envelope·controls·review와 기록된 seed로 정상 public V6 CLI를 다시 실행했다. 세 후보팩 모두 기존 파일과 바이트까지 같고, 현재 sibling photo 기준값도 같은 SHA다. 이미지 추가 생성은 하지 않았고 원래 픽셀 결과 A/B FAIL, C의 정한 기준 PASS와 사용자 수락 pending 상태를 바꾸지 않았다.

전체 unittest discovery에서 1,253개 테스트를 368개 독립 배치로 실행했고 모두 통과했다. 실패 배치 0개이며 발견된 ID 전체가 실행됐음을 확인했다. 검사 전후 운영 입력 92개의 SHA-256도 같았다. 결과는 `VALIDATION.json`에 저장했다. 큰 부모 색인 캐시는 Git parent에서 다시 얻을 수 있으므로 중복하여 커밋하지 않는다. 전체 실행 로그와 발견된 테스트 ID·결과는 `diagnostic-evidence.tar.gz`와 SHA-256 manifest로 보존한다.

- [전체 검증 결과](VALIDATION.json)
- [전체 진단 증거 SHA-256](diagnostic-evidence-manifest.json)
- [양쪽 원본·blob 보존](AUTHORED-PRESERVATION.json)
- [파생 인덱스 확인](INDEX-VERIFICATION.json)
- [동결 사례의 실제 CLI 재실행](FROZEN-PACK-REPLAY.json)
- [사전·색인 검사](VALIDATORS.json)
- [병합 운영 입력 92개](OPERATIONAL-INPUTS.json)

이 문서는 병합 parent와 검증 결과를 기록한다. 이전 neutral 통합·native 보고서는 원래 실행 당시의 commit/입력 해시를 유지하는 역사 증거다. 기존 generated 이미지의 결과를 새 생성이나 데이터 추가의 인과 효과로 해석하지 않는다. 작업 도중 생긴 별도 religion/myth 연구의 미추적 파일은 이 작업의 stage·commit·push 범위에 포함하지 않는다.
