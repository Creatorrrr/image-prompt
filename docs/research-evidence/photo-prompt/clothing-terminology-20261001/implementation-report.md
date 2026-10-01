# 의류 용어의 시각 의미 데이터 통합 및 3개 독립 이미지 검증

조사 결과에서 **145개 용어군을 287개 관찰 가능한 후보와 대응 시각 프로필로 구현**했다. 294개 부품·연결 판정 게이트와 30개 선택적 조합을 추가하고 실제 검색 인덱스를 재생성했다. 독립 서브에이전트 3개가 각각 다른 복잡한 장면을 무작위로 선택하고, 첨부 초상을 사용하여 첫 이미지를 1회씩 생성했다.

이미지에서 총 24개 키워드 관찰 중 **17 PASS·7 PARTIAL**이었다. `partial_is_fail` 기준의 전체 사례 통과는 **0/3**이다. 프롬프트 및 실제 생성 입력 감사는 세 사례 모두 PASS이다. 결과 이미지와 호출 기록, 부분 반영 근거를 모두 보존했다.

기계 판독 가능한 결과는 [qualification-summary.json](qualification/qualification-summary.json), 프로필별 한정된 검증 상태는 [variant-qualification-overlay.json](qualification/variant-qualification-overlay.json)에 있다. 연구 원본은 [research-report.md](research-report.md)와 [integration-plan.md](integration-plan.md)를 유지했다.

## 데이터 반영 범위와 의미

| 모듈 | 후보·시각 프로필 수 | 주요 관찰 대상 |
|---|---:|---|
| clothing_structure | 157 | 칼라·네크라인·소매·패널·봉제선·주름·여밈·착의 관계 |
| textile_surface | 38 | 편직·직조·표면 결·반사·기모 등 보이는 표면 |
| accessory_structure | 68 | 신발의 갑피·끈 구조, 장신구 부품과 연결, 착용 액세서리 |
| traditional_clothing_detail | 24 | 한복과 기타 전통 복식의 구체적인 부품·겹침·결합 |
| 합계 | 287 | 시각 게이트 294개, 조합 30개 |

후보 슬롯은 `garment_detail` 106, `wardrobe_style` 55, `surface_material` 38, `wearable_accessory` 52, `footwear` 18, `costume_style` 18개이다. 각 모듈은 후보 extension과 시각 의무 registry extension을 한 쌍으로 갖는다.

각 항목은 영어·한국어로 구체적인 관찰 문장을 제공한다. 부품, 방향이 있는 연결 관계, 보이는 효과, 착용자와 의복의 소유 범위, 혼동 대체물 및 실패 조건을 명시한다. 예를 들어 Henley는 칼라 없는 목둘레와 짧은 가슴 단추 여밈의 관계로, bail은 펜던트 상단 고리와 체인이 그 구멍을 통과하는 관계로 작성했다. 단순한 이름 출현으로 연결 구조의 성공을 인정하지 않는다.

전체 영어 구조 문장 및 대응 한국어 문장은 정확 활성화 경로를 지원한다. Henley, raglan, bail, kimono 등의 넓은 명칭은 후보 발견에 사용하며, 특정 변형의 필수 의무를 자동으로 만들지 않는다. 간접 부품 표현으로 발견한 시각 개념은 작성자가 실제 후보팩에서 선택해야 해당 프로필 게이트가 활성화된다.

조합에는 Henley+raglan, sweetheart+princess, 고름+노리개, 기모노 겹침+오비 등 서로 양립하는 부품 관계를 묶었다. 조합이 노출되거나 선택되었다는 사실만으로 대응 시각 프로필이 모두 필수 게이트로 승격되지는 않는다. 원래 요청과 잠긴 의미를 유지하며, 바지 허리밴드를 치마에 옮기는 등의 소유 범위 전이는 기각한다.

`variant-authoring.psv`와 `integrate_research.py`에서 재현 가능한 authoring 입력 및 통합 절차를 제공한다. `runtime-integration.json`은 원본 연구 행·변형·후보·프로필·게이트·출처·파일 해시의 연결을 저장한다. 각 extension에는 별도 유지보수 sidecar를 추가했다.

## 출처의 강도와 보류 항목

통합한 287개 변형 중 75개는 출처의 해당 특징을 참고했고, 204개는 용어군 수준의 출처 맥락을 바탕으로 관찰 가능한 변형을 작성했으며, 8개는 제품 사례를 참고했다. 기하학적 표현과 검증 게이트는 작성된 데이터이다. 제품 사례의 특징을 해당 의류군 전체의 보편적인 정의나 빈도로 확대하지 않는다.

