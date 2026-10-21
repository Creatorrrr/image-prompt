"""Conservative, source-witnessed ordering for an explicit inscription literal.

This is advisory retrieval ordering, never native eligibility or permission to
rewrite a fixed source word. Raw BM25F/cosine and their RRF10 remain intact.
Unsupported language, ambiguous multiple literals, or missing carrier evidence
retain the original order. No candidate IDs or slot names are decision inputs.
"""
import hashlib
import re

RECIPE = 'photo-h-f2-carried-literal-order/v2'
_MARKER = re.compile(r'\bexact\s+(?:word|phrase|letters|numerals|text)\s+', re.I)
_QUOTES = {'"': '"', "'": "'", '“': '”', '‘': '’'}
_STOP = frozenset('a an the its their already declared requested supplied specified same existing of'.split())
_CARRIER = re.compile(r'\b(?:on|across)\s+(?P<carrier>.+?)(?=[.;,\n]|\s+(?:with|while|through|and|in|inside|within|as)\b|$)', re.I)
_FIXED = re.compile(r'\b(?:carries|reads|says|spells|bears|displays)\s+(?P<value>"[^"\n]+"|“[^”\n]+”|\x27[^\x27\n]+\x27|[A-Z\d][A-Z\d]*(?:[ -][A-Z\d]+)*)(?=\s+(?:in|on|across|as|with|at|from)\b|[.;,]|$)')
_TEXT = re.compile(r'\b(?:inscription|lettering|letters|word|text|numerals|character sequence)\b', re.I)
_DECLARED = re.compile(r'\b(?:already declared|requested|supplied|specified)\s+(?:inscription|lettering|text)\b', re.I)
_RETAIN = re.compile(r'\b(?:retains?|preserves?|keeps?)\b', re.I)
_SEQUENCE = re.compile(r'\b(?:complete character sequence|exact (?:text|wording|character sequence))\b', re.I)
_CASE = re.compile(r'\b(?:capitalization|letter case|case)\b', re.I)

def _span(text, start, end):
    return {'start': start, 'end': end, 'quote': text[start:end]}

def _negative(prefix):
    # Fail closed on explicit negative/alternative contexts. No truth inference.
    return bool(re.search(r'\b(?:not|never|without|rather than|instead of)\b', prefix, re.I))

def _carrier(text, offset, tokenize):
    found = _CARRIER.search(text, offset)
    if found is None:
        return None
    start, end = found.span('carrier')
    words = [x for x in tokenize(text[start:end]) if x not in _STOP]
    # A terminal generic surface names the bearing face of the preceding
    # carrier, not a new object named "surface". Keep the full original quote.
    # Named parts such as panel/pane and reversed noun order remain distinct.
    if words and words[-1] == 'surface':
        words = words[:-1]
    if len(set(words)) < 2:
        return None
    return {**_span(text, start, end), 'terms': words, 'head': words[-1]}

def request(text, scope, tokenize):
    matches = list(_MARKER.finditer(text))
    if len(matches) != 1:
        return None
    match = matches[0]
    # Only a positive direct assertion, outside a quoted sentence or comparison.
    if not any(r['start'] <= match.start() < r['end'] for r in scope['positive_spans']):
        return None
    from photo_h_f2_query_scope import _quoted
    if any(a <= match.start() < b for a, b in _quoted(text)):
        return None
    boundary = max(text.rfind(c, 0, match.start()) for c in '.;!?\n')
    if _negative(text[boundary + 1:match.start()]):
        return None
    start = match.end()
    if start >= len(text):
        return None
    if text[start] in _QUOTES:
        stop = text.find(_QUOTES[text[start]], start + 1)
        if stop < 0:
            return None
        begin, end = start + 1, stop
        tail = stop + 1
    else:
        value = re.match(r'[^\W_]+(?:[-][^\W_]+)*', text[start:], re.UNICODE)
        if value is None:
            return None
        begin, end = start, start + value.end()
        tail = end
        # Unquoted prose must have an explicit realization boundary.
        if not re.match(r'\s+(?:is\s+|are\s+)?(?:painted|printed|written|inscribed|displayed|shown|on|across)\b', text[tail:], re.I):
            return None
    if not text[begin:end].strip() or end - begin > 160:
        return None
    boundary = re.search(r'[.;!?\n]', text[tail:])
    clause_end = tail + boundary.start() if boundary else len(text)
    carrier = _carrier(text[:clause_end], tail, tokenize)
    if carrier is None:
        return None
    return {'literal': _span(text, begin, end), 'carrier': carrier,
            'input_sha256': hashlib.sha256(text.encode()).hexdigest()}

