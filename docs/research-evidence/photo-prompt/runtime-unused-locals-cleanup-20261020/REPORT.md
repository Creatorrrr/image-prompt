# 사진 스킬 미사용 지역 변수 정리 및 F841 검사 확대

커밋된 코드의 미사용 지역 변수 17건을 정리했다. 이 계산에만 쓰이던 `audit_authorial_pack.provenance`, `audit_moe_render_review.visual_required_gates` 두 선행 계산도 함께 제거했다. 단순 계산·과거 분기 플래그를 제거하고, 후보 ID 열거/변환, typed assertion 해석, frozen policy 검증 호출과 `craft.pop()` 두 호출의 순서·인자는 보존했다. 검토한 대입문 외 AST가 같은지 작업본과 HEAD 투영본에서 각각 확인했다.

Ruff는 0.15.1을 유지하고 F401·F841을 검사한다. 자동 수정 허용은 F401뿐이며 F841은 수동 검토한다. CI workflow/job ID, 재노출 23개, 로딩 순서용 줄 예외와 해시 봉인 worker의 F401 예외는 유지했다. 새 F841 위반을 수정 파일 네 곳에 각각 삽입하면 모두 검출한다. 커밋할 코드의 Ruff 결과는 17→0건이며 기존 미커밋 코드의 `source_key` 한 건은 수정·stage·예외 처리하지 않았다. 작업본은 18→1건이므로 전체 작업본 Ruff 성공으로 보고하지 않는다. 원격 CI는 이번 커밋을 push하지 않아 실행하지 않았고 실제 커밋 투영본에서 CI와 같은 명령을 검증했다.

작업본의 변경 전후 각각 관련 테스트 86개가 모두 PASS했다. HEAD 소스만 투영한 대조군/수정군은 각각 86개 검사에서 같은 기존 실패 35건(서브테스트 포함), 오류 0건이며 새 회귀가 없다. 기존 contextual axis/source-effects 수정에 의존하는 실패를 해결하려고 사용자 미커밋 작업을 함께 커밋하거나 테스트를 완화하지 않았다. 임시 모델 경로가 symlink여서 거부된 최초 검증 시도는 남겼고, 독립 APFS 모델 복사본으로 고쳐 최종 검사를 완료했다. 검사는 네트워크·원본 쓰기·원본 scripts/precore fallback·torch 로딩을 차단했다. 전체 suite 성공을 뜻하지 않는다.

원래 설치 선택을 사용한 임시 후보 소스와 적용 후 원본 진입점에서 각각 issued-view→retrieve→view→compose-audit→deliver 다섯 명령이 PASS했다. texture 목표는 공통 positive 풀 18,180 CID/18,182 RID, BM25F 1회·로컬 cosine 1회이며 기존 query vector를 재사용하고 원래 결과를 유지했다. 원래 두 목표 composition/lighting의 전체 점수·순위와 H/native receipt·구성 감사도 재현했다. 파생 native public view의 대조/수정 출력은 같고, archive 전체 순위 450개와 전용 검사 17개가 재현됐다. 과거 품질 HOLD는 그대로다. 원래 봉인 코드의 신규 발행이나 검색 품질 개선 판정을 수행하지 않았다.

기존 161,150경로와 CURRENT 168개를 보호 목록으로 고정했다. 원본에 적용하기 전 범위 밖 미추적 `candidate-p0-stage-20261020/primary_gold_choices.py` 한 파일의 동시 변경을 감지했다(3,964→3,994 bytes). 이 작업은 해당 파일에 쓰지 않았다. 이전 내용은 해시 기록만 있어 바이트 단위 원본 복원을 입증하지 않으며, 현재 내용을 별도 보관하고 그대로 유지한다. 최초 strict FAIL과 고정 기준선을 보존하고 이 한 파일의 정확한 새 해시만 별도 검토한 뒤 후속 전체 보존 검사를 수행했다. 이 예외를 다른 경로나 임의의 변경으로 확대하지 않았다. 대상 파일의 기존 dirty patch는 HEAD 투영과 작업본 사이에 동일하며, 다른 worktree와 CURRENT·후보·색인·해시 봉인 worker는 변경하지 않았다. 원시 검증 로그와 복구본은 저장소 밖 private evidence 경로에 있다.

이번 source/config/docs만 별도로 stage한다. Gemini·새 임베딩 추론·이미지 API·원래 CURRENT 쓰기·운영 발행·push는 없다. 이 검증은 선택한 운영/과거 재현 경로에 한정한다.
