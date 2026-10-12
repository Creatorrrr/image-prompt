# 6단계 — Native 감사·receipt·참조 무결성

감사 코드는 저장된 exact query vector와 pinned native source로 전체 허용 후보와 BM25F 통계·cosine 순위·RRF 합산·unique/role 예산을 다시 계산한다. 생성기의 선택 결과나 cache 통계를 그대로 신뢰하지 않는다. 조건 판정의 공통 의미 함수와 저수준 lexical tokenizer는 공유하되, 순위/할당 계산은 별도 구현이며 API 재호출을 하지 않는다.

v2 receipt는 native corpus/binding/catalog/index/query/algorithm 및 전체 public pack을 바인딩한다. 공급된 receipt가 런타임에 실제 발급·저장된 원본인지 대조한다. corpus 원본·역할 조건·효과·본문·후보 누락/치환·query 변경·허위 hybrid·구 v6/v1 입력을 거부한다. native reference dereference view는 v7만 읽으며, 원래 wire hash를 유지하고 공통 payload를 해소한다. 구 슬롯 배열이나 구 ID를 받아들이는 reader가 아니다.

독립 replay/변조/스키마 검사 42개 통과. 공개 CLI로 새 v7 팩·receipt를 발급하고, 파란 컵의 동결 baseline을 유지하면서 optional 후보를 모두 거절한 composition을 공개 receipt-bound auditor로 검증했다. COMPOSE-AUDIT.json의 실패 0건이다. 정확한 prompt/negative/intent/embodiment/global retrieval hash를 넣은 실제 render-request JSON의 공개 transport 감사도 실패 0건이다. 본문 변경·위조 receipt·구 pack·구 receipt의 공개 경로 거부를 별도 기록했다.

현재 worker는 현행 native source와 일치하는 generation만 감사한다. saved generation의 historical 코드를 실행하는 workflow worker와 legacy in-memory fallback을 종료했다. image provider 호출과 이미지/native pixel 검사는 이 단계에서 하지 않았다. transport 감사 통과는 이미지 의미 품질의 증거가 아니다.
