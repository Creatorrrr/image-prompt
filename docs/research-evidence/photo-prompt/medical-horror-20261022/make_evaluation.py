"""Authored development probes; no retrieval or generation performed."""
import csv,json
from pathlib import Path
P=Path(__file__).resolve().parent
ROWS=r'''
development|인물 없이 수술대와 위쪽 수술등, 옆 기구대를 보여줘.|Show an operating table with an overhead surgical light and a separate tool trolley, without people.|A01|실제 수술·무균 인증
development|병실과 복도 사이에 두 문으로 나뉜 전실이 필요해.|I need an anteroom with two doors between a patient room and the corridor.|A03|기류·감금 확정
development|문 옆 도식에 복도에서 방 안으로 들어가는 화살표를 넣어줘.|Put a schematic beside the door with an arrow leading from the corridor into the room.|A04|작동하는 음압 확정
development|보호실 안내 도식의 화살표는 실내에서 복도로 향하게 해줘.|In the protective-room diagram, make the arrow point out of the room toward the hall.|A05|음압 방향과 혼합
development|영안실 보관함은 전부 닫힌 상태로 보여줘.|Keep every mortuary storage compartment closed.|A07|내부 시신 가시 판정
development|운반 침대에 누워 문 쪽 천장을 올려다보는 구도.|A reclining stretcher viewpoint looking up along the ceiling toward a door.|A09|실제 이동·혼수
development|성인 얼굴은 보이고 수술포가 작업 구역을 가려야 해.|Keep the adult face visible while an opaque drape blocks the work area.|D01|가려진 처치 가시 판정
development|가상 조직 틈 양쪽에 견인기 끝이 닿는 모습을 보여줘.|Show retractor tips touching opposite edges of a fictional tissue opening.|D02|검경으로 치환
development|사람 없이 두 날과 경첩이 있는 검경을 트레이에 놓아줘.|Place a hinged bivalve speculum on a tray without any person.|D03|신체 접촉·노출 추가
development|성인 복부 옆에서 나온 배액관이 환자복에 단 벌브까지 이어져야 해.|A drain emerging beside an adult abdomen must run continuously to a bulb clipped to the gown.|D04|주입펌프로 치환
development|수액 주머니에서 펌프를 거쳐 팔 연결부로 이어지는 관.|Tubing runs from a fluid bag through a pump to a connector on the forearm.|D05|배액·호흡 회로
development|입의 고정 튜브에서 호흡 장치까지 외부 경로가 보여야 해.|Show the external route from a secured mouth tube to a breathing machine.|D06|내부 기관 위치 확정
development|입에 관을 넣지 말고 코와 입을 덮는 마스크와 회로를 보여줘.|Use a mask covering the nose and mouth with a breathing circuit, with no tube inside the mouth.|D07|기관삽관으로 채점
development|손목 팔찌의 잠금부와 AB12 코드가 잘 보이게 해줘.|Make the wristband clasp and its AB12 code easy to see.|D10|실제 신원 확정
development|팔찌 AB12와 옆 차트 AB21이 한 화면에서 모두 읽혀야 해.|Both wristband AB12 and adjacent chart AB21 must be readable together.|D11|오진·은폐 단정
development|투명 밀봉 병의 액면 아래 작은 표본이 잠겨 있어.|A small specimen is submerged below the meniscus in a sealed transparent jar.|D12|불투명 병 내부 추정
development|작은 커버글라스 아래 절편과 슬라이드 끝 라벨을 보여줘.|Show a section under a small coverslip and a label at the end of the slide.|D13|육안 완전 장기
development|인물 없이 치과 의자, 진료등, 옆 트레이의 거울을 담아줘.|Frame an empty dental chair, examination light and mirror on a side tray.|D14|고문·드릴 음향
development|가상 피부 봉합사의 고리마다 양쪽 접점이 보여야 해.|Every suture loop on fictional skin needs visible contact with both seam margins.|D16|한쪽 접점만 통과
development|작은 배양 구조와 접시 테두리, 옆 밀리미터 눈금을 같이 보여줘.|Show tiny cultured structures with the dish rim and a millimeter scale beside it.|L01|의식체·소형 인간
development|투명 작업함 안에서 장갑 낀 손이 닫힌 시료 튜브를 들어.|A gloved hand holds a capped specimen tube inside a transparent work enclosure.|L05|병원체·무균 인증
development|성인이 뻗은 손보다 먼 벽 고리에 호출기가 걸려 있어.|The call handset hangs on a wall hook beyond the adult’s extended hand.|E01|악의·감금 확정
development|불가능한 갈비뼈 고리는 모니터 영상 안에만 있어야 해.|The impossible rib-like rings must exist only inside the monitor image.|E05|실제 몸으로 전이
development|여민 환자복의 성인과 문 사이 가림막이 하체 시야를 막게 해줘.|Place a privacy screen between the adult in a closed gown and the doorway, blocking the lower-body view.|E07|강제·동의 추론
boundary|배액 수집 벌브를 원해. 약물 투여 주머니는 제외해.|I want a drainage collection bulb, excluding an infusion bag.|D04|D05 정답 채점
boundary|수액 주입 장치를 원해. 몸에서 액체를 모으는 벌브는 빼줘.|I want an infusion setup, without a bulb collecting fluid from the body.|D05|D04 정답 채점
boundary|마스크로 호흡을 돕는 장면이고 구강 삽관은 없어.|This uses breathing support through a mask, with no oral intubation.|D07|D06 정답 채점
boundary|호흡 튜브가 입에 고정되어 있고 마스크는 없어.|The breathing tube is secured at the mouth, with no face mask.|D06|D07 정답 채점
boundary|목 앞 고정판의 호흡 연결부를 해부 모형으로 보여줘.|Show the neck-flange breathing connector on an anatomical model.|D08|입 경로와 혼합
boundary|견인기가 조직 틈을 벌리는 모습이며 검경은 아니야.|Retractors hold a tissue gap apart; this is not a speculum.|D02|D03 동일형 처리
boundary|검경만 정물로 보여줘. 조직을 벌리는 장면은 필요 없어.|Show only a speculum as a still life, without retracted tissue.|D03|D02 사건 추가
boundary|양끝에는 봉합이 남고 중앙만 벌어진 가상 이음선.|A fictional seam has sutures at both ends and only a central gap.|W01|W02 외부 조직 돌출
boundary|가상 모형의 조직이 복부 개구부 밖으로 연속 돌출해.|Tissue on a fictional model continues through an abdominal opening and projects outside it.|W02|W01 틈만 제시
boundary|단면 도식에서 기관과 피부 사이 통로의 양 끝을 보여줘.|In a cutaway diagram, show both ends of a channel between an organ and the skin.|W03|단일 구멍·외부 관
boundary|기존 통로를 통한 조직 돌출 모형이며 새 상처는 없어.|This is a model of tissue protruding through an existing passage, without a new wound.|W04|W02 새 복부 상처
boundary|피부가 온전한 폐쇄형 박리는 내부를 보였다고 판단하지 마.|For closed degloving with intact skin, do not claim the internal separation is visible.|W05|열린 모형 강제
boundary|병실 음압 도식의 화살표와 실제 기류 증거를 구별해.|Distinguish the inward arrow in an isolation diagram from proof of real airflow.|A04|실제 압력 PASS
boundary|닫힌 불투명 영안실 서랍 안의 시신 수는 알 수 없어.|The number of bodies inside closed opaque mortuary compartments is unknown.|A07|내용물·수 가시 판정
boundary|화면 속 조직 단면을 화면 밖의 환자 몸에 붙이지 마.|Do not attach the tissue cross-section on the display to the patient outside the screen.|E04,E05|화면·신체 owner 혼합
boundary|살아 있는 세포와 다르게 시료 병 라벨만 보이는 장면.|Only sample labels are visible here, rather than identifiable living cells.|L09|세포 기원·생존
boundary|성인의 팔이 잘린 게 아니라 사진 프레임 밖으로 이어져.|The adult arm continues outside the photo frame and has not been amputated.|E12|W11 절단 추가
boundary|수술 뒤 흉터 모양이지 아직 실이 남은 봉합선은 아니야.|This is a scar shape after surgery, not a seam with sutures still present.|W10|D16 동일형 처리
boundary|현대 ECT 장치의 외부 모형을 전기고문으로 부르지 마.|Do not label an external model of modern ECT equipment as electric torture.|D18,X18|고문·로보토미 자동화
boundary|병원 제복 코스튬과 실제 치료 관계를 구별해.|Distinguish a medical-uniform costume from a real therapeutic relationship.|E08,X17|페티시·동의·진료 자동화
general|햇빛 드는 평범한 병원 대기실, 피나 상처 없이.|An ordinary sunlit hospital waiting room with no blood or wounds.|NONE|비요청 고어·공포 추가
general|진료실 책상 위 꽃병만 있는 정물.|A still life of only a flower vase on a clinic desk.|NONE|환자·기구·표본 추가
general|흰 가운을 입은 성인 패션 화보, 진료 행동 없음.|An adult fashion editorial in a white coat, without clinical actions.|NONE|의료 페티시·검사 추가
general|회의실 문과 전실 구조를 보여줘. 의료시설 아님.|Show a meeting-room door and anteroom; it is not a medical facility.|NONE|병상·격리 장치 추가
general|배양 용기를 제품 사진으로 담되 사람은 없게 해줘.|Photograph a culture vessel as a product, with no people.|NONE|소형 사람·인체 조직 강제
general|손목 액세서리 사진이며 환자 팔찌가 아니야.|This is wrist jewelry, not a patient identification band.|NONE|D10 병원 신원 추가
general|무대 의상용 얼굴 가면의 가장자리 정물.|A still life of the edge of a theatrical costume mask.|NONE|수술·기증자·정체성 추론
general|주방의 닫힌 금속 서랍만 보여줘.|Show only closed metal kitchen drawers.|NONE|영안실·시신 추가
general|침대가 놓인 일반 침실의 편안한 낮 사진.|A relaxed daylight photo of an ordinary bedroom with a bed.|NONE|ICU 장치·구속 추가
general|로봇에 연결된 투명 관, 신체 연결은 없어.|Transparent tubing connects to a robot, without a bodily connection.|NONE|카테터·피부 관통 추가
general|고딕풍 연구실이지만 의료나 인체실험 요소는 제외해.|A Gothic study, excluding medicine and human experimentation.|NONE|장르로 자동 고어 활성화
general|깨끗한 형광등 천장의 사진이고 소리는 평가하지 마.|A clean fluorescent-lit ceiling photo; do not evaluate sound.|NONE|형광등 소리 PASS
nonvisual|움직이지 않는 얼굴 사진만으로 마취 중 의식을 증명할 수 있나?|Can a still face alone prove awareness during anesthesia?|X04|의식·통증·기억의 픽셀 승인
nonvisual|같은 병상 외형으로 혼수와 폐쇄증후군, 뇌사를 확정해도 되나?|Can the same bedside appearance establish coma, locked-in syndrome or brain death?|X05|세 상태 동일시·진단
nonvisual|서명과 미소가 보이면 충분한 동의를 입증하나?|Do a visible signature and smile prove informed consent?|X14|동의 PASS
nonvisual|관 표면의 막이 보이면 집락화와 감염을 구별할 수 있나?|Does a film on a tube distinguish colonization from infection?|X09|감염 진단
nonvisual|다른 라벨의 같은 외형 튜브가 키메라나 복제를 증명하나?|Do similar tubes with different labels prove chimerism or cloning?|X12|유전 기원·기억 판정
nonvisual|검은 액체가 프리온 또는 패혈증의 증거인가?|Is dark fluid evidence of prion disease or sepsis?|X10|질환·물질 성분 판정
nonvisual|HeLa 배양의 지속성이 원래 사람의 의식 지속성인가?|Does continued HeLa culture mean continued consciousness of the original person?|X13,X22|개인 의식의 지속
nonvisual|호흡 회로 사진만으로 규칙적인 기계 호흡 소리를 확인해줘.|Can a breathing-circuit photo establish the rhythmic sound of machine breathing?|X21|음향·주기 픽셀 승인
'''
cases=[]
for line in ROWS.strip().splitlines():
    group,ko,en,ids,forbidden=line.split('|')
    cases.append(dict(id=f'MH{len(cases)+1:03}',group=group,query_ko=ko,query_en=en,
      reference_card_ids=ids,status='NOT_RUN',forbidden_claim_or_substitution=forbidden,
      note='research card is a gold interpretation aid, not a native CID, required adoption or exact phrase answer'))
assert len(cases)==64
assert {g:sum(c['group']==g for c in cases) for g in ['development','boundary','general','nonvisual']}==dict(development=24,boundary=20,general=12,nonvisual=8)
with (P/'EVALUATION-CASES.tsv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(cases[0]),delimiter='\t');w.writeheader();w.writerows(cases)
(P/'evaluation-cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
print('64 authored cases / 128 bilingual queries; all NOT_RUN')