def compile_contract(document, tokenize):
    """Query-independent witnesses from a direct initial source assertion only."""
    # A later caption, negated example, quoted mention, or lookup alias cannot
    # provide the positive carrier/sequence contract for another source clause.
    end = re.search(r'[.!?\n]', document)
    end = end.start() if end else len(document)
    claim = document[:end]
    if not _TEXT.search(claim) or _negative(claim):
        return None
    if claim.startswith(tuple(_QUOTES)):
        return None
    preservation = None
    declaration = _DECLARED.search(claim)
    retain = _RETAIN.search(claim)
    sequence = _SEQUENCE.search(claim)
    case = _CASE.search(claim)
    if declaration and retain and sequence and case and declaration.start() < retain.start() < sequence.start():
        carrier = _carrier(document[:end], sequence.end(), tokenize)
        if carrier:
            preservation = {'declaration': _span(document, *declaration.span()),
                            'retention': _span(document, *retain.span()),
                            'sequence': _span(document, *sequence.span()),
                            'case': _span(document, *case.span()), 'carrier': carrier}
    fixed = []
    for m in _FIXED.finditer(claim):
        start, stop = m.span('value')
        if document[start] in _QUOTES:
            start += 1
            stop -= 1
        fixed.append(_span(document, start, stop))
    if preservation and fixed:
        return None  # A preservation template cannot also prescribe another word.
    if not preservation and not fixed:
        return None
    return {'document_sha256': hashlib.sha256(document.encode()).hexdigest(),
            'claim': _span(document, 0, end), 'preservation': preservation, 'fixed': fixed}

def compile_contracts(documents, tokenize):
    contracts = {}
    for identity, text in documents.items():
        contract = compile_contract(text, tokenize)
        if contract:
            contracts[identity] = contract
    return contracts

def order_literal(order, text, scope, contracts, tokenize):
    req = request(text, scope, tokenize)
    trace = {'schema': RECIPE, 'applied': False, 'candidate_filter': False,
             'native_approval': False, 'score_changes': 0}
    if req is None:
        return order, trace
    trace['request'] = req
    compatible, conflicting = {}, {}
    wanted = req['literal']['quote']  # Preserve exact case, spaces and punctuation.
    terms = set(req['carrier']['terms'])
    for row in order:
        identity = row['id']
        contract = contracts.get(identity)
        if not contract:
            continue
        preserve = contract['preservation']
        if preserve:
            carrier = preserve['carrier']
            if carrier['head'] == req['carrier']['head'] and len(terms & set(carrier['terms'])) >= 2:
                compatible[identity] = {'kind': 'preserves_declared_sequence', 'source': contract}
        elif len(contract['fixed']) == 1:
            claim_terms = set(tokenize(contract['claim']['quote']))
            if req['carrier']['head'] not in claim_terms or len(terms & claim_terms) < 2:
                continue
            value = contract['fixed'][0]['quote']
            entry = {'kind': 'fixed_exact_match' if value == wanted else 'fixed_literal_conflict', 'source': contract}
            (compatible if value == wanted else conflicting)[identity] = entry
    # No positive same-carrier replacement means no automatic reordering.
    if not compatible:
        trace['reason'] = 'no_positive_same_carrier_literal_contract'
        return order, trace
    priority = lambda row: 0 if row['id'] in compatible else 2 if row['id'] in conflicting else 1
    result = sorted(order, key=priority)  # Stable original RRF10 order per group.
    if [r['id'] for r in result] == [r['id'] for r in order]:
        trace['reason'] = 'order_already_satisfies_literal_contract'
        return order, trace
    trace.update({'applied': True, 'compatible': compatible, 'conflicting': conflicting,
                  'before_winner': order[0]['id'], 'after_winner': result[0]['id'],
                  'within_group_order': 'stable original RRF10', 'whole_pool_retained': True})
    return result, trace

