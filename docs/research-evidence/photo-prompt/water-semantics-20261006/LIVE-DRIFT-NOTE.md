# 공유 checkout의 기준점 차이

이 연구가 만든 authored 산출물은 `docs/research-evidence/photo-prompt/water-semantics-20261006/` 안에 있다. 활성 자산·index·생성 경로·사용자 작업을 수정하거나 되돌리지 않았다.

최초 `CHECKOUT-SNAPSHOT.json`은 live asset JSON·Python script·skill/maintenance 문서 124개를 기록했다. 최종 비교에서 같은 HEAD 아래 일부 자산·index·source manifest·code가 다른 bytes로 바뀌었고 신규 appearance source가 관찰됐다. 다른 연구 폴더·테스트·shard도 추가되어 Git status 전체 무변경은 성립하지 않는다. 이 비교만으로 변경 주체를 특정할 수 없으며 그 파일들을 reset·stash·삭제하지 않는다.

처음 관찰한 차이는 기존 파일 17개 변경과 신규 live 파일 2개였고, 최신 열거 결과는 [PRESERVATION-CHECK.json](PRESERVATION-CHECK.json)에 있다. `audited_live_inputs_unchanged: false`는 공유 원본 drift를 뜻하며, 이번 물 데이터가 활성 채택되었다는 증거가 아니다.

최신 원본 catalog를 다시 읽고 기존 ID 연결·현행 compiler 형식을 재확인했다. [EXISTING-DATA-CATALOG.json](EXISTING-DATA-CATALOG.json)은 각 source의 실제 읽은 bytes 해시를 보존한다. 조사 완료 뒤에도 checkout이 변할 수 있으므로 구현 시작 시 최신 snapshot·owner·property·manifest를 새로 고정해야 한다.

[VALIDATION.json](VALIDATION.json)의 PASS는 연구 파일·coverage·ID 연결·relation binding·compiler 형식에 한정된다. 최초 snapshot과 최신 원본의 동등성, 실제 후보팩·이미지 개선·다른 작업의 성공을 의미하지 않는다.
