# 전기 시각 의미·후보 데이터 반영 및 독립 이미지 테스트 결과

2026-10-08. 연구 116개 카드 중 91개를 후보 98개와 새 시각 의미 프로필 97개로 반영하고 최신 로컬 런타임을 활성화했다. 독립 서브에이전트 세 개가 첨부 이미지를 실제 appearance reference로 사용하여 서로 다른 복잡한 장면을 작성·생성·평가했다. **세 장 모두 주요 전기 형상이 보이지만, 전체 필수 기준은 1개 장면만 통과했다.** 부분 실현이나 가려진 관계를 전체 PASS로 계산하지 않았다.

| 구분 | 결과 | 확인 범위 |
|---|---|---|
| 데이터 채택·등록 | PASS | 91개 카드, 98개 후보, 97개 새 프로필; 기존 항목 보존 |
| Dictionary·semantic/visual indexes·runtime publisher | PASS | 최종 immutable generation으로 실제 조회·생성 |
| 전기 회귀 검사 | PASS | 11개; 관련 검사도 통과, 중복 실행 수는 합산하지 않음 |
| 실제 native 생성 | 완료 | 각 arm 1회, 총 3회; 추가 생성 없음 |
| 주요 전기 형상 관측 | 3/3 | 방전 모양·매질·끝점·소유 관계의 보이는 범위 |
| 전체 필수 장면 기준 | **1 PASS / 2 FAIL** | 독립적으로 동결한 기준과 적용된 native gates 모두 고려 |
| 전체 98개 후보·97개 프로필 native 검증 | 미완료 | 실제 선택된 새 ordinary 후보는 3종, 새 전기 프로필은 2종 |
| 사용자 선호·기존 이미지 대비 개선 | 미판정 | 사용자 결과 평가 미수신; 동일 장면 baseline render 없음 |

## 데이터에 실제 반영한 내용

긍정 시각 요소를 원자로 분리하고, 그 요소가 어느 물체·매질·신체에 속하는지 directed relations로 연결했다. 후보는 기존 슬롯 20개에 추가했고, 새 프로필의 전체 native gates는 고유 ID 292개다. 전압/전류 계기, 전기 창/검/채찍, 외부 방벽/몸 표면 갑옷, 서로 다른 채널 색, 왕관/제단/피부 표식처럼 소유와 연결이 다른 항목을 하나의 모호한 electric glow로 합치지 않았다. 오로라는 기존 `auroral_arc_curtain_atmosphere`의 전체 의무를 재사용했다.

- [후보 원본](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_electrical_relations_extension.json)
- [시각 의미 원본](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_electrical_relations.json)
- [중앙 등록 manifest](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_source_manifest.json)
- [연구 카드별 채택·보류·출처 매핑](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/ADOPTION-LEDGER.json)
- [구현·effects 검토·검사 세부 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/README.md)

P0 24개 전부, P1 47개, P2 20개를 채택했다. 이 카드들이 연결하는 seed 키워드는 184개다. 원 연구의 435개 키워드 전체를 각각 독립적으로 검증·승격했다는 뜻은 아니다. 나머지 25개는 시간 연속 기록이 필요한 표현, 보고된 구상 발광의 물리적 정체, 임상·전문 도해, 목적·음성·비유 의존 의미 등을 구별해 보류했다. 출처 URL과 연구 상태는 evidence ledger에 두었으며 검색 후보의 긍정 시각 문장에 검증되지 않은 과학적 사실처럼 넣지 않았다.

Broad electricity/번개/색/비유만으로 특정 방전의 hard duty가 생성되지는 않는다. Approximate discovery는 선택 가능한 제안으로 남고, 명시적으로 채택한 시각 프로필의 전체 의무는 생략할 수 없다. 초기 `target: * / property: *` effects가 얼굴·헤어 lock과 과도하게 충돌하는 문제를 실제 조회에서 발견해, 생성 전에 property domain을 검토·수정하고 모든 arm에서 원래 입력 bytes를 그대로 replay했다. 얼굴·헤어를 바꾸지 않는 장치 방전은 허용되지만, 같은 hair geometry나 skin marking lock은 다른 carrier dimension으로 우회할 수 없다.

## 사용한 최신 스킬과 독립성

