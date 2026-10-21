"""Bounded selected-primary layout and scene-affect signatures.

No corpus IDs, queries, tags, ranks or model calls. This advisory compiler keeps
whole guards/effects in its output; source and request relations must agree.
"""
import hashlib
import json
import re

_LM_RXFLAGS=re.I|re.S

def _LM_has(pattern,text):return bool(re.search(pattern,text,_LM_RXFLAGS))

def _LM_seal(value):return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

_LM_OWNER={
 'human':r'\b(?:human|adult|person|people|man|woman|actor(?![- ]relative))\b|성인|사람|배우|인물',
 'bowl':r'\b(?:ceramic\s+)?bowl\b|도자기\s*그릇|도자기\s*볼',
 'cloth':r'\b(?:linen\s+)?cloth\b|리넨\s*천|접은\s*천|접힌\s*천|직물',
 'table':r'\btable(?:top)?\b|탁자|테이블|식탁|상판|찻상',
 'pear':r'\bpear\b|배\s*하나',
 'stone':r'\bstones?\b|돌\s*(?:세|3)|돌의',
 'teapot':r'\bteapot\b|찻주전자',
 'cup':r'\bcup\b|찻잔',
 'spoon':r'\bspoon\b|숟가락|스푼',
 'vase':r'\bvase\b|꽃병',
 'chair':r'\bchairs?\b|의자',
 'bench':r'\bbench\b|벤치',
 'door':r'\bdoor(?:way)?\b|출입구|가게\s*문|문\s*안쪽',
 'window':r'\bwindow\b|창가|창문|큰\s*창',
 'mirror':r'\bmirror\b|거울',
 'branch':r'\bbranches\b|foliage|나뭇가지|전경\s*가지',
 'boat':r'\bboat\b|배\s*한\s*척|먼\s*배',
 'cyclist':r'\bcyclist\b|자전거\s*탄',
 'route':r'\b(?:road|route|path)\b|도로|시골길',
 'spacecraft':r'\bspacecraft\b|우주선',
 'envelope':r'\benvelope\b|봉투',
 'book':r'\bbook\b|책(?:을|이|의|과|\s)',
 'lamp':r'\blamp(?:light)?\b|등불빛|등불|램프',
 'decoration':r'\b(?:paper\s+)?decorations?\b|종이\s*장식',
}
# Explicit source identities/contexts that cannot disappear into a generic
# layout or mood phrase. This is an open bounded detector, not an owner ontology.
_LM_CONTEXT={
 'cosmic':r'interstellar|spacecraft|성간|우주선',
 'mythic':r'\b(?:Nataraja|Apasmara|Anubis|Thoth|Ammit|Osiris)\b|나타라자|아파스마라|이집트\s*심판',
 'human_pose':r'\b(?:elbow|knee|wrist|torso|forehead)\b|팔꿈치|무릎|손목|몸통|이마',
 'seated':r'\b(?:sits?|seated)\b|앉아|앉은',
 'standing':r'\bstands?\b|서\s*있|서\s*있다',
 'stage_light':r'warm\s+stage\s+light|따뜻한\s*무대\s*조명',
 'audience':r'\baudience\b|청중|관객',
 'garment':r'\b(?:garment|scarf|zipper|fringe|hair|robe)\b|의복|스카프|지퍼|앞머리|로브',
}
_LM_AFFECT={
 'calm':r'\b(?:calm|unhurried|serene|peaceful|relaxed|contemplative)\b|차분|서두르지\s*않|평온|편안|사색',
 'uneasy':r'\b(?:uneasy|unresolved|tense|threatening|anxious)\b|불편|해소되지\s*않|긴장|위협|불안',
 'wistful':r'\b(?:wistful|melanchol\w*|lonely|bittersweet|nostalgic)\b|아련|멜랑콜리|외로운|달콤씁쓸|씁쓸한|향수',
 'hopeful':r'\bhopeful\b|희망',
 'intimate':r'\b(?:intimate|hushed)\b|친밀|고요',
 'festive':r'\b(?:festive|cheerful)\b|축제|경쾌',
}

