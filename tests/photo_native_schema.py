"""Construct current native fixture records; never adapts production sources."""
import copy

def slot(tag, dimensions, *, neighbors=(), priority="core", semantic_role="direct",
         property_prefixes=("lighting.",), evidence_terms=("light",)):
    return {"id":tag,"description":"Declared fixture role for " + tag,
        "description_ko":"검증용 " + {"lighting":"조명 구성","light_type":"광원 종류","color":"색 표현"}.get(tag,tag),"dimensions":list(dimensions),"applicability":{},
        "semantic_role":semantic_role,"owners":["fixture_owner"],
        "property_prefixes":list(property_prefixes),"evidence_terms":list(evidence_terms),
        "includes":["A declared property on the fixture owner"],
        "excludes":["A property owned by a different carrier"],"neighbors":list(neighbors),
        "core_fields":["style","visual_priorities"],"priority":priority}

def candidate(cid, kind, content, effects, provenance, conditions=None):
    return {"id":cid,"record_kind":kind,"content":copy.deepcopy(content),
        "conditions":copy.deepcopy(conditions or {}),"effects":copy.deepcopy(effects),
        "provenance":copy.deepcopy(provenance)}
