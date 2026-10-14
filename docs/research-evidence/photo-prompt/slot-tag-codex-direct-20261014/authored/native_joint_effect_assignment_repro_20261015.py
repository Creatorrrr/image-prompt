"""Read-only diagnostic. Manually authored isolated fixtures; no actual proof edits.

Run with env-i and sandbox-exec deny network*. Only --output creates a new,
explicit immutable research result. Synthetic vectors are constants, not inference.
"""
from pathlib import Path
import argparse, copy, hashlib, json, sys, tempfile, traceback

ROOT = Path(__file__).resolve().parents[5]
SCRIPTS = ROOT / 'skills/photo-prompt-image-generator/scripts'
sys.path[:0] = [str(ROOT), str(SCRIPTS)]
from tests.test_photo_semantic_evidence import source, fact, owner_map, seal, core, A
from tests.test_photo_native_compound_evidence import dependencies, B
from tests.test_photo_native_owner_selection import (P, texture_source, owner_core,
    selections, sign_core, owner_pack, chosen_composition)
from tests.photo_native_schema import slot
import photo_candidate_corpus as c
import photo_semantic_evidence as e
import photo_search_layout as layout
import prompt_generator as g
import audit_composed_prompt as audit
import audit_image_render_request as render

R = ROOT / 'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
BATCH = R / 'native_batches/root-00000-00020-01/BATCH-WIRE-02.json'
PIN = '26ad6216c781ae3cf24ea8a71997fcf6f1a098c70ed9b6c19749ee79bc1fef9b'
FILES = [SCRIPTS / name for name in ['photo_semantic_evidence.py',
    'photo_candidate_corpus.py', 'photo_shared_views.py', 'photo_candidate_realizations.py',
    'photo_candidate_semantics.py', 'photo_search_layout.py', 'prompt_generator.py',
    'audit_composed_prompt.py', 'audit_image_render_request.py']]
FILES += [ROOT / 'tests/test_photo_native_source_guards_v2.py', BATCH]

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def error_or(fn):
    try: return {'returned': fn()}
    except (ValueError, KeyError, TypeError) as exc: return {'error': str(exc)}

def lens_source(cid, value, *, other_property=False, operation='set_value',
                value_type=None, prerequisite=None, receivers=()):
    # These are synthetic source records. Actual ordinal 9/17 remain untouched.
    prop = 'lens.other_explicit_setting' if other_property else 'lens.focal_length_mm'
    text = ('The existing camera has the explicitly declared prior focal length 50mm; '
            if prerequisite is not None else '')
    text += 'Set the existing camera focal length to '+value+'mm.'
    if other_property: text = 'Set the existing camera other explicit setting to '+value+'.'
    if receivers: text += ' The named receiver is the existing scene.'
    rows = []
    if prerequisite is not None:
        rows.append(fact('prior','camera','camera','lens.focal_length_mm','prerequisite',
            prerequisite,[],quote='prior focal length 50mm'))
    row = fact('setting','camera','camera',prop,'effect',value,
        ['prior'] if prerequisite is not None else [], quote=value+'mm' if not other_property else value,
        operation=operation,receivers=list(receivers))
    if value_type is not None: row['value']['type']=value_type
    rows.append(row)
    mapping={'schema':e.SELECTOR_OWNER_SCHEMA,'bindings':[{'target':target,'origin':'existing',
        'introduced_by':None,'selector':{'kind':'selected_existing_owner'}}
        for target in ['camera',*receivers]]}
    data=source(text,rows,{'lens':slot('lens',['camera'],property_prefixes=['lens.'])},
        {'base':mapping})
    rec=data['candidates'].pop(A);rec['id']=cid;data['candidates'][cid]=rec
    return seal(data,{'lens':['setting']},cid=cid)

def lens_core(*,prior=False):
    values=[('subject',owner,'entity.presence','present')
        for owner in ['camera_A','camera_B','scene_A']]
    if prior: values.append(('camera','camera_A','lens.focal_length_mm','50'))
    frozen=core(['camera_A','camera_B','camera_alias','scene_A','scene_alias'],values,
        [('equivalent','camera_A','camera_alias'),('equivalent','scene_A','scene_alias'),
         ('disjoint','camera_A','camera_B'),('disjoint','scene_A','camera_A'),
         ('disjoint','scene_A','camera_B')],role_bindings={'recording_camera':'camera_A'})
    if prior:
        frozen['intent_lock']['locked_dimensions'].remove('camera')
        frozen['intent_lock']['open_dimensions'].append('camera')
        frozen['intent_lock']['semantic_anchors']=[{'dimension':'camera','target':'camera_A',
            'property':'lens.focal_length_mm'}]
    return sign_core(frozen)

