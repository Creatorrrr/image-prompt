case-05 초기 세대 독립 검증 결과입니다. 실제 인간이 직접 사진 주제를 요청한 사례가 아니라 coordinator가 만든 격리 QA 주제입니다.

| 판단 | 결과 | 검증 범위 |
| --- | --- | --- |
| 기술 감사 | PASS | 공식 composed audit 실패 0건, 경고 6건 |
| 연결 정확성 | PASS | 후보 64개·관련 노드 49개 query, 고유 경로 126개·원본 참조 169개 대조 |
| 최신성·거부 동작 | PASS | 실제 require-current 성공, 손상 report 및 다른 root 거부 |
| 요청·의미 보존 | PASS | 초기 영어 baseline bytes 그대로 보존, 후보/visual concept 채택 0개 |
| 작품 판단 | PARTIAL | 접사의 재료·조명·초점 관계는 일관됨; 실제 이미지 미검증 |
| optional 후보의 의미 범위 | PARTIAL | 명시적 adult receiver가 필요한 eligible 두 항목과 추가 review를 별도 기록 |

관리 report의 generation_id는 `2135faf8f2451eac73b90c447edbd496545d20d974c158f44ec67d98e9107f2a`이며 실제 pack receipt와 같습니다. 번들 경로는 `meaning_support: not_inferred`, `profile_activation: independent_request_evidence_only`를 유지합니다. 미연결 후보 51개도 원본 선언과 일치했으며 강제 연결이나 채택을 하지 않았습니다. 부조 번들은 두 component를 갖는 optional 전체 계약이고, 연관 프로필은 자동 hard obligation으로 활성화되지 않았습니다.

카메라의 방향·높이는 요청에 지정되지 않아 unprescribed/open과 빈 evidence를 유지했습니다. 낮은 옆빛은 광원의 높이·방향입니다. 사람 없음으로 sensual/fetish 실효값은 0이며 explicit_nonsexual을 임의로 true로 바꾸지 않았습니다. 거친 비늘 면과 틈의 시각적 효과는 후보를 보기 전 작성한 required assertion이 담당합니다.

초기 catalog_path의 절대 경로를 계약 문자열로, 영어 people 제외를 literal 요청의 사람은 없음.으로 표기한 기술 사본을 사용했습니다. 원본·교정 이유·해시·DATA 접근 순서는 schema-corrections.json과 command-evidence.ndjson에 보존했습니다. 독립 checker에서 record-only hash와 단일 원본 비교 가정을 각각 공식 entity recipe 및 명시된 context extension 합성 비교로 교정한 기록도 남겼습니다. 실제 DATA와 관리 도구를 수정하지 않았습니다.

초기 노출 중 pr_fixed_surveillance_observation_candidate와 hr_mockumentary_evidence_display는 원문에 adult가 명시됩니다. formal_biwu_courtyard_platform은 비무 주인공/관전자 문맥의 추가 review입니다. hand_finishing_mechanical_watch_bridges는 human/object/product가 모두 허용된 마감 후보이므로 이름만으로 인물 receiver 결함으로 판정하지 않았습니다. 몸·손·얼굴 전제와 인간 전용 전제는 human-receiver-observations.json의 16행에서 구분했습니다. 이는 전체 DATA 의미 검토 완료를 뜻하지 않습니다.

최종 영어 프롬프트:

A macro photograph of a pine cone centers on the gaps between its scales and their rough woody surfaces. The scales are dry, with fibrous ridges and slightly chipped edges interrupting their repeated pattern. Low side light grazes across the scale relief, bringing raised ridges into brightness while the crevices hold narrow shadows. A close crop lets the overlapping scales form an irregular layered rhythm. The central cluster is crisply resolved; neighboring layers soften gently enough to retain their shapes. The cone rests against a plain charcoal-brown background. Muted russet and umber tones keep attention on the transition from illuminated surface to shaded gap.

영어 문장은 독립 baseline과 동일합니다. 중앙 초점과 가까운 겹침의 흐림은 표면의 깊이를 남기고, 낮은 측광은 융기와 틈의 차이를 연결합니다. 이 설계가 실제로 선명하고 보기 좋은 사진이 되는지는 아직 판단할 수 없습니다. 이미지 픽셀·사용자 수용은 NOT_VERIFIED입니다. API·이미지·네트워크 호출은 하지 않았습니다.

실행 명령의 argv·시각·종료값·stdout/stderr 해시는 command-evidence.ndjson에 있습니다. 대표 명령은 generate-pack-schema-corrected-local-lexical, composed-audit, build-maintenance-report, query-relief-current, query-all-exposed-bidirectional, query-relief-profile-reverse, query-relief-bundle, query-macro-lens-unlinked, reject-damaged-report, reject-wrong-source-root, independent-source-check-complete-record입니다. 최초 검증 실패 및 checker 교정 기록도 삭제하지 않았습니다.
