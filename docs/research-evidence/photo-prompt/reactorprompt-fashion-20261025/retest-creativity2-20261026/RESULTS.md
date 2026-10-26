# 패션 후보 검색·선택 보완 및 creativity=2 재시험

같은 첨부 사진을 사용해 독립 gpt-6-luna/max 저자 3명이 각자 기본안·질의를 작성하고, 기본 image_gen을 1회씩 호출했다. 총3장 모두 반환·저장됐고 원본/사본 해시와 호출 입력을 대조했다. **전체 신규 패션 코호트에서는 B안의 크림색 하이넥 니트와 별도 남색 코트의 겹침 1건이 프롬프트와 실제 픽셀에 반영됐다. 보강한8개 자체의 직접 기여는0건이다.** 후자는 모두 해결된 것으로 볼 수 없다.

## 검색되지 않은 원인

8개 모두 실제 선택된 e8d4f903… 색인에 들어 있고 각5개 alias가 존재한다. 직전42개 질의에서 후보별 최고 전체 순위는368,416,583,1860,2212,1111,1345,1026위로, 기존32개 창 밖이었다. 같은 질의를 그대로 쓰면96개 창에도 들지 못한다. 색인 누락이나 표본 추출 결함으로 볼 근거는 없다. 질의가 자기 기본안의 실제 의상명·소재·형태를 지우고 추상적인 읽힘/분위기로 약해진 것이 중요한 원인이었다.

별도9개 진단 질의에서는 회색 헤링본 코트가66위·92위로 올라왔다. 이 진단은 조사자가 alias를 본 뒤 작성했으므로 독립 시험 성과로 세지 않았다. 실제 독립 재시험에서는 로퍼 후보가 C-footwear의 발급된96개 창 중25번째에 들어왔지만, 최초 표본에는 뽑히지 않았다. 첫 eligible anchor1개와 나머지 표본의 무작위 선택은 특정25번째 후보의 노출을 보장하지 않는다. 재추첨이나 목표 후보 강제 삽입은 하지 않았다.

## 이번 보완

- [SKILL.md](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/SKILL.md): 역할에 맞는 실제 의상·소재·owner 관계를 질의에 남기고, 편집 가능한 선택이라는 이유로 검색 단서를 지우지 않도록 했다. 최소 식별 근거에 임의의 포즈·연출을 붙여 필수 조건으로 고정하는 문제도 보완했다.
- [composition-contract.md](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/composition-contract.md): 다른 옷·색·장면을 실제 조건 위반과 구분하고, creativity2–3에 맞는 완전한 교체·재구성 대안을 비교하도록 했다.
- [photo_semantic_witnesses.md](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/precore/photo_semantic_witnesses.md): 최소 owner/role/presence 증거와 전체 요청 provenance, 진짜 보호할 행동·관계의 근거를 분리했다. 잘못 동결된 초기 core는 보존하고 후보 접근 전에 새 core로 교정했다.

문서 변경 두 묶음은 독립 검토를 통과했다. 설치된 검색·생성 런타임 코드·후보 레코드·색인·점수식·추출 알고리즘·보호 조건은 이번에 바꾸지 않았다. 실행 근거를 대조하는 시험용 helper는 별도로 추가했다. 설치된 파서가 비유적 연결/배경의 물과 옷 윤곽을 잘못 묶는 한계는 의미를 명확히 한 질의로 피했으며, 일반적인 파서 결함까지 수정한 것으로 주장하지 않는다.

세 기본안과 모든 질의를 검색 전에 확정했다. 실제 발급된20개 역할 질의와6개 장면 전체 질의가 검토한 내용과 일치했고, 모두96/12 정책을 사용했다. 저장된 전체 출처 페이지와 발급 표본, 실제 선택 행의 CID/RID/hash/질의 조합을 대조했다. A83종/96건, B88종/96건, C104종/120건이 모두 일치한다.

C안의 선택 기록에서는 불투명 타이츠·페이턴트 로퍼와 정장 구두에 다른 출처의 반투명/하이힐 속성을 섞은 오류, 실제 전체 효과가 없는 대안을 비교 근거로 인용한 오류도 발견했다. 같은 저자가 실제5개 출처의 완전한 A7–A11 대안과 출처별 이유를 작성해 교정했다. 원본을 보존하고 root가 의미를 대조한 뒤에만 생성했다. 선택 횟수나 특정 후보 채택은 강제하지 않았다.

## 단계별 결과

| 단계 | 신규 패션 코호트2430개 | 보강8개 |
|---|---:|---:|
| 발급 검색 창 | 고유67개 / 중복149건 | 1개 / 1건 |
| 실제 표본 | 고유17개 / 중복19건 | 0 |
| 최종 프롬프트의 새 기여 | 1개 | 0 |
| 관찰 가능한 신규 시각 단서 검증 | 1개, B안 | 0 |
| native 전체 후보 공식 선택 | 0 | 0 |

전체 표본은312건, 고유CID254개다. 최종 일반적 영감은8건이고, root의 복합 픽셀 기준에서5건 통과·3건 부분 충족이다. 이 수치는 후보 전체의 native 채택과 다르다. 이전 시험의 신규 표본5건보다 이번19건이 많지만, 기본안·질의·창 크기가 함께 바뀌었으므로 한 변경의 인과 효과나 품질 향상을 입증하지는 않는다.

| 안 | 신규 코호트 표본 | 새 프롬프트 기여 | 신규 시각 단서 통과 | 보강8개 기여 |
|---|---:|---:|---:|---:|
| case-a | 3종 / 3건 | 0 | 0 | 0 |
| case-b | 5종 / 5건 | 1 | 1 | 0 |
| case-c | 9종 / 11건 | 0 | 0 | 0 |

