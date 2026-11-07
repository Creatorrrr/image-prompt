import json,re,uuid
from pathlib import Path
R=Path('/Users/chasoik/Projects/image-prompt');O=Path(__file__).parent
report=(R/'docs/research/cosplay-visual-semantics-research-plan-20261106.md').read_text().split('## 2.')[1].split('## 3.')[0]
lookup={'캣수트':['C01'],'젠타이':['C02'],'태버드':['C03'],'오프숄더':['C04'],'콜드숄더':['C05'],'분리 소매':['C06'],'언더버스트':['C07'],'버슬':['C08'],'레이스업':['C09'],'메일·체인메일':['C10'],'폴드런':['C11'],'뱀브레이스':['C11'],'고르젯':['C12'],'브레스트플레이트·백플레이트':['C12'],'분리 커프스':['C13'],'바니수트':['C13'],'절대영역':['C14'],'가터':['C15'],'벨벳':['C16'],'스플릿 다이':['C18'],'아호게':['C19'],'히메컷':['C20'],'드릴 컬':['C21'],'망가 래시':['C22'],'인형':['C23','C47'],'오드아이 연출':['C24'],'케모노미미':['C25'],'깃털 날개':['C26'],'막날개':['C27'],'헤일로':['C28'],'아니메가오 키구루미':['C29'],'그리모어':['C30'],'스태프·완드':['C30','C32'],'발도':['C31'],'마법 시전':['C32'],'망토 펼치기':['C33'],'고양이 손·발 포즈':['C34'],'한쪽 무릎 꿇기':['C35'],'검을 세워 들기':['C36'],'등 맞대기':['C37'],'불안한 미소':['C38'],'배틀 대미지':['C40'],'오페라 글러브':['C42'],'오버니':['C43'],'마법소녀':['C44'],'아이돌':['C45'],'윙크':['C46'],'페티코트':['C47'],'퍼슈트':[]}
rows=[]
for line in report.splitlines():
 m=re.match(r'^(\d+(?:-\d+)?)\. \*\*(.*?) \((\d+); (.*?)\)\*\* — (.*)',line)
 if not m:continue
 sec,title,count,routes,rest=m.groups()
 if sec=='18':continue
 entries=rest.split('. ')[0].rstrip('.').split(', ');assert len(entries)==int(count),(sec,len(entries),count)
 for i,name in enumerate(entries,1):
  ids=sorted(set(code for term,codes in lookup.items() if term in name for code in codes))
  rows.append({'id':f'COS-T{sec}-{i:03}','section':title,'term_from_research_plan':name,'route_codes':routes,'new_example_ids':ids,'status':'example_added_further_semantic_review_needed' if ids else 'research_scope_only_further_comparison_needed'})
assert len(rows)==356
out={'schema':'cosplay-research-inventory/v1','source':'docs/research/cosplay-visual-semantics-research-plan-20261106.md#2','scope_note':'Rows transcribed in prior research from conversation tables. Links indicate associated examples, not complete coverage or semantic equivalence. Existing corpus reuse is not asserted without full review.','total_rows':len(rows),'rows':rows}
(O/'inventory.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('rows',len(rows),'with new-example link',sum(bool(r['new_example_ids']) for r in rows))
