# 사진 의미·후보 데이터 개선 및 독립 생성 평가

시각 의미 프로필 26개를 교정하고, 102개 의미 묶음이 실제 선택 가능한 후보팩 계약으로 전달되도록 구현했다. 기존 프로필 ID 354개와 후보 7,400개의 참조는 유지했다. 아래 데이터·코드 검증과 이미지 관찰은 서로 다른 증거다.

## 적용 내용

| 구분 | 실제 적용 | 확인 범위 |
|---|---|---|
| D1 활성화 | 전문 역할 10개, 겨드랑이 강조, contained-affect의 hard 의무는 실제 요청의 행위·강조 근거가 있어야 활성화 | 직업·복장·휴식·제품 언급은 관련 선택 후보로 남고, 명시된 업무와 강조는 필수 관계 유지 |
| D2 의미 교정 | Rembrandt의 near/far 고정을 key/shadow-side로 변경. 망원 화각은 narrow로 교정. 연결 후보의 설명·검색 키워드도 정렬 | short/broad 방향과의 정의 충돌 제거; 새 렌더로 해당 조명 조합을 실증했다는 뜻은 아님 |
| D3 개념과 예시 | yandere의 같은 대상에 대한 애정·통제·행위·결과를 유지하며 간호사·주사기·성별·고정 표정 예문을 일반화. menhera는 프로젝트의 제한된 시각 해석임을 명시 | 원래 얀데레 간호사 요청에 의료 처치가 자동 추가되지 않음; 관계 증거 누락은 계속 실패 |
| D4 의미 묶음 | 102개 원자료를 candidate_bundles로 컴파일하고 참조·원자료 해시를 검증. 설명용 정책 10개는 외부 유지보수 기록으로 이동 | 실제 rule 생성→v6 팩→상세 뷰→전체 composed 감사 통과. 잘못된 참조·미지 실행 키·필수 확장 누락·위조된 채택 조건 거부 |
| D5 공개 후보 | 짧은 concept_units와 방향이 있는 relations를 보존. 선택한 모든 구성요소·관계에 literal evidence 요구 | 관리 태그 노출 484개→0개. 묶음 내부 멤버는 단독 선택권이 아니며 연결 프로필도 자동 필수화되지 않음 |
| D6 검색 | 긍정 의미와 주장 한계를 분리. lexical/vector 검색이 같은 허용 필드를 소비하고 관리용 ID·대조·주장 한계는 긍정 문서에서 제외 | 23개 프로필에 claim_limits 분리. health/fertility나 nonsexual 제한 문구에 의한 기존 상위 검색 오염 해소. 의미 자체인 부정 표현은 유지 |
| D7 증거 원천 | Rembrandt·clamshell·split-diopter 3개를 authored component에서 그룹·증거·작성 지시·게이트가 생성되도록 이관 | 눈 감김 조건과 직접 catchlight 요청 및 부정 조건을 구분. split-diopter는 촬영 이력을 증명한다고 하지 않고 가시적 연속성만 판정 |
| D8 정리 | street 계열은 안정 ID와 대표 개념 연결을 유지. 편의점 외부와 일반 장소의 라벨을 구별. profile ID+수정 해시로 외부 검토 이력 연결 | 288개 category 전면 재분류나 대규모 삭제는 하지 않음 |

일반 명칭의 업무 강제를 막은 전문 역할은 pilot, cabin crew, nurse, police, firefighter, EMT, coast guard, rail driver, platform dispatcher, private security다. 직업만으로 좁은 행동을 확정하던 같은 원인을 일반 활성화 계약으로 처리했다.

추가로 스킬 진입 문서에 빠져 있던 typed assertion의 중립 JSON 형식을 보완했다. 독립 작성 에이전트 5개 모두가 이 누락을 지적했고, 의미나 사례를 공급하지 않는 같은 스키마를 읽은 뒤 기본 프롬프트를 고정했다.

## 계약과 범위

새 공개 의미 표면은 `photo-candidate-semantic-surface/v1`, 선택 묶음은 `photo-candidate-bundles/v1`이다. 기존 v4/v5 및 새 표면이 없는 저장된 v6 팩은 기존 읽기 경로를 유지한다. 새 표면의 선택 묶음은 현재 공개 후보와의 관련성, 명시적으로 열린 차원, 요청 제외, 개별·상호 자격과 충돌을 검증한다. 조건이 묶음 내부에서 함께 성립해야 하는 경우도 같은 소스 사본의 감사자가 다시 계산한다. 원래 비공개 샘플러 선택을 공개하거나 `eligible` 자기 선언만 믿지 않는다.

