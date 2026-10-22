# 기존 코퍼스 조사와 항목별 처리

연구 시점 HEAD와 파일 해시는 [BASELINE.json](BASELINE.json), 67모듈의 읽기 시점 해시는 [CORPUS-AUDIT.json](CORPUS-AUDIT.json)에 있다. 후보 19,801개·연결 14,246개를 읽는 동안 조사 대상 manifest/module의 해시 변화는 없었다. 별도의 작업 종료 시점 변화는 [PRESERVATION.json](PRESERVATION.json)에 기록한다.

## 어휘 검사 결과의 해석

검사한 긍정 필드는 `en`, `ko`, `definition`, `phrase_en`, `phrase_ko`, `composition_instruction`, `runtime_expression`이다. 태그·aliases·research metadata·negative를 검색 근거로 사용하지 않았다. 45개 focus 중 정확 어휘 0건은 20개였다. **이 결과는 BM25F/cosine 순위나 의미 부재를 뜻하지 않는다.** 후보마다 모든 조건과 실제 선택 branch를 다시 읽어야 한다.

`airlock`, `depressurization`, `scrubber`, `hull breach`, `generation ship`, `cryopod`, `stasis`, `bioship`, `alien ocean`, `parasitoid`, `ovipositor`, `artificial womb` 등의 정확 어휘가 0이었다. 추가 검사에서도 `air-lock`, `decompression`, `pressure hatch`, `cabin pressure`, `cryogenic`, `suspended animation`, `oviposition`, `에어록`, `동면`은 0이었다. 다만 다른 성분으로 같은 뜻을 담은 원문이 있을 가능성은 남는다.

[SYNONYM-NEIGHBORS.json](SYNONYM-NEIGHBORS.json)은 보조 18개 표현의 원문 일부를 기록한다. 이 보조 검사는 부분문자열을 사용하므로 `air lock`이 `hair lock`에서 1건 잡혔다. 이를 에어록 근거로 취급하지 않았다. `진공`은 진공 포장·구도 후보에서, `군체`는 산호에서, `umbilical`은 발사대 정비에서 잡혔다. 현재 단어 수가 장면 의미의 충분함을 보장하지 않는 구체적인 예다.

## 실제 원문에서 확인한 경계

아래는 전체 승인 결과가 아닌 **연구 단계의 처리 권고**다. exact CID는 [existing-source-snapshots.json](existing-source-snapshots.json)의 전체 원문·조건·효과·연결과 대조할 수 있다. 그 밖의 본문까지 native 승인한 것은 아니다.

