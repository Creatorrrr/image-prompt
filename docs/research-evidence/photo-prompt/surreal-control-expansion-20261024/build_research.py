#!/usr/bin/env python3
"""Build reviewed research artifacts only; never writes operating skill assets."""
import collections
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT/'skills/photo-prompt-image-generator/assets'


def read(p): return json.loads(p.read_text())
def dump(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def digest(v): return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def main():
    pro=read(HERE/'input/pro-candidate-draft.json')
    corpus={}
    for m in read(ASSETS/'photo_candidate_corpus_manifest.json')['modules']:
        if m['kind']=='candidates':corpus.update(read(ASSETS/m['file'])['candidates'])
    # Source facts are scoped to the actual current read, not inherited approval.
    notes={
      'S01':('body_read','일상 사물의 발견·조작·제작과 형식/상징 유추. 원전의 정확한 장면을 새 후보로 귀속하지 않는다.'),
      'S02':('catalogue_body_and_primary_search_excerpt','1937년 서지와 반사 불일치 확인. 정상 책 반사는 공식 검색 본문 발췌와 대조; 현재 페이지의 전체 연구 본문이 항상 노출되지는 않는다.'),
      'S03':('body_read','털로 덮은 컵·받침·숟가락. 돌의 실제 연성이나 새 베개의 촉감을 증명하지 않는다.'),
      'S04':('catalogue_loaded_body_timeout','공식 대형 카탈로그는 열렸으나 설명문 후속 조회는 timeout. 구체적 방법론 근거는 S05로 교체한다.'),
      'S05':('body_read','2016 전시 설명의 균형·일상 사물의 용도 변경·맥락/지각 관계를 확인했다.'),
      'S06':('body_read','특정 장소에서 수초 존재하는 구름과 사진 기록. 실내 구름의 지속성·무장치 제작을 뜻하지 않는다.'),
      'S07':('body_read','1953–54 소장판의 낮 하늘/밤 거리 결합. 단일 관계의 주도 가능성에 대한 선례이며 설정 임계값은 아니다.'),
      'S08':('body_read','2021년 제안문은 화강석 경계석 선의 도로 이탈을 말한다. 흰 도료가 천으로 변한다는 자료가 아니다.'),
      'S09':('catalogue_metadata_only','현재 응답은 1987년 영화·매체 서지 중심. Equilibres의 정지사진/균형 설명은 S20에서 별도로 확인했다.'),
      'S10':('body_read','1952 작품의 생활 사물 상대 비례와 실내/실외 대응. 실제 대형 찻잔 청소의 선례는 아니다.'),
      'S11':('body_read','1953년 7월 석판화와 여러 방향 기준을 확인했다. 실제 중력장 증거로 쓰지 않는다.'),
      'S12':('body_read','먼지에 물체 부재의 흔적을 남기는 방법. 소멸 원인·과거 물체의 정체는 별도다.'),
      'S13':('body_read','2004 설치판의 유리 위 얕은 물/아래 빈 공간. 지각적 낯섦과 실제 물리 구조를 분리한다.'),
      'S14':('institutional_abstract_only','두 과제의 주시 이후 처리 결과만 확인. 전문 PDF 접근은 403이므로 효과 크기·보편 탐지 법칙을 주장하지 않는다.'),
      'S15':('body_read','1990년 방 내부를 뜬 석고 양형과, 사진에서 제작 원리가 명백하지 않다는 공식 시각 설명을 확인했다.'),
      'S16':('body_read','접착식 노면표시와 접착 실패 가능성. 특정 한국 도로 공법의 진술로 확대하지 않는다.'),
    }
    sources=[]
    for src in pro['provenance']['sources']:
        sources.append({'source_id':src['id'],'title':src['title'],'publisher':src['publisher'],'url':src['url'],
                        'current_access_status':notes[src['id']][0],'review_ko':notes[src['id']][1],
                        'review_date_kst':'2026-10-24','support_scope':'principle_or_counterexample_only',
                        'does_not_attest_exact_new_candidate':True})
    extra_sources=[
      ('S17','Erik Johansson — About / Work Process','artist','https://www.erikjo.com/about/','사진의 결합에서 조명·원근의 일관성과 아이디어/장면의 연결을 설명한다. 작가 모방 스타일이나 새 후보의 성공 증거가 아니다.'),
      ('S18','Do Ho Suh: Almost Home','Smithsonian American Art Museum','https://americanart.si.edu/exhibitions/suh','손으로 봉제한 반투명 집·통로와 가정 사물 복제. 구조 재질 전환의 선례이며 사용자의 기억·이주 경험을 외형에서 증명하지 않는다.'),
      ('S19','La condition humaine, 1933','National Gallery of Art','https://www.nga.gov/artworks/70170-la-condition-humaine','창밖 풍경과 캔버스 풍경의 정렬, 이젤·캔버스 경계의 재현 층위. 실제 관통·무한 재귀의 증거가 아니다.'),
      ('S20','Peter Fischli David Weiss — Teacher Resource Unit','Solomon R. Guggenheim Museum','https://www.guggenheim.org/wp-content/uploads/2019/12/guggenheim-teaching-materials-fischli-weiss.pdf','PDF pp.8–9의 Equilibres(1984–86)와 일시적 균형 사진 설명. 영화의 인과 연쇄와 정지사진의 상태를 구분한다.'),
      ('S21','Your uncertain shadow (colour), 2010','Studio Olafur Eliasson','https://olafureliasson.net/artwork/your-uncertain-shadow-colour-2010/','여러 색 광원과 가림으로 여러 색 그림자가 생기는 정상 광학의 사례. 그림자 수·색만으로 자율성이나 소유자 불일치를 단정하지 않는다.'),
      ('S22','La Clef des champs, 1936','Museo Nacional Thyssen-Bornemisza','https://www.museothyssen.org/coleccion/artistas/magritte-rene/llave-campos-clef-des-champs','깨진 유리 조각에 외부 풍경과 대응하는 그림이 남는 재현 관계. 실제 빛이나 풍경의 물질 전이로 단정하지 않는다.'),
      ('S23','Chema Madoz: The nature of things and its echoes in the collection','Museo Patio Herreriano','https://museopatioherreriano.org/exposicion/chema-madoz-la-naturaleza-de-las-cosas-y-su-eco-en-la-coleccion-joan-brossa-angel-ferrant-perejaume','자연물/사물의 형식 유추·기능 전환과 작은 관계 변화. 새 장면의 정확한 형태와 관객 정서는 저술 가설이다.'),
      ('S24','James Turrell on Meeting — artist transcript','MoMA PS1','https://www.momaps1.org/en/post/237-james-turrell-on-meeting','실내/하늘 경계와 빛이 고체처럼 느껴지는 지각. 실제 고체화·비정상 날씨나 모든 관객의 동일 색지각을 증명하지 않는다.'),
      ('S25','La Reproduction interdite — audio transcript','MoMA','https://www.moma.org/audio/playlist/180/2381','1937년 인물의 얼굴을 보여 주지 않는 거울과 책의 정체를 설명한다. 화분·꽃·미래 거울은 새 저술이다.'),
    ]
    for sid,title,publisher,url,note in extra_sources:
        sources.append({'source_id':sid,'title':title,'publisher':publisher,'url':url,
                        'current_access_status':'body_read','review_ko':note,'review_date_kst':'2026-10-24',
                        'support_scope':'principle_or_counterexample_only','does_not_attest_exact_new_candidate':True})
    dump(HERE/'sources.json',{'schema':'surreal-control-research-sources/v1','sources':sources,
      'access_limits':[{'url':'https://www.research.ed.ac.uk/files/12628030/HENDERSON_JM_Does_gravity_matter_Effects_of_semantic_and_syntactic_inconsistencies_on_the_allocation_of_attention_during_scene_perception.pdf','status':'403','used_as_full_text':False},
                       {'url':'https://www.glenstone.org/artworks/equilibres-a-quiet-afternoon?rel=collections','status':'open_failed_search_excerpt_only','used_as_main_balance_evidence':False}],
      'quotation_policy':'No verbatim work descriptions copied into new candidate prose. Facts are short scoped paraphrases.'})
    principles=[
      ('M01','선택적 반사·그림자 불일치',['S02','S21','S25'],['cand_1244bf25f81d5a4781f69b18d6f36501','cand_4867f579f94f5cdb9391bebc93c3e9ad','cand_ff9b3acd769b5305b9c4c8dae92b0dec'],'있음: 행동·몸/그림자 소유자와 수광면. 식물의 상태·사물의 기능 형태 변형은 완성 변형별 대조가 필요.','정상 대응을 남겨 선택적 차이를 읽게 하되 실제 시간차·자율성은 정지사진만으로 증명하지 않는다.'),
      ('M02','재질·형태·사용 기대의 충돌',['S03','S17'],['cand_daf0e469e7115693851218ff4daf8326','cand_b294c59558ce5b2483da3b0d26fc1fea','cand_ac6637db4275532ba045cac779951277'],'있음: 도자 커튼·털 찻잔 등. 경도/연성은 외관과 실제 물성을 분리할 필요.','같은 표면의 연속성·접힌 형상·접촉을 적고 실제 경도나 변형 이력은 주장하지 않는다.'),
      ('M03','기능 부분의 위치와 행위 수신자 전환',['S01','S05'],['cand_9881fcf73bfd50c9a71031e1c5c2a367','cand_cc25b6962c565b6491d063a0ade8e7fb','cand_290e7bca82cd50d8b36f734480a9c348'],'부분 이웃: 정상 찻잔·의자·무릎 위 동물. 내부 손잡이 사용/빈 의자 돌봄의 동일 완성 관계는 선별 원문에서 미확인.','실제 제작 가능한 조형도 포함한다. 단순 수리·운반·제품 설명으로 읽힐 가능성을 따로 평가한다.'),
      ('M04','환경 현상의 장소와 조건 불일치',['S06','S07','S24'],['cand_5883f06fe96c5f358b8b0d7fcbbb9aed','cand_a274d7b4192a513a83c31c6fe8130824','cand_9c069a207d845a049b59dc6823b2353f'],'있음: 구름 위 침대·집 위 구름·구름 벽화. 실내의 독립 구름과 동시 낮/밤의 완성 관계는 선별에서 미확인.','구름 조형물·안개·노출 차이와 구분하고 지속성·실제 동시 시간은 추론 한계로 남긴다.'),
      ('M05','지지·하중 외관과 국소 방향 규칙',['S11','S20'],['cand_c54c7d2b2e2456e7a1ec521383ea2816','cand_7c64f1d3664757439b12fbb35271f97e','cand_7767dc7dc8b7561cb5d955b385decea2'],'있음: 수직 보행면별 인물과 일반 중력 이탈. 약한 지지체의 접촉·다른 지지 가능성 분해가 필요.','한 프레임의 접지/간격/방향만 평가한다. 질량·실제 중력장·숨은 지지의 부재를 확정하지 않는다.'),
      ('M06','국소 규칙 예외와 계절 경계',['S17','S23'],['cand_127c0ace3acd5724abb155e5cef707c3','cand_192c1989f25a5a96b9454926f302d132'],'원리가 이미 있음. 열·소리·바람과 시간변화를 정지사진 증거로 대체하지 않는 완성 사례 정제가 우선.','계절/비의 가시 경계와 같은 대상의 연속성을 명시하고 실제 기후나 보호 효력은 주장하지 않는다.'),
      ('M07','상대 크기와 포함 세계',['S10'],['cand_f78b8c2e0cd35d21a931a23bfdb8e3de','cand_55c2dad821f4596c941a8d4cea2d8476','cand_99877e25fc1f5e318ec6bfae0591bf00'],'구체적인 작은 문/의자와 광물 내 도시가 이미 있음. 거대 배경과 전경 찻잔을 거대 찻잔으로 재사용할 수는 없음.','같은 깊이·접촉·정상 기준의 조합. 촬영 방법과 실치수는 분리한다.'),
      ('M08','재현 평면·물리 공간의 경계',['S19','S22'],['cand_7193917dbadb5f5f97e1284c74e349c9','cand_2688bf2be5365cde9f1728e258ebe8ce','cand_90f4412c7de75c5f8e9a234043b64857'],'책 밖 팔/화면 밖 다리 등 이미 있음. 인간 신체를 추가하지 않는 사물 변형과 정렬만 있는 정상 대조가 유용.','그림·반사·실제 공간의 각 소유자와 경계를 고정한다. 단순 정렬을 실제 관통으로 판정하지 않는다.'),
      ('M09','공간 외피와 건축 재질 전환',['S18'],['cand_dbbaeb68cc555881beb4b119c8b32d11','cand_118163cedc90550899969a70d966babd'],'유기 벽과 장식 천 이웃이 있음. 문틀·벽 자체가 봉제 외피로 읽히는 관계는 이와 다름.','벽에 천이 걸린 것과 건축 부분의 외피가 천인 것을 구분한다. 하중·이주·실제 기억은 추론하지 않는다.'),
      ('M10','빈 공간의 물체화',['S15'],[],'선별 원문에서 대응 완성 사례 미확인. Ghost는 한 장 설명 의존 위험도 함께 알려 준다.','양형과 원래 용기의 맞물리는 표면을 함께 보이되 실제 주조 과정의 증명이라고 하지 않는다.'),
      ('M11','재귀·전역 연결·공유 경계',['S11','S19'],['cand_1a7a2cd1b6875505ba73c523bc9142c2','cand_b72dd798af61585ab251aaf345157566','cand_8a9a3c1297605719b6bfed20536bd230'],'이미 풍부한 구체 사례가 있음. 우선 재사용·관측성 정제.','무한·실제 비유클리드 공간·두 읽기의 동시 지각을 주장하지 않는다. 전체 끝점이 필요할 때 잘라서 통과시키지 않는다.'),
      ('M12','형식·상징 유추와 일상적 관계',['S01','S05','S23'],['cand_e457312a87545b27b2dfe7c20a64c5e1','cand_010c1935b7bc5fe7832855df90d199ff'],'일반 자문과 사물 변형 이웃은 있음. 관계 효과와 작품 장르 소속을 분리하는 자료 보강이 필요.','물리적 불가능성이 필수는 아니다. 기호·사용 맥락의 낯섦은 시각 관계로 설계하고 관객 정서는 가설로 둔다.'),
    ]
    mechanisms=[{'mechanism_id':i,'name_ko':name,'source_ids':ss,'witness_candidate_ids':ids,
                 'coverage_finding_ko':finding,'meaning_boundary_ko':boundary,
                 'scope':'293 related source records plus scoped root-primary and role-lead review; not full semantic corpus certification'}
                for i,name,ss,ids,finding,boundary in principles]
    dump(HERE/'mechanism-coverage.json',{'schema':'surreal-control-mechanism-coverage/v1','mechanisms':mechanisms})

    decisions={
      'C01':('M01','P0',['cand_1244bf25f81d5a4781f69b18d6f36501','cand_4867f579f94f5cdb9391bebc93c3e9ad'],'new_complete_variant','기존 행동/손 위치 차이는 개화 상태 차이가 아니다. 해당 원문을 꽃으로 바꾸지 않고 자연물의 상태·정상 대조를 한 완성 변형으로 제안한다.'),
      'C02':('M02','P0',['cand_daf0e469e7115693851218ff4daf8326','cand_b294c59558ce5b2483da3b0d26fc1fea'],'new_complete_variant','재질 전이 원리는 있으나 도자 커튼을 눌리는 베개로 고쳐 쓰면 의미가 달라진다. 실제 경도가 아닌 외관/형태 충돌을 별도 변형으로 기록한다.'),
      'C03':('M03','P1',['cand_cc25b6962c565b6491d063a0ade8e7fb','cand_290e7bca82cd50d8b36f734480a9c348'],'new_complete_variant','의자 구조와 반려동물 안기기의 존재가 빈 의자 돌봄 관계를 증명하지 않는다. 실제 운반/수리와 구분될지 평가가 필요한 저술안.'),
      'C04':('M03','P0',['cand_9881fcf73bfd50c9a71031e1c5c2a367','cand_299cf0bdaa2f58c7b8a1f9a03a65273b'],'new_complete_variant','정상 찻잔의 연결 구조와 서랍 손잡이 안 지형은 내부 손잡이 찻잔이 아니다. 뒤쪽 외부 손잡이 부재를 한 시점에서 증명하려 하지 않는다.'),
      'C05':('M04','P0',['cand_5883f06fe96c5f358b8b0d7fcbbb9aed','cand_a274d7b4192a513a83c31c6fe8130824','cand_9c069a207d845a049b59dc6823b2353f'],'new_complete_variant','구름 위 침대·집 위 구름·벽화는 실내 천장/탁자 사이의 구름이 아니다. 공간 경계와 덩어리의 분리를 저술한다.'),
      'C06':('M04','P1',['cand_de9922139bfc5373a09607eec027e840','cand_fd3010192e7f53f592c574bd4be8a486'],'new_complete_variant','국소 광학 이음과 정상 노을은 동시 낮/밤 인상과 다르다. 원문 전수 의미 부재라고는 주장하지 않는다.'),
      'C07':('M02','HOLD',['cand_b32a0e01f10b56a78a84ecc0e1fe64bf'],'hold','실제 테이프 박리라는 강한 대체 설명. 신규 시각 원리의 확정 사례 대신 정상 대조/보류 자료로 유지한다.'),
      'C08':('M05','P1',['cand_c54c7d2b2e2456e7a1ec521383ea2816'],'new_complete_variant','일반 중력 이탈은 풀잎·돌의 접촉/지지 원리와 다르다. 질량과 숨은 보강 부재를 증명하지 않는 범위로 제한한다.'),
      'C09':('M07','P0',['cand_f78b8c2e0cd35d21a931a23bfdb8e3de','cand_55c2dad821f4596c941a8d4cea2d8476','cand_99877e25fc1f5e318ec6bfae0591bf00'],'new_complete_variant','Pro의 재사용 권고를 수정한다. 작은 문·광대한 환경으로 변한 사물·정상 찻잔과 거대 배경은 거대 찻잔 청소의 동일 source가 아니다. 같은 깊이와 실제 사용을 묶은 새 완성 변형의 가치가 있다.'),
      'C10':('M05','P2',['cand_7c64f1d3664757439b12fbb35271f97e','cand_7767dc7dc8b7561cb5d955b385decea2'],'new_complete_variant','국소 방향의 서 있는 인물은 이미 있다. 의자·앉은 독서자·소매 처짐을 추가한 것은 다른 완성 계약이므로 기존 source를 대체하지 않는다.'),
    }
    cards=[]
    for c in pro['candidates']:
        mid,priority,neighbors,decision,reason=decisions[c['id']]
        cards.append({'research_id':c['id'],'origin':'pro_draft_reviewed_against_current_source','title_ko':c['name_ko'],
          'mechanism_id':mid,'priority':priority,'decision':decision,'decision_reason_ko':reason,
          'proposal_en':c['scene']['en'],'proposal_ko':c['scene']['ko'],
          'relation_record':c['relations'],'same_frame_evidence':c['same_frame_evidence'],
          'confounds':c['confounds'],'claim_limits':c['static_not_verifiable'],
          'source_ids':(['S05'] if c['id']=='C03' else c['source_ids']),
          'neighbor_candidate_ids':neighbors,'native_approval':False,'pixel_status':'NOT_RUN',
          'intrinsic_surreal_level':None,'tone_status':'authorial_hypothesis',
          'pro_draft_sha256':hashlib.sha256((HERE/'input/pro-candidate-draft.json').read_bytes()).hexdigest(),
          'migration_note':'Research prose only. Normalize exact visible meaning and author conditions/effects before any operational registration.'})
    # Narrow one unobservable global-negative claim without altering its raw source file.
    cup=next(c for c in cards if c['research_id']=='C04')
    cup['proposal_en']='An empty white porcelain teacup is held just above a table by one index finger passing through a complete loop attached at two points to its inner wall. A high oblique view shows both inner attachments, the open loop around the finger, and the separate outer wall of the same cup.'
    cup['proposal_ko']='빈 흰 도자기 찻잔의 안쪽 벽에 두 지점으로 붙은 온전한 고리에 검지 하나가 들어가 잔을 탁자 위로 조금 든다. 높은 사선 구도로 두 내부 접합점, 손가락 주위 고리의 빈 공간, 같은 잔의 별도 외벽이 함께 보인다.'
    cup['same_frame_evidence']=['같은 잔의 보이는 외벽과 내부 고리','내벽에 붙는 두 고리 접합점','고리를 통과한 손가락과 빈 틈','탁자에서 떨어진 잔의 밑면']
    cup['relation_record']['states']=[x for x in cup['relation_record']['states'] if x!='외부에는 다른 손잡이가 없다.']
    cup['authorial_revision_note']='외벽 전체에 손잡이가 없다는 전역 부재 주장을 제거하고 실제 보이는 내부 접합과 사용 관계를 보존했다. 원본 Pro 파일은 그대로 보관한다.'

    def add(rid,title,mid,priority,en,ko,owners,relations,evidence,confounds,limits,sources,neighbors,reason,decision='new_complete_variant',reuse=None):
        row={'research_id':rid,'origin':'new_research_authored','title_ko':title,'mechanism_id':mid,'priority':priority,
             'decision':decision,'decision_reason_ko':reason,'proposal_en':en,'proposal_ko':ko,
             'relation_record':{'owners':owners,'relations':relations},'same_frame_evidence':evidence,
             'confounds':confounds,'claim_limits':limits,'source_ids':sources,'neighbor_candidate_ids':neighbors,
             'native_approval':False,'pixel_status':'NOT_RUN','intrinsic_surreal_level':None,'tone_status':'authorial_hypothesis',
             'migration_note':'A complete optional visual realization; no control value or genre automatically activates it.'}
        if reuse:
            original=corpus[reuse]
            row.update(origin='existing_source_reused_without_mutation',reuse_candidate_id=reuse,existing_source_sha256=digest(original),
                       proposal_en=original['content']['en'],proposal_ko=original['content']['ko'],
                       relation_record={'source':'complete_existing_source','candidate_id':reuse,
                                        'conditions':original['conditions'],'effects':original['effects'],
                                        'research_semantics':original['content'].get('research_semantics')})
        cards.append(row)

    add('R11','닫힌 우산과 펼쳐진 그림자','M01','P0',
      'A closed umbrella stands with its tip touching a pale tiled floor beside one exposed lamp. A single connected shadow begins at that tip and opens into the distinct ribbed outline of an expanded umbrella canopy on the same floor. The closed fabric, tip contact, shadow connection and open shadow canopy are visible together.',
      '닫힌 우산 끝이 밝은 타일 바닥에 닿아 있고 옆에 노출 조명 하나가 있다. 끝 접점에서 이어진 그림자 하나가 같은 바닥에서 펼쳐진 우산살 윤곽의 넓은 차양 모양을 이룬다. 접힌 천, 끝 접점, 그림자의 연결부, 펼쳐진 그림자 차양이 함께 보인다.',
      ['umbrella','lamp','floor','shadow'],['tip contacts floor','shadow connects tip','shadow depicts expanded canopy'],
      ['접힌 실물 천과 펼쳐진 그림자의 구별','끝에서 시작하는 연결과 동일 수광면'],['벽의 별도 우산 그림','여러 광원','접힌 천의 정상적인 넓은 투영'],['그림자의 독립 행동·시간 지연·숨은 광원 부재'],['S02','S21','S25'],['cand_db5627732e3253898ef5e9541d5b9a53','cand_ff9b3acd769b5305b9c4c8dae92b0dec'],'기존 손·팔의 불일치를 신체 없이 표현하는 완성 변형. 실물/수광면 연결은 보존한다.')
    add('R12','그릇의 빈 안쪽과 맞물리는 고형','M10','P1',
      'A shallow ceramic bowl is tipped onto its side beside a solid matte block with the convex shape of the bowl’s interior. The bowl’s open concavity faces the block, and one distinctive notch in the rim corresponds to a raised tab on the block. Both separate outlines and the gap between them remain visible on the same table.',
      '얕은 도자기 그릇이 옆으로 기울어 있고 옆에는 그릇 안쪽과 같은 볼록한 형상의 무광 고형이 따로 놓여 있다. 열린 오목면이 고형을 향하며 테두리의 특징적인 홈 하나가 고형의 돌출 탭과 대응한다. 같은 탁자에서 두 개체의 윤곽과 사이 틈이 함께 보인다.',
      ['bowl','solid','table'],['concavity faces solid','notch corresponds to tab','solid separate from bowl'],['빈 용기와 대응하는 양형의 동시 비교','서로 분리된 경계와 특징적 맞물림'],['뚜껑','공장 주형','무관한 둥근 소품'],['실제 주조 과정·빈 공기의 물질화·관객의 즉각적인 원리 이해'],['S15'],['cand_6bffebe753ee51f8ab02a8528fde36ba'],'Ghost의 설명 의존 위험을 줄이기 위해 원형 용기와 양형의 비교를 함께 설계했다. 제작 가능한 조형이라는 대체 해석은 남는다.')
    add('R13','봉제 외피로 접히는 문틀','M09','P0',
      'In an ordinary hallway, one doorway is formed from translucent sewn fabric with visible hinge and latch shapes stitched into it. A lower corner of the same doorway folds onto the floor, exposing its fabric hem, while a solid wooden doorway beside it retains normal thickness. The stitched opening, folded corner and neighboring wooden reference are visible together.',
      '평범한 복도에서 문틀 하나가 반투명 봉제 천으로 이루어지고 천 위에 경첩과 빗장 형상이 박음질되어 있다. 같은 문틀의 아래 모서리가 바닥으로 접혀 천 단을 드러내며, 옆의 단단한 나무 문틀은 정상 두께를 유지한다. 봉제 개구부, 접힌 모서리, 옆 나무 기준이 함께 보인다.',
      ['fabric_doorway','floor','wooden_doorway'],['fold belongs to fabric doorway','hem continuous with doorway','wooden doorway separate reference'],['봉제선·천 단·한 문틀의 접힘 연속','별도의 정상 건축 기준'],['커튼이 달린 정상 문','벽 장식 천','축소 세트'],['실제 하중·거주 가능성·소유자의 기억이나 이주 경험'],['S18'],['cand_118163cedc90550899969a70d966babd','cand_dbbaeb68cc555881beb4b119c8b32d11'],'일반 장식 천과 유기적 벽을 대체하지 않는 건축 외피 변형. 인물이나 기계가 필수는 아니다.')
    add('R14','인쇄 강에서 탁자로 이어지는 리본','M08','P1',
      'An open illustrated book rests on a table. A blue river printed on one page becomes a narrow physical ribbon at a clearly visible page edge; that same ribbon arches over a small air gap and settles on the tabletop with a contact shadow. The printed river, edge transition and separate ribbon underside remain visible together.',
      '그림책이 탁자에 펼쳐져 있다. 한 페이지에 인쇄된 푸른 강이 보이는 페이지 가장자리에서 가는 실제 리본으로 이어지고, 같은 리본이 작은 공기 틈 위로 휘어 탁자에 닿아 접촉 그림자를 만든다. 인쇄 강, 가장자리 전환부, 리본의 별도 아랫면이 함께 보인다.',
      ['book','printed_river','ribbon','table'],['ribbon continuous with printed river','ribbon crosses page edge','ribbon contacts table'],['평면 인쇄와 두께 있는 리본을 가르는 경계','동일 경로의 연속과 탁자 접촉'],['페이지 위에 놓은 무관한 끈','책갈피','팝업 북의 정상 제작'],['실제 차원 이동·애니메이션·강의 물이 흘렀다는 이력'],['S19','S22'],['cand_7193917dbadb5f5f97e1284c74e349c9','cand_2688bf2be5365cde9f1728e258ebe8ce'],'기존 책 밖 팔/스크린 밖 다리와 달리 인간 부위를 추가하지 않는 재현-물체 경계의 완성 사례.')
    add('R15','빗의 이와 뿌리가 이어지는 정물','M12','P1',
      'A wooden comb lies across the rim of a shallow tray of soil. Its teeth continue into separate tapering root forms that enter the soil, while the polished handle and several unaltered teeth remain recognizable above the tray. The tooth-to-root joins and soil entry points are visible in one still-life view.',
      '나무 빗이 흙 담긴 얕은 쟁반 테두리를 가로지른다. 빗살들이 각각 가늘어지는 뿌리 형상으로 이어져 흙에 들어가며, 매끈한 손잡이와 변하지 않은 빗살 몇 개가 쟁반 위에서 식별된다. 빗살과 뿌리의 접합, 흙 진입점이 한 정물 시점에서 보인다.',
      ['comb','roots','soil','tray'],['roots continuous with comb teeth','roots enters soil','handle remains recognizable'],['같은 사물에서 보존된 기능 형상과 전환부','각 뿌리의 연결과 흙 진입'],['빗 뒤에 꽂은 별도 식물','뿌리 장식 제품','흙에서 자란 실제 빗'],['실제 발아·생명·진화·성장 과정'],['S01','S23'],['cand_542fa53665fe5810a406b0f6b9984eae'],'잎 달린 열쇠라는 기존 원리를 다른 식물 소품으로만 늘리지 않도록 기능 형상과 뿌리의 대응을 비교할 후속안. 이 보완이 약하면 별도 후보 대신 연구 변형으로 남긴다.')
    add('R16','빗속의 한 마른 자리','M06','P0',
      'Rain streaks and small splash crowns occupy a paved courtyard, but one sharply bounded circular patch around a plain chair remains visibly dry. Wet paving and falling drops surround that patch on every visible side, and the same paving grid continues across its boundary. An open side view includes clear air above the chair and both wet and dry ground.',
      '포장 중정에 빗줄기와 작은 튀는 물방울이 보이지만 단순한 의자 주위의 경계 뚜렷한 원형 자리 하나는 마른 표면이다. 보이는 모든 방향에서 젖은 포장과 빗방울이 그 자리를 둘러싸며 같은 바닥 격자가 경계를 가로질러 이어진다. 열린 측면 시점에 의자 위 공기와 젖은/마른 바닥이 함께 들어온다.',
      ['chair','dry_patch','wet_paving','rain'],['dry patch surrounds chair','wet paving surrounds dry patch','same paving continues across boundary'],['강우·젖은 바깥과 마른 안쪽의 국소 차이','바닥 연속과 보이는 위쪽 공간'],['차양','다른 재질의 발수 바닥','막 그친 비','부분 물뿌리기'],['실제 보호 마법·연속 강우 시간·화면 밖 차양 부재'],['S17'],['cand_127c0ace3acd5724abb155e5cef707c3'],'소리/열까지 한 외형으로 통합하지 않고, 기존 국소 예외 원리의 가시적 강우 변형을 독립 제안한다.')
    add('R17','한 가지에만 남은 서리','M06','P0',
      'A continuous leafy branch lies across an ordinary sunlit garden bench. One short bounded section carries white frost crystals over its leaves and wood, while the connected sections on either side remain green and clear. Both transition boundaries, the continuous branch and ordinary summer foliage behind it are visible together.',
      '햇빛 드는 정원 벤치에 잎 달린 가지 하나가 연속해서 놓여 있다. 짧고 경계 있는 한 구간의 잎과 목재에만 흰 서리 결정이 붙고, 연결된 양쪽 구간은 녹색의 맑은 표면을 유지한다. 두 전환 경계, 연속된 가지, 뒤의 평범한 여름 잎이 함께 보인다.',
      ['branch','frost_section','leaves','bench'],['frost belongs to bounded branch section','green sections continuous with same branch'],['같은 가지의 양끝 전환과 결정 구조','다른 녹색 가지가 뒤에 놓인 원근 혼동 방지'],['인공 눈','소금 결정','그늘에 남은 서리','장식 가지'],['실제 계절·온도·서리가 자란 과정·생존 여부'],['S23'],['cand_192c1989f25a5a96b9454926f302d132','cand_02a670e5fc2b59e8b9ce3d4ab33d6a40'],'기존 계절 예외를 시간 경과 없이 관찰 가능한 한 대상의 경계로 정제한 완성 변형이다.')
    add('R18','손에서 떨어진 빗자루의 접촉 상태','M03','P1',
      'A broom leans diagonally over a small dust line with its bristles contacting the floor and its handle suspended clear of surrounding furniture. A person stands beside it with both open hands visibly separated from the handle. The bristle contact, entire handle and gaps around it are readable in the same frame.',
      '빗자루가 작은 먼지 선 위로 비스듬히 놓이고 솔은 바닥에 닿지만 손잡이는 주변 가구에서 떨어져 있다. 옆 인물의 펼친 두 손은 손잡이와 분리되어 보인다. 솔 접촉, 손잡이 전체, 주위 간격이 같은 프레임에서 읽힌다.',
      ['broom','dust','floor','person'],['bristles contacts floor','hands separated from handle','handle clear of furniture'],['지지 끝점과 손의 분리','빗자루 전체·먼지의 현 상태'],['정지된 균형','숨은 줄','순간적으로 놓은 도구'],['스스로 움직임·청소 완료·자율성·연속 지지 부재'],['S05','S20'],['cand_b87c0f3464fe5d18b30c009a9a866001'],'스스로 청소한다는 상위 서사를 정지된 무접촉/접촉 상태와 분리한다. 자동 청소의 직접 증거로 승격하지 않는다.')
    add('R19','수면에서 이어지는 열린 액체 고리','M02','P2',
      'A clear glass contains water. One smooth liquid arch rises from two distinct points on the same water surface, leaving an open air gap beneath its curved top. The two surface joins, transparent arch and uninterrupted glass rim remain visible; small highlights follow the arch’s continuous surface.',
      '투명 유리잔에 물이 담겨 있다. 같은 수면의 서로 다른 두 지점에서 매끈한 액체 아치 하나가 이어져 나오고 굽은 꼭대기 아래에는 열린 공기 틈이 남는다. 두 수면 접합점, 투명 아치, 끊기지 않은 잔 테두리가 보이며 작은 하이라이트가 아치 표면을 따라 이어진다.',
      ['glass','water_surface','liquid_arch'],['arch joins same surface at two points','air gap below arch'],['두 액체 연결점과 닫힌 잔 테두리','고리 아래 공기·연속 표면'],['순간 물튀김','투명 고체 조형','별도 유리 손잡이'],['지속 부유·운동 방향·표면장력 법칙 위반·실제 물질 조성'],['S17'],['cand_4b7b95746ccc5196825384fa83558cac'],'액체 형태 유지라는 일반 후보의 두 접합점을 가진 완성 변형. 물튀김의 정상 대체 해석이 강해 후순위다.')
    add('R20','작은 캔버스와 창밖 나무의 정렬','M08','P1',
      'A small unframed landscape canvas stands on an easel directly in front of a window. A painted tree branch continues in alignment with the visible branch outside the canvas edge, while the canvas thickness, top clip and easel legs remain visible. An ordinary windowsill separates the interior supports from the outdoor view.',
      '작은 액자 없는 풍경 캔버스가 창 앞 이젤에 놓여 있다. 그림 속 나뭇가지가 캔버스 가장자리 밖에서 보이는 가지와 정렬되지만 캔버스 두께, 상단 클립, 이젤 다리는 보인다. 평범한 창턱이 실내 지지물과 바깥 풍경을 구분한다.',
      ['canvas','painted_branch','outdoor_branch','easel','window'],['painted branch aligns with outdoor branch','canvas supported by easel','window separates views'],['재현면의 두께·지지와 실외 대응의 동시 가시성'],['정상적인 정렬 촬영','투명 판','화면 합성'],['실제 가지 관통·풍경 소실·무한 재귀·캔버스를 옮긴 후 상태'],['S19','S22'],['cand_90f4412c7de75c5f8e9a234043b64857'],'재현과 실제의 지각적 경계만 다룬다. 물리적 불가능성을 요구하지 않는 설정 범위와 경계 대조에 유용하다.')

    reuse_specs=[
      ('R21','네 접속점의 계단 루프','M11','P2','cand_1a7a2cd1b6875505ba73c523bc9142c2',['S11'],['네 계단 구간·네 계단참·한 방향의 상승 디딤면'],['일반 나선 계단','가린 모서리'],['실제 무한 계단·실제 비유클리드 공간'],'기존 완성 관계가 이미 있어 새 계단 후보를 추가할 필요가 없다.'),
      ('R22','실제 방과 같은 열린 방 모형','M11','P1','cand_4f9aa7915bdd53f5b9a974059bebf7d7',['S19'],['같은 창과 탁자 배치의 실제 방/모형 동시 가시성'],['비슷한 모형','그림 속 방'],['무한·실제 기억·시간 되돌림'],'기존 H01의 완성 원문을 재사용하고 자기귀환 주장과 단순 대응을 분리한다.'),
      ('R23','보통 의자와 작은 문','M07','P0','cand_f78b8c2e0cd35d21a931a23bfdb8e3de',['S10'],['온전한 문·의자·동일 바닥과 깊이'],['원근 축소','부분 문 장식'],['실제 치수·다른 세계로 통하는 기능'],'기존 완성 규모 관계를 강도 비교와 의미 조회 경로에 재사용한다.'),
      ('R24','방은 반사되지만 인물은 없는 거울','M01','P1','cand_3fc04cefeec75be28caf26ffd8ed227c',['S02','S25'],['같은 인물의 위치·거울·뒤 공간 대응'],['반사 밖 시점','거울 아닌 창'],['인물의 실제 비존재·정체성 상실'],'기존 선택적 반사 부재 source를 보존한다. 꽃 상태 차이와 자동 대체하지 않는다.'),
      ('R25','빛 원뿔 안의 국소 어두운 면','M04','P2','cand_b7befd8e444c554bb8ada27ef14c8c6f',['S21','S24'],['빛 원뿔·수광벽·같은 원뿔 안의 어두운 패치'],['평범한 투영 그림자','검은 페인트','전역 저노출'],['실제 빛 소멸·암흑 물질·효력'],'기존 source를 의미상 완전히 유지하고 어둠 키워드만 새로 더하지 않는다.'),
      ('R26','두 기둥과 아치의 얼굴 읽기','M11','P1','cand_7b3f6740821d5f839db30de43420e00e',['S01','S23'],['두 기둥의 밑동·중앙 빈 공간·얼굴의 이중 읽기'],['실제 얼굴 조각','단순 얼굴무늬'],['실제 생명·의도·두 읽기의 동시 지각'],'이미 있는 B01 완성 사례. 공유 경계 원리를 검증되지 않은 새 장르 규칙으로 바꾸지 않는다.'),
    ]
    for rid,title,mid,priority,cid,ss,evidence,confounds,limits,reason in reuse_specs:
        add(rid,title,mid,priority,'','',[],[],evidence,confounds,limits,ss,[cid],reason,decision='reuse_same_source',reuse=cid)
    for card in cards:
        card['neighbor_sources']=[{'candidate_id':cid,'source_sha256':digest(corpus[cid]),
                                  'source_primary_en':corpus[cid]['content'].get('en'),
                                  'source_primary_ko':corpus[cid]['content'].get('ko')}
                                 for cid in card['neighbor_candidate_ids']]
        card['strength_guidance']={'1':'관계를 읽을 수 있는 상태로 남기면서 사용자 장면을 보조할 수 있는지 검토.',
                                  '2':'대응·경계·접점과 실제 차이를 분명히 읽을 수 있는지 검토.',
                                  '3':'같은 관계가 전체 사진의 주된 해석을 이끄는지 검토. 면적이나 이상 요소 수만으로 판정하지 않음.',
                                  'all_levels_feasible':None,'image_verified':False}
    dump(HERE/'candidate-proposals.json',{'schema':'surreal-control-candidate-research/v1','status':'research_only_not_operating_assets',
      'counts':dict(collections.Counter(c['decision']for c in cards)),
      'novelty_limit':'Full source bodies of cited neighbors reviewed; root-primary lexical screen omits profile internals and nested branches. No whole-corpus semantic novelty claim.',
      'cards':cards})
    cue_pairs={
      'C01':('거울 속 가지에만 피어 있는 꽃','blossoms on the reflected branch only'),
      'C02':('돌처럼 보이는데 뺨 아래 눌린 베개','stone-looking pillow dented under a cheek'),
      'C03':('빈 의자를 아기처럼 안는 사람','cradling an empty chair on a lap'),
      'C04':('잔 안쪽 고리에 손가락을 걸어 들기','lifting a cup by a loop attached inside its wall'),
      'C05':('식탁과 천장 사이의 작은 구름','one cloud between a dining table and ceiling'),
      'C06':('낮 하늘 아래 밤 같은 골목','daylit sky over a nightlike lane'),
      'C07':('도로에 붙은 흰 표시의 들린 끝','raised end of a white road marking'),
      'C08':('가는 풀잎이 받친 큰 조약돌','a pebble resting on a narrow blade of grass'),
      'C09':('사람이 바닥의 거대 찻잔을 닦는 모습','cleaning a waist-high teacup on the floor'),
      'C10':('벽을 바닥처럼 쓰는 독서자','reader using a side wall as a floor'),
      'R11':('닫힌 우산과 펼쳐진 우산 그림자','closed umbrella with an open-canopy shadow'),
      'R12':('그릇의 빈 안쪽과 대응하는 고형','solid form matching a bowl interior'),
      'R13':('천 단이 접히는 봉제 문틀','sewn fabric doorway folding at its hem'),
      'R14':('인쇄 강에서 책 밖 리본으로 이어지는 길','printed river continuing as a ribbon beyond a page'),
      'R15':('빗살이 뿌리로 이어지는 정물','comb teeth continuing into root forms'),
      'R16':('비 오는 포장 한가운데 마른 자리','one dry patch surrounded by falling rain'),
      'R17':('같은 가지 한 구간의 서리','frost restricted to one section of the same branch'),
      'R18':('손이 떨어진 빗자루와 바닥 접점','broom-floor contact with hands clear of its handle'),
      'R19':('수면 두 점을 잇는 열린 액체 아치','liquid arch joining two points of one water surface'),
      'R20':('창밖 가지와 정렬된 캔버스','canvas branch aligned with the view outside a window'),
      'R21':('네 접속점이 드러난 상승 계단 루프','ascending stair loop with all four landings visible'),
      'R22':('실제 방과 같은 열린 방 모형','open model repeating the actual room layout'),
      'R23':('같은 바닥의 보통 의자와 작은 문','ordinary chair and tiny door at the same depth'),
      'R24':('방은 비추지만 앞사람은 없는 거울','mirror reflecting the room while omitting its standing person'),
      'R25':('빛 원뿔 안의 국소 어둠','localized dark zone inside a light cone'),
      'R26':('두 기둥과 빈 아치가 만드는 얼굴 윤곽','two columns and an arch void also forming a face outline'),
    }
    dump(HERE/'discovery-routes.json',{'schema':'surreal-control-discovery-research/v1',
      'automatic_activation':False,'fixed_intensity_routes':False,
      'rules':['These are authored discovery expressions, not independently verified genre definitions.',
               'Alias words alone do not establish complete source meaning or adoption authority.',
               'A held record is a diagnostic/control lead and is not a positive material target.'],
      'routes':[{'route_id':'route_'+c['research_id'],'mechanism_id':c['mechanism_id'],
                 'research_card_id':c['research_id'],'ko':cue_pairs[c['research_id']][0],
                 'en':cue_pairs[c['research_id']][1],
                 'existing_source_ids':[c['reuse_candidate_id']] if c.get('reuse_candidate_id') else [],
                 'proposed_new_source_id':None,'positive_material_target':c['decision']!='hold',
                 'confusion_boundaries':c['confounds'],'approval':'research_only'}for c in cards]})
    ordinary={
      'C01':('현관 거울에 화분과 찻잔이 정상적으로 비치는 일상','An ordinary entryway mirror accurately reflecting a potted plant and cup.'),
      'C02':('평범한 침실에서 천 베개에 기대 쉬는 모습','Resting on a fabric pillow in an ordinary bedroom.'),
      'C03':('작은 의자를 옮기는 가구 정리','Moving a small chair while arranging furniture.'),
      'C04':('바깥 손잡이를 잡은 평범한 빈 찻잔','An ordinary empty teacup held by its external handle.'),
      'C05':('실내 아침 식탁과 창밖 구름','Breakfast indoors with clouds outside the window.'),
      'C06':('낮 하늘과 햇빛 드는 주택가','A daytime sky above sunlit residential houses.'),
      'C08':('땅에 놓인 조약돌과 뒤의 풀잎','A pebble resting on the ground with grass behind it.'),
      'C09':('정상 크기 찻잔을 손으로 닦는 부엌','Cleaning a normal-sized teacup by hand in a kitchen.'),
      'C10':('복도 바닥의 의자에 앉아 읽는 사람','Reading in a chair supported by the hallway floor.'),
      'R11':('닫힌 우산과 대응하는 가는 그림자','A closed umbrella and its corresponding narrow shadow.'),
      'R12':('분리된 평범한 그릇과 뚜껑','An ordinary bowl and its separate lid.'),
      'R13':('단단한 나무 문틀에 걸린 얇은 커튼','A sheer curtain hanging within a solid wooden doorway.'),
      'R14':('책 위 인쇄된 강과 별도 책갈피','A river printed in a book and a separate bookmark.'),
      'R15':('화분 옆 탁자 위 빗','A comb on a table beside a potted plant.'),
      'R16':('차양 아래 마른 포장과 비 내리는 주변','Dry paving beneath an awning with rain around it.'),
      'R17':('정원의 평범한 녹색 가지','An ordinary green branch in a garden.'),
      'R18':('손으로 잡고 바닥을 쓸고 있는 빗자루','A broom held by a hand while sweeping the floor.'),
      'R19':('잔에서 순간적으로 튄 물방울','A splash of water above a glass in one frozen instant.'),
      'R20':('풍경을 그린 캔버스를 창 옆에서 보기','Viewing a landscape canvas beside a window.'),
      'R23':('작은 용과 집에서 아침 먹기 surreal=0','Breakfast at home with a small dragon, surreal=0.'),
    }
    cases=[]
    for c in cards:
        rid=c['research_id']
        if rid not in ordinary:continue
        ko,en=cue_pairs[rid]
        cases.append({'case_id':'positive_'+rid,'kind':'intended_relation','ko':ko,'en':en,
                      'research_target':rid,'must_review':['whole source meaning','owner and medium match','claim limits'],
                      'expected_operational_cid':c.get('reuse_candidate_id')})
        ko,en=ordinary[rid]
        cases.append({'case_id':'control_'+rid,'kind':'explicit_fantasy_preservation' if rid=='R23' else 'ordinary_or_normal_alternative',
                      'ko':ko,'en':en,'research_target':None,'must_review':['no unrequested alteration in final composition',
                      'retrieval exposure is recorded separately from adoption'],
                      'preserve_explicit_fantasy':rid=='R23'})
    dump(HERE/'retrieval-evaluation-plan.json',{'schema':'surreal-control-retrieval-evaluation/v1','status':'NOT_RUN',
      'case_count':len(cases),'bilingual_query_count':len(cases)*2,'cases':cases,
      'independent_holdout':False,'development_data_limit':'These requests were authored with access to the proposals. Separate blind requester paraphrases must be obtained before a holdout claim.',
      'comparison':'same queries against pinned current and staged generation; actual H-F2 BM25F/local-cosine lanes',
      'metrics':['correct complete source exposure','wrong owner/medium/state exposure','conditional adoption compatibility',
                 'unrequested final surreal addition','explicit fantasy preserved at zero'],
      'not_measured_by_this_research':['actual H-F2 ranks','local cosine recall','final rendered quality']})
    all_ids=set(cid for c in cards for cid in c['neighbor_candidate_ids'])|set(cid for m in mechanisms for cid in m['witness_candidate_ids'])
    dump(HERE/'evidence/decision-source-snapshots.json',{'records':{cid:corpus[cid]for cid in sorted(all_ids)}})

    diagnostics=[
      ('D04','정상적인 여러 색 그림자',['여러 광원과 한 인물의 여러 색 실루엣'],['그림자의 자율 행동','소유자 증식'],['S21'],'빛의 수·색만으로 초현실 설정 구현을 판정하지 않는다.'),
      ('D05','풍경과 정렬한 정상 캔버스',['캔버스 가장자리와 배경 대응'],['실제 차원 관통','풍경 복제 능력'],['S19'],'상징적/지각적 낯섦은 허용하지만 물리적 불가능성의 증거와 분리한다.'),
      ('D06','돌처럼 보이는 눌린 소품',['광물 같은 표면과 오목한 형상'],['진짜 석재의 연성','눌린 과정'],['S03'],'후보 C02의 외관·형태 관계와 물질 검증을 분리한다.'),
      ('D07','들린 도로 표시',['연속 표시와 들린 끝'],['재질 변환','살아 있는 도로'],['S08','S16'],'C07을 정상 도로 테이프/박리라는 반증 대조로 보존한다.'),
      ('D08','한 프레임의 균형과 무접촉',['돌·풀잎 접촉 또는 떨어진 손'],['지속 지지력','숨은 지지 부재','자율 청소'],['S20'],'행위 명칭이 정지 상태 이상의 증거를 공급하지 않는다.'),
      ('D09','하늘 구멍과 고체처럼 보이는 빛',['천장 개구부·하늘과 실내 조명'],['실제 고체화','다른 기후'],['S24'],'지각과 물리 상태를 분리하며 분위기만으로 불가능 사건을 발명하지 않는다.'),
      ('D10','박음질 건축 조형',['봉제 외피·정상 건축 기준'],['실제 거주 이력','인물 기억·향수','보이지 않는 하중'],['S18'],'작가의 주제 설명을 참조 인물의 실제 생애로 옮기지 않는다.'),
      ('D11','유리 아래 수영장 공간',['수면 인상·사람·실내 경계'],['수중 호흡','마른 옷의 원인'],['S13'],'실제 설치 구조가 가능한 경우도 초현실 인상 연구에 포함한다.'),
      ('D12','계절이 다른 듯한 한 구간',['서리 같은 결정·녹색 잎·전환'],['실제 온도','시간 경과','초자연적 보호'],['S23'],'기후/시간이라는 비가시 원인을 관계 단서로 과장하지 않는다.'),
      ('D13','틈이 작아서 안 보이는 관계',['해상도별 가시성 차이'],['은근한 강도 1의 성공'],['S14'],'미구현·미관측을 낮은 강도와 구분한다. 구체 임계 픽셀 수를 보편화하지 않는다.'),
      ('D14','사용자가 명시한 판타지와 surreal 0',['명시한 용·판타지 인물·불가능 구조'],['추가 설정이 0이므로 명시 요소 삭제'],[],'설정 0은 에이전트가 추가할 처리만 끈다. 사용자 소유 의미가 우선한다.'),
      ('D15','일반 반사·접촉 그림자 정합성',['정상 대응·촬영 원근'],['초현실 효과의 존재'],['S17'],'현재 surreal_physics_detail 일부는 보조 현실성 단서다. 별도 의미 구분 없이 효과 수로 세지 않는다.'),
      ('D16','강한 인상과 많은 소품의 혼동',['하나의 주도 관계 또는 다수 보조 요소'],['이상 요소 개수로 3 판정'],['S07'],'동일 관계의 역할을 판단하고 새로운 의무 수를 만들지 않는다.'),
    ]
    imported=[]
    for c in pro['diagnostics']:
        imported.append({'diagnostic_id':c['id'],'title_ko':c['name_ko'],'observable':c['observable'],
                         'not_inferable':c['not_inferable'],'source_ids':c['source_ids'],
                         'use_ko':'Pro의 진단 원문을 보존한 대조 자료. 긍정 시각 후보로 자동 변환하지 않는다.','positive_retrieval':False})
    imported.extend({'diagnostic_id':i,'title_ko':title,'observable':obs,'not_inferable':no,'source_ids':ss,'use_ko':use,'positive_retrieval':False}
                    for i,title,obs,no,ss,use in diagnostics)
    dump(HERE/'diagnostics.json',{'schema':'surreal-control-diagnostics/v1','records':imported})

    calibrations=list(pro['intensity_comparisons'])
    for item in calibrations:item['origin']='pro_original_preserved';item['execution_status']='NOT_RUN'
    additional=[
      ('I05','도자 커튼의 재질·형태','창가 정물과 커튼','천 커튼','C02','접힌 도자 판 커튼 하나','재질 경계와 고리/봉을 함께 보이되 창가 장면을 보조','도자 판과 커튼 기능의 충돌이 명백','같은 커튼의 물성이 공간을 읽는 주된 관계가 됨'),
      ('I06','닫힌 우산과 펼쳐진 그림자','현관의 우산 정물','닫힌 우산과 정상 그림자','R11','같은 닫힌 우산과 펼쳐진 그림자 하나','닫힌 실물과 펼쳐진 그림자 연결은 읽히며 현관 사용 맥락이 먼저 읽힘','실물과 그림자의 상태 차이가 명확','같은 상태 불일치가 사진 전체의 의미를 이끎'),
      ('I07','서리 경계가 있는 자연물','정원 벤치의 잎 달린 가지','정상 녹색 가지','R17','같은 가지의 같은 서리 구간','연속된 가지와 서리 경계가 읽히며 정원 정물을 보조','국소 결정과 양쪽 녹색 구간을 명확히 비교','경계 양쪽의 자연 상태 충돌이 사진의 주된 인상이 됨'),
      ('I08','봉제 문틀의 건축 외피','복도와 두 문틀','두 정상 나무 문틀','R13','같은 봉제 문틀과 같은 접힌 모서리','봉제선과 접힘은 읽히며 복도 생활 공간의 인상을 보조','나무와 천 문틀의 물성 차이가 명확','같은 문틀의 접힘과 건축 외피 관계가 사진의 공간 해석을 이끎'),
    ]
    for cid,title,topic,normal,ref,relation,one,two,three in additional:
        calibrations.append({'id':cid,'title_ko':title,'origin':'additional_domain_comparison','core_user_request_ko':topic,
          'candidate_ref':ref,'user_invariants':[topic,'명시 주제·대상 관계 보존'],'single_added_relation_ko':relation,
          'fixed_across_1_2_3':['선택한 관계의 대상·개수·핵심 형태','비교에 필요한 같은 소유자와 경계'],
          'levels':[{'level':0,'scene_ko':normal,'expected_main_impression':'명시된 주제를 보존하고 추가 관계를 넣지 않음'},
                    {'level':1,'scene_ko':one,'expected_main_impression':'판독 가능한 보조'},
                    {'level':2,'scene_ko':two,'expected_main_impression':'명확한 표현'},
                    {'level':3,'scene_ko':three,'expected_main_impression':'주된 해석과 방향'}],
          'common_evidence':['각 단계의 실제 이미지에서 관계 구현·판독·역할을 별도로 기록','면적·발견 시간·요소 수 하나로 수준을 결정하지 않음'],
          'invalid_success_cases':['핵심 관계 가리기','불완전한 렌더를 1로 분류','사용자 의미 삭제','명시한 환상 요소를 0에서 제거'],
          'is_tested':False,'execution_status':'NOT_RUN'})
    # I05 uses an existing porcelain-curtain realization rather than the stone-pillow card.
    calibrations[4]['candidate_ref']='cand_b294c59558ce5b2483da3b0d26fc1fea'
    dump(HERE/'calibration-plan.json',{'schema':'surreal-control-calibration-research/v1','groups':calibrations,
      'comparison_count':len(calibrations),'scene_count':sum(len(g['levels'])for g in calibrations),
      'generation_calls_executed':0,'global_unreality_monotonicity_required':False,
      'review_order':['labels_hidden_free_description','request_and_relation_fidelity','prominence_and_preference_separately'],
      'failure_categories':['relation_not_implemented','relation_unobservable','ordinary_alternative_dominates','wrong_prominence','request_meaning_lost'],
      'execution_staging':'16-image smoke subset before expanding to the Pro 48-image pilot; all image execution is future work requiring an image-test request.'})

    acquisition={'conversation_id':'6adc3342-1ccc-83ec-b74b-6f5a0f8edb14','conversation_url':'https://chatgpt.com/c/6adc3342-1ccc-83ec-b74b-6f5a0f8edb14',
      'read_thread':{'turn_limit':10,'has_more':False,'turn_count':1,'raw_response':'input/thread-read.json','attachments_returned':0},
      'chrome_fallback':{'reason':'generated sandbox files not returned as readable attachments','method':'cua native Chrome preview and download UI',
                          'downloaded':['surreal_candidate_draft.json','surreal_research_report_ko.md'],'completed':True},
      'files':[{'path':str(p.relative_to(HERE)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in sorted((HERE/'input').glob('*'))],
      'no_browser_followup_prompt_sent':True,'no_library_upload_performed':True,
      'content_scope':'one original user request, full assistant response, full 10-card/3-diagnostic/4-comparison/16-source JSON and full Markdown report'}
    dump(HERE/'evidence/acquisition.json',acquisition)
    print(json.dumps({'sources':len(sources),'mechanisms':len(mechanisms),'cards':len(cards),
      'decisions':dict(collections.Counter(c['decision']for c in cards)),'diagnostics':len(imported),'calibration_groups':len(calibrations)},ensure_ascii=False))


if __name__=='__main__':main()
