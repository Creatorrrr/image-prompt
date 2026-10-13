"""Single native candidate payload, with bounded many-to-many presentation refs."""
import copy
import photo_candidate_corpus as c
CONTRACT='photo-candidate-pack/v10'

class WorkingPack(dict):
    def __init__(self,value,roles):super().__init__(value);self.working_roles=roles;self.query_context=None

class CandidatePack(dict):
    def __init__(self,value,query_context):super().__init__(value);self.query_context=query_context

def role_cards(pack):
    if isinstance(pack,WorkingPack):return pack.working_roles
    if pack.get('contract_version')!=CONTRACT:raise ValueError('native v10 pack required')
    result={}
    for tag,view in pack['role_views'].items():
        rows=[]
        for ref in view['candidate_refs']:
            cid,pid=ref['candidate_id'],ref['proposal_id'];row=copy.deepcopy(pack['candidate_pool'][cid]);proposal=pack['role_proposals'][pid]
            row.update(copy.deepcopy(row.get('realization_views',{}).get(proposal['realization_id'],{})))
            if proposal['candidate_id']!=cid or proposal['target_slot_id']!=tag:raise ValueError('foreign role proposal')
            row.update({'slot':tag,'entry_id':cid,'proposal_id':pid,'binding_id':proposal['source_binding_id'],
                        'affected_dimensions':proposal['effects']['dimensions'],'affected_properties':proposal['effects']['properties'],
                        'source_conditions':proposal['conditions'],
                        'role_conditions':proposal['role_conditions'],
                        'realization_id':proposal['realization_id'],
                        'semantic_role':proposal['semantic_role'],
                        'applicability':{'status':proposal['applicability_status'],
                                         'source':'native_owned_role_fit',
                                         'reason':proposal['semantic_fit']['reason']}});rows.append(row)
        result[tag]={**{k:v for k,v in view.items() if k!='candidate_refs'},'candidates':rows}
    return result

def resolve_rows(pack,section,key='candidates'):
    value=pack.get(section) or {};refs=value.get(key) or []
    if isinstance(pack,WorkingPack):return refs
    result=[]
    for ref in refs:
        if 'candidate_id' in ref and ref['candidate_id'] in pack['candidate_pool']:
            row=copy.deepcopy(pack['candidate_pool'][ref['candidate_id']])
            context=copy.deepcopy(ref.get('view_context') or {})
            if context.pop('_native_view',None)=='bundle':row.update(copy.deepcopy(row['bundle_view']))
            row.update(context);result.append(row)
        else:result.append(ref)  # Policy-authored guidance is not a corpus candidate.
    return result

