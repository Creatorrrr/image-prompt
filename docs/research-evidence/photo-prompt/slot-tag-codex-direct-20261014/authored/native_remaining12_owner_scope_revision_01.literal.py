"""First five individually reviewed source-only owner/effect proposals.

No native proof/fact ID/signature/acceptance is produced. P/E plans below are
manual authoring intentions; only copying, deltas and hashes are mechanical.
"""
from pathlib import Path
import copy, gzip, hashlib, json
R=Path(__file__).resolve().parents[1]
P=R/'authored/native_11870_formal03_remaining_pending_source_proposals_v1.json'
OLD=json.loads(P.read_text());assert hashlib.sha256(P.read_bytes()).hexdigest()=='c961d3db79e11e0e5cea008733eca78089937c3e9b77fcb46899a12d41db88d3'
CAT=json.loads((R/'CATALOG-FINAL-144-V4.json').read_text())
CURRENT=json.loads(gzip.decompress((R/'native-inputs/11870-01250-01300-plan-03/CURRENT-PROPOSAL.json.gz').read_bytes()))
ORIGINAL=json.loads(gzip.decompress((R/'SOURCE.json.gz').read_bytes()))
def digest(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert digest(CURRENT)=='30924a72de7d3011af26b7ef7c0192ff12edd732131f3c18ed29748e805d5477'
assert digest(CAT)=='5bc5f6d185b6ef6e2d8d3a2bf6e4aa02d73e22143b0529a233fd5f98ddbed908'
def F(owner,dim,prop,value):return {'kind':'frozen_value','owner':owner,'dimension':dim,'property':prop,'value':{'type':prop+'/v1','value':value}}
def D(left,right):return {'kind':'owner_relation','relation':'disjoint','left':left,'right':right}
def E(dim,target,prop,value,receivers=(),operation='set_value',value_type=None):
    return {'mode':'effect','dimension':dim,'target':target,'property':prop,
        'value':{'type':value_type or prop+'/v1','value':value},'operation':operation,'receivers':list(receivers)}
MANUAL={
1255:{'option':'same_holder_existing_item','application':
    'Use the independently declared existing holder and held object explicitly selected by the caller. They must be explicitly disjoint actual owners in the frozen graph. The subject in English and 자기 in Korean denote that same holder. Select that holder holding that same object neutrally near their own side. Holding, near-self placement and neutral presentation are all chosen effects, not already-held or already-placed prerequisites. The holder/object E receiver addresses must be reciprocal as specified below. Do not invent a hand, finger, object type, other person, threat, offering or private intent.',
    'common_guards':[D('holder','held_object')],
    'plans':{'base':{'targets':['holder','held_object'],'guards':[],
        'effects':[E('action','holder','action.holding','holding_same_selected_object',['held_object']),
            E('composition','held_object','props.placement.near_same_holder','near_same_selected_holder',['holder'],'relocate'),
            E('role','held_object','prop.state.neutral_presentation','neutral_presentation')] }},
    'reading':'The Korean co-reference supports one same holder; it does not supply specific hands or an object type. Disjoint graph scope is an explicit existing-application restriction, not a string-inequality inference.',
    'boundary':'No pre-frozen holding/placement/state relation is required. Those are the mutable meaning and remain E. No new part_of or assigned-owner relation is fabricated.'},
1256:{'option':'blank_badge_or_text_unspecified_access_card','application':
    'Use the independently declared existing human gaze carrier with independently declared actual eyes on that same carrier. Select exactly one existing target of the actual branch: a badge or an access card, not an invented combined access-token type. Require explicit frozen disjointness between this gaze carrier and that selected target for this application. Select gaze toward that exact target. On blank_badge only, also select absence of lettering on that badge as a real text-state effect. On access_card make no lettering or blankness selection. Preserve the intrinsic human guard and the independent old presentation restrictions. Add no eye, actor, target, office, access authority or head orientation.',
    'common_guards':[F('gaze_owner','subject','entity.category','human'),F('gaze_owner','subject','anatomy.eyes.presence','present'),D('gaze_owner','target')],
    'plans':{
        'blank_badge':{'targets':['gaze_owner','target'],'guards':[F('target','subject','props.type','badge')],
            'effects':[E('expression','gaze_owner','gaze.target','same_selected_branch_target',['target']),
                E('text','target','text.lettering.presence','absent')]},
        'access_card':{'targets':['gaze_owner','target'],'guards':[F('target','subject','props.type','access_card')],
            'effects':[E('expression','gaze_owner','gaze.target','same_selected_branch_target',['target'])]}},
    'reading':'Root-preferred least-added modifier scope retained. Blankness is not imposed on the access-card branch. Lettering absence is an actual text footprint; it must not pass a frozen text lock merely because a prior proposal placed it only under role/prop.state.',
    'boundary':'No extra face-presence, separate eye node or part_of relation is inferred from gaze. Atomic eyes is on the selected gaze carrier. Disjointness is an explicit bounded application; an actually overlapping/part-owned target requires separate adjudication, not fake disjoint metadata. Absence of lettering is not automatically a positive visible_text tag.'},
1258:{'option':'same_operator_tester_actual_voltage_check','application':
    'Use the independently declared existing human operator, existing voltage tester and existing electrical-potential measurement target explicitly selected by the caller. The operator and tester must have independently declared disjoint actual scope. Select that same operator checking voltage safely with that same tester at that same selected target; the action receivers bind the tester and measurement target jointly. Safely remains a qualification of the actual selected checking E, not a frozen safety-context substitute or real-world safety certification. No pre-existing use/holding/checking relation is assumed. The selected target may be a whole or part only as independently declared; do not invent disjointness or part_of between tester and measurement target, wiring, contact geometry, probes, PPE, a voltage, result or completion.',
    'common_guards':[F('operator','subject','entity.category','human'),F('tester','subject','props.type','voltage_tester'),
        F('tested_endpoint','concept','measurement.target_domain','electrical_potential'),D('operator','tester')],
    'plans':{'base':{'targets':['operator','tester','tested_endpoint'],'guards':[],
        'effects':[E('action','operator','action.checking_voltage_safely_with_same_tester',
            'safe_voltage_check_with_same_selected_tester_and_target',['tester','tested_endpoint'])]}},
    'reading':'The performed operator/tool/target relation belongs to this E and its exact receiver SET. A pre-frozen currently-testing/using relation would improperly hide the action. An independently declared electrical measurement target is a new explicit applicability condition, not supplied by a tester noun.',
    'boundary':'The body does not prescribe tester-to-target contact or a particular whole/part topology. Do not guess it. If a concrete request requires further port/system/part relations for the performed action, author those exact requested witnesses in a new literal before native review; this source proposal does not assert unknown topology is valid. A frozen designated-target relation can be added only if the new source explicitly makes that extra precondition, not as a default.'},
1273:{'option':'existing_small_toy_or_branches','application':
    'Select exactly one actual realization of the original action-figure OR doll alternative. Independently require the precise already-existing identity of that same selected object for its branch. Select that same object as a small scene prop. Smallness and scene-prop role are real mutable E, not pre-frozen small/prop-state conditions. Do not add a toy, actor, child, body part, holder, comparative size ratio, count, manufacture or motion. Preserve intrinsic human applicability separately; it does not classify the toy as a human.',
    'common_guards':[],
    'plans':{
        'small_action_figure':{'targets':['toy'],'guards':[F('toy','subject','props.type','action_figure')],
            'effects':[E('appearance','toy','object.geometry.size','small'),E('role','toy','props.scene_role','scene_prop')]},
        'small_doll':{'targets':['toy'],'guards':[F('toy','subject','props.type','doll')],
            'effects':[E('appearance','toy','object.geometry.size','small'),E('role','toy','props.scene_role','scene_prop')]}},
    'reading':'The OR is retained with precise per-RID type P. Current object_structure actually owns non-anatomical object.geometry under appearance, so size keeps that dimension. Small alone supplies no comparative scale_relation basis.',
    'boundary':'No synthetic generic figure_or_doll type, no simultaneous type conjunction and no inferred represented face/eyes/body anatomy. Introducing a toy is a separate source application with actual entity/count/subject effects; not covered here.'},
1284:{'option':'same_face_carrier_owned_eyes','application':
    'Use the independently declared existing image bound explicitly to the common image role and the existing face carrier explicitly selected by the caller. There is no automatic primary-face selection. Independently require subject/anatomy.face.presence/anatomy.face.presence/v1/present and subject/anatomy.eyes.presence/anatomy.eyes.presence/v1/present on that same actual face carrier. Select the image focal plane precisely on that carrier own eye region in the stated album-cover style. The E receiver is that same face carrier, with eye-region scope encoded in the chosen focal-plane value; no separate eye owner is created. Preserve the original kpop-or-album eligibility condition. Add no eyes, face, lens, depth extent, actual album release or publication format.',
    'common_guards':[F('face','subject','anatomy.face.presence','present'),F('face','subject','anatomy.eyes.presence','present')],
    'plans':{'base':{'targets':['image:core_role=image','face'],'guards':[],
        'effects':[E('camera','image','focus.selected_plane','precise_owned_eyes_of_same_selected_face_in_album_cover_style',['face'],'select_plane')]}},
    'reading':'The original positive phrase does not choose primary_face. This revision removes that prior application-only narrowing and preserves atomic eyes on the exact selected face carrier. It is an actual focal-plane E, not sharpness postprocessing or preserved existing focus.',
    'boundary':'Atomic eyes presence on a face carrier is not a separate eye owner or automatic anatomical part edge. A core that only describes a separate eyes node cannot silently inherit this tuple onto the face; it needs a separately explicit application/witness. Album-cover qualifier is preserved in the chosen focal-plane value and original eligibility, not expanded into a new release format.'},
}

def endpoint(cid,target):return {'kind':'source_target','candidate_id':cid,'target':target}
def guards(cid,rows,prefix):
    result=[]
    for i,row in enumerate(rows):
        value={'id':prefix+'_'+str(i),**copy.deepcopy(row)}
        for key in ['owner','left','right']:
            if key in value:value[key]=endpoint(cid,value[key])
        result.append(value)
    return {'schema':'photo-native-source-guards/v2','rules':result}
def mapping(targets):
    rows=[]
    for target in targets:
        if ':core_role=' in target:target,role=target.split(':core_role=');selector={'kind':'core_role','role':role}
        else:selector={'kind':'selected_existing_owner'}
        rows.append({'target':target,'origin':'existing','introduced_by':None,'selector':selector})
    return {'schema':'photo-native-owner-bindings/v3','bindings':rows}
def footprint(rows):return {'dimensions':sorted({r['dimension'] for r in rows}),
    'properties':[{k:r[k] for k in ['dimension','target','property']} for r in rows]}

records=[]
for ordinal,manual in MANUAL.items():
    old=next(row for row in OLD['proposals'] if row['ordinal']==ordinal);cid=old['candidate_id']
    assert old['whole_before_source']==CURRENT['candidates'][cid] and old['whole_original_source']==ORIGINAL['candidates'][cid]
    prior=next(opt for opt in old['options'] if opt['option_id']==manual['option'])
    after=copy.deepcopy(prior['whole_proposed_after_source']);before=copy.deepcopy(old['whole_before_source'])
    after['content']['application_contract']=manual['application']
    if manual['common_guards']:after['conditions']['native_guards']=guards(cid,manual['common_guards'],'common')
    if 'realizations' in after['effects']:
        after['effects']['dimensions']=[];after['effects']['properties']=[]
        for branch in after['effects']['realizations']['branches']:
            plan=manual['plans'][branch['id']];branch['effects']=footprint(plan['effects'])
            if plan['guards']:branch['conditions']['native_guards']=guards(cid,plan['guards'],'branch')
    else:after['effects']=footprint(manual['plans']['base']['effects'])
    delta=[{'pointer':'/content/application_contract','before_exists':'application_contract' in before['content'],'after_exists':True,
        'before':before['content'].get('application_contract'),'after':manual['application'],'reason':manual['reading']},
        {'pointer':'/conditions','before_exists':True,'after_exists':True,'before':before['conditions'],'after':after['conditions'],'reason':'Consume explicit existing-carrier/topology guards; intrinsic conditions remain ANDed.'},
        {'pointer':'/effects','before_exists':True,'after_exists':True,'before':before['effects'],'after':after['effects'],'reason':'Keep every manually reviewed actual selected E and its per-RID footprint.'}]
    for key in ['ko','realization_content']:
        if after['content'].get(key)!=before['content'].get(key):delta.append({'pointer':'/content/'+key,'before_exists':key in before['content'],
            'after_exists':True,'before':before['content'].get(key),'after':copy.deepcopy(after['content'][key]),'reason':'Preserve the explicitly chosen original OR / translation clarification from the prior source proposal.'})
    records.append({'ordinal':ordinal,'candidate_id':cid,'prior_option_id':manual['option'],'source_before':before,
        'source_before_sha256':digest(before),'prior_source_after':copy.deepcopy(prior['whole_proposed_after_source']),
        'prior_source_after_sha256':prior['proposed_after_source_sha256'],'source_after':after,'source_after_sha256':digest(after),
        'exact_top_delta':delta,'complete_own_bindings_unchanged':copy.deepcopy(old['complete_own_bindings']),
        'original_compiled_locator':old['original_compiled_locator'],'original_compiled_row_sha256':old['original_compiled_row_sha256'],
        'owner_plans':{rid:mapping(plan['targets']) for rid,plan in manual['plans'].items()},
        'manual_P_E_receiver_intent_not_a_native_proof':copy.deepcopy(manual['plans']),
        'independent_reading':manual['reading'],'remaining_limits':manual['boundary']})
spec_keys=sorted({k for row in OLD['proposals'] if row['ordinal'] in MANUAL for k in row['relevant_full_current_specs']})
payload={'schema':'photo-native-source-owner-scope-revision/v1','author':'/root/native_evidence','batch':1,
    'input_proposal':{'file':str(P),'raw_sha256':hashlib.sha256(P.read_bytes()).hexdigest()},
    'current_source_canonical_sha256':digest(CURRENT),'catalog_canonical_sha256':digest(CAT),
    'actual_read_ordinals':list(MANUAL),'whole_full_specs_read':{k:CAT[k] for k in spec_keys},
    'records':records,'source_choices_not_applied':True,'proof_or_signature_or_status_updates':0,
    'new_custom_witnesses':'entity.category/props.type/measurement.target_domain remain new exact candidate-free core authoring obligations; common atomic face/eyes presence use the current neutral protocol, never inferred from roles or category.',
    'limits':['Source-only proposals require root whole-after semantic selection and a fresh immutable input before native review.',
        'No actual source, binding, catalog, code, runtime, registry or Git mutation; no provider/network/inference call.',
        'Disjoint and other new prerequisites are explicit bounded application conditions, not names-based graph inferences. Unknown remains unsatisfied.']}
OUT=R/'authored/native_remaining12_owner_scope_revision_01.json'
if __name__=='__main__':
    assert not OUT.exists();OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'output':str(OUT),'records':len(records),'raw_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest()},ensure_ascii=False))
