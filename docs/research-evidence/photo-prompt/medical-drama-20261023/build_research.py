"""Build inert research artifacts inside this folder only. No API or index calls."""
import collections
import csv
import hashlib
import json
from pathlib import Path
from research_cards import make_cards
from research_sources import sources
from route_spec import routes

ROOT=Path(__file__).resolve().parent
def write(name,data):
    (ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def md(text): return str(text).replace('|',' / ').replace('\n',' ')

def main():
    ref=json.loads((ROOT/'reference-conversation.json').read_text())
    # Keep the referenced conversation, remove unrelated sidebar/navigation UI.
    if '내가 한 말:' in ref['text']:
        ref['text']=ref['text'].split('내가 한 말:',1)[1].split('ChatGPT는 실수할 수 있습니다.',1)[0].strip()
        ref['extraction_scope']='Visible conversation only; unrelated sidebar and composer UI removed.'
        write('reference-conversation.json',ref)
    cards=make_cards()
    existing=json.loads((ROOT/'existing-source-mapping.json').read_text())['selected']
    srcs=sources()
    src_lookup={s['id']:s for s in srcs}
    # Upgrade only an actually reread source's access description.
    src_lookup['S36']['access']='page_read_selected_sections'
    fresh_sources=['S03','S13','S08','S01','S01','S23','S13','S13','S14','S14','S14','S21','S01','S01','S37','S37','S37','S28','S21','S01','S03','S37']
    for old,sid in zip(existing,fresh_sources):
        rec=old['source_record'];reg=old['registry_card'];rr=reg.get('relations',[])
        edges=[{'from':e['subject'],'relation':e['predicate'],'to':e['object']} for e in rr]
        ownership=[]
        for endpoint in {e[k] for e in edges for k in ('from','to')}:
            if '.' in endpoint:ownership.append({'part':endpoint,'owner':endpoint.split('.',1)[0]})
        cards.append(dict(id=old['id'],title_ko=reg['title_ko'],mode='existing_visual_reuse_proposal',
            positive_en=rec['content']['en'],positive_ko=rec['content']['ko'],
            candidate_id=rec['id'],source_file=old['source_file'],source_record_sha256=old['source_record_sha256'],
            full_source_snapshot='existing-source-mapping.json',inherited_conditions=rec.get('conditions',{}),
            inherited_effects=rec.get('effects',{}),inherited_application_contract=rec['content'].get('application_contract'),
            owner_nodes=sorted({e[k] for e in edges for k in ('from','to')}|{o['owner'] for o in ownership}),
            relations=edges,part_ownership=ownership,
            observable_gates=[rec['content']['en']]+[f"{e['from']} {e['relation']} {e['to']}" for e in edges],
            confusion_boundary='; '.join(reg.get('confusion_boundaries',[])),
            claim_limit=reg.get('claim_limit_ko','Visible form only; nonvisual claims require separate context.'),
            source_ids=[sid],suggested_slots=sorted({x['record']['slot_id'] for x in old['binding_records'].values()}),
            priority='P1',readiness='reuse_proposed_requires_current_full_source_qualification',
            native_approval=False,runtime_importable=False,activation='optional_post_core_only',
            source_support_scope='Existing complete canonical literal is preserved. Current web source supports the boundary only.',
            unobservable_policy='UNOBSERVABLE_NOT_PASS',whole_case_policy='partial_is_fail'))
    rout=routes(ref,cards)
    for card in cards:
        card['source_keyword_ids']=[r['id'] for r in rout if card['id'] in r['optional_visual_card_ids']+r['context_card_ids']+r['held_card_ids']]
    # Duplication and source wording are review findings, never silent edits.
    byid={c['id']:c for c in cards}
    byid['G06']['overlap_review']={'existing_card':'R20','decision':'prefer existing complete source when its chair, coat, unused gloves and clothed-adult constraints fit; add couch variant only if independently useful'}
    byid['R15']['registry_drift_note']='Canonical owner is biopunk/body-horror and its complete bilingual text differs from the medical registry synopsis. Only canonical text is retained here; registry graph is advisory and requires renewed review.'
    byid['R18']['precision_review']='Healed is an authored source descriptor, not clinical healing proof. Review visual versus medical interpretation before adoption.'
    byid['R06']['readiness']='reuse_proposed; exact instrument variant still requires plate review'
    visual=[c for c in cards if c['positive_en'] is not None]
    drafts=[dict(id='draft_'+c['id'],card_id=c['id'],kind=c['mode'],en=c['positive_en'],ko=c['positive_ko'],
        suggested_slots=c['suggested_slots'],source_ids=c['source_ids'],owner_nodes=c['owner_nodes'],relations=c['relations'],
        preserve_complete_proposition=True,native_approval=False,runtime_importable=False,
        future_conditions='Explicitly bind actual owners and all changed dimensions/properties after independently frozen requester meaning.',
        claim_limit=c['claim_limit']) for c in visual]
    write('sources.json',dict(schema='medical-drama-source-ledger/v1',sources=srcs))
    write('semantic-cards.json',dict(schema='medical-drama-research-cards/v1',cards=cards,native_approval=False))
    write('candidate-drafts.json',dict(schema='medical-drama-inert-candidate-drafts/v1',drafts=drafts,runtime_importable=False))
    write('keyword-routes.json',dict(schema='medical-drama-advisory-routes/v1',routes=rout))
    with (ROOT/'SOURCES.tsv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['id','title','url','access','supported_scope','claim_limit'],delimiter='\t',extrasaction='ignore');w.writeheader();w.writerows(srcs)
    atlas=['# 원 대화 용어 전체 연결','',
        '346개는 표의 행 수다. 복합 항목을 임의로 쪼개 수량을 늘리지 않았고, 반복된 의료 테마 코스튬 행도 원문 위치를 유지했다. 8개 장면 조합은 별도 파일이다.',
        '연결은 관련된 선택지를 찾는 경로이며 동의어·전체 정의·필수 활성화 규칙이 아니다. 개별 임상 정의 검증률을 뜻하지 않는다.','',
        '|ID|절|원문 용어|문맥|선택적 시각 카드|보류|','|---|---|---|---|---|---|']
    for r in rout:atlas.append('|'+ '|'.join(map(md,[r['id'],r['section'],r['term'],', '.join(r['context_card_ids']),', '.join(r['optional_visual_card_ids']) or '없음',', '.join(r['held_card_ids']) or '없음']))+'|')
    (ROOT/'KEYWORD-ATLAS.md').write_text('\n'.join(atlas)+'\n')
    doc=['# 시각 의미·후보 카드','',
        'A–G는 신규 작성 100개, R은 기존 완전 소스 재사용 제안 22개다. X 42개는 비가시 문맥, H 8개는 추가 자료가 필요한 항목이다. 모든 문장은 연구 초안이며 실제 임상 사진의 관측 기록이나 native 승인 자료가 아니다.','',
        '관계 그래프는 검토용이다. 운영 타입·guard·owner permission으로 자동 변환하지 않는다. 체내 끝점·소리·시간·진단·동의를 가시 끝점으로 바꾸지 않는다.','']
    for c in cards:
        doc.extend([f"## {c['id']} · {c['title_ko']}",'',f"분류: `{c['mode']}`. 출처: "+', '.join(f"[{s}: {src_lookup[s]['title']}]({src_lookup[s]['url']})" for s in c['source_ids']), ''])
        if c['positive_en']:
            doc.extend([c['positive_en'],'',c['positive_ko'],'','관찰 기준: '+'; '.join(c['observable_gates']),'',
                '소유·관계: '+'; '.join(f"{e['from']} → {e['relation']} → {e['to']}" for e in c['relations']),''])
        doc.extend(['혼동 경계: '+c['confusion_boundary'],'','주장 한계: '+c['claim_limit'],''])
        if c.get('registry_drift_note'):doc.extend(['기존 레지스트리 차이: '+c['registry_drift_note'],''])
    (ROOT/'VISUAL-CARDS.md').write_text('\n'.join(doc)+'\n')
    counts=dict(keyword_rows=len(rout),combination_rows=len(ref['tables'][-1]['rows'])-1,
        new_visual_drafts=100,existing_visual_reuse_proposals=len(existing),visual_candidates=len(visual),
        context_cards=sum(c['mode']=='context_only' for c in cards),held_cards=sum(c['mode']=='held_reference_needed' for c in cards),
        total_cards=len(cards),source_records=len(srcs),external_source_records=len(srcs)-1,
        source_access=dict(collections.Counter(s['access'] for s in srcs)),
        observable_checks=sum(len(c['observable_gates']) for c in visual),
        suggested_presentation_links=sum(len(c['suggested_slots']) for c in visual),
        runtime_imports=0,image_calls=0,embedding_calls=0)
    write('SUMMARY.json',dict(schema='medical-drama-research-summary/v1',date_kst='2026-10-23',counts=counts,
        evidence=dict(research_structure='PENDING_VALIDATION',native_qualification='NOT_RUN',live_retrieval='NOT_RUN',
        image_generation='NOT_RUN',pixel_evaluation='NOT_RUN',installation='NOT_RUN',user_acceptance='NOT_REQUESTED',commit='NOT_RUN',push='NOT_RUN')))
    print(json.dumps(counts,ensure_ascii=False))

if __name__=='__main__':main()
