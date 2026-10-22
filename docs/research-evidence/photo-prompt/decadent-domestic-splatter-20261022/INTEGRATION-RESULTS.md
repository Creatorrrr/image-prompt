# 퇴폐미 가정 스릴러 스플래터 데이터 반영과 이미지 검증

2026년 10월 22일. **시각 의미와 후보 데이터를 운영 검색에 반영했다. 독립 에이전트 세 개의 생성 시도는 이미지 두 장과 출력 필터 차단 한 건으로 끝났다.** 원래 정한 이미지 기준에서는 B가 전체 통과, C가 지지 상태의 가림으로 부분 미충족, A가 픽셀 관찰 불가다.

이번 신규 후보는 실제 검색에서 노출됐지만 세 에이전트 모두 비교 후 채택하지 않았다. 따라서 아래 이미지는 복합 주제의 제한된 표현을 확인하는 결과이며, 새 데이터가 이미지 품질을 개선했다는 인과 증거는 아니다.

## 반영한 데이터

Decadent Aesthetic × Domestic Thriller × Splatter Horror 연구의 108개 카드를 실제 모듈에 등록했다. 장르 이름이 특정 소품이나 신체 상태를 자동으로 요구하지 않도록 완전한 선택 실현안과 문맥 전용 의미를 분리했다.

|항목|실제 반영|
|---|---|
|시각 의미 카드|108개: 관찰 가능한 선택안 86개, 문맥 전용 22개|
|후보 원문|완전한 한영 시각 후보 86개와 긍정 검색에서 제외되는 diagnostic 22개|
|선택 binding|172개; 기존 149개 슬롯 vocabulary 유지|
|키워드 경로|원 대화의 189행 모두 연결: 조합 축 3, 용어 170, 창작 조합명 8, 참고 작품 8|
|관계 검토|소유자·매체·양 끝점·연속성·현재 상태를 보존한 방향 관계 gate 252개|
|기존 데이터|후보 19,275개·binding 13,328개·catalog·policy 모두 보존|
|반영 후 데이터|후보 19,383개: 긍정 19,115개, diagnostic 268개; binding 13,500개|
|기존 source 대조|28개 이웃 후보의 전체 원문·조건·효과·binding을 다시 확인; 연구 이후 해당 원문 drift 0개|

실제 데이터는 [후보 모듈](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_decadent_domestic_splatter_20261022.json), [binding 모듈](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_decadent_domestic_splatter_bindings_20261022.json), [시각 의미 registry](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_decadent_domestic_splatter_semantics_20261022.json)에 있다. 카드별 CID와 채택 판단은 [DATA ADOPTION](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/decadent-domestic-splatter-20261022/DATA-ADOPTION.tsv), 사용 경계는 [스킬 reference](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/decadent-domestic-splatter-semantics.md)에 정리했다.

금박 손실과 순금 부식, 실크 섬유와 새틴형 반사, 천 손상과 피부 손상, 분리된 신체 부분과 연결된 외부 기관, 해부학 모형과 실제 허구 신체 결과를 구분했다. 열쇠·돈의 접촉만으로 반복 통제를 입증하거나, 모발 장신구를 모두 애도로 해석하거나, 책과 출처 카드로 인피 재질을 인증하지 않는다. 성적·폭력적·의학적·혈연·시간·음향 의미도 문맥 기록에 보존했다.

새 후보는 기존 원문의 조건을 완화한 수정본이 아니라 경계가 명시된 별도 선택안이다. 정확히 같은 긍정 문장은 없었지만 전체 corpus에 의미 중복이 전혀 없다는 판단은 하지 않았다. 모든 신규 source의 `native_approval`은 false다. 연구 graph·출처 URL·검색 노출은 whole-source native 자격이나 기존 소유자를 변경할 권한을 만들지 않는다. 독립 번역자 검토도 별도 과제로 남는다.

## 인덱스와 설치 상태

