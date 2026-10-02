# 독립 시험에서 발견한 검색·표면 의미 보강

2026-10-02. 최초 91축 반영 이후 세 독립 core의 첫 후보팩을 보존했다. A/C의 관련 후보와 B의 피부·체모 후보가 실제 목록에 거의 없었다. 주된 원인은 의미를 이미 담은 `visual_priorities`가 관찰별 검색과 전체 후보 수 제한의 우선순위에 반영되지 않았다는 것이다. 실제 core와 baseline은 변경하지 않고, source-opted-in 후보의 열린 효과와 property lock을 검사하는 공통 검색 경로를 보완했다. 검색에서 떠도 선택 전까지 의무가 생기지 않는다.

추가 데이터는 12개 기존 국소 축의 자연스러운 한·영 의역이다. 넓거나 좁은 어깨, 길거나 짧은 손가락 등 서로 독립된 값의 검색을 지원하며, 서로 다른 값을 하나의 이미지에 모두 요구하지 않는다. 시험 문장 전체나 고정 장면을 positive prototype에 복사하지 않았다. Exact 승격은 하지 않았다.

## S48 — Piloerection의 연결 구조

[Shwartz et al., Cell, 2020](https://pubmed.ncbi.nlm.nih.gov/32679029/), DOI 10.1016/j.cell.2020.06.031. PubMed 초록과 Figure 6 설명을 확인했다. PMC 직접 열기는 자동 확인 화면으로 반환되어 논문 전체를 읽었다고 기록하지 않는다. [연구를 수행한 Harvard HSCRB의 설명](https://hscrb.harvard.edu/news/the-real-reason-behind-goosebumps/)도 확인했다.

논문은 털집·털세움근·교감신경의 연결과 털세움을 다룬다. 주된 실험은 생쥐이며, 사람 사진에서 생리적 원인이나 질환을 판별하는 근거로 사용하지 않는다. 시각 데이터는 국소 모낭 요철, 피부에 붙은 서 있는 털, 주변 피부의 연속성으로 한정했다. 모공의 구멍/평면 질감과 별도 축 `bm_skin_piloerection`을 만들었다. 이 구분은 관찰 목적의 저작 추론이며 모든 돌기를 생리적 소름이라고 판정하는 규칙이 아니다.

## S49 — 체모 굵기·길이·색의 분리

[DermNet, Hair loss](https://dermnetnz.org/topics/hair-loss), dermatologist Amanda Oakley, updated May 2023. 모발 성장 설명을 직접 확인했다. 문서는 vellus와 terminal hair의 상대적인 굵기·길이·색 차이를 기술한다. `bm_body_hair_fiber`에 fine/short/lightly pigmented와 coarse/longer/pigmented 검색 의역을 추가했다. 해당 이미지의 나이·성별·호르몬·병력은 털의 형태로 추정하지 않는다.

## S50 — Goosebump-like appearance의 반례

[DermNet, Keratosis pilaris](https://dermnetnz.org/topics/keratosis-pilaris), Sarah Winter and Richard Motley, March 2022. 모낭 각질과 소름처럼 보이는 피부 돌기에 관한 설명을 직접 확인했다. 비슷한 돌기만으로 털세움이나 질환을 확정할 수 없다는 가까운 반례에 사용했다. 질환 진단이나 치료 정보는 후보의 positive text에 넣지 않았다.

## 범위

이 추가 조사는 소름 축 1개와 의역 12가족의 근거를 보완한다. 최초 47개 출처의 읽기 수준이나 연구 제안 70사례의 미실행 상태를 소급해서 바꾸지 않는다. 원문·core·초기 팩·개선 팩·프롬프트·이미지·판정은 별도 증거다. 같은 core에서 후보 노출이 늘었다고 픽셀 품질 개선까지 입증했다고 주장하지 않는다.
