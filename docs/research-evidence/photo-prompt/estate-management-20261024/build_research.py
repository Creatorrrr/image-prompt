#!/usr/bin/env python3
"""Build research-only JSON/Markdown from authored records. No asset writes."""
from __future__ import annotations
import collections, datetime, hashlib, json, pathlib, re, subprocess, sys
sys.dont_write_bytecode=True

HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(HERE))
from reference_inventory import SECTIONS
from research_sources import SOURCES
from research_cards import VISUAL, CONTEXT

def digest(v):
    b=v if isinstance(v,bytes) else json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
    return hashlib.sha256(b).hexdigest()
def write(name,value):
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

SCENE_MAP={
 '가난한 변경 영주의 첫 시찰':['A01','A05','E04','G06','K03','K06'],
 '유능한 여성 영주의 재정 개혁':['B01','B02','B06','E03','K02','K05'],
 '대규모 관개공사':['A03','A04','A05','E06'],
 '부유한 상업도시의 영주':['C07','C08','B05','F01','K02','K07'],
 '봉신의 충성 의례':['E01','E02','K02','K08'],
 '포위된 성의 마지막 회의':['D08','E06','G01','G02','K06'],
 '정략혼 연회와 비밀 협상':['D01','K09','K10','K12','K17'],
 '성인 인물의 사적인 착의 장면':['F08','K10','K12','K17'],
 '폭정에 대한 공개 청원':['E03','B01','K05','K15'],
 '전쟁 후 영지 재건':['A05','C08','E07','E08','K06','K16'],
}
rows=[]
for n,(title,labels) in enumerate(SECTIONS,1):
    for i,label in enumerate(labels.split('|'),1):
        # Links are review navigation only. Partial substring matches never establish
        # exact definition support or full coverage of compound labels.
        v=[c['id'] for c in VISUAL if any(t in label for t in c['terms'])]
        k=[c['id'] for c in CONTEXT if any(t in label for t in c['terms'])]
        # A worn gauntlet is not the requested removal action. Keep it only as
        # a contrast reference rather than a positive navigation result.
        contrast=[]
        if label.startswith('건틀릿 벗기'):
            contrast=v;v=[]
        if n==20: v=[x for x in SCENE_MAP[label] if not x.startswith('K')];k=[x for x in SCENE_MAP[label] if x.startswith('K')]
        state='bounded_visual_and_context' if v and k else 'bounded_visual' if v else 'context_only' if k else 'retained_definition_deferred'
        rows.append(dict(row_id=f'S{n:02}R{i:02}',section=n,section_title=title,original_label=label,
            visual_card_ids=v,context_card_ids=k,contrast_card_ids=contrast,disposition=state,
            exact_definition_verified=False,compound_label_fully_covered=False,
            route_authority='review_navigation_only_not_semantic_match',
            next_action='Review exact term and split compound label before runtime registration; linked cards are bounded realizations, not a definition certificate.'))
write('reference-inventory.json',dict(schema='estate-reference-inventory/v1',
    conversation_id='6adb6fa8-75e8-83ee-b793-434d3667a266',title='영지물 용어 정리',
    read_thread_limit=20000,chrome_full_main_text_characters=27655,section_count=20,row_count=len(rows),
    chrome_counts=[14,15,20,17,19,18,22,18,18,22,20,22,18,23,17,16,24,32,9,10],
    capture='All 20 sections and every table were read in authenticated Chrome through CUA DOM. First-column labels transcribed; not a byte-exact full-conversation archive.',rows=rows))