def finalize(pack,data,selected_ids,query_context):
    pool={};bindings={};views={};proposals=pack['global_retrieval']['role_proposals']
    def own(row):
        cid=str(row.get('source_candidate_id') or row.get('candidate_id') or row.get('id') or '')
        if cid not in data['candidates']:return None
        value={k:copy.deepcopy(v) for k,v in row.items() if k not in {'slot','entry_id','binding_id','proposal_id','axis','carrier'}}
        value['id']=cid;value['record_kind']=data['candidates'][cid]['record_kind']
        value['authored_record']=copy.deepcopy(data['candidates'][cid])
        conditional=data['candidates'][cid]['effects'].get('realizations')
        if not conditional:value.pop('realization_id',None)
        rid=value.get('realization_id') if conditional else None
        if rid is not None:
            view={k:copy.deepcopy(v) for k,v in value.items() if k not in {'authored_record','realization_views','id','record_kind'}}
            value['realization_views']={rid:view}
        if cid in pool:
            for k,v in value.items():
                if k=='realization_views':
                    for rid,view in v.items():pool[cid].setdefault(k,{}).setdefault(rid,{}).update(view)
                    continue
                if k not in pool[cid]:pool[cid][k]=v
        else:pool[cid]=value
        return cid
    for tag,role in pack.working_roles.items():
        refs=[]
        for row in role['candidates']:
            cid=own(row);pid=row['proposal_id'];bid=proposals[pid]['source_binding_id']
            if bid is not None:bindings[bid]=copy.deepcopy(data['slot_bindings'][bid])
            refs.append({'candidate_id':cid,'proposal_id':pid})
        views[tag]={**{k:copy.deepcopy(v) for k,v in role.items() if k!='candidates'},'candidate_refs':refs}
    def intern(rows):
        result=[]
        for row in rows:
            cid=own(row)
            if cid:
                context={k:copy.deepcopy(row[k]) for k in ('axis','carrier','slot','expression_scope') if k in row}
                if 'member_candidates' in row and 'components' in row:
                    pool[cid]['bundle_view']=copy.deepcopy(row)
                    context={'_native_view':'bundle'}
                # Eligibility is specific to this presentation, even when a
                # role card for the same source record requires later review.
                for key in ('applicability','adoption','opt_in_contract'):
                    if key in row and pool[cid].get(key)!=row[key]:context[key]=copy.deepcopy(row[key])
                result.append({'candidate_id':cid,'view_context':context})
            else:result.append(copy.deepcopy(row))
        return result
    result=dict(pack)
    for field in ('visual_concept_candidates','candidate_bundles'):
        if isinstance(result.get(field),dict):result[field]={**result[field],'candidates':intern(result[field].get('candidates') or [])}
    if isinstance(result.get('character_response'),dict):
        result['character_response']=copy.deepcopy(result['character_response']);advisory=result['character_response'].get('advisory_retrieval')
        if advisory:advisory['candidates']=intern(advisory.get('candidates') or [])
    adult=result.get('adult_appeal')
    if adult:
        result['adult_appeal']=copy.deepcopy(adult)
        for axis in result['adult_appeal'].get('axes',{}).values():axis['candidate_inventory']=intern(axis.get('candidate_inventory') or [])
    for cid in selected_ids:
        if cid not in pool:
            entry=c.entry(data,cid);record=data['candidates'][cid]
            own({'id':cid,'label_en':entry.get('en') or entry.get('definition') or (entry.get('semantics') or {}).get('definition') or 'optional visual meaning','label_ko':entry.get('ko') or entry.get('en') or '',
                 'concept_units':entry.get('concept_units') or [],'relations':entry.get('relations') or [],'affected_dimensions':record['effects']['dimensions'],'affected_properties':record['effects']['properties'],
                 'content_form':'unordered_inspiration_terms','concept_terms':list(dict.fromkeys((entry.get('concept_units') or [])+((entry.get('concept_candidate') or {}).get('concept_terms') or [])+[entry.get('en') or entry.get('definition') or (entry.get('semantics') or {}).get('definition') or 'optional visual meaning'])),
                 'adoption':'optional','applicability':{'status':'review_required' if not record['effects']['dimensions'] else 'eligible','source':'global_shared_corpus'},'conflicts_with':[]})
    for row in pool.values():
        if row.get('content_form')=='unordered_inspiration_terms':
            row.pop('label_en',None);row.pop('label_ko',None)
    if not set(pool)<=set(selected_ids):raise ValueError('optional presentation expanded beyond globally retrieved unique candidate budget')
    result['candidate_pool']=pool;result['candidate_bindings']=bindings;result['role_proposals']=copy.deepcopy(proposals);result['role_views']=views
    result['unbound_candidate_refs']=[cid for cid in selected_ids if not any(row['candidate_id']==cid for row in proposals.values())]
    result['contract_version']=CONTRACT
    for field in ('character_response','adult_appeal','candidate_bundles','visual_concept_candidates'):
        if isinstance(result.get(field),dict) and 'canonical_sha256' in result[field]:
            result[field]['canonical_sha256']=c.digest({k:v for k,v in result[field].items() if k!='canonical_sha256'})
    return CandidatePack(result,query_context)

def validate(pack):
    if pack.get('contract_version')!=CONTRACT or 'slots' in pack:raise ValueError('native v10 pack required')
    if len(pack.get('candidate_pool',{}))>64:raise ValueError('global unique candidate budget exceeded')
    for cid,row in pack['candidate_pool'].items():
        if not c.ID.fullmatch(cid) or row.get('id')!=cid or row['authored_record']['id']!=cid:raise ValueError('invalid native candidate identity')
    for pid,proposal in pack['role_proposals'].items():
        cid=proposal['candidate_id']
        if pid!=proposal['proposal_id'] or cid not in pack['candidate_pool'] or proposal['source_record_sha256']!=c.digest(pack['candidate_pool'][cid]['authored_record']):raise ValueError('role source mismatch')
    role_cards(pack)
    return pack

class _Section(dict):
    """Read-only native reference dereferencing, preserving original wire bytes."""
    def __init__(self,value,pack):dict.__init__(self,value);self._pack=pack
    def _resolve(self,value):
        if isinstance(value,dict):return _Section(value,self._pack)
        if isinstance(value,list):
            result=[]
            for row in value:
                if isinstance(row,dict) and set(row)<={'candidate_id','view_context'} and 'candidate_id' in row:
                    cid=row['candidate_id']
                    if cid not in dict.__getitem__(self._pack,'candidate_pool'):raise ValueError('dangling native presentation reference')
                    resolved=copy.deepcopy(dict.__getitem__(self._pack,'candidate_pool')[cid])
                    context=copy.deepcopy(row.get('view_context') or {})
                    if context.pop('_native_view',None)=='bundle':resolved.update(copy.deepcopy(resolved['bundle_view']))
                    resolved.update(context);result.append(resolved)
                else:result.append(row)
            return result
        return value
    def __getitem__(self,key):return self._resolve(dict.__getitem__(self,key))
    def get(self,key,default=None):return self._resolve(dict.get(self,key,default))
    def values(self):return [self[key] for key in dict.keys(self)]
    def __deepcopy__(self,memo):return {key:copy.deepcopy(value,memo) for key,value in dict.items(self)}
    def __setitem__(self,*args):raise TypeError('native dereference views are read-only')
    def update(self,*args,**kwargs):raise TypeError('native dereference views are read-only')

class _ReadPack(_Section):
    def __init__(self,value):dict.__init__(self,value);self._pack=self

def read_view(pack):
    if isinstance(pack,_ReadPack):return pack
    validate(pack)
    return _ReadPack(pack)
