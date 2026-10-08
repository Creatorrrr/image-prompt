# 조사 중 관찰된 저장소 변경

조사 시작 HEAD는 `629bf4a88e1f1f524d177d67c09615a7fdb4f89d`였고, 최종 점검에서는 `30fc97a84fb3c8a7863adf0b8b60010dce73b444`의 VEL 확장 커밋이 관찰됐다.

이 연구 작업은 Git mutation·active source 수정·canonical index build를 실행하지 않았다. 시작 때 존재한 asset JSON 109개 중 108개와 기존 dirty direct file 281개 중 280개는 SHA-256이 같았다. 변경된 한 파일은 semantic index이며 현재 HEAD의 Git blob과도 다르다. 커밋 전환과 작업 index 변경을 각각 관찰된 외부 상태로 기록하고 그대로 보존했다. 그 index의 작성자·원인 또는 어느 chat이 수정했는지는 확인하지 않았다.

현재 compiler·candidate semantics·contracts·source manifest Python 파일은 두 HEAD와 현재 작업 파일 사이에서 동일한 bytes였다. 조사 시작의 working-code hash를 따로 저장하지 않았으므로 시간 전체의 동일성을 과도하게 주장하지 않는다. draft-shape 검증은 실행 시점의 구현에 대한 제한된 결과이며 새 runtime index 전체나 최신 검색 품질의 검증은 아니다.

untracked directory 34개의 전체 하위 파일 bytes까지 비교한 것은 아니다. 모든 기존 파일이 한 바이트도 바뀌지 않았다고 주장하지 않으며, 이번 작성 도구의 출력은 research 폴더로 한정했다.

자세한 비교는 [LIVE-DRIFT.json](LIVE-DRIFT.json)과 [PRESERVATION-CHECK.json](PRESERVATION-CHECK.json)에 있다.