write('sources.json',dict(schema='estate-research-sources/v1',sources=SOURCES))
write('semantic-cards.json',dict(schema='estate-visual-research/v1',cards=VISUAL,context_diagnostics=CONTEXT))
drafts=[]
for c in VISUAL:
    drafts.append(dict(draft_id='estate_'+c['id'].lower(),card_id=c['id'],
        schema='estate-candidate-draft/v1',record_kind='proposed_visual_option',
        en=c['visible_en'],ko=c['visible_ko'],source_ids=c['source_ids'],
        components=c['components'],relations=c['relations'],
        conditions_to_review=['Independently frozen request meaning permits the complete realization.',
            'Every introduced actor, carrier, object, count, attachment and environment change needs explicit effect/permission review.',
            'The selected historical scope or declared fantasy scope is compatible with the request.',
            'All distinguishing endpoints and connecting paths can be inspected in one chosen view.'],
        effect_review=dict(status='NOT_AUTHORED_NATIVE_EFFECTS',
            note='Proposed slots are review destinations only. Never infer native dimensions/properties from these names.',
            owner_ids=[x['id'] for x in c['components']]),
        binding_proposals=[dict(slot=s,status='REVIEW_REQUIRED',role_authority=False) for s in c['proposed_slots']],
        confusion_boundary_ko=c['confusion_boundary_ko'],pixel_gates_ko=c['pixel_gates_ko'],
        canonical_candidate_id=None,native_approval=False,runtime_registration='none',
        automatic_activation=False,partial_is_fail=True,unobservable_policy='UNOBSERVABLE_NOT_PASS',
        pixel_status='NOT_RUN',source_support_scope=c['source_support_scope']))
write('candidate-drafts.json',dict(schema='estate-candidate-drafts/v1',
    warning='Research drafts are deliberately not native candidate-module records and must not be registered directly.',drafts=drafts))
write('scene-combinations.json',dict(schema='estate-scene-review/v1',scenes=[dict(
    original_scene=k,card_ids=v,status='planning_only',
    all_cards_automatically_combined=False,
    selection_rule='Choose a legible whole-scene purpose and one compatible realization per required relation. A scene label does not activate all listed cards.',
    legal_temporal_or_psychological_claims='Require declared context or separate evidence; never counted as saved-pixel pass.') for k,v in SCENE_MAP.items()]))

cases=[]
for c in VISUAL:
    cases.append(dict(id=c['id']+'-POS',card_id=c['id'],type='positive_relation',
        query_ko=c['visible_ko'],query_en=c['visible_en'],
        expected='Retrieve a compatible complete relation or flag missing; then independently audit source/role/permissions. Retrieval alone cannot pass pixels.',
        required_pixel_gates=c['pixel_gates_ko'],execution='NOT_RUN'))
    cases.append(dict(id=c['id']+'-NEG',card_id=c['id'],type='nearest_confusion',
        negative_boundary_ko=c['confusion_boundary_ko'],
        expected='Do not equate the neighbor or unobservable claim with this complete realization.',execution='NOT_RUN'))
    cases.append(dict(id=c['id']+'-OCC',card_id=c['id'],type='occlusion_or_wrong_owner',
        input_rule='Hide one endpoint or attach a named part to a different actor/object.',
        expected='UNOBSERVABLE_NOT_PASS for hidden evidence; FAIL for wrong-owner or contradictory visible evidence. Never whole-scene PASS from partial evidence.',execution='NOT_RUN'))
controls=[
 ('CTL01','현대 사무실에서 계약서를 받는 사람','No mandatory castle, medieval costume, coin, lord or vassal.'),
 ('CTL02','박물관에 전시한 파니에 받침','Do not introduce a human wearer merely from a human-only binding; inspect actual role applicability.'),
 ('CTL03','손을 맞잡은 두 연인','Do not convert to homage or legal vassalage.'),
 ('CTL04','현대 제분 공장의 수차 모형','Do not infer medieval setting, functioning mill or rent.'),
 ('CTL05','천 코이프를 쓴 제빵사','Do not introduce metal mail coif.'),
 ('CTL06','허리에 바느질한 드레스의 보디스','Do not force a separate stays/corset layer.'),
 ('CTL07','서양풍 영지에 관개를 설치하는 골렘','Fantasy proposal permitted only within declared request, never historical evidence.'),
 ('CTL08','검지장 옆 창고의 쌀 포대','Do not equate assessed kokudaka and current rice inventory.'),
 ('CTL09','성인의 사적 착의와 넥라인','Do not infer sexual service, consent, coercion or feudal first-night right.'),
 ('CTL10','영지물 풍경, 사람 없음','Do not automatically insert lord, clerk, laborers or human-specific role bindings.'),
 ('CTL11','반쯤 내려온 격자문','Portcullis may fit; do not add drawbridge or moving-state proof.'),
 ('CTL12','영지의 세 구획 밭','Do not count crop rotation or three-field chronology as proven.'),
]
cases.extend(dict(id=i,type='control',query_ko=q,expected=e,execution='NOT_RUN') for i,q,e in controls)
write('regression-cases.json',dict(schema='estate-research-evaluation/v1',cases=cases))

