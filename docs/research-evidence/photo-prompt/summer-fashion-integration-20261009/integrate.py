"""Promote reviewed visible variants, preserving existing authored records.

Research provenance stays here. Runtime files carry only selected visible
constructions, their complete effects, and ordinary optional contracts.
"""
from pathlib import Path
from collections import defaultdict, Counter
import hashlib
import json

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
RESEARCH = ROOT / "docs/research-evidence/photo-prompt/summer-fashion-20261009"
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"

LABELS = {
 1:["짧은 밀착 소매와 힙 윗선 밑단의 티셔츠"],
 2:["두 의복 경계 사이 복부 띠가 보이는 크롭톱","낮은 갈비뼈 밑단과 높은 하의 허리선"],
 3:["앞뒤 몸판을 잇는 넓은 탱크 어깨띠","앞뒤 윗선을 잇는 가는 캐미솔 끈"],
 4:["허리까지 이어진 수평 윗선의 스트랩리스 몸판"],
 5:["앞목을 높이 덮고 목 뒤에서 연결되는 홀터","열린 앞목에서 올라와 목 뒤에서 묶인 두 띠"],
 6:["등의 매듭과 뾰족한 밑단을 가진 스카프 톱","한쪽 어깨와 목 연결쇠에 고정한 스카프 톱"],
 7:["두 천 컵이 밑가슴 밴드에 연결되는 짧은 상의"],
 8:["옆허리 끈으로 고정한 겹침 몸판","봉제선에 고정된 사선 겹침 앞판"],
 9:["앞의 두 끈 끝을 묶은 매듭","등의 두 끈 끝을 묶은 매듭"],
 10:["컵 주변 개더와 네모 목둘레의 블라우스","넓은 목둘레에 주름을 모은 블라우스"],
 11:["블라우스 허리판을 모으는 평행 봉제 줄","작은 주름을 잇는 기하 장식 스모킹"],
 12:["연결된 실 고리와 실제 구멍의 크로셰 층"],
 13:["연속된 겉원단을 통해 보이는 독립 이너"],
 14:["열린 앞목 양쪽에 펼쳐진 캠프 칼라"],
 15:["셔츠 원단을 따라 반복되는 큰 열대 잎 무늬"],
 16:["접힌 칼라 아래의 짧은 앞단추 플래킷"],
 17:["중앙 단추 줄에 맞닿는 민소매 베스트 앞판"],
 18:["목 아래 가까이 놓인 둥근 크루 목둘레"],
 19:["넓은 곡선으로 내려간 스쿠프 목둘레","가슴 위쪽까지 내려간 깊은 스쿠프 윗선"],
 20:["두 사선 변이 중앙에서 만나는 V 목둘레","중앙으로 길게 내려간 깊은 V 윗선"],
 21:["가로 윗선과 두 옆 모서리의 스퀘어 목둘레"],
 22:["두 둥근 호가 중앙 홈에서 만나는 윗선"],
 23:["몸통 앞을 가로지르는 곧은 의복 윗선"],
 24:["쇄골 가까이 넓게 펼쳐진 보트 목둘레"],
 25:["앞목 아래로 부드럽게 처진 카울 주름"],
 26:["양어깨 아래로 내려간 연속된 의복 윗선"],
 27:["한쪽 어깨만 잇는 비대칭 몸판"],
 28:["어깨 위 브리지와 아래 소매가 남은 콜드숄더"],
 29:["연결부 아래에 둘러싸인 키홀 구멍","앞 몸판을 비운 마감된 컷아웃 구멍"],
 30:["연속된 투과 패널이 윗목과 몸판을 잇는 일루전"],
 31:["마감된 암홀의 민소매 몸판","어깨끝을 짧게 덮는 캡 소매"],
 32:["어깨에서 넓게 떨어지는 플러터 소매","양 연결선 사이에 부푼 퍼프 소매"],
 33:["겨드랑이에서 목둘레로 향하는 래글런 연결선","어깨끝 바깥 팔 윗부분의 소매 연결선"],
 34:["몸통 옆으로 낮게 내려간 깊은 암홀"],
 35:["한 중앙 요크로 합류하는 등 어깨끈","등에서 교차한 뒤 반대편 아래에 붙는 두 끈"],
 36:["낮게 내려간 의복 뒤판 윗선","끈만으로 남은 열린 등 연결"],
 37:["옆허리의 둘러싸인 컷아웃","윗부분과 허리띠 사이 열린 옆선"],
 38:["몸통 가까이 따르는 상의와 국소 여유","몸을 스치며 떨어지는 드레스 주름"],
 39:["몸통과 힙을 가까이 따르는 몸판"],
 40:["몸통을 두른 반복 수평 밴드의 드레스"],
 41:["좁은 허리 아래로 퍼지는 스커트"],
 42:["몸통을 스치며 사선 주름이 생긴 드레스"],
 43:["몸통에서 떨어지는 박시한 옆판","넓은 몸판과 팔 아래 소매 연결"],
 44:["세로 패널과 가슴 위 컵선의 몸판","가슴 아래 윗선에서 시작하는 코르셋 몸판"],
 45:["낮은 컵 윗선과 바깥쪽 지지끈","비교적 높게 덮는 별도 컵 윗선"],
 46:["낮은 중앙 연결부와 두 컵 안쪽 변"],
 48:["한 점으로 모이는 두 다트 봉제선","두 몸판을 잇는 세로 곡선 프린세스 심"],
 49:["의복 윗선 위의 가슴 윗부분 피부 영역","성인 의복 중앙 개구부에서 보이는 가슴 사이 홈"],
 50:["성인 불투명 몸판 옆에서 보이는 가슴 외곽","성인 불투명 상의 아래에서 보이는 가슴 아랫경계"],
 51:["상의 밑단과 허리선 사이에 보이는 배꼽","복부 띠만 보이고 배꼽은 허리선에 가려진 착장"],
 52:["긴 스커트의 높은 트임 꼭짓점","낮은 스커트 트임과 별도 밑단"],
 53:["불투명 이너가 실제 오픈워크 구멍 뒤에 놓인 층"],
 55:["겉옷 허리선 위로 보이는 독립 이너 끈","긴 투과 겉드레스 뒤에 보이는 독립 이너"],
 57:["가는 끈에 매달린 단순 드레스 몸판","칼라와 스커트 방향 단추 줄의 셔츠 드레스"],
 58:["허리에 여유가 있는 직선 시프트 드레스","밑단으로 넓어지는 A라인 드레스"],
 59:["가슴 바로 아래에 붙는 스커트","자연허리 아래 낮은 절개에 붙는 스커트"],
 60:["가로 개더 연결선을 가진 연속 스커트 층"],
 61:["몸판에서 두 짧은 다리통으로 이어지는 롬퍼"],
 62:["무릎과 발목 사이 밑단의 스커트","무릎 위 밑단의 스커트"],
 63:["힙을 따르며 좁은 밑단으로 내려가는 스커트","맞춘 허리선 아래로 퍼지는 짧은 스커트"],
 64:["반복 능선과 골이 이어지는 스커트 플리츠"],
 65:["힙을 두른 천의 끝이 옆허리 매듭에서 만나는 랩"],
 66:["같은 스커트에서 앞보다 긴 뒤 밑단"],
 67:["부푼 부피 아래 안으로 모인 버블 밑단","힙과 윗허벅지 아래로 퍼지는 스커트"],
 68:["두 다리통 끝에 올풀림이 남은 데님 쇼츠"],
 69:["무릎 가까이에 닿는 두 쇼츠 밑단"],
 70:["두 다리입구 위에 부푼 천이 모인 쇼츠"],
 71:["윗허벅지를 따르는 신축형 쇼츠"],
 72:["허벅지 옆판에 붙인 덮개 덧주머니"],
 73:["연결 쇼츠 앞을 겹쳐 덮는 스커트판","공유 허리 아래 분리된 두 넓은 바지통"],
 74:["무릎 아래에서 끝나 발목 간격이 남는 바지"],
 75:["허리선 아래 부드러운 주름의 넓은 바지통"],
 76:["허리 케이싱 출입구에서 나온 드로코드"],
 77:["배꼽 위에 놓인 하의 허리선","배꼽 아래에 놓인 하의 허리선"],
 78:["두 삼각 수영복 패널과 지지끈","패널 끝에서 연결되는 가는 수영복 끈"],
 79:["윗선과 밑단이 따로 있는 수영복 수평 밴드","수영복 밴드에서 목 뒤로 이어진 끈","컵 아래로 이어진 롱라인 수영복 몸판"],
 80:["독립 밑단이 겹친 탱키니 상하의","허리를 거쳐 두 다리입구로 연결된 원피스 수영복"],
 81:["상하 수영복 부분을 잇는 좁은 몸통 패널과 옆 컷아웃"],
 82:["깊은 중앙 앞목 수영복 윗선","낮은 수영복 뒤판 윗선"],
 83:["허리선과 구별되는 높은 바깥 다리입구","독립 다리입구 위에 높게 놓인 수영복 허리선"],
 84:["옆힙 매듭에서 만나는 수영복 끈 끝"],
 85:["곡선 변의 좁아진 수영복 뒤판","두 지지끈 사이에 이어진 가는 뒤 스트립"],
 86:["두 짧은 다리통을 가진 보이쇼츠 수영복","가는 지지끈으로 연결한 작은 수영복 패널"],
 87:["몸통을 따르는 민소매가 아닌 수영 상의","소매 몸판과 하의가 연결된 서프수트"],
 88:["독립 허리선과 두 다리통의 스윔 쇼츠"],
 89:["수영복 하의 허리선에 연결된 짧은 스커트 층"],
 90:["머리 덮개가 몸통 상의에 연결된 수영 착장","독립 머리 덮개와 상의 및 바지의 수영 착장"],
 91:["선택한 수영복 위의 독립 커버업 층","앞의 두 몸판이 겹치는 수영복 위 로브"],
 93:["평평한 띠와 번갈아 반복되는 시어서커 요철","독립 이너 윤곽이 비치는 가벼운 보일 층"],
 94:["겉면에서 사선 결이 읽히는 직물","서로 다른 실 색으로 생긴 잔잔한 짜임 색면"],
 95:["가는 주름으로 떨어지는 가벼운 연속 직물","몸통 밖으로 각을 유지하는 얇은 직물"],
 96:["직물 주름을 따라 넓게 이동하는 광택"],
 97:["그림자로 구별되는 반복 리브 골","기저 조직 위에 올라온 작은 테리 고리"],
 98:["온전한 바탕천 사이 자수 테두리 구멍","불투명 이너 앞에 놓인 실 그물 구멍"],
 99:["옆 개더 봉제선으로 모이는 몸판 주름"],
 100:["목둘레 부착선에 모인 러플 주름","매끈한 부착선 아래 넓게 퍼진 플라운스"],
 101:["의복 끝에 따로 붙인 늘어진 프린지","한 부착점에 모인 태슬 실 묶음","곡선 호가 반복되는 스캘럽 경계"],
 102:["마주 보는 아일렛 줄 사이를 잇는 레이싱","두 의복 끈 끝을 연결하는 링"],
 103:["원단 구멍 경계의 해진 실 끝","의복 경계에 붙인 작은 금속형 스터드"],
 104:["두 색 띠가 교차하는 작은 격자 무늬","셔츠 몸판에서 반복되는 가로 줄무늬"],
 105:["몸판에 작게 반복되는 잔꽃 모티프","넓은 몸판 면적을 차지하는 큰 잎 모티프"],
 106:["선명한 경계에서 만나는 의복 색면","직물 위에 번진 불규칙한 색 패치"],
 107:["민소매 상의 위의 여유 있는 독립 셔츠"],
 108:["목둘레 리본과 허리에서 겹치는 랩 스커트"],
 109:["드레스 허리의 웨스턴 벨트와 독립 부츠","물빛 직물에 붙인 진주형 장식"],
 110:["데님 허리선 위로 떨어지는 짧은 소매 저지"],
 111:["불투명 이너 드레스 위의 검정 오픈워크 층"],
 112:["발가락 사이 기둥과 밑창 연결의 Y 샌들 끈","발등을 교차해 밑창 양쪽에 붙는 케이지 띠"],
 113:["앞발과 뒤꿈치를 잇는 쐐기 밑창과 로프형 둘레","앞발을 덮고 뒤꿈치가 열린 낮은 신발"],
 114:["낮은 밑창에 붙인 반투명 성형 갑피","낮은 밑창 위에 놓인 그물 갑피","낮은 밑창에 붙인 불투명 성형 갑피"],
 115:["열린 머리윗부분 아래의 밴드와 돌출 바이저 챙"],
 116:["바구니형 가방 몸체에 이어진 짜임 손잡이","머리를 두르고 뒤에서 묶은 천 끝"],
 117:["신발 위 발목을 두른 연결 구슬 체인"],
 118:["하의 허리선과 별도로 복부를 두른 체인","목 체인과 허리 체인을 잇는 중앙 장신구 체인"]
}

