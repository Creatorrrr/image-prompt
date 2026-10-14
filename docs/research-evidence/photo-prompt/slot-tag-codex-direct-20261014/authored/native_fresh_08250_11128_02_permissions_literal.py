"""Actual frozen whole consumer dimension/property lock tests, separate artifact."""
import copy,hashlib,json,runpy,sys
from pathlib import Path
M=runpy.run_path(str(Path(__file__).with_name('native_fresh_08250_11128_02.py')));R=M['R'];F=M['FROZEN'];s=M['s'];c=M['c'];CID=M['CID'];PROOF=M['PROOF']
sys.path[:0]=[str(F/'scripts'),str(F/'precore')]
import prompt_generator as g
J=json.loads((R/'authored/native_fresh_08250_11128_02_checks.json').read_text());rec=copy.deepcopy(M['AFTER']);rec['content']['role_evidence']=PROOF;data={'slot_catalog':M['CAT'],'slot_bindings':{},'candidates':{CID:rec}}
def eligible(entry,core,adult_allowed=True):return g.core_entry_eligible(data,core,{'adult_allowed':adult_allowed,'subject_category':'human','intent_constraints':{'subject_categories':['human'],'domains':[]}}, {'subject':{'tags':['human']}},'wardrobe_style',entry)
cases=[]
for rid in ['standing','walking']:
 for form,entry in [('full',s._guard_entry(PROOF,rid,{})),('compact',c.entry(data,CID,realization_id=rid))]:
  good=J['candidate_free_fixture_cores']['known_absent'];assert eligible(entry,good)
  cases.append({'rid':rid,'form':form,'case':'age_dimension_remains_locked_without_age_mutation','allowed':True})
  for dimension in PROOF['effect_sets'][rid]['dimensions']:
   bad=copy.deepcopy(good);bad['intent_lock']['open_dimensions'].remove(dimension);bad['intent_lock']['locked_dimensions'].append(dimension)
   assert not eligible(entry,bad);cases.append({'rid':rid,'form':form,'case':'whole_dimension_lock','dimension':dimension,'allowed':False})
  literal_values=[('appearance','wardrobe.ensemble','wardrobe.ensemble/v1','pencil_skirt','The already fixed outfit is a pencil skirt.'),('pose','body.pose','body.pose/v1','natural_standing' if rid=='standing' else 'natural_walking','The already fixed posture is natural standing.' if rid=='standing' else 'The already fixed posture is natural walking.')]
  if rid=='walking':literal_values.append(('action','action.walking','action.walking/v1','walking','The already fixed activity is walking.'))
  for d,p,typ,value,literal in literal_values:
   bad=copy.deepcopy(good);bad['baseline_prompt_en']+=' '+literal;bad['subject']=bad['baseline_prompt_en'];bad['request_binding']['active_spans'][0]['text']=bad['baseline_prompt_en'];bad['intent_lock']['semantic_anchors'].append({'dimension':d,'target':'person_A','property':p})
   request=bad['request_binding'];sha=hashlib.sha256(bad['baseline_prompt_en'].encode()).hexdigest();request['request_sha256']=sha;request['request_envelope_sha256']=hashlib.sha256(('explicit fixture envelope '+bad['baseline_prompt_en']).encode()).hexdigest();request['input_inventory']['items'][0]['sha256']=sha
   for row in bad['semantic_assertions']:
    if row['axes']['kind']=='scope_inventory':
     inventory=json.loads(row['axes']['inventory']);inventory['input_binding']=s.witnesses.input_binding(request);row['axes']['inventory']=s.witnesses.canonical(inventory)
   # Repeating the exact current value must not turn this selected actual
   # mutation into preservation/no-op permission.
   bad['semantic_assertions'].append({'assertion_id':'same_effect_value','dimension':d,'polarity':'required','source_span_ids':['request'],'affected_dimensions':[d],'evidence':{'literal':literal},'axes':{'native_schema':'photo-frozen-semantics/v1','kind':'fact','owner':'person_A','property':p,'value_type':typ,'value':value}})
   assert not eligible(entry,bad);cases.append({'rid':rid,'form':form,'case':'same_value_property_lock','property':p,'allowed':False})
  noage=copy.deepcopy(good);noage['adult_allowed']=True;noage['semantic_assertions']=[r for r in noage['semantic_assertions'] if r['assertion_id']!='adult'];assert not eligible(entry,noage)
  cases.append({'rid':rid,'form':form,'case':'adult_permission_does_not_witness_declared_adulthood','allowed':False})
  assert not eligible(entry,good,False);cases.append({'rid':rid,'form':form,'case':'source_adult_permission_guard_is_conjunctive','allowed':False})
modules={name:{'file':str(Path(module.__file__)),'sha256':hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()} for name,module in sys.modules.items() if getattr(module,'__file__',None) and (name.startswith('photo_') or name=='prompt_generator')}
assert all('/generations/' in v['file'] for v in modules.values())
p=R/'authored/native_fresh_08250_11128_02_permissions_literal.json';assert not p.exists();p.write_text(json.dumps({'schema':'fresh-native-11128-whole-consumer-lock-checks/v1','cases':cases,'frozen_production_modules':modules,'root_accepted':False,'operating_native_qualified_count':0},ensure_ascii=False,indent=2)+'\n');print(json.dumps({'cases':len(cases),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}))
