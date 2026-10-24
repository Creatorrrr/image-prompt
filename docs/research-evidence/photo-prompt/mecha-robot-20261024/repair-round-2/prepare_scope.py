from pathlib import Path
import json,hashlib
R=Path('/Users/chasoik/Projects/image-prompt');O=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_bytes())
old={'a':R/'generated/photo-runs/mecha-20261024-arm-a','b':R/'generated/photo-runs/mecha-20261024-arm-b/current','c':R/'generated/photo-runs/mecha-20261024-arm-c'}
for a,parent in old.items():
 out=O/('retry-'+a);out.mkdir(exist_ok=True);w=read(parent/'workflow.json');core=read(Path(w['artifacts']['authorial_core_normalized']['path']));audit=read(Path(w['artifacts']['review_audit']['path']))['visual'];child=R/'generated/photo-runs'/('mecha-20261024-repair2-'+a);cw=read(child/'workflow.json');env=read(Path(cw['artifacts']['request_envelope_input']['path']))
 ledger=parent/'image_runs.ndjson' if a!='b' else parent.parent/'image_runs.ndjson';rows=[json.loads(v) for v in ledger.read_text().splitlines() if v.strip()];runid={'a':'23686135e6dc0d04','b':'8f6a0db573677853','c':'921cba5da2392e6d'}[a];attempt=next(v for v in rows if v['run_id']==runid);(out/'attempt.json').write_text(json.dumps(attempt,ensure_ascii=False,indent=2))
 preserved=['subject','reference_use','appearance'] if a=='a' else ['concept','subject','event','reference_use','appearance']
 changed=[v for v in core['intent_lock']['open_dimensions'] if v not in preserved]
 corrected=['concept','event'] if a=='a' else []
 changed+=corrected
 d={'schema_version':'photo-repair-decision/v1','current_source_span_ids':['repair'],'source_text':env['active_spans'][0]['text'],'preserved_dimensions':preserved,'allowed_changes':changed,'requester_corrected_dimensions':corrected,'allowed_properties':[],'local_axes':['object_geometry','contact_geometry','local_pose','camera','framing','lighting','occlusion'],'failed_gate_ids':[v['gate'] for v in audit['failed_hard_gates']],'failure_class':'meaning_rebuild' if a=='a' else 'pixel_realization_mismatch','additional_invocation_limit':1,'obligation_dimensions':{}}
 (out/'decision.json').write_text(json.dumps(d,ensure_ascii=False,indent=2));(out/'args.json').write_text(json.dumps({'run':str(parent),'decision':str(out/'decision.json'),'current_envelope':cw['artifacts']['request_envelope_input']['path'],'attempt':str(out/'attempt.json'),'ledger':str(ledger),'output':str(out/'projection')},indent=2))
 print(a,json.dumps(d,ensure_ascii=False))
