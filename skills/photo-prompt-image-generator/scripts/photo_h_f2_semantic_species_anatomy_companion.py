"""Bounded selected-primary semantic matching; no retrieval/native permission.

All original units, application constraints and complete effects are retained in
source descriptors. Assertions come only from actual positive primary fields.
The class is self-contained for AST integration into the sealed query module.
"""
import re


class Semantic:
    ROLES = {'species_marker', 'anatomical_connection', 'companion_animal'}
    TYPE_RX = {
        'red_fox': r'\bred\s+fox\b|붉은\s*여우',
        'fennec': r'\bfennec(?:\s+fox)?\b|페넥(?:여우)?|사막여우',
        'crane': r'\bcranes?\b|두루미|(?<![가-힣])학(?:의|이|은|을|\s|$)',
        'animal': r'\banimals?\b|동물',
        'raven': r'\b(?:common\s+)?raven\b|큰까마귀',
        'butterfly': r'\bbutterfl(?:y|ies)\b|나비',
        'axolotl': r'\baxolotls?\b|아홀로틀',
        'cat': r'\b(?:cats?|feline)\b|(?:집)?고양이',
        'dog': r'\b(?:dogs?|canine|terriers?)\b|강아지|테리어|(?<![가-힣])개(?:가|의|는|를|와|\s|$)',
        'horse': r'\bhorses?\b|말(?:이|의|과|\s+한|\s*$)',
        'parrot': r'\bparrots?\b|앵무새',
        'heron': r'\bherons?\b|왜가리',
        'dove': r'\bdoves?\b|비둘기',
        'rabbit': r'\brabbits?\b|토끼',
        'bird': r'\b(?:birds?|avian)\b|조류|(?<![가-힣])새(?:의|가|는|와|\s|$)',
        'fox': r'\bfox(?:es)?\b|여우',
        'human': r'\b(?:human|person|people|handler|walker|reader|dancers?)\b|성인|사람|인간|독자|무용수|보호자',
        'plant': r'\b(?:plant|botanical|leaves|leaf|petiole|blossoms?|flowers?|woody\s+branch)\b|식물|잎자루|목질\s*가지|꽃|잎',
    }
    PARENTS = {'red_fox': {'fox', 'animal'}, 'fennec': {'fox', 'animal'},
               'fox': {'animal'}, 'crane': {'bird','animal'}, 'raven': {'bird', 'animal'},
               'bird': {'animal'}, 'parrot': {'bird','animal'}, 'heron': {'bird','animal'}, 'dove': {'bird','animal'}, 'butterfly': {'animal'}, 'axolotl': {'animal'},
               'cat': {'animal'}, 'dog': {'animal'}, 'horse': {'animal'}, 'rabbit': {'animal'}}
    PART_RX = {
        'hoof': r'\b(?:hoofs?|hooves)\b|발굽',
        'mane': r'\bmanes?\b|갈기',
        'ear': r'\b(?:ears?|pinnae?|pinna)\b|귓바퀴|귀',
        'tail': r'\btails?\b|꼬리',
        'bill': r'\b(?:bills?|beaks?)\b|부리',
        'feather': r'\b(?:feathers?|plumage)\b|깃털|깃덮',
        'crest': r'\b(?:crests?|crown\s+(?:feathers?|plumage))\b|머리깃|볏',
        'scale': r'\bscales?\b|비늘',
        'horn': r'\b(?:horns?|antlers?)\b|뿔',
        'fin': r'\bfins?\b|지느러미',
        'shell': r'\b(?:shells?|carapace)\b|등딱지|등껍질',
        'tooth': r'\b(?:tusks?|fangs?)\b|엄니|송곳니',
        'claw': r'\b(?:claws?|talons?)\b|발톱',
        'fur': r'\b(?:fur|pelage)\b|모피|털가죽',
        'throat': r'\bthroat\b|목\s*깃',
        'antenna': r'\bantenna(?:e|s)?\b|더듬이',
        'wing': r'\b(?:wings?|forewing|outer[- ]wing|upper[- ]wing)\b|날개',
        'gill': r'\bgills?\b|아가미',
        'whisker': r'\bwhiskers?\b|수염',
        'arm': r'\b(?:arms?|upper\s+arm|forearm)\b|위팔|아래팔|전완|(?<![가-힣])팔(?:이|을|에|의|로|\s|$)',
        'shoulder': r'\bshoulders?\b|어깨',
        'elbow': r'\belbows?\b|팔꿈치',
        'wrist': r'\b(?:wrists?|carpus|carpal)\b|손목',
        'hand': r'\bhands?\b|(?<![가-힣])손(?:을|이|도|의|에|과|\s|$)|손의\s*기저',
        'leg': r'\b(?:legs?|limbs?|hindleg|foreleg|hindlimb|forelimb)\b|다리|사지',
        'paw': r'\b(?:paws?|hind[- ]?paw|forepaw)\b|뒷발|앞발',
        'hock': r'\bhock\b|발목(?:관절)?',
        'leaf': r'\b(?:leaves|leaf)\b|(?<!꽃)잎(?!자루)',
        'petiole': r'\bpetioles?\b|잎자루',
        'stem': r'\b(?:stems?|branches|branch)\b|줄기|가지',
        'flower': r'\b(?:flowers?|blossoms?)\b|꽃',
    }
    MARKER_PARTS = {'ear','tail','bill','throat','antenna','wing','gill','whisker','hoof','mane',
                    'feather','crest','scale','horn','fin','shell','tooth','claw','fur'}
    SPECIES_INTENT_RX = r'\bspecies[- ](?:defining|specific|diagnostic|identifying)\b|\b(?:species|taxonomic)\s+(?:cues?|markers?|features?|traits?|identification)\b|종(?:의)?\s*(?:식별|구별|고유|특유)|분류학적\s*특징'

    def _species_feature_parts(self, parts, text):
        # Explicit role intent can select any already recognized animal body
        # part. A bare role label without a concrete owner and part cannot.
        selected = set(parts) & self.MARKER_PARTS
        if self._rx(self.SPECIES_INTENT_RX, text):
            selected |= set(parts) - {'leaf','petiole','stem','flower'}
        return selected

    REL_RX = r'\b(?:own|owns|owned|its|has|carries|joined?|joins|connect\w*|attach\w*|continu\w*|articulat\w*|belong\w*|rooted|emerg\w*|meets|separat\w*|cut)\b|자기|같은|속한|속하는|이어|붙어|연결|관절|뿌리|절단|분리'
    COMPANION_RX = r'\b(?:accompan\w*|companions?|companionship|keeping\b.{0,45}\bcompany|staying\s+with)\b|동반|동행|곁을\s*지키|말동무'
    NEG_MERGE_RX = r'\bwithout\s+(?:merg\w*|fus\w*|conflat\w*)[^.!?;\n]*|(?:옆(?:의)?|인접한|다른)\s*(?:앞|뒷)(?:발|다리)(?:과|와)\s*(?:합치|융합하|섞)[^.!?;\n]{0,20}?(?:않는다|않게|말고)'

    def __init__(self, masker):
        self.masker = masker

    @staticmethod
    def _rx(pattern, text):
        return re.search(pattern, text, re.I)

    def _positive(self, text):
        text = str(text)
        if not text.strip():
            return text
        # A prohibited merge has a bounded relation argument. Mask it before
        # a general clause masker can swallow an earlier affirmative route
        # joined by a Korean connective in the same sentence.
        prepared = re.sub(self.NEG_MERGE_RX, lambda m: ' ' * len(m.group()), text, flags=re.I)
        if not prepared.strip():
            return prepared
        positive = self.masker(prepared)
        if not isinstance(positive, str) or len(positive) != len(text):
            raise ValueError('masker must preserve Unicode character offsets')
        chars = list(positive)
        for match in re.finditer(r'“[^”]*”|"[^"\n]*"|‘[^’]*’', text):
            chars[match.start():match.end()] = ' ' * (match.end() - match.start())
        return ''.join(chars)

    def _types(self, text):
        found = set()
        for kind, pattern in self.TYPE_RX.items():
            matches = list(re.finditer(pattern, text, re.I))
            if kind == 'dog':
                matches = [m for m in matches if not (m.group().startswith('개') and
                    self._rx(r'(?:\d+|한|두|세|네|다섯|여섯|일곱|여덟|아홉|열|몇|여러)\s*$', text[:m.start()]))]
            if matches:
                found.add(kind)
        # Adult modifies the named animal in adult butterfly; it does not
        # manufacture an additional human. A bare adult otherwise names a person.
        if self._rx(r'\badult\b', text) and not self._rx(r'\badult\s+(?:butterfly|bird|cat|dog|animal|fox|rabbit|horse)\b', text):
            found.add('human')
        for specific, ancestors in self.PARENTS.items():
            if specific in found:
                found.difference_update(ancestors)
        return found

    def _parts(self, text):
        return {kind for kind, pattern in self.PART_RX.items() if self._rx(pattern, text)}

    def _carrier(self, text):
        if self._rx(r'\b(?:radiograph|x[- ]ray)\b|방사선\s*(?:영상|사진)|엑스레이', text):
            return 'radiograph'
        if self._rx(r'\banatomical\s+(?:diagram|illustration|drawing|chart)\b|해부(?:학)?(?:도|\s*도표|\s*그림)', text):
            return 'diagram'
        return 'physical'

    def _routes(self, text):
        text = re.sub(self.NEG_MERGE_RX, lambda m: ' ' * len(m.group()), text, flags=re.I)
        return {kind for kind, pattern in {
            'hind': r'\bhind(?:limb|leg|paw|[- ](?:limb|leg|paw))?\b|\bhock\b|뒷(?:다리|발)',
            'fore': r'\bfore(?:limb|leg|paw)\b|\bfront\s+(?:limb|leg|paw)\b|앞(?:다리|발)',
        }.items() if self._rx(pattern, text)}

    def _shapes(self, text):
        # Each feature includes its actual part, preventing a triangular
        # composition or broad head from becoming an ear/tail property.
        near = lambda part, shape: self._rx('(?:' + part + r').{0,65}(?:' + shape + ')|(?:' + shape + r').{0,65}(?:' + part + ')', text)
        features = set()
        if near(r'ear|pinna|귀|귓바퀴', r'pointed|triang|뾰족|삼각'): features.add('pointed_ear')
        if near(r'ear|pinna|귀|귓바퀴', r'large|tall|oversized|큰|크다|크며|키\s*큰|크게'): features.add('large_ear')
        if near(r'tail|꼬리', r'thick|bushy|broad|fur.covered|풍성|폭넓'): features.add('bushy_tail')
        if near(r'tail|꼬리', r'wedge|쐐기'): features.add('wedge_tail')
        if near(r'tail|꼬리', r'taper|narrow\w*\s+toward|가늘어'): features.add('taper_tail')
        if near(r'bill|beak|부리', r'long|긴'): features.add('long_bill')
        if self._rx(r'\b(?:curved|hooked)\s+(?:[a-z]+\s+){0,3}(?:beaks?|bills?)\b|\b(?:beaks?|bills?)\s+(?:is|remains?)\s+(?:[a-z]+\s+){0,2}(?:curved|hooked)\b|(?:굽은|갈고리\s*모양)\s*부리', text): features.add('curved_bill')
        if self._rx(r'\bstraight\s+(?:[a-z]+\s+){0,3}(?:beaks?|bills?)\b|곧은\s*부리', text): features.add('straight_bill')
        if near(r'legs?|다리', r'narrow|slender|가느다란|가는'): features.add('narrow_leg')
        if near(r'antenna|더듬이', r'club|swollen|thicken|곤봉|부푼|굵어'): features.add('club_antenna')
        if near(r'gill|아가미', r'branch|feathery|가지|깃털'): features.add('branch_gill')
        return features

    def _colors(self, text):
        # Biological names remain names, never coat-color evidence.
        text = re.sub(self.TYPE_RX['red_fox'], ' ', text, flags=re.I)
        return {c for c, pattern in {'white':r'\bwhite\b|흰색|흰\s', 'black':r'\bblack\b|검은|검정',
            'red':r'\bred\b|빨간|붉은', 'blue':r'\bblue\b|파란', 'green':r'\bgreen\b|초록|녹색'}.items() if self._rx(pattern,text)}

    def _activity(self, text):
        return {name for name, pattern in {
            'overhead':r'\b(?:arms?|hands?).{0,24}(?:above|over)\s+(?:the\s+)?head|머리\s*위.{0,12}(?:팔|손)',
            'chin_contact':r'(?:touch|contacts?|supports?).{0,24}chin|턱.{0,12}(?:닿|받치)',
            'walking':r'\bwalk(?:s|ing)?\b|걷|산책',
            'resting':r'\b(?:rests?|resting|sleep\w*|seated|sits?)\b|쉬|자는|앉',
        }.items() if self._rx(pattern,text)}

    def _features(self, text):
        return {
            'check_in':bool(self._rx(r'look\w*\s+back|turn\w*\s+(?:its|the\s+dog.s)\s+head\s+back|check[- ]in|돌아보|고개.{0,24}(?:사람|성인).{0,16}(?:돌려|돌리)',text)),
            'shoulder':bool(self._rx(r'\bshoulder\b|어깨',text)),
            'perched':bool(self._rx(r'\bperch\w*\b|어깨.{0,16}앉|앉아.{0,16}어깨',text)),
            'shared_travel':bool(self._rx(r'\b(?:travell?ing\s+companion|shared\s+(?:walk|travel|direction\s+of\s+travel)|both\s+(?:already\s+)?walking)\b|함께\s*걷|같이\s*걷|공통\s*진행\s*방향|인간\s*동행자',text)),
        }

    def _witnesses(self, text, pattern, pointer):
        return [{'pointer':pointer,'start':m.start(),'end':m.end(),'quote':text[m.start():m.end()]}
                for m in re.finditer(pattern, self._positive(text), re.I)]

    def request(self, role, text):
        if role not in self.ROLES:
            return None
        match = re.search(r'^Photographic role:[ \t]*(.*?)(?=\nScene context:|\Z)', text, re.S)
        focus = match.group(1) if match else text
        scene = text[match.end():] if match else ''
        positive = self._positive(focus)
        # These negatives are predicates about this role, not a ban on every
        # ordinary result or proof that a neighboring animal is absent.
        if self._rx(r'동물\s*동반자.{0,10}없는|동물은\s*없|without\s+an?\s+animal\s+companion',focus):
            return None
        route_focus = re.sub(self.NEG_MERGE_RX, lambda m:' '*len(m.group()),positive,flags=re.I)
        types = self._types(positive)
        parts = self._parts(route_focus)
        carrier = self._carrier(positive)
        scene_positive = self._positive(scene)
        if role == 'species_marker':
            if self._rx(r'costume|headband|accessor|머리띠|코스튬|의상\s*소품|울\s*코트|칼라',positive):return None
            if not (types - {'human','plant'}) or not self._species_feature_parts(parts, positive):return None
            # A requested human handler remains human even with a fox mentioned
            # later as the independently owned background animal.
            human = self._rx(self.TYPE_RX['human'],positive)
            animal = self._rx('|'.join(v for k,v in self.TYPE_RX.items() if k not in {'human','plant'}),positive)
            if human and animal and human.start() < animal.start():return None
        elif role == 'anatomical_connection':
            if not self._rx(self.REL_RX,positive) or not parts:return None
            explicit_route = self._rx(r'anatomical\s+(?:route|connection|continuity)|\b(?:joint|articulat\w*|joins?|connect\w*|attach\w*|continu\w*|traceable)\b|\bcut\s+between\b|\bseparate\s+endpoints\b|연결|이어|관절|절단|분리|붙어',positive)
            if not explicit_route:return None
            if self._rx(r'paper\s+(?:flower|blossom)|종이꽃|metal\s+(?:fan|rib)|금속\s*.*부채|mannequin|마네킹',positive):return None
            # Existing identifying ears/gills plus the word anatomy do not
            # create a joint route or a botanical endpoint request.
            if parts <= self.MARKER_PARTS and not self._rx(r'joint|shoulder|articulat|관절|어깨',positive):return None
            if carrier == 'diagram' and not types.intersection({'cat','dog','bird'}):types.add('human')
            if not types:types = self._types(scene_positive)
            if not types:return None
        else:
            if not self._rx(self.COMPANION_RX,positive):return None
            if self._rx(r'poster|printed\s+text|memory|remembered|포스터|사진첩|기억',positive):return None
            if not types.intersection(set(self.PARENTS)|{'bird','fox'}):
                types |= self._types(scene_positive)
            if not types.intersection(set(self.PARENTS)|{'bird','fox','animal'}):return None
            # A generic role definition is not a scene declaration. Two counted
            # existing animal companions identify both real participants without
            # inventing a human or choosing their species.
            if types == {'animal'} and not self._rx(r'\b(?:two|2)\s+(?:separately\s+)?(?:already\s+)?declared\s+(?:companion\s+)?animals\b|별도로\s*선언된\s*(?:두|2)\s*(?:동물\s*동반자|동반\s*동물)',positive):return None
        pattern = self.COMPANION_RX if role=='companion_animal' else self.REL_RX+'|'+'|'.join(self.PART_RX.values())
        witnesses = self._witnesses(focus,pattern,'/role_focus')
        descriptor = {'role':role,'prefer_role':role,'asserts':True,'witnesses':witnesses,
            'types':sorted(types),'parts':sorted(parts),'routes':sorted(self._routes(positive)),
            'carrier':carrier,'shapes':sorted(self._shapes(positive)),
            'colors':sorted(self._colors(positive+' '+scene_positive)),
            'activity':sorted(self._activity(positive+' '+scene_positive)),
            'features':self._features(positive+' '+scene_positive),
            'focus':focus,'positive_focus':positive,'scene':scene,
            'scene_types':sorted(self._types(scene_positive)),
            'native_approval':False}
        descriptor['separation']=bool(self._rx(r'\b(?:detached|disconnected|severed|unattached|removed\s+(?:botanical\s+)?leaf|cut\s+between)\b|절단|떼어낸|분리된\s*두\s*끝',positive))
        if role=='companion_animal':
            # The positive role names the animal then its identified counterpart.
            animal_types=types-{'human','plant'}
            primary_types={'human'} if 'human' in types else set()
            if 'horse' in types and 'dog' in types:
                animal_types={'dog'};primary_types={'horse'}
            if not primary_types:
                primary_types=self._types(scene_positive)-animal_types-{'plant'}
            if types == {'animal'}:
                primary_types={'animal'}
            descriptor.update(animal_types=sorted(animal_types),primary_types=sorted(primary_types),
                companion_declared=True)
        return descriptor

    def source(self, role, units, effects):
        if role not in self.ROLES:return None
        facts=[];constraints=[]
        for unit in units:
            pointer=unit.get('pointer','');raw=unit.get('text','')
            if not isinstance(raw,str):continue
            if 'application_contract' in pointer or 'contextual_usage' in pointer:
                constraints.append(dict(unit));continue
            if re.search(r'/content/(?:en$|ko$|definition$|concept_units(?:/|$)|semantic_relations(?:/|$)|semantics/(?:definition|visual_components)|composition_instruction$|components/)',pointer):
                facts.append(dict(unit))
        positive='\n'.join(self._positive(u['text']) for u in facts)
        raw='\n'.join(u['text'] for u in facts)
        guard_text='\n'.join(u['text'] for u in constraints)
        types=self._types(positive);parts=self._parts(positive)
        carrier=self._carrier(positive)
        relation=bool(self._rx(self.REL_RX,positive))
        evidence=[]
        pattern=self.COMPANION_RX if role=='companion_animal' else self.REL_RX+'|'+'|'.join(self.PART_RX.values())
        for u in facts:
            spans=self._witnesses(u['text'],pattern,u['pointer'])
            if spans:evidence.append({**u,'matches':spans})
        desc={'role':role,'asserts':False,'types':sorted(types),'parts':sorted(parts),
            'routes':sorted(self._routes(positive)),'carrier':carrier,
            'shapes':sorted(self._shapes(positive)),'colors':sorted(self._colors(positive)),
            'activity':sorted(self._activity(positive)),'features':self._features(positive),
            'evidence':evidence,'units':list(units),'application_constraints':constraints,
            'complete_effects':effects,'positive_primary':positive,'raw_primary':raw,
            'native_approval':False,'guard_check_required':True}
        allowed_effect_prefixes={
            'species_marker':('species.','body.species','body.ear_structure','body.tail','body.fur.','body.plumage.'),
            'anatomical_connection':('body.connection','body.topology','anatomy.connection','topology.','botanical.structure','leaf.surface_finish'),
            'companion_animal':('companion.animal.','participant.animal.','head.orientation','body.perched_configuration'),
        }[role]
        # A convenient relation cannot donate permission for a wider pose,
        # composition, inventory or other receiver mutation. This is a
        # conservative withholding check, never positive semantic evidence.
        desc['unmodeled_effects']=[p for p in effects.get('properties',[])
            if not p.get('property','').startswith(allowed_effect_prefixes)]
        desc['separation']=bool(self._rx(r'\b(?:detached|disconnected|severed|unattached|cut\s+end)\b|절단|떼어낸|분리되어',positive))
        if not facts or not evidence:return desc
        if role=='species_marker':
            bodyparts=self._species_feature_parts(parts, positive)
            artifact=bool(self._rx(r'headband|necklace|bodice|costume|ornament|brooch|charm|motif|embroider|animal[- ]shaped|butterfly[- ]shaped|머리띠|목걸이|보디스|코스튬|나비\s*모양\s*장식',positive))
            desc['asserts']=bool(types-{'human','plant'} and bodyparts and relation and not artifact)
        elif role=='anatomical_connection':
            botanical='plant' in types and bool(parts & {'leaf','petiole','flower','stem'})
            anatomical=bool(parts & {'arm','shoulder','elbow','wrist','hand','leg','paw','hock','wing'})
            route_relation=bool(self._rx(r'\b(?:joins?|joined|connect\w*|attach\w*|continu\w*|articulat\w*|belongs?\s+to|traceable|separat\w*|cut)\b|연결|이어|붙어|관절|속한|절단|분리',positive))
            desc['asserts']=bool(route_relation and (botanical or anatomical) and types)
            if self._rx(r'paper\s+flowers?|silk\s+flowers?|fabric\s+rosette|종이꽃|직물\s*꽃|조화',positive):desc['asserts']=False
        else:
            relation=bool(self._rx(self.COMPANION_RX,positive))
            variable_primary=bool(self._rx(r'primary\s+(?:may|can)\s+be\s+human\s+or\s+nonhuman|no\s+physical\s+touch,\s*human\s+primary|인간\s*주\s*대상[^.!?\n]{0,90}요구하지\s*않',raw))
            variable_animal=bool(self._rx(r'(?:existing|declared)\s+animal\s+companion|independently\s+declared\s+animal\s+accompanies|기존\s*동물\s*동반자',positive))
            animal_types=types-{'human','plant'}
            primary_types={'human'} if 'human' in types and not variable_primary else set()
            mandatory_human=bool(self._rx(r'\b(?:require|requires)\b[^.!?\n]{0,90}\b(?:existing\s+)?human\s+primary\b|반드시[^.!?\n]{0,30}인간\s*주\s*대상',guard_text))
            if mandatory_human:
                variable_primary=False
                primary_types={'human'}
            if not primary_types and not variable_primary and types=={'bird'}:primary_types={'bird'}
            features=desc['features']
            explicit_preserve=bool(self._rx(r'preserv\w*|retain\w*|keeps?\s+its\s+established|유지|보존',positive+'\n'+guard_text))
            desc.update(primary_variable=variable_primary,animal_variable=variable_animal,
                animal_types=sorted(animal_types),primary_types=sorted(primary_types),
                activity_parameter=explicit_preserve,
                requires_shared_travel=features['shared_travel'] or bool(self._rx(r'share\s+travel\s+context',guard_text)),
                requires_both_walking=bool(self._rx(r'both\s+(?:are\s+)?(?:already\s+)?walking|human\s+and\s+dog\s+must\s+already\s+be\s+walking|이미\s*걷고',raw+'\n'+guard_text)),
                prior_relation_required=bool(self._rx(r'(?:declared|existing|identified).{0,65}(?:companion|accompan)|선언된\s*동반\s*관계|기존\s*동물\s*동반자',positive+'\n'+guard_text)))
            desc['asserts']=bool(relation and (animal_types or variable_animal) and (primary_types or variable_primary) and desc['prior_relation_required'])
        return desc

    def _type_fits(self, required, declared):
        entailed=set(declared)
        for kind in list(entailed):entailed.update(self.PARENTS.get(kind,set()))
        return set(required).issubset(entailed)

    def fit(self, req, src):
        if not req or not src or req.get('role')!=src.get('role'):return 'unproven'
        if not src.get('asserts'):return 'unproven'
        if src.get('unmodeled_effects'):return 'unproven'
        role=req['role']
        if role in {'species_marker','anatomical_connection'}:
            if req['carrier']!=src['carrier']:return 'conflicting'
            required_types=set(src['types'])
            if not self._type_fits(required_types,req['types']):return 'conflicting'
            if src.get('separation') and not req.get('separation'):return 'conflicting'
            # Full extra source actions and fixed colors must not be imported
            # from an unrelated bundle merely to borrow its anatomical clause.
            if src['colors'] and req['colors'] and set(src['colors']).isdisjoint(req['colors']):return 'conflicting'
            if set(src['colors'])-set(req['colors']):return 'unproven'
            if set(src['activity'])&{'overhead','chin_contact'}-set(req['activity']):return 'conflicting'
            wanted_routes=set(req['routes']);found_routes=set(src['routes'])
            if wanted_routes and found_routes and wanted_routes.isdisjoint(found_routes):return 'conflicting'
            if wanted_routes-found_routes:return 'unproven'
            if not set(req['parts']).issubset(set(src['parts'])):return 'unproven'
            if not set(req['shapes']).issubset(set(src['shapes'])):return 'unproven'
            # Intentional separation is a physical predicate, not a species or
            # vague continuity synonym. Preserve both explicit endpoints.
            sep_pattern=r'cut\s+between|separate\s+endpoints|removed\s+leaf|절단|분리된\s*두\s*끝'
            if self._rx(sep_pattern,req['positive_focus']) and not self._rx(sep_pattern,src['positive_primary']):return 'unproven'
            return 'supported'
        if not req.get('companion_declared'):return 'unproven'
        if not src.get('animal_variable') and not self._type_fits(src.get('animal_types',[]),req.get('animal_types',[])):return 'conflicting'
        if not src.get('primary_variable') and not self._type_fits(src.get('primary_types',[]),req.get('primary_types',[])):return 'conflicting'
        if not src.get('primary_variable') and not req.get('primary_types'):return 'unproven'
        rf=req['features'];sf=src['features']
        # A source's directed check-in or shoulder perch is a complete
        # additional relation, not a fragment to borrow for mere accompaniment.
        if sf['check_in'] and not rf['check_in']:return 'unproven'
        if sf['perched'] and not rf['perched']:return 'unproven'
        if rf['check_in'] and not sf['check_in']:return 'unproven'
        if rf['shoulder'] and rf['perched'] and not (sf['shoulder'] and sf['perched']):return 'unproven'
        walking='walking' in req['activity']
        if src.get('requires_both_walking') and not walking:return 'unproven'
        if src.get('requires_shared_travel') and not (walking or rf['shared_travel']):return 'unproven'
        if src['colors'] and set(src['colors'])-set(req['colors']):return 'unproven'
        return 'supported'
