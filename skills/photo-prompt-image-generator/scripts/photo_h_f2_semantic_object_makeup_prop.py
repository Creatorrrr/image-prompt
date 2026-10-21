"""Bounded selected-primary whole-relationship semantics for advisory ordering.

No IDs, slot-tag votes, new effects, native qualification, searches or score
changes. Positive source facts come only from selected-RID primary fields.
Application/condition/effect constraints are retained separately. Unsupported
owners, carriers, fixed designs and physical prerequisites never bind by a
convenient fragment. The result is supported/conflicting/unproven.
"""
import re


def hits(text, patterns):
    return {k:[{'start':m.start(),'end':m.end(),'quote':m.group()} for m in re.finditer(p,text,re.I)] for k,p in patterns.items() if re.search(p,text,re.I)}

OBJ={
 'stool':r'\bstools?\b|스툴|(?:접이식|캠핑)\s*의자',
 'desk_lamp':r'\b(?:(?:desk|task|articulated)\s+){1,3}lamps?\b|탁상등|책상\s*램프',
 'carabiner':r'\b(?:carabiner|karabiner)s?\b|카라비너|카라비나',
 'drawer_cabinet':r'\b(?:cabinet|carcass)\b|수납장|캐비닛',
 'headphones':r'\bheadphones?\b|헤드폰',
 'equipment_case':r'\b(?:hard\s+(?:equipment\s+)?case|equipment\s+case)\b|(?:장비용\s*)?하드\s*케이스',
 'bicycle':r'\bbicycle\b|자전거', 'umbrella':r'\bumbrella\b|우산', 'toolbox':r'\btoolbox\b|공구함',
 'folding_chair':r'\bfolding\s+chair\b|접이식\s*의자',
 'lens_mount':r'\b(?:camera\s+lens\s+mount|bayonet\s+lens\s+mount|camera\s+assembly)\b|카메라\s*(?:조립체|렌즈\s*마운트)',
 'scissors':r'\bscissors\b|가위', 'phone':r'\bphone\b|휴대전화|휴대폰',
}
PART={
 'seat':r'\bseat(?:\s+panel)?\b|좌판|좌면',
 'crossed_legs':r'\b(?:cross\w*.{0,30}(?:legs?|support)|(?:legs?|support).{0,30}cross\w*)\b|교차.{0,18}(?:다리|지지)',
 'pivot':r'\bpivot\b|회전축', 'base':r'\bbase\b|받침|밑판|본체',
 'arm_sections':r'\b(?:arm\s+(?:sections?|members?)|(?:lower|upper)\s+arm)\b|팔\s*(?:구간|부재)',
 'joint':r'\b(?:joint(?:ed|s)?|hinge(?:d|s)?|joined|attached|connection)\b|관절|경첩|부착부|연결',
 'shade':r'\bshade\b|(?:^|\s)갓(?:의|을|이|에|\s|$)',
 'frame':r'\b(?:frame|loop)\b|프레임|고리', 'gate':r'\bgate\b|게이트', 'nose':r'\bnose\b|노즈',
 'carcass':r'\b(?:carcass|cabinet|bounded\s+box)\b|수납장|몸체|상자\s*형태',
 'drawer_fronts':r'\bdrawer.{0,35}front|front.{0,20}drawer|서랍.{0,18}앞판',
 'runners':r'\b(?:runner|rail)s?\b|레일|서랍\s*지지부',
 'headband':r'\bheadband\b|헤드밴드','earcups':r'\bear\s*cups?\b|이어컵','yokes':r'\byokes?\b|요크',
 'lid':r'\blid\b|뚜껑','cavities':r'\b(?:recess(?:es)?|cavit(?:y|ies))\b|수납\s*홈|형태.{0,12}홈|홈들',
 'inside':r'\b(?:inside|interior|within)\b|안쪽|내부|본체\s*안',
 'support_legs':r'\b(?:paired\s+(?:supporting\s+)?legs|(?:front|back|supporting)\s+leg\s+members)\b|한\s*쌍의\s*지지\s*다리|지지\s*다리',
 'frame_tubes':r'\b(?:frame\s+tubes?|upper\s+frame\s+member|down\s+tube)\b|프레임\s*튜브|상부\s*프레임\s*부재',
 'head_tube':r'\b(?:head\s+tube|steering[- ]head\s+tube)\b|헤드\s*튜브|조향\s*헤드',
 'fork':r'\bfork\b|포크', 'axle':r'\baxle\b|차축|축을',
 'barrel':r'\bbarrel\b|배럴', 'bayonet':r'\bbayonet\b|바요넷',
}
MECH={
 'bicycle':{'frame_tubes','head_tube','fork','axle','joint'},
 'folding_chair':{'seat','support_legs','joint'},
 'lens_mount':{'barrel','bayonet','joint'},
 'stool':{'seat','crossed_legs','pivot'},'desk_lamp':{'base','arm_sections','shade','joint'},
 'carabiner':{'frame','gate','joint'},'drawer_cabinet':{'carcass','drawer_fronts','runners'},
 'headphones':{'headband','earcups','yokes'},'equipment_case':{'lid','base','joint','cavities','inside'},
}
MEDIUM={
 'skin_piece':r'\b(?:cosmetic\s+(?:stars?|pearls?|pieces)|discrete\s+(?:applied\s+)?cosmetic\s+pieces)\b|개별\s*화장\s*장식\s*조각|화장용\s*진주|화장(?:용)?\s*별\s*조각',
 'foil':r'\b(?:cosmetic\s+foil|metallic[- ]foil|gold[- ]leaf\s+makeup|foil\s+fragments?)\b|(?:화장용\s*)?(?:메탈릭\s*)?포일',
 'crystal':r'\b(?:cosmetic\s+crystals?|crystal\s+face\s+gems?|decorative\s+crystals?|face\s+gems?)\b|(?:화장용\s*|장식용\s*)?크리스[털탈]|크리스털\s*젬',
 'applique':r'\b(?:stickers?|decals?|appliqu[eé]s?)\b|스티커|데칼|아플리케',
 'glitter':r'\bglitter\b|글리터',
 'paint':r'\b(?:cosmetic\s+(?:paint|pigment)|body[- ]makeup|body\s+makeup)\b|화장용\s*(?:안료|물감)|보디\s*메이크업|\bpaint(?:ed|ing)?\b.{0,60}\bcosmetic\b',
}
REGION={
 'cheek':r'\bcheek\b|볼\s*피부|볼에|볼의','temple':r'\btemple\b|관자놀이',
 'outer_eye':r'\bouter\s+eye\b|눈꼬리','near_eye':r'\bnear\s+(?:the\s+)?eye\b|눈\s*주변',
 'forehead':r'\bforehead\b|이마','clavicle':r'\b(?:collarbone|clavicle)\b|쇄골',
 'hand':r'\b(?:hand\s+skin|back\s+of\s+the\s+hand)\b|손\s*피부|손등',
 'upper_arm':r'\bupper\s+arm\b|위팔',
}
MOTIF={
 'star':r'\bstar(?:s|[- ]shaped)?\b|별\s*(?:모양|스티커|장식)|은색\s*별',
 'floral':r'\b(?:floral|botanical|flowers?|petals?)\b|꽃|꽃잎|식물',
 'dots':r'\b(?:dotted|dots?)\b|점\s*장식|점\s*모티브','ribbon':r'\bribbon\b|리본',
 'openwork_curls':r'\b(?:curls?|openwork)\b|장식\s*곡선|열린\s*틈',
}
PP={
 'handle':r'\bhandles?\b|손잡이','directed':r'\b(?:point\w*|project\w*|fac\w*)\s+toward\b|향하|향해',
 'dish':r'\b(?:saucers?|support\s+dishes|support\s+dish|dish)\b|받침|접시',
 'beside':r'\b(?:beside|next to|alongside)\b|옆','two_hands':r'\b(?:both|two)\s+hands\b|양손|두\s*손',
 'waist':r'\bwaist\b|허리','level':r'\b(?:horizontally|horizontal|level)\b|수평',
 'edge':r'\b(?:edge|boundary)\b|가장자리|모서리|경계','cross':r'\b(?:across|over|beyond|cross\w*)\b|걸쳐|가로질러|넘어|밖',
 'hang':r'\b(?:hang\w*|downward)\b|늘어지|늘어진|아래로','between':r'\b(?:between|separat\w*)\b|사이',
 'ground':r'\b(?:ground|floor)\b|바닥|지면',
 'rest':r'\b(?:rest\w*|set|place\w*|position\w*|keep|contact\w*|meet\w*)\b|놓|둔다|두며|두고|닿|접촉',
 'pocket':r'\bpocket\b|주머니','contain':r'\b(?:into|enclos\w*|contain\w*|tuck\w*)\b|꽂|넣|안에',
 'up':r'\b(?:upward|upwards)\b|위로|위를\s*향','lean':r'\blean\w*\b|기대',
 'lower':r'\b(?:lower\s+end|one\s+end|tip)\b|한쪽\s*끝|아래쪽\s*끝',
 'upper':r'\b(?:higher|upper|other(?:\s+end)?)\b|다른\s*끝|높은\s*부분|위쪽',
 'contact':r'\b(?:contact\w*|touch\w*|meet\w*|against)\b|닿|접촉',
 'flat':r'\b(?:flat|broad\s+face)\b|납작|넓은\s*면',
 'parallel':r'\bparallel\b|평행',
 'actor_side':r"\banatomical\s+side\b|(?:subject|actor|person|reader|repairer|holder|visitor|owner)(?:’s|'s)\s+(?:left|right)\b|(?:인물|독자|수리공|방문객|소유자|작업자)의.{0,18}(?:측면|왼쪽|오른쪽)|해부학적\s*측면",
 'diagonal':r'\b(?:diagonal(?:ly)?|oblique)\b|비스듬|대각선',
 'vessel':r'\b(?:cup|vessel|mug)\b|컵|용기|찻잔',
 'matching_dish':r'\b(?:matching|own).{0,30}(?:saucer|support\s+dish)\b|짝이\s*되는\s*받침|자체\s*받침',
}
PPF={
 'flat_actor_edge':{'parallel','actor_side','edge','rest'},
 'utensil_dish':{'diagonal','cross','dish','vessel','matching_dish'},
 'handled_support':{'handle','directed','dish','beside'},
 'held_waist':{'two_hands','waist','level'},
 'edge_drape':{'edge','cross','hang'},
 'ground_between':{'between','ground','rest'},
 'pocket_up':{'pocket','contain','up'},
 'two_contact_lean':{'lean','ground','lower','upper','contact'},
}
CLASS={
 'serving_utensil':r'\b(?:teaspoon|spoon|serving\s+utensil)\b|티스푼|숟가락|식사용\s*도구',
 'handled_vessel':r'\b(?:teacup|cup|mug|handled\s+vessel|handled\s+prop)\b|찻잔|머그|컵|손잡이\s*용기',
 'flat_prop':r'\b(?:map|notebook|book|flat\s+(?:portable\s+)?prop|sheet)\b|지도|노트|책|납작한\s*휴대\s*소품',
 'loose_textile':r'\b(?:scarf|loose\s+textile|cloth|runner|shawl)\b|목도리|스카프|느슨한\s*직물|같은\s*천',
 'slender_tool':r'\b(?:paintbrush|brush|pencil|slender\s+(?:hand\s+)?tool)\b|붓|연필|가늘고\s*긴\s*손도구',
 'elongated_prop':r'\b(?:walking\s+stick|cane|rod|pole|umbrella|elongated\s+prop)\b|지팡이|막대|우산|길쭉한\s*소품',
 'grounded_prop':r'\b(?:lantern|basket|object|prop)\b|랜턴|바구니|물체|소품',
}
FAMILY_CLASS={'flat_actor_edge':'flat_prop','utensil_dish':'serving_utensil','handled_support':'handled_vessel','held_waist':'flat_prop','edge_drape':'loose_textile','pocket_up':'slender_tool','two_contact_lean':'elongated_prop','ground_between':'grounded_prop'}
SURFACE={
 'table':r'\b(?:table|tabletop|desk|counter|workbench|work\s+surface)\b|탁자|테이블|책상|조리대|작업\s*(?:표면|대)',
 'bench':r'\bbench\b|벤치','chair':r'\bchair\b|의자','ground':r'\b(?:floor|ground)\b|바닥|지면',
 'pocket':r'\bpocket\b|주머니','dish':r'\b(?:saucer|dish)\b|받침|접시',
}
FACE={'cheek','temple','outer_eye','near_eye','forehead'}
ALLOWED_POINTER=re.compile(r'^/content/(?:en$|ko$|definition$|embedding_text$|concept_units/|components/|semantics/definition$|semantics/visual_components/)')

