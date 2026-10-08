arm-1은 “비에 씻겨 거칠어진 야외 클레이 코트를 인물이 수동 롤러로 복구하는 순간”을 seed 126364945로 독립 선택했다. native image_gen을 1회 호출해 실제 PNG를 얻었으며, 저장 원본과 arm 복사본은 동일한 SHA-256을 갖는다. 이미지 크기는 1237×1272이다.

흙 주제의 구현은 **pass**다. 원통 앞의 거친 젖은 흙 덩어리, 원통의 지면 접촉, 뒤쪽의 매끈한 압착 띠가 같은 프레임에서 이어진다. 부츠·의복에는 국소 흙 부착이 보이고, 낡은 네트·울타리·흰 코트선이 복구 작업의 용도를 설명한다. 첨부의 짧은 검갈색 bob, 성긴 앞머리, 어두운 눈과 부드러운 얼굴·입술 특징도 유지된다. 이는 보이는 외형의 비교이며 실제 신원 판정은 아니다.

새 흙 데이터의 실제 프롬프트 기여는 **0**이다. soil_e082의 완전한 의미는 도구가 고랑을 만들고 뒤집힌 흙을 그 옆에 남기는 과정이고, soil_e097은 흙 안료·도막 견본·결합제를 함께 놓는 과정이다. 두 후보 모두 팩에서 노출됐지만 현재 압착 복구에 덜 유용해 채택하지 않았다. 흙 관련 visual concept는 노출되지 않았다. 최종 프롬프트는 후보 접근 전에 고정한 baseline과 바이트가 같으며, 이미 존재하던 흙 표현을 새 데이터의 개선 효과로 계산하지 않았다.

**현재 스킬의 hard gate**

| 항목 | 결과 | 픽셀 근거 |
|---|---|---|
| 신체 소유 | pass | 같은 인물의 두 팔·손·다리·부츠가 연결된다. |
| 관절·도달 | pass | 몸통→팔→손잡이, 양측 프레임→원통 축의 경로가 일관된다. |
| 지지·균형 | pass | 어긋난 두 부츠가 몸을 받치고 원통은 지면에 실린다. |
| 접촉·공간 | pass | 손의 막대 grip과 원통의 흙 접촉, 앞/뒤 표면 변화가 명료하다. |
| 가시성·투영 | pass | 얼굴·양손·부츠·롤러·핵심 지면 관계를 모두 검토할 수 있다. |

whole view와 original 배율로 실제 저장본을 봤다. review audit는 record_valid=true, technical_qualification=pass이며 schema failure와 failed hard gate는 없다. 초기 준비 오류와 invalid review는 보존했고, 최종 기록은 실제 native 반환 경로와 해시에 묶었다.

**제가 만든 보조 테스트 기대값**

| 기대 관찰 | 결과 |
|---|---|
| 거친 흙과 평탄한 압착 띠 | pass |
| 손·도구·지면·압착 결과의 연결 | pass |
| 유실 홈과 침전 팬의 연속성 | fail |
| 고운 침전과 자갈의 분리 위치 | fail |
| 광택 있는 젖은 면과 밝은 무광의 거친 면 | pass |
| 코트 복구 행동의 목적 | pass |
| 참고 얼굴·헤어 외형 | pass |
| 현재 작업과 압착 결과의 장면 이해 | pass |

보조 기대값은 요청자 하드 의무가 아니다. 6/8 관찰만 통과했으므로 보조 테스트 전체는 **fail**로 남겼다. 오른쪽 웅덩이와 밝은 퇴적 같은 표면은 있으나 유실 홈과의 연결은 불명확하다. 주변 큰 조각이 자갈인지 흙 덩어리인지도 충분히 구분되지 않는다. 작은 보조 차이 때문에 추가 생성하지 않았다.

현재의 작업·압착 결과는 설명 없이 읽히지만, 구체적인 강우 유실과 입자 sorting의 앞선 과정은 일부 작가 설명에 의존한다. 얼굴·팔의 존재감과 실용적인 동작에 보조적인 인물 매력이 더해져 저장된 sensual 1에 대체로 부합한다. fetish 0, surreal 0의 일상적 장면을 유지했다. 사용자의 미학적 수용은 **not_yet_received**이며, 별도의 baseline 렌더와 비교하지 않아 새 데이터의 픽셀 개선이나 선호 우위를 주장할 수 없다.

[저장 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/soil-earth-semantics-20261008/image-tests/arm-1/render-attempt-1.png), [최종 영문 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/soil-earth-semantics-20261008/image-tests/arm-1/final_prompt_en.txt), [결과 JSON](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/soil-earth-semantics-20261008/image-tests/arm-1/ARM-RESULT.json), [데이터 기여 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/soil-earth-semantics-20261008/image-tests/arm-1/DATA-CONTRIBUTION.json), [픽셀 리뷰](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/soil-earth-semantics-20261008/image-tests/arm-1/final_visual_review.json), [독립 manifest](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/soil-earth-semantics-20261008/image-tests/arm-1/run_manifest.json), [ledger](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/soil-earth-semantics-20261008/image-tests/arm-1/image_runs.ndjson).

팩 2cb0afc9676d67ee와 실제 receipt는 generation b731e8ce874eb58e76404f5d61045ccc0de201dac6e4a47137c6635d5ed32e7c에 결속된다. ledger에는 실제 호출 성공 1행만 있으며 run_id는 a4107fe4a7b7c035이다. native 도구는 이미지 모델 식별자를 제공하지 않았다. 다른 arm의 프롬프트·팩·이미지는 입력으로 사용하지 않았다.
