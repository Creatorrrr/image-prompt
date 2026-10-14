import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
rows=json.loads((R/'authored/native_fresh_08250_17437_04_precision.json').read_text())['resolutions']
for r in rows[int(sys.argv[1]):int(sys.argv[2])]:
 f=r['fresh_canonical_fact'];rid=r['realization_id'];root='/content/realization_content/'+rid
 print(json.dumps({'index':r['reviewed_occurrence_index'],'class':r['issue_id'],'RID':rid,'local_pointer':r['exact_local_pointer'].replace(root,'{RID_ROOT}'),'local_quote':r['exact_local_quote'],'old_narrow_quote':r['historical_narrow_quote'],'old_mode':r['historical_mode'],'old_target':r['historical_target'],'old_property':r['historical_property'],'old_value':r['historical_typed_value'],'canonical':{k:f[k] for k in ['id','pointer','quote','dimension','target','property','mode','value']},'local_relation':r['fresh_local_reference_unit']['reference_relation'],'retained_local_facts':r['local_constraint_fact_ids']},ensure_ascii=False,separators=(',',':')))