155개 연구 용어군 중 10개는 추가 1차 정의가 필요하여 런타임 후보 등록을 보류했다. CT092 피케·시어서커·테리, CT117 체인 링크, CT134 안경·시계, CT138 한복 머리장식, CT143 아시아 복식군, CT144 아바야·카프탄·토브, CT145 머리 덮개, CT146 켄테·다시키·부부, CT147 유럽·아메리카 복식군, CT150 역사적 테일러링이다.

개별 변형 3개도 보류했다. CT033-v1은 주름만으로 바이어스 재단을 입증할 수 없고, CT078-v1은 광택만으로 실크 섬유를 확정할 수 없으며, CT082-v1은 실루엣만으로 섬유 조성과 신축 성능을 확정할 수 없다. 대응하는 관찰 가능한 변형은 숨겨진 재료·기능을 주장하지 않도록 작성했다. 310개 초안 중 보류 23개를 제외한 수가 287개이다.

원본 키워드 표의 개별 미정의 702개 라벨은 기존 연구 backlog로 남아 있다. 이번 반영 단위는 명시적으로 정의한 용어군과 관찰 가능한 변형이며, 원본 표의 모든 라벨에 독립적인 완전 정의가 생긴 것으로 계산하지 않는다. 세 이미지 역시 등록된 287개 프로필 전체를 검증하지 않는다.

## 런타임 연결 및 회귀 검사

`prompt_generator.py`에 4개 후보 extension 및 4개 시각 registry extension을 연결했고, 기본 dictionary의 `required_extensions`에 후보 파일 4개를 등록했다. 용어마다 특수한 분기 알고리즘은 추가하지 않았다.

기존 registry loader가 이미 지원하던 scoped `concept_candidate` 필드와 validator의 허용 필드가 달라, 원래 editing-effects 프로필 22개에서 검증 오류가 있었다. validator를 같은 generic scope 계약에 맞췄다. 미지원 필드는 계속 거부하며, discovery를 사용하는 프로필에는 대상 dimension과 property 검증을 적용한다. 기존 editing-effects 데이터는 변경하지 않았다.

| 검증 | 결과와 한계 |
|---|---|
| 신규 의류 의미 회귀 검사 | 7개 PASS: 양언어 활성화, 넓은 명칭·부정·소유 범위 경계, 287/294 연결과 보류 항목, 30개 선택적 조합, 실제 인덱스 및 오래된 해시 거부, scoped validator, 간접 표현의 선택적 발견 |
| dictionary metadata | PASS |
| semantic index | 실제 재생성 및 검사 PASS: 10,174 entries, Gemini embedding 768d, 16 shards |
| visual profile index | 실제 재생성 및 검사 PASS: 1,385 profiles, 3,305 exact terms |
| costume·traditional 인접 검사 | 15개 method 실행. 변경 전의 6개 optional-routing fixture 불일치는 그대로 남음. 기존 schema 오류 2개는 해소 |
| broader candidate·visual·editing 검사 | 53개 method 실행. 인덱스 재생성 중 발생한 7개 hash mismatch는 최종 인덱스로 재실행하여 모두 PASS. 다른 8개 routing fixture 불일치는 변경 전 HEAD registry와 결과가 같음을 재확인 |

전체 회귀 검사를 PASS로 표기하지 않는다. 남은 인접 fixture 불일치의 기대값을 이번 변경에 맞춰 수정하지 않았다. [adjacent-baseline-comparison.json](validation/adjacent-baseline-comparison.json)과 [routing-baseline-comparison.json](validation/routing-baseline-comparison.json)에 비교 근거가 있다. 후자는 기존 registry 파일의 바이트 및 관련 routing 함수 AST가 HEAD와 같음을 확인한 뒤 프로필 추가 전후 결과를 비교했다.

새 semantic shard 세대를 활성 manifest에 연결했다. 빌더의 기본 정리로 제거된 기존 tracked 세대는 복구하여 과거 파일도 유지했다. 생성 인덱스는 수동 편집하지 않았다.

## 독립 테스트 구성

각 서브에이전트는 자신의 8개 장면 제안 중 seeded random으로 1개를 선택했다. 해당 장면, 키워드, 실패 기준, 초상 사용 범위 및 authorial core를 검색 전에 동결했다. 연구 데이터와 후보팩을 본 뒤 기준을 다시 만들거나 다른 사례의 프롬프트·이미지·판정을 참조하지 않았다. 데이터 준비 전 있었던 중립 계약 형식 수정은 별도 초기 아티팩트와 함께 보존했다.

세 에이전트 모두 `--n 1`의 실제 semantic v6 후보팩을 1개 만들었고 rule fallback은 관찰되지 않았다. 모든 native 호출은 첨부 파일을 실제 참조 경로로 전달했다. 초상에서는 보이는 얼굴과 짧은 어두운 단발·앞머리만 참고했다. 성인 생성 대상은 시나리오의 명시적 선택이며, 참조 인물의 실제 나이·신원·민족·성격·체형을 추론하지 않았다.