# V3 adds exact selected-primary, bilingual carrier declarations. The legacy
# narrow API stays available for unambiguous earlier queries and test fixtures.
_legacy_compile_contracts=compile_contracts
_legacy_order_literal=order_literal
_PRIMARY_RECIPE='photo-h-f2-primary-carried-literal/v3'
_CARRIER_TYPES={
 'glazed_door':re.compile(r'(?:glass|glazed).{0,20}(?:entrance )?door|door.{0,16}glass|유리\s*(?:출입)?문|출입문\s*유리',re.I),
 'fabric_banner':re.compile(r'(?:fabric|cloth|textile).{0,12}banner|(?:천|직물)\s*(?:배너|현수막)',re.I),
 'wooden_crate':re.compile(r'wooden.{0,12}crate|나무\s*상자|목재\s*상자',re.I),
 'rigid_board':re.compile(r'rigid (?:sign )?board|station board|chalkboard|sign board|안내판|칠판|단단한\s*(?:표지판|판)',re.I),
 'ceramic_vessel':re.compile(r'\bceramic\s+(?:vessel|mug|cup|bowl)\b|\b(?:mug|cup|bowl|vessel)[’\x27]s\s+ceramic\s+(?:surface|body|face)\b|도자기\s*(?:용기|머그잔|잔|컵)|(?:머그잔|컵|잔|용기)(?:\s+(?:테두리|몸통|표면))?\s*(?:아래|위|옆)?\s*도자기\s*표면',re.I),
 'luminous_display':re.compile(r'(?:illuminated|luminous|glowing).{0,18}(?:sign|display|digits)|scoreboard|neon.{0,30}(?:sign|letters)|전광판|발광.{0,12}(?:표시|간판)|네온.{0,15}(?:글자|간판)',re.I),
 'carton_label':re.compile(r'(?:label.{0,45}(?:parcel|carton)|(?:parcel|carton).{0,45}label)|(?:소포|판지\s*상자).{0,30}(?:라벨|레이블)|(?:라벨|레이블).{0,30}(?:소포|판지\s*상자)',re.I),
}
_VESSEL_SURFACE=re.compile(r'\b(?:mug|cup|bowl|vessel)\b(?:\s+(?:rim|body|handle|surface))?\s*,?\s*(?:(?:with|and)\s+)?(?:the\s+)?(?:letters|characters|inscription|text)\s+(?:following|on|across)\s+(?:its|the)\s+ceramic\s+(?:surface|body|face)\b',re.I)
_PHYSICAL=re.compile(r'\b(?:painted|printed|engraved|incised|inscribed|lettering|handwritten|letters|characters|digits|numerals|capitals|word|text|reads?|spells?|carries|bears|displays)\b|적힌|적혀|인쇄|새겨|글자|문자|숫자|문구|읽히|배치',re.I)
_PAYLOAD=re.compile(r'(?<![A-Za-z0-9_])(?:[A-Z][A-Z0-9]*(?:[ \t]+[A-Z0-9]+)*|[0-9]+(?:[–—-][0-9]+)*)(?![A-Za-z0-9_])')
_CONTEXT=re.compile(r'external.{0,15}caption|publication caption|spoken|speaks?|says? aloud|series title|working title|company name|operator.{0,15}name|외부.{0,12}캡션|출판.{0,12}캡션|말로|발화|구두|작업\s*제목|연작\s*제목|상호|운영자',re.I)
_BLANK=re.compile(r'\b(?:blank|unmarked|uninscribed|no (?:letters|marks|writing|text)|without (?:letters|marks|writing|text))\b|아무.{0,8}(?:글자|문자|기호).{0,10}없|무표기|빈\s*(?:판|종이)|완전히.{0,8}(?:표시|글자).{0,8}없',re.I)
_PARAMETER=re.compile(r'already declared inscription|declared (?:inscription|lettering|text)|이미\s*선언된\s*(?:문구|글자|문자)',re.I)
_COMPLETE=re.compile(r'complete character sequence|완전한\s*문자\s*순서',re.I)
_PRESERVE_CASE=re.compile(r'capitalization|\bcase\b|대소문자',re.I)
_PRESERVE_TEXT=re.compile(r'\b(?:retains?|preserves?|keeps?)\b|유지|보존',re.I)
_ATTACH=re.compile(r'\b(?:adhered|stuck|attached|affixed|glued)\b|붙|부착',re.I)
_MEDIA={
 'incised':r'\b(?:engraved|incised)\b|새겨|각인',
 'paint':r'\bpaint(?:ed)?\b|페인트',
 'print':r'\bprinted\b|인쇄',
 'chalk':r'\bchalk\s+(?:strokes|letters|writing)\b|분필\s*(?:획|글씨|글자)',
 'neon':r'\bneon\s+(?:tubing|letters|lettering|strokes)\b|네온\s*(?:관|글자)',
 'led':r'\bLED\s+(?:segments|digits|letters|display)\b',
 'pixel':r'\bpixel\s+(?:display|letters|digits)\b',
}

