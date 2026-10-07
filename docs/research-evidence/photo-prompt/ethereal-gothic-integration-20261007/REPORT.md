# 시각 의미·후보 데이터 반영과 독립 생성 테스트

연구 결과를 현재 프로젝트 데이터에 반영하고, 최신 로컬 스킬을 사용한 독립 서브에이전트 3개의 실제 이미지 테스트를 완료했다. 선택한 새 데이터의 모든 구성요소가 보이는지를 기준으로 **A 통과, B·C 실패**다. 기본 생성 3회와 제한된 수정 2회, 총 5회의 네이티브 이미지 호출이 모두 이미지를 반환했다. 생성 성공과 의미 구현 통과는 별도로 판정했다.

현재 데이터·인덱스·로컬 런타임은 게시되었다. 새 데이터 전용 12개 검사는 통과했다. 전체 회귀검사는 실패가 남아 있어 전체 저장소의 검증 완료 또는 모든 새 주제의 이미지 구현 완료를 주장하지 않는다.

## 반영한 데이터

| 구분 | 실제 반영 | 적용 방식 |
|---|---:|---|
| 새 후보 | 60개 | 관찰 가능한 관계 후보 40개, 소유 대상이 분리된 팔레트 20개 |
| 새 시각 의미 프로필 | 41개 | 관계 40개, 공통 3대상 팔레트 역할 1개 |
| 선택형 번들 | 68개 | 원자 번들 60개, 여러 관계를 묶은 선택형 조합 8개 |
| 기존 후보 보강 | 5개 | 기존 필드를 보존하고 동등한 풀이·사용 맥락만 덧붙임 |
| 소스 등록 | 2개 | 후보·프로필 로드 순서 각각 끝에 추가 |

연구의 70개 의미 카드 전부에 실제 처리 결과를 기록했다. 36개는 새 관계로 반영, 1개는 새 관계와 기존 보강에 함께 반영, 16개는 기존 의미 재사용, 5개는 문맥 설명으로 유지했다. 11개는 분야 검토, 1개는 출처 확인이 필요해 반영을 보류했다. 원 대화에서 복구한 키워드는 350개이며, 대화에서 언급된 360개 중 나머지 10개는 확인 가능한 원문이 없어 만들지 않았다.

이번 데이터는 'gothic' 같은 넓은 분위기 단어가 의상·표정·포즈를 자동 결정하지 않게 설계했다. 직물 로제트와 살아 있는 꽃, 회화 속 꽃과 실제 가지, 금빛 표면과 금박 제조법, 서리와 이슬, 입자와 그레인, 안개와 광학 확산을 구분한다. 팔레트는 이미 존재하는 대상의 색 역할을 바꾸며 물건·금속·피부색을 새로 만들지 않는다. 헤어·표정·피부 관련 후보는 소유 대상과 변경 속성을 선언하고 참조 잠금과 충돌하면 채택할 수 없다.

보강한 기존 항목은 `low_bun_hair`, `cr_candidate_cool_subject`, `cr_candidate_dark_on_dark`, `pe_neutral_diffusion`, `cr_candidate_low_chroma`다. 코일 번·눈썹 높이 앞머리·피부 가장자리 온도 같은 추가 의미는 넓은 기존 항목의 별칭으로 넣지 않고 독립적인 선택 후보로 만들었다. 기존 광학 확산 후보의 중립색 번짐 조건도 유지했다.

- [후보 데이터](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_ethereal_gothic_scene_extension.json)
- [시각 의미 데이터](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_ethereal_gothic_scene.json)
- [70개 카드의 실제 처리 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/INTEGRATION-MAP.json)
- [연구 보고서와 출처](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-research-20261007/RESEARCH.md)

## 독립성·참조·실행 방법

세 에이전트는 대화 이력을 전달하지 않은 별도 컨텍스트에서 시작했다. 코디네이터가 최신 요청 원문을 담은 요청 봉투를 먼저 만들고 고정했다. 전차·온실·무대라는 넓은 탐색 분야만 나누어 주었고, 각 에이전트가 운영체제 난수로 자체 컨셉 목록에서 하나를 뽑았다. 다른 에이전트의 프롬프트·팩·이미지는 입력으로 쓰지 않았다.

