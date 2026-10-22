#!/usr/bin/env python3
"""Build research-only documents. Does not write operating assets or call providers."""
import collections, copy, csv, hashlib, json
from pathlib import Path
from research_cards import CARDS, EXISTING_DECISIONS
from research_context import NOTES, WORKS, category, route
from research_sources import sources
from evaluation_cases import CASES

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT/'skills/photo-prompt-image-generator/assets'
HELD = {
 'A002':'VHS-C model-specific reference/adapter compatibility review needed',
 'A012':'choose generic bars or independently review a named test-pattern standard',
 'A015':'teletext grid and original page detail reference needed',
 'A058':'independent face-pareidolia primary reference needed',
 'A061':'mechanical access-panel reference needed; creator interview not fully read',
 'A076':'Morse-code table and exact encoded string need independent verification'
}
def write(n, data): (HERE/n).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
def md(n, text): (HERE/n).write_text(text.rstrip()+'\n')
def source_link(sid, by): return f'[{sid}: {by[sid]["title"]}]({by[sid]["url"]})'
def source_for(n, linked):
    found = sorted({sid for c in linked for sid in c['source_ids']})
    if n in WORKS: return WORKS[n][1]
    if found: return found
    if n <= 15: return ['S19','S21']
    if 66 <= n <= 79: return ['S09'] if n==68 else ['S21']
    if 139 <= n <= 155: return ['S35'] if n==155 else ['S30']
    if 156 <= n <= 167: return ['S33'] if n==167 else ['S34'] if n==163 else ['S32']
    if 168 <= n <= 171: return ['S28']
    if n in (181,182): return ['S29','S36']
    if n==38: return ['S15']
    return ['S21']