기존 설치 엔진과 임베딩 공간을 유지한 데이터 세대를 만들고 원문·전역 BM25F 통계·벡터·실행 증거를 검증한 뒤 설치했다. 먼저 비활성 설치를 검사하고, 검색 비교를 마친 다음 기본 설정을 교체했다. native `CURRENT.json`은 쓰지 않았다.

|항목|확인한 값|
|---|---|
|기본 H F2 세대|`3633746531a13fadf48051978d5b5d21bbbcaa0cfd976edf18270835f6d4ae73`|
|대응 native 세대|`0b6a92977f9f0277f62c72240b93f1a942b0d29f46a480d5388923d39b8f2e53`|
|설치 검색 문서|긍정 CID 19,115개 / 실제 RID 문서 19,117개|
|설치 검색 벡터|기존 문서 19,031개 바이트 재사용, 새 문서 86개 로컬 임베딩|
|작업용 native 인덱스|기존 후보 벡터 19,029개 재사용, 새 후보 86개 로컬 임베딩|
|설치용 native 인덱스|기존 후보 벡터 19,029개 재사용, 새 후보 86개 로컬 임베딩|
|모델 공간|기존 pinned `google/embeddinggemma-2`, 768차원, 로컬 실행|
|검색 엔진 코드 hash|기존 `96b67dedcfea019115cd46c6542287d7102e46cd12a486f1e817d79f3c634d0e` 유지|
|세 에이전트가 읽은 최신 SKILL hash|`7fe5b6cfc2da6e65dd9b9dc999e46d70a1fac7dce8c47157e53c1cba43b00f35`|

각 인덱스의 로컬 실행은 별개 작업이다. 표의 새 문서 86개를 전체 작업의 추론 호출 합계로 해석하지 않는다. 작업용 원문 인덱스와 설치용 canonical snapshot의 seal도 서로 구분한다.

작업용 dictionary와 인덱스, 설치본 전체 검사, 활성화 후 recorder/runtime 검사가 통과했다. H F2 관련 기존 회귀 검사 242개도 통과했다. 실제 로그와 세대 검증은 [integration evidence](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/decadent-domestic-splatter-20261022/integration-evidence/)에 있다.

## 실제 한영 검색 비교

[평가 사례 88개](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/decadent-domestic-splatter-20261022/EVALUATION-CASES.tsv)를 한영으로 각각 실행해 176개 질의와 반영 전후 352회 전체 pool 검색을 남겼다. 두 lane은 같은 질의로 BM25F와 로컬 cosine을 각각 한 번 실행했다.

|집단|실행 결과|
|---|---|
|개발 질의 72개|목표 신규 후보 상위 8개 노출 72개: 한국어 36/36, 영어 36/36|
|대조 질의 104개|58개 질의에서 신규 후보 상위 8개 노출: 경계 33, 일반 13, 비가시 12|
|대조의 실제 노출 검토|79개 질의–신규 후보 쌍; 33개 원 사례의 전체 긍정 원문과 의미 경계를 기록|

이 개발 세트는 데이터를 저술한 연구자가 만든 질의이며 독립 holdout이 아니다. 목표 신규 CID는 반영 전 세대에 없었다. 위 수치는 실제 검색 노출이며 독립 사용자 검색 개선율이나 생성 성능의 인과 추정이 아니다. 관리형 슬롯의 의미 projection·난수 표본과도 구분한다.

[검색 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/decadent-domestic-splatter-20261022/integration-evidence/retrieval-qualification.json)와 [대조 원문 검토](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/decadent-domestic-splatter-20261022/integration-evidence/control-exposure-review.json)에는 새틴과 실크, 살아 있는 연인의 모발 선물과 추모 브로치, 토마토 수프와 찢긴 냅킨 옆 붉은 웅덩이, 실제 허구 신체 분리와 분장 매체의 차이를 보존했다. 관련성 있는 선택안과 실제 불일치를 구분했으며 대조군 후보를 자동 채택하거나 대조군 이미지를 생성하지 않았다.