각 에이전트는 첨부 사진을 실제로 열어 관찰했다. 사진에 보이는 얼굴·짧은 머리·앞머리만 참조했으며 실제 나이·직업·신원·성격을 추정하지 않았다. 장면 속 성인 역할은 창작 설정으로 구분했다. 복잡한 장면과 기준 프롬프트를 먼저 작성하고, 그 뒤 후보 없는 중립 카탈로그에서 9개 범주를 선택했다. 요청·컨트롤·핵심 장면·신체 관계 사전 검토·선택 기록을 고정한 다음에만 데이터 후보 검색을 허용했다.

실제 컨트롤 해석은 세 경우 모두 sensual=1, fetish=0, surreal=0, creativity=1이었다. 공용 V6 생성기의 정상 경로로 각 1개 팩을 만들었다. 런타임 검색 방식은 **core_bm25f**였으며, 이 세 실험에서 실시간 임베딩 검색이 작동했다고 주장하지 않는다. 선택하지 않은 후보를 억지로 주입하거나, 후보를 얻으려고 고정 장면을 수정하지 않았다.

최신 로컬 스킬 [SKILL.md](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/SKILL.md)의 SHA256은 `7dc4220b1dd784abe8ed7c93b84612d0472591c7753f0dcfda0c88da229ac857`이다. 테스트 요청 원문의 SHA256은 `e01d0ad2bb1da5978db473bef7ce3e0212453e8f35839532c8ba05a27dbc7fff`, 사진의 SHA256은 `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`이다.

## 세 테스트의 실제 결과

| 실험 | 무작위 복잡한 컨셉 | 선택한 새 데이터 | 새 데이터 전체 구현 | 신체·접촉 필수 검사 | 호출 |
|---|---|---|---|---|---:|
| A | 마지막 회차 정류장의 꽃 운반 여행자 | 직물 로제트와 실제 꽃의 서로 다른 재질·소유 대상 | **PASS** | 5/5 PASS | 1 |
| B | 야간 수분 관찰 유리온실 | 로제트와 실제 꽃, 얼굴 양옆 어두운 여백 | **FAIL** | 5/5 PASS | 2 |
| C | 빈 리허설룸의 무대 셔터 조절 기술자 | 드문 꽃이 붙은 목질 가지, 차가운 중심 피부와 따뜻한 피부 가장자리 | **FAIL** | 4/5 PASS | 2 |

### A — 전차에서 꽃을 운반하는 장면

난수 seed `4697092674311968183`, 자체 목록 7개 중 index 5를 선택했다. 팩 `00bc29627d02e714`에서 새 후보 2개가 노출됐고, 직물 로제트/실제 꽃 관계 1개를 채택했다. 닫힌 눈 후보는 줄기에 주의를 기울이는 장면을 약하게 만들 수 있어 채택하지 않았다.

옷깃의 로제트에는 접힌 직물 층과 천 가장자리가 보이고, 운반함의 꽃은 별도 식물 꽃잎과 자기 줄기를 가진다. 에이전트가 나눈 5개 세부 관찰 항목과 신체 필수 검사 5개가 모두 통과했다. 코디네이터도 원본 해상도에서 결과를 확인했다.

![A 최종 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/arm_a/native_image_attempt_1.png)

[프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/arm_a/final_prompt_en.txt) · [실험 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/arm_a/REPORT.md) · [결과 JSON](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/arm_a/QUALIFICATION-RESULT.json)

### B — 온실에서 야간 수분을 관찰하는 장면

난수 seed `11651423125803864286429695462563180664`, 자체 목록 6개 중 index 0을 선택했다. 팩 `0af3f03fdf8f79a1`에서 새 일반 후보 5개·번들 3개가 노출됐고, 로제트/실제 꽃 후보와 어두운 측면 여백 번들을 채택했다.

첫 이미지에서 검은 천 로제트와 식물의 흰 꽃은 구분된다. 그러나 얼굴 옆 영역에 식물·유리창 프레임 등 세부가 차 있어, 얼굴과 주변 장식을 분리하는 어두운 저밀도 간격은 두 구성요소 모두 실패했다. 열린 composition 범위에서만 양옆 실제 간격을 확보하는 수정 1회를 실시했다. 원 사진과 첫 이미지의 정확한 파일을 편집 입력으로 제공했고, 얼굴·머리·손과 반투명 종이의 접촉·나방과 꽃의 접촉·통과한 재질 구분을 유지했다. 수정 후에도 여백은 구현되지 않았다. 최종 4개 새 데이터 구성요소 중 2개 PASS·2개 FAIL이며 전체 FAIL로 남겼다.

