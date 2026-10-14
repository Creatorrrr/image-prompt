"""Manual precision corrections after source and fullspec recomparison; no classifier."""
import runpy
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'authored/native_05250_05250_06250.06000_06050.literals.py';D=runpy.run_path(str(p))['D']
def C(d,t,p,m,v,req=[],op=None,recv=None,typ=None):return(d,t,p,m,typ or p+'/v1',v,req,op,recv)
m='/content/embedding_text';k='/content/ko'
# EN chain does not itself name an anchor/bridge. M-only coherence claim already preserves that precision.
D[6008]['claims']['chain']=C('composition','depth_planes','spatial.depth.chain','effect','foreground_midground_distant_background_depth_chain',[],'set_value',[])
# The singular-axis precision is actually explicit in Korean, so bind that fact to its actual positive field.
D[6025]['anchors']=[('k_axis',k,key,'들것·구급차 적재부·병원 인계 방향이 한 이송 축으로 보이는 구역') if fid=='e_axis' else (fid,path,key,q) for fid,path,key,q in D[6025]['anchors']]
D[6025]['roles']['composition']=(['k_axis'],['effect'])
# Four conjunctions are not an automatic total ordering of their first three operations.
D[6027]['claims']['sequence']=C('timing','procedure','procedure.sequence.context','context','petition_permission_verification_resource_exchange_and_ruling_recording_conjoined_operations')
# M says commercial key art, EN says campaign; keep each field's actual precision.
D[6028]['claims']['purpose']=C('role','capture','capture.purpose','effect','commercial_fantasy_key_art_armor_legibility',[],'set_value',['capture'])
# Korean rolloff has no 'gentle' qualifier; that precision stays EN only.
D[6036]['claims']['kgeneric']=C('color','image_tone','image.tone.context.ko','context','highlight_rolloff_and_rich_black_tone')
D[6036]['anchors']=[('k_generic',path,'kgeneric',q) if fid=='k_rolloff' else (fid,path,key,q) for fid,path,key,q in D[6036]['anchors']]
# Body-region fact scope is the positive named local region, not inferred complete body anatomy.
D[6015]['claims']['cheek_region']=C('body_geometry','cheek_temple_span','body.region.cheekbone','prerequisite','high_cheekbone_region')
D[6015]['claims']['temple_region']=C('body_geometry','cheek_temple_span','body.region.temple','prerequisite','temple_region')
q='cosmetic blush distributed from the high cheekbones toward the temples in an elongated softly blended path'
D[6015]['anchors'] += [('m_cheek_region',m,'cheek_region',q),('m_temple_region',m,'temple_region',q)]
D[6015]['roles']['body_region']=(['m_cheek_region','m_temple_region'],['prerequisite'])
D[6015]['owner_issue']+=' Namedcheekbone/temple localregionP now separatelyauthored, actualcarrieridentity/visibilitystillunproved; notanatomicalgeometrychange ornewfacepresence.'
D[6034]['roles']['body_region']=(['m_scalp'],['prerequisite'])
D[6034]['owner_issue']+=' Namedscalp-regionbody_regionproposal only; independentwholeactoridentity/visibilitynotasserted.'
D[6041]['roles']['body_region']=(['m_knees','m_lower'],['prerequisite'])
# The full silhouette_proportion spec explicitly includes clothed silhouette proportions.
D[6041]['claims']['silhouette']=C('body_geometry','shorts','wardrobe.silhouette.relative_length','effect','owned_bermuda_silhouette_ends_around_same_knees_longer_than_ordinary_shorts_shorter_than_calf_length_capri',['m_region','m_knees'],'set_value',['shorts','wearer_lower_region'])
D[6041]['anchors'].append(('m_silhouette',m,'silhouette',D[6041]['text_corrections'][0]['after']))
D[6041]['roles']['silhouette_proportion']=(['m_silhouette'],['effect'])
D[6041]['owner_issue']='Existingwearerknee/lowerlegowner witness andnewgarment/hem/exposure/visibility/ownedclothedsilhouette effectspermissions pending. Garmentownedlegs notextraanatomiclegs. Full144spec explicitlyincludesclothedsilhouetteproportion, so relativeknee-length factstaysshorts-owned andsupports silhouette_proportion alongsideindependenthemconstruction; noactualbodyproportionchange. Regioninputclarificationunapproved.'
D[6041]['binding_intent']='Preserve optional/direct silhouette_proportion .54 human/sixdeny plusintrinsichuman. Fullspecclothedsilhouette permitsseparatelyauthoredshorts-ownedrelativehem/kneelength, garment_detailownsthehemconstruction. No bodyproportionmutation, twohemsnotanatomiccountorfootwearstate.'
for a in D.values():
 units={}
 for fid,path,key,q in a['anchors']:units.setdefault(path,[]).append(fid)
 a['units']=units
 a['effects']=sorted({(v[0],v[1],v[2]) for v in a['claims'].values() if v[3]=='effect'})
with p.open('w') as f:
 f.write('"""Explicit manually authored native meaning/fact cells; no semantic inference code."""\nD={}\n')
 for o,a in D.items():f.write('D['+str(o)+']='+repr(a)+'\n')
