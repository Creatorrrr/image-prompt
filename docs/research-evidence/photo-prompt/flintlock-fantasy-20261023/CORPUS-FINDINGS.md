# 기존 후보 원문 감사

작업 트리 20,341개 source와 15,120개 binding을 읽었다. 지정 어휘 44개 일치 중 13개를 수동 검토했다. 특정 용어가 없다고 전체 의미가 없다고 단정하지 않으며 실제 검색은 실행하지 않았다.

| CID | 결정 | 카드 | 이유 |
|---|---|---|---|
| `cand_db7d982e859c5f52aa75982e7e263f8a` | context | A01, B01 | EN은 일반 총기 정물이나 embedding에는 현대 슬라이드/회전탄창/receiver가 있다. 수석식 정답으로 취급하지 않는다. 기능성도 원문 외형만으로 추정하지 않는다. |
| `cand_2a4606c052a65cb194a4dbf7ae04447d` | context | A07, B01 | 현대 소총 구조라는 명시를 보존한다. rifle과 flintlock의 축을 구분하는 현대 control이며 역사 총기 부족을 채우는 재사용 대상이 아니다. |
| `cand_9c0d3821b9ae5cc49781a59f278b4f29` | refine | D01 | 기존 포좌-흉벽-포문 정렬을 재사용 검토한다. KO 축약을 보완하고 cannon의 신규 owner와 effects를 현행 계약에 맞게 직접 검토한다. |
| `cand_6bd1ad0fcf775ccaa867d438086d2182` | reuse | C07 | 낡은 삼각모 소품만 재사용 검토 가능하다. pirate tag는 착용자의 직업·시대·국가 증거가 아니다. human guard를 유지한다. |
| `cand_f365853663525b9e852396e14eae05c8` | reuse | C08 | 왕실 문장 견장의 원래 전체 뜻이 요청과 맞을 때만 재사용한다. 장교 계급·충성·고증의 자동 증거로 삼지 않는다. |
| `cand_e55f66332e315f20bf90ddbb61f8d36b` | reuse | C08 | 재킷 어깨의 장식 견장과 부착부를 부품 수준으로 검토한다. 수석식 시대와 계급은 별도 명시가 필요하다. |
| `cand_748ceab940f952b9830b04d8b619219e` | reuse | B08 | 세이버라는 물건 유형은 재사용 검토 가능하다. 별도 곡률·칼집·소유자·접촉·역사 모델은 이 CID에서 얻지 못한다. |
| `cand_00e1c881614a51ed8f149a9a4fc0b416` | context | C06 | 흉갑과 러프가 함께 있는 완전 bundle이다. 러프를 삭제해 나폴레옹 흉갑기병으로 재명명하지 않는다. 흉갑기병은 별도 실현을 제안한다. |
| `cand_9debbd3052f958bdb327be49da46722c` | context | C08 | 왕실/공주 문맥과 실제 subject_applicability를 포함한다. 일반 장교 제복 또는 현지 회사군으로 무단 변환하지 않는다. |
| `cand_ce196d11c0855603851e504849247bec` | reuse | B08 | 칼집 속 의장용 소품이라는 전체 한정이 맞을 때만 재사용한다. 실제 전투 무기 또는 뽑힌 검으로 바꾸지 않는다. |
| `cand_42d2b29291fe52db93a6bf09617d266e` | refine | D05, D06 | EN은 본체 부착 보루/해자 건너 분리된 외보/입구 차폐를 갖지만 KO는 제목형 축약이다. 번역·embedding·effect 범위를 검토하고 이 전체 관계를 보존한다. |
| `cand_033e7d080d73a070221b915a72412fea` | context | B04 | bayonet은 카메라 렌즈 마운트다. 총검 정답이 아닌 다의어 control이다. |
| `cand_c79a072f53df533cb9a46d96e9ced116` | reuse | A03 | 외부 wheel이 있는 휠록 전시다. alias의 플린트록은 비교 경계일 뿐 positive flintlock 격발부가 아니다. 전시/총열 아래 위치의 전체 의미를 유지하고 원전 도판으로 재검토한다. |

`existing-source-mapping.json`에 원본 전체/conditions/effects/bindings/record hash를 저장했다. 어휘만 일치한 나머지는 모두 defer이다. 파일명 재사용은 현재 source 재사용과 구별하며, actual CID/RID·native 자격은 이번 연구 초안에 부여하지 않았다.