def choice(data,frozen,owner_b='camera_A',*,receiver_alias=False,texture=False):
    entries=[]
    for cid in data['candidates']:
        p=data['candidates'][cid]['content']['role_evidence']
        bindings=[]
        for row in p['owner_maps']['base']['bindings']:
            target=row['target']
            owner=('coat_surface' if texture else 'camera_A') if cid==P else owner_b
            if target=='scene':owner='scene_alias' if receiver_alias and cid==B else 'scene_A'
            bindings.append({'target':target,'owner_id':owner})
        entries.append({'candidate_id':cid,'realization_id':'base','meaning_sha256':p['meaning_sha256'],
            'qualification_sha256':c.digest(p),'bindings':bindings})
    return {'schema':e.OWNER_SELECTION_SCHEMA,'core_sha256':frozen['canonical_sha256'],
        'owner_graph_sha256':c.digest(e.frozen_witnesses(frozen)['graph']),'entries':entries}

def combine(left,right,*,required=False):
    data=copy.deepcopy(left);data['candidates'].update(copy.deepcopy(right['candidates']))
    if required:
        data['candidates'][P]['record_kind']='visual_bundle'
        data['candidates'][P]['content']['member_candidates']=[{'candidate_id':B,'adoption':'required','requirements':{}}]
        dependencies(data,P,'base',[B]);seal(data,{'lens':['setting']},cid=P)
    c.validate(data)
    return data

def direct_case(name,*,value='24',owner_b='camera_A',required=False,other_property=False,
                operation='set_value',value_type=None,prior=False,receivers=(),receiver_alias=False,receiver_b_absent=False):
    data=combine(lens_source(P,'50',receivers=receivers,other_property=prior),
        lens_source(B,value,other_property=other_property,operation=operation,value_type=value_type,
                    prerequisite='50' if prior else None,receivers=() if receiver_b_absent else receivers),required=required)
    frozen=lens_core(prior=prior);selected=choice(data,frozen,owner_b,receiver_alias=receiver_alias)
    results=[]
    for mode in ['full','compact']:
        view=data if mode=='full' else {**data,'candidates':{cid:layout.guard_record(rec,data)
            for cid,rec in data['candidates'].items()}}
        entries=[c.entry(view,cid,realization_id='base',owner_selections=selected)
                 for cid in ([P] if required else [P,B])]
        composed={'chosen_candidate_ids':[P] if required else [P,B],
            'candidate_interpretations':[{'candidate_id':cid,'realization_id':'base'}
                for cid in ([P] if required else [P,B])], 'owner_selections':selected}
        results.append({'view':mode,'admissions':[e.admission(entry,frozen) for entry in entries],
            'permission_scopes':[error_or(lambda entry=entry:e.permission_scope(entry,frozen)) for entry in entries],
            'eligibility':[g.core_entry_eligible(view,frozen,{'subject_category':'object','intent_constraints':{'domains':[]}},
                {'subject':{}},'',entry) for entry in entries],
            'final_native_adoption_failures':audit.audit_native_adoptions({'authorial_core':frozen,'creative_controls':{}},composed,view)})
    return {'case':name,'required_child':required,'source':data,'frozen_core':frozen,'owner_selections':selected,'results':results}

def within_cid_control():
    data=lens_source(P,'50');rec=data['candidates'][P]
    rec['content']['en']+=' Set another explicit local camera address to 24mm.'
    rec['effects']['properties'].append({'dimension':'camera','target':'other_camera','property':'lens.focal_length_mm'})
    proof=rec['content']['role_evidence']
    proof['facts'].append(fact('other','camera','other_camera','lens.focal_length_mm','effect','24',[],
        quote='24mm',operation='set_value',receivers=[]))
    proof['owner_maps']['base']['bindings'].append({'target':'other_camera','origin':'existing',
        'introduced_by':None,'selector':{'kind':'selected_existing_owner'}})
    seal(data,{'lens':['setting','other']},cid=P);c.validate(data)
    frozen=lens_core();selected=choice(data,frozen);rows=[]
    for mode in ['full','compact']:
        view=data if mode=='full' else {**data,'candidates':{P:layout.guard_record(rec,data)}}
        entry=c.entry(view,P,realization_id='base',owner_selections=selected)
        result=e.admission(entry,frozen);scope=error_or(lambda:e.permission_scope(entry,frozen))
        assert result['allowed'] is False and 'conflicting actual-owner effect assignment' in scope['error']
        rows.append({'view':mode,'admission':result,'permission_scope':scope})
    return {'source':data,'frozen_core':frozen,'owner_selections':selected,'results':rows}

