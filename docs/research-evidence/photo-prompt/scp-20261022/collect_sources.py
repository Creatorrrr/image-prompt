"""Read-only public SCP page capture; writes only research metadata and /tmp cache."""
import concurrent.futures, hashlib, json, pathlib, re, urllib.request
from html.parser import HTMLParser

HERE = pathlib.Path(__file__).resolve().parent
CACHE = pathlib.Path('/tmp/image-prompt-scp-research-20261022')

class MainText(HTMLParser):
    def __init__(self):
        super().__init__(); self.depth = 0; self.parts = []; self.links = []; self.skip = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'div' and a.get('id') == 'page-content': self.depth = 1
        elif self.depth and tag == 'div': self.depth += 1
        if self.depth:
            if tag in ('script', 'style'): self.skip += 1
            if tag in ('p','li','br','h1','h2','h3','h4','tr','div'): self.parts.append('\n')
            if tag == 'a' and a.get('href'): self.links.append(a['href'])
    def handle_endtag(self, tag):
        if self.depth and tag in ('script','style'): self.skip = max(0,self.skip-1)
        if self.depth and tag == 'div': self.depth -= 1
    def handle_data(self, data):
        if self.depth and not self.skip: self.parts.append(data)

def fetch(url):
    key = hashlib.sha256(url.encode()).hexdigest()[:16]
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (research; public source reading)'})
        with urllib.request.urlopen(req, timeout=20) as r: raw=r.read(); status=r.status; final=r.url
        html = raw.decode('utf-8','replace'); p=MainText(); p.feed(html)
        body = re.sub(r'[ \t]+',' ',''.join(p.parts)); body=re.sub(r'\n\s*\n+', '\n', body).strip()
        title = re.search(r'<title>(.*?)</title>',html,re.S)
        rev = re.search(r'page revision:.*?last edited:.*?</',html,re.S)
        (CACHE/(key+'.txt')).write_text(body)
        author=re.search(r'Cite this page as:\s*"[^"\n]+"\s+by\s+(.+?),\s+from the SCP Wiki',body)
        return {'url':url,'final_url':final,'http_status':status,'title':title.group(1) if title else '', 'text_chars':len(body),'text_sha256':hashlib.sha256(body.encode()).hexdigest(),'html_sha256':hashlib.sha256(raw).hexdigest(),'licensebox_author':author.group(1).strip() if author else None,'revision_html':rev.group(0)[:350] if rev else None,'cache_file':str(CACHE/(key+'.txt')),'links':sorted(set(p.links)),'access_status':'body_available' if body else 'empty_body','retrieved_on':'2026-10-22'}
    except Exception as e: return {'url':url,'access_status':'failed','error':str(e),'retrieved_on':'2026-10-22'}

if __name__ == '__main__':
    CACHE.mkdir(exist_ok=True)
    ref=json.loads((HERE/'reference-glossary.json').read_text())
    urls={x['url'] for x in ref['links']}
    urls.update('https://scp-wiki.wikidot.com/'+s for s in ['guide-for-newcomers','licensing-guide','image-use-policy','anomaly-classification-system-guide','sarkicism-hub','antimemetics-division-hub','fear-alone','scp-5411','scp-5866','scp-231','scp-610','scp-173','scp-3008'])
    rows=list(concurrent.futures.ThreadPoolExecutor(max_workers=6).map(fetch,sorted(urls)))
    (HERE/'SOURCE-ACCESS.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'pages':len(rows),'available':sum(x['access_status']=='body_available' for x in rows),'failures':[{k:v for k,v in x.items() if k in ('url','error','text_chars','access_status')} for x in rows if x['access_status']!='body_available']},ensure_ascii=False))
