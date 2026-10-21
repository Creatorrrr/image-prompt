"""Bounded, source-witnessed age/iris/thermal relationship comparison.

Advisory semantics only. No retrieval, IDs, score changes, new owners, or native
qualification. Unrecognized relations and unmet prerequisites stay unproven.
"""
import re


def _hits(text, pattern):
    return [(m.start(), m.end(), m.group()) for m in re.finditer(pattern, text, re.I)]


def _mask(text):
    chars = list(text)
    for m in re.finditer(r'“[^”]*”|"[^"\n]*"|‘[^’]*’', text):
        chars[m.start():m.end()] = ' ' * (m.end()-m.start())
    # Each coordinated predicate owns its negation, not the preceding statement.
    for clause in re.finditer(r'[^.!?;\n]+', ''.join(chars)):
        raw = clause.group(); off = clause.start()
        for m in re.finditer(r'\b(?:without|rather than|instead of|do not|must not|not(?!\s+only)|never|no(?!\s+longer))\b[^.!?;\n]*', raw, re.I):
            stop = re.search(r'\b(?:but|however|yet)\b', m.group(), re.I)
            end = off + m.start() + (stop.start() if stop else len(m.group()))
            chars[off+m.start():end] = ' ' * (end-off-m.start())
        for m in re.finditer(r'(?:하지\s*(?:않|말)|부여하지|추론하지|명시되지|정하지\s*않|미지정|unspecified|unstated)', raw, re.I):
            start = 0
            prefix = raw[:m.start()]
            joins = list(re.finditer(r'(?:하고|하며|하면서|유지하고|유지하며|보존하고|보존하며|으며|이고|이며|지만|말고|,)', prefix))
            if joins: start = joins[-1].end()
            chars[off+start:off+m.end()] = ' ' * (m.end()-start)
    return ''.join(chars)


_VALUES = {'old':r'older[- ]looking|looks? older|\bolder adult\b|elderly|나이\s*들어\s*보|노인처럼',
           'youth':r'youthful(?:[- ]looking)?|younger[- ]looking|young[- ]looking|젊어\s*보|젊게',
           'middle':r'middle[- ]aged(?:[- ]looking| appearance)?|중년'}
_REGIONS = {'face':r'\bface\b|\bfacial\b|얼굴', 'hands':r'\bhands?\b|back.of.hand|손등|양손|두\s*손|(?<![가-힣])손(?:이|을|과|은|의|에|\s|$)'}
_COLOR = {'blue':r'blue|파란|파랑|푸른|파란색', 'brown':r'brown|갈색|브라운',
          'gray':r'gr[ae]y|회색', 'green':r'(?:moss[- ]|olive[- ]?)?green|녹색|초록|이끼빛',
          'olive':r'olive|올리브', 'amber':r'amber|호박색'}