def _types(text):
    kinds={k:[_span(text,*m.span()) for m in p.finditer(text)] for k,p in _CARRIER_TYPES.items() if p.search(text)}
    # A same-vessel surface continuation can cross a comma; adjacent ceramic
    # objects cannot lend their material to a metal/glass vessel.
    extra=[_span(text,*m.span()) for m in _VESSEL_SURFACE.finditer(text)]
    if extra:kinds.setdefault('ceramic_vessel',[]).extend(extra)
    return kinds

_CARRIER_MEDIA_EN=re.compile(
    r'\b(?:painted|printed|engraved|incised)\s+'
    r'(?:(?!(?:letters|characters|glyphs|strokes|text|inscription|word|numerals|digits|on|across|onto|above|below|at|in|with|as|by|is|are)\b)[A-Za-z-]+\s+){0,4}'
    r'(?:crate|box|board|banner|mug|cup|vessel|bowl|door|label|sign|display|panel|surface|finish)\b',re.I)
_CARRIER_MEDIA_KO=re.compile(
    r'(?:페인트(?:로)?\s*(?:칠한|칠해진|칠해\s*둔)|인쇄된|새겨진)\s*'
    r'(?:(?:나무|목재|도자기|직물|천|금속|종이|판지|유리)\s*){0,2}'
    r'(?:상자|안내판|칠판|배너|현수막|머그잔|컵|용기|문|라벨|간판|패널|표면|마감)')

def _media(text):
    # A carrier's painted/printed/engraved finish is a different owned fact
    # from the method making its glyphs. Preserve original witness offsets;
    # never use carrier paint to satisfy an inscription-medium prerequisite.
    carrier_spans=[m.span() for p in (_CARRIER_MEDIA_EN,_CARRIER_MEDIA_KO) for m in p.finditer(text)]
    out={}
    for kind,pattern in _MEDIA.items():
        matches=[_span(text,*m.span()) for m in re.finditer(pattern,text,re.I)
                 if not any(a<=m.start() and m.end()<=b for a,b in carrier_spans)]
        if matches:out[kind]=matches
    return out

def _clauses(text):
    from photo_h_f2_query_scope import _quoted
    quoted=_quoted(text);start=0
    for i,c in enumerate(text):
        if c in '.;!?\n' and not any(a<=i<b for a,b in quoted):
            if start<i:yield start,i
            start=i+1
    if start<len(text):yield start,len(text)

def _primary_text_units(units):
    return [u for u in units if re.match(r'^/content/(?:en$|ko$|definition$|concept_units(?:/|$)|semantic_relations(?:/|$)|embedding_text$)',u['pointer'])]

def _fixed_primary(unit,positive):
    # Fixed content needs the actual positive reads/carries/spells operator and
    # its carrier, not a redundant 'word/lettering' noun in sentence one.
    out=[];raw=unit['text']
    for a,b in _clauses(raw):
        claim=raw[a:b];pos=positive[a:b];kinds=_types(pos)
        if len(kinds)!=1 or not _PHYSICAL.search(pos) or _CONTEXT.search(pos) or _BLANK.search(pos):continue
        if 'carton_label' in kinds and not _ATTACH.search(pos):continue
        for m in _FIXED.finditer(claim):
            if not pos[m.start():m.start('value')].strip():continue
            s,e=m.span('value')
            if claim[s] in _QUOTES:s+=1;e-=1
            if claim[s:e].strip():out.append({**unit,'carrier_types':kinds,'claim':_span(raw,a,b),'value':_span(raw,a+s,a+e)})
    return out