status=subprocess.check_output(['git','status','--porcelain=v1','-z'],cwd=ROOT)
entries=[x.decode(errors='replace') for x in status.split(b'\0') if x]
asset_dir=ROOT/'skills/photo-prompt-image-generator/assets'
manifest_path=asset_dir/'photo_candidate_corpus_manifest.json'
manifest=json.loads(manifest_path.read_text())
catalog_path=asset_dir/'photo_candidate_slot_catalog.json'
catalog=json.loads(catalog_path.read_text())['slot_catalog']
proposed={s for c in VISUAL for s in c['proposed_slots']}
assert proposed<=set(catalog), f'Unknown proposed roles {proposed-set(catalog)}'
baseline=dict(snapshot_time_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    snapshot_date_for_user='2026-10-24 Asia/Seoul',head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
    source_manifest_schema=manifest['schema'],source_module_count=len(manifest['modules']),
    source_manifest_sha256=digest(manifest_path.read_bytes()),slot_catalog_sha256=digest(catalog_path.read_bytes()),
    slot_count=len(catalog),git_status_counts=dict(collections.Counter(e[:2] for e in entries)),
    git_status_sha256=digest(status),operating_assets_modified_by_this_research=False,
    source_modules=[dict(**m,sha256=digest((asset_dir/m['file']).read_bytes())) for m in manifest['modules']])
protected={}
for entry in entries:
    code,path=entry[:2],entry[3:]
    if code=='??' or code==' D':continue
    f=ROOT/path
    if f.is_file():protected[path]=digest(f.read_bytes())
baseline['existing_dirty_tracked_file_hashes']=protected
if not (HERE/'BASELINE.json').exists():write('BASELINE.json',baseline)

# Audit direct positive fields, excluding aliases, keyword routes, research metadata,
# activation dictionaries, provenance and conditions. This avoids a metadata-only
# mention masquerading as a candidate realization.
patterns={
 'estate_land':r'장원|직영지|\bmanor(?:ial)?\b|\bdemesne\b',
 'agri_logistics':r'관개|곡물|곡창|제분|\birrigation\b|\bgrain\b|\bgristmill\b',
 'fiscal_admin':r'제분료|지대명부|토지대장|\bmulture\b|\btally\b|\brent roll\b',
 'homage_fealty':r'봉신예|충성선서|\bhomage\b|\bfealty\b',
 'waterwheel':r'(?<![가-힣])수차|\bwaterwheel\b|\bwater wheel\b',
 'portcullis':r'포트컬리스|\bportcullis\b',
 'pannier':r'파니에|\bpanniers?\b',
 'brigandine':r'브리건딘|\bbrigandine\b',
 'early15c_dress':r'우플랑드|키르틀|\bhouppelande\b|\bkirtle\b',
 'east_asia_land':r'검지장|석고제|\bkokudaka\b|\bkenchi\b',
}
compiled={k:re.compile(v,re.I) for k,v in patterns.items()}
positive_keys={'en','ko','phrase_en','phrase_ko','embedding_text','concept_units','definition'}
def positives(content,path='content'):
    found=[]
    if not isinstance(content,dict):return found
    for k,v in content.items():
        if k in positive_keys:
            if isinstance(v,str):found.append((path+'.'+k,v))
            elif isinstance(v,list):found.extend((path+'.'+k+f'[{i}]',s) for i,s in enumerate(v) if isinstance(s,str))
        elif k=='realizations':
            it=v.items() if isinstance(v,dict) else enumerate(v) if isinstance(v,list) else []
            for rid,r in it:
                if isinstance(r,dict):found.extend(positives(r,path+f'.realizations.{rid}'));found.extend(positives(r.get('content',{}),path+f'.realizations.{rid}.content'))
    return found
