# 기존 데이터와의 대조

현재 source manifest의 전체 53개 모듈을 JSON으로 읽었다. 후보 19,179개, 긍정 18,945개, diagnostic 234개다. `CORPUS-LEXICAL-AUDIT.json`에는 모듈별 hash·지정 field·패턴·실제 일치 CID를 보존했다. `existing-source-mapping.json`에는 24개 선택 CID의 전체 레코드와 binding snapshot을 보존했다. 이 자료는 lexical/content inspection이며 실제 BM25F·cosine·RRF 검색 실행이 아니다.

다음 판단은 원문의 이웃성에 대한 계획 제안이다. 전체 source의 native proof·role eligibility·branch·effect 권한을 승인하지 않았다. 구현 시 스냅샷과 현행 source hash가 같은지부터 확인한다.

|기존 source|연결|제안과 한계|
|---|---|---|
|`cand_69aad1c674b64b97968b2f8673853038`|D01/D02/D03|티포트 몸·주둥이·손잡이·뚜껑은 재사용 이웃. 컵·손·그릇 전달을 이미 포함했다고 세지 않음|
|`cand_e42be4c368ba8e143d743e35db88b881`|D02|도구–용기–받침의 실제 접촉과 기존 소유자 조건 보존. 사람 손이 지지하는 동작으로 바꾸면 의미 변화|
|`cand_83206043de15574488e68c0dca2cd729`|A08/D06|성인 사용자가 필수 생활품 기능 마모를 수선하는 의미가 가까움. 소매·패치·숫돌은 새 저술 필요|
|`cand_32f534773ab55b75bbcf885e4b56e012`|D06/D12|무대 기술자와 갭모에 대비 맥락이 붙음. 역할·대비·반환을 삭제하고 일반 돌봄으로 relabel하지 않음|
|`cand_74c968440a0e56b1907e181579c565b4`|B01/D06|로코코 패니어의 재사용 부품은 구체적 의복 구조. 건축 부재 재사용은 별도 소유자·재료 관계|
|`cand_c49cab39f4375620ad188e535af021de`|E01/A02|에테르 카트리지 교체·하류 흐름 확인·인계의 순서가 있음. 한 프레임으로 전체 절차 성공을 채점하지 않음|
|`cand_52b17aedc71a5b608e903aec505bccc1`|E03/E07|배급 토큰·필터·검사표·줄의 소품 묶음. 제공자·저울·음식·수신 통의 연결은 별도|
|`cand_cfb0f5034e965ac8bf9404e74062ab39`|E02/E03|공정·정당성의 상황 서술. 이 표현을 가시성 gate로 승격하지 않음|
|`cand_b1dff106e3f85371bc1ad2beb7760e22`|E10|장례지도사 역할은 선언으로 사용 가능. 의복·얼굴이 직업을 입증하지 않음|
|`cand_6c405a8b0ca75bc2a211e7ce949809c7`|B07/H03|유골 저장 구획과 통로의 형태 이웃. 살아 있는 상인·애도 행동·경제는 별도|
|`cand_5c55276f88ca543f99e39f23eb3a95bc`|C01|기질·가지줄·국소 결절의 기존 형태. 급수 호스·편익·기억·지능은 새 사실로 추가하지 않음|
|`cand_4a860cd5b3415010a963025a16272a66`|C08|숙주 경계의 균류 부착. 피해·감염·동의의 진단은 하지 않음|
|`cand_253d14b94e0b5b13b3fb9a41eab3d9c6` / `cand_b99c238a660a5456a449f51519650678`|B10|종이 위 밑글/덧글. 도시 벽과 간판의 재태깅은 단순 확장이 아님|
|`cand_0bb2983bbfaa5b19bbcd8b811ae3a8a1`|H06/H11|섭취자·음식 출처를 분리하는 diagnostic. 긍정 선택 source로 전환하지 않음|

영어 `molt`의 단순 부분문자열은 molten rock를, `ration`은 calibration을 잡았다. 한국어 `수선`은 조석 수선도 잡는다. 이 세 CID를 false-friend 대조로 보존했으며 보강 전후 검색 평가의 경계 사례에 포함했다. 최종 audit는 영어 단어 경계를 적용했지만 전체 숫자는 여전히 의미 정답 수가 아니다.

지정 field·패턴에서 hospitality/communal-food/molting/spolia가 0이라는 것은 해당 표기의 미일치다. 다른 표현·동의어·구조로 이미 존재할 수 있다. 새 데이터가 필요한지는 84개 초안마다 전체 원문을 대조한 후 결정한다. 현재 24개 mapping만으로 전체 corpus의 의미 중복을 제거했다고 하지 않는다.

`RUNTIME-OBSERVATION.json`은 config가 선택하는 installed source manifest의 같은 후보 수를 확인했다. 작업 search와 installed native search의 선언된 corpus fingerprint는 별도로 기록한다. **같은 개수는 동일한 source/index/code closure의 증거가 아니다.** installed metadata를 읽은 사실과 전체 설치 무결성 검증·실제 검색 결과는 구분한다.