LABELS.update({
 10:["가로 가슴 절개 위의 개더와 플러터 소매를 가진 블라우스","넓은 목둘레에 주름을 모은 블라우스"],
 13:["연속된 겉원단을 통해 보이는 불투명 캐미솔","겉원단이 겹친 부위에서 약해진 이너 윤곽"],
 19:["쇄골 아래 넓은 U 곡선의 스쿠프 목둘레"],
 20:["가슴 위쪽 아래 중앙 점에서 만나는 V 목둘레"],
 21:["가로 아랫변과 두 옆 모서리의 스퀘어 목둘레"],
 23:["몸통 앞의 곧은 윗선 양 끝에 붙은 가는 어깨끈"],
 29:["목둘레 밴드가 윗변을 잇는 둘러싸인 키홀"],
 30:["몸판 변과 어깨 봉제선을 잇는 투과 패널","피부와 비슷한 색이지만 봉제선과 접힌 변이 있는 원단"],
 36:["높은 앞목과 견갑골 아래의 낮은 뒤판"],
 38:["접촉 부위 사이에 여유가 남는 바디스키밍 원단"],
 43:["허리에 여유가 있고 곧은 밑단으로 내려가는 박시 셔츠"],
 44:["가슴 아래에서 시작하는 구조적 겉옷과 그 위로 이어지는 이너 블라우스","컵 영역에서 허리로 이어지는 봉제선 분할 오버버스트 몸판"],
 45:["수평에 가까운 컵 윗선과 바깥쪽 지지끈"],
 49:["의복 윗선 위에 드러난 쇄골 영역","성인 의복 중앙 개구부에서 보이는 가슴 사이 홈"],
 52:["윗허벅지 트임 꼭짓점 양쪽에 남은 긴 스커트 밑단"],
 55:["낮은 바지 허리선 위에서 Y로 합류하는 독립 이너 끈"],
 71:["윗허벅지에 밀착하고 중간에서 끝나는 쇼츠 밑단"],
 78:["두 삼각 수영복 패널과 지지끈","작은 수영복 패널에서 등 매듭으로 이어지는 가는 끈"],
 79:["수영복 수평 밴드 양 끝에서 목으로 향하는 홀터 끈","컵 아래로 이어진 롱라인 밴드와 별도 수영복 하의"],
 82:["높은 앞가슴 패널과 견갑골 아래의 수영복 뒤판"],
 83:["높은 허리선과 독립적으로 힙 옆으로 올라가는 다리입구"],
 85:["곡선 변의 좁아진 수영복 뒤판","허리밴드와 아래 수영복 패널을 잇는 가는 뒤 연결부"],
 87:["독립 밑단을 가진 소매 수영 상의와 별도 하의","긴소매 몸판에서 하부로 이어진 두 다리입구의 서프수트"],
 90:["머리 덮개가 긴소매 상의에 이어지고 바지가 분리된 수영 착장"],
 91:["별도 칼라와 밑단이 있는 열린 겉셔츠 및 안쪽 수영복","별도 수영복 하의 위로 떨어지는 넓은 튜닉 몸판과 밑단"],
 94:["원단 주름을 따라 이어지는 데님 사선 실 능선"],
 95:["속의 옷에서 떨어져 각을 유지하는 반투명 오간자 주름"],
 96:["부드러운 주름에 따라 달라지는 넓은 원단 광택"],
 101:["의복 밑단에 따로 붙인 늘어진 프린지","연속된 의복 밑단에 반복되는 둥근 스캘럽 호"]
})

