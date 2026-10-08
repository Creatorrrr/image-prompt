"""Review, author and register soil data; research prose stays outside assets."""
from __future__ import annotations
import argparse, copy, hashlib, importlib.util, json, sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
RESEARCH = OUT.parent
ROOT = OUT.parents[4]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
ASSETS = SKILL / 'assets'
sys.path.insert(0, str(SKILL / 'scripts'))
from photo_candidate_semantics import validate_candidate_entries
from photo_contracts import INTENT_LOCK_DIMENSIONS
from visual_profile_contracts import validate_visual_profile_source, compile_visual_profile
from photo_runtime_sources import source_update

spec = importlib.util.spec_from_file_location('soil_research_author', RESEARCH/'author_research.py')
research_author = importlib.util.module_from_spec(spec)
spec.loader.exec_module(research_author)

KO_ROWS = '''
E004|고운 퇴적물 속 둥근 자갈|크기가 다른 자갈의 구분되는 가장자리|자갈 사이를 채우는 고운 기질
E006|흙 단면 안에 겹친 얇은 수평 입단|같은 입단을 구획하는 분리면|노출된 흙 구조 옆의 센티미터 눈금
E013|구멍이 구분되는 노출 흙 단면|단면 안으로 이어지는 뿌리 굵기의 통로|통로 입구 주위의 부스러기형 입단 경계
E018|한 흙 단면의 밝은 중간 띠|밝은 띠 바로 아래의 어두운 띠|같은 단면에서 두 띠를 잇는 연속 경계
E020|퇴적층 아래에 묻힌 흙 같은 띠|그 띠 위를 덮는 퇴적물 묶음|두 묶음의 위아래 관계가 보이는 한 노출면
E022|두껍고 어두운 지표 가까운 흙 띠|어두운 띠 바로 아래의 대비되는 흙 띠|어두운 상부 띠 안으로 들어가는 풀뿌리
E024|느슨하고 입자가 드러난 흙 표본|표본 옆에서 구분되는 다공성 암편|흙 표본과 별도 재 표본 사이의 경계
E025|어두운 유기물 덩어리 안의 알아볼 수 있는 식물 섬유|같은 덩어리 옆면에서 겹쳐 눌린 섬유|그 덩어리에 속한 젖은 절단 가장자리
E026|한 점토질 단면의 쐐기 모양 입단|같은 입단에 속한 매끈하고 홈이 난 면|지표에서 아래로 이어지는 깊은 틈
E027|노출된 흙 단면의 회색 기질|같은 회색 기질 안의 녹빛 반점|반점이 있는 흙을 가로지르는 뿌리 통로
E028|한 흙 표면에 붙은 흰 결정 피막|깨진 피막 가장자리 아래 보이는 갈색 바탕|그 가장자리에서 낱개로 구분되는 도톰한 결정
E029|강둑 절개면의 얇은 퇴적 띠|고운 띠 사이에 끼어 있는 굵은 입자 띠|같은 넓은 프레임에 보이는 인접한 강
E030|느슨한 모래가 주를 이루는 깊은 흙 절개|절개 가장자리에서 구분되는 모래알|같은 모래 절개 안으로 드문드문 들어가는 뿌리
E031|한 흙 단면 안에 박힌 밝은 결절|깨진 결절 안쪽에서 보이는 흰 물질|같은 결절을 둘러싼 대비되는 고운 흙 기질
E037|가파른 흙 양옆을 가진 깊게 파인 도랑|도랑 상단의 급하게 꺾인 침식 두부|같은 도랑벽 옆에 있는 크기 기준
E040|물길 입구의 혀 모양 혼합 퇴적물|고운 진흙 기질에서 튀어나온 큰 암편|같은 퇴적물 양옆을 구획하는 융기 띠
E041|한 사면 위쪽의 활 모양 노출 턱|그 턱 아래로 이어지는 어긋난 흙 덩어리|같은 사면 아래 끝에서 불룩한 퇴적부
E042|급한 사면 위의 깨진 암벽|그 암벽 아래에 모인 각진 암편|작은 암편 사이에 놓인 큰 암괴
E043|주변 테두리가 이어지는 닫힌 지표 함몰|같은 테두리 일부에 드러난 흙과 암석|테두리보다 낮은 함몰 바닥
E044|새로 흩어진 모래에 둘러싸인 분사 구멍|같은 교란 지면 안의 가까운 균열|그 교란면 곁에서 기울어진 물체
E045|지면을 덮는 불투수성 포장 가장자리|포장 가장자리 아래로 이어지는 노출 흙|같은 가장자리의 보이는 피복 경계
E047|가파른 옆면에 둘러싸인 넓고 평평한 정상|가까이에 따로 솟은 더 작은 평탄 정상 지형|두 지형 사이를 잇는 낮은 평원
E048|낮은 안부 양옆의 높은 능선 두 구간|두 능선 사이를 잇는 낮은 고갯길|같은 안부 아래에 놓인 계곡 바닥
E049|깨진 암석 표면의 풍화된 바깥 피막|같은 파단면의 더 신선한 내부|그 파단면 바로 아래의 느슨한 알갱이
E050|좁은 산지 출구에서 퍼지는 부채꼴 퇴적체|그 꼭짓점으로 이어지는 좁은 물길|넓어지는 퇴적체를 받는 열린 평원
E051|낮은 퇴적 능선에 둘러싸인 물길|같은 물길 옆으로 이어지는 낮은 능선|그 능선 뒤쪽의 더 낮고 젖은 지면
E052|본류에서 떨어져 있는 굽은 수역|그 굽은 수역과 강 사이를 가르는 육지|같은 공중 시점에서 보이는 가까운 본류
E053|퇴적 사주를 사이에 두고 갈라지는 얕은 물길들|갈라진 물길들로 둘러싸인 노출 자갈 사주|하류에서 다시 이어지는 갈라졌던 물길
E054|현재 강보다 높은 평탄한 단|그 단과 아래 범람원을 가르는 계단 모양 사면|같은 단 아래를 흐르는 현재 강
E055|큰 육지 두 덩어리를 잇는 좁은 목|그 목 양옆의 물|그 목을 통해 연속으로 이어지는 두 육지
E056|본토와 앞바다 섬을 잇는 퇴적 띠|그 띠 바깥쪽 끝에 붙은 섬|연결 띠의 양옆을 둘러싼 물
E057|얕은 조수 물길 옆의 젖고 고운 퇴적 평면|같은 평면에 갈라져 팬 배수 홈|그 평면 곁의 물러난 수면 경계
E058|바닷물에 둘러싸인 고립 바위기둥|같은 수면 경계 위의 가까운 해안 절벽|절벽과 바위기둥 사이를 끊김 없이 가르는 바다
E059|두 뿔이 뻗은 초승달 모양 모래 능선|그 능선 한쪽의 더 급한 사면|같은 능선 반대쪽의 더 완만한 사면
E060|한 모래 표면에 반복되는 낮은 사련 능선|그 능선 사이의 마른 모래 골|같은 사련 패턴 옆의 작은 크기 기준
E061|수직 틈이 있는 고운 퇴적물 절벽|같은 절개면 전체에 드러난 고운 물질|그 절개 너머로 이어지는 주변 지형
E062|식생이 드문 지형에 나란히 길게 뻗은 능선들|그 능선 사이를 따라 이어지는 침식 골|같은 능선들을 받치는 공통 지면
E063|마른 지형을 덮는 촘촘한 자갈 표면|그 자갈 사이에서 보이는 고운 기질|자갈 피복과 구분되는 가까운 느슨한 모래 부분
E064|어두운 통로로 이어지는 경계 있는 동굴 입구|같은 입구 통로를 둘러싼 연속 암벽|바깥 지면과 끊기지 않고 이어지는 입구 바닥
E065|동굴 천장에 붙어 아래로 가늘어지는 구조|그 아래 바닥에 붙어 위로 자란 구조|천장과 바닥을 잇는 별도의 연속 기둥
E066|가파른 양옆을 가진 넓은 U자 계곡|양옆 사이의 비교적 넓은 계곡 바닥|같은 계곡 상류 끝의 그릇 모양 분지
E067|빙하 가장자리 옆으로 이어지는 암편 능선|같은 능선에서 구분되는 다양한 크기의 암편|같은 넓은 시야에 보이는 인접한 빙하 가장자리
E068|얼음 쐐기가 노출된 동결 지면 절개|같은 절개 안으로 아래로 뻗는 얼음 쐐기|쐐기 위 지표의 다각형 경계
E069|해빙 웅덩이 곁의 낮게 꺼진 지면|같은 낮은 함몰 안의 고인 물|그 웅덩이 곁의 불규칙한 가장자리
E070|한 암석 노출면 안에서 휘어진 연속 층 띠|여러 이웃 띠가 함께 휘는 굽힘 중심|그 습곡 전체를 담는 하나의 암면
E072|암석 표본에서 맞물리는 밝고 어두운 결정|같은 결정을 드러내는 신선한 파단면|표본 가장자리 옆의 크기 기준
E073|한 암석 표본을 가로지르는 대비되는 광물 띠|같은 띠 양옆에 보이는 모암|그 광물 띠를 구획하는 두 접촉 경계
E077|한 젖은 흙 표면의 마디 있는 지렁이|같은 동물 옆의 작은 굴 입구|그 입구 가까이의 작은 구불구불한 분변토
E078|흙 둥지 입구 옆에서 구분되는 개미|주변에 느슨한 알갱이가 있는 한 입구|그 입구 가까이 옮겨지거나 밀려난 알갱이
E082|한 밭 구간의 흙을 파고드는 경운 도구|그 도구 뒤로 이어지는 새 고랑|같은 고랑 옆으로 뒤집혀 놓인 흙덩이
E083|살아 있는 작물 줄 사이의 흙을 덮는 식물 잔재|같은 잔재층 사이로 나오는 어린 싹|그 잔재 사이에서 작게 드러난 흙 표면
E084|한 언덕 사면을 따라 계단으로 내려가는 경작 단|이웃 경작 단 사이의 급한 단차|사면을 곧장 내려가지 않고 단을 따르는 작물 줄
E085|섬유 조각과 굵은 포함물이 섞인 재배 기질|그 기질을 담는 한 식물 용기|같은 용기 안 기질로 들어가는 뿌리
E087|불규칙하고 둥근 가장자리의 연속 흙벽|같은 벽의 국소 손상부에서 보이는 섬유|모듈 벽돌 줄눈 대신 이어지는 흙 재료
E090|한 벽 가장자리의 뿌리로 묶인 잔디 덩어리|그 덩어리를 한데 잡는 촘촘한 뿌리|흙 지붕층 아래의 지지 구조
E091|흙 양옆이 노출된 열린 굴착 도랑|그 도랑 곁에 따로 놓인 파낸 흙더미|도랑 바닥까지 이어지는 연속 절개면
E092|능선 꼭대기가 끊기지 않는 긴 흙 둑|같은 둑 한쪽을 나란히 따르는 도랑|그 둑과 도랑을 잇는 공통 지면
E094|기존 점토 그릇 입구에 붙이는 점토 코일|같은 그릇 아래 벽을 이루는 앞선 코일들|그 접합부를 문질러 붙이는 손가락 끝
E096|굽에서 드러나는 무광 적색 도자기 몸체|그 굽 위에서 끝나는 광택 유약|유약과 같은 점토 몸체 사이의 보이는 경계
E097|한 곳에 모인 갈색 흙 안료 분말|같은 분말 옆의 바인더를 섞은 색 견본|분말 곁에 따로 놓인 바인더 용기
E098|한 장소에서 의도적으로 배열된 흙과 돌|그 배열과 끊김 없이 이어지는 주변 지형|같은 배열의 장소 규모를 보여주는 크기 단서
E099|구획된 발굴 격자 곁의 층진 노출면|층 경계에 일부 박힌 도자기 조각|그 조각과 층 접촉면 옆의 눈금
E100|둥근 흙 봉분|그 봉분의 바닥 둘레로 이어지는 경계|같은 봉분 둘레에서 이어지는 주변 지면
E101|흙 양옆이 연속인 좁게 파인 통로|같은 통로의 진흙 바닥에 놓인 나무 판|같은 통로 위 가장자리 일부에 놓인 모래주머니
E102|교란되어 솟은 테두리가 있는 지면 함몰|그 테두리 곁으로 밀려난 흙 조각|그 흙 가까이에 일부 묻힌 생활 물체
E105|한 마을 마당에서 함께 연주하는 농악 연행자들|같은 연행자가 들고 있는 타악기|그 집단 아래로 연속되는 마당 지면
E106|용기에서 한 지면 부분으로 붓는 액체|같은 지점 위에 들고 있는 붓는 용기|그 지면 곁에 따로 놓인 돌 봉헌 더미
E107|흙 재료로 구성된 사람 형태 몸체|같은 몸체에 이어지는 덩어리 관절|한 물체에 작용하는 손 옆의 흙 부스러기
E108|지면과 떨어져 떠 있는 층진 흙 덩어리|그 덩어리 아래 노출면에서 매달린 뿌리|같은 덩어리 아래의 연속 공기 틈
E116|연속으로 솟은 테두리를 가진 한 분화구|그 테두리 밖으로 방사상 뻗은 거친 퇴적물|같은 분화구 바깥으로 이어지는 주변 지형
'''

