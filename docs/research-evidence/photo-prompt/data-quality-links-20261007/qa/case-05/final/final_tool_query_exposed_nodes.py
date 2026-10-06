import json, sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'tool-final'))
from tools.photo_data_maintenance.report import load_report
from tools.photo_data_maintenance.links import query
run=root/'run'
report=load_report(run/'management-final-report',require_links=True)
pack=json.loads((run/'candidate_pack.json').read_text())[0]
exposed=sorted({row['id'] for slot in pack['slots'].values() for row in slot['candidates']})
forward=[query(report['inventory'],report['links'],node,report['reviews']) for node in exposed]
related={n for result in forward for n in result['unique_related_nodes'] if n.startswith(('bundle:','profile:'))}
related.update('profile:'+row['profile_id'] for row in pack['semantic_clarification']['candidates'] if row.get('profile_id'))
related.update(row['id'] for row in pack['candidate_bundles']['candidates'])
reverse=[query(report['inventory'],report['links'],node,report['reviews']) for node in sorted(related)]
result={'schema':'independent-qa-query-evidence/v1','query_api':'tools.photo_data_maintenance.links.query; same public function used by CLI','report_binding':report['manifest']['binding'],'freshness':'pinned_report','forward':forward,'reverse':reverse}
(run/'final-tool-exposed-query-evidence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
summary={'forward_nodes':len(forward),'forward_paths':sum(x['path_count'] for x in forward),'unlinked_exposed':[x['node'] for x in forward if x['path_count']==0],'reverse_nodes':len(reverse),'reverse_paths':sum(x['path_count'] for x in reverse),'reverse_ids':[x['node'] for x in reverse],'output':str(run/'final-tool-exposed-query-evidence.json')}
print(json.dumps(summary,ensure_ascii=False,indent=2))