| 사례 | seed와 장면 | 키워드 결과 | 전체 판정 |
|---|---|---|---|
| arm-1 | 2389700930, 도서관 건축 투어를 기다리는 테일러링 의상 | 6 PASS, 2 PARTIAL | FAIL |
| arm-2 | 884213793, 도예 작업대에 그릇이 놓인 판을 옮기는 니트·카고 의상 | 5 PASS, 3 PARTIAL | FAIL |
| arm-3 | 1372153937, 역 보관함 앞의 한복·노리개 착장 | 6 PASS, 2 PARTIAL | FAIL |

### arm-1: 도서관의 구조적 테일러링

princess seam, sweetheart neckline, gigot sleeve, welt pocket, inverted box pleat, Derby의 구조는 원본 픽셀에서 확인됐다. piping은 밝은 테두리가 있으나 둥근 코드의 입체 단면이 flat binding과 구분되지 않았다. pendant bail은 작은 상단 연결부가 보이나, 열린 고리와 체인이 그 구멍을 통과하는 구조를 확인할 수 없었다.

새 ordinary 후보 3개와 대응 프로필 3개를 채택했다: CT036-v1 sweetheart, CT109-v2 펜던트, CT116-v1 bail. sweetheart와 pendant의 프로필 게이트 3개는 PASS, bail의 게이트 2개는 FAIL이다. 나머지 여섯 테스트 키워드의 별도 새 후보는 이 팩에서 미노출이며, 에이전트가 검색 전에 작성한 기준으로 계속 평가했다.

[첫 이미지](qualification/arm-1/generated_image-1.png) · [독립 판정](qualification/arm-1/pixel_review.json) · [전체 사례 보고서](qualification/arm-1/result_report.md)

### arm-2: 도예 작업실의 표면·착의·주머니 관계

Henley, cable knit, rib knit, half tuck, layer order는 확인됐다. raglan은 기울어진 편직선이 있으나 목에서 겨드랑이까지의 연속 봉제선을 케이블 패턴·소매 접힘과 분리하여 추적하기 어려웠다. cargo pocket은 패치와 덮개가 보이나 확장 거싯을 평평한 봉제 테두리와 구분하지 못했다. drawstring은 매듭과 끝단이 보이나 두 허리밴드 출구와 casing 연결이 불확정이었다.

실제 composer catalog의 새 노출은 14개이다: ordinary 5, 시각 개념 8, 조합 1. Henley+raglan 조합과 CT001-v1, CT044-v1, CT008-v1, CT057-v1 시각 개념을 채택했다. CT154-v1의 중앙 앞 tuck은 동결한 한쪽 half tuck과 달라 기각했고, lining·underskirt·wrap 후보도 채택하지 않았다. 신체·접촉 게이트 5개는 모두 PASS이며 새 프로필 게이트 4개 중 Henley·cable 2개만 PASS이다.

주 에이전트의 첫 관찰은 8 PASS였지만, 독립 에이전트가 위 세 부품 관계를 더 엄격히 보았다. 양쪽 원본 판정을 유지하고, 완전한 연결 구조가 확인되지 않은 항목을 최종 PARTIAL로 채택했다. [review-reconciliation.json](qualification/review-reconciliation.json)에 차이와 이유를 남겼다. 단추가 약 4개로 생성된 점, half tuck의 actor-relative 좌우가 초안과 반대인 점도 키워드 일반 구조 판정과 별도로 기록했다.

[첫 이미지](qualification/arm-2/first-native.png) · [독립 판정](qualification/arm-2/native_pixel_review.json) · [전체 사례 보고서](qualification/arm-2/qualification_summary.md)

### arm-3: 한복의 겹침과 장신구 연결

jeogori, dongjeong, goreum, chima, layer order, bezel setting은 확인됐다. norigae의 장식 매듭·펜던트·술은 보이지만 상부 고리가 고름 뒤에 가려져 부착 경로를 확인하지 못했다. pendant bail 역시 매듭과 펜던트 테두리 사이의 독립된 열린 고리로 식별되지 않았다. 검은 가방이 actor-left 대신 actor-right 손에 생성된 추가 불일치도 기록했다.

새 ordinary CT137-v1 노리개와 CT114-v2 베젤을 채택하고, CT114-v2 베젤 및 CT136-v1 치마 허리단 프로필을 선택했다. 두 프로필 게이트는 PASS이다. 노출된 CT014-v1은 바지에 속한 높은 허리밴드여서 치마에 전용하지 않고 기각했다. 전체 실패는 작은 연결부의 접촉·가시성 불확정과 좌우 불일치에 근거한다.