def main():
    src=sources(); by={x['id']:x for x in src}
    terms=list(csv.DictReader((HERE/'seeds.tsv').open(), delimiter='\t'))
    cards=copy.deepcopy(CARDS); drafts=[]
    for c in cards:
        c.update(schema='analog-horror-research-card/v1',
                 activation='post_core_optional_complete_realization; broad genre never activates all cards',
                 source_claim_scope='sources support only their ledger scopes; exact components, layouts and scenes are authored proposals, not canonical source descriptions',
                 evidence_status='research_proposal_not_native_qualified', native_approval=False, runtime_importable=False,
                 whole_case_rule='partial_is_fail; UNOBSERVABLE_NOT_PASS', requester_acceptance='pending',
                 definition_review='additional_detail_reference_required' if c['id'] in HELD else 'bounded_source_context_and_authored_realization',
                 unproven=['actual medium provenance','causal mechanism','temporal behavior','audio','identity/consent/intent','viewer fear or nostalgia'])
        c['positive_en']='Show '+'. Show '.join(o['visible_en'] for o in c['owners'])+'. '+'. '.join(r['visible_en'] for r in c['relations'])+'.'
        c['positive_ko']='. '.join(o['visible_ko'] for o in c['owners'])+'. '+'. '.join(r['visible_ko'] for r in c['relations'])+'.'
        c['render_gate_proposals']=[dict(id=c['id']+'_owner_'+o['id'], owner=o['id'], requirement_en=o['visible_en'], requirement_ko=o['visible_ko'], scale='native') for o in c['owners']]
        c['render_gate_proposals'] += [dict(id=c['id']+'_relation_'+str(i+1), subject=r['subject'], object=r['object'], predicate=r['predicate'], requirement_en=r['visible_en'], requirement_ko=r['visible_ko'], scale='native') for i,r in enumerate(c['relations'])]
        if c['id'] in HELD: c['draft_hold_reason']=HELD[c['id']]; continue
        drafts.append(dict(id='draft_'+c['id'], card_id=c['id'], seed_ids=c['seed_ids'],
                           positive_en=c['positive_en'], positive_ko=c['positive_ko'],
                           owners=c['owners'], relations=c['relations'], proposed_slots=c['proposed_slots'],
                           conditions_proposal={'explicit_carrier_required':c['layer'] in ('playback_raster','playback_signal','composite_signal','transmission','display','digitization'),
                                                'digital_transfer_required':c['layer']=='digital_codec',
                                                'subject_eligibility':'preserve requested subjects; no automatic person/monster/violence addition'},
                           effect_targets_proposal=[dict(owner=o['id'], scope=c['layer']) for o in c['owners']],
                           source_ids=c['source_ids'], confusion_boundaries_ko=c['confusion_boundaries_ko'],
                           claim_limit_ko=c['claim_limit_ko'], render_gate_proposals=c['render_gate_proposals'],
                           native_approval=False, runtime_importable=False, registration_status='not_in_operating_manifest',
                           adoption='reuse/refine/new decision required against current complete source; draft count is not planned net additions'))
    routes=[]
    independently_bounded={33,34,35,38,43,48,49,50,51,54,55,56,58,59,68,98,139,168,169,170,171,174,175,181}
    for term in terms:
        n=int(term['id']); linked=[c for c in cards if n in c['seed_ids']]
        mode,note=route(n,linked)
        r=dict(id=f'K{n:03}',seed_id=n,en=term['en'],ko=term['ko'],category=category(n),route=mode,
               note_ko=note,card_ids=[c['id'] for c in linked],source_ids=source_for(n,linked),
               source_support='bounded_definition_or_distinction' if n in independently_bounded else 'family_context_or_authored_proxy_not_individual_definition_verification',
               native_approval=False)
        if n>=183:
            version,refs,review=WORKS[n]
            r.update(version_scope=version,canon_review_ko=review,definition_review='pending_primary_scene_review')
        routes.append(r)
    mapping=json.loads((HERE/'existing-source-mapping.json').read_text())
    for row in mapping:
        action,reason=EXISTING_DECISIONS[row['cid']]
        row['research_decision']=dict(action=action,reason_ko=reason,status='bounded_source_review_not_native_approval')
    findings=['# 현재 코퍼스와의 중복·공백·다의어 진단', '',
              '원문 후보 19,801개, 직접 binding 14,246개, manifest 모듈 67개를 읽은 고정 시점 진단이다. 200개 원 용어 중 지정 필드에서 0건은 105개다. 0건은 의미 부재나 검색 실패의 증거가 아니며, 아래 표본 19개만 전체 레코드와 직접 binding을 읽어 판단했다.', '',
              '필드: content의 en, ko, definition, phrase_en, phrase_ko, composition_instruction, runtime_expression과 해당 realization 필드. aliases/embedding_text/tags/negative/provenance는 이 어휘 진단에서 제외했다. 영어는 낱말 경계를 적용했고 복합 항목은 / 기준의 제한된 분리다. 대소문자·표기·철자 변형 전체를 포괄하지 않는다.', '',
              '표본 선정은 focus term마다 manifest 순서의 처음 두 레코드다. 관련성 순위나 검색 top-k가 아니다. `CORPUS-LEXICAL-AUDIT.json`의 SHA와 changes_during_read를 함께 확인한다. 원문 판단은 native qualification과 다르다.', '',
              '|source ID|payload owner|판단|이유|', '|---|---|---|---|']
    for x in mapping:
        d=x['research_decision'];findings.append(f'|{x["cid"]}|{x["module"]}|{d["action"]}|{d["reason_ko"]}|')
    findings += ['', '## 신규 source가 필요한지 확인할 영역', '',
                 'color bars·teletext·spectrogram·head switching·mistracking·redaction 등의 지정 영문 focus는 이 진단에서 0건이었다. 한국어·동의어·다른 필드·기존 전체 source의 다른 관계로 구현돼 있을 수 있으므로 신규 등록의 직접 근거는 아니다. 먼저 기존 한국어/관계/장면 의미까지 검색하고 전체 source를 심사한다.', '',
                 '## 재사용과 정정의 기준', '',
                 'VHS 거실·애니매트로닉·유기 건축은 장면이 맞을 때 전체 source 재사용을 우선한다. 조건부 dropout은 이미 선언한 playback image에만 결함을 두는 분기를 보존한다. 렌즈 ghosting·solar tracking·색채 chroma의 기존 의미를 변경하지 않으며, broadcast echo·tape tracking·video color delay가 별도 공백인지 검토한다.', '',
                 '기존 VHS scanlines/color bleed의 혼합 표현은 분리 보완 우선순위다. 단순 설명 교체로 effects·owner·필수 의무가 달라진 사실을 숨기지 않고, 변경 전후 source와 후속 검증을 남긴다.', '',
                 '## 현재 결과의 한계', '',
                 '실제 BM25F/embedding/cosine/RRF·role exposure·선택·prompt transport·이미지·native pixels는 실행하지 않았다. source ID·내용 해시·직접 binding 전체는 existing-source-mapping.json에 있으며 코드가 재사용을 자동 승인하지 않는다.']
    md('CORPUS-FINDINGS.md','\n'.join(findings))
    write('existing-source-mapping.json',mapping)
    write('sources.json',dict(schema='analog-horror-source-ledger/v1',sources=src))
    write('keyword-routes.json',dict(schema='analog-horror-keyword-routes/v1',routes=routes))
    write('semantic-cards.json',dict(schema='analog-horror-research-registry/v1',cards=cards))
    write('candidate-drafts.json',dict(schema='analog-horror-candidate-drafts/v1',runtime_importable=False,drafts=drafts,held_cards=HELD))
    write('evaluation-cases.json',dict(schema='analog-horror-evaluation-plan/v1',status='NOT_RUN',cases=CASES))
    with (HERE/'EVALUATION-CASES.tsv').open('w') as f:
        w=csv.writer(f,delimiter='\t'); w.writerow(['id','split','group','query_ko','query_en','expected_cards','reject','review','status'])
        for x in CASES: w.writerow([x['id'],x['split'],x['group'],x['query_ko'],x['query_en'],','.join(x['expected_card_ids']),x['reject_ko'],x['review_ko'],x['execution_status']])
    with (HERE/'SOURCES.tsv').open('w') as f:
        w=csv.writer(f,delimiter='\t');w.writerow(['id','title','url','access','read_scope','finding_ko'])
        for x in src: w.writerow([x[k] for k in ('id','title','url','access','read_scope','finding_ko')])
    atlas=['# 원 대화 200개 키워드의 처리 경로', '', '원래 복합 항목의 번호를 보존했다. `mixed`는 부분별 관찰 가능성이 다르다는 뜻이다. 맥락만 남긴 용어도 누락된 것이 아니다.', '',
           '독립 원전 정의를 200개 모두 검증한 것은 아니다. source_support가 개념군 문맥인 항목은 저술한 시각 proxy 또는 후속 조사 경로다.', '',
           '|번호|용어|경로|연결 카드|반영 판단|', '|---|---|---|---|---|']
    for r in routes: atlas.append(f'|{r["seed_id"]}|{r["en"]} / {r["ko"]}|{r["route"]}|{", ".join(r["card_ids"]) or "—"}|{r["note_ko"]}|')
    atlas += ['', '판본별 검토 상태:', '', '|번호|판본 범위|원전 확인 한계|', '|---|---|---|']
    for r in routes:
        if r['seed_id']>=183:atlas.append(f'|{r["seed_id"]}|{r["version_scope"]}|{r["canon_review_ko"]}|')
    md('KEYWORD-ATLAS.md','\n'.join(atlas))
    visual=['# 시각 의미 카드 78개', '', '각 카드는 하나의 선택형 저술 실현이다. 원래 용어 전체의 정의·사실·원작 형상을 보장하지 않는다. 가시 성분과 관계를 모두 확인하며 부분 성공은 전체 성공이 아니다.', '']
    for c in cards:
        visual += [f'## {c["id"]} {c["title_ko"]}', '', f'원 용어: {", ".join(str(x) for x in c["seed_ids"])} · layer={c["layer"]} · {c["evidence_mode"]} · {c["priority"]}', '',
                   '**EN** '+c['positive_en'], '', '**KO** '+c['positive_ko'], '', '성분: '+ '; '.join(o['id']+': '+o['visible_ko'] for o in c['owners']), '',
                   '방향 관계: '+ '; '.join(r['subject']+' → '+r['predicate']+' → '+r['object'] for r in c['relations']), '',
                   '혼동 경계: '+ '; '.join(c['confusion_boundaries_ko']), '', '주장 한계: '+c['claim_limit_ko'], '',
                   '예정 slot: '+', '.join(c['proposed_slots']), '', '출처의 제한된 근거: '+', '.join(source_link(s,by) for s in c['source_ids']), '',
                   '검토: 모든 owner와 relation을 같은 native 이미지에서 확인. 가려짐·병합·관계 역전·텍스트 오독은 실패. 소리·시간·동의·초자연 인과는 평가 범위 밖.', '']
        if c['id'] in HELD: visual += ['**후보 초안 보류:** '+HELD[c['id']], '']
    md('VISUAL-CARDS.md','\n'.join(visual))
    summary=dict(seeds=len(routes),cards=len(cards),candidate_drafts=len(drafts),held_cards=len(HELD),
                 sources=len(src),source_access_counts=dict(collections.Counter(x['access'] for x in src)),
                 route_counts=dict(collections.Counter(x['route'] for x in routes)),
                 card_mode_counts=dict(collections.Counter(x['evidence_mode'] for x in cards)),
                 evaluation_cases=len(CASES),bilingual_queries=2*len(CASES),case_groups=dict(collections.Counter(x['group'] for x in CASES)),
                 existing_sources_reviewed=len(mapping),runtime_adoption='NOT_RUN',retrieval_evaluation='NOT_RUN',image_generation='NOT_RUN',pixel_evaluation='NOT_RUN')
    write('SUMMARY.json',summary)
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__': main()