# Reviewed equivalence: location differences retain independent candidates.
REUSE = {
 (11,1):"clt_ct064_v1", (11,2):"clt_ct064_v2", (33,2):"fit_ff09_v1_candidate",
 (35,1):"fit_ff52_v1_candidate", (35,2):"fit_ff52_v2_candidate",
 (48,2):"clt_ct031_v1", (100,2):"clt_ct065_v2"
}

def domain(n):
    if 49 <= n <= 56: return "coverage"
    if 38 <= n <= 43: return "fit"
    if 78 <= n <= 91: return "swimwear"
    if 92 <= n <= 98: return "textile"
    if 107 <= n <= 111: return "style"
    if 104 <= n <= 106 or 112 <= n <= 118: return "ornament"
    return "clothing_structure"

# These paths describe all visible choices in each sentence, including the
# additional hem/inner layer/footwear that the original research template left
# for review. Identity and body geometry never follow from garment geometry.
EFFECTS = {
 1:"garment_type fit.local_ease length.top_hem structure.sleeve.length",
 2:"length.top_hem coverage.midriff waistline.height garment_type",
 3:"structure.strap_paths structure.strap_width structure.armhole material.drape",
 4:"structure.strap_paths neckline.shape length.top_hem",
 5:"structure.strap_paths neckline.height neckline.depth coverage.back",
 6:"garment_type structure.front_fastener_state structure.strap_paths length.hem_shape coverage.back",
 7:"garment_type structure.cup_sections structure.underbust_band length.top_hem",
 8:"structure.front_fastener_state structure.panel_overlap neckline.shape",
 9:"structure.strap_fastener structure.front_fastener_state",
 10:"neckline.shape structure.cup_sections details.gathers_shirring_smock fit.local_ease",
 11:"details.gathers_shirring_smock",
 12:"material.surface_topology material.transmission layers.order",
 13:"material.transmission layers.order layers.inner_coverage material.drape",
 14:"structure.collar neckline.shape structure.front_placket",
 15:"pattern.motif pattern.repeat",
 16:"structure.collar structure.front_placket",
 17:"garment_type structure.front_fastener_state fit.local_ease structure.panel_join",
 18:"neckline.shape neckline.height",
 19:"neckline.shape neckline.width neckline.depth",
 20:"neckline.shape neckline.depth",
 21:"neckline.shape neckline.width",
 22:"neckline.shape",
 23:"neckline.shape neckline.height",
 24:"neckline.shape neckline.width neckline.height",
 25:"neckline.shape material.drape details.gathers",
 26:"neckline.position structure.sleeve_attachment coverage.shoulder",
 27:"structure.strap_paths neckline.asymmetry coverage.shoulder",
 28:"structure.sleeve_attachment structure.shoulder_bridge structure.aperture coverage.shoulder",
 29:"structure.aperture neckline.shape coverage.front",
 30:"material.transmission structure.panel_join neckline.height layers.order",
 31:"structure.sleeve.length structure.armhole structure.sleeve_attachment",
 32:"structure.sleeve.shape structure.sleeve.length details.gathers",
 33:"structure.sleeve_attachment fit.shoulder.seam_position",
 34:"structure.armhole.depth coverage.side",
 35:"structure.back_strap_connection",
 36:"coverage.back structure.back_strap_connection neckline.back_height",
 37:"structure.aperture coverage.side structure.side_connection",
 38:"fit.local_ease material.drape silhouette.waist_to_hem",
 39:"fit.local_ease silhouette.body_contour",
 40:"structure.band_panels fit.local_ease garment_type",
 41:"fit.waist silhouette.waist_to_hem garment_type",
 42:"material.drape fit.local_ease",
 43:"fit.local_ease structure.sleeve_attachment length.sleeve",
 44:"structure.cup_sections structure.panel_join length.top_hem coverage.upper_chest",
 45:"structure.cup_sections structure.strap_paths coverage.upper_chest",
 46:"structure.cup_sections neckline.depth coverage.central_chest",
 48:"details.princess_dart structure.panel_join fit.local_ease",
 49:"neckline.depth coverage.central_chest coverage.upper_chest",
 50:"coverage.lateral_chest coverage.lower_chest structure.armhole material.transmission length.top_hem",
 51:"length.top_hem waistline.height coverage.midriff coverage.navel",
 52:"structure.slit.apex length.hem coverage.thigh",
 53:"material.surface_topology material.transmission layers.order layers.inner_coverage",
 55:"layers.order layers.inner_coverage waistline.height coverage.back material.transmission length.hem",
 57:"garment_type structure.strap_paths structure.collar structure.front_placket silhouette.waist_to_hem material.drape",
 58:"garment_type fit.waist silhouette.waist_to_hem",
 59:"waistline.seam_height silhouette.waist_to_hem fit.local_ease",
 60:"structure.tier_connections details.gathers silhouette.waist_to_hem",
 61:"garment_type structure.torso_to_leg_connection structure.leg_division length.hem",
 62:"length.hem garment_type",
 63:"fit.hip silhouette.hip_to_hem length.hem details.folds",
 64:"details.pleat structure.fold_direction",
 65:"garment_type structure.panel_overlap structure.front_fastener_state",
 66:"length.hem_shape length.hem",
 67:"length.hem_shape details.gathers silhouette.hip_to_hem fit.hip",
 68:"material.visible_weave length.hem_finish structure.leg_division garment_type",
 69:"length.hem structure.waistband structure.leg_division",
 70:"structure.leg_opening details.gathers silhouette.leg_volume",
 71:"fit.local_ease length.hem structure.leg_division",
 72:"details.pocket_position details.pocket_flap",
 73:"garment_type structure.panel_overlap structure.leg_division layers.order length.hem",
 74:"length.hem structure.leg_division",
 75:"silhouette.leg_width material.drape structure.leg_division",
 76:"structure.waistband structure.drawcord_path",
 77:"waistline.height coverage.navel",
 78:"structure.swim_panel_shape structure.strap_paths structure.strap_width",
 79:"structure.swim_panel_shape structure.strap_paths structure.strap_width length.top_hem",
 80:"garment_type structure.torso_to_leg_connection structure.leg_division length.top_hem layers.order coverage.torso",
 81:"garment_type structure.torso_to_leg_connection structure.aperture coverage.side",
 82:"neckline.depth neckline.back_height coverage.back coverage.central_chest",
 83:"structure.leg_opening.height waistline.height coverage.hip",
 84:"structure.strap_fastener structure.side_connection",
 85:"coverage.rear structure.rear_panel_width structure.strap_paths",
 86:"structure.swim_panel_shape structure.leg_division length.hem structure.strap_paths coverage.torso coverage.rear",
 87:"garment_type structure.sleeve.length structure.torso_to_leg_connection coverage.torso",
 88:"garment_type structure.leg_division structure.waistband length.hem",
 89:"garment_type layers.order structure.overlay_attachment length.hem",
 90:"garment_type layers.order structure.head_cover_connection structure.leg_division coverage.head coverage.torso",
 91:"garment_type layers.order structure.panel_overlap length.hem fit.local_ease",
 93:"material.surface_relief material.visible_weave material.drape material.transmission layers.inner_coverage",
 94:"material.visible_weave material.surface_color_structure",
 95:"material.drape material.transmission material.surface_stiffness",
 96:"material.surface_luster material.drape",
 97:"material.surface_relief material.surface_topology",
 98:"material.surface_topology details.embroidery layers.order layers.inner_coverage material.transmission",
 99:"details.gathers material.drape",
 100:"details.ruffle_flounce details.trim_position",
 101:"details.trim_position details.trim_attachment details.fringe_tassel_scallop",
 102:"details.eyelet structure.lacing_path structure.connector_ring structure.strap_fastener",
 103:"material.surface_wear details.stud_attachment",
 104:"pattern.repeat pattern.geometry color",
 105:"pattern.motif pattern.repeat pattern.scale",
 106:"color pattern.color_fields material.surface_luster",
 107:"garment_type layers.order fit.local_ease structure.sleeve.length silhouette.leg_width",
 108:"garment_type details.ribbon_attachment layers.order structure.panel_overlap material.drape",
 109:"accessories.belt footwear.type details.embellishment material.surface_luster color",
 110:"garment_type structure.sleeve.length length.top_hem layers.order waistline.height fit.local_ease",
 111:"garment_type color material.surface_topology layers.order layers.inner_coverage",
 112:"footwear.sandal_strap_paths footwear.toe_post footwear.sole_connection",
 113:"footwear.sole_topology footwear.heel_height footwear.forefoot_height footwear.heel_openness footwear.upper_coverage footwear.surface_relief",
 114:"footwear.upper_structure footwear.material.transmission footwear.sole_connection footwear.heel_height",
 115:"accessories.headwear.crown accessories.headwear.brim accessories.headwear.band",
 116:"accessories.bag_body accessories.bag_handles accessories.headwear.wrap",
 117:"accessories.anklet_location accessories.bead_connection",
 118:"accessories.chain_paths accessories.chain_connection layers.order"
}

