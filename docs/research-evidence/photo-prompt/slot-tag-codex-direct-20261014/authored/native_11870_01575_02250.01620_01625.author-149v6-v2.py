"""Manual1620 field-local quote refinement and explicit negative grammar. Earlier literal immutable."""
from pathlib import Path
p=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/authored/native_11870_01575_02250.01620_01625.author-149v6-v1.py');s=p.read_text().replace('Do not add a body, chair, limb, foot, floor contact, armrest, controller or screen; infer laziness, sleep, emotion, gaming history or exact recline angle.','Do not add a body, chair, limb, foot, floor contact, armrest, controller or screen. Do not infer laziness, sleep, emotion, gaming history or exact recline angle.');exec(compile(s,str(p)+'[field_local_v2]','exec'))
r=ROWS[0];next(f for f in r['literal_native_facts']if f['id']=='poseE')['positive_evidence']=[{'pointer':'/content/application_contract','positive_quote':'human loosely slouched while seated and leaning in that same gaming chair'}]
next(u for u in r['whole_positive_source_units']if u['pointer']=='/content/ko')['fact_refs']=['chairP','supportE']
r['semantic_reference_plan'].append({'pointer':'/content/ko','full_quote':r['proposed_source_after']['content']['ko'],'canonical_App_fact_refs':['poseE'],'relation':'partial_restatement','reason':'KO explicitly seated/leaning andEnglishslouched detail are retained in the completeAppvalue, without forcingKOtoindependentlyassert everyEnglishslouch nuance.'})
for f in r['literal_native_facts']:
 if f['id']=='supportE':
  f['positive_evidence']=[{'pointer':'/content/ko','positive_quote':'게이밍 의자에 느슨하게 기대앉은'},{'pointer':'/content/application_contract','positive_quote':'Select that human loosely slouched while seated and leaning in that same gaming chair, retaining the actual chair support stated in Korean'}]
