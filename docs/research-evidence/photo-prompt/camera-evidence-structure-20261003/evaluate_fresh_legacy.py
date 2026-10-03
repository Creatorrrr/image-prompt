"""Frozen raw ownership oracle and separately labelled synthetic retrieval probe.

Never edits, pads or upgrades the independently authored baseline. The synthetic
core is a caller contract probe, not an independently authored full scene core.
No oracle phrase is supplied as an input anchor. Public order is not rank.
"""
import argparse, hashlib, json, re, subprocess, sys
from pathlib import Path
from unittest import mock

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('runtime-repo','data-repo','test-repo','fixture','output'):
        p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();sys.path.insert(0,str(a.runtime_repo/'skills/photo-prompt-image-generator/scripts'))
    import prompt_generator as pg
    import photo_camera_evidence as camera
    sys.path.insert(1,str(a.test_repo))
    from tests import photo_prompt_fixtures as f
    raw=a.fixture.read_bytes();inputs=json.loads(raw)
    assert hashlib.sha256(raw).hexdigest()=='5c73a0ddb796bb89c96a35ff818660bd602d6de34238086eda23c06088ac7150'
    report={'runtime_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=a.runtime_repo,text=True).strip(),
        'runtime_sources':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in (a.runtime_repo/'skills/photo-prompt-image-generator/scripts').glob('*.py')},
        'fixture_sha256':hashlib.sha256(raw).hexdigest(),'provider_calls':0,'pixel_quality_evaluated':False,
        'caller_probe':'Synthetic core over unchanged complete baseline. Subject/event are first baseline sentence; setting/style are neutral scaffold. No oracle input anchors, no baseline padding, no property locks inferred. This is not the actual independent authoring workflow.',
        'rows':[]}
    with mock.patch.object(pg,'cached_gemini_client',side_effect=AssertionError('offline evaluation')),mock.patch.object(pg,'embed_texts_with_gemini',side_effect=AssertionError('offline evaluation')):
        data=pg.load_runtime_data(a.data_repo/'skills/photo-prompt-image-generator/assets/photo_prompt_tags.json')
        report.update(dictionary_hash=pg.dictionary_hash(data),quality_layers_loaded=pg.QUALITY_LAYERS_DATA_KEY in data,semantic_entries=len(data[pg.SEMANTIC_INDEX_DATA_KEY]['entries']),visual_profiles=len(data[pg.VISUAL_OBLIGATIONS_DATA_KEY]['profiles']))
        for case in inputs['cases']:
            text=case['english_baseline'];request=case['natural_request'];subject=text.split('.')[0]
            row={'id':case['id'],'expected':case['expected'],'raw_text_sha256':hashlib.sha256(text.encode()).hexdigest(),'axes':{}}
            raw_core={'subject':subject,'baseline_prompt_en':text}
            for axis in ('direction','height'):
                extracted=camera.legacy_camera_clauses(raw_core,axis);expected=case['expected'][axis+'_span']
                owner=case['expected']['owner_span']
                row['axes'][axis]={'expected_literal_axis':expected,'extracted_owned_clauses':extracted,
                    'exact_span_match':extracted==([expected] if expected else []),
                    'owner_and_axis_literal_coverage':bool(expected and any(expected in x and owner in x for x in extracted)),
                    'abstention':not extracted}
            # Candidate-free mechanical adapter, explicitly not authoring evidence.
            words=text.split();anchors=list(dict.fromkeys(' '.join(words[i:i+6]).strip(' ,.;:!?') for i in range(0,len(words)-5,3) if len(pg.authorial_request_content_words(' '.join(words[i:i+6])))>=2))[:3]
            authored=f.core(request,interpreted_intent=text,subject=subject,event=subject,setting='a modest ordinary photographic setting',visual_priorities=('readable subject structure','natural material detail'),baseline_prompt_en=text,anchor_evidence=tuple(anchors))
            # Disable the test helper's general prompt-budget extension. The raw
            # independent baseline is the only prose sent to normalization.
            authored['baseline_prompt_en']=text
            controls=pg.creative_controls.resolve(request,overrides={'sensual':0,'fetish':0},seed=829)
            authored['creative_controls_sha256']=controls['canonical_sha256']
            try:
                core=pg.normalize_authorial_core(authored,request_envelope=pg.normalize_request_envelope(f.envelope(request)),creative_control_snapshot=controls)
                slots,binding,_=pg.retrieve_core_slots(data,core,controls)
                row.update(preflight_error=None,core_sha256=core['canonical_sha256'],property_locks=pg.intent_property_locks(core['intent_lock']),total_candidates=sum(len(x['candidates']) for x in slots.values()),candidate_adoption=binding['candidate_adoption'])
                contract,picked=pg.frozen_core_context(data,core,controls)
                for axis in ('direction','height'):
                    slot='camera_'+axis;query,fields=pg.core_slot_focus_queries(data,core,slot)
                    candidates=slots.get(slot,{}).get('candidates',[])
                    row['axes'][axis].update(query=query,query_fields=fields,legacy_clause_forwarded='baseline_prompt_en.camera_clause' in fields,
                        exposed_candidates=[{'id':x['id'],'label':x.get('label'),'applicability':x.get('applicability')} for x in candidates],
                        eligible_before_ranking=sum(pg.core_slot_entry_eligible(data,core,contract,picked,slot,x) for x in data['slots'].get(slot,[])))
            except ValueError as exc:
                row['preflight_error']=str(exc)
            # Scope test is counterfactual: it is never input to retrieval/adoption.
            lock={'contract_version':'photo-intent-lock/v2','semantic_anchors':[{'dimension':'camera','target':'camera','property':'viewpoint.'+axis} for axis in ('direction','height') if case['expected'][axis+'_span']]}
            allowed=[]
            for entry in data['slots']['camera_direction']:
                source=pg.photo_candidate_semantics.semantic_source(entry,'camera_direction',data.get('candidate_semantic_policy'))
                allowed.append(pg.property_effects_allowed(lock,source.get('affected_dimensions') or [],source.get('affected_properties',[])))
            row['counterfactual_property_lock_compatible_direction_rows']=sum(allowed)
            row['total_direction_rows']=len(allowed)
            report['rows'].append(row)
    positives=[x for x in report['rows'] if not x['expected']['abstain']];negatives=[x for x in report['rows'] if x['expected']['abstain']]
    report['summary']={'positive_cases':len(positives),'positive_cases_exact_axis_span_match':sum(all(y['exact_span_match'] for y in x['axes'].values()) for x in positives),
        'positive_cases_owner_and_axis_literal_coverage':sum(all(y['owner_and_axis_literal_coverage'] for y in x['axes'].values()) for x in positives),
        'negative_cases':len(negatives),'negative_cases_abstained':sum(all(y['abstention'] for y in x['axes'].values()) for x in negatives),
        'preflight_admitted':sum(x['preflight_error'] is None for x in report['rows']),
        'axes_with_owned_clause_query':sum(y.get('legacy_clause_forwarded',False) for x in report['rows'] for y in x['axes'].values()),
        'max_candidates':max((x.get('total_candidates',0) for x in report['rows']),default=0)}
    assert raw==a.fixture.read_bytes()
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report['summary']),flush=True)

if __name__=='__main__':main()