# Review each alternative separately rather than applying the union of a family.
VARIANT_EFFECTS = {
 (3,1):"structure.strap_paths structure.strap_width structure.armhole", (3,2):"structure.strap_paths structure.strap_width material.drape",
 (5,1):"structure.strap_paths neckline.height", (5,2):"structure.strap_paths neckline.depth structure.strap_fastener",
 (6,1):"garment_type structure.strap_fastener length.hem_shape", (6,2):"garment_type structure.strap_paths structure.connector_ring length.hem_shape coverage.back structure.strap_fastener",
 (8,1):"structure.front_fastener_state structure.panel_overlap", (8,2):"structure.panel_overlap structure.panel_join neckline.shape",
 (9,1):"structure.front_fastener_state", (9,2):"structure.back_fastener_state",
 (31,1):"structure.sleeve.length structure.armhole", (31,2):"structure.sleeve.length structure.sleeve_attachment",
 (36,1):"coverage.back neckline.back_height", (36,2):"coverage.back structure.back_strap_connection",
 (44,1):"structure.cup_sections structure.panel_join coverage.upper_chest", (44,2):"structure.panel_join length.top_hem coverage.upper_chest",
 (49,1):"neckline.depth coverage.upper_chest", (49,2):"neckline.depth coverage.central_chest",
 (50,1):"coverage.lateral_chest structure.armhole material.transmission", (50,2):"coverage.lower_chest length.top_hem material.transmission",
 (55,1):"layers.order layers.inner_coverage waistline.height coverage.back", (55,2):"layers.order layers.inner_coverage material.transmission length.hem",
 (57,1):"garment_type structure.strap_paths material.drape", (57,2):"garment_type structure.collar structure.front_placket",
 (67,1):"length.hem_shape details.gathers silhouette.hip_to_hem", (67,2):"silhouette.hip_to_hem fit.hip",
 (73,1):"garment_type structure.panel_overlap structure.leg_division layers.order length.hem", (73,2):"garment_type structure.leg_division silhouette.leg_width length.hem",
 (79,1):"structure.swim_panel_shape length.top_hem", (79,2):"structure.swim_panel_shape structure.strap_paths", (79,3):"length.top_hem structure.underbust_band",
 (80,1):"garment_type length.top_hem layers.order coverage.torso", (80,2):"garment_type structure.torso_to_leg_connection structure.leg_division",
 (82,1):"neckline.depth coverage.central_chest", (82,2):"neckline.back_height coverage.back",
 (83,1):"structure.leg_opening.height coverage.hip", (83,2):"waistline.height",
 (85,1):"coverage.rear structure.rear_panel_width", (85,2):"coverage.rear structure.rear_panel_width structure.strap_paths",
 (86,1):"structure.leg_division length.hem coverage.rear", (86,2):"structure.swim_panel_shape structure.strap_paths coverage.torso coverage.rear",
 (87,1):"garment_type structure.sleeve.length fit.local_ease coverage.torso", (87,2):"garment_type structure.sleeve.length structure.torso_to_leg_connection coverage.torso",
 (90,1):"garment_type layers.order structure.head_cover_connection coverage.head coverage.torso", (90,2):"garment_type layers.order coverage.head coverage.torso structure.leg_division",
 (93,1):"material.surface_relief material.visible_weave", (93,2):"material.visible_weave material.drape material.transmission layers.inner_coverage layers.order",
 (95,1):"material.drape", (95,2):"material.drape material.surface_stiffness",
 (97,1):"material.surface_relief", (97,2):"material.surface_relief material.surface_topology",
 (98,1):"material.surface_topology details.embroidery", (98,2):"material.surface_topology layers.order layers.inner_coverage material.transmission",
 (102,1):"details.eyelet structure.lacing_path", (102,2):"structure.connector_ring structure.strap_fastener",
 (103,1):"material.surface_wear", (103,2):"details.stud_attachment",
 (106,1):"color pattern.color_fields", (106,2):"color pattern.color_fields",
 (109,1):"accessories.belt footwear.type", (109,2):"details.embellishment material.surface_luster color",
 (112,1):"footwear.sandal_strap_paths footwear.toe_post footwear.sole_connection", (112,2):"footwear.sandal_strap_paths footwear.sole_connection",
 (113,1):"footwear.sole_topology footwear.heel_height footwear.forefoot_height footwear.surface_relief", (113,2):"footwear.heel_openness footwear.upper_coverage footwear.heel_height",
 (116,1):"accessories.bag_body accessories.bag_handles", (116,2):"accessories.headwear.wrap",
 (118,1):"accessories.chain_paths", (118,2):"accessories.chain_paths accessories.chain_connection"
}

