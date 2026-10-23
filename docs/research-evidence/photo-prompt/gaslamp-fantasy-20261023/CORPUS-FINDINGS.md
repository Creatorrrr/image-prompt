# 기존 후보와 반영 판단

아래는 manifest에 등록된 source에 대한 지정 field 어휘 조사와 30개 full-record/binding snapshot을 바탕으로 한 계획이다. 운영 검색·순위·의미 전체의 부재 증거가 아니다.

| 카드 | 어휘 조회 | 일치 수 | 제안 | 판단 | snapshot CID |
|---|---|---:|---|---|---|
| G00 | gaslamp | 3 | context | 세 hit 모두 gaslighting 관련이다. 원문 gaslamp 장르와 일치한 근거로 쓰지 않는다. | cand_a9c35cceb8a853d283039da02e60b607, cand_736be7dfa29d55be954c8448bb83e96b |
| G03 | gas_infrastructure | 0 | new_if_no_semantic_equivalent | 지정 어휘 0 hit. lamp 일반 후보 및 광원/하우징 관계를 추가 확인한 뒤 신규 판단. |  |
| G12 | hansom | 0 | new_if_no_semantic_equivalent | 지정 어휘 0 hit. 일반 마차와 이륜/후방 마부의 완전 의미 중복을 먼저 조사. |  |
| G27 | crinoline | 1 | refine | 기존 CID의 silhouette와 owner relation을 재사용. 내부 후프/허리 지지는 별도 선택 변형이며 기존 실루엣에 강제하지 않는다. | cand_11f0f0fd765e50ae85e0d5ad684d52a5 |
| G28 | bustle | 5 | refine | 기존 뒤 볼륨 owner를 유지하고 착용자 방향·정면 대비·영어 bustle 동음이의어 대조를 강화. | cand_3671de101025584d832f8dc031a5ec61, cand_d5ad48669b645106a7acedb08380f70e |
| G33 | chatelaine | 2 | refine | 기존 두 CID의 허리 고리/체인 문장을 보존. 같은 허리 소유자라는 native 연결을 검토하고 누락된 동일-owner 조건만 보완. | cand_1685b60c50b2553fa2574bd57942b0d4, cand_d9c46193feaa5072a676b5cdf50088df |
| G37 | mourning_hair | 4 | reuse | 기존 locket CID는 모발·힌지·체인과 비애도 대조까지 보유. 동의어만 늘린 복제 후보를 만들지 않는다. | cand_4375105f2a13508f89054e385d6c9c41, cand_d4b28ffad10e5ac59533573616b38b84 |
| G22 | calling_dance_card | 2 | new_if_no_semantic_equivalent | 기존 playing-card/시그넷-token은 방문 명함/무도회 카드의 의미상 동등물이 아니다. | cand_c166357edcc95f4ba658c74763fc8f08, cand_cf70267511b852b9a22f23c3fb2ef101 |
| G18 | conservatory | 2 | new_if_no_semantic_equivalent | 기존 온실 CID는 성인과 빗장을 한 프레임에 함께 요구한다. 이를 단순 온실로 축소 재해석하지 않고 중립 온실 후보의 존재를 추가 확인. | cand_27f3b5743f96520dba3514ee5bda0a94, cand_316522c32c815f7b804490596151ced5 |
| G40 | planchette | 0 | new_if_no_semantic_equivalent | 지정 어휘 0 hit. 펜·작은 판·바퀴·종이 접촉을 generic writing과 비교 후 신규/재사용 선택. |  |
| G42 | spirit_photography | 5 | refine_or_new | double-exposure 스튜디오/매체와 인화물 안의 두 상은 역할이 다르다. 매체/상/공간 경계를 검토. | cand_fe0d7e0899065deeba38fa09679ac551, cand_951436f4a40051f1bae4e99a445b5bf2 |
| G43 | pepper_ghost | 0 | new_if_no_semantic_equivalent | 지정 어휘 0 hit. 일반 reflection 관계를 재사용할 수 있으나 원상-판-상 전체 의미가 동등한지 확인. |  |
| G56 | faerie_contract | 1 | refine | 기존 양측-한 문서 CID의 완전 의미를 재사용. effects에 여러 차원/각 소유자의 포괄적 property가 있어 실제 변화하는 owner/property로 수작업 축소 검토; 법·동의 효력은 context. | cand_53801d41b5e55a64b1da60297c42198c |
| G67 | automaton | 18 | refine_or_reuse | 18 lexical hit는 충분성 지표가 아니다. 새 clockpunk 모듈과 관절-손-출력 관계의 full-source 동등성을 비교하여 중복을 줄인다. | cand_13b604cb96315410b10cbeb79aedfbee, cand_522fa4df296f59db9a1dc282d7ec8f4c |
| G69 | galvanism | 0 | new_if_no_semantic_equivalent | 지정 어휘 0 hit. 의료/실험장치 source의 전극/회로를 검토하고 가상 표본의 주장을 분리. |  |
| G70 | phrenology | 0 | defer_specific_artifact | 독립 물건 사진/본문 접근 부족. 추론 금지 context는 우선 보존하고 구체 도표는 실물 검증 후 채택. |  |
| G72 | laudanum | 0 | new_if_no_semantic_equivalent | 사각병과 마개는 generic bottle 재사용 가능. 라벨·내용물·섭취·중독은 서로 별도 역할로 검토. |  |
| G80 | adult_context | 0 | context | 어휘 0 hit를 외형 부재로 해석하지 않는다. 성적 직업/지향/경제관계는 body/wardrobe 태그로 변환하지 않는다. |  |

source와 설치본, 이미지가 각각 다를 수 있다. 운영 기능의 개선은 후속 독립 검색·native 자격·이미지 gate로 별도 확인한다.
