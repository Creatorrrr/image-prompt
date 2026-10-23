"""Authored future evaluation inputs. Creating cases is not running retrieval or pixels."""
import csv
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
# kind | ko | en | expected cards | expected distinction
ROWS=r"""
boundary|스크럽을 입은 두 의료인이 일하는 모습|Two clinicians working in scrubs|B02 X02|스크럽 색·나이로 직급·성별 역할을 부여하지 않음
boundary|백의를 입은 외래 의료인|An outpatient clinician wearing a white coat|B01 X18|백의를 멸균 수술가운으로 대체하지 않음
boundary|수술가운 소매 위로 덮인 장갑 끝|Glove cuffs overlapping surgical gown sleeves|B04 B13|겉가운·스크럽·장갑의 소유와 겹침이 보임
boundary|고무줄 테두리가 있는 둥근 수술모|A round bouffant cap with an elastic rim|B08 B07 B17|부팡 캡·끈 수술모·역사적 캡을 구분
boundary|마스크를 쓰고 진료하는 인물|A clinician wearing a surgical mask|B09 B10|N95 인증·밀착시험 결과를 추정하지 않음
boundary|안면보호판 안쪽에 보이는 마스크|A mask visible behind a face shield|B12|보호판·마스크·얼굴의 별도 층
boundary|1930년대 영국 간호복을 참고한 앞치마|An apron based on a 1930s English nursing collection|B16 B18 X39|다른 연대 케이프를 한 벌의 고증으로 합치지 않음
boundary|동일한 체형에 검사 가운 대신 상하의 환자복|Two-piece hospital pajamas rather than an examination gown on the same body|B19 R12|상의·바지 구조와 등 여밈 검사 가운을 구분
boundary|등받이만 올라간 파울러 침대|A Fowler bed with only the backrest raised|C04 C11|엉덩이 굴곡과 직선 전체 경사를 구분
boundary|머리가 발보다 낮은 직선 수술대|A straight table tilted with the head below the feet|C10 C11|머리·발 높이 방향이 뒤집히지 않음
boundary|쇄석위의 양쪽 다리받침|Both leg supports in lithotomy position|C09 C12|각 종아리·각 받침·수술대 부착을 모두 확인
boundary|가슴과 무릎을 받치는 교육용 슬흉위|An educational knee-chest position supported at chest and knees|C12 C13|잭나이프의 수술대 굴곡과 혼동하지 않음
boundary|옆으로 누운 환자와 무릎 사이 베개|A side-lying patient with a pillow between the knees|C03 C08|측와위·심스 체위의 몸통 회전을 구분
boundary|테이블에 양팔을 지지하고 앞으로 기댄 환자|A patient leaning forward with both forearms supported on a table|C07|손·팔·발의 실제 지지점을 확인
boundary|귀꽂이에서 청진판까지 연결된 청진 장면|Auscultation with continuous tubing from earpieces to chestpiece|D01|목에 걸린 소품만으로 청진 통과 처리하지 않음
boundary|환자의 엄지 쪽 손목에 두 손가락|Two fingers on the thumb side of a patient's wrist|D04 A11|맥박 촉지와 정서적 손잡기를 구분
boundary|두 손으로 하는 타진 자세|Two-hand percussion examination pose|D03|각 손의 소유와 접촉 층을 구분; 타진음은 비가시
boundary|한쪽 콧구멍으로 들어가는 비위관|A nasogastric tube entering one nostril|D10 D08|캐뉼라의 두 짧은 코갈래를 부여하지 않음
boundary|양 코갈래와 귀 뒤 관이 있는 산소 캐뉼라|An oxygen cannula with two nasal prongs and tubing behind the ears|D08 D10|두 코 접점과 외부 경로를 모두 확인
boundary|입의 고정 튜브부터 인공호흡기까지|From a secured oral tube to the ventilator|R09 R11|입·목 접점과 외부 연결 끝점을 구분
boundary|목 앞 고정판과 끈이 있는 기관절개관|A tracheostomy flange and neck strap at the front of the neck|R11|실제 기관 내부 위치는 이미지로 입증하지 않음
boundary|산소마스크에 연결된 가는 공급관|A narrow supply tube connected to an oxygen mask|D09 R10|기계환기의 큰 회로를 자동 혼합하지 않음
boundary|손가락 집게와 상완 혈압띠|A finger clip and an upper-arm blood pressure cuff|D07 D06|두 장비를 위치·구조로 구분하며 수치 정확성을 추정하지 않음
boundary|수액백에서 펌프를 거쳐 팔까지|From an IV bag through a pump to an arm connector|R08 D13|수액백 펌프와 주사기펌프를 구조 없이 합치지 않음
boundary|동맥관이 필요하니 일반 수액관으로 대신하지 마|An arterial line is required; do not substitute a generic IV|H01 X09|정확한 소스 부재를 기록하고 IV로 충족 주장하지 않음
boundary|CRRT의 유출액 주머니가 보이는 장치|A CRRT device with a visible effluent bag|H02 F06|일반 투석 도식으로 CRRT의 전체 장치를 통과 처리하지 않음
boundary|ECMO와 투석기의 차이를 보이는 교육 도식|An educational diagram distinguishing ECMO from dialysis|F07 F06|산소화기·펌프·투석 필터의 기능 블록을 혼용하지 않음
boundary|일직선 모니터와 제세동 장면|A flat monitor line and a defibrillation scene|X11 D12|무수축·PEA를 자동 충격 리듬으로 표현하지 않음
boundary|호흡기가 연결된 환자가 눈을 감고 있다|A patient connected to a ventilator has closed eyes|X15 R09|혼수·뇌사·죽음을 추정하지 않음
boundary|마취 상태는 설명에만 있고 눈은 보이지 않는다|Anesthesia is stated in context but the eyes are not visible|X16 R21|눈·자세로 마취·진통·기억의 증거를 만들지 않음
boundary|장갑 낀 팀이 수술 전 확인표를 보는 순간|A gloved team looking at a preoperative checklist|A13 X18|정지 장면은 타임아웃 내용·완료·멸균의 증거가 아님
boundary|밝은 피부의 건강한 인물|A healthy person with light skin|E12 X38|창백·빈혈·병약미를 자동 추가하지 않음
boundary|푸른 병원 조명 아래 입술|Lips under blue hospital lighting|E13 X13|파란 광원을 청색증의 증거로 취급하지 않음
boundary|황색 필터 없이 공막의 노란 기운|A yellow scleral tint without a yellow image filter|E14|공막과 홍채를 구분; 특정 간질환 추정 없음
boundary|다리가 가는 환자와 탈모|A thin-legged patient with hair loss|X38|악액질·암·항암치료의 확진이나 원인을 추정하지 않음
boundary|팔을 완전히 감싼 캐스트와 부분 부목|An encircling arm cast and a partial splint|E02 E03|단단한 면의 둘레와 스트랩의 역할을 구분
boundary|보조기를 온전한 다리에 착용한 인물|A person wearing a brace around an intact leg|E06 E07|없는 부분을 대체하는 의족을 자동 부여하지 않음
boundary|휠체어를 사용하지만 서 있을 수도 있는 인물|A wheelchair user who may also be able to stand|E08 X38|휠체어를 보행 불가·영구 장애로 단정하지 않음
boundary|환자의 손을 잡은 사람|A person holding a patient's hand|A11 X26|동의·가족·연인·정서를 확정하지 않음
boundary|샤프롱이 동석한 민감 부위 진찰의 문맥|An intimate examination with a chaperone stated in context|X30 X26|제3자의 외형만으로 자격·동의가 입증되지 않음
boundary|필요한 진료 노출을 요청했고 가운은 열려 있어야 함|Required clinical exposure with an open examination gown|X30 R19 R12|닫힌 가운·가림막을 필수 실현으로 채택해 요청을 지우지 않음
boundary|성인 의료 코스튬을 입은 패션 퍼포머|An adult fashion performer wearing a medical-themed costume|B21 X33|실제 의료인·성적 합의·진료 여부를 외형에서 추정하지 않음
boundary|의료진과 환자의 친밀함을 다루는 스릴러|A thriller about intimacy between clinician and patient|X34 X27|로맨스·착취·동의를 하나의 긍정 후보로 합치지 않음
boundary|현대 ECT를 설명하는 자료|Material explaining modern ECT|X24 H04|흉부 제세동·고문·무마취 처벌 장면으로 대체하지 않음
boundary|성폭력 진료실의 증거 키트|An evidence kit in a sexual-assault examination context|G04 X36|키트·상처만으로 사건·가해자·인계 연속성을 입증하지 않음
boundary|DNR이 있으나 계속되는 돌봄|Continued care in a DNACPR context|X37 A11|모든 치료 중단·임박한 사망으로 바꾸지 않음
boundary|복도를 따라가는 긴 촬영과 심박 경보음|A long corridor tracking shot with a heartbeat alarm|X40 A14|정지 이미지에서 촬영 지속시간·소리를 통과 판정하지 않음
boundary|바이오펑크 소스의 봉합선 전체를 사용|Use the complete canonical biopunk suture source|R15|의료 레지스트리의 짧은 요약으로 정본 문장·조건을 대체하지 않음
ordinary|야간 카페의 손님|A guest in a cafe at night||의료복·환자·검사관을 자동 추가하지 않음
ordinary|박물관의 유리 진열장|A museum glass display case||격리실·환자를 자동 추가하지 않음
ordinary|공연용 간호사 코스튬 상품 사진|A product photo of a nurse costume for performance|B21 X33|사람·환자·진료 접촉을 상품 요청에 자동 추가하지 않음
ordinary|수의사가 동물을 살피는 장면|A veterinarian examining an animal||인간 환자 전제의 전신 후보를 무조건 전이하지 않음
ordinary|천문대 모니터의 그래프|A graph on an observatory monitor||ECG·심정지로 자동 해석하지 않음
ordinary|건물 안전도 트리아지|Building safety triage||임상 KTAS와 다른 문맥을 보존
ordinary|정비사가 부품을 인계하는 모습|A mechanic handing over a component||환자 인계·SBAR로 재해석하지 않음
ordinary|장작과 불쏘시개 조각|Firewood and kindling splints||splint의 의료 부목 의미를 부여하지 않음
ordinary|손이 화면 밖인 의사 초상|A doctor's portrait with hands outside the frame|X02|선택하지 않은 접촉 후보의 의무를 자동 부여하지 않음
ordinary|신생아만 있는 NICU 실내|A NICU interior with only a newborn|A03 X04|성인 역할극·코스튬·의료 페티시 후보가 섞이지 않음
ordinary|의료인이 없는 빈 복도|An empty corridor without clinicians||no-people 제약을 병원 장르로 무시하지 않음
ordinary|병원과 무관한 검정 가죽 케이프|A black leather cape unrelated to hospitals||역사 간호 케이프를 장식 유사성만으로 강제하지 않음
"""

