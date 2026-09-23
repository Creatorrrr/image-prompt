# 실사 요소 운영 반영과 3개 이미지 실험

## 반영 범위

- 연구안 21개 중 관찰 가능한 관계 12개를 새 시각 의무 프로필로 구현했다. 원근·초점·피부·반사 4개는 기존 프로필을 재사용했다.
- 디지털 노이즈·JPEG 압축·필름/인화 입상감은 선택형 후보로 유지했다. 다큐멘터리 진정성 및 보편적인 결함 수량 규칙은 픽셀 프로필로 만들지 않았다.
- 총 19개 슬롯 후보와 3개 장면 묶음을 운영 연구 확장에 추가했다. 운영 후보는 모두 선택 사항이며 잠긴 의도를 변경할 수 없다. 연구의 14개 예시 묶음 전체를 자동 활성화한 것은 아니다.
- `photo_prompt_visual_profile_index.json`과 `photo_prompt_semantic_index.json`을 새 소스 해시로 재생성했다. 각각 631개 프로필, 8,609개 의미 문서가 현재 인덱스에 있다.
- [구현 대응표](implementation-coverage.json), [운영 확장](../../../../skills/photo-prompt-image-generator/assets/photo_prompt_photorealism_elements_extension.json), [시각 프로필](../../../../skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_photorealism_elements.json), [동결한 세 실험](qualification/test_cases.json)을 참조한다.

## 구조 검증

사전 메타데이터 검증, 시각 인덱스 해시 검증, 새 관계 테스트 4개, 기존 관계·데이터 테스트 31개, v6 작성 코어 테스트 18개, 장면 표현 감사 112개 경로가 통과했다. 새 테스트는 완성 관계의 정확 경로만 하드 의무가 되고, 단편·부정·일반 실사·RAW·documentary 표현은 하드 의무를 만들지 않는지 확인한다. 후보 묶음은 모든 구성원과 열린 차원이 있어야 노출된다. 광범위 시각 의무 테스트 실행은 시간이 길어 중단했으며 완료된 통과로 계산하지 않는다.

## 후보팩 노출과 렌더 판정

세 서브에이전트는 동일한 사용자 원문과 첨부 JPEG를 공유하되 서로 다른 무작위 장면·독립 코어·독립 팩으로 작업했다. 초기 팩의 일부 목표 관계가 전역 검색 상한에서 누락되어, 이미지 생성 전에 짧은 범용 관찰 단서를 추가하고 인덱스를 다시 만들었다. 동결 코어는 유지했다. 이 조정은 첫 세 팩의 결과를 보고 이루어졌으므로 세 장면은 독립적인 미사용 사례 검증이 아니다.

재생성한 팩에서 목표 시각 개념의 노출은 A 1/3, B 0/4, C 2/3이었다. 나머지 관계는 소스와 인덱스에 있어도 해당 복합 장면의 공개 후보팩에 나타나지 않았다. 세 장면 묶음은 구성원의 `affected_dimensions` 중 잠긴 차원이 있어 제외됐다. 이 정책 결과를 우회하지 않았다. 팩 노출과 실제 이미지의 관계 재현은 별도 판정한다.

## 저장 이미지와 엄격 판정

동결한 세 코어로 첨부 JPEG를 실제 reference input에 넣어 각 1회씩 native 이미지 생성을 수행했다. 세 결과 파일의 SHA-256은 각 arm의 manifest와 독립적으로 재대조했고 모두 일치했다. 프롬프트 구성 감사와 정확한 이미지 요청 감사는 3/3 통과했다. 이는 픽셀 통과와 다르다.

| 실험 | 복합 장면 | 공개 팩의 목표 프로필 | 실제 픽셀: 목표 프로필 | 전체 |
|---|---|---:|---:|---|
| [A](qualification/arm_a/arm_result.json) | 식물 표본 작업실에서 종이 폴리오를 황동 자에 맞춤 | 1/3 | 1/3 | FAIL |
| [B](qualification/arm_b/qualification_result.json) | 비 그친 보행교에서 투명 우산과 경로 카드를 듦 | 0/4 | 3/4 | FAIL |
| [C](qualification/arm_c/result_summary.json) | 씨앗 교환실의 캠코더 프레임에서 그릇을 내려놓음 | 2/3 | 0/3 | FAIL |

- A: 작업장과 인물의 연결은 보인다. 앞치마의 여밈 구조와 자의 광원 일치 그림자는 확인되지 않았고, 요청한 손·종이 이동 동작도 맞지 않는다. [이미지](/Users/chasoik/Projects/image-prompt/generated_images/photorealism-arm-a-20260923/render.png), [에이전트 픽셀 판정](qualification/arm_a/external_target_pixel_review.json).
- B: 머리카락 움직임, 주변부 크롭, 원근 대비는 확인된다. 젖은 바닥 반사의 소유자 정렬·가림에 따른 끊김·wet/dry 경계는 모두 확인되지 않는다. 발과 지지면도 하단 크롭 밖이다. [이미지](qualification/arm_b/generated_images/bridge-rain-observation-20260923/render_01.png), [픽셀 판정](qualification/arm_b/target_pixel_review.json).
- C: 캠코더 표시와 손·그릇 접촉은 보이지만 국소 움직임 흔적, 비디오 프레임의 일관된 질감, 작은 행동 결과가 부족하다. 창밖의 디테일 손실 범위도 지나치게 넓다. [이미지](qualification/arm_c/generated_images/seed-swap-camcorder-20260923T035043Z/native_render.png), [픽셀 판정](qualification/arm_c/external_target_review.json).

목표 관계 단위는 4/10 통과했지만, 한 장면이라도 필요한 관계 전체와 핵심 행동까지 통과한 경우는 **0/3**이다. [엄격 종합 판정](qualification/adjudication.json)에는 A의 예비 재확인과 에이전트의 소유자별 판정이 달랐던 항목을 보수적으로 실패 처리한 경위도 남겼다. 원본 크기에서 모든 구성요소가 같은 최종 이미지에 있어야 하며, 부분 충족은 실패다.

## 해석 한계

이번 세 장면은 첫 팩 노출 실패를 본 뒤 범용 검색 단서를 보강해 같은 동결 코어로 다시 평가했다. 독립적인 미사용 사례의 성능 개선이나 키워드 인과 효과로 읽을 수 없다. A 에이전트는 코어 동결 전에 일반 메모리 레지스트리를 조회했다고 자진 기록했으므로, 절차상 완전한 pre-core 격리도 주장하지 않는다. 서로 다른 arm의 팩·프롬프트·이미지는 공유하지 않았고 각 manifest에 그 경계를 기록했다. B는 최초 코어의 assertion 차원을 스키마에 맞추는 기계적 수정 시점을 별도 기록했다.

참고 인물 사진은 보이는 성인 외형의 연속성 판단에만 썼다. 신원·생체정보·보호 특성을 추론하지 않았으며, 사용자 선호는 직접 받기 전까지 pending이다. 이번 결과의 핵심 후속 과제는 복합 장면에서 국소 관계가 공개 팩 검색 상한에 묻히는 현상과, 프롬프트 감사 통과 뒤에도 행동·반사·노출의 모든 픽셀 성분이 재현되지 않는 현상을 별도로 개선하고 새 장면으로 다시 확인하는 것이다.