검색 텍스트는 `semantic-text-v5`, 시각 프로필은 `photo-visual-profile-text/v2`로 변경했다. 8,142개 일반 의미 항목과 354개 프로필의 인덱스를 생성기로 갱신했다. 변경된 텍스트만 batch size 1로 임베딩하며, 동일 벡터 공간의 완전히 같은 텍스트만 캐시 재사용했다. 파생 인덱스를 직접 편집하지 않았다.

D7은 세 프로필에서 검증한 단계적 이관이다. singleton literal 규칙은 990개에서 975개로 줄었으며 나머지를 자동 삭제하거나 검사를 완화하지 않았다. category 전체 재설계, graph/profile의 전면 참조형 통합, 모든 산문 정의의 수동 재검토는 이번 완료 범위에 포함하지 않는다.

## 독립 실행 설계

과거 시도한 요청 중 큐피드, 금·은도끼 산신령, 츤데레 메이드, 얀데레 간호사, 항공기 화장실 승무원 5개를 새 결과를 보기 전에 선정했다. 원래 요청 전체와 정확한 active spans를 그대로 복사하고 얼굴 참고 2개도 원본 해시를 보존했다. 과거 프롬프트·팩·렌더·평가 결과는 새 작성자에게 전달하지 않았다.

각 에이전트는 원문과 허용된 얼굴 외모 참고만으로 기본문구를 먼저 작성했다. 단어 수는 199 / 229 / 319 / 301 / 187이고 모두 코어 검사를 통과했다. 그 후 같은 소스 사본을 각 환경에 배포했다. 에이전트 문맥·소스·입력·캐시 디렉터리·출력·장부를 분리했고, 호스트 OS·Python 라이브러리·자격 증명 공급원·이미지 서비스는 공유했다. OS 보안 샌드박스 격리라고 주장하지 않는다.

- 변경 전 Git: `0330d8118398d9dabc6c11ba39fdb54a8d2e6235`
- 생성에 사용한 스킬 사본 SHA-256: `c0eeb2bf23fc913b79a4161361d9da305c89cd4ce4a277dae77d06f5d6a727c6`
- 사후 CLI 진단 보완을 포함한 최종 소스 SHA-256: `3381c4ecd3b45200ba3e294fd1d1c4a03468556ba1d31fc929461ef74861831e`
- 각 arm: creativity 0.5, seed 6101–6105, candidate pack 1개, native image tool 1회, 재시도·CLI 우회 0회
- 기본문구와 user intent는 동결하며, 후보가 고정 의미를 대신 정하지 않음
- 별도 평가자는 원문과 참고만으로 기준을 먼저 고정하고, 최종 프롬프트나 자기평가를 읽기 전에 전달 픽셀을 관찰함

## 검증 결과

사전 고정한 원문 기준 독립 픽셀 관찰은 산신령·츤데레 PASS, 얀데레 FAIL(partial)이다. 최종 프롬프트·실행 입력 감사는 5개 모두 PASS이며, 실제 이미지 호출 5회에서 3개 이미지가 전달되었다. 큐피드와 승무원은 출력 단계 `moderation_blocked`로 픽셀 미채점이다. 두 차단을 픽셀 실패나 품질 0점으로 계산하지 않는다.

독립 평가자의 세부 계약 대조는 전달된 3개 모두 FAIL이다. 츤데레의 실제 gate는 4/9 PASS, 얀데레는 4/15 PASS이며, 산신령은 일반 의미 조건을 별도 표로 대조했다. 작성자의 자기평가도 세 사례의 세부 조건 미충족을 기록했지만 얀데레 gate 수는 8/15 PASS로 달랐다. 양쪽 원본을 보존했다. 원문이 요구한 핵심을 알아볼 수 있는지와, 작성자가 추가로 고정한 모든 손·시선·반응·결과를 재현했는지는 서로 다른 질문이다.

