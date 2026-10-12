"""Private immutable query context, separate from immutable source data."""
import hashlib,re
from photo_candidate_corpus import digest
from photo_embedding_provider import embed,SPACE,validate_vector
from photo_global_index import QUERY_RECIPE
HASH=re.compile(r'[0-9a-f]{64}\Z')

def prepare(text,core_sha256,controls_sha256,cache):
    binding={'recipe':QUERY_RECIPE,'core_sha256':core_sha256,'controls_sha256':controls_sha256}
    if not text.strip() or any(not HASH.fullmatch(v) for v in (core_sha256,controls_sha256)):
        raise ValueError('query requires nonempty frozen text and exact core/control bindings')
    result=embed(text,binding,cache)
    context={'schema':'photo-frozen-query-vector/v1','text':text,'text_sha256':hashlib.sha256(text.encode()).hexdigest(),
        'binding':binding,'space':SPACE,'vector':result['vector'],'vector_sha256':result['vector_sha256'],
        'execution':result['execution'],'cache_hit':result['cache_hit']}
    context['canonical_sha256']=digest(context)
    return context

def validate(context,text,core_sha256,controls_sha256):
    if not isinstance(context,dict):raise ValueError('hybrid retrieval requires an exact recorded query context')
    material={k:v for k,v in context.items() if k!='canonical_sha256'}
    if context.get('schema')!='photo-frozen-query-vector/v1' or context.get('canonical_sha256')!=digest(material):
        raise ValueError('query vector context checksum/schema mismatch')
    if context.get('space')!=SPACE or context.get('text')!=text or context.get('text_sha256')!=hashlib.sha256(text.encode()).hexdigest():
        raise ValueError('query vector space/text mismatch')
    if context.get('binding')!={'recipe':QUERY_RECIPE,'core_sha256':core_sha256,'controls_sha256':controls_sha256}:
        raise ValueError('query vector frozen core/control/recipe mismatch')
    validate_vector(context.get('vector'))
    if context.get('vector_sha256')!=digest(context['vector']):raise ValueError('query vector content hash mismatch')
    trace=context.get('execution') or {}
    if trace.get('provider_executed') is not True or trace.get('http_status')!=200 or not HASH.fullmatch(trace.get('response_sha256','')):
        raise ValueError('hybrid query requires recorded real provider execution')
    return context
