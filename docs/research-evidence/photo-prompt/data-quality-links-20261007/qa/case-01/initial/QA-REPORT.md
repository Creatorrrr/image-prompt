이 사례는 coordinator가 만든 합성 테스트 요청이다. 초기 세대의 독립 검증 결과는 PARTIAL이다. 관리 그래프와 현재성 검증은 통과했지만, 활 점검을 첼로 연주 동작으로 치환하는 필수 프로필 때문에 공식 composed audit는 FAIL이다. 요청 의미와 동결된 영어 문장은 바꾸지 않았다.

| 평가 | 결과 | 근거 |
|---|---|---|
| technical_audit | FAIL | 공식 composed audit가 pass하지 못했다. 유효한 frozen 입력과 feature validator는 통과했지만 활 점검과 충돌하는 필수 첼로 연주 프로필 때문에 profile evidence와 required clarification을 충족할 수 없다. baseline을 바꾸거나 허위 evidence를 작성하지 않았다. |
| graph_accuracy | PASS | 관리 그래프는 원본 JSON의 명시적 번들 참조와 일치했다. 13,931개 source reference를 독립적으로 해석했고 원본에서 재구성한 2,971개 edge가 모두 일치했다. CLI query 100개와 189개 경로 인스턴스를 원본 참조로 대조했으며, 노출 후보→프로필 경로 32개의 역방향 결과도 일치했다. |
| freshness | PASS | 초기 세대에서 --require-current query가 current_verified로 성공했다. 자신의 scratch 복사본 links.json 손상은 checksum mismatch로 거부됐고, 잘못된 root는 report authority/root differs로 거부됐다. 원본 관리 보고서는 변하지 않았다. |
| request_meaning_fidelity | FAIL | 독립 baseline과 최종 영어 문장 자체는 성인·바닷바람·공연 전·첼로 활 점검을 보존하지만 runtime hard contract는 이를 연주 중 활-현 접촉 및 왼손 운지로 바꾼다. 의미 충실한 조합이 현재 필수 계약을 만족할 수 없다. 이 실패는 그래프 경로가 아니라 일반 첼로 명칭으로 연주 프로필을 hard 활성화한 원본 activation 범위에서 발생한다. |
| artistic_quality_judgement | PARTIAL | 문장 수준에서는 정지한 활과 바람에 움직이는 머리·천의 대비, 실제 활 점검 접점, 대기 중인 악보대가 하나의 준비 장면을 만든다. 차분한 인물의 존재감과 절제된 배경을 유지한 선택은 적절하다고 판단한다. 다만 전신 지지와 활털·손끝 세부를 함께 읽히게 하는 프레이밍은 실제 이미지에서 확인해야 하고, 상투적인 해변 환경 초상 이상의 시각적 강도도 검증되지 않았다. |

공식 audit 실패는 `composed-audit.json`, 의미 충돌은 `SEMANTIC-CONFLICT.json`에 보존했다. 원본 `photo_prompt_visual_obligations.json#/profiles/114`는 일반 `cello`·`첼리스트` 명칭만으로 활-현 접촉 및 왼손 운지를 필수화한다. 활 자체를 양손으로 확인하는 이 요청의 순간과 양립하지 않는다. 필수 프로필을 억지로 적용하지 않아 audit 실패가 유지됐다.

관리 보고서는 receipt의 generation_id로 실제 CLI build했다. 노출 후보 64개와 관련 프로필 36개를 실제 CLI query했고, 50개 후보의 무연결 결과도 정상으로 보존했다. 원본 참조에서 재구성한 2,971개 edge와 query 189개 경로 인스턴스가 일치했다. 연결된 노출 후보→프로필 경로 32개는 역방향 profile query에서도 확인했다.

그래프의 번들 경유 연관은 의미 전체 충족이나 필수 활성화를 뜻하지 않는다. 부드러운 광원 후보가 공원·진료 공간 번들과 연결된다고 해서 그 후보만으로 각 공간의 모든 의미가 충족되는 것은 아니다. query 결과의 `meaning_support:not_inferred`와 `profile_activation:independent_request_evidence_only`를 확인했다. 이번 첼로 hard 활성화 충돌은 이 연관 그래프와 별개의 exact-term 프로필 적용 범위 문제다.

`--require-current`의 정상 결과는 `query-current-cello-pose.json`이다. 자신의 scratch report 복사본 손상과 잘못된 root는 실제 CLI에서 exit 1로 거부됐고 `NEGATIVE-CHECKS.json`에 기록했다. 원본 skill은 수정하지 않았으며 mutation은 scratch에서만 했다.

초기 pack: `8881de196d3625e9`

초기 runtime generation: `2135faf8f2451eac73b90c447edbd496545d20d974c158f44ec67d98e9107f2a`

영어 최종 프롬프트는 227단어 baseline과 byte-identical하다.

A photograph of an adult cellist checking a cello bow before an outdoor performance on a small wooden stage beside the sea. The cellist is seated on a plain chair, with both feet set apart on the deck. The cello rests upright between their knees, its endpin planted in a rubber stop. They hold the bow horizontally at waist height in front of the cello. Their right thumb and forefinger pause at the frog's adjustment screw while the left hand supports the wooden stick near its balance point; their gaze follows the narrow, evenly stretched ribbon of hair beneath the stick. The sea breeze lifts loose hair at their temple and pulls a dark shirt cuff away from the wrist, while their shoulders stay settled and their mouth is softly set in concentration. Two waiting chairs and a music stand with clipped sheet music sit farther along the stage, making this small preparation feel close to the first note. Soft coastal daylight grazes the cheek and open collar, with a gentle glint along the bow hair and warm amber reflections in the cello. Compose a quiet environmental portrait that keeps the seated figure, both hands, the entire bow, and the instrument's point of support readable, with the pale water receding behind them. The fine, steady line of the bow carries attention against the moving hair and cloth.

API·이미지 호출과 native pixel 검토를 수행하지 않았다. 문장 수준의 의미·장면 평가는 독립적 판단이며 실제 이미지 품질이나 사용자 수용을 검증했다는 뜻이 아니다. 수정된 세대의 재검증은 별도 증거로 남길 예정이다.