| 검증 | 결과와 근거 |
|---|---|
| 데이터 교정 집중 검사 | 30개 PASS. 직업 이름/복장과 명시 행위를 구분하고 잘못된 조명·주장 한계·증거 조건을 검증 |
| 후보 계약 집중 검사 | 39개 PASS. 생성된 후보팩의 실제 묶음 선택부터 전체 composed 감사까지 별도 재통과 |
| 새 테스트 | 전체 suite에 새로 추가된 39개 메서드 PASS; 위 집중 검사와 겹치므로 합산하지 않음 |
| 사전 코어 및 실제 호출 결속 | 5개 환경 각각 29개 검사 PASS. 소스 80개, 원문·참고·코어·프롬프트·실행 입력·이미지·원장 해시 확인 |
| 사전·인덱스 | dictionary 검증, 354개/1,758개 시각 프로필·별칭, 8,142개 일반 의미 항목 PASS |
| 현재 장면 계약 | `audit_scene_expression.py --current` 112/112 PASS |
| 외부 검토 기록 | 프로필 26개 및 확장 기록 10개의 실제 내용 해시 일치 |
| 변경 전 전체 검사 | 1,048개 실행, 실패 레코드 41개·오류 4개. 변경 전부터 존재하는 실패를 보존 |
| 변경 후 전체 검사 | 최초 1,087개 실행, 실패 레코드 40개·오류 4개. 아래 사후 재검사와 구분해 보존하며 전체 PASS 아님 |
| 사용자 판단 | 미수집 |

신체 추론 제한 문구의 `definition → claim_limits` 이동과 yandere reject-code 일반화를 기대값에 반영하지 못한 테스트 두 곳은 최소 교정 후 각각 재검사 PASS다. 자세·가시적 관계·거부 경계 검증은 그대로 유지했다. 이전 오류·실패 로그와 원래 holdout/golden 데이터도 유지했다.

공개 `visual_obligation_routing_v1.jsonl`의 menhera 양성 사례 하나는 구현 단계에서 이름만 있는 advisory 사례와 제한된 시각 해석을 명시한 hard 양성 사례로 나누었다(119→120행). 이 공개 fixture의 이관과 고정 holdout 불변은 구분한다. 아래 비교 대상 yandere 5행의 입력·기대값은 변경 전후 그대로다.

추가로 잘못된 확장 메타데이터를 거부할 때 traceback을 출력하던 CLI 진단 회귀를 교정했다. 기존 진단문 회귀, 미지 확장 키의 구체 진단과 비정상 종료, 정상 데이터의 전체 검증을 재통과했다. 전체 검사 시작 뒤 전문 역할 테스트의 이름이 변경되어 생긴 discovery 오류 1건도 원본에 남기고, 최종 이름의 메서드를 별도로 실행해 PASS를 확인했다. 최종 테스트 집합은 1,087개이며 초기 목록과 이름 1쌍만 다르다.

**고정 라우팅 사례 5건은 새 후보 목록 불일치가 남아 있다.** 같은 입력을 양쪽 코드에서 직접 진단한 결과, 변경 전에는 잘못된 업무 hard 의무 때문에 실패했고 선택 후보 목록은 기대와 일치했다. 변경 후에는 hard 의무가 기대대로 정리됐지만 `clinical_nursing_duty_system`이 관련 선택 후보로 남아 이전의 정확한 후보 목록과 달라졌다. 이는 D1/D3의 broad profession advisory 정책에 따른 행동 변화이며, 기존 오류와 같은 원인이라고 집계하거나 새 회귀가 0건이라고 하지 않는다. 원래 fixture/holdout의 PASS를 얻도록 기대값을 소급 바꾸지 않았다.

전체 검사 숫자의 감소를 개선율로 사용하지 않는다. 변경 전 별도 사본에는 과거 참조 파일이 없어 실패했지만 현재 작업 경로에서는 통과한 환경 차이도 있다. 원인별 최종 분류와 미해소 항목은 [회귀 비교](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-09-06-photo-data-implementation/regression-comparison.json)에 남겼다.

최초 후보 검사 44개 실패·오류 레코드의 최종 분류는 같은 원인의 기존 실패 35건, 새 advisory 후보 목록 불일치 5건, 교정 후 별도 재검사로 통과한 기대값 2건·CLI 진단 1건·이름 변경 실행 오류 1건이다. 고유 실패 메서드는 최초 baseline 28개, 후보 29개였다. 최종 메서드 집합 1,087개에서 실행하지 않은 항목은 없지만, 남은 실패가 있어 전체 suite를 통과로 표시하지 않는다.

이 실행들은 과거 요청의 회귀 재현이며 새로운 독립 holdout이나 수정 전후 이미지 A/B 실험이 아니다. 범위 내 데이터·계약 교정은 적용했지만, 전반적인 이미지 품질 개선이나 모든 입력의 성공을 입증한 것으로 승격하지 않는다.

