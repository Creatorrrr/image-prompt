"""Manual exact-quote, owner and mode audit; no semantic classifier."""
import runpy
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'authored/native_05250_05250_06250.05850_05900.literals.py';D=runpy.run_path(str(p))['D']
def value(o,key,val):
 a=list(D[o]['claims'][key]);a[5]=val;D[o]['claims'][key]=tuple(a)
def quote(o,fid,q):D[o]['anchors']=[(i,path,key,q if i==fid else old) for i,path,key,old in D[o]['anchors']]
def after(o):return next(a['after'] for a in D[o]['text_corrections'] if a['pointer']=='/content/embedding_text')
value(5850,'context','localized_fumarole_steam_vent_context')
value(5855,'dead','one_specific_existing_dead_person');value(5857,'representative','declared_representative_fermentation_sample')
quote(5860,'m_pose',after(5860).split(' Its existing anatomy')[0])
full='Divide the main composition into the requested large color regions with a readable directional boundary.'
for fid in ['e_layout','m_layout','u_layout','e_visible','m_visible']:quote(5864,fid,full)
value(5867,'disk','one_opaque_disk');value(5867,'registration','central_marker_preserves_solar_registration')
quote(5867,'m_reg','solar observation hardware evidence where one opaque disk masks the bright photosphere, a central marker preserves solar registration and the ejection front expands outside the mask')
# Split ordinary-summer context and independent missing-wearer/weather-scope claim.
value(5872,'context','ordinary_summer_dailywear')
D[5872]['claims']['scope']=('concept','garment_pair','concept.owner_scope.context','context','concept.owner_scope.context/v1','no_particular_wearer_or_live_summer_weather_specified',[],None,None)
D[5872]['anchors']=[(i,path,'scope' if i=='m_scope' else key,q) for i,path,key,q in D[5872]['anchors']]
quote(5875,'m_rib',after(5875).split(' Judge ')[0])
# Foot availability is an actual selected pose requirement, not preexisting just because stable.
c=D[5878]['text_corrections'][0];c['after']=c['after'].replace('foot remains stably available','foot is stably available');c['reason']+=' Final manual mode audit: source stable/available does not say preserve a prior available pose; selected availability is actual E.'
a=list(D[5878]['claims']['footavailable']);a[3]='effect';a[6]=['m_player','m_foot'];a[7]='set_value';a[8]=['player'];D[5878]['claims']['footavailable']=tuple(a)
quote(5878,'m_available','That player’s existing one selected foot is stably available for a pedal')
D[5878]['roles']['body_pose']=(['m_pose','m_available'],['effect'])
D[5878]['meaning']=D[5878]['meaning'].replace('Stable available-foot relation P','Actual stable available-foot pose requirement E')
D[5878]['owner_issue']=D[5878]['owner_issue'].replace('Stable foot remains availability P proposal root-unapproved','Stable foot availability is selected pose E after direct mode audit; prior partial30 preservation superseded, literal proposal root-unapproved')
# Existing resources input scope is explicit, not borrowed from adult adjective.
c=D[5884]['text_corrections'][0];c['after']=c['after'].replace('existing adult, matching resources','existing adult, existing matching resources');quote(5884,'m_res','existing matching resources')
value(5887,'regression','affected_by_regression_context')
# M grammatically coordinates coherent crevasses AND debris with accumulate; retain both, mark precision pending.
full='natural process action: a continuous ice mass moves down a broad glacial valley while coherent crevasses and transported debris accumulate along its margins'
quote(5890,'m_accumulate',full)
D[5890]['claims']['crevasseaccum']=('action','crevasses','material.motion.accumulation','effect','material.motion.accumulation/v1','coherent_crevasses_accumulate_along_ice_margins_manifestation_unspecified',[],'set_value',['crevasses','ice'])
D[5890]['anchors'].append(('m_crevasseaccum','/content/embedding_text','crevasseaccum',full));D[5890]['units']['/content/embedding_text'].append('m_crevasseaccum')
D[5890]['meaning']+=' Mgrammar coordinates crevasses and debris with accumulate; the crevasse accumulation demand is retained unresolved, not silently limited to debris.'
D[5890]['owner_issue']=D[5890]['owner_issue'].replace('Mpronoun margin antecedent requires full sentence exact anchor in final audit.','Full Msentence anchors ice-margin antecedent and both conjuncts accumulating; exact crevasse-accumulation meaning remains pending, not repaired by domain assumptions.')
# Actual presence/readability of functional cues is retained E, not turned into keep by rewriting provides.
c=D[5892]['text_corrections'][0];c['after']=c['after'].replace('intended use remain,','intended use are present,');c['reason']+=' Final manual audit retains original provides-clear-cues as actual cue presence/readability E, rather than added remains preservation.'
a=list(D[5892]['claims']['cues']);a[2]='framing.functional_cues';a[3]='effect';a[4]='framing.functional_cues/v1';a[5]='clear_route_timing_intended_use_cues_present';a[6]=['m_place'];a[7]='set_value';a[8]=['place'];D[5892]['claims']['cues']=tuple(a)
quote(5892,'m_cues','clear cues of route, timing and intended use are present')
D[5892]['meaning']+=' Actual clear functional/timing-cue presence E retained; no preservation-only rewrite of provides.'
quote(5896,'m_gems',after(5896).split(' The exact region')[0]);quote(5896,'m_visible',after(5896).split(' The exact region')[0])
quote(5898,'m_axis',after(5898).split(' This is')[0]);quote(5898,'m_height',after(5898).split(' This is')[0])
for o in [5878,5890,5892]:D[o]['effects']=sorted({(v[0],v[1],v[2]) for v in D[o]['claims'].values() if v[3]=='effect'})
with p.open('w') as f:
 f.write('"""Explicit manually authored meaning/fact cells; no semantic inference code."""\nD={}\n')
 for o,a in D.items():f.write('D['+str(o)+']='+repr(a)+'\n')
print('Explicit manual precision/mode audit completed; formal qualification0.')
