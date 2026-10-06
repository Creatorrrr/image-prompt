# 후보·시각 의미 데이터 관리 도구

후보와 시각 의미 원본을 분리한 현재 구조에서 전체 점검과 양방향 연결 조회를 제공한다. 표준 라이브러리만 사용하며 이미지·임베딩 API를 호출하지 않는다. 원본 수정, Git 갱신, 검색 순위 변경, 필수 프로필 활성화는 수행하지 않는다.

저장된 보고서는 특정 검증 세대의 명시적 관계를 계산한 관리 산출물이다. 검색 결과나 의미 유사도를 저장한 캐시가 아니다. 후보 → 번들 → 프로필과 그 역방향을 같은 edge에서 조회하므로 양쪽 목록을 수작업으로 관리할 필요가 없다.

## 실행

저장소 루트에서 실행한다. `ROOT`, `RUNTIME`, `REPORTS`에는 원하는 절대 경로를 지정한다. 런타임 세대 ID는 기존 런타임 게시 결과나 후보 pack의 receipt에서 가져온다.

```bash
python -m tools.photo_data_maintenance.cli audit \
  --source-root "$ROOT" --runtime-store "$RUNTIME" \
  --output /ABSOLUTE/PATH/draft-audit

python -m tools.photo_data_maintenance.cli build \
  --source-root "$ROOT" --runtime-store "$RUNTIME" \
  --generation GENERATION_ID --output /ABSOLUTE/PATH/generation-report \
  --report-store "$REPORTS" \
  --reviews docs/data-maintenance/photo-data-review-decisions.ndjson

python -m tools.photo_data_maintenance.cli query \
  --report-store "$REPORTS" --source-root "$ROOT" --runtime-store "$RUNTIME" \
  --candidate slot:light_shape:lit_clean_vertical_catchlight_pair

python -m tools.photo_data_maintenance.cli query \
  --report /ABSOLUTE/PATH/generation-report \
  --profile clamshell_dual_source_portrait_light

python -m tools.photo_data_maintenance.cli diff \
  --before /ABSOLUTE/PATH/previous-report --after /ABSOLUTE/PATH/new-report
```

`--candidate`에는 슬롯까지 포함한 식별자를 쓴다. `--profile`, `--bundle`에는 원본 ID를 쓴다. 하나의 후보가 여러 번들을 경유하면 모든 경로를 보존한다. 정상 종료는 0, 구조·무결성·현재성 오류는 1이다. 명령 사용 오류는 argparse의 2이다.

## 점검과 정상 조회

`audit`는 편집 중인 원본을 직접 수집하고 입력 복사본, 위치, 오류를 보존한다. 등록표 누락·미등록 파일, 중복 키·ID, 깨진 참조, 순환, 기존 검증기 오류 등을 점검한다. 잘못된 입력에서도 진단을 남기지만 draft를 정상 연결 조회에 사용할 수 없다. 협력 유지보수의 미완료 편집은 `--runtime-store`를 지정하면 함께 감지한다.

`build`는 기존 런타임 로더가 검증한 불변 세대에서 후보·번들·프로필을 수집한다. 등록된 모든 원본과 기존 슬롯 문맥 확장을 포함한다. 세대가 불완전하면 정상 보고서를 만들지 않는다. `inputs/`, `inventory.json`, `findings.json`, `links.json`, `reviews.json`, `SUMMARY.md`, 해시를 포함한 `manifest.json`을 새 출력 폴더에 쓴다. 기존 출력은 덮어쓰지 않는다.

문장이 동일한 항목은 의미 검토의 단서로만 표시한다. 짧은 설명이나 추상적인 분위기 자체를 오류로 판정하지 않는다. 미연결은 선언된 관계가 없다는 정보이며 누락이나 데이터 불량을 뜻하지 않는다. 링크의 `meaning_support: not_inferred`는 번들 연관이 프로필 전체 외형 충족이나 요청의 필수 활성화를 증명하지 않는다는 뜻이다.

## 새 데이터와 현재성

새 파일은 기존 source manifest에 등록하고, 새 행은 해당 원본에 추가한다. 기존 유지보수 경로로 원본 검증·인덱스 재생성·런타임 세대 게시를 완료한 다음 `build`한다. 전체 등록 원본에서 관계를 다시 추출하므로 새 후보·프로필·번들과 이전 항목의 관계가 함께 반영된다. 임베딩이나 모든 항목의 의미적 연결 분석을 수행할 필요는 없다.

고정 `--report` 조회는 과거 세대를 명시적으로 허용한다. 현재 조회는 `--require-current --source-root ... --runtime-store ...`를 함께 사용한다. `--report-store` 조회에는 이 검사가 자동 적용된다. 실제 루트, 현재 런타임 세대, 원본 지문, 도구 코드·레시피, 보고서 파일 해시를 확인하며, 검증 세대에서 inventory를 독립 재계산해 비교한다. 편집 중이거나 현재 원본이 검증 세대와 다르면 오래된 결과를 현재 결과로 반환하지 않는다.

관리 `CURRENT`는 런타임 `CURRENT`와 별도 저장소에 게시된다. 늦게 끝난 게시 작업이 앞선 작업을 덮어쓰는 것을 방지하고 게시 직전에도 현재성을 재확인한다. 최신성 기준은 지정한 **로컬 원본**이다. 원격 main의 갱신 여부는 기존 Git/remote 런타임 갱신 절차에서 별도로 확보해야 한다. TTL이나 수정 시각만으로 최신성을 판단하지 않는다.

## 의미 검토 기록

검토 결정은 NDJSON에 별도로 보관한다. 각 기록은 대상 finding·edge·path와 관련 항목의 완전한 내용 해시, 레시피, 판단자·시각·근거를 결합한다. ID가 같아도 의미나 조건, 번들 구성원이 달라지면 관련 결정만 `stale`이 된다. 파일 이동만으로 내용이 변하지 않으면 유지할 수 있다. 검토 결정으로 구조 오류를 면제하거나 런타임 활성화를 바꿀 수 없다.

현재 샘플 기록은 동일 표현의 유지·보류 사례와 세로 캐치라이트의 부분 연관 사례다. 전체 데이터의 의미 검토 완료를 뜻하지 않는다. 설명 보강·중복 통합·새 관계 채택은 보고서를 근거로 원본에서 별도 검토한다.

## 검증

```bash
python -m unittest tests.test_photo_data_maintenance -v
python -m unittest tests.test_photo_data_quality_scopes tests.test_photo_instrument_semantics -v
```

도구 코드나 레시피가 바뀌면 이전 버전 보고서는 현재 도구의 무결성 검사를 통과하지 않는다. 해당 불변 세대에서 새 보고서를 만들거나, 과거 도구 버전과 함께 과거 보고서를 재현한다. 보고서와 점검 통과는 이미지 픽셀 품질이나 사용자 수용의 증거가 아니다.
