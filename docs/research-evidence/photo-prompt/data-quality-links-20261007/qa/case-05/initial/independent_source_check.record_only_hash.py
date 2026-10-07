import hashlib, json
from collections import defaultdict
from pathlib import Path
root=Path(__file__).resolve().parents[1]
run=root/'run'; report_root=run/'maintenance-report'
inv=json.loads((report_root/'inventory.json').read_text())
nodes={row['id']:row for row in inv['nodes']}
evidence=json.loads((run/'exposed-query-evidence.json').read_text())
manifest=json.loads((report_root/'manifest.json').read_text())
cache={}; file_proof={}
def original(ref):
    filename=ref['file']
    path=root/'skill'/'assets'/filename
    assert path.resolve().is_relative_to((root/'skill/assets').resolve())
    if filename not in cache:
        raw=path.read_bytes()
        digest=hashlib.sha256(raw).hexdigest()
        assert digest==manifest['files']['inputs/'+filename], (filename,'source bytes differ from generation report input')
        assert raw==(report_root/'inputs'/filename).read_bytes(), (filename,'report source copy differs')
        cache[filename]=json.loads(raw)
        file_proof[filename]={'path':str(path),'sha256':digest}
    value=cache[filename]
    if ref['pointer']:
        for token in ref['pointer'].split('/')[1:]:
            token=token.replace('~1','/').replace('~0','~')
            value=value[int(token)] if isinstance(value,list) else value[token]
    return value
# Establish identities and candidate slot lookup without calling report/link implementation.
by_entry=defaultdict(set)
for node in nodes.values():
    if node['kind']=='candidate':
        by_entry[node['record']['id']].add(node['id'])
expected=set(); unresolved=[]; raw_bundles={}
for node in nodes.values():
    if node['kind']!='bundle':continue
    raw=original(node['source_refs'][0]); raw_bundles[node['id']]=raw
    assert node['id']=='bundle:'+raw['id']
    profiles=list(raw.get('hard_profile_ids') or [])
    if raw.get('hard_profile_id'):
        profiles.append(raw['hard_profile_id'])
    members=set()
    for cid in raw.get('candidate_ids') or []:
        if cid.startswith('slot:'):
            resolved={cid} if cid in nodes else set()
        elif cid in (raw.get('candidate_slots') or {}):
            named='slot:'+raw['candidate_slots'][cid]+':'+cid
            resolved={named} if named in nodes else set()
        else:
            resolved=by_entry.get(cid,set())
        if len(resolved)!=1:
            unresolved.append({'bundle':node['id'],'declared_member':cid,'possible_nodes':sorted(resolved)})
            continue
        members.update(resolved)
    assert set(node['record']['associated_profile_ids'])==set(profiles), (node['id'],'profile association differs from authored reference')
    if not any(row['bundle']==node['id'] for row in unresolved):
        assert {x['id'] for x in node['record']['member_candidates']}==members, (node['id'],'compiled members differ from raw declaration')
    for member in members:
        for pid in profiles:
            profile='profile:'+pid
            if profile in nodes:
                expected.add((member,node['id'],profile))
