# H 단독+F2 설치본 기본 검색 적용

2026-10-18 · 기본 검색 적용·실제 실행 검증 PASS · native CURRENT 유지

현재 설치된 `photo-prompt-image-generator`의 새 managed run은 평범한
`photo_workflow.py retrieve --run RUN`으로 H 단독+F2를 사용한다. 별도
`--retrieval-policy`, `--generation-id`, `--runtime-store`는 필요 없다.
후보나 테스트 요청을 연구 디렉터리에서 실행 중 읽어 오는 방식이 아니다.

## 적용 방식

- 설치본의 `photo_workflow.py`가 `photo_installed_h_f2.py`를 통해 검증된
  실행 세대를 선택한다. `retrieval-runtime.json`은 코드·검색·native 감사
  세대를 함께 고정한다.
- 검증한 코드, canonical 후보 원문, F2 문서·posting·통계·벡터를
  `~/.cache/image-prompt/photo-shared-runtime/h-f2-installed`에 실제 복사했다.
  실행 전 코드 봉인과 세대 연결을 확인하고, 원문과 벡터는 기존 검증기로
  검증한다. 연구 checkout이나 원래 build cache에 대한 런타임 의존성은 없다.
- CURRENT는 수정하지 않았다. 기존 main의 미커밋 source-effects 수정과
  기존 corpus/index 자산도 바꾸지 않았다. 서로 다른 corpus 스키마나 native
  감사 구현을 섞지 않기 위해 검증된 세대의 실행 코드와 감사 코드를 함께
  사용한다. 이미 발급된 이전 native run은 원래 설치본의 receipt 경로를 유지한다.
- 스킬 소유 로컬 임베딩 Python·모델·worker의 정확한 binding을 확인한다.
  native 검증용 모델 파일도 설치하고 Python 환경만 기존 스킬 런타임에
  연결했다. 기본 `.venv`에 NumPy가 없어도 일반 명령으로 실행된다.
- `build_photo_slot_intents.py`는 직접 작성한 전체 의도·슬롯별 목표·검색어에
  구조적 hash를 붙인다. 검색어, 의미 판정, 슬롯 태그는 생성하거나 바꾸지 않는다.
  스킬과 실행 문서도 이 기본 경로 및 managed 감사 명령을 사용하도록 수정했다.

설치된 H-F2 세대:
`663038595155d8d48bfa20339bbe7a5c3128eea4ce504900c9a8fdadd34c152b`

함께 설치된 native 감사 세대:
`9649504ffbcd1ebe7d9aedf9eab821fc18aa0300a8f70b65dbdd145b435ec1da`

실행 코드 원본은 앞서 커밋·검증한 `8469562a4`의 봉인된 배포 산출물이다.
이번 커밋은 그 산출물을 실제 설치본의 기본 진입점에 배포·연결한다.
연구 브랜치 전체를 main에 병합하는 작업은 하지 않았다.

## 실제 기본 명령 검증

기존 실제 managed 요청의 요청/core/controls/기본 프롬프트를 보존해 새 run을
만들었다. 채플에서 천을 바치는 인물의 조명·구도 표현 목표와 검색어는 직접
다시 작성했다. 새 두 검색어는 캐시에 없어 로컬 모델로 실제 임베딩했다.
추가 검토한 날씨 슬롯은 비적용으로 기록했다.

전체 CLI 실행 동안 macOS `sandbox-exec`로 네트워크와 연구 checkout,
원래 H-F2 store 및 관련 build cache의 읽기를 차단했다. 네트워크 접속과
차단 경로 읽기가 실제 `Operation not permitted`로 거부되는 것도 확인했다.

| 검증 | 결과 |
|---|---|
| 기본 `retrieve`에 policy/generation/store flag | 사용하지 않음 |
| 표현 계획 없는 첫 retrieve | authoring 요청; 검색0회 |
| 검색한 슬롯 | lighting, composition |
| 각 슬롯 대상 | 기존 positive CID18,180개·RID18,182개 전체 |
| 기존 후보 집합 | 설치본 corpus와 snapshot의 전체 CID18,250개 집합 일치 |
| 각 슬롯 호출 | BM25F1회 + local cosine1회 |
| 새 query 임베딩 | 로컬 모델로 서로 다른 text2개 실제 실행; cache hit0 |
| 날씨 슬롯 | 검색0회 |
| 반환 | 각 슬롯 top8, 총16연결 |
| view와 CID 상세 | PASS |
| 반복 retrieve·resume | 저장된 원래 증거 재사용; 추가 검색0회 |
| compose-audit·deliver | PASS; 원래 최종 prompt와 core 유지 |
| Gemini·이미지 호출 | 각각0회 |
| native CURRENT | 원래 SHA256 유지 |

H-F2 소재를 native 후보 채택으로 둔갑시키지 않았다. 원래 native 선택은
빈 목록으로 유지하고 소재1건에는 명시적인 `skip` 결정을 기록했다. 이
검증은 검색·조회·새 로컬 추론·감사·프롬프트 전달의 실제 통합 검증이다.

## 기존 평가 재현과 회귀 확인

새 설치에서 실제 사용할 NumPy2.5.4로 기존8개 목표를 다시 검색했다.
기존64개 판정의 CID/RID/원문 hash 연결을 그대로 재사용했다.

- BM25F와 cosine 원시 점수:8개 모두 비트 단위 일치.
- 전체 순위8개와 top8 연결64개: 모두 정확 일치.
- 기존 품질 결과: 창작 소재7/8, 원문 조건을 지킨 활용4/8, 스케치 요청3/4 유지.
- 검색은 목표별1+1; query 증거는 재사용하고 새 의미 판정은 하지 않았다.
- 설치 진입점·변조 거부·누락 시 fallback 차단·기존 run 보존·neutral freeze·
  상태·transport·기존 source-effects 관련23개 테스트 통과.
- 기존 dirty 파일7,928개의 원래 bytes 및 기존 staging 공백을 확인했다.
  작업 전후 native CURRENT SHA256은
  `8ad5fa8e361ad4607f6a7b12a5c8b95d6ed96413084a91ac09145c143ef040c4`로 같다.

## 실행과 유지보수 경계

실제 설치본의 기본 경로 적용을 완료했다. 작은 합성 평가의7/8을 모든149개
슬롯의 Recall로 확대하지 않으며, 이미지 생성·픽셀·새 사용자 선호는 검증하지
않았다. 이번 작업은 기존 품질을 보존해 배포한 것이며 새 품질 향상 실험이 아니다.

실행 세대는 고정된 snapshot이다. 작업 corpus 편집이나 CURRENT 변경이 여기에
자동 반영되지는 않는다. 후보 데이터/검색 코드를 갱신하려면 새 전체 세대를
준비·검증하고 `install_photo_h_f2_runtime.py`로 명시적으로 설치해야 한다.
다른 컴퓨터도 검증된 배포 산출물과 로컬 임베딩 설치가 필요하다. 대형 코드/
데이터/모델 런타임은 cache에 있고 Git에는 설치 도구·선택 manifest·문서·검증
증거를 보관한다. 자동 다운로드나 원격 fallback은 없다.

[실제 기본 실행](../research-evidence/photo-prompt/h-f2-installed-default-20261018/DEFAULT-SMOKE.json)
· [기존 평가 재현](../research-evidence/photo-prompt/h-f2-installed-default-20261018/PARITY.json)
· [기존 파일/CURRENT 보호](../research-evidence/photo-prompt/h-f2-installed-default-20261018/PRESERVATION.json)
