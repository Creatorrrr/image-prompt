# 현재 코퍼스 진단과 통합 판단

이 진단은 후보 19,006개, binding 12,879개, manifest 49개 모듈을 읽은 스냅샷이다. 읽는 도중 해당 모듈 해시는 바뀌지 않았다. 프로젝트의 다른 작업은 계속 진행 중이므로 구현 시점의 최신 상태와 동일하다고 가정하지 않는다.

[CORPUS-LEXICAL-AUDIT.json](CORPUS-LEXICAL-AUDIT.json)은 고정한 `en`, `ko`, `definition`, `phrase_en`, `phrase_ko`, `composition_instruction`, `runtime_expression` 계열만 조사했다. aliases·모든 typed fact·검색 query embedding·현재 설치본의 검색 결과를 검증한 것이 아니다. 169/247개 매칭 0을 의미 공백 비율로 보고하지 않는다.

`focus_results`는 추가 탐색용 부분 문자열이며 관련도 순위가 아니다. `crypt`의 3건은 encrypted/cryptic 계열 오탐이다. atlas의 원 용어 진단은 영문 단어 경계를 사용한다. 두 진단의 수치를 섞지 않는다.

## 원문과 의무를 보존해야 하는 사례

아래의 판단은 실제 긍정 문장·조건·효과·역할 연결과 기록된 연구 계약을 대조한 연구 의견이다. 독립 native proof, 모든 primary field의 source-unit 승인, 실제 검색 노출이나 픽셀 합격은 아니다. 전체 레코드 18개와 연결은 [existing-source-mapping.json](existing-source-mapping.json)에 보존했다. deterministic first-two 목록이며 18개가 최적 후보라는 뜻은 아니다.

| 기존 CID | 실제 범위 | 연구안과의 관계 | 제안 |
|---|---|---|---|
| `cand_35d20354a50251a095ad689bb4cebaf1` | 살아 있는 네크로맨서와 특정 망자의 인과 상호작용; human 조건, subject effect | M01의 의식자/환영 위치는 인과 사슬 전체와 다름 | 기존 의미를 위치 묘사로 축소하지 않는다. 재사용하려면 인과 의무 전체 검토. |
| `cand_5e09c39e63e4510eb8be49e45f65beb4` | operator → 특정 망자 anchor → 국소 반응 → 결과의 프로파일 | 묘지·원·색 빛은 대체 불가라는 기존 경계가 있음 | 새 후보가 아니라 질의/관계 표현 보강을 우선 검토. 넓은 necromancy 라벨의 자동 활성화 여부도 확인. |
| `cand_0c0b3f8e71025fe0909e56400013b882` | chiaroscuro의 다섯 관찰 관계 프로파일 | F01은 한 얼굴의 명암 실현으로 더 좁음 | 프로파일을 1개 광원/볼 묘사로 덮어쓰지 않는다. 완전 프로파일과 작은 선택안을 분리. |
| `cand_de12f7d606275a50bf973a3735501680` | 금박·거울·벨벳·대리석을 분리하는 바로크 조명 | 특정 재질·전체 위계가 추가됨 | 단순 명암용 동의어로 재사용하지 않는다. 재질/배경 락과 함께 검토. |
| `cand_e1e04727a9a65c279a41504f95642b04` | 어둠 우세, 고립된 빛, 보호된 국소 세부 등 다섯 관계 | F02와 가까우나 기존 의무가 더 구체적 | 원 프로파일 전체를 보존한 재사용을 먼저 검토. 낮은 노출과의 음성 평가 추가. |
| `cand_6c405a8b0ca75bc2a211e7ce949809c7` | 반복 보관 감실·뼈·그 사이 통로; Ossuary/Necropolis가 함께 표기 | D04의 보관과 D01의 묘 건축 거리는 다른 규모/기능 | 기존 항목은 완전한 선택안으로 유지. 제목만 보고 도시 묘역을 통과시키지 않는다. |
| `cand_a304b049381f5fb587505b2a22f212f9` | 빈 opening, 관절, 양 접지, 사물 상호작용이 보이는 속 빈 living armor 프로파일 | M07의 생체 착용 갑옷과 다른 존재 구조 | hollow/animated와 worn/organic-interface를 별도 분기. 기존 빈 내부 의무를 삭제하지 않는다. |
| `cand_8ed5a9486be65af9b7a3e3d39ca477fb` | 벽/유기 opening/석재로 이어지는 conduit | M08의 내피/유연 경첩과 부분 중첩 | 새 경첩 관계가 필요한지 검토하고 단순 재명명 중복을 피한다. |
| `cand_d40afe99e20559b7b6cd132206b30030` | 마녀/마법사의 마도서와 촛불; human 조건 | O05의 열린 도식 책에는 촛불이 필수 아님 | 촛불/인물 조건을 삭제해서 일반 책 후보로 넓히지 않는다. |
| `cand_e355eac6ef4750c7b60a90e531cefbcf` | 열린 책·낡은 페이지·잠긴 보관 공간, 특정 금서 명칭의 원전 문맥 | O05와 겹치지만 보관 장소·특정 서명 의미가 추가됨 | 한정 전체가 맞으면 재사용; 일반 grimoire의 자동 잠금/특정 신화화 금지. |
| `cand_3d076f2067dc5ccdb652525ed05caba9` | 은빛 블론드의 고스 머리색; human/도메인 조건 | Gothic 문학·건축과 다른 맥락 | 의미상 오류가 아니라 문맥 분리 대상. 장르만으로 머리색 변경 허용 금지. |
| `cand_8a5c372460635eeba54f3196e99657c0` | 검은 레이스 고스 돌 드레스, attire contextual binding | 고딕 성당의 구조 의미를 주지 않음 | 복식 후보를 장르/건축 direct 역할로 승격하지 않는다. |
| `cand_1110ec4c710b585badc550be3a4780a3` | 종의 보이는 clapper 변위와 떨어진 손 | 의식 소품의 위치는 있으나 소리/자율 작동은 미입증 | 소리·원인 비추론 회귀에 재사용 검토. |
| `cand_22fce7248cc35990b2b431cbbeb8cac0` | 성인 의식자, 정해진 의례 중심, 경계 표시 물체 | M01의 망자·질문·응답은 아직 별개 | 경계와 인물 관계를 재사용하되 망자/성공을 태그로 끼워 넣지 않는다. |
| `cand_d276d699cec651e0b78ccab0ff1572e9` | 어깨 근처 박쥐 날개 형태의 레이스 그림자 | M05의 동일 신체 그림자 불일치와 다름 | 단순 shadow hit를 빙의/소유 불일치 후보로 채택하지 않는다. |
| `cand_04f09d75bbf4503aa6b7af7b1f17520c` | 밤의 재봉 작업실과 그늘 속 원단 | shadow라는 공통 어휘만 겹침 | 의미 이웃의 정답으로 사용하지 않는다. |
| `cand_39f9d62fdc6157c2bf8122b42c77a688` / `cand_1da4e4464be1571396973365076b8d82` | 암호화 하드드라이브 / 명령 입력 | crypt 부분 문자열 오탐 | 묘실 재사용 후보에서 제외. 실제 검색 실패로 확대 해석하지 않는다. |

