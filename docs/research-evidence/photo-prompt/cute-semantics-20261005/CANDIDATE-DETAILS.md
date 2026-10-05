# 대표 후보의 구체적인 작성안

다음 14건은 [78개 후보 초안](CANDIDATE-DRAFTS.json)과 [22개 맥락 패턴](SEMANTIC-UNITS.json) 중 중요한 관계·변형을 더 구체적으로 풀어 쓴 연구자 제안이다. 영어 문장도 검토용 초안이다. 선택한 구현의 형상을 설명하며, 문화 이름의 유일한 정의나 현재 런타임 필드의 완성본으로 취급하지 않는다. 실제 작성 시 한·영 설명의 동등성, guard, 효과 속성, 변형 근거를 함께 심사한다.

## 27. 한쪽 볼 부풀림

기존 `pv_puffed_cheeks`와 다른 것은 양쪽이 아닌 **지정한 한쪽**의 상대적 팽창이다. 영구 얼굴 비대칭이나 체형을 뜻하지 않는다.

> The declared left or right cheek has an outward rounded expansion, while the opposite cheek retains its comparatively resting contour; the lips remain closed.

성분은 팽창한 볼, 반대 볼의 비교 윤곽, 닫힌 입술이다. `actor.face.left/right.cheek`를 행위자 기준으로 고정한다. 영상의 좌우 반전과 카메라 쪽의 가까운 볼은 같은 속성이 아니다. `expression` 효과로 작성하고 고정된 `body_geometry`·age를 바꾸지 않는다. 양 볼 부풀림·볼 가림·한쪽 얼굴 확대가 대조 실패다.

## 35. 엄지·검지 교차형 손하트

