# P0 반영 결과

작성일: 2026-10-07. 기준 HEAD: `4c9a0054473c4383ca5287ca3bf294b277e5c6e7`. [상세 계획](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-07-photo-skill-session-review/P0_PLAN.ko.md)의 두 P0를 현재 작업 폴더에 반영했다. commit·push·PR 생성은 수행하지 않았다.

## 반영 내용

| 영역 | 결과 |
|---|---|
| 의미 판정 | `photo-meaning-diagnostics/v1`에 원본 축 값·매칭 문구·기대/실제 클래스·관계 구조·문맥 근거를 기록. 누락, 표현 미인식, 클래스 차이, 명시적 제외, 부정/미해결 극성을 구분 |
| 관계 | 실제 operator 부재와 구성원·endpoint·선후 차이를 분리. same_target의 구성원 순서는 의미를 바꾸지 않음 |
| clarification·감사·뷰 | `photo-semantic-clarification/v2`로 갱신. ‘긍정 문맥을 못 찾음’을 ‘다른 의미로 해결됨’으로 설명하지 않음. 원본 source에서 진단을 재계산하고 catalog/details에 보존 |
| 작성 DATA | open_warmth의 검토된 대응 표현 3개 추가. 기존 얀데레 프로필의 affect_leak_intentionality 요구/제외 조건만 보조 axis_advisories로 이동. 다른 프로필과 동결 core의 요구·관계를 유지 |
| API 진입점 | pack·정확한 receipt·composed·render request 필수. 두 감사를 실제 수행하고 감사한 runtime 문자열만 전송. 미감사 prompt-json/folder 실행 경로 제거 |
| 지원 범위 | 현재 API lane은 text-only. 참조·활성 reference-edit mode·미지원 runtime 추가 문장을 호출 전에 거부하며 원문이나 참조를 자동 변경하지 않음 |
| 실행 기록 | exact-input preflight 파일/해시, runtime UTF-8 해시, core/intent/repair·선택 ID, 요청 모델/크기와 관측 모델/request ID를 연결. 성공 이미지 파일 해시 보존 |
| 오류·재시도 | 전체 오류 bytes와 기존 native capture 유지. 명시적 block·미관측 결과·저장/기록 실패는 자동 재호출 중단. 허용된 transient HTTP retry는 같은 입력과 바로 전 run_id를 사용 |

얀데레 이름을 검사하는 코드 분기는 추가하지 않았다. 해당 항목의 조정은 작성 데이터에 있으며, 공통 판정기에서 처리한다. 스킬의 초기 의미 해결·독립 baseline·사용자 정의 우선순위·속성 잠금·선택 후보의 advisory 권한을 유지했다.

## 주요 구현

- [공통 의미 진단](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/photo_meaning_diagnostics.py)
- [프로필·문맥 판정](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py:5572)
- [API 입력 준비·원본 바이트 재검증](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/photo_api_render.py)
- [API 실행 진입점](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/generate_images_via_api.py:107)
- [레저 연결 검증](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/record_image_run.py:207)
- [실행 안내](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/image-runtime.md)

기록 검증은 sidecar의 구조 미리보기 대신 보존한 원본 UTF-8 입력을 다시 파싱한다. 미리보기 JSON의 키 정렬이 동결 설정의 authoring brief 재검증에 영향을 주던 문제를 이 경계에서 해결했다. 원본 request·pack·receipt 파일을 사후 재독해 실행 입력을 바꾸지 않는다.

## 검증

중복 제거한 관련 테스트 **194개**를 확인했다. 전체 저장소 suite를 실행한 결과는 아니다.

