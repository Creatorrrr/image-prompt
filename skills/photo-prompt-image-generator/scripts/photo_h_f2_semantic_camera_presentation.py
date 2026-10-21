"""Bounded candidate-free personal-appearance focus helpers for manual integration.
No IDs, retrieval slots, ranks or benchmark strings are runtime inputs/rules.
This is a semantic discovery proposal, never native owner/effect permission.
"""
import re

STYLE_PATTERNS = {
    'finished': r'polished|meticulous\w*|put[- ]together|tidy|neatly|neat(?:ly)?\s+groomed|carefully finished|prepared.{0,20}orderly|orderly.{0,20}(?:finish|appearance|presentation)|세심|단정|정돈|말끔|세련',
    'casual': r'informal|casual\w*|relaxed|easy|everyday|loose|lived[- ]in|uncontrived|unstyled|편안|편하고|느긋|일상|느슨|생활감|수수|꾸미지',
    'unstyled': r'unstyled|uncontrived|unpolished|lived[- ]in|loosely separated|꾸미지\s*않은|수수|성기게\s*나뉜|생활감',
    'decorative': r'ornate|elaborate|decorative|dense.{0,25}decoration|repeated ornament|화려|장식적|반복\s*장식|밀도\s*있는.{0,15}장식',
    'understated': r'understated|restrained|unobtrusive|discreet|low\s+in\s+saturation|low[- ]saturation|plain outfit|절제|담백|차분|낮은\s*채도|단순한\s*옷차림',
    'formal': r'formal|pressed jacket|격식|정장|다림질된\s*재킷',
}
STYLE_RX = {k: re.compile(r'(?<![a-z])(?:'+v+r')(?![a-z])', re.I) for k,v in STYLE_PATTERNS.items()}
SCOPE_RX = re.compile(r'presentation|appearance|grooming|styling|(?:overall|entire).{0,25}look|그루밍|몸단장|외적\s*연출|외양|전체.{0,18}차림|옷차림', re.I)
HAIR_RX = re.compile(r'\bhair\b|\bgrooming\b|\bcurls?\b|머리|헤어|그루밍|몸단장', re.I)
ATTIRE_RX = re.compile(r'\b(?:attire|clothes|clothing|garment|outfit|jacket|shirt|trousers|scarf)\b|knitted top|의복|옷차림|재킷|셔츠|바지|니트|스카프', re.I)
SAME_OWNER_RX = re.compile(r"same (?:existing )?(?:adult )?(?:wearer|person|human)|wearer(?:'s| has)|same person's|같은\s*(?:성인\s*)?착용자|착용자는|착용자의", re.I)
SYNTHETIC_RX = re.compile(r'\b(?:mannequin|android|display dummy)\b|마네킹|안드로이드', re.I)
LOCK_RX = re.compile(r'(?:preserv\w*|keep|retain|maintain).{0,80}(?:existing|current|unchanged|all other)|(?:existing|current).{0,80}(?:unchanged|preserv\w*)|기존.{0,80}(?:유지|보존)', re.I)
NAMED_PRIMARY_RX = re.compile(r'^/content/(?:en|ko|definition|phrase_en|phrase_ko)$|^/content/(?:concept_units/\d+|paraphrases/\d+|semantics/definition)$')
CONSTRAINT_PRIMARY_RX = re.compile(r'^/content/(?:application_contract|authored_components/obligations/\d+/instruction)$')


def mask_quoted(text):
    # Apostrophes in possessives are not quotation delimiters.
    return re.sub(r'“[^”]*”|“[^”]*$|"[^"\n]*"|‘[^’]*’|`[^`]*`', lambda m: ' '*len(m.group()), text)


def clauses(text):
    text = mask_quoted(text)
    return [s.strip() for s in re.split(r'[.;\n]|\bwithout\s+(?=(?:inferring|assigning|implying)\b)|유지하고|유지하며|보존하고', text, flags=re.I) if s.strip()]


