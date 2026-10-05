#!/usr/bin/env python3
"""Acquire public publisher pages and their explicitly linked artwork.

This is a source receipt, not a runtime data generator. Observation and the
reviewed runtime bridge are authored separately after viewing the images.
"""
from __future__ import annotations
import hashlib
import html
import json
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import urlopen

HERE = Path(__file__).resolve().parent
CACHE = Path('/tmp/image-prompt-character-appearance-100-20261004')

class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.images = []; self.links = []; self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'img': self.images.append(attrs)
        if tag == 'a' and attrs.get('href'): self.links.append(attrs['href'])

def entries():
    groups = [
        ('hololive', 'Publisher talent page primary full-body artwork, retrieved 2026-10-04', '''
tokino-sora|토키노 소라|Tokino Sora
roboco-san|로보코|Robocosan
sakuramiko|사쿠라 미코|Sakura Miko
hoshimachi-suisei|호시마치 스이세이|Hoshimachi Suisei
azki|AZKi|AZKi
shirakami-fubuki|시라카미 후부키|Shirakami Fubuki
natsuiro-matsuri|나츠이로 마츠리|Natsuiro Matsuri
nakiri-ayame|나키리 아야메|Nakiri Ayame
yuzuki-choco|유즈키 초코|Yuzuki Choco
oozora-subaru|오오조라 스바루|Oozora Subaru
ookami-mio|오오카미 미오|Ookami Mio
nekomata-okayu|네코마타 오카유|Nekomata Okayu
inugami-korone|이누가미 코로네|Inugami Korone
usada-pekora|우사다 페코라|Usada Pekora
shiranui-flare|시라누이 플레어|Shiranui Flare
shirogane-noel|시로가네 노엘|Shirogane Noel
houshou-marine|호쇼 마린|Houshou Marine
tsunomaki-watame|츠노마키 와타메|Tsunomaki Watame
tokoyami-towa|토코야미 토와|Tokoyami Towa
himemori-luna|히메모리 루나|Himemori Luna
'''),
        ('guilty_gear_strive', 'GUILTY GEAR -STRIVE- publisher character-page main artwork', '''
sol|솔 배드가이|Sol Badguy
ky|카이 키스크|Ky Kiske
may|메이|May
axl|액슬 로우|Axl Low
chp|치프 자너프|Chipp Zanuff
pot|포템킨|Potemkin
mll|밀리아 레이지|Millia Rage
zat|자토 ONE|Zato-1
ram|램리썰 밸런타인|Ramlethal Valentine
leo|레오 화이트팽|Leo Whitefang
gio|지오바나|Giovanna
anji|미토 안지|Anji Mito
ino|이노|I-No
gld|골드루이스 디킨슨|Goldlewis Dickinson
jko|잭 오|Jack-O'
cos|해피 케이오스|Happy Chaos
bgt|브리짓|Bridget
sin|신 키스크|Sin Kiske
bed|베드맨?|Bedman?
ask|아스카 R♯|Asuka R♯
'''),
        ('tekken8', 'TEKKEN 8 publisher character sheet artwork, retrieved 2026-10-04', '''
jin-kazama|카자마 진|Jin Kazama
kazuya-mishima|미시마 카즈야|Kazuya Mishima
jun-kazama|카자마 준|Jun Kazama
paul-phoenix|폴 피닉스|Paul Phoenix
marshall-law|마샬 로우|Marshall Law
king|킹|King
lars-alexandersson|라스 알렉산더슨|Lars Alexandersson
ling-xiaoyu|링 샤오유|Ling Xiaoyu
nina-williams|니나 윌리엄스|Nina Williams
leroy-smith|리로이 스미스|Leroy Smith
asuka-kazama|카자마 아스카|Asuka Kazama
lili|리리|Lili
bryan-fury|브라이언 퓨리|Bryan Fury
hwoarang|화랑|Hwoarang
claudio-serafino|클라우디오 세라피노|Claudio Serafino
jack-8|잭 8|Jack-8
yoshimitsu|요시미츠|Yoshimitsu
alisa-bosconovitch|알리사 보스코노비치|Alisa Bosconovitch
zafina|자피나|Zafina
reina|레이나|Reina
'''),
        ('pokemon', 'Official Japanese Pokedex default form artwork; no Mega/regional forms', '''
0025|피카츄|Pikachu
0133|이브이|Eevee
0134|샤미드|Vaporeon
0135|쥬피썬더|Jolteon
0136|부스터|Flareon
0196|에브이|Espeon
0197|블래키|Umbreon
0470|리피아|Leafeon
0471|글레이시아|Glaceon
0700|님피아|Sylveon
0006|리자몽|Charizard
0009|거북왕|Blastoise
0003|이상해꽃|Venusaur
0094|팬텀|Gengar
0778|따라큐|Mimikyu
0448|루카리오|Lucario
0282|가디안|Gardevoir
0475|엘레이드|Gallade
0212|핫삼|Scizor
0445|한카리아스|Garchomp
'''),
        ('demon_slayer', 'TV anime Tanjiro Kamado Unwavering Resolve Arc publisher character artwork', '''
tanjiro|카마도 탄지로|Tanjiro Kamado
neduko|카마도 네즈코|Nezuko Kamado
zennitsu|아가츠마 젠이츠|Zenitsu Agatsuma
inosuke|하시비라 이노스케|Inosuke Hashibira
giyuu|토미오카 기유|Giyu Tomioka
urokodaki|우로코다키 사콘지|Sakonji Urokodaki
sabito|사비토|Sabito
makomo|마코모|Makomo
shinobu|코쵸 시노부|Shinobu Kocho
kanawo|츠유리 카나오|Kanao Tsuyuri
kyojurou|렌고쿠 쿄쥬로|Kyojuro Rengoku
tengen|우즈이 텐겐|Tengen Uzui
mitsuri|칸로지 미츠리|Mitsuri Kanroji
muichirou|토키토 무이치로|Muichiro Tokito
gyoumei|히메지마 교메이|Gyomei Himejima
obanai|이구로 오바나이|Obanai Iguro
sanemi|시나즈가와 사네미|Sanemi Shinazugawa
muzan|키부츠지 무잔|Muzan Kibutsuji
tamayo|타마요|Tamayo
yushiro|유시로|Yushiro
'''),
    ]
    rows = []
    for group, version, raw in groups:
        for line in raw.strip().splitlines():
            slug, ko, en = line.split('|')
            if group == 'hololive': url = f'https://hololive.hololivepro.com/en/talents/{slug}/'
            elif group == 'guilty_gear_strive': url = f'https://www.guiltygear.com/ggst/en/character/{slug}/'
            elif group == 'tekken8': url = f'https://tekken.com/fighters/{slug}'
            elif group == 'pokemon': url = f'https://zukan.pokemon.co.jp/detail/{slug}'
            else: url = f'https://kimetsu.com/anime/risshihen/character/?chara={slug}'
            rows.append(dict(id=f'C{len(rows)+1:03}', group=group, slug=slug, name_ko=ko,
                             name_en=en, version_scope=version, source_url=url))
    assert len(rows) == 100
    return rows