hits=[];count=0
for m in manifest['modules']:
    if m['kind']!='candidates':continue
    data=json.loads((asset_dir/m['file']).read_text())['candidates']
    it=data.items() if isinstance(data,dict) else [(x['id'],x) for x in data]
    for cid,c in it:
        count+=1;fields=positives(c.get('content',{}));matches=[]
        for topic,pattern in compiled.items():
            fields_hit=[dict(pointer=p,text=s) for p,s in fields if pattern.search(s)]
            if fields_hit:matches.append(dict(topic=topic,positive_fields=fields_hit))
        if matches:hits.append(dict(candidate_id=cid,module=m['file'],record_kind=c.get('record_kind'),
            canonical_sha256=digest(c),matches=matches,conditions=c.get('conditions',{}),effects=c.get('effects',{}),
            disposition='lexical_positive_hit_requires_full_source_and_role_review'))
manual_specs=[
 ('photo_candidate_candidates_004.json','cand_1bd324372fab529e83751368b01edd9c',['A03','B01','B06','E06'],'review_existing_compound',
  '이미 토지대장·측량줄·수로 모형·임금 장부·곡물 용기 묶음이 있다. 각 물건의 소유·실무 연결은 부족하고 primary tag 조건이 있다. 기존 묶음은 보존하고 개별 관계로 보완 검토. 빈 effects는 자유로운 무조건 추가의 권한이 아니다.'),
 ('photo_candidate_candidates_009.json','cand_8f33f22aa0de5e3dbb8815b70d686d3e',['D02'],'reuse_after_bilingual_and_role_review',
  '영문에 문·수직 홈·성문 공간의 완전 관계가 있고 한국어는 짧은 표제다. 신규 중복 전에 한영 대응과 전체 source/role 자격 검토.'),
 ('photo_candidate_candidates_001.json','cand_493311a3b926597783f631f889a05400',['D02'],'reuse_optional_view_only',
  '격자문 가장자리와 안내 홈을 보여주는 구도. 이 국소 관찰이 전체 성문·문 양쪽의 모든 gate를 대신하지 않는다.'),
 ('photo_candidate_candidates_013.json','cand_b9a6a8e1281f5d019c338b9f4e4b3198',['D02'],'inspect_existing_bundle_closure',
  '문·홈·일부 내려온 상태의 기존 bundle과 두 member가 있다. source closure·독립 요청 의미·현재 허용 범위를 검토; 낱말 검색 0건을 부재로 해석하지 않는다.'),
 ('photo_candidate_candidates_008.json','cand_dfd89db900735d9b8116fccb6c52a6d2',['F07'],'reuse_partial_relation_not_complete_support',
  '치마의 좌우 확장만 말한다. 허리 부착·받침·겉치마 지지 전체를 증명하지 않는다. 한국어 표제는 영문 전체 관계보다 짧다.'),
 ('photo_candidate_candidates_015.json','cand_22079d8d7f705caea3f446184813280f',['F07'],'reuse_partial_relation_not_complete_support',
  '좌우보다 앞뒤 깊이가 작다는 비교 관계. 위 CID와 같은 한국어 표제라도 동일한 원문 의미의 후보가 아니다.'),
 ('photo_candidate_court_palace_20261023.json','cand_a1425f8956985eaeafa7c7a7c954255a',['F07'],'prefer_full_relation_reuse_review',
  '허리 연결·옆 받침·겉치마·좌우/앞뒤 비교가 이미 있다. 원문 조건·effects·carrier를 보존해 재사용 검토; 연구 native_approval=false를 PASS로 바꾸지 않는다.'),
 ('photo_candidate_candidates_007.json','cand_74c968440a0e56b1907e181579c565b4',['F07','G06'],'keep_rococopunk_distinct',
  '부러진 파니에 보강재를 재사용 부품으로 바꾸는 로코코펑크 대안. 단순 역사 파니에나 평범한 의복 수선으로 잘라 재사용하지 않는다; 실제 primary tag 조건 유지.'),
]
manual=[]
for module,cid,card_ids,decision,rationale in manual_specs:
    c=json.loads((asset_dir/module).read_text())['candidates'][cid]
    manual.append(dict(candidate_id=cid,module=module,card_ids=card_ids,decision=decision,rationale_ko=rationale,
        canonical_sha256=digest(c),record=c,review_scope='Source meaning/conditions/effects read for research planning; bindings, native proof, live retrieval and pixels not qualified.'))