def negative_clause(text):
    # Do not misread the affirmative adjective '꾸미지 않은' as an instruction.
    return bool(re.search(r'\b(?:do not|never|without|exclude|not to)\b|(?:부여|연출|변경|만들|지정).{0,10}하지\s*않|부여하지\s*않', text, re.I))


def style_facets(text):
    positive=set();excluded=set()
    for k,rx in STYLE_RX.items():
        for m in rx.finditer(text):
            if re.match(r'\s*(?:(?:은|는|이|가|을|를)\s*)?(?:없이|아닌|아니라)',text[m.end():]):
                excluded.add(k)
            else:positive.add(k)
    return positive,excluded


def request_contract(text):
    focus = re.sub(r'^Photographic role:\s*', '', text.split('\nScene context:',1)[0])
    if re.search(r'only.{0,45}(?:jacket|blazer|one garment)|(?:재킷|블레이저|의복\s*하나)만',focus,re.I) and re.search(r'preserv|retain|유지|보존',focus,re.I):
        return None
    accepted=[];excluded=set()
    for clause in clauses(focus):
        if LOCK_RX.search(clause):
            continue
        fs,local_excluded=style_facets(clause)
        excluded.update(local_excluded)
        if negative_clause(clause):
            excluded.update(fs);continue
        if fs and (SCOPE_RX.search(clause) or (HAIR_RX.search(clause) and ATTIRE_RX.search(clause)) or (SYNTHETIC_RX.search(clause) and '연출' in clause)):
            accepted.append((clause,fs))
    if not accepted:
        return None
    kinds={'synthetic' if SYNTHETIC_RX.search(c) else 'human' for c,_ in accepted}
    if len(kinds)!=1:
        return {'state':'review_required','reason':'ambiguous mutation owner'}
    return {'state':'asserted_change','owner_kind':next(iter(kinds)),
            'facets':sorted(set().union(*(fs for _,fs in accepted))),
            'excluded_facets':sorted(excluded),'clauses':[c for c,_ in accepted]}


def compile_contract(primary_units, effects, conditions):
    # Effects are only a routing prerequisite. Full primary assertions are the proof.
    properties=effects.get('properties',[])
    routed=[x for x in properties if x.get('property','').startswith(('presentation.','appearance.presentation'))]
    if not routed:return None
    buckets={name for name in ('grooming','attire','coordination') if any(name in x['property'].split('.') for x in routed)}
    if buckets != {'grooming','attire','coordination'}:return None
    if {x.get('target') for x in properties} != {'main_subject'}:
        return {'state':'review_required','reason':'unresolved complete effect receiver scope','whole_effects':effects}
    semantic=[u for u in primary_units if NAMED_PRIMARY_RX.search(u['pointer'])]
    complete=[u for u in semantic if HAIR_RX.search(u['text']) and ATTIRE_RX.search(u['text']) and SAME_OWNER_RX.search(u['text'])]
    if not complete:return None
    facets={k:[] for k in STYLE_RX}
    for unit in complete:
        positive=mask_quoted(unit['text'])
        # Negated source style is a constraint, never affirmative style proof.
        # Bound the English negative scope at a sentence or affirmative 'but'.
        positive=re.sub(r'\b(?:without|no|not|never|excluding)\b[^.;\n]*?(?=\bbut\b|[.;\n]|$)',lambda m:' '*len(m.group()),positive,flags=re.I)
        for k,rx in STYLE_RX.items():
            facets[k].extend({'pointer':unit['pointer'],'quote':m.group(),'start':m.start(),'end':m.end()} for m in rx.finditer(positive) if not re.match(r'\s*(?:(?:은|는|이|가|을|를)\s*)?(?:없이|아닌|아니라)',positive[m.end():]))
    constraints=[u for u in primary_units if CONSTRAINT_PRIMARY_RX.search(u['pointer'])]
    return {'state':'source_witnessed','owner_kind':'human','facets':{k:v for k,v in facets.items() if v},
            'whole_primary_units':primary_units,'constraints':constraints,'conditions':conditions,
            'whole_effects':effects,'intrinsic_body_parts_are_owned_not_extra_participants':True,
            'parameter_preservation':False,'native_approval':False}


