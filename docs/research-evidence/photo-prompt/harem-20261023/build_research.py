"""Build research-only JSON/Markdown. Does not write operational skill files."""
from pathlib import Path
import json, collections
from reference_inventory import inventory
from research_sources import sources
from research_cards import cards

HERE=Path(__file__).resolve().parent

def write_json(name,data):
 (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def build():
 keywords=inventory(); semantic=cards(); src=sources()
 lookup={k['id']:k for k in keywords}
 for k in keywords:
  linked=[c for c in semantic if k['id'] in c['keyword_ids']]
  k['card_ids']=[c['id'] for c in linked]
  k['definition_status']='source_scoped_review_only_not_universal_definition'
  if k['section']==20:
   k.update(route='combination_blueprint',reason='원 대화의 창작 조합. SCENE-BLUEPRINTS.md에서 독립 장면으로 구체화; 작품 고증 예시 아님.')
  elif linked:
   k.update(route='visual_or_proxy_with_context' if any(c['mode']!='context' for c in linked) else 'context_only',
    reason='카드의 가시 gate와 비동치 경계를 함께 읽음. 키워드 연결은 동의어·전형·자동 활성화 승인이 아님.')
  elif k['section'] in [13,14,15,16,17,18,19]:
   k.update(route='reuse_or_detail_research_pending',reason='기존 전체 source 의미·조건·효과·binding 및 구체 형태를 후속 심사. 새 후보 부재나 exact 동의어를 뜻하지 않음.')
  else:
   k.update(route='context_detail_pending',reason='장르·성격·배경·시간·의도에 해당. 각 속어의 독립 정의 확인 또는 선택적 대리 장면 저술이 추가로 필요.')
 drafts=[]
 for c in semantic:
  if c['mode']=='context': continue
  drafts.append(dict(draft_id='DRAFT-'+c['id'],card_id=c['id'],label_ko=c['label_ko'],
   en=c['positive_en'],ko=c['positive_ko'],suggested_slots=c['suggested_slots'],
   prerequisites='Independently declared owners, participant count and selected visual state; no invented relationship, age, consent or backstory.',
   conditions_review_required=True,effects_review_required=True,owner_binding_review_required=True,
   research_owner_nodes=c['research_owner_nodes'],research_relations=c['research_relations'],
   acceptance_gate=c['observable_gate'],confusion_boundary=c['confusion_boundary'],
   priority='P0' if c['id'].startswith('H') else 'P1',source_ids=c['source_ids'],
   native_qualification='NOT_RUN',runtime_importable=False))
 write_json('sources.json',dict(schema='harem-research-sources/v1',sources=src))
 write_json('keyword-routes.json',dict(schema='harem-keyword-research-routes/v1',
  conversation_id='6adb5af5-62c0-83ee-ac08-0af3cfba439a',capture='Visible Chrome DOM; exact first cells transcribed in reference_inventory.py',
  term_rows=314,combination_rows=6,keywords=keywords))
 write_json('semantic-cards.json',dict(schema='harem-research-semantic-cards/v1',runtime_importable=False,cards=semantic))
 write_json('candidate-drafts.json',dict(schema='harem-research-drafts/v1',runtime_importable=False,drafts=drafts))
 atlas=['# 전체 키워드 연결','', '314개 용어 행 + 6개 창작 조합. 원 표의 묶음 표제는 분해해 숫자를 늘리지 않았다. 모든 표제가 독립 외부 검증을 마쳤다는 뜻은 아니다.','',
 '|ID|원 표제|연결 카드|처리|','|---|---|---|---|']
 for k in keywords: atlas.append(f"|{k['id']}|{k['term']}|{', '.join(k['card_ids']) or '—'}|{k['route']}|")
 (HERE/'KEYWORD-ATLAS.md').write_text('\n'.join(atlas)+'\n')
 page=['# 시각 의미 카드','', '모든 positive는 선택 가능한 연구자 저술이다. source는 지정 어휘/문맥의 근거이며 모든 장면 geometry를 증명하지 않는다. 그래프는 심사 메모다.','']
 for c in semantic:
  page += [f"## {c['id']} {c['label_ko']} — {c['mode']}",'',c['positive_ko'] or c['context_ko'],'',c['positive_en'] or c['context_en'],'',
   f"- gate: {c['observable_gate']}",f"- 경계: {c['confusion_boundary']}",
   f"- 검토 role: {', '.join(c['suggested_slots']) or '문맥 전용'}; 출처: {', '.join(c['source_ids']) or '외부 lexical 정의 확인 보류; 물리 장면은 연구자 저술'}",'']
 (HERE/'VISUAL-CARDS.md').write_text('\n'.join(page)+'\n')
 ledger=['# 출처와 실제 접근 범위','', '|ID|출처|접근|검토 범위|한계|','|---|---|---|---|---|']
 for s in src: ledger.append(f"|{s['id']}|[{s['publisher']}: {s['title']}]({s['url']})|{s['access']}|{s['read_scope']}|{s['limits']}|")
 (HERE/'SOURCES.md').write_text('\n'.join(ledger)+'\n')
 evaluation=[]
 for c in semantic:
  evaluation.append(dict(id='DEV-'+c['id'],kind='card_derived_development_not_holdout',card_id=c['id'],
   query_ko=c['positive_ko'] or c['context_ko'],query_en=c['positive_en'] or c['context_en'],
   evaluation='Physical selected relations must pass together; no promotion of nonvisual claims.' if c['mode']!='context' else 'Must not create positive visual proof from this context.',
   gate=c['observable_gate'],retrieval_status='NOT_RUN',adoption_status='NOT_RUN'))
 write_json('development-cases.json',dict(schema='harem-development-cases/v1',cases=evaluation,query_count=2*len(evaluation),independent_holdout=False))
 print(json.dumps(dict(keyword_rows=len(keywords),card_count=len(semantic),modes=dict(collections.Counter(c['mode'] for c in semantic)),draft_count=len(drafts),routes=dict(collections.Counter(k['route'] for k in keywords))),ensure_ascii=False))

if __name__=='__main__': build()
