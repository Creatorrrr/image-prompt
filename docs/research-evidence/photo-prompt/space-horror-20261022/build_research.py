#!/usr/bin/env python3
"""Derive reviewable research artifacts in THIS directory only. No API/runtime writes."""
import collections, csv, hashlib, io, json, re
from pathlib import Path
from research_sources import sources
from research_cards import DATA
from research_context import DATA as CONTEXT_DATA, NONVISUAL, SEQUENCE, CONTEXT

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
SLOTS=json.loads((ROOT/'skills/photo-prompt-image-generator/assets/photo_candidate_slot_catalog.json').read_text())['slot_catalog']
def dump(n,v): (HERE/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def write(n,v): (HERE/n).write_text(v)
def rows(data): return [line.split('|') for line in data.strip().splitlines() if line.strip()]
def mdcell(s): return str(s).replace('|',' / ').replace('\n',' ')
def source_links(ids): return ', '.join('['+i+']('+SS[i]['url']+')' for i in ids)

SS={r['source_id']:r for r in sources()}
cards=[]
for row in rows(DATA):
    assert len(row)==12,(len(row),row[0])
    cid,title,seeds,mode,en,ko,ownertext,reltext,confusion,limit,src,slots=row
    owners=dict(x.split(':',1) for x in ownertext.split(';'))
    relations=[dict(zip(['from','relation','to'],x.split('>'))) for x in reltext.split(';')]
    proposed=slots.split(',')
    card=dict(card_id=cid,title=title,seed_ids=[int(x) for x in seeds.split(',')],observability=mode,proposal_en=en,proposal_ko=ko,owners=owners,directed_relations=relations,nearest_confusion=confusion,claim_limit=limit,source_ids=src.split(','),proposed_slots=proposed,proposed_dimensions=sorted({d for s in proposed for d in SLOTS[s]['dimensions']}),
              priority='P0' if int(cid[1:]) in list(range(1,18))+[18,19,21,26,28,31,34,35,36,37,48,55,62,63] else 'P1',
              semantic_authority='research_only',native_approval=False,visual_status='authored_optional_realization_not_canonical_design',source_claim_scope='sources support bounded definitions or work-specific context; selected geometry and narrative cues are authored',
              review_gates=[dict(gate_id=f'{cid}-R{i+1}',required_visible_relation=r,status='NOT_RUN',partial_is_fail=True,unobservable_is_pass=False) for i,r in enumerate(relations)],
              scope_gate=dict(required='judge only declared visible morphology/relations; do not mark title or hidden cause as pixel-proved',status='NOT_RUN'))
    cards.append(card)

contexts=[]
for did,seedids,dist,support,limit,src in rows(CONTEXT_DATA):
    contexts.append(dict(context_id=did,seed_ids=[int(x) for x in seedids.split(',')],distinction=dist,permitted_visible_support=support,not_established=limit,source_ids=src.split(','),material_retrieval=False,native_approval=False,assertion_strength='context_only_not_hard_visual_profile'))

adj=[('Eldritch','기괴하고 이계적인'),('Abyssal','심연의'),('Chthonic','지하·저승의'),('Cyclopean','거석적·압도적인'),('Sepulchral','무덤 같은'),('Necrotic','괴사성의'),('Chitinous','키틴질의'),('Visceral','내장적·본능적인'),('Amorphous','일정한 형태가 없는'),('Non-anthropomorphic','비인간형의'),('Bioluminescent','생물발광성의'),('Voidborne','공허·우주에서 온 듯한 창작어'),('Starless','별이 없는'),('Desolate','황량하고 버려진'),('Sterile','무균의·불모의'),('Airless','공기가 없는'),('Lightless','빛이 없는'),('Unfathomable','깊이·본질을 헤아릴 수 없는'),('Ineffable','언어로 충분히 표현할 수 없는'),('Primordial','태초의·원초적인')]
labels=[]
for line in (HERE/'reference-keywords.txt').read_text().splitlines():
    number,rest=line.split('. ',1);en,ko=rest.split(' — ',1);labels.append((int(number),en,ko))
labels += [(181+i,en,ko) for i,(en,ko) in enumerate(adj)]
assert [x[0] for x in labels]==list(range(1,201))

keyword_routes=[]
for number,en,ko in labels:
    linked=[c['card_id'] for c in cards if number in c['seed_ids']]
    diagnostic=[c['context_id'] for c in contexts if number in c['seed_ids']]
    route='nonvisual' if number in NONVISUAL else 'sequence' if number in SEQUENCE else 'context' if number in CONTEXT else 'still' if any(c['observability']=='still' for c in cards if c['card_id'] in linked) else 'proxy'
    if number in range(181,201): linked=list({184:['V26','V27'],186:['V39'],189:['V30'],190:['V30'],193:['V64'],194:['V18','V23'],196:['V01'],197:['V64']}.get(number,linked))
    keyword_routes.append(dict(id=f'K{number:03}',source_number=number,en=en,ko=ko,source_group='core180' if number<=180 else 'descriptive20',handling=route,visual_card_ids=linked,context_ids=diagnostic,automatic_hard_profile=False,
                               treatment='related cards are optional visible realizations; the source term is not a universal image recipe; preserve contextual or sequential remainder',definition_status='source_conversation_label_verified; bounded independent concept-family research, not 200 independent dictionary validations'))

withheld={'V41','V47','V61'}
drafts=[]
for c in cards:
    if c['card_id'] in withheld: continue
    drafts.append(dict(draft_id='SH-DRAFT-'+c['card_id'],card_id=c['card_id'],record_kind_proposal='visual_option',en=c['proposal_en'],ko=c['proposal_ko'],owners=c['owners'],relations=c['directed_relations'],proposed_slots=c['proposed_slots'],proposed_dimensions=c['proposed_dimensions'],claim_limit=c['claim_limit'],confusion_boundary=c['nearest_confusion'],source_ids=c['source_ids'],stage='research_draft_not_loader_input',native_approval=False,candidate_id=None,realization_id=None,
                       adoption='defer_iconography_review' if c['card_id']=='V45' else 'defer_physical_or_projection_review' if c['card_id'] in {'V56','V57'} else 'review_reuse_refine_new_before_registration',
                       application_contract='One complete optional realization. Preserve every stated owner, count, layer, directed endpoint and EN/KO clause. Do not inherit a diagnosis, hidden cause, identity, consciousness, consent, lineage, time history, specific work design or scientific measurement from the title. All required visible relations must be assessable together; partial or unobservable is not pass. Research sources and graphs grant no native source facts, role permissions or effect permissions.',
                       source_qualification='NOT_RUN',retrieval_evaluation='NOT_RUN',pixel_evaluation='NOT_RUN',required_effect_review='derive exact owner/property changes against independently frozen core; unknown or broad effects cannot qualify a partial lock'))

dump('sources.json',dict(schema='space-horror-sources/v1',sources=list(SS.values())))
dump('semantic-cards.json',dict(schema='space-horror-research-cards/v1',cards=cards))
dump('context-records.json',dict(schema='space-horror-context/v1',records=contexts))
dump('keyword-routes.json',dict(schema='space-horror-keyword-routes/v1',source_conversation='6ada0050-0814-83ec-9e08-64f95a15d94e',routes=keyword_routes))
dump('candidate-drafts.json',dict(schema='space-horror-research-drafts/v1',excluded_positive_cards=sorted(withheld),drafts=drafts))

atlas=['# 키워드 전체 경로\n\n180개 원문 번호와 보조 어휘 20개를 보존했다. `/`로 묶인 용어는 동의어 자동 병합이 아니다. `still`도 그 단어 전체의 입증을 뜻하지 않는다. 과학적 지위와 시각적 관찰 가능성은 별개 축이다. 상세한 구분·한계는 연결된 D/V 기록을 읽는다.\n\n|번호|English|한국어|처리|시각 카드|문맥 기록|\n|---|---|---|---|---|---|\n']
for k in keyword_routes: atlas.append('|'+ '|'.join(map(mdcell,[k['source_number'],k['en'],k['ko'],k['handling'],', '.join(k['visual_card_ids']) or '선택 실현 미작성',', '.join(k['context_ids'])]))+'|\n')
write('KEYWORD-ATLAS.md',''.join(atlas))

carddoc=['# 시각 의미 카드 64개\n\n출처가 지원하는 정의·작품별 해석과 저술한 장면 기하를 구분한다. 모든 관계 gate의 실제 이미지 검토는 NOT_RUN이다. V41·V47·V61은 문맥 단서 카드로 보존하고 양성 후보 초안에서 보류했다.\n']
for c in cards:
    carddoc.append(f"\n## {c['card_id']} {c['title']}\n\n- 원문: {', '.join(map(str,c['seed_ids']))}; 관찰: {c['observability']}; 우선순위: {c['priority']}.\n- EN: {c['proposal_en']}\n- KO: {c['proposal_ko']}\n- 구성 소유자: {'; '.join(k+': '+v for k,v in c['owners'].items())}.\n- 방향 관계: {'; '.join(r['from']+' → '+r['relation']+' → '+r['to'] for r in c['directed_relations'])}.\n- 혼동 경계: {c['nearest_confusion']}.\n- 주장 한계: {c['claim_limit']}\n- 제안 슬롯: {', '.join(c['proposed_slots'])}; 실제 binding 승인 아님.\n- gate: 관계 {len(c['review_gates'])}개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.\n- 출처: {source_links(c['source_ids'])}.\n")
write('VISUAL-CARDS.md',''.join(carddoc))

doc=['# 문맥·과학·비가시 구분\n\n이 20개 기록은 양성 이미지 레시피가 아니다. 정의의 전 범위를 검증한 원전 독해와 현재의 제한된 출처 조사를 구분한다.\n']
for c in contexts:
    doc.append(f"\n## {c['context_id']}\n\n원문 번호: {', '.join(map(str,c['seed_ids']))}.\n\n{c['distinction']}\n\n가시 지원: {c['permitted_visible_support']}\n\n주장 한계: {c['not_established']}\n\n출처: {source_links(c['source_ids'])}.\n")
write('CONTEXT-DISTINCTIONS.md',''.join(doc))

out=io.StringIO();w=csv.writer(out,delimiter='\t');w.writerow(['id','title','url','access','read_scope','supports','limits'])
for s in SS.values():w.writerow([s[x] for x in ['source_id','title','url','access','read_scope','supports','limits']])
write('SOURCES.tsv',out.getvalue())

counts=dict(keywords=len(keyword_routes),core_keywords=180,descriptive_keywords=20,visual_cards=len(cards),candidate_drafts=len(drafts),withheld_positive_cards=sorted(withheld),context_records=len(contexts),sources=len(SS),source_access=dict(collections.Counter(s['access'] for s in SS.values())),keyword_routes=dict(collections.Counter(k['handling'] for k in keyword_routes)),relation_gates=sum(len(c['review_gates']) for c in cards),image_calls=0,retrieval_calls=0,operating_source_writes=0,implementation_status='NOT_RUN')
dump('COUNTS.json',counts)
print(json.dumps(counts,ensure_ascii=False))
