"""Record actual source-image observations separately from proposed render gates."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
reference = json.loads((ROOT / 'SOURCE-RECEIPTS.json').read_text())
supplemental = json.loads((ROOT / 'SUPPLEMENTAL-SOURCES.json').read_text())

# Each row was visually inspected at the supplied original resolution.
observations = {
 'S001': ('1200×900 기본 3면도', '높은 좌우 묶임점, 각진 검정/분홍 머리 장치, 몸판과 떨어진 소매, 소매와 치마의 평면 패널 도형이 보인다.', '밝은 테두리는 자체 발광·작동 상태를 입증하지 않는다. 왼팔 숫자 표식은 피부 표면의 도상이며 상처가 아니다.'),
 'S003': ('1200×900 기본 3면도', '짧은 머리, 세일러 목선, 귀 옆에서 입 근처로 이어진 마이크, 팔의 분리 소매가 보인다.', '원문은 짧은 뒤묶음이라고 했지만 이 자료에서 독립된 후면 묶임점은 확정하지 못했다. 제안 K04의 완전 증거로 사용하지 않는다.'),
 'S004': ('1200×900 기본 3면도', '분홍 장발, 검정/금색 몸판과 긴 옆트임 치마, 노랑/금색 부츠, 회색 어깨 패널과 위팔 부속이 보인다.', '원문의 검정 부츠 설명과 다르다. 어깨의 패널을 지우고 완전한 민소매로 단순화하지 않는다. 다른 Luka 판본의 규칙은 아니다.'),
 'S005': ('1200×900 기본 3면도', '갈색 짧은 머리, 목 뒤로 이어진 붉은 짧은 상의, 앞 지퍼가 있는 붉은 치마, 갈색/황갈색 부츠가 보인다.', '원문의 붉은 high collar·dark-red boots 요약을 수정한다. 가슴 중앙의 세로 경계만으로 그 부분도 실제 지퍼라고 확정하지 않는다.'),
 'S007': ('700×501 V2 상품 배너', '녹색 머리끝이 바깥으로 반복 굽고, 머리 위 고글과 주황/노랑 의상, 주름 장식이 보인다.', '가쿠포 등 다른 배너처럼 크롭 여부를 개별 확인한다. 하단 밖의 발/밑창 정보는 이 배너에서 판정할 수 없다.'),
 'S018': ('720×720 V2 패키지', '팔 앞쪽에 손보다 큰 두 원형 장치가 있고 외곽 원과 안쪽 동심원 면이 보인다. 붉은 동물형 헬멧과 장치가 의상에 이어진다.', '패키지 이미지에서 뒤쪽 접속 세부와 실제 음향 출력은 확인되지 않는다. 사람이 로봇이라는 결론도 만들지 않는다.'),
 'S019': ('657×241 V3 상반신 배너', '짧은 뒤쪽 머리와 두 긴 앞쪽 다발, 각진/원형 머리 부속이 보인다.', '전신·후드 뒤 부속은 배너만으로 확정하지 않는다. 2011 원 제작자 자료 X001–X003으로 후면 및 소유 관계를 보완했다.'),
 'S022': ('720×363 히메·미코토 합성 설정 이미지', '두 캐릭터 각각에 뿔형 외곽과 매우 넓은 소매가 보인다.', '여러 작은 그림과 텍스트가 합쳐진 낮은 높이 자료다. 한 캐릭터의 부속을 다른 캐릭터로 옮기거나 작은 체결점을 확정하지 않는다.'),
 'S024': ('600×600 IA 패키지', '긴 머리, 독립적으로 읽히는 상의와 주름 치마, 길게 보이는 다리가 묘사된다.', '자세·굽·가림과 그림 표현을 인체의 실제 길이 비율로 전이하지 않는다. 정밀 anatomical endpoints는 불충분하다.'),
 'S025': ('600×600 MAYU 패키지', '앞뒤 의상 그림, 장발 색 변화, 어두운 몸판과 치마, 밑단의 긴 밝은/짧은 어두운 건반형 평면 무늬, 손에 든 천 인형이 보인다.', '치마의 건반 무늬는 실제 악기가 아니다. 인형의 부속과 인물의 피부·의복은 서로 다른 owner다. 작은 레이스/봉제 섬유는 이 해상도로 확정하지 않는다.'),
 'S029': ('600×600 Merli 패키지', '머리 부근 다면체 별 모양 장식과 긴 모발의 파란색 구획, 손에 든 긴 장식 막대가 보인다.', '겉/안쪽 머리층을 단일 그림만으로 완전히 판정하기 어렵다. 보석처럼 그린 별의 실제 재질·투명도·발광은 추가 근거가 필요하다.'),
 'S030': ('600×600 Fukase 패키지', '붉은 머리와 얼굴의 붉은 도형, 다른 색의 의복 패널/띠와 패키지 배경 선 그림이 보인다.', '붉은 도형은 혈액이나 상처를 입증하지 않는다. 인쇄/그림 선과 실제 노출 실 봉제선을 구분해야 한다.'),
 'S032': ('600×600 LUMi 패키지', '뒤쪽 원형 canopy와 가장자리 장식, 긴 머리, 아래로 이어지는 소매 띠와 흰 의상이 보인다.', 'canopy, 소매 띠, 실제 신체 촉수를 하나의 owner/부품으로 합치지 않는다. canopy와 띠 전체가 연결되어 있다는 증거는 부족하다.'),
 'S034': ('702×606 Sapphire 일러스트', '몸 바깥 허리 높이의 건반형 고리, 주변의 반투명 색 띠와 선 도형, 드레스 아래 맨발이 보인다.', 'MAYU의 의복 프린트와 다른 공간 배치다. 빛/투명 그래픽이 실제 키보드 하드웨어·홀로그램 장치·물리적 무지지를 입증하지 않는다.'),
 'S035': ('2481×3520 NurseRobot 일러스트', '옅은 큰 셔츠, 어깨/가슴 스트랩, 등에 멘 상자 장치, 주황 십자 모자, 불투명한 광택 주황 다리 착용물, 별도 둥근 로봇과 장면 속 코드가 보인다.', '주황 광택은 자체 발광과 다르다. 이름/제품 서사의 android 설명으로 노출된 관절을 추가하지 않는다. 둥근 로봇은 별도 owner이며 코드가 있으므로 모든 주변 물체를 무연결 부유 장식으로 분류하지 않는다.'),
 'S042': ('600×600 UNI 일러스트', '분홍 사이드 포니테일, 귀 옆 장치, 뺨의 별, 치마 표면의 높이가 다른 색 블록 열이 보인다.', '블록 열은 평면 무늬다. 몸판의 컬러 패널만으로 모든 선을 실제 princess seam으로 확정하지 않는다. 입 근처 막대는 귀 장치 접속을 별도 확인한다.'),
 'S043': ('375×624 AVANNA 패키지', '얼굴, 녹색 몸판, 황색 망토와 장식 구획이 보인다. 얼굴에 작은 점처럼 읽히는 표면 표시가 있다.', '작은 얼굴 영역으로 주근깨의 개수·간격을 정밀 판정할 수 없다. 파란 원형 장식만으로 실제 결정·광택 재질을 확정하지 않는다.'),
 'S048': ('232×397 BRUNO 공식 축약 그림', '큰 머리 비율의 축약 인물, 모자, 청록색 겉옷과 갈색 하의가 보인다.', '축약 그림의 head/body ratio는 실제 사람의 형태가 아니다. 미세 얼굴 점은 명확하지 않아 주근깨의 완전 증거로 쓰지 않는다.'),
 'S051': ('236×424 Append 게임 모듈', '3D 게임 표현의 긴 양갈래, 흰 몸판, 팔 덮임, 허리 주변 장치와 드러난 발 일부가 보인다.', '원래 제품 설정과 게임 모델은 다른 representation이다. 발 일부가 가려져 전후 모든 표면의 무신발 여부를 완전 판정하지 않는다.'),
 'S072': ('900×500 Snow2023 축약 설정표', '정면/후면/측면 축약 도형, 여러 색의 긴 양갈래, 머리와 의복의 눈꽃 무늬, 우산형 소품이 보인다.', '공식 그림이라도 축약 매체다. 큰 머리 비율을 normal human body로 전이하지 않는다. 작은 부속/봉제는 확대 설정 자료가 필요하다.'),
 'S075': ('1000×556 Snow2026 축약 설정표', '초콜릿색 비스듬한 모자와 디저트형 도상, 밝은 옷의 패널, 스커트의 지정 비대칭, 양갈래 색 띠가 보인다.', '2026 costume의 정보이며 다른 Snow 연도와 혼합하지 않는다. 음식 도상은 실제 음식 재질과 다르고 축약 비율도 인체 기본값이 아니다.'),
 'S079': ('850×700 Racing2015 피규어 사진', '왕관형 머리 부속, 의상 위 판형 장식, 방패처럼 읽히는 손 소품, 반대 손의 긴 접힌 우산형 소품이 보인다.', 'Good Smile 공식 제품 설명에서 parasol을 확인했다. 창 같은 좁고 뾰족한 실루엣이 실제 창이라는 정체성의 증거가 되지는 않는다. 축약 figure 비율과 실제 받침도 별도 매체 정보다.'),
 'S080': ('750×650 Racing2017 피규어 사진', '투명 얇은 날개 판에 선무늬, 녹색에서 밝아지는 긴 양갈래, 흰 착용물과 실제 원형 피규어 받침이 보인다.', '날개는 외부 장식 판으로 읽힌다. 실제 생물 날개, 회로 작동, 자유 비행을 입증하지 않는다. 피규어 pose/support를 사람 포즈에 그대로 강제하지 않는다.'),
 'S084': ('236×424 Heart Hunter 게임 모듈', '복부 쪽 bounded opening, 긴 팔/다리 착용물, 등 뒤 막형 날개가 보인다.', '작은 공식 게임 썸네일로 날개 부착 기구·섬유·미세 재질은 확정하지 않는다. 인체의 해부학적 날개로 바꾸지 않는다.'),
 'S086': ('236×424 Dark Angel 게임 모듈', '좌우 녹색 나선 모발, 어두운 의상, 머리 위 검정 돌출물이 보인다.', '堕悪天使라는 이름만으로 날개를 추가하지 않는다. 그림에서 날개는 확인되지 않는다.'),
 'S095': ('236×424 Sexy Pudding 게임 모듈', '분홍 몸판, 앞 교차끈, 초록 허리 리본, 긴 장갑과 어두운 다리 착용물이 보인다.', '모듈명은 평가어/고유명사이며 형태나 성적 상태의 활성화 근거가 아니다. 작은 얇은 끈의 부재를 확정하기에는 해상도가 부족하다.'),
 'S096': ('236×424 Rasetsu Mukuro 게임 모듈', '머리 한쪽에 비껴 단 흰/붉은 가면, 검정/붉은 머리, 어두운 의복과 허리 띠가 보인다.', '얼굴 전체를 덮은 가면이 아니다. 붉은 눈/희게 그린 얼굴이 질병·위협 의도·혈액을 뜻하지 않는다.'),
 'X001': ('650×1000 2011 제작자 모발 설정', '정면·측면·후면에서 짧은 후두부와 얼굴 옆의 두 긴 묶인 다발이 모두 보인다.', '긴 뒤머리를 유지하는 hime cut과 반대의 지역 길이 배치다. 현재 신판이 아닌 2011 자료라는 범위를 유지한다.'),
 'X002': ('650×1000 2011 제작자 후면 설정', '짧은 뒤머리, 긴 앞쪽 다발의 링, 후드에서 길게 늘어진 귀형 천 부속, 원형 하드웨어와 분홍 띠가 보인다.', '후드의 귀형 부속은 인체의 귀가 아니다. 장치 그림의 강한 하이라이트와 도형이 전자 동작을 증명하지 않는다.'),
 'X003': ('650×1000 2011 제작자 의복 설정', '앞쪽 모발·짧은 후면 길이·별도 겉옷과 inner garment·허리 장치가 보인다.', '겉옷을 벗은 모습과 착용 모습은 같은 장면의 동시 의무가 아니라 판본 내 상태 대안이다.'),
 'X004': ('200×200 SONiKA 공식 V2 아카이브', '녹색 머리와 황색 상의의 상품 패키지가 보인다.', '원문이 특정한 초기 3D 외형·구슬 목걸이·문자 문양을 이 썸네일로 확정하지 못했다. primary replacement로 전면 채택하지 않는다.'),
 'X005': ('200×200 OLIVER 공식 V3 아카이브', '선원 모자와 옷, 한쪽 눈 부근의 흰 덮임이 보인다.', '전신·팔 붕대·겹친 천 가장자리의 미세 구조는 불충분하다. 붕대 원인의 서사를 추론하지 않는다.'),
 'X006': ('200×200 Tianyi 공식 V3 아카이브', 'V3 패키지의 작은 캐릭터 도형이 보인다.', '머리의 braid 교차와 loop fastening은 세부 판정 불가다. V5 Lite와 하나의 canonical visual로 합치지 않는다.'),
 'X007': ('200×200 Yanhe 공식 V3 아카이브', 'V3 상품 패키지와 작은 인물 도형이 보인다.', '전신 미세 부속 판정 불가다. V3, V5 Lite, 새 엔진용 판본을 분리한다.'),
}
for source in [*reference['receipts'], *supplemental['receipts']]:
    sid = source['source_id']
    if sid in observations:
        source['visual_review_status'] = 'source_original_reviewed'
        source['review_limit'] = observations[sid][2]

def rep(case):
    group = case['group']
    label = case['case_label']
    if group in ('game_module', 'sakura') or '게임 모델' in label:
        return 'official_game_model_thumbnail'
    if '피규어' in label:
        return 'official_figure_product_photo'
    if '축약 그림' in label:
        return 'official_chibi_illustration'
    if group == 'snow_annual':
        return 'annual_costume_reference; chibi_or_illustration_specific_to_year'
    return 'voicebank_package_or_product_art; inspect each source for crop and medium'

for case in reference['cases']:
    case['representation'] = rep(case)
    case['variant_key'] = {'case_label': case['case_label'], 'source_id': case['source_id'],
                           'representation': case['representation']}
    case['case_status'] = 'source_seed_with_bounded_review; not_whole_character_qualified'

(ROOT / 'SOURCE-RECEIPTS.json').write_text(json.dumps(reference, ensure_ascii=False, indent=2) + '\n')
(ROOT / 'SUPPLEMENTAL-SOURCES.json').write_text(json.dumps(supplemental, ensure_ascii=False, indent=2) + '\n')

review = {'schema_version': 'vocaloid-source-review/v1', 'runtime_artifact': False,
          'review_method': 'All 91 reference images were visually triaged on 8 contact sheets; 27 were then individually viewed at original supplied resolution. All 7 supplemental images were individually viewed. This is source-art review, not generated-image qualification.',
          'counts': {'reference_image_triage': 91, 'reference_source_original_review': 27,
                     'supplemental_source_original_review': 7, 'total_source_original_review': 34,
                     'reference_url_primary_access': 94, 'reference_url_secondary_only': 2},
          'native_render_qualification': 'not_run',
          'observations': [{'source_id': sid, 'representation_and_resolution': row[0],
                            'observed': row[1], 'limits_or_correction': row[2]}
                           for sid, row in observations.items()]}
(ROOT / 'SOURCE-REVIEW.json').write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
lines = ['# 일차 자료 검토와 원문 수정 사항', '',
         '원문 96개 URL 중 공식 이미지 91개와 공식 HTML 3개에 접근했다. 초기 TLS 클라이언트 오류 2개는 인증 검증을 유지한 다른 Python 환경에서 재확인했다. 해당 두 상품 페이지에는 정밀 전신 그림이 없어 이미지 증거로 승격하지 않았다. Fandom 2개는 일차 자료로 세지 않았다.', '',
         '추가 공식 이미지 7개를 보완했다. 원문 이미지 91개는 8장 contact sheet로 윤곽을 검토했고 그중 27개, 보완 이미지 7개는 공급된 원본 해상도로 개별 확인했다. **34개 원본 확인은 source art review이며 생성 이미지 합격이 아니다.**', '',
         '|출처|표현·해상도|직접 관찰|한계·수정|', '|---|---|---|---|']
all_sources = {x['source_id']: x for x in [*reference['receipts'], *supplemental['receipts']]}
for sid, row in observations.items():
    lines.append(f"|[{sid}]({all_sources[sid]['requested_url']})|{row[0]}|{row[1]}|{row[2]}|")
lines.extend(['', '## 판본 관리에서 유지할 경계', '',
              '- 상품 판본/연도, 게임 모델, 설정화, 패키지, 축약 그림, 피규어를 한 appearance truth로 합치지 않는다.',
              '- `case_label + source_id + representation`을 연구용 variant key로 쓴다. 원문에 판본이 없으면 `unspecified` 상태를 유지하고 미세 색/부속 확정을 보류한다.',
              '- 두 인물이 있는 합성 이미지나 companion robot은 owner를 나눠 기록한다.',
              '- 미세 봉제·레이스·투명 끈·후면 체결점이 안 보이는 자료는 더 큰 일차 자료가 필요하다.',
              '- 장치의 밝은 그림, 원형/키보드 도형, 붉은 얼굴 도상, 붕대만으로 작동·부상·신체 구조를 추가하지 않는다.',
              '- 음성 상품의 Adult/Power/Sweet 같은 이름은 목소리 판본명이다. 연령·체형·표정·성격의 증거가 아니다.', ''])
(ROOT / 'SOURCE-REVIEW.md').write_text('\n'.join(lines))
print(json.dumps(review['counts']))