def smooth_texture():
    # Exact manual before/after: cracked -> smooth only on the effect clause/value;
    # presence/leather prerequisites, owner selector, operations and receivers retained.
    data=texture_source(B);rec=data['candidates'][B]
    rec['content']['en']='A smooth texture is applied to the existing leather surface, preserving its carrier and leather identity.'
    row=next(f for f in rec['content']['role_evidence']['facts'] if f['id']=='cracks')
    row['quote']='smooth';row['value']['value']='smooth'
    rec['content']['role_evidence']['review']['basis']='Manually authored isolated smooth texture variant; not an actual source correction or approval.'
    return seal(data,{'texture':['cracks']},cid=B)

def pack_case(required):
    data=texture_source();data['candidates'][B]=smooth_texture()['candidates'][B]
    if required:
        data['candidates'][P]['record_kind']='visual_bundle'
        data['candidates'][P]['content']['member_candidates']=[{'candidate_id':B,'adoption':'required','requirements':{}}]
        dependencies(data,P,'base',[B]);seal(data,{'texture':['cracks']},cid=P)
    c.validate(data);before_source=c.digest(data)
    with tempfile.TemporaryDirectory(prefix='native-joint-diagnostic-') as temp:
        _,pack,runtime,query=owner_pack(Path(temp),data,bundle_refs=[P] if required else [])
        try:
            frozen=pack['authorial_core'];before_pack=c.digest(pack)
            composed=chosen_composition(pack,runtime)
            phrase='A smooth texture is also explicitly assigned across that same existing secondary leather coat surface.'
            composed['prompt_en']+=' '+phrase
            composed['owner_selections']=choice(data,frozen,'coat_surface',texture=True)
            if not required:
                composed['chosen_candidate_ids'].append(B)
                row={'candidate_id':B,'realization_id':'base','artistic_interpretation':'Retain the existing leather identity.',
                    'transformation':'Assign smooth texture to the same existing coat surface.',
                    'prompt_evidence':phrase,'affected_properties':[{'dimension':'material','target':'coat_surface','property':'texture.surface'}]}
                composed['candidate_interpretations'].append(row)
                for decision in composed['creative_augmentation_brief']['decisions']:
                    if decision['candidate_id']==B:
                        decision.update(row,decision='transformed',rationale='Apply the explicitly authored smooth texture.',affected_dimensions=['material'])
                        composed['candidate_interpretations']=[r for r in composed['candidate_interpretations'] if r['candidate_id']!=B]
            composed['embodiment_review']['review']['prompt_sha256']=hashlib.sha256(composed['prompt_en'].encode()).hexdigest()
            report=audit.audit_composed_prompt(pack,composed,source_data=runtime,query_context=query)
            resolution=report.get('native_owner_resolution') or {}
            request={'schema_version':'photo-image-render-request/v2','pack_id':pack['pack_id'],
                'global_retrieval_sha256':pack['global_retrieval']['canonical_sha256'],
                'source_intent_lock_sha256':frozen['intent_lock']['canonical_sha256'],
                'source_embodiment_preflight_sha256':pack['embodiment_preflight']['canonical_sha256'],
                'runtime_prompt_en':composed['prompt_en']+'\n\nAvoid: '+composed['negative_en'],
                'runtime_negative_en':composed['negative_en'],'references':[],
                'audit_boundary':{'composed_prompt_audit_status':'pass','runtime_prompt_audit_status':'not_run',
                    'inherits_composed_prompt_pass':False},
                'native_owner_resolution_sha256':resolution.get('canonical_sha256'),
                'source_composed_sha256':resolution.get('composed_sha256')}
            with audit.bound_native_source(runtime,query):
                runtime_result=render.audit_image_render_request(pack,composed,request)
            assert c.digest(pack)==before_pack
            return {'case':'required_child' if required else 'independent_chosen',
                'data_sha256_before_pack_policy_fixture':before_source,'fixture_data':data,
                'pack':pack,'composed':composed,'audit':report,'render_boundary':runtime_result,
                'render_request':request,
                'pack_immutable':True,'runtime_mode':'isolated lazy search layout, constant synthetic vectors; no provider/acquire/image rendering'}
        finally:runtime.reader.close()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    assert not args.output.exists(),'immutable research output already exists'
    before={str(path.relative_to(ROOT)):sha(path) for path in FILES}
    assert sha(BATCH)==PIN
    batch=json.loads(BATCH.read_text());actual=[]
    for row in batch['records']:
        if row['ordinal'] not in [9,17]:continue
        proof=row['proof'];rec=copy.deepcopy(row['source_after'])
        assert e.meaning_sha256(rec)==proof['meaning_sha256']
        assert e.native_contract_sha256(proof)==proof['review']['native_review']['native_contract_sha256']
        for f in proof['facts']:
            assert f['quote'] in e.positive_string(rec,f['pointer'],realization_id=f['realization_id'])
        actual.append({'ordinal':row['ordinal'],'candidate_id':row['candidate_id'],
            'source_after_sha256':c.digest(rec),'proof_sha256':c.digest(proof),
            'effects':[f for f in proof['facts'] if f['mode']=='effect'],'owner_maps':proof['owner_maps'],
            'meaning_and_signature_and_positive_quotes_exact':True})
    cases=[]
    options=[('conflicting_values',{}),('identical_values',{'value':'50'}),
        ('explicit_owner_alias_conflict',{'owner_b':'camera_alias'}),
        ('explicit_disjoint_owners',{'owner_b':'camera_B'}),
        ('distinct_properties',{'other_property':True}),
        ('type_conflict',{'value':'50','value_type':'lens.other_explicit_value/v1'}),
        ('operation_conflict',{'value':'50','operation':'relocate'}),
        ('receiver_set_conflict',{'value':'50','receivers':('scene',),'receiver_b_absent':True}),
        ('canonical_receiver_alias_identical',{'value':'50','receivers':('scene',),'receiver_alias':True}),
        ('prerequisite_old_effect_new',{'prior':True})]
    for required in [False,True]:
        for name,kw in options:cases.append(direct_case(name,required=required,**kw))
    packs=[]
    for required in [False,True]:
        try:packs.append(pack_case(required))
        except (ValueError,KeyError,TypeError) as exc:
            packs.append({'case':'required_child' if required else 'independent_chosen',
                'execution_error':str(exc),'traceback':traceback.format_exc(),
                'limitation':'Pack generation did not reach final/runtime audit; no success claim.'})
    after={str(path.relative_to(ROOT)):sha(path) for path in FILES};assert before==after
    result={'schema':'photo-native-joint-effect-assignment-diagnostic/v1',
        'revision':'r02; r01 retained as initial execution evidence',
        'read_only_inputs':before,'actual_rows_read_and_exact_checked':actual,
        'direct_cases':cases,'within_cid_rejection_control':within_cid_control(),
        'public_pack_cases':packs,'inputs_unchanged':True,
        'count':{'direct_cases':len(cases),'full_compact_executions':2*len(cases),'public_pack_cases':len(packs)},
        'limits':['Isolated synthetic declarations and constant vectors; not actual native approval, full corpus truth or image pixels.',
                  'Actual two root proofs only read and exact checked; never attached to an operating or fixture corpus.',
                  'Direct-case final_native_adoption_failures use an incomplete diagnostic core/controls envelope, so context/schema failures are not value-conflict detection evidence. Only the real frozen public-pack final audit is authoritative for that boundary.',
                  'Render boundary uses the explicit workflow transport shape and exact fresh composed mapping/hash; no provider, operating snapshot acquire or image rendering is called.']}
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'output':str(args.output),'raw_sha256':sha(args.output),'count':result['count'],
        'pack_results':[{'case':p['case'],'status':p.get('audit',{}).get('status'),
            'failures':p.get('audit',{}).get('failures'),'execution_error':p.get('execution_error'),
            'render_failures':p.get('render_boundary',{}).get('failures')} for p in packs]},ensure_ascii=False))

if __name__=='__main__':main()