_EYE_PROPERTIES = {
 'radial':r'radial (?:streak|texture|pattern|fibers?|fibres?)|(?:uneven|fine).{0,25}streaks?.{0,35}(?:outward|pupil)|방사형\s*(?:무늬|줄무늬|질감)|줄무늬.{0,35}바깥쪽으로',
 'annulus':r'inner annular (?:outline|structure)|inner ring|안쪽 고리 윤곽',
 'limbal':r'limbal|(?:dark|darker) outer iris (?:margin|edge)|darker outer margin|(?:thin|narrow).{0,25}(?:dark )?(?:outline|border).{0,75}(?:outer|iris meets|iris.{0,20}white)|dark perimeter.{0,65}(?:eye white|흰자)|(?:iris|홍채).{0,35}(?:흰자|white).{0,35}(?:테두리|border)|가는.{0,20}윤곽.{0,35}바깥',
 'pupil':r'\bround\b.{0,20}(?:dark|black)?\s*pupil|둥[근글].{0,16}동공',
 'pupil_boundary':r'(?:bounded|distinct|separate).{0,30}(?:pupil|opening)|pupil.{0,40}(?:distinct|separate (?:central )?opening|boundary)|또렷한\s*동공\s*경계|구별되는.{0,20}동공|동공.{0,30}별도',
 'central':r'(?:color|amber|colored).{0,35}ring.{0,35}(?:around|hugs|pupil)|동공.{0,25}(?:색\s*고리|호박색\s*고리)|inner iris ring',
 'bilateral':r'one iris.{0,100}(?:other|opposite) iris|left iris.{0,55}right iris|왼쪽\s*홍채.{0,35}오른쪽\s*홍채|한쪽.{0,40}반대쪽.{0,15}홍채',
 'sectoral':r'(?:bounded\s+)?wedge of colou?r.{0,70}(?:part of|within) (?:one |the same )?iris|sectoral colou?r.{0,35}iris|홍채.{0,25}부채꼴\s*색',
 'concentric':r'(?:two or more|several|multiple).{0,20}(?:circular bands|iris rings).{0,35}(?:share|same).{0,20}(?:iris )?cent(?:er|re)|concentric iris rings|여러\s*원형\s*띠.{0,30}홍채\s*중심',
 'sclera':r'(?:visible )?scleral band.{0,35}(?:iris|lower lid)|lateral sclera.{0,35}(?:both sides|iris)|흰자위.{0,35}(?:아랫눈꺼풀|측면)|홍채.{0,30}양쪽\s*측면.{0,20}흰자위',
 'flecks':r'pigment flecks|pigment.{0,15}marks|색소\s*반점',
 'crypt':r'crypt|irregular hollows|불규칙한\s*오목',
 'collarette':r'collarette|칼라레트',
 'furrows':r'contraction furrows|curved grooves|수축\s*주름',
}
_PROP_MAP = [('inner_annular_outline','annulus'),('radial_texture','radial'),('limbal_border','limbal'),('pupil_shape','pupil'),
             ('pupil_iris_boundary','pupil_boundary'),('pigment_flecks','flecks'),('crypt_texture','crypt'),
             ('collarette','collarette'),('peripheral_furrows','furrows'),('iris_ring_topology','concentric'),('sclera_exposure','sclera')]
_IRIS_ASSERTION = r'(?:iris|irises|pupil|sclera).{0,70}(?:has|have|carries|carry|retains?|remains?|forms?|occupies|bounded|surface|texture|structure)|(?:bounded|visible|existing|declared|separate|artificial|replacement).{0,35}(?:iris|pupil|sclera)|(?:bands?|rings?|wedges?|hollows?).{0,70}(?:iris|pupil)|(?:홍채|동공|흰자위).{0,50}(?:있|보인|남|유지|경계|구조|질감)'
_THERMAL = {'cold':r'physically cold|physical coldness|explicitly (?:cold|chilled)|차갑|차가움|냉각된',
 'hot':r'physically hot|hot physical temperature|declared hot|물리적으로\s*뜨거|뜨겁|뜨거운',
 'warm':r'physically warm|warm physical temperature|(?:declared|stated).{0,25}warm temperature|\bwarm temperature state\b|물리적으로\s*따뜻',
 'frozen':r'(?:declared|explicitly).{0,25}frozen(?: temperature| physical)? state|frozen physical state|frozen solid|frozen water sample',
 'ambient':r'room[- ]temperature|at room temperature|same physical temperature as.{0,40}room|실온|주변 실내와 같은 물리적 온도',
 'warming':r'getting warmer|\bwarming\b|temperature (?:is )?(?:rising|increasing)|온도.{0,8}(?:올라|상승)|데워',
 'cooling':r'losing heat|\bcooling\b|temperature (?:is )?(?:falling|decreasing)|온도.{0,8}(?:내려|하강)|식고|식어|열을 잃'}
_TEMP = r'(?<![\w.])([+-]?(?:\d+(?:\.\d+)?|\.\d+))\s*(°\s*[CF]|℃|℉|kelvins?|K)(?![A-Za-z])'


