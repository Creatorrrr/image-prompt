"""Compile research into selected visible variants; no broad-label hard defaults."""
import hashlib
import json
from pathlib import Path

P = Path(__file__).resolve().parent
R = P.parents[3]
A = R / 'skills/photo-prompt-image-generator/assets'
matrix = {x['id'][3:]: x for x in json.loads((P/'keyword-matrix.json').read_text())}

def digest(x):
    return hashlib.sha256(json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def write(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')

# Each line is a deliberately selected variant, never a definition of all retail uses.
# Component 1 and 2 jointly define the opt-in gate. Broad labels aid discovery only.
rows = '''
onepiece|wardrobe_style|the swimsuit bodice continues through the waist into the brief section|the connected swimsuit has two separate leg openings
bikini|wardrobe_style|the swim top and swim bottom are separate garments|the top hem remains distinct from the bottom waistband
tankini|wardrobe_style|the long swim top covers the torso and ends in a free hem|a separate swim bottom begins beneath the overlapping top
swimdress|wardrobe_style|a skirt panel is attached over the swimsuit body|the skirt has a free lower hem distinct from the fitted swimsuit beneath
legsuit|wardrobe_style|the swimming garment joins the torso to two short trouser legs|each short leg ends in its own thigh-level hem
triangle|garment_detail|the swim top has two distinct triangular fabric panels|the upper point of each triangular panel connects to a supporting strap
string|garment_detail|narrow cords connect the fabric sections of the swimsuit|each visible cord has a traceable attachment or tied endpoint
bandeau|garment_detail|the swim top forms a continuous horizontal fabric band across the front|the band retains a distinct upper edge and lower hem
strapless|garment_detail|the swimsuit upper edge stays below both bare shoulders|the selected strapless construction leaves the neck free of supporting straps
halter|garment_detail|two supporting swimsuit straps rise toward the sides of the neck|the supporting straps meet behind the neck
longline|garment_detail|the swim top has a fabric band extending below the cup region|the extended band ends in a separate lower hem above the swim bottom
sporttop|wardrobe_style|the cropped swim top has broad shoulder straps joined to its front panel|the cropped top ends at a distinct underbust band above separate swim bottoms
scoop|garment_detail|the swimsuit front neckline forms a rounded U-shaped edge|both sides of the front neckline rise toward the shoulder attachments
square|garment_detail|the swimsuit front neckline has a nearly horizontal central edge|two distinct corners join that edge to its rising sides
sweetheart|garment_detail|the swimsuit front upper edge forms two rounded lobes|the two lobes meet at a shallow central dip
plunge|garment_detail|the swimsuit front neckline descends in a deep V|the two finished neckline edges meet at a defined lower point
highneck|garment_detail|the swimsuit front panel rises to the base of the neck|the high front neckline remains separate from the sleeve and back design
oneshoulder|garment_detail|the swimsuit connects over only one of the wearer shoulders|the opposite upper edge passes below the other bare shoulder
offshoulder|garment_detail|the swimsuit upper bands pass across the upper arms below both shoulders|both shoulder tops remain above the garment edge
crossback|garment_detail|two separate swimsuit straps cross diagonally on the back|each strap continues past the crossing to its own attachment
scoopback|garment_detail|the swimsuit back opening has a deep rounded U-shaped boundary|the back opening ends at a defined lower edge above the brief section
vback|garment_detail|the swimsuit back opening forms a V between two finished edges|the two back edges meet at a defined lower point
laceup|garment_detail|a cord alternates through multiple attachment points along two swimsuit back edges|the laced cord visibly bridges and tightens the space between those edges
tieback|garment_detail|two swimsuit back ties converge at one tied knot|the tied ends remain visibly connected to opposite garment edges
keyhole|garment_detail|a small enclosed opening interrupts the swimsuit back panel|a continuous finished fabric boundary surrounds the opening
straps|garment_detail|a swimsuit shoulder strap passes through a small adjustment slider|both sides of the slider continue into the same fabric strap
highleg|garment_detail|the swimsuit leg openings rise high at the outer hips|the elevated leg edges remain distinct from the garment waistline
midlowrise|garment_detail|the swim bottom waistband sits low across the hips|the waistband remains a distinct upper edge separate from the leg openings
boyleg|garment_detail|the swim bottom extends into two short legs|the two leg hems run across the upper thighs
tieside|garment_detail|the swim bottom front and rear panels meet through side ties|each visible side tie forms a physical knot with free ends
vfront|garment_detail|the swim bottom front waistband slopes downward toward the center|the two sloping upper edges meet in a central V
foldover|garment_detail|the swim bottom waistband folds outward over itself|the folded band exposes a doubled fabric edge
skirtbottom|wardrobe_style|a separate swim bottom carries an attached outer skirt|the outer skirt hem hangs below its attachment at the waistband
rashguard|wardrobe_style|the rashguard is a separate sleeved swim top with its own hem|a distinct lower garment waistband remains beneath the rashguard hem
surfsuit|wardrobe_style|the sleeved surf swimsuit joins the torso directly to its brief section|the sleeves and brief section belong to the same continuous garment
wetsuit|wardrobe_style|the selected wetsuit has joined fitted torso and limb panels|the garment entry follows a visible zipper or overlapping opening
springsuit|wardrobe_style|the selected springsuit has long fitted sleeves|its short legs end in separate hems on the upper thighs
jane|wardrobe_style|the selected Long Jane wetsuit has a sleeveless torso|two joined long legs continue down toward the ankles
swimskin|wardrobe_style|the thin racing swimskin forms an outer layer over the swimming outfit|the outer racing layer has its own closure and lower leg hems
leggings|wardrobe_style|the separate swim leggings have a distinct waistband|their two fitted legs continue to ankle-level hems
boardshorts|wardrobe_style|the boardshorts have separate loose leg tubes below a defined waistband|each leg tube ends in a free straight hem
wrapcover|wardrobe_style|a separate beach wrap overlaps around the swimsuit waist|the wrap has a tied attachment and a free hanging hem
coverup|wardrobe_style|a loose beach cover-up forms an outer garment over the swimsuit|its open front and sleeve hems remain distinct from the swimsuit underneath
beachshirt|wardrobe_style|an open beach shirt forms a separate layer over the swimsuit|the shirt placket and lower hem stay distinct from the swimsuit edges
rib|garment_detail|parallel raised ribs run across the selected swimsuit fabric panel|small shadows separate the raised ribs from the recessed channels
crinkle|garment_detail|small repeated puckers cover the selected swimsuit fabric panel|the fine surface puckers remain distinct from larger seam-directed folds
terry|garment_detail|small textile loops cover the selected swimsuit surface|the looped pile remains visible along the fabric edge
jacquard|garment_detail|the selected swimsuit pattern changes with the local yarn structure|the patterned region retains visible interlaced textile detail
crochet|garment_detail|an open looped-yarn layer forms the swimsuit outer surface|a separate opaque lining remains visible behind the yarn openings
mesh|garment_detail|a bounded mesh insert occupies part of the swimsuit panel|fine threads remain visible across the insert opening
finish|garment_detail|the selected swimsuit fabric has a broad satin-like highlight|the fabric retains soft folds and finished textile edges within the sheen
ruched|garment_detail|folds in the swimsuit fabric converge toward a selected gathering seam|the gathering seam anchors the ends of those folds
shirred|garment_detail|multiple parallel stitch rows cross a swimsuit fabric panel|small gathers repeat in the spaces between those stitch rows
smocked|garment_detail|decorative stitches connect repeated folds in the swimsuit panel|the connected folds form a regular relief pattern
pleats|garment_detail|the selected swimsuit skirt panel has repeated aligned folded pleats|each pleat continues toward a free lower hem
ruffle|garment_detail|a ruffle strip is attached along one swimsuit edge|its opposite free edge forms projecting fabric waves
scallop|garment_detail|repeated rounded scallops shape the swimsuit fabric edge|the scalloped boundary remains part of the same fabric panel
piping|garment_detail|a narrow raised piping cord follows a swimsuit seam|the piping remains seated between the adjoining fabric panels
cutout|garment_detail|an open cutout interrupts the swimsuit waist panel|finished fabric edges surround the opening while a fabric bridge connects the garment sections
wrapfront|garment_detail|two swimsuit front panels overlap diagonally|the upper panel edge remains traceable across the panel beneath it
twist|garment_detail|two swimsuit front fabric sections twist around one another at the center|folds radiate from the physical central twist into both panels
ring|garment_detail|two swimsuit fabric sections attach to opposite sides of one ring|the ring visibly connects those garment sections
belt|garment_detail|a separate belt passes around the swimsuit waist|the belt ends connect through a visible buckle
zip|garment_detail|a vertical zipper follows the center front of the swimsuit|the zipper slider and lower endpoint lie on that same opening
wet|garment_detail|discrete water droplets rest on the swimsuit fabric|the fabric texture remains visible between the droplets
'''
profiles=[]
extension={'schema_version':'photo-prompt-research-extension/v1','slots':{'wardrobe_style':[],'garment_detail':[]},'visual_semantics':[]}
mapping={}
for line in rows.strip().splitlines():
    key,slot,*phrases=line.split('|')
    research=matrix[key];pid='sw_'+key;cid='sw_candidate_'+key
    aliases=research['terms']
    # Avoid claiming selected variations exhaust broad grouped research vocabulary.
    specific={'straps':['adjustable swimsuit strap','길이조절 수영복 끈'], 'crinkle':['crinkle swimsuit fabric','크링클 수영복 원단'], 'scallop':['scalloped swimsuit edge','스캘럽 수영복 가장자리'], 'piping':['swimsuit seam piping','수영복 솔기 파이핑'], 'finish':['satin-look swimsuit fabric','새틴 광택 수영복 원단'], 'twist':['twist-front swimsuit','트위스트 프런트 수영복'], 'springsuit':['long sleeve short leg springsuit','긴소매 짧은다리 스프링수트'], 'jane':['Long Jane wetsuit','롱제인 웨트수트'], 'leggings':['swim leggings','swim tights','수영 레깅스'], 'midlowrise':['low-rise swim bottom','로우라이즈 수영복 하의'], 'coverup':['open beach cover-up','앞이 열린 비치 커버업'], 'beachshirt':['open beach shirt','앞이 열린 비치 셔츠']}
    aliases=specific.get(key,aliases)
    components=[{'id':f'component_{i}','match_terms':[phrase],'evidence_field':f'component_{i}_phrase','evidence_terms':[phrase],'min_content_words':3,'instruction':'Keep this selected garment relation visible: '+phrase,'render_gate':{'id':f'vo_{pid}_{i}','review_scale':'both' if slot=='wardrobe_style' else 'native','description':phrase+'. The saved image must show the relation; occlusion or substitution does not pass.'}} for i,phrase in enumerate(phrases,1)]
    profiles.append({'id':pid,'category':'swimwear_selected_visible_relation','activation':{'exact_terms':['; '.join(phrases)],'requires_adult_character':False,'semantic_discovery_requires_component_evidence':True},'semantics':{'definition':'Selected '+aliases[0]+' relation: '+'; '.join(phrases)+'.','paraphrase_examples':[research['proposed_visible_evidence'],*aliases],'contrast_examples':[research['confusion_boundary']],'claim_limits':['A selected visible variant, not every retail use of its label.','Garment structure does not establish wearer identity, body shape, nationality, comfort or performance.', 'Hidden construction, chemical composition, UPF and waterproofness are not pixel claims.']},'concept_candidate':{'concept_terms':[*aliases,*phrases]},'runtime_expression':{'default_mode':'definition_with_optional_label','prompt_label_terms':[],'forbidden_prompt_terms':[],'runtime_forbidden_labels':[]},'reject_substitutes':[research['confusion_boundary']],'authored_components':{'contract_version':'photo-authored-visual-components/v1','components':components}})
    entry={'id':cid,'ko':research['proposed_visible_evidence'],'en':'; '.join(phrases),'aliases':aliases,'concept_units':phrases,'affected_dimensions':['appearance'],'weight':0.5,'tags':['human','swimwear_visual_semantics',slot],'keywords':[*aliases,*phrases],'embedding_text':'Selected swimwear structure: '+'; '.join(phrases),'for_any':['human']}
    extension['slots'][slot].append(entry)
    mapping[key]=(cid,slot,pid,phrases)
    extension['visual_semantics'].append({'id':'sw_variant_'+key,'primary_visual_proposition':'; '.join(phrases),'hard_profile_ids':[pid],'component_groups':[{'id':f'component_{i}','visible_evidence':[x]} for i,x in enumerate(phrases,1)],'candidate_ids':[cid],'candidate_slots':{cid:slot},'confusion_boundaries':[research['confusion_boundary']],'source_keywords':aliases,'candidate_only':True,'activation_mode':'component_complete_exact_only'})

# Reuse existing source-owned candidates rather than copying their meanings.
mapping['highrise']=('high_rise_waist_navel_relation','silhouette_proportion',None,['the swim bottom waistband sits around or above the navel'])
# Research bundle concepts with unavailable exact counterparts remain documented, not silently substituted.
research_bundles=json.loads((P/'candidate-drafts.json').read_text())['bundles']
skipped=[]
for b in research_bundles:
    keys=[x[3:] for x in b['component_ids']]
    if any(k not in mapping for k in keys):
        skipped.append({'id':b['id'],'reason':'Existing racerback sports-bra profile is narrower than general swimwear; no automatic transplant.'});continue
    mapped=[mapping[k] for k in keys]
    extension['visual_semantics'].append({'id':b['id'],'primary_visual_proposition':b['primary_visual_proposition'],'hard_profile_ids':[], 'component_groups':[{'id':k,'visible_evidence':m[3]} for k,m in zip(keys,mapped)],'candidate_ids':[m[0] for m in mapped],'candidate_slots':{m[0]:m[1] for m in mapped},'confusion_boundaries':b['confusion_boundaries'],'source_keywords':[a for k in keys for a in matrix[k]['terms']], 'candidate_only':True,'activation_mode':'optional_joint_choice'})

record={'contract_version':'photo-extension-maintenance/v1','record_id':'photo_prompt_swimwear_extension','source_filename':'photo_prompt_swimwear_extension.json','authored_source_sha256':digest(extension),'runtime_keys':['slots','visual_semantics'],'maintenance_only':{'research_path':str(P.relative_to(R)),'candidate_drafts_sha256':hashlib.sha256((P/'candidate-drafts.json').read_bytes()).hexdigest(),'source_ledger_sha256':hashlib.sha256((P/'sources.json').read_bytes()).hexdigest(),'profile_scope':{p['id']:{'source_ids':matrix[p['id'][3:]]['source_ids'],'claim':'Authored visible variant; not source-photo inspected or a universal retail definition.'} for p in profiles},'excluded_from_hard_profiles':['internal','performance','fibers','era','monokini','mood','accessories','environment','coverage','bralette','balconette','underwire','highrise','racerback','print'],'skipped_research_bundles':skipped},'adoption_scope':'Selected observable garment variants; generic names advisory; hidden performance and broad fashion moods excluded from hard pixel duties.'}
write(R/'docs/research-evidence/photo-prompt/extension-maintenance/photo_prompt_swimwear_extension.json',record)
extension['maintenance_ref']={'contract_version':'photo-extension-maintenance-ref/v1','record_id':record['record_id'],'sha256':digest(record)}
write(A/'photo_prompt_swimwear_extension.json',extension)
write(A/'photo_prompt_visual_obligations_swimwear.json',{'schema_version':'photo-visual-obligation-registry-extension/v1','relation_contract_version':'photo-visual-relation/v1','description':'Selected swimwear garment connections, openings, closures and textile relations.','profiles':profiles})
for path in [R/'skills/photo-prompt-image-generator/scripts/prompt_generator.py',A/'photo_prompt_tags.json']:
    text=path.read_text()
    for old,new in [('photo_prompt_palace_fortification_extension.json','photo_prompt_swimwear_extension.json'),('photo_prompt_visual_obligations_palace_fortification.json','photo_prompt_visual_obligations_swimwear.json')]:
        if new not in text and old in text:
            lines=text.splitlines(keepends=True)
            for i,line in enumerate(lines):
                if '"'+old+'"' in line:
                    if not line.rstrip().endswith(','): lines[i]=line.rstrip('\n')+',\n'
                    indent=line[:len(line)-len(line.lstrip())]
                    lines.insert(i+1,indent+'"'+new+'",\n');break
            text=''.join(lines)
    # JSON trailing comma only when insertion follows the last list item.
    if path.suffix=='.json':
        import re
        text=re.sub(r',\n(\s*\])',r'\n\1',text)
        json.loads(text)
    path.write_text(text)
write(P/'runtime-installation.json',{'profiles':len(profiles),'gates':len(profiles)*2,'new_candidates':sum(map(len,extension['slots'].values())),'bundles':len(extension['visual_semantics']),'reused_candidates':['high_rise_waist_navel_relation'],'skipped_research_bundles':skipped})
print((P/'runtime-installation.json').read_text())
