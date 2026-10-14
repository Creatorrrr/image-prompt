"""Same five manual drafts; explicit1612 negative grammar and whole placing-field anchors. Prior literal preserved."""
from pathlib import Path
p=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/authored/native_11870_01575_02250.01610_01615.author-149v6-v1.py')
s=p.read_text().replace('Do not add the actor, talisman, door, hand or tool; prescribe glue, a nail, pressure or final completed attachment; infer a religion, magic, readable inscription, ritual outcome or a location.','Do not add the actor, talisman, door, hand or tool. Do not prescribe glue, a nail, pressure or final completed attachment. Do not infer a religion, magic, readable inscription, ritual outcome or a location.')
s=s.replace("[('en','on a door'),('ko','문에'),('embedding_text','on a door'),('application_contract','talisman being affixed on that door at the selected placing instant')]","[('en','placing a talisman on a door'),('ko','문에 부적을 붙이는'),('embedding_text','placing a talisman on a door'),('application_contract','talisman being affixed on that door at the selected placing instant')]")
exec(compile(s,str(p)+'[manual_whole_anchor_v2]','exec'))