## 독립 에이전트 세 개의 실험 설계

세 에이전트는 이전 작업 history 없이 시작했다. 공통 원문 요청·정확한 이전 사용자 주제 인용·첨부 사진을 받고, 서로 다른 넓은 출발 영역 안에서 각자 여섯 개 메뉴와 난수 seed로 복잡한 장면 하나를 골랐다. 출발 영역은 코디네이터가 분리했으므로 완전히 무조건적인 장면 추첨은 아니다. 서로의 프롬프트나 결과를 공유하지 않았다.

후보를 보기 전에 각자의 envelope·입력 inventory·controls·기본 프롬프트·core·feature selection·embodiment review·판정 기준을 고정했다. 구체적 장면과 소품은 실험자 선택이며 사용자 hard lock으로 바꾸지 않았다. saved controls는 sensual 1 / fetish 0 / surreal 0 / creativity 1을 사용했다.

참고 JPEG는 실제 파일로 확인하고 모든 생성 호출의 `referenced_image_paths`에 전달했다. 얼굴·단발 외형의 안내로 사용했으며 실제 정체·나이를 추론하지 않았다. 원본 SHA256은 `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`이다.

|Arm|무작위로 고른 장면|생성 전 핵심 판정|
|---|---|---|
|A|체인 잠금 현관에서 장갑 낀 방문객의 열쇠 접시 전달을 멈춘 주민|문·체인·양쪽 손·접시의 연결, 호사와 쇠락, 생활 표면의 비산 흔적|
|B|끊어진 장식용 수화기를 든 수집가가 복도에서 켜진 다른 인터폰을 바라보는 순간|끊어진 선의 끝, 수화기·손·같은 쪽 얼굴 접촉, 별도 장치와 복도의 연결, 훼손된 호사와 붉은 impact fan|
|C|마지막 디저트 코스를 되돌리는 카트가 사적 연회와 주방의 문턱에서 멈춘 순간|얼굴·카트·바퀴·식탁·출입구 관계, 두 곳 이상의 비산 흔적, 호사와 과잉, 지지 상태|

seed·원 메뉴·동결 파일·사전 기준은 각 [Arm A](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/decadent-domestic-splatter-20261022/image-tests/arm-a/), [Arm B](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/decadent-domestic-splatter-20261022/image-tests/arm-b/), [Arm C](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/decadent-domestic-splatter-20261022/image-tests/arm-c/)에 있다.

## 검색과 프롬프트에 실제 사용된 자료

|Arm|실제 질의 / 반환 occurrence / 고유 source|신규 노출|신규 사용|최종 선택|
|---|---|---|---|---|
|A|5 / 32 / 31|E02 1개, 1회|0|완성 대안 13개 비교 후 독립 baseline 유지|
|B|6 / 48 / 44|A01·B07 2개, 3회|0|완성 대안 9개 비교 후 독립 baseline 유지|
|C|6 / 48 / 40|C07·E01·E02·E04 4개, 8회|0|baseline과 대안 비교 후 기존 source의 일반적인 쟁반 반사광 1개 사용|

합계는 17개 실제 질의, 128개 occurrence, 중복을 합친 source 104개다. 신규 source의 합집합은 6개다. 세 run 모두 이번에 설치한 같은 세대에 바인딩됐으며, 반환된 128개 occurrence마다 원문 hash와 개별 결정이 정확히 대응함을 확인했다. [실제 검색 노출](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/decadent-domestic-splatter-20261022/image-tests/managed-retrieval-summary.json)과 [구성 무결성](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/decadent-domestic-splatter-20261022/integration-evidence/managed-composition-integrity.json)을 따로 보존했다.

A의 `environment_detail`은 “without overtaking the person and hands”라는 저술 문구가 제한 변화로 해석되어 `nonpositive_scope_without_requested_change` 모드에서 0건을 반환했다. 전체 pool 검색은 실행됐고 결과를 다시 뽑지 않았다. [질의와 projection](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/decadent-domestic-splatter-20261022/integration-evidence/managed-empty-query-observation.json)을 보존했으며, 이를 corpus에 해당 자료가 없다는 증거로 해석하지 않는다.

