"""Build inert research artifacts. Reads corpus; writes only this directory."""
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
import research_data as data
import research_context as context

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
def dump(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
def digest(raw):
    return hashlib.sha256(raw).hexdigest()
def tsv(name, fields, rows):
    with (OUT/name).open('w') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t');w.writeheader();w.writerows(rows)
def md(name, text):
    (OUT/name).write_text(text.rstrip()+'\n')

seeds=[]
for line in data.SEEDS.strip().splitlines():
    if line.startswith('## '):
        section=line[3:];continue
    en,ko=line.split('|');seeds.append(dict(id=f'K{len(seeds)+1:03}',section=section,en=en,ko=ko))
assert len(seeds)==181
sources=[]
for line in data.SOURCES.strip().splitlines():
    if not line.strip(): continue
    i,title,url,access,support,limit=line.split('|')
    if i=='S32':
        url='https://grants.nih.gov/policy-and-compliance/policy-topics/sharing-policies/dms/privacy/nih-lacks-family-agreement'
        access='initial_www_403; official_search_body_reverified'
        support='1951년 동의 없이 얻은 조직에서 HeLa가 유래; 2013년 가족과의 유전체 접근 합의'
        limit='검색 본문으로 재확인; 개인 의식·기억 지속성 또는 모든 세포 사용의 포괄 동의가 아님'
    sources.append(dict(id=i,title=title,url=url,access_status=access,supported_claim_ko=support,
                        claim_limit_ko=limit,reviewed_date_kst='2026-10-22',quotation_used=False))
dump('sources.json',sources)
tsv('SOURCES.tsv',list(sources[0]),sources)
src={s['id']:s for s in sources}
cards=[]
for raw in data.CARDS:
    c=dict(raw)
    if c['id']=='W07': c['source_refs']=['S47']
    if c['id']=='W08': c['source_refs']=['S48']
    if c['id']=='L02':
        c['source_refs']=['S21','S32']
        c['claim_limit_ko']='증식 지속성·개인·계약·동의는 비가시 문맥이다. HeLa의 비동의 채취는 NIH 검색 본문에서 재확인했으나 용기 외형으로 시료 신원을 확인할 수 없다.'
    c.update(schema='medical-horror-research-card/v1',basis='project_authored_visual_proposal',
      source_support_scope='definition or boundary only; geometry/composition is authored, not an observed clinical photograph',
      observable_components=[c['phrase_en']],positive_ko=c['phrase_ko'],
      render_gates=[{'kind':'complete_visual_proposition','description':c['phrase_en']}]+
       [dict(kind='directed_relation',description=f"{r['subject']} {r['predicate']} {r['object']}") for r in c['relations']],
      evidence_required='all specified owners, counts, boundaries and contact endpoints visible together at useful scale',
      unobservable_policy='UNOBSERVABLE_NOT_PASS',whole_case_policy='partial_is_fail',
      runtime_registration=False,native_approval=False,adoption_decision='pending_full_source_comparison')
    cards.append(c)
for i,title,terms,channel,refs,limit in context.CONTEXTS:
    if i=='X07':
        refs='S06,S51'
        limit='통증·노시보의 인과는 비가시다. NCI는 기대와 관련된 증상 발생으로 노시보를 정의한다. 환상지통의 전문 정의는 추가 확인 대상이며, 부위 부재나 약병만으로 통증·기대를 입증하지 않는다.'
    if i=='X08':
        refs='S49,S50'
        limit='허혈의 혈액 공급 부족과 저산소의 산소 공급 감소는 구별된다. 색·가는 사지를 진단으로 바꾸지 않는다. 위축의 세부 정의와 전후 변화는 추가 전문 자료가 필요하다.'
    limit=limit.replace('具体的','구체적').replace('HeLa 관련 세부는 이번 NIH 본문 접근 실패로 보류하며','HeLa의 1951년 비동의 채취와 2013년 합의는 NIH 검색 본문으로 재확인했으며')
    cards.append(dict(schema='medical-horror-research-card/v1',id=i,title_ko=title,seed_terms=terms.split(';'),
      evidence_mode=channel,source_refs=refs.split(','),claim_limit_ko=limit,observable_components=[],relations=[],
      proposed_slots=[],render_gates=[],basis='context_boundary_not_positive_visual_fact',runtime_registration=False,
      native_approval=False,adoption_decision='context_or_further_research',unobservable_policy='UNOBSERVABLE_NOT_PASS',
      whole_case_policy='partial_is_fail',priority='P2'))
dump('semantic-cards.json',cards)
routes=[]
for k in seeds:
    matches=[c for c in cards if k['en'] in c['seed_terms']]
    assert matches,k
    visual=[c for c in matches if not c['id'].startswith('X')]
    boundary=[c for c in matches if c['id'].startswith('X')]
    channel=('still_or_proxy_with_context' if visual and boundary else
             'visible_proposal' if visual else boundary[0]['evidence_mode'])
    routes.append(dict(**k,route=channel,visual_card_ids=[c['id'] for c in visual],
      boundary_card_ids=[c['id'] for c in boundary],
      source_refs=sorted({s for c in matches for s in c['source_refs']}),
      review_status='research_mapping_only; not per-term medical certification or native approval'))
dump('keyword-routes.json',routes)
dump('seed-keywords.json',dict(conversation_id='6ad9bf80-f358-83ec-a33b-134542ed0c4d',
 title='메디컬 호러 용어 정리',read_thread_limit_chars=20000,read_thread_truncated=True,
 recovery='logged-in Chrome DOM: 13 terminology tables, 11 work rows, 7 combination rows, 4 historical examples',
 terms=seeds,works=context.WORKS,historical_examples=['Tuskegee','Henrietta Lacks / HeLa','Eugenic sterilization','Anatomical body trade'],
 combinations=[dict(title=t,cards=c.split(','),visible_proposal=v,nonvisual_limit=l) for t,c,v,l in context.COMBINATIONS]))

catalog=json.loads((ASSETS/'photo_candidate_slot_catalog.json').read_text())['slot_catalog']
drafts=[]
for c in cards:
    if c['id'].startswith('X'):continue
    for slot in c['proposed_slots']:assert slot in catalog,(c['id'],slot)
    dims=sorted({d for s in c['proposed_slots'] for d in catalog[s]['dimensions']})
    drafts.append(dict(id='medical_draft_'+c['id'],card_id=c['id'],phrase_en=c['phrase_en'],phrase_ko=c['phrase_ko'],
       suggested_slots=c['proposed_slots'],proposed_dimension_review=dims,relations=c['relations'],
       condition_review=['fit independently frozen scene','preserve explicit person count and adult context where stated',
                         'preserve illustrative/fictional/staged mode where stated','all affected owner properties must be open'],
       effect_review='Inspect actual nouns, counts, placement, text, body geometry and occlusion; slot tags do not own effects.',
       source_refs=c['source_refs'],claim_limit_ko=c['claim_limit_ko'],confusion_boundaries=c['confusion_boundaries'],
       evidence_mode=c['evidence_mode'],render_gates=c['render_gates'],
       runtime_eligible=False,native_approval=False,status='inert bilingual authored draft; no CID/RID issued'))
dump('candidate-drafts.json',drafts)

# One immutable read per manifest module; lexical diagnostic is deliberately not retrieval.
manifest_raw=(ASSETS/'photo_candidate_corpus_manifest.json').read_bytes();manifest=json.loads(manifest_raw)
records={};owners={};bindings={};module_hashes={};text_fields={}
for mod in manifest['modules']:
    f=ASSETS/mod['file'];raw=f.read_bytes();module_hashes[mod['file']]=digest(raw);o=json.loads(raw)
    if mod['kind']=='candidates':
        for cid,r in o['candidates'].items():
            if cid in records:assert records[cid]==r,('conflicting_duplicate',cid)
            records[cid]=r;owners.setdefault(cid,[]).append(mod['file'])
    elif mod['kind']=='slot_bindings':bindings.update(o['slot_bindings'])
for cid,r in records.items():
    c=r['content'];text_fields[cid]={k:(c[k] if isinstance(c[k],str) else json.dumps(c[k],ensure_ascii=False)) for k in ['en','ko','definition','aliases'] if c.get(k)}
def fieldtext(v):return v if isinstance(v,str) else json.dumps(v,ensure_ascii=False)
def hit(term,txt):
    return bool(re.search(r'(?<![A-Za-z])'+re.escape(term)+r'(?![A-Za-z])',txt,re.I))
def terms_for(k):
    out=[k['en'],k['ko']]
    out+=k['en'].split(' / ')+k['ko'].split('·')
    if ', ' in k['en']:out+=k['en'].split(', ')
    return sorted(set(x.strip() for x in out if len(x.strip())>=3))
audit=[]
for k in seeds:
    terms=terms_for(k);hits=[]
    patterns={t:re.compile(r'(?<![A-Za-z])'+re.escape(t)+r'(?![A-Za-z])',re.I) for t in terms}
    for cid,fields in text_fields.items():
        matched={f:[t for t,p in patterns.items() if p.search(v)] for f,v in fields.items()}
        matched={f:v for f,v in matched.items() if v}
        if matched:hits.append(dict(cid=cid,record_kind=records[cid]['record_kind'],owner_modules=owners[cid],matched_fields=matched))
    audit.append(dict(seed_id=k['id'],term=k['en'],tested_terms=terms,hit_count=len(hits),hits=hits))
probes={}
for term in ['surgical drape','catheter','ventilator','dehiscence','fistula','specimen','hospital','organoid','consent','suture','retractor','medical','amputation']:
    probes[term]=[cid for cid,fields in text_fields.items() if any(hit(term,fieldtext(v)) for v in fields.values())]
selected=[]
for term in ['hospital','organoid','specimen','suture','medical','amputation']:
    ids=probes[term]
    # Include medical extension records before generic older lexical overlaps.
    ids=sorted(ids,key=lambda cid:(not any('biopunk' in o or 'scp' in o for o in owners[cid]),cid))
    for cid in ids[:3]:
        if cid not in [x['cid'] for x in selected]:
            selected.append(dict(cid=cid,matched_probe=term,owner_modules=owners[cid],record=records[cid],
              bindings={bid:b for bid,b in bindings.items() if b['candidate_id']==cid},
              record_sha256=digest(json.dumps(records[cid],ensure_ascii=False,sort_keys=True).encode()),
              status='full-source snapshot; semantic decision pending'))
dump('existing-source-mapping.json',selected)
drift=[name for name,h in module_hashes.items() if digest((ASSETS/name).read_bytes())!=h]
dump('CORPUS-LEXICAL-AUDIT.json',dict(schema='research-field-lexical-audit/v1',candidate_count=len(records),
 positive_count=sum(r['record_kind']!='diagnostic' for r in records.values()),binding_count=len(bindings),
 module_count=len(manifest['modules']),fixed_fields=['content.en','content.ko','content.definition','content.aliases'],
 excluded_fields=['source_refs','application_contract','research_semantics','provenance','generated index text'],
 method='case-insensitive whole English phrase boundaries; explicit slash and Korean middle-dot alternatives; no stemming or embeddings',
 limitation='zero lexical hit is not semantic absence; alias/definition hit is not a complete-source positive match',
 manifest_sha256=digest(manifest_raw),module_hashes=module_hashes,source_drift_during_read=drift,
 zero_hit_terms=sum(x['hit_count']==0 for x in audit),probe_counts={k:len(v) for k,v in probes.items()},terms=audit))

md('KEYWORD-ATLAS.md','# 원 대화 181개 용어의 처리 경로\n\n전체 연결은 개별 임상 정의의 검증 완료를 뜻하지 않는다. 가시 카드는 창작 실현이며 X 카드는 비가시 주장 경계다.\n\n| ID | 구역 | EN / KO | 가시 카드 | 경계 카드 | 경로 |\n|---|---|---|---|---|---|\n'+
 '\n'.join(f"| {r['id']} | {r['section']} | {r['en']} / {r['ko']} | {', '.join(r['visual_card_ids']) or '—'} | {', '.join(r['boundary_card_ids']) or '—'} | {r['route']} |" for r in routes))
lines=['# 시각 의미 카드','', '출처는 정의·경계의 근거다. 구체적 구도·소유 관계는 이번에 저술한 창작 제안이며 임상 사진 관찰 결과가 아니다.','']
for c in cards:
    lines.extend([f"## {c['id']} {c['title_ko']}",'',f"연결 용어: {'; '.join(c['seed_terms'])}",f"처리: {c['evidence_mode']} / {c['priority']}",''])
    if c['observable_components']:
        lines.extend([c['phrase_en'],'',c['phrase_ko'],'','관계: '+ '; '.join(f"{r['subject']} → {r['predicate']} → {r['object']}" for r in c['relations']),
                      '슬롯 제안: '+', '.join(c['proposed_slots']),'혼동: '+'; '.join(c['confusion_boundaries']),''])
    lines.extend(['주장 한계: '+c['claim_limit_ko'],'', '근거: '+', '.join(f"[{i} {src[i]['title']}]({src[i]['url']})" for i in c['source_refs']),
      '', '판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.',''])
md('VISUAL-CARDS.md','\n'.join(lines))
md('SCENE-DIRECTIONS.md','# 원 대화의 일곱 조합을 장면으로 전개\n\n조합을 자동 패키지로 채택하지 않는다. 각 장면은 독립 core 동결 후 필요한 카드만 검토한다.\n\n'+
 '\n\n'.join(f'## {i+1}. {t}\n\n선택 가능한 카드: {c}.\n\n보이는 제안: {v}.\n\n남는 문맥: {l}.' for i,(t,c,v,l) in enumerate(context.COMBINATIONS)))
md('ACCESS-LIMITS.md',f'# 출처 접근·사용 한계\n\n출처 {len(sources)}개를 실제 읽은 범위로 구분했다. 요약·검색 본문 확인을 논문·책 전체 읽음으로 표현하지 않는다. 서지·정의 확인은 이미지 관찰·시술 유효성·법적 판단·현재 기술 승인 증거가 아니다.\n\n'+
 '\n'.join(f"- [{s['id']} {s['title']}]({s['url']}): {s['access_status']}. {s['claim_limit_ko']}" for s in sources)+
 '\n\nNIH-Lacks 페이지는 처음 www 주소에서 403이었으나 공식 grants.nih.gov 검색 본문으로 1951년 비동의 채취와 2013년 합의를 재확인했다. 상세 자료 접근 조건은 실제 적용 시 재확인한다. 참조 대화의 American Mary, Re-Animator는 이번에 작품별 원문을 별도 검증하지 않았고, 장면별 프레임 검토도 하지 않았다. 모든 원문 이미지·영상은 미다운로드·미검토다.')
dump('SUMMARY.json',dict(seed_terms=len(seeds),visible_cards=len(drafts),context_cards=len(context.CONTEXTS),
 cards=len(cards),drafts=len(drafts),sources=len(sources),works=len(context.WORKS),combinations=len(context.COMBINATIONS),
 corpus_candidates=len(records),corpus_bindings=len(bindings),corpus_modules=len(manifest['modules']),
 lexical_zero_terms=sum(x['hit_count']==0 for x in audit),source_drift_during_read=drift,
 runtime_mutated=False,embedding_calls=0,image_calls=0,retrieval_run=False,pixel_review=False))
print(json.dumps(json.loads((OUT/'SUMMARY.json').read_text()),ensure_ascii=False))