세 arm은 현재 작업 공간의 [photo-prompt-image-generator SKILL.md](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/SKILL.md)를 사용했다. SHA256은 `9e9b87e6f0b2c1ec1c36bd8e9d55f90950d53529a0b873722b546924dfc7043b`이고, candidate pack V6로 실행했다. 각 agent는 fresh context에서 일반 지식과 허용된 neutral 입력 및 원본 reference만으로 랜덤 seed, 장면, core, baseline, selection, 접촉 검토와 자체 pixel criteria를 먼저 동결했다. 후보·연구·다른 arm 결과를 이 단계에서 읽지 않았다. 이후 최신 generation을 조회한 후보 중 자신의 장면과 양립하는 항목만 선택했다. 세 run manifest의 `cross_arm_inputs_used`는 모두 false다.

Controls는 모두 sensual 1, fetish 0, creativity 1, surreal 0, reference_edit_mode off이며 별도 override는 없었다. 첨부 이미지는 얼굴·헤어 appearance reference로 실제 전송했다. 인물의 신원·나이·성격·직업·과거는 사진에서 추정하지 않았고, 세 장면의 역할과 이야기는 agent가 작성한 허구다.

원본 reference SHA256: `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`.

세 run 모두 다음 source generation에 연결됐다.

- Generation: `2834651af2b0ea5161d8a8cc743ff23525b6479a89a30bcda7ee6af05b632da6`
- Source fingerprint: `4ab1a58fdb72b9bcad7e3a934410acc9c555202f7942f62c8a7b2b6dae68674c`
- 로컬 활성화 revision 51. Semantic index 10,888 entries / 16 shards, visual index 2,645 profiles / 5,261 exact terms.

실제 생성 도구는 native `image_gen`이다. Workflow transport의 모델 기본값은 실제 반환 이미지의 모델 관찰 증거로 취급하지 않았다. 실제 이미지 dimensions와 hash는 반환된 원본 파일에서 확인했다.

## Case 1 — 이동 박물관 고전압 시연기 복원

랜덤 seed `8405845492962504737`. 복원 기록을 적는 인물, 여행용 케이스와 교체 부품, 금속 구형 단자 사이의 짧은 청백색 spark, 별도 곡선 유리관 내부의 주황·적색 glow를 한 장에 배치했다. 두 현상의 공간·형상·매질·끝점을 구분하고 손의 접촉 대상까지 검사하는 장면이다.

![Case 1 원본 native 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/qualification/case-1/image.png)

[영문 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/qualification/case-1/prompt.en.txt) · [실제 runtime 전송 문장](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/qualification/case-1/runtime.prompt.txt) · [동결 기준](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/qualification/case-1/frozen_native_criteria.json) · [agent 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/qualification/case-1/independent_native_assessment.json) · [root 별도 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/qualification/case-1/root_native_review.json)

Ordinary 후보 `electric_short_spark_gap`와 새 프로필 `electric_short_spark_gap_relation`, `electric_bounded_glow_tube_relation`를 실제 선택했다. 두 프로필의 전기 gates 6/6 PASS다. Spark의 양 끝이 각각 금속 tip에 붙고 주변 공기는 더 어둡다. 곡선 유리관의 광량은 관 내부에 머물며 두 끝 cap과 유리 가장자리가 구별된다. 원본 appearance와 복원 흔적도 읽힌다.

**전체 FAIL.** 원래 동결한 `E07_body_and_contact`의 왼손은 별도 콘솔에 놓여야 하지만, 실제로는 기록지·앞 작업대 가장자리에 놓였다. Native `embodiment_contact_and_space`도 FAIL이라 formal hard gates는 10/11이다. 전기 주제 형상 기준은 4/4, 보조 기준은 4/5지만 두 수를 전체 성공으로 합치지 않았다. 이는 접촉 대상의 실현 실패이며 손의 해부학적 변형으로 진단하지 않았다.

한 장의 still은 spark의 짧은 지속 시간이나 glow의 연속 작동을 확인할 수 없다. 6개 프로필 gate와 주제 형상의 PASS는 보이는 공간 형태를 대상으로 하며, temporal 부분은 UNOBSERVABLE로 별도 기록했다. 실제 전압·가스 종류·이전 복원 성공도 입증하지 않는다.

원본 1536×1024, SHA256 `4cc467f4dbe5ed0e7bcdba6635c608fde1ec29eb2f97783ec2fcd69a2823d633`. Native 호출 1회, ledger run `81e1a79027a362a3`.

## Case 2 — 폭풍 속 선박 조타실

랜덤 seed `8647799625889260945`. 한 손은 젖는 기상 기록지를 눌러 고정하고 다른 손은 창 latch를 잡는다. 창밖 가까운 금속 mast tip에는 국소 청자색 corona, 먼 구름 안에는 가로 방향의 흰 branching lightning을 배치했다. 거리·광원 소유·인물의 두 접촉과 계측 화면을 함께 검사한다.

![Case 2 원본 native 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/qualification/case-2/image.png)

