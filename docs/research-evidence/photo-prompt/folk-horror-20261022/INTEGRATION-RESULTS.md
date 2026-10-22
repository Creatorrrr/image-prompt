# 포크 호러 데이터 반영 결과

2026-10-22. 앞선 리서치 전용 단계에 이어, 사용자의 데이터 반영·독립 3개 이미지 테스트 요청을 실행했다. 이 문서는 데이터와 검색 증거를 다룬다. 실제 생성물 판정은 [IMAGE-TEST-RESULTS.md](IMAGE-TEST-RESULTS.md)에 별도로 기록한다.

## 실제 반영 범위

| 항목 | 반영 결과 |
|---|---|
| 원 대화 키워드 | 150개 경로 유지, 각 경로에서 실제 CID로 연결 |
| 시각 의미 | 89개 카드: 가시 실현 70개, 비가시·역사·해석 경계 19개 |
| 새 후보 | 완전한 한영 가시 옵션 69개 + 양성 검색에서 제외한 진단 19개 |
| 재사용 | R01 공동체 원/방문자/길의 기존 whole source 1개, 원문·조건·effects 보존 |
| 연결 | 기존 슬롯으로 optional binding 133개 추가 |
| 전체 데이터 | 후보 19,471 → 19,559, 양성 CID 19,187 → 19,256, binding 13,644 → 13,777 |

가시 카드 70개와 후보 70개는 같은 연구 단위다. 이를 합쳐 140개라고 세지 않는다. 새 CID는 진단을 포함한 88개다. 모든 새 후보는 `native_approval: false`이며 native 의미 자격을 획득한 것으로 취급하지 않는다.

실제 파일:

- [시각 의미 registry](../../../../skills/photo-prompt-image-generator/assets/photo_folk_horror_semantics_20261022.json)
- [후보 모듈](../../../../skills/photo-prompt-image-generator/assets/photo_candidate_folk_horror_20261022.json)
- [binding 모듈](../../../../skills/photo-prompt-image-generator/assets/photo_candidate_folk_horror_bindings_20261022.json)
- [선택·혼동 경계 설명](../../../../skills/photo-prompt-image-generator/references/folk-horror-visual-semantics.md)

위 상대 경로는 저장소 루트 기준으로 연결한다. 모듈 두 개를 기존 corpus manifest에 추가하고 작업 인덱스를 재구축했다. 기존 19,471개 후보, 13,644개 binding, 기존 개별 모듈·slot catalog·정책·중립 저작 코드·SKILL은 작업 시작 시의 바이트를 보존했다. 시작 때 이미 변경되어 있던 파일을 원복하거나 별도 작업까지 커밋하지 않았다.

## 의미를 어떻게 담았는가

장르 이름을 소품 목록으로 확장하지 않고, 물체·소유자·부착·위치 관계와 화면에서 구분할 조건을 한 단위로 저장했다. 예를 들어 낮게 패인 옛길은 양옆 흙둑과 노면의 높이차가 필요하고, 문턱의 그릇은 문턱과 실내/실외 위치가 함께 보여야 한다. 밀봉 불투명 병의 외형과 열린 병의 내용물은 별개의 완전한 옵션이다.

금줄/시메나와, 장승/솟대, 마녀 방어 표식/피부에 대한 낙인, 모형/시신, 희생/붉은 액체를 구분했다. 초자연적 정체·숨은 원인·동의·역사적 실재를 외형만으로 승인하지 않는다. 효과 범위는 각 source의 전체 내용을 기준으로 작성했으며, 연구의 관계 그래프가 typed native fact나 소유자 권한을 만들어내지는 않는다.

`research_semantics`에 복사한 `registration`·`adoption`은 리서치 당시 제안의 스냅샷이다. 현재 등록 결과는 `registration_status`, 실제 manifest, CID 및 이 보고서로 확인한다. 출처 해시는 웹 문서 원문을 수집한 해시가 아니라 연구 명세의 바이트 해시다. 43개 출처가 150개 모든 용어의 개별 원전 검증을 뜻하지 않는다.

## 검색·설치 검증

| 검증 | 결과 | 증거의 한계 |
|---|---|---|
| 데이터 구조·참조·분류 검사 | 7개 필수 검사 PASS, 사전 validator 오류 0 | 실제 이미지 의미를 증명하지 않음 |
| 기존 회귀 검사 | 46개 unittest PASS | 별도 전체 제품 QA는 아님 |
| canonical 변환 | 88개 신규 source의 원문 snapshot 정확 보존, 기존 19,471개 그대로 | native 의미 승인 아님 |
| 작업 인덱스 | 789개 closure 무결성 PASS | 순위 적합성은 별도 |
| 설치 release | sealed code/data와 deployed recorder 검사 PASS | 개별 후보의 자격은 별도 |
| 한영 검색 | 104개 질의 × 전/후 2회 = 208회 실제 실행 | source에서 만든 개발 질의이며 독립 holdout 아님 |
| 목표 검색 | 개발 48개 질의 모두 목표 CID가 상위 10개 및 32개 안에 노출 | 강제 선택·정답 채택·픽셀 성공을 뜻하지 않음 |
| 대조 검색 | 56개 중 31개 질의의 상위 10개에 새 source가 나타남 | 노출 자체를 오류로 세지 않으며 전체 의미 검토 필요 |

