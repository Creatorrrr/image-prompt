"""Durable, record-centred semantic assessment. Never writes operating sources.

This is a text-model dataset review, not an independent human assessment or a
keyword/embedding score. Catalog and source hashes bind every actual request.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import argparse,copy,gzip,hashlib,json,os,sys,time,threading
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
import photo_candidate_corpus as c
from photo_embedding_provider import load_env,atomic
from google import genai
from google.genai import types
MODEL='gemini-3.8-flash'
class SpendingCapReached(RuntimeError):pass
RULES='''You are reviewing a photographic visual candidate dataset, not generating images. Read EVERY candidate's complete positive meaning, its negative/confusion boundaries, applicability, effects and references. Assess ALL 139 flat roles. Source slot names/tags are not proof, no minimum tag quota. Infer no missing people, adult/sexual context, identity, clinical facts, hidden material performance, intentions or apparatus. Keep declared narrative context as contextual, observable surface/form/direction as direct. Entire profiles/bundles represent complete meanings, not an unconditional union of their children's properties. OR alternatives and conditions remain conditional. Never use a negative example or avoided confounder as a positive fact. Surface finish != image grain; garment topology != anatomy; gaze direction != head orientation/engagement. Age alone != sexual/fetish context; material latex/leather or underwear alone != fetish. Physical residue of a completed prior event alone qualifies aftermath_trace. Explicit role of another participant != count inferred from composition. Actual source facets/guards must be preserved, not used as a source of visual facts.
Return one JSON review for EACH supplied primary ID, in order. For each suitable role supply role ID, semantic role, concise rationale, and ONE OR MORE exact positive evidence quotes with JSON pointer into that candidate's content (not its references). Quotes MUST be exact contiguous substrings of a string at that pointer. Describe real owner, dimension and precise property using the role's property prefix but do not invent a fact to fit the prefix. Owners must name the source carrier: main_subject/body/hair/garment/image/background/cup etc; unknown owners remain unknown and are not approved. Include every suitable role, reject broad-only membership. facts describe all potential properties touched by adopting the actual source, with exact evidence; for alternative-specific facts name their realization_id, otherwise use base. Do not add properties implied only by a role name. For roles supported only by some source alternatives, state scope='positive_alternative' and explain the exact option and its preconditions; otherwise scope='whole_record'. A source literal descriptive alternative can change the SAME property without forcing ALL its values. No new semantic text; if meaning/translation/owner/temporal conflict is wrong, propose an exact string replacement and why, with field pointer and existing exact string. Problems requiring specialist historical/scientific validation must be marked uncertainty; do not assert factual authenticity merely from a research URL. diagnostic records have no positive roles/facts; pure guard/router/readability rules without a concrete visual meaning must recommend diagnostic rather than turn them into visual details. Preserve a relationship mechanism as a mechanism, not an invented concrete action. Distinguish visual_semantic_ambiguity (must resolve before application) from external_fact_not_verified (does not fabricate truth).
Output keys for each review: id, meaning_summary, roles (array of {slot_id,semantic_role,scope,realization_ids,rationale,evidence:array of {pointer,quote,dimension,target,property}}), facts (array same evidence fields plus realization_id), corrections (array {pointer,before,after,reason}), recommended_kind (current kind unless pure diagnostic), uncertainties (array of {kind,detail}), rejected_boundaries (array of brief explanations for likely confusions), all_roles_considered=true. JSON only. Explain meaning faithfully, not flattering dataset quality.'''

def jsonbytes(x):return c.canonical_bytes(x)
def dump(path,x):atomic(path,x)
def raw_atomic(path,body):
 tmp=path.with_name(path.name+'.pending');tmp.write_bytes(body);os.replace(tmp,path)
def refs(value):
 if isinstance(value,str) and c.ID.fullmatch(value):yield value
 elif isinstance(value,dict):
  for key,v in value.items():yield from refs(key);yield from refs(v)
 elif isinstance(value,list):
  for v in value:yield from refs(v)
def blinded(r):
 value=copy.deepcopy(r);value.pop('provenance',None)
 value['content'].pop('role_evidence',None);value['content'].pop('semantic_review',None)
 # Library tags/facets are applicability information, not current role membership.
 return value

def freeze():
 corpus=c.load(SKILL/'assets');path=HERE/'REVIEW-SOURCE.json.gz'
 if path.exists():
  saved=json.loads(gzip.decompress(path.read_bytes()))
  if c.digest(saved)!=c.digest(corpus):
   assert set(saved['candidates'])==set(corpus['candidates']),'candidate identities changed; freeze a new review cohort'
   assert saved['slot_catalog']==corpus['slot_catalog'],'role catalog changed; re-review its meaning'
   affected=[]
   for cid,old in saved['candidates'].items():
    new=corpus['candidates'][cid]
    assert all(old[k]==new[k] for k in ['content','conditions','record_kind','provenance']),'semantic source changed; re-review '+cid
    def branch_meaning(record):
     value=copy.deepcopy(record['effects'].get('realizations'))
     if value:
      for branch in value['branches']:branch.pop('effects',None)
     return value
    assert branch_meaning(old)==branch_meaning(new),'realization conditions/members changed; re-review '+cid
    if old['effects']!=new['effects']:affected.append(cid)
   dump(HERE/'REVIEW-CURRENT-SOURCE-COMPARISON.json',{'frozen_review_source_sha256':c.digest(saved),'current_source_sha256':c.digest(corpus),'positive_meanings_intrinsic_conditions_kinds_provenance_and_branches_identical':True,'metadata_effect_refinements':affected,'provider_inputs_remain_bound_to_the_frozen_review_source':True})
  return saved
 raw=jsonbytes(corpus);raw_atomic(path,gzip.compress(raw,mtime=0));dump(HERE/'REVIEW-SOURCE-MANIFEST.json',{'schema':'photo-semantic-review-source/v1','source_sha256':c.digest(corpus),'catalog_sha256':c.digest(corpus['slot_catalog']),'records':len(corpus['candidates']),'ids':sorted(corpus['candidates']),'model':MODEL,'rules_sha256':hashlib.sha256(RULES.encode()).hexdigest(),'independent_human_review':False})
 (HERE/'REVIEW-RULES.txt').write_text(RULES+'\n');return corpus

def ensure_prompt_cache(client,data):
 catalog={tag:{k:v for k,v in spec.items() if k in {'description','description_ko','semantic_role','owners','dimensions','property_prefixes','includes','excludes'}} for tag,spec in sorted(data['slot_catalog'].items())}
 prefix=RULES+'\nFLAT ROLE CATALOG:\n'+json.dumps(catalog,ensure_ascii=False,separators=(',',':'))
 # Explicit remote prompt cache only reduces repeated catalog tokens; the exact
 # prefix is frozen locally, and a missing cache creates a fresh bound cache.
 cache_file=HERE/'TEXT-PROMPT-CACHE.json';cache=None
 if cache_file.exists():
  meta=json.loads(cache_file.read_text())
  if meta['prefix_sha256']==hashlib.sha256(prefix.encode()).hexdigest() and meta['expires_at_epoch']>time.time()+180 and meta.get('status','active')=='active':
   cache=meta['name']
 if not cache:
  cached=client.caches.create(model=MODEL,config=types.CreateCachedContentConfig(contents=prefix,ttl='14400s',display_name='photo-corpus-semantic-review-20261014'))
  cache=cached.name;dump(cache_file,{'name':cache,'model':MODEL,'prefix_sha256':hashlib.sha256(prefix.encode()).hexdigest(),'expires_at_epoch':time.time()+14400})
 return cache,catalog,prefix

def main():
 p=argparse.ArgumentParser();p.add_argument('--start',type=int,default=0);p.add_argument('--count',type=int,default=12);p.add_argument('--workers',type=int,default=2);p.add_argument('--batch-size',type=int,default=12);p.add_argument('--probe',action='store_true');a=p.parse_args()
 load_env(ROOT/'.env');data=freeze();client=genai.Client(http_options=types.HttpOptions(retry_options=types.HttpRetryOptions(attempts=1)))
 stop=threading.Event()
 pilot=[json.loads(s)['candidate_id'] for s in (HERE.parent/'slot-tag-pilot-20261013/REVIEWS.jsonl').read_text().splitlines()]
 ids=list(dict.fromkeys(pilot+['cand_0754e4248862538eb282a8451f28d4d7']+sorted(data['candidates'])))
 dump(HERE/'REVIEW-ORDER.json',{'ids':ids,'source_sha256':c.digest(data)})
 out=HERE/'model-reviews';out.mkdir(exist_ok=True)
 cache,catalog,prefix=ensure_prompt_cache(client,data)
 def one(offset,group):
  if stop.is_set():raise SpendingCapReached('new requests stopped after the project spending cap')
  file=out/f'{offset:05d}.json'
  if file.exists():
   old=json.loads(file.read_text());assert old['ids']==group;return {'offset':offset,'count':len(group),'cached_local':True}
  prim=[blinded(data['candidates'][cid]) for cid in group];referenced=set()
  for r in prim:referenced.update(refs(r['content']))
  referenced-=set(group)
  payload={'primary_records':prim,'referenced_records':[blinded(data['candidates'][cid]) for cid in sorted(referenced)]}
  request=json.dumps(payload,ensure_ascii=False,separators=(',',':'));errors=[]
  for attempt in range(5):
   try:
    if stop.is_set():raise SpendingCapReached('new requests stopped after the project spending cap')
    attempt_path=out/f'{offset:05d}.attempt-{attempt+1}.json'
    dump(attempt_path,{'schema':'photo-text-provider-attempt/v1','ids':group,'request_sha256':hashlib.sha256(request.encode()).hexdigest(),'model':MODEL,'started_at_epoch':time.time(),'status':'started_response_unknown'})
    t=time.time();resp=client.models.generate_content(model=MODEL,contents=request,config=types.GenerateContentConfig(cached_content=cache,response_mime_type='application/json',temperature=.2,max_output_tokens=65536,thinking_config=types.ThinkingConfig(thinking_level='HIGH')))
    dump(attempt_path,{'schema':'photo-text-provider-attempt/v1','ids':group,'request_sha256':hashlib.sha256(request.encode()).hexdigest(),'model':MODEL,'status':'response_returned','response_sha256':hashlib.sha256((resp.text or '').encode()).hexdigest(),'usage':resp.usage_metadata.model_dump(mode='json') if resp.usage_metadata else None})
    reviews=json.loads(resp.text)
    if isinstance(reviews,dict) and 'reviews' in reviews:reviews=reviews['reviews']
    elif isinstance(reviews,dict) and len(group)==1 and 'id' in reviews:reviews=[reviews]
    assert isinstance(reviews,list) and [r['id'] for r in reviews]==group,'record coverage or order differs'
    for r in reviews:
     assert r.get('all_roles_considered') is True
     assert all(x['slot_id'] in catalog for x in r['roles'])
    envelope={'schema':'photo-model-semantic-review-batch/v1','model':MODEL,'source_sha256':c.digest(data),'catalog_sha256':c.digest(catalog),'prefix_sha256':hashlib.sha256(prefix.encode()).hexdigest(),'request_sha256':hashlib.sha256(request.encode()).hexdigest(),'ids':group,'record_sha256':{cid:c.digest(data['candidates'][cid]) for cid in group},'referenced_ids':sorted(referenced),'reviews':reviews,'provider_response_sha256':hashlib.sha256(resp.text.encode()).hexdigest(),'usage':resp.usage_metadata.model_dump(mode='json') if resp.usage_metadata else None,'finish_reasons':[str(x.finish_reason) for x in resp.candidates or []],'elapsed_seconds':time.time()-t,'attempt_errors':errors,'independent_human_review':False,'actual_provider_call':True}
    dump(file,envelope);return {'offset':offset,'count':len(group),'actual_provider_call':True,'seconds':round(time.time()-t,2)}
   except Exception as exc:
    errors.append({'attempt':attempt+1,'type':type(exc).__name__,'detail':str(exc)[:2000]});dump(out/f'{offset:05d}.errors.json',{'ids':group,'errors':errors})
    if 'monthly spending cap' in str(exc).lower() or isinstance(exc,SpendingCapReached):
     stop.set();raise SpendingCapReached('project monthly spending cap; no automatic billing change or alternate-provider bypass') from exc
    if attempt==4:raise
    time.sleep(min(20,2**attempt))
 groups=[(n,ids[n:min(n+a.batch_size,a.start+a.count)]) for n in range(a.start,min(len(ids),a.start+a.count),a.batch_size)]
 with ThreadPoolExecutor(max_workers=a.workers) as pool:
  futures=[pool.submit(one,n,g) for n,g in groups]
  try:
   for f in as_completed(futures):print(json.dumps(f.result()),flush=True)
  except SpendingCapReached:
   stop.set()
   for future in futures:future.cancel()
   raise
if __name__=='__main__':main()
