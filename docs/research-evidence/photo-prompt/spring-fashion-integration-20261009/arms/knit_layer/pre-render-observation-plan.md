# A arm 사전 픽셀 평가표

컨셉: 강변 인쇄 공방의 첫 도판과 봄바람
Core: `97ece69a1d3d842933a440b9a99891dd640e1cf943a85509f06b72787c61f3b3`

현재 단계는 READY 전 관찰 준비다. 원문·locks·baseline은 유지하며, 아래 의복 구조와 장면은 authorial/optional 선택이다. 최종 hard gate 집합은 pack·audited composed selection·review-shape에서 파생한다. 이 표 자체는 새 hard gate를 만들지 않는다.

권장 관찰: 정면에 가까운 약한 3/4 투영, 머리부터 종아리 중간까지의 세로 구도, 종이는 몸판 옆에 두어 니트·이너 경계와 손 접촉을 함께 볼 수 있게 한다. 방향·높이·구도는 열린 작가 선택이다.

| 항목 | 관찰할 관계 | 성공 근거 | 실패·미관찰 경계 |
| --- | --- | --- | --- |
| O01 Actual open knit cells | outer vest yarn paths → true gaps → independently declared blouse surface | Opaque connected yarn bounds actual open gaps, and a separate surface is visible through them in this one image. | Unresolved yarn paths or openings hidden behind paper/arms cannot pass. |
| O02 Yarn, blouse and camisole are separate owners | outer knit vest → sheer blue blouse → opaque sage camisole | The three distinct clothing surfaces show one consistent exterior-to-interior order rather than a flat combined print. | If the lower surface cannot be owned, record unobservable instead of inferring it from the prompt. |
| O03 One sheer panel crosses the camisole boundary | blue blouse upper chest → camisole straight upper edge → same blouse over sage body | A visibly continuous blue textile layer transmits skin above the solid inner-top edge and sage cloth below it; the inner edge has a concrete owner. | A concealed inner edge or unresolved blue textile makes this observation fail for visibility. |
| O04 Sleeve fabric transmission | blue sleeve textile → same wearer arm skin; cuff → sleeve | Positive blue cloth continuity and softened underlying arm tone remain readable together; cuffs belong to the same sleeves. | A sleeve wholly in dark shadow or cropped out is unobservable. |
| O05 Raised rib edges versus holes | vest neckline/hem ribbed bands → same vest openwork body | Dense ribbed bands have actual raised/recessed yarn structure and visibly join the same openwork vest. | A band that is visually smooth or fully obscured cannot establish rib topology. |
| O06 Hem order | outer vest ribbed hem → blouse strip → skirt upper edge | The three actual garment boundaries preserve the stated overlap order and reveal the intervening blouse strip. | Any missing boundary makes the complete three-edge relationship unobservable. |
| O07 Pleats and wrap edge belong to one skirt | skirt folded ridges/recesses → same skirt diagonal crossing front edge | Actual folded fabric creates broad vertical pleats while a distinct front crossing boundary belongs to the same skirt. | Do not infer a wrap layer from a diagonal shadow or a pleat label. |
| O08 Upper clip contact | same woman right thumb/index → spring clip → paper dry upper margin and taut drying line | The fingers coherently operate the actual clip; its jaws engage the paper margin and line in one load-bearing contact arrangement. | A hidden jaw-to-paper/line relation is a visibility failure, not proof of an impossible mechanism. |
| O09 Lower paper support and body chain | same woman left thumb/fingertips → dry lower paper corner; shoulders/elbows → both hands | A distinct left hand holds the dry lower corner while a plausible connected arm chain reaches it; it does not merge into the print or right hand. | Hidden consequential support is unobservable; ordinary foot support may remain outside the mid-calf crop. |
| O10 Meaning of the practical moment | open window and lifted curtain → curling free paper corner → stabilized held corner and attention toward upper clip | The image supports an understandable paper-stabilizing action, with a visible reason to handle the sheet now; the richer backstory remains an authored inference. | A missing story link is supplemental scene weakness rather than an invented profile gate. |
| O11 Reference-guided face and short black bob | attached source photograph → generated subject visible face/hair guidance | Source-guided facial cues, short black bob and wispy fringe remain recognizable as appearance guidance at the selected portrait distance. | A profile-hidden face or unresolved hair is not reference fidelity proof. |
| O12 Whole image impression and controls | subject bearing/expression + practical setting + material hierarchy | Describe the actual impression, subject presence and hierarchy first; separately compare with subtle sensual support, ordinary causality and restrained creativity. | Artistic weakness stays qualitative even when technical gates pass. |

원본 해상도에서 확인하며, 필수 계약의 부분 충족이나 가려진 관계는 fail로 기록한다. prompt·runtime·index PASS는 픽셀 성공을 대신하지 않는다. 전체 인상과 이야기 연결, control의 지각적 표현은 supplemental 관찰이며 사용자 수락은 아직 받지 않았다.

READY 이후에만 같은 generation으로 retrieve → compact view/full selected detail → compose audit → native runtime audit/plan → native 1회 → actual result recording → exact review-shape → native pixel review/audit를 실행한다.