기존 보류 항목의 재심사 대상이다. 손 이름만 추가하지 않고 교차형 변형의 관찰 형태와 다중 용례를 심사한다. [Unicode의 원 제안서](https://www.unicode.org/L2/L2019/19327-thumb-index-crossed.pdf)는 같은 제스처의 금전·손하트 용례를 다룬다.

> The thumb and index finger of the same declared hand cross over a short visible overlap; the remaining fingers fold toward that palm, and the crossing is readable from the chosen viewing side.

엔티티는 같은 손의 엄지·검지·나머지 손가락·손목이다. `crosses(thumb,index)`와 각 손가락의 동일 손 소유를 선언한다. 작은 하트 물체·검지중지 교차·엄지검지 집기와 구분한다. 손의 어느 면을 보일지 명시해야 하며 필수 교차가 소매 뒤에 가려지면 통과가 아니다. 금전 문맥을 손하트 의도로 바꾸지 않는다.

## 36. 양손 하트의 한 가지 topology

아래는 엄지와 검지의 외곽을 사용하는 **선택된 변형**이다. 다른 손하트의 정의로 확대하지 않는다.

> Each index finger curves along one upper side of the heart outline; the two hands meet at the declared upper and lower junctions, leaving one readable heart-shaped opening between them.

양손의 각 윤곽, 두 중앙 접점, 하나의 내부 빈 공간을 분리한다. 실제 변형 심사에서 어느 손끝끼리 닿는지 확인해 `meets(finger_A,finger_B)`를 작성한다. 모든 변형에 엄지 접촉을 강제하지 않는다. 두 주먹·기도 손·별도 하트 소품은 실패 대조다. 손가락 전체를 안 보이게 덮고 하트라는 이름만 남겨서는 안 된다.

## 37. 볼 윤곽을 사용하는 볼하트 변형

명명된 용례와 손가락 세부 형태의 근거를 구분한다. 아래는 손의 C형 윤곽과 볼 윤곽을 연결하는 연구 구현안이며, 원본 변형 대조 후 승격한다.

> A curved contour made by the declared hand sits beside the cheek; from the chosen viewpoint, that contour and the cheek boundary form the selected heart outline, with contact or a small gap recorded explicitly.

`projected_contour_continuity(hand,cheek)`와 `physical_contact(hand,cheek)`는 별개다. 화면상 곡선이 이어지는 요청을 실제 손-볼 접촉으로 바꾸지 않는다. 볼 콕·충치 포즈·볼 전체 가림과 대조한다. 미리 고정된 시점으로 해당 윤곽이 안 읽힌다면 카메라를 몰래 바꾸지 않고 부적합 또는 관찰 불가로 남긴다.

## 52. 양 검지 끝 맞대기

> The two index fingers extend from separate hands and meet tip to tip at the declared position; both wrists connect to their own forearms near the body.

각 손의 검지, 검지 끝 두 개의 접점, 각각의 손목·전완 연결을 검증한다. 자기 두 손인지 다른 사람의 손인지 원 요청에서 정한다. 엄지검지 손하트·손바닥 맞대기·끝이 떨어진 두 검지는 다른 상태다. 접점을 읽힐 범위가 남아야 하며, 이 형태만으로 실제 망설임·수줍음·동의를 확정하지 않는다.

## 73. 상대 소매 끝 잡기

> Actor A's thumb and index finger pinch the end of actor B's sleeve; that cloth edge continues to B's arm, while A's hand connects to A's wrist and forearm.

`owns(A,hand_A)`, `wears(B,sleeve_B)`, `pinches(hand_A,sleeve_B)`를 분리한다. 작은 잡기인지 당기는 위상인지도 선택해야 한다. 실제 힘의 크기는 사진에서 측정할 수 없다. 자기 소매·상대 손·분리된 천·잘못된 팔로 전이하면 실패다. `action/pose/relationship`과 실제 바뀌는 옷/물체 속성을 모두 검토하고, 단독 인원 고정을 우회해 B를 추가하지 않는다.

## 77. 두 사람의 공동 하트

> Actor A contributes one declared half of the outline and actor B contributes the complementary half; their selected endpoints meet around one shared heart-shaped opening.

서로 다른 A·B의 각 절반과 하나의 공동 외곽을 검증한다. 두 사람이 각자 하트를 만드는 장면과 다르고, 한 사람의 양팔 하트도 다르다. 팔로 만든 변형·손으로 만든 변형을 한 topology로 섞지 않는다. 중앙 접점과 각 팔의 소유를 별도 gate로 두어 세 번째 손·몸을 관통하는 팔·잘린 중심을 잡는다.

## 83. 등 뒤 선물과 관찰 가능성

> The declared hand holds the gift behind the actor's torso; a readable portion of that same gift remains visible to the camera, with its connection to the holding hand preserved.

`behind(gift,torso)`와 `holds(hand,gift)`, 관찰자에게 남는 가시 범위를 분리한다. 수신자가 요청됐다면 수신자 시점에서의 가림도 따로 선언한다. 단독 인물에 수신자를 자동 추가하지 않는다. 선물을 뒤 배경 상자로 옮기거나 완전히 삭제하면 실패다. 카메라를 고정한 상태에서 손-선물의 필수 접점이 완전히 숨는다면 관찰 불가로 평가한다.

## 95. 수직에 가까운 탑다운

> The camera observes the declared subject and surrounding plane from above along a near-vertical downward axis; their projected overlap follows that viewpoint consistently.

관찰점의 높이·시선축과 몸의 방향·인물의 홍채 방향을 독립적으로 기록한다. 인물의 몸 비례를 바꾸지 않는다. 일반 하이앵글·멀리서 넓게 보는 버드아이 범위·flat-lay 행동·단순 고개 숙임은 각각 다른 상태다. `camera`와 바뀌는 `composition/framing` 효과를 모두 심사한다.

## 109. 일반 캐치라이트의 중립 원자

`glossy_wet_catchlight_eyes`는 젖어 보이는 눈이 추가된 기존 후보다. 아래처럼 일반 반사광을 설명하는 원자와 동등하다고 무조건 확장하지 않는다. [캐치라이트의 직접 설명](https://www.sandracoaneducation.com/blog/catchlights-what-they-are-and-what-they-can-teach-us-about-light)

> A small specular patch lies within the visible eye surface; its declared shape and placement are compatible with the chosen light direction, while the iris and eyelid boundaries remain readable.

안구 표면·반사 패치·선언한 광원의 방향 관계를 검증한다. 상부 반사, 여러 반사, 특정 광원 모양은 변형값이다. 수직 두 반사를 일반 정의로 고정하지 않는다. 별 그래픽·동공 발광·눈물 고임은 다른 성분이다. 기대감·진실한 감정·정확한 광원 개수의 증거로 확대하지 않는다.

## 128. 성인의 관능과 귀여움의 복합 맥락

이 항목은 한 포즈의 새 원자보다 두 의미 축을 보존하는 선택형 조합이다.

> Preserve the explicitly requested adult appeal cue and a separate, readable cute cue in the same scene; keep the declared age, identity, body proportions and wardrobe constraints.

실제 candidate를 작성할 때는 `요청한 관능 cue가 어떤 표정·자세·빛인가`와 `귀여운 cue가 어떤 손동작·형태·행동인가`를 먼저 구체화한다. 후보의 선택은 그 둘을 모두 보존할 때만 성립한다. 큰 눈·작은 몸·유아 비례·추가 노출을 자동 cue로 삼지 않는다. 기존 adult/flirt guard와 `sexual_tone` 및 실제 carrier 차원의 고정을 심사한다. 관능을 삭제하고 리본만 남기거나, 반대로 귀여운 동작을 삭제하면 실패다.

## 135. 야미카와이의 상징 층

아래는 **상징을 의복에 인쇄하는 요청**의 구현이다. 용어 전체를 인쇄물·의료품으로 제한하거나 실제 사건 요청까지 이 변형으로 바꾸지 않는다. [창작자의 설명](https://harajuku-pop.com/67775/)

> The chosen pastel or dreamlike visual layer and the explicitly requested dark motif remain readable on the same declared garment surface; the motif retains its printed or attached material layer.

밝은 조형·어두운 모티프·소유 표면을 독립 gate로 둔다. 모티프는 원 요청이 선택한 의료·불안·폭력 등의 범위에서 구체화한다. 단순 의료품으로 축소하거나 실제 병력·자해 사건을 추정하지 않는다. 피부 위 인쇄와 실제 상처도 같은 후보로 취급하지 않는다. 어두운 상징 층 없이 색만 맞추거나 밝은 층 없이 어두운 의복만 남기는 것은 실패다.

## 136. 구로카와이의 조형물 변형

> The small rounded plush form and the requested blood, bone or stitched-body motif coexist on the declared object; each motif stays attached to the chosen material surface.

작고 둥근 봉제 형상, 요청한 신체 모티프, 동일 물체 표면의 소유·부착을 분리한다. 붕대만 붙인 일반 봉제인형이 모든 구로 요청의 대체는 아니다. 인쇄·패치·조형·실제 신체 손상을 구체 요청에 따라 분리한다. 실제 사람·동물에 같은 모티프를 전이하지 않는다. 귀여움과 신체 모티프 중 어느 한 층이 사라지면 실패다.

## 5. 갭모에의 관계 패턴

이 항목은 78개 국소 후보 초안과 별도로 다룬 22개 맥락 패턴에 속한다. 현재 character의 기존 대비 family와 일반 actor-target-response 구조를 재사용할지 심사한다.

> A visible surface attitude contrasts with the same actor's declared action toward the same target; the immediate visible consequence makes the action readable without requiring a fixed costume or prop.

`actor / surface_affect / target / primary_action / visible_response / immediate_consequence`를 명시한다. 특정 정장·인형·미소를 정의로 만들지 않는다. 행동의 대상과 표면 태도의 관련 대상이 서로 무관한 장면은 별도로 심사한다. 성격의 과거·숨은 마음은 사실 gate로 삼지 않는다. 관찰 가능한 대비가 요청한 갭모에 인상으로 읽히는지는 형태 gate 이후 사람의 평가로 판단한다.