def compare(req, source):
    if not req:return {'decision':'no_full_presentation_change'}
    if not source or source.get('state')!='source_witnessed':return {'decision':'unproven'}
    if req.get('owner_kind')!=source.get('owner_kind'):return {'decision':'conflict','reason':'mutation owner differs'}
    wanted=set(req['facets']);found=set(source['facets']);excluded=set(req.get('excluded_facets',[]))
    if excluded & found:return {'decision':'conflict','reason':'explicitly excluded style facet','facets':sorted(excluded&found)}
    if 'unstyled' in wanted and 'finished' in found and 'unstyled' not in found:
        return {'decision':'conflict','reason':'prepared finish conflicts with unstyled request'}
    if 'finished' in wanted and 'unstyled' in found:
        return {'decision':'conflict','reason':'loose lived-in arrangement does not supply meticulous finish'}
    if 'formal' in wanted and 'casual' in found and 'formal' not in found:
        return {'decision':'conflict','reason':'informal-only complete attire conflicts with formal request'}
    if 'decorative' in wanted and 'decorative' not in found:return {'decision':'unproven','reason':'no complete ornamental presentation witness'}
    if 'understated' in wanted and 'decorative' in found:return {'decision':'conflict','reason':'dense ornament conflicts with understated request'}
    # No generic preserve-word bypass for a fixed style. Every wanted facet needs evidence.
    if wanted-found:return {'decision':'unproven','missing_facets':sorted(wanted-found)}
    return {'decision':'semantic_support_only','whole_source_review_required':True,'native_approval':False}


_CAM_CAPTURE = re.compile(r'(?:taking|capture|photographing) camera|camera (?:making|taking|that makes) (?:this|the) photograph|camera.{0,18}photographing|(?:optical|viewing) axis|촬영\s*카메라|(?:사진|이미지)을\s*찍는\s*카메라|이를\s*촬영하는\s*카메라|관찰축|광축',re.I)
_CAM_DEPICTED = re.compile(r'security camera|surveillance camera|CCTV|camera (?:visible|depicted|inside)|보안\s*카메라|장면\s*속.{0,15}카메라',re.I)
_CAM_BODY = re.compile(r'\b(?:body|head|sitter|subject)\b.{0,35}(?:turn|pitch|pose|lean)|인물.{0,25}(?:몸|자세)|고개|머리.{0,18}기울',re.I)
_CAM_ARCH = re.compile(r'(?:look|view).{0,30}(?:across|oblique).{0,40}(?:building|corner)|건물.{0,30}(?:사선|모서리).{0,25}(?:바라|관찰)|(?:모서리|외벽).{0,30}비껴',re.I)
_CAM_NAMED = re.compile(r'^/content/(?:en|ko|definition|phrase_en|phrase_ko)$|^/content/(?:concept_units/\d+|paraphrases/\d+|semantics/definition)$')
_CAM_CONSTRAINT = re.compile(r'^/content/(?:application_contract|authored_components/obligations/\d+/instruction)$')


def _cam_clauses(text):
    return [m for m in re.finditer(r'[^.;\n]+',text) if m.group().strip()]


def _cam_is_capture(raw):
    if re.search(r'camera\s+height|카메라\s*높이',raw,re.I) and not re.search(r'(?:optical|viewing)\s+axis|camera\s+viewing\s+direction|camera.{0,22}(?:points?|looks?|aims?|faces?|is rolled)|카메라.{0,18}(?:광축|관찰축|향한다|바라본다|내려다본다|올려다본다)',raw,re.I):return False
    if _CAM_DEPICTED.search(raw) and not _CAM_CAPTURE.search(raw):return False
    if _CAM_BODY.search(raw) and not _CAM_CAPTURE.search(raw):return False
    return bool(_CAM_CAPTURE.search(raw) or _CAM_ARCH.search(raw) or re.search(r'\bcamera\b|카메라',raw,re.I))


