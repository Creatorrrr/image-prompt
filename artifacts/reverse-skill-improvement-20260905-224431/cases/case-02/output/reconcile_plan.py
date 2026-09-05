import json,hashlib,datetime
from pathlib import Path
p=json.loads(Path('output/plan.draft.json').read_text());c=p['render_contract'];ct=c['color_tone_contract']
for e in c['aggregate_effects']:
 if e['id'] in ['effect-front','effect-shoulder-slope']:e['region_ids']=['person']
for r in c['component_relations']:
 if r['id']=='diagonal':r.pop('frame_reference');r['reference_region_id']='shorts'
# Remove color-bearing adjectives from generic ownership and give trim its color owner.
for co in c['emitted_controls']:
 if co['id']=='control-shorts':co['prompt_excerpt']=co['prompt_excerpt'].replace('thin pale piping','thin piping')
 if co['id']=='control-clutter':co['prompt_excerpt']=co['prompt_excerpt'].replace(' and dark hardware',' and hardware')
# Supporting displayed color compounds have one literal claim and a complete multi-axis effect list.
secondary={
 'shorts-hue':('intrinsic',[('shorts','hue'),('shorts','chroma')]),
 'left-wall-color':('processing',[('left-wall','hue'),('left-wall','value')]),
 'note-color':('intrinsic',[('note','hue'),('note','chroma')]),
 'counter-color':('processing',[('counter','value'),('counter','hue'),('clutter','value'),('clutter','hue')]),
 'hair-phone-color':('processing',[('hair','value'),('phone','value')])}
for id,(layer,axes) in secondary.items():
 co=next(x for x in ct['emitted_controls'] if x['id']=='control-'+id);cl=next(x for x in c['candidate_claims'] if x['id']=='claim-'+id);base=next(x for x in ct['aggregate_effects'] if x['id']=='effect-'+id)
 new=[]
 ct['aggregate_effects'].remove(base)
 for n,(reg,ax) in enumerate(axes):
  e={**base,'id':'effect-'+id+'-'+str(n),'axis':ax,'region_id':reg};ct['aggregate_effects'].append(e);new.append(e)
 cl['perceptual_effects']=[{'aggregate_effect_id':e['id'],'causal_layer':layer,'confidence':'medium','source_evidence':e['source_evidence']} for e in new]
 co.update({'causal_layer':layer,'control_role':'compound-control','aggregate_effect_ids':[e['id'] for e in new],'compound_justification':'A compact, explicitly owned displayed-color phrase preserves the inseparable low-chroma hue/value read of this bounded garment or supporting region; independent required primary garment axes are controlled separately.'});co.pop('region_id',None);co.pop('axis',None)
 for reg in ct['regions']:
  for a in reg['intrinsic_axes']:
   if a.get('aggregate_effect_id')=='effect-'+id:a.pop('aggregate_effect_id');a.update({'emission':'diagnostic-only','non_emission_reason':'Low-chroma or supporting displayed-color compound is retained as a complete multi-axis control; no separate isolated intrinsic axis is established.'})
