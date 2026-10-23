# 기존 코퍼스 대조

읽기 시점 authored 후보 20,871개, binding 15,839개에서 네 지정 positive field(en/ko/phrase_en/phrase_ko)의 부분 문자열을 조사했다. 이 수는 설치본의 검색 가능한 문서 수가 아니다. manifest와 읽은 module은 감사 도중 해시가 안정적이었다.

24개 기존 레코드와 연결된 binding 24개를 전체 스냅샷으로 보존했다. 어휘 hit는 원문을 찾기 위한 수단이다. 0건은 의미 부재, 순위 또는 신규 생성 필요성을 증명하지 않는다.

| 대상 | 기존 소스의 실제 의미 | 제안 |
|---|---|---|
| 트렌치 b077/6907/8dcd | 견장·벨트 / 상부 플랩 / 벨트-고리-앞판 각각 별개, 뒤 둘은 human 전제와 구체적 appearance 효과 | 각각 완전 의미를 재사용 검토. 전체 조립 초안에 대한 세 소스 자동 합집합 금지 |
| 노치 e0df / 숄 a7a1 | 칼라의 단차 / 재킷 개구를 따르는 둥근 선, lapel property 효과 | reuse 검토. peak/peaked 어휘 0건을 피크 라펠 부재로 해석하지 않음 |
| 콘트라포스토 aa7f | 지지 다리·이완 다리·골반/어깨 대응 경사, pose 효과 | 완전 의미 reuse 우선. S자 윤곽과 구분 |
| 돌아보기 2c85 / 시점 aa81 | over-the-shoulder look은 action 효과, viewpoint는 camera 효과와 human/animal 전제 | 배우 머리 회전과 카메라 role 혼동 방지. 원래 효과를 무시한 binding만 추가하지 않음 |
| 이어피스 5bd8/a9f6/122f/09f0 | 통신 cue / surveillance earpiece / 입 옆까지 가는 마이크 붐 / 귀 옆에 수화부를 듦 | 네 가지를 동의어 처리하지 않음. 새 손끝-착용 장치 관계는 실제 기존 장치와 소유자 조건부터 검토 |
| 반사 509b | 암시된 표적을 거울로 관찰, human 및 action 효과 | 거울과 실제 표적의 경계를 보완할 수 있으나 보이지 않던 표적을 임의 추가할 권한은 없음 |
| 스리피스 1fc7 | 재킷 아래 별도 조끼, suit_ensemble 효과 | 원래 전체 실현이 맞는 경우 reuse 우선 |
| 새틴 6c14 | 같은 슬립 드레스의 곡선 주름과 넓은 하이라이트, garment_type/material/drape 효과 | 일반 직물 광택으로 축약하여 쓰지 않음. 의복 종류 효과와 잠긴 속성을 함께 검토 |
| 슬릭백 c799 / 스터블 b0c7 | 젖은 듯한 슬릭백 / 가벼운 스터블 | 첫 소스의 wet-look 추가 효과를 보존. 모든 슬릭백의 완전 동의어가 아님 |
| 슬립 드레스 4556/051c/bc0d | 드롭웨이스트 새틴 / 티셔츠 위 90년대 레이어 / 레이스 연결과 별도 카디건 | 일반 슬립 드레스 초안에 부수 레이어를 자동 강제하지 않음 |
| 장갑 d85d | 영문 to leave no trace, 한국어 흔적을 남기지 않는, effects는 빈 배열 | 비가시 성능과 보이는 착용을 분리하는 refine 검토. 연구 중 원문은 수정하지 않음 |
| 첩보 eace | cold-war espionage realism, setting 효과, world의 contextual binding | 장르·시대 문맥 유지. 장비나 의복의 완전 시각 후보로 취급하지 않음 |
| 피팅 f1c6 | 접촉·국소 천 변화·도달/지지, production_activity/photography_workflow/garment_fitting 전제 | 일상 커프 정리로 전제 제거 금지. 별도 자기 손-반대 커프 실현 비교 |
| 청삼 f89d | 사선 앞개구와 매듭 여밈이라는 특정 변형 | 해당 관계만 reuse 검토. 모든 치파오·시대·핏으로 일반화하지 않음 |

각 표의 ID는 가독성을 위한 축약이다. 실제 전체 CID, source file, 원문·조건·효과·provenance·binding과 해시는 [existing-source-mapping.json](existing-source-mapping.json)에 있다.

검토 중 발견한 차이를 근거 없이 운영 데이터의 오류로 확정하지 않는다. 원래의 목적과 downstream 사용을 확인한 뒤 수정 또는 별도 대안으로 반영한다. 특히 native qualification, 설치본 노출, 최종 선택 가능성은 이 소스 감사로 검증되지 않았다.