PIXELS=r"""
P01|B04 D18|가운 보조와 양쪽 손목 겹침|조력자의 두 팔·뒤 끈·착용자 두 팔·소매와 장갑 끝이 한 장면에서 구별됨
P02|B08 B17|수술모 대비|둥근 고무줄 캡과 각진 역사 캡은 서로 다른 독립 요청에서 비교; 한 캡의 혼성 형태 금지
P03|C04 C11|등받이와 전체 경사|독립된 두 체위 요청; 골반 굴곡과 직선 상판, 머리·발 상대 높이를 판독
P04|C09|쇄석위 양쪽 다리 지지|좌우 종아리·별도 패딩·두 수술대 부착점을 동시에 확인
P05|C13|잭나이프 모형|모형 문맥, 골반 아래 굴곡점, 양쪽 낮은 상판, 가슴·다리 지지
P06|D01|청진기 전체 경로|한 의료진의 귀꽂이·연속 관·손·청진판·환자 가슴까지 확인
P07|D04 A11|맥박 촉지와 손잡기|각각의 독립 요청에서 접촉 위치와 손의 소유를 판독; 맥박 자체는 비가시
P08|D08 D10|캐뉼라와 비위관|각각의 독립 요청; 두 코갈래와 한 콧구멍 진입, 외부 경로를 구분
P09|R09 R11|입·목의 호흡관|각 독립 요청에서 고정점·외부 연결부·주름관·장치의 끝점 확인
P10|R08 D13|수액펌프와 주사기펌프|각 독립 요청에서 저장부 종류·기계 접점·관의 경로를 확인
P11|E02 E03|캐스트와 부목|각 독립 요청에서 둘러싸는 단단한 면과 부분 지지면·스트랩을 구분
P12|E06 E07|보조기와 의지|각 독립 요청에서 온전한 다리와 잔존지·소켓·대체부를 구분
P13|E11 E09|보행 보조|환자 양손·보행기·바닥 접점·치료사 손·허리벨트와 팔꿈치 위치 확인
P14|F01|초음파의 외부 연결|손·탐촉자·복부·젤·전선·카트·별도 화면 경계를 확인
P15|F07 F06|ECMO와 투석 도식|각 독립 도식 요청에서 펌프·산소화기와 투석 필터의 완전한 블록/경로를 판독
P16|A11 F12|따뜻한 침상 돌봄|양 인물 손목·손의 소유·접촉과 얼굴의 가독성; 감정 효과는 별도 평가
"""