# Trim value is literal; its hue is too indistinct for an isolated target.
from plan_helpers import color
color(p,'trim-value','The shorts piping is pale.', ['Thin trim is lighter than the shorts along hems and side seam.'],region='shorts-trim',axis='value',role='supporting')
ct['regions'].append({'id':'shorts-trim','role':'supporting','prompt_anchor':'The shorts piping','source_evidence':['Pale thin curved hems contrast against dark shorts.'],'intrinsic_axes':[{'axis':'value','observation':'The shorts piping is pale.','confidence':'high','source_evidence':['Trim is visibly lighter than shorts.'],'role':'supporting','evidence_scope':'midtone','emission':'required','aggregate_effect_id':'effect-trim-value'}],'tone_zones':[],'relative_relations':['Lighter than shorts.']})
# Explicit decisions binding all independently drifting lane obligations.
M={
'global_lane':{'phone-face-occlusion':'phone','single-reflected-figure':'photo','aspect-ratio':'photo','upper-boundary':'frame','lower-body-extent':'counter','horizontal-distribution':'frame','subject-frame-share':'frame','open-garment-silhouette':'cardigan','left-opening':'wall','right-dark-mass':'right-dark','small-note':'note','counter-band':'counter','partial-clutter':'clutter','soft-detail':'softness','surface-irregularity':'grain'},
'spatial_lane':{'ratio':'photo','single-reflection':'photo','head-scale-position':'frame','crown-crop':'frame','front-surface':'front','torso-diagonal':'diagonal','head-offset':'head-offset','shoulder-slope':'shoulder-slope','footprint':'phone','face-visibility':'phone','grip':'arms-grip','arm-asymmetry':'arms-grip','braid-placement':'hair','garment-boundaries':'cardigan','body-boundary':'counter','partial-lowered-hand':'arms-grip','note':'note','towel-rail':'wall'},
'appearance_lane':{'two-braids':'hair','fringe':'hair','unequal-lengths':'hair','neckline-straps':'top','fit':'top','hem-gap':'top','open-dropped':'cardigan','volume-cuff':'cardigan','hanging-side':'cardigan','loose-shape':'shorts','drawstring-piping':'shorts','displayed-surface':'skin-surface'},
'color_lane':{'top-hue':'top-hue','top-value':'top-value','top-chroma':'top-chroma','cardigan-hue':'cardigan-hue','cardigan-value':'cardigan-value','cardigan-chroma':'cardigan-chroma','shorts-value':'shorts-value','shorts-chroma-hue':'shorts-hue','value':'skin-value','hue':'skin-hue','chroma':'skin-chroma','left-wall':'left-wall-color','right-dark':'right-dark','note':'note-color','counter':'counter-color','hair-phone':'hair-phone-color','key':'global-key','microcontrast':'global-microcontrast','soft-form':'soft-form','occlusion-shade':'local-shade'},
'capture_lane':{'photo':'photo','global-softness':'softness','texture':'grain','low-legibility':'clutter'}}
reports=[];fds=[];ods=[];imap={i['id']:i for i in c['invariants']};priority=[]
for name,lookup in M.items():
 r=json.loads(Path('output/'+name+'.report.json').read_text());reports.append(r)
 for f in r['findings']:
  mapped=[]
  for o in f['atomic_obligations']:
   iid=lookup[o['id'].split(':')[-1]];inv=imap[iid];inv['source_obligation_ids'].append(o['id']);mapped.append(iid)
   assert not(o['proposed_role']=='primary' and inv['role']!='primary')
   ods.append({'obligation_ids':[o['id']],'disposition':'merged','final_invariant_id':iid,'final_role':inv['role'],'reason':'Visible result and source direction retained by the named consolidated literal control.'})
  iid=mapped[0];assert not(f['proposed_role']=='primary' and imap[iid]['role']!='primary')
  fds.append({'finding_ids':[f['id']],'disposition':'merged','final_invariant_id':iid,'final_role':imap[iid]['role'],'reason':'Narrative finding split among its individually bound atomic obligations: '+', '.join(dict.fromkeys(mapped))})
  priority.append({'finding_id':f['id'],'viewer_priority':f.get('priority','P1' if f['proposed_role']=='primary' else 'P2'),'invariant_ids':list(dict.fromkeys(mapped))})
