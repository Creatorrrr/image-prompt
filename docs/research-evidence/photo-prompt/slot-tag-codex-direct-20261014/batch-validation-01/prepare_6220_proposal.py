"""Freeze a reviewable complete controlled-core proposal; no search/adoption.

Root supplied the exact controlled meaning and final phrase. The existing
reviewed fixture supplies only its identical typed assertions/owner addresses.
Root must read and approve the complete output before any candidate is adopted.
"""
import ast, copy, hashlib, json
from pathlib import Path
import run as batch
import creative_controls
import photo_authoring_wire as wire
import photo_embodiment_review as embodiment

O=batch.OUT/'native6220-proposal-04';O.mkdir(exist_ok=False)
T='This controlled request declares the existing whole image image_A as the image context. Its object contours are continuous and its small surface details are readable; preserve both. The unrelated owner other_A is distinct and disjoint. Image detail may be refined without creating or altering depicted physical objects.'
FINAL='Clean, continuous photographic edges, with continuous object contours and readable small surface details preserved on the same whole image.'
path=batch.R/'authored/native_05250_simple5-source96.check-v1.py'
raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()=='fdb0ea0fff17dae462f41833286472b2110605f3c97eff6b57a278bff53751ad'
module=ast.parse(raw)
fixture=next(node for node in module.body if isinstance(node,ast.FunctionDef) and node.name=='fixture')
ns={'n':batch.native,'EXPECTED':{6220:[('style','image.detail')]}}
exec(compile(ast.Module(body=[fixture],type_ignores=[]),str(path),'exec'),ns)
old=ns['fixture'](6220)
envelope={'contract_version':'photo-request-envelope/v1','provenance':'requesting_user',
    'request_id':'root-controlled-native6220-proposal-01','request_text':T,
    'request_sha256':hashlib.sha256(T.encode()).hexdigest(),
    'active_spans':[{'span_id':'controlled_request','start':0,'end':len(T),'text':T}]}
envelope=wire.normalize_request_envelope(envelope)
controls=creative_controls.resolve(T,context={'subject_category':'nonhuman','no_people':False,'explicit_nonsexual':False},seed=6220)
rows=copy.deepcopy(old['semantic_assertions'])
for row in rows:row['evidence']={'controlled_request':T}
core={'contract_version':'photo-authorial-core/v3','provenance':'agent_prepack',
    'interpreted_intent':'Controlled integrity case for the same existing whole image image_A. Preserve its already continuous contours and readable small details while leaving image detail refinement open. The unrelated other_A remains disjoint. This is a synthetic controlled request, not a real image observation.',
    'subject':'the existing whole image image_A','setting':'the same existing whole-image context',
    'event':'image detail refinement remains open',
    'visual_priorities':['continuous object contours','readable small surface details','the same whole image image_A'],
    'baseline_prompt_en':T,'user_definitions':[],
    'interpretation_provenance':[{'term':'governing controlled request','source_text':T,'basis':'request_context',
        'resolution':'Use only the exact root-reviewed existing image meaning and preservation properties. No clean_edges effect is required by the baseline.','sources':[]}],
    'unresolved_ambiguities':[],'user_exclusions':[],'runtime_forbidden_labels':[],
    'semantic_assertions':rows,
    'intent_lock':{'contract_version':'photo-intent-lock/v2','priority':'requesting_user',
        'locked_dimensions':['concept','subject','setting','event'],
        'open_dimensions':['style'],
        'semantic_anchors':[{'anchor_id':'controlled_concept','dimension':'concept','source_text':T,
            'prompt_evidence':'without creating or altering depicted physical objects'},
            {'anchor_id':'image_context','dimension':'setting','source_text':T,'prompt_evidence':'as the image context'},
            {'anchor_id':'open_refinement','dimension':'event','source_text':T,'prompt_evidence':'Image detail may be refined'},
            {'anchor_id':'same_image','dimension':'subject','source_text':T,
            'prompt_evidence':'the existing whole image image_A'},
            {'anchor_id':'contours','dimension':'style','target':'image','property':'image.contour.continuity',
                'source_text':T,'prompt_evidence':'Its object contours are continuous'},
            {'anchor_id':'details','dimension':'style','target':'image','property':'image.small_surface_detail.readability',
                'source_text':T,'prompt_evidence':'its small surface details are readable'}]},
    'style':{'domain':'general_photo','family':'controlled whole-image detail integrity case',
        'evidence':['Its object contours are continuous','its small surface details are readable']},
    'request_lineage':None,'variation_key':'root-controlled-native6220-proposal-01','source_request':T,
    'creative_controls_sha256':controls['canonical_sha256']}
normalized=wire.normalize_authorial_core(core,request_envelope=envelope,creative_control_snapshot=controls)
review={'contract_version':'photo-embodiment-review/v1','provenance':'agent_prepack','scope':'not_applicable',
    'summary':'This controlled whole-image detail request declares no articulated body or body interaction. It preserves existing depicted physical objects without adding them.',
    'checks':{},'prompt_sha256':hashlib.sha256(T.encode()).hexdigest()}
embodiment.build_policy(normalized,review)
for name,value in [('REQUEST-ENVELOPE.json',envelope),('CREATIVE-CONTROLS.json',controls),('AUTHORIAL-CORE-INPUT.json',core),
        ('AUTHORIAL-CORE-NORMALIZED.json',normalized),('EMBODIMENT-REVIEW.json',review),
        ('PROPOSAL-SCOPE.json',{'schema':'photo-controlled-native6220-core-proposal/v1','root_full_json_review_required':True,
            'request_meaning_supplied_by_root':True,'existing_typed_fixture_file':str(path.relative_to(batch.ROOT)),
            'existing_typed_fixture_raw_sha256':hashlib.sha256(raw).hexdigest(),'typed_assertions_retained_except_source_evidence_text':True,
            'final_addition_phrase_proposed_by_root':FINAL,'adoption_executed':False,'native_approvals_created':0,
            'canonical_property_anchor_target':'image existing role resolves to the unchanged image_A owner; no new alias or owner',
            'boundary':'A reviewable controlled complete-core proposal only. Structure normalization and hashes do not prove semantic truth.'})]:
    (O/name).write_bytes(batch.c.canonical_bytes(value)+b'\n')
print(O)