## 생성 이미지와 원래 기준의 판정

내장 `image_gen`을 각 arm에서 한 번씩, 총 세 번 호출했다. 두 장이 반환됐고 한 건은 출력 단계 moderation으로 차단됐다. 추가 이미지 호출·다른 제공자 fallback은 없었다. 프롬프트와 실제 native plan·참고 이미지 hash를 대조했고, 반환된 두 장은 원래 도구 파일과 workspace 전달본의 바이트가 같다. 최종 보고서가 지정한 파일 45개의 실제 hash도 확인했다.

|Arm|도구 결과|사전 기준 판정|관찰 근거|
|---|---|---|---|
|A|`safety_block`, 이미지 없음|6개 모두 관찰 불가|출력 필터가 sexual·violence 범주를 보고. 이는 관찰한 픽셀 결함이 아님|
|B|이미지 1장|7/7 PASS|호사·닳은 커튼·핏빛 fan·끊긴 선·별도 인터폰·시선·손의 연결이 같은 장면에서 보임|
|C|이미지 1장|5/6 PASS, 전체 PARTIAL FAIL|주제 신호와 서비스 동선은 보이나 발·하체 지지 상태가 카트에 가려짐|

코디네이터도 저장된 원본 두 장을 직접 열어 별도 검토했다. B는 원래 기준 전체 통과, C는 같은 부분 미충족으로 판정했다. C는 손·손잡이·바퀴가 연결되지만 숨은 지지를 추정으로 통과시키지 않았다. 과일의 부패·꽃의 시듦을 확정하지 않고, 사전 기준의 excess 선택지에 따라 과장된 디저트 장식과 밀집된 연회 서비스를 가시적 과잉으로 판단했다.

B와 C의 Splatter 판정은 **비노골적인 붉은 비산 잔흔**의 범위다. 혈액 성분이나 실제 상해·가해자·사망·반복 통제를 픽셀만으로 입증하지 않는다. 명시적 고어 전체나 신규 카드 108개·관계 gate 252개의 픽셀 자격을 검증한 결과도 아니다.

### 수집실의 끊어진 인터폰

![수집실의 끊어진 인터폰](/Users/chasoik/Projects/image-prompt/generated/photo-runs/dds-arm-b-20261022-1c937745/output/arm-b-intercom-collection.png)

[B의 정확한 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/dds-arm-b-20261022-1c937745/authored/final-prompt.txt) · [에이전트 픽셀 판정](/Users/chasoik/Projects/image-prompt/generated/photo-runs/dds-arm-b-20261022-1c937745/authored/topic-pixel-review.json) · [코디네이터 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/decadent-domestic-splatter-20261022/integration-evidence/root-pixel-review-b.json)

### 마지막 디저트 코스가 멈춘 문턱

![마지막 디저트 코스가 멈춘 문턱](/Users/chasoik/Projects/image-prompt/generated/photo-runs/dds-arm-c-20261022-7ba06d79/arm-c-final.png)

[C의 정확한 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/dds-arm-c-20261022-7ba06d79/final-prompt.txt) · [에이전트 픽셀 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/decadent-domestic-splatter-20261022/image-tests/arm-c/pixel-review.json) · [코디네이터 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/decadent-domestic-splatter-20261022/integration-evidence/root-pixel-review-c.json)

A의 이미지는 없다. [작성한 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/dds-arm-a-20261022-bcef4064/final-prompt.txt), [원래 도구 오류](/Users/chasoik/Projects/image-prompt/generated/photo-runs/dds-arm-a-20261022-bcef4064/native-attempt-error.json), [현재 차단 상태](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/decadent-domestic-splatter-20261022/image-tests/arm-a/blocked-status.json)를 보존했다. 도구가 보고한 stage는 `output`, code는 `moderation_blocked`, request ID는 `6103c2a4-dbee-45b5-8455-5815c633853b`다. 반환되지 않은 화면 내용을 추정하지 않았다.

