#!/usr/bin/env python3
import csv,io,json
from pathlib import Path
from evaluation_data import DATA
HERE=Path(__file__).resolve().parent
cards=json.loads((HERE/'semantic-cards.json').read_text())['cards']
cases=[]
for c in cards:
    cases.append(dict(case_id='EX-'+c['card_id'],split='development_exact_realization',query_ko=c['proposal_ko'],query_en=c['proposal_en'],target=c['card_id'],expected='inspect optional whole-source compatibility; no hidden semantic proof',execution='NOT_RUN',holdout=False))
for n,line in enumerate(DATA.strip().splitlines(),1):
    kind,ko,en,target=line.split('|')
    cases.append(dict(case_id=f'{kind.upper()}-{n:03}',split=kind,query_ko=ko,query_en=en,target=target,expected='manual relation-specific relevance and scope review',execution='NOT_RUN',holdout=False))
(HERE/'evaluation-cases.json').write_text(json.dumps(dict(schema='space-horror-evaluation-plan/v1',cases=cases,limitation='all cases were authored with access to this research; none is an independent frozen holdout'),ensure_ascii=False,indent=2)+'\n')
out=io.StringIO();w=csv.writer(out,delimiter='\t');w.writerow(['case_id','split','query_ko','query_en','target','execution'])
for c in cases:w.writerow([c[x] for x in ['case_id','split','query_ko','query_en','target','execution']])
(HERE/'EVALUATION-CASES.tsv').write_text(out.getvalue())
print(json.dumps(dict(cases=len(cases),bilingual_queries=2*len(cases),execution='NOT_RUN')))
