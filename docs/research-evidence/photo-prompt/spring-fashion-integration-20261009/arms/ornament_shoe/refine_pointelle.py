from pathlib import Path
import json,hashlib,ast
B=Path(__file__).resolve().parent
ns={'__file__':str(B/'author_data.py')}
source=(B/'author_data.py').read_text();ast.parse(source)
exec(compile(source.split('assert set(ROWS)==set(D)')[0],str(B/'author_data.py'),'exec'),ns)
row=ns['ROWS']['sf057_01'];d=ns['D']['sf057_01']
j=json.loads((B/'data-fragment.json').read_text());parts=row['parts'];en='; '.join(parts)+'.';ko=row['ko']
relations=[{'id':'declared_owner','type':'declared_owner_scope','subject':row['owner'],'object':'main_subject'}]
relations.extend({'id':f'edge_{i:02d}','type':typ,'subject':sub,'object':obj} for i,(typ,sub,obj) in enumerate(row['edges'],1))
for g in j['domain_writes']:
 if not any(c['id']=='spf_sf057_01' for c in g['candidates']):continue
 c=next(c for c in g['candidates'] if c['id']=='spf_sf057_01')
 p=next(p for p in g['profiles'] if p['id']=='spring_sf057_01')
 b=next(b for b in g['visual_semantics'] if b['id']=='spf_sf057_01_bundle')
 effects=[{'dimension':dim,'target':'main_subject','property':path} for dim in c['affected_dimensions'] for path in row['paths']]
 c.update(ko=ko,en=en,aliases=[ko,en],keywords=list(dict.fromkeys([ko,en]+parts)),embedding_text=' | '.join([ko,en]+parts),concept_units=parts,relations=relations,affected_properties=effects)
 p['activation']['exact_terms']=[en]
 p['activation']['hard_activation']['required_any_groups'][0]['any_terms']=[en]
 p['semantics'].update(definition=en,paraphrase_examples=[ko],visual_components=parts,contrast_examples=[row['contrast']])
 for i,comp in enumerate(p['authored_components']['components']):
  phrase=parts[i];comp.update(match_terms=[phrase],evidence_terms=[phrase],instruction='Keep this selected owner-bound structure readable in the photograph: '+phrase+'.')
  comp['render_gate']['description']=row['gate_descriptions'][i]
 p['concept_candidate'].update(concept_terms=[ko,en],affected_properties=effects)
 p['reject_substitutes']=[row['contrast']]
 vr=p['visual_relation'];vr['source']['literal_evidence']=parts
 vr.update(entities=list(dict.fromkeys([row['owner'],'main_subject']+[x for r in row['edges'] for x in r[1:]])),visible_regions=row['visible_regions'],relations=[f"{r['subject']} {r['type']} {r['object']}" for r in relations],observable_effects=parts,confusion_negatives=[row['contrast']],flexible_fields=row['paths'])
 vr['observability']['required_visible_regions']=row['visible_regions']
 b.update(primary_visual_proposition=en,component_groups=[{'id':f'component_{i:02d}','visible_evidence':[phrase]} for i,phrase in enumerate(parts,1)],confusion_boundaries=[row['contrast']],source_keywords=[ko,en],relations=relations)
for e in j['evidence']:
 if e['draft_id']!='SPR_DRAFT_SF057_01':continue
 e.update(authored_variant_components=parts,authored_variant_relations=relations,effect_paths=row['paths'],contrast=row['contrast'])
 e['special_claim_limits']=['Every small opening rim is formed by actual knit yarn loops and continues into the surrounding knit surface; repeated nearby loop-like marks do not establish this boundary topology. Manufacturing process, exact gauge and fiber composition are not pixel duties.']
 e['refinement_basis']='Coordinator review clarified the authored pointelle boundary topology; this does not alter original requester bytes or frozen core.'
 e['qualification']['profile_compile']='pending_refinement_validation'
for dec in j['decisions']:
 if dec['draft_id']=='SPR_DRAFT_SF057_01':
  dec['reason']='New narrow variant for '+ko+'. Its complete clauses are bound to '+', '.join(row['paths'])+'. Each aperture rim is formed by actual knit yarn loops continuous with the same repeated knit surface, rather than nearby loop-like marks. Existing IDs remain unchanged; manufacturing, gauge and fiber composition are not duties.'
(B/'data-fragment.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
(B/'evidence-sidecar.json').write_text(json.dumps({'schema_version':'spring-fashion-arm-evidence/v1','arm':'ornament_shoe','records':j['evidence']},ensure_ascii=False,indent=2)+'\n')
# Identity/content preservation is checked independently of the new authoring code.
m=json.loads((B/'pointelle-preservation-before.json').read_text())
digest=lambda value:hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
records={}
for g in j['domain_writes']:
 for k in ['candidates','profiles','visual_semantics']:
  for v in g[k]:records[(k,v['id'])]=digest(v)
for k in ['decisions','evidence']:
 for v in j[k]:records[(k,v['draft_id'])]=digest(v)
assert all(records[(r['kind'],r['id'])]==r['sha256'] for r in m['unchanged_records'])
assert all(hashlib.sha256(Path(v['path']).read_bytes()).hexdigest()==v['sha256'] for v in m['frozen_artifacts'].values())
assert hashlib.sha256((B/'run/workflow.json').read_bytes()).hexdigest()==m['workflow_sha256']
assert hashlib.sha256((B/'request_envelope.json').read_bytes()).hexdigest()==m['request_envelope_sha256']
report={'status':'pass','scope':['spf_sf057_01','spring_sf057_01','spf_sf057_01_bundle'],'unchanged_record_count':len(m['unchanged_records']),'frozen_artifact_hash_check':'pass','workflow_unchanged':'pass','request_envelope_unchanged':'pass','manufacturing_gauge_fiber_pixel_duty':'absent','fragment_sha256':hashlib.sha256((B/'data-fragment.json').read_bytes()).hexdigest()}
(B/'pointelle-preservation-after.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
