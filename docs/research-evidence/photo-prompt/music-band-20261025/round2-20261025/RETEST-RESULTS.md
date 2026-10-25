# 음악물 후보 미채택 분석·개선·재시험

2026-10-25. 같은 참고 파일로 새 독립 서브에이전트 세 곳에서 한 장씩, 실제 native 이미지 3장을 생성했다. 기존 21개 판정 항목은 원문과 해시를 보존했다. 부모의 보수적인 직접 픽셀 판정은 **13/21 → 16/21**, 엄격 전체 장면 통과는 **0/3 → 0/3**이다. 얼굴·머리 참고와 음악 주제는 계속 3/3 통과했다. 기존 통과 항목의 회귀는 없었다.

일부 수리는 실제로 보인다. 밴드의 드럼 의자 지지, 스튜디오의 배우 기준 좌우 손 역할과 USB 경로가 개선됐다. 다만 밴드의 완전한 케이블 연결, 정확한 페달 접점, 눌린 흰 건반을 확인하는 조건은 남았다. 전체 실패가 해결됐다는 결론이나 신규 음악 데이터의 인과적 효과는 주장할 수 없다.

**미채택 원인과 수정.** 첫 시험의 미채택은 서로 다른 단계에서 발생했다. 밴드에는 사건·인원·기구를 바꾸는 후보가 있었고, 피아노의 양손·건반 관계는 독립 초안에 이미 있었다. 스튜디오의 새 자료는 rank window에는 있었으나 작가가 읽는 표본에 없었다. 이들을 모두 승인 플래그 때문이라고 설명하면 부정확하다.

일부 일반적인 손·발 지지 조언에는 `native_approval: false`와 여러 신체 부위를 언급한다는 사실을 과도한 거부 근거로 쓴 흔적도 있었다. 최신 canonical SKILL과 composition-contract에 일반적인 조언과 전체 원문 계약을 구분하는 세 문단을 추가했다. 실제 충돌·중복·조건·가시성 부담을 근거로 판단하고, 유지된 조언에는 초안과 달라진 최종 문장과 독립적인 정당화를 남기도록 했다. 실제 native 계약의 조건·소유자·권한은 그대로다. [원인 분석](ROOT-CAUSE-ANALYSIS.md), [이번 수정만의 patch](skill-policy-clarification.patch), [변경 전후 해시](policy-patch-provenance.json)에 근거를 보존했다.

시험에 사용한 SKILL SHA256은 `d666eb93c9335508f0e5db27efa90b8915e9638eeda694703de05df8a0446957`이다. 후보·시각 의미 데이터와 검색 선택 파일, 검색·표본 정책은 이번 수리를 위해 바꾸지 않았다. 시각 카드 124개의 미승인 상태와 자동 hard activation 비활성도 유지했다.

**재시험 통제.** `/root/music_r2_a`, `/root/music_r2_b`, `/root/music_r2_c`는 각각 새 문맥에서 시작했다. 자기 부모의 검증된 retry context와 관련 실패를 받아 독립 초안을 먼저 동결했고, 다른 팔의 초안·후보·이미지로 초기 초안을 만들지 않았다. 이후 원래 testcase를 읽고 동일 기준을 보존했다. 카메라·배치·자세·접점·조명의 열린 범위에서 수리했고, 표본을 받은 뒤 seed를 바꾸거나 신규 CID를 지정해 노출시키지 않았다. [생성 전 고정 기록](PROTOCOL.json)에 세 core·참고·기준 해시가 있다.

참고 파일 SHA256은 `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`이다. 세 실제 payload 모두 같은 절대 파일 경로를 `referenced_image_paths`로 첨부했다. [전달 검증](transport-verification.json)에서 payload와 감사된 runtime prompt의 동일성을 확인했다. 원본 이미지는 byte-identical로 보존했고 편집·재인코딩하지 않았다. 실제 모델명은 도구가 반환하지 않아 `unknown`이다.