def _cam_features(text):
    """Return independent parameter axes; reference horizontal/level is not a value."""
    axes={}
    def put(axis,value,pattern):
        m=re.search(pattern,text,re.I)
        if m:axes[axis]={'value':value,'start':m.start(),'end':m.end(),'quote':m.group()}
    put('pitch','down',r'\bdown(?:ward)?\b|descend\w*|(?:아래로|내려다|내려가|하향)')
    put('pitch','up',r'\bupward\b|rises? above the horizontal|(?:위로\s*향|위를\s*향|상향)|위로.{0,20}(?:바라|향)')
    put('pitch','level',r'(?:optical|viewing) axis\s+(?:(?:is|stays|remains)\s+)?horizontal|(?:level|horizontal)\s+(?:optical|viewing)\s+axis|(?:pointed|points?)\s+horizontally|(?:광축|관찰축)(?:은|는|이|을)?\s*수평(?:이고|으로|인|을|이다|이며|$)|(?:카메라|광축|관찰축).{0,12}수평\s*방향|수평인\s*관찰축')
    put('pitch','vertical_down',r'(?:axis|camera).{0,30}(?:nearly\s+)?vertical(?:ly)?\s+down|strict top[- ]down|top[- ]down flat|directly overhead camera|수직\s*(?:하향|탑다운|아래로|아래)|수직으로\s*향|정수직\s*부감')
    put('pitch_geometry','nonvertical',r'(?:diagonal(?:ly)?|obliquely)\s+down(?:ward)?|non[- ]vertical|intermediate inclination|shallow descending|small oblique component|비스듬히\s*아래로|완만하게\s*아래로|중간\s*기울기|작은\s*사선\s*성분')
    put('surface_visibility','top_and_near_side',r'(?:top(?:\s+(?:surfaces?|faces?|planes?))?|upper\s+(?:surfaces?|faces?)|their\s+tops).{0,100}(?:front\s+(?:faces?|planes?)|near[- ]facing\s+(?:sides?|front\s+faces?))|(?:object\s+fronts).{0,100}(?:upper\s+faces)|윗면.{0,40}(?:앞면|옆면)|앞면.{0,80}윗면')
    put('pitch','level',r'level\s+(?:oblique\s+)?(?:camera\s+)?viewing\s+(?:direction|axis)|horizontal\s+pitch')
    put('yaw','front',r'faces?.{0,65}squarely|straight\s+(?:toward|at|ahead)|frontal yaw|정면.{0,20}곧바로|곧바로.{0,20}(?:정면|마주)|똑바로.{0,12}앞')
    put('yaw','oblique',r'(?:look|looks|looking|view|viewing|directed).{0,55}(?:across|obliquely).{0,45}corner|(?:level|horizontal) oblique (?:camera )?(?:view|viewing direction)|(?:building|facade).{0,35}three[- ]quarter\s+direction|건물.{0,30}사선\s*방향|모서리.{0,35}(?:비껴|사선)|수평\s*사선\s*시점')
    put('roll','level',r'(?:frame\s+)?roll\s+(?:(?:is|stays|remains)\s+)?level|level\s+roll|(?:프레임의?\s*)?롤(?:도|은|을)?\s*수평|좌우\s*기울기(?:는|를)?\s*수평')
    put('roll','tilted',r'\broll(?:ed|s|ing)?\b.{0,35}(?:clockwise|counterclockwise|tilt|rotat)|camera\s+roll\s+(?:tilts?|rotates?)|dutch\s*(?:angle|tilt)|카메라.{0,35}시계\s*방향.{0,18}회전|카메라\s*롤.{0,30}기울')
    put('roll_sign','clockwise',r'(?<!counter)\bclockwise\b|(?<!반)시계\s*방향')
    put('roll_sign','counterclockwise',r'counterclockwise|counter[- ]clockwise|반시계\s*방향')
    if 'roll_sign' in axes and re.search(r'camera|roll|카메라|회전',text,re.I):
        axes.setdefault('roll',{'value':'tilted',**{k:v for k,v in axes['roll_sign'].items() if k!='value'}})
    put('route','shoulder',r'(?:viewing\s+axis|camera).{0,80}(?:past|beyond).{0,60}shoulder|camera.{0,35}(?:observes|sees).{0,55}beyond.{0,35}shoulder|(?:over[- ]the[- ]shoulder)|관찰축.{0,35}어깨.{0,45}(?:지나|향)|카메라.{0,35}어깨\s*너머')
    # Bare camera level is a leveling instruction, not horizontal pitch proof.
    if not any(k in axes for k in ('pitch','roll')):
        put('leveling','level',r'camera.{0,35}(?:remains|keep|keeps|stays)?\s*(?:level|horizontal)|카메라(?:는|가)?\s*수평(?:을|으로)?\s*유지')
    return axes


