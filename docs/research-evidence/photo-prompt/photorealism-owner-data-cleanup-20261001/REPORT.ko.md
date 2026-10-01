# 사진 현실감 데이터의 이미지 영역 소유 관계 검토

19개 행을 조사하고 3개 owner 수정을 고정해 검증했다. 최종적으로 JPEG 압축 흔적 한 행만 채택하고, 노이즈와 필름 grain/print 행은 정확한 baseline으로 복원했다.

- 채택한 JPEG owner는 압축된 이미지의 고대비 경계다. 파일·화면·재게시 맥락, 경계 부근의 약한 ringing/blocking, 주요 동작 가독성 조건은 그대로다.
- 노이즈의 이미지/장면 영역 불일치는 남아 있다. 제안 벡터에서 물리적인 가루 표면 near-miss가 9→8위로 가까워져 보류했다.
- 필름의 picture/print 두 층 구분도 원문상 타당한 수정이었다. 다만 grain+print 양성이 구체적인 두 층 의무를 갖지 않은 일반 grain 후보 뒤로 1→2위로 밀리고, print가 필요 없는 lexical 양성도 무관한 halation 뒤로 4→5위가 됐다. 먼지 near-miss의 3→4위 하락은 여전히 top5 노출이어서 이 손실을 보상하지 못했다.

보류는 원래 데이터 문제를 부정하는 결정이 아니다. 결과를 본 뒤 문구나 질의를 다시 조정하지 않았고, 원안 결과·미사용 벡터·모든 비용 시도를 보존했다.

## 고정된 검증 범위

새로 작성한 7개 진단은 양성 4개와 물리 표면 near-miss 3개다. 별도로 이전 pixel-rubric 입력 12개를 문자열과 원래 not_run/unscored 상태 그대로 보존해 탐색적 검색 진단으로 사용했다. 이 12개 중 provenance나 이름 바꾸기 오용을 다루는 문구에는 관련 optional 후보가 검색되는 것이 타당할 수 있다. 높은 순위를 금지 조건으로 바꾸거나 이미지 평가가 실행됐다고 해석하지 않는다.

채택안에서 7개 주 진단의 두 검색 방식 target 순위와 상위 5개 ID 순서는 모두 baseline과 같다. 역사적 q14의 상위 순서만 달라지며, 전체 이미지 pixel mosaic 문구에서 JPEG 후보가 2→3위로 내려간다. 일반화·실제 이미지 품질 개선이나 모든 의미 혼동 해소를 주장하지 않는다.

## 출처와 index

최종 데이터 변경은 JPEG relation object 한 값과 그 소스에 대한 versioned maintenance_ref다. 18개 행은 그대로다. 원래 maintenance 기록을 덮어쓰지 않고 새 기록에 동일한 coverage/제한과 이 한 변경의 revision을 기록했다. 두 hash 연결이 모두 일치하며 원래 기록의 바이트도 유지됐다.

10,174개 문서 중 새 벡터는 1개, 정확한 baseline 재사용은 10,173개다. 처음 생성한 3개 문서 벡터는 전부 보존했다. 독립 read-only 검토가 114개 baseline/proposal/accepted 결과 행과 실제 소스·index·BM25·cache·binding을 재현했다. 추가 API 호출은 없었다.

## 테스트와 비용

DATA/background/photorealism 154개와 effect/bundle/profile 40개, 총 194개가 통과했다. Dictionary metadata와 1,385개 visual profile/3,305개 exact-term index도 검증했다. 기존 role/projection 11개 중 10개 통과, 지역 평판 fixture 1개는 기존 실패다. social-recognition 후보가 요구 top6 대신 7위에 있으며, 세 fixture 질의의 top12 ID 순서는 baseline과 채택안이 같다. 기대값을 낮추지 않았다. 전체 저장소 green으로 표현하지 않는다.

22개 입력이 각각 한 번 성공했다. 입력은 5,707 UTF-8 bytes이며 비용의 추가 보수적 상한은 $0.0360448, 추적 누적 상한은 $1.1272192다. 미채택 벡터 비용도 포함된다. 청구서 실측이 아니며 별도 upstream 사용액은 대조하지 않았다.

최신 main pull 뒤 검사와 정상 push/remote 확인은 별도 publication 단계다. 원래 dense-final/lexical-final은 3개 제안 결과이며 실제 채택 결과는 dense-accepted/lexical-accepted다. 해당 publication checkout에서 replay_acceptance.py를 실행하면 API 없이 세 상태와 index를 검증한다.
