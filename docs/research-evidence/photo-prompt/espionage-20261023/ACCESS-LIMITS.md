# 접근·근거 한계

2026-10-23.

1. read_thread로 참조 대화 두 turn을 읽었다. nextCursor는 없고 각 agentMessage에는 truncated=true가 있다. 한 turn당 20,000자까지다. 파서가 추출한 완결 행은 340개, 미완결 행은 1개다. 전체 20분야 또는 외형 12절 전체 복원으로 보고하지 않는다.
2. 브라우저로 원 대화 URL을 열었지만 ‘잠시만 기다리십시오…’ 대기 화면만 관찰했다. 본문, 잘린 뒷부분 또는 원 대화의 인용 링크 목록은 확보하지 못했다. 우회하지 않았고 임시 탭은 닫았다.
3. 이전 대화의 chatgpt-content-reference 색인은 외부 출처 URL로 복원하지 않았다. 이번 조사에서 확인한 URL만 sources.json에 기록했다.
4. S01 CIA glossary는 A-L이 포함된 첫 페이지를 읽었다. 사이트는 3페이지임을 표시한다. 현재 페이지에 보이지 않는 원 대화 용어를 CIA가 모두 정의했다고 쓰지 않는다.
5. S02/S03 MI5는 검색 발췌와 open의 문서 일부를 읽었다. 본문 위치로 재요청한 호출은 timeout이었다. 기관별 agent/officer 구분은 CIA의 자체 정의와 함께 범위를 한정한다.
6. S10 Met, S12 V&A collection은 검색 발췌 수준이다. S20 FBI는 검색 발췌와 페이지 시작부를 읽었고 본문 재요청은 timeout이었다. 해당 실물의 세부 구조나 재현 정확도는 확정하지 않았다.
7. S24 라펠 가이드는 본문 도입부와 검색 발췌를 읽었고 세부 재요청은 timeout이었다. 피크 라펠의 정확한 도판 검토는 남았다.
8. S26 CIA 연구 PDF는 검색 발췌가 있었지만 full open은 404였다. MICE의 한계를 짧게 언급한 발췌 이상의 내용을 근거로 삼지 않았다.
9. 외부 이미지 도판은 직접 pixel review하지 않았다. 박물관의 텍스트·alt description·specification 확인과 도판의 실제 관찰을 구분한다. 재료, 제품 performance, 역사 표본의 디테일을 추정으로 승인하지 않는다.
10. 138개 카드의 완전 장면·관계·gate는 연구자가 저술한 시각 제안이다. source_refs는 개념군/관습 지원이며 모든 카드의 모든 단어가 개별 원전으로 증명되었다는 뜻이 아니다. 외형 미연결 65개와 10개 detail/specimen hold를 남겼다.
11. 기존 코퍼스의 literal substring 감사는 실제 BM25F/embedding 검색이 아니다. ‘spy’가 wispy와 겹치는 식의 어휘 오탐을 의미적 존재/부재의 근거로 쓰지 않는다. 24개 스냅샷과 현재 소스의 차이는 후속 구현 전에 재확인해야 한다.
12. 실행한 runtime check는 의존성·설치 recorder의 읽기 전용 확인이다. 이 연구 데이터의 등록, 검색 노출, source qualification, prompt 채택, 이미지 성공 또는 사용자 수용을 증명하지 않는다.
