"""Mechanical binding wire for explicit fresh05 literal facts/roles/units. No semantic choices/status defaults. No output at import."""
import json,gzip,hashlib,sys,copy
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');O=R/'native_batches/review11870-01250-01300-05';D=R/'native-inputs/prepared/review11870-01250-01300-05';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
import photo_candidate_realizations as real
import photo_semantic_role_views as v
assert hashlib.sha256(Path(n.__file__).read_bytes()).hexdigest()=='f74a5ef91bc07048c8bf312b66680c5b92b3b7b388f31f1890f31c8578609dee'
I=json.loads((D/'INPUT.json').read_text());A=json.loads((D/'ASSIGNMENT.json').read_text());P=json.loads((D/'PREPARED-PACKET.json').read_text());S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()));CAT=I['catalog_review']['after'];CH=c.digest(CAT)
assert c.digest(I)=='8e55650ab768cd287b707bebeb11ba2139b475f6f3b0a3d1d17fe82ab128ea66'and CH=='d9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15'and c.digest(S)=='5ee63da71e477de1d52677fa768dd715eb6589c6f0f77ac213c11825b0c2fd44'
ROWS=[];CHECKS=[]
def read_assessment(name,sha):
 x=json.loads((O/name).read_text());assert c.digest(x)==sha;return x

def emit(ordinal,status,literal,rids,roles,owner_plans,extra_units,view_plans,reason):
 assert status in ['approved','pending'];cid=literal['candidate_id'];assert ordinal==literal['ordinal'];before=P['original_records'][cid];after=P['current_records'][cid];old=P['historical_compiled_rows'][cid];rev=I['required_revisions'][cid];proof=None
 assert after==literal['source_after']and real.ids(after)==rids and literal['required_CID_closure']=={}and literal['required_binding_closure']=={}
 if status=='approved':
  facts=copy.deepcopy(literal['facts']);rolemap={tag:{'spec_sha256':c.digest(CAT[tag]),'scope':scope,'realization_ids':choices,'fact_refs':refs,'support_modes':modes}for tag,scope,choices,refs,modes in roles}
  units=[{**copy.deepcopy(u),'disposition':'semantic'}for u in literal['full_units']]+copy.deepcopy(extra_units)
  proof={'schema':n.SCHEMA,'meaning_sha256':n.meaning_sha256(after),'catalog_sha256':CH,'complete':True,'facts':facts,'roles':rolemap,'owner_maps':copy.deepcopy(owner_plans),'source_units':units,'effect_sets':{rid:n.effect_set(after,rid)for rid in rids},'dependencies':{rid:[]for rid in rids},'reference_sha256':{},'guard_sets':{rid:n.source_guard_set(after,rid,S)for rid in rids},'profile_contracts':{rid:None for rid in rids},'review':{'basis':reason,'whole_source_reviewed':True,'source_correction':None if n.meaning_sha256(before)==n.meaning_sha256(after)else{'before_sha256':n.meaning_sha256(before),'after_sha256':n.meaning_sha256(after),'rationale':'Exact root selected formal05 fullafter, no further source change. '+reason},'original_review':{'candidate_id':cid,'source_record_sha256':old['source_record_sha256'],'catalog_sha256':old['catalog_sha256'],'decision_sha256':I['original_decisions'][cid]['row_sha256'],'artifact':I['original_decisions'][cid]['file']+'#item='+str(I['original_decisions'][cid]['item'])},'native_review':{'reviewer':'/root/review_11870_12250','method':'codex_subagent_direct_source_read','native_contract_sha256':''}}}
  if view_plans:
   proof['manual_role_views']=[]
   byid={f['id']:f for f in facts}
   for plan in view_plans:
    vi,role,rid,facets,facetmeaning,retained,boundary=plan;refs=[byid[fid]for fid,quote in facets];anchors=[];endpoints=[];required=set()
    def requirements(f):
     for child in f['requires']:
      if child not in required:required.add(child);requirements(byid[child])
    for fid,facet in facets:
     f=byid[fid];unit=next(u for u in units if u['disposition']=='semantic'and u['pointer']==f['pointer']and u['realization_id']==rid);text=n.positive_string(after,f['pointer'],realization_id=rid);start=text.index(facet,text.index(f['quote']));assert facet in f['quote'];anchors.append({'fact_id':fid,'pointer':f['pointer'],'source_unit_sha256':c.digest(unit),'full_field_sha256':c.digest(text),'facet_quote':facet,'start':start,'stop':start+len(facet)});endpoints.append({'fact_id':fid,'position':'target'});endpoints += [{'fact_id':fid,'position':'receiver','index':j}for j in range(len(f.get('receivers',[])))];requirements(f)
    view={'schema':v.SCHEMA,'id':vi,'candidate_id':cid,'realization_id':rid,'role_id':role,'spec_sha256':c.digest(CAT[role]),'canonical_fact_refs':[{'fact_id':f['id'],'fact_sha256':c.digest(f),'mode':f['mode']}for f in refs],'normal_anchors':anchors,'endpoint_refs':endpoints,'requires_refs':sorted(required),'whole_closure_sha256':c.digest({key:proof[key]for key in v.CLOSURE_FIELDS}),'manual_semantic_facet':facetmeaning,'whole_value_retained':retained,'manual_boundary_rationale':boundary}
    proof['manual_role_views'].append(view);proof['roles'][role].setdefault('view_refs',[]).append(vi)
  proof['review']['native_review']['native_contract_sha256']=n.native_contract_sha256(proof);record=copy.deepcopy(after);record['content']['role_evidence']=proof;S['candidates'][cid]=record;n.validate(record,CAT,catalog_sha256=CH,corpus=S);compact=n.compact(record,S)
  CHECKS.append({'ordinal':ordinal,'full_source_validation':True,'compact':compact,'proof_sha256':c.digest(proof),'literal_fresh_assessment_row_sha256':c.digest(literal),'native_signature':proof['review']['native_review']['native_contract_sha256']})
 delta=[{'pointer':'/'+k,'before_exists':True,'before':before[k],'after_exists':True,'after':after[k],'reason':'Exactformal05 root input, no current source edit. '+reason}for k in ['content','conditions','effects','provenance','record_kind']if before[k]!=after[k]]
 ROWS.append({'candidate_id':cid,'ordinal':ordinal,'status':status,'rationale':reason,'source_before':before,'source_after':after,'delta':delta,'original_compiled':I['original_decisions'][cid],'proof':proof,'dependency_records':{},'reference_bindings':{},'source_reread_complete':True,'reference_reread_complete':True,'revision':{'prior_review':rev['prior_review'],'memo_artifacts':rev['memo_artifacts'],'rationale':'Fresh manual literal source/spec/facts/RID/owners/wholeunits decision, not oldapproval/proof conversion. '+reason}})
def owner_map(literal,rid='base',branch=False):
 # Only serialize the literal manually specified existing selectors, no inferred owner/kind/role.
 values=literal['owner_bindings'][rid]if branch else literal['owner_bindings'];return {'schema':n.SELECTOR_OWNER_SCHEMA,'bindings':[{'target':k,**copy.deepcopy(val)}for k,val in values.items()]}
def modules():
 out={}
 for name,m in sorted(sys.modules.items()):
  if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
   p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);out[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 return out
