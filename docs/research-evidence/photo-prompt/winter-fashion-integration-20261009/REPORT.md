# 겨울 패션 시각 의미·후보 반영과 독립 이미지 테스트

원문 304개 용어 행의 연구를 토대로, 소유자가 분명한 가시 변형 **162개 후보·162개 프로필·162개 선택 조합**을 등록했다. 기존 후보 **5개**는 동등한 한·영 표현과 해석 문맥만 추가했다. 원료·필파워·성능·공정·데니어 같은 숨은 명세는 해석 문맥에 남기며 사진에 보이는 형태로 인증하지 않는다.

## 변경 범위

- `skills/photo-prompt-image-generator/assets/photo_prompt_winter_fashion_extension.json`
- `skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_winter_fashion.json`
- source manifest의 신규 2행과 정규 빌더가 만든 의미/BM25F·시각 프로필 인덱스·참조 shard
- `tests/test_photo_winter_fashion_integration.py`
- 이 evidence 폴더의 구현·실험·검증 기록

스킬 절차·precore·생성기·감사 코드·기존 holdout·다른 authored source는 겨울 작업에서 수정하지 않았다. 파일럿은 현재 canonical skill을 읽으며 SHA-256은 `9e9b87e6f0b2c1ec1c36bd8e9d55f90950d53529a0b873722b546924dfc7043b`다. 새 gate는 전체 선택 변형의 같은 착용자·의복·두 끝점·연결 경로를 원본 해상도에서 확인하도록 작성했다. 넓은 겨울 패션 명칭은 변형 전체를 자동 필수화하지 않는다.

## 데이터·인덱스·런타임 검증

최종 집중 검사 **18개 PASS**, 사전 메타데이터 PASS, 실제 시각 프로필 인덱스 체크 PASS다. 런타임은 정규 publisher로 완료했고 generation은 `922451d0548100a2825a0c2578ae3bee4f070f5b045b204c1af47731c9bce438`다. 이 게시 스냅샷에는 겨울 외 동시 작업도 포함된다: 슬롯 114개, 후보 11,462개, 프로필 3,251개. 이번 작업의 새 후보는 정확히 162개이며 기존 `winter_` 접두 후보 3개를 신규 수에 포함하지 않는다.

초기 격리 원본에서 의미 벡터 162개와 프로필 벡터 162개를 새로 만들었다. 이후 현재 primary 원본의 정규 빌더는 텍스트·provider·model·dimensions가 동일한 호환 캐시만 사용하며 문서·통계·해시를 현재 원본에서 다시 산출했다. 외부에 키나 벡터를 공개하지 않는다.

초기 넓은 테스트 실행은 exhaustive 전체 프로필 exact-route 행렬에서 중단해 완료된 검사만 보존했다. 격리 공간의 기존 maintenance evidence 누락은 현 원본 evidence를 복사해 보완했고 해당 검사는 최종 원본에서 통과했다. 전체 suite PASS는 주장하지 않는다. primary 빌더의 중첩 source-update가 거절된 과정도 로그를 보존했고, builder staging store를 분리한 뒤 두 인덱스를 검증하고 정규 `--complete-update` 경로로 본 작업의 미완료 revision을 닫았다.

## 보존 상태

기존 tracked dirty 중 인덱스·manifest 외 **10개**는 바이트와 권한이 모두 동일하다. 초기 tracked/untracked dirty 8,579개 비교 중 8,560개가 동일하고, 다른 계절 연구와 별도 실행 ledger **19개**의 동시 갱신을 관찰했다. 이 경로들은 복원·stage·삭제하지 않았다. 다른 작업의 새로운 원본도 manifest를 현 상태에서 추가 병합하고 현재 전체 인덱스를 재산출해 보존했다. 겨울 작업의 commit·push는 수행하지 않았다.

## 독립 실험 설계

세 에이전트 모두 과거 대화·연구·다른 arm을 전달하지 않은 `fork_turns=none`으로 시작했다. 코디네이터가 byte-exact 요청 envelope를 먼저 봉인했으며, 세 개의 서로 다른 일반 지식 범위에서 각자 random seed·후보군·상황·옷 조합·관찰 목표를 작성했다. saved controls는 sensual 1 / fetish 0 / creativity 1 / surreal 0을 그대로 사용한다. 참조 파일 SHA-256은 `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`이며 얼굴·헤어의 보이는 모습 가이드로 실제 이미지 도구에 전달한다.

