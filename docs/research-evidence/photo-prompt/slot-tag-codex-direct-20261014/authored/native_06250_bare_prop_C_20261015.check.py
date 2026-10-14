"""Offline exact GEN07143 source-unit/retrieval diagnostics only; no full proof or admission."""
import sys,json,hashlib,copy
from pathlib import Path
R=Path(__file__).resolve().parent.parent
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/07143a62ae23201a5cceedf155a985e204256740da96fc083e703d8ac5e7ba07')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(G/'scripts/photo_semantic_evidence.py')=='7d9f7e7c69bc1f8186af9a289eb46defd0e953de9c27d1b0b770142ad2660205'
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_semantic_evidence as e
import photo_global_index as i
p=R/'authored/native_06250_bare_props_01236_00259_00807_00924_C_20261015.json';d=json.loads(p.read_text());results=[]
for r in d['records']:
 before,after=r['source_before'],r['source_after'];facts={f['id']:f for f in r['facts']}
 assert {k:v for k,v in after['content'].items() if k!='application_contract'}==before['content']
 assert all(after[k]==before[k] for k in ['id','record_kind','conditions','provenance'])
 assert e.primary_paths(after,'base')-e.primary_paths(before,'base')=={'/content/application_contract'}
 e._validate_source_units(after,{'source_units':r['source_units']},facts,'base')
 for f in facts.values():assert f['quote'] in e.positive_string(after,f['pointer'],realization_id='base')
 assert i.fields(before)==i.fields(after);assert i.text(before)==i.text(after)
 missing=copy.deepcopy(r['source_units']);missing=missing[1:]
 try:e._validate_source_units(after,{'source_units':missing},facts,'base')
 except ValueError:missing_reject=True
 else:raise AssertionError('missing application unit accepted')
 wrong=copy.deepcopy(r['source_units']);wrong[1]['fact_refs']=['not_a_fact']
 try:e._validate_source_units(after,{'source_units':wrong},facts,'base')
 except ValueError:anchor_reject=True
 else:raise AssertionError('wrong anchor accepted')
 results.append({'ordinal':r['ordinal'],'source_unit_shape':'pass','exact_original_search_fields_text_recipe':'unchanged','missing_application_unit_rejected':missing_reject,'foreign_anchor_rejected':anchor_reject,'native_fullproof_validation':False,'admission_or_lockconsumer_executed':False})
modules={}
for name,m in sorted(sys.modules.items()):
 if name.startswith(('photo_','photo_precore_')) and getattr(m,'__file__',None):
  path=Path(m.__file__).resolve();assert path.is_relative_to(G), (name,path);modules[name]={'file':str(path),'raw_sha256':sha(path)}
out=R/'worker-notes/native-06250-bare-prop-C-diagnostics-20261015.json';assert not out.exists();out.write_text(json.dumps({'schema':'photo-native-draft-source-unit-diagnostic/v1','input_file':str(p),'input_raw_sha256':sha(p),'generation':str(G),'results':results,'actual_imported_modules':modules,'boundary':'Only published primary_paths/exact source-unit/same-RID direct anchoring and retrieval projection identity checked. No semantic entailment, fullproof acceptance, guard admission, whole-lock acceptance, runtime index, provider or network execution.'},ensure_ascii=False,indent=2)+'\n');print(out,sha(out));print('actual_modules',len(modules),'rows',len(results))
