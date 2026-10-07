from pathlib import Path
import hashlib,json,sys
from collections import defaultdict
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parent.parent
RUN=ROOT/'run'
ASSETS=ROOT/'skill/assets'
sys.path.insert(0,str(ROOT/'tool-final'))
from tools.photo_data_maintenance.report import load_report
from tools.photo_data_maintenance.links import query

manifest=json.loads((ASSETS/'photo_prompt_source_manifest.json').read_text())
source_kinds={'photo_prompt_tags.json':'candidate','photo_prompt_visual_obligations.json':'visual_profile'}
source_kinds.update({r['file']:r['kind'] for r in manifest['sources']})
raw_nodes={}
raw_refs={}
raw_bundles={}
parsed={}
candidate_ids=defaultdict(list)
for filename,kind in source_kinds.items():
    if kind not in {'candidate','visual_profile'}:
        continue
    payload=json.loads((ASSETS/filename).read_text())
    parsed[filename]=payload
    if kind=='candidate':
        for slot,rows in payload.get('slots',{}).items():
            for i,row in enumerate(rows):
                nid=f"slot:{slot}:{row['id']}"
                assert nid not in raw_nodes,nid
                raw_nodes[nid]=row
                raw_refs[nid]={'file':filename,'pointer':f'/slots/{slot}/{i}'}
                candidate_ids[row['id']].append(nid)
        for i,row in enumerate(payload.get('visual_semantics',[])):
            if not row.get('candidate_ids'):
                continue
            bid='bundle:'+row['id']
            assert bid not in raw_bundles,bid
            raw_bundles[bid]=row
            raw_refs[bid]={'file':filename,'pointer':f'/visual_semantics/{i}'}
    else:
        for i,row in enumerate(payload.get('profiles',[])):
            nid='profile:'+row['id']
            assert nid not in raw_nodes,nid
            raw_nodes[nid]=row
            raw_refs[nid]={'file':filename,'pointer':f'/profiles/{i}'}

# Expected relationships come directly from authored candidate_ids,
# candidate_slots and hard_profile_ids. Report compiled member_candidates and
# the maintenance build_links implementation are not the expected-value source.
expected_edges=set()
bundle_members={}
bundle_profiles={}
for bid,row in raw_bundles.items():
    members=[]
    for entry_id in row['candidate_ids']:
        slot=(row.get('candidate_slots') or {}).get(entry_id)
        if entry_id.startswith('slot:'):
            nid=entry_id
        elif slot:
            nid=f'slot:{slot}:{entry_id}'
        else:
            matches=candidate_ids[entry_id]
            assert len(matches)==1,(bid,entry_id,matches)
            nid=matches[0]
        assert nid in raw_nodes,(bid,nid)
        members.append(nid)
        expected_edges.add((nid,'member_of',bid))
    profile_ids=list(row.get('hard_profile_ids',[]))
    if row.get('hard_profile_id'):
        profile_ids.append(row['hard_profile_id'])
    profiles=sorted({'profile:'+pid for pid in profile_ids})
    for pid in profiles:
        assert pid in raw_nodes,(bid,pid)
        expected_edges.add((bid,'associated_with',pid))
    bundle_members[bid]=sorted(set(members))
    bundle_profiles[bid]=sorted(set(profiles))
report=load_report(RUN/'management-final-report',require_links=True)
actual_edges={(e['source'],e['type'],e['target']) for e in report['links']['edges']}
actual_nodes={n['id']:n for n in report['inventory']['nodes']}
raw_all_nodes=set(raw_nodes)|set(raw_bundles)
pack=json.loads((RUN/'candidate_pack.json').read_text())[0]
exposed=sorted({c['id'] for s in pack['slots'].values() for c in s['candidates']})
related_profiles={pid for bid,members in bundle_members.items() if set(members)&set(exposed) for pid in bundle_profiles[bid]}
related_profiles.update('profile:'+c['profile_id'] for c in pack['semantic_clarification']['candidates'] if c.get('profile_id'))
related_profiles.update('profile:'+pid for b in pack['candidate_bundles']['candidates'] for pid in b['associated_profile_ids'])
exposed_bundles=sorted(b['id'] for b in pack['candidate_bundles']['candidates'])