def fetch(url, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists(): return target.read_bytes()
    with urlopen(url, timeout=40) as response:
        raw = response.read()
    target.write_bytes(raw)
    return raw

def page(row):
    target = CACHE / 'pages' / (row['id'] + '.html')
    raw = fetch(row['source_url'], target)
    row['source_page_sha256'] = hashlib.sha256(raw).hexdigest()
    row['source_page_cache'] = str(target)
    text = raw.decode('utf-8')
    title = re.search(r'<title[^>]*>(.*?)</title>', text, re.S)
    row['source_page_title'] = html.unescape(title.group(1)) if title else ''
    return row

def main():
    rows = entries()
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(page, row) for row in rows]
        out=[]
        for row, future in zip(rows, futures):
            try: out.append(future.result())
            except Exception as e: row['acquisition_error'] = str(e); out.append(row)
    (HERE/'SOURCE-INVENTORY.json').write_text(json.dumps({
        'schema_version':'character-appearance-source-inventory/v1',
        'acquired_at_utc': datetime.now(timezone.utc).isoformat(),
        'rows':out}, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'rows':len(out),'errors':[{ 'id':x['id'], 'error':x['acquisition_error']}
          for x in out if x.get('acquisition_error')]},ensure_ascii=False))

if __name__ == '__main__': main()
