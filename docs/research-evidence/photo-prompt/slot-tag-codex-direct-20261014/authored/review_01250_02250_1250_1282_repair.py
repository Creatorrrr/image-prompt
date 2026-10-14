"""Individually authored correction after direct reread of ordinal 1282."""
import json,sys
from pathlib import Path
r=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');sys.path.insert(0,str(r));import direct_review as d
p=json.loads((r/'packets/01250-250.json').read_text());a=r/'authored/review_01250_02250_01250_01500.json';v=json.loads(a.read_text());row=v['decisions'][32]
assert p['records'][row['candidate_id']]['content']['embedding_text']=='glitch anxiety as robot concept proof or scene anchor'
change=dict(pointer='/content/embedding_text',before='glitch anxiety as robot concept proof or scene anchor',after='glitch anxiety as an affective mood without proving a robot concept, identity or scene anchor',reason='Glitch anxiety names an affective atmosphere; it does not establish a robot subject, identity or selected reality-anchor relationship.')
if change not in row['corrections']:row['corrections'].append(change)
row['rejected_boundaries']=['The corrected cue expresses glitch anxiety only; no actual robot, robot identity, specific visible encoding artifact, or reality-anchor relation is supplied.']
d.write(a,v)
n=r/'worker-notes/review_01250_02250-01250-01500.json';note=json.loads(n.read_text());note['qualification_issues'].append({'ordinal':1282,'detail':'Directly reread full mood cue and authored exact embedding correction removing unsupported robot concept/identity/anchor proof. Positive English glitch anxiety remains the evidence for mood only.'});d.write(n,note)
data=d.source()
for i,row in enumerate(v['decisions'],1):d.validate_decision(dict(d.binding(data,row['candidate_id'])|row,schema=d.SCHEMA,reviewer='Codex',review_method='codex_direct_source_read',independent_human_review=False,packet_sha256=d.c.digest(p),authored_decision=dict(file=str(a),item=i,sha256=d.c.digest(row))),data)
print('First block ready: 250 rows validated with 1282 embedding correction')