def compile_contracts(documents,tokenize,*,source_units=None):
    out=_legacy_compile_contracts(documents,tokenize)
    if source_units is None:return out
    from photo_h_f2_query_scope import _focus_positive
    for did,document in documents.items():
        if did not in out and not (_COMPLETE.search(document) or (_PHYSICAL.search(document) and _types(document))):continue
        units=_primary_text_units(source_units(did))
        if did in out:
            claim=out[did]['claim']['quote']
            if not any(claim in u['text'] for u in units) or _CONTEXT.search(_focus_positive(claim)):out.pop(did)
        preservation=[];physical=[];fixed=[]
        for u in units:
            positive=_focus_positive(u['text']);kinds=_types(positive)
            if not kinds or _CONTEXT.search(positive):continue
            base={**u,'carrier_types':kinds}
            if _PARAMETER.search(positive) and _COMPLETE.search(positive) and _PRESERVE_CASE.search(positive) and _PRESERVE_TEXT.search(positive):preservation.append(base)
            unit_fixed=_fixed_primary(u,positive)
            # Painted material or an instruction to read an object does not
            # itself assert nonempty glyphs on that carrier.
            text_assertion=bool(_TEXT.search(positive) or re.search(r'글자|문자|문구',positive) or unit_fixed)
            if _PHYSICAL.search(positive) and text_assertion:physical.append(base)
            fixed.extend(unit_fixed)
        if preservation or physical:
            # The primary fixed witnesses never masquerade as legacy document
            # offsets; every value retains its actual field/RID/hash provenance.
            out.setdefault(did,{'preservation':None,'fixed':[]})['primary_contract']={
             'schema':_PRIMARY_RECIPE,'preservation_evidence':preservation,'physical_evidence':physical,
             'fixed_primary_evidence':fixed,
             'carrier_types':sorted({k for u in preservation+physical for k in u['carrier_types']}),
             'requires_nonempty_declared_characters':True,'native_approval':False}
    return out

def _quoted_payload(raw,a,b,positive):
    # A named person or quoted entire instruction is not inscription content.
    before=positive[:a];after=positive[b:]
    return bool(re.search(r'\b(?:word|text|phrase|letters|lettering|inscription|reads?|spells?|bears|carries)\s*$',before,re.I)
      or re.match(r'\s*(?:(?:is|are)\s+)?(?:painted|printed|written|engraved|incised|inscribed|displayed|on|across)\b',after,re.I)
      or re.match(r'\s*(?:라는\s*(?:글자|문자|문구|단어)|(?:이|가)?\s*(?:적힌|적혀|인쇄|새겨))',raw[b:]))

