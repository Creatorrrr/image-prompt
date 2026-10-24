"""Maintenance probes: exact sealed source exposure and natural query recall.

These are independent of the three agents' natural scene queries, and do not
grant any source adoption or pixel qualification.
"""
from pathlib import Path
import gc
gc.disable()
import json, sys

O = Path(__file__).resolve().parent
ROOT = Path('/Users/chasoik/Projects/image-prompt')
SKILL = ROOT/'skills/photo-prompt-image-generator'
release = json.loads((O/'successor.json').read_bytes())
native = Path(release['store'])/'generations'/release['native_generation_id']
sys.path.insert(0, str(native/'scripts'))
from photo_h_f2_generation import Generation
from photo_h_f2_encoder import LocalEncoder
from photo_h_f2_search import present_material
from photo_recall_generation import write
import photo_candidate_corpus as corpus
import photo_canonical_source as canonical

cases = [('route', 'R01', 'A loaded cart follows a completely visible path from fields through a real gap in the threshing-yard curb and onwards to the storehouse, with no buildings or figures hiding the path.'), ('drain', 'R02', 'A drainage inspection photograph shows dry paving, the full open channel, its outlet lip, the short water stream and the lower wet receiving earth together.'), ('gaze', 'R03', 'An estate inspector points at the cart at the storehouse and the foreman looks at that exact cart while holding a plan below chest height.'), ('same_parcel', 'R04', 'Two petitioners put separate fingertips inside one enclosed parcel on a map on the same bank of a river, leaving the complete parcel boundary clear.'), ('map_register', 'R05', 'An estate map and an open bound register show the same river bend, bridge and closed parcel with all boundary endpoints visible; a straightedge lies on a blank margin.'), ('pen_contact', 'R06', 'A clerk writes a short visible ink stroke in the ruled entry of an open bound register; the pen tip touches the actual bound page while the other hand steadies that book.'), ('four_hands', 'R07', 'At a communal bakehouse two people support one loaf with four separate hands. Each wrist and each real palm-to-loaf contact is visible with clear gaps between the hands.'), ('small_tear', 'R08', 'Two people hold a mostly connected loaf with a tiny central fissure, a narrow pale crumb line and a broad intact lower crust bridge.'), ('control_cafe', None, 'A modern city cafe, a barista pours espresso into a ceramic cup beside the coffee machine.'), ('control_station', None, 'A lone commuter waits beneath a neon timetable on a contemporary train platform.'), ('control_portrait', None, 'A simple photographic headshot with short dark hair and a plain background.'), ('control_landscape', None, 'An empty coastal landscape with waves and rocks at sunrise.')]

g = Generation(Path(release['store']), release['generation_id'], full=True)
new = json.loads((O/'new-native-records.json').read_bytes())
mapping = {x['card_id']:x['candidate_id'] for x in json.loads((O/'card-candidate-map.json').read_bytes())}
positive = {cid for cid,r in new.items() if r['record_kind']!='diagnostic'}
diagnostics = set(new)-positive
indexed = {d['cid'] for d in g.metadata}
assert positive <= indexed and not (diagnostics & indexed)
for cid,r in new.items():
    assert canonical.native_snapshot(g.body.record(cid)) == r
source = {'new_positive_indexed':len(positive), 'diagnostics_excluded':len(diagnostics),
          'new_source_roundtrips_exact':len(new), 'all_expected_positive_present':True,
          'diagnostics_positive_exposure':0, 'status':'pass'}
write(O/'sealed-source-exposure.json', source)
index = g.index()
with LocalEncoder(SKILL) as encoder:
    assert encoder.binding == g.binding
    rows = encoder.encode([q for _,_,q in cases], 'query')
results=[]
for (name,card,q),row in zip(cases,rows,strict=True):
    result=index.search(q,row,g.binding)
    window,projection=present_material(result['order'],result['query_scope']['event_phase'],literal=result['query_scope']['literal_text'],focus=result['query_scope']['primary_focus'],maximum=8)
    expected=mapping.get(card)
    rank=next((i+1 for i,d in enumerate(result['order']) if d['cid']==expected),None) if expected else None
    results.append({'case':name,'query':q,'expected_card':card,'expected_cid':expected,
                    'expected_rank':rank,'expected_in_presented_8':any(d['cid']==expected for d in window) if expected else None,
                    'top_20':result['order'][:20], 'presented':window,'projection':projection,
                    'new_CIDs_presented':sorted({d['cid'] for d in window}&positive),
                    'lane_calls':result['lane_calls'],'considered_CIDs':result['considered_CIDs'],
                    'considered_RIDs':result['considered_RIDs'], 'embedding_execution':row['execution']})
report={'schema':'estate-maintenance-probes/v1','generation_id':g.id,
        'source_exposure':source,'natural_queries':len(cases),
        'target_queries':8,'target_presented_8':sum(x['expected_in_presented_8'] is True for x in results),
        'results':results,'qualification':'maintenance source/index and recall probes only; no prompt, native or pixel qualification',
        'original_192_research_cases_executed':False}
write(O/'runtime-probes.json',report)
print(json.dumps({k:v for k,v in report.items() if k!='results'}),flush=True)
