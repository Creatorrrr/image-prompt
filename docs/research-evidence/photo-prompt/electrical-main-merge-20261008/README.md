# 전기 데이터와 최신 main 병합

2026-10-08. 원격 main을 pull한 뒤 전기 시각 의미·후보 데이터와 동결된 연구/이미지 평가 증거를 병합했다. 기본 체크아웃의 다른 dirty/untracked 작업은 배포 범위에 넣지 않는다.

## 양쪽에서 유지한 의도

- Pulled main: `d77ee2f232e2fc670c998eb85cbac9590348dedc`. 앞 지퍼 수영복의 center-front 관계에 잘못 붙어 있던 `back zip` alias/keyword와 visual paraphrase/concept term 제거를 유지한다.
- 이번 작업: 연구 91개 카드의 후보 98개·새 시각 의미 프로필 97개, 전기 회귀 테스트와 연구/독립 native 평가 증거를 그대로 추가한다. 후보·프로필 원본은 이전 검사 때의 SHA256과 일치한다.
- 중앙 manifest의 기존 모든 등록 행은 원격 main의 순서와 값을 보존한다. 전기 candidate/visual-profile만 각각 load_order 61/43으로 추가한다. 기본 체크아웃의 미게시 등록과 기존 load_order는 로컬 복원 단계에서 별도로 보존한다.
- 원격 main의 자산 805개 중 804개는 byte-identical이다. 나머지 수영복 candidate 파일은 `maintenance_ref`만 후속 기록으로 변경했다. 기존 원본의 다른 모든 필드, visual profile 및 이전 maintenance record는 유지했다.

## 수영복 출처 결합 보정

첫 63개 회귀 실행에서 기존 수영복 maintenance record가 수정 이전 source digest에 결합된 문제가 발견됐다. `upstream-binding-baseline.log`는 해당 검사의 입력 source와 record가 pulled main bytes와 같음을 확인하고 동일 실패를 재현한 기록이다.

이전 record를 수정하지 않고 `swimwear-front-zip-binding-20261008.json`을 추가했다. 후속 record는 이전 maintenance_ref를 그대로 연결하고, 수정된 현재 source의 digest를 인증한다. 이번 보정으로 슬롯·후보의 시각 내용·profile/gates·코드·원본 연구 계약은 바뀌지 않는다. 검사의 기대값이나 기준은 수정하지 않았다. 세부 hash와 의미 보존 확인은 `SWIMWEAR-BINDING-REPAIR.json`에 있다.

## 인덱스와 검사

Semantic/visual indexes는 병합된 원본에서 다시 생성했다. Gemini `gemini-embedding-2` / 768 dimensions의 identity·positive text·recipe·model·dimension이 맞는 벡터만 재사용했다. Rebuild helper는 임베딩 호출과 socket network access를 차단한다. `INDEX-REBUILD.json`에는 10,845 semantic entries, 2,602 visual profiles, embedding calls 0 및 실제 immutable runtime receipt가 있다. 이전 shard는 삭제하지 않았다.

최종 검증은 `VALIDATION.json`과 `focused-tests.log`, `dictionary-validation.log`를 따른다. 선택한 회귀 범위는 전기, 수영복, candidate semantics, semantic index, visual profile shards다. 첫 실패 로그와 원인, 보정 전 인덱스 receipt는 삭제하지 않고 initial 파일로 남겼다. 전체 테스트 discovery를 실행한 것으로 보고하지 않는다.

## 이미지 증거의 판정 유지

이 병합에서 이미지를 다시 생성하지 않았다. 이전 세 독립 arm의 원본 출력·exact prompt·기준·조회/선택/감사 기록 150개 파일을 byte-identical로 보존했다. 주요 방전 형상은 세 장 모두 보였지만 전체 필수 장면은 폭풍 조타실 1개만 PASS다. 박물관 장면의 손 접촉 대상과 등대 장면의 두 번째 램프 배선 끝점은 FAIL이다. 사용자 선호 및 동일 장면 baseline 비교는 미판정이다.

이전 native run은 generation `2834651af2b0ea5161d8a8cc743ff23525b6479a89a30bcda7ee6af05b632da6`의 snapshot을 사용했다. 현재 main으로 병합·인덱스 검증한 사실을 새로운 native 검증으로 바꾸어 보고하지 않는다. 원본 결과는 `../electrical-semantics-20261008/integration/FINAL-REPORT.md`와 qualification 폴더에 있다.

## 게시·기본 체크아웃 검증

`COMMIT-SCOPE.json`의 명시된 경로만 stage한다. 기본 체크아웃 동기화는 fast-forward로 수행하고, unrelated dirty bytes와 로컬 미게시 등록을 복원한 뒤 전체 로컬 corpus의 indexes를 다시 생성한다. 백업은 `.codex-artifacts/`에 보존한다. 실제 최종 commit·원격 main·기본 HEAD 일치와 보존 결과는 로컬 `FINAL-PUBLICATION.json`, `PRIMARY-SYNC-VERIFICATION.json`에 기록한다.