## 원자 표현의 어휘 공백과 의미 공백 구별

지정 필드의 focus 문자열로 reliquary, gargoyle, memento mori, catacomb, body fusion, fallen paladin, death knight가 0건이었다. 의미가 다른 문장이나 다른 필드로 존재할 수 있다. 구현의 신규 판단 전에는 실제 한영 자연어 검색과 complete source를 확인한다.

living armor의 근접 의미를 추가로 조사한 [topology-neighbors.json](topology-neighbors.json)에는 3개 레코드가 있다. 둘은 일반 의복의 `torso/folds/bridge` 어휘가 겹친 오탐이고, 다음 하나는 실제 관련성이 있다.

- `cand_1e0b067ca7085a25b42b63196f074897`: 유기적으로 보이는 분절 외피가 어깨/몸통을 덮고 열린 테두리에서 **외피와 피부 사이의 틈**이 보인다. M07의 피부와 닿는 덩굴과는 다른 관계다. 유기 외피/착용자라는 공통 부분을 재사용 검토할 수 있지만, 기존 gap을 지워 접합 의미로 바꾸면 안 된다.

이 추가 탐색은 별도 시점의 고정 5개 field 결합 진단이다. 기본 18개 목록과 동일 스냅샷/정확한 순위라고 주장하지 않는다. semantic registry의 G01은 한 몸의 인접한 두 구조 상태와 연속 경계를, N07은 변형된 사람의 사지를 동료가 돕는 관계를 다루고 있어 변형/돌봄 연구의 재사용 이웃이다. 레지스트리는 실제 CID·RID·원문의 native 승인 권위가 아니다.

## working source·검색 manifest·설치본은 별도

조사 중 다른 작업에 의한 모듈/런타임 포인터 변화가 관찰됐다. 초기 파일 목록의 45 모듈과 나중 진단의 49 모듈을 같은 상태로 부르지 않는다. `BASELINE.json`은 시작점이고 corpus audit의 module hashes가 해당 진단의 기준이다.

읽기 전용 installed check는 pass였고 이미지 호출/소스 쓰기 0이었다. 그 결과는 의존성 및 recorder 계약 확인이며 연구 초안의 운영 반영이나 최신 데이터 검색 자격을 입증하지 않는다. 진단 시 검색 manifest는 `embeddinggemma2-local`, `google/embeddinggemma-2`, 768차원을 선언했다. working source 수와 검색 manifest metadata 수가 다르다는 사실만으로 고장이나 성공을 단정하지 않는다. 실제 구현에서는 exact source/index/installed generation을 함께 다시 고정한다.