## 기록 복구와 보존

A는 최신 JS 오류 캡처의 `image_gen.imagegen`·`codex_native` 라벨과 sealed native 기록기의 `image_gen`·`native_imagegen` 라벨이 달라 장부 기록이 처음 실패했다. 원 capture와 실패 기록을 그대로 보존하고, 같은 실제 도구를 가리키는 두 protocol 라벨만 정규화한 별도 파생 기록을 만들었다. raw error·전체 outcome·요청·실제 시작과 종료 시각·attempt는 동일하다. 같은 native plan으로 기록을 재감사해 차단 시도 한 건을 장부에 연결했다. 이는 새 생성이나 정책 판단 변경이 아니다.

B는 최초 장부에 SKILL hash를 잘못 입력했다. 잘못된 원본 ledger·manifest를 보존하고, 같은 run ID·operation·timestamp·이미지·프롬프트의 해당 hash만 교정한 새 ledger를 authoritative로 지정했다. 두 row의 차이는 `skill_sha256` 하나이며 실제 도구 호출은 한 번이다. C의 일시적인 에이전트 모델 용량 오류도 같은 core·검색 receipt·표본에서 재개했고 새 시도로 세지 않았다.

[전체 시도와 이미지 검증 JSON](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/decadent-domestic-splatter-20261022/IMAGE-TEST-RESULTS.json)에 유효 장부, 원본/교정 이력, 이미지·프롬프트·manifest hash를 연결했다. 구성·runtime·delivery 감사의 PASS는 유효한 기록과 요청 연결의 결과다. A의 이미지 성공이나 C의 완전한 시각 통과를 뜻하지 않는다. 사용자 미적 수용은 pending이다.

## 결과에 따른 후속 검증 계획

1. 이번 신규 source를 실제 사용한 결과를 검증하려면 exact CID/RID의 긍정 필드·조건·효과·소유자 증거를 먼저 수동 심사한다. source가 요구하는 성인·손 소유자·같은 물건·매체 사실을 이미 동결된 요청에 소급해 만들어 넣지 않는다. whole-source 자격과 요청의 조건을 충족하는 독립 실험에서 완전한 관계의 픽셀을 검사한다.
2. A에서 드러난 “without overtaking”의 의미 projection은 별도 경계 회귀 대상으로 다룬다. 실제 의미를 검토해 질의 해석을 개선하며, 현재 run을 재표본추출하거나 결과가 나오도록 동결 문구를 바꾸지 않는다.
3. C의 지지 검증은 얼굴·양손·카트·바퀴·식탁의 연결을 보존하면서 발과 하체의 지지면까지 드러나는 구도를 별도 제한 실험으로 검사한다. 현재 이미지의 숨은 부분을 통과로 재분류하지 않는다.
4. 아직 이미지로 시험하지 않은 해부학적 결과·모형·재료 인증·성적/폭력적 문맥은 현재 연구 경계와 native 자격을 유지한다. 비노골적 두 이미지의 판정을 전체 데이터로 확대하지 않는다.

선행 연구의 README·평가 표·VALIDATION·SHA256SUMS는 당시 상태로 유지했다. 그 안의 NOT RUN과 36장 제안은 이번 독립 세 시도와 다른 기록이다. 후속 실행 상태는 이 보고서와 integration evidence를 따른다. maintenance source 사본도 실행용 파일과 구분해 보존했다.

기존 dirty 작업과 7,022개 추적 파일의 시작 바이트를 대조했다. 이번 작업이 바꾼 기존 파일은 corpus manifest·작업용 검색 manifest·설치 설정·기존 내용을 보존한 reference 추가뿐이다. HEAD `8a67fe575092d46fecc4b80d530cf36e74e92685`는 유지됐으며 commit·push는 수행하지 않았다.