모든 core·neutral feature selection·embodiment review는 후보 접근 전에 봉인한다. 각 정상 retrieval pack과 receipt를 유지하며 미노출 선택·자동 hard 승격은 허용하지 않는다. 독립 테스트 목표, 새 후보의 노출/선택, literal prompt, runtime 감사, 저장된 픽셀 결과와 사용자 판단은 각각 구분한다. 첫 시도는 보존하고 가림·부분 구현·해상도 부족은 합격으로 올리지 않는다.

세 pack에는 새 겨울 슬롯 후보가 노출됐지만 직접 winter opt-in visual-concept 항목은 0개다. 따라서 이번 3개 이미지가 새 시각 프로필의 직접 opt-in 경로를 검증했다고 주장하지 않는다. 실제 새 후보 계약과 독립된 겨울 관찰 목표의 이미지 결과를 아래 최종 실험 기록에 별도로 연결한다.

## 실험 결과

첨부 참조를 실제로 전달한 native 이미지 호출은 **3회**, arm별 첫 시도 1회다. 재생성·fallback은 없으며 반환된 원본 PNG를 그대로 저장했다. 세 프롬프트의 compose/runtime 감사와 정규 픽셀 review 기록의 형식 검증은 모두 PASS다. 기록이 유효하다는 사실과 의복 조건이 이미지에 구현됐다는 사실은 구분한다.

B 에이전트의 생성·독립 픽셀 검토·ledger·manifest·정규 감사 저장은 완료됐지만 마지막 보고서 출력과 출력 재시도에서 모델 용량 오류가 발생했다. B의 REPORT/RESULT만 조정자가 저장된 독립 기록에서 내보냈으며 원래 기록이나 이미지·프롬프트는 변경하지 않았다. 최종 산출물의 요청·참조·원본 이미지·pack·감사 기록·신규 후보 ID 바인딩 **81개 검사 PASS**를 별도로 저장했다. 이 81개는 추가 이미지 테스트나 시각 합격 개수가 아니다.

| 독립 컨셉 | 새 후보의 선택 관계 | 원래 봉인한 겨울 목표 | 활성 일반 시각·신체 gate | 전체 복합 조건 |
|---|---:|---:|---:|---|
| A · 눈 덮인 과수원 작업장의 가지 표식 묶기 | 0/1 PASS | 4/6 PASS | 5/8 PASS | FAIL |
| B · 눈보라 뒤 항구에서 묘목 상자를 두고 승선 대기 | 2/2 PASS | 4/6 PASS | 8/8 PASS | FAIL |
| C · 소극장 입구의 포스터 케이스 잠금 마무리 | 3/4 PASS | 3/6 PASS* | 5/5 PASS | FAIL |

새 후보에서 실제 채택한 관계 **7개 중 5개**를 원본 픽셀에서 확인했다. 전체 복합 조건의 완전 합격은 **0/3**이다. B와 C의 활성 일반 gate 통과가 선택한 겨울 관계나 모든 독립 목표의 통과를 대신하지 않는다. 세 arm의 전체 겨울 분위기와 의복 소재는 분명하지만 부분 구현과 가림은 완전 합격으로 올리지 않았다.