![B 최종 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/arm_b/native_attempt_2.png)

[독립 장면 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/arm_b/standalone_prompt_en.txt) · [실제 수정 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/arm_b/final_prompt_attempt_2.txt) · [실험 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/arm_b/QUALIFICATION-REPORT.md)

### C — 무대의 셔터를 조절하는 장면

난수 seed `2907888127213958793`, 자체 목록 6개 중 index 4를 선택했다. 팩 `9fc4f41e3ef3c7d4`의 맥락 후보 목록에서 목질 가지와 피부 색 분리 후보 2개가 노출돼 채택됐다.

실제 가지의 연속된 줄기, 떨어져 붙은 밝은 꽃, 드문 잎과 노출된 목질 간격은 보인다. 피부 중앙의 비교적 차가운 색도 관찰했지만, 따뜻한 색은 주로 머리카락에 보이며 **얼굴 피부의 경계에 한정된 따뜻한 조명**은 확인되지 않는다. 머리카락의 금빛을 피부 구현으로 대체하지 않았다.

셔터 장치의 손→줄→도르래→움직이는 문짝 부착 지점도 끝까지 추적되지 않았다. 열린 카메라·프레이밍·구도·색·조명 범위에서 연결부와 피부 경계를 드러내는 수정 1회를 했으나, 수정 후에도 부착 지점과 따뜻한 피부 구역을 확인할 수 없었다. 이것은 확인 불가능한 투영·가시성 실패이며 해부학적 변형이라고 단정하지 않는다. 새 데이터 2개 중 1개 전체 PASS, 1개 FAIL로 전체 FAIL이고, 신체 필수 검사는 4/5 PASS다.

![C 최종 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/arm_c/generated_image_attempt_2.png)

[독립 장면 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/arm_c/final_standalone_prompt_en.txt) · [실제 수정 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/arm_c/final_actual_edit_prompt_en.txt) · [실험 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/arm_c/QUALIFICATION-REPORT.md)

## 증거 범위와 남은 한계

세 팩 모두 새 시각 의미 프로필은 선택 후보로 노출되지 않았다. 따라서 새 프로필에서 파생된 hard gate가 실제 세 이미지에서 통과했다고 주장할 수 없다. 신체의 5개 필수 게이트는 실제 감사기가 파생했다. 선택한 일반 후보·번들의 의미는 원문 구성요소 전부를 확인하는 **별도의 원본 이미지 관찰**로 검사했다. 프로필 ID가 연결돼 있다는 이유로 필수 게이트를 만들어 넣지 않았다.

세 실험에서 채택한 새 항목은 중복을 제외해 **4/60개**다. 로제트/실제 꽃과 목질 가지는 확인됐고, 어두운 측면 여백과 피부의 국소 온도 분리는 실패했다. 41개 프로필 전체, 20개 팔레트, 다른 꽃·직물·광학 관계의 이미지 검증은 아직 되지 않았다.

새 문구의 기준 프롬프트 대비 실제 추가 부분은 각 실험의 literal delta 파일에 남겼다. 기준 프롬프트에도 이미 꽃·장식·조명·일부 재질 구분이 있었다. 기준 이미지를 따로 생성하거나 제거 실험을 하지 않았으므로, 이번 데이터 때문에 이미지 품질이 향상됐다는 인과 결론은 낼 수 없다. 사용자 취향·참조 닮음에 대한 최종 수용 판정도 대기 상태다. 감사기 종료 코드 1은 A·B의 경우 기술 실패가 아니라 이 사용자 판정 대기 때문이며, C는 실제 필수 게이트 실패가 추가로 있다.

코디네이터는 전체 2,290개 프로필을 대상으로 독립적인 풀이 문장 6개를 실제 Gemini `gemini-embedding-2`, 768차원, batch=1로 검색했다. 임베딩 단독은 4/6, hybrid는 5/6에서 목표 프로필을 돌려줬다. 인접한 부정 문맥에서 새 hard 활성화는 0개였다. 금빛 모자이크 관계는 두 경로 모두 실패했고, 드문 꽃의 목질 가지는 hybrid에서만 발견됐다. 이것은 검색 진단이며 세 에이전트의 실제 BM25F 경로와 구분한다. 검색 임계값을 낮추거나 테스트 문장을 hard 별칭으로 추가하지 않았다.

