"""Complete hard evidence on open action/timing while retaining present stillness."""
import json
from pathlib import Path
from compose_cases import reject, authored_review

OUT=Path(__file__).resolve().parent

def compose(pack):
    spec=json.loads((OUT/'GOLEM-COMPOSITION-AUTHORING.json').read_text())
    composed=reject(pack)
    prompt=composed['prompt_en']+' '+spec['label_phrase']+' '+' '.join(spec['evidence'].values())
    composed['prompt_en']=prompt
    composed['visual_obligation_evidence']={'golem_constructed_material_agency':spec['evidence']}
    composed['required_hard_gates']=pack['visual_obligations']['required_hard_gates']
    composed['authorial_core_binding']['authorial_decisions']=[
        {'dimension':'action','decision':'Show only the aftermath of a gate-clearance task while the golem stands still.',
         'rationale':'The existing hard golem contract needs agency and task consequences; preserve the requested still present rather than adding a moving gesture.'},
        {'dimension':'timing','decision':'Place the completed action before the shutter moment.',
         'rationale':'The opened passage and earlier grit trace support the preceding action; the complete final text retains the same stationary stone figure and old gate.'}]
    composed['embodiment_review']=authored_review(pack,prompt)
    composed['embodiment_review']['review']['summary']='Full final prose review: '+spec['review']['present_action']+' '+spec['review']['ownership']+' '+spec['review']['support']+' '+spec['review']['reach_contact']+' '+spec['review']['projection']+' '+spec['review']['boundary']
    return composed
