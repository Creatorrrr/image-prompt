"""Final signed artifact binding audit; no mutable or operating data writes."""
import copy,hashlib,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];A=R/'authored';GEN=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/188c56270ebc2c973defd3307d8fa43df60e55701baa30c45367a4e2e3efe2bb');sys.path[:0]=[str(GEN/'scripts'),str(GEN/'precore')]
import photo_semantic_evidence as s
import photo_candidate_corpus as c
import photo_search_layout as layout
CHECK=json.loads((A/'native_fresh_08250_17437_05_checks.json').read_text());U=json.loads((A/'native_fresh_08250_17437_05_unsigned.json').read_text());BPATH=R/'native_batches/review08250-17437-05/BATCH.json';B=json.loads(BPATH.read_text());row=B['records'][0];p=row['proof'];cid=row['candidate_id'];old=copy.deepcopy(U['proof_draft']);new=copy.deepcopy(p)
for v in [old,new]:v['review'].pop('basis');v['review']['native_review'].pop('native_contract_sha256')
assert c.canonical_bytes(old)==c.canonical_bytes(new)
assert row['source_after']==U['source_after']
assert p['review']['native_review']['native_contract_sha256']==s.native_contract_sha256(p)
rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=p
I=json.loads((R/'native-inputs/prepared/review08250-17437-05/INPUT.json').read_text());DATA={'candidates':{cid:rec},'slot_catalog':I['catalog_review']['after'],'slot_bindings':{}};s.validate(rec,DATA['slot_catalog'],corpus=DATA);small=layout.guard_record(rec,DATA);CD={**DATA,'candidates':{cid:small}}
rids=list(p['owner_maps']);cases=[]
for rid in rids:
 selected=next(x['selected'] for x in U['selected_layouts'] if x['rid']==rid)
 key=('_'.join(x for x in ['help' if 'help' in selected else '', 'cheek' if 'cheek_warmth' in selected else ('mouth' if 'mouth_warmth' in selected else ''),'recovery' if 'recovery' in selected else ''] if x)) or ('setback' if 'setback' in selected else 'base')
 for form,data in [('full',DATA),('compact',CD)]:
  entry=c.entry(data,cid,realization_id=rid);result=s.admission(entry,CHECK['core_fixtures'][key]);assert result['allowed']
  cases.append({'rid':rid,'form':form,'allowed':True,'selected_effect_scope':s.permission_scope(entry,CHECK['core_fixtures'][key])})
mods={k:{'file':str(Path(v.__file__).resolve()),'raw_sha256':hashlib.sha256(Path(v.__file__).read_bytes()).hexdigest()} for k,v in sys.modules.items() if getattr(v,'__file__',None) and k.startswith('photo_')}
assert all(Path(x['file']).is_relative_to(GEN) for x in mods.values());assert mods['photo_semantic_evidence']['raw_sha256']=='6833e00c03ee4aa1222ea1a9e7c5304d8a98d62ad1d3d0e3ff6a3d666bb313e9'
out={'schema':'photo-native-fresh05-final-artifact-preservation/v1','candidate_id':cid,'batch_raw_sha256':hashlib.sha256(BPATH.read_bytes()).hexdigest(),'batch_canonical_sha256':c.digest(B),'final_proof_sha256':c.digest(p),'unsigned_draft_semantics_equals_final_except_explicit_review_basis_and_native_signature':True,'semantic_fields_compared':'All facts/source_units/guard_supports/roles/owner_maps/effect_sets/dependencies/guard_sets/profile_contracts/reference bindings and original/source correction provenance exact. Only final review prose basis and computed native signature differ.','source_after_exact_unsigned':True,'earlier_check_report_raw_sha256':hashlib.sha256((A/'native_fresh_08250_17437_05_checks.json').read_bytes()).hexdigest(),'full_compact_final_signed_admission_cases':cases,'actual_loaded_modules':mods,'root_accepted':False,'operating_qualified':0,'provider_model_network_calls':0}
o=A/'native_fresh_08250_17437_05_final_preservation.json';assert not o.exists();o.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(len(cases),hashlib.sha256(o.read_bytes()).hexdigest())
