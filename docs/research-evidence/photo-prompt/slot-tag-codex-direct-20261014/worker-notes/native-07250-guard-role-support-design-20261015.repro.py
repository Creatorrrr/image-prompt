"""Read-only contract diagnostic. No native proof, core, source or runtime writes.

The miniature graph is a synthetic low-level fixture, not an independently
qualified authorial core. It demonstrates the current v1 guard evaluator only.
"""
import ast, copy, hashlib, json, pathlib, sys

R = pathlib.Path(__file__).resolve().parents[1]
GEN = pathlib.Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/2ad7b2bfd3f4d730985c23ed89e3513a326a0a2ceea22aecfe28cb5d05c98ac9')
sys.path.insert(0, str(GEN / 'scripts'))
import photo_semantic_evidence as n
import photo_candidate_corpus as c

def raw(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def binding(p):
    v=json.loads(p.read_text())
    return {'file':str(p),'raw_sha256':raw(p),'canonical_sha256':c.digest(v)}

packet_path=R/'native-inputs/prepared/review08250-17437-04/PREPARED-PACKET.json'
packet=json.loads(packet_path.read_text())
cid='cand_d15b4c6334a45b61a7407a022a2cc8e0'
source=packet['current_records'][cid]
old=json.loads((R/'native_batches/review08250-17437-03/BATCH.json').read_text())['records'][0]['source_after']
assert source==old
n.validate_source_guards(source['conditions']['native_guards'])
pointer='/content/authored_components/obligations/0/render_gates/1/description'
quote='its face is explicitly part of that actor'
assert quote in n.positive_string(source,pointer,realization_id='baseline')

graph={'schema':n.witnesses.SCHEMA,'owners':{'fixture_actor':'actor','fixture_face':'face'},
       'roles':{'main_subject':'fixture_actor','primary_face':'fixture_face'},
       'equivalent':[],'part_of':[['fixture_face','fixture_actor']],'disjoint':[]}
frozen={'graph':graph,'facts':[{'dimension':'role','target':'fixture_actor',
 'property':'participant.role.peer_rival','value':{'type':'participant.role.peer_rival/v1','value':'declared'},
 'assertion_id':'fixture_peer_role'}],'scope_inventories':[]}
entry={'_source_conditions':source['conditions'],'_selected_conditions':{}}
assert n.proof_of(entry) is n.MISSING
yes=n._evaluate_role_guards(entry,{},frozen=frozen)
assert yes['allowed'] and len(yes['rules'])==2
missing=copy.deepcopy(frozen);missing['graph']['part_of']=[]
no=n._evaluate_role_guards(entry,{},frozen=missing)
assert not no['allowed'] and no['reason']=='native_owner_relation_unverified'
assert n.native_status(source)=='unqualified'

# Read exact current contracts without constructing a fake complete proof.
tree=ast.parse(pathlib.Path(n.__file__).read_text())
functions={x.name:{'start':x.lineno,'stop':x.end_lineno} for x in tree.body if isinstance(x,ast.FunctionDef)}
catalog_path=R/'CATALOG-FINAL-146-V5.json'
cat=json.loads(catalog_path.read_text());prior=json.loads((R/'CATALOG-FINAL-144-V4.json').read_text())
out={'schema':'photo-native-read-only-guard-role-diagnostic/v1',
 'task':'/root/review_07250_08250','model':'gpt-6.1-sol','reasoning_effort':'high',
 'native_proof_created':False,'qualified_operational_count':0,'production_changed':False,
 'generation':str(GEN),'imported_modules':[
 {'file':str(pathlib.Path(mod.__file__)),'raw_sha256':raw(pathlib.Path(mod.__file__))}
 for mod in [n,c,n.witnesses]],
 'read_code_bindings':[{'file':str(GEN/p),'raw_sha256':raw(GEN/p)} for p in [
 'scripts/photo_semantic_evidence.py','scripts/photo_candidate_corpus.py',
 'scripts/photo_candidate_realizations.py','scripts/photo_precore_bridge.py',
 'scripts/photo_slot_semantics.py','scripts/photo_role_proposals.py','scripts/photo_native_pack.py',
 'scripts/photo_search_layout.py','scripts/photo_search_reader.py','scripts/photo_runtime_sources.py',
 'precore/photo_semantic_witnesses.py']],
 'packet':binding(packet_path),'catalog':binding(catalog_path),
 'actual_current_source_sha256':c.digest(source),'exact_current04_equals_03_source_after':True,
 'source_guard_schema':source['conditions']['native_guards']['schema'],
 'manual_positive_anchor':{'realization_id':'baseline','pointer':pointer,'quote':quote},
 'actual_v1_rule':source['conditions']['native_guards']['rules'][0],
 'low_level_synthetic_graph_only':{'graph':graph,'positive_receipt':yes,'missing_part_of_receipt':no,
   'limit':'Not admission, core validation, role qualification or production evidence. v2 runtime evaluator not executed with a fabricated proof.'},
 'current_contract_obstruction':{'role_exact_fields':['spec_sha256','scope','realization_ids','fact_refs','support_modes'],
 'source_unit_exact_fields':sorted(n.SOURCE_UNIT_FIELDS),
 'fact_refs_nonempty':True,'guard_refs_unsupported':True,
 'source_remains_unqualified':True},
 'full_specs_directly_read_this_turn':{k:{'sha256':c.digest(cat[k]),'equal_to_actual144V4':cat[k]==prior[k]} for k in ['anatomical_connection','body_form','action','relational_action']},
 'semantic_module_function_locators':{k:functions[k] for k in [
 'native_contract_sha256','positive_string','primary_paths','_validate_source_units','_fact_valid',
 '_validate_owner_map','validate','compact','qualification','admission','source_guard_set',
 '_evaluate_role_guards','_validate_target_guards','validate_guard_namespaces','_guard_context',
 '_evaluate_target_guards','evaluate_native_guards','permission_scope']}}
dest=R/'worker-notes/native-07250-guard-role-support-design-20261015.repro.json'
assert not dest.exists();dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'output':str(dest),'raw_sha256':raw(dest),
 'positive_guard_receipt':yes,'negative_guard_receipt':no,'native_proof_created':False},ensure_ascii=False,indent=2))
