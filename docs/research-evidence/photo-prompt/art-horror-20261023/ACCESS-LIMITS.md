# 출처 접근 범위와 제한

## 원 대화

`read_thread`가 단일 답변을 20,000자에서 잘라 반환했다. 앞부분의 완전한 표 행 137개와 부분 행 하나를 보존했다. 이후 사용자의 요청에 따라 **로그인된 크롬에서 정확한 대화 URL과 제목을 확인하고 마지막 문단까지 읽었다.** 15개 표의 데이터 행 수는 `13,12,15,13,11,12,16,13,11,16,11,11,12,7,6`이다.

T138 Subjective Sound의 설명을 완성하고 T139–T154, 영화 12편, 미술 사례 7개, 조합 6개를 복원했다. 원 대화에서 만든 조합 표현은 정식 하위 장르로 승격하지 않는다. [보완 전사](browser_supplement.py), [보완 메타데이터](browser-supplement.json), [원래 잘린 반환](conversation-excerpt.json)을 함께 보존한다. 잘린 반환 자체는 역사적 원본으로 유지하므로 그 안의 `source_truncated=true`는 현재 연구 범위가 미복원이라는 뜻이 아니다.

첫 in-app browser는 로그인 화면으로 이동했다. 크롬의 다른 작업과 조작이 겹쳐 초기에 다른 대화가 표시된 시도들은 원 대화 증거로 사용하지 않았다. 최종 확인은 제목 `Art Horror 용어 설명`, URL `6adaf50e-502c-83ee-894e-85601ea7cd1c`, 표 15개, 여섯 조합과 마지막 문단이 함께 확인된 결과만 사용했다.

## 외부 문헌

- Criterion Channel 직접 열기는 지역 제한 화면으로 이동했다. 공식 검색 색인에 노출된 기획 설명만 사용했고 영화 스트리밍이나 전체 영화를 열람하지 않았다.
- Tate의 비체 미술·이미래 전시 안내 직접 접근은 403/timeout이었다. 검색에서 제시된 `up.railway.app` 복제 호스트는 공식 출처로 채택하지 않았다. 비체는 Columbia의 Kristeva 설명, 설치는 공식 Hyundai Artlab으로 교차 확인했다.
- Tate 쪽 색인 복제문은 설치의 사슬을 54개, Hyundai Artlab 본문은 49개로 제시한다. 이 연구는 해당 수치를 후보/필수 gate로 채택하지 않는다. 두 설명을 같은 작품의 고정 수량으로 섞지 않는다.
- Routledge의 Harrington/Creed는 공식 검색 색인의 출판사 설명·주제 목록을 읽었다. 직접 본문 열기는 실패했다. 책 전체를 읽었다는 의미가 아니다.
- Mulvey는 공식 Screen 서지와 DOI를 확인했다. 다른 재인쇄 페이지는 405, 대학 PDF는 추출 본문이 비어 있었다. 상세 논증을 검증한 것으로 처리하지 않는다.
- Yale의 과거 film-analysis 주소 네 개는 접근할 수 없었다. 촬영·조명·롱테이크는 Columbia Film Language Glossary를 사용했다.
- Oklahoma State의 음향 교재는 공식 색인에 노출된 문장을 사용했고 직접 열기는 403이었다.
- informe는 MIT Press의 Bois 서지 포인터만 확인했다. Bataille 원전과 Bois/Krauss 저서를 직접 검토하기 전 상세 이론 데이터 승인은 보류한다.
- Hamburg narratology 페이지는 timeout이었다. 그 페이지를 읽었다고 기록하거나 source ledger에 검증 출처로 추가하지 않았다.

## 증거 수준

[sources.json](sources.json)의 각 `read_scope`와 `limit`가 기준이다. 직접 읽은 기관 글, 공식 색인의 본문/설명, 서지 포인터는 서로 다르다. 원 대화의 키워드 전수 보존과 개별 정의의 원전 전수 검증 역시 다르다.

작품 목록의 일부는 원 대화 참조를 보존한 수준이다. [reference-work-mapping.json](reference-work-mapping.json)에 각 작품의 후속 확인 여부를 적었다. 실제 영화 전체, 퍼포먼스 전체, 원작 픽셀을 이번에 감상·검증하지 않았다. 새 후보의 검색·선택·native 자격·이미지 생성·사용자 수용도 아직 검증하지 않았다.
