# 흙·땅 데이터 main 통합

2026-10-08 KST

원격 main을 fetch·pull한 별도 작업공간에서 흙 후보 96개, 시각 프로필 96개와 288개 픽셀 의무를 통합했다. 기존 물 후보·프로필 5쌍의 ID를 유지했다. 최신 main의 카메라 축 소유권 안내 수정도 함께 가져왔다. 미공개 intellectual 등록과 다른 작업의 dirty 원본은 이 커밋에 섞지 않았다.

## 양쪽 원본 보존

초기 main `579265f7`의 등록 원본 101개는 바이트를 그대로 유지했다. 나머지 물 원본에서는 기존 프로필·필드·표현을 유지하고 5개 프로필에 이번 흙 보강 paraphrase만 추가했다. 기존 후보의 효과·속성·ID는 변경하지 않았다. main manifest의 기존 행과 순서를 유지하고 흙 원본 2개를 candidate 60, visual_profile 42의 다음 등록 위치에 추가했다.

검증 후 main에 추가된 `71fdbb15`는 SKILL.md의 카메라 소유권 안내 수정이었다. 별도 축 anchor, 총 16개 anchor 한도와 기존 core 재생 경계를 확인하고 해당 수정 전체를 fast-forward로 가져왔다. 데이터·실행 코드·인덱스 입력은 동일했고, 작성 규약과 사전 격리 검사를 추가로 수행했다.

[원본 보존 증거](AUTHORED-PRESERVATION.json)에 main 원본 지문, 물 프로필의 실제 append 목록, 흙 원본 지문과 역사 자료 보존을 기록했다. 흙 연구·이미지 검증 파일 330개는 내용과 mode를 유지해 복사했다. 실행 캐시·LOCK·Python 캐시는 커밋 범위에서 제외하고 원래 작업공간에 남겼다.

## 인덱스와 검증

합쳐진 authored corpus로 canonical builder 함수를 사용해 semantic metadata, BM25F와 visual index를 재생성했다. 재사용 조건은 entry ID·전체 positive text·provider·model·차원 일치다. 네트워크와 새 임베딩 함수를 금지한 재생성에서 기존 벡터만 사용했다. 새 인덱스의 실제 shard 참조만 커밋하며 과거 shard generation을 삭제하지 않았다.

| 검사 | 결과 |
|---|---|
| 흙·물·후보 의미, BM25F와 visual retrieval | 49 tests PASS |
| 작성 규약·사전 격리 | 18 tests PASS |
| dictionary metadata | PASS |
| visual index 깊이 검사 | 2,505 profiles / 5,078 exact terms PASS |
| SKILL frontmatter | PASS |
| semantic index | 10,747 entries |
| 추가 embedding/image 호출 | 0 / 0 |

[VALIDATION](VALIDATION.json), [INDEX-REBUILD](INDEX-REBUILD.json)와 원본 로그에 실제 검사 범위를 보관했다. 이는 전체 테스트 스위트나 96개 프로필 전체의 이미지 품질을 통과로 주장하는 기록이 아니다.

초기 canonical CLI가 기본 환경의 provider key 검사를 요구한 기록과 기본 Python의 yaml 부재 기록을 보존했다. 호환 벡터만 허용하는 offline build 및 기존 .venv에서 같은 metadata 검사를 완료했다. 키를 출력하거나 환경 의존성을 새로 설치하지 않았다.

## 이전 이미지 검증의 의미

[독립 이미지 테스트](../soil-earth-semantics-20261008/image-tests/qualification-report.md)의 이미지 3장, 프롬프트, ledger, 실패 판정은 바꾸지 않았다. 당시 source generation과 SKILL 지문에 묶인 역사 관찰이며 최신 main으로 재해석하지 않는다. 코트 6/8, 부조 7/8, 우주선 온실 8/8이라는 자체 기대값과 신규 흙 프로필 미선택, 사용자 수용 미확인도 유지했다.

## 게시·원래 작업공간 동기화

커밋에는 흙 원본·물 5개 보강·manifest 2행·현재 인덱스/shard·흙 테스트·연구와 검증 자료만 포함한다. 실제 staged 범위는 COMMIT-SCOPE 기록으로 확인한다. 원격 main을 다시 확인하고 일반 fast-forward push를 사용한다.

원래 dirty 작업공간은 별도 before-byte backup을 만든 뒤 fast-forward한다. 겹치는 미공개 manifest는 파일 identity로 합쳐 기존 로컬 등록과 상대 순서를 유지한다. working corpus에 맞는 인덱스를 다시 생성하고 runtime을 검증한다. 예기치 않은 HEAD·staged·중첩 파일 변경은 덮어쓰지 않고 중단한다. 실제 게시와 보존 결과는 동기화 뒤 생성하는 FINAL-PUBLICATION 기록에 남긴다.