REUSE = {'E012':('surface_material','water_w120','water_rel_w120'),
 'E035':('location','water_w002','water_rel_w002'),
 'E052':('location','water_w069','water_rel_w069'),
 'E053':('location','water_w070','water_rel_w070'),
 'E056':('location','water_w077','water_rel_w077')}

LABELS = {
 'E018':'밝은 중간 흙 띠와 아래 어두운 띠', 'E020':'퇴적물 아래 묻힌 흙 같은 띠',
 'E022':'풀뿌리가 들어가는 두꺼운 어두운 표층', 'E024':'다공성 암편과 구분되는 흙·재 표본',
 'E026':'쐐기 입단과 매끈한 홈 면', 'E027':'회색 흙 바탕 안의 녹빛 반점',
 'E029':'강둑 단면의 굵고 고운 퇴적 띠', 'E030':'느슨한 모래 절개와 드문 뿌리',
 'E031':'흙 기질 안의 밝은 결절', 'E037':'깊은 흙 도랑과 상단 턱',
 'E043':'둘레가 닫힌 지표 함몰', 'E044':'모래 분사공과 인접한 지면 균열',
 'E047':'넓고 작은 평탄 정상 지형의 대비', 'E055':'두 육지를 잇는 좁은 목',
 'E057':'젖은 고운 갯벌과 배수 홈', 'E059':'초승달 모래 능선의 비대칭 사면',
 'E061':'수직 틈을 가진 고운 퇴적 절벽', 'E062':'나란한 긴 침식 능선',
 'E064':'암벽으로 둘러싸인 동굴 입구', 'E066':'넓은 U자 계곡과 상류 분지',
 'E067':'빙하 가장자리의 혼합 암편 능선', 'E068':'다각형 지표 아래의 노출 얼음 쐐기',
 'E069':'낮게 꺼진 지면과 연결된 웅덩이', 'E070':'연속 층 띠가 휜 습곡 암면',
 'E073':'모암을 가로지르는 대비 광물 띠', 'E078':'개미와 흙 둥지 입구',
 'E083':'작물 사이의 식물 잔재 피복', 'E085':'식물 용기 속 섬유·입자 배지',
 'E090':'뿌리로 묶인 잔디 블록과 흙 지붕 지지부', 'E091':'열린 굴착 도랑과 파낸 흙더미',
 'E092':'연속 흙 둑과 평행 도랑', 'E096':'무광 도자기 굽과 유약 경계',
 'E097':'흙 안료 분말과 바인더 색 견본', 'E098':'지면과 이어지는 흙·돌 배열',
 'E100':'둘레가 보이는 닫힌 흙 봉분', 'E102':'교란된 지면 테두리와 일부 묻힌 생활 물체',
 'E105':'마당 지면과 농악 연행의 배치', 'E106':'땅으로 붓는 액체와 별도 돌 봉헌',
 'E110':'기존 의복 표면의 국소 진흙 부착', 'E116':'연속 분화구 테두리와 방사상 퇴적물',
}

