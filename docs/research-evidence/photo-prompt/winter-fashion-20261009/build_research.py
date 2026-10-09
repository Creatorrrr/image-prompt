"""Build research artifacts only. Does not import or modify runtime assets."""
import collections
import csv
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]

def dump(name,value):
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def read_rows(name,n):
    rows=[]
    for line in (HERE/name).read_text().splitlines():
        if not line or line.startswith('#'):continue
        row=line.split('|');assert len(row)==n,(name,row[0],len(row))
        rows.append(row)
    return rows

def main():
    inv=json.loads((HERE/'term-inventory.json').read_text())
    ids=json.loads((HERE/'current-record-ids.json').read_text())
    real_ids=set(ids['candidates'])|set(ids['profiles'])
    snapshot=json.loads((HERE/'source-snapshot.json').read_text())
    sources=[dict(id=k,issuer=issuer,title=title,url=url,access_level=access,
                  verified_scope_ko=scope,claim_limits_ko=limits,checked_date_kst='2026-10-09')
             for k,issuer,title,url,access,scope,limits in read_rows('source-notes.txt',7)]
    source_by_id={s['id']:s for s in sources}
    relations={k:{'subject':subject,'predicate':predicate,'object':obj,'binding_ko':binding,
                  'status':'family_example_not_activated_runtime_relation'}
               for k,subject,predicate,obj,binding in read_rows('relation-blueprints.txt',5)}
    cards=[]
    for row in read_rows('research-cards.txt',13):
        k,title,groups,axis,owner,props,meaning,boundary,visible,refs,existing,priority,variants=row
        refs=refs.split(',');existing=[] if existing=='-' else existing.split(',')
        assert all(x in source_by_id for x in refs),(k,refs)
        assert all(x in real_ids for x in existing),(k,existing)
        cards.append(dict(id=k,title_ko=title,seed_groups=groups.split(','),axis=axis,owner_ko=owner,
            proposed_property_suffixes=props.split(','),meaning_ko=meaning,confusion_boundary_ko=boundary,
            observation_prerequisites_ko=visible,source_ids=refs,existing_ids_to_review=existing,
            priority=priority,independent_clauses_en=[] if variants=='-' else variants.split('~'),
            relation_example=relations[k],status='research_proposal_not_runtime_registration',
            fact_boundary='Source scope is bounded and may cover a family or one product only. Component graphs, candidate formulations and tests are researcher proposals.',
            alternatives='Choose one specific variant; never turn the family pool into an all-of obligation.',
            activation='Bare labels and search similarity are advisory. Hard duties require exact requester context, owner binding and explicit selected components.',
            validation_status='no_live_retrieval_no_candidate_selection_no_render'))
    assert len(cards)==79 and len(relations)==79
    card_by_id={c['id']:c for c in cards}
    routes={t['id']:[] for t in inv['terms']};groups={g['id']:g['term_ids'] for g in inv['groups']}
    def a(group,card_ids,positions=None):
        card_ids=[card_ids] if isinstance(card_ids,str) else card_ids
        for i in (range(1,len(groups[group])+1) if positions is None else positions):
            row=routes[groups[group][i-1]];row.extend(k for k in card_ids if k not in row)
    a('01','WF01',[1,2,3,4]);a('01','WF02',[5,7,8,9]);a('01','WF03',[6,10,11]);a('01','WF04',[12])
    a('02a','WF05',range(1,9));a('02a','WF07',[9]);a('02a','WF06',[10,11]);a('02a','WF08',[12])
    a('02b','WF09',[1,2,3]);a('02b','WF10',[4,5,6]);a('02b','WF11',[7,8,9]);a('02b','WF12',[10,11,12])
    a('02b','WF13',[13,14]);a('02b','WF14',[15,16,17]);a('02b','WF07',[16]);a('02b','WF04',[18]);a('02b','WF03',[19,20])
    a('03','WF15',[1,2]);a('03','WF16',[3,4,7]);a('03','WF17',[5,6]);a('03','WF18',[8,9,10])
    a('03','WF19',[11]);a('03','WF20',[12,13]);a('03','WF21',[14,15,16]);a('03','WF22',[17,18])
    a('04a','WF23',[1,2,13,14]);a('04a','WF24',[3,4,5]);a('04a','WF25',[6]);a('04a','WF26',[7,8,9])
    a('04a','WF27',[10,11]);a('04a','WF28',[12]);a('04a','WF29',[15]);a('04a','WF30',[16])
    a('04b','WF31',[1,2,3,4]);a('04b','WF32',[5,6,7]);a('04b','WF33',[8,9,10]);a('04b','WF34',[11,12,13,14])
    a('04b','WF35',[15,16,17]);a('04b','WF07',[18])
    a('05','WF36',[1,2,3,4,5]);a('05','WF37',[6,7,8,9,10]);a('05','WF38',[11,12,13]);a('05','WF39',[14,15,16])
    a('06','WF41',[1,6,7,8,9,10,11,12]);a('06','WF40',[2,3,4,5]);a('06','WF42',[13,14,15,16,17,18]);a('06','WF43',[19,20,21])
    a('07','WF44',[1,2,3,4]);a('07','WF45',[5,6,7,8,9,10,11,12]);a('07','WF46',[13,14,15,16,17,18])
    a('08','WF47',[1,2,3,4]);a('08','WF48',[5,6,7,8,9]);a('08','WF49',[10,11,12]);a('08','WF50',[13,14])
    a('08','WF51',[15,16,17]);a('08','WF52',[18,19,20]);a('08','WF43',[20])
    a('09a','WF53');a('09a','WF16',[2]);a('09a','WF44',[3]);a('09a','WF36',[4]);a('09a','WF13',[5]);a('09a','WF45',[8]);a('09a','WF42',[9]);a('09a','WF48',[10])
    a('09b','WF54',range(1,11));a('09b','WF55',[8,11,12,13,14,15])
    a('10','WF56',range(1,10));a('10','WF05',[1]);a('10','WF57',[10,11,12,13,14]);a('10','WF47',[8,9])
    a('11','WF58',range(1,8));a('11','WF05',[6]);a('11','WF16',[7]);a('11','WF59',[8,9]);a('11','WF60',[10,11,12]);a('11','WF61',[13,14,15]);a('11','WF62',[16,17,18])
    a('12','WF63',[1,2,3,4,5]);a('12','WF64',[6,7,8,9,10]);a('12','WF65',[11,12,14,15,16]);a('12','WF07',[13]);a('12','WF63',[13])
    a('13','WF66',range(1,7));a('13','WF67',range(7,13));a('13','WF68',range(13,18));a('13','WF69',[18,19,20])
    a('14','WF70',range(1,10));a('14','WF25',[10]);a('14','WF71',range(11,18));a('14','WF08',[18])
    a('15','WF72',range(1,8));a('15','WF73',[8,9,10,11]);a('15','WF74',[12,13]);a('15','WF75',[14,15,16,17,18]);a('15','WF76',[19,20]);a('15','WF77',[21,22])
    assert all(routes.values())
    fiber_specs={'Wool','Merino wool','Lambswool','Cashmere','Mohair','Angora','Alpaca','Camel hair','Down','Synthetic insulation','Wool trousers','Wool shorts','Wool tights'}
    tech_specs={'Thermal','Insulation','Windproof','Water-repellent','Waterproof','Fill power','Fill weight'}
    processes={'Fisherman’s rib','Jacquard knit','Intarsia','Crochet','Boning','Underwire','Fleece-lined tights','Hold-ups / Stay-ups','Skort','Bodysuit'}
    term_plan=[]
    for t in inv['terms']:
        cs=[card_by_id[k] for k in routes[t['id']]];en=t['en']
        if en in tech_specs:kind='technical_specification';action='명세 의미 유지; 겉외관에서 성능·수치 추론 금지'
        elif en in fiber_specs:kind='fiber_specification_plus_optional_visible_surface';action='원료 명세 보존; 사용자가 선택한 가시 표면만 별도 변형으로 작성'
        elif t['group']=='15':kind='advisory_aesthetic';action='기존 하위 의미와 선택 조합 재사용; 고정 레시피·정체성·사건 금지'
        elif en in processes:kind='visible_result_and_hidden_construction_split';action='가시 형상·공정·내부 구조를 나누며 보이지 않는 부분은 별도 근거 필요'
        elif en in {'Sideboob / Side cleavage','Underboob'}:kind='explicit_adult_context_state';action='이름·조건 유지; 직접 용어 출처와 성인·정확한 가시 경계 확인 후 승격'
        else:kind='visible_form_or_state';action='기존 의미와 소유·범위·가시 조건까지 동등성 비교 후 재사용 또는 보강'
        term_plan.append(dict(id=t['id'],group=t['group'],source_term=t['source_term'],ko=t['ko'],en=en,
            card_ids=routes[t['id']],priority=min(c['priority'] for c in cs),meaning_kind=kind,planned_action_ko=action,
            source_ids=sorted({s for c in cs for s in c['source_ids']}),
            source_scope='Family-level or selected-product evidence; not every alias independently verified. Promotion resolves term-specific gaps.',
            existing_ids_to_review=sorted({i for c in cs for i in c['existing_ids_to_review']}),
            candidate_mention_count=len(t['positive_field_mentions']['candidates']),profile_mention_count=len(t['positive_field_mentions']['profiles']),
            record_equivalence='not_inferred_from_lexical_mention',runtime_ready=False))
    proposals=[]
    for c in cards:
        for i,clause in enumerate(c['independent_clauses_en'],1):
            bundle=int(c['id'][2:])>=72
            slot='surface_material' if int(c['id'][2:]) in set(range(4,23))|{58,59,60} else 'garment_detail'
            if int(c['id'][2:]) in set(range(23,45))|{53,54,56,57}|set(range(72,80)):slot='wardrobe_style'
            proposals.append(dict(id=f"{c['id']}_D{i:02d}",card_id=c['id'],en=clause,ko_meaning=c['title_ko'],
                proposal_kind='optional_bundle_clause' if bundle else 'selected_visible_variant_clause',
                proposed_slot=slot,owner_ko=c['owner_ko'],concept_units_proposal=[clause],
                family_relation_to_specialize=c['relation_example'],
                property_suffix_pool_to_narrow=c['proposed_property_suffixes'],
                owner_binding='Bind actual declared garment and wearer from requester/core. Research symbolic nodes are not runtime IDs.',
                effect_review='Inventory every asserted effect in the clause; assign only this variant effects using valid current target/property contracts. Never apply the whole family suffix pool.',
                selection_conditions=['garment already declared or garment creation explicitly open','exact requester context supports these components','every affected property unlocked or explicitly requested','all other garments, body, pose, location, lens and framing retained'],
                evidence_draft={'native_observation':c['observation_prerequisites_ko'],'reject_substitutes':c['confusion_boundary_ko'],
                    'gate_policy':'All activated evidence for the selected variant must be visible on the bound owner. Partial or unobservable evidence does not pass; hidden specifications use separate verification.'},
                source_ids=c['source_ids'],source_binding='Bounded source facts and researcher formulation; direct source checks before promotion if marked pending.',
                requires_explicit_adult_context=c['id'] in {'WF50','WF77'},
                runtime_registration=False,runtime_ready=False,images_generated=0))
    pairs=[dict(id=k,card_ids=cs.split(','),mode=mode,shared_request_context_ko=context,
                variant_A_ko=A,variant_B_ko=B,expected_distinction_ko=expected,status='planned_not_executed')
           for k,cs,mode,context,A,B,expected in read_rows('regression-pairs.txt',7)]
    mutations=[
        ('WM01','owner_swap','코트의 퍼 트림을 착용자 머리카락으로 대체','WF08'),
        ('WM02','disconnected_relation','토글·고리는 보이지만 통과와 양 앵커를 제거','WF25'),
        ('WM03','underlayer_delete','포인텔의 불투명 이너를 지워 맨살로 바꾸기','WF21'),
        ('WM04','hidden_spec_promotion','부푼 패널만 보고 down·800FP·방수 PASS 추가','WF03'),
        ('WM05','scope_expansion','코트 벨트 선택으로 안쪽 상의나 신체 허리를 변경','WF26'),
        ('WM06','camera_side_effect','니트 표면 후보 선택으로 고정된 전신 구도를 macro로 변경','WF15'),
        ('WM07','partial_gate','가터끈만 보이고 스타킹 밴드 연결은 없는데 통과 처리','WF61'),
        ('WM08','occlusion_pass','스카프·코트가 가린 목선·등판을 라벨만으로 통과','WF79'),
        ('WM09','semantic_label_autoactivation','bare Fair Isle 또는 winter로 모든 부품을 강제','WF18'),
        ('WM10','unrequested_event','mob wife·military·harness로 범죄·무기·강제 사건 추가','WF76'),
        ('WM11','source_and_history_rewrite','기존 봉제·핏 의미·옛 fixture를 새 초안으로 통째 덮어쓰기','WF70'),
        ('WM12','mere_color_inference','피부색 안층을 착용자 맨살·피부색 변경으로 해석','WF59')]
    mutations=[dict(id=k,type=kind,mutation_ko=meaning,card_id=card,expected='reject_or_unscored_by_contract',status='planned_not_executed')
               for k,kind,meaning,card in mutations]
    render_groups=[
        ('WN01','리브·코듀로이·케이블','WF11,WF16,WF17','세로 골의 실제 구조·입체 교차·같은 니트 바탕'),
        ('WN02','포인텔·오픈워크+이너','WF21,WF52','구멍·연속 바탕·불투명 이너의 전부'),
        ('WN03','페어아일·요크','WF18,WF20','반복 모티프·배치 구역; 뒷면 공정은 별도'),
        ('WN04','시어링·셰르파·트림','WF07,WF08','바탕·접힌 양면·국소 부착 경계'),
        ('WN05','배플·누빔','WF04,WF31','볼록 셀·낮은 스티치 경계·코트 소유'),
        ('WN06','더플 토글·더블 앞판','WF24,WF25','양 앞판·여밈 부착점·통과 경로'),
        ('WN07','스카프 코트·별개 목통','WF30,WF66','접합부·닫힌 고리 또는 독립 자유 끝'),
        ('WN08','목선·어깨·커프','WF40,WF42,WF70','접힘·어깨 지지·썸홀 소유; 인체 실행 가능성 별도'),
        ('WN09','크롭·지퍼·배꼽','WF47,WF51','상의·하의·겉옷 경계·슬라이더 상태·명시된 기준점'),
        ('WN10','일루전·실제 빈 개구','WF43,WF48,WF52','직물 실체·빈 구역·연결부·아래층'),
        ('WN11','하이넥·등 개방·코트','WF49,WF79','원래 구도에서 실제 등 가시성; 진단 시점은 별개 요청'),
        ('WN12','타이츠·페이크 시어','WF58,WF59','실제 층 경계; 숨은 안기모·데니어는 이미지 PASS 제외'),
        ('WN13','가터·스타킹·부츠 구간','WF61,WF63,WF78','지지 전체 경로·같은 다리의 끝단·앞표면 정체'),
        ('WN14','미튼·머프·귀마개','WF67,WF68','손·엄지 공간·공용 통·귀 패드의 다른 소유'),
        ('WN15','별개 하네스·장식','WF69,WF71','스트랩·고리·앵커·그 아래 연속 옷; 사건 추가 없음'),
        ('WN16','원문 코디의 회귀','WF72,WF73,WF74,WF75,WF76,WF77,WF79','선택한 부품별 가시 의무·기존 옷·원문 의도·가림 보존')]
    render_groups=[dict(id=k,title_ko=title,card_ids=cs.split(','),native_gate_ko=gate,
        sample_plan='At least three independently sealed samples for the chosen difficult variant; compare against unchanged baseline only after identical non-target intent locks are verified.',
        evidence=['request envelope','authorial core and controls','candidate-pack v6','selected candidate/profile IDs','runtime receipt and audits','native image','per-gate review','user judgement'],
        result_states=['PASS','FAIL','UNOBSERVABLE_NOT_PASS','MODERATION_BLOCKED_UNSCORED','NOT_RUN'],status='NOT_RUN')
        for k,title,cs,gate in render_groups]
    dump('sources.json',{'schema_version':'research-sources/v1','sources':sources,'scope':'46 bounded sources; search body versus direct page access recorded separately; no wholesale copies of webpages.'})
    dump('semantic-cards.json',{'schema_version':'winter-fashion-research-cards/v1','cards':cards})
    dump('candidate-proposals.json',{'schema_version':'winter-fashion-candidate-drafts/v1','runtime_ready':False,
        'count_note':'Clause drafts include optional bundle clauses. Neither count is a count of new runtime candidates.', 'proposals':proposals})
    dump('term-plan.json',{'schema_version':'winter-fashion-term-plan/v1','terms':term_plan})
    fields=['id','group','source_term','en','card_ids','priority','meaning_kind','planned_action_ko','source_ids','existing_ids_to_review','candidate_mention_count','profile_mention_count','source_scope','record_equivalence','runtime_ready']
    with (HERE/'term-plan.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for t in term_plan:w.writerow({k:';'.join(t[k]) if isinstance(t[k],list) else t[k] for k in fields})
    supplement=json.loads((HERE/'reference-supplement.json').read_text())
    dump('regression-plan.json',{'schema_version':'winter-fashion-regression-plan/v1','comparison_pairs':pairs,
        'mutation_cases':mutations,'native_render_groups':render_groups,'body_region_queries':supplement['body_region_index'],
        'outfit_examples':supplement['outfit_examples'],'all_cases_executed':False,
        'baseline_rule':'Use frozen identical requester/core constraints. New diagnostics do not prove the original hidden or occluded request.'})
    packages=[
        dict(id='WP1',name='원료·니트·파일·충전·레그웨어 표면',cards=[f'WF{i:02d}' for i in range(4,23)]+['WF58','WF59','WF60'],
             targets=['photo_prompt_textile_surface_extension.json','photo_prompt_visual_obligations_textile_surface.json'],
             rule='기존 리브·케이블·퀼팅·시어 ID 동등성 검토 먼저; 배플·작은 구멍·뒷면·겹층 변형만 보강'),
        dict(id='WP2',name='코트·상의·핏·네크라인·개구·소매',cards=[f'WF{i:02d}' for i in range(23,58)]+['WF70'],
             targets=['photo_prompt_clothing_structure_extension.json','photo_prompt_visual_obligations_clothing_structure.json',
                      'photo_prompt_fashion_fit_extension.json','photo_prompt_visual_obligations_fashion_fit.json',
                      'photo_prompt_portrait_fashion_exposure_extension.json','photo_prompt_visual_obligations_portrait_fashion_exposure.json'],
             rule='핏 축·현재 가시 상태·여밈 보유·개방을 분리; 성인 범위와 기존 의미를 유지'),
        dict(id='WP3',name='레그웨어·부츠·겨울 액세서리·장식',cards=[f'WF{i:02d}' for i in range(61,70)]+['WF71'],
             targets=['photo_prompt_accessory_structure_extension.json','photo_prompt_visual_obligations_accessory_structure.json',
                      'photo_prompt_ornament_structure_extension.json','photo_prompt_visual_obligations_ornament_structure.json'],
             rule='독립 소유자와 지지·부착 경로; 썸홀·가터 기존 후보의 전체 효과 범위 검토'),
        dict(id='WP4',name='겨울 스타일 선택 조합',cards=[f'WF{i:02d}' for i in range(72,78)],
             targets=['photo_prompt_subculture_appearance_extension.json','photo_prompt_visual_obligations_subculture_appearance.json',
                      'photo_prompt_y2k_extension.json','photo_prompt_visual_obligations_y2k.json','photo_prompt_sensual_fetish_fashion_extension.json'],
             rule='기존 하위 미감의 ID를 유지; 22 라벨을 고정 의상 또는 인물 정체성으로 복제하지 않음'),
        dict(id='WP5',name='층·노출 구간·복수 의복 조합',cards=['WF01','WF47','WF52','WF78','WF79'],
             targets=['existing candidate_bundles and owner-bound wardrobe relations',
                      'photo_prompt_winter_fashion_extension.json (conditional proposal)',
                      'photo_prompt_visual_obligations_winter_fashion.json (conditional proposal)'],
             rule='기존 가족으로 표현이 충분하면 새 겨울 파일을 만들지 않음; 새 파일은 독립 겨울 관계가 남을 때만 manifest 등록')]
    phases=[
        dict(id='P0',name='원본 재확인과 동등성 결정',depends_on=[],outputs=['fresh hashes and relevant dirty-work inventory','term by term semantic disposition','selected variant/effect inventory'],
             exit_criteria=['read original positive semantics, owner, relation ends and scope','classify reuse / equivalent alias / narrowed successor / new variant / specification / source follow-up','do not equate phrase absence with missing semantics']),
        dict(id='P1',name='원본 데이터 작성',depends_on=['P0'],outputs=['selected extension entries','authored_components profiles','optional bundle clauses'],
             exit_criteria=['same garment endpoints and all effects explicit','existing IDs and historical baselines retained','valid current effect schema and optional post-core activation','authored_components v1 for single duties; v2 for coupled component evidence; no generated profile fields authored']),
        dict(id='P2',name='파생 인덱스와 원본 검증',depends_on=['P1'],outputs=['manifest updates only for new files','semantic BM25F/index','visual profile index','verified runtime generation'],
             exit_criteria=['vectors reused only for identical text/provider/model/dimensions','new or changed text vectors separately accounted','complete source, bundle and index validation before publication','keep old generation/receipts and avoid rewriting CURRENT by hand']),
        dict(id='P3',name='검색·선택·구성 회귀',depends_on=['P2'],outputs=['304 term coverage receipt','15 body query and 10 original outfit receipts','56 pair and 12 mutation results'],
             exit_criteria=['prove semantic lookup separately from slot exposure and explicit selection','native Korean/English and synonyms tested in actual requester context','same non-target intent locks and owner preserved','full clauses reviewed for camera, body and unselected wardrobe effects']),
        dict(id='P4',name='별도 생성 단계의 픽셀 자격 확인',depends_on=['P3'],outputs=['16 diagnostic groups selected by need','native per-gate evidence','original-request coverage results','user acceptance status'],
             exit_criteria=['all activated visible gates on same owner pass','unobservable/partial evidence does not pass','hidden facts have separate evidence','moderation block has no scored pixels','diagnostic alternative never replaces original request proof']),
        dict(id='P5',name='검토 가능한 반영 전달',depends_on=['P3','P4'],outputs=['scoped diff','validation matrix','adopted/deferred term map','publication receipts if later requested'],
             exit_criteria=['document authored/index/retrieval/selection/audit/pixel/user layers separately','preserve concurrent unrelated changes','do not label all data pixel-qualified if only some variants were tested'])]
    dump('implementation-plan.json',{'schema_version':'winter-fashion-implementation-plan/v1','runtime_changes_executed':False,
        'objective':'Owner-bound visible distinctions and optional candidates retained through lookup, selection, composition and appropriate evidence gates.',
        'packages':packages,'phases':phases,'current_contract_references':['references/maintenance.md','scripts/photo_source_manifest.py',
        'scripts/photo_candidate_semantics.py','scripts/visual_profile_contracts.py'],
        'proposed_validation_targets':['tests/test_photo_clothing_terminology_semantics.py','tests/test_photo_textile_opacity_effect_scope.py',
        'tests/test_photo_fashion_fit_semantics.py','tests/test_photo_portrait_fashion_exposure.py','tests/test_photo_visual_profile_retrieval.py',
        'tests/test_photo_winter_fashion_semantics.py (new only for meaningful new behavior)'],
        'deferred_source_checks':['Angora rabbit term-specific primary fibre reference','selected dolman/batwing and coat variant diagrams',
        'sideboob/underboob direct terminology source','selected hold-up silicone or skort/bodysuit hidden topology','every selected historical or commercial variant before hard promotion'],
        'change_boundary':'Research-only now. No runtime source, manifest, index, SKILL.md, controls, precore resolver, generation workflow or historical fixture edits in this request.'})
    md=['# 겨울 패션 시각 의미 카드','', '가족 수준 리서치와 후보 초안이다. 변형은 대안이며 전체를 한 의무로 활성화하지 않는다. 직접 출처의 사실 범위와 연구자의 그래프·문장 제안을 구분한다.','']
    for c in cards:
        r=c['relation_example'];refs=', '.join(f"[{sid}: {source_by_id[sid]['issuer']}]({source_by_id[sid]['url']})" for sid in c['source_ids'])
        md += [f"## {c['id']} — {c['title_ko']} ({c['priority']})",'',c['meaning_ko'],'',
               f"- 소유자: {c['owner_ko']}",f"- 관계 예: `{r['subject']} → {r['predicate']} → {r['object']}`. {r['binding_ko']}",
               f"- 속성 후보 풀: {', '.join(c['proposed_property_suffixes'])}. 선택 변형별로 범위를 다시 좁혀야 한다.",
               f"- 혼동 경계: {c['confusion_boundary_ko']}",f"- 관찰 조건: {c['observation_prerequisites_ko']}",
               f"- 기존 ID 검토: {', '.join(c['existing_ids_to_review']) or '용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요'}",f"- 근거: {refs}",'']
        if c['independent_clauses_en']:
            md += ['각각 독립된 선택형 문장 초안:','']+[f"{i}. {s}" for i,s in enumerate(c['independent_clauses_en'],1)]+['']
        else:md += ['비시각 명세다. 자동 시각 후보를 작성하지 않는다.','']
    (HERE/'semantic-cards.md').write_text('\n'.join(md)+'\n')
    assert len(sources)==46 and len(term_plan)==304 and len(pairs)==56 and len(render_groups)==16
    assert len({p['id'] for p in proposals})==len(proposals)
    assert all(p['proposed_slot'] in {'wardrobe_style','surface_material','garment_detail'} for p in proposals)
    assert all(k in card_by_id for t in term_plan for k in t['card_ids'])
    assert all(k in card_by_id for p in pairs for k in p['card_ids'])
    assert all(k in card_by_id for g in render_groups for k in g['card_ids'])
    assert all(k in card_by_id for rows in [supplement['body_region_index'],supplement['outfit_examples']] for row in rows for k in row['cards'])
    with (HERE/'term-plan.csv').open() as f: csv_rows=list(csv.DictReader(f))
    assert len(csv_rows)==len(term_plan) and [r['id'] for r in csv_rows]==[t['id'] for t in term_plan]
    for row,t in zip(csv_rows,term_plan):
        for k in fields:
            expected=';'.join(t[k]) if isinstance(t[k],list) else str(t[k])
            assert row[k]==expected,(t['id'],k)
    summary={'status':'PASS_research_integrity_only','vocabulary_terms':304,'vocabulary_tables':18,'main_sections':15,
        'sources':len(sources),'semantic_cards':len(cards),'relation_examples':len(relations),
        'clause_drafts':len(proposals),'selected_visible_variant_drafts':sum(p['proposal_kind']=='selected_visible_variant_clause' for p in proposals),
        'optional_bundle_clause_drafts':sum(p['proposal_kind']=='optional_bundle_clause' for p in proposals),
        'comparison_pairs':len(pairs),'mutation_cases':len(mutations),'native_render_groups':len(render_groups),
        'body_query_rows':15,'original_outfit_rows':10,'card_priorities':dict(collections.Counter(c['priority'] for c in cards)),
        'handling_kinds':dict(collections.Counter(t['meaning_kind'] for t in term_plan)),
        'terms_with_candidate_mentions':sum(t['candidate_mention_count']>0 for t in term_plan),
        'terms_with_profile_mentions':sum(t['profile_mention_count']>0 for t in term_plan),
        'source_stable_during_load':not snapshot['changed_during_load'],
        'evidence_limit':'Schema/link/id/count checks validate research artifacts only; no runtime registration, index rebuilding, actual retrieval, selection or pixels.',
        'embedding_calls':0,'image_calls':0,'runtime_changes_executed':False}
    dump('research-validation.json',summary);print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__':main()