class Semantic:
    def __init__(self, masker=None):
        self.masker = masker

    def _positive(self, text):
        # The caller's masker may add exclusions; both surfaces preserve offsets.
        own = _mask(text)
        if self.masker is None: return own
        other = self.masker(text)
        if not isinstance(other, str) or len(other) != len(text):
            raise ValueError('positive masker must preserve Unicode offsets')
        # Never resurrect a caller-excluded assertion. The native local mask
        # additionally prevents quoted/negative material becoming source facts.
        return ''.join(' ' if a.isspace() or b.isspace() else a
                       for a,b in zip(own,other))

    def request(self, role, text):
        if role not in ('age_presentation','eye_detail','thermal_state'): return None
        m = re.search(r'^Photographic role:\s*(.*?)(?=\nScene context:|\Z)',text,re.S)
        focus = m.group(1) if m else text
        desc = self._describe(role, self._positive(focus), self._positive(text), source=False)
        if desc is None: return None
        desc.update(role=role, asserts=True, origin='request', raw_text=text,
                    witnesses=[{'pointer':'/request','start':a,'end':b,'quote':v}
                               for a,b,v in self._witnesses(role,text)])
        return desc

    def source(self, role, units, effects):
        if role not in ('age_presentation','eye_detail','thermal_state'): return None
        units = list(units)
        usable=[u for u in units if isinstance(u.get('text'),str) and u.get('pointer','').startswith('/content/')]
        body=[u for u in usable if u['pointer']=='/content/en']
        if not body: body=[u for u in usable if u['pointer']!='/content/application_contract']
        text='\n'.join(self._positive(u['text']) for u in body)
        full='\n'.join(self._positive(u['text']) for u in usable)
        desc=self._describe(role,text,full,source=True,effects=effects)
        if desc is None:return None
        witnesses=[]
        for u in usable:
            for a,b,v in self._witnesses(role,u['text']):
                witnesses.append({**u,'start':a,'end':b,'quote':v})
        desc.update(role=role,origin='source',witnesses=witnesses,
                    evidence=[u for u in usable if u['pointer']!='/content/application_contract'],primary_units=usable,effects=effects,application_contracts=[u for u in usable if u['pointer']=='/content/application_contract'],
                    native_approval=False,guard_obligations_retained=True)
        return desc

    def _witnesses(self,role,text):
        positive=self._positive(text)
        patterns = list(_VALUES.values())+list(_REGIONS.values())+[r'chronological.age|실제\s*연령|(?:declared|명시된|선언된).{0,45}(?:age|year.old|세)'] if role=='age_presentation' else list(_EYE_PROPERTIES.values())+list(_COLOR.values())+[_IRIS_ASSERTION] if role=='eye_detail' else list(_THERMAL.values())+[_TEMP,r'(?:retain|preserv)\w*.{0,110}temperature.{0,30}(?:value|number).{0,30}unit',r'온도.{0,20}수치.{0,20}단위']
        return sorted(set((a,b,text[a:b]) for pat in patterns for a,b,_ in _hits(positive,pat)
                          if all(positive[i]==text[i] for i in range(a,b))))

    def _describe(self,role,focus,full,source=False,effects=None):
        if role=='age_presentation':return self._age(focus,full,source)
        if role=='eye_detail':return self._eye(focus,full,source,effects or {})
        return self._thermal(focus,full,source)

    @staticmethod
    def _age(text,full,source):
        synthetic=bool(re.search(r'synthetic|android|안드로이드|합성',full,re.I))
        depicted=bool(re.search(r'framed portrait|depicted elder|액자.{0,20}(?:노인|묘사)|묘사된\s*노인',text,re.I))
        domain='synthetic' if synthetic else 'depicted' if depicted else 'human'
        adult=bool(re.search(r'\badult\b|성인',full,re.I)) and not synthetic
        count=2 if re.search(r'\btwo\b.{0,40}\badults\b|\btwo adult|두\s*(?:명의?\s*)?성인|성인.{0,30}둘',full,re.I) else 1
        vals={k:_hits(text,p) for k,p in _VALUES.items()};regions={k:_hits(text,p) for k,p in _REGIONS.items()}
        rel=[]
        # Whole-person assignment is distinct from local face/hand inventory.
        if count==2 and vals['old'] and vals['youth'] and not regions['face'] and not regions['hands']:
            rel=[('first','whole','old','one'),('second','whole','youth','one')]
        else:
            for region,locs in regions.items():
                for a,b,_ in locs:
                    separators=list(re.finditer(r'[.;\n]|\b(?:while|whereas|but)\b',text,re.I))
                    boundary=max([z.end() for z in separators if z.end()<=a] or [0])
                    end=min([z.start() for z in separators if z.start()>=b] or [len(text)])
                    options=[(min(abs(a-y),abs(x-b)),k,x,y) for k,hits in vals.items() for x,y,_ in hits if boundary<=x<end]
                    if not options:continue
                    preceding=[o for o in options if o[3]<=a and a-o[3]<30]
                    distance,value,x,y=min(preceding or options)
                    if distance>110:continue
                    segment=text[max(boundary,a-55):min(end,b+55)]
                    quant='both' if region=='hands' and re.search(r'both|each hand|양손|두\s*손',segment,re.I) else 'inventory' if region=='hands' and re.search(r'\bhands\b|손들',segment,re.I) else 'inventory' if region=='hands' and re.search(r'[가-힣]',segment) and not re.search(r'한 손|선택된',segment) else 'one'
                    if region=='hands' and re.search(r'both hands|양손|두 손',full,re.I): quant='both'
                    rel.append(('self',region,value,quant))
        rel=sorted(set(rel))
        number_words=set('zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred'.split())
        chrono_preserve=bool(re.search(r'chronological.age|실제\s*연령',full,re.I) and re.search(r'preserv|retain|유지|보존',full,re.I)) if source else False
        # Explicit declarations only. Values remain literal, including words.
        chrono=[]
        for pat in [r'(?:declared|stated|supplied).{0,35}age (?:of )?([a-z]+(?:-[a-z]+)?|\d+)',r'(?:declared|stated|supplied|independently declared)\s+([a-z]+(?:-[a-z]+)?|\d+)[- ]year[- ]old',r'(?:declared adult age of|adult age of)\s+([a-z]+(?:-[a-z]+)?|\d+)',r'(?:선언된|명시된|성인)\s*(\d+)\s*세']:
            chrono += [m.group(1) for m in re.finditer(pat,text,re.I) if m.group(1).isdigit() or all(w in number_words for w in m.group(1).lower().split('-'))]
        only=chrono_preserve and not rel if source else bool(chrono) and not rel
        if not rel and not only:return None
        return dict(domain=domain,adult=adult,owner_count=count,relations=rel,chronological_values=sorted(set(chrono)),chronological_preservation=chrono_preserve,declaration_only=only,
                    preserved_regions=sorted(k for k,p in _REGIONS.items() if re.search(r'(?:preserv\w*|retain\w*).{0,65}(?:'+p+r').{0,15}appearance',text,re.I)),regions_present=sorted(k for k,p in _REGIONS.items() if re.search(p,full,re.I)),hands_outside=bool(re.search(r'hands outside|hands out of|손.{0,10}화면 밖',full,re.I)),owner_assignment_preservation=count==2)

    @staticmethod
    def _eye(text,full,source,effects):
        domain='printed' if re.search(r'print\w*.{0,70}(?:chart|diagram)|(?:chart|diagram).{0,70}print|도표.{0,25}인쇄|인쇄.{0,25}도표',text,re.I) else 'physical'
        anatomical_head=bool(re.search(r'\b(?:iris|irises|pupil|sclera|scleral|limbal|collarette)\b|\b(?:human|actual|existing|declared|same) eyes?\b|홍채|동공|흰자위|칼라레트',text,re.I))
        if source and not anatomical_head:return None
        props={k for k,p in _EYE_PROPERTIES.items() if re.search(p,text,re.I)}
        if 'annulus' in props and not re.search(r'selected color.{0,40}ring|ring.{0,55}different.{0,20}color|color.{0,25}ring.{0,25}pupil',text,re.I):props.discard('central')
        elif 'central' in props:props.discard('annulus')
        mutation=set()
        unwitnessed_effects=[]
        for e in effects.get('properties',[]):
            prop=e.get('property','')
            # Effect metadata is only a family hint. A primary affirmative
            # assertion must independently witness every modeled mutation.
            for suffix,k in _PROP_MAP:
                if suffix in prop:
                    if k in props:mutation.add(k)
                    else:unwitnessed_effects.append(prop)
            if source and re.search(r'(?:^|\.)eyes\.',prop):
                mapped=any(suffix in prop for suffix,_ in _PROP_MAP)
                color_distribution='iris_color_distribution' in prop and bool(props & {'sectoral','central','bilateral'})
                fixed_color='iris.color' in prop and bool(re.search(r'iris|irises|홍채',text,re.I)) and bool(re.search('|'.join(_COLOR.values()),text,re.I))
                if not(mapped or color_distribution or fixed_color):
                    unwitnessed_effects.append(prop)
        # Footprints choose the actual asserted property, never its neighboring
        # mention (crypts mention radial texture; furrows mention an outer edge).
        if source and mutation:
            props = mutation | ({'pupil_boundary'} if 'radial' in mutation and re.search(r'pupil.{0,40}separate|separate opening',text,re.I) else set())
        if source and not mutation:mutation=set(props)
        colors=[]
        for color,pat in _COLOR.items():
            for a,b,_ in _hits(text,pat):
                clause=text[max(0,a-35):min(len(text),b+55)]
                if re.search(r'(?:pigment|fleck|色素|색소|반점)',clause,re.I):continue
                sides=[(abs(a-y),name) for name,rx in [('left',r'left iris|왼쪽\s*홍채'),('right',r'right iris|오른쪽\s*홍채')] for x,y,_ in _hits(text,rx) if y<=a+5 and a-y<45]
                side=min(sides)[1] if sides else 'both'
                zonehits=[(min(abs(a-y),abs(x-b)),name) for name,rx in [('inner',r'ring|고리|inner'),('outer',r'outer iris|바깥쪽|outer part|올리브색')] for x,y,_ in _hits(text,rx) if min(abs(a-y),abs(x-b))<40]
                zone=min(zonehits)[1] if zonehits else 'base'
                if re.match(r'[- ]*(?:iris|irises|홍채)',text[b:],re.I):zone='base'
                colors.append((side,zone,color))
        colors=sorted(set(colors))
        variable=bool(re.search(r'selected color|선택한.{0,5}색|first selected color',full,re.I))
        existing=bool(re.search(r'(?:established|existing) iris colou?r|iris.{0,40}base colou?r.{0,20}(?:visible|preserv)|기존\s*홍채\s*색|홍채\s*바탕색',full,re.I))
        if not props and not source:return None
        anatomical=bool(re.search(_IRIS_ASSERTION,text,re.I))
        # Unknown iris anatomy still has a witnessed physical/depicted owner.
        # Compile it for exclusion/owner checks, but never claim modeled fit.
        unmodeled=source and anatomical and not props
        if source and not props and not anatomical:return None
        if not props and not colors and not unmodeled:return None
        return dict(domain=domain,properties=sorted(props),mutations=sorted(mutation),colors=colors,variable_colors=variable,existing_color_preservation=existing,
                    unmodeled_properties=bool(unmodeled),unwitnessed_effects=sorted(set(unwitnessed_effects)),
                    human_present=bool(re.search(r'\bhuman\b|\badult\b|\bsitter\b|성인|사람|인물',full,re.I)),both_eyes=bool(re.search(r'both|each|양쪽|양안',text,re.I)),unchanged=bool(re.search(r'unchanged|no request to develop|no.{0,15}local iris|외양은 유지|외양은\s*유지|구조를 더할 요청이 없는',full,re.I)),human_required=source and bool(re.search(r'human|사람|피사체',full,re.I)))

    @staticmethod
    def _thermal(text,full,source):
        state_text=re.sub(r'cooling history|cooling after|냉각 이력', ' ', text, flags=re.I)
        states=sorted(k for k,p in _THERMAL.items() if re.search(p,state_text,re.I))
        values=sorted(set((m.group(1),re.sub(r'\s+','',m.group(2))) for m in re.finditer(_TEMP,text,re.I)))
        preserve=source and bool(re.search(r'temperature.{0,35}(?:value|number).{0,25}unit|온도.{0,15}수치.{0,15}단위',full,re.I) and re.search(r'retain|preserv|유지|보존',full,re.I) and re.search(r'supplied|declared|선언|제시',full,re.I))
        if not states and not values and not preserve:return None
        classes=[]
        for kind,pat in {'utensil':r'spoon|utensil|숟가락|식기','ceramic':r'ceramic|도자기','liquid':r'\bwater\b|\bliquid\b|물의|물은|물을|물이|물속|액체|그릇 속 물','solid':r'solid|stone|slab|tile|brick|glass tumbler|고체|벽돌|석판|타일|유리 텀블러'}.items():
            if re.search(pat,text,re.I):classes.append(kind)
        phase='solid' if 'frozen' in states else 'liquid' if 'liquid' in classes else 'solid' if any(k in classes for k in ['solid','utensil','ceramic']) else None
        return dict(states=states,temperatures=values,numeric_preservation=bool(preserve),carrier_classes=classes,phase=phase,
                    region=bool(re.search(r'local region|identified region|central patch|국소\s*구역|특정\s*구역',text,re.I)),
                    refrigeration=bool(re.search(r'refrigerat\w*|fridge|냉장',full,re.I)),generic_carrier=source and bool(re.search(r'identified physical carrier|existing solid object|식별된 물리적',text,re.I)))

    def fit(self,req,src):
        if not req or not src or req.get('role')!=src.get('role'):return 'unproven'
        role=req['role']
        if role=='age_presentation':return self._fit_age(req,src)
        if role=='eye_detail':return self._fit_eye(req,src)
        return self._fit_thermal(req,src)

    @staticmethod
    def _fit_age(req,src):
        if req['domain']!=src['domain']:return 'conflicting'
        if src['adult'] and not req['adult']:return 'unproven'
        if src['owner_count']!=req['owner_count']:return 'conflicting'
        if src['declaration_only']:
            return 'supported' if req['chronological_values'] and not req['relations'] else 'unproven'
        if not req['relations'] or not src['relations']:return 'unproven'
        if src['relations']!=req['relations']:
            # A plural independently established set can match the same known
            # inventory, but never collapse an explicit both-hands source to one.
            norm=lambda rs:{(a,b,c,'inventory' if d=='inventory' else d) for a,b,c,d in rs}
            return 'conflicting' if {(a,b,c) for a,b,c,d in src['relations']}!={(a,b,c) for a,b,c,d in req['relations']} else 'unproven'
        if req['hands_outside'] and any(r[1]=='hands' for r in src['relations']):return 'conflicting'
        return 'supported'

    @staticmethod
    def _fit_eye(req,src):
        if req['domain']!=src['domain']:return 'conflicting'
        if src.get('unmodeled_properties') or src.get('unwitnessed_effects'):return 'unproven'
        if src['human_required'] and not req.get('human_present'):return 'unproven'
        wanted=set(req['properties']);found=set(src['properties']);mut=set(src['mutations'])
        if req['unchanged'] and mut:return 'conflicting'
        if not wanted:return 'unproven'
        if not wanted <= found:return 'unproven'
        if mut-wanted:return 'unproven'
        reqcolors={c for _,_,c in req['colors']};srccolors={c for _,_,c in src['colors']}
        if srccolors and reqcolors and not srccolors <= reqcolors:return 'conflicting'
        if src['colors'] and req['colors'] and not src['variable_colors'] and set(src['colors'])!=set(req['colors']):return 'conflicting'
        if wanted & {'central','bilateral'}:
            return 'supported' if src['variable_colors'] and len(reqcolors)>=2 else 'unproven'
        if src['colors'] and req['colors'] and set(src['colors'])!=set(req['colors']):return 'conflicting'
        return 'supported'

    @staticmethod
    def _fit_thermal(req,src):
        if src['temperatures'] and src['temperatures']!=req['temperatures']:return 'conflicting'
        if src['numeric_preservation'] and not req['temperatures']:return 'unproven'
        if req['temperatures'] and not(src['numeric_preservation'] or req['temperatures']==src['temperatures']):return 'unproven'
        if src['phase'] and req['phase'] and src['phase']!=req['phase']:return 'conflicting'
        if src['region']!=req['region']:return 'conflicting'
        if src['refrigeration'] and not req['refrigeration']:return 'unproven'
        if set(src['states'])!=set(req['states']):return 'unproven'
        if not req['carrier_classes']:return 'unproven'
        if not src['generic_carrier']:
            specifics=set(src['carrier_classes'])-{'solid'}
            if specifics and not specifics<=set(req['carrier_classes']):return 'conflicting'
        return 'supported'