- **A:** 케이블 가디건·색 배색 니트·셔츠의 층과 골지 표면은 읽힌다. 새 `winter_wf36_v1`의 단추는 한쪽 앞섶에 달려 있을 뿐 반대 앞섶 단춧구멍을 통과해 두 가장자리를 연결하지 않는다. 머플러의 아래 끝 하나는 팔에 가리고, 표식 끈이 가지를 감싸 돌아오는 연결 경로도 확인되지 않는다. 작은 thumbnail에서는 손끝과 가는 끈의 접점이 판독되지 않는다. [프롬프트](arms/a/final_prompt.txt), [원본 이미지](arms/a/generated_result.png), [개별 보고서](arms/a/REPORT.md), [판정 JSON](arms/a/RESULT.json).
- **B:** 새 `winter_wf25_v2`의 같은 코트 후드·목선 연결과 `winter_wf33_v2`의 코트 아래 별도 얕은 누빔 층은 확인된다. 독립 조건 중 하단 토글 2개의 대응 나무 막대는 식별되지 않고, 중간 의복의 민소매 여부는 코트에 가린다. 원래 작성한 스웨터가 베스트보다 아래로 나오는 옷단 순서는 반대가 됐으며, 상자에 닿는 손의 인물 기준 좌우도 바뀌었다. 신체 연결과 접촉 자체는 자연스럽지만 이 작성 조건의 불일치는 남는다. [프롬프트](arms/b/final_prompt.txt), [원본 이미지](arms/b/generated_image.png), [개별 보고서](arms/b/REPORT.md), [판정 JSON](arms/b/RESULT.json).
- **C:** 새 `winter_wf30_v2`의 별도 머플러, `winter_wf78_v1`의 치마와 부츠 사이 가장 바깥 타이츠, `winter_wf01_v2`의 열린 코트 안 별도 니트는 확인된다. `winter_wf65_v1`의 앞꿈치와 뒤꿈치 모두를 받치는 두꺼운 밑창은 구현되지 않았다. 낮은 블록 굽과 얇은 밑창 테두리는 이 조건의 증거가 아니다. 목 위로 드러나야 하는 터틀넥 경계는 머플러에 가린다. [프롬프트](arms/c/final_prompt_en.txt), [원본 이미지](arms/c/generated_image.native.png), [개별 보고서](arms/c/REPORT.md), [판정 JSON](arms/c/RESULT.json).

\* C의 원래 목표 6개 중 양말 끝점 관련 2개는 새 타이츠 관계를 채택하면서 최종 프롬프트에서 제외했다. 최초 목표는 수정하지 않고 미실행으로 기록했으며, 이 두 항목은 생성 모델의 실패로 계산하지 않는다. 나머지 실패 1개는 실제 칼라 가림이다.

이번 결과는 선택 관계 7개에 대한 파일럿이며 전체 162개 변형의 이미지 적합성을 인증하지 않는다. 데이터 반영 전의 대응 이미지가 없어 개선 효과의 인과 비교도 하지 않는다. 세 정상 pack에 직접 노출된 겨울 opt-in 시각 프로필은 모두 0개이며 해당 경로는 **미검증**이다. 연결된 bundle profile을 자동 hard gate로 승격하지 않았다. 얼굴·헤어 참조의 가시적 유사성은 확인되지만 동일 인물의 보증이나 요청자의 만족 판정을 대신하지 않는다.

## 후속 검증 계획

1. 같은 봉인 core와 정상 조회 방식으로 겨울 프로필 노출 경로를 먼저 재현·점검한다. 현재의 미노출만으로 런타임 오류라고 단정하거나 넓은 별칭에 모든 변형을 강제하지 않는다.
2. 현재 원본을 단추의 두 앞섶 접점, 토글 쌍의 전체 개수, 앞·뒤꿈치 밑창 연속성, 가려진 칼라·머플러 끝점의 회귀 반례로 보존한다. 다음 전용 케이스는 필요한 접점과 두 끝점이 함께 보이는 구도를 먼저 정하고 평가한다.
3. 원래 독립 목표와 채택 후 목표의 변경을 추적해 미실행·가림·형태 불일치를 나눠 집계한다. 모든 변형을 인증하려면 미선택 변형과 직접 opt-in 경로의 별도 픽셀 검증이 필요하다.

## 연결 자료

- [304행 반영 경로와 variant/source 매핑](AUTHORED-MAPPING.json)
- [최종 검사](FINAL-CHECKS.json)
- [현재 원본 게시](PRIMARY-APPLICATION.json)
- [작업 전후 비교](PRIMARY-PRESERVATION.json)
- [봉인된 요청과 첨부 바인딩](DELEGATION-BINDINGS.json)
- [조정자의 원본 픽셀 검토](COORDINATOR-PIXEL-REVIEW.json)
- [최종 산출물 바인딩 검증](DELIVERY-VALIDATION.json)
