"""Build research-only cards/routes. Deliberately does not import runtime builders."""
from pathlib import Path
import collections, csv, hashlib, json
from research_sources import SOURCES

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

def read(name):
    return json.loads((HERE/name).read_text())

def write(name, value):
    (HERE/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

def tsv(name):
    with (HERE/name).open() as f:
        return list(csv.DictReader(f, delimiter='\t'))

def seeds(value):
    return [f'K{int(n):03d}' for n in value.split(',')]

SLOTS = {
 'training':['relational_action','prop_placement','location'],
 'stage':['body_pose','relational_action','composition'],
 'fan':['relational_action','prop_placement','prop'],
 'camera':['composition','lighting','capture_context'],
 'concept':['presentation_style','wardrobe_style','lighting'],
 'wardrobe':['wardrobe_style','wardrobe_layering','object_structure'],
 'gesture':['hand_pose','body_pose','expression'],
 'appearance':['hair_style','makeup_style'],
 'equipment':['prop','anatomical_connection','prop_placement'],
 'japan':['prop','wardrobe_style','prop_placement'],
 'virtual':['prop_placement','capture_context','object_structure'],
 'dark':['situation_context','relational_action','prop_placement'],
}

# Narrow presentation suggestions. They remain proposals, never source qualification.
SLOT_ROWS = '''
I001 composition,location
I002 composition,relational_action
I003 location,prop_placement
I004 relational_action,body_pose
I005 relational_action,prop_placement
I006 relational_action,location
I007 relational_action,prop_placement
I008 relational_action,prop_placement
I009 composition,location
I010 relational_action,prop_placement
I011 composition,proxemics
I012 body_pose,composition
I013 body_pose,composition
I014 body_pose,hand_pose
I015 body_pose,proxemics
I016 body_pose,relational_action
I017 body_pose,prop_placement
I018 hair_style,body_pose
I019 body_pose,composition
I020 relational_action,prop_placement
I021 relational_action,prop_placement
I022 prop_placement,composition
I023 composition,location
I024 prop_placement,composition
I025 hand_pose,prop_placement
I026 prop_placement,object_structure
I027 prop_placement,object_structure
I028 prop_placement,location
I029 prop_placement,relational_action
I030 composition,capture_context
I031 prop_placement,relational_action
I032 prop_placement,location
I033 composition
I034 composition
I035 composition
I036 composition,location
I037 location,proxemics
I038 lighting
I039 lighting,space_condition
I040 prop_placement,composition
I041 prop_placement,space_condition
I042 composition,prop_placement
I043 lighting,wardrobe_style,location
I044 expression,lighting,wardrobe_style
I045 hand_pose,wardrobe_style
I046 body_pose,wardrobe_style,expression
I047 wardrobe_style
I048 wardrobe_style,lighting
I049 wardrobe_style,expression,makeup_style
I050 body_pose,expression,wardrobe_style
I051 wardrobe_style,lighting
I052 wardrobe_style,object_structure
I053 wardrobe_style,lighting
I054 wardrobe_style
I055 wardrobe_style,surface_material
I056 wardrobe_style,object_structure
I057 wardrobe_style,object_structure
I058 wardrobe_style
I059 wardrobe_style,composition
I060 wardrobe_style,wardrobe_layering
I061 wardrobe_style
I062 wardrobe_style,object_structure
I063 wardrobe_style,object_structure
I064 wardrobe_style,object_structure
I065 wardrobe_style,wardrobe_layering
I066 wardrobe_style,wardrobe_layering
I067 wardrobe_style,wardrobe_layering
I068 wardrobe_style,object_structure
I069 wardrobe_style,wardrobe_layering
I070 wardrobe_style,object_structure
I071 wardrobe_style,object_structure
I072 wardrobe_style,object_structure
I073 wardrobe_style,object_structure
I074 wardrobe_style,surface_material
I075 wardrobe_style,object_structure
I076 wardrobe_style,object_structure
I077 hand_pose,wardrobe_style
I078 wardrobe_style,surface_material
I079 wardrobe_style,object_structure
I080 wardrobe_style,surface_material
I081 wardrobe_style,object_structure
I082 wardrobe_style,object_structure
I083 hand_pose
I084 body_pose,hand_pose
I085 hand_pose
I086 hand_pose
I087 hand_pose
I088 expression
I089 hand_pose,expression
I090 hand_pose
I091 expression
I092 expression,body_pose
I093 body_pose
I094 body_pose,hand_pose
I095 body_pose
I096 relational_action,prop_placement
I097 hair_style
I098 hair_style
I099 hair_style
I100 hair_style
I101 hair_style
I102 hair_style
I103 hair_color,hair_style
I104 eyeshadow_style,eye_makeup_line
I105 makeup_decoration
I106 skin_finish,cheek_makeup
I107 makeup_style
I108 makeup_decoration,hand_pose
I109 prop_placement,anatomical_connection
I110 prop_placement
I111 prop_placement,object_structure
I112 wardrobe_style,composition
I113 prop_placement,capture_context
I114 prop_placement,capture_context
I115 prop_placement,composition
I116 makeup_style,prop_placement
I117 proxemics,relational_action
I118 prop_placement,composition
I119 lighting,prop_placement
I120 prop_placement,relational_action
'''
SLOT_OVERRIDES={line.split()[0]:line.split()[1].split(',') for line in SLOT_ROWS.splitlines() if line.strip()}

def main():
    terms=read('seed-keywords.json')
    sources=[dict(zip(['id','title','url','source_type','access_status','verified_scope_ko','limits_ko'],s),
                  accessed='2026-10-23', access_timezone='Asia/Seoul',
                  remote_content_hash=None, pixel_specimen_reviewed=False) for s in SOURCES]
    write('sources.json',sources)
    cards=[]
    for r in tsv('visual-authored.tsv'):
        cards.append({
          'schema':'idol-research-visual-card/v1','id':r['id'],'name_ko':r['name_ko'],
          'family':r['family'],'seed_ids':seeds(r['seed_numbers']),'source_ids':r['source_ids'].split(','),
          'source_support':'domain_context_only_not_whole_scene_or_exact_specimen_proof',
          'authorship':'original_optional_scene_proposition_not_source_quote',
          'phrase_en':r['phrase_en'],'phrase_ko':r['phrase_ko'],
          'observable_components':[{'id':r['id']+f'.{i+1}','requirement_ko':s,'required_if_selected':True}
                                   for i,s in enumerate(r['visible_checks'].split('|'))],
          'owner_relation_contract':{
            'complete_proposition_en':r['phrase_en'],'complete_proposition_ko':r['phrase_ko'],
            'owner_rule':'Retain each stated actor, limb, garment, prop, surface, display and represented image owner; every directed relation keeps both endpoints.',
            'occluded_endpoint':'unobservable_not_pass','actor_count':'only_the_count_explicit_in_this_selected_proposition',
            'no_new_owner_permission':True},
          'confusion_boundary':r['confusion_boundary'],'proposed_slots':SLOT_OVERRIDES[r['id']],
          'slot_status':'unreviewed_role_proposals','evidence_level':'authored_research_draft',
          'adoption_rule':'Optional whole proposition only, subject to frozen request compatibility; no keyword-triggered adoption.',
          'pixel_gate':'All selected distinguishing components and relation endpoints jointly observable; hidden or partial required evidence cannot pass.',
          'native_qualification':'not_attempted','runtime_importable':False,'native_approval':False,
          'status':'research_only_draft_requires_bilingual_source_and_role_review',
        })
    contexts=[]
    for r in tsv('context-authored.tsv'):
        contexts.append({'id':r['id'],'name_ko':r['name_ko'],'seed_ids':seeds(r['seed_numbers']),
                         'source_ids':[] if r['source_ids']=='-' else r['source_ids'].split(','),'meaning_boundary_ko':r['meaning_boundary'],
                         'required_evidence_ko':r['required_evidence'],'positive_retrieval':False,
                         'source_support':'no_direct_source_preserved_seed_with_authored_inference_boundary' if r['source_ids']=='-' else 'bounded_context_only_review_limits_in_sources_and_holds',
                         'runtime_importable':False,'native_approval':False})
    holds=read('holds.json')
    routes=[]
    for term in terms:
        k=term['id']; visual=[c['id'] for c in cards if k in c['seed_ids']]
        context=[c['id'] for c in contexts if k in c['seed_ids']]
        hold=[h['id'] for h in holds if k in h['seed_ids']]
        routes.append({**term,'optional_component_card_ids':visual,'context_card_ids':context,
                       'hold_ids':hold,
                       'route_type':'component_options_with_context' if visual else 'context_only',
                       'coverage_status':'research_disposition_complete_not_semantic_verification_complete',
                       'equivalence':False,'whole_compound_term_qualified':False,
                       'adoption_authority':False,'runtime_importable':False,
                       'unrealized_variants':'Compound terms retain all seed wording; a linked component is one option, not coverage of every variant.'})
    write('semantic-cards.json',cards)
    write('context-distinctions.json',contexts)
    write('keyword-routes.json',routes)
    write('candidate-drafts.json',{'schema':'idol-research-candidate-proposals/v1',
          'runtime_importable':False,'not_native_corpus_schema':True,
          'proposals':[{'proposal_id':'D'+c['id'][1:],'research_card_id':c['id'],
                        'phrase_en':c['phrase_en'],'phrase_ko':c['phrase_ko'],
                        'proposed_slots':c['proposed_slots'],'source_ids':c['source_ids'],
                        'required_review':['whole bilingual meaning','intrinsic conditions and actual effects',
                                           'source-local positive anchors','all owners and receivers',
                                           'each proposed role','fresh native qualification'],
                        'native_candidate_id':None,'record_kind_proposal':'visual_option',
                        'native_approval':False,'runtime_importable':False} for c in cards]})
    audit=read('CORPUS-AUDIT.json');byid={x['candidate_id']:x for x in audit['hits']}
    triage=[
      ('cand_6ff9d861c3db5ee7bb25f18010fbb409','reuse_if_full_source_review_passes','기존 손가락 하트 표현. I083의 좌우·교차·세 손가락과 정확히 같은 의미인지는 별도 검토.'),
      ('cand_5378606137b15201a2e4a17cc6efa6cd','keep_broad_subject','adult idol-style model은 직업·실력·특정 장면·매력을 충분히 표현하지 않는다.'),
      ('cand_65179620e4b4565d86edad1b72df6ffe','keep_role_context','연습생 직업과 나이·데뷔 확정·스쿨룩을 분리할 것.'),
      ('cand_a484eccc3cca5836b6e16efb8477bbef','split_into_new_proposals','동선·보컬·수선·큐시트·팬메시지를 한 행동에 섞는다. 기존 원문을 보존하고 I001~I010을 독립 대안으로 추가 검토.'),
      ('cand_55c9e3a3366255c9ae86faa1526726b5','context_not_visual_proof','제작 노동의 권리·휴식이 성공을 유지한다는 인과는 한 장의 가시 표현이 아님.'),
      ('cand_64d41dce1fb952dfbe9884764f91b5a5','separate_static_from_temporal','초점 회전·시선 인계는 단일 포즈와 구분. 인원 추가와 동작 변경은 코어 제약 점검.'),
      ('cand_b2a186e4393d5f998f3d4e4e25b0c3aa','reuse_location_if_compatible','일반 모션캡처 제작실을 재사용하되 실물·화면 소유자를 I113~I115에서 별도 묶는다.'),
      ('cand_22328a3da9755a8d89e3752f8e1ffefb','separate_visible_tools_from_claims','마커·격자·상태등·권리 태그는 도구이며 권한·정체성·지연 성능의 증거가 아님.'),
      ('cand_7ac104d9560a5ec882e71d5df014434a','reuse_props_if_compatible','동선표·악보·수선복·큐시트는 여러 소유자의 독립 소품. 전부를 강제 번들로 묶지 않는다.'),
      ('cand_6d044ad239ee56bf94758f381458a149','reuse_prop_components_if_compatible','일반 응원 조명·카드 슬리브·바인더를 포토카드·탑꾸·팬덤 정체성의 동의어로 만들지 않는다.'),
      ('cand_897f789501cc5135b3aecb9e01ffb4a7','do_not_generalize_exclusions','실존 인물·아바타·로고·안무·UI를 제외하는 개별 후보 조건을 아이돌 장르의 전역 배제로 옮기지 않는다.'),
      ('cand_b698686e52cd53d2bf567691b46becaa','retain_cross_genre_context_only','마법소녀·아이돌·버추얼 창작자를 섞은 세계 맥락은 본 연구의 세부 구별을 대신하지 못함.'),
    ]
    write('existing-source-triage.json',[{**byid[cid],'decision':d,'rationale_ko':why,
           'source_mutation':False,'reuse_approved':False} for cid,d,why in triage])
    counts={'seed_keywords':len(terms),'seed_scene_examples':len(read('seed-scene-examples.json')),
            'public_sources':len(sources),'visual_cards':len(cards),'candidate_proposals':len(cards),
            'context_distinctions':len(contexts),'keyword_routes':len(routes),
            'routes_with_component_options':sum(bool(r['optional_component_card_ids']) for r in routes),
            'context_only_routes':sum(not r['optional_component_card_ids'] for r in routes),
            'hold_topics':len(holds),'held_seed_keywords':len({k for h in holds for k in h['seed_ids']}),
            'observable_components':sum(len(c['observable_components']) for c in cards),
            'existing_source_triage':len(triage),
            'proposed_slot_links':sum(len(c['proposed_slots']) for c in cards),
            'visual_families':dict(collections.Counter(c['family'] for c in cards)),
            'runtime_source_records_added':0,'native_qualifications':0,'image_calls':0}
    write('SUMMARY.json',counts)
    lines=['# 아이돌물 시각 카드 초안','',
           '모든 카드는 연구용 선택 대안이다. 출처는 분야·기능 맥락을 뒷받침하며 아래 전체 장면은 작성자가 설계했다. 출처의 정확한 표본·모든 구조가 확인되었다는 뜻이 아니다. 실제 데이터 등록·native 자격·검색·이미지 검증은 실행하지 않았다.','']
    for c in cards:
        lines += [f"## {c['id']} {c['name_ko']}",'',c['phrase_ko'],'',c['phrase_en'],'',
                  '- 관찰: '+' / '.join(x['requirement_ko'] for x in c['observable_components']),
                  '- 경계: '+c['confusion_boundary'],
                  '- 출처 맥락: '+', '.join(c['source_ids'])+'; 전체 장면은 저자 설계.',
                  '- 제안 슬롯: '+', '.join(c['proposed_slots'])+'; 개별 역할 적합성 검토 전.','']
    (HERE/'VISUAL-CARDS.md').write_text('\n'.join(lines))
    lines=['# 원문 325개 키워드별 반영 처분','',
           '연결은 전체 용어의 동의어·필수 표현·모든 하위 변형의 검증을 뜻하지 않는다. 원문은 비신뢰 조사 씨앗이며 각각의 현행 사실을 보증하지 않는다.','',
           '| ID | 원문 용어 | 선택형 부분 카드 | 문맥 카드 | 보류 |','|---|---|---|---|---|']
    for r in routes:lines.append('| '+' | '.join([r['id'],r['term'],', '.join(r['optional_component_card_ids']) or '—',', '.join(r['context_card_ids']),', '.join(r['hold_ids']) or '—'])+' |')
    (HERE/'KEYWORD-ATLAS.md').write_text('\n'.join(lines)+'\n')
    lines=['# 출처와 사용 범위','',
           '열람일: 2026-10-23, Asia/Seoul. 원격 페이지 바이트 해시는 저장하지 않았고, 검색 반환 본문·목록만 확인한 항목은 접근 상태로 구분한다. 시각 표본의 픽셀 검토는 이번 패키지에 없다.','']
    for s in sources:lines += [f"## {s['id']} [{s['title']}]({s['url']})",'',
         f"상태: `{s['access_status']}`",'',s['verified_scope_ko'],'',s['limits_ko'],'']
    (HERE/'SOURCES.md').write_text('\n'.join(lines))
    print(json.dumps(counts,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