[실제 검색 진단](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/LIVE-RETRIEVAL-PROBES.json) · [종합 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/QUALIFICATION-SUMMARY.json)

## 검사·현재 런타임·보존

새 데이터 검사 12/12가 현재 primary에서 통과했고, 새 등록 순서와 과거 소유 대상 기록 검사 2개도 수정 후 통과했다. 전역 유지관리 검사 1개는 기존 `photo_prompt_clothing_structure_extension`의 CT073 기록에 `maintenance_only`가 없어 계속 실패한다. 이번 유지관리 기록의 같은 누락은 v2로 보완했고 해시 연결도 확인했다. 기존 CT073 기록은 수정하지 않았다. [현재 데이터 검사 로그](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/current-data-regression-recheck.log)

사전·실제 인덱스 바인딩 검사가 통과했다. 시각 인덱스는 2,290개 프로필·4,888개 exact term, 의미 인덱스는 10,536개 항목이다. 동일 텍스트·모델·차원·해시 조건을 만족한 기존 벡터만 재사용했다. 이전 shard를 삭제하지 않았다.

전체 회귀 실행의 최초 발견 항목은 1,803개였고, 실제 1,705개가 실행됐다. 기록상 39개 assertion 실패·17개 오류가 있으며, class setup 실패와 import 단계 문제로 완전 실행도 아니었다. 보조 실행 도구가 import 실패 항목을 `unittest.loader`로 잘못 묶어 생긴 누락은 따로 기록하고 원래 14개 모듈 각각을 추가 실행했다. 추가 실행에서는 13개 모듈의 157개 검사가 통과했고, robe 과거 경계 모듈 1개는 기존 photorealism 소스의 V32 seal 불일치 때문에 import 단계에서 막혔다. 추가 결과와 모든 최초 실패는 [회귀 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/full-suite/RESULT.json), [추가 실행](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/full-suite/SUPPLEMENT-RESULT.json)에 보존했다. 전체 PASS로 바꾸지 않았다.

확인한 실패에는 이미 시작 전부터 V24/V32/V33 seal과 달랐던 photorealism 소스·manifest·index, 과거 고정 candidate-pack의 바이트 불일치, 기존 프로필 수정과 옛 snapshot의 차이, worktree에서 누락됐던 과거 이미지·makeup 실행 자료가 있다. 현재 작업과 무관하다고 모든 실패를 일괄 분류하지 않는다. 조용한 환경에서 aggregate 검사 1개를 다시 실행했으나 17.583초 뒤 고정 photo baseline pack 해시 불일치로 실패했다. 기존 seal이나 gate를 완화해서 통과시키지 않았다. [원인 분류](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/REGRESSION-DIAGNOSTICS.json)

이미지 실험의 generation은 `a3d47aa324454069153da1b6c4a8d965e134fe9e907cee72390e6f9b7a0648f5`, fingerprint는 `2476149f066c2867e9dd10ba7444ecd4f41cffdf3d00023909bd30a3828bc4f4`다. 전용 worktree와 그 바이트를 그대로 보존했다.

현재 primary는 유지관리 v2 보완 후 generation `ccd67dc9bd1f66c268223cd79fdd13d6b40714be70df584b6dc996c1846b6b79`, fingerprint `f9f4a78b53c02a29055a6a537689d7059b5a9105d047a00c3c378f72279bc8a7`로 게시됐다. 두 버전의 실제 후보·번들·기존 보강 내용은 완전히 동일하고 `maintenance_ref`만 바뀌었다. 시각 프로필 데이터도 바이트가 동일하다. 이 후속 게시를 이미지를 다시 생성한 증거로 바꾸지 않았다.

코디네이터의 최종 바인딩 검사는 PASS다. 모든 고정 핵심 파일·요청·도구에 전달한 정확한 텍스트·참조 파일·5개 이미지 해시·각 ledger의 1/2/2 호출과 retry 연결을 확인했다. 기존 보호 소스 136개도 초기 해시와 일치한다. 수정 전 실패 이미지를 지우거나 여러 시도의 부분 성공을 합쳐 통과로 만들지 않았다. [바인딩 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/BINDING-VERIFICATION.json)

커밋·push·PR·외부 배포는 수행하지 않았다. 다음 보강의 순서·통과 조건·중단 조건은 [후속 반영 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/FOLLOW-UP-PLAN.md)에 구체화했다.
