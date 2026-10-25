"""Read-only authored-corpus inventory; this does not run retrieval."""
from pathlib import Path
import json, re, hashlib, collections
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
ASSETS=REPO/'skills/photo-prompt-image-generator/assets'
PATTERNS={
 'guitar':r'\bguitar(?:ist)?\b|기타리스트|기타 연주|일렉기타|전기 기타',
 'electric_bass_explicit':r'\bbassist\b|\bbass guitar\b|\belectric bass\b|베이시스트|베이스 기타|일렉 베이스',
 'double_bass':r'\bdouble[- ]bass\b|콘트라베이스|더블베이스',
 'drums':r'\bdrummer\b|\bdrum kit\b|\bdrumsticks?\b|드러머|드럼스틱',
 'classical_ambiguous':r'\bviolin\b|\bcello\b|\bconductor\b|바이올린|첼로|지휘자',
 'wind_ambiguous':r'\bsaxophone\b|\bflute\b|색소폰|플루트',
 'dj_ambiguous':r'\bDJ\b|\bturntable\b|\bcrossfader\b|턴테이블',
 'studio_ambiguous':r'\bDAW\b|\bcomping\b|\bMIDI\b|\boverdub\b|멀티트랙',
 'microphone_ambiguous':r'\bmicrophone\b|마이크',
 'monitoring_ambiguous':r'\bin.ear\b|\bwedge monitor\b|인이어|웨지',
 'live_tech':r'\bstage plot\b|\binput list\b|\bline check\b|\bsoundcheck\b|사운드체크|라인체크',
 'band_genre':r'\bshoegaze\b|\bgrunge\b|\briot grrrl\b|\bvisual kei\b|슈게이즈|그런지|라이엇 그럴|비주얼계',
 'fashion_explicit':r'\bbondage trousers\b|\bbattle (?:jacket|vest)\b|\bbullet belt\b|본디지 트라우저|배틀 재킷|불릿 벨트',
 'audience_ambiguous':r'\bmosh\b|\bcrowd.?surf\b|\bstage div\b|모싱|크라우드서핑|스테이지 다이빙',
 'ensemble':r'\borchestra\b|\bchoir\b|\ba cappella\b|\bjazz trio\b|오케스트라|아카펠라|재즈 트리오'
}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=ASSETS/'photo_candidate_corpus_manifest.json'; m=json.loads(manifest.read_text())
records={}; bindings={}; hashes={};total=0;kinds=collections.Counter()
for module in m['modules']:
 p=ASSETS/module['file'];hashes[str(p.relative_to(REPO))]=sha(p);d=json.loads(p.read_text())
 if module['kind']=='candidates':
  for cid,r in d['candidates'].items():
   total+=1;kinds[r.get('record_kind','unknown')]+=1
   c=r.get('content',{});t=' '.join(str(c.get(k,'')) for k in ['en','ko','definition','aliases'])
   hits=[k for k,pat in PATTERNS.items() if re.search(pat,t,re.I)]
   if hits:records[cid]={'file':str(p.relative_to(REPO)),'clusters':hits,'record':r}
 elif module['kind']=='slot_bindings':
  for bid,r in d.get('slot_bindings',{}).items():bindings.setdefault(r.get('candidate_id'),[]).append({'id':bid,'file':str(p.relative_to(REPO)),'record':r})
for cid,r in records.items():r['bindings']=bindings.get(cid,[])
data={'scope':'lexical_inventory_not_semantic_or_retrieval_verification','snapshot_date':'2026-10-25 KST','manifest_sha256':sha(manifest),'module_count':len(m['modules']),'total_source_records':total,'record_kind_counts':dict(kinds),'unique_lexical_hit_records':len(records),'cluster_counts':{k:sum(k in r['clusters'] for r in records.values()) for k in PATTERNS},'patterns':PATTERNS,'source_hashes':hashes,'searched_fields':['content.en','content.ko','content.definition','content.aliases'],'limits':['No stemming, vector search or source-equivalence proof. Zero lexical hits is not proof of a semantic gap.','Case-insensitive MIDI matches midi skirt; conductor, wedge, turntable, 마이크로, 플루트 and datamoshing produce known non-music hits.','Source eligibility, full conditions, effects, branches, native qualification and actual retrieval need separate review.']}
(ROOT/'corpus-audit.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(ROOT/'existing-records.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in data.items() if k not in ['patterns','source_hashes']},ensure_ascii=False,indent=2))
