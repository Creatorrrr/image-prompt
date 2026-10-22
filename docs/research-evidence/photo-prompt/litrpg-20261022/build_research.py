"""Build research artifacts only. Does not import retrieval or edit operating sources."""
import collections, csv, hashlib, json, re, sys
from pathlib import Path
from research_data import DATE, REFERENCE_ID, REFERENCE_COUNTS, TAIL_TABLES, SOURCE_ROWS, CARD_ROWS, ROUTE_ROWS

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
def sha(b): return hashlib.sha256(b).hexdigest()
def dump(name,x): (HERE/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def md(name,lines): (HERE/name).write_text('\n'.join(lines)+'\n')
sources=[]
for row in SOURCE_ROWS.splitlines():
 sid,title,url,access,claim=row.split('|')
 sources.append(dict(id=sid,title=title,url=url,access=access,supported_claim_and_limit_ko=claim,checked_on_kst=DATE,geometry_support='definition_or_case_context; all draft scene geometry is independently authored'))
dump('sources.json',sources)
tables=collections.defaultdict(list); table=-1
for line in (HERE/'REFERENCE-PREFIX.md').read_text().splitlines():
 if line.startswith('| **'):
  if line.startswith('| **LitRPG'): table=0
  label=line.split('|')[1].strip().replace('**','')
  tables[table].append(label)
 elif line.startswith('| 용어 |') and tables[table]: table+=1
# Prefix stops inside Dubcon, which lacks a complete markdown row.
if tables[9] and tables[9][-1].startswith('Dubcon'): tables[9].pop()
for i,block in TAIL_TABLES.items(): tables[i].extend(block.splitlines())
assert [len(tables[i]) for i in range(18)]==REFERENCE_COUNTS, [len(tables[i]) for i in range(18)]
cards=[]
slot_map={'표시 매체':['surreal_concept','surface_material','prop_placement'],'정보 구조':['visible_text','object_structure'], '퀘스트·경제':['prop','contact_point'],'전투·협업':['relational_action','participant_role'],'세계·성장 주체':['location','object_structure'],'죽음·이력':['narrative_clue','visible_text'],'폭력·신체':['prop_state','transformation_stage'],'관계·권한':['visible_text','relational_action'],'UI 구성':['visible_text','visual_hierarchy']}
catalog=json.loads((ASSETS/'photo_candidate_slot_catalog.json').read_text())['slot_catalog']
for line in CARD_ROWS.splitlines():
 cid,family,title,mode,src,owner_str,rel_str,en,ko,limits=line.split('|')
 diagnostic=mode in ('context','sequence')
 owners=dict(x.split('=',1) for x in owner_str.split(';')) if not diagnostic else {}
 relations=[dict(zip(('subject','predicate','object'),x.split('>'))) for x in rel_str.split(';')] if not diagnostic else []
 cards.append(dict(id=cid,family=family,title_ko=title,evidence_mode=mode,source_ids=src.split(),source_role='concept_or_precedent_only; authored proposal is not a source quotation',owners=owners,relations=relations,phrase_en=en,phrase_ko=ko,confusion_and_limits_ko=limits.split(';'),proposed_slots=[s for s in slot_map.get(family,[]) if s in catalog],context_requirement=en if diagnostic else None,pixel_gates=[] if diagnostic else [dict(id=f'{cid}-owners',requirement='Every named owner and part is separately recognizable in one evidence unit.'),dict(id=f'{cid}-relations',requirement='All listed directed relations and their endpoints are visible together.'),dict(id=f'{cid}-meaning',requirement='Read labels needed for the displayed claim; appearance alone must not substitute for them.')],failure_policy='partial_is_fail; UNOBSERVABLE_NOT_PASS',native_approval=False))
byid={c['id']:c for c in cards}
supp={13:'U07 I01 U01 E06 I04 U04 U03',14:'I01 U02 U08 U08 U06 U05',15:'U01 I01 I01 C06 U06 U03 U04 U05 X12 E05 H03 R04',16:'U07 E06 X18 U06 X18',17:'X02 Q06 X17 X17 X18 X18 U01 U01 X02 X04 X09 X07'}
routes=[]
for t in range(18):
 ids=(ROUTE_ROWS[t] if t<13 else supp[t]).split()
 assert len(ids)==len(tables[t]),(t,len(ids),len(tables[t]))
 for n,(label,cid) in enumerate(zip(tables[t],ids),1):
  routes.append(dict(id=f'T{t+1:02d}R{n:02d}',table=t,row=n,label=label,kind='term' if t<13 else 'reference_or_design_question',card_ids=[cid],mode=byid[cid]['evidence_mode'],advisory_only=True,auto_obligation=False))
# Explicit second routes preserve distinctions lost by broad families.
extra={'T01R20':['X01'],'T02R09':['U06'],'T03R13':['X04'],'T04R10':['X05'],'T04R18':['I01'],'T04R20':['X08'],'T06R12':['Q08'],'T06R15':['Q07'],'T06R19':['Q04'],'T08R03':['X07'],'T09R04':['X13'],'T10R05':['X09'],'T10R06':['X09'],'T10R19':['X09'],'T10R20':['X09'],'T10R21':['X08'],'T10R22':['X10'],'T10R23':['R01'],'T10R26':['R05'],'T10R27':['R05'],'T11R01':['U01'],'T11R05':['U03'],'T11R14':['Q07'],'T11R20':['U02'],'T11R22':['X17'],'T11R24':['X16'],'T12R05':['X02'],'T13R01':['U01']}
for r in routes:
 r['card_ids']+=extra.get(r['id'],[])
for c in cards:c['keyword_route_ids']=[r['id'] for r in routes if c['id'] in r['card_ids']]
drafts=[]
for c in cards:
 if c['evidence_mode'] in ('context','sequence'):continue
 drafts.append(dict(id='draft_litrpg_'+c['id'].lower(),card_id=c['id'],record_kind='research_visual_option_draft',content={'en':c['phrase_en'],'ko':c['phrase_ko']},owners=c['owners'],relations=c['relations'],source_ids=c['source_ids'],keyword_route_ids=c['keyword_route_ids'],proposed_slots=c['proposed_slots'],activation_conditions=['Explicit compatible requester meaning or open agent-owned staging dimension.','Review complete bilingual source meaning and all owners before adoption.','Displayed values remain claims made by the depicted display.'],exclusions=c['confusion_and_limits_ko'],native_approval=False,index_registered=False,application_contract='Keep every owner, part, count, state and directed endpoint of this whole authored realization. Citation, aliases, research graphs and proposed slots create no native facts, permissions, selection or qualification. A displayed claim does not prove truth or historical causation.'))
dump('reference-register.json',{'conversation_id':REFERENCE_ID,'url':'https://chatgpt.com/c/'+REFERENCE_ID,'title':'LitRPG 용어 조사 설명','read_thread_prefix_chars':20000,'browser_body_chars':28740,'access_note':'read_thread truncated; all 18 rendered tables inspected through CUA DOM. Labels after the prefix manually transcribed from observed table extraction; full body not archived.','table_counts':REFERENCE_COUNTS,'tables':[dict(index=i,labels=tables[i]) for i in range(18)]})
dump('keyword-routes.json',routes);dump('semantic-cards.json',cards);dump('candidate-drafts.json',drafts)
md('KEYWORD-ATLAS.md',['# 참조 대화 전체 키워드 경로','', '255개 용어 행과 42개 작품·스타일·설계 질문 행. 같은 행의 영문·국문·슬래시 표현을 서로 독립된 개념 수로 부풀리지 않는다. 경로는 조사를 찾기 위한 연결이며 자동 트리거가 아니다.','', '| 원문 행 | 용어 또는 참조 항목 | 연구 카드 | 증거 종류 |','|---|---|---|---|']+[f"| {r['id']} | {r['label']} | {', '.join(r['card_ids'])} | {r['mode']} |" for r in routes])
lines=['# 시각 의미 카드','', '모든 구체적 장면은 이번 연구에서 작성한 선택적 실현이다. 출처가 이 기하학이나 재질을 직접 규정했다는 뜻이 아니다.','']
for c in cards:
 lines += [f"## {c['id']} {c['title_ko']}",'',f"분류: {c['family']} / {c['evidence_mode']}. 근거: {', '.join(c['source_ids'])}.",'',c['phrase_ko'],'',c['phrase_en'],'', '소유자: '+json.dumps(c['owners'],ensure_ascii=False), '', '관계: '+('; '.join(f"{r['subject']} → {r['predicate']} → {r['object']}" for r in c['relations']) or '시각 후보 없음. 문맥 또는 연속 증거 필요.'),'','혼동 경계: '+'; '.join(c['confusion_and_limits_ko']), '']
md('VISUAL-CARDS.md',lines)
md('CANDIDATE-ATLAS.md',['# 후보 초안','', '운영 후보 등록 이전의 완전한 양언어 실현 초안. 개별 효과·조건·전체 원문·native source 검토가 남아 있다.','', '| 초안 | 카드 | 제안 슬롯 | 한국어 실현 |','|---|---|---|---|']+[f"| {c['id']} | {c['card_id']} | {', '.join(c['proposed_slots']) or 'slot review pending'} | {c['content']['ko']} |" for c in drafts])
md('SOURCES.md',['# 출처와 접근 한계','', '확인일: 2026-10-22 KST. body는 텍스트 확인이며 픽셀 관찰을 뜻하지 않는다. 제한된 페이지는 확인된 근거로 승격하지 않는다.','']+[f"- **{s['id']} [{s['title']}]({s['url']})** — `{s['access']}`. {s['supported_claim_and_limit_ko']}" for s in sources])

if '--keep-corpus-snapshot' in sys.argv:
 counts=json.loads((HERE/'COUNTS.json').read_text())
 counts.update(sources=len(sources),source_access=dict(collections.Counter(s['access'] for s in sources)),semantic_cards=len(cards),evidence_modes=dict(collections.Counter(c['evidence_mode'] for c in cards)),candidate_drafts=len(drafts))
 dump('COUNTS.json',counts)
 print(json.dumps({'research_regenerated':True,'historical_corpus_snapshot_preserved':True,'cards':len(cards),'drafts':len(drafts),'sources':len(sources)}))
 raise SystemExit(0)

# Source-only lexical diagnostic: selected positive prose fields, never aliases/tags/retrieval.
FIELDS=('en','ko','definition','phrase_en','phrase_ko','composition_instruction','runtime_expression')
FOCUS={
 'status':r'status.?screen|stat.?screen|상태창|캐릭터.?시트',
 'hud':r'\bHUD\b|diegetic|world.space|screen.space|홀로그램',
 'resources':r'\bHP\b|\bMP\b|stamina|health.?bar|체력.?바|스태미나',
 'progression':r'level.up|skill.?tree|ability.?score|레벨업|스킬.?트리|능력치',
 'quest':r'\bquest\b|퀘스트',
 'inventory':r'\binventory\b|equipment.?slot|인벤토리|장비.?슬롯',
 'craft':r'crafting|recipe|socket|제작법|소켓',
 'combat':r'cooldown|aggro|taunt|재사용.?대기|쿨다운|어그로',
 'party':r'\bparty\b|\braid\b|\bhealer\b|파티|(?<![가-힣])레이드|힐러',
 'dungeon_core':r'dungeon.?core|던전.?코어',
 'death':r'respawn|permadeath|corpse.?run|리스폰|영구.?사망',
 'deck':r'deckbuild|draw.?pile|discard.?pile|덱빌딩|손패|버림패',
 'affinity':r'affection.?meter|relationship.?meter|호감도',
 'contract':r'soulbound|binding.?contract|귀속|구속.?계약',
 'viewer':r'spectator|sponsor|관전|성좌|후원',
 'glitch':r'glitch|corrupted.?UI|redaction|글리치|검열',
}
def strings(obj):
 if isinstance(obj,str):yield obj
 elif isinstance(obj,dict):
  for v in obj.values():yield from strings(v)
 elif isinstance(obj,list):
  for v in obj:yield from strings(v)
def positive(r):
 for k in FIELDS:
  yield from strings(r.get('content',{}).get(k,[]))
 for rid,branch in r.get('realizations',{}).items():
  if isinstance(branch,dict):
   for box in (branch,branch.get('content',{})):
    for k in FIELDS:yield from strings(box.get(k,[]))
manifest_path=ASSETS/'photo_candidate_corpus_manifest.json'; manifest_raw=manifest_path.read_bytes();manifest=json.loads(manifest_raw)
records={};bindings={};owners={};module_hashes={};duplicates=[]
for mod in manifest['modules']:
 f=mod['file'];raw=(ASSETS/f).read_bytes();module_hashes[f]=sha(raw);d=json.loads(raw)
 for cid,r in d.get('candidates',{}).items():
  if cid in records:duplicates.append(cid)
  records[cid]=r;owners[cid]=f
 bindings.update(d.get('slot_bindings',{}))
texts={cid:'\n'.join(positive(r)) for cid,r in records.items()}
focus=[];selected={}
for family,p in FOCUS.items():
 pat=re.compile(p,re.I);hits=[cid for cid,text in texts.items() if pat.search(text)]
 # Prefer already registered LitRPG for comparison, then shortest examples. Not relevance rank.
 shortlist=sorted(hits,key=lambda cid:('metafiction_existential_litrpg' not in owners[cid],len(texts[cid]),cid))[:3]
 focus.append(dict(family=family,pattern=p,lexical_record_count=len(hits),shortlist=shortlist))
 for cid in shortlist:selected.setdefault(cid,[]).append(family)
neighbors=[dict(cid=cid,module=owners[cid],families=families,record=records[cid],bindings={bid:b for bid,b in bindings.items() if b.get('candidate_id')==cid},record_sha256=sha(json.dumps(records[cid],sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()),review='pending_full_semantic_review',native_approval=False) for cid,families in selected.items()]
audit=dict(schema='litrpg-source-audit/v1',selected_fields=FIELDS,excluded=['aliases','tags','research_semantics','negative metadata'],manifest_sha256=sha(manifest_raw),module_sha256=module_hashes,candidate_count=len(records),binding_count=len(bindings),module_count=len(manifest['modules']),record_kinds=dict(collections.Counter(r.get('record_kind','unspecified') for r in records.values())),duplicate_ids=duplicates,focus=focus,changes_during_read=[f for f,h in module_hashes.items() if sha((ASSETS/f).read_bytes())!=h],manifest_changed_during_read=sha(manifest_path.read_bytes())!=sha(manifest_raw),runtime_search_performed=False,limit='Lexical diagnostic only: neither semantic absence, deduplication, retrieval exposure nor native adoption is proved.')
dump('CORPUS-AUDIT.json',audit);dump('existing-source-neighbors.json',neighbors)
counts=dict(term_rows=sum(REFERENCE_COUNTS[:13]),supplemental_rows=sum(REFERENCE_COUNTS[13:]),routes=len(routes),sources=len(sources),source_access=dict(collections.Counter(s['access'] for s in sources)),semantic_cards=len(cards),evidence_modes=dict(collections.Counter(c['evidence_mode'] for c in cards)),candidate_drafts=len(drafts),existing_records=len(records),existing_bindings=len(bindings),existing_modules=len(manifest['modules']),neighbor_records=len(neighbors),operating_data_modified=False,index_built=False,image_calls=0)
dump('COUNTS.json',counts)
print(json.dumps(counts,ensure_ascii=False,indent=2))
