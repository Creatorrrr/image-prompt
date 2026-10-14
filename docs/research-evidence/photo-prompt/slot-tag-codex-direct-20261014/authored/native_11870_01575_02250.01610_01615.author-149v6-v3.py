"""Manual1614 moving-with-frozen-reflection fullquote anchors; preserve prior drafts."""
import runpy
from pathlib import Path
q=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/authored/native_11870_01575_02250.01610_01615.author-149v6-v2.py');a=runpy.run_path(str(q));ROWS=a['ROWS'];I=a['I'];CAT=a['CAT'];digest=a['digest']
f=next(f for f in ROWS[4]['literal_native_facts']if f['id']=='movingE')
f['positive_evidence']=[{'pointer':'/content/en','positive_quote':'subject moves but the reflection stays frozen'},{'pointer':'/content/ko','positive_quote':'본체가 움직여도 반사는 멈춰 있음'},{'pointer':'/content/application_contract','positive_quote':'physical subjects motion while its corresponding reflection stays still'}]
if __name__=='__main__':
 import json
 print(json.dumps({'ordinal':1614,'whole_after':ROWS[4]['proposed_source_after'],'movingE':f},ensure_ascii=False,indent=2))
