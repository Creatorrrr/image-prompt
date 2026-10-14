"""Same unapproved literal experiment; fix only independent fixture evidence grounding and negative-catch boundary."""
from pathlib import Path
import json,hashlib
O=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/native_batches/review11870-01299-149-06');p=O/'research_repro_v1.py'
error={'schema':'photo-research-helper-failure-preserved/v1','helper':str(p),'helper_file_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'actual_error':'ValueError: invalid or ungrounded frozen semantic witness','location':'make_core -> projection -> n.frozen_witnesses -> witnesses.read line86','manual_diagnosis':'Independent fixture assertion.evidence used a generic explanation absent from its exact baseline, so witness parser correctly rejected it before B1 experiment. Replace only that fixture evidence with literal baseline substring Controlled independent request. No source/fact/meaning/permission conclusion from this failed run. Also move missing-presence projection into expected-negative exception boundary; no witness weakened.','source_assessment_written':True,'native_proof_created':False,'root_acceptance':0,'operating':0}
ep=O/'REPRO-ERROR-v1.json';assert not ep.exists();ep.write_text(json.dumps(error,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
code=p.read_text().replace("write(O/'SOURCE-ASSESSMENT-v1.json',assessment)","assert load(O/'SOURCE-ASSESSMENT-v1.json')==assessment")
code=code.replace("'meaning':'Independent controlled request declared in exact baseline text, not source-generated witness.'","'meaning':'Controlled independent request'")
code=code.replace("reseal(bad);badq=projection(bad)","reseal(bad);badq=None")
code=code.replace("try:resolver.resolve_selected_contracts(bad,badq)","try:resolver.resolve_selected_contracts(bad,projection(bad)if badq is None else badq)")
code=code.replace("FOOTPRINT-COUNTEREXAMPLE-v1.json","FOOTPRINT-COUNTEREXAMPLE-v2.json")
exec(compile(code,str(p)+'[fixture_grounding_v2]','exec'))
