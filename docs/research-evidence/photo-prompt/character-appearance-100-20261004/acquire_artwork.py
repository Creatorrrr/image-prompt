#!/usr/bin/env python3
"""Download only image URLs actually published in each acquired source page."""
from __future__ import annotations
import hashlib
import html
import io
import json
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse
from PIL import Image, ImageDraw, ImageFont
from acquire_sources import HERE, CACHE, Tags, fetch

def artwork(row):
    assert not row.get('acquisition_error'), row
    text = Path(row['source_page_cache']).read_text()
    tags = Tags(text); url = row['source_url']; group = row['group']
    if group == 'hololive':
        images = [x for x in tags.images if x.get('alt') == '全身画像']
        assert images, row['id']
        chosen = next((x for x in images if x.get('class') == 'active'), images[0])
        source = chosen['src']; label = 'primary full-body artwork'
    elif group == 'guilty_gear_strive':
        images = [x for x in tags.images if '/uploads/' in x.get('src','') and re.search(r'/chara(?:[_.-].*)?\.(?:png|webp)',x['src'])]
        assert images, row['id']
        source = images[0]['src']; label = 'main character-page artwork'
    elif group == 'pokemon':
        data = json.loads(re.search(r'<script id="json-data"[^>]*>(.*?)</script>',text,re.S).group(1))
        p = data['pokemon']; assert p['no'] == row['slug'] and p['sub'] == 0
        source = p['image_l']; label = 'official Pokedex default form artwork'
        row['publisher_display_name'] = p['name']
    elif group == 'demon_slayer':
        images=[x for x in tags.images if 'img_chara_' in x.get('src','')]
        assert images, row['id']
        source=images[0]['src'];label='Unwavering Resolve Arc character-page illustration'
    else:
        m=re.search(r'<script[^>]*id="tekken-state"[^>]*>(.*?)</script>',text,re.S)
        data=json.loads(html.unescape(m.group(1)).replace('&q;','"'))['apollo.state']
        assets=[v for v in data.values() if isinstance(v,dict) and v.get('__typename')=='Asset']
        prefix=row['slug'].split('-')[0]
        candidates=[a for a in assets if 'character-wall-art-lrg' in a.get('fileName','').lower()
                    and (prefix in a['fileName'].lower() or prefix in str(a.get('altText','')).lower())]
        if not candidates:
            candidates=[a for a in assets if 'character-art-lrg' in a.get('fileName','').lower()
                        and prefix in a['fileName'].lower()]
        if not candidates:
            candidates=[a for a in assets if prefix in a.get('fileName','').lower()
                        and ('fighter-800px' in a['fileName'].lower() or 'character@' in a['fileName'].lower())]
        if not candidates:
            candidates=[a for a in assets if re.search(r'01.*権利表記',a.get('fileName',''))]
        assert candidates, (row['id'],row['slug'])
        source=candidates[0]['url'];label=candidates[0]['fileName']
    source=urljoin(url,html.unescape(source))
    ext=Path(urlparse(source).path).suffix or '.image'
    target=CACHE/'originals'/(row['id']+ext)
    raw=fetch(source,target)
    im=Image.open(io.BytesIO(raw));im.load()
    row.update(artwork_url=source,artwork_label=label,artwork_cache=str(target),
               artwork_sha256=hashlib.sha256(raw).hexdigest(),artwork_bytes=len(raw),
               artwork_dimensions=list(im.size),artwork_format=im.format)
    return row

def sheets(rows):
    dest=CACHE/'inspection-sheets';dest.mkdir(exist_ok=True)
    font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',23)
    for start in range(0,len(rows),5):
        batch=rows[start:start+5];canvas=Image.new('RGB',(2500,1100),'#eeeeee');draw=ImageDraw.Draw(canvas)
        for i,row in enumerate(batch):
            if not row.get('artwork_cache'):continue
            im=Image.open(row['artwork_cache']).convert('RGBA')
            # A reading projection only; original source bytes remain untouched.
            bbox=im.getbbox()
            if bbox:im=im.crop(bbox)
            im.thumbnail((490,1000))
            canvas.paste(im,(i*500+(500-im.width)//2,58),im)
            draw.text((i*500+12,10),row['id']+' '+row['name_en'],font=font,fill='black')
        p=dest/f'{batch[0]["id"]}-{batch[-1]["id"]}.jpg';canvas.save(p,quality=95)

def main():
    inventory=json.loads((HERE/'SOURCE-INVENTORY.json').read_text())
    rows=inventory['rows'];out=[]
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures=[pool.submit(artwork,r) for r in rows]
        for row,f in zip(rows,futures):
            try:out.append(f.result())
            except Exception as e:row['artwork_error']=str(e);out.append(row)
    (HERE/'SOURCE-RECEIPTS.json').write_text(json.dumps({
        'schema_version':'character-appearance-source-receipts/v1',
        'acquired_at_utc':datetime.now(timezone.utc).isoformat(),
        'artwork_scope':'publisher-selected artwork snapshot, not all costumes or all views',
        'rows':out},ensure_ascii=False,indent=2)+'\n')
    sheets(out)
    print(json.dumps({'rows':len(out),'artworks':sum('artwork_cache' in x for x in out),
                     'errors':[{'id':x['id'],'error':x['artwork_error']} for x in out if x.get('artwork_error')]},ensure_ascii=False))

if __name__=='__main__':main()
