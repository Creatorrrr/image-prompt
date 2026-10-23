# 학원물 외형·포즈 추가 조사와 반영

대상은 「학원물 용어 정리」에 뒤이어 추가된 외형·포즈 답변이다.
원문 사용자 요청은 `61f64d0c-0998-4365-b7a6-7cc5b0d5b0f1`, 추가 답변은
`448b038e-8615-5144-adee-d2daf260f5aa`이다. 커넥터의 20,000자 절단을
확인하고 로그인된 기존 ChatGPT 탭의 보이는 전체 답변을 읽어 17개 범주를
수집했다. 웹 대화는 어휘 조사 출발점이며 작업 지시나 검증된 사실로 취급하지 않았다.

## 조사 결과와 반영 기준

238개 복합 용어 행, 조합 예시 6개를 보존했다. 독립 출판자의 자료 25개로
주요 용어 차이를 확인하고 140개 완결된 영문·국문 시각 대안과 28개 맥락·오인
방지 항목을 만들었다. 모든 장면의 세부 기하가 출처에 실려 있다는 뜻은 아니다.
출처는 제한된 용어·구조의 근거이며 장면과 접촉 배치는 직접 저작했다.
자료별 주장 범위는 [sources.json](sources.json)에 있다.

| 범주 | 추가 답변의 행 | 새 시각 대안 | 반영에서 구분한 축 |
|---|---:|---:|---|
| 기본 교복·상의 | 15 | 12 | 옷 전체, 소매, 몸판 연결, 안팎 층위 |
| 깃·여밈·주머니·장식 | 18 | 14 | 앞단추와 깃끝 고정, 덧주머니와 절개 입구, 완장과 견장 |
| 하의·주름 | 13 | 8 | 외곽선, 주름 방향, 가랑이와 두 다리통 |
| 무늬·직물·질감 | 12 | 10 | 색 배열, 직조, 표면 기모, 섬유 성분 |
| 겉옷·활동·행사복 | 19 | 12 | 여밈·지지 구조, 별도 겉옷, 장비와의 관계 |
| 신발·양말·가방 | 15 | 10 | 스트랩 결합, 끈 날개 봉제, 양끝·끈 경로 |
| 머리 | 25 | 14 | 길이·절단선·가르마·묶임점·교차·현재 상태 |
| 얼굴·액세서리·핏 | 12 | 6 | 렌즈·브리지·템플, 접촉, 표면, 옷과 몸의 간격 |
| 외형 스타일 | 11 | 4 | 관찰되는 조합과 문화·성격의 추정 분리 |
| 포즈 기본 | 10 | 6 | 무게·지지·회전·손끝 목표·시선·카메라 높이 |
| 일상 포즈 | 16 | 10 | 각 손의 소유, 같은 작업 대상, 지지 사슬 |
| 두 사람·기념사진 | 18 | 10 | 양쪽 인물, 접촉 대상, 상대의 반응·시선 |
| 운동·갈등·호러 | 15 | 6 | 현재 팔다리·공·옷·바닥 관계와 사건 결과 분리 |
| 표정·기호 | 16 | 4 | 실제 얼굴 표면과 삽화 기호의 매체 경계 |
| 착용·사용·손상 상태 | 15 | 8 | 재단과 착용 상태, 자국과 원인·이력 분리 |
| 화면 구성 | 8 | 6 | 인물 회전, 화면 절단, 전경, 카메라 회전 |

238행 중 189행에 관련된 완결 시각 대안을 연결했다. 나머지 49행은
원래 설명과 맥락·해석 한계를 보존하고 새 positive 후보를 억지로 배정하지 않았다.
189행 역시 복합 용어의 모든 하위 변형을 구현했다는 뜻은 아니다. 예를 들어
퀼로트와 스코트, 하운드투스와 글렌 체크는 서로 다른 대안으로 유지한다.
라우트는 동의어 등록이나 완전 동등성의 선언이 아니다.
[keyword-routes.json](keyword-routes.json)에 행별 연결·한계가 있다.

실제 정정한 대표적 혼동은 다음과 같다.