checked_nodes=set(); checked_refs=[]; candidate_source_checks=[]; path_checks=[]; query_checks=[]
for group in ['forward','reverse']:
    for result in evidence[group]:
        assert result['path_count']==len(result['paths'])
        actual={tuple(path['nodes']) for path in result['paths']}
        expected_for_node={p for p in expected if result['node'] in p}
        assert actual==expected_for_node, (result['node'],'missing or spurious authored path', sorted(actual-expected_for_node),sorted(expected_for_node-actual))
        query_checks.append({'node':result['node'],'direction':group,'path_count':len(actual),'expected_path_count':len(expected_for_node),'status':'PASS'})
        touched={result['node']}
        for path in result['paths']:
            triple=tuple(path['nodes']); assert triple in expected
            assert path['meaning_support']=='not_inferred'
            assert result['profile_activation']=='independent_request_evidence_only'
            assert path['relation']=='via_bundle'
            for node_id in path['nodes']:
                node=nodes[node_id]; assert path['source_refs'][node_id]==node['source_refs']
                assert path['entity_hashes'][node_id]==node['entity_sha256']
                touched.add(node_id)
            path_checks.append({'query_node':result['node'],'path_id':path['id'],'nodes':list(triple),'status':'PASS','source_refs':path['source_refs'],'meaning_support':'not_inferred'})
        for node_id in touched:
            if node_id in checked_nodes:continue
            checked_nodes.add(node_id); node=nodes[node_id]
            record=node['record']
            assert hashlib.sha256(json.dumps(record,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()==node['entity_sha256']
            for ref in node['source_refs']:
                raw=original(ref)
                assert raw['id']==record['id']
                if node['kind']=='candidate':
                    assert raw==record, (node_id,'candidate source record is not byte-equivalent as parsed JSON')
                    candidate_source_checks.append({'node':node_id,'source_ref':ref,'complete_record_equal':True})
                elif node['kind']=='profile':
                    # Compilers add obligations and normalized semantics; check independently authored identity/activation/components verbatim.
                    for key in ['category','activation','runtime_expression','authored_components','reject_substitutes']:
                        if key in raw:assert record.get(key)==raw[key], (node_id,key,'authored profile field changed')
                    if isinstance(raw.get('semantics'),dict):
                        for key,value in raw['semantics'].items():
                            assert record['semantics'].get(key)==value, (node_id,'semantics.'+key)
                checked_refs.append({'node':node_id,'kind':node['kind'],'source_ref':ref,'resolved_id':raw['id'],'status':'PASS'})
# Independently check the actual jointly associated relief realization.
bundle=nodes['bundle:orn_gd65_bundle']['record']; raw_bundle=raw_bundles['bundle:orn_gd65_bundle']
assert [x['id'] for x in bundle['components']]==[x['id'] for x in raw_bundle['component_groups']]
for comp,raw_comp in zip(bundle['components'],raw_bundle['component_groups']):
    assert comp['concept_units']==raw_comp['visible_evidence']
    assert comp['minimum_realizations']==1
assert bundle['profile_activation']=='independent_request_evidence_only'
pack=json.loads((run/'candidate_pack.json').read_text())[0]
composed=json.loads((run/'composed_prompt.json').read_text())
audit=json.loads((run/'command-logs/composed-audit.stdout').read_text())
assert composed['chosen_candidate_ids']==[] and composed['chosen_visual_concept_ids']==[]
assert audit['effective_visual_contract_sha256'] is None
assert 'orn_profile_gd65' not in [x.get('profile_id') for x in (pack.get('visual_obligations') or {}).get('profiles',[])]
result={'schema':'independent-source-link-check/v1','status':'PASS','method':'stdlib-only JSON-pointer, hash and authored-declaration comparison; no implementation link resolver used','generation_id':manifest['binding']['generation_id'],'forward_nodes_checked':len(evidence['forward']),'reverse_nodes_checked':len(evidence['reverse']),'query_checks':query_checks,'path_occurrences_checked':len(path_checks),'unique_paths_checked':len({x['path_id'] for x in path_checks}),'source_nodes_checked':len(checked_nodes),'source_references_checked':len(checked_refs),'candidate_complete_record_checks':len(candidate_source_checks),'source_files':list(file_proof.values()),'raw_reference_ambiguities_global':unresolved,'path_checks':path_checks,'source_checks':checked_refs,'candidate_source_checks':candidate_source_checks,'unlinked_exposed':[x['node'] for x in evidence['forward'] if not x['paths']],'relief_bundle':{'status':'PASS','associated_profile_ids':bundle['associated_profile_ids'],'component_count':len(bundle['components']),'profile_activation':bundle['profile_activation'],'all_components_required_if_adopted':True,'adopted':False,'auto_hard_promotion_observed':False},'semantic_limit':'Explicit association and source integrity are checked. Complete meaning support, mandatory profile activation, pixel fidelity and user acceptance are not inferred from a graph path.'}
(run/'independent-source-link-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k in ['status','forward_nodes_checked','reverse_nodes_checked','path_occurrences_checked','unique_paths_checked','source_nodes_checked','source_references_checked','candidate_complete_record_checks','raw_reference_ambiguities_global','relief_bundle','semantic_limit']},ensure_ascii=False,indent=2))