## 이번 평가에서 남은 문제

1. **인간 캐릭터의 동물 품질 오분류.** `cat-eared` 같은 의상·특징 토큰이 실제 동물 subject 라우팅에 영향을 주어 츤데레 팩에 털·동물 해부학 네거티브가 섞였다. 긍정 의미와 주장 한계 분리와는 별도의 subject 소유권 문제다. 우산 동작의 미재현 원인이라고 단정할 근거는 없다. [실제 전파 경로와 후속 교정·회귀 범위](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-09-06-photo-data-implementation/animal-quality-routing-followup.md)를 작성했다.
2. **일반 의미의 픽셀 게이트 공백.** 산신령의 일반 `semantic_assertions`는 프롬프트 감사가 가능하지만 character/visual-profile 계약처럼 자동 렌더 게이트가 생성되지 않았다. 작성자는 모든 동결 의미를 수동 검토했고, 자동 리뷰의 계약 부재 오류도 보존했다. 이를 자동 픽셀 감사 PASS로 처리하지 않았다.
3. **원문 필수 의미와 작성자 세부 선택의 평가 구분.** 눈물의 특정 눈, 가방이 떨어지는 순간처럼 작성자가 추가한 설정까지 엄격 조건에 들어간다. 후속 개선은 출처별 요구 수준과 가시적 판정 가능성을 유지하면서 조건을 구분해야 한다. 이미 실패한 실험의 기준을 소급 완화해서는 안 된다.
4. **관계의 가림과 순간 동작.** 손·손잡이의 연결, 우산이 보호하는 범위, 상대의 반응은 최종 이미지에서 명확하지 않을 수 있다. 새 코어를 작성하는 후속 실험에서 핵심 관계의 가시성과 부차 조건 수를 조정하고 검증할 필요가 있다.
5. **보조 검색 진단의 불일치.** 츤데레 코어에는 작성된 축과 `same_target`·`temporal_order` 관계가 있으나, 보조 검색의 `semantic_consistency`는 누락으로 표시했다. 실제 필수 typed 계약은 유지됐으며 원인은 아직 확인하지 않았다. 관련 없는 겨드랑이 강조·kuudere 후보도 작성자가 거절했다. 이 관측을 [실험 기록](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/environments/arm-03-tsundere/outputs/evaluation.json)에 보존했다.

생성에 사용한 소스 사본·팩·코어·이미지·원장은 계속 보존한다. 전체 회귀 검사에서 발견한 CLI 진단 오류는 생성 후 root의 `validate_photo_prompt_dictionary.py`만 보완하고 별도 소스 해시로 기록했다. 생성기·데이터·감사기를 포함한 나머지 79개 파일은 생성 당시와 같다. 이 진단 보완을 포함한 최종 tree에서 이미지를 다시 생성했다고 주장하지 않는다. 잔여 시각 의미 문제는 후속 변경으로 추적하며 이번 결과를 다시 채점하거나 추가 생성으로 교체하지 않는다.

## 재현 및 근거

- [초기 개선안](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-09-06-photo-data-improvement-proposal.md)
- [데이터 재현 결과](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-09-06-photo-data-implementation/data-replay.json)
- [실제 후보 묶음·전체 감사](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-09-06-photo-data-implementation/candidate-contracts/composed-audit.json)
- [시각 의미 교정 집중 검사](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/validation/data-corrections-summary.json)
- [최종 구조 검사](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/validation/final-structural-checks.json)
- [회귀 비교](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-09-06-photo-data-implementation/regression-comparison.json)
- [개선 반복 기록](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-09-06-photo-data-implementation/iteration-record.json)
- [독립 실행 설계와 원문 해시](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/evaluation-manifest.json)
- [스킬 소스 사본 명세](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/candidate-source/source-manifest.json)
- [최종 소스 명세와 사후 변경 범위](/Users/chasoik/Projects/image-prompt/generated_images/photo-data-five-case-20260906/final-source-manifest.json)
- [생성 이미지·프롬프트·평가](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-09-06-photo-data-five-case-results.md)

Rembrandt/short/broad 및 초점거리 교정의 근거는 [Westcott의 조명 패턴 설명](https://westcottu.com/4-essential-portrait-lighting-patterns)과 [Nikon의 초점거리 설명](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/understanding-focal-length)이다. 출처·유지보수 설명은 런타임 후보와 분리했다.
