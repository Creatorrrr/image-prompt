"""Build and validate research-only tables; never edits runtime data or indexes."""
from __future__ import annotations

import collections
import csv
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def read(name):
    return json.loads((HERE / name).read_text())


def dump(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    inventory = read('term-inventory.json')['terms']
    cards = read('semantic-cards.json')['cards']
    sources = read('sources.json')['sources'] + read('supplemental-sources.json')['sources']
    records = read('current-positive-records.json')
    source_map = {s['id']: s for s in sources}
    term_map = {t['ko']: t for t in inventory}
    card_map = {c['id']: c for c in cards}
    owner = {}
    assert len(term_map) == len(inventory) == 347
    assert len(source_map) == len(sources)
    assert len(card_map) == len(cards) == 113
    observed_paths = {p['property'] for c in records['candidates'] for p in c.get('affected_properties', [])}
    for card in cards:
        assert set(card['source_ids']) <= source_map.keys(), card['id']
        assert card['visible_components_ko'] and card['confusion_boundaries_ko']
        assert card['definition_ko'] and card['claim_limits_ko']
        for seed in card['seed_ko']:
            assert seed in term_map, (card['id'], seed)
            assert seed not in owner, (seed, owner.get(seed), card['id'])
            owner[seed] = card['id']
    assert set(owner) == set(term_map), sorted(set(term_map) - set(owner))
    plan = []
    for term in inventory:
        card = card_map[owner[term['ko']]]
        mentions = term['positive_field_mentions']
        if 'metadata' in card['kind']:
            decision = 'retain_specification_and_separate_observable_proxy'
        elif any(mentions.values()):
            decision = 'review_existing_equivalence_then_reuse_or_extend'
        else:
            decision = 'inspect_equivalent_structure_then_add_distinct_variant_only_if_needed'
        plan.append({'term_id': term['id'], 'source_term': term['source_term'], 'section': term['section'],
            'card_id': card['id'], 'priority': card['priority'], 'decision': decision,
            'meaning_class': card['kind'], 'source_ids': card['source_ids'],
            'candidate_neighbor_ids': [h['id'] for h in mentions['candidates']],
            'profile_neighbor_ids': [h['id'] for h in mentions['profiles']],
            'neighbor_authority': 'lexical_only; exact record meaning must be reviewed',
            'property_paths_proposal': card['property_paths_proposal'],
            'entry_count_committed': 0,
            'before_promotion': ['Verify this term-specific definition and modern variants against an appropriate product/pattern source.',
                'Compare garment owner, body region, layer, prerequisites and complete effects with each existing record.',
                'Add an equivalent alias only when the entire current meaning remains equivalent; split other variants.',
                'Do not index counterexamples, source prose or invisible claims as positive semantics.',
                'Bind exact selected components and native-image visibility gates independently of family aliases.']})
    dump('term-plan.json', {'status': 'research_only_not_runtime_changes', 'terms': plan})
    csv_fields = ['term_id','section','source_term','card_id','priority','meaning_class','decision','source_ids',
        'candidate_neighbor_ids','profile_neighbor_ids','property_paths_proposal']
    with (HERE / 'term-plan.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=csv_fields)
        writer.writeheader()
        for row in plan:
            writer.writerow({k: ';'.join(row[k]) if isinstance(row[k],list) else row[k] for k in csv_fields})
    candidates = []
    for card in cards:
        neighbors = {kind: sorted({h['id'] for seed in card['seed_ko']
            for h in term_map[seed]['positive_field_mentions'][kind]}) for kind in ['candidates','profiles']}
        for i, draft in enumerate(card['drafts'],1):
            phrase = draft['phrase_en']
            assert len(phrase.split()) >= 9 and not re.search(r'\{.+\}|TODO|placeholder',phrase), phrase
            assert all(draft['relation'][key].strip() for key in ['type','subject','object'])
            slot = 'wardrobe_style' if card['kind']=='style_family' else (
                'surface_material' if 69 <= int(card['id'][3:]) <= 85 else 'garment_detail')
            candidates.append({'id': f"af_{card['id'].lower()}_v{i}_draft", 'card_id':card['id'],
                'status':'research_draft_not_loadable_runtime_source', 'slot_proposal':slot,
                'priority':card['priority'], 'phrase_en':phrase, 'concept_units_proposal':[phrase],
                'relation_proposal':draft['relation'], 'relation_type_status':'proposed_name_requires_current_contract_review',
                'same_owner_binding':card['owner_binding'],
                'property_scope_candidates':[{'target':'main_subject','property':p,
                    'current_positive_record_uses_path':p in observed_paths} for p in card['property_paths_proposal']],
                'effect_scope_status':'family-scope review inputs; exact per-variant affected_properties must be authored before promotion',
                'complete_effect_review':['List every garment, color, material, opening and layer introduced by this literal phrase.',
                    'Retain effects on one wardrobe under appearance/material consistently; changing a carrier does not bypass a property lock.',
                    'Do not import every family property or every alternative as a duty for this one variant.'],
                'applicability':['Same named wearer and garment owner, including every stated inner/outer garment.',
                    'Every actual affected property is open or explicitly supports this exact requester-owned meaning.',
                    'Required view, scale and body landmarks are visible without contradicting locked framing or pose.',
                    'If a required owner/view is absent, decline or author within permitted open scope; do not pretend it is present.'],
                'source_ids':card['source_ids'], 'lexical_neighbors_for_review':neighbors,
                'native_review_contract':{'positive_realization':phrase,
                    'selected_variant_evidence':[{'id':'selected_literal_realization','statement_en':phrase,
                        'duty':'Review every feature asserted by this selected literal realization, including both relation endpoints.'}],
                    'family_axes_for_review_only':card['visible_components_ko'],
                    'family_axis_authority':'Advisory review menu only. Sibling variant axes are not active all-of gates.',
                    'relation_subject':draft['relation']['subject'], 'relation_object':draft['relation']['object'],
                    'owner_gate':'Same declared garment(s)/wearer; no swapped owner or merged garments.',
                    'relation_gate':'Both endpoints and their declared physical relation are discernible in one saved native image.',
                    'visibility_gate':'Occluded, cropped, tiny or partial evidence is not a PASS for an active required feature.',
                    'confusion_gate':card['confusion_boundaries_ko'],
                    'claim_limits':card['claim_limits_ko'],
                    'status':'not_executed; future adopted variant needs its own exact all-of gates'}})
    assert len({c['id'] for c in candidates}) == len(candidates) == 129
    dump('candidate-proposals.json', {'schema_version':'autumn-fashion-candidate-research/v1',
        'runtime_ready':False, 'candidate_count_is_not_new_entry_count':True, 'candidates':candidates})
    markdown = ['# 가을 패션 상세 의미 카드', '',
        '113개 의미군과 129개 가시 구현 초안. 카드 안의 여러 이름·문장은 독립 선택지이며 동시에 필요한 조건 목록이 아니다.',
        '정의는 원문과 공개 근거를 대조한 연구자의 종합이다. 출처가 용어의 모든 현대 변형·별칭을 각각 검증했다는 뜻은 아니다.',
        '관찰 구성·후보 문장·혼동 검사·속성 경로는 반영 설계다. 구조 검사 성공이 라이브 검색이나 이미지 성공을 증명하지 않는다.', '']
    for card in cards:
        markdown += [f"## {card['id']} — {card['title']}", '',
            f"- 원문 범위: {' / '.join(card['seed_ko'] or card.get('supplemental_terms_ko',[]))}",
            f"- 우선순위 / 유형: {card['priority']} / {card['kind']}",
            f"- 뜻과 축: {card['definition_ko']}",
            f"- 소유자: {card['owner_binding']}",
            f"- 관찰 단서: {'; '.join(card['visible_components_ko'])}",
            f"- 혼동 경계: {'; '.join(card['confusion_boundaries_ko'])}",
            f"- 주장 한계: {card['claim_limits_ko']}",
            f"- 부분 속성 제안: {', '.join(card['property_paths_proposal'])}"]
        members = [t for t in plan if t['card_id']==card['id']]
        cids = sorted({x for t in members for x in t['candidate_neighbor_ids']})
        pids = sorted({x for t in members for x in t['profile_neighbor_ids']})
        markdown += [f"- 현 후보 이웃(표현 대조, 의미 보증 아님): {', '.join(cids[:12]) or '해당 씨앗 표현의 이웃 없음'}",
            f"- 현 프로필 이웃(표현 대조): {', '.join(pids[:12]) or '해당 씨앗 표현의 이웃 없음'}",'']
        if card['drafts']:
            for i,d in enumerate(card['drafts'],1):
                markdown += [f"**독립 구현 {i}:** {d['phrase_en']}", '',
                    f"관계: `{d['relation']['subject']}` → `{d['relation']['object']}` ({d['relation']['type']}, 유형명은 초안).",
                    '필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.', '']
        else:
            markdown += ['이 카드는 명세/용어 메타데이터다. 숨은 기원·수치·가격을 픽셀 프로필로 자동 승격하지 않는다.', '']
        markdown += ['출처: ' + ', '.join(f"[{s}: {source_map[s]['title']}]({source_map[s]['url']})" for s in card['source_ids']), '']
    (HERE / 'semantic-cards.md').write_text('\n'.join(markdown)+'\n')
    source_lines = ['# 가을 패션 출처 원장', '',
        '출처의 확인한 사실, 연구자의 가시 구현 추론, 승격 전 확인 조건을 구분한다. 검색 제공 본문과 직접 열린 페이지를 같은 접근 수준으로 표현하지 않는다.', '']
    for source in sources:
        source_lines += [f"## {source['id']} — {source['title']}", '',
            f"[원문]({source['url']})", '',
            f"- 종류 / 접근: {source['kind']} / {source['access']}",
            f"- 확인 범위: {source['source_supported_fact']}",
            f"- 한계: {source['limits']}", '']
    (HERE / 'sources.md').write_text('\n'.join(source_lines)+'\n')
    summary = {'integrity':'PASS','scope':'research artifact structure and exact seed ownership only',
        'terms':len(plan),'cards':len(cards),'candidate_drafts':len(candidates),'sources':len(sources),
        'term_priority_counts':dict(collections.Counter(t['priority'] for t in plan)),
        'term_decision_counts':dict(collections.Counter(t['decision'] for t in plan)),
        'unmapped_terms':[], 'duplicate_term_owners':[],
        'proposed_property_paths_not_in_selected_current_records':sorted({p for c in cards for p in c['property_paths_proposal'] if p not in observed_paths}),
        'runtime_assets_modified':False,'runtime_registration_executed':False,'index_rebuild_executed':False,
        'live_retrieval_executed':False,'embedding_calls':0,'image_calls':0,'pixel_review_executed':False,
        'source_fact_sufficiency':'claim-by-claim review still required for direct promotion; not 347 independent primary-source definitions'}
    dump('research-validation.json',summary)
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':
    main()