대조에서 나타난 신규 source 37건을 모두 검토했다. 시각 구분 참고 4건, 조건부 선택 가능 18건, 명시적 충돌로 skip 5건, 전체 의미가 다르므로 skip 5건, 범위 초과 skip 1건, 문맥 문의이므로 skip 2건, 추가 범위 검토 2건이다. 검색 잡음은 남아 있다. 예컨대 시데 제외 질의에 시데를 요구하는 source가 나타나거나, 밀봉 불투명 병 질의에 열린 병 source가 나타난 경우 전체 source를 보존한 채 제외해야 한다. 검색 점수를 의미 자격으로 승격하지 않았다.

임베딩은 기존 로컬 EmbeddingGemma 공간을 유지했다. 작업 인덱스에서는 기존 19,187개 벡터, 설치 H-F2에서는 기존 19,189개 문서 벡터를 그대로 재사용하고 신규 양성 69개만 계산했다. 외부 임베딩 서비스를 호출하지 않았다. 현재 sealed kernel 코드를 바꾸지 않았다.

실행된 검색은 raw whole-pool probe다. 실제 slot sampling, 배제 조건의 투영, 선택 승인과 구분한다. 생성 arm은 별도의 정상 managed workflow에서 자연 검색·전체 source 검토·대안 비교·프롬프트/픽셀 검사를 수행한다.

개발 질의의 지정 target은 새 CID이므로 반영 전 target 회수는 0/48이었다. 이 전후 차이 자체가 기존의 유사 후보보다 의미 품질이 높아졌다는 증거는 아니다. 새 자료의 검색 가능성을 확인한 결과이며, 기존 동등 후보 전체에 대한 독립 정답 평가나 이미지의 인과적 개선 측정은 수행하지 않았다.

## 설치된 세대와 복구 경계

| 항목 | 값 |
|---|---|
| 새 H-F2 generation | `0ad30ffe246d77f7c711ea49244b407b71ff747cbc33b380f6f12aaacd657cf2` |
| 새 native generation | `4cf1bf4117010c240ccb49148e2ee1bd5be2ca58d79c1f1521888aa16f9c0b20` |
| 새 source fingerprint | `23c16288d9d7c1bd7f3aaebb28c45e757e079220c5c711851244b2f17d744415` |
| 새 작업 layout | `cf9b845706c0381f97ea7a68e729845fe187024ea2be1e2c1ad0870000788692` |
| 이전 H-F2 generation | `0df1fb14b8c36b9580c218e0e931039dc695593c3f5d9cdc30f61d6c8ede42b9` |
| 이전 native generation | `19795ff984fbc3d90e804d7a74b8ca2d138defa2134be76a64858e6c9d669c9f` |

설치 store는 `/Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed`다. `retrieval-runtime.json`의 기본 H-F2 선택은 새 세대로 바뀌었으며 세 arm 모두 이 세대에 binding됐다. 이전 설치 세대는 유지한다. 복구가 필요하면 기존 installer로 위 이전 qualified release를 다시 선택할 수 있다. 이미 발급된 run은 자신의 세대와 receipt를 유지한다.

별도의 로컬 native `CURRENT.json`은 변경하지 않았다. 시작/설치 후 SHA-256은 모두 `8ad5fa8e361ad4607f6a7b12a5c8b95d6ed96413084a91ac09145c143ef040c4`다. 작업 source/index와 H-F2 기본 설정 변경을 이 CURRENT 보존과 혼동하지 않는다. commit/push는 수행하지 않았다.

최종 Git 비교에서 동시 작업의 surreal/posthuman 데이터 출판 커밋과 merge로 HEAD가 시작의 `17c0dd349304a18abac290beae114f199114e379`에서 `332d98937a69021e80846619526fe1d851bb6ada`로 이동한 것을 확인했다. 이 작업은 commit/push를 실행하지 않았고 해당 커밋을 되돌리지 않았다. HEAD 동일성을 주장하지 않고, 실제 보호 대상 62개 working file의 바이트 동일성과 이번 새 파일의 미커밋 상태를 별도로 확인했다.

## 재검토 가능한 증거

- [원본 보존](integration-evidence/source-preservation.json), [필수 데이터 검사](integration-evidence/focused-data-checks.json), [canonical source 검증](integration-evidence/canonical-source-validation.json)
- [질의·벡터 실행 근거](integration-evidence/qualification-query-evidence.json), [104개 전후 결과](integration-evidence/retrieval-qualification.json), [대조 37건 전체 의미 판정](integration-evidence/control-semantic-review.json)
- [작업 인덱스](integration-evidence/working-integration.json), [새 release](integration-evidence/successor.json), [설치 recorder](integration-evidence/installed-recorder-check.json)
- [회귀 검사 로그](integration-evidence/focused-checks.log), [사전 validator](integration-evidence/dictionary-validation.log), [설치 로그](integration-evidence/install-activation.log)
- 재현 helper는 `integration-evidence/*.py.snapshot`이며 작업 코드는 `generated/maintenance/folk-horror-20261022/`에 남겼다. 스냅샷은 즉시 재실행 지시가 아니다. 재구축 전 현재 source·동시 작업·발급된 run 경계를 다시 확인해야 한다.

첫 연구 단계의 [VALIDATION.json](VALIDATION.json), [PIXEL-PLAN.md](PIXEL-PLAN.md)와 `NOT_RUN`은 당시의 연구 증거다. 계획했던 36장 A/B/C나 모든 카드의 픽셀 검증을 이번 3장 테스트로 완료했다고 보고하지 않는다.
