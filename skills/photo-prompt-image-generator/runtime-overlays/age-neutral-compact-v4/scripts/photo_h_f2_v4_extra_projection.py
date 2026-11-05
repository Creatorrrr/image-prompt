"""Source-bound display aliases for reviewed age-neutral research identifiers."""
import copy, hashlib, json, re
import photo_h_f2_workflow as workflow
from photo_h_f2_v4_extra_inventory import MANIFEST

MARK='[research semantics: optional review metadata, not native adoption authority] '
WARNING='[identifiers and relation expressions in this block are display projections, not source literals or native selectors] '

def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def alias(cid,value,namespace):
    return namespace+'_'+hashlib.sha256(('photo-display-alias/v1\0'+cid+'\0'+value).encode()).hexdigest()[:16]

def project(material,record,rid='base'):
    cid=record['id'];spec=MANIFEST.get(cid)
    if spec is None:return copy.deepcopy(material),None
    if digest(record)!=spec['sha256'] or material.get('candidate_id')!=cid or material.get('conditions')!=record.get('conditions'):
        raise ValueError('reviewed display source or conditions changed')
    out=copy.deepcopy(material);lines=out['meaning'].split('\n');primary_aliases={};primary_sites=[]
    for site in spec.get('primary_sites',[]):
        if site['rid']!=rid:continue
        path=site['path'].removeprefix('/content/');old='['+path+'] '+site['value']
        if old not in lines:continue  # A selected sibling can be deliberately excluded.
        if lines.count(old)!=1:raise ValueError('ambiguous structural source unit')
        def neutral(m):return 'people' if m.group(0).lower()=='adults' else 'person'
        new='['+re.sub(r'adults?',neutral,path,flags=re.I)+'] '+re.sub(r'adults?',neutral,site['value'],flags=re.I)
        if new in lines and new!=old:raise ValueError('structural display alias collision')
        lines[lines.index(old)]=new;primary_aliases[new]=old;primary_sites.append(site)
    if not spec['occurrences']:
        if primary_sites:out['meaning']='[structural identifiers in this result are display projections, not source literals or native selectors]\n'+'\n'.join(lines)
        return out,{'state':'projected','source_sha256':spec['sha256'],'reverse_aliases':primary_aliases,'reviewed_sites':primary_sites}
    indices=[i for i,line in enumerate(lines) if line.startswith(MARK)]
    if len(indices)!=1:raise ValueError('expected one source research block')
    index=indices[0];before=json.loads(lines[index][len(MARK):])
    raw=record['content'].get('research_semantics',{})
    expected={k:copy.deepcopy(v) for k,v in raw.items() if k in workflow.RESEARCH_MEANING_FIELDS and v not in (None,[],{},'')}
    for k in ('positive_en','positive_ko','proposal_en','proposal_ko','phrase_en','phrase_ko','visible_en','visible_ko'):
        if isinstance(expected.get(k),str) and expected[k] in lines[:index]:del expected[k]
    if before!=expected:raise ValueError('display research differs from source')
    research=copy.deepcopy(before);mapping={key:alias(cid,key,namespace) for key,namespace in spec['identifiers'].items()}
    if len(set(mapping.values()))!=len(mapping):raise ValueError('display alias collision')
    source_text=json.dumps(before,ensure_ascii=False)
    if any(value in source_text for value in mapping.values()):raise ValueError('display alias already exists in source')
    renames=[]
    for site in spec['occurrences']:
        path=site['path'];parent=research
        for bit in path[:-1]: parent=parent[int(bit)] if isinstance(parent,list) else parent[bit]
        key=int(path[-1]) if isinstance(parent,list) else path[-1]
        old=site['value']
        if site['kind']=='key':
            if not isinstance(parent,dict) or key!=old or key not in parent:raise ValueError('identifier key changed')
            renames.append((parent,key,mapping[old]))
        else:
            if parent[key]!=old:raise ValueError('identifier reference changed')
            parent[key]=mapping[old]
    for parent,old,new in renames:
        if new in parent:raise ValueError('identifier key collision')
        parent[new]=parent.pop(old)
    # Symbolic relation expressions may mention a reviewed identifier as a
    # token. Do not rewrite ordinary source prose or any conditions.
    def expressions(value,path=()):
        if isinstance(value,dict):
            return {k:expressions(v,path+(k,)) for k,v in value.items()}
        if isinstance(value,list):return [expressions(v,path+(str(i),)) for i,v in enumerate(value)]
        if isinstance(value,str) and path and path[-1] in {'description','requirement','requirement_en'}:
            for old,new in sorted(mapping.items(),key=lambda x:-len(x[0])):
                if '_' in old or any(ch.isdigit() for ch in old):
                    value=re.sub(r'(?<![A-Za-z0-9_])'+re.escape(old)+r'(?![A-Za-z0-9_])',lambda _:new,value)
                else:
                    value=re.sub(r'(?<![A-Za-z0-9_])'+re.escape(old)+r'(?=\.)',lambda _:new,value)
        return value
    research=expressions(research)
    # Reversibility proves that only reviewed identifiers were transformed.
    reverse={v:k for k,v in mapping.items()}
    def restore(value):
        if isinstance(value,dict):return {restore(k):restore(v) for k,v in value.items()}
        if isinstance(value,list):return [restore(v) for v in value]
        if isinstance(value,str):
            for display,original in reverse.items():value=value.replace(display,original)
        return value
    if restore(research)!=before:raise ValueError('display projection is not reversible')
    lines[index]=MARK+WARNING+json.dumps(research,ensure_ascii=False,sort_keys=True,separators=(',',':'))
    if primary_sites:lines.insert(0,'[structural identifiers in this result are display projections, not source literals or native selectors]')
    out['meaning']='\n'.join(lines)
    reverse.update(primary_aliases)
    return out,{'state':'projected','source_sha256':spec['sha256'],'reverse_aliases':reverse,'reviewed_sites':spec['occurrences']+primary_sites}