def main():
    cases=[]
    for line in ROWS.strip().splitlines():
        kind,ko,en,refs,expected=line.split('|')
        cases.append(dict(id=f'E{len(cases)+1:03d}',kind=kind,query_ko=ko,query_en=en,
            card_ids=refs.split(),expected=expected,result='NOT_RUN',independent_holdout=False,
            input_origin='authored_for_this_research',interpretation='expected disposition, not a requirement that every listed card rank or be adopted'))
    (ROOT/'evaluation-cases.json').write_text(json.dumps({'schema':'medical-drama-development-evaluation/v1','cases':cases},ensure_ascii=False,indent=2)+'\n')
    with (ROOT/'EVALUATION-CASES.tsv').open('w',newline='') as f:
        w=csv.writer(f,delimiter='\t');w.writerow(['id','kind','query_ko','query_en','card_ids','expected','result'])
        for c in cases:w.writerow([c['id'],c['kind'],c['query_ko'],c['query_en'],','.join(c['card_ids']),c['expected'],c['result']])
    pixel=[]
    for line in PIXELS.strip().splitlines():
        pid,refs,title,gates=line.split('|');pixel.append(dict(id=pid,card_ids=refs.split(),title=title,
            required_visible=gates,status='NOT_RUN',scope='split distinct meanings into independent matched requests; never require alternative cards together'))
    (ROOT/'pixel-cases.json').write_text(json.dumps({'schema':'medical-drama-pixel-plan/v1','cases':pixel,
        'conditions':['baseline_existing_only','new_data_available_authorial_selection','authored_relation_target'],
        'replicates_per_condition_proposed':2,'minimum_images_if_one_request_per_family':96,
        'warning':'Several families contain two independent meanings. Splitting them increases the image count; 96 is a lower-bound planning estimate, not a budget or completed run.',
        'executed_images':0},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'cases':len(cases),'kind_counts':{k:sum(x['kind']==k for x in cases) for k in ['boundary','ordinary']},
        'bilingual_queries':len(cases)*2,'pixel_families':len(pixel),'all_status':'NOT_RUN'},ensure_ascii=False))

if __name__=='__main__':main()
