# 러브코미디 개선 및 독립 재생성 결과

같은 참조 이미지로 독립 서브에이전트 3개가 각 1장씩 재생성했고, 루트도 저장 원본과 접점 crop을 직접 검토했다. **전체 엄격 시나리오 통과는 0/3**, 최종 활용된 일반 지침의 명확한 시각 구현은 **1/3(A)**이다. 신규 자료의 실제 프롬프트 활용은 생겼으나, 완전한 픽셀 충족은 입증되지 않았다.

세 관리 리뷰의 기록 유효성은 모두 PASS다. 관리 generic 수리 게이트는 A/C PASS·B FAIL, embodiment 신체·투영 게이트는 A PASS·B/C FAIL이다. 이 검토 범위들과 위의 전체 시나리오·신규 지침 판정은 서로 다르다. 최종 집계는 [FINAL-SUMMARY.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/romcom-20261024/round2-20261024/FINAL-SUMMARY.json)에 있다.

## 원인과 반영 내역

첫 시험의 문제는 인덱스 등록 누락이 아니었다. 실제 질의의 순위·샘플 노출 손실, 노출된 자료와 선택 장면의 완전한 의미 불일치, 창작 참고자료와 네이티브 후보 승인의 차이가 겹쳤다. 첫 시험의 세 최종 프롬프트는 각 독립 baseline과 같았고, 새 자료의 최종 활용도 0개였다.

스킬에 경쟁 해석, 결정적 접점, 실제 조작부와 모든 지지 끝점의 가시성 검토를 추가했다. 기존 자료 50개에 실제 장르 조회 문구를 보강하고 일반 구도 참고자료 6개를 더했다. 결과는 **124개 레코드(긍정 105·진단 제외 19), 연결 203개**다. 기존 118개 명제·조건·효과·출처와 317개 라우트를 보존했다. 별도의 네이티브 승인을 부여하거나 채택 할당량을 만들지 않았다.

상세한 원인·변경·검색 비교·실행 복구는 [분석 문서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/romcom-20261024/round2-20261024/CAUSE-AND-CHANGES.md)에 있다.

반영 위치: [스킬의 장면·접점 검토](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/SKILL.md:425), [시각 의미 자료](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_romcom_semantics_20261024.json), [후보 자료](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_romcom_20261024.json), [후보 연결](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_romcom_bindings_20261024.json), [실행·복구 지침](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/photo-workflow.md).

## 노출, 실제 활용, 픽셀을 구분한 결과

| 시험 | 반환된 러브코미디 자료: 고유/출현 | 최종 활용한 신규 일반 지침 | 해당 지침의 픽셀 구현 | 전체 엄격 판정 |
|---|---:|---|---|---|
| A 꽃꽂이 경합 | 9 / 11 | P05 1개: 접점과 두 얼굴의 동시 판독 | PASS | FAIL |
| B 겨울 축제 스케이트 | 6 / 7 | P06 1개: 태연함과 어긋난 자세·상대 반응의 대비 | 부분·FAIL | FAIL |
| C 비 온 뒤 카페 파라솔 | 7 / 8 | P02·P06 2개 출처: 하나의 겹치는 표정 수정 | 부분·FAIL | FAIL |

이 표의 활용은 `inspiration_only`로 최종 프롬프트에 남은 구체적인 기여다. **세 시험 모두 네이티브 `chosen_candidate_ids`는 0개**다. 원래의 특수 구성이나 신규 일반 자료가 네이티브로 승인됐다는 의미가 아니다. C의 두 출처는 두 개의 독립된 효과로 세지 않는다. B의 지지점·여백은 새 독립 baseline에 이미 있어 P03의 새 활용 실적으로 세지 않았다.

세 최종 프롬프트 모두 이번 독립 baseline과 달라졌고, 실제 도구에 그 최종 문자열이 전달됐다. 이전 실제 질의·임베딩·시드를 그대로 유지한 오프라인 개발 비교에서는 신규 자료의 순위 창 출현이 9→109회, 샘플 출현이 2→32회였다. 실제 재시험은 새 장면 질의이므로 이 두 종류의 수치를 같은 실험처럼 합치지 않았다. 새로운 질의에 대한 일반 검색 성능이나 데이터만의 이미지 개선 효과는 증명하지 않았다.

## A: 접점과 두 얼굴은 읽히지만 희소성은 재실패

![A 꽃꽂이 경합](/Users/chasoik/Projects/image-prompt/generated/photo-runs/romcom-20261024-r2-a/compatible-run/image.png)