def _cam_positive_and_negative(raw,masker=None):
    # Split a new affirmative verb after a negated conjunct before masking.
    pieces=re.split(r'(?:\band\s+|,\s*)(?=(?:keep|maintain|aim|point|direct|face|roll)\b)|(?<=않고)\s*',raw,flags=re.I)
    pos=[];neg=[]
    for piece in pieces:
        piece=mask_quoted(piece)
        if re.search(r'\brather than\b',piece,re.I):
            a,b=re.split(r'\brather than\b',piece,maxsplit=1,flags=re.I);pos.append(a);neg.append(b);continue
        if re.search(r'\b(?:do not|not to|never|no\s+(?:sideways|roll|tilt))\b|(?:숙이지|향하지|두지|기울이지|바라보지)\s*않',piece,re.I):
            # Korean local negation: retain the earlier affirmative 수평 predicate.
            k=re.search(r'(?:유지하고|유지하며|하되)\s*',piece)
            if k:pos.append(piece[:k.start()]);neg.append(piece[k.end():])
            else:
                operator=re.search(r'\b(?:do not|not to|never|no\s+(?:sideways|roll|tilt))\b',piece,re.I)
                if operator and operator.start()>0:
                    pos.append(piece[:operator.start()]);neg.append(piece[operator.start():])
                else:neg.append(piece)
            continue
        if '대신' in piece:
            a,b=piece.split('대신',1);neg.append(a);pos.append(b);continue
        pos.append(piece)
    if masker:
        pos=[masker(x) for x in pos]
    return pos,neg


def _cam_request(text,masker=None):
    focus=re.sub(r'^Photographic role:\s*','',text.split('\nScene context:',1)[0])
    if re.search(r'(?:direction|viewing direction)\s+(?:is\s+)?unspecified|without assigning.{0,30}(?:camera|axis)|관찰\s*방향은?\s*지정하지|카메라\s*축을\s*지정하지',focus,re.I):return None
    axes={};excluded={};evidence=[]
    for clause in _cam_clauses(focus):
        raw=clause.group()
        if not _cam_is_capture(raw):continue
        pos,neg=_cam_positive_and_negative(raw,masker)
        for part in pos:
            found=_cam_features(part)
            for aspect,w in found.items():
                # Find the exact matched value in the original field, preserving offsets.
                loc=raw.find(w['quote'])
                if loc<0:continue
                row={**w,'start':clause.start()+loc,'end':clause.start()+loc+len(w['quote'])}
                axes[aspect]=row;evidence.append({'pointer':'/role_focus',**row})
        for part in neg:
            for aspect,w in _cam_features(part).items():excluded.setdefault(aspect,[]).append(w['value'])
            if re.search(r'no\s+sideways\s+slant|옆으로\s*비껴',part,re.I):excluded.setdefault('yaw',[]).append('oblique')
    if not axes:return None
    return {'role':'camera_direction','asserts':True,'axes':axes,'excluded_axes':excluded,'witnesses':evidence,
            'request_text':text,'focus_text':focus,'owner':'taking_camera','native_approval':False}


