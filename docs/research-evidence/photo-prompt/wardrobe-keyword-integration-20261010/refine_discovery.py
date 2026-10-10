"""Optional part discovery is separate from complete selected relationship proof."""
from pathlib import Path
import json
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
from photo_candidate_semantics import digest
from photo_runtime_sources import source_update

# These are positive observation fragments, not exact aliases or field evidence.
# They apply to the entire authored cohort, independently of any test arm.
CUES={
1:['front buttons','button placket','collared shirt'],3:['baby tee','cropped tee','short-sleeve tee'],
4:['ribbed tank','sleeveless top','open shirt'],5:['bandeau','detached sleeves'],6:['open vest','knit top','padded vest'],
7:['inner top','ribbed top'],8:['loose coat','long coat','open coat','robe'],9:['open robe','separate dress'],
10:['short cape','crimson cape','black dress'],11:['blazer on','folded blazer','blouse'],12:['bodice lacing','eyelets','corset'],
13:['tiered skirt','gathered skirt','tier seams'],15:['one-piece swimsuit','back opening'],17:['pleated skirt','pleats'],
18:['ruffled skirt','ruffles','side drawstring'],19:['high-low hem','high-low skirt','longer rear hem'],20:['overskirt','shorts'],
21:['standing collar','high collar'],22:['wrap neckline','overlapping front','V neckline'],23:['neckline'],
25:['lace neckline','scalloped lace','lace inset'],26:['bodice support'],27:['keyhole','high neckline'],28:['open back','back opening'],
30:['puff sleeve','puffed sleeves'],31:['loose sleeve','draped sleeves'],32:['upper-arm band','detached sleeves','organza sleeves'],
33:['cuff'],34:['draped dress','fitted bodice','hanging folds'],35:['knee-length skirt','knee hem'],36:['waistband'],37:['skirt silhouette'],
39:['panel edge','overlay'],40:['skirt lining','lining revealed','underskirt'],41:['skirt opening'],42:['sash','overlap bodice'],
43:['goreum','jeogori','chima'],44:['apron straps','apron bow'],45:['trouser zipper','waistband button'],
47:['visible weave','woven cloth','twill','fine yarns'],48:['sheer layer','organza','chiffon','underlayer'],49:['mesh','tulle','netting'],
50:['textile sheen'],51:['velvet','pile panel','satin panel','reflective panel'],52:['crepe-like','crepe texture'],53:['knit relief'],
54:['denim fading','denim creases','faded denim'],55:['glossy garment','patent surface','glossy fabric'],56:['eyelet lace','scalloped trim'],
57:['sports mesh','mesh jersey'],58:['woven motif','jacquard','damask'],59:['printed pattern'],60:['embroidery','embroidered','raised thread'],
61:['jersey number','printed 10','number 10'],62:['attached ornament'],63:['ribbon knot','bow knot','ribbon tails'],64:['piping','contrast trim'],
65:['repair stitches','mended frill','worn frill'],66:['butterfly ornament','butterfly brooch'],67:['ivory bodice','ivory top','cream panel'],
68:['white-to-pink','pink gradient','gradient skirt'],70:['red sash','red fabric plane','black garment'],72:['brass fitting','metal ring','tarnished metal'],
73:['black velvet','black satin','black texture contrast'],74:['sheer sleeves','organza sleeves','opaque bodice','velvet bodice'],
75:['legwear'],76:['sock top','sock adjustment'],77:['shoe strap'],78:['split-toe boot','tabi boot'],
80:['bag strap','bag handle','crossbody bag','canvas bag'],81:['head ornament'],82:['long glove','elbow glove'],83:['jewelry attachment'],
84:['asymmetric earrings','long earring','stud earring'],85:['chain','chain fittings','draped chain','brooches'],87:['raised arm','arm raised'],
88:['pulling hem','pinching skirt','skirt hem'],89:['blouse hem','blouse adjustment'],90:['skirt side edge','walking skirt','lining'],
91:['tray','handoff','offering tray'],92:['wrapped candy','offering candy','candy bowl'],93:['paper bag','food bag'],94:['upper cabinet','reaching arm'],
95:['seated skirt','compressed folds','skirt folds','bench seat'],96:['floating','water surface'],97:['cat','seawall','crouching'],
98:['ribbon tail','moving hem','windblown skirt'],99:['wet cloth','darkened cloth','water contact'],100:['stitches','mended edge','worn textile'],
101:['textile fragment','floral fragment'],103:['waist-up','sleeve bands'],104:['three-quarter viewpoint','sleeve band'],
105:['near hand','close perspective'],106:['direct flash','handheld tilt'],107:['side light','embroidered fabric','metal buttons'],
108:['white garment','bright background','white folds'],109:['warm foreground','cool background','warm light'],110:['image grain','knit ribs'],
111:['foreground door','ribbon junction'],113:['doorway threshold','stepping','skirt edge'],115:['open vest','ruffled shirt'],
116:['cover-up','swim layer'],117:['dark sash','waist sash'],118:['flared skirt','waist attachment'],119:['wide-leg trousers','wide trousers'],
121:['tie bar','shirt tie'],122:['watch','bangle','wrist band'],123:['bent knee','lower leg'],124:['lowered sunglasses','sunglasses'],125:['metal fitting','cream textile'],
}