class Semantic:
    def __init__(self,masker):self.masker=masker

    def _surface(self,text):
        text=re.sub(r'누구의[^.!?;\n]{0,260}사실로\s*확정하지\s*않는다',' ',text)
        text=self.masker(text)
        # Type/epistemic references do not create physical people or hands.
        text=re.sub(r'\b(?:left|right)[- ]hand(?=\s+(?:field|side|region|area|corner))','coordinate',text,flags=re.I)
        text=re.sub(r'(?:(?:한|두|세|네|다섯|여섯|몇)\s+|\b\d+\s*)개(?:가|를|는|의|로|와|도)?',lambda m: ('three objects' if m.group().lstrip().startswith('세') else 'two objects' if m.group().lstrip().startswith('두') else 'objects'),text)
        text=re.sub(r'\bwhile\s+leaving\b[^.!?;\n]{0,170}\b(?:feelings?|mental\s+states?)\b[^.!?;\n]{0,50}\bunknown\b',' ',text,flags=re.I)
        text=re.sub(r'모든\s*인물의\s*실제\s*감정은?[^.!?;\n]{0,40}알\s*수\s*없는',' ',text)
        return text

    def _owners(self,text):return sorted(k for k,p in _LM_OWNER.items() if _LM_has(p,text))

    def _affects(self,focus):
        # Resolve local positive affect owners, not every adjective in the scene.
        text=self._surface(focus)
        # Avoid is an exclusion operator; retain a positive request after seek.
        text=re.sub(r'\bavoid\b.*?(?=;|\bseek\b|\Z)',' ',text,flags=re.I|re.S)
        text=re.sub(r'[^,;.!?\n]{0,90}해석을\s*피하고',' ',text)
        text=re.sub(r'\b(?:actor.?s?\s+)?(?:deliberately\s+)?(?:anxious|tense)\s+facial\s+performance',' ',text,flags=re.I)
        text=re.sub(r'(?:연기하는|연기할)\s*(?:불안한|긴장된)\s*표정',' ',text)
        return sorted(k for k,p in _LM_AFFECT.items() if _LM_has(p,text))

    def request(self,role,text):
        m=re.search(r'^Photographic role:[ \t]*(.*?)(?=\nScene context:|\Z)',text,re.S)
        if not m:return None
        focus=m.group(1);c=re.search(r'\nScene context:[ \t]*(.*)',text,re.S);scene=c.group(1) if c else ''
        if role=='visual_hierarchy':
            ordered=self._attention_request(text,focus,scene,m.start(1))
            if ordered is not None:return ordered
            equal=re.search(r'equal\s+(?:(?:image|visual)\s+)?prominence|equally\s+(?:visually\s+)?prominent|(?:동등한|같은|동일한)\s*(?:시각적\s*)?(?:두드러짐|주목도)|(?:모두|각자).{0,25}동등하게.{0,20}두드러',self._surface(focus),re.I)
            if equal:
                return {'role':role,'asserts':False,'exclusion_only':True,'intent_mode':'equal_attention_without_priority',
                        'witnesses':[{'pointer':'/request','start':m.start(1),'end':m.end(1),'quote':focus}],
                        'constraint':'Existing declared owners have equal image prominence; no primary/secondary priority may be supplied.','native_approval':False}
            return None
        f=self._surface(focus);s=self._surface(scene);both=f+'\n'+s
        owners=self._owners(s);contexts=sorted(k for k,p in _LM_CONTEXT.items() if _LM_has(p,s))
        neutral=_LM_has(r'neutral.{0,20}(?:reading|atmosphere)|(?:정서|분위기).{0,15}중립|중립.{0,15}(?:정서|분위기)',f)
        affects=self._affects(focus)
        affect_head=_LM_has(r'atmosphere|emotional\s+(?:tone|reading)|festive\s+(?:warmth|mood)|photograph.{0,35}feel|scene.{0,35}(?:tone|serene)|(?:serene|calm|peaceful)\s+scene|\bfeel\s+(?:quiet|bittersweet|nostalgic|wistful|tense|calm|intimate)|정서|분위기|사진.{0,30}느껴|장면.{0,20}평온',f)
        if role in ('mood','emotional_mood'):
            if neutral:return None
            if not affects or not affect_head:return None
            carriers=[]
            if self._contextual_moment(both) and self._existing_setting(both):carriers.append('contextual_moment')
            if _LM_has(r'spacing|empty\s+space|interval|opposite\s+ends|between\s+them|간격|빈\s*공간|양\s*끝|그\s*사이',both):carriers.append('interval')
            if _LM_has(r'pool\s+of\s+(?:lamp)?light|share.{0,40}(?:lamp)?light|arrangement\s+and\s+light|등불빛|빛을\s*함께|배치와\s*빛',both):carriers.append('shared_light')
            if _LM_has(r'\bopens?\b.{0,70}\b(?:shop|door)|가게\s*문을\s*열|개구부.{0,30}열',s) and _LM_has(r'light|warm\s+interior|빛|따뜻한\s*실내',s):carriers.append('lit_opening')
            if all(v in owners for v in ('bowl','cloth','table')) and _LM_has(r'soft|부드러',s):carriers.append('bowl_cloth')
            return {'role':'emotional_mood','active':True,'asserts':True,'witnesses':[{'start':m.start(1),'end':m.end(1),'quote':focus}],'affects':affects,'carriers':carriers,'owners':owners,'contexts':contexts,'scene':s,'focus':f,'native_approval':False}
        if role!='composition':return None
        # A nominal role definition without a concrete scene/owner or an
        # affirmative placement assertion is discovery context, not a binding.
        imperative=_LM_has(r'^(?:place|arrange|keep|balance|align|use|let|give|make|retain|preserve|position|frame)\b',f.strip())
        finite_relation=_LM_has(r'\b(?:occupies|sits|rests|stands|extends|surrounds)\b|놓여\s*있|차지한다|이어진다',f)
        counted_owner=_LM_has(r'\b(?:one|two|three|four|single)\b.{0,45}\b(?:objects?|subjects?|forms?|masses|elements?|anchors?)\b|(?:한|두|세)\s*(?:물체|대상)|물체\s*(?:하나|둘|셋)',f)
        if not s.strip() and not owners and not (imperative or finite_relation or counted_owner):return None
        # Scene mood predicate outranks geometry used only as its means.
        if affects and affect_head and not neutral:return None
        if _LM_has(r'printed|motif|label\s+letter|인쇄|무늬|라벨\s*글자',f):return None
        kinds=[]
        if _LM_has(r'triang\w*|non[- ]collinear|삼각|비공선',f):kinds.append('triangle')
        if _LM_has(r'symmetr\w*|bilateral\s+correspondence|좌우\s*대칭',f):kinds.append('symmetry')
        if _LM_has(r'counterbalanc\w*|counterweight|balanc\w*.{0,130}(?:across\s+the\s+frame|between\s+them)|반대쪽.{0,100}균형',f):kinds.append('counterbalance')
        if _LM_has(r'diagonal|대각선',f):kinds.append('diagonal')
        if _LM_has(r'foreground.{0,65}(?:frame|boundary|enclos\w*)|전경.{0,55}(?:틀|경계|둘러)',f):kinds.append('foreground_boundary')
        if _LM_has(r'(?:uninterrupted|low-detail|negative.space|open\s+space).{0,40}|빈\s*공간|여백',f) and not kinds:kinds.append('negative_space')
        if self._unequal_pair_field(f+' '+s):kinds.append('unequal_pair_field')
        if not kinds:return None
        coords=[]
        for name,p in [('lower_left',r'low\s+on\s+the\s+left|lower[- ]left|왼쪽\s*아래'),('lower_right',r'lower[- ]right|오른쪽\s*아래'),('upper_left',r'upper[- ]left|왼쪽\s*위')]:
            if _LM_has(p,f):coords.append(name)
        return {'role':'composition','active':True,'asserts':True,'witnesses':[{'start':m.start(1),'end':m.end(1),'quote':focus}],'kinds':kinds,'coordinates':coords,'owners':owners,'contexts':contexts,'scene':s,'focus':f,'native_approval':False}

    def source(self,role,units,effects):
        if role=='visual_hierarchy':return self._attention_source(units,effects)
        # Exact positive selected fields only; metadata/aliases add no authority.
        selected=[u for u in units if re.match(r'^/content/(?:en$|ko$|definition$|embedding_text$|concept_units/|components/|semantics/definition$|composition_instruction$)',u.get('pointer',''))]
        if not selected:return None
        raw='\n'.join(u['text'] for u in selected);text=self._surface(raw)
        record={'role':role,'source_units':selected,'evidence':selected,'constraints':[u for u in units if u.get('pointer')=='/content/application_contract'],'effects':effects,'effects_sha256':_LM_seal(effects),'native_approval':False,'whole_source_conditions_effects_cumulative':True}
        if role in ('mood','emotional_mood'):
            record['role']='emotional_mood'
            if not ('atmosphere' in effects.get('dimensions',[]) or any(p.get('property','').startswith(('mood.','affect.')) for p in effects.get('properties',[]))):return None
            parameter=_LM_has(r'(?:requested|declared).{0,45}(?:emotional|affect)|요청된\s*정서|선언.{0,30}정서',text)
            if any(self._moment_source_field(self._surface(u['text'])) for u in selected):kind='contextual_moment';fixed=[]
            elif _LM_has(r'(?:two|둘).{0,80}(?:scene\s+elements|장면\s*요소)',text) and _LM_has(r'interval|intervening\s+space|간격|그\s*사이\s*공간',text):kind='interval';fixed=[]
            elif _LM_has(r'coherent\s+region\s+of\s+illumination|일관된\s*조명\s*영역',text):kind='shared_light';fixed=[]
            elif _LM_has(r'existing\s+opening|기존\s*개구부',text) and _LM_has(r'current\s+action|opening\s+action|현재\s*행동|여는\s*동작',text):kind='lit_opening';fixed=[]
            elif _LM_has(_LM_OWNER['bowl'],text) and _LM_has(_LM_OWNER['cloth'],text):kind='bowl_cloth';fixed=['bowl','cloth','table']
            else:return None
            record.update(kind=kind,parameter_affect=parameter,fixed_owners=(self._owners(text) if kind=='contextual_moment' else fixed),fixed_context=(sorted(k for k,p in _LM_CONTEXT.items() if _LM_has(p,text)) if kind=='contextual_moment' else []),affects=[] if parameter else self._affects(raw),required_human=kind=='lit_opening',required_source_duties={'contextual_moment':['independently_declared_pause_or_unresolved_phase','existing_surroundings','requested_interpretive_affect','no_new_event_or_private_emotion_fact'],'interval':['two_existing_owners','two_boundaries','readable_interval'],'shared_light':['two_or_more_existing_receivers','coherent_light_region','source_direction','readable_darker_surroundings'],'lit_opening':['existing_actor','existing_opening','current_opening_action','light_across_boundary'],'bowl_cloth':['ceramic_bowl','folded_cloth','tabletop','small_gap','soft_side_light']}[kind])
            return record
        if role!='composition' or 'composition' not in effects.get('dimensions',[]):return None
        kinds=[]
        if _LM_has(r'triangular\s+grouping|object.{0,100}non[- ]collinear|물체.{0,80}삼각\s*배치',text):kinds.append('triangle')
        if _LM_has(r'bilateral\s+correspondence|paired\s+scene\s+masses.{0,110}(?:correspond|axis)|중심축.{0,45}대응|좌우\s*대칭',text):kinds.append('symmetry')
        if any(self._image_counterbalance_field(self._surface(u['text'])) for u in selected):kinds.append('counterbalance')
        if any(self._unequal_pair_field(self._surface(u['text'])) and _LM_has(r'independently\s+declared|독립적으로\s*선언',u['text']) for u in selected):kinds.append('unequal_pair_field')
        if _LM_has(r'(?:route|path).{0,100}diagonal|diagonal.{0,40}(?:path|route)|길.{0,90}대각선|대각선\s*움직임\s*경로',text):kinds.append('diagonal')
        if _LM_has(r'(?:scene[- ]bound|physical).{0,70}foreground.{0,80}(?:boundary|edge)|foreground\s+boundary\s+enclos|실제\s*전경\s*경계',text):kinds.append('foreground_boundary')
        if _LM_has(r'negative.space|low-detail\s+(?:area|field)|저정보\s*(?:영역|배경)',text) and not kinds:kinds.append('negative_space')
        if not kinds:return None
        coords=[]
        for name,p in [('lower_left',r'lower[- ]left|왼쪽\s*아래'),('lower_right',r'lower[- ]right|오른쪽\s*아래'),('upper_left',r'upper[- ]left|왼쪽\s*위')]:
            if _LM_has(p,text):coords.append(name)
        # Boundary-type alternatives are a domain, not simultaneous fixed owners.
        domain_boundary='foreground_boundary' in kinds and _LM_has(r'\bor\s+other\s+scene[- ]bound|doorway,\s*window|foliage\s+gap',text)
        fixed_context=sorted(k for k,p in _LM_CONTEXT.items() if _LM_has(p,text))
        fixed_owners=self._owners(text)
        if domain_boundary:fixed_owners=[]
        required_human=(effects.get('source_conditions',{}).get('for_any')==['human'])
        direct_relation='\n'.join(self._surface(u['text']) for u in selected if u['pointer']!='/content/embedding_text')
        required_gaze=_LM_has(r'\bgaze\b|바라보는\s*인물|시선\s*벡터',direct_relation)
        record.update(required_human=required_human,required_gaze=required_gaze,placement_parameter='unequal_pair_field' in kinds and _LM_has(r'(?:specified|declared).{0,30}(?:position|placement)|지정된.{0,15}위치',text),kinds=kinds,coordinates=coords,fixed_owners=fixed_owners,fixed_context=fixed_context,owner_parameter_domain=domain_boundary or _LM_has(r'independently\s+declared|existing\s+(?:object|moving\s+subject)|독립적으로\s*선언',text))
        return record

    def _existing_setting(self,text):
        return _LM_has(r'\b(?:station|room|surroundings|setting|domestic|platform|street|workshop|garden|interior|landscape)\b|주변|환경|장소|실내|방|역|정원',text)

    def _contextual_moment(self,text):
        return _LM_has(r'\b(?:pause|pauses|paused|waiting|lingering\s+moment|unresolved\s+(?:event|phase|outcome))\b|before\b[^.!?;\n]{0,90}\boutcome\b[^.!?;\n]{0,30}\bknown\b|멈춤|잠시\s*멈|기다리|미정인|아직.{0,25}(?:결과|정해지)',text)

    def _moment_source_field(self,text):
        return (_LM_has(r'independently\s+declared|독립적으로\s*선언',text)
                and _LM_has(r'pause|unresolved\s+event\s+phase|멈춤|사건\s*단계',text)
                and _LM_has(r'existing\s+surroundings|기존\s*주변',text)
                and _LM_has(r'requested\s+emotional\s+atmosphere|요청된\s*정서',text))

    def _unequal_pair_field(self,text):
        if _LM_has(r'\b(?:three|four|five|several|many)\b.{0,35}\bobjects\b|물체\s*(?:셋|넷)|세\s*물체',text):return False
        pair=_LM_has(r'\btwo\b.{0,45}\bobjects\b|두\s*(?:기존\s*)?물체|물체\s*(?:둘|두)|\b(?:main|primary)\b.{0,60}\bsecondary\b',text) or len(set(self._owners(text))-{'human','cyclist','route','door','window'})==2
        visual=_LM_has(r'unequal\s+(?:visual\s+(?:weight|masses)|image\s+(?:weight|prominence))|balanced\s+secondary|(?:불균등|불균형).{0,20}시각적?\s*무게',text)
        field=_LM_has(r'negative.space|open\s+(?:image\s+)?(?:region|field|space)|빈\s*영역|여백|빈\s*공간',text)
        return pair and visual and field

    def _image_counterbalance_field(self,text):
        # A posture can counterbalance physically. The composition family needs
        # one field witnessing the full image-owned unequal-weight relation.
        primary=_LM_has(r'(?:dominant|primary).{0,40}off[- ]cent(?:er|re)|(?:큰|지배적인).{0,25}오프센터.{0,25}(?:주\s*피사체|덩어리)',text)
        secondary=_LM_has(r'(?:smaller|secondary).{0,65}(?:counterweight|cue)|작은.{0,25}(?:보조\s*요소|대비\s*요소)',text)
        separation=_LM_has(r'separated|across\s+the\s+(?:field|frame)|intervening\s+(?:open\s+)?space|떨어진|사이의.{0,15}(?:공간|여백)',text)
        image_relation=_LM_has(r'visual\s+(?:balance|equilibrium)|across\s+the\s+(?:field|frame)|시각\s*무게.{0,25}상쇄|비대칭\s*균형\s*구도',text)
        return primary and secondary and separation and image_relation

    def fit(self,req,src):
        if not req or not src or not req.get('active',True):return 'unproven'
        if req.get('role')!=src.get('role'):return 'unproven'
        if req['role']=='visual_hierarchy':
            if not req.get('asserts') or len(req.get('owner_order',[]))<2:return 'unproven'
            if src.get('parameter_order'):
                if src.get('extra_owner_requirements') or src.get('extra_method_requirements'):return 'unproven'
                grouped=any(len(level)>1 for level in req.get('owner_levels',[]))
                if grouped != bool(src.get('parameter_partial_order')):return 'unproven'
                return 'supported'
            if any(len(level)>1 for level in req.get('owner_levels',[])):return 'unproven'
            source_order=src.get('owner_order',[])
            if len(source_order)!=len(req['owner_order']):return 'conflicting'
            if source_order!=req['owner_order']:return 'conflicting'
            return 'supported'
        if req['role']=='composition':
            wanted=set(req['kinds']);found=set(src['kinds'])
            if 'unequal_pair_field' in found and set(src['effects'].get('dimensions',[]))-{'composition'}:return 'unproven'
            if 'unequal_pair_field' in wanted and 'unequal_pair_field' not in found:return 'unproven'
            if not wanted&found:return 'conflicting'
            if src.get('required_human') and 'human' not in req.get('owners',[]):return 'unproven'
            if src.get('required_gaze') and not _LM_has(r'\b(?:gaze|looks?|looking)\b|바라보|시선',req['focus']+' '+req['scene']):return 'unproven'
            if set(src.get('fixed_context',[]))-set(req.get('contexts',[])):return 'unproven'
            if set(src.get('fixed_owners',[]))-set(req.get('owners',[])):return 'unproven'
            if not src.get('placement_parameter') and set(req.get('coordinates',[]))-set(src.get('coordinates',[])):return 'unproven'
            if 'triangle' in wanted and not (_LM_has(r'three|세\s*(?:개|objects)|3',req['focus']+' '+req['scene']) and _LM_has(r'three|exactly\s+three|세\s*(?:개|objects)', '\n'.join(u['text'] for u in src['source_units']))):return 'unproven'
            # A source with a fixed shape family cannot borrow a named motif or
            # unrelated owner as its existing physical component.
            return 'supported'
        if src['kind'] not in req.get('carriers',[]):return 'unproven'
        if src['kind']=='contextual_moment' and set(src['effects'].get('dimensions',[]))-{'atmosphere'}:return 'unproven'
        if set(src.get('fixed_context',[]))-set(req.get('contexts',[])):return 'unproven'
        if set(src.get('fixed_owners',[]))-set(req.get('owners',[])):return 'unproven'
        if not src.get('parameter_affect') and set(src.get('affects',[])).isdisjoint(req.get('affects',[])):return 'conflicting'
        return 'supported'

    def _attention_request(self,text,focus,scene,offset):
        # Equal weight, quoted commands, contextual rank and postposed negation
        # are not affirmative viewer-attention order. Keep original offsets.
        unquoted=self.masker(focus)
        if _LM_has(r'equal\s+(?:image\s+|visual\s+)?(?:weight|prominence)|(?:같은|동일한|동등한)\s*시각적\s*무게|모두가?\s*똑같이\s*두드러|(?:relative\s+visual\s+prominence|viewing\s+order).{0,35}(?:unspecified|unassigned)|(?:순서|두드러짐).{0,30}(?:지정하지|정하지)|(?:어느\s*쪽도).{0,70}(?:읽히지|지배하지)',unquoted):return None
        positive=list(unquoted)
        for c in re.finditer(r'[^,;.!?\n]+',unquoted):
            if _LM_has(r'(?:읽히지|보이지|두드러지지|지배하지|쓰지|하지)\s*(?:않|말)',c.group()):positive[c.start():c.end()]=' '*(c.end()-c.start())
        positive=''.join(positive)
        # Multiple owner-bearing positions are required. Each capture addresses
        # its exact independently supplied phrase; no owner is synthesized.
        partial=self._attention_partial(positive)
        spans=partial if partial else self._attention_positions(positive)
        if len(spans)<2:return None
        owners=[{'position':i+1,'start':offset+a,'end':offset+b,'quote':text[offset+a:offset+b]} for i,(a,b) in enumerate(spans)]
        order=[self._attention_key(o['quote']) for o in owners]
        if len(set(order))!=len(order):return None
        levels=[[order[0]],order[1:]] if partial else [[o] for o in order]
        return {'role':'visual_hierarchy','active':True,'asserts':True,
                'witnesses':[{'start':offset,'end':offset+len(focus),'quote':focus}],
                'owner_witnesses':owners,'owner_order':order,'owner_levels':levels,
                'ordered_relations':([{'earlier_position':1,'later_position':i+1} for i in range(1,len(owners))] if partial else [{'earlier_position':i+1,'later_position':i+2} for i in range(len(owners)-1)]),
                'order_owner':'whole_image','existing_owner_declarations':'exact positive requester endpoints; no source-created owners',
                'scene':self._surface(scene),'native_approval':False}

    def _attention_key(self,value):
        value=re.sub(r'^(?:let|give|keep|make|the|an?|and|with)\s+','',value.strip(),flags=re.I)
        return re.sub(r'\s+',' ',value).casefold().strip(' ,.;')

    def _attention_partial(self,value):
        patterns=[r'^(?:Let\s+)?(.+?)\s+lead\s+(?:the\s+)?attention\s+while\s+(.+?)\s+and\s+(.+?)\s+remain\s+subordinate\s+but\s+readable[.!?]?$',
                  r'^(.+?)(?:이|가)\s*주의를\s*이끌고\s+(.+?)(?:과|와)\s+(.+?)(?:은|는)\s*(?:그보다\s*)?덜\s*두드러지면서\s*읽을\s*수\s*있게']
        for p in patterns:
            m=re.search(p,value,re.I|re.S)
            if m:return [m.span(i) for i in (1,2,3)]
        return []

    def _attention_positions(self,value):
        # General grammatical constructions, without any scene/entity literals.
        patterns=[
          (r'^(?:Make|Keep)\s+(.+?)\s+(?:the\s+)?first\s+visual\s+read,\s*(.+?)\s+second(?:,?\s+and\s+(.+?)\s+third)?[.!?]?$',(1,2,3)),
          (r'^Read\s+(.+?)\s+first,\s*(.+?)\s+second(?:,?\s+and\s+(.+?)\s+third)?(?:\s+through\s+(?:a\s+)?(?:coherent\s+)?visual\s+hierarchy)?[.!?]?$',(1,2,3)),
          (r'\b(?:attention|viewer.?s?\s+eye|visual\s+read)\s+from\s+(.+?)\s+to\s+(.+?)(?:,?\s+then\s+to\s+(.+?))?[.!?]?$',(1,2,3)),
          (r'\b(?:eye|viewer)\b.{0,45}?\b(?:discover|notice|see|read)\w*\s+(.+?)\s+before\s+(?:noticing|discovering|seeing|reading)\s+(.+?)(?:\s+and\s+(?:only\s+)?later\s+(.+?))?[.!?]?$',(1,2,3)),
          (r'^(?:Let\s+)?(.+?)\s+(?:command|draw|receive|hold|attract)\w*\s+(?:the\s+)?attention\s+first,\s*(.+?)\s+(?:next|second)(?:,?\s+and\s+(.+?)\s+(?:last|third))?[.!?]?$',(1,2,3)),
          (r'^Give\s+(.+?)\s+(?:the\s+)?(?:greatest|greater|primary|strongest)\s+visual\s+prominence,\s*(?:let|make)\s+(.+?)\s+support\s+it(?:,?\s+and\s+keep\s+(.+?)\s+visually\s+subordinate)?[.!?]?$',(1,2,3)),
          (r'\baround\s+(.+?)\s+as\s+(?:the\s+)?dominant\s+read,\s*with\s+(.+?)\s+(?:serving|acting)\s+as\s+(?:a\s+)?(?:quieter\s+)?second\b',(1,2)),
          (r'^Keep\s+(.+?)\s+visually\s+dominant\s+while\s+(.+?)\s+remains?\s+(?:a\s+)?supporting\s+(?:presence|element)',(1,2)),
          (r'^(.+?)에서\s+(.+?)(?:으로|로),?\s*(?:이어|그다음)\s+(.+?)(?:으로|로)\s*(?:주의|시선)',(1,2,3)),
          (r'^(.+?)에\s+가장\s*먼저\s*시선.{0,20}?,\s*(.+?)(?:이|가)\s*그다음,\s*(.+?)(?:이|가)\s*마지막',(1,2,3)),
          (r'^(.+?)(?:을|를)\s*시각적으로\s*(?:가장\s*)?두드러.{0,12}?,\s*(.+?)(?:이|가)\s*이를\s*받치.{0,12}?\s+(.+?)(?:은|는)\s*시각적으로\s*종속',(1,2,3)),
          (r'^(.+?)(?:을|를)\s*먼저\s*발견.{0,12}?,\s*이어\s*(.+?)(?:을|를)\s*알아보.{0,12}?\s+(.+?)(?:은|는)\s*나중',(1,2,3)),
          (r'^(.+?)(?:을|를)\s*지배적인\s*첫\s*시선.{0,35}?삼고\s+(.+?)(?:은|는)\s*더\s*조용한\s*두\s*번째',(1,2)),
          (r'^(?:같은\s*프레임\s*안에서\s*)?(.+?)(?:이|가)\s*시각적으로\s*우세하고\s+(.+?)(?:은|는)\s*이를\s*받치는',(1,2)),
        ]
        for pat,groups in patterns:
            m=re.search(pat,value,re.I|re.S)
            if not m:continue
            spans=[]
            for group in groups:
                if m.start(group)<0:continue
                a,b=m.span(group)
                while a<b and value[a].isspace():a+=1
                while b>a and value[b-1].isspace():b-=1
                if a<b:spans.append((a,b))
            if len(spans)>=2:return spans
        return []

    def _attention_source(self,units,effects):
        if 'composition' not in effects.get('dimensions',[]):return None
        properties=[p for p in effects.get('properties',[]) if p.get('property','').startswith(('composition.hierarchy','layout.hierarchy'))]
        if not properties:return None
        direct=[u for u in units if re.match(r'^/content/(?:en|ko|definition|concept_units/\d+)$',u.get('pointer',''))]
        evidence=[];parameter=False;partial=False
        for u in direct:
            t=self._surface(u['text'])
            # Domain, order and declaration must co-occur within one actual
            # positive field; application instructions cannot donate the fact.
            owned=_LM_has(r'\b(?:owners|nominated\s+owner)\b|대상들|각\s*대상|앞선\s*대상',t)
            declared=_LM_has(r'\b(?:independently\s+declared|already\s+identified|existing\s+visible|declared\s+ordered)\b|독립적으로\s*지정|이미\s*식별',t)
            ordered=_LM_has(r'(?:attention|prominence).{0,110}(?:order|earlier|later|next)|(?:주의|두드러).{0,100}(?:순서|앞선|다음|뒤의)',t)
            grouped=(_LM_has(r'primary.{0,50}visible\s+owner|주된\s*시각\s*대상',t) and _LM_has(r'two\s+or\s+more.{0,45}supporting\s+owners|둘\s*이상의\s*보조\s*대상',t) and _LM_has(r'remain\s+subordinate\s+and\s+readable|덜\s*두드러지면서\s*읽을',t))
            if declared and grouped:evidence.append(u);parameter=True;partial=True
            elif owned and declared and ordered:evidence.append(u);parameter=True
        text='\n'.join(self._surface(u['text']) for u in direct)
        constraints=[u for u in units if u.get('pointer')=='/content/application_contract']
        if parameter:
            # Actual new physical duties cannot be hidden behind the general
            # preservation relation. Enumerated generic owner types and a
            # conditional face example are domains, not concrete extra owners.
            domain_surface=re.sub(r'including\s+(?:existing\s+)?(?:object|person|body[- ]region|interaction|background)(?:\s*(?:,|or|and)\s*(?:object|person|body[- ]region|interaction|background))*\s+owners', 'owner parameter types',text,flags=re.I)
            extra_owners=self._owners(domain_surface)
            extra_method=[]
            if any(d!='composition' for d in effects.get('dimensions',[])):extra_method.append('additional_effect_dimension')
            if any(not p.get('property','').startswith(('composition.hierarchy','layout.hierarchy')) or p.get('target') not in ('whole_image','image','image_plane') for p in effects.get('properties',[])):extra_method.append('additional_effect_or_receiver')
            if _LM_has(r'(?:requires?|must|under)\s+(?:a\s+)?(?:warm|hard|soft|stage)\s+(?:side\s+)?light|warm\s+stage\s+light|(?:무대|측면)\s*조명.{0,20}필수',text):extra_method.append('fixed_lighting')
            if _LM_has(r'\baudience\b|\bthird\s+(?:actor|person)\b|새\s*참가자|세\s*번째\s*인물',text):extra_method.append('additional_participant')
            return {'role':'visual_hierarchy','parameter_order':True,'parameter_partial_order':partial,'evidence':evidence,'source_units':direct,'constraints':constraints,
                    'extra_owner_requirements':extra_owners,'extra_method_requirements':extra_method,
                    'effects':effects,'effects_sha256':_LM_seal(effects),'native_approval':False,
                    'required_source_duties':['declared_partial_order_without_support_order' if partial else 'exact_declared_existing_owner_order','every_nominated_owner_readable','no_added_level_owner_action_cause_or_physical_method'],
                    'whole_source_conditions_effects_cumulative':True}
        # Fixed ordered sources are never treated as generic preservation.
        for u in direct:
            t=self._surface(u['text']);spans=self._attention_positions(t)
            if len(spans)>=2:
                order=[self._attention_key(t[a:b]) for a,b in spans]
                return {'role':'visual_hierarchy','parameter_order':False,'owner_order':order,'evidence':[u],'source_units':direct,'constraints':constraints,'effects':effects,'effects_sha256':_LM_seal(effects),'native_approval':False,'whole_source_conditions_effects_cumulative':True}
        return None