두 사람이 별도 손으로 하나의 연속된 꽃줄기를 잡고, 두 얼굴과 접점을 함께 읽을 수 있다. P05의 일반 가시성 지침은 구현됐다. 그러나 왼쪽 배경에 다른 흰 꽃이 생겨 마지막 한 송이라는 수량 제한이 성립하지 않았다. 작성자의 더 세부적인 테스트에서는 여성의 작은 웃음 누출도 불명확했다. 풍성한 초록 잎만으로 대체 꽃이라고 단정하지 않았으며, 명백한 배경 꽃을 실패 근거로 삼았다.

관리 기술 게이트는 PASS지만 그 범위는 일반 held-flower 관계와 신체 검토다. 전체 희소성·표정 시나리오의 PASS가 아니다.

[실제 전달 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/romcom-20261024-r2-a/runtime-prompt-exact.txt) · [에이전트 결과](/Users/chasoik/Projects/image-prompt/generated/photo-runs/romcom-20261024-r2-a/result-summary.json) · [루트 픽셀 검토](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/romcom-20261024/round2-20261024/root-pixel-review-a.json)

## B: 오른쪽 잘림은 해결, 왼쪽 날은 여전히 관찰 부족

![B 겨울 축제 스케이트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/romcom-20261024-r2-b/compatible-run/result.png)

네 부츠와 오른쪽 끝 스케이트는 프레임 안에 있고 바깥쪽 얼음 여백도 생겼다. 중앙의 연결된 손과 양쪽 난간 지지도 읽힌다. 그러나 왼쪽 흰 스케이트가 앞끝 방향으로 강하게 기울어 긴 날과 날-얼음 접촉을 전체로 추적할 수 없다. 잘림을 고친 것과 모든 날·접촉을 보인 것은 다른 결과다. 보이지 않는 날의 형태가 잘못됐다고 진단하지 않고, 필요한 관찰이 부분적이라고 판정했다.

P06 판정에는 해석 차이가 있었다. 루트의 최초 판독은 안정된 상체와 벌어진 무릎의 대비를 통과로 봤지만, 독립 작성자는 일반적인 다정한 스케이팅 사진이라는 경쟁 해석과 태연한 표정의 약함을 지적했다. 최종 판정은 충분히 뚜렷한 대비가 아니라는 **부분·FAIL**이다. 이미지나 기준은 바꾸지 않았고 [최초 루트 판독](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/romcom-20261024/round2-20261024/root-pixel-review-b.initial-root-reading.json)을 보존했다. 서로 다른 미소만으로 특정 코믹 대비가 성립했다고 올려 세지 않았다.

[실제 전달 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/romcom-20261024-r2-b/runtime-prompt-exact.txt) · [에이전트 결과](/Users/chasoik/Projects/image-prompt/generated/photo-runs/romcom-20261024-r2-b/compatible-run/result-summary.json) · [루트 픽셀 검토](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/romcom-20261024/round2-20261024/root-pixel-review-b.json)

## C: 크랭크는 해결, 물의 끝점과 표정 대비는 미달

![C 카페 파라솔](/Users/chasoik/Projects/image-prompt/generated/photo-runs/romcom-20261024-r2-c/result.png)

오른손이 검은 외측 크랭크 손잡이를 잡고, 노출된 금속 팔·기어박스·기둥 연결이 함께 보인다. 이전에 실패한 핵심 조작부 접촉은 PASS다. 물방울과 젖은 어깨·냅킨도 있지만, 원본 crop에서 물이 셔츠에 닿는 마지막 지점은 명확하지 않다. 그럴듯한 경로와 젖은 자국으로 접점을 추론해 통과시키지 않았다. 남성의 보조 손은 냅킨 가장자리보다 여성 손목 쪽으로 보이는 추가 편차도 있다.

표정은 서로 다른 정도의 부드러운 미소로 읽혀, 태연한 피해자와 웃음을 참는 상대라는 강한 대비가 충분하지 않았다. P02·P06은 하나의 겹치는 수정이며 최종 픽셀 판정은 부분·FAIL이다. 루트도 전체 프레임의 최초 판독 후 native 물 경로 crop에서 끝점 부족을 확인했고 [그 최초 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/romcom-20261024/round2-20261024/root-pixel-review-c.initial-full-frame.json)을 보존했다.

[실제 전달 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/romcom-20261024-r2-c/runtime-prompt-exact.txt) · [에이전트 결과](/Users/chasoik/Projects/image-prompt/generated/photo-runs/romcom-20261024-r2-c/result-summary.json) · [루트 픽셀 검토](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/romcom-20261024/round2-20261024/root-pixel-review-c.json)

## 실행과 반영 증거

