# ReactorPrompt 증분 코퍼스 시각 의미 리서치

상태: **`proposed` — 연구·설계 완료, 런타임 미구현**

새로 수집한 ReactorPrompt 프롬프트 924개를 16개 주제에서 각각 전수 스캔하고, 주제별 양성·근접대조 코퍼스 이미지를 직접 검토했다. 16개 보고서의 표본 합은 게시물 검토 301회, 이미지 검토 593회이며 중복 표본을 포함한다.

## 핵심 산출물

- [종합 결론과 우선순위](synthesis.md)
- [기계 판독 후보 백로그](candidate-backlog.json)
- [검증 가능한 iteration record](iteration-record.json)
- [공통 연구 브리프](coordination/research-brief.md)

## 주제 보고서

| # | 주제 | 표본 | 보고서 |
|---:|---|---:|---|
| 1 | 구도·프레이밍·크롭·여백·주의 계층 | 20게시물·40장 | [보고서](topics/01-composition-framing.md) |
| 2 | 포즈·신체 역학·지지·접촉 | 16게시물·32장 | [보고서](topics/02-pose-body-mechanics.md) |
| 3 | 카메라 시점·렌즈·원근·심도·초점 | 17게시물·34장 | [보고서](topics/03-camera-optics-focus.md) |
| 4 | 조명·노출·그림자·필·림·재질 반응 | 20게시물·40장 | [보고서](topics/04-lighting-exposure-material-response.md) |
| 5 | 색·화이트밸런스·톤·그레이딩 | 12게시물·24장 | [보고서](topics/05-color-palette-tone-grading.md) |
| 6 | 환경·배경·깊이·대기·날씨 | 32게시물·47장 | [보고서](topics/06-environment-depth-atmosphere.md) |
| 7 | 피사체–소품 상호작용·도구·상태 | 15게시물·30장 | [보고서](topics/07-subject-prop-interaction.md) |
| 8 | 다중 피사체·시선·가림·관계 토폴로지 | 23게시물·43장 | [보고서](topics/08-multi-subject-staging-relations.md) |
| 9 | 표정·시선·머리 방향·가독성 | 18게시물·36장 | [보고서](topics/09-expression-gaze-readability.md) |
| 10 | 의상·구성·소재·질감·드레이프 | 14게시물·28장 | [보고서](topics/10-wardrobe-material-drape.md) |
| 11 | 헤어·메이크업·피부·beauty capture | 15게시물·30장 | [보고서](topics/11-hair-makeup-skin-beauty-capture.md) |
| 12 | 촬영 매체·스마트폰·플래시·그레인·처리 | 25게시물·50장 | [보고서](topics/12-capture-medium-processing.md) |
| 13 | 사건 타이밍·미완 전환·가시 결과 | 16게시물·29장 | [보고서](topics/13-narrative-event-timing.md) |
| 14 | negative·false substitute·artifact·실패 예방 | 21게시물·42장 | [보고서](topics/14-negative-constraints-failure-modes.md) |
| 15 | clause 소유권·중복·번역 drift·evidence budget | 14게시물·28장 | [보고서](topics/15-prompt-language-architecture.md) |
| 16 | 제품·음식·건축·자연·시스템·증거 기록 | 23게시물·60장 | [보고서](topics/16-nonportrait-domain-coverage.md) |

모든 보고서는 프롬프트 924개를 전수 스캔했다. 이미지 수는 주제별 목적 표본이며 코퍼스 4,908장의 빈도나 성공률이 아니다.

## 증거 경계

- 코퍼스 프롬프트 관찰과 코퍼스 픽셀 관찰은 분리했다.
- 현재 authored source 비교와 generated index를 분리했다.
- generated index는 파생물이며 직접 의미 소유자로 사용하지 않았다.
- 코퍼스 픽셀은 새 제안의 독립 렌더 자격 증거가 아니다.
- 새 candidate pack, composed prompt, runtime request, 독립 렌더, 사용자 판단은 수행하지 않았다.
- 필요한 영역이 보이지 않으면 `UNSCORED`, 보이는 strict 구성 일부만 충족하면 `partial_is_fail`이다.

## 현재 승격 상태

| 층 | 상태 |
|---|---|
| 구조 연구 | `proposed` |
| 대상 스킬 구현 | 미구현 |
| package 검증 | `not-run` |
| prompt 동작 검증 | `not-run` |
| 신규 렌더 검증 | `UNSCORED` |
| 사용자 판단 | `UNSCORED` |

## 산출물 검증

- topic report 16개 존재, 전부 924개 프롬프트 스캔과 `proposed` 경계 포함
- 주제별 최소 표본: 12개 게시물·24장
- 보고서에서 이름을 명시한 고유 코퍼스 이미지 파일 426개: 모두 로컬 존재 확인
- manifest, gallery, translations 해시: 동결값과 일치
- authored source 4개 해시: snapshot commit `401f450e4c0ec32ef79c502e3c6a6666c9a106c4`에서 동결값과 일치
- `candidate-backlog.json`, `iteration-record.json`: JSON parse 통과
- iteration record validator: `status=ok`, 오류 0개
- 로컬 Markdown 링크, code fence, trailing-whitespace 검사 통과