# Trim detail is supported by the source and the shorts detail obligation as a second distinct value result.
imap['trim-value']['source_obligation_ids']=['lane.subject-appearance:shorts:drawstring-piping']
# Preserve literal source directions and all report IDs without changing raw reports.
order=['photo','softness','grain','frame','front','diagonal','head-offset','shoulder-slope','phone','arms-grip','hair','top','cardigan','shorts','counter','soft-form','local-shade','skin-surface','top-value','top-chroma','top-hue','cardigan-value','cardigan-chroma','cardigan-hue','shorts-value','shorts-hue','trim-value','skin-value','skin-chroma','skin-hue','global-key','global-microcontrast','note','wall','clutter','left-wall-color','right-dark','note-color','counter-color','hair-phone-color']
controls={x['id']:x for x in c['emitted_controls']+ct['emitted_controls']+c['light_form_contract']['emitted_controls']};prompt='\n\n'.join(' '.join(controls['control-'+id]['prompt_excerpt'] for id in group) for group in [order[:4],order[4:10],order[10:18],order[18:32],order[32:]])+'\n'
# All exact non-v6 geometry is also exposed for the source-aware critic.
p['supplemental_literal_spatial_audit']=[{'control_id':x['id'],'prompt_excerpt':x['prompt_excerpt'],'scope':'Complete literal clause including implicit effects','source_relations':[r for e in c['aggregate_effects'] if e['id'] in x['aggregate_effect_ids'] for r in e.get('relation_ids',[])],'intended_effect':'Retain only named projected position, occlusion, contact, coverage, or crop; no exact hidden physical rotation or support load.','review_status':'pending independent source-aware critic'} for x in c['emitted_controls'] if any(e.get('relation_ids') for e in c['aggregate_effects'] if e['id'] in x['aggregate_effect_ids'])]
Path('output/plan.review.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n');Path('output/prompt.review.txt').write_text(prompt)
canonical=json.dumps(p,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();ph=hashlib.sha256(canonical).hexdigest();promptsha=hashlib.sha256(prompt.encode()).hexdigest()
bundle={'schema_version':'reverse-image-analysis-bundle/v2','request':{'user_request':'이 이미지에서 충실한 독립형 영문 이미지 생성 프롬프트를 추출하고, 그 프롬프트만으로 이미지를 한 장 생성해줘.','intent_mode':'faithful'},'source_artifact':{'sha256':'9f22a88255115bd33062593568a9773626ccb23f8e482824752a09b91f20fc71','frame':'399x623'},'route':json.loads(Path('output/route.json').read_text()),'execution':{'mode':'mixed','prompt_frozen':False,'independence_claimed':False,'independent_lanes':['lane.global-composition','lane.spatial-topology'],'fallback_lanes':['lane.subject-appearance','lane.color-light-material','lane.medium-aesthetic-capture']},'integrated_plan':{'payload':p,'sha256':ph},'lane_reports':reports,'integration':{'status':'complete','finding_dispositions':fds,'obligation_dispositions':ods,'conflicts':[]},'adjudications':[],'coverage_review':{'reviewer_context':'independent','source_sha256':'9f22a88255115bd33062593568a9773626ccb23f8e482824752a09b91f20fc71','route_fingerprint':'822687b7c91719dff3964c9ab4e7a12db7dcae540fd98ec8cdf198cc31177975','integrated_plan_sha256':ph,'reviewed_finding_ids':[],'reviewed_obligation_ids':[],'reviewed_invariant_ids':[],'status':'blocked','issues':[{'kind':'unresolved-uncertainty','evidence':'Independent source-aware critic has not yet reviewed this draft.'}]}}
Path('output/bundle.review.json').write_text(json.dumps(bundle,ensure_ascii=False,indent=2)+'\n');Path('output/priority-map.json').write_text(json.dumps(priority,indent=2)+'\n')
Path('output/critic-input-manifest.json').write_text(json.dumps({'source_path':str(Path('source.jpg').resolve()),'source_sha256':bundle['source_artifact']['sha256'],'route_path':str(Path('output/route.json').resolve()),'route_fingerprint':bundle['route']['route_fingerprint'],'raw_report_paths':[str(Path('output/'+n+'.report.raw.json').resolve()) for n in M],'bundle_path':str(Path('output/bundle.review.json').resolve()),'plan_path':str(Path('output/plan.review.json').resolve()),'integrated_plan_sha256':ph,'prompt_path':str(Path('output/prompt.review.txt').resolve()),'prompt_sha256':promptsha,'priority_map_path':str(Path('output/priority-map.json').resolve()),'required_reviewed_finding_ids':[f['id'] for r in reports for f in r['findings']],'required_reviewed_obligation_ids':[o['id'] for r in reports for f in r['findings'] for o in f['atomic_obligations']],'required_reviewed_invariant_ids':list(imap),'execution_note':'Mixed: two fresh delegated lanes, three sequential fallback lanes after actual thread-limit failure. Requested critic: root independent of case integrator, shared reviewer across cases, not a new empty context.','source_critic_required':'Inspect actual source and every complete literal clause, P0/P1 coverage, all obligation directions, implicit spatial effects, color/light ownership and standalone meaning. Return honest pass/targeted-repair/blocked plus bundle-compatible coverage_review fields and exact IDs.'},ensure_ascii=False,indent=2)+'\n')
Path('output/integration-decisions.json').write_text(json.dumps({'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':'mixed','dominant_fidelity_axis':'mixed','primary_cue_set':['Phone completely hides facial features','Tall tight crown-to-upper-thigh crop and shallow sink foreground','Projected torso/head-left-of-hips and unequal shoulders','Two braids, dropped cardigan, fitted blue tank, dark loose shorts','Low-key soft and faintly grainy photographic capture'],'finding_dispositions':fds,'obligation_dispositions':ods,'schema_adjustments':['Within-person front/shoulder projections use the single person region; the torso-to-shorts diagonal retains its named cross-region relation.','Color-bearing generic adjectives moved or fully scoped to Color/Tone controls.'],'instruction_version':'v1 observations and unchanged views; v2 validation tools','critic_status':'pending','semantic_repair_count':0},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'plan_canonical_sha256':ph,'prompt_sha256':promptsha,'findings':len(fds),'obligations':len(ods),'invariants':len(imap),'prompt_words':len(prompt.split())}))