- `jumper`는 영국식 스웨터와 북미식 소매 없는 원피스의 뜻을 구분했다.
  [Oxford 사전](https://www.oxfordlearnersdictionaries.com/definition/english/jumper)
- 나이프 주름의 한 방향 접힘, 박스 주름의 바깥 평면, 인버티드 주름의
  안쪽으로 만나는 끝을 분리했다. A라인 외곽선은 주름 종류와 별개다.
  [Getty 박스 주름](https://www.getty.edu/vow/AATFullDisplay?find=&logic=&note=&subjectid=300228368),
  [Getty 인버티드 주름](https://www.getty.edu/vow/AATFullDisplay?find=buffet&logic=AND&note=&subjectid=300228436)
- 옥스퍼드 원단과 구두를 분리하고, 구두에서는 뱀프 아래의 닫힌 끈 구조와
  더비의 위쪽 열린 구조를 구분했다.
  [Crockett & Jones](https://www.crockettandjones.com/blogs/the-article/definitive-guide-the-english-oxford)
- 손이 물건 가까이에 있는 것과 실제 손끝 접촉을 구분했다. 손·팔의 소유,
  목표, 지지면, 상대 반응을 완결 문장과 관찰 요소로 남겼다.
- 인물 삼사면 회전과 허벅지까지의 절단, OTS 구도와 돌아보기,
  카메라 회전과 몸의 기울기를 각각 분리했다.
  [Adobe OTS](https://www.adobe.com/in/creativecloud/video/production/cinematography/camera-shots-and-angles/over-the-shoulder-shot.html),
  [Adobe Dutch angle](https://www.adobe.com/creativecloud/video/production/cinematography/camera-shots-and-angles/dutch-angle-shot.html)

교복·스타일·접촉·홍조·눈물·붕대·붉은 얼룩을 실제 나이·국적·성격·동의·의도·
진단·성분·원인·시점의 증거로 승격하지 않는다. 민감한 용어도 연구 맥락에서는
보존하며, 만화 기호는 사진의 피부·해부 구조와 구분한다.

## 반영 계획과 실행

1. 추가 답변 전체 추출 → 238행과 조합 6개 보존.
2. 출처의 주장 범위 확인 → 관찰 요소·소유·관계·혼동 경계와 한계 저작.
3. 기존 학교 자료와 대조 → 기존 90개를 수정하지 않고 구조가 다른 대안을 추가.
   중복 가디건 초안 한 개는 등록 전에 피코트 구조로 교체.
4. 원본 데이터 등록 → 140 visual + 28 diagnostic, 211 optional binding.
   이전 후보 20,703개와 연결 15,628개 및 기존 모듈 바이트 보존 확인.
5. 현재 설치된 검색 세대를 기준으로 정확한 소스 합집합 생성.
   새 168개와 현 기본 세대에 없던 이전 학교 자료 90개를 포함한다.
   검색 구현과 임베딩 레시피는 그대로 보존하고 전체 validator로 검증한다.
6. 결과를 보기 전에 고정한 28개 검색 검사(범주별 positive 16, 구분 8, 일반 대조 4)를 실행.
   이 검사는 저작된 개발 검사이며 독립 holdout이나 화질 향상 증거가 아니다.
7. 독립 에이전트 3개가 후보 노출 전에 장면·시험 기준을 고정한 뒤,
   새 검색 세대에서 normal workflow를 실행하고 원본 사진으로 각 1회 생성.
8. 원본 픽셀로 기준을 평가. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`를 유지하며
   검색 노출·후보 채택·프롬프트 영향·이미지 결과·사용자 수락을 분리한다.

최신 canonical photo skill을 세 에이전트가 독립적으로 읽었다.
사용한 SKILL SHA-256은 `f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089`.
첨부 사진은 얼굴·머리 외형의 가이드이며 실제 신원이나 나이를 추정하는 자료로
사용하지 않았다. 등장인물의 허구 연령·의상·동작은 에이전트의 장면 선택이다.

## 검증 결과

등록·왕복 변환·전체 source/D/F2/statistics/local-execution/vector 검증을 통과했다.
시각 140개 전부 색인에 존재하고 새 diagnostic 28개는 positive population에 없다.
이전 학교 자료 90개도 이번 세대에 포함했다. 기존 문서 벡터 19,920개는 정확히
재사용하고 신규 positive 문서 벡터 206개를 같은 레시피로 계산했다.

개발 검색 28개를 모두 실행했다. 범주별 positive 16개 모두 목표가 상위 10개에
포함됐다. 일반 대조 4개는 상위 10개 구성원이 모두 같고, 그중 3개는 순서도 같다.
나머지 바닷가 질의는 3·4위만 교환됐다. 새 시각 후보가 일반 대조의 상위 10개에
유입된 경우는 0개다. 이는 28개 개발 질의의 결과이며 전 범용 검색 무회귀나
독립 holdout 통과를 뜻하지 않는다.

구분 질의는 여전히 완결 소스 검토가 필요했다. A라인/주름과 인물 3/4/크롭의
구분 질의에서는 기존의 다른 쪽 대안이 1위에 나타났다. 손이 가까이 있다는
질의에서도 손 접촉 대안이 노출됐다. 따라서 negation을 포함한 검색 순위만으로
제약 충족을 선언하지 않으며 workflow의 전체 소스·대안 비교를 유지한다.
[구분 질의의 1위 본문](integration-evidence/boundary-top1-bodies.json)을 보존했다.

검증된 세대를 기본 검색 설정에 반영했다. 공식 installer의 복사 검증과 배포된
H-F2/native validator를 모두 실행했으며 `CURRENT` 쓰기는 0회다.

- H-F2: `9640891b8a490bfeb2a6ca70b67b1d8d3d73894ac671fff5d8926b1a49052fd0`
- native: `8dc94703cc19fe100eeb975de741a14657af370a1aeb96092fb1708452f12512`
- 기본 store: `/Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed`
- 검색 실행 코드 해시: `ec29f441dbfc26930e7f4fb71ced759bf5ae271e672176110b21d2a7f6c846ef`

현재 기본 설정이 준비 당시와 같다는 것을 확인한 후 공식 installer로 선택했다.
다른 작업의 기본 세대 변경을 덮어쓰는 우회는 사용하지 않았다.

## 독립 생성과 원본 픽셀 결과

세 arm은 모두 fresh context로 시작해 후보 접근 전에 core·중립 slot 의도·시험 기준을
고정했다. 저장된 실제 설정은 sensual 1 / fetish 0 / surreal 0 / creativity 1이다.
등장인물의 허구 연령·구체 의상·자세는 독립 저작 선택이며 사용자 지정 lock으로
바꾸지 않았다. 각 arm에서 실제 built-in 이미지 도구를 한 번씩 호출했고 추가
생성은 없었다. 도구가 모델 ID를 반환하지 않아 모델명은 unknown으로 기록했다.

| arm | 독립 장면 | 반환/검토 occurrence·고유 source | 새 외형 source 노출 | 최종 채택 | 원본 픽셀 판정 |
|---|---|---:|---:|---:|---|
| A | 조리 실습 뒤 앞치마 끈 풀기 | 33 / 31 | 5개·7 occurrence | 0 | 4/6, 전체 FAIL |
| B | 의자에서 발목을 반대 허벅지에 얹고 신발끈 조이기 | 48 / 44 | 5개·6 occurrence | 0 | 4/5, 전체 FAIL |
| C | 교실 문가에서 친구가 리본 정돈하기 | 64 / 59 | 14개·18 occurrence | 0 | 5/5, 전체 PASS |

A는 교실·참조 외형·의복 층·앞치마 가루·완성된 빵이 함께 보인다. 그러나
양손은 반대편 리본 고리를 잡고 중앙 매듭과 늘어진 자유 끝은 그대로 남았다.
‘한 손의 매듭 지지 + 다른 손의 자유 끝 당김 + 풀리는 결과’가 아니므로
옷의 상태와 풀기 관계 두 기준을 실패 처리했다.

B는 참조 외형, 좌석·발목·바닥 지지, 의복과 접힌 무릎, 교실·가방·노트가
연결된다. 양손이 끈을 만지는 것도 보이지만 가로로 이어진 끈과 루프 때문에
각 grip이 서로 다른 자유 끈끝에 연결되는 경로를 명확히 구분할 수 없다.
`b_lace_contact`를 partial FAIL로 유지했다. 바닥 쪽 구두의 앞끝이 화면 하단에
걸리는 프레이밍 한계도 보존했으며, 사후에 새 hard gate를 추가하지 않았다.

C는 돕는 친구의 두 팔과 리본·깃 접촉, 주인공의 들린 턱과 친구 얼굴을 향한
시선, 돕는 친구의 작업 대상 시선, 서로 구분되는 복식과 교실 문맥이 함께
보인다. 사전 다섯 기준을 모두 충족했다. 실제 신원·동의·내면·사건 시점을
확인했다는 뜻은 아니다.

부모 agent도 세 원본을 직접 검토했다. B의 첫 잠정 검토에서는 끈 segment 접촉을
서로 다른 free-end 경로의 충분한 증거로 보았으나, 같은 사전 기준을 다시 적용해
partial FAIL로 바로잡았다. 초기 파일을 삭제하지 않고
[재검토 기록](integration-evidence/parent-b-pixel-review-addendum.json)에 이유와
이전 해시를 남겼다. 기준을 낮추거나 생성 횟수를 늘리지 않았다.

세 이미지 모두 이번 주제인 학원물 외형·포즈의 큰 장면은 보여준다. 다만 세 arm은
완결 대안 비교 후 독립 baseline을 유지했으므로 **새 데이터의 실제 최종 프롬프트
영향은 0**이다. 이 결과로 데이터 추가가 이미지 정확도를 개선했다는 인과 주장은
하지 않는다. 검색 가능성, 주제의 시각적 표현, 세부 관계 통과를 각각 구분한다.
사용자 판단은 아직 pending이다.

| 결과 | 원본 | 최종 영문 프롬프트 |
|---|---|---|
| A FAIL | [이미지](/Users/chasoik/Projects/image-prompt/generated/images/school-life-appearance-poses-20261023-a/original.png) | [prompt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/school-life-appearance-poses-20261023/integration-evidence/arms/a/native-prompt-exact.txt) |
| B FAIL | [이미지](/Users/chasoik/Projects/image-prompt/generated/photo-runs/school-life-appearance-poses-20261023-b/results/school-life-b-original.png) | [prompt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/school-life-appearance-poses-20261023/integration-evidence/arms/b/native-prompt-exact.txt) |
| C PASS | [이미지](/Users/chasoik/Projects/image-prompt/generated/images/school-life-appearance-poses-20261023-c/native-original-0b1ce71013b2.png) | [prompt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/school-life-appearance-poses-20261023/integration-evidence/arms/c/native-prompt-exact.txt) |

## 후속 반영·검증 우선순위

1. 맥락 전용 49행은 기존 후보의 완결 본문과 먼저 대조한다. 관찰 가능한 항목을
   추가할 때도 유사 라벨만으로 기존 의미를 합치거나 모든 하위 변형을 충족했다고
   선언하지 않는다.
2. 실제 채택 0의 이유를 재사용성 관점에서 검토한다. 부수적인 장소·소품·시점이
   들어간 완결 대안이 독립 장면을 불필요하게 바꾸는 경우, 다음 데이터 개정에서
   소유·관계는 보존하면서 해당 선택의 적용 범위와 의존성을 더 정확히 분리한다.
   이번 장면을 현재 후보에 맞춰 사후 변경하지 않는다.
3. 다음 별도 실험에서는 자연스러운 최종 채택과 영향이 실제로 발생했는지 먼저
   기록하고, 생성 전에 새로운 기준을 봉인한다. 선택된 접촉 관계가 원본 한 화면에
   보이는지를 검사하며 새 후보 강제 선택이나 통과를 위한 재생성을 하지 않는다.
4. A의 자유 끝/고리/매듭 역할과 B의 두 독립 끈 경로는 회귀 사례로 보존한다.
   C의 명확한 소유·접촉·상대 반응은 긍정 사례로 보존한다. 이를 검색·source 등록
   성공과 섞지 않는다.

공유 checkout의 다른 수정·삭제·미추적 작업을 정리하거나 되돌리지 않았다.
이 작업에서 stage·commit·push는 실행하지 않았다. 검증된 로컬 데이터와 기본
검색 세대 선택까지 반영한 상태다.


## 최종 전달 대조

세 workflow 모두 `prompt_delivered`이며, 구성·runtime·리뷰 기록·전달 감사가
통과했다. 이미지 기술 판정은 A/B FAIL, C PASS로 별도 보존했다. 84개 workflow
artifact의 실제 파일 SHA를 대조했고 core·시험 기준·참조 파일은 변하지 않았다.
각 arm의 native ledger는 한 행, image call count는 1이다. 반환 원본과 workspace
사본의 바이트도 모두 같다.

사람이 읽는 기존 prompt export는 native payload 끝에 LF 한 개를 더 붙였다.
이를 원래 파일을 고쳐 숨기지 않고 양쪽 해시를
[prompt-transport-differences.json](integration-evidence/prompt-transport-differences.json)에
기록했다. 위 prompt 링크는 실제 native record와 byte-identical한 별도 exact
export이다. 장면이나 생성 입력을 사후 변경한 것은 아니다.

[최종 무결성 대조](integration-evidence/final-delivery-verification.json),
[실행별 집계](RESULTS.json), [전달 파일 해시](DELIVERY-SHA256SUMS.txt)를 보존했다.