def expected_paths(nid):
    paths=[]
    if nid.startswith('slot:'):
        for bid,members in bundle_members.items():
            if nid in members:
                profiles=bundle_profiles[bid]
                paths.extend([[nid,bid,pid] for pid in profiles] or [[nid,bid]])
    elif nid.startswith('profile:'):
        for bid,profiles in bundle_profiles.items():
            if nid in profiles:
                members=bundle_members[bid]
                paths.extend([[member,bid,nid] for member in members] or [[bid,nid]])
    else:
        members=bundle_members[nid]; profiles=bundle_profiles[nid]
        if profiles:
            paths.extend([[member,nid,pid] for member in members for pid in profiles])
        else:
            paths.extend([[member,nid] for member in members])
    return sorted(paths)

results={}
comparisons=[]
files_checked={}
for nid in [*exposed,*sorted(related_profiles),*exposed_bundles]:
    result=query(report['inventory'],report['links'],nid,report['reviews'])
    result.update({'generation_id':report['manifest']['binding']['generation_id'],'source_fingerprint':report['manifest']['binding']['source_fingerprint'],'freshness':'pinned_report'})
    results[nid]=result
    actual=sorted(p['nodes'] for p in result['paths'])
    expected=expected_paths(nid)
    path_entities=set([nid]+[n for path in expected for n in path])
    refs_ok=True
    for entity in path_entities:
        expected_ref=raw_refs[entity]
        refs_ok=refs_ok and expected_ref in actual_nodes[entity]['source_refs']
        filename=expected_ref['file']
        sha=hashlib.sha256((ASSETS/filename).read_bytes()).hexdigest()
        files_checked[filename]={'source_sha256':sha,'report_snapshot_sha256':report['manifest']['files'].get('inputs/'+filename),'match':sha==report['manifest']['files'].get('inputs/'+filename)}
    comparisons.append({'node':nid,'kind':result['kind'],'expected_paths_from_original_json':expected,'actual_query_paths':actual,'paths_match':expected==actual,'source_refs_match_original':refs_ok,'meaning_not_inferred':all(p['meaning_support']=='not_inferred' for p in result['paths']),'profile_activation_independent':result['profile_activation']=='independent_request_evidence_only','normal_unlinked':not expected})
comparison={
 'checked_at_utc':datetime.now(timezone.utc).isoformat(),
 'oracle':'actual original skill/assets JSON; independent reconstruction of explicit candidate_ids/candidate_slots -> visual_semantics -> hard_profile_id or hard_profile_ids references',
 'generation_id':report['manifest']['binding']['generation_id'],
 'source_root':str(ROOT/'skill'),
 'raw_candidate_count':sum(nid.startswith('slot:') for nid in raw_nodes),
 'raw_profile_count':sum(nid.startswith('profile:') for nid in raw_nodes),
 'raw_bundle_count':len(raw_bundles),
 'raw_node_set_matches_report':raw_all_nodes==set(actual_nodes),
 'expected_edge_count':len(expected_edges),'actual_edge_count':len(actual_edges),
 'all_edges_match_original':expected_edges==actual_edges,
 'missing_edges':sorted(expected_edges-actual_edges),'unexpected_edges':sorted(actual_edges-expected_edges),
 'exposed_slot_candidate_count':len(exposed),
 'candidate_query_count':len(exposed),'profile_query_count':len(related_profiles),'bundle_query_count':len(exposed_bundles),
 'candidate_nodes_with_paths':sum(bool(results[nid]['paths']) for nid in exposed),
 'candidate_normal_unlinked_count':sum(not results[nid]['paths'] for nid in exposed),
 'all_query_paths_match':all(r['paths_match'] for r in comparisons),
 'all_source_refs_match':all(r['source_refs_match_original'] for r in comparisons),
 'all_original_file_hashes_match_report':all(r['match'] for r in files_checked.values()),
 'association_promoted_to_meaning_or_required_activation':not all(r['meaning_not_inferred'] and r['profile_activation_independent'] for r in comparisons),
 'files_checked':files_checked,'comparisons':comparisons
}
(RUN/'final_tool_management_queries.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
(RUN/'final_tool_independent_graph_comparison.json').write_text(json.dumps(comparison,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in comparison.items() if k not in {'comparisons','files_checked'}},ensure_ascii=False,indent=2))
assert comparison['raw_node_set_matches_report']
assert comparison['all_edges_match_original']
assert comparison['all_query_paths_match']
assert comparison['all_source_refs_match']
assert comparison['all_original_file_hashes_match_report']
assert not comparison['association_promoted_to_meaning_or_required_activation']