def read(p): return json.loads(p.read_text())
def dump(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 parser=argparse.ArgumentParser(); parser.add_argument('--apply',action='store_true'); args=parser.parse_args()
 units={u['id']:u for u in read(RESEARCH/'research-units.json')['units']}
 ko=copy.deepcopy(research_author.KOREAN_COMPONENTS)
 for line in KO_ROWS.strip().splitlines():
  uid,*phrases=line.split('|'); ko[uid]=phrases
 # One visible realization per source row. Survey apparatus stays in separately
 # selected survey variants; names/diagnoses do not become visual duties.
 override={
  'E002':('구분되는 자연 모래알', [('sand','individual coarse grains resolved on one sand patch','한 모래 표면에서 구분되는 굵은 모래알'),('sand','small shadows between adjacent grains on that patch','같은 모래알 사이의 작은 그림자'),('sand_patch','a continuous granular bed around those resolved grains','구분된 알갱이 주위로 이어지는 모래 바탕')]),
  'E006':('단면 안의 얇은 판상 입단',[('soil_face','thin horizontal peds stacked within one soil face','한 흙 단면 안에 겹친 얇은 수평 입단'),('ped_boundary','separation planes bounding those same peds','같은 입단의 경계를 이루는 분리면'),('soil_face','continuous soil material around the stacked peds','겹친 입단 주위로 이어지는 흙 기질')]),
  'E016':('지표에서 아래로 이어지는 토양 단면',[('soil_cut','a continuous vertical soil exposure from surface downward','지표에서 아래로 이어지는 연속 수직 흙 노출면'),('horizon_boundary','irregular boundaries separating contrasting soil bands','대비되는 흙 띠를 가르는 불규칙한 경계'),('soil_cut','the same cut face continuing beneath the lowest visible band','가장 아래 보이는 띠 밑으로 이어지는 같은 절개면')]),
  'E021':('입자 표면을 가진 적갈색 흙',[('soil_patch','a reddish brown soil patch with visible granular texture','입자 질감이 보이는 적갈색 흙 표면'),('grain','small grains carrying the same reddish brown hue','같은 적갈색을 띠는 작은 흙 알갱이'),('color_boundary','a visible edge confining that hue to the soil patch','그 색을 같은 흙 표면에 한정하는 경계')]),
  'E037':('깊은 흙 도랑과 상단 턱',[('gully','a deeply incised channel with steep soil sides','가파른 흙 양옆을 가진 깊은 도랑'),('headcut','an abrupt headcut at the upper channel end','같은 도랑 상단의 급한 침식 두부'),('gully_floor','a continuous channel floor beneath the headcut','그 두부 아래로 이어지는 같은 도랑 바닥')]),
  'E060':('한 모래 표면의 반복 사련',[('ripple','repeated low ripple ridges on one sand patch','한 모래 표면의 반복되는 낮은 사련 능선'),('trough','dry sandy troughs between those same ridges','같은 능선 사이의 마른 모래 골'),('sand_patch','one continuous sand patch carrying ridge and trough','능선과 골이 함께 놓인 하나의 모래 바탕')]),
  'E100':('둘레가 보이는 닫힌 흙 봉분',[('mound','a rounded earthen mound above the surrounding ground','주변 지면 위의 둥근 흙 봉분'),('mound_base','a continuous visible base boundary around that mound','같은 봉분 둘레의 연속으로 보이는 바닥 경계'),('ground','surrounding ground adjoining the mound base','그 바닥과 맞닿아 이어지는 주변 지면')]),
  'E110':('기존 의복 표면의 국소 진흙 부착',[('garment','the existing garment fabric retaining its seams and folds','원래 봉제선과 주름이 유지되는 의복 천'),('mud_deposit','raised muddy clumps attached near that garment hem','같은 의복 밑단 가까이에 붙은 도톰한 진흙덩이'),('stain_edge','a bounded deposit edge adjoining clean fabric on that garment','같은 의복의 깨끗한 천과 맞닿은 국소 부착물 경계')]),
 }
 variants=[
  ('E004','angular','각진 쇄석과 고운 기질',[('gravel','angular broken stones embedded in finer soil','고운 흙에 박힌 각진 쇄석'),('edge','fresh sharp edges belonging to those same stones','같은 돌에 속한 날카로운 파단 가장자리'),('matrix','fine material filling gaps between the angular stones','같은 각진 돌 사이를 채우는 고운 기질')]),
  ('E006','columnar','흙 단면의 수직 기둥형 입단',[('ped','vertical column-like peds within one soil face','한 흙 단면의 수직 기둥형 입단'),('boundary','vertical separation surfaces between those same peds','같은 입단 사이의 수직 분리면'),('soil_face','continuous surrounding soil carrying those columns','같은 기둥들을 담는 주변의 연속 흙 기질')]),
  ('E024','ash','암편과 구분되는 느슨한 재 표본',[('ash','a loose fine ash sample in one specimen tray','한 표본 접시의 느슨하고 고운 재 표본'),('rock','porous rock fragments in a separate adjoining tray','별도 인접 접시의 다공성 암편'),('boundary','a clear tray boundary separating ash and rock fragments','재와 암편을 가르는 명확한 접시 경계')]),
  ('E070','fault','같은 층의 단층 어긋남',[('layer','matching layered rock bands on both sides of a fracture','균열 양옆에서 대응되는 암석 층 띠'),('fracture','a fracture cutting across those layered bands','같은 층 띠들을 가로지르는 균열'),('offset','a visible displacement between matching bands across that fracture','같은 균열 양옆 대응 층 띠의 보이는 어긋남')]),
  ('E094','slab','점토 판 접합과 눌린 이음',[('slab','two clay slabs meeting along one vessel wall seam','한 그릇벽의 이음에서 만나는 두 점토 판'),('junction','soft clay pressed across that same seam','같은 이음 위에 눌려 이어진 부드러운 점토'),('hand','fingertips smoothing the junction on that vessel','그 그릇의 같은 접합부를 문지르는 손가락 끝')]),
  ('E100','chamber','열린 석실의 벽과 내부 바닥',[('chamber','an open stone chamber with continuous wall blocks','벽 돌이 이어지는 열린 석실'),('floor','a visible floor bounded by those same chamber walls','같은 벽으로 둘러싸인 보이는 내부 바닥'),('opening','an unobstructed opening exposing that chamber interior','같은 내부를 드러내는 가리지 않은 입구')]),
 ]
 candidates=[]; profiles=[]; mappings=[]; enrich={}; profile_enrich=[]
 def author(uid, suffix='', variant=None):
  u=units[uid]; slot=u['proposed_slot']; key=uid.lower()+('_'+suffix if suffix else '')
  label=LABELS.get(uid,u['label_ko'])
  triples=[(c['owner'],c['visible_phrase_en'],ko[uid][i]) for i,c in enumerate(u['components'])]
  if uid in override: label,triples=override[uid]
  if variant: label,triples=variant
  # These component words describe the image; they carry no source title/URL.
  en=[v[1].replace('documented ','') for v in triples]; local=[v[2] for v in triples]
  proposition='; '.join(en)+'.'; korean='; '.join(local)
  effects=[dict(dimension=d,target=t,property=p) for d,t,p in [research_author.SCOPE[slot],*research_author.EXTRA_EFFECTS.get(uid,[])]]
  if uid in {'E014','E093','E094'}: effects.append(dict(dimension='material',target='clay_object',property='surface_shape'))
  if uid=='E093': effects.extend([dict(dimension='setting',target='pottery_wheel',property='object.arrangement'),dict(dimension='appearance',target='main_subject',property='skin.surface_coating')])
  if uid=='E106': effects.append(dict(dimension='pose',target='main_subject',property='hand.container_contact'))
  if uid=='E097': effects.append(dict(dimension='setting',target='selected_prop',property='object.arrangement'))
  if uid=='E077': effects.append(dict(dimension='setting',target='selected_terrain',property='burrow_and_casts'))
  if uid=='E078': effects.append(dict(dimension='setting',target='selected_terrain',property='nest_opening'))
  if uid=='E105': effects.extend([dict(dimension='count',target='selected_actor',property='performer_group'),dict(dimension='appearance',target='selected_actor',property='held_instruments')])
  if uid=='E109': effects=[dict(dimension='appearance',target='main_subject',property='skin.surface_coating'),dict(dimension='material',target='main_subject',property='skin.surface_deposit')]
  # E109 shows a retained fingertip trace, not a required currently touching hand.
  dimensions=list(dict.fromkeys(e['dimension'] for e in effects))
  related=triples[1][0] if triples[1][0]!=triples[0][0] else triples[2][0]
  relation=[dict(id=key+'_relation_1',subject=related,type='adjoins',object=triples[0][0])]
  if not variant and uid not in override: relation=copy.deepcopy(u['relations'])
  local_relations={
   ('E002',''):('sand','part_of','sand_patch'),('E006',''):('ped_boundary','bounds','soil_face'),
   ('E016',''):('horizon_boundary','crosses','soil_cut'),('E021',''):('grain','part_of','soil_patch'),
   ('E037',''):('gully_floor','below','headcut'),('E060',''):('ripple','part_of','sand_patch'),
   ('E100',''):('mound','above','ground'),('E004','angular'):('matrix','surrounds','gravel'),
   ('E006','columnar'):('boundary','bounds','ped'),('E024','ash'):('ash','separated_from','rock'),
   ('E070','fault'):('fracture','crosses','layer'),('E094','slab'):('hand','contacts','junction'),
   ('E100','chamber'):('chamber','bounds','floor')}
  if (uid,suffix) in local_relations:
   subject,rel_type,obj=local_relations[(uid,suffix)]
   relation=[dict(id=key+'_relation_1',subject=subject,type=rel_type,object=obj)]
  if uid=='E109': relation=[dict(id=key+'_relation_1',subject='mud_coat',type='adheres_to',object='skin'),dict(id=key+'_relation_2',subject='finger_track',type='crosses',object='mud_coat')]
  if uid=='E110': relation=[dict(id=key+'_relation_1',subject='mud_deposit',type='adheres_to',object='garment')]
  limits=['A selected physical realization is optional and preserves the frozen requester meaning and owner-specific property locks.',
   'Still pixels do not establish classification, chemical identity, origin, duration, fertility, smell, sound, cultural identity, intent, consent or desire.',
   'A name or approximate retrieval hit does not activate this complete realization as a hard duty.']
  boundary=u['confusion_boundary_ko']
  c={'id':'soil_'+key,'ko':label,'en':'; '.join(en),'weight':0.45,'tags':['earth_material'],
   'aliases':[],'keywords':[label,*local,*en],'paraphrases':[korean,proposition],
   'embedding_text':label+'; '+korean+'; '+proposition,'concept_terms':en,'concept_units':en,'relations':relation,
   'affected_dimensions':dimensions,'affected_properties':effects,'core_assertion_discovery':True,
   'contextual_usage':{'contexts':[{'id':'soil_'+key+'_boundary','definition':boundary,'observable_interpretation':'; '.join(en),
     'claim_limits':limits,'activation_authority':'interpretation_only_not_a_required_visual_recipe'}]}}
  # Discovery may match partial material evidence. Explicit selection always
  # promotes all duties below; partial native pixels still fail.
  comp=[]
  for i,(owner,phrase,lp) in enumerate(zip([t[0] for t in triples],en,local),1):
   cid=key+'_component_'+str(i)
   comp.append({'id':cid,'match_terms':[phrase,lp], 'evidence_field':cid+'_phrase','evidence_terms':[phrase],
    'min_content_words':3,'instruction':'Preserve this selected component on the same declared owner: '+phrase+'.',
    'render_gate':{'id':'vo_soil_'+cid,'review_scale':'native','description':f'{phrase} must be visible on {owner} in the same relevant surface/frame; missing, partial, hidden or wrongly owned evidence fails.'}})
  p={'id':'soil_rel_'+key,'category':'soil_earth_owned_observation',
   'activation':{'exact_terms':[proposition],'requires_adult_character':False,'semantic_discovery_requires_component_evidence':True,
    'hard_activation':{'contract_version':'photo-visual-hard-activation/v1','required_any_groups':[{'id':'complete_owned_proposition','any_terms':[proposition]}]}},
   'semantics':{'definition':'; '.join(en),'paraphrase_examples':[label,korean], 'visual_components':en,
    'contrast_examples':[boundary],'claim_limits':limits},
   'authored_components':{'contract_version':'photo-authored-visual-components/v1','components':comp},
   'concept_candidate':{'concept_terms':en,'core_assertion_discovery':True,'affected_dimensions':dimensions,'affected_properties':effects},
   'runtime_expression':{'default_mode':'definition_with_optional_label','prompt_label_terms':[],'forbidden_prompt_terms':[],'runtime_forbidden_labels':[]},
   'reject_substitutes':[boundary]}
  validate_visual_profile_source(p); compiled=compile_visual_profile(p)
  return slot,c,p,len(compiled['render_gates'])
 for uid,u in units.items():
  if u['proposed_slot'] is None:
   mappings.append({'research_unit_id':uid,'disposition':'maintenance_context_only','reason':u['capture_policy'],'candidate_ids':[],'profile_ids':[]}); continue
  if uid=='E023':
   mappings.append({'research_unit_id':uid,'disposition':'shared_physical_realization','reason':'Pale/dark bands share E018; Podzol diagnostic identity is not a pixel duty.','candidate_ids':['soil_e018'],'profile_ids':['soil_rel_e018']}); continue
  slot,c,p,gates=author(uid)
  if uid in REUSE:
   slot,cid,pid=REUSE[uid]; enrich.setdefault(slot,{})[cid]={'paraphrases':c['paraphrases'],'contexts':c['contextual_usage']['contexts']}
   profile_enrich.append((pid,c['paraphrases']))
   mappings.append({'research_unit_id':uid,'disposition':'equivalent_enrichment_existing_ids','candidate_ids':[cid],'profile_ids':[pid]}); continue
  candidates.append((slot,c)); profiles.append(p)
  mappings.append({'research_unit_id':uid,'disposition':'new_physical_realization','candidate_ids':[c['id']],'profile_ids':[p['id']], 'source_ids':u['source_ids'], 'named_context_not_identity_proof':u['representation_mode']=='named_context'})
 for uid,suffix,label,triples in variants:
  slot,c,p,gates=author(uid,suffix,(label,triples)); candidates.append((slot,c)); profiles.append(p)
  mappings.append({'research_unit_id':uid,'disposition':'separate_variant','candidate_ids':[c['id']],'profile_ids':[p['id']]})
 slots={}
 for slot,c in candidates: slots.setdefault(slot,[]).append(c)
 extension={'schema_version':'photo-prompt-research-extension/v1','slots':slots,'existing_slot_context_extensions':enrich}
 visual={'schema_version':'photo-visual-obligation-registry-extension/v1','relation_contract_version':'photo-visual-relation/v1','profiles':profiles}
 validate_candidate_entries(extension,set(INTENT_LOCK_DIMENSIONS))
 # Prepare reviewed artifacts before any live mutation.
 dump(OUT/'candidate-source.proposed.json',extension); dump(OUT/'visual-source.proposed.json',visual)
 record={'new_candidates':len(candidates),'new_profiles':len(profiles),'new_compiler_gates':sum(len(compile_visual_profile(p)['render_gates']) for p in profiles),
  'existing_candidate_enrichments':sum(len(v) for v in enrich.values()),'existing_profile_enrichments':len(profile_enrich),
  'decisions':mappings,'source_evidence_file':'../sources.json','scope':'Authored physical realizations; context, diagnostic claims and unsupported provenance remain research records.'}
 dump(OUT/'integration-map.json',record)
 if args.apply:
  targets={'photo_prompt_soil_earth_extension.json':extension,'photo_prompt_visual_obligations_soil_earth.json':visual}
  manifest_path=ASSETS/'photo_prompt_source_manifest.json'
  water_path=ASSETS/'photo_prompt_visual_obligations_water_relations.json'
  with source_update(SKILL):
   manifest=read(manifest_path); water=read(water_path)
   for name in targets:
    if (ASSETS/name).exists(): raise RuntimeError('Existing source would be overwritten: '+name)
   dump(OUT/'manifest.before.json',manifest); dump(OUT/'water-profiles.before.json',water)
   by_id={p['id']:p for p in water['profiles']}
   for pid,phrases in profile_enrich:
    dest=by_id[pid]['semantics']['paraphrase_examples']
    for phrase in phrases:
     if phrase not in dest: dest.append(phrase)
   for name,payload in targets.items(): dump(ASSETS/name,payload)
   for name,kind in [('photo_prompt_soil_earth_extension.json','candidate'),('photo_prompt_visual_obligations_soil_earth.json','visual_profile')]:
    order=max(r['load_order'] for r in manifest['sources'] if r['kind']==kind)+1
    manifest['sources'].append({'file':name,'kind':kind,'required':True,'load_order':order})
   dump(water_path,water); dump(manifest_path,manifest)
  record['authored_sources_applied']=True
  record['changed_authored_files']=[str((ASSETS/n).relative_to(ROOT)) for n in [*targets,'photo_prompt_visual_obligations_water_relations.json','photo_prompt_source_manifest.json']]
  record['after_sha256']={p:digest(ROOT/p) for p in record['changed_authored_files']}
  dump(OUT/'integration-map.json',record)
 print(json.dumps({k:v for k,v in record.items() if k not in {'decisions','after_sha256'}},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
