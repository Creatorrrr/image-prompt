"""Source-bound authored search views; no interpretation or admission authority.

Each view belongs to one real CID/RID. Multiple view scores reduce to one
document score before lexical/dense fusion, without duplicating lexical votes.
Importing this module performs no IO, model load, or corpus access.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
from numbers import Real

SCHEMA = 'photo-candidate-retrieval-views/v1'
RECIPE = 'photo-reviewed-bilingual-search-view/v1'
CANONICAL_SCHEMA = 'photo-canonical-retrieval-views/v1'
KINDS = frozenset({'whole', 'context', 'relation'})
POSITIVE_KINDS = frozenset({'visual_option', 'visual_profile', 'visual_bundle',
                          'relationship_concept', 'relationship_mechanism'})


def digest(value):
    raw=json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
    return hashlib.sha256(raw).hexdigest()


def realization_ids(record):
    contract=record['effects'].get('realizations')
    if not contract:return ['base']
    ids=[row['id'] for row in contract['branches']]
    return (['base']+ids) if contract['mode']=='optional' else ids


def at_pointer(value,pointer):
    if not isinstance(pointer,str) or not pointer.startswith('/'):raise ValueError('absolute source pointer required')
    for token in pointer.split('/')[1:]:
        key=token.replace('~1','/').replace('~0','~')
        value=value[int(key)] if isinstance(value,list) else value[key]
    return value


def document_text(view):
    """Encode authored meaning, without IDs, review votes, or source guards."""
    return 'English: '+view['text_en']+'\nKorean: '+view['text_ko']


def view_id(cid,rid,key):
    return 'view_'+digest([cid,rid,key])[:32]


def validate(module,records,*,require_complete=True):
    """Check bindings/coverage, not natural-language truth or native approval."""
    if not isinstance(module,dict) or module.get('schema')!=SCHEMA or module.get('recipe')!=RECIPE:
        raise ValueError('unsupported retrieval view module')
    if module.get('native_approval',False) is not False:
        raise ValueError('search views grant no native approval')
    rows=module.get('views')
    if not isinstance(rows,list):raise ValueError('retrieval views must be a list')
    seen=set();whole={};covered=set()
    for view in rows:
        cid=view['candidate_id'];record=records.get(cid)
        if record is None:raise ValueError('unknown view candidate')
        if record.get('id')!=cid:raise ValueError('view candidate identity changed')
        if record['record_kind']=='diagnostic':raise ValueError('diagnostic source cannot own positive views')
        if record['record_kind'] not in POSITIVE_KINDS:raise ValueError('unknown positive source kind')
        if view.get('native_approval',False) is not False:
            raise ValueError('search views grant no native approval')
        rid=view['realization_id']
        if rid not in realization_ids(record):raise ValueError('view belongs to unknown realization')
        key=view['key']
        if not isinstance(key,str) or not key.strip():raise ValueError('nonempty view key required')
        identity=view_id(cid,rid,key)
        if view.get('id')!=identity or identity in seen:raise ValueError('duplicate or changed view identity')
        seen.add(identity);covered.add((cid,rid))
        if view.get('source_record_sha256')!=digest(record):raise ValueError('stale view source')
        if view.get('kind') not in KINDS:raise ValueError('unknown search view kind')
        for name in ('text_en','text_ko'):
            if not isinstance(view.get(name),str) or not view[name].strip():raise ValueError('bilingual view text required')
        quotes=view.get('source_quotes')
        if not isinstance(quotes,list) or not quotes:raise ValueError('search view needs source evidence')
        for quote in quotes:
            pointer=quote.get('pointer','')
            if not pointer.startswith('/content/'):raise ValueError('search evidence must be authored positive content')
            prefix='/content/realization_content/'
            if pointer.startswith(prefix) and pointer[len(prefix):].split('/')[0]!=rid:
                raise ValueError('sibling realization cannot supply view evidence')
            try:value=at_pointer(record,pointer)
            except (KeyError,IndexError,TypeError,ValueError):raise ValueError('missing view source quote') from None
            if not isinstance(value,str) or not isinstance(quote.get('quote'),str) or not quote['quote'] or quote['quote'] not in value:
                raise ValueError('view quote differs from source')
        if view['kind']=='whole':whole[(cid,rid)]=whole.get((cid,rid),0)+1
    if any(count!=1 for count in whole.values()):raise ValueError('exactly one whole view per realization required')
    expected={(cid,rid) for cid,record in records.items() if record['record_kind']!='diagnostic' for rid in realization_ids(record)}
    required=expected if require_complete else covered
    if not covered<=expected or set(whole)!=required or (require_complete and covered!=expected):
        raise ValueError('positive realization whole-view coverage mismatch')
    return module


def documents(module,records,document_ids,*,require_complete=True):
    """Prepare dense inputs for one explicit RID population, without lexical rows.

    IDs and hashes are metadata, never embedding text. Callers still need actual
    provider execution proofs and a newly sealed generation before activation.
    """
    validate(module,records,require_complete=require_complete)
    expected={cid+'|'+rid for cid,record in records.items()
              if record['record_kind']!='diagnostic' for rid in realization_ids(record)}
    if len(document_ids)!=len(set(document_ids)) or set(document_ids)!=expected:
        raise ValueError('view document population differs from lexical RID population')
    rows=[]
    for view in sorted(module['views'],key=lambda row:row['id']):
        text=document_text(view)
        rows.append({'id':view['id'],'document_id':view['candidate_id']+'|'+view['realization_id'],
                     'candidate_id':view['candidate_id'],'realization_id':view['realization_id'],
                     'source_record_sha256':view['source_record_sha256'],'kind':view['kind'],
                     'recipe':RECIPE,'text':text,
                     'text_sha256':hashlib.sha256(text.encode()).hexdigest()})
    return rows


def canonical_bindings(module,records,canonical_records,*,canonical_api,require_complete=True):
    """Bind reviewed authored views to validated native literal owners.

    The caller supplies the canonical API from the generation's verified code
    closure. Its full validator and native snapshot codec remain authoritative;
    this adapter neither reconstructs native records nor transfers admission.
    A source edit requires a freshly built canonical record with the same edit.
    Historical content locators are opaque keys in ``primary``, never paths
    walked in a canonical record.
    """
    validate(module,records,require_complete=require_complete)
    positive={cid:record for cid,record in records.items()
              if record['record_kind']!='diagnostic'}
    if set(canonical_records)!=set(positive):
        raise ValueError('canonical view source population mismatch')
    for cid,record in canonical_records.items():
        canonical_api.validate(record)
        if record.get('id')!=cid or not canonical_api.positive(record):
            raise ValueError('canonical view needs its positive source owner')
        if digest(canonical_api.native_snapshot(record))!=digest(positive[cid]):
            raise ValueError('canonical origin differs from reviewed authored source')
    rows=[]
    for view in sorted(module['views'],key=lambda row:row['id']):
        cid=view['candidate_id'];rid=view['realization_id']
        record=canonical_records[cid];meaning=record['meaning']
        primary=meaning['primary'].get(rid)
        if primary is None:raise ValueError('missing canonical view realization')
        bindings=[]
        for quote in view['source_quotes']:
            locator=quote['pointer'];literal_id=primary.get(locator)
            if literal_id is None:
                raise ValueError('view quote lacks same-RID primary literal')
            literal=meaning['literals'][literal_id]
            if (literal!=at_pointer(positive[cid],locator)
                or quote['quote'] not in literal):
                raise ValueError('canonical view quote differs from authored literal')
            bindings.append({'locator':locator,'literal_id':literal_id,
                             'quote':quote['quote']})
        row=copy.deepcopy(view)
        row['authored_source_sha256']=view['source_record_sha256']
        row['source_record_sha256']=digest(record)
        row['literal_bindings']=bindings
        rows.append(row)
    return {'schema':CANONICAL_SCHEMA,'recipe':RECIPE,
            'authored_module_sha256':digest(module),
            'authored_sources_sha256':digest(positive),
            'canonical_sources_sha256':digest(canonical_records),
            'views':rows,'native_approval':False}


def canonical_documents(compiled,module,records,canonical_records,document_ids,*,canonical_api,require_complete=True):
    """Replay every source/literal binding before preparing dense inputs.

    This verifies compiled metadata, not provider execution, quality or release.
    The text recipe is identical to the authored-view recipe; source hashes are
    explicitly kept in their two separate hash domains.
    """
    expected=canonical_bindings(module,records,canonical_records,canonical_api=canonical_api,require_complete=require_complete)
    if digest(compiled)!=digest(expected):
        raise ValueError('compiled canonical view binding changed')
    bindings={view['id']:view for view in compiled['views']}
    rows=documents(module,records,document_ids,require_complete=require_complete)
    for row in rows:
        view=bindings[row['id']]
        row['authored_source_sha256']=row['source_record_sha256']
        row['source_record_sha256']=view['source_record_sha256']
        row['literal_bindings_sha256']=digest(view['literal_bindings'])
    return rows


def pool_scores(views,scores,document_ids):
    """Max per actual CID/RID, before dense ranking and RRF; retain witnesses.

    More authored views still create more chances to match, so this function
    does not claim to remove view-count selection bias.
    """
    if len(views)!=len(scores):raise ValueError('view score population mismatch')
    if len(document_ids)!=len(set(document_ids)):raise ValueError('duplicate document identity')
    allowed=set(document_ids);best={};counts={};view_ids=set()
    for view,score in zip(views,scores,strict=True):
        if isinstance(score,bool) or not isinstance(score,Real) or not math.isfinite(score):
            raise ValueError('finite view score required')
        score=float(score)
        identity=view['candidate_id']+'|'+view['realization_id']
        if identity not in allowed:raise ValueError('view score belongs to foreign document')
        vid=view['id']
        if vid in view_ids:raise ValueError('duplicate view score witness')
        view_ids.add(vid);counts[identity]=counts.get(identity,0)+1
        old=best.get(identity)
        if old is None or score>old[0] or (score==old[0] and vid<old[1]):best[identity]=(float(score),vid)
    if set(best)!=allowed:raise ValueError('document lacks a scored search view')
    dense=[best[identity][0] for identity in document_ids]
    witnesses=[{'document_id':identity,'view_id':best[identity][1],'score':best[identity][0],
                'considered_views':counts[identity]} for identity in document_ids]
    return dense,witnesses
