# 기존 코퍼스와의 비교

조사 스냅샷은 `CORPUS-LEXICAL-AUDIT.json`의 파일 해시를 기준으로 한다. 첫 검사에서 19,559개 고유 후보, 13,777개 binding, 61개 manifest 모듈을 읽었다. 별도의 시작 BASELINE에서는 모듈이 59개였다. 동시 작업이 있으므로 실제 구현 전에 반드시 재기준화한다. 검사 자체의 모듈 읽기 전후 해시 변화는 없었다. 최신 재실행 수치는 `SUMMARY.json`을 우선한다.

## 어구 진단의 결과와 한계

`content.en / ko / definition / aliases` 네 필드만 검사했다. 영어 어구의 알파벳 경계를 사용하며 slash·쉼표·한글 가운데점 대안을 명시적으로 검사했다. 출처·긴 연구 메타데이터·application contract·생성 인덱스 텍스트는 제외했다. 181개 용어 중 130개가 매칭 0이었다. 이 결과는 **실제 hybrid 검색·인덱스 검색·의미 적합도 평가가 아니다**.

세부 probe에서 `surgical drape / catheter / ventilator / dehiscence / fistula / retractor`는 0, `suture`는 1, `organoid`는 2, `hospital`은 7, `specimen`은 35, `consent`는 23이었다. 철자·영어 형태가 다르거나 다른 단위에 분산된 의미는 빠질 수 있다. 반대로 alias·definition에만 있는 단어가 실제 선택 문장에 없는 경우도 있다.

## 실제 원문·조건·효과·binding을 읽은 비교

[existing-source-mapping.json](existing-source-mapping.json)에 원본 전체와 owner 파일·hash·binding을 보존했다. 아래 판단은 연구 시점의 채택 제안이며 native 승인이 아니다.

| 기존 CID | 원래 의미·역할 | 이번 카드와의 차이·제안 |
|---|---|---|
| `cand_6ae44ec9028b5eb39009f3e3bd91a8ba` | 허구 조직 이음선 양쪽을 잇는 고리·봉합, 양 끝 접점. `anatomical_connection` direct. body geometry/appearance 효과 | D16과 매우 가깝다. **reuse 우선**. 닫힌 피부선·수·가시 범위가 기존 전체 의미와 맞는지 검토한다. W01의 중앙 열개·시간 이력까지 포함하지 않는다. |
| `cand_3a07312de26c59f2890147fc6dab3ad1` | 경계가 있는 배양 용기 속 작은 3차원 조직, 용기 테두리·스케일. object structure/contact point direct | L01의 기반으로 **reuse 우선**. 여러 구조·밀리미터 눈금은 기존 원문에 없는 추가 제약이므로 별도 refine/new 또는 요청 고유 요소로 처리한다. |
| `cand_1fb6cf35a25b581bb4279d4b37156b9e` | 조직 구성체 부피 안의 상호 연결된 관로망 | alias의 organoid 매칭이 L01의 용기·눈금을 충족하지 않는다. 내부 관로가 필요한 장면에서만 재사용 검토. W03 누공·D04 외부 배액으로 등치하지 않는다. |
| `cand_61edeb3d2827505fb7262b5ad8e0747b` | 상자 앞 원형 포트에 붙은 긴 장갑 두 개, 상자 안 시료 | L05와 인접하나 장갑이 포트에 붙은 glovebox와 사람이 일반 장갑을 끼고 함 안에 손을 둔 상황은 다르다. 요청의 장치 유형을 먼저 정하고 재사용/신규를 결정한다. |
| `cand_97990b7bb11e5a04bb81ee6d75fa3983` | 투명 용기 안 받침의 불규칙 물체, 벽과의 빈 간격 | D12의 액면·잠김·뚜껑을 충족하지 않는다. 액체가 없는 받침 표본이면 reuse, 액체 속 표본이면 다른 완전 실현 검토. |
| `cand_32a4b68635a352c4b78cd8ed16798d47` | 깨끗한 임상 복도, 빈 휠체어, 열린 문과 닫힌 프라이버시 커튼. location/prop placement direct | A03의 두 문·전실, E07의 환자·문 사이 가림과 다르다. 휠체어·복도·커튼을 몰래 추가하는 재사용은 요청의 수·배경 lock을 바꾼다. |
| `cand_1c02d63adeb3516db3d1afc30a715103` | 병원 기록실의 유리 접수창. location direct | 제도적 공간에 reuse 가능. E03의 서류 가림·D11의 코드 불일치·실제 기록 조작을 제공하지 않는다. |
| `cand_da97514b5a605ad69f59193096d5ec86` | 의료 장치가 있는 방·출구·가시 제어장치. situation context/narrative clue contextual | 의료시설 경계의 기반 후보. 실제 감금·퇴원 거부·직원의 악의와 구별한 기존 contextual 역할을 유지한다. |
| `cand_e6e861838dfd51258634d2ab10772105` | 열린 구속 장치 옆 시설 경계를 지나는 가상 인물. narrative clue contextual | specimen 어구가 있어도 표본병 후보가 아니다. E01의 닿지 않는 호출기·E02의 팔 고정점을 충족하지 않는다. |
| `cand_591f5358b318561a910a08fed8209810` | 병상·노인·정지한 군중을 의식 상실·불사와 동일시하지 않는 diagnostic 경계 | X05와 재사용 가능성이 있는 문맥 경계다. positive 역할로 승격하지 않는다. |
| `cand_2b5d709794a1506d8941839a4b44d951` | adult 조건의 흰 가운 코스튬. attire context contextual | E08과 인접하지만 성인 두 명·스튜디오·소품 의자는 없다. 의료복만으로 페티시·동의·실제 치료를 생성하지 않는다. |
| `cand_2cbc3b8844544efeb5751150830f7d8a` | 같은 성인의 손등과 얼굴의 국소 연령 외형 차이, human/adult 조건 | medical 단어는 원인 단정을 막는 문맥에 있다. 이를 성형수술·질병·이식 설명의 긍정 후보로 취급하면 안 된다. |

## 초기 채택 방향

D16·L01은 재사용을 먼저 검토한다. 수술포의 가림(D01), 배액·주입·호흡의 서로 다른 경로(D04–D08), 코드 불일치(D11), 상처·단면 도식(W01–W09)은 기존 전체 원문 비교 뒤 부족한 관계를 좁게 추가할 우선 영역이다. 모든 64개 초안을 신규 후보 64개로 등록하는 계획이 아니다.

19,559개 전체에 대한 완전한 사람 의미 검토, 실제 모든 슬롯 검색, native proof 재검증은 수행하지 않았다. 그 경계를 유지하면서 다음 단계에서 카드별로 `reuse / refine / new / context / defer`를 확정한다.