| 범위 | 검증 |
|---|---|
| 의미·프로필·composer view | 32개 통과. 원문 공백·offset, 부정/극성, 다국어 대응 표현, 관계 구조, 원래 판정의 보존, 진단 변조 거부 |
| API·오류 증거 | 32개 통과. 미감사/변조 입력 0회 호출, 실제 감사기, 정확한 전송·레저 연결, 원본 사후 변경, raw HTTP/UTF-8/native 오류 보존 |
| 추가 불변 조건 | 4개 통과. 진단 변조, transient retry 동일 입력·즉시 연결, 기록된 policy block 중단, unknown 결과 중단. 진단 변조는 위 의미 범위와 중복 제거 |
| core·조회·설정·격리·manifest | 67개 통과 |
| runtime freshness | 실제 파일·generation 경계의 지정 4개 통과. receipt 부정합, pinned 재감사, 구 worker 거부, snapshot 불변성 |
| visual/embodiment/repair | 최초 묶음의 통과 사례와 실패 지점 재검증을 합산. 실패했던 문맥/등록 조회와 publication race를 해결한 후 해당 사례 및 embodiment pipeline 5개 통과 |
| dictionary/index | dictionary 검증 통과. semantic index 10,536개 모두 기존 벡터 재사용, 임베딩 호출 0회 |
| 최신 실행 묶음 | 실제 receipt 세대에서 두 감사 및 dry-run 통과. key 조회·네트워크·실제 이미지 호출 0회 |

초기 실패·중단 로그도 보존했다. 최초 runtime 묶음은 1개 실패와 setUpClass 오류가 있었으므로 해당 로그 전체를 PASS로 세지 않았다. 검증 JSON에 고유 테스트 ID와 재검증 내역을 기록했다.

검증 근거: [테스트 ID·로그·호출 수](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-07-photo-skill-session-review/p0-implementation/VERIFICATION.json), [인덱스 갱신](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-07-photo-skill-session-review/p0-implementation/INDEX_REBUILD.json), [실제 입력 dry-run](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-07-photo-skill-session-review/p0-implementation/DRY_RUN.json).

## 소스 세대와 기존 작업 보존

- 최종 dry-run generation: `88555987df57257d770c1488ce2e3f0bb772a28e2f2d34a46f1b5757942db045`
- source fingerprint: `71ffc1b9e1324f1e7c20c17a13ba8a2bb45cc1fd2afa6e9c56e5666a16ace1d9`
- pack ID: `17ef844953b7e076`
- 기존 미커밋 추적 파일 중 의도적으로 갱신한 semantic index를 제외한 14개가 시작 시점과 byte-identical하다.
- 시작 시점 index가 참조하던 기존 shard 16개 모두 보존됐고 파일 해시가 같다. 역사 pack·레저를 새 계약으로 다시 쓰지 않았다.
- HEAD가 시작 시점과 같다. 기존 source registration과 visual index의 미커밋 작업을 보존했다.

근거: [작업 전 기준](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-07-photo-skill-session-review/p0-implementation/BEFORE.json), [보존 확인](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-07-photo-skill-session-review/p0-implementation/PRESERVATION.json), [변경 후 소스 해시](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-07-photo-skill-session-review/p0-implementation/SOURCE_AFTER.json), [최종 runtime publication](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-07-photo-skill-session-review/p0-implementation/runtime-publication-final.log).

## 사용과 한계

새 API CLI의 입력은 다음 네 파일이다. 유지보수에서 준비·감사만 확인할 때는 `--dry-run`을 붙인다.

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_images_via_api.py \
  --pack /absolute/path/pack.json \
  --runtime-receipt /absolute/path/receipt.json \
  --composed /absolute/path/composed.json \
  --render-request /absolute/path/request.json \
  --dry-run
```

이번 검증은 판정·source·실행 입력·기록 경계의 증거다. 실제 이미지 생성, OpenAI 제공자의 live 응답, 픽셀 품질 비교, 사용자 수용 평가는 실행하지 않았다. 표현 인식은 검토된 어휘와 제한된 부정 범위이며 모든 자연어의 의미·대상 관계를 이해하는 모델 판정이 아니다. 참조 API transport와 P1 품질 비교는 이 P0의 완료 범위 밖이다.