VARIANT_EFFECTS.update({
 (10,1):"details.gathers_shirring_smock structure.panel_join structure.sleeve.shape structure.sleeve_attachment",
 (10,2):"neckline.shape neckline.width details.gathers_shirring_smock fit.local_ease",
 (18,1):"neckline.shape neckline.height coverage.upper_chest",
 (23,1):"neckline.shape neckline.height structure.strap_paths structure.strap_width",
 (30,1):"material.transmission structure.panel_join layers.order", (30,2):"color structure.panel_join layers.order",
 (36,1):"coverage.back neckline.back_height neckline.height",
 (38,1):"fit.local_ease material.drape", (43,1):"fit.local_ease silhouette.waist_to_hem length.hem_shape",
 (39,1):"fit.local_ease silhouette.body_contour material.transmission",
 (44,1):"garment_type neckline.height coverage.upper_chest layers.order layers.inner_coverage",
 (44,2):"structure.cup_sections structure.panel_join fit.local_ease coverage.upper_chest",
 (49,1):"neckline.height coverage.collarbone",
 (55,1):"layers.order layers.inner_coverage waistline.height structure.back_strap_connection",
 (79,1):"structure.swim_panel_shape structure.strap_paths", (79,2):"length.top_hem structure.underbust_band layers.order",
 (78,2):"structure.strap_paths structure.strap_width structure.strap_fastener structure.swim_panel_shape",
 (82,1):"neckline.back_height coverage.back neckline.height coverage.upper_chest",
 (83,1):"structure.leg_opening.height waistline.height coverage.hip",
 (87,1):"garment_type structure.sleeve.length length.top_hem layers.order coverage.torso",
 (88,1):"garment_type structure.leg_division structure.waistband length.hem fit.local_ease",
 (90,1):"garment_type layers.order structure.head_cover_connection structure.sleeve.length structure.leg_division length.hem coverage.head coverage.torso",
 (91,1):"garment_type layers.order structure.front_fastener_state structure.collar length.top_hem",
 (91,2):"garment_type layers.order length.top_hem fit.local_ease material.drape",
 (94,1):"material.visible_weave", (95,1):"material.drape material.transmission material.surface_stiffness layers.order layers.inner_coverage",
 (101,1):"details.trim_position details.trim_attachment details.fringe", (101,2):"length.hem_shape details.scallop_edge"
})