write('existing-source-mapping.json',dict(schema='estate-existing-source-audit/v1',
    snapshot_manifest_sha256=baseline['source_manifest_sha256'],candidate_count=count,
    hit_count=len(hits),search_patterns=patterns,
    counts_by_topic={k:sum(any(m['topic']==k for m in h['matches']) for h in hits) for k in patterns},
    method='Selected direct positive fields only, supplemented by eight full source records manually reviewed. Not semantic absence proof; excludes lexical-only tags/aliases/research metadata. No retrieval/ranking execution.',hits=hits,manual_source_reviews=manual))

stats=dict(section_count=20,reference_rows=len(rows),sources=len(SOURCES),
    sources_by_access=dict(collections.Counter(x['access'] for x in SOURCES)),
    visual_cards=len(VISUAL),context_diagnostics=len(CONTEXT),candidate_drafts=len(drafts),
    proposed_binding_pairs=sum(len(c['proposed_slots']) for c in VISUAL),
    additional_plate_review_cards=sum(c['additional_source_plate_review_required'] for c in VISUAL),
    regression_cases=len(cases),coverage_dispositions=dict(collections.Counter(x['disposition'] for x in rows)),
    exact_definition_verified_rows=0,
    corpus_candidates_scanned=count,corpus_positive_hits=len(hits),slot_count=len(catalog),
    claims='Counts are research inventories, not runtime or image qualification.')
write('research-summary.json',stats)

pending=['# 원문 항목별 후속 보강 목록','',
 '원문 행을 삭제하지 않고 보류한 목록이다. 완전 정의/도판/역할 검토가 끝났다는 뜻이 아니다.', '']
for n,title in enumerate((x[0] for x in SECTIONS),1):
    group=[r for r in rows if r['section']==n and r['disposition']=='retained_definition_deferred']
    if group:
        pending += [f'## {n}. {title}','']
        pending += [f"- {r['row_id']}: {r['original_label']}" for r in group]
        pending += ['']
pending += ['## 후속 작업 순서','',
 '1. 산업 설비와 성곽 부위: 정확한 원료·부품·출입 경로를 보여주는 시대별 유물/구조 도판.',
 '2. 생활 소품·복식 흔적·사회 지위: 물건 형상과 신분/직무 해석을 분리하는 단독 자료.',
 '3. 군제·전쟁·협상: 급료·계약·동원·지휘와 보이는 장비를 분리하는 지역별 연구.',
 '4. 포즈·행동: 동작의 물리 관계를 먼저 쓰고, 시대별 예법·권력·정서 해석은 별도 출처로 검토.',
 '5. 문맥 카드에 연결된 민감한 제도: 각 지역·시대의 정의와 주장 한계를 별도 확보. 문맥 연결만으로 exact definition 확인 처리하지 않음.','']
(HERE/'FOLLOWUP-BACKLOG.md').write_text('\n'.join(pending))

lines=['# 영지물 시각 의미 카드 상세','',
 '모든 장면은 출처의 개념 구분을 바탕으로 저술한 선택형 제안이다. 역사 장면의 완전 재현, native 자격, 검색 노출, 생성 픽셀 검증은 아직 수행하지 않았다.','']
src={x['id']:x for x in SOURCES}
for c in VISUAL:
    lines += [f"## {c['id']} — {' / '.join(c['terms'])}",'',f"범위: {c['scope']}",'',
        c['visible_ko'],'',c['visible_en'],'',f"혼동 경계: {c['confusion_boundary_ko']}",'',
        '관계: '+ '; '.join(f"{r['subject']} → {r['type']} → {r['object']}" for r in c['relations']), '',
        '픽셀 확인: '+ '; '.join(c['pixel_gates_ko']), '',
        '출처: '+', '.join(f"[{i}: {src[i]['title']}]({src[i]['url']})" for i in c['source_ids']), '',
        f"추가 도판 검토 필요: {c['additional_source_plate_review_required']}. 모든 도판 직접 검토 및 생성 픽셀: NOT_RUN.",'']
for c in CONTEXT:
    lines += [f"## {c['id']} — {' / '.join(c['terms'])}",'',c['distinction_ko'],'',
        '외형으로 확인되지 않는 것: '+c['not_proven_by_pixels'],'','반영: '+c['routing_ko'],'',
        '출처 범위: '+', '.join(f"[{i}]({src[i]['url']})" for i in c['source_ids']), '']
(HERE/'SEMANTIC-DETAILS.md').write_text('\n'.join(lines)+'\n')
print(json.dumps(stats,ensure_ascii=False,indent=2))