[영문 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/qualification/case-2/prompt.en.txt) · [실제 runtime 전송 문장](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/qualification/case-2/runtime.prompt.txt) · [동결 기준](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/qualification/case-2/frozen_native_criteria.json) · [agent 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/qualification/case-2/independent_native_assessment.json) · [root 별도 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/qualification/case-2/root_native_review.json)

새 ordinary 후보 `electric_screen_voltage_time_axes`를 실제 선택했다. 같은 화면의 graticule/trace, 세로 V 축, 가로 ms 축, 같은 계측기의 probe 연결이라는 components 4개와 directed relations 2개가 모두 보인다. 새 전기 visual opt-in profile은 이 pack에 노출되지 않았고 강제로 삽입하지 않았다. 기존 `pr_atmospheric_distance_contrast` 프로필을 선택했다.

**전체 PASS.** 독립 필수 5/5, 기존 atmosphere gates 4/4, embodiment gates 5/5라 formal hard gates 9/9다. 구름 내부의 수평 분기와 두 금속 tip의 작은 brush가 다른 위치·깊이·carrier로 구별된다. 두 손의 arm chain과 지정한 접촉 표면도 보인다. Root는 child 최종 판정 전에 원본을 보고 같은 결론을 기록했다.

표시 화면이 이 폭풍을 측정했다는 증거는 없다. Probe는 계측기에 연결되어 있지만 counter에 놓여 있다. 실제 IC lightning 메커니즘·전기장·보정된 전압값이나 창이 닫히는 시간 변화는 입증하지 않는다. 카메라를 바라보는 시선으로 작업 순간이 다소 연출된 인상이고, 요청하지 않은 작은 문구·브랜드가 생긴 점은 별도 미학적 한계로 기록했다.

원본 1536×1024, SHA256 `857941654d683d43c2108d05c7da323e1483206e95edc47f94b1d8b299428f4a`. Native 호출 1회, ledger run `9647287d37f62cf3`.

## Case 3 — 마지막 등대 기록실의 장치 종료

랜덤 seed `1574489756`. 정리된 기록 상자와 떠날 가방 앞에서 lever를 잡은 인물, ceramic pedestal의 두 구형 전극, 작은 spark와 별도 comb tip corona, coil과 lamp의 배선을 배치했다. 허구의 장치이지만 photographic materials와 접촉·배선 끝점이 읽혀야 한다는 기준을 먼저 동결했다.

![Case 3 원본 native 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/qualification/case-3/image.png)

[영문 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/qualification/case-3/prompt.en.txt) · [실제 runtime 전송 문장](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/qualification/case-3/runtime.prompt.txt) · [동결 기준](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/qualification/case-3/frozen_native_criteria.json) · [agent 최초 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/qualification/case-3/independent_native_assessment.json) · [root 별도 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/qualification/case-3/root_native_review.json)

새 ordinary 후보 `electric_declared_spark_gap_apparatus`와 `electric_short_spark_gap`를 선택했다. Components 6개와 directed relations 2개 모두 PASS다. 두 terminal과 별도 ceramic support, 그 사이의 gap, 양 끝에 붙은 얇은 spark가 보이고 별도 comb에 국소 corona가 붙어 있다. 이 pack에서는 새 전기 visual opt-in profile이 노출되지 않아 선택하지 않았다.

**전체 FAIL.** 원래 독립 필수 기준은 5/6이다. `fiction_circuit_ownership`이 요구한 램프의 짝 배선 중 귀환 경로의 두 번째 끝점을 추적할 수 없다. 한 가닥 외피가 보인다는 이유로 내부의 숨은 conductor 수나 완전한 회로를 추정하지 않았다. 이 조건은 formal embodiment-only 계약에 포함되지 않으므로 formal hard gates 5/5 및 review audit는 PASS다. 이 감사 PASS를 전체 독립 테스트 PASS로 승격하지 않았다.

Lever와 두 손의 접촉, appearance, 물리적인 brass/ceramic/glass/wool은 잘 읽힌다. 램프 점등의 onset, 실제 작동 회로, 마지막 keeper라는 과거는 한 장에서 증명할 수 없다.

원본 1024×1536, SHA256 `50f178a4f7ff9973450f7a026b4c68b97fdcceab387ae0dcc84fee673f36e788`. Native 호출 1회, ledger run `542fd7b777eaa7fc`.

## 감사 기록과 생성 실패 처리

세 managed run 모두 `review_record_validated`까지 진행했고 stale artifact가 없다. 원본 이미지·조합 프롬프트·실제 runtime prompt·동결 criterion·skill·reference·source generation hash를 대조했다. Review schema failures는 세 admitted record 모두 0개다. 기술 판정은 arm 1 FAIL, arm 2/3 PASS이며, 전체 독립 장면 판정은 arm 1/3 FAIL, arm 2 PASS다.