def _semantic_conditions(units,effects):
    if 'source_conditions' in effects:
        common=effects['source_conditions'];branch=effects.get('realization_conditions',{})
        return ({'all_of':[common,branch]} if branch else common),False
    for u in units:
        if 'source_conditions' in u:return u['source_conditions'],False
    return {},True


def _cam_source(units,effects,masker=None):
    # Dimension/prefix is only a loading hint, never sufficient semantic support.
    if 'camera' not in effects.get('dimensions',[]) and not any(x.get('dimension')=='camera' for x in effects.get('properties',[])):return None
    evidence=[];axes={};excluded={}
    semantic=[u for u in units if _CAM_NAMED.search(u['pointer'])]
    for unit in semantic:
        before_evidence=len(evidence)
        for clause in _cam_clauses(unit['text']):
            raw=clause.group()
            if not _cam_is_capture(raw):continue
            pos,neg=_cam_positive_and_negative(raw,masker)
            for part in neg:
                for aspect,w in _cam_features(part).items():excluded.setdefault(aspect,[]).append(w['value'])
            for part in pos:
                for aspect,w in _cam_features(part).items():
                    loc=raw.find(w['quote'])
                    if loc<0:continue
                    row={**w,'start':clause.start()+loc,'end':clause.start()+loc+len(w['quote'])}
                    axes.setdefault(aspect,[]).append(row)
                    evidence.append({**unit,'matches':[row]})
        # Surface visibility may be the next sentence of the same complete
        # camera-owned primary field, rather than repeating the camera noun.
        if len(evidence)>before_evidence:
            if re.search(r'(?:front\s+(?:faces?|planes?)|near[- ]facing\s+(?:sides?|front\s+faces?)).{0,30}(?:not\s+visible|hidden|occluded)|(?:앞면|옆면).{0,20}(?:보이지\s*않|가려)',unit['text'],re.I):
                excluded.setdefault('surface_visibility',[]).append('top_and_near_side')
            positive=masker(unit['text']) if masker else mask_quoted(unit['text'])
            surface=_cam_features(positive).get('surface_visibility')
            if surface:
                span=unit['text'][surface['start']:surface['end']]
                tail=unit['text'][surface['end']:surface['end']+45]
                if not re.search(r'\b(?:not|without|cannot|neither)\b|않|없',span,re.I) and not re.match(r'\s*(?:are|is|remain|remains)?\s*(?:not\s+visible|hidden|occluded)|.{0,8}(?:보이지\s*않|가려)',tail,re.I):
                    axes.setdefault('surface_visibility',[]).append(surface)
                    evidence.append({**unit,'matches':[surface]})
    if not evidence:return None
    # A specific whole-source vertical claim cannot be diluted by a broad
    # translated 'down' label. Keep its own exact witness; never rewrite it.
    if any(w['value']=='vertical_down' for w in axes.get('pitch',[])):
        axes['pitch']=[w for w in axes['pitch'] if w['value']!='down']
    for aspect,rows in axes.items():
        if len({w['value'] for w in rows})>1:
            return {'role':'camera_direction','state':'review_required','reason':'incompatible complete source parameter values','aspect':aspect,'evidence':evidence,'whole_primary_units':units,'whole_effects':effects}
    conditions,unknown=_semantic_conditions(units,effects)
    primary='\n'.join(u['text'] for u in semantic)
    constraints=[u for u in units if _CAM_CONSTRAINT.search(u['pointer'])]
    constraint_text='\n'.join(u['text'] for u in constraints)
    requirements={
      'object_front_side':bool(any(w['value']=='oblique' for w in axes.get('yaw',[])) and re.search(r'front.{0,100}(?:adjacent side|side faces?|side and|adjoining)|앞면.{0,55}옆면|정면.{0,55}측면',primary,re.I)),
      'building':bool(re.search(r'existing building|기존\s*건물',primary,re.I)),
      'underside':bool(re.search(r'(?:existing|elevated) structure|기존.{0,12}구조물',primary,re.I) and re.search(r'underside|lower surface|아랫면',primary,re.I)),
      'upright_front':bool(re.search(r'identified upright planar front|기존\s*물체.{0,12}앞면',constraint_text+'\n'+primary,re.I) and any(w['value']=='front' for w in axes.get('yaw',[]))),
      'two_humans':any(w['value']=='shoulder' for w in axes.get('route',[])),
      'stable_references':bool('roll_sign' in axes),
    }
    return {'role':'camera_direction','state':'source_witnessed','owner':'taking_camera','axes':axes,'excluded_axes':excluded,'evidence':evidence,
            'whole_primary_units':units,'constraints':constraints,'conditions':conditions,'conditions_unknown':unknown,
            'requirements':requirements,'whole_effects':effects,'parameter_preservation':False,'native_approval':False}


