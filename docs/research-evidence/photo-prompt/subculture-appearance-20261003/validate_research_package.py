"""Validate this research package only. No runtime writes or semantic test claims."""
import json
import re
from pathlib import Path

OUT=Path(__file__).resolve().parent


def load(name):
    return json.loads((OUT/name).read_text())


def main():
    files=list(OUT.glob("*.json"))
    for file in files:json.loads(file.read_text())
    terms=load("TERM-INVENTORY.json")["terms"]
    units=load("SEMANTIC-UNITS.json")["units"]
    candidates=load("CANDIDATE-DRAFTS.json")["candidates"]
    cases=load("CHARACTER-CASEBOOK.json")["cases"]
    source=load("RESEARCH-SOURCES.json")["sources"]
    assert len(terms)==171 and len(units)==len(candidates)==187 and len(cases)==37 and len(source)==58
    for collection in [terms,units,candidates,cases,source]:
        assert len({x['id'] for x in collection})==len(collection)
    tids={x['id'] for x in terms};uids={x['id'] for x in units};sids={x['id'] for x in source}
    scopes=load("REFERENCE-CATALOG-SNAPSHOT.json")["candidate_semantic_policy"]["slot_dimensions"]
    relation_count=0
    for unit in units:
        assert set(unit['term_ids'])<=tids and set(unit['source_ids'])<=sids
        assert len(unit['components'])>=2 and len(unit['render_gates_proposed'])==len(unit['components'])+1
        assert unit['observability']['partial_is_fail'] and unit['observability']['occluded']=='UNOBSERVABLE'
        assert unit['owner_template']['binding_required']
        relation_count+=len([r for r in unit['relations'] if 'contract_status' in r])
    for draft in candidates:
        assert draft['semantic_unit_id'] in uids and set(draft['source_ids'])<=sids
        assert draft['runtime_eligible_now'] is False
        assert draft['affected_properties_proposal'] and draft['concept_units_proposal']
        allowed=scopes[draft['slot_proposal']]
        if not allowed:assert draft['status']=='HOLD_UNSCOPED_SLOT'
        if set(draft['affected_dimensions_proposal'])-set(allowed):assert draft['status']=='HOLD_CROSS_DIMENSION'
    for case in cases:
        assert set(case['source_ids'])<=sids and set(case['related_term_ids'])<=tids
        assert set(case['boundary_comparison_unit_ids'])<=uids and case['runtime_index_proper_names'] is False
    catalog=load('REFERENCE-CATALOG-SNAPSHOT.json')
    profile_ids={x['id'] for x in catalog['profiles']}
    entry_keys={x['slot']+'.'+x['id'] for x in catalog['candidates']}
    mappings=load('OWNER-MAP.json')['mappings'];assert len(mappings)==32
    for mapping in mappings:
        assert set(mapping['existing_profile_ids'])<=profile_ids
        assert set(mapping['existing_candidate_keys'])<=entry_keys
    regression=load('REGRESSION-PROPOSALS.json')['cases'];assert len(regression)==52
    assert all(x['status']=='PROPOSED_NOT_RUN' for x in regression)
    for fixture in regression:assert set(fixture.get('unit_ids',[]))<=uids
    packs=load('PACK-CONTEXT-PROPOSALS.json')['contexts'];assert len(packs)==8
    cids={d['id'] for d in candidates}
    for pack in packs:
        assert set(pack['candidate_research_ids'])<=cids and len(pack['candidate_research_ids'])<=8
        assert pack['status']=='RESEARCH_FIXTURE_NOT_RUNTIME_PACK'
    local_links=[]
    for file in OUT.glob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)',file.read_text()):
            if '://' in link or link.startswith('#'):continue
            target=link.split('#')[0].split(':')[0]
            assert (file.parent/target).exists(),(file.name,link)
            local_links.append({'file':file.name,'target':target})
    summary=load('SUMMARY.json');assert summary['typed_structural_relations']==relation_count
    for file in OUT.iterdir():
        if file.is_file() and file.suffix in {'.py','.md','.json','.psv'}:
            assert all(line==line.rstrip() for line in file.read_text().splitlines()), ('trailing whitespace',file.name)
    result={'schema_version':'research-package-validation/v1','status':'PASS',
            'scope':'JSON parse, ID/source/unit references, component gate shape, proposed hold states, baseline owner IDs, local Markdown links',
            'json_files_checked':len(files),'local_links_checked':len(local_links),'counts':summary,
            'semantic_regressions':'PROPOSED_NOT_RUN','runtime_pack_execution':'NOT_RUN',
            'native_generated_pixel_qualification':'NOT_RUN','runtime_integration':'NOT_PERFORMED',
            'does_not_establish':['runtime semantic correctness','retrieval recall or precision','actual candidate eligibility','rendered pixel quality','user acceptance'],
            'local_links':local_links}
    (OUT/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['local_links','counts']},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
