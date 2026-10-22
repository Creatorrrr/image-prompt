"""Network read only; writes research metadata and temporary text, never runtime data."""
import concurrent.futures, hashlib, json, re, tempfile, urllib.request
from html.parser import HTMLParser
from pathlib import Path
from research_sources import SOURCES
HERE=Path(__file__).resolve().parent
CACHE=Path(tempfile.gettempdir())/'lovecraftian-research-20261022'
class Text(HTMLParser):
    def __init__(self):super().__init__();self.parts=[];self.skip=0
    def handle_starttag(self,t,a):
        if t in ('script','style'):self.skip+=1
        if t in ('p','div','br','h1','h2','h3','li'):self.parts.append('\n')
    def handle_endtag(self,t):
        if t in ('script','style'):self.skip=max(0,self.skip-1)
    def handle_data(self,d):
        if not self.skip:self.parts.append(d)
def collect(s):
    s=dict(s)
    try:
        req=urllib.request.Request(s['url'],headers={'User-Agent':'Mozilla/5.0 (research; read-only)'})
        with urllib.request.urlopen(req,timeout=25) as r:
            raw=r.read();s.update(http_status=r.status,final_url=r.url)
        p=Text();p.feed(raw.decode('utf-8',errors='replace'))
        text=re.sub(r'[ \t]+',' ',''.join(p.parts));text=re.sub(r'\n\s*\n+','\n',text).strip()
        (CACHE/(s['source_id']+'.txt')).write_text(text)
        s.update(body_sha256=hashlib.sha256(raw).hexdigest(),text_sha256=hashlib.sha256(text.encode()).hexdigest(),text_chars=len(text),probe_hits=[])
        for probe in s['probes']:
            m=re.search(re.escape(probe),text,re.I)
            if m:s['probe_hits'].append(dict(probe=probe,offset=m.start()))
        s['access_status']='body_fetched_probe_review_pending' if s['probe_hits'] else 'body_fetched_no_probe_match'
    except Exception as e:s.update(access_status='fetch_failed',error=str(e))
    return s
if __name__=='__main__':
    CACHE.mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: rows=list(pool.map(collect,SOURCES))
    (HERE/'sources.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    for s in rows: print(s['source_id'],s['access_status'],s.get('text_chars',0),[x['probe'] for x in s.get('probe_hits',[])])
