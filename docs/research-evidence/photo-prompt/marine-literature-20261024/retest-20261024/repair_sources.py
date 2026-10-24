"""Reviewed bilingual naming and visibility planning; never widen visual contracts."""
from pathlib import Path
import copy, hashlib, json

T=Path(__file__).resolve().parent
R=T.parents[4]
A=R/'skills/photo-prompt-image-generator/assets'
Q=T.parent
read=lambda p:json.loads(p.read_bytes())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

# Authored English names denote the existing complete observable proposition.
# No genre token is added to every record, and aliases supply no adoption duty.
names='''faceted short-brimmed military utility cap
red cloth name tape attached to uniform chest
separate patch resting on skin
matte lace-up combat boot with tongue eyelets and treaded sole
local camouflage pattern on military uniform fabric
intact military physical training outfit
identification tag suspended from a neck chain
red triangular briefs garment alternative
red rectangular shorts garment alternative
cap and lower garment minimal outfit alternative
bare upper torso visible clothing boundary
small ring attached to an ear
lower-body military equipment and boots outfit
ordinary hand tool held by a uniformed person
exaggerated broad shoulders chest and upper arms
short thick neck connecting head to torso
small head relative to large torso
cap brim casting shadow across the wearer's face
eyes and teeth visible within face shadow
short side hair with longer hair on top
central mohawk ridge
black headscarf wrapping the head
monitor head connected to mechanical body
ordinary and very large body proportions compared
red monster body surface
elongated horse-shaped face
upturned chin and head orientation
stern tense facial expression
raised mouth corners with otherwise neutral face
open smile exposing teeth
wide eyes and rigid closed mouth
forehead sweat droplets and closed mouth
half-closed eyes and neutral mouth
exaggerated drawn tears in a comic image
military attention stance with aligned body
hand-to-forehead salute
people lined up facing the same direction
one person's forearms crossed across their own chest
two hands held behind the same person's back
hands placed on both sides of the waist
chest-forward upright posture
one person looking down at another person
pointing finger directed toward a visible target
torso leaning toward another person
seated person with widely separated legs
person spanning a doorway opening
stiff shoulders and arms
rear foot placement in a movement instant
compact curled body posture
visible open palm maintaining interpersonal distance
person seated low on the floor
both hands cupping the same person's head
clothed full prostration with knees hands and forehead on floor
straight-arm plank with visible hand and toe support
forward-leaning running instant
running away from a visible threatening arrangement
group dispersing toward the same side
one contrasting reaction within a group
stacked shipping container fortress
seventeen separately countable container stories
repeated barracks bunks lockers and central aisle
military kitchen and communal dining space
text marking the third compartment
empty room with a door sign
discoloured river surface without chemical inference
grotesque creatures and trees in a garden
red boxy old-style passenger minibus exterior
driver and passenger in distinct front seats
contradiction between vehicle interior and exterior space
truck with open cargo bed
adjustable wrench with movable jaw and worm screw
compartmented metal meal tray
small metal personal storage locker
food label separate from unverified contents
low-angle upward camera view
high-angle downward camera view
different adult body proportions at equal depth
backlight and dark silhouette
central person with bilateral symmetry
people arranged around a central person
near hand enlarged by perspective
drawn focus lines converging on one target
parallel drawn speed lines
large graphic sound-effect lettering beside a person
bold ink outlines and hatching
reaction face inside a separate bordered inset
red accent localized to one object
drawn curved odour lines as a comic proxy
cloudy atmospheric layer with depth separation
military slogan board with visible carrier and lettering
contradictory weather in separately visible areas
ironic contrast between written slogan and visible scene'''.splitlines()
assert len(names)==92

def main():
 path=A/'photo_candidate_marine_literature_20261024.json'
 side=A/'photo_marine_literature_semantics_20261024.json'
 module=read(path);sem=read(side)
 assert not (T/'source-repair.json').exists(),'This repair is single application; preserve original evidence.'
 write(T/'source.before.json',module);write(T/'semantics.before.json',sem)
 protected={m['file']:sha(A/m['file']) for m in read(A/'photo_candidate_corpus_manifest.json')['modules'] if m['file']!=path.name}
 rows=[]
 planning={
  'owner_and_direction':'When laterality matters, resolve actor-relative anatomical left/right separately from screen position. Trace each arm continuously to its owned hand; a mirrored arrangement does not satisfy an explicit side contract.',
  'connections':'Plan a view in which every selected required owner, part, endpoint and connection is visible together at review scale. A local contact does not prove a complete route.',
  'support':'A required floor, seat or object support must be visible. Occluded contact beneath water, fabric, a hull or frame crop is unobservable rather than presumed supported.',
  'shadow':'A required cast-shadow relationship needs a visible occluder, light direction and connected receiver footprint. Dark material or unrelated ground shade does not establish that relationship.',
  'status':'Advisory rendering plan only; the existing complete proposition and pixel gates remain unchanged. No native or pixel approval.'}
 for cid,r in module['candidates'].items():
  if r['record_kind']!='visual_option':continue
  content=r['content'];card=content['research_semantics'];key=card['id'];label=names[int(key[1:])-1]
  prior=copy.deepcopy(content)
  content['aliases']=list(dict.fromkeys([*content['aliases'],label]))
  content['definition']=label+'. '+prior['definition']
  card['label_en']=label;card['render_planning']=copy.deepcopy(planning)
  # Keep all original literal render propositions, intrinsic guards and effects.
  assert content['en']==prior['en'] and content['ko']==prior['ko']
  rows.append({'card':key,'cid':cid,'label_en':label,'literal_propositions_unchanged':True,'conditions_effects_provenance_unchanged':True})
 for card in sem['cards']:
  if card['id'].startswith('V'):
   card['label_en']=names[int(card['id'][1:])-1];card['render_planning']=copy.deepcopy(planning)
 sem['repair_note']='Bilingual object naming and visibility planning added; source gates and diagnostic boundaries unchanged.'
 write(path,module);write(side,sem)
 assert protected=={name:sha(A/name) for name in protected},'Concurrent module changed: preserve, inspect and rebaseline; never overwrite.'
 write(T/'protected-source-baseline.json',protected)
 write(T/'release-new-native-records.json',module['candidates']);write(T/'changed-native-records.json',{})
 write(T/'release-bindings.json',read(A/'photo_candidate_marine_literature_bindings_20261024.json'))
 write(T/'source-preservation.json',{'status':'pass','other_modules_unchanged':True,'module_count':len(protected),'original_visual_propositions_conditions_effects_provenance_unchanged':True})
 write(T/'source-repair.json',{'status':'applied','visual_records':len(rows),'diagnostic_records_unchanged':247,'new_diagnostic_positive_routing':False,'ranking_bonus':False,'sampling_policy_changed':False,'rows':rows,'candidate_sha256':sha(path),'semantics_sha256':sha(side)})
 print(json.dumps({'status':'applied','visual_records':len(rows),'diagnostic_records_unchanged':247}))

if __name__=='__main__':main()