|기존 CID / 의미|확인한 성분·조건·효과|권고와 새 카드의 관계|
|---|---|---|
|`cand_49652d62206e522fb28ad2b5d4c2bc43` 미세중력 내부|정거장 랙·지지 없는 부유·방향 다양성·레일/구속 제어의 네 성분을 요구하는 authored-components 계약|reuse 우선. V16을 단순 동의어 신규 후보로 만들지 않음; 실제 전체 gate와 효과를 유지|
|`cand_7b74028598cd503abdcd5256886084e5` EVA 기술자|압력복·배낭·부착 안전줄; subject 효과|정상 EVA는 reuse. V15의 이탈과 동시에 채택하면 모순; 자유 줄 끝은 별도 실현|
|`cand_cd9dbfd011485f92beeaf7f8a708ab69` EVA 미학|선체 외부·구속·도구 접촉; style 효과와 aesthetic_trend 연결의 documentary 등 deny|코어 장면과 binding 조건을 함께 검토. 소재가 documentary처럼 보인다는 이유로 guard를 무시하지 않음|
|`cand_a7226f4763845d2691a0f7a635fea1c0` sky-dock tether|부력 셀·바람·밸러스트·계류 장력; `punk_skypunk` primary 조건|우주 EVA로 전용하지 않음. 단어 tether만 공유|
|`cand_7e3a0e42226b591c9deeffb66b6e3f34` derelict space|낡고 방치된 일반 공간; setting 효과; space_condition에 domain deny 존재|노후 표면은 reuse 검토. 우주선의 도킹/압력 경계가 빠져 V18은 별도 관계 검토|
|`cand_33e0096e59a5582a8844388034c8833a` ghost ship|rigging·갑판·불투명 선체·유령성 단절·수면/항적 등을 요구하는 수상 선박 구조|빈 자동 우주선으로 재해석하지 않음. V19는 다른 의미이므로 독립 필요|
|`cand_8ed5a9486be65af9b7a3e3d39ca477fb` living architecture|벽 안의 막·건축면으로 이어지는 도관; 생명/지성/소화 미입증|기존 접점은 reuse/refine. V28은 우주선의 구조 지지 관계가 추가되는지 검토|
|`cand_4c2a218da12358c2ab9e8ae53951adc4` 기생 접점|숙주·별도 부착체·부착 기관; 피해/영양/편익은 미확정|V31 reuse 우선. V32의 출현 형태와 최종 숙주 사망의 시간 조건은 분리|
|`cand_ee6b62e77e9357b69cd2ae19b63a3677` 배태 외형|숙주·내부 타원체·막; 임신·기생·발생 원인·동의 미확정|V44와 중복 비교 후 reuse/refine. 강제 임신/동의 판단으로 승격 금지|
|`cand_610afa98d8c8552a99d827ad83f47f01` hive mind 실현|복수 몸·가는 연결·같은 방향; composition/concept 효과; 군체 의식은 설정|연결/정렬 재료는 reuse 가능하지만 공유 의식·swarm intelligence와 동의어화하지 않음|
|`cand_82127c4d15035b52bf706e79eed0bfde` 군집 행동|`for_any: robot, object`; action 효과|로봇 군집 관계로 유지. 생물 군체에 조건을 지워 적용하지 않음|
|`cand_e86ead0041ee5c1787e0259e037a2b94` 귀환 격리실|`infinite_flow_return_quarantine_scene` primary 조건; setting 효과|조건 유지. V35–V37의 우주 오염 방향·경계 통과는 독립 의미/조건 검토|
|`cand_2df4095d20fa5b53a99b8af64432f4e8` 검역 담당자|일반 공중보건 인물; subject 효과; KO도 영어 문장|우주 보호복/표본 경로의 근거로 확장 금지. 번역 보완은 별도 scoped diff|
|`cand_313088e0690a56688ea5e89ee2577058` 성적 생체기계|유기 형상·기계·연속 접합; 성적 상징 문맥과 material/concept 효과|전체 의미를 검토. 일반 생체선에 자동 성적 문맥을 옮기지 않고 V28과 분리|
|`cand_ffd66c197f525d9393ccf212a2785e2e` 서비스 안드로이드|일반 synthetic 주체; subject 효과|주체 재사용 검토. V48의 열린 외피·손 연결은 독립적인 시각 보완이지 악의/의식 근거가 아님|
|`cand_a7f1e74071375d87a59a7181fe761301` 인지/정보 위험 구분|context-only; 빈 효과·연결 없음|D14와 context 재사용/보완. V53의 독자/매개체를 위험의 실증으로 만들지 않음|
|`cand_d1d1920147855b41a40559368ae95ea0` 블랙홀 실현|그림자·원반·렌즈상; concept/lighting 효과; 원반은 선택형|V55 reuse 우선. 특이점·지평선의 실제 관측이나 보편 원반 의무와 분리|
|`cand_c82b8a00a8545749b587291103f35e9d`, `cand_860e002f8f095131ad59cd5285e4fd69` 시간 반복|둘 다 문맥 진단·빈 효과; 복도 반복은 시간 반복의 증거가 아님|D16 context 보존. 시퀀스가 필요하면 별도 형식으로 작성|
|`cand_678e4c31c333544ba24b9d3d4f7772ea`, `cand_1d5cd5da16b95bfe95d6e0887ee03dad` cassette|카세트 연대/레이블 노동·던전 신스 물품; 후자는 primary 조건|V63의 제어계 양식과 단어만 공유. source 범위 유지|
|`cand_40412df852a1502d9eefc44e366601a5`, `cand_50c34ab35e5a59a6ba557d1476ff78d8` CRT|보존 재료 또는 text-world archive; 후자는 primary 조건|CRT만으로 전체 함교를 재사용하지 않음; 필요한 독립 기능 배치 검토|
|`cand_16a369703de2528fbf8ceee0faa7539e`, `cand_2e56b944d56f50e3af7ac1a4adf95eaa` 식인 구분|먹는 대상의 정체·종·관계·제의/성적 의미를 분리하는 진단|D18 재사용. 일반 육식 장면을 식인 증거로 채택하지 않음|
|`cand_45636926015a56baac3360fe3cb94584`, `cand_a5c1093b16de5e8b94e9f87b41087dc2` 진공 포장|object/packaging 조건과 action/composition 효과|우주 진공과 다의어 분리; 기존 포장 의미·조건을 보존|

현재 lexical 자료만으로 실제 상위 검색 결과에 위 후보가 나오는지, 설치본에 동일 원문이 들어 있는지는 확정하지 않았다. 소스 스냅샷·현재 체크아웃·봉인 설치본은 서로 다른 증거다. 검색 평가와 적용 전에 정확한 generation을 고정해야 한다.