def _cam_scene_support(req,src):
    text=req['request_text'];positive=mask_quoted(text)
    c=src['conditions'];guards=c.get('all_of',[c]);tags=set().union(*(set(g.get('requires_any_tags',[])) for g in guards));requirements=src['requirements']
    if tags & {'product','box'} and not re.search(r'\b(?:product|box|package|carton)\b|제품|상자|박스|포장',positive,re.I):return False
    if tags & {'table','tabletop','workbench','still_life'} and not re.search(r'table|desk|workbench|still.life|탁자|테이블|책상|작업대|정물',positive,re.I):return False
    if any(g.get('for_any')==['human'] for g in guards) and not re.search(r'person|people|adult|human|sitter|portrait|reader|성인|인물|사람|독자',positive,re.I):return False
    if requirements['object_front_side']:
        # The camera may vary yaw only around actual independent front/side
        # references. A level-only request cannot silently invent those faces.
        if not re.search(r'(?:front|facade).{0,80}(?:side|adjoin)|(?:앞면|정면).{0,60}(?:옆면|측면|인접)',positive,re.I):return False
        if re.search(r'\b(?:person|human|sitter|portrait)\b|인물|모델',positive,re.I) and not re.search(r'\b(?:object|cabinet|package|box|building|facade|structure|housing|panel)\b|물체|수납장|상자|건물|외벽|구조물',positive,re.I):return False
    if requirements['building']:
        if not re.search(r'building|facade|architecture|brick|건물|외벽|건축|벽돌',positive,re.I):return False
        if not re.search(r'corner|모서리',positive,re.I):return False
        if not re.search(r'(?:front|facade).{0,65}(?:side|adjoin)|정면.{0,30}(?:측면|인접)',positive,re.I):return False
    if requirements['underside']:
        if not re.search(r'underside|lower surface|아랫면',positive,re.I):return False
        if not re.search(r'structure|bridge|overhang|architecture|building|구조물|다리|육교|고가|건축',positive,re.I):return False
    if requirements['upright_front']:
        if not re.search(r'(?:camera|axis).{0,95}(?:front of|front surface|upright front)|카메라.{0,65}(?:정면|앞면)',req['focus_text'],re.I):return False
        if re.search(r'(?:toward|at|faces?).{0,15}(?:the )?(?:person|adult|sitter|human face)',req['focus_text'],re.I):return False
    if requirements['two_humans'] and not re.search(r'two\s+(?:adult|people|person)|성인\s*두\s*명|두\s*(?:성인|사람)',positive,re.I):return False
    if requirements['stable_references'] and not re.search(r'(?:room|wall|scene).{0,25}(?:edges|lines|references)|stable.{0,25}(?:upright|level|reference)|방의\s*모서리|기준선|벽.{0,12}모서리',positive,re.I):return False
    return True


