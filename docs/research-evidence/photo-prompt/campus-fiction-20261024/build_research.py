"""Build research artifacts only. Never imports or writes operating candidates/indexes."""
import collections
import csv
import hashlib
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]

def dump(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def norm(s):
    return re.sub(r'[^a-z0-9가-힣]', '', s.lower())

def main():
    sources = json.loads((HERE / 'sources.json').read_text())
    source_ids = {s['id'] for s in sources}
    cards = []
    with (HERE / 'cards-authored.psv').open() as f:
        for r in csv.DictReader(f, delimiter='|'):
            graph = []
            nodes = set()
            for item in r['graph'].split(';'):
                a, rel, b = item.split('>')
                nodes.update([a, b])
                graph.append({'from': a, 'relation': rel, 'to': b})
            # A_/B_/C_/D_ are authored owner namespaces, never sentence-position inference.
            for node in sorted(nodes):
                match = re.match(r'^([ABCD])_(?!and_)(.+)$', node)
                if match:
                    owner = match.group(1)
                    link = {'from': node, 'relation': 'belongs_to', 'to': owner}
                    if link not in graph:
                        graph.append(link)
                    nodes.add(owner)
            srcs = r['sources'].split(',')
            assert set(srcs) <= source_ids, r['id']
            visual = r['kind'] in ('observable', 'staged_proxy')
            cards.append({
                'id': r['id'], 'related_terms': r['terms'].split('/'), 'mode': r['kind'],
                'positive_ko': r['ko'] if visual else None,
                'positive_en': r['en'] if visual else None,
                'context_ko': None if visual else r['ko'],
                'context_en': None if visual else r['en'],
                'owner_nodes': [{'id': n, 'description': n.replace('_', ' ')} for n in sorted(nodes)],
                'owner_graph_origin': 'Explicit authored A_/B_/C_/D_ node namespaces expanded to belongs_to edges; no sentence-position owner inference.',
                'relations': graph, 'confusion_boundary': r['boundary'], 'observable_gate': r['gate'],
                'suggested_slots': r['slots'].split(','), 'source_ids': srcs,
                'source_evidence_scope': 'Read source passages establish only the claim_scope in sources.json. These exact scene/pose/garment specimens and their geometry are authored optional proposals; citations do not prove all geometry, all related term definitions or a documented occurrence.',
                'term_mapping_policy': 'Related realization or boundary, never synonym equivalence; grouped alternate structures require separate specimens before exact-term adoption.',
                'priority': 'P0' if r['id'] in {'W01','W02','W04','W23','W27','W28','S01','S03','S07','S09','S11','A13','A14','A21','A23','A25','A27','A29','A30','A32','A37','A38','P07','C02','C09','C10','C14','C15','C20'} else 'P1',
                'activation': 'optional_post_core_only' if visual else 'context_only_no_positive_candidate',
                'unobservable_policy': 'UNOBSERVABLE_NOT_PASS', 'partial_policy': 'partial_is_fail',
                'runtime_importable': False, 'native_approval': False, 'pixel_status': 'NOT_RUN',
            })
    assert len(cards) == len({c['id'] for c in cards})
    dump('semantic-cards.json', {'schema': 'campus-research-semantic-cards/v1', 'cards': cards})
    drafts = []
    for c in cards:
        if c['mode'] not in ('observable', 'staged_proxy'):
            continue
        drafts.append({
            'draft_id': 'campus_draft_' + c['id'], 'card_id': c['id'],
            'positive_en': c['positive_en'], 'positive_ko': c['positive_ko'],
            'owner_nodes': c['owner_nodes'], 'relations': c['relations'],
            'confusion_boundary': c['confusion_boundary'], 'observable_gate': c['observable_gate'],
            'suggested_slots': c['suggested_slots'], 'source_ids': c['source_ids'],
            'decision': 'reuse_refine_new_review_required', 'runtime_importable': False,
            'native_approval': False, 'pixel_status': 'NOT_RUN',
            'owner_policy': 'Map every body part/object to independently declared requester owners. Research labels create no entity, age proof, permission, identity or relationship.',
            'effects_review': 'Enumerate actual introduced/changed owners, count, clothing, contact, support, pose, setting, light, text and depicted-media properties. Suggested slots do not establish native effect permission.',
            'age_policy': 'Campus, university, NA and clothing never establish adulthood. Explicit adult subjects and independent eligibility are required for adopted adult intimate/sexual styling contexts.',
        })
    dump('candidate-drafts.json', {'schema': 'campus-research-drafts-not-native/v1', 'drafts': drafts})
    dom = json.loads((HERE / 'reference-browser.json').read_text())
    routes, examples = [], []
    category_defaults = ['C01','C02','C03','C04','C05','C03','C06','C02','C07','C08','C09','C22','C10','C19','C20','C21','C21','C09','C03','C02','C05','C03','C08','C16','C01']
    for ti, table in enumerate(dom['tables']):
        if table['precedingHeading'].startswith('16.'):
            examples = [{'id': 'EX%02d' % i, 'name': row[0], 'narrative': row[1], 'appearance_scene': row[2], 'status': 'reference_authored_example_not_external_work'} for i, row in enumerate(table['rows'][1:], 1)]
            continue
        for row in table['rows'][1:]:
            label, desc = row[:2]
            parts = [norm(x) for x in re.split(r'\s*/\s*|·|[()]', label)] + [norm(label)]
            hits = []
            for c in cards:
                terms = [norm(t) for t in c['related_terms']]
                if any(t and (t in parts or (len(t) >= 4 and any(t in p for p in parts))) for t in terms):
                    hits.append(c['id'])
            default = category_defaults[ti]
            if default not in hits:
                hits.append(default)
            direct = [cid for cid in hits if not cid.startswith('C') and cid != 'F07']
            routes.append({'id': 'K%03d' % (len(routes)+1), 'section': table['precedingHeading'],
                           'term': label, 'reference_explanation': desc, 'card_ids': hits,
                           'mapping_kind': 'related_optional_realization_and_boundary' if direct else 'context_or_temporal_boundary_only',
                           'definition_status': 'reference_retained_not_blanket_independently_verified',
                           'coverage_limit': 'Route coverage only. Any compound term may need separate structure-specific specimens and source checks. No claim of complete visual or external verification.',
                           'runtime_activation': False})
    dump('keyword-routes.json', {'schema': 'campus-research-keyword-routes/v1','routes': routes})
    dump('reference-concept-examples.json', examples)
    dump('development-cases.json', [{'id':'DEV_'+c['id'],'card_id':c['id'],'ko':c['positive_ko'] or c['context_ko'],'en':c['positive_en'] or c['context_en'],'expected_gate':c['observable_gate'],'executed':False,'independence':'derived_from_authored_cards_not_holdout'} for c in cards])
    atlas = ['# 원 대화 키워드 연결', '', '26개 표의 364개 데이터 행 중 용어 행 356개와 창작 조합 8개를 구분한다. 표 밖 17장의 혼동 경계 6개는 RESEARCH.md에서 별도 다룬다. 원 설명은 참조 대화 데이터이며 외부 검증 완료의 표지가 아니다.', '', '모든 연결은 관련 실현/경계이다. 동의어·정의 일치나 전 항목의 시각 완전성을 의미하지 않는다.', '']
    for r in routes:
        atlas += [f"- **{r['id']} {r['term']}** ({r['section']}) → {', '.join(r['card_ids'])}; {r['mapping_kind']}"]
    (HERE / 'KEYWORD-ATLAS.md').write_text('\n'.join(atlas)+'\n')
    lines = ['# 시각 의미 카드', '', '관계의 양 끝과 물리적 귀속을 보존한다. 아래 구도는 연구자가 제안한 실현이며 문헌이 모든 geometry를 증명한 것은 아니다.', '']
    for c in cards:
        lines += [f"## {c['id']} {', '.join(c['related_terms'])}", '', f"- 유형: {c['mode']} / {c['priority']}", f"- 한글: {c['positive_ko'] or c['context_ko']}", f"- English: {c['positive_en'] or c['context_en']}", '- 관계: ' + '; '.join(f"{r['from']} → {r['relation']} → {r['to']}" for r in c['relations']), f"- 혼동 경계: {c['confusion_boundary']}", f"- 관찰 게이트: {c['observable_gate']}", f"- 제안 슬롯: {', '.join(c['suggested_slots'])}; 출처: {', '.join(c['source_ids'])}", '']
    (HERE / 'VISUAL-CARDS.md').write_text('\n'.join(lines)+'\n')
    source_md=['# 출처와 확인 범위', '', '지정 문단·소장품 텍스트·색인 발췌만 조사했다. 외부 문서 전체 완독, 유물 원 이미지 픽셀 검토, 작품 전편 감상, 빈도 통계 검증을 뜻하지 않는다. 모든 접근일은 한국시간 2026-10-24이다.', '']
    for s in sources:
        source_md += [f"- **{s['id']} [{s['title']}]({s['url']})** — {s['publisher']}; `{s['access_status']}`; 문단/행 {s['passage']}. {s['claim_scope']}"]
    (HERE / 'SOURCES.md').write_text('\n'.join(source_md)+'\n')
    summary={'reference_table_rows':sum(len(t['rows'])-1 for t in dom['tables']),'glossary_routes':len(routes),'concept_examples':len(examples),'cards':len(cards),'card_modes':dict(collections.Counter(c['mode'] for c in cards)),'drafts':len(drafts),'sources':len(sources),'source_access':dict(collections.Counter(s['access_status'] for s in sources)),'development_cases':len(cards),'development_queries':2*len(cards),'executed_search_queries':0,'generated_images':0,'native_candidates_added':0}
    dump('PACKAGE-SUMMARY.json',summary)
    scan = json.loads((HERE / 'corpus-scan.json').read_text())
    existing = json.loads((HERE / 'existing-records.json').read_text())
    triage = json.loads((HERE / 'triage-authored.json').read_text())
    findings = ['# 기존 source 읽기 전용 진단', '', f"조사 snapshot HEAD: `{scan['head']}`. manifest 모듈 {scan['counts']['modules']}개, 전체 candidate {scan['counts']['candidates']:,}개, binding {scan['counts']['slot_bindings']:,}개, catalog slot {scan['counts']['slots']}개를 JSON으로 읽었다. 전체 candidate 수에는 문맥/진단 record도 포함한다. corpus native validator, actual retrieval, index closure 검증을 수행한 수치가 아니다.", '', '## 좁힌 어휘 탐색', '', 'positive content의 en/ko/phrase_en/phrase_ko와 제한된 realization 하위 필드만 탐색했다. alias·정의·주석·research metadata는 제외했다. 아래 수치는 검색엔진 결과나 의미의 유무를 뜻하지 않는다.', '', '| 패턴 | record 수 |', '|---|---:|']
    for k, v in scan['lexical'].items():
        findings.append(f'| {k} | {len(v)} |')
    findings += ['', '`dormitory` 0건이어도 기존 `cand_ff15b8efa40558cc903aaea6d86f0f4c`는 침대와 책상이 한 방에 있는 가시 구조를 이미 가진다. `lecture` 0건도 모든 강의실 관련 의미의 부재가 아니다. `critique` 패턴의 architectural은 비캠퍼스 건축에도 맞고 `aftermath`의 멍은 구멍에도 맞는다. 자동 집계로 의미 적합성이나 신규 필요성을 확정하지 않는다.', '', '## 14개 기존 후보의 원문·조건·effects·모든 binding 대조', '', '아래는 반영 전 제안이다. 원문 전체는 existing-records.json에 보존했으며 기존 provenance/qualification을 이번 조사에서 새로 인증하지 않았다.', '']
    for t in triage:
        r=existing[t['candidate_id']]
        canonical=json.dumps(r['record'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
        t['source_record_sha256']=hashlib.sha256(canonical).hexdigest()
        t['source_module']=r['module']
        t['binding_ids']=list(r['bindings'])
        findings += [f"- **{t['candidate_id']} → {t['decision_proposal']}** ({', '.join(t['card_ids'])}). {t['rationale']} 원문 모듈: `{r['module']}`; binding {len(r['bindings'])}개."]
    findings += ['', '기존 native 검증·현행 installed runtime·source와 index 일치는 재검증하지 않았다. 연구 validator가 관찰한 이후 변동은 VALIDATION.json에서 확인한다. 실제 반영 직전 최신 상태로 다시 심사한다.']
    dump('existing-source-triage.json',triage)
    (HERE/'CORPUS-FINDINGS.md').write_text('\n'.join(findings)+'\n')
    print(json.dumps(summary,ensure_ascii=False))

if __name__ == '__main__':
    main()
