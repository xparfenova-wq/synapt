# -*- coding: utf-8 -*-
# Графические конструкции Synapt для постов и сторис: сети-связки в языке сайта.
# Каждая конструкция показывает смысл, а не украшает. Вывод: SVG + HTML для рендера в PNG.
import os, math, random, json

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(SRC), 'assets', 'graphics')
os.makedirs(OUT, exist_ok=True)

W = H = 1080
LIME = '#D0E865'; INK = '#12150A'; MILK = '#F4F6F5'; BG = '#131514'; SURF = '#151A18'
WHITE = '#F0F2F1'; MUTED = '#9AA5A1'; DIM = '#6E7975'

FONTS = ''.join(
    "@font-face{font-family:'JetBrains Mono';font-weight:%s;src:url('file://%s/fonts/JetBrainsMono-%s-%s.woff2') format('woff2')}" % (w, SRC, w, s)
    for w in ('400', '500') for s in ('latin', 'cyrillic')) + ''.join(
    "@font-face{font-family:'Manrope';font-weight:%s;src:url('file://%s/fonts/Manrope-%s-%s.woff2') format('woff2')}" % (w, SRC, w, s)
    for w in ('400', '500', '600') for s in ('latin', 'cyrillic'))

class T:
    """тема: фон, узлы, линии, подписи"""
    def __init__(self, bg, node, node_on, line, line_on, text, glow):
        self.bg, self.node, self.node_on, self.line, self.line_on, self.text, self.glow = bg, node, node_on, line, line_on, text, glow

DARK = T(BG, '#8C9591', LIME, 'rgba(240,242,241,.16)', LIME, MUTED, 'rgba(208,232,101,.35)')
LIMEBG = T(LIME, '#4A5526', INK, 'rgba(18,21,10,.26)', INK, '#3E4A1E', 'rgba(18,21,10,.22)')
MILKBG = T(MILK, '#4F5855', INK, 'rgba(18,21,10,.30)', '#6E8A18', '#4F5855', 'rgba(110,138,24,.32)')

def node(x, y, r, t, on=False, glow=False):
    s = ''
    if glow:
        s += '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (x, y, r * 4.2, t.glow)
    s += '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (x, y, r, t.node_on if on else t.node)
    return s

