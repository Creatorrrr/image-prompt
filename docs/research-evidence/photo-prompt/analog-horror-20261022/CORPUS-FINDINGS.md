# 현재 코퍼스와의 중복·공백·다의어 진단

원문 후보 19,801개, 직접 binding 14,246개, manifest 모듈 67개를 읽은 고정 시점 진단이다. 200개 원 용어 중 지정 필드에서 0건은 105개다. 0건은 의미 부재나 검색 실패의 증거가 아니며, 아래 표본 19개만 전체 레코드와 직접 binding을 읽어 판단했다.

필드: content의 en, ko, definition, phrase_en, phrase_ko, composition_instruction, runtime_expression과 해당 realization 필드. aliases/embedding_text/tags/negative/provenance는 이 어휘 진단에서 제외했다. 영어는 낱말 경계를 적용했고 복합 항목은 / 기준의 제한된 분리다. 대소문자·표기·철자 변형 전체를 포괄하지 않는다.

표본 선정은 focus term마다 manifest 순서의 처음 두 레코드다. 관련성 순위나 검색 top-k가 아니다. `CORPUS-LEXICAL-AUDIT.json`의 SHA와 changes_during_read를 함께 확인한다. 원문 판단은 native qualification과 다르다.

|source ID|payload owner|판단|이유|
|---|---|---|---|
|cand_87585d0a3333587a811818ca4e402216|photo_candidate_candidates_000.json|reuse_if_compatible|홈비디오 거실 설정으로만 재사용. VHS 물체·손상 신호 전체의 의미를 맡기지 않는다.|
|cand_09dc4590c0f654729757916a5a3501a7|photo_candidate_candidates_002.json|refine|VHS scanlines and color bleed를 표시 주사선/색 번짐의 독립 실현과 명시적 carrier로 분리한다.|
|cand_40412df852a1502d9eefc44e366601a5|photo_candidate_candidates_005.json|context_only|보존 표면 복합 후보다. CRT TV의 가시 구조 전체를 재사용했다고 볼 수 없다.|
|cand_50c34ab35e5a59a6ba557d1476ff78d8|photo_candidate_candidates_006.json|do_not_broaden|text_persistent_world_recovery_scene의 primary 조건을 장르 라벨로 해제하지 않는다.|
|cand_99862b5e0d11592dadf9860ad7ca36f5|photo_candidate_candidates_001.json|reject_polysemy|CME 팽창 추적은 테이프 트래킹 오류와 다른 의미다.|
|cand_4bc100634382539f95a82e78e0324be9|photo_candidate_candidates_001.json|reject_polysemy|VTuber 모션 추적 마커는 비디오 헤드 트랙 추적과 다르다.|
|cand_f5a02e6e7c965c508b537b95f8f0fda7|photo_candidate_candidates_006.json|do_not_broaden|홀로그램 표면의 선을 CRT 표시 래스터와 동일시하지 않는다.|
|cand_b98c83caa6d45d3699c2a6101f760e28|photo_candidate_candidates_007.json|do_not_broaden|피부 표면의 선은 CRT 화면 owner와 다르다.|
|cand_aceaa5a1d9465f5a9e9ded075cefeac0|photo_candidate_candidates_000.json|reuse_branch_review|물리 매체+선택적 재생 영상 dropout 분기다. 전체를 보존하며 선택한 분기의 carrier 조건을 검토한다.|
|cand_13d8065131ae521183055d14318faa36|photo_candidate_candidates_003.json|reject_polysemy|광원과 렌즈 축에 정렬된 내부 반사 고스트다. 방송 신호의 수평 윤곽 겹상으로 재태깅하지 않는다.|
|cand_d1c18ed396a658ce8b79571391acb58a|photo_candidate_liminal_dreamcore_20261022.json|context_only|장르 라벨 노출을 화면 구성요소·공포 성공의 증거로 보지 않는다.|
|cand_1ef1f3cd1ec75dc5af21ee54752d5561|photo_candidate_candidates_000.json|do_not_broaden|surveillance-state robot world 설정이다. 일반 CCTV 시점으로 robot world를 불러오지 않는다.|
|cand_7943af3de7a658c19ce18178e146322e|photo_candidate_candidates_000.json|context_only|감시 업무와 애정 부재의 설명이다. 고정 CCTV 프레임의 시각 후보를 대체하지 않는다.|
|cand_a33a937063c758f6b7d84dd735def7f2|photo_candidate_candidates_007.json|do_not_broaden|제작 도구의 timecode 메모는 화면에 삽입된 타임코드가 아니다.|
|cand_f318eda868e45d9cbd49f77d5bd00a98|photo_candidate_candidates_000.json|reject_polysemy|Low-Chroma Palette는 선택 색 영역의 낮은 채도 관계다. 비디오 색 신호 지연과 다른 의미다.|
|cand_43b61efd4d2b578496555d6ee7af9130|photo_candidate_candidates_000.json|reject_polysemy|Vivid-on-Muted는 피사체와 주변의 채도 차이다. 비디오 색 번짐과 다른 의미다.|
|cand_44b6a2aecbdc5a0cb7dffbcde8aa809c|photo_candidate_candidates_002.json|reuse_if_compatible|테마파크 애니매트로닉 subject는 재사용 가능. 기구 접점은 별도 보완한다.|
|cand_2d5565650bda5cfbb88d9d9a5876a5c9|photo_candidate_candidates_006.json|reuse_if_compatible|무대 설정은 재사용 후보이며 인형 내부·빙의·가해 사건을 뜻하지 않는다.|
|cand_8ed5a9486be65af9b7a3e3d39ca477fb|photo_candidate_cosmic_horror_20261021.json|reuse_complete_source|벽-막-능선의 기존 전체 관계를 우선 재사용. 감축·재태깅·새 동일 후보 등록은 피한다.|

## 신규 source가 필요한지 확인할 영역

color bars·teletext·spectrogram·head switching·mistracking·redaction 등의 지정 영문 focus는 이 진단에서 0건이었다. 한국어·동의어·다른 필드·기존 전체 source의 다른 관계로 구현돼 있을 수 있으므로 신규 등록의 직접 근거는 아니다. 먼저 기존 한국어/관계/장면 의미까지 검색하고 전체 source를 심사한다.

## 재사용과 정정의 기준

VHS 거실·애니매트로닉·유기 건축은 장면이 맞을 때 전체 source 재사용을 우선한다. 조건부 dropout은 이미 선언한 playback image에만 결함을 두는 분기를 보존한다. 렌즈 ghosting·solar tracking·색채 chroma의 기존 의미를 변경하지 않으며, broadcast echo·tape tracking·video color delay가 별도 공백인지 검토한다.

기존 VHS scanlines/color bleed의 혼합 표현은 분리 보완 우선순위다. 단순 설명 교체로 effects·owner·필수 의무가 달라진 사실을 숨기지 않고, 변경 전후 source와 후속 검증을 남긴다.

## 현재 결과의 한계

실제 BM25F/embedding/cosine/RRF·role exposure·선택·prompt transport·이미지·native pixels는 실행하지 않았다. source ID·내용 해시·직접 binding 전체는 existing-source-mapping.json에 있으며 코드가 재사용을 자동 승인하지 않는다.
