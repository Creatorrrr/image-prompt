#!/usr/bin/env python3
"""Compile research-only records and coverage. Does not write runtime assets."""
import collections, csv, json, pathlib, re, unicodedata

HERE = pathlib.Path(__file__).resolve().parent
def read(name): return json.loads((HERE / name).read_text())
def write(name, obj): (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
def norm(s):
    s = unicodedata.normalize('NFKD', s).casefold()
    s = unicodedata.normalize('NFC', ''.join(c for c in s if not unicodedata.combining(c)))
    return ' '.join(re.sub(r'[^a-z0-9가-힣]+',' ',s).split())
def aliases(s): return [v.strip() for v in s.split('/') if v.strip()]

inventory = read('keyword-inventory.json')
audit = read('current-data-audit.json')
sources = read('sources.json')
source_by_id = {s['id']: s for s in sources['sources']}
audit_by_id = {k['keyword_id']: k for k in audit['keywords']}
records = []
for n, seed in enumerate(csv.DictReader((HERE / 'semantic-record-seeds.psv').open(), delimiter='|'), 1):
    terms = aliases(seed['terms'])
    labels = {norm(t) for t in terms + [seed['title']]}
    matched = [k for k in inventory['keywords']
               if k['section'] in seed['sections'].split(',')
               and ({norm(k['en']), norm(k['ko'])} - {''}) & labels]
    candidate_pointers = sorted({(v['slot'], v['id']) for k in matched
                                for v in audit_by_id[k['id']]['candidate_hits']})
    exact_profiles = sorted({p for k in matched for p in audit_by_id[k['id']]['exact_profile_ids']})
    section = seed['sections'].split(',')[0]
    slug = seed['slug']
    if section.startswith('4-6') or section.startswith('4-7'):
        slot, module = 'footwear', 'accessory_structure'
    elif section.startswith('4'):
        slot, module = 'wearable_accessory', 'accessory_structure'
    elif section.startswith('3-2') or section.startswith('3-3') or section.startswith('3-4'):
        slot, module = 'surface_material', 'textile_surface'
    elif section.startswith('5'):
        slot, module = 'costume_style', 'traditional_variants'
        if slug in {'norigae_attachment','hanbok_headwear','head_cover_paths'}:
            slot = 'wearable_accessory'
        elif slug in {'jeogori_parts','armour_owner_parts'}:
            slot = 'garment_detail'
    elif section.startswith('2') or section.startswith('3') or section == '6':
        slot, module = 'garment_detail', 'garment_structure'
    else:
        slot, module = 'wardrobe_style', 'garment_structure'
    ss = seed['sources'].split(',')
    assert set(ss) <= set(source_by_id)
    body = [s for s in ss if source_by_id[s]['retrieval_status'] == 'body_read']
    limited = [s for s in ss if source_by_id[s]['retrieval_status'] != 'body_read']
    support = seed['support']
    if support == 'source_expand_required':
        status = 'additional_primary_definition_required'
    elif body and support == 'direct_feature':
        status = 'source_feature_checked_design_unqualified'
    elif support == 'product_example':
        status = 'variant_example_only_design_unqualified'
    elif not body:
        status = 'limited_retrieval_design_unqualified'
    else:
        status = 'family_context_checked_design_unqualified'
    rec = {
        'id': f'CT{n:03d}', 'slug': slug, 'title_ko': seed['title'],
        'conversation_sections': seed['sections'].split(','), 'terms_for_research': terms,
        'term_scope': 'Terms are related family members or contextual senses, not an alias-equivalence assertion.',
        'owner_domain': seed['owner'], 'primary_slot_proposal': slot, 'module_proposal': module,
        'priority': seed['priority'], 'feature_pool': seed['features'].split(';'),
        'feature_pool_contract': 'Select a variant and its necessary feature subset before creating any hard profile. Features and candidate phrases can describe mutually exclusive alternatives.',
        'confusion_boundary': seed['confusion'],
        'candidate_phrase_drafts': [
            {'variant_id': f'{slug}_v{i}', 'en': p,
             'authorship': 'researcher-authored visual candidate proposal, not quotation or final runtime entry',
             'owner_domain': seed['owner'], 'affected_dimensions_proposal': ['appearance'],
             'component_subset_status': 'requires_variant_specific_authoring',
             'hard_profile_activation': 'never_from_optional_selection_alone'}
            for i,p in enumerate(seed['phrases'].split('~'), 1)],
        'visibility_view_proposal': seed['view'],
        'visibility_contract': {
            'view_is_test_design_only': True,
            'cannot_override_request_locked_composition': True,
            'required_relation_occluded': 'partial_is_fail_when_relation_is_request_required',
            'hidden_construction_or_material_provenance': 'not_pixel_verifiable_without_independent_evidence',
            'sufficient_detail_rule': 'The relevant boundary and connection must be visible at native resolution; category names and prompt text cannot substitute for pixels.'
        },
        'source_ids': ss, 'source_support': support, 'body_read_source_ids': body,
        'limited_retrieval_source_ids': limited,
        'source_scope': 'Only claims declared in sources.json are source-checked. Candidate variants, feature pools, boundaries, slot choices and gates are authored interpretation.',
        'research_status': status, 'runtime_ready': False,
        'keyword_ids_exactly_mapped': [k['id'] for k in matched],
        'existing_data_comparison': {
            'method': 'normalized exact label mapping to the lexical audit; review sense and owner before reuse',
            'possible_exact_profile_ids': exact_profiles,
            'candidate_pointer_count': len(candidate_pointers),
            'candidate_pointer_sample': [{'slot': s, 'id': i} for s,i in candidate_pointers[:12]],
            'full_pointers_location': 'current-data-audit.json, keyed by keyword_id',
            'reuse_decision': 'pending_component_and_owner_comparison',
            'no_hit_is_not_semantic_absence': True
        },
        'qualification': {k:'not_tested' for k in
            ['activation','candidate_pack_exposure','adoption','native_pixels','user_acceptance']}
    }
    records.append(rec)

record_by_id = {r['id']: r for r in records}
mapped = collections.defaultdict(list)
for r in records:
    for k in r['keyword_ids_exactly_mapped']: mapped[k].append(r['id'])
coverage_keywords = []
for k in inventory['keywords']:
    ids = mapped[k['id']]
    rstatus = [record_by_id[r]['research_status'] for r in ids]
    coverage_keywords.append({
        'keyword_id': k['id'], 'section':k['section'], 'ko':k['ko'], 'en':k['en'],
        'research_record_ids':ids,
        'coverage_status': 'specific_record_draft' if ids else 'family_scope_only_definition_backlog',
        'source_feature_directly_checked': any(s=='source_feature_checked_design_unqualified' for s in rstatus),
        'current_lexical_status': audit_by_id[k['id']]['status'],
        'runtime_qualification':'not_tested'
    })
family_rows=[]
for sec, sv in inventory['sections'].items():
    rr=[r for r in records if sec in r['conversation_sections']]
    kk=[k for k in coverage_keywords if k['section']==sec]
    family_rows.append({
        'section':sec,'name':sv['name'],'seed_terms':len(kk),
        'record_ids':[r['id'] for r in rr], 'record_count':len(rr),
        'specific_keyword_mappings':sum(bool(k['research_record_ids']) for k in kk),
        'definition_backlog_keywords':[k['keyword_id'] for k in kk if not k['research_record_ids']],
        'direct_source_feature_records':[r['id'] for r in rr if r['source_support']=='direct_feature'],
        'scope_covered':bool(rr),'all_terms_source_verified':False,'all_terms_runtime_qualified':False
    })
counts={
    'records':len(records),'candidate_phrase_drafts':sum(len(r['candidate_phrase_drafts']) for r in records),
    'inventory_rows':len(coverage_keywords),'unique_normalized_labels':len({k['normalized_term'] for k in inventory['keywords']}),
    'specific_keyword_mappings':sum(bool(k['research_record_ids']) for k in coverage_keywords),
    'definition_backlog_rows':sum(not k['research_record_ids'] for k in coverage_keywords),
    'source_feature_direct_keyword_mappings':sum(k['source_feature_directly_checked'] for k in coverage_keywords),
    'source_count':len(source_by_id),'source_retrieval_status':dict(collections.Counter(s['retrieval_status'] for s in source_by_id.values())),
    'record_status':dict(collections.Counter(r['research_status'] for r in records)),
    'priority':dict(collections.Counter(r['priority'] for r in records)),
    'modules':dict(collections.Counter(r['module_proposal'] for r in records))
}
write('semantic-records.json',{
    'schema_version':'clothing-visual-semantics/research-draft-v1','as_of':'2026-10-01',
    'runtime_integrated':False,
    'global_contracts':['Vocabulary families are not synonym sets.',
        'Optional candidate retrieval cannot establish a hard obligation.',
        'Fit concerns garment geometry and cannot silently change requester-locked body geometry.',
        'The source validates its limited claim; the visual expression and proposed gates are authorial interpretation.',
        'A family record is not a fully authored hard profile. Variant-specific necessary components must be selected and tested.'],
    'counts':counts,'records':records})
write('coverage-ledger.json',{'schema_version':'clothing-research-coverage/v1','counts':counts,
    'counting_note':'A specific keyword mapping is an exact contextual label association with a draft record. It is not a complete definition, alias equivalence, primary-source verification or effectiveness metric.',
    'families':family_rows,'keywords':coverage_keywords})

tick=chr(96)
md=['# 의류 시각 의미 레코드 초안','',
    '2026-10-01 · 연구 설계 자료 · 런타임 미반영 · 모든 노출/채택/픽셀 평가는 미실행.',
    '', '용어군은 동의어 묶음이 아니다. 각 레코드의 특징과 영문 후보는 대안 변형을 포함하며, 실제 반영 전에 변형별 필수 부품을 따로 작성한다.',
    '', '출처의 제한된 확인 사실은 [sources.json](sources.json)에 있으며, 아래 표현·경계·뷰·슬롯 선택은 연구자가 작성한 적용안이다.','']
for r in records:
    citations=', '.join(f"[{sid}]({source_by_id[sid]['url']})" for sid in r['source_ids'])
    md += [f"## {r['id']} — {r['title_ko']}",'',
        f"- 원문 분류: {', '.join(r['conversation_sections'])} · 우선순위: {r['priority']} · 제안 슬롯: {tick}{r['primary_slot_proposal']}{tick}",
        f"- 관련 용어: {', '.join(r['terms_for_research'])}",
        f"- 소유 대상: {tick}{r['owner_domain']}{tick} · 특징 풀: {' / '.join(r['feature_pool'])}",
        f"- 혼동 경계: {r['confusion_boundary']}",
        f"- 출처 범위: {tick}{r['source_support']}{tick} · 조사 상태: {tick}{r['research_status']}{tick} · {citations}",
        f"- 시험 뷰: {tick}{r['visibility_view_proposal']}{tick}. 원래 요청 구도를 변경할 권한은 포함하지 않는다.",
        f"- 후보 표현 A: {r['candidate_phrase_drafts'][0]['en']}",
        f"- 후보 표현 B: {r['candidate_phrase_drafts'][1]['en']}",
        f"- 기존 데이터 비교 포인터: exact profile {len(r['existing_data_comparison']['possible_exact_profile_ids'])}개 / candidate lexical {r['existing_data_comparison']['candidate_pointer_count']}개. 재사용 확정 전 의미·부위·owner 대조 필요.",'']
(HERE/'semantic-records.md').write_text('\n'.join(md)+'\n')
print(json.dumps(counts,ensure_ascii=False,indent=2))