| 장면 | 첫 시험 | 재시험 부모 판정 | 실제 부분 개선 | 남은 완전 조건 |
| --- | --- | --- | --- | --- |
| A 밴드 | 3/6 | 4/6, 전체 FAIL | 의자 좌면·기둥·다리 지지, 스네어 막대 끝 접촉, 바닥 케이블 대부분 | 기타 plug 주변 추가 loop의 연결 모호함. lead의 고개가 큐인지 프렛 확인인지 불명확 |
| B 피아노 | 6/8 | 6/8, 전체 FAIL | 페달 세 shaft와 lyre·양발 노출 증가 | 신발 앞이 실제 작동 pedal tip을 겹쳐 정확한 오른쪽 sustain 접점을 확정하기 어려움 |
| C 스튜디오 | 4/7 | 6/7, 전체 FAIL | 왼손 건반·오른손 노브 역할 수리, 두 케이블 전체 경로와 필수 끝점 노출 | 정확한 흰 건반 눌림 상태와 손 접점 |

A의 독립 에이전트는 고개 큐를 통과로 보고 **5/6**으로 평가했다. 부모는 경쟁하는 프렛 확인 해석 때문에 해당 결합 조건을 partial로 남겼다. 두 판정을 보존하며, 독립 팔 합계는 17/21, 부모 합계는 16/21이다. **엄격 전체 실패 0/3이라는 결론은 같다.** partial을 통과로 올리지 않는다. 정지 사진은 실제 음향·첫 박자 동시성·신호 전달을 증명하지 않는다. [부모 직접 리뷰](parent-pixel-review.json)에 21개 항목별 관찰이 있다.

C의 최초 검토 초안은 4/7이었다. 원래 gate에 없는 printed label/front-only port 및 비필수 외곽 전체 노출을 요구한 가정을 제거해, 두 경로와 필수 끝점이 실제로 보이는 signal/count를 통과로 정정했다. unbranded side의 원형 plug는 일반 audio input으로 물리적으로 그럴듯하며 실제 신호 전달까지 증명하는 판정은 아니다. 정확한 흰 건반 상태는 여전히 실패다. [초기 부모 초안](parent-pixel-review.initial-draft.json)과 [정정 이유](parent-review-clarification.json)를 보존했으며 testcase·이미지·호출 수는 바뀌지 않았다.

**후보 사용 결과.** 원문 view와 최종 결정의 모든 query/CID/RID 및 source hash를 부모가 교차 검증했다. 전체 144 occurrence, 중복을 합친 109개 source를 읽었다. 신규 음악 CID는 14개/22 occurrence였다. 기존 완전 원문 재사용 2개는 신규에서 제외했다. [자료 사용 감사](material-use-audit.json)가 기준이다.

| 팔 | 전체 읽음 고유/등장 | 신규 음악 고유/등장 | 전체 일반 조언 최종 기여 | 신규 음악 최종 기여 | native 선택 |
| --- | --- | --- | --- | --- | --- |
| A | 36 / 40 | 11 / 12 | 1 / 1 | 0 | 0 |
| B | 54 / 72 | 2 / 9 | 1 / 1 | 0 | 0 |
| C | 30 / 32 | 1 / 1 | 1 / 1 | 0 | 0 |

이번에도 신규 음악 후보의 추가 기여는 0이었다. 피아노의 양손·페달 조언은 수리한 독립 초안에 이미 있었고, 스튜디오에 전달된 신규 후보는 계약 압박의 두 사람·추가 소품·다른 사건을 요구해 맞지 않았다. 밴드 후보도 기존 접점과의 중복, 다른 연주 순간·사건 또는 추가 관찰 부담을 구분해 검토했다. 후보별 근거와 완전한 대안 비교는 `arms/*/composition-comparison.md`와 각 팔의 source review에 보존했다. 승인 플래그만의 일괄 거부가 고쳐졌다는 사실과 신규 음악 데이터가 실제로 기여했다는 사실은 별개다.

