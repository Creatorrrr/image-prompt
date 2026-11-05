# 연극 누락 범위 보강 연구

기준일 2026-11-05. 기존 연구 `research-and-plan.md`와 사용자가 연결한 연극 대화 1~15절을 기준으로 한다. 이번 확장은 시각적으로 구체화할 수 있는 **대안**과 소리·시간·극작·정체성처럼 정지 사진만으로 입증하기 어려운 **문맥 진단**을 별도 보관한다. 후보 장면의 인물 수, 접촉과 조명은 아래 문헌의 공연 사진을 복사한 것이 아니라 조사에 근거한 창작 제안이다.

## 빠진 범위와 조사 근거

| 범위 | 근거와 반영 경계 |
|---|---|
| 장르와 연출 | [V&A의 영국 연극사](https://www.vam.ac.uk/articles/the-story-of-theatre)는 역사적 무대 디자인·멜로드라마·스펙터클을 구분한다. 사실주의·표현주의·부조리·서사극·비극·희극 등의 이름이 단일 색상, 특정 포즈 또는 필수 소품을 지시하지 않도록, 서로 다른 개별 장면은 선택지로, 극적 구조와 언어는 진단으로 둔다. |
| 팬터마임과 무언극 | [V&A 팬터마임](https://www.vam.ac.uk/articles/the-story-of-pantomime)은 영국 panto의 관객 참여·희극·무대 변화를 설명한다. mime과 영국 pantomime의 구분을 유지하고, 소리의 부재나 실제 동작의 연속은 사진으로 단정하지 않는다. |
| 장치·조명 | [National Theatre 고보 자료](https://images.nationaltheatre.org.uk/uploads/2023/11/2023-TheWitches-post-show-activity-pack.pdf)와 [스크림 조명 설명](https://theatrecrafts.com/pages/home/topics/lighting/lighting-gauze-scrim/)은 빛 무늬와 막 앞뒤의 관계를 설명한다. 빛의 모양은 묘사할 수 있으나 고보가 원인인지, 페이드가 일어났는지는 별도 관측이 필요하다. |
| 의복 실루엣 | [Met의 18세기 실루엣](https://www.metmuseum.org/ja/essays/eighteenth-century-silhouette-and-support), [Met 파니에 실물](https://www.metmuseum.org/art/collection/search/139668), [V&A 코르셋·크리놀린·버슬](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)은 서로 다른 시대·구조를 보여 준다. 겉 실루엣만 보일 때 내부 지지물의 정체를 확정하지 않으며, 무대 의상은 역사적 복식과 별도로 명시한다. |
| 카바레·버레스크 | [Burlesque Hall of Fame 소장품](https://burlesquehall.com/press/), [미국 버레스크 역사](https://burlesquehall.com/exhibition/permanent-exhibition-spectacular-erotic-and-slightly-shocking-a-timeline-of-american-burlesque/)는 팬·장갑·보아·소도구와 시대에 따른 형식 변화를 보여 준다. 성인 버레스크의 선택지와 일반 카바레·레뷔·드래그를 별도 취급한다. 한 소품이 장르나 실제 동의를 입증하지 않는다. |
| 폭력·분장 | [RSC 소품](https://www.rsc.org.uk/about-us/how-we-make-theatre/props)과 [RSC 의상 효과](https://www.rsc.org.uk/blogs/out-of-the-spotlight/costume-effects)는 제작·의상 얼룩·모형을 설명한다. 무대 폭력, 상처 효과, 실제 부상과 사건의 원인을 분리한다. 잔혹극을 유혈의 동의어로 사용하지 않는다. |
| 한국 공연 | [UNESCO 탈춤](https://ich.unesco.org/en/RL/talchum-mask-dance-drama-in-the-republic-of-korea-01742), [국립국악원 판소리](https://www.gugak.go.kr/ency/topic/view/1327), [고수](https://www.gugak.go.kr/ency/topic/view/1575), [남사당놀이](https://ich.unesco.org/doc/src/06859-EN.pdf)를 토대로 마당·가면·소리꾼과 고수·인형의 관계를 분리한다. 지역 탈이나 작품을 무근거로 지정하지 않는다. |
| 일본 공연 | [노가쿠 자료](https://ich.unesco.org/doc/src/00010-EN.pdf), 일본 예술문화진흥회의 [하나미치](https://www2.ntj.jac.go.jp/dglib/modules/kabuki_dic_en/entry.php?entryid=1245), [미에](https://www2.ntj.jac.go.jp/unesco/kabuki/en/production/scene4.html), [히키누키](https://www2.ntj.jac.go.jp/unesco/kabuki/en/production/performance1.html), [분라쿠 조종 구조](https://www2.ntj.jac.go.jp/unesco/bunraku/en/doll/doll2.html)를 바탕으로 한다. 노·교겐·가부키·분라쿠를 섞지 않고 가면이나 구마도리를 전 역할에 강제하지 않는다. 히키누키의 한 화면은 빠른 변화 자체를 입증하지 않는다. |
| 중국 공연 | [UNESCO 경극](https://ich.unesco.org/en/RL/peking-opera-00418)은 노래·낭송·연기·무술, 양식화한 동작, 의상과 분장의 맥락을 설명한다. 특정 분장의 색과 인물 성격을 만능 규칙으로 처리하지 않고, 긴 소매의 가시 구조와 배역·전통의 판정을 분리한다. |

## 데이터 설계와 판정

* 새 모듈은 기존 T01~T26을 수정하거나 대체하지 않는다. 키워드·양성 선택지·맥락 진단을 분리하고, 키워드가 전체 선택지를 자동으로 강제하지 않는다. 모든 양성 후보는 사람·소품의 소유자와 수, 가능한 접촉·간격 및 위치를 완결된 한영 문장으로 지정한다.
* 성적 맥락의 개별 후보는 해당 공연자를 명시적 성인으로 작성하고 `requires_adult_context` 조건을 둔다. 이 boolean은 각 인물의 나이를 입증하는 증거가 아니다. 요청에 실제 성인 사실과 사용 권한이 없으면 전체 적용을 승인하지 않는다. 일반 카바레와 드래그 자체를 성적 장면이나 성인으로 일괄 분류하지 않는다.
* 폭력과 상처의 표현을 장르나 소재라는 이유로 누락하지 않되 실제 폭행·합의·고통·사망·진행 과정은 한 장면만으로 확정하지 않는다. 무대 장치의 연결점이 가려졌다면 관찰 불가로 기록한다.
* 지역·시대·배역이 출처로 특정되지 않은 경우는 일반적 무대 연출 또는 해당 전통에서 영감을 받은 예시로만 둔다. 출처는 원칙과 유형의 근거이며, 개별 후보의 정확한 장면·색상·배우 수에 대한 기록이 아니다.
* 기술 검사·검색 노출·원본 의미 승인·프롬프트 채택·화소 재현·사용자 수용을 서로 다른 증거로 남긴다.