B의 출처는 `cand_24b2c29e16ee56b39c5ebcef5695bb2a / base`, hash `adb49b5d00e523a11e97c2b2def7034c153d6cbcdd3448c391a02e946011a477`이다. 기존 새틴 블라우스가 크림색 하이넥 니트로 바뀌고, 별도 남색 코트 아래 목 부분과 소매가 구분돼 보인다. 실제 섬유 성분까지 픽셀로 입증한 것은 아니다.

A는 패션·부두·몸의 회전은 보이지만 시선이 카메라로 돌아와 부두를 향한 관심 관계가 부분 충족이다. far shoe의 접점도 일부 가려져 두 밑창 전체의 평평한 지지를 root가 추정하지 않았다. B의 blue/amber 조명은 전체 인상으로 보이나 두 수광 영역이 표면 굴곡/가림을 따르는 복합 조건은 부분 충족으로 보수적으로 판정했다. C는 한쪽 지지 다리와 기울어진 가벼운 반대쪽 접촉이 구분돼 일반적 자세 단서를 통과했다. 진로 선택 같은 마음속 의도와 마지막 열차라는 시간 사실은 한 장으로 입증하지 않았다.

A의 로퍼나 C의 광택 있는 신발처럼 생성기가 만든 세부가 미채택 후보와 닮아도 그 후보의 기여로 소급하지 않았다. 특히 보강8개는 실제 입력 표본에 없었다. `partial_is_fail`과 `UNOBSERVABLE_NOT_PASS`를 유지하며 사용자 수락은 pending이다.

## 이미지와 프롬프트

- case-a: [이미지](/Users/chasoik/Projects/image-prompt/generated/images/reactorprompt-fashion-creativity2-20261026/case-a.png), [최종 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/reactorprompt-fashion-creativity2-20261026/delivery/case-a-prompt.txt), [root 픽셀 판정](/Users/chasoik/Projects/image-prompt/generated/photo-runs/reactorprompt-fashion-creativity2-20261026/ROOT-PIXEL-REVIEW-a.json)
- case-b: [이미지](/Users/chasoik/Projects/image-prompt/generated/images/reactorprompt-fashion-creativity2-20261026/case-b.png), [최종 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/reactorprompt-fashion-creativity2-20261026/delivery/case-b-prompt.txt), [root 픽셀 판정](/Users/chasoik/Projects/image-prompt/generated/photo-runs/reactorprompt-fashion-creativity2-20261026/ROOT-PIXEL-REVIEW-b.json)
- case-c: [이미지](/Users/chasoik/Projects/image-prompt/generated/images/reactorprompt-fashion-creativity2-20261026/case-c.png), [최종 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/reactorprompt-fashion-creativity2-20261026/delivery/case-c-prompt.txt), [root 픽셀 판정](/Users/chasoik/Projects/image-prompt/generated/photo-runs/reactorprompt-fashion-creativity2-20261026/ROOT-PIXEL-REVIEW-c.json)

## 검증 및 한계

최종 프롬프트 감사3/3은 실패 없이 통과했다. 보존된 근거에 관한 비차단 `uncovered_intent` 경고21건은 기록에 남겼다. 최종 native 실행은 각1회, 총3회이며 실제 저장 호출 객체가 native-plan payload와 같고 정확한 프롬프트·동일 사진 경로를 포함한다. 실행/리뷰 기록과 원본·사본 SHA-256을 대조했다. 관리형 기술 리뷰 결과와 root의 실제 픽셀 판정은 별도로 보존했다.

전체2556개 문서의 이미지 구현 시험은 아니다. 8개 모두의 실제 반영, native 전체 출처 채택, 사용자 선호 및 같은 core를 쓴 creativity1 대비 인과적 품질 개선은 입증하지 않았다. C의 지연 중 같은 저자를 재개한 일과 A의 기술적 집계 숫자 노출 등 제한적 절차 편차는 [PROCESS-DEVIATIONS.json](/Users/chasoik/Projects/image-prompt/generated/photo-runs/reactorprompt-fashion-creativity2-20261026/PROCESS-DEVIATIONS.json)에 공개했다. 다른 안의 프롬프트·이미지·후보 본문을 저술 입력으로 제공하지 않았다.

기계 판독 결과: [FINAL.json](/Users/chasoik/Projects/image-prompt/generated/photo-runs/reactorprompt-fashion-creativity2-20261026/FINAL.json). 단계별 근거: [검색 노출](/Users/chasoik/Projects/image-prompt/generated/photo-runs/reactorprompt-fashion-creativity2-20261026/RETRIEVAL-EXPOSURE.json), [선택 대조](/Users/chasoik/Projects/image-prompt/generated/photo-runs/reactorprompt-fashion-creativity2-20261026/MATERIAL-USE-AUDIT.json), [출처 페이지 범위](/Users/chasoik/Projects/image-prompt/generated/photo-runs/reactorprompt-fashion-creativity2-20261026/SOURCE-VIEW-COVERAGE.json), [실제 호출·파일 검증](/Users/chasoik/Projects/image-prompt/generated/photo-runs/reactorprompt-fashion-creativity2-20261026/DELIVERY-VERIFICATION.json). 자세한 원인과 변경은 [ANALYSIS-AND-CHANGES.md](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-fashion-creativity2-20261026/ANALYSIS-AND-CHANGES.md)에 있다.
