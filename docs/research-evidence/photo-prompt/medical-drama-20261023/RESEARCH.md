# 의학물·메디컬물 시각 의미와 후보 데이터 리서치

2026-10-23 KST. [참조 대화](https://chatgpt.com/c/6adb5b1d-dee8-83e8-8152-98a2c2ed957c)의 전체 내용을 로그인된 Chrome에서 읽었다. 19개 절, 24개 표의 **용어 행 346개와 장면 조합 8개**를 보존했다. 기본 조회 도구의 20,000자 제한 뒤에 있던 상해·완화의료·복장·포즈·체위·장비·촬영 요소까지 포함한다. 복합 항목을 임의로 분할한 개수가 아니며, 반복된 코스튬 행은 원문 위치를 유지했다.

이번 보강의 중심은 일반 진료, 팀의 노동, 돌봄과 재활이다. 기존 메디컬 호러 자료는 수술실·관·검체·신체 경계를 재사용할 수 있지만, 모든 의학물을 불안·훼손·통제의 외형으로 바꾸면 원래 의미를 잃는다. 반대로 성·생식·성인 역할극·의료학대·법의학·고어를 목록에서 지우지도 않았다. 해당 용어는 **보이는 형태, 사용자가 지정하는 사건 문맥, 보이지 않는 판단**을 구분해 연결했다.

산출물은 신규 시각 후보 100개, 기존 완전 소스 재사용 제안 22개, 비가시 문맥 카드 42개, 추가 자료가 필요한 보류 카드 8개다. 후보마다 한영 완전 문장, 소유자·접점·끝점, 관찰 기준, 혼동 경계, 출처와 주장 한계를 두었다. [전체 카드](VISUAL-CARDS.md), [원문 전체 연결](KEYWORD-ATLAS.md), [원시 데이터](semantic-cards.json)를 함께 제공한다. 구조화와 검증은 데이터 등록·검색 성공·생성 이미지 성공을 의미하지 않는다.

## 1. 장르와 직급을 복장으로 확정하지 않는다

의학물·병원물·프로시저럴·진단 미스터리는 무엇에 관심을 두고 이야기를 전개하는지에 관한 분류다. 같은 백의·병상·모니터가 코미디, 로맨스, 스릴러와 돌봄 서사에 모두 등장한다. 장르 이름으로 한 가지 조명·질환·피해 관계를 필수 활성화하면 후보의 다양성보다 오판이 커진다.

메디컬 로맨스도 한 출판사의 실제 시리즈에서는 의료인 두 사람의 협업과 의료 사건이 관계 발전에 관여한다. 이 출판 지침은 장르 사용의 근거로 유용하지만 모든 작품의 보편 정의나 한 사진의 연애 판정 기준은 아니다. [Harlequin Medical Romance](https://harlequin.submittable.com/submit/29558/harlequin-medical-romance-series-50-000-words)

X01–X04·X19·X39가 장르, 면허·수련, 전문과, 장소 기능, 인물 원형의 문맥을 보존한다. B01 백의, B02 스크럽, B14 명찰은 별도 외형 선택지다. 인턴·레지던트·펠로·전문의·어텐딩을 얼굴의 나이, 성별, 가운 길이, 스크럽 색으로 등급화하지 않는다. 국내외 직급과 자격의 세부 정의는 원문 범위를 보존했으며, 이번에 각각의 법령·교육제도를 독립 재검증한 것은 아니다.

## 2. 진료 장면은 행위자와 대상의 연결로 구체화한다

청진·촉진·타진·시진은 서로 다른 검사 방식이다. 이미지에서는 사용 기구, 접촉 부위, 손의 소유, 몸의 지지를 구분할 수 있지만, 들린 소리·통증·촉지 결과는 확인할 수 없다. [MedlinePlus 신체진찰](https://medlineplus.gov/ency/article/002274.htm)

|원문 표현|후보에서 추가한 관찰 요소|반드시 남는 한계|
|---|---|---|
|청진|D01: 의료진 귀꽂이 → 연속 관 → 쥔 손 → 청진판 → 환자 가슴|심음·호흡음·진단은 보이지 않음|
|맥박 촉지|D04: 엄지 쪽 손목, 두 손끝, 손바닥을 위로 한 팔 지지|맥박 존재·빈도·세기는 보이지 않음|
|타진|D03: 환자 등에 둔 한 손 중지, 그 위의 다른 손끝|타진음·타격 횟수는 보이지 않음|
|인계|A07: 가리키는 사람과 받치는 사람, 공유 차트, 서로 다른 두 손|구두 정보와 권한 이전은 보이지 않음|
|가운 착용 보조|D18: 착용자 두 팔, 뒤의 조력자, 뒤 끈과 접점|전체 무균 과정은 한 장면으로 증명되지 않음|
|보행 보조|E11: 환자·치료사·보행기, 허리벨트·손·팔꿈치 주변의 별도 접점|안전한 술기·기능 회복은 보장하지 않음|

SBAR는 의사소통 내용의 구조이고 인계는 정보와 책임·권한의 전환까지 포함한다. 차트를 건네거나 대화하는 모습은 가능한 대리형일 뿐이다. X05가 그 차이를 유지한다. [AHRQ SBAR](https://www.ahrq.gov/teamstepps-program/curriculum/communication/tools/sbar.html), [AHRQ Handoff](https://www.ahrq.gov/teamstepps-program/curriculum/communication/tools/handoff.html)

손을 추가하는 후보는 손만 바꾸는 후보가 아니다. 두 번째 인물, 팔의 연결, 접촉 대상, 장비나 종이의 지지까지 바꿀 수 있다. 따라서 실제 반영 때는 `hand_pose` 슬롯에 제시되더라도 전체 인물 수·행동·관계·소품·구도를 검토해야 한다.

## 3. 환자 체위는 지지면과 관절의 형태로 나눈다

C01–C14에 원문의 체위 14개를 모두 연결했다. 침상 체위와 지지 장치의 구별은 공개 간호 교재를 근거로 삼았다. [OpenStax 침상 체위](https://openstax.org/books/clinical-nursing-skills/pages/9-4-positioning-in-bed), [OpenStax 수술 중 체위](https://openstax.org/books/medical-surgical-nursing/pages/26-2-intraoperative-considerations)

가장 중요한 경계는 **파울러 체위의 등받이 굴곡**과 **역트렌델렌버그의 직선 상판 전체 경사**다. 상체가 높다는 공통점으로 합치면 침대 구조와 몸통·골반·다리의 관계가 틀어진다. C04는 올린 등받이와 낮은 하체 지지면, C11은 하나의 직선 경사면을 요구한다. C10은 같은 직선 상판에서 머리가 발보다 낮은 반대 방향이다. 반파울러·고파울러는 서로 다른 기울기의 제안으로 두되, 기관·문헌의 변형을 무시하는 보편 각도 수치는 추가하지 않았다.

쇄석위 C09는 각각의 종아리와 각각의 받침, 받침과 진찰대의 부착이 함께 보여야 한다. 슬흉위 C12는 가슴과 두 무릎의 지지, 잭나이프 C13은 골반 아래 수술대 굴곡과 양쪽 낮은 면이 다르다. 새 연구에서는 세 OpenStax 도판을 직접 보았다. 쇄석위 도판은 작은 측면 도해라 두 다리의 깊이 분리가 제한되고, 두 경사 도해는 머리·발 높이와 직선 상판을 분명히 보여 준다. 관찰 기록은 [VISUAL-REFERENCE-REVIEW.md](VISUAL-REFERENCE-REVIEW.md)에 있다. 이 도판 확인을 모든 임상 체위·보조 장치의 픽셀 검증으로 확대하지 않는다.

모든 체위는 수면·혼수·마취·뇌사·사망과 별개다. C12–C13의 모형 문맥은 완전 후보의 일부이므로 실제 사람의 장면으로 옮기면서 조용히 삭제하면 안 된다.

## 4. 호흡관·주입관·배액관은 접점과 경로가 다르다

|구별|필수로 분리한 외부 형태|카드|
|---|---|---|
|비강 캐뉼라 / 비위관|양쪽 짧은 코갈래·귀 뒤 경로 / 한쪽 콧구멍 진입·볼 고정·외부 관|D08 / D10|
|산소마스크 / 기계환기 마스크|가는 공급관 / 별도 연결부와 주름진 회로|D09 / R10|
|기관내관 / 기관절개관|입의 고정 튜브 / 목 앞 고정판·목끈|R09 / R11|
|수액펌프 / 주사기펌프|주머니–펌프–팔 경로 / 수평 주사기·플런저 구동부|R08 / D13|
|심전도 / 맥박산소측정 / 혈압 측정|피부 패드와 리드선 / 손가락 집게 / 상완 커프|D11 / D07 / D06|
|혈액투석 / ECMO|투석 필터를 거치는 왕복 경로 / 분리된 펌프·산소화기 블록|F06 / F07|

산소 장비와 기계환기의 개념은 [OpenStax 산소 장비 표](https://openstax.org/books/fundamentals-nursing/pages/19-4-management-of-impaired-cardiopulmonary-functioning), [NHLBI 인공호흡기](https://www.nhlbi.nih.gov/health/ventilator), 침상 장비들의 독립성은 [NHS ICU 설명](https://www.nhs.uk/tests-and-treatments/intensive-care/)을 확인했다. 특정 공급량·약물·주입속도를 프롬프트 기본값으로 가져오지 않았다.

기능은 보이는 관의 색이나 굵기만으로 입증되지 않는다. F06·F07은 명시적 교육 도식이다. 실제 환자의 혈액 흐름·가스교환·여과를 사진으로 증명하는 후보가 아니다. ECMO의 펌프·산소화기·배액과 반환, 투석 필터의 왕복 연결이라는 경계만 자료에서 확인했다. [Alfred ECMO 구성](https://ecmo.icu/safety-essentials-circuit-components/), [NIDDK 혈액투석](https://www.niddk.nih.gov/health-information/kidney-disease/kidney-failure/hemodialysis)

중심정맥관·동맥관 H01, CRRT H02, 요도카테터·소변주머니 H03는 정확한 구성별 도판을 더 읽어야 한다. 일반 IV나 투석 도식으로 이 요청들을 충족했다고 표시하지 않는다. 보이지 않는 체내 끝점도 외부 관의 연속성으로 대신 증명하지 않는다.

## 5. 복장·보호구의 의미는 구조와 착용 상태로 분해한다

B01–B21은 백의·스크럽·튜닉·수술가운·격리가운·보호복·모자·마스크·보안경·안면보호판·장갑·명찰·방사선 보호복·역사 제복·환자복·스타킹·코스튬의 가능한 실현을 다룬다. 일부는 하나의 완전한 복장 조합이다. 예를 들어 앞치마를 검색했다고 B16의 원피스와 교차 어깨끈을 빼고 단어만 가져오면 원본 전체 소스의 채택이 아니다.

수술가운과 격리가운은 용도와 보호 범위가 다르다. 흰색 백의·청색 천·장갑의 존재가 멸균을 증명하지 않는다. [FDA 의료 가운](https://www.fda.gov/medical-devices/personal-protective-equipment-infection-control/medical-gowns)

마스크와 호흡보호구도 밀착 설계가 다르며 안면보호판과 보안경은 별도의 층이다. B10은 얼굴 윤곽과 두 머리끈을 제안하지만 N95 인증·필터 성능·밀착시험 PASS를 외형으로 주장하지 않는다. [FDA 마스크와 호흡보호구](https://www.fda.gov/medical-devices/personal-protective-equipment-infection-control/n95-respirators-surgical-masks-face-masks-and-barrier-face-coverings)

역사 복식은 연대와 물건의 소유를 보존한다. B16은 영국 1930–1940 소장품의 줄무늬 원피스와 별도 앞치마를 참고했다. 그 소장품 자체가 서로 다른 제복에서 모은 복합이며, 앞치마는 1910–1935로 기재된다. B18의 회색·적색 테두리 케이프는 별도 1910–1920 Batten 소장품이다. 둘을 한 벌의 실제 군 간호복으로 묶지 않는다. 원물 사진을 확인한 것이 아니라 소장품 설명을 읽었다. [SMG 복합 제복](https://collection.sciencemuseumgroup.org.uk/objects/co122317), [SMG 케이프 소장품](https://collection.sciencemuseumgroup.org.uk/objects/co121248)

## 6. 진단·응급 상황·정신 상태는 표시와 분리한다

AHA의 현재 확인한 2025 성인 심정지 알고리즘은 VF/무맥성 VT와 무수축/PEA를 나눈다. 이를 X11 혼동 방지 기준으로 보존했다. 일반적인 일직선 모니터 화면에 자동으로 전기충격과 즉시 회복을 붙이지 않는다. D14는 교육 마네킹의 정지된 압박 자세이며 압박률·반동·소생 성공을 검증하지 않는다. [AHA 알고리즘](https://cpr.heart.org/-/media/CPR-Files/CPR-Guidelines-Files/2025-Accessible/Algorithm-ACLS-CA-LngDscrp-250725-Ed.pdf)

CT·MRI·초음파는 다른 영상 원리를 갖는다. F02·F03은 전형적인 한 장비 배치의 제안이며 실제 제품 구분법은 아니다. MRI에 방사선 보호 앞치마·일반 금속 장비를 의료 소품이라는 이유로 함께 넣지 않는다. F01은 탐촉자–피부–전선–장치–화면의 외부 관계를 다루며 태아·장기·확진을 입증하지 않는다. [CT](https://www.radiologyinfo.org/en/info/bodyct), [MRI](https://www.radiologyinfo.org/en/info/bodymr), [초음파](https://www.radiologyinfo.org/en/info/genus)

F04의 PACS 단면, F05의 기록 파형, D12의 수치·파형은 모두 화면이나 종이에 표현된 정보다. 환자 몸과 화면 속 해부학의 소유를 합치지 않는다. 산소측정 수치도 정확한 생리 상태의 독립 증거가 아니다. FDA는 피부 색소, 순환 등 여러 조건에서 정확성 한계를 설명한다. [FDA 맥박산소측정기](https://www.fda.gov/consumers/consumer-updates/pulse-oximeter-basics)

정신증·환각·망상 X22와 현대 ECT X24는 성난 얼굴·구속복·무마취 전기고문으로 바꾸지 않는다. NIMH가 설명하는 현대 ECT에는 마취와 근이완 문맥이 있다. 머리 전극만으로 치료명·동의·진단을 확정하지 않는다. [NIMH 정신증](https://www.nimh.nih.gov/health/publications/understanding-psychosis), [NIMH 뇌자극 치료](https://www.nimh.nih.gov/health/topics/brain-stimulation-therapies/brain-stimulation-therapies)

## 7. 외형·상처·보조 장구는 원인과 경과를 대신하지 않는다

E12–E15는 국소 색차, 입술의 청회색, 공막의 황색, 땀방울의 가능한 표현이다. 밝은 피부를 빈혈, 파란 조명을 청색증, 노란 색보정을 황달로 판정하지 않는다. 피부색과 관찰 부위의 차이를 유지한다. [창백](https://medlineplus.gov/ency/article/003244.htm), [청색증](https://medlineplus.gov/ency/article/003215.htm), [황달](https://medlineplus.gov/jaundice.html)

악액질은 단순히 마른 체형으로 확정할 수 없고, 탈모도 항암치료의 자동 증거가 아니다. 이 영역은 X38 문맥 카드로 남겼다. 관해·재발·완치 역시 같은 말이 아니다. [NCI 영양·악액질](https://www.cancer.gov/about-cancer/treatment/side-effects/appetite-loss/nutrition-hp-pdq), [NCI 관해](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/remission)

E02 캐스트는 둘러싸는 단단한 면, E03 부목은 부분 지지면과 별도 스트랩을 갖는다. E06은 연속된 다리 바깥 보조기, E07은 잔존지와 소켓·대체 부위를 갖는 의지다. 휠체어·목발·보행기 사용을 영구 장애나 보행 불가의 증거로 보지 않는다. [AAOS 캐스트와 부목](https://www.orthoinfo.org/recovery/care-of-casts-and-splints/), [WHO 재활](https://www.who.int/news-room/fact-sheets/detail/rehabilitation)

G01–G03은 분장·교육 모형에서 얕은 긁힘, 찢긴 개구부와 곧은 개구부, 온전한 표면의 색차와 융기의 대비를 제안한다. 기존 R15·R16·R17·R18·R22의 봉합선·피부층·어두운 표면·잔존지·흉터도 완전 소스로 보존했다. 상처 원인·가해자·도구·발생 날짜·괴사·감염·수술 이력은 외형 하나로 확정하지 않는다. 고어 항목은 삭제하지 않았으나, 개방성 골절·압궤·관통·절단의 임상적 정확성은 H05로 추가 자료를 요구한다. [OpenStax 상처 분류](https://openstax.org/books/fundamentals-nursing/pages/24-3-wound-classification)

## 8. 민감 진료·성인 연출·학대·법의학의 문맥을 유지한다

민감 부위 진찰, 골반 진찰, 질경, 직장수지검사, 유방 진찰은 서로 다른 대상·기구·행위를 갖는다. 쇄석위나 검사 가운은 그 중 일부의 가능한 구성이다. R06의 두 날 검경은 독립 소품이며 실제 사용 장면 전체를 의미하지 않는다. 샤프롱은 동석자의 외형으로 확정하는 직함이 아니다. 설명, 중단할 권리, 동의 또는 유효한 권한, 가림과 동석 역할을 따로 다룬다. [GMC 민감 진찰](https://www.gmc-uk.org/professional-standards/the-professional-standards/intimate-examinations-and-chaperones/intimate-examinations-and-chaperones), [ACOG 골반 진찰](https://www.acog.org/womens-health/faqs/pelvic-exams)

사용자가 의료적 노출을 지정한 경우, 닫힌 가운 R12·R19를 자동 채택해 요청을 지우면 안 된다. 각 후보의 옷 여밈·노출·가림은 선택된 소스의 구체적 의미다. 명시적 요청과 맞지 않으면 그 후보를 채택하지 않는다. 모든 진료·성인 창작을 한 가지 복장이나 가림 규칙으로 통일하지 않았다.

B21은 성인 의료 테마 코스튬, R20·G06은 명시적으로 연출한 성인 역할극의 가능한 장면이다. 의료 페티시·검진의 성애화·금지된 관계·권력 착취는 X33–X34에 각각의 문맥을 유지한다. 코스튬을 실제 직업, 진찰 접촉을 성적 의미, 성인 연출을 합의의 증거로 자동 승격하지 않는다. 참조 대화의 Oxford 문화연구 링크는 열리지 않아 전문이나 초록을 읽었다고 표시하지 않았고 근거 앵커에서도 제외했다.

출산 중 학대는 존엄·선택·행위의 문맥을 갖는다. 기구나 고통스러운 표정으로만 판정할 수 없다. SAFE는 건강 돌봄과 기록·검체 수집을 포함하는 검사이며, 증거 봉투 G04는 그 일부의 외부 매체다. 봉투·상처만으로 성폭력이나 연속된 증거 인계를 증명하지 않는다. [WHO 존중받는 산모·신생아 돌봄](https://www.who.int/publications/b/78409), [DOJ SAFE 설명](https://www.justice.gov/ovw/sexual-assault-medical-forensic-examination-safe-information)

## 9. 돌봄·완화의료와 영상 연출의 폭을 넓힌다

A10 눈높이 대화, A11 손잡기, A09·E11 재활, F12 따뜻한 침상등은 장비와 관계를 함께 보여 주는 선택지다. H/C·sickfic·whump는 고통·질병·돌봄의 서사적 비중이 달라 같은 붕대 장면에 합치지 않는다. Fanlore의 sickfic·whump는 검색 노출분만 읽었고 해당 전문은 403이었다. 완전한 문화연구 검증으로 주장하지 않는다.

완화의료는 마지막 순간에만 국한되지 않고, DNR/DNACPR은 모든 치료와 간호의 중단과 같지 않다. X37이 제도 문맥을 유지하며, G05는 논의의 기록 대리형이다. [WHO 완화의료](https://www.who.int/news-room/fact-sheets/detail/palliative-care), [NHS DNACPR](https://www.nhs.uk/tests-and-treatments/do-not-attempt-cardiopulmonary-resuscitation-dnacpr-decisions/)

F08–F12는 환자 시점, 오버헤드, 유리, 커튼, 빛의 관계를 제안한다. 차가운 팔레트는 의학물의 필수요소가 아니다. 복도 트래킹·롱테이크·핸드헬드·호흡음·호출 방송은 X40에서 시간·음향 의미를 유지한다. 정지 이미지의 흔들림이나 동선으로 촬영 지속시간과 실제 소리를 PASS 처리하지 않는다. 8개 장면 조합의 구체적 적용은 [SCENE-BLUEPRINTS.md](SCENE-BLUEPRINTS.md)에 정리했다.

## 10. 반영에 앞서 남는 검증

외부 출처는 49개다. 본문·선택 구간·검색 본문·검색 요약·접근 실패를 [출처 원장](SOURCES.tsv)에 구분했다. 개별 용어 346개의 임상 정의를 모두 독립 검증한 수치가 아니다. 도판을 직접 본 범위는 체위 3개이며 정확한 기구·고급 장비·역사 고증 8개 분야는 계속 보류다.

[반영 계획](IMPLEMENTATION-PLAN.md)은 정본 재사용, 신규 초안, 번역·문맥 수정, 비가시 진단 기록, 추가 도판 필요 항목을 나눈다. 한영 120개 질의의 예상 판정과 16개 이미지 검증군을 준비했지만 모두 미실행이다. 선택된 소스가 프롬프트에 실렸다는 사실, 실제 이미지의 전체 관계가 보였다는 사실, 장르적·미적 선호와 사용자의 수락은 별도 증거로 기록해야 한다.
