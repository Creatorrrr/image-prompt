"""Research structure/integrity checks only. No runtime, embedding or image calls."""
from pathlib import Path
import json, hashlib, re, collections, datetime
from reference_inventory import SECTIONS, EXPECTED_COUNTS

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
DOM_CHECKS='dff3cebf 56d1d3f5 6f9a5802 49212588 191d4f85 fed3c141 7c6a7a0a 32da91ae 7dd0d93b 278b22d4 8817eae5 76d4f97d e236cf0b 12dc2cf9 6f719c7b 75f9cc8f 48343cbd de41342e 79b22936 2cd8f022'.split()

def read(name): return json.loads((HERE/name).read_text())
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def canon(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def fnv(text):
 h=2166136261
 raw=text.encode('utf-16-le')
 for n in range(0,len(raw),2): h=((h^int.from_bytes(raw[n:n+2],'little'))*16777619)&0xffffffff
 return f'{h:08x}'

def run():
 checks=[]
 def check(name,ok):
  checks.append(dict(name=name,passed=bool(ok)))
 k=read('keyword-routes.json')['keywords'];c=read('semantic-cards.json')['cards'];d=read('candidate-drafts.json')['drafts'];s=read('sources.json')['sources']
 kid={x['id'] for x in k};cid={x['id'] for x in c};sid={x['id'] for x in s}
 check('exact 320 rows / 314 terms / 6 combinations',len(k)==320 and sum(x['item_kind']=='term_row' for x in k)==314 and sum(x['item_kind']=='combination_example' for x in k)==6)
 check('all 20 visible DOM title checks match',len(SECTIONS)==20 and [fnv(t) for _,t in SECTIONS]==DOM_CHECKS)
 check('section row counts', [sum(x['section']==n for x in k) for n in range(1,21)]==EXPECTED_COUNTS)
 check('unique keyword/card/source/draft IDs',len(kid)==len(k) and len(cid)==len(c) and len(sid)==len(s) and len({x['draft_id'] for x in d})==len(d))
 check('90 cards / 76 drafts',len(c)==90 and len(d)==76)
 check('68 visible / 8 proxy / 14 context',collections.Counter(x['mode'] for x in c)==dict(visible=68,proxy=8,context=14))
 check('all card keyword and source references exist',all(set(x['keyword_ids'])<=kid and set(x['source_ids'])<=sid for x in c))
 check('every keyword has route and reason',all(x['route'] and x['reason'] and set(x['card_ids'])<=cid for x in k))
 check('context cards have no positive visual text/draft',all(not x['positive_en'] and not x['positive_ko'] and x['context_en'] and x['context_ko'] and all(y['card_id']!=x['id'] for y in d) for x in c if x['mode']=='context'))
 check('visual/proxy cards have complete bilingual propositions',all(x['positive_en'] and x['positive_ko'] for x in c if x['mode']!='context'))
 check('graph endpoints closed within research nodes',all(all(e['from'] in x['research_owner_nodes'] and e['to'] in x['research_owner_nodes'] for e in x['research_relations']) for x in c))
 check('noncontext cards have relation notes',all(x['research_relations'] for x in c if x['mode']!='context'))
 catalog=json.loads((ROOT/'skills/photo-prompt-image-generator/assets/photo_candidate_slot_catalog.json').read_text())['slot_catalog']
 check('suggested role IDs exist in current catalog',all(set(x['suggested_slots'])<=set(catalog) for x in c))
 check('drafts exactly match their selected cards',all(y['en']==next(x for x in c if x['id']==y['card_id'])['positive_en'] and y['ko']==next(x for x in c if x['id']==y['card_id'])['positive_ko'] for y in d))
 check('research not runtime/qualification/pixel approval',all(x['runtime_importable'] is False and x['pixel_status']=='NOT_RUN' for x in c) and all(y['native_qualification']=='NOT_RUN' and y['runtime_importable'] is False and y['effects_review_required'] for y in d))
 check('26 sources with explicit access limits',len(s)==26 and all(x['limits'] and x['read_scope'] and x['url'].startswith('https://') for x in s))
 check('source access counts',collections.Counter(x['access'] for x in s)==dict(body_excerpt=20,search_excerpt=1,failed_403=3,failed_429=1,failed_robots=1))
 preview=read('conversation-preview.json')
 check('bounded reference capture remains marked truncated',any(i.get('truncated') for t in preview['turns'] for i in t['items']))
 snap=read('corpus-snapshot.json')
 check('all preserved source records match their canonical hashes',all(hashlib.sha256(canon(x['record'])).hexdigest()==x['record_sha256'] for x in snap['matches']))
 decisions=read('existing-source-decisions.json')['decisions']
 check('18 decisions retain complete original record/bindings',len(decisions)==18 and all(x['record'] and 'conditions' in x['record'] and 'effects' in x['record'] and 'bindings' in x and x['reason'] for x in decisions))
 check('self interlaced hands not approved for cross-owner reuse',any(x['candidate_id']=='cand_d2834908636b578489498652230bafd9' and x['research_decision']=='owner_scope_no_direct_reuse' for x in decisions))
 dev=read('development-cases.json');b=read('boundary-cases.json')
 check('324 designed development queries, no claimed holdout',dev['query_count']==180 and b['query_count']==144 and len(b['pairs'])==36 and not dev['independent_holdout'] and not b['independent_holdout'])
 check('no claimed retrieval/adoption execution',all(x['retrieval_status']=='NOT_RUN' and x['adoption_status']=='NOT_RUN' for x in dev['cases']) and all(x['status']=='DESIGNED_NOT_RUN' for x in b['pairs']))
 broken=[]
 for p in HERE.glob('*.md'):
  for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
   generated_here=link in {'VALIDATION.json','SHA256SUMS'}
   if not re.match(r'^[a-zA-Z]+:',link) and not generated_here and not (p.parent/link.split('#')[0]).exists(): broken.append(dict(file=p.name,link=link))
 check('local Markdown links resolve',not broken)
 baseline=read('BASELINE.json');drift=[]
 for name,expected in baseline['protected_sha256'].items():
  p=ROOT/name
  actual=sha(p) if p.is_file() else None
  if actual!=expected: drift.append(dict(path=name,before=expected,after=actual))
 check('protected baseline files unchanged',not drift)
 failed=[x['name'] for x in checks if not x['passed']]
 structure_failed=[x for x in failed if x!='protected baseline files unchanged']
 status='STRUCTURE_FAIL' if structure_failed else ('STRUCTURE_PASS_SOURCE_DRIFT_REQUIRES_REBASELINE' if drift else 'STRUCTURE_AND_BASELINE_PRESERVATION_PASS')
 result=dict(status=status,checked_at=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(),
  checks=checks,passed=sum(x['passed'] for x in checks),total=len(checks),broken_links=broken,
  protected_file_count=len(baseline['protected_sha256']),observed_drift=drift,
  limits='Structure, title transcription and local integrity only. No factual, bilingual semantic, native, search, image or user-acceptance certification.',
  runtime_status=dict(source_mutation='NOT_PERFORMED_BY_THIS_RESEARCH',native='NOT_RUN',index='NOT_RUN',search='NOT_RUN',images='NOT_RUN',activation='NOT_RUN',commit_push='NOT_RUN'))
 (HERE/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 files=sorted(p for p in HERE.iterdir() if p.is_file() and p.name!='SHA256SUMS')
 (HERE/'SHA256SUMS').write_text(''.join(f'{sha(p)}  {p.name}\n' for p in files))
 assert (HERE/'VALIDATION.json').is_file() and (HERE/'SHA256SUMS').is_file()
 print(json.dumps(dict(status=status,passed=result['passed'],total=len(checks),observed_drift_count=len(drift),structure_failed=structure_failed,broken_links=broken),ensure_ascii=False))
 if structure_failed: raise SystemExit(1)

if __name__=='__main__':run()