참조 파일은 원래 JPEG 그대로이며 SHA256은 `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`다. 각 실제 도구 payload에 이 파일의 경로가 들어갔다. 참조의 역할은 얼굴·머리 외형 가이드이며 실제 정체성·나이를 판정하지 않았다.

이번 실제 native imagegen 호출은 **3회: A/B/C 각 1회**다. 각 arm의 부모 1회를 포함한 ledger 누적 호출은 2회다. 추가 재생성이나 API 대체 경로를 사용하지 않았다. 실제 모델명은 native 도구가 노출하지 않아 미확인이다. 실제 인자와 감사된 plan, 반환 원본 PNG와 복사본 SHA, 고정 입력과 최종 runtime 문자열을 [파일·계보 대조 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/romcom-20261024/round2-20261024/arm-artifact-verification.json)에 기록한다. 저장된 메타데이터의 대조이며 별도 서버 측 호출 증명이나 픽셀 통과 증명이 아니다.

시각 의미 테스트 7개, 재시도 범위 재결합 테스트 16개, 역할 교정 경계 테스트 6개를 통과했다. 전체 소스·벡터·실행 폐쇄 검증도 통과했다. B의 역할 교정은 기존 요청과 실패 기록을 보존하고 고정·검색·구성 입력 해시를 모두 유지한 채 같은 계보·구성·실행 감사를 거친 원자적 revision이다. [복구 증거](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/romcom-20261024/round2-20261024/b-prospective-role-recovery.json)가 있으며 이 과정은 이미지 호출을 하지 않았다.

세 시험의 고정 실행본은 H-F2 `22aa903c…ffe46fb`, native `278453eb…b7c19`다. 시각 작성에 사용한 스킬 스냅샷은 [SKILL-used.md](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/romcom-20261024/round2-20261024/SKILL-used.md), SHA256 `83b3239eda5b5e26b1c51dad268258eb21a24f3dbca3b814517eb89169390cb8`다. `SKILL.md`는 네이티브 매니페스트 구성원이 아니므로 별도로 바인딩했다. 실행 중 관찰된 역할 교정 문제는 실행 문서에 추가 반영했다.

개선 자료는 공용 로컬 기본 실행본 `87bb0530…6c621d`로 반영했으며 동시 작업의 자료를 보존했다. 그 반영본과 시험본의 이번 124개 자료·203개 연결·실행 코드가 같음을 [검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/romcom-20261024/round2-20261024/publication-retention-verification.json)했다. 이후 다른 작업에서 스킬·기본 실행본을 갱신한 상태는 [최종 선택본 보존 확인](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/romcom-20261024/round2-20261024/selected-default-retention-verification.json)에 별도 기록한다. 후속 동시 변경을 덮어쓰거나 이번 고정 실험의 일부로 섞지 않았다.

2026-10-24 09:25:59 KST 확인 시 공용 선택은 `eeaa196d…510471`, 현재 스킬 SHA는 `e26f7fbe…b49cf9`로 후속 갱신돼 있었다. 이번 후보·연결 파일과 연구 의미 자료는 그대로이고 새 스킬 지침 두 문단도 보존됐다. 후속 실행 코드는 시험본과 달라졌으므로 현재 선택본 전체의 이미지 검증으로 확대하지 않는다. 재시험은 이번 수정 후 의미를 고정할 당시의 최신 스킬 스냅샷과 고정 실행본으로 수행했다.

## 남은 개선 계획과 해석 한계

다음 시각 개선의 검증 목표는 A의 배경까지 포함한 대체 자원 배제, B의 각 스케이트를 긴 날이 판독되는 방향으로 배치하는 것, C의 물-직물 접촉부에서 식별 가능한 종착점을 확보하는 것이다. P02/P06은 양쪽을 일반 미소로 만드는 경쟁 해석을 이길 정도의 입·눈썹·자세 대비를 전체 장면에서 검증해야 한다. 이 계획의 효과는 이번 세 이미지에서 입증되지 않았다.

원래 특수한 자료를 네이티브 후보로 선택하려면 명제별 사실·소유자·역할·완전한 계약 증명의 별도 검증이 필요하다. 검색 노출이나 이번 일반 지침의 시각 구현을 그 승인으로 바꾸지 않았다.

세 장의 정성 검토이며 스킬과 데이터가 함께 바뀌었다. 데이터만의 인과 효과, 통계적 일반화, 실제 감정·의도·관계 이력·정체성·나이의 증거로 해석할 수 없다. `partial_is_fail`과 `UNOBSERVABLE_NOT_PASS`를 유지했다. 사용자 수용은 직접 피드백 전까지 **pending**이다.