# Reviewed compatibility with the current property vocabulary. A new name must
# not bypass an existing lock for the same concrete garment change.
PROPERTY_COMPATIBILITY = {
 "garment_type":["type"],
 "length.top_hem":["top.hem_relative_to_waist","length.bodice_lower_edge"],
 "length.hem":["length.hem_landmark"],
 "neckline.shape":["neckline.outline"],
 "structure.armhole.depth":["fit.armhole_depth"],
 "structure.armhole":["coverage.armhole"],
 "structure.sleeve.length":["length.sleeve","sleeves.sleeve_length"],
 "structure.panel_join":["structure.panel_joins"],
 "structure.panel_overlap":["structure.wrap_overlap"],
 "structure.torso_to_leg_connection":["structure.torso_lower_connection"],
 "structure.leg_division":["structure.leg_bifurcation"],
 "structure.strap_paths":["structure.strap_attachment"],
 "structure.cup_sections":["details.bra_cup_seam"],
 "structure.underbust_band":["structure.cup_band_connection"],
 "structure.waistband":["structure.waist_band"],
 "structure.drawcord_path":["details.tie_drawstring"],
 "waistline.height":["fit.waistband_landmark"],
 "waistline.seam_height":["structure.waist_seam_position"],
 "structure.leg_opening.height":["coverage.leg_opening"],
 "structure.rear_panel_width":["coverage.rear_panel"],
 "coverage.lateral_chest":["coverage.lateral_bust"],
 "coverage.lower_chest":["coverage.lower_bust"],
 "coverage.midriff":["coverage.abdominal_gap"],
 "material.transmission":["surface.sheer_opacity"],
 "fit.waist":["fit.waist_contact"],
 "fit.hip":["fit.hip_contact"],
 "details.pleat":["details.pleat_topology"],
 "structure.fold_direction":["structure.pleat_direction"],
 "details.fringe":["details.tassel_fringe_braid"],
 "details.embroidery":["details.applique_embroidery_cutwork"],
 "details.eyelet":["details.lace_up_eyelet"],
 "structure.lacing_path":["structure.lacing"],
 "details.stud_attachment":["details.sequins_beads_studs"],
 "structure.slit.apex":["details.hem_slit_vent"],
}

# Narrow optional discovery names; they never enter exact/hard activation.
# This is a reviewed selection, not the original 299-row vocabulary inventory.
DISCOVERY_NAMES = {
 (1,1):["baby tee","베이비 티"], (2,1):["cropped top","크롭톱"],
 (2,2):["cropped top with high-rise trousers"],
 (3,1):["tank top","탱크톱"], (3,2):["camisole","캐미솔"],
 (4,1):["strapless tube top","스트랩리스 튜브톱"],
 (5,1):["high-front halter top"], (5,2):["tie-neck halter top"],
 (10,1):["gathered milkmaid blouse"], (10,2):["gathered peasant blouse"],
 (12,1):["openwork crochet top","오픈워크 크로셰"],
 (13,1):["sheer shirt over opaque camisole"], (14,1):["camp collar","캠프 칼라"],
 (18,1):["crew neckline","크루넥"], (19,1):["scoop neckline","스쿠프넥"],
 (20,1):["V neckline","브이넥"], (21,1):["square neckline","스퀘어넥"],
 (22,1):["sweetheart neckline","스위트하트넥"], (23,1):["straight neckline with straps"],
 (24,1):["boat neckline","보트넥"], (25,1):["cowl neckline","카울넥"],
 (26,1):["off-shoulder neckline","오프숄더"], (27,1):["one-shoulder bodice","원숄더"],
 (28,1):["cold-shoulder sleeve","콜드숄더"], (29,1):["enclosed keyhole neckline","키홀넥"],
 (31,1):["sleeveless bodice"], (31,2):["cap sleeve","캡 소매"],
 (32,1):["flutter sleeve","플러터 소매"], (32,2):["puff sleeve","퍼프 소매"],
 (33,1):["raglan seam","래글런"], (34,1):["deep armhole"],
 (36,1):["low-back high-front bodice"], (38,1):["body-skimming fabric","바디스키밍"],
 (39,1):["opaque bodycon dress"], (40,1):["bandage bodice","밴디지"],
 (41,1):["fit-and-flare dress"], (43,1):["boxy shirt","박시 셔츠"],
 (44,1):["underbust outer garment over blouse"], (44,2):["overbust bodice panels"],
 (45,1):["balconette cup outline"], (46,1):["plunge cup connector"],
 (49,1):["visible collarbones","데콜테"], (49,2):["central cleavage opening"],
 (51,1):["visible navel between garment edges"], (52,1):["high skirt slit"],
 (57,1):["slip dress","슬립 드레스"], (57,2):["shirt dress","셔츠 드레스"],
 (58,1):["shift dress","시프트 드레스"], (58,2):["A-line dress","A라인 드레스"],
 (59,1):["empire waist seam","엠파이어 절개"], (59,2):["drop-waist seam","드롭웨이스트"],
 (60,1):["tiered skirt","티어드 스커트"], (61,1):["romper","롬퍼"],
 (62,1):["midi skirt","미디 스커트"], (62,2):["mini skirt","미니 스커트"],
 (63,1):["pencil skirt"], (64,1):["pleated skirt","플리츠 스커트"],
 (65,1):["sarong waist knot","사롱"], (66,1):["high-low skirt hem"],
 (67,1):["bubble skirt hem","버블 스커트"], (67,2):["flared skirt below fitted hips"],
 (68,1):["frayed denim shorts"], (69,1):["Bermuda shorts","버뮤다 쇼츠"],
 (70,1):["puffed shorts openings"], (71,1):["close-fitting cycling-length shorts"],
 (72,1):["cargo pocket","카고 포켓"], (73,1):["skort","스코트"],
 (73,2):["wide culotte legs"], (74,1):["cropped trouser hems"],
 (75,1):["wide-leg soft trousers"], (76,1):["drawcord waistband"],
 (77,1):["high waist above navel"], (77,2):["low waist below navel"],
 (78,1):["triangle bikini panels"], (78,2):["string bikini back knot"],
 (79,1):["bandeau halter bikini"], (79,2):["longline bikini band"],
 (80,1):["tankini separate hem","탱키니"], (80,2):["connected one-piece swimsuit"],
 (81,1):["modern cutout monokini","현대 컷아웃 모노키니"],
 (82,1):["high-front low-back swimsuit"], (83,1):["high-waist high-leg swimsuit"],
 (84,1):["side-tie bikini knot"], (85,1):["narrow rear swim panel"],
 (85,2):["thong rear connector"], (86,1):["boyshort swim bottom"],
 (86,2):["small supported swim panels"], (87,1):["rashguard separate bottom"],
 (87,2):["long-sleeved surf suit"], (88,1):["loose swim shorts"],
 (89,1):["attached swim skirt"], (90,1):["connected swim hood and separate trousers"],
 (91,1):["open beach shirt over swimsuit"], (91,2):["loose swim tunic"],
 (93,1):["seersucker relief","시어서커"], (93,2):["voile layer","보일"],
 (94,1):["denim diagonal weave"], (95,1):["organza structured folds","오간자"],
 (96,1):["satin-like broad fabric highlights"], (97,1):["rib knit columns"],
 (97,2):["terry pile loops"], (98,1):["eyelet embroidery holes"],
 (98,2):["net layer over opaque inner garment"], (99,1):["side ruching seam"],
 (100,1):["gathered neckline ruffle"], (101,1):["attached hem fringe"],
 (101,2):["scalloped fabric hem"], (102,1):["crossed eyelet lacing"],
 (102,2):["ring strap connector"], (103,1):["frayed fabric opening"],
 (103,2):["attached garment studs"], (104,1):["two-color gingham check"],
 (104,2):["horizontal shirt stripes"], (105,1):["ditsy floral motifs"],
 (105,2):["large tropical leaves"], (106,1):["garment color blocking"],
 (106,2):["blurred fabric dye patches"], (109,1):["western belt and cowboy boots"],
 (109,2):["pearl ornaments on sea-colored fabric"], (110,1):["loose sports jersey above denim waist"],
 (111,1):["black openwork over opaque dress"], (112,1):["toe-post flip-flop","토포스트 플립플롭"],
 (112,2):["fisherman sandal bands","피셔맨 샌들"], (113,1):["rope-edged wedge sole"],
 (113,2):["low open-back mule"], (114,1):["translucent molded jelly shoe"],
 (114,2):["mesh flat shoe"], (114,3):["opaque molded jelly shoe"],
 (115,1):["sun visor","선바이저"], (116,1):["woven basket bag"],
 (116,2):["tied headscarf"], (117,1):["beaded anklet"],
 (118,1):["separate waist chain"], (118,2):["connected neck and waist body chain"]
}

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n")

