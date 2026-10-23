# 현재 데이터 진단

2026-10-23 관찰. manifest에 연결된 81개 모듈, 후보 레코드 20,341개, binding 15,120개, catalog 슬롯 149개를 확인했다. 후보에는 visual option뿐 아니라 profile/bundle/diagnostic도 포함되므로 전부를 독립 장면 20,341개로 해석하면 안 된다. 원문과 모듈 해시는 [corpus-audit.json](corpus-audit.json), 선택한 기존 원문·조건·효과·binding은 [existing-source-snapshots.json](existing-source-snapshots.json)에 있다.

## 문자열 출현의 관찰

실제 후보 `content.en`, `ko`, `definition`, `aliases`에 한정한 검사다. 중첩 realization의 모든 필드나 전체 의미를 평가한 것은 아니다.

|검색 문자열|포함 레코드|해석|
|---|---:|---|
|mirror|129|반사가 풍부하지만 소유자·매체·대응 상태가 서로 다름|
|negative space|26|신체 사이의 빈 모양과 공간적 부재의 구도는 별도|
|uncanny|20|일반 분위기 문장과 구체 관계가 함께 있음|
|abject|13|문맥용 진단과 시각적 실현이 섞여 있음|
|tableau|10|촬영 맥락 태그만 있는 레코드는 완결 장면과 다름|
|chiaroscuro / tenebris|6 / 3|명암 외관과 완결 조명 source를 구분할 필요|
|reliquary / vanitas|5 / 3|내용물·용기·도상·정물의 구성 의미를 확인할 필요|
|mise en abyme|5|그림·모형·중첩 단계가 다른 후보를 재사용 검토 가능|
|gynaehorror / acousmatic|1 / 1|주로 문맥 구분이며 양성 시각 자격의 증거가 아님|
|haptic / arthouse / art horror / butoh / institutional critique|0|지정 본문 필드의 문자열 부재. 의미 부재나 데이터 추가 필요의 독립 근거는 아님|

## 기존 source 15개와의 대조

다음 CID는 모두 현재 실제 원문에서 확인했다. ‘재사용 우선’은 검토 순서이며 동일 의미 판정이나 native 승인이 아니다. 새 문장에 추가된 성인 조건·재료 유사성·새 endpoint·다른 물체까지 기존 source가 지지한다고 간주하지 않는다.

|새 카드|기존 CID|기존 의미와 새 의미의 차이·권장 판단|
|---|---|---|
|V01|`cand_62b2336d58395b0688f96fd1cc511216`|오른손의 펴짐/주먹 반사 불일치. 성인 조건과 전체 거울 경계까지 한영 원문을 대조|
|V07|`cand_adedeca2e608587e8585c7112575611a`|경계 테두리에 붙는 막은 있음. 새 외피 소유자·구멍은 원문 추가 조건|
|V08|`cand_251dffe09ca15e9c93647415b13a41d3`|의지·소켓·양쪽 표면의 접합. 착용자와 adult qualifier를 따로 검토|
|V11|`cand_d16fd394d2ef5dc39c5b0b51b446560c`|새틴 주름의 하이라이트다. 젖은 섬유 경계로 덮어쓰지 않음|
|V16|`cand_d721153af85f50f0be0896d11bde19d8`|다른 성인의 거울상을 보는 관찰자다. 벽 틈 관찰과는 다른 구조|
|V20|`cand_4f9aa7915bdd53f5b9a974059bebf7d7`|같은 방의 창·탁자·모형 대응. 우선 재사용 검토|
|V25|`cand_95c0893727b35d5c97537ec39a454aa2`|투명 창과 내부 뼈 파편. bone과 bone-like, reliquary와 reliquary-shaped의 차이를 유지|
|V26|`cand_9d1213229e6757e18c9bc2472067997c`|왕관·상한 과일·책 조합. 악기·해골·꺼진 초 조합과 별도|
|V31|`cand_87bfef4aae77597ca226eec19c993f93`|암부 속 얼굴·손의 하이라이트. 새 카드의 몸 연결 가시성은 추가 검토|
|V32|`cand_577175d2238f5266825a75fefb755d7f`|문틀 경계의 차가운/따뜻한 조명. 녹색/빨강이라는 정확한 색으로 자동 확대하지 않음|
|V35|`cand_d43d9575faec53a48e8c35b5c60a6487`|바닥과 이어진 뼈 같은 아치. 새 카드의 부드러운 관은 기존 원문에서 빌릴 수 없음|
|V42|`cand_1e0f80a818b552e1a664c716445637b9`|성인 모형의 팔·패드 끈·침대 틀. 무대 장치와 물리적 인간/모형의 차이를 검토|
|V43|`cand_c73c675fcbb95197afe210ad76644853`|상해 분장과 피부 사이 이음선. intact·stage lighting 등 추가 qualifier를 따로 검토|
|V46|`cand_2da0ba86c4aa5e309a69093d3304e36c`|찢긴 냅킨과 붉은 액체. 소매·팔·벽 균열과 별도 장면|
|V50|`cand_25b9386ea05954b8b4eb94ee648fbebd`|방 안 같은 방 그림의 중첩. 나선 무늬의 타일/그림 반복과 다른 구조|

조사 결과는 기존 source를 최대한 살리면서 실제 추가 의미를 구별하는 방향이다. 64개 초안 모두를 새 CID로 등록하거나, 비슷한 영어 문장을 갖는 기존 후보에 모두 alias만 붙이는 방식은 권하지 않는다.

## 슬롯의 반영

새 카드의 `subject_relation`, `medium_relation` 등은 연구 차원의 이름이며 실제 catalog 슬롯 ID가 아니다. [slot-mapping.json](slot-mapping.json)에 현재 존재하는 ID와의 대안을 기록했다. 실제 binding을 만들 때는 한 source의 완결 의미와 선택 역할을 개별 검토한다. 새 runtime 슬롯은 제안하지 않는다.

## 이 진단이 입증하지 않는 것

원문을 읽은 사실은 source qualification, installed index 노출, 후보 선택, 프롬프트 채택, 이미지 품질의 증거가 아니다. 모듈 원문 스냅샷의 조건과 효과를 살펴보는 후속 native 검토가 필요하다. 동시 수정에 따른 source drift는 [VALIDATION.json](VALIDATION.json)의 관찰을 따른다.
