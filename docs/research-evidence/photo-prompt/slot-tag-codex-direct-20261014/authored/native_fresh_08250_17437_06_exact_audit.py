"""Post-manual exact preservation checks; comparison never authors facts/status."""
import copy,collections,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];A=R/'authored'
old=json.loads((R/'native_batches/review08250-17437-05/BATCH.json').read_text())['records'][0]
new=json.loads((R/'native_batches/review08250-17437-06/BATCH.json').read_text())['records'][0]
p=old['proof'];q=new['proof']
def norm(v):
 if isinstance(v,str):return v.replace('g06_','g05_')
 if isinstance(v,list):return [norm(x) for x in v]
 if isinstance(v,dict):return {k:norm(x) for k,x in v.items()}
 return v
assert old['source_after']==new['source_after']
N=norm(q);assert p['facts']==N['facts']
for k in ['owner_maps','effect_sets','dependencies','guard_sets','profile_contracts','reference_sha256','guard_supports']:
 assert p[k]==N[k],k
units=[]
for i,(b,a) in enumerate(zip(p['source_units'],N['source_units'])):
 if b==a:continue
 assert i in [174,303,435,565,661,757]
 bb=copy.deepcopy(b);assert len(bb['fact_refs'])==4;bb['fact_refs']=bb['fact_refs'][:2];assert bb==a
 units.append({'source_unit_index':i,'realization_id':a['realization_id'],'pointer':a['pointer'],'exact_full_quote':a['quote'],'before':b,'after':q['source_units'][i],'reason':'Only cheek cue ownership/color/exclusions are in this exact gate. Baseline eye/expression remain in actual separate instructions, canonical facts and effects.'})
assert len(units)==6
role_diffs=[]
for k,v in p['roles'].items():
 if v==N['roles'][k]:continue
 b=copy.deepcopy(v);a=N['roles'][k];assert k=='body_pose';b['spec_sha256']=a['spec_sha256'];assert b==a;role_diffs.append({'slot_id':k,'before_spec_sha256':v['spec_sha256'],'after_spec_sha256':a['spec_sha256'],'manual_fit':'Direct149V6 fullspec reread: common poised bearing remains owned whole-body bearing; no new local joint/stance/contact/part is inferred.'})
groups=collections.defaultdict(list)
for f in q['facts']:
 if f['mode']=='effect':groups[(f['realization_id'],f['dimension'],f['target'],f['property'])].append(f)
conflicts=[]
for key,fs in groups.items():
 vals={json.dumps({k:f[k] for k in ['value','operation','receivers']},sort_keys=True) for f in fs}
 if len(vals)!=1:conflicts.append(key)
assert not conflicts and len(groups)==138
for u in units:
 rid=u['realization_id'];root='/content/realization_content/'+rid+'/authored_components/obligations/'
 instr=u['pointer'].removesuffix('/render_gates/0/description')+'/instruction'
 refs=[x for x in q['source_units'] if x['realization_id']==rid and x['pointer']==instr and x['disposition']=='semantic_reference'];assert len(refs)==1
 assert refs[0]['fact_refs']==['g06_'+rid+'_eye_effect','g06_'+rid+'_expression']
 u['separate_actual_instruction_baseline_reference']=refs[0]
out={'schema':'photo-native-fresh06-manual-exact-preservation-audit/v1','task_name':'/root/review_08250_09250','model':'gpt-6.1-sol','reasoning_effort':'high','source_after_exact_previous_and_INPUT':True,'comparison_only_not_oldproof_conversion':True,'fact_ID_namespace_change':'g05_ to g06_; exact semantic payload preserved after whole fresh reading','facts':len(q['facts']),'effect_assignment_groups':len(groups),'effect_assignment_conflicts':conflicts,'source_units':len(q['source_units']),'exact_six_reference_repairs':units,'exact_role_spec_binding_changes':role_diffs,'all_other_semantic_fields_equal_after_ID_normalization':True,'fact_mode_counts':dict(collections.Counter(f['mode'] for f in q['facts'])),'unit_disposition_counts':dict(collections.Counter(u['disposition'] for u in q['source_units'])),'root_acceptance':False,'operating_native_qualified_count':0,'limitation':'Equality and conflict absence do not independently establish semantic entailment; actual manual source/spec/quote/branch review is recorded separately.'}
pth=A/'native_fresh_08250_17437_06_exact_audit.json';assert not pth.exists();pth.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(hashlib.sha256(pth.read_bytes()).hexdigest(),len(units),len(groups))