VARIANT_CUES={
'crew':['crewneck','crew neck','shallow rounded neckline'],
'scoop':['scoop neck','scoop neckline'],
'square':['square neckline','square neck'],
'bateau':['boat neck','bateau','broad shallow neckline'],
'asymmetric_bateau':['asymmetric neckline','asymmetric bateau'],
'strapless':['strapless','bodice upper edge'],
'off_shoulder':['off-shoulder','off shoulder'],
'spaghetti':['spaghetti straps','thin straps'],
'halter':['halter','neck strap'],
'short_puff':['short puff sleeve','puff sleeves'],
'shoulder_puff_long':['shoulder puff','puff-shoulder sleeve'],
'three_quarter':['three-quarter sleeve','three quarter sleeve'],
'lower_drape':['draped sleeve','elbow drape'],
'column':['long sleeve folds','long pleated sleeve'],
'lace_cuff':['lace cuff','lace wrist trim'],
'rolled':['rolled sleeves','rolled cuff','folded cuffs'],
'detachable':['detachable cuff','separate wrist cuff'],
'high':['high waist','high-waisted','high-rise'],
'natural':['natural waist','waist-level waistband'],
'low':['low rise','low-rise','low waistband'],
'a_line':['A-line skirt','A line skirt'],
'bell':['bell skirt','rounded skirt'],
'narrow_layers':['layered narrow skirt','two skirt layers'],
'lower_volume':['voluminous skirt','wide lower skirt'],
'diagonal':['diagonal panel','overlapping skirt panel'],
'crescent':['crescent panel','crescent textile edge'],
'curved_overlay':['boot overlay','curved leather overlay'],
'slit':['skirt slit','single slit'],
'wrap_gap':['wrap skirt','overlapping skirt panels'],
'drawstring':['drawstring','side adjustment cord'],
'faille_surface':['faille','transverse ribs'],
'satin_surface':['satin','smooth sheen'],
'rib':['rib-knit','rib knit','ribbed knit','ribbed top'],
'cable':['cable knit','crossed knit columns'],
'pointelle':['pointelle','knit openings'],
'floral':['floral print','flower print'],
'plaid':['plaid','checked skirt','check pattern'],
'pinstripe':['pinstripe','thin stripes'],
'petal_relief':['applique petals','flower applique','raised petals'],
'rhinestone':['rhinestone','faceted ornaments'],
'pearl_like':['pearl-like','rounded beads'],
'knee_sock':['knee sock','knee-length sock'],
'thigh_high':['thigh-high','thigh band'],
'tights':['tights','waistband of tights'],
'mary_jane':['Mary Jane','instep strap'],
'ankle_sandal':['ankle sandal','sandal strap'],
'knee_boot':['knee-high boot','knee boot'],
'horn_headband':['horn headband','costume horns'],
'bunny_headband':['bunny headband','costume ears'],
'hair_ribbon':['hair ribbon','hair bow'],
'pendant':['pendant','necklace chain'],
'brooch':['brooch','pinned ornament'],
'neck_armor':['armor collar','neck armor'],
}

# Separate phrases for separate units. One cue cannot fill both parts of a
# multi-part discovery claim; adopted evidence and native gates remain all-of.
MULTI={
7:[['inner top','ribbed top'],['rolled sleeves','folded cuffs']],
9:[['open robe','separate dress'],['slip layer','inner slip']],
19:[['high-low hem','longer rear hem'],['diagonal panel','asymmetric panel']],
26:[['strapless','bodice upper edge'],['side panels','bodice panels']],
42:[['sash','overlap bodice'],['short tied end','short obi']],
45:[['trouser zipper','waistband button'],['pocket opening','separate pocket']],
51:[['velvet','pile panel','satin panel'],['visible seam','joined panels','panel junction']],
70:[['red sash','red fabric plane'],['black panels','black garment']],
87:[['raised arm','arm raised'],['armhole folds','shirt tension']],
91:[['tray','handoff'],['two people','giver and receiver']],
96:[['floating','water surface'],['water contact','torso at water']],
98:[['ribbon tail','moving hem'],['attached knot','waistband attachment']],
}