def _cam_fit(req,src):
    if not req or not src or src.get('state')!='source_witnessed':return 'unproven'
    if req.get('owner')!=src.get('owner'):return 'conflicting'
    if src.get('conditions_unknown'):return 'unproven'
    found={k:{x['value'] for x in ws} for k,ws in src['axes'].items()}
    # Vertical plan view cannot fulfill an affirmative top-plus-front relation,
    # even when the request omits the word nonvertical.
    if req['axes'].get('surface_visibility',{}).get('value')=='top_and_near_side' and found.get('pitch')=={'vertical_down'}:return 'conflicting'
    for aspect,values in src.get('excluded_axes',{}).items():
        if req['axes'].get(aspect,{}).get('value') in values:return 'conflicting'
    for aspect,ws in req.get('excluded_axes',{}).items():
        if set(ws)&found.get(aspect,set()):return 'conflicting'
    for aspect,w in req['axes'].items():
        value=w['value']
        if aspect=='leveling':
            if found.get('roll')=={'tilted'}:return 'conflicting'
            if 'level' not in found.get('roll',set()) and 'level' not in found.get('pitch',set()):return 'unproven'
            continue
        if aspect=='pitch' and value=='down' and found.get('pitch')=={'vertical_down'}:
            if req['axes'].get('pitch_geometry',{}).get('value')=='nonvertical':return 'conflicting'
            continue
        if aspect=='pitch_geometry' and value=='nonvertical' and found.get('pitch')=={'vertical_down'}:return 'conflicting'
        if aspect in found and value not in found[aspect]:return 'conflicting'
        if value not in found.get(aspect,set()):return 'unproven'
    if not _cam_scene_support(req,src):return 'unproven'
    return 'supported'


class Semantic:
    """Exact selected-primary semantic discovery; never native qualification."""
    def __init__(self,masker=None):
        self.masker=masker

    def request(self,role,text):
        if role=='camera_direction':return _cam_request(text,self.masker)
        if role!='presentation_style':return None
        req=request_contract(text)
        if req is None or req.get('state')!='asserted_change':return None
        focus=re.sub(r'^Photographic role:\s*','',text.split('\nScene context:',1)[0]);w=[]
        for clause in req['clauses']:
            at=focus.find(clause)
            if at>=0:w.append({'pointer':'/role_focus','start':at,'end':at+len(clause),'quote':clause})
        return {**req,'role':role,'asserts':True,'witnesses':w,'request_text':text,'native_approval':False}

    def source(self,role,units,effects):
        units=list(units)
        if role=='camera_direction':return _cam_source(units,effects,self.masker)
        if role!='presentation_style':return None
        conditions,unknown=_semantic_conditions(units,effects);src=compile_contract(units,effects,conditions)
        if src is None:return None
        evidence=[]
        for rows in src.get('facets',{}).values():
            for row in rows:
                unit=next(u for u in units if u['pointer']==row['pointer']);evidence.append({**unit,'matches':[row]})
        return {**src,'role':role,'evidence':evidence,'conditions_unknown':unknown}

    def fit(self,req,src):
        if not req or not src or req.get('role')!=src.get('role'):return 'unproven'
        if req['role']=='camera_direction':return _cam_fit(req,src)
        result=compare(req,src)['decision']
        if result=='semantic_support_only':
            positive=' '.join(c for c in clauses(re.sub(r'이며|이고', '.', req['request_text'])) if not negative_clause(c))
            guards=src['conditions'].get('all_of',[src['conditions']])
            for guard in guards:
                if 'adult' in guard.get('requires_all_tags',[]) and not re.search(r'\badults?\b|성인',positive,re.I):return 'unproven'
                if guard.get('for_any')==['human'] and not re.search(r'\b(?:persons?|people|humans?|adults?|wearer|sitter|portrait|subject)\b|성인|인물|사람|착용자',positive,re.I):return 'unproven'
        if result!='conflict' and src.get('conditions_unknown'):return 'unproven'
        return {'semantic_support_only':'supported','conflict':'conflicting'}.get(result,'unproven')
