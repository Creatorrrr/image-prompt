"""Rebuild inert research outputs from authored proposals and current read-only source."""
import collections,csv,hashlib,json,re
from pathlib import Path
from research_cards import CARDS
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
def digest(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def read(p):return json.loads(p.read_text())
def write(name,x):(HERE/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def tsv(name,headers,rows):
    with (HERE/name).open('w',newline='') as f:
        w=csv.writer(f,delimiter='\t');w.writerow(headers);w.writerows(rows)

# Each row corresponds exactly to the original rendered table, in source order.
# Plus means contextual distinctions and optional examples, never all-of obligations.
ROUTES={
0:'K01 K01 K01 K01+R02 K01+R01 K01 K01 K03 K02+R06 K02+R20 R01 K02+R20 K01+R02 K01',
1:'K02+R07 K02 K02 K02+R06 K02 K03 K03 R11+K03 R09+R10+K03 R05 R37+K03 K03+R29',
2:'R07 R07 R07 K04+R09 K04 R06 K12+R47 K04+K02 K04 K04 K04+R09 R08 K04',
3:'K05+R03 K05+R15 K05 K05 R56+K05 R57 K06+R19 K06+R21 R21+R32 R18 R17 R17+K07 R16 R15 R20 R04',
4:'K07 K07+R47 R12+K07 K07 R12+K07 R17+K07 R13+K07 R13+K07 K07 K07+R39 R15 R14+K11',
5:'K08 K08 K08 K08',
6:'R22+R23 K09 K09 R31 K10 K10 K11 K11 K11 K11+R50',
7:'R28 R37+K15 R24+R25 R26 R27 R29 K26 K26+R44 R30 R04+K25',
8:'R46 K12+R46+R47 K12 K12 K12 K12 K12 R48 R49 R50 R51 K13+R46',
9:'K14+R52 K14+R53 K14 K14+R48 K14+R53 K14+R52 R53 K14+R54 R54 R55 K14+K18 K14',
10:'K15+R37 K15+R36 R37+K22 K15 K15 K15+R26 R41 K22 K15 R42 R43 K16 K16 K16+R44 R39+R40 K03 K15+K22',
11:'K17 K17 R37+K17 K17 K17 K17 K17 K19 K18 K18 K18 K18 K18',
12:'K20 K20 K20 K20 K05 K20 K05 R18 K20+R15 K20 K20 K20',
13:'R34 R34 K27+R28 K27+R28 R33 R36 K22 R35 R36 K27+R36',
14:'R44+K21 R44+K21 K21 K21 R45 K21 K21',
15:'K23 K23 K24 K24 R04+K25 K25 K25 K25 K25 K19 R38+K25',
}

def main():
    conversation=read(HERE/'conversation-dom.json');cards={c['card_id']:dict(c) for c in CARDS}
    sources=read(HERE/'sources.json');source_by_id={s['source_id']:s for s in sources}
    routes=[]
    for ti,route in ROUTES.items():
        data=conversation['tables'][ti][1:];mapped=route.split()
        assert len(data)==len(mapped),(ti,len(data),len(mapped))
        for ri,(row,ids) in enumerate(zip(data,mapped),1):
            refs=ids.split('+');assert all(r in cards for r in refs)
            routes.append(dict(seed_id=f'T{ti+1:02d}.{ri:02d}',table_index=ti,row_index=ri,
                original_term=row[0],conversation_definition=row[1],card_refs=refs,
                source_refs=sorted({s for c in refs for s in cards[c]['source_refs']}),
                routing_authority='research_seed_only; not runtime activation or verified alias',
                independent_definition_verification='partial; inspect card claim limits and source review scope',
                hard_visual_obligation=False))
    seed_refs=collections.defaultdict(list)
    for r in routes:
        for cid in r['card_refs']:seed_refs[cid].append(r['seed_id'])
    catalog=read(ASSETS/'photo_candidate_slot_catalog.json')['slot_catalog']
    for cid,c in cards.items():
        c['seed_refs']=seed_refs[cid]
        c['source_scope']=[dict(source_id=s,kind=source_by_id[s]['kind'],
            review_level=source_by_id[s].get('review_level','pending')) for s in c['source_refs']]
        if cid.startswith('R'):
            assert all(s in catalog for s in c['proposed_slots']), (cid,c['proposed_slots'])
            c['gates']=[dict(gate_id=cid+'.owners',criterion='Every declared owner is independently legible at the chosen review scale.',required_owners=list(c['owners']))]
            for i,e in enumerate(c['relations'],1):
                c['gates'].append(dict(gate_id=f'{cid}.relation{i}',criterion=f"{e['from']} {e['predicate']} {e['to']}; both endpoints and the connection/comparison must be readable in the same planned view.",required_owners=[e['from'],e['to']]))
            c['gates'].append(dict(gate_id=cid+'.whole',criterion='All selected components, counts, boundaries and relations must coexist; partial or unobservable evidence cannot pass the whole case.'))
            c['gates'].append(dict(gate_id=cid+'.bilingual',criterion='Both authored languages retain every declared material, owner, count, endpoint and claim limit; human meaning review required.'))
            if 'visible_text' in c['proposed_slots']:c['gates'].append(dict(gate_id=cid+'.text',criterion='Required identifiers, dates or stroke landmarks are actually readable at native resolution; invented unreadable glyphs cannot pass exact text.'))
            c['candidate_eligible']=True
    drafts=[]
    for cid,c in cards.items():
        if not c.get('candidate_eligible'):continue
        drafts.append(dict(draft_id='D-'+cid,card_ref=cid,registration_status='research_only_not_in_operating_manifest',
            proposed_disposition=c['adoption'],phrase_ko=c['proposal_ko'],phrase_en=c['proposal_en'],
            owner_components=c['owners'],directed_relations=c['relations'],source_refs=c['source_refs'],
            proposed_slots=c['proposed_slots'],affected_dimensions_proposal=sorted({d for s in c['proposed_slots'] for d in catalog[s]['dimensions']}),
            required_review='Whole canonical source + both languages + exact selected owner/property effects + all guards; tag/slot overlap gives no permission.',
            applicability='Only when compatible with the complete frozen request and all changed properties are open. Explicitly chosen full realization only; optional siblings never become all-of.',
            claim_limit_ko=c['claim_limit_ko'],confusion_boundary_ko=c['confusion_boundary_ko'],
            render_gates=c['gates'],runtime_candidate_id=None,runtime_realization_id=None,native_approval=False))
    write('keyword-routes.json',routes);write('semantic-cards.json',list(cards.values()));write('candidate-drafts.json',drafts)
    atlas=['# 참조 대화의 키워드 전체 경로','', '정의는 대화의 연구 seed다. 독립 원전 검증 범위는 카드·출처에서 확인한다. `+`는 관련 경로이며 동시 의무가 아니다.','', '| ID | 원 항목 | 카드 |','|---|---|---|']
    atlas += [f"| {r['seed_id']} | {r['original_term']} | {', '.join(r['card_refs'])} |" for r in routes]
    atlas += ['', '## 별도 보존한 보조 표', '', '혼동 정정 9행, 작품 안내 12행, 창작 조합 6행은 185개 용어와 합산하지 않는다.']
    (HERE/'KEYWORD-ATLAS.md').write_text('\n'.join(atlas)+'\n')
    md=['# 시각 의미 카드','', '모든 가시 실현은 선택형 저술 제안이다. 원전·단어 뜻이 구체 배치 전체를 인증하지 않는다.','']
    for c in cards.values():
        md += [f"## {c['card_id']} {c['title_ko']}",'',f"판정: `{c['mode']}` / 반영: `{c['adoption']}` / 우선순위: {c['priority']}",'',c.get('proposal_ko',c.get('meaning_ko','')),'']
        if c.get('proposal_en'):md += [c['proposal_en'],'']
        if c['owners']:md += ['소유자: '+ '; '.join(f'{k}={v}' for k,v in c['owners'].items()),'', '관계: '+ '; '.join(f"{e['from']} → {e['predicate']} → {e['to']}" for e in c['relations']),'']
        md += ['혼동 경계: '+c['confusion_boundary_ko'],'','주장 한계: '+c['claim_limit_ko'],'','출처: '+', '.join(f"[{s}]({source_by_id[s]['url']})" for s in c['source_refs']),'','기존 의미 카드: '+(', '.join(c['existing_card_refs']) or '이번 범위에서 직접 매핑 없음'), '']
    (HERE/'VISUAL-CARDS.md').write_text('\n'.join(md)+'\n')
    tsv('SOURCES.tsv',['id','title','url','kind','review_level','status','checked_scope','limit'],[[s['source_id'],s['title'],s['url'],s['kind'],s.get('review_level','pending'),s['access_status'],s['takeaway_ko'],s['claim_limit_ko']] for s in sources])
    tsv('REALIZATIONS.tsv',['draft','card','disposition','slots','ko','en','claim_limit'],[[d['draft_id'],d['card_ref'],d['proposed_disposition'],','.join(d['proposed_slots']),d['phrase_ko'],d['phrase_en'],d['claim_limit_ko']] for d in drafts])
    audit_corpus(routes,cards)
    stats=dict(keyword_routes=len(routes),semantic_cards=len(cards),candidate_drafts=len(drafts),sources=len(sources),
        cards_by_adoption=dict(collections.Counter(c['adoption'] for c in cards.values())),
        drafts_by_adoption=dict(collections.Counter(d['proposed_disposition'] for d in drafts)),
        cards_by_mode=dict(collections.Counter(c['mode'] for c in cards.values())),runtime_changes=0,embedding_calls=0,image_calls=0)
    write('COUNTS.json',stats);print(json.dumps(stats,ensure_ascii=False,indent=2))

def audit_corpus(routes,cards):
    manifest_bytes=(ASSETS/'photo_candidate_corpus_manifest.json').read_bytes()
    manifest=json.loads(manifest_bytes);candidates={};bindings={};owners={};modules={}
    for m in manifest['modules']:
        path=ASSETS/m['file'];raw=path.read_bytes();data=json.loads(raw);modules[m['file']]=digest(raw)
        if m['kind']=='candidates':
            for cid,c in data['candidates'].items():
                assert cid not in candidates; candidates[cid]=c;owners[cid]=m['file']
        if m['kind']=='slot_bindings':bindings.update(data['slot_bindings'])
    sem_path=ASSETS/'photo_cosmic_horror_semantics_20261021.json';registry=read(sem_path)
    old={c['id']:c for c in registry['cards']}
    ref_to_cids=collections.defaultdict(list)
    for cid,c in candidates.items():
        rid=c.get('content',{}).get('research_semantics',{}).get('card_id')
        if rid:ref_to_cids[rid].append(cid)
    requested=sorted({r for c in cards.values() for r in c['existing_card_refs']})
    mappings=[]
    for ref in requested:
        assert ref in old,ref
        records=[]
        for cid in ref_to_cids[ref]:
            own_bindings={bid:b for bid,b in bindings.items() if b.get('candidate_id')==cid}
            records.append(dict(candidate_id=cid,module=owners[cid],source_record_sha256=digest(canonical(candidates[cid])),record=candidates[cid],bindings=own_bindings,
                status='present_in_authored_manifest; native proof, installed release, selected RID, retrieval and pixels not established'))
        mappings.append(dict(existing_card_id=ref,existing_semantics=old[ref],semantics_module=str(sem_path.relative_to(ROOT)),semantic_record_sha256=digest(canonical(old[ref])),
            research_cards=[c['card_id'] for c in cards.values() if ref in c['existing_card_refs']],source_records=records))
    write('existing-source-mapping.json',mappings)
    texts={cid:' '.join(str(v) for k,v in c.get('content',{}).items() if k in ('en','ko','definition','phrase_en','phrase_ko','aliases')).casefold() for cid,c in candidates.items()}
    hits=[]
    for r in routes:
        parts=r['original_term'].split(' — ',1);en=parts[0];ko=parts[1] if len(parts)>1 else ''
        search=[x.strip() for x in re.split(r' / | /|/ |·',en) if len(x.strip())>2]
        if ko:search+=[ko]
        found=[cid for cid,txt in texts.items() if any(term.casefold() in txt for term in search)]
        hits.append(dict(seed_id=r['seed_id'],terms=search,exact_substring_source_record_count=len(found),sample_ids=found[:5]))
    changed_during_audit=[n for n,sha in modules.items() if digest((ASSETS/n).read_bytes())!=sha]
    manifest_changed=digest((ASSETS/'photo_candidate_corpus_manifest.json').read_bytes())!=digest(manifest_bytes)
    write('CORPUS-LEXICAL-AUDIT.json',dict(candidate_count=len(candidates),binding_count=len(bindings),slot_count=len(read(ASSETS/'photo_candidate_slot_catalog.json')['slot_catalog']),
        manifest_sha256=digest(manifest_bytes),module_sha256=modules,snapshot_consistency='COHERENT' if not changed_during_audit and not manifest_changed else 'SOURCE_CHANGED_DURING_AUDIT_REBASELINE',
        changed_during_audit=changed_during_audit,manifest_changed_during_audit=manifest_changed,primary_fields=['en','ko','definition','phrase_en','phrase_ko','aliases'],
        method='casefold exact-substring audit of declared fields; not token scoring, synonym search, embeddings, retrieval, or semantic absence proof',routes=hits))
    for ref in ('C119','C120','C126','C169','C173','C174'):
        rows=[m for m in mappings if m['existing_card_id']==ref]
        if rows:
            for c in rows[0]['source_records']:
                c['review_issue']='Full EN/KO meaning equivalence and relation endpoint completeness require human review; source record presence is not qualification.'
    write('existing-source-mapping.json',mappings)

if __name__=='__main__':main()
