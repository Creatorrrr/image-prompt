#!/usr/bin/env python3
"""Build only this research folder. Reads source modules; no engine/API imports."""
import collections
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True

from research_cards import DATA
from research_sources import SOURCES
from evaluation_cases import DATA as EVALUATION_DATA

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def dump(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def cell(x):
    return str(x).replace('|', '\\|').replace('\n', ' ')

def main():
    groups = []
    seeds = []
    for line in (HERE/'seeds.txt').read_text().splitlines():
        if line.startswith('['):
            group=line[1:-1];groups.append(group)
        elif line.strip():
            ko, sep, en = line.partition(' — ')
            seeds.append(dict(id=f'T{len(seeds)+1:03d}', group=group,
                              label=line, ko=ko if sep else '', en=en if sep else ko))
    routes={}
    for line in (HERE/'term_routes.txt').read_text().splitlines():
        if not line or line.startswith('#'):continue
        term, mode, refs, note=line.split('|')
        assert term not in routes, term
        routes[term]=dict(evidence_mode=mode, optional_cards=refs.split(), boundary_ko=note)
    assert len(seeds)==247 and len(routes)==247,(len(seeds),len(routes))
    assert {s['en'] for s in seeds}==set(routes)
    cards=[]
    catalog=json.loads((ASSETS/'photo_candidate_slot_catalog.json').read_text())['slot_catalog']
    for line in DATA.strip().splitlines():
        fields=line.split('|');assert len(fields)==13,(fields[0],len(fields))
        cid,title,terms,mode,sources,slots,parts,relations,en,ko,confusions,limit,priority=fields
        owners=[dict(id=p.split('=',1)[0],visible_component_en=p.split('=',1)[1]) for p in parts.split(';')]
        edges=[dict(subject=s,predicate=p,object=o) for s,p,o in (r.split('>') for r in relations.split(';'))]
        ids={x['id'] for x in owners}
        assert all(e['subject'] in ids and e['object'] in ids for e in edges),cid
        assert all(t in routes for t in terms.split(';')),(cid,terms)
        assert set(slots.split())<=set(catalog),(cid,slots)
        cards.append(dict(id=cid,title_ko=title,seed_terms=terms.split(';'),evidence_mode=mode,
                          source_refs=sources.split(),proposed_current_slots=slots.split(),owners=owners,relations=edges,
                          phrase_en=en,phrase_ko=ko,confusion_boundaries=confusions.split(';'),claim_limit_ko=limit,
                          priority=priority,source_support='definition_or_context_only; concrete geometry is authored',
                          activation='optional_post_core_only; genre_label_never_activates_all_cards',
                          qualification='research_draft_not_native_approved',
                          gates=[] if mode=='context' else
                          [dict(kind='component',owner=o['id'],description=o['visible_component_en']) for o in owners]+
                          [dict(kind='relation',**e) for e in edges],
                          review_policy=dict(unobservable='UNOBSERVABLE_NOT_PASS',whole_case='partial_is_fail')))
    assert len(cards)==72
    cardmap={c['id']:c for c in cards};sourcemap={s['id']:s for s in SOURCES}
    assert all(set(c['source_refs'])<=set(sourcemap) for c in cards)
    group_sources={groups[0]:['S01','S02','S07','S08','S09'],groups[1]:['S04','S06','S26'],
                   groups[2]:['S02','S03'],groups[3]:['S04','S05'],groups[4]:['S03','S36'],
                   groups[5]:['S04','S12','S33'],groups[6]:['S22','S25','S31','S32','S33'],
                   groups[7]:['S23','S24','S34','S35'],groups[8]:['S10','S28'],
                   groups[9]:['S10','S36'],groups[10]:['S06','S11','S37','S38','S41','S42','S43','S44'],
                   groups[11]:['S12','S14','S15'],groups[12]:['S16','S17','S18','S19','S20','S21'],
                   groups[13]:['S03','S27'],groups[14]:['S29','S30'],groups[15]:['S29','S30']}
    for seed in seeds:
        seed.update(routes[seed['en']]);assert set(seed['optional_cards'])<=set(cardmap)
        seed['source_refs']=sorted(set(group_sources[seed['group']]+[s for c in seed['optional_cards'] for s in cardmap[c]['source_refs']]))
        seed['source_scope']='family_definition_or_interpretation_boundary; not independent verification of every term'
        seed['definition_origin']='referenced_chat_rendered_table; no prior citation adopted as verified'
        seed['planned_disposition']='context_only' if seed['evidence_mode'] in ('context','sequence','nonvisual','advisory') else 'reuse_refine_or_new_after_full_source_review'
    dump('sources.json',SOURCES)
    dump('semantic-cards.json',dict(schema='dark-fantasy-research-cards/v1',runtime_importable=False,cards=cards))
    dump('keyword-routes.json',dict(schema='dark-fantasy-research-atlas/v1',reference_conversation='6ad8d93d-e51c-83ec-96a0-2aafa7512902',routes=seeds))
    drafts=[]
    for c in cards:
        if c['evidence_mode']=='context':continue
        drafts.append(dict(research_id=c['id'],phrase_en=c['phrase_en'],phrase_ko=c['phrase_ko'],
                           owners=c['owners'],relations=c['relations'],source_refs=c['source_refs'],
                           proposed_slots=c['proposed_current_slots'],evidence_mode=c['evidence_mode'],
                           required_context='independently authored scene; all owners and effects need explicit native review',
                           effects_status='NOT_AUTHORED_NATIVE_EFFECTS; resolve every added/modified entity and owned property',
                           claim_limit_ko=c['claim_limit_ko'],confusion_boundaries=c['confusion_boundaries'],
                           status='research_only_not_loader_input_not_approved',native_cid=None,native_rid=None))
    dump('candidate-drafts.json',dict(schema='dark-fantasy-research-drafts/v1',runtime_importable=False,drafts=drafts))
    lines=['# 키워드 247개의 시각 의미 경로','',
           '원 대화의 16개 용어 표를 복원했다. 7개 조합 예시는 별도 서사 설계 자료다. 아래 카드는 선택 가능한 연구안이며 단어의 필수 외형이나 자동 의무가 아니다.',
           '', 'still=정지 화면의 형태/관계, proxy=외형 단서만, versioned=원전/판본 구분, context=명시 문맥, sequence=시간 축, nonvisual=다른 감각, advisory=넓은 분류/정조.',
           '', '출처는 주로 가족 개념/판정 한계를 뒷받침한다. 247개 개별 정의 모두를 독립 사전에서 검증했다는 의미가 아니다. 구체적인 장면은 저술한 제안이다.','']
    for group in groups:
        lines += [f'## {group}','','| ID | 원 용어 | 근거 방식 | 선택 실현 | 의미·혼동 경계 | 근거 |','|---|---|---|---|---|---|']
        for s in seeds:
            if s['group']==group:
                lines.append('| '+' | '.join(cell(x) for x in [s['id'],s['label'],s['evidence_mode'],' '.join(s['optional_cards']) or '문맥/추가 원전',s['boundary_ko'],' '.join(s['source_refs'])])+' |')
        lines.append('')
    (HERE/'KEYWORD-ATLAS.md').write_text('\n'.join(lines)+'\n')
    lines=['# 시각 의미 카드 72개','', '정의 근거와 아래 가시 실현의 창작 저술을 구분한다. 4개 context 카드는 시각 후보로 변환하지 않는다.','']
    for c in cards:
        lines += [f"## {c['id']} {c['title_ko']}",'',f"- 연결 키워드: {'; '.join(c['seed_terms'])}",
                  f"- 방식/우선순위: {c['evidence_mode']} / {c['priority']}; 슬롯 제안: {', '.join(c['proposed_current_slots'])}",
                  f"- EN: {c['phrase_en']}",f"- KO: {c['phrase_ko']}",
                  '- 소유자: '+'; '.join(o['id']+' = '+o['visible_component_en'] for o in c['owners']),
                  '- 관계: '+'; '.join(e['subject']+' → '+e['predicate']+' → '+e['object'] for e in c['relations']),
                  '- 혼동: '+'; '.join(c['confusion_boundaries']),f"- 주장 한계: {c['claim_limit_ko']}",
                  '- 출처: '+', '.join('['+sid+']('+sourcemap[sid]['url']+')' for sid in c['source_refs']),
                  '- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.','']
    (HERE/'VISUAL-CARDS.md').write_text('\n'.join(lines)+'\n')
    (HERE/'SOURCES.tsv').write_text('id\ttitle\turl\taccess\tlocator\tsupported_scope_and_limit_ko\n'+'\n'.join('\t'.join(cell(s[k]).replace('\t',' ') for k in ['id','title','url','access','locator','supported_scope_and_limit_ko']) for s in SOURCES)+'\n')
    evaluation=[]
    for line in EVALUATION_DATA.strip().splitlines():
        qid,cohort,ko,en,refs,expected,forbidden=line.split('|')
        assert refs=='none' or set(refs.split())<=set(cardmap)
        evaluation.append([qid,cohort,ko,en,refs,expected,forbidden,'NOT_RUN'])
    assert len(evaluation)==56
    (HERE/'EVALUATION-CASES.tsv').write_text('id\tcohort\tquery_ko\tquery_en\ttarget_cards_not_cids\texpected_boundary\tforbidden_inference\tstatus\n'+'\n'.join('\t'.join(row) for row in evaluation)+'\n')
    print(json.dumps(dict(seeds=len(seeds),cards=len(cards),candidate_drafts=len(drafts),sources=len(SOURCES),
                          term_modes=dict(collections.Counter(s['evidence_mode'] for s in seeds)),
                          card_modes=dict(collections.Counter(c['evidence_mode'] for c in cards))),ensure_ascii=False))

if __name__=='__main__':main()
