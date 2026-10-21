"""Bounded source-witnessed semantics. No IDs, query fixtures or data mutations.

Inputs are original request text, actual selected primary units and canonical
actual effects. Conditions remain the caller's separate, cumulative authority.
This helper never grants native approval or verifies rendered realization.
"""
import re

class Semantic:
    def __init__(self, masker):
        self.masker = masker

    def _pos(self, text):
        value = self.masker(text)
        chars = list(value)
        # Predicate-scoped rejection; preserve the earlier affirmative clause.
        for m in re.finditer(r'\bgeneric\b[^.;!\n]{0,140}\b(?:do|does)\s+not\s+(?:establish|constitute|prove|define)\b[^.;!\n]*|[^.;!\n]{0,100}?\balone\b[^.;!\n]{0,35}\b(?:does?\s+not|cannot)\b[^.;!\n]*',value,re.I):
            chars[m.start():m.end()] = ' '*(m.end()-m.start())
        for m in re.finditer(r'\b(?:rejects?|refuses?|renounces?|excludes?)\b[^.;!\n]*', value, re.I):
            chars[m.start():m.end()] = ' '*(m.end()-m.start())
        for m in re.finditer(r'[^.;!\n,]*?(?:거부한다|거부하며|배제한다|제외하고|제외하며|하지\s*않는다|지정하지\s*않았다)', value):
            chars[m.start():m.end()] = ' '*(m.end()-m.start())
        return ''.join(chars)

    @staticmethod
    def _w(text, pattern):
        return [{'start':m.start(),'end':m.end(),'quote':text[m.start():m.end()]} for m in re.finditer(pattern,text,re.I)]

    @staticmethod
    def _families(text):
        ps = {
          'minimal':r'\bminimal(?:is\w*)?\b|미니멀|monochrome\s+architectural(?=[^.;!\n]{0,110}\bfew\b[^.;!\n]{0,45}\b(?:planes?|planar\s+forms?)\b)',
          'geometry':r'geometric.{0,28}(?:modern|photograph)|기하학.{0,20}(?:모더니즘|사진)|기하적.{0,15}(?:사진|미학)',
          'typology':r'typolog\w*|유형학',
          'straight':r'straight[- ]photograph\w*|스트레이트\s*사진',
          'pictorial':r'pictorial\w*|painterly\s+photographic|회화주의|회화적\s*(?:사진|세부|처리)',
          'chromatic':r'chromatic\s+relationships?|colou?r\s+fields?|areas?\s+of\s+colou?r|색의\s*관계|넓은\s*색면|색면.{0,20}(?:조직|미학)|컬러\s*블로킹',
        }
        return {k for k,p in ps.items() if re.search(p,text,re.I)}

    @staticmethod
    def _carriers(text):
        ps = {
          'water':r'\bwater\b|물줄기|(?<![가-힣])물(?:이|을|은|의|\s)',
          'liquid':r'\bliquid\b|액체', 'flame':r'\bflame\b|불꽃|화염|촛불',
          'gel':r'\bgel\b|젤', 'paste':r'\bpaste\b|페이스트',
          'wax':r'\bwax\b|왁스|밀랍', 'dough':r'\bdough\b|반죽',
          'honey':r'\bhoney\b|꿀', 'oil':r'\boil\b|기름',
          'smoke':r'\bsmoke\b|연기', 'foam':r'\bfoam\b|거품',
          'cream':r'\bcream\b|크림', 'clay':r'\bclay\b|점토',
          'resin':r'\bresin\b|수지',
        }
        return {k for k,p in ps.items() if re.search(p,text,re.I)}

    def request(self, role, text):
        m = re.search(r'^Photographic role:[ \t]*(.*?)(?=\nScene context:|\Z)',text,re.S)
        focus = m.group(1) if m else text
        pos = self._pos(focus); context = self._pos(text)
        evidence = []
        req = {'role':role,'asserts':True,'focus':focus,'positive':pos,'context':context,'native_approval':False}
        if role == 'subject_identity':
            pattern = r'\b(?:principal|primary|main)\s+(?:(?:declared|visible|observed|physical|photographic)\s+){0,2}(?:subject|entity|object|person|animal|plant)\b|central\s+(?:object|entity|subject)\s+of\s+interest|(?:photograph|photo|image).{0,30}(?:main|primary)\s+attention|what\s+(?:this|the)\s+(?:photograph|photo|image)\s+is\s+about|\bsubject\s+is\b|(?:주된|주요|주)\s*(?:가시적(?:인)?\s*)?(?:피사체|대상|인물|개체|물체)|관심(?:의)?\s*중심.{0,12}(?:물체|대상)|주로\s*관찰하는\s*대상|사진(?:의)?\s*주된\s*관심|피사체(?:은|는|이|가)'
            evidence = self._w(pos,pattern)
            if re.search(r'number of|count of|how many|피사체\s*수|몇\s*(?:명|개)',pos,re.I):return None
            main = re.split(r';|,\s*with\b|\bwith\b|;|이며\s*(?=.+(?:동반|배경))',pos,maxsplit=1,flags=re.I)[0]
            # Background/companion clauses never identify the principal entity.
            main = re.split(r'\s+(?:동반\s*동물|배경\s*장비)',main,maxsplit=1)[0]
            req['main_scope'] = main
            req['representation'] = bool(re.search(r'paper label|printed word|ceramic sculpture|sculpture|drawing|painting|carving|embroidered|embroidery|인쇄된\s*영상|그림|자수|조각|종이\s*라벨|인쇄된\s*단어|조각',main,re.I))
        elif role == 'aesthetic_practice':
            families = self._families(pos)
            style = r'visual\s+practice|photograph\w*\s+(?:aesthetic|practice|treatment)|aesthetic|사진\s*(?:미학|미감|관습)|회화주의|색의\s*관계.{0,50}사진.{0,25}미학'
            evidence = self._w(pos,style)
            if not families or not evidence:return None
            # Affiliation belongs to catalog/artist, not to the enclosing image.
            if re.search(r'(?:catalog|biograph|도록).{0,60}(?:declares|belongs|소속|속한다고|선언)',pos,re.I):return None
            req['families'] = sorted(families)
            req['series'] = bool(re.search(r'photographic series|photo(?:graph)? series|사진\s*(?:연작|연속|시리즈)',context,re.I))
            req['physical_print'] = bool(re.search(r'(?:existing|actual|physical)\s+(?:print|mount)|실제\s*(?:인화물|마운트)|기존\s*인화물',context,re.I))
        elif role == 'material_form':
            owner_clause = re.split(r';|\bbeside\b|\bnext to\b|\bnear\b|,\s*while\b',pos,maxsplit=1,flags=re.I)[0]
            carriers = self._carriers(owner_clause)
            shape = r'\b(?:body|silhouette|outline|contour|shape|volume|mound|pool|rope|ribbon|strand|bridge|coil|arch|dome|rim|crest|tip|lobe|spiral)\b|몸체|윤곽|형상|형태|부피|더미|웅덩이|덩어리|아치|나선|코일|가장자리|꼭대기|엽상|타원'
            predicate = r'\b(?:give|choose|shape|develop|arrange|keep|forms?|spans?|extends?|swells?|tapers?|narrows?)\b|만들|고른|구성|놓고|유지|보이게|부풀|가늘어|이어지|되게'
            evidence = self._w(pos,shape)
            if not carriers or not evidence or not re.search(predicate,pos,re.I):return None
            if re.search(r'(?:ceramic|rigid|glass|metal|wooden)\s+(?:jug|vessel|container|bottle)|(?:도자기|단단한|유리|금속|목제)\s*(?:주전자|용기|병|그릇)|벽에\s*비친\s*빛|빛(?:의)?\s*영역|patch\s+of\s+light|projected\s+light|flame[’\']s\s+(?:shadow|reflection)|(?:flame|liquid).{0,12}(?:drawing|photograph)',owner_clause,re.I):return None
            # A material mentioned inside another owner's clause cannot
            # transfer that owner's contour to the contained material.
            alien_prefix = re.match(r'^(?:a|an|the|one)\s+[^.;!\n]{0,65}?\b(?:spoon|jar|vessel|container|bottle|chair|lamp|garment|sleeve|hand|finger|drawing|diagram|photograph|painting|label)\b',owner_clause,re.I)
            if alien_prefix and self._carriers(owner_clause[alien_prefix.end():]) and not self._carriers(owner_clause[:alien_prefix.end()]):return None
            req['carriers']=sorted(carriers)
            req['existing_body']=any(re.search(r'existing|already|이미|기존',clause,re.I) and bool(self._carriers(clause)&carriers) for clause in re.split(r'[.!?;\n]',context))
            # An affirmative actual-body proposition supplies its own owner.
            # Material existence is not dependent on one English keyword.
            # Generic requests about possible forms still lack a carrier.
            affirmative_body = bool(re.search(r'^(?:a|an|the|one)\s+[^.;!\n]{0,90}\b(?:forms?|spans?|extends?)\b',owner_clause,re.I))
            delimited_body = bool(re.search(r'\bshape\s+(?:a|an|the|one)\s+',owner_clause,re.I) and re.search(r'\b(?:ribbon|strand|body|mass|mound|pool|bridge)\b',owner_clause,re.I) and re.search(r'\b(?:between|from|onto|across)\b',owner_clause,re.I))
            if (affirmative_body or delimited_body) and not re.search(r'\b(?:hypothetical|possible|concept|drawing|diagram|label)\b',owner_clause,re.I):
                req['existing_body']=True
            req['body_declaration_mode']='positive_owned_proposition' if affirmative_body or delimited_body else 'independent_context'
            req['desired_shape']=pos
            req['shape_effect_mode']='requested_not_observed'
        else:return None
        if not evidence:return None
        # Witnesses address the literal original role field, never derived prose.
        req['witnesses']=[{**w,'quote':focus[w['start']:w['end']]} for w in evidence]
        req['focus_offset']=m.start(1) if m else 0
        return req

    def source(self, role, units, effects):
        # Keep every actual unit/constraint; only ordinary positive meaning fields
        # vote for the family. Application clauses remain cumulative constraints.
        semantic=[u for u in units if re.match(r'^/content/(?:en$|ko$|definition$|embedding_text$|concept_units/\d+$|semantic_relations/)',u.get('pointer',''))]
        if not semantic:return None
        texts=[self._pos(u['text']) for u in semantic];joined='\n'.join(texts)
        src={'role':role,'evidence':semantic,'all_units':list(units),'effects':effects,'constraints':[u for u in units if u.get('pointer')=='/content/application_contract'],'native_approval':False}
        if role=='subject_identity':
            if 'subject' not in effects.get('dimensions',[]) and not any(p.get('property','').startswith(('entity.','subject.')) for p in effects.get('properties',[])):return None
            identities=[]
            for u in semantic:
                t=self._pos(u['text']).strip()
                if u['pointer'] not in ('/content/en','/content/ko'):continue
                en=re.match(r'^(?:A|An|The)\s+(.{1,90}?)\s+(?:is|has|owns|forms)\b',t,re.I)
                if en:identities.append(en.group(1))
                elif re.match(r'^(?:a|an|the)\s+[\w -]+$',t,re.I) and len(t.split())<=7:identities.append(re.sub(r'^(?:a|an|the)\s+','',t,flags=re.I))
                ko=re.match(r'^(.{1,50}?)(?:은|는|이|가)\s',t)
                if ko:
                    key=self._identity_key(ko.group(1))
                    # An adjectival 가는 is not noun 가 + topic 는. Keep
                    # unknown one-syllable clause fragments review-required.
                    if len(re.sub(r'\s+','',key))>=2 and not re.search(r'\S+(?:을|를|에서|으로)\s',key):identities.append(ko.group(1))
                elif re.fullmatch(r'[가-힣 -]{2,24}',t):identities.append(t)
            if not identities:return None
            src['identities']=identities
            src['representation']=bool(re.search(r'paper label|sculpture|printed image|종이\s*라벨|조각|인쇄된\s*영상',joined,re.I))
        elif role=='aesthetic_practice':
            fam=self._families(joined)
            color=bool(re.search(r'(?:large|broad).{0,25}color\s+fields?.{0,40}organiz.{0,30}composition',joined,re.I) and re.search(r'photographic.{0,20}shading|depth\s+cues',joined,re.I))
            pict=bool(re.search(r'fine.{0,20}detail.{0,45}soft\s+tonal\s+masses',joined,re.I) and re.search(r'subject\s+geometry.{0,25}photographic\s+light.{0,25}legible',joined,re.I))
            if color:fam.add('chromatic')
            if pict:fam.add('pictorial')
            # A movement name or fashion/architecture label cannot replace
            # the connected photographic practice actually requested. Every
            # source relation remains field-local and owner-scoped below.
            photo=bool(re.search(r'photograph\w*|사진',joined,re.I))
            connected={
                'minimal':photo and bool(re.search(r'contour|outline|silhouette|윤곽',joined,re.I)) and bool(re.search(r'spac|interval|surrounding area|간격|공간',joined,re.I)) and bool(re.search(r'tonal|colou?r|계조|명도|색',joined,re.I)) and bool(re.search(r'hierarchy|subordinate|dominant|main relationships|위계|덜\s*두드러|중심',joined,re.I)),
                'geometry':photo and bool(re.search(r'recurr|repeat|되풀이|반복',joined,re.I)) and bool(re.search(r'rhythm|picture edges|리듬|화면\s*가장자리',joined,re.I)) and bool(re.search(r'volume|shading|입체|음영',joined,re.I)),
                'typology':photo and bool(re.search(r'consistent|comparable|일관|비교\s*가능',joined,re.I)) and bool(re.search(r'across|among photographs|사진들?\s*사이|연작',joined,re.I)) and bool(re.search(r'specimen|표본',joined,re.I)),
                'straight':photo and bool(re.search(r'precise|readable.*detail|정밀|읽을\s*수\s*있는\s*표면',joined,re.I)) and bool(re.search(r'structur|contours|구조|윤곽',joined,re.I)) and bool(re.search(r'tonal|volume|계조|입체',joined,re.I)),
                'chromatic':color, 'pictorial':pict,
            }
            fam={f for f in fam if connected.get(f,False)}
            if not fam:return None
            src['families']=sorted(fam)
            src['whole_color_relation']=color
            src['soft_tonal_relation']=pict
            src['series_required']=bool(re.search(r'independently\s+declared\s+photographic\s+series|독립적으로\s*선언된\s*사진\s*연작',joined,re.I))
            src['physical_print_required']=bool(re.search(r'hand[- ]worked.{0,30}(?:print|mount)|손작업.{0,20}(?:인화|마운트)',joined,re.I))
            src['artifact_only']=bool(re.search(r'displayed\s+artifact|mounted\s+design|depicted\s+paper|작품의\s*평면|걸린\s*도안',joined,re.I))
            # Intrinsic positive owners are not erased by empty conditions.
            src['added_owner_scope']=bool(set(effects.get('dimensions',[]))&{'subject','count','setting'})
            source_properties={p.get('property','') for p in effects.get('properties',[])}
            required=[]
            if 'subject.functional_object' in source_properties:
                required=[r'functional object|기능성\s*물체',r'floor.{0,25}wall|바닥.{0,20}벽']
            if 'subject.everyday_vessel' in source_properties:
                required=[r'vessel|vase|jug|bowl|용기|주전자|꽃병|그릇',r'backdrop|background|배경',r'contact shadow|접촉\s*그림자',r'support(?:ing)? surface|tabletop|table|받침|탁자|테이블']
            src['required_owner_patterns']=required
            src['joined']=joined
        elif role=='material_form':
            preservation=bool(re.search(r'(?:independently|supplied).{0,70}(?:contour|shape)|(?:contour|shape).{0,70}independently',joined,re.I) and re.search(r'same.{0,30}(?:body|carrier)|같은.{0,15}(?:몸체|주체)',joined,re.I) and re.search(r'preserv|retain|keeps?|유지',joined,re.I))
            props=[p.get('property','') for p in effects.get('properties',[])]
            if not preservation and not any(p.startswith(('matter.form','matter.volume_shape','matter.contour')) for p in props):return None
            src['parameter_preservation']=preservation;src['carriers']=sorted(self._carriers(joined));src['joined']=joined
            src['fixed_shape']='sagging' if re.search(r'bows downward|middle hangs lower|아래로\s*휜|낮게\s*늘어',joined,re.I) else 'necked' if re.search(r'slim waist|concave.{0,30}middle|가는\s*허리',joined,re.I) else 'coiled_deposit' if re.search(r'upper strand|receiving material|위쪽\s*가닥',joined,re.I) else 'fixed'
        else:return None
        return src

    @staticmethod
    def _identity_key(value):
        value=re.sub(r'\b(?:declared|existing|independently|actual|wooden|ceramic|sheet-metal|mechanical|adult|living|mature|gnarled|twisted|recognizable)\b',' ',value,flags=re.I)
        value=re.sub(r'\bcontaining\s+(?:a|an|one)\s+', 'containing ',value,flags=re.I)
        value=re.sub(r'(?:선언된|기존의?|이미|목재|판금|기계식|성인|울퉁불퉁한|살아\s*있는)',' ',value)
        return ' '.join(value.split()).casefold()

    def fit(self, req, src):
        if not req or not src or req.get('role')!=src.get('role'):return 'unproven'
        role=req['role']
        if role=='subject_identity':
            if bool(req.get('representation')) != bool(src.get('representation')):return 'conflicting'
            main=self._identity_key(req['main_scope'])
            for raw in src['identities']:
                key=self._identity_key(raw)
                if not key:continue
                if re.search(r'[가-힣]',key):
                    if len(re.sub(r'\s+','',key))<2:continue
                    boundary=r'(?=$|[\s.,;!?]|(?:은|는|이|가|을|를|의|에|와|과|로|으로|다|이다)(?=$|[\s.,;!?]))'
                    match=re.search(r'(?<![가-힣])'+re.escape(key)+boundary,main,re.I)
                else:match=re.search(r'(?<![a-z])'+re.escape(key)+r'(?![a-z])',main,re.I)
                if match:return 'supported'
            return 'unproven'
        if role=='aesthetic_practice':
            wanted=set(req['families']);found=set(src['families'])
            if not wanted&found:return 'conflicting'
            if src['artifact_only']:return 'unproven'
            if src['series_required'] and not req['series']:return 'unproven'
            if src['physical_print_required'] and not req['physical_print']:return 'unproven'
            if src['added_owner_scope']:
                required=src.get('required_owner_patterns',[])
                if not required or not all(re.search(p,req['context'],re.I) for p in required):return 'unproven'
            if 'chromatic' in wanted and not src['whole_color_relation']:return 'unproven'
            if 'pictorial' in wanted and not src['soft_tonal_relation']:return 'unproven'
            return 'supported'
        if role=='material_form':
            if not req.get('existing_body'):return 'unproven'
            if src.get('parameter_preservation'):
                # Scope is positively supplied by this exact role field and its
                # independently declared existing carrier; no caller assertion
                # or query-copy candidate is used to manufacture this relation.
                return 'supported'
            request=set(req['carriers']);source=set(src['carriers'])
            allowed=request|({'liquid'} if request&{'water','oil','honey'} else set())
            if source and not source&allowed:return 'conflicting'
            desired=req['desired_shape']
            if src['fixed_shape']=='sagging' and re.search(r'arch|아치',desired,re.I):return 'conflicting'
            if src['fixed_shape']=='necked' and re.search(r'narrows? at both ends|양끝.{0,25}가늘',desired,re.I):return 'conflicting'
            # A related fixed family cannot entail the complete independently
            # supplied contour. It remains reviewable rather than target proof.
            return 'unproven'
        return 'unproven'