def _literal_request(text,scope,tokenize):
    from photo_h_f2_query_scope import _focus_positive, _quoted
    match=re.search(r'^Photographic role:[ \t]*(.*?)(?=\nScene context:|\Z)',text,re.S)
    focus=match.group(1) if match else text;offset=match.start(1) if match else 0
    positive=_focus_positive(focus);kinds=_types(positive);candidates=[]
    for a,b in _clauses(focus):
        raw=focus[a:b];pos=positive[a:b];types=_types(pos)
        if not types or not _PHYSICAL.search(pos) or _CONTEXT.search(pos):continue
        # Preserve the existing separation for named bearing parts.
        if re.search(r'\b(?:panel|pane)\b|패널|유리판',pos,re.I):continue
        found=[]
        # Unquoted values come from the positive surface, never the erased raw
        # negation or a quoted whole instruction. Offsets still address input.
        for m in _PAYLOAD.finditer(pos):
            if m.group()[0].isdigit() and not re.search(r'digits|numerals|score|number|reads?|painted|printed|engraved|incised|inscribed|숫자|번호|점수|적힌|적혀|인쇄|새겨',pos,re.I):continue
            found.append(_span(text,offset+a+m.start(),offset+a+m.end()))
        for qstart,qend in _quoted(raw):
            inside=raw[qstart+1:qend-1]
            if qend>len(raw) or raw[qend-1:qend] not in _QUOTES.values():continue
            if inside.strip() and len(inside)<=160 and _quoted_payload(raw,qstart,qend,pos):found.append(_span(text,offset+a+qstart+1,offset+a+qend-1))
        if found:candidates.append((a,b,types,sorted(found,key=lambda r:r['start'])))
    if len(candidates)==1:
        a,b,types,literals=candidates[0]
        if len(types)>1:return None
        media=_media(positive[a:b])
        return {'schema':_PRIMARY_RECIPE,'mode':'physical','literals':literals,
          'carrier_type':next(iter(types)),'carrier_witnesses':{k:[{**r,'start':offset+a+r['start'],'end':offset+a+r['end']} for r in v] for k,v in types.items()},
          'assertion':_span(text,offset+a,offset+b),'input_sha256':hashlib.sha256(text.encode()).hexdigest(),
          'required_medium':'incised' if 'incised' in media else None,'required_media':media}
    if not candidates and kinds and _BLANK.search(focus):return {'schema':_PRIMARY_RECIPE,'mode':'blank','carrier_types':sorted(kinds),'input_sha256':hashlib.sha256(text.encode()).hexdigest()}
    if not candidates and _CONTEXT.search(positive):return {'schema':_PRIMARY_RECIPE,'mode':'context_only','carrier_types':sorted(_types(text)),'input_sha256':hashlib.sha256(text.encode()).hexdigest()}
    return None

def order_literal(order,text,scope,contracts,tokenize):
    legacy_order,legacy_trace=_legacy_order_literal(order,text,scope,contracts,tokenize)
    req=_literal_request(text,scope,tokenize)
    if req is None or not any('primary_contract' in c for c in contracts.values()):return legacy_order,legacy_trace
    from photo_h_f2_query_scope import _focus_positive
    compatible={};conflicting={};kinds={req['carrier_type']} if req['mode']=='physical' else set(req['carrier_types'])
    for row in legacy_order:
        c=contracts.get(row['id'],{});pc=c.get('primary_contract')
        if not pc:continue
        # Context-only words have no physical inscription owner to intersect.
        # Withhold only witnessed positive physical text, not mere metadata or
        # an unrelated object/lighting mention whose type happens to match.
        if req['mode']=='context_only':
            if pc['physical_evidence'] or pc['preservation_evidence']:conflicting[row['id']]={'reason':'context_is_not_physical_text','source':pc}
            continue
        if not kinds.intersection(pc['carrier_types']):continue
        if req['mode']!='physical':
            if pc['physical_evidence'] or pc['preservation_evidence']:conflicting[row['id']]={'reason':'no_physical_nonempty_inscription_requested','source':pc}
            continue
        actual_media={k for u in pc['physical_evidence'] for k in _media(_focus_positive(u['text']))}
        required=set(req.get('required_media',{}))
        if actual_media and required and actual_media.isdisjoint(required):
            conflicting[row['id']]={'reason':'explicit_medium_conflict','source':pc};continue
        if pc['preservation_evidence']:
            # Intrinsic medium prerequisites of preservation sources cannot be
            # supplied by an unspecified request or by an adjacent owner.
            if actual_media-required:continue
            compatible[row['id']]={'kind':'primary_declared_sequence_preservation','source':pc}
        else:
            fixed=pc.get('fixed_primary_evidence',[])
            values={f['value']['quote'] for f in fixed if kinds.intersection(f['carrier_types'])}
            if len(req['literals'])==1 and len(values)==1:
                same=next(iter(values))==req['literals'][0]['quote']
                (compatible if same else conflicting)[row['id']]={'kind':'fixed_exact_match' if same else 'fixed_literal_conflict','source':pc}
    result=sorted(legacy_order,key=lambda r:0 if r['id'] in compatible else 2 if r['id'] in conflicting else 1)
    trace={'schema':_PRIMARY_RECIPE,'request':req,'compatible':compatible,'conflicting':conflicting,
           'legacy':legacy_trace,'applied':[r['id'] for r in result]!=[r['id'] for r in order],
           'score_changes':0,'candidate_filter':False,'whole_pool_retained':True,'native_approval':False}
    return result,trace