초기 effects 충돌 pack, controls seed 결합 실패, compose/review wire 형식 실패는 pre-render 기록으로 보존했다. 이 실패들이 이미지 재생성을 일으키지는 않았다. Arm 3에서는 반환 경로를 두 개 붙여 읽은 observer가 실제 접근 가능한 결과를 preview-only로 오분류했다. 원래 관찰·metadata를 보존하고 실제 경로와 bytes를 확인해 **같은 recorder operation**만 회복했다. Native 도구 오류·fallback·추가 호출은 없었다.

[통합 case manifest](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/qualification/CASE-MANIFEST.json)에는 원본 경로, exact prompt/image hash, actual call count, 선택 항목, source binding과 각 판정이 있다. 각 case 폴더의 `run_manifest.json`, `native_ledger_row.json`, `review_audit.json`과 pre-core/selection/compose/runtime 증거는 admitted 원본의 byte 사본이다. `runtime.prompt.txt`는 실제 전송 문장으로, 읽기용 positive prompt에 runtime 계약을 덧붙인 전체 문장을 확인할 수 있다.

## 이번 결과로 좁혀진 후속 반영 계획

| 우선순위 | 관측한 문제 | 다음 변경·검사 |
|---|---|---|
| P0 | Arm 1의 손 접촉 표면이 지정과 다름 | 다음 독립 장면에서 별도 콘솔·기록지·손 접촉 영역을 구도로 분리하고 정확한 표면을 볼 수 있게 구성한다. 원 criterion을 완화하지 않고 같은 contact gate로 재평가한다. |
| P0 | Arm 3의 두 번째 램프 배선 끝점이 가려짐 | 두 외부 lead가 coil↔lamp의 각 terminal에 붙는 경로·양 끝점을 동시에 보이게 한다. 장면이 요구하면 별도 closed-loop 후보/프로필을 채택하고 모든 endpoint gate를 검사한다. 모든 electricity 후보에 짝 배선을 의무화하지 않는다. |
| P1 | 대기·허구 arm에서 새 전기 visual opt-in이 노출되지 않음 | 현재 정확한 core 문맥과 source evidence requirements의 매핑을 별도 retrieval 회귀로 진단한다. 의미가 맞는 optional 제안의 노출을 검토하고, 기존 pre-core 의미나 필수 의무를 넓히지 않는다. |
| P1 | 새 ordinary 후보 3종, 새 전기 프로필 2종만 native 평가 | Hair/skin/surface/material, plasma media, field/charge apparatus, bounded fictional objects 등 아직 생성하지 않은 family를 소유·관계·혼동 boundary별 추가 native cases로 확장한다. |
| P1 | brief/sustained/onset·측정 causality는 still에서 미확인 | 시간 의미는 sequential frames/video나 별도 instrument record가 필요한 후속 검증으로 둔다. Still 판정은 보이는 carrier·형태·공간 관계로 제한한다. |
| P2 | 25개 보류 family | 임상·전문 도해·정체가 불명확한 현상은 각 전용 source/evidence 계약을 먼저 연구하고, generic glow로 대체하지 않는다. |

이번 테스트를 맞추기 위해 원 기준을 수정하거나 다른 arm의 컨셉을 섞지 않았다. 후속 native 확대·수정 생성은 이 보고서에 계획으로 남겼고 이번 실제 호출 수에는 포함하지 않는다. 세 장의 관측으로 데이터 전체의 native 성공이나 통계적·인과적 개선을 주장하지 않는다.

## 보존·제출 상태

[최종 보존 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/PRIMARY-PRESERVATION-FINAL.json)는 시작 시 보호 대상으로 수집한 23,998개 중 의도한 manifest/semantic-index/visual-index 3개를 제외한 **23,995개 파일이 byte-identical이고 삭제가 0개**임을 확인했다. 비교 대상에는 이번 owned integration 경로와 run artifact 경로를 포함하지 않았으므로 전체 파일 시스템 보존 증명으로 해석하지 않는다. HEAD는 시작과 끝 모두 `0f970cdfdeb1715f05da4480442de7a1e1c7b849`다. Reference 원본 hash도 그대로다.

반영·검증·로컬 runtime 활성화는 완료했다. Commit/push/PR은 수행하지 않았다. [최종 검증 상태 JSON](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/INTEGRATION-VALIDATION.json)에 데이터·검사·runtime·native 판정·보존 상태를 함께 기록했다.