def save(path,value): path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def main():
 A=SKILL/'assets'
 ep=A/'photo_prompt_wardrobe_owner_relations_extension.json'
 vp=A/'photo_prompt_visual_obligations_wardrobe_owner_relations.json'
 e=json.loads(ep.read_text());v=json.loads(vp.read_text());d=json.loads((HERE/'INTEGRATION-DECISIONS.json').read_text())
 entries={x['id']:x for rows in e['slots'].values() for x in rows}
 # The research meaning is a support surface, not a particular furniture type.
 cid='wkr_wk095_selected_relation_candidate';x=entries[cid]
 old=x['en'];new=old.replace('chair seat','seat surface')
 for k in ['en','embedding_text']:x[k]=x[k].replace(old,new)
 for k in ['aliases','keywords','paraphrases','concept_terms','concept_units']:x[k]=[z.replace(old,new) for z in x[k]]
 for r in x['relations']:r['object']=r['object'].replace('chair-seat','seat-surface')
 for b in e['visual_semantics']:
  if cid in b['candidate_ids']:
   b['primary_visual_proposition']=new
   for c in b['component_groups']:c['visible_evidence']=[z.replace(old,new) for z in c['visible_evidence']]
   b['source_keywords']=[z.replace(old,new) for z in b['source_keywords']]
   b['relations']=x['relations']
 changes=[]
 for p in v['profiles']:
  parts=p['id'].split('_');num=int(parts[1][2:]);suffix='_'.join(parts[2:])
  if p['id']=='wkr_wk095_selected_relation':
   for k in ['exact_terms']:p['activation'][k]=[z.replace(old,new) for z in p['activation'][k]]
   for g in p['activation']['hard_activation']['required_any_groups']:g['any_terms']=[z.replace(old,new) for z in g['any_terms']]
   p['semantics']['definition']=new
   p['semantics']['visual_components']=[z.replace(old,new) for z in p['semantics']['visual_components']]
   p['concept_candidate']['concept_terms']=[z.replace(old,new) for z in p['concept_candidate']['concept_terms']]
  cues=VARIANT_CUES.get(suffix,CUES[num])
  for i,c in enumerate(p['authored_components']['components']):
   if num==95:
    for k in ['match_terms','evidence_terms']:c[k]=[z.replace(old,new) for z in c[k]]
    c['instruction']=c['instruction'].replace(old,new);c['render_gate']['description']=c['render_gate']['description'].replace(old,new)
   extra=MULTI[num][i] if len(p['authored_components']['components'])>1 else cues
   c['match_terms']=list(dict.fromkeys([*c['match_terms'],*extra]))
  changes.append({'profile_id':p['id'],'component_discovery_terms':[c['match_terms'] for c in p['authored_components']['components']],
                  'hard_exact_terms_unchanged':num!=95,'adopted_all_of_evidence_unchanged':num!=95,'native_gate_set_unchanged':True})
 for r in d['rows']:
  if r.get('candidate_id')==cid:
   r['reviewed_text']=new;r['relations']=x['relations']
 d['discovery_refinement']={'reason':'Initial independent frozen-core probes exposed few new slot candidates and zero new visual concepts. Full-sentence-only component lexicons prevented natural phrasing from reaching optional concepts.',
    'scope':'All 146 reviewed selected variants, with positive part observations. No arm-specific routing, rank changes, artificial core rewriting or new hard aliases.',
    'rules':'Discovery fragments establish only optional exposure. The complete relation, every adopted evidence field and native gate remain required after selection.',
    'support_surface_correction':'WK095 uses the research seat/support surface, not an unnecessary chair-type restriction.',
    'changes':changes}
 prior=e.pop('maintenance_ref');rp=ROOT/'docs/research-evidence/photo-prompt/extension-maintenance'
 old_record=json.loads((rp/(prior['record_id']+'.json')).read_text())
 record={**old_record,'record_id':'wardrobe-owner-relations-20261010-v6','prior_maintenance_ref':prior,
         'authored_source_sha256':digest(e),'profile_source_sha256':digest(v),'decisions_sha256':digest(d),
         'reason':'Natural optional component discovery with unchanged full selected obligations; restore generic seat support meaning.'}
 e['maintenance_ref']={**prior,'record_id':record['record_id'],'sha256':digest(record)}
 with source_update(SKILL):
  save(ep,e);save(vp,v);save(HERE/'INTEGRATION-DECISIONS.json',d);save(rp/(record['record_id']+'.json'),record)
 print('refined profiles',len(changes),'changed slot prototype',1)


if __name__=='__main__':main()