[첫 이미지](qualification/arm-3/generated-first.png) · [독립 판정](qualification/arm-3/native_pixel_review.json) · [전체 사례 요약](qualification/arm-3/qualification_summary.json)

## 무엇이 검증되었는가

실제 새 노출 표면은 시각 개념 14, ordinary 슬롯 10, 조합 1, adult-appeal augmentation 2개이다. augmentation 두 항목은 이미 등장한 source 후보의 반복 표면으로 계산한다. 채택 표면은 총 15개이다. 새 프로필 9개를 실제 선택해 해당 11개 부품 게이트를 검증했고, 프로필 단위 결과는 6 PASS·3 FAIL이다. 나머지 278개 프로필은 이미지 미검증 상태이다.

세 사례의 정식 hard gate는 총 26개로 18 PASS·8 FAIL이며 정식 리뷰 스키마 오류는 없다. 연결부의 접촉·가시성 FAIL은 원하는 관계를 판정할 수 없다는 뜻이다. 이를 신체 기형에 대한 주장으로 사용하지 않는다.

프롬프트 감사, 실제 runtime 입력 감사, 실제 생성 성공, 후보 노출·채택, 원본 픽셀 성공, 사용자 수용을 별도로 기록했다. 실제 native 호출은 총 3회, 품질 재생성과 CLI fallback은 0회이다. 사용자 수용은 미수신이다. 데이터 추가 전의 대응 baseline 이미지를 생성하지 않았으므로 이번 데이터가 이미지 품질을 인과적으로 개선했다는 결론은 아직 없다.

`qualification/data-freeze.json`의 8개 source 파일 해시가 생성 이후에도 같음을 확인했다. 각 이미지·후보팩·core·intent lock·effective visual contract·정확 prompt·negative·참조 파일과 native 입력을 arm별 manifest 및 `image_runs.ndjson`에 연결했다. 주 에이전트가 호출 입력 일치와 파일 해시, 세 정식 리뷰를 재검증하여 집계했다.

## 후속 반영·검증 계획

1. **작은 연결부의 가독성부터 해결한다.** bail의 개방 구멍, 체인 관통, 노리개의 고름 부착을 각각 완전한 경로로 노출한다. 적절한 크기의 장신구, 가리지 않는 고름 배치, 부품 사이 명암·공간 분리와 native 해상도에서 충분한 투영 면적을 관찰 조건으로 삼는다. full-body 스트레스 사례와 장신구 상세 사례를 따로 사전 등록하여 신발과 작은 고리를 한 프레임에서 동시에 증명해야 하는 부담도 측정한다.
2. **표면 무늬와 구조선의 혼동을 줄인다.** 라글란 연결선을 케이블 무늬와 독립적으로 추적할 수 있는 어깨 배치, 카고 거싯의 펼쳐진 측면, 배경보다 명확한 두 조임끈 출구를 지정한다. piping은 단순 밝은 띠 대신 둥근 단면의 하이라이트·그림자가 구별되는 경계를 검증한다. 기준을 낮춰 통과시키지 않는다.
3. **candidate coverage를 별도 확장한다.** arm-1의 미노출 여섯 용어와 arm-3의 노리개·bail 연결에 대해 독립 표현의 concept-unit·관계·owner 대응을 조사한다. 실제 후보 발견률과 소유 범위 음성 사례를 추가하고, 넓은 명칭의 hard activation 또는 특정 테스트 문장 강제 주입으로 해결하지 않는다. 중앙 tuck/한쪽 tuck, 바지/치마의 scope 혼동은 현재 음성 검사로 유지한다.
4. **보류 데이터를 1차 정의로 보완한다.** 보류 10개 용어군은 독립적인 부품 정의와 혼동 경계를 확인한 뒤 별도 authoring 행으로 편입한다. 재료·재단·기능 항목에는 사진으로 확인 가능한 상태와 추가 증거가 필요한 상태를 계속 구분한다. 개별 미정의 라벨 backlog를 용어군별로 나눠 source coverage를 채운다.
5. **검증 범위를 넓히고 효과를 비교한다.** 미검증 278개 프로필에서 관찰 부위·가림·재질·다국어 표현·복식군 경계를 기준으로 다음 cohort를 선정한다. source 변경은 새 데이터 snapshot과 인덱스를 만든 후 새 core·팩·생성·픽셀 리뷰에 연결한다. 같은 요청·참조·잠긴 의미의 baseline 대조를 사전 등록해야 후보 추가의 인과적 효과를 평가할 수 있다.

이번 세 원본 결과는 첫 생성의 실패를 포함한 고정된 증거로 유지한다. 후속 사례를 수행하면 별도 attempt와 snapshot으로 기록하여 비교할 수 있도록 했다.
