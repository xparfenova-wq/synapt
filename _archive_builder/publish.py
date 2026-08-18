# -*- coding: utf-8 -*-
"""Собирает страницы услуг и кейсов и кладёт их в site/ для выкладки на synapt.tech

Запуск:  python3 builder/publish.py
Потом:   git add -A && git commit -m "правка страницы" && git push
Сервер подхватит изменения в течение двух минут.
"""
import sys as _sys
if '--force' not in _sys.argv:
    print('СТОП: генератор отстал от живых страниц в site/ (правки 16–18.08 сделаны напрямую). Запуск перезапишет их. Если точно нужно: python3 builder/publish.py --force')
    raise SystemExit(1)
import pathlib, re, shutil, subprocess, sys

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
SITE = ROOT / 'site'

# какая собранная папка какой странице сайта соответствует
PAGES = {
    'ai-desant': 'desant',
    'globaldent': 'globaldent',
    'innorto': 'innorto',
    'bezopasnost': 'safe',
    'otdel-prodazh': 'prodazh',
}

# внешние адреса черновиков переписываем на пути внутри сайта
LINKS = [
    (r'https://synapt-site\.vercel\.app/?', '/'),
    (r'https://synapt-(?:audit14|checkup)\.vercel\.app/?', '/checkup/'),
    (r'https://synapt-ai-desant\.vercel\.app/?', '/desant/'),
    (r'https://synapt-globaldent\.vercel\.app/?', '/globaldent/'),
    (r'https://synapt-innorto\.vercel\.app/?', '/innorto/'),
    (r'https://synapt-(?:safe(?:-layer)?|bezopasnost)\.vercel\.app/?', '/safe/'),
    (r'https://synapt-(?:otdel-)?prodazh\.vercel\.app/?', '/prodazh/'),
    (r'https://synapt-content\.vercel\.app/?', '/content/'),
    # видимый текст адреса в подвале тоже приводим к домену
    (r'synapt-[a-z0-9-]+\.vercel\.app', 'synapt.tech'),
]

subprocess.run([sys.executable, str(HERE / 'build.py')], cwd=HERE, check=True)

out = HERE / 'out'
made = []
for slug, dest in PAGES.items():
    src = out / slug / 'index.html'
    if not src.exists():
        continue
    html = src.read_text(encoding='utf-8')
    for pat, rep in LINKS:
        html = re.sub(pat, rep, html)
    target = SITE / dest
    target.mkdir(parents=True, exist_ok=True)
    (target / 'index.html').write_text(html, encoding='utf-8')
    made.append(dest)

print('обновлены страницы:', ', '.join(made) or 'ни одной')
print('дальше: git add -A && git commit -m "правка" && git push')