def line(a, b, t, on=False, w=1.6, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f"%s/>' % (a[0], a[1], b[0], b[1], t.line_on if on else t.line, w, d)

def label(x, y, s, t, size=22, anchor='start', color=None, fam='mono'):
    f = "'JetBrains Mono', monospace" if fam == 'mono' else "'Manrope', sans-serif"
    return '<text x="%.1f" y="%.1f" font-family="%s" font-size="%d" letter-spacing="%s" fill="%s" text-anchor="%s">%s</text>' % (
        x, y, f, size, '.06em' if fam == 'mono' else '-.01em', color or t.text, anchor, s)

def ring(cx, cy, r, t, dash='6 10', w=1.4, color=None):
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="%.1f" stroke-dasharray="%s"/>' % (cx, cy, r, color or t.line, w, dash)

def scatter(rng, n, box, mind=70):
    pts = []
    x0, y0, x1, y1 = box
    tries = 0
    while len(pts) < n and tries < 5000:
        tries += 1
        p = (rng.uniform(x0, x1), rng.uniform(y0, y1))
        if all(math.dist(p, q) > mind for q in pts): pts.append(p)
    return pts

def links(pts, maxd):
    out = []
    for i, a in enumerate(pts):
        for j, b in enumerate(pts):
            if j <= i: continue
            if math.dist(a, b) < maxd: out.append((i, j))
    return out

def wrap(inner, t, title=None, kick=None):
    s = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">' % (W, H, W, H)
    s += '<rect width="%d" height="%d" fill="%s"/>' % (W, H, t.bg)
    s += inner
    if kick: s += label(72, 96, kick, t, 22)
    if title: s += label(72, H - 84, title, t, 40, fam='sans', color=(INK if t.bg != BG else WHITE))
    return s + '</svg>'

# ── 01 синапс: сигнал переходит из одного кластера в другой
def g01(t):
    rng = random.Random(11)
    A = scatter(rng, 14, (110, 260, 470, 820), 80)
    B = scatter(rng, 14, (610, 260, 970, 820), 80)
    s = ''
    for i, j in links(A, 190): s += line(A[i], A[j], t)
    for i, j in links(B, 190): s += line(B[i], B[j], t)
    a = min(A, key=lambda p: -p[0]); b = min(B, key=lambda p: p[0])
    s += line(a, b, t, on=True, w=2.2)
    for p in A + B: s += node(p[0], p[1], 6, t)
    s += node(a[0], a[1], 9, t, on=True, glow=True) + node(b[0], b[1], 9, t, on=True, glow=True)
    m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    s += node(m[0], m[1], 5, t, on=True, glow=True)
    s += label(a[0] - 8, a[1] - 22, 'процесс', t, 20, 'end') + label(b[0] + 8, b[1] - 22, 'AI', t, 20)
    return s

# ── 02 карта процессов: узлы-отделы, узкие места подсвечены
def g02(t):
    names = ['заявки', 'продажи', 'закупки', 'документы', 'клиенты', 'знания', 'отчёты', 'склад']
    rng = random.Random(5)
    cx, cy, R = 540, 560, 300
    pts = []
    for i, n in enumerate(names):
        a = -math.pi / 2 + i * 2 * math.pi / len(names) + rng.uniform(-.12, .12)
        r = R + rng.uniform(-40, 40)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    s = ''
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if rng.random() < .42: s += line(pts[i], pts[j], t)
    hot = {1, 3, 6}
    for i, p in enumerate(pts):
        s += node(p[0], p[1], 8 if i in hot else 6, t, on=i in hot, glow=i in hot)
        dx = 16 if p[0] >= cx else -16
        s += label(p[0] + dx, p[1] + 7, names[i], t, 22, 'start' if dx > 0 else 'end')
    s += label(72, H - 150, 'узкие места – там, где уходит время', t, 22)
    return s

# ── 03 было / стало: хаос слева, порядок справа
def g03(t):
    rng = random.Random(21)
    A = scatter(rng, 26, (100, 240, 470, 860), 46)
    s = ''
    for i, j in links(A, 130): s += line(A[i], A[j], t, w=1.2)
    for p in A: s += node(p[0], p[1], 5, t)
    cols = [640, 760, 880, 1000]; rows = [300, 420, 540, 660, 780]
    B = [(x, y) for y in rows for x in cols]
    for i in range(len(rows)):
        for j in range(len(cols) - 1): s += line(B[i * 4 + j], B[i * 4 + j + 1], t, on=True, w=1.4)
    for j in range(len(cols)):
        for i in range(len(rows) - 1): s += line(B[i * 4 + j], B[(i + 1) * 4 + j], t, on=True, w=1.4)
    for p in B: s += node(p[0], p[1], 6, t, on=True)
    s += label(100, 200, 'было', t, 22) + label(640, 200, 'стало', t, 22)
    return s

# ── 04 три шага: чекап, десант, система
def g04(t):
    s = ''
    P = [(220, 700), (540, 520), (860, 340)]
    R = [40, 62, 88]
    for i in range(2): s += line(P[i], P[i + 1], t, on=True, w=2)
    for i, (p, r) in enumerate(zip(P, R)):
        s += ring(p[0], p[1], r, t, color=t.line_on)
        s += node(p[0], p[1], 9, t, on=True, glow=True)
        rng = random.Random(30 + i)
        for k in range(i * 4 + 3):
            a = rng.uniform(0, 2 * math.pi); rr = r * rng.uniform(.35, .85)
            q = (p[0] + rr * math.cos(a), p[1] + rr * math.sin(a))
            s += line(p, q, t, w=1) + node(q[0], q[1], 4, t)
    for p, n, d in zip(P, ['01 чекап', '02 десант', '03 система'], ['две недели', 'месяц', '3–5 недель']):
        s += label(p[0], p[1] + R[P.index(p)] + 44, n, t, 22, 'middle') + label(p[0], p[1] + R[P.index(p)] + 74, d, t, 18, 'middle', color=t.text)
    return s

# ── 05 компания и Synapt: пересечение
def g05(t):
    s = ''
    L, Rr = (400, 560), (680, 560)
    s += ring(L[0], L[1], 250, t) + ring(Rr[0], Rr[1], 250, t)
    rng = random.Random(7)
    A = scatter(rng, 9, (200, 380, 470, 740), 70)
    B = scatter(rng, 9, (610, 380, 880, 740), 70)
    m = (540, 560)
    for p in A: s += line(p, m, t, w=1)
    for p in B: s += line(p, m, t, w=1)
    for p in A + B: s += node(p[0], p[1], 5, t)
    s += node(m[0], m[1], 11, t, on=True, glow=True)
    s += label(400, 280, 'ваша компания', t, 22, 'middle') + label(680, 280, 'команда Synapt', t, 22, 'middle')
    return s

# ── 06 десант: специалист внутри команды, связи растут по неделям
def g06(t):
    s = ''
    rng = random.Random(9)
    team = scatter(rng, 18, (140, 260, 940, 860), 90)
    c = (540, 560)
    order = sorted(range(len(team)), key=lambda i: math.dist(team[i], c))
    for k, i in enumerate(order):
        on = k < 12
        s += line(c, team[i], t, on=on, w=1.6 if on else 1, dash=None if on else '4 8')
    for i, j in links(team, 170): s += line(team[i], team[j], t, w=.8)
    for k, i in enumerate(order):
        s += node(team[i][0], team[i][1], 6, t, on=k < 12)
    s += node(c[0], c[1], 12, t, on=True, glow=True)
    s += label(c[0], c[1] - 26, 'специалист Synapt', t, 20, 'middle')
    s += label(72, H - 150, 'неделя 1 – 3 человека, неделя 4 – вся команда', t, 22)
    return s

# ── 07 модули системы вокруг ядра, безопасный слой кольцом
def g07(t):
    s = ''
    c = (540, 560)
    names = ['продажи', 'аналитика', 'команда', 'экспертиза', 'операции', 'документы']
    s += ring(c[0], c[1], 330, t, dash='2 9', w=2, color=t.line_on)
    s += label(c[0], c[1] - 356, 'безопасный слой', t, 20, 'middle')
    for i, n in enumerate(names):
        a = -math.pi / 2 + i * 2 * math.pi / 6
        p = (c[0] + 230 * math.cos(a), c[1] + 230 * math.sin(a))
        s += line(c, p, t, on=True, w=1.4) + node(p[0], p[1], 9, t, on=True, glow=True)
        lx = p[0] + 44 * math.cos(a); ly = p[1] + 44 * math.sin(a) + 7
        anchor = 'middle' if abs(math.cos(a)) < .3 else ('start' if math.cos(a) > 0 else 'end')
        s += label(lx, ly, n, t, 22, anchor)
    s += node(c[0], c[1], 14, t, on=True, glow=True)
    return s

# ── 08 разбор звонков: 300 точек, было 5 в разборе, стало все
def g08(t):
    s = ''
    cols, rows = 20, 15
    x0, y0, gap = 110, 260, 45
    rng = random.Random(3)
    hot = set(rng.sample(range(cols * rows), 5))
    for i in range(cols * rows):
        x = x0 + (i % cols) * gap; y = y0 + (i // cols) * gap
        s += node(x, y, 5 if i in hot else 3.5, t, on=True, glow=i in hot) if i in hot else node(x, y, 3.5, t)
    s += label(72, 200, '300 разговоров в месяц', t, 22)
    s += label(72, H - 150, 'руководитель слушал 5', t, 22)
    s += label(H - 72 if False else W - 72, H - 150, 'с AI в разборе все 300', t, 22, 'end', color=t.node_on)
    return s

# ── 09 знания: стопка документов превращается в сеть
def g09(t):
    s = ''
    for i in range(7):
        y = 330 + i * 52
        s += '<rect x="130" y="%d" width="300" height="34" rx="6" fill="none" stroke="%s" stroke-width="1.4"/>' % (y, t.line)
    rng = random.Random(13)
    B = scatter(rng, 16, (620, 280, 980, 840), 70)
    for i, j in links(B, 160): s += line(B[i], B[j], t, on=True, w=1.2)
    for p in B: s += node(p[0], p[1], 6, t, on=True)
    s += line((430, 512), (620, 560), t, on=True, w=2, dash='3 8')
    s += label(130, 290, '800 страниц методики в PDF', t, 22) + label(620, 240, 'отвечает клиенту 24/7', t, 22)
    return s

# ── 10 безопасный контур: данные внутри, модель за границей
def g10(t):
    s = ''
    c = (540, 560)
    s += '<rect x="170" y="230" width="740" height="660" rx="40" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="4 10"/>' % t.line_on
    rng = random.Random(17)
    A = scatter(rng, 14, (240, 300, 840, 820), 90)
    for i, j in links(A, 200): s += line(A[i], A[j], t)
    for p in A: s += node(p[0], p[1], 6, t)
    gate = (910, 560)
    s += node(gate[0], gate[1], 10, t, on=True, glow=True)
    s += line(gate, (1010, 560), t, on=True, w=2, dash='3 6')
    s += node(1010, 560, 5, t, on=True)
    s += label(190, 210, 'ваш контур', t, 22) + label(1010, 520, 'модель', t, 20, 'end')
    s += label(72, H - 150, 'наружу уходят только разрешённые поля', t, 22)
    return s

# ── 11 лестница: пять ступеней воронки
def g11(t):
    s = ''
    P = [(160, 800), (350, 700), (540, 600), (730, 500), (920, 400)]
    for i in range(4): s += line(P[i], P[i + 1], t, on=True, w=1.8)
    for i, p in enumerate(P):
        s += node(p[0], p[1], 8 if i < 4 else 12, t, on=True, glow=i == 4)
        s += line((p[0], p[1] + 20), (p[0], 880), t, w=1, dash='2 8')
    names = ['не видит', 'видит', 'выбирает тип', 'сравнивает', 'готов']
    for p, n in zip(P, names): s += label(p[0], 920, n, t, 20, 'middle')
    return s

# ── 12 где AI не нужен: одна прямая линия среди сети
def g12(t):
    s = ''
    rng = random.Random(23)
    A = scatter(rng, 22, (120, 260, 960, 860), 80)
    for i, j in links(A, 170): s += line(A[i], A[j], t, w=1)
    for p in A: s += node(p[0], p[1], 5, t)
    a, b = (150, 560), (930, 560)
    s += line(a, b, t, on=True, w=3)
    s += node(a[0], a[1], 9, t, on=True, glow=True) + node(b[0], b[1], 9, t, on=True, glow=True)
    s += label(72, H - 150, 'иногда задача решается процессом, без AI', t, 22)
    return s

ITEMS = [
    ('01-synapse', g01, DARK, 'Синапс: где сигнал переходит', 'о студии'),
    ('02-process-map', g02, DARK, 'Карта процессов с узкими местами', 'AI-чекап'),
    ('03-before-after', g03, LIMEBG, 'Было и стало', 'кейс'),
    ('04-three-steps', g04, DARK, 'Три шага: чекап, десант, система', 'услуги'),
    ('05-company-synapt', g05, MILKBG, 'Компания и команда Synapt', 'почему мы'),
    ('06-desant', g06, DARK, 'Месяц внутри команды', 'AI-десант'),
    ('07-modules', g07, DARK, 'Модули системы', 'AI-система'),
    ('08-calls', g08, LIMEBG, 'Разбор всех разговоров', 'кейс, продажи'),
    ('09-knowledge', g09, DARK, 'Знания начинают отвечать', 'кейс, экспертиза'),
    ('10-contour', g10, DARK, 'Данные не покидают контур', 'безопасность'),
    ('11-ladder', g11, MILKBG, 'Пять ступеней клиента', 'воронка'),
    ('12-no-ai', g12, DARK, 'Где AI не нужен', 'честность'),
]

manifest = []
for name, fn, theme, title, kick in ITEMS:
    svg = wrap(fn(theme), theme, title=title, kick=kick)
    svg_path = os.path.join(OUT, 'graphic-%s.svg' % name)
    open(svg_path, 'w', encoding='utf-8').write(svg)
    html = '<!doctype html><meta charset="utf-8"><style>%s body{margin:0;background:%s}</style>%s' % (FONTS, theme.bg, svg)
    html_path = os.path.join(OUT, '_%s.html' % name)
    open(html_path, 'w', encoding='utf-8').write(html)
    manifest.append(dict(html=html_path, png=os.path.join(OUT, 'graphic-%s.png' % name), w=W, h=H))
json.dump(manifest, open(os.path.join(OUT, '_manifest.json'), 'w'))
print(len(manifest), 'graphics ->', OUT)