세 일반 조언의 기여는 모두 기존 자료에서 왔다. A는 기존 stool의 좌면 하중 경계를 읽기 위한 좁은 측면 보조광, B는 이미 바닥에 닿는 왼발·오른뒤꿈치 바로 아래의 접촉 그림자, C는 기존 창빛을 pale wall에서 반사한 얼굴 보조광을 추가했다. soft cushion·paving·casting 장면 같은 전체 원문 구현은 선택하지 않았고 실제 source 조건과 열린 lighting 범위에서 독립적으로 정당화했다. 이 수치는 **최종 프롬프트의 사용 기록**이다. 픽셀에서 그 source 전체를 검증했다거나 그 조언이 개선을 일으켰다는 증거는 아니다. H-F2 material-v2의 native 선택 수 0만으로 일반 조언 기여 0을 추론하지 않는다.

재시험은 고정 H-F2 `d75d1546f9bdb3537d1316c0e14a5a04903fd29b1cedcfc63caefa328b690cd1`, native `f3e06322413adee3264fb44778c3264cee5491f9672236896497edd246707da7`를 썼다. 첫 시험은 이전 음악 전용 release였고, 이번에는 전체 검색 모집단·독립 초안·질의 범위·표본 draw가 다르다. A는 5개 질의, B는 10개 질의 중 1개 빈 결과, C는 4개 질의였다. 생성기도 확률적이다. 따라서 이 세 장의 전후 차이를 스킬 문구나 데이터의 단독 인과 효과로 해석하지 않는다.

마감 중 공유 기본 selector가 다른 버전으로 변경된 것을 확인했다. 스킬 문구·음악 데이터 원문은 시작 해시를 유지했으며 이 작업은 selector를 바꾸지 않았다. 세 실행의 발급 영수증은 위의 동일 고정 버전을 계속 가리킨다. 종료 시 기본값은 H-F2 `0c489235e02de580bfca1a76fdf1ea35b6fa070748c9ee13b301a61c65ee4c21`, native `409e65bb548578f4b995b530a8ea4ba906120b3102c57f89c8e455d4e165a544`였다. 새 기본값의 픽셀 품질을 이번 시험으로 검증했다고 주장하지 않는다. [selector 변경 기록](selector-drift.json)을 보존하고 공유 파일을 덮어쓰지 않았다.

**다음 개선 범위.** A는 기타 plug 주변에 케이블이 분기해 보이는 부분과 명확한 시선/고개 큐, B는 세 pedal 중 실제 작동 끝점의 노출, C는 흰 건반의 정확한 눌림 경계를 우선 수리해야 한다. 이 항목을 해결하기 전에는 완전 픽셀 검증이나 신규 native 승인을 부여하지 않는다. 별도의 신규 데이터 기여 평가는 후보를 보기 전의 독립 초안에 미해결 표현 차원이 남는 holdout 장면에서 반복하고, 초안 중복에는 credit을 주지 않는 방식이 적절하다. 이번 시험 도중 기준을 낮추거나 추가 이미지를 생성하지 않았다.

A [이미지](image-test-evidence/a/image.png) · [실제 프롬프트](image-test-evidence/a/prompt.txt) · [동일 testcase](image-test-evidence/a/testcase.json)

B [이미지](image-test-evidence/b/image.png) · [실제 프롬프트](image-test-evidence/b/prompt.txt) · [동일 testcase](image-test-evidence/b/testcase.json)

C [이미지](image-test-evidence/c/image.png) · [실제 프롬프트](image-test-evidence/c/prompt.txt) · [동일 testcase](image-test-evidence/c/testcase.json)

사용자 수용은 pending이다. 최초 결과는 덮어쓰지 않았다. 최종 통합 상태와 파일·감사 근거는 [FINAL-RESULT.json](FINAL-RESULT.json)에 있다.


최종 마감 검증: 세 workflow는 모두 `review_record_validated`이며 ledger는 각각 실제 native 호출 1행/1회다. 구성·runtime·review 기록 감사는 유효하지만 기술 픽셀 qualification은 모두 실패로 남았다. 입력 key·dispatch·빈 page·부적용 recorder 옵션 같은 처리 실패는 원문을 보존한 뒤 동일 초안/표본/이미지로 복구했고, 추가 이미지 재생성은 없었다. [마감 무결성 검증](final-integrity-validation.json)에 해시·동일 기준·참고 전달·원본 보존 검사를, `SHA256SUMS`에 이번 폴더의 최종 파일 해시를 남겼다.