def effects(n, v, slot):
    names = VARIANT_EFFECTS.get((n,v), EFFECTS[n]).split()
    names = list(dict.fromkeys([*names,*(q for p in names for q in PROPERTY_COMPATIBILITY.get(p,[]))]))
    def path(p):
        return p if p.startswith(("accessories.","footwear.")) else "wardrobe."+p
    rows = [dict(dimension="appearance",target="main_subject",property=path(p)) for p in names]
    dimensions = ["appearance"]
    material_names = [p for p in names if p.startswith("material.") or ".material." in p]
    if material_names:
        dimensions.append("material")
        rows.extend(dict(dimension="material",target="main_subject",property=path(p)) for p in material_names)
    if slot == "color" or "color" in names:
        dimensions.append("color")
        rows.append(dict(dimension="color",target="main_subject",property="wardrobe.color"))
    if (n,v) in {(90,1),(90,2),(116,2)}:
        rows.append(dict(dimension="appearance",target="main_subject",property="hair.visibility"))
    return dimensions, rows

def main():
    cards = {c["id"]:c for c in json.loads((RESEARCH/"semantic-cards.json").read_text())}
    proposals = json.loads((RESEARCH/"candidate-proposals.json").read_text())
    import sys
    sys.path.insert(0,str(ASSETS.parent/"scripts"))
    import prompt_generator as pg
    import photo_candidate_semantics as cs
    before = pg.load_json(ASSETS/"photo_prompt_tags.json")
    old = {e["id"]:(slot,e) for slot,entries in before["slots"].items() for e in entries}
    blobs, registries, mapping = {}, {}, []
    for p in proposals:
        c = cards[p["card_id"]]; n=int(c["id"][2:]); v=int(p["id"].rsplit("v",1)[1]); d=domain(n)
        assert len(LABELS[n]) == len(c["variants"]), (n, len(LABELS[n]),len(c["variants"]))
        ko = LABELS[n][v-1]; text=p["payload_draft"]["en"]
        ext=blobs.setdefault(d,dict(schema_version="photo-prompt-research-extension/v1",slots={},visual_semantics=[],existing_slot_context_extensions={}))
        reg=registries.setdefault(d,dict(schema_version="photo-visual-obligation-registry-extension/v1",relation_contract_version="photo-visual-relation/v1",description="Independent selected visible garment, surface, layer and accessory relations.",profiles=[]))
        if (n,v) in REUSE:
            cid=REUSE[(n,v)]; slot,entry=old[cid]
            ext["existing_slot_context_extensions"].setdefault(slot,{})[cid]={"paraphrases":[ko,text]}
            mapping.append(dict(draft_id=p["id"],card_id=c["id"],action="reuse_equivalent_and_add_reviewed_paraphrases",candidate_id=cid,slot=slot,source_ids=c["source_ids"],owner=c["owner"]))
            continue
        slot=p["slot"]; stem=f"suf_{c['id'].lower()}_v{v}"; cid=stem+"_candidate"
        units=p["payload_draft"]["concept_units"]
        relation={"id":stem+"_owner_relation",**p["payload_draft"]["relations"][0]};relation["id"]=stem+"_owner_relation"
        relation_text=f"{relation['subject']} {relation['type'].replace('_',' ')} {relation['object']}"
        dims, props=effects(n,v,slot)
        names=DISCOVERY_NAMES.get((n,v),[])
        candidate=dict(id=cid,ko=ko,en=text,weight=0.35,tags=["clothing"],aliases=[ko,text,*names],
                       keywords=[ko,*units,*names],embedding_text=" | ".join([text,ko,relation_text,*names]),concept_units=units,
                       relations=[relation],affected_dimensions=dims,affected_properties=props,
                       core_assertion_discovery=True,for_any=["human"])
        ext["slots"].setdefault(slot,[]).append(candidate)
        components=[]
        for i,unit in enumerate(units,1):
            components.append(dict(id=f"component_{i}",match_terms=[unit],evidence_field=f"component_{i}_phrase",evidence_terms=[unit],min_content_words=3,
                                   instruction="Realize this selected visible construction: "+unit,
                                   render_gate=dict(id=f"vo_{stem}_{i}",review_scale="native",description=unit+" The declared garment and boundary must be visible in this saved image; occluded or partial evidence is not a pass.")))
        if relation_text not in units:
         components.append(dict(id="owner_relation",match_terms=[relation_text],evidence_field="owner_relation_phrase",evidence_terms=[relation_text],min_content_words=3,
                               instruction="Keep the declared owner and both relationship endpoints visible: "+relation_text,
                               render_gate=dict(id=f"vo_{stem}_owner",review_scale="native",description="Read both endpoints and their connection on the same declared garment, layer or accessory: "+relation_text+" Hidden endpoints or a different owner are not a pass.")))
        profile=dict(id=stem,category="summer_"+d+"_selected_visible_relation",
                     activation=dict(exact_terms=[text],requires_adult_character=((n==49 and v==2) or n in {50,55,85,86}),semantic_discovery_requires_component_evidence=True,
                                     hard_activation=dict(contract_version="photo-visual-hard-activation/v1",required_any_groups=[dict(id="complete_selected_variant",any_terms=[text])])),
                     semantics=dict(definition=text,paraphrase_examples=list(dict.fromkeys([ko,relation_text,*names])),visual_components=list(dict.fromkeys([*units,relation_text])),contrast_examples=[c["confusion_boundary"]],
                                    claim_limits=[c["observation_condition"],"One selected variant; alternatives never form a combined obligation.","Garment appearance does not establish identity, body dimensions, age, fiber composition, hidden construction, performance or change history."]),
                     authored_components=dict(contract_version="photo-authored-visual-components/v1",components=components),
                     concept_candidate=dict(concept_terms=[ko,text,*names],core_assertion_discovery=True,affected_dimensions=dims,affected_properties=props),
                     runtime_expression=dict(default_mode="definition_with_optional_label",prompt_label_terms=[],forbidden_prompt_terms=[],runtime_forbidden_labels=[]),reject_substitutes=[c["confusion_boundary"]])
        reg["profiles"].append(profile)
        ext["visual_semantics"].append(dict(id=stem+"_bundle",primary_visual_proposition=text,hard_profile_ids=[stem],
             component_groups=[dict(id=x["id"],visible_evidence=x["evidence_terms"]) for x in components],
             candidate_ids=[cid],candidate_slots={cid:slot},confusion_boundaries=[c["confusion_boundary"]],source_keywords=[ko,text],
             candidate_only=True,activation_mode="component_complete_exact_only",relations=[relation]))
        mapping.append(dict(draft_id=p["id"],card_id=c["id"],action="add_independent_visible_relation",candidate_id=cid,profile_id=stem,bundle_id=stem+"_bundle",slot=slot,
                            domain=d,source_ids=c["source_ids"],owner=c["owner"],affected_dimensions=dims,affected_properties=props))
    for c in cards.values():
        if not c["variants"]:
            mapping.append(dict(card_id=c["id"],action="preserve_nonvisual_specification_no_automatic_pixel_claim",source_ids=c["source_ids"],seed_term_ids=c["seed_term_ids"],meaning=c["meaning_ko"]))
    dump(HERE/"draft-to-runtime.json",mapping)
    record=dict(contract_version="summer-fashion-maintenance/v1",record_id="summer-fashion-visible-relations-20261009",research_manifest_sha256=hashlib.sha256((RESEARCH/"final-validation.json").read_bytes()).hexdigest(),
                policy="Reuse reviewed equivalent meaning; independent variants and complete effects; source URLs only in research evidence.",
                promoted=mapping,counts=dict(research_drafts=len(proposals),new_candidates=sum(len(es) for x in blobs.values() for es in x["slots"].values()),new_profiles=sum(len(r["profiles"]) for r in registries.values()),reused_candidates=len(REUSE),metadata_only_cards=4))
    dump(HERE/"maintenance-record.json",record)
    manifest=json.loads((ASSETS/"photo_prompt_source_manifest.json").read_text())
    names=[]
    for d in sorted(blobs):
        ext=blobs[d]
        if not ext["existing_slot_context_extensions"]:ext.pop("existing_slot_context_extensions")
        cn=f"photo_prompt_summer_{d}_extension.json";pn=f"photo_prompt_visual_obligations_summer_{d}.json"
        domain_record={**record,"schema_version":"photo-extension-maintenance/v1","maintenance_only":True,
                       "record_id":f"summer-fashion-{d}-20261009","authored_source_sha256":cs.digest(ext),
                       "source_filename":cn,"runtime_keys":sorted(ext),
                       "promoted":[x for x in mapping if x.get("domain")==d or (x.get("action","").startswith("reuse_") and domain(int(x['card_id'][2:]))==d)]}
        dump(ROOT/"docs/research-evidence/photo-prompt/extension-maintenance"/(domain_record["record_id"]+".json"),domain_record)
        ext["maintenance_ref"]=dict(contract_version="photo-extension-maintenance-ref/v1",record_id=domain_record["record_id"],sha256=cs.digest(domain_record))
        dump(ASSETS/cn,ext);dump(ASSETS/pn,registries[d]);names.extend([cn,pn])
        for name,kind in [(cn,"candidate"),(pn,"visual_profile")]:
            existing=[s for s in manifest["sources"] if s["file"]==name]
            if existing:
                assert len(existing)==1 and existing[0]["kind"]==kind and existing[0]["required"] is True, name
                continue
            order=max(s["load_order"] for s in manifest["sources"] if s["kind"]==kind)+1
            manifest["sources"].append(dict(file=name,kind=kind,required=True,load_order=order))
    dump(ASSETS/"photo_prompt_source_manifest.json",manifest)
    dump(HERE/"integration-scope.json",dict(new_source_files=names,modified_existing=["photo_prompt_source_manifest.json"],counts=record["counts"],
          storage_choice="Seven existing semantic domains use separate additive contributions. No new slots, no duplicate independent store, and no source changes to previously authored candidate/profile records."))
    print(json.dumps(record["counts"]))

if __name__=="__main__":main()