# Recognized requirement vocabulary describes carrier/type/contact obligations,
# not a candidate dictionary. Unknown positive mandatory clauses fail closed.
_REQUIREMENT_WORDS=set("use only for apply to when requires require an a the one two exactly independently present declared named existing selected actual this that its own same and or with whose their already is are be as at on of in by from into within without all each both any every no not positive physical visible visibly evidenced established specifically specified supplied complete nonempty particular current separate distinct bounded independent supporting support supports supported surface surfaces region regions skin facial person human adult actor actors owner holder wearer ownership tool pocket carrier garment object prop flat portable elongated slender hand hands upper lower end contact relation relationship panel seat leg legs crossing construction stool folding lamp articulated desk members arrangement base shade carabiner frame hinged hinge gate equipment hard case lid interior receiving cavities drawer cabinet runner rails headband cup yokes headphones over ear cosmetic decal decals applique appliques design decorative motif body makeup pigment painting layer loose textile floor handled vessel dish designated available relationships these context explicitly identifies scene edge ground".split())
_REQUIREMENT_WORDS.update('discrete applied pieces chair paired camera lens barrel bayonet mount attached anatomical side work serving utensil matching diagonal placement connections assembly table'.split())
_REQUIREMENT_START=re.compile(r'^(?:Requires?\b|Use only\b|Apply only\b)',re.I)

