#!/usr/bin/env python3
"""Author bounded non-BDSM fashion-parts research artifacts, without manifest mutation."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[3]
SKILL=ROOT/'photo-prompt-image-generator'
# __file__ parents[3] is skills/; SKILL is its child
ASSETS=SKILL/'assets'; PLAN=SKILL/'references/fashion-visual-semantics-research-plan-20261108.md'
sys.path.insert(0,str(SKILL/'scripts'))
import photo_candidate_retrieval_views as rv
import photo_candidate_corpus as corpus

def H(x):return hashlib.sha256(x.encode()).hexdigest()
def sh(o):return H(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False))
def dump(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
# Each row is an independently authored, specific visual proposition, not a universal definition.
raw='''7-1|boning|보닝|garment_detail|On an opened garment, a narrow reinforcing strip is visible inside a stitched fabric channel.|펼쳐진 의복 안쪽에서 길쭉한 보강 심재가 봉제된 천 통로 안에 보인다.
7-1|bone channel|보닝 채널|garment_detail|Two parallel vertical stitch lines outline a narrow channel on the front of a fitted bodice.|맞는 보디스 앞면에서 두 개의 평행한 세로 봉제선이 좁은 채널을 이룬다.
7-1|busk|버스크|garment_detail|At the center front of a corset, a vertical row of small loops fastens to a corresponding row of studs.|코르셋 앞 중심에서 작은 고리들이 맞은편 돌기 줄에 세로로 채워져 있다.
7-1|lacing|레이싱|garment_detail|A cord crosses repeatedly between two parallel rows of eyelets on the back of a bodice.|보디스 뒤쪽의 평행한 두 아일릿 줄 사이로 끈이 반복해 교차한다.
7-1|lacing gap|레이싱 갭|garment_detail|A narrow vertical opening remains between the two laced edges on the back of a corset.|코르셋 뒤쪽의 끈으로 묶인 양 가장자리 사이에 좁은 세로 틈이 남아 있다.
7-1|eyelet|아일릿|garment_detail|A small metal-rimmed hole is visible at the edge of a fabric panel with a cord passing through it.|천 패널 가장자리의 작은 금속 테두리 구멍에 끈이 통과한다.
7-1|grommet|그로밋|garment_detail|A round reinforcing ring surrounds a hole at the edge of a cloth panel.|천 패널 가장자리의 구멍 둘레를 둥근 보강 고리가 감싼다.
7-1|modesty panel|모디스티 패널|garment_detail|Behind the crossed lacing, a fabric panel spans the gap between the two edges of the corset.|교차한 끈 뒤에서 천 패널이 코르셋 양 가장자리 사이의 틈을 가린다.
7-1|waist tape|웨이스트 테이프|garment_detail|Inside an opened corset, a narrow horizontal tape follows the waist across several fabric panels.|펼친 코르셋 안쪽에서 좁은 가로 테이프가 여러 천 패널을 가로질러 허리선을 따른다.
7-1|panel|패널|garment_detail|Curved seams join adjacent shaped fabric panels on a fitted bodice.|맞는 보디스에서 곡선 솔기가 모양을 낸 천 패널들을 이어 준다.
7-1|cup|컵|garment_detail|Two separately shaped fabric cups meet at the center of a structured top.|구조가 잡힌 상의에서 각각 형태를 낸 두 천 컵이 가운데에서 만난다.
7-1|underwire|언더와이어|garment_detail|On an opened garment, a curved support wire is visible along the lower edge of one cup.|펼친 의복에서 곡선형 지지 와이어가 한쪽 컵의 아래 가장자리를 따라 보인다.
7-1|center gore|센터 고어|garment_detail|A small fabric bridge joins the inner edges of two cups at the front center.|작은 천 연결부가 앞 중앙에서 두 컵의 안쪽 가장자리를 잇는다.
7-1|underband|언더밴드|garment_detail|A continuous band runs horizontally beneath both cups and around the torso.|양쪽 컵 아래에서 연속된 밴드가 몸통 둘레를 가로로 감싼다.
7-1|shoulder strap|어깨끈|garment_detail|A narrow strap extends from the front of the top over the shoulder toward the back.|가는 끈 하나가 상의 앞에서 어깨를 넘어 등 쪽으로 이어진다.
7-2|buckle|버클|garment_detail|A flat strap passes through a rectangular buckle on the front of a belt.|평평한 끈이 벨트 앞면의 사각 버클을 통과한다.
7-2|strap adjuster slider|끈 조절 슬라이더|garment_detail|A small rectangular slider sits on a folded segment of the shoulder strap.|작은 사각 슬라이더가 어깨끈의 접힌 부분에 놓여 있다.
7-2|D-ring|D링|garment_detail|A D-shaped metal ring joins two visible fabric straps on a bag.|D자 모양 금속 고리가 가방의 두 천 끈을 잇는다.
7-2|O-ring|O링|garment_detail|A circular metal ring joins two straps on the side of a garment.|원형 금속 고리가 의복 옆면의 두 끈을 잇는다.
7-2|stud|스터드|garment_detail|Small rounded studs appear in a row on the edge of a jacket pocket.|작은 둥근 스터드 장식들이 재킷 주머니 가장자리에 줄지어 있다.
7-2|spike|스파이크 장식|garment_detail|Short pointed studs project outward along the edge of a jacket lapel.|짧고 뾰족한 장식이 재킷 깃 가장자리를 따라 바깥으로 돌출된다.
7-2|rivet|리벳|garment_detail|A small metal rivet is visible at the corner where two denim panels overlap.|두 데님 조각이 겹치는 모서리에 작은 금속 리벳이 보인다.
7-2|exposed zipper|노출 지퍼|garment_detail|The zipper teeth and fabric tape remain visible along the front opening of a jacket.|재킷 앞 여밈을 따라 지퍼 톱니와 지퍼 테이프가 바깥에 드러난다.
7-2|hook-and-eye|후크 앤드 아이|garment_detail|A small metal hook catches a matching eye along the edge of a garment opening.|작은 금속 갈고리가 의복 여밈 가장자리의 맞은편 고리에 걸려 있다.
7-2|cutout|컷아웃|garment_detail|A geometric opening interrupts the fabric at one shoulder of a long-sleeved top.|긴 소매 상의의 한쪽 어깨에서 기하학적 구멍이 원단을 비운다.
7-2|piping|파이핑|garment_detail|A narrow raised strip follows the curved edge of a jacket collar.|가느다랗게 도드라진 띠가 재킷 칼라의 곡선 가장자리를 따른다.
7-2|scalloped edge|스캘럽 가장자리|garment_detail|A lace hem ends in a repeating sequence of small rounded scallops.|레이스 밑단이 작은 반원 모양의 물결로 반복해 끝난다.
7-2|fringe|프린지|garment_detail|Many short strands hang in a continuous row along the bottom edge of a shawl.|여러 개의 짧은 실 가닥이 숄 아래 가장자리를 따라 연속으로 늘어진다.
7-2|tassel|태슬|garment_detail|A bundled tassel hangs from the end of a single decorative cord.|한 가닥 장식 끈의 끝에 실을 묶은 태슬이 늘어진다.
8-1|stockings|분리형 스타킹|wearable_accessory|Two separate stockings cover the legs, each ending in its own visible upper band.|양다리를 덮은 두 스타킹이 각각 독립된 윗밴드에서 끝난다.
8-1|tights|타이츠|wearable_accessory|Opaque hosiery covers both legs and joins into one continuous waist section.|불투명한 호지어리가 양다리를 덮으며 한 벌의 허리 부분으로 이어진다.
8-1|pantyhose|팬티호스|wearable_accessory|Sheer hosiery covers both legs and connects continuously to the waist.|비치는 호지어리가 양다리를 덮고 허리까지 한 벌로 이어진다.
8-1|hold-ups stay-ups|홀드업 스테이업|wearable_accessory|A wide top band encircles the upper edge of each separate stocking, with no supporting strap visible.|분리된 각 스타킹의 윗단을 넓은 밴드가 둘러싸며 지지 끈은 보이지 않는다.
8-1|thigh-high|사이하이 길이|wearable_accessory|The top edge of one stocking reaches the wearer's upper thigh.|한쪽 스타킹의 윗가장자리가 착용자의 허벅지 위쪽에 닿는다.
8-1|garter belt suspender belt|가터 벨트|wearable_accessory|A belt around the waist supports several straps that extend toward the tops of separate stockings.|허리 둘레의 벨트에서 여러 끈이 각각 분리된 스타킹의 윗단 쪽으로 내려간다.
8-1|garter strap|가터 스트랩|garment_detail|A narrow strap runs down from a waist belt to the upper edge of a stocking.|가는 끈이 허리 벨트에서 스타킹의 윗가장자리까지 아래로 이어진다.
8-1|garter clip|가터 클립|garment_detail|A small clip at the end of a hanging strap grips the upper band of a stocking.|내려온 끈 끝의 작은 클립이 스타킹 윗밴드를 잡고 있다.
8-1|welt|스타킹 웰트|garment_detail|A wide reinforced band forms the upper edge of a stocking.|넓게 보강된 밴드가 스타킹의 윗가장자리를 이룬다.
8-1|lace top|스타킹 레이스 윗단|garment_detail|A patterned openwork lace band encircles the top of a stocking.|무늬가 있는 성긴 레이스 밴드가 스타킹 윗단을 둘러싼다.
8-1|back seam|스타킹 백심|garment_detail|A narrow dark line runs vertically along the back of one stocking from ankle toward the upper band.|한쪽 스타킹 뒤쪽에서 가는 어두운 선이 발목부터 윗밴드 쪽으로 세로로 이어진다.
8-1|ripped hosiery|찢어진 스타킹|garment_detail|An irregular tear interrupts the surface of a stocking at one knee.|한쪽 무릎의 스타킹 표면이 불규칙하게 찢어져 있다.
8-1|laddered hosiery|올이 나간 스타킹|garment_detail|A narrow vertical run extends from a small snag in the knitted stocking.|편성 스타킹의 작은 올 손상에서 가느다란 세로 올풀림이 이어진다.
8-2|stiletto heel|스틸레토 힐|wearable_accessory|A shoe has a long slender heel beneath its rear edge.|신발 뒤쪽 아래에 길고 가느다란 굽이 있다.
8-2|platform sole|플랫폼 밑창|wearable_accessory|A thick platform sole is visible beneath the front of a shoe.|신발 앞부분 아래에 두꺼운 플랫폼 밑창이 보인다.
8-2|knee-high boot|니하이 부츠|wearable_accessory|The shaft of a boot ends near the wearer's knee.|부츠 통이 착용자의 무릎 부근에서 끝난다.
8-2|over-the-knee boot|오버더니 부츠|wearable_accessory|A boot shaft rises beyond the top of the wearer's knee.|부츠 통이 착용자의 무릎 위까지 올라온다.
8-2|thigh-high boot|사이하이 부츠|wearable_accessory|A boot shaft extends up the wearer's thigh.|부츠 통이 착용자의 허벅지까지 길게 이어진다.
8-2|lace-up boot|레이스업 부츠|wearable_accessory|A cord crisscrosses through eyelets along the front of a boot shaft.|부츠 통 앞면에서 끈이 아일릿을 지나며 엇갈려 교차한다.
8-2|ankle strap|앵클 스트랩|wearable_accessory|A narrow strap encircles the ankle and connects to the sides of a shoe.|가는 끈이 발목을 한 바퀴 두르고 신발 양옆에 연결된다.
8-2|pointed toe|포인티드 토|wearable_accessory|The front of a shoe tapers to a pointed toe.|신발 앞부분이 점점 좁아져 뾰족한 앞코로 끝난다.
8-2|boot shaft|부츠 샤프트|garment_detail|The tall upper shaft of a boot surrounds the lower leg above the ankle.|부츠의 긴 통 부분이 발목 위쪽의 종아리를 감싼다.
8-2|shoe vamp|신발 뱀프|garment_detail|The front upper panel of a shoe covers the top of the foot.|신발 앞쪽의 갑피 조각이 발등을 덮는다.
8-2|shoe heel|신발 굽|garment_detail|A distinct heel raises the rear of a shoe above the ground.|구별되는 굽이 신발 뒤쪽을 바닥 위로 들어 올린다.
8-2|shoe sole|신발 밑창|garment_detail|The edge of a flat sole runs beneath the full length of a shoe.|평평한 밑창의 가장자리가 신발 전체 길이 아래로 이어진다.
9|choker|초커|wearable_accessory|A short necklace rests close to the base of the wearer's neck.|짧은 목걸이가 착용자의 목 아래 둘레에 가깝게 놓인다.
9|collar|일반 의복 칼라|garment_detail|A folded fabric collar frames the neckline of a shirt.|접힌 천 칼라가 셔츠 목둘레를 따라 놓인다.
9|cuff|소맷단 커프|garment_detail|A folded cuff finishes the end of the shirt sleeve at the wrist.|접힌 커프가 손목에서 셔츠 소매 끝을 마감한다.
9|opera gloves|오페라 장갑|wearable_accessory|A long glove covers the hand and extends above the elbow.|긴 장갑이 손을 덮고 팔꿈치 위까지 이어진다.
9|fingerless gloves|핑거리스 장갑|wearable_accessory|A glove covers the palm while leaving the fingers exposed beyond its openings.|장갑이 손바닥을 덮고 손가락은 구멍 밖으로 드러난다.
9|mask|가면|wearable_accessory|A decorative half mask covers the area around the eyes while leaving the lower face visible.|장식 반가면이 눈 둘레를 덮고 얼굴 아래쪽은 드러낸다.
9|hood|후드|wearable_accessory|A fabric hood surrounds the back and sides of the head with the face visible at its opening.|천 후드가 머리 뒤와 옆을 감싸고 앞쪽의 열린 부분으로 얼굴이 보인다.
9|decorative chain|장식 체인|garment_detail|A short chain of linked metal loops decorates the edge of a jacket pocket.|금속 고리가 이어진 짧은 체인이 재킷 주머니 가장자리를 장식한다.
9|padlock motif|자물쇠 모티프|wearable_accessory|A small padlock-shaped ornament hangs from a necklace.|작은 자물쇠 모양 장식이 목걸이에 매달려 있다.
2-1|foot|발|body_pose|A bare foot rests flat on the floor with the toes visible from above.|맨발 하나가 바닥에 평평하게 놓이고 위에서 발가락이 보인다.
2-1|hand|손|hand_pose|One open hand rests on a tabletop with the fingers gently separated.|한쪽 손이 손가락을 살짝 벌린 채 탁자 위에 놓인다.
2-1|leg|다리|body_pose|Both legs are visible in profile from hip to ankle.|두 다리가 엉덩이부터 발목까지 옆모습으로 보인다.
2-1|neck nape|목 목덜미|body_region|The back of the neck is visible below a short haircut.|짧은 머리 아래로 목덜미가 보인다.
2-1|navel|배꼽|body_region|The navel is visible near the center of the abdomen.|복부 중앙 부근에 배꼽이 보인다.
2-1|hair|머리카락|hair_style|A short straight bob frames the face and ends near the jaw.|짧고 곧은 단발머리가 얼굴을 감싸고 턱 부근에서 끝난다.
2-1|body hair|체모|body_hair|Fine body hair is visible on a forearm in a close view.|가까운 화면에서 팔뚝의 가는 체모가 보인다.
2-1|nail|손톱|nail_appearance|The fingernails are painted an even dark red with glossy reflections.|손톱에 고르게 칠한 짙은 붉은 색과 광택 반사가 보인다.
2-1|muscle|근육|body_form|The outline of a flexed forearm muscle is visible as the arm bends.|팔을 굽힌 상태에서 팔뚝 근육의 윤곽이 보인다.
2-1|size difference|체격 차이|scale_relation|Two adults stand side by side, with one visibly taller than the other.|성인 두 명이 나란히 서 있고 한 사람이 다른 사람보다 눈에 띄게 크다.
2-1|tattoo|문신|body_marking|A dark floral tattoo is visible on the outside of one forearm.|한쪽 팔뚝 바깥에 어두운 꽃무늬 문신이 보인다.
2-1|piercing|피어싱|wearable_accessory|A small ring earring passes through the visible earlobe.|작은 고리 귀걸이가 보이는 귓불을 통과한다.
2-2|balloon|풍선|prop|A round inflated balloon is held by one hand, with a bright reflection on its curved surface.|둥글게 부푼 풍선을 한 손으로 들고 있으며 곡면에 밝은 반사가 보인다.
2-2|wet and messy|젖음과 오염 상태|garment_detail|A garment has an irregular darker patch beside a lighter section.|의복에서 불규칙하게 더 어두운 부분이 밝은 부분 옆에 있다.'''
notes={
'boning':'심재는 실제로 드러난 경우에만 확인한다. 겉의 채널만으로 재질을 단정하지 않는다.', 'bone channel':'채널 외관과 내부 심재는 별도다.', 'busk':'앞 중심 여밈의 한 사례이며 모든 코르셋의 필수 구조는 아니다.', 'lacing':'끈 여밈은 레이스 직물과 다르다.', 'lacing gap':'간격과 안쪽 패널은 별도 속성이다.', 'eyelet':'구멍과 보강 부속은 문맥에 따라 구분한다.', 'grommet':'아일릿과 크기·용례가 겹친다.', 'modesty panel':'레이싱 뒤 안쪽 천이다. 가려지면 확인 불가.', 'waist tape':'내부 보강 테이프는 겉에서 반드시 드러나지 않는다.', 'underwire':'와이어 자체가 숨겨지면 실제 심재 여부는 미상이다.', 'center gore':'두 컵 사이 중앙 연결부다.', 'underband':'가슴 아래 밴드와 어깨끈은 다르다.', 'D-ring':'장식과 기능을 별도로 기록한다.', 'O-ring':'원형 고리는 장식일 수도 있다.', 'stud':'장식성 돌출과 체결 리벳은 구별한다.', 'rivet':'겉모양만으로 체결 기능이 보장되지는 않는다.', 'fringe':'연속된 가닥 장식이다.', 'tassel':'다발 장식이며 프린지와 다르다.', 'stockings':'각 다리가 분리된 형태의 좁은 영어 용례다. 한국어 사용은 더 넓다.', 'tights':'연결된 허리 부분과 비침은 독립 속성이다.', 'pantyhose':'영어 지역·상업 용례의 차이를 보존한다.', 'hold-ups stay-ups':'상단 자체 고정을 뜻하나 사진에서 끈이 보이지 않는 것만으로 고정 방식을 확정할 수 없다.', 'thigh-high':'길이만 표시하며 고정 방식은 뜻하지 않는다.', 'garter clip':'클립이 스타킹 윗단을 잡는 관계가 보여야 한다.', 'back seam':'실제 봉제선인지 장식선인지는 구별될 수 있다.', 'laddered hosiery':'찢김과 연속된 올풀림은 별도다.', 'stiletto heel':'굽 모양은 앞코 모양과 별도다.', 'platform sole':'앞발 아래 두께는 뒤굽과 별도다.', 'knee-high boot':'통의 높이와 굽 형태는 별개다.', 'over-the-knee boot':'무릎 위라는 범위와 허벅지까지라는 범위는 다르다.', 'thigh-high boot':'허벅지까지 오는 통은 스타킹과 다른 물체다.', 'lace-up boot':'끈과 여밈의 위치를 기록한다.', 'ankle strap':'신발 연결과 발목 위치를 보존한다.', 'pointed toe':'앞코 모양이며 굽 높이가 아니다.', 'shoe vamp':'발등을 덮는 신발 앞 갑피다.', 'choker':'일반 장신구이며 관계나 활동을 추론하지 않는다.', 'collar':'일반 셔츠 칼라의 독립 용례다.', 'cuff':'의복 소맷단이라는 일반 용례다.', 'mask':'얼굴 장식 가면으로 기록하며 감각 제한 용례는 제외한다.', 'hood':'열린 일반 후드이며 가면이나 특정 기능과 같지 않다.', 'decorative chain':'의복 장식으로만 다룬다.', 'padlock motif':'자물쇠 모양 장식일 뿐 관계·기능을 추론하지 않는다.', 'foot':'발의 외형과 발에 대한 취향은 별개다.', 'hand':'손의 외형은 관심이나 의도를 입증하지 않는다.', 'leg':'다리의 외형과 관심은 별개다.', 'neck nape':'목과 목덜미는 범위가 다르다.', 'navel':'배꼽의 가시성과 관심은 별개다.', 'hair':'머리카락의 길이·형태와 관심은 별개다.', 'body hair':'체모와 두발을 분리한다.', 'nail':'손톱과 발톱을 맥락에 따라 구분한다.', 'muscle':'근육 윤곽만으로 활동이나 신체 상태를 단정하지 않는다.', 'size difference':'성인 둘 사이 비교이며 감정·권한 관계를 뜻하지 않는다.', 'tattoo':'문신 외관만으로 정체성이나 제작 과정을 알 수 없다.', 'piercing':'실제 구멍을 통과하는 모습과 장식 부착은 다르다.', 'balloon':'소재·형태·반사와 소리·취향은 별도다.', 'wet and messy':'젖음의 시각적 상태는 wetlook 표면 표현과 다르며 맥락이 실제 젖음을 명시할 때만 적용한다.'}
# Context-only terms preserve nonvisual concepts without asserting a picture proves them.
context_only=[('2-1','foot fetish podophilia','발에 대한 관심이며 발이 보인다는 사실은 그 관심을 입증하지 않는다.'),('2-1','hand fetish','손에 대한 관심과 손의 외형은 별도다.'),('2-1','leg fetish','다리에 대한 관심과 다리의 외형은 별도다.'),('2-1','neck nape fetish','목이나 목덜미에 대한 관심과 보이는 부위는 별도다.'),('2-1','navel fetish','배꼽에 대한 관심과 그 부위의 외형은 별도다.'),('2-1','hair fetish trichophilia','두발에 대한 관심과 머리 모양은 별도다.'),('2-1','body-hair fetish','체모에 대한 관심과 체모가 보이는 상태는 별도다.'),('2-1','nail fetish','손발톱에 대한 관심과 손발톱의 형태는 별도다.'),('2-1','muscle fetish','근육에 대한 관심과 근육 윤곽은 별도다.'),('2-1','size-difference kink','성인 체격 대비에 대한 관심과 보이는 키·체형 차이는 별도다.'),('2-1','tattoo piercing fetish','문신·피어싱에 대한 관심과 장식의 외형은 별도다.'),('2-1','scent odor fetish','후각에 대한 관심은 사진만으로 확인할 수 없다.'),('2-1','voice kink','목소리에 대한 관심은 정지 사진에서 직접 확인할 수 없다.'),('2-1','texture interest','촉각 선호와 사진에서 보이는 표면은 다르다.'),('8-1','denier','실의 선밀도 단위이며 사진의 비침만으로 숫자를 확정할 수 없다.'),('8-2','ballet boots fetish pointe shoes','발끝이 아래로 뻗은 극단적 형태를 일반 발레 토슈즈와 구별한다. 시각 예시는 근거 보류.'),('2-2','shoe footwear fetish','신발에 대한 집중된 관심과 신발의 외관은 별도다.'),('2-2','boot fetish','부츠에 대한 관심과 부츠 착용은 별도다.'),('2-2','hosiery stocking fetish','스타킹류에 대한 관심과 호지어리 자체는 별도다.'),('2-2','glove fetish','장갑에 대한 관심과 착용은 별도다.'),('2-2','mask hood interest','가면·후드에 대한 관심과 가시적 착용은 별도다.'),('2-2','balloon fetish','풍선에 대한 관심과 풍선의 외형은 별도다.'),('2-2','uniform fetish','제복에 대한 관심과 실제 직업·복장 형태는 별도다.')]
rows=[]
for i,line in enumerate(raw.splitlines(),1):
 sec,term,ko,slot,en,korean=line.split('|');tid='FPA-'+sec+'-'+format(i,'03d')
 rows.append({'term_id':tid,'section':sec,'term':term,'label_ko':ko,'slot':slot,'en':en,'ko':korean,'boundary':notes.get(term,'특정한 관찰 예시이며 보이는 형태만으로 동기·기능·관계·재질이나 숨은 구조를 확정하지 않는다.')})
for i,(sec,term,note) in enumerate(context_only,1):rows.append({'term_id':'FPA-'+sec+'-C'+format(i,'03d'),'section':sec,'term':term,'label_ko':term,'boundary':note})
planhash=hashlib.sha256(PLAN.read_bytes()).hexdigest()
reg={'schema':'photo-fashion-parts-semantics/v1','scope':'비-BDSM 의복 파츠·호지어리·신발·일반 장식·신체 관심; term inventory is a bounded derivative of the reviewed conversation summary, not independently verified for each term','source_plan':'skills/photo-prompt-image-generator/references/fashion-visual-semantics-research-plan-20261108.md','source_plan_sha256':planhash,'source_conversation':'https://chatgpt.com/c/6aeef5f7-3398-83e8-80a7-996fd5badce2','rows':[],'native_approval':False,'pixel_qualification':'NOT_RUN'}
for row in rows:
 reg['rows'].append({'term_id':row['term_id'],'source_section':row['section'],'term':row['term'],'name_ko':row['label_ko'],'context_ko':row['boundary'],'classification':'visual_example_plus_context' if 'en' in row else 'context_only_or_evidence_pending','independent_term_source_status':'not_individually_verified','native_approval':False})
regpath=ASSETS/'photo_fashion_parts_semantics_20261108.json';dump(regpath,reg); regsha=hashlib.sha256(regpath.read_bytes()).hexdigest()
context={'schema':'photo-fashion-parts-context-views/v1','source_registry':regpath.name,'source_registry_sha256':regsha,'search_scope':'research context only; not a positive retrieval source or native selection','views':[]}
for i,row in enumerate(reg['rows']):
 context['views'].append({'id':'fashion-parts-context-'+row['term_id'],'term_id':row['term_id'],'context_ko':row['context_ko'],'source_quotes':[{'pointer':f'/rows/{i}/term','quote':row['term']},{'pointer':f'/rows/{i}/context_ko','quote':row['context_ko']}],'context_only':True,'native_approval':False,'boundary':'Context does not establish a visible fact, an individual source verification, or native selection.'})
dump(ASSETS/'photo_fashion_parts_research_context_views_20261108.json',context)
cs={};bs={};vs=[]
slots=json.loads((ASSETS/'photo_candidate_slot_catalog.json').read_text())['slot_catalog']
for row in rows:
 if 'en' not in row:continue
 cid='cand_'+H('fashion-parts-20261108:'+row['term_id'])[:32]
 metadata={'term_id':row['term_id'],'name_ko':row['label_ko'],'observable_gate':'All stated entities, locations and relations in the bilingual proposition must be visible; a hidden part is unobservable.','context_boundary_ko':row['boundary'],'sources_reference':regpath.name,'source_scope':'A bounded independently authored example. The prior conversation and topical review do not verify each detailed proposition or make it universal.','native_approval':False,'pixel_status':'NOT_RUN'}
 en=row['en'];ko=row['ko']; candidate={'id':cid,'record_kind':'visual_option','content':{'en':en,'ko':ko,'definition':'Optional fashion and appearance visual realization: '+en,'aliases':[row['term'],row['label_ko']],'application_contract':'Use only as a complete optional proposition, with independently established owners and permitted changes. Preserve stated objects, location, count, contact and relations. Clothing and body details do not establish age, sexual interest, intent, identity, consent, real material or hidden construction. Hidden details are unobservable. Search views and research context confer no native approval.','research_semantics':metadata},'conditions':{},'effects':{'dimensions':['appearance','relationship'],'properties':[]},'provenance':[{'source':'authored-research:photo-prompt/fashion-parts-20261108/'+row['term_id'],'sha256':regsha}]}
 cs[cid]=candidate
 slot=row['slot'];
 if slot not in slots:raise ValueError('unknown slot '+slot)
 bid='bind_'+H('fashion-parts-20261108:'+cid+':'+slot)[:32];bs[bid]={'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional','semantic_role':'direct','conditions':{'subject_applicability':{}},'weight':1.0}
 key=cid+':base:whole';vs.append({'id':rv.view_id(cid,'base',key),'candidate_id':cid,'realization_id':'base','key':key,'kind':'whole','source_record_sha256':rv.digest(candidate),'text_en':en,'text_ko':ko,'source_quotes':[{'pointer':'/content/en','quote':en},{'pointer':'/content/ko','quote':ko}],'native_approval':False})
cm={'schema':'photo-candidate-module/v3','candidates':cs};bm={'schema':'photo-candidate-slot-bindings/v3','slot_bindings':bs};vm={'schema':'photo-candidate-retrieval-views/v1','recipe':'photo-reviewed-bilingual-search-view/v1','source_inventory_id':'fashion-parts-20261108','coverage':{'positive_realizations':len(cs)},'native_approval':False,'views':vs}
rv.validate(vm,cs,require_complete=True)
base=corpus.load(ASSETS);base['candidates'].update(cs);base['slot_bindings'].update(bs);corpus.validate(base)
dump(ASSETS/'photo_candidate_fashion_parts_20261108.json',cm);dump(ASSETS/'photo_candidate_fashion_parts_bindings_20261108.json',bm);dump(ASSETS/'photo_candidate_retrieval_views_fashion_parts_20261108.json',vm)
print(json.dumps({'terms':len(rows),'context_only':len(context_only),'visual_candidates':len(cs),'bindings':len(bs),'retrieval_views':len(vs),'context_views':len(context['views'])},ensure_ascii=False))