class Semantic:
    def __init__(self,masker): self.masker=masker

    def _positive(self,text):
        if not text.strip():return text
        # Final Korean negation scopes over noun enumerations across commas.
        # Finite positive coordinators retain their separate clauses.
        chars=list(text)
        # A free-of complement is negative even when the topic is cosmetic.
        # Stop at a finite contrast so a separate positive clause survives.
        for m in re.finditer(r'[^.;!?\n]*?\bfree\s+of\b.*?(?=[.;!?\n]|\bbut\b|\bwhile\b|$)',text,re.I):
            raw=m.group();anchor=list(re.finditer(r'\band\s+(?:keep|leave)\b',raw,re.I))
            start=m.start()+(anchor[-1].start() if anchor else 0)
            chars[start:m.end()]=' '*(m.end()-start)
        for sentence in re.finditer(r'[^.!?;\n]+',text):
            raw=sentence.group();n=re.search(r'(?:추가하지|하지|두지|붙이지|그리지|만들지|바꾸지|변경하지|옮기지|잡지|들지)\s*않',raw)
            if not n:continue
            sep=list(re.finditer(r'보여주고|표현하고|놓고|두고|두되|놓되|배치하며|보이되|그리되|붙이되|하되|하지만|그러나',raw[:n.start()]))
            start=sentence.start()+(sep[-1].end() if sep else 0)
            chars[start:sentence.end()]=' '*(sentence.end()-start)
        prepared=''.join(chars)
        if not prepared.strip():return prepared
        out=self.masker(prepared)
        if len(out)!=len(text):raise ValueError('masker must preserve Unicode offsets')
        return out

    def _role_scene(self,text):
        m=re.search(r'^Photographic role:[ \t]*(.*?)(?=\nScene context:|\Z)',text,re.S)
        role=m.group(1) if m else text
        scene=text.split('\nScene context:',1)[1] if '\nScene context:' in text else ''
        return role,scene,(m.start(1) if m else 0)

    def _object(self,text,source=False):
        t=self._positive(text);k=hits(t,OBJ);parts=hits(t,PART)
        fam={name for name,need in MECH.items() if name in k and need<=parts.keys()}
        if source and 'carabiner' in fam and 'nose' not in parts:fam.remove('carabiner')
        # No construction is asserted by localized rust/chipping alone.
        if re.search(r'rust|chipped|flaking|녹슨|벗겨진',t,re.I) and not set(parts)&{'frame','gate','runners','headband','earcups','arm_sections','cavities','crossed_legs'}:fam=set()
        return {'families':sorted(fam),'kinds':sorted(k),'part_names':sorted(parts),'witnesses':[v for name in sorted(fam) for part in sorted(MECH[name]) for v in parts[part]],'closed':bool(re.search(r'\bclosed\b|닫힌|닫혀',t,re.I)),'interior_visible':bool(re.search(r'\b(?:interior|inside).{0,30}(?:visible|exposed)|\b(?:visible|exposed).{0,30}(?:interior|inside)|내부.{0,18}(?:보이|보이는|드러)|본체\s*안|bounded\s+inside',t,re.I))}

    def _makeup(self,role,scene='',source=False):
        t=self._positive(role);c=self._positive(scene);media=hits(t,MEDIUM);reg=hits(t,REGION);motif=hits(t,MOTIF)
        skin=bool(re.search(r'\b(?:skin|face|facial|temple|forehead|cheek|collarbone|eye)\b|피부|얼굴|관자놀이|이마|쇄골|눈꼬리',t,re.I))
        cosmetic=bool(re.search(r'\b(?:cosmetic|makeup|body[- ]makeup|beauty)\b|화장|메이크업|뷰티',t+(' '+c if not source else ''),re.I))
        if source and set(media)<={'applique','glitter','crystal','skin_piece'} and media and skin:cosmetic=True
        # Applied pigment/blush alone is tonal cosmetics, not an ornament.
        design=bool(motif or re.search(r'\b(?:motifs?|ornaments?|decorat\w*|designs?)\b|모티브|장식|문양|도안',t,re.I))
        if 'paint' in media and not design:media.pop('paint')
        physical=bool(media and skin and cosmetic)
        if re.search(r'\b(?:permanent|healed).{0,20}(?:ink|tattoo)|영구\s*(?:잉크|문신)|아문.{0,10}문신',t,re.I):physical=False
        generic=bool(re.search(r'\b(?:declared|specified|supplied)\b|선언|명시|지정|제공',t,re.I) and re.search(r'\b(?:skin\s+region|facial\s+skin\s+region)\b|피부\s*부위',t,re.I) and re.search(r'\b(?:preserv\w*|retain\w*|remain\w*|exactly)\b|유지|그대로',t,re.I))
        face_only=bool(re.search(r'\b(?:facial|face\s+gems)\b|얼굴\s*피부|얼굴의',t,re.I))
        owner='artist' if re.search(r"artist(?:’s|'s)?\s+(?:own|cheek)|아티스트.{0,18}자신",t,re.I) else 'model' if re.search(r"model(?:’s|'s)|모델의",t,re.I) else 'selected_person'
        sides=hits(t,{'left':r'\bleft\s+(?:cheek|temple|eye|hand)\b|왼쪽','right':r'\bright\s+(?:cheek|temple|eye|hand)\b|오른쪽'})
        # Bare skin on another named person does not erase an artist's design.
        bare_scene=bool(re.search(r'bare[- ]faced|no.{0,20}(?:skin\s+ornament|cosmetic\s+decoration)|undecorated|민낯|장식이\s*없|장식이\s*없는',scene,re.I))
        selected_bare=bare_scene and not(owner=='artist' and re.search(r'\bmodel\b|모델',scene,re.I))
        color=hits(t,{'gold':r'\bgold\b|금색','silver':r'\bsilver\b|은색','pearlescent':r'\bpearlescent\b|진주광'})
        # Foil/crystal sources must describe localized real material, not just
        # beauty/casting/framing. Full primary embedding prose can witness it.
        if source and 'foil' in media:physical=physical and bool(reg) and bool(re.search(r'edge|fragment|accent|포인트|조각|경계',t,re.I))
        if source and 'crystal' in media:physical=physical and bool(re.search(r'attach|localized|constellation|부위|별자리|붙',t,re.I))
        return {'families':sorted(media) if physical else [],'regions':sorted(reg),'motifs':sorted(motif),'colors':sorted(color),'generic_region':generic,'generic_design':generic,'face_only':face_only,'removable':bool(re.search(r'\b(?:removable|temporary)\b|떼어낼|지울\s*수|일시적',t,re.I)),'owner':owner,'sides':sorted(sides),'selected_bare':selected_bare,'witnesses':[v for d in (media,reg,motif) for vals in d.values() for v in vals]}

    def _prop(self,text,source=False):
        t=self._positive(text);atoms=hits(t,PP);types=hits(t,CLASS);surfaces=hits(t,SURFACE)
        families={k for k,v in PPF.items() if v<=atoms.keys()}
        # 'Between contacts' is not an actor-between relation.
        two_actors=bool(re.search(r'\btwo\s+(?:(?:named|seated|adult)\s+)*(?:actors|adults|people|persons|hikers)\b|두\s*(?:지정된\s*)?(?:인물|성인|등산객)|성인.{0,20}두\s*명',t,re.I))
        if not two_actors:families.discard('ground_between')
        if 'two_contact_lean' in families:families.discard('ground_between')
        # Query objects must inhabit the source's declared physical class.
        families={k for k in families if FAMILY_CLASS[k] in types}
        human=bool(re.search(r'\b(?:adult|person|people|subjects?|actors?|holder|hikers?)\b|성인|인물|소유자|화가|방문객|안내원|등산객',t,re.I))
        fixed_umbrella=bool(re.search(r'\b(?:folded\s+)?umbrella\b|접은\s*우산',t,re.I))
        generic_class=bool(re.search(r'\b(?:existing|declared)\b|기존|선언',t,re.I) and re.search(r'\b(?:elongated\s+prop|flat\s+portable\s+prop|slender\s+hand\s+tool|loose\s+textile|handled\s+vessel)\b|길쭉한\s*소품|납작한\s*휴대\s*소품|가늘고\s*긴\s*손도구|느슨한\s*직물|손잡이\s*용기',t,re.I))
        side_matches=re.finditer(r"(?:subject|actor|person|reader|repairer|holder|visitor|owner)(?:’s|'s)\s+(left|right)\b",t,re.I)
        actor_sides={m.group(1).lower() for m in side_matches}
        actor_sides.update({'왼쪽':'left','오른쪽':'right'}[m.group(1)] for m in re.finditer(r'(?:인물|독자|수리공|방문객|소유자|작업자)의\s*(왼쪽|오른쪽)',t))
        actor_sides=sorted(actor_sides)
        return {'actor_sides':actor_sides,'families':sorted(families),'classes':sorted(types),'surfaces':sorted(surfaces),'two_actors':two_actors,'human':human,'fixed_umbrella':fixed_umbrella and not generic_class,'generic_class':generic_class,'chair_leg':bool(re.search(r'\bchair\s+leg\b|의자\s*다리',t,re.I)),'backrest':bool(re.search(r'\b(?:chair\s+back|backrest)\b|의자\s*등받이',t,re.I)),'witnesses':[v for k in sorted(families) for atom in sorted(PPF[k]) for v in atoms[atom]]}

    def _scoped_constraints(self,body,scene,role):
        """Retain actual requester limits without treating them as scene facts."""
        specs={
            'placement_unspecified':r'\b(?:placement|position|location)\b.{0,35}\b(?:unspecified|unknown|undetermined|not\s+(?:specified|declared|established))\b|\b(?:leave|keep)\b.{0,50}\b(?:placement|position|location)\b.{0,15}\bunspecified\b|\b(?:does\s+not|doesn.t)\b.{0,30}\b(?:establish|determine|specify)\b.{0,55}\b(?:where|position|location)\b|\bno\b.{0,35}\bplacement\b.{0,30}\bdeclared\b|(?:배치|위치).{0,18}(?:지정하지|정하지|선언되지|알\s*수\s*없)|명칭.{0,35}실제\s*위치.{0,15}정하지',
            'preserve_position':r'\b(?:preserv\w*|retain\w*|keep\w*)\b.{0,25}\b(?:current|existing|same)\b.{0,15}\b(?:position|placement|location)\b|\b(?:must\s+not|do\s+not|don.t)\s+(?:move|reposition)\b|\bstay\s+where\s+(?:they|it)\s+(?:are|is)\b|현재\s*위치.{0,15}유지|위치.{0,12}(?:바꾸지|옮기지)',
            'preserve_orientation':r'\b(?:do\s+not|must\s+not|don.t)\s+change\b.{0,30}\b(?:orientation|direction|flat)\b|\b(?:preserv\w*|retain\w*|keep\w*)\b.{0,30}\b(?:orientation|direction|flat)\b|방향.{0,12}바꾸지|(?:기존|현재).{0,20}방향.{0,15}유지',
            'no_holding':r'\b(?:must\s+not|do\s+not|don.t|never|not)\s+(?:carry|hold|grip|lift)\b(?:\s+or\s+(?:carry|hold|grip|lift))?|(?:들지|잡지).{0,8}않|(?:들거나|잡거나|들게|잡게).{0,20}(?:안\s*된|않|금지)',
            'selected_owner_only':r'\bonly\b[^.;\n]{0,65}?(?:[’\x27]s|their|his|her)\s+\w+|(?:도구|소품|물건)만',
            'no_decoration':r'\bfree\s+of\b.{0,65}\b(?:ornament|decoration)s?\b|\b(?:no|without|undecorated)\b.{0,45}\b(?:skin\s+ornament|cosmetic\s+decoration|cheeks?)\b|\b(?:bare[- ]faced|bare\s+skin|undecorated\s+(?:facial\s+skin|cheeks?))\b|민낯|일시적.{0,15}화장.{0,12}장식.{0,12}없|(?:피부|볼).{0,30}(?:장식이?\s*없|장식을?\s*두지)|(?:붙이거나|그린).{0,20}장식.{0,15}두지',
            'no_construction':r'\bno\b.{0,35}\b(?:construction\s+detail|mechanical\s+object|jointed\s+product)\b|\bdo\s+not\s+add\b.{0,80}\b(?:hinge|joint|connecting\s+part)\b|(?:제작\s*구조|구조\s*세부|기계\s*물체|관절이\s*있는\s*제품).{0,30}(?:요청하지|선언하지|않)|(?:경첩|관절|연결\s*부품).{0,50}추가하지',
        }
        allow={'prop_placement':{'placement_unspecified','preserve_position','preserve_orientation','no_holding','selected_owner_only'},'makeup_decoration':{'no_decoration'},'object_structure':{'no_construction'}}[role]
        out=[]
        for field,text in [('role',body),('scene',scene)]:
            for name in sorted(allow):
                for m in re.finditer(specs[name],text,re.I):
                    out.append({'kind':name,'field':field,'start':m.start(),'end':m.end(),'quote':m.group()})
        return out

    def _excluded_intent(self,role,body,scene,frame):
        limits=self._scoped_constraints(body,scene,role)
        if role=='makeup_decoration':
            # Ordinary pigment/blush is an adjacent positive cosmetic property,
            # not a negative ornament request. Require an actual exclusion.
            domain=bool(re.search(r'cosmetic|makeup|face\s+gems|ornament|decoration|undecorated|bare[- ]faced|화장|메이크업|장식|민낯',body+' '+scene,re.I))
            if not domain or not limits:return None
            mode='excluded_cosmetic_decoration'
        elif role=='object_structure':
            if not limits:
                quoted=list(re.finditer(r'“[^”]*”|‘[^’]*’|"[^"\n]*"',body))
                literal_parts=[m for m in quoted if re.search(r'hinge|joint|pivot|gate|mechanical|경첩|관절|회전축',m.group(),re.I)]
                if literal_parts and re.search(r'title|printed|catalog|label|제목|인쇄|카탈로그',body,re.I):
                    limits=[{'kind':'literal_only_construction','field':'role','start':m.start(),'end':m.end(),'quote':m.group()} for m in literal_parts]
                else:return None
            mode='excluded_object_construction'
        else:return None
        return {**frame,'families':[],'asserts':False,'exclusion_only':True,'positive_relation':False,'intent_mode':mode,'constraints':{'clauses':limits,'source_discovery':'no_unknown_padding'},'witnesses':[{'start':0,'end':len(body),'quote':body}]}

    def _prop_intent(self,body,scene,frame):
        """Recognize requested placement even when no complete family models it.

        This is an intent fence, never a source-family witness or a new physical
        owner. Literal/unknown/preserve-only limits remain nonpositive.
        """
        limits=self._scoped_constraints(body,scene,'prop_placement')
        spatial=r'\b(?:on|beside|next\s+to|alongside|under|between|against|near|above|below|across|inside|outside|relative\s+to)\b|옆|위에|아래|사이|바닥|가로질러|평행|방향'
        entity=r'\b(?:objects?|props?|items?|tools?|utensils?|vessels?|books?|notebooks?|baskets?|bottles?|scarves|scarf|lanterns?|maps?|cups?|mugs?|stones?|sculptures?|chairs?|stools?|vases?|toolbox(?:es)?|walking\s+sticks?|umbrellas?)\b|도구|소품|물건|물체|바구니|공구함|조각|꽃병|의자|지팡이|우산|찻잔|목도리|스카프|지도|(?:^|\s)책(?:을|이|은|의|\s)|(?:^|\s)병(?:을|이|은|의|\s)|(?:^|\s)돌(?:을|이|은|의|\s)'
        domain=r'\b(?:placement|position|location|orientation|where|physically\s+sits)\b|배치|위치|방향'
        owned_nominal=r'\b(?:existing|declared|actual|physical|owned)\s+(?:[a-z][\w-]*\s+){0,3}[a-z][\w-]*\b|기존(?:의)?\s+[^\s,;.]+|선언된\s+[^\s,;.]+'
        raw_has_entity=bool(re.search(entity+'|'+owned_nominal,body+' '+scene,re.I))
        physical_anchor=r'\b(?:floor|ground|pavement|table|workbench|counter|bench|seat|shelf|rack|ledge|plinth|pedestal|wall|pocket|dish|tray)\b|바닥|지면|탁자|작업대|벤치|선반|받침|주머니|접시'
        abstract=r'\b(?:hope|trust|idea|concept|theme|mood|memory|argument|condition|equation|value|number|symbol)\b|희망|신뢰|개념|주장|방정식'
        relevant=raw_has_entity and bool(re.search(domain,body,re.I) or re.search(spatial,body,re.I))
        kinds={x['kind'] for x in limits}
        quoted=list(re.finditer(r'“[^”]*”|‘[^’]*’|"[^"\n]*"|(?<!\w)\x27[^\x27\n]*\x27(?!\w)',body))
        t=self._positive(body)
        chars=list(t)
        for m in quoted:chars[m.start():m.end()]=' '*(m.end()-m.start())
        t=''.join(chars)
        action=r'\b(?:plac(?:e|es|ed|ing)|position(?:s|ed|ing)?|arrang(?:e|es|ed|ing)|put(?:s|ting)?|set(?:s|ting)?|lay(?:s|ing)?|keep(?:s|ing)?|rest(?:s|ing)?|leave(?:s)?)\b'
        affirmative=False
        for a in re.finditer(action,t,re.I):
            tail=t[a.end():];rel=re.search(spatial,tail,re.I)
            if rel is None:continue
            target=tail[:rel.start()]
            concrete_target=bool(re.search(entity+'|'+owned_nominal,target,re.I) or re.search(r'\b(?:it|them)\b',target,re.I) and raw_has_entity)
            if not concrete_target and re.search(physical_anchor,t,re.I) and re.search(r'\b(?:the|an?|one)\s+\w+',target,re.I) and not re.search(abstract,target,re.I):concrete_target=True
            if not concrete_target:continue
            if re.search(r'\b(?:icon|picture|image|drawing|caption|title|logo|printed\s+phrase)\b|그림|인쇄\s*문구|제목',target,re.I):continue
            affirmative=True;break
        # Subject-owned physical predication, not a person situated near a prop.
        if not affirmative:
            affirmative=bool(re.search(r'(?:'+entity+r').{0,65}\b(?:rests?|lies?|stands?|sits?|is|are|remains?)\b.{0,30}(?:'+spatial+r')',t,re.I))
        if not affirmative and re.search(entity+'|'+owned_nominal,t,re.I) and re.search(r'배치|놓|두(?:며|고|되|다|어|라)|기대|걸쳐',t) and re.search(spatial,t,re.I):affirmative=True
        definition_only=bool(re.search(r'\b(?:position|placement)\b.{0,25}\borientation\b.{0,35}\b(?:owned|declared)\s+props?\b',t,re.I) and not scene.strip())
        if definition_only:affirmative=True
        if relevant and 'placement_unspecified' in kinds:
            return {**frame,'families':[],'asserts':False,'exclusion_only':True,'positive_relation':False,'intent_mode':'excluded_or_unspecified','constraints':{'clauses':limits,'source_discovery':'no_unknown_padding'},'witnesses':[{'start':0,'end':len(body),'quote':body}]}
        if relevant and not affirmative and 'preserve_position' in kinds:
            return {**frame,'families':[],'asserts':False,'exclusion_only':True,'positive_relation':False,'intent_mode':'preserve_only','constraints':{'clauses':limits,'source_discovery':'no_unknown_padding'},'witnesses':[{'start':0,'end':len(body),'quote':body}]}
        literal_spatial=any(re.search(spatial+'|'+domain,m.group(),re.I) for m in quoted)
        if relevant and not affirmative and literal_spatial and re.search(r'\b(?:printed|label|caption|title|phrase|text)\b|인쇄|문구|라벨|제목|설명문',body,re.I):
            return {**frame,'families':[],'asserts':False,'exclusion_only':True,'positive_relation':False,'intent_mode':'literal_only_placement','constraints':{'clauses':limits,'source_discovery':'no_unknown_padding'},'witnesses':[{'start':m.start(),'end':m.end(),'quote':m.group()} for m in quoted]}
        if not affirmative:return None
        owners=[]
        for m in re.finditer(r'\b([a-z][\w -]{0,25})(?:’s|\x27s)\s+(?:own\s+)?(?:tools?|objects?|props?|items?)\b|([가-힣A-Za-z]+)의\s*(?:도구|소품|물건)',body,re.I):
            owner=(m.group(1) or m.group(2)).strip()
            owner=re.sub(r'^(?:(?:the|a|an|only|arrange|place|position|keep|set|put)\s+)+','',owner,flags=re.I)
            owner_start=m.start()+m.group().lower().find(owner.lower())
            if owner in {'자신','본인'}:
                antecedent=re.search(r'([가-힣A-Za-z]+)\s*$',body[:m.start()])
                if antecedent:owner=antecedent.group(1);owner_start=antecedent.start(1)
            owners.append({'owner_text':owner,'start':owner_start,'end':m.end(),'quote':body[owner_start:m.end()]})
        witnesses=[{'start':m.start(),'end':m.end(),'quote':body[m.start():m.end()]} for pattern in [entity,owned_nominal,action,spatial] for m in re.finditer(pattern,t,re.I)]
        return {**frame,'families':[],'asserts':True,'exclusion_only':False,'positive_relation':True,'intent_mode':'owned_relation_unmodeled','definition_only':definition_only,'constraints':{'clauses':limits,'owner_mentions':owners,'source_discovery':'no_unknown_padding','unmodeled_relationship_never_supplies_source_support':True},'witnesses':witnesses}

    def request(self,role,text):
        body,scene,offset=self._role_scene(text)
        if role=='object_structure':
            d=self._object(body)
            if not d['families']:
                joined=self._object(body+'\n'+scene)
                joined['families']=[f for f in joined['families'] if MECH[f]<=set(d['part_names'])]
                if joined['families']:d=joined
        elif role=='makeup_decoration':d=self._makeup(body,scene)
        elif role=='prop_placement':d=self._prop(body+'\n'+scene)
        else:return None
        if role=='prop_placement' and d['families']:
            f=set(d['families'])
            if 'handled_support' in f and not ('table' in d['surfaces'] and d['human']):f.remove('handled_support')
            if 'held_waist' in f and not d['human']:f.remove('held_waist')
            if 'flat_actor_edge' in f and not ('table' in d['surfaces'] and d['human']):f.remove('flat_actor_edge')
            if 'edge_drape' in f and not set(d['surfaces'])&{'bench','chair','table'}:f.remove('edge_drape')
            if 'two_contact_lean' in f and not ('ground' in d['surfaces'] and set(d['surfaces'])&{'chair','bench','table'}):f.remove('two_contact_lean')
            d['families']=sorted(f)
        if not d['families']:
            intent=self._prop_intent(body,scene,d) if role=='prop_placement' else self._excluded_intent(role,body,scene,d)
            if intent is None:return None
            d=intent
        else:
            d['intent_mode']='modeled_owned_relation'
            d['constraints']={'clauses':self._scoped_constraints(body,scene,role)}
        witnesses=[]
        for w in d.pop('witnesses',[]):
            w=dict(w);w['field']='role' if w['start']<len(body) else 'scene'
            if w['field']=='role':w['start']+=offset;w['end']+=offset
            else:
                scene_offset=text.index('\nScene context:')+len('\nScene context:') if '\nScene context:' in text else len(body)+1
                w['start']+=scene_offset-len(body)-1;w['end']+=scene_offset-len(body)-1
            w['pointer']='/request';witnesses.append(w)
        # Clause constraints retain separate original field-local offsets; they
        # are restrictions, never affirmative source/owner facts.
        asserts=d.pop('asserts',True)
        return {**d,'role':role,'asserts':asserts,'text':text,'role_text':body,'scene_text':scene,'witnesses':witnesses,'native_approval':False}

    def _mandatory(self,units):
        rows=[]
        for u in units:
            if u['pointer']!='/content/application_contract':continue
            positive=self._positive(u['text'])
            for m in re.finditer(r'[^.!?;]+',positive):
                raw=m.group().strip()
                if not (_REQUIREMENT_START.search(raw) or re.search(r'\bmust\s+(?:have|include|contain|stand|sit|be\s+(?:a|an|the))\b|^Only\s+if\b',raw,re.I)):continue
                unknown=sorted({w for w in re.findall(r'[a-z]+',raw.casefold()) if w not in _REQUIREMENT_WORDS})
                rows.append({'unit':u,'quote':raw,'unknown_required_terms':unknown})
        return rows

    def source(self,role,units,effects):
        # Effects remain exact; empty property lists are not missing meaning.
        # Every candidate still needs a positive primary whole-family witness.
        if role=='makeup_decoration' and not set(effects.get('dimensions',[]))&{'appearance','material'}:return None
        facts=[u for u in units if ALLOWED_POINTER.match(u['pointer'])]
        alternatives=[]
        for u in facts:
            t=u['text']
            if role=='object_structure':d=self._object(t,True)
            elif role=='makeup_decoration':d=self._makeup(t,'',True)
            elif role=='prop_placement':d=self._prop(t,True)
            else:return None
            if d['families']:alternatives.append({'frame':d,'unit':u})
        if not alternatives:return None
        return {'role':role,'alternatives':alternatives,'evidence':facts,'all_primary_units':units,
                'constraints':{'application_units':[u for u in units if u['pointer']=='/content/application_contract'],
                               'original_conditions':[u['conditions'] for u in units if 'conditions' in u],
                               'effects':effects},'mandatory':self._mandatory(units),'extra_actor_actions':[u for u in facts if re.search(r'\b(?:a|an|one|two|the)\s+(?:adult|person|worker|model|wearer)\b.{0,50}\b(?:holds?|sits?|wears?|carries|grips?|stands?)\b',self._positive(u['text']),re.I)],'effects':effects,'native_approval':False}

    def _requirements_fit(self,req,src):
        if any(x['unknown_required_terms'] for x in src.get('mandatory',[])):return 'unproven'
        positive=self._positive(req['role_text']+' '+req['scene_text'])
        if req['role']=='object_structure' and src.get('extra_actor_actions'):return 'unproven'
        human=bool(re.search(r'\b(?:person|people|subject|model|artist|dancer|actor|guide|hiker|holder|adult(?!\s+(?:dog|cat|horse)))\b|성인|사람|인물|모델|배우|아티스트|무용수|안내원|등산객',positive,re.I))
        # A declared cosmetic region is the actual skin owner, not a new
        # independently invented person. Ordinary color-only makeup never
        # reaches this branch because it lacks decorative intent.
        human=human or (req['role']=='makeup_decoration' and bool(req.get('regions')) and bool(req.get('families')))
        for row in src.get('mandatory',[]):
            text=row['quote']
            if re.search(r'\b(?:person|human|adult|actor|holder)\b',text,re.I) and not human:return 'unproven'
            if re.search(r'\btwo\s+(?:human\s+|adult\s+|named\s+)*(?:actors|people|persons)\b',text,re.I):
                if not re.search(r'\btwo\s+(?:adult\s+|named\s+|seated\s+)*(?:actors|adults|people|persons|hikers)\b|두\s*(?:인물|성인|등산객)|성인.{0,20}두\s*명',positive,re.I):return 'unproven'
        allowed={
            'object_structure':('object.structure.','object.connection.','object.geometry.'),
            'makeup_decoration':('makeup.decoration','skin.cosmetic_decoration'),
            'prop_placement':('prop.position','prop.orientation','props.placement','objects.position','body.two_hand_prop_support_at_waist'),
        }[req['role']]
        if any(not p.get('property','').startswith(allowed) for p in src['effects'].get('properties',[])):return 'unproven'
        for cond in src.get('constraints',{}).get('original_conditions',[]):
            if not cond:continue
            # Native guards remain host-enforced. For semantic promotion this
            # bounded evaluator never turns an unknown guard into success.
            if set(cond)-{'for_any','native_guards'}:return 'unproven'
            domains=set(cond.get('for_any',[]))
            if domains and not domains&{'human','object','product'}:return 'unproven'
            if domains and domains<={'human'} and not human:return 'unproven'
            for rule in cond.get('native_guards',{}).get('rules',[]):
                if rule.get('kind')!='frozen_value':return 'unproven'
                value=rule.get('value',{}).get('value')
                if not isinstance(value,str):return 'unproven'
                # Exact known object kinds can be checked via the same closed
                # semantic class vocabulary; unknown typed values stay unknown.
                fixed=hits(value,OBJ)
                requested=hits(positive,OBJ)
                if fixed and not set(fixed)<=set(requested):return 'conflicting'
                if not fixed and not re.search(r'\b'+re.escape(value)+r'\b',positive,re.I):return 'unproven'
        return 'supported'

    def fit(self,req,src):
        if req is None or src is None:return 'unproven'
        if req['role']!=src['role']:return 'conflicting'
        if req.get('asserts') is False:
            return 'conflicting' if req.get('intent_mode') in {'excluded_cosmetic_decoration','excluded_object_construction','excluded_or_unspecified','literal_only_placement'} else 'unproven'
        if req.get('intent_mode')=='owned_relation_unmodeled':return 'unproven'
        if req['role']=='prop_placement':
            limits={x['kind'] for x in req.get('constraints',{}).get('clauses',[])}
            # Unresolved restriction scope cannot be borrowed as permission.
            if 'placement_unspecified' in limits:return 'unproven'
            if 'no_holding' in limits and any('held_waist' in a['frame']['families'] for a in src.get('alternatives',[])):return 'unproven'
        if not any(set(req['families'])&set(a['frame']['families']) for a in src['alternatives']):return 'conflicting'
        requirements=self._requirements_fit(req,src)
        if requirements!='supported':return requirements
        statuses=[]
        for alt in src['alternatives']:
            z=alt['frame'];role=req['role']
            if not set(req['families'])&set(z['families']):statuses.append('conflicting');continue
            if role=='object_structure':
                if not set(req['families'])&set(z['families']):statuses.append('conflicting');continue
                if set(z['kinds'])-set(req['kinds']):statuses.append('conflicting');continue
                if 'equipment_case' in z['families']:
                    whole=req['role_text']+' '+req['scene_text']
                    if re.search(r'\bclosed\b|닫힌|닫혀',whole,re.I):statuses.append('conflicting');continue
                    if not re.search(r'\b(?:interior|inside|recess|cavit)|내부|본체\s*안|홈들',self._positive(whole),re.I):statuses.append('unproven');continue
                statuses.append('supported')
            elif role=='makeup_decoration':
                if set(req['families'])!=set(z['families']):statuses.append('conflicting');continue
                if req['selected_bare']:statuses.append('conflicting');continue
                if z['owner']!='selected_person' and z['owner']!=req['owner']:statuses.append('conflicting');continue
                if z['sides'] and req['sides'] and set(z['sides']).isdisjoint(req['sides']):statuses.append('conflicting');continue
                qr=set(req['regions']);sr=set(z['regions'])
                if z['face_only'] and qr-FACE:statuses.append('conflicting');continue
                region_ok=(bool(qr) and z['generic_region']) or (bool(qr) and qr<=sr) or (bool(qr) and not sr and z['face_only'] and qr<=FACE) or (bool(qr) and sr=={'near_eye'} and qr<={'temple','outer_eye','near_eye'})
                if not region_ok:statuses.append('conflicting' if sr and qr else 'unproven');continue
                if z['motifs'] and not z['generic_design'] and set(z['motifs'])!=set(req['motifs']):statuses.append('conflicting');continue
                if z['colors'] and req['colors'] and set(z['colors']).isdisjoint(req['colors']):statuses.append('conflicting');continue
                if req['removable'] and not z['removable']:statuses.append('unproven');continue
                statuses.append('supported')
            else:
                common=set(req['families'])&set(z['families'])
                if not common:statuses.append('conflicting');continue
                if z.get('actor_sides') and set(z['actor_sides'])!=set(req.get('actor_sides',[])):statuses.append('conflicting' if req.get('actor_sides') else 'unproven');continue
                if z['fixed_umbrella'] and not req['fixed_umbrella']:statuses.append('conflicting');continue
                if z['chair_leg'] and req['backrest'] and not req['chair_leg']:statuses.append('conflicting');continue
                if 'ground_between' in common and not req['two_actors']:statuses.append('conflicting');continue
                # Concrete source supports stay concrete. The generic families
                # bind only the independent request's already supplied members.
                if set(z['surfaces'])-set(req['surfaces']):statuses.append('conflicting');continue
                statuses.append('supported')
        return 'supported' if 'supported' in statuses else 'conflicting' if 'conflicting' in statuses else 'unproven'
