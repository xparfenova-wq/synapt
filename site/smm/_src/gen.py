# -*- coding: utf-8 -*-
# Генератор HTML-слайдов Synapt для соцсетей. Тексты дословно с synapt.tech
import json, os, re, html as H

ROOT = '/private/tmp/claude-501/-Users-xeniaparfenova-A-AAM/b8920e5c-bebf-49bd-9213-58265736edd5/scratchpad/smm'
SRC = os.path.dirname(os.path.abspath(__file__))  # _src: шрифты и logo.svg живут здесь, в ROOT только ссылки на них
os.makedirs(ROOT, exist_ok=True)
for _f in ('fonts', 'logo.svg'):
    if not os.path.exists(os.path.join(ROOT, _f)):
        os.symlink(os.path.join(SRC, _f), os.path.join(ROOT, _f))
OUT_HTML = os.path.join(ROOT, 'html')
OUT_PNG = os.path.expanduser('~/business-shared/_drafts/synapt-repo/site/smm/assets')
os.makedirs(OUT_HTML, exist_ok=True); os.makedirs(OUT_PNG, exist_ok=True); os.makedirs(os.path.join(OUT_PNG, 'svg'), exist_ok=True)
LOGO = open(os.path.join(ROOT, 'logo.svg'), encoding='utf-8').read()
LOGO = LOGO.replace('class="lg-mark"', '')

NB = ' '
SHORT = r'(в|во|и|а|с|со|к|ко|у|о|об|на|не|ни|из|по|за|от|до|для|как|что|но|же|ли|под|при|без|над|то|это|где|или|уже|ещё|бы|чем|там|тут|так|вы|мы|её|их|им|ей|он|она|они|тем|том|все|всё|нас|вас|вам|нам|его|ему|ней|них|кто|чтобы|если|через|один|одну|две|три|раз|мин|ч|сек)'

def nb(s):
    s = H.escape(s, quote=False)
    # число + разряд: 19 900, 1 500+, 25-35 ч
    s = re.sub(r'(\d)\s(\d{3})', r'\1' + NB + r'\2', s)
    # число + единица
    s = re.sub(r'(\d\+?)\s(₽|дней|день|дня|минут|минуты|мин|секунд|недел\w*|ч|часов|часа|час|человек|отдела|отдел|тыс\.|тысяч|сотрудников|из|карт|мес\.|разговоров|отзывов|пар|проекта|систем\w*|звонков|лет|записей|уроков)', r'\1' + NB + r'\2', s)
    s = re.sub(r'(из)\s(\d)', r'\1' + NB + r'\2', s)
    s = re.sub(r'(от|до|за|в)\s(\d)', r'\1' + NB + r'\2', s)
    s = re.sub(r'(тыс\.)\s(₽|руб\.)', r'\1' + NB + r'\2', s)
    s = re.sub(r'([A-Za-z]+-[А-Яа-яЁё]+)', r'<span style="white-space:nowrap">\1</span>', s)
    # диапазоны вида 3-5 недель не рвём по дефису
    s = re.sub(r'(\d+-\d+(?:' + NB + r'[а-яё]+)?)', r'<span style="white-space:nowrap">\1</span>', s)
    # предлоги и союзы
    # lookbehind вместо захвата: цепочки коротких слов («и как», «а не») обрабатываются целиком
    for _ in range(2):
        s = re.sub(r'(?:^|(?<=[\s(«]))' + SHORT + r'\s', lambda m: m.group(1) + NB, s, flags=re.I)
    return s

FONTS = open(os.path.join(ROOT, 'fonts', 'local.css'), encoding='utf-8').read().replace('%', '%%')
CSS = FONTS + '''

:root{--bg:#0E1211;--surface:#151A18;--milk:#F4F6F5;--text:#E8EEEC;--text2:#C4CAC7;--muted:#9AA5A1;--dim:#6E7975;--line:#232A28;--line2:#2C3532;--accent:#D0E865;--ink:#0E1211;
 --sans:"Manrope",system-ui,sans-serif;--mono:"JetBrains Mono",ui-monospace,monospace}
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:var(--bg);width:%(w)dpx;height:%(h)dpx;overflow:hidden}
body{color:var(--text);font-family:var(--sans);-webkit-font-smoothing:antialiased;position:relative}
.frame{position:absolute;inset:0;padding:%(pt)dpx 90px %(pb)dpx;display:flex;flex-direction:column;background:var(--bg)}
.frame.milk{background:var(--milk);color:var(--ink)}
.frame.graphite{background:var(--surface)}
.top{display:flex;justify-content:space-between;align-items:center;font-family:var(--mono);font-size:%(kick)dpx;letter-spacing:.06em;line-height:1;height:%(kick)dpx}
.top .kick{color:var(--accent)}
.top .idx{color:var(--dim)}
.milk .top .idx{color:#8A928F}
.body{flex:1;display:flex;flex-direction:column;justify-content:center;gap:40px;min-height:0}
.body.start{justify-content:flex-start;padding-top:60px}
.foot{display:flex;justify-content:space-between;align-items:center;height:48px}
.foot .logo{color:#8A928F;height:%(logo)dpx;display:block}
.foot .logo svg{height:100%%;width:auto;display:block}
.milk .foot .logo{color:#0E1211}
.foot .site{font-family:var(--mono);font-size:%(kick)dpx;color:var(--dim);letter-spacing:.02em}
.milk .foot .site{color:#8A928F}
h1{font-weight:600;letter-spacing:-.03em;line-height:1.05;color:#fff}
.milk h1{color:var(--ink)}
h1.xl{font-size:%(h_xl)dpx}
h1.l{font-size:%(h_l)dpx}
h1.m{font-size:%(h_m)dpx;line-height:1.1}
p.tx{font-size:%(tx)dpx;line-height:1.42;color:var(--text2);letter-spacing:-.005em}
p.tx.center{text-align:center}
.milk p.tx{color:#2B3330}
.center{text-align:center;align-items:center}
.metrics{display:flex;flex-direction:column;gap:44px}
.metrics.row{flex-direction:row;gap:60px}
.metrics.row>div{flex:1}
.num{font-family:var(--mono);font-weight:500;letter-spacing:-.03em;line-height:1;color:#fff;white-space:nowrap}
.num.big{font-size:%(n_big)dpx}
.num.mid{font-size:%(n_mid)dpx}
.num.sm{font-size:%(n_sm)dpx}
.num .tail{font-size:.5em;color:var(--text2);letter-spacing:0}
.num.ac{color:var(--accent)}
.cap{font-family:var(--mono);font-size:%(cap)dpx;color:var(--muted);margin-top:14px;line-height:1.35;letter-spacing:.01em}
.chip{display:inline-flex;align-self:flex-start;border:2px solid var(--line2);border-radius:999px;padding:14px 26px;font-family:var(--mono);font-size:%(kick)dpx;color:var(--muted);letter-spacing:.02em}
.list{display:flex;flex-direction:column;gap:%(gap)dpx}
.it{display:grid;grid-template-columns:%(ncol)dpx 1fr;gap:26px;align-items:baseline}
.wide .it{grid-template-columns:200px 1fr}
.wide2 .it{grid-template-columns:300px 1fr}
.it b{font-family:var(--mono);font-weight:500;font-size:%(cap)dpx;color:var(--accent);letter-spacing:.02em}
.it .t{font-size:%(tx)dpx;line-height:1.3;color:#fff;font-weight:500;letter-spacing:-.01em}
.it .s{font-size:%(cap)dpx;line-height:1.35;color:var(--muted);margin-top:8px}
.milk .it .t{color:var(--ink)}
.milk .it .s{color:#5A6360}
.cards{display:flex;flex-direction:column;gap:22px}
.card{border:2px solid var(--line);border-radius:28px;padding:36px 40px;background:var(--surface)}
.card.on{border-color:rgba(208,232,101,.6);background:rgba(208,232,101,.07)}
.card .k{font-family:var(--mono);font-size:%(kick)dpx;color:var(--dim);letter-spacing:.06em;margin-bottom:16px}
.card.row{display:grid;grid-template-columns:200px 1fr;gap:24px;align-items:baseline;padding:30px 40px}
.card.row .k{margin:0}
.card.on .k{color:var(--accent)}
.card .v{font-size:%(tx)dpx;line-height:1.35;color:#fff;font-weight:500;letter-spacing:-.01em}
.card .v span{color:var(--muted);font-weight:400}
.card .nm{font-size:%(tx)dpx;color:#fff;font-weight:600;letter-spacing:-.01em;line-height:1.2}
.card .rl{font-family:var(--mono);font-size:%(cap)dpx;color:var(--muted);margin-top:12px;line-height:1.35}
.card .num{margin-top:6px}
.btn{display:inline-flex;align-self:flex-start;background:var(--accent);color:var(--ink);border-radius:22px;font-size:%(tx)dpx;font-weight:600;padding:30px 54px;letter-spacing:-.01em;line-height:1}
.quotes{display:flex;flex-direction:column;gap:%(gap)dpx}
.q{font-size:%(tx)dpx;line-height:1.38;color:#fff;font-weight:500;letter-spacing:-.01em;padding-left:44px;border-left:5px solid var(--accent)}
.q.plain{border:0;padding:0;font-size:%(h_m)dpx;line-height:1.16;font-weight:600;letter-spacing:-.025em}
.q .who{display:block;font-family:var(--mono);font-size:%(cap)dpx;color:var(--muted);margin-top:22px;font-weight:400;letter-spacing:.01em}
.q .m{color:var(--accent)}
.net{position:absolute;inset:0;z-index:0;pointer-events:none}
.frame>*:not(.net){position:relative;z-index:1}
.ac{color:var(--accent)}
.hlcover{position:absolute;inset:0;background:var(--surface);display:flex;align-items:center;justify-content:center;flex-direction:column;gap:56px}
.hlcover .w{font-family:var(--mono);font-size:120px;color:#fff;letter-spacing:.02em;line-height:1;text-align:center;white-space:nowrap}
.hlcover .mark{width:150px;height:150px;color:var(--accent)}
.frame.fr-lime{--bg:#D0E865;--surface:rgba(18,21,10,.06);--text:#12150A;--text2:#2A3115;--muted:#3E4A1E;--dim:#55622B;--line:rgba(18,21,10,.22);--accent:#12150A;--milk:#12150A}
.frame.fr-lime .kick,.frame.fr-lime .idx{color:#3E4A1E}
.frame.fr-lime h1{color:#12150A}
.frame.fr-lime .tx{color:#2A3115}
.frame.fr-milk{--bg:#F4F6F5;--surface:rgba(18,21,10,.04);--text:#12150A;--text2:#2E3532;--muted:#5A6560;--dim:#78827E;--line:rgba(18,21,10,.14);--accent:#5F7A16;--milk:#12150A}
.frame.fr-milk .kick,.frame.fr-milk .idx{color:#78827E}
.frame.fr-milk h1{color:#12150A}
.frame.fr-milk .tx{color:#2E3532}
.card .ph{width:148px;height:148px;border-radius:50%%;object-fit:cover;display:block;margin-bottom:22px}
.card.pcard{display:flex;align-items:center;gap:36px}
.card.pcard .ph{margin-bottom:0;flex:none}
'''

def scale(fmt):
    if fmt == 'post':
        return dict(w=1080, h=1350, pt=90, pb=90, kick=36, logo=54, h_xl=96, h_l=84, h_m=70, tx=48, n_big=132, n_mid=108, n_sm=84, cap=36, gap=44, ncol=80)
    return dict(w=1080, h=1920, pt=250, pb=250, kick=44, logo=58, h_xl=108, h_l=86, h_m=72, tx=50, n_big=140, n_mid=110, n_sm=95, cap=44, gap=48, ncol=96)

def net_svg(w, h, seed=3, on=(4, 11)):
    import random
    r = random.Random(seed)
    pts = [(r.randint(60, w-60), r.randint(60, h-60)) for _ in range(26)]
    els = []
    for i, (x, y) in enumerate(pts):
        for j, (x2, y2) in enumerate(pts):
            if j <= i: continue
            d = ((x-x2)**2 + (y-y2)**2) ** .5
            if d < 330:
                els.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#1C2321" stroke-width="2"/>' % (x, y, x2, y2))
    cand = sorted([i for i,(x,y) in enumerate(pts) if 0.12*h < y < 0.42*h and x > 0.68*w], key=lambda i: -pts[i][0])
    on = tuple(cand[:2])
    for i, (x, y) in enumerate(pts):
        if i in on:
            els.append('<circle cx="%d" cy="%d" r="9" fill="#D0E865"/><circle cx="%d" cy="%d" r="22" fill="#D0E865" opacity=".18"/>' % (x, y, x, y))
        else:
            els.append('<circle cx="%d" cy="%d" r="6" fill="#2A3330"/>' % (x, y))
    return '<svg class="net" viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" opacity=".5">%s</svg>' % (w, h, ''.join(els))

def page(fmt, inner, idx=None, kick='', net=False, cls='', logo=True, site=True):
    sc = scale(fmt)
    top = '<div class="top"><span class="kick">%s</span><span class="idx">%s</span></div>' % (nb(kick), idx or '')
    foot = '<div class="foot">%s%s</div>' % (
        '<span class="logo">%s</span>' % LOGO if logo else '<span></span>',
        '<span class="site">synapt.tech</span>' if site else '')
    return '<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>%s</style></head><body><div class="frame %s">%s%s%s%s</div></body></html>' % (
        CSS % sc, cls, net_svg(sc['w'], sc['h']) if net else '', top, inner, foot)

# ---------- блоки ----------
def thesis(title, text=None, size='l', center=False, start=False):
    b = '<div class="body%s%s">' % (' center' if center else '', ' start' if start else '')
    b += '<h1 class="%s">%s</h1>' % (size, nb(title))
    if text: b += '<p class="tx%s">%s</p>' % (' center' if center else '', nb(text))
    return b + '</div>'

def metric_block(num, cap, size='mid', tail=None, ac=False):
    t = ' <span class="tail">%s</span>' % nb(tail) if tail else ''
    return '<div><div class="num %s%s">%s%s</div><div class="cap">%s</div></div>' % (size, ' ac' if ac else '', nb(num), t, nb(cap))

def metrics(title, items, kick_chip=None, text=None, size='mid', row=False, tsize='m', text_after=False):
    b = '<div class="body">'
    if kick_chip: b += '<span class="chip">%s</span>' % nb(kick_chip)
    if title: b += '<h1 class="%s">%s</h1>' % (tsize, nb(title))
    if text and not text_after: b += '<p class="tx">%s</p>' % nb(text)
    b += '<div class="metrics%s">' % (' row' if row else '')
    for it in items:
        b += metric_block(it[0], it[1], size, it[2] if len(it) > 2 else None)
    b += '</div>'
    if text and text_after: b += '<p class="tx">%s</p>' % nb(text)
    return b + '</div>'

def lst(title, items, text=None, tsize='m', numbered=True, wide=False):
    b = '<div class="body%s">' % ((' ' + wide) if isinstance(wide, str) else (' wide' if wide else ''))
    b += '<h1 class="%s">%s</h1>' % (tsize, nb(title))
    if text: b += '<p class="tx">%s</p>' % nb(text)
    b += '<div class="list">'
    for i, it in enumerate(items, 1):
        if numbered:
            n = '%02d' % i; t = it[0]; s = it[1] if len(it) > 1 else None
        else:
            n = it[0]; t = it[1]; s = it[2] if len(it) > 2 else None
        b += '<div class="it"><b>%s</b><div><div class="t">%s</div>%s</div></div>' % (nb(n), nb(t), '<div class="s">%s</div>' % nb(s) if s else '')
    return b + '</div></div>'

def plist(items, off):
    # два принципа на кадр: номер, заголовок и описание дословно с главной synapt.tech
    b = '<div class="body"><div class="list" style="gap:72px">'
    for i, (t, d) in enumerate(items[off:off+2], off+1):
        b += '<div class="it"><b>%02d</b><div><div class="t">%s</div><div class="s">%s</div></div></div>' % (i, nb(t), nb(d))
    return b + '</div></div>'

def cards(title, items, on_last=False, text=None, tsize='m', all_on=False, row=False):
    b = '<div class="body">'
    if title: b += '<h1 class="%s">%s</h1>' % (tsize, nb(title))
    if text: b += '<p class="tx">%s</p>' % nb(text)
    b += '<div class="cards">'
    for i, it in enumerate(items):
        on = all_on or (on_last and i == len(items) - 1)
        b += '<div class="card%s%s"><div class="k">%s</div><div class="v">%s</div></div>' % (' on' if on else '', ' row' if row else '', nb(it[0]), nb(it[1]))
    return b + '</div></div>'

def photo_uri(path):
    import base64 as _b
    return 'data:image/jpeg;base64,' + _b.b64encode(open(path, 'rb').read()).decode()

def team(title, people, text=None):
    b = '<div class="body"><h1 class="m">%s</h1>' % nb(title)
    if text: b += '<p class="tx">%s</p>' % nb(text)
    b += '<div class="cards">'
    for item in people:
        if len(item) == 3:
            n, r, ph = item
            b += '<div class="card pcard"><img class="ph" src="%s"><div><div class="nm">%s</div><div class="rl">%s</div></div></div>' % (photo_uri(ph), nb(n), nb(r))
        else:
            n, r = item
            b += '<div class="card"><div class="nm">%s</div><div class="rl">%s</div></div>' % (nb(n), nb(r))
    return b + '</div></div>'

def cta(title, text, btn='Оставить заявку', size='l'):
    return '<div class="body"><h1 class="%s">%s</h1><p class="tx">%s</p><span class="btn">%s</span></div>' % (size, nb(title), nb(text), nb(btn))

def quotes(title, qs, tsize='m'):
    b = '<div class="body">'
    if title: b += '<h1 class="%s">%s</h1>' % (tsize, nb(title))
    b += '<div class="quotes">'
    for q in qs:
        b += '<div class="q">%s</div>' % nb(q)
    return b + '</div></div>'

def bigquote(text, who=None):
    return '<div class="body"><div class="q plain"><span class="m">«</span>%s<span class="m">»</span>%s</div></div>' % (nb(text), '<span class="who">%s</span>' % nb(who) if who else '')

HL_VARIANTS = {1: ('#151A18', '#FFFFFF'), 2: ('#D0E865', '#12150A'), 3: ('#F4F6F5', '#12150A'), 4: ('#151A18', '#D0E865'), 5: ('#D0E865', '#12150A')}

def hlcover(word, idx=1):
    sc = scale('story')
    bg, fg = HL_VARIANTS.get(idx, HL_VARIANTS[1])
    ov = '<style>.hlcover{background:%s}.hlcover .w{color:%s}</style>' % (bg, fg)
    return '<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>%s</style>%s</head><body><div class="hlcover"><div class="w">%s</div></div></body></html>' % (CSS % sc, ov, nb(word))

# ---------- контент ----------
slides = []  # (name, fmt, html)

# Логотип: в сторис знак и synapt.tech только на последнем кадре серии,
# в постах-каруселях только пост 1 несёт знак, посты 2 и 3 без подписи, обложки без знака
def P(name, kick, inner, i, n, net=False, cls='', logo=False):
    slides.append((name, 'post', page('post', inner, '%d / %d' % (i, n), kick, net, cls, logo=logo, site=logo)))

def S(name, kick, inner, net=False, cls='', logo=False):
    # Сторис без знака и подписи: человек уже в нашем профиле
    slides.append((name, 'story', page('story', inner, None, kick, net, cls, logo=False, site=False)))

# ПОСТ 1 – кто мы: миссия и команда (главная synapt.tech: hero, 04 Почему мы, Почему сейчас, 07 Консультация)
N = 7
P('post1-01', 'студия', thesis('Студия AI и IT-разработки для бизнеса', 'Соединяем AI, процессы и людей в устойчивую рабочую систему', 'xl'), 1, N, net=True, logo=True)
P('post1-02', 'почему мы', thesis('Объединяем компанию с AI и ускоряем прогресс', 'Синапс – место, где сигнал переходит от одного нейрона к следующему, и из таких точек собрана любая нейросеть. Для того же работает наша команда: приходим в компанию и соединяем её процессы и людей с новыми технологиями', 'm'), 2, N, logo=True)
P('post1-03', 'миссия', thesis('Мы хотим, чтобы после нас задачи решались быстрее, показатели росли, а люди занимались тем, что двигает их и бизнес вперёд', 'Каждая такая связка помогает эволюционировать не только компании, но и человечеству', 'm'), 3, N, logo=True)
P('post1-04', 'почему сейчас', cards('AI внедряют почти все, вопрос в том, как', [
    ('одни', 'покупают подписки и раздают инструменты сотрудникам. Работа при этом остаётся прежней'),
    ('другие', 'перестраивают сам процесс: кто принимает заявку, откуда берутся знания, как работа идёт дальше'),
], on_last=True, tsize='m'), 4, N, logo=True)
TEAM_PH = '/private/tmp/claude-501/-Users-xeniaparfenova-A-AAM/b8920e5c-bebf-49bd-9213-58265736edd5/scratchpad/team'
P('post1-05', 'команда', team('Кто ведёт проект', [
    ('Виктор Калугин', 'технический партнёр, архитектура системы', TEAM_PH + '/витя.jpg'),
    ('Антон Орешкин', 'стратегический партнёр, продукт и развитие', TEAM_PH + '/антон.jpg'),
    ('Никита', 'project manager студии', TEAM_PH + '/никита.jpg'),
]), 5, N, logo=True)
P('post1-06', 'в цифрах', metrics(None, [
    ('19 900 ₽', 'чекап бизнеса за две недели'),
    ('3-5 недель', 'до готового продукта'),
    ('60 дней', 'на связи после завершения'),
], size='sm'), 6, N, logo=True)
P('post1-07', 'следующий шаг', cta('30 минут в Zoom с партнёрами студии', 'Вы рассказываете про бизнес, мы задаём вопросы и совместно определяем цели. После присылаем запись разговора и разбор: что увидели и с чего рекомендуем начать'), 7, N, net=True, logo=True)

# ПОСТ 2 – услуги: три шага и модули системы (главная synapt.tech, 01 Услуги; цена десанта с synapt.tech/desant)
P('post2-01', 'услуги', thesis('Сначала формируем карту процессов бизнеса, затем строим систему под неё', 'На старте изучаем, где компания теряет деньги и где их недополучает, а потом собираем под это AI-систему', 'l'), 1, N, net=True, cls='fr-lime')
P('post2-02', 'шаг 1 из 3', metrics('AI-чекап бизнеса', [
    ('19 900 ₽', 'две недели, сумма фиксированная'),
    ('14 дней', 'от Zoom до карты процессов и первого агента'),
], text='Две недели, после которых отдаём карту всех процессов компании с узкими местами, приоритеты по эффекту и план внедрения с вилкой бюджета', size='sm', tsize='l'), 2, N)
P('post2-03', 'шаг 2 из 3', metrics('AI-десант и обучение команды', [
    ('30 дней', 'один специалист, полный рабочий месяц'),
    ('от 80 тыс. ₽', 'месяц работы специалиста внутри вашей команды'),
], text='Месяц работы внутри компании: специалист студии встраивает нейросети в повседневные задачи каждого отдела, а курс даёт команде знания и кураторскую поддержку', size='sm', tsize='l'), 3, N)
P('post2-04', 'шаг 3 из 3', metrics('AI-система, усиливающая и ускоряющая бизнес', [
    ('3-5 недель', 'до готового продукта'),
    ('60 дней', 'на связи после завершения'),
], text='Система разрабатывается из блоков. Какие именно нужны вам, показывают AI-чекап и AI-десант. Они дают карту процессов и показывают, где команда теряет время', size='sm', tsize='l'), 4, N)
P('post2-05', 'модули системы', lst('Система разрабатывается из блоков', [
    ('продажи', 'Работа с клиентом'),
    ('управление', 'AI-дашборд для собственника'),
    ('команда', 'Знания и адаптация'),
    ('экспертиза', 'AI-эксперт'),
    ('операции', 'Интеграции и автоматизация'),
    ('основа всех блоков', 'Безопасный слой'),
], numbered=False, wide='wide2'), 5, N)
P('post2-06', 'не нашли свою задачу', thesis('Список блоков – частые запросы, не весь возможный набор', 'Если процесс повторяется и по нему есть данные, соберём под него решение. Если задача больше отдельного блока: SaaS, мобильное приложение, внутренняя система. Вместе сформируем техническое задание и возьмём работу целиком: интерфейс, backend, инфраструктуру и запуск', 'l'), 6, N)
P('post2-07', 'следующий шаг', cta('30 минут в Zoom с партнёрами студии', 'Вы рассказываете про бизнес, мы задаём вопросы и совместно определяем цели. После присылаем запись разговора и разбор: что увидели и с чего рекомендуем начать'), 7, N, net=True)

# ПОСТ 3 – как работаем: шесть принципов и этапы (главная synapt.tech, 05 Подход и 03 Как работаем)
PRINC = [
    ('Сначала проводим анализ, только потом определяем стоимость и критерии', 'Первый Zoom – погружение в запрос и контекст. Затем внутренний анализ, форматы сотрудничества на выбор и чёткие критерии приёмки в договоре'),
    ('Работаем быстро и итеративно', 'Первый результат отдаём команде через 3-5 недель. Каждую неделю показываем прогресс и дорабатываем по обратной связи'),
    ('Система остаётся у вас целиком', 'Передаём вам всю систему: код, доступы, промпты, базу знаний и документацию. Продолжить работу можно с нами или с другой командой'),
    ('Данные не покидают ваш контур', 'Фиксируем, какие поля уходят в модель. Обезличивание, ролевой доступ и логирование настраиваем мы, ваш юрист получает описание контура'),
    ('60 дней на связи после сдачи', 'В первые недели обкатываем систему на работе, и если что-то идёт не так, правим. Заодно быстро донастраиваем под нагрузку и новые сценарии, которые появляются по ходу'),
    ('Берёмся только за то, что умеем', 'AI-агенты, интеграции, веб и мобильная разработка для бизнеса. Игровые проекты, встроенное ПО и задачи, где нужна команда из тридцати человек, отдаём коллегам и говорим об этом сразу. Если задача решается на уровне процесса и AI не нужен – тоже скажем'),
]
P('post3-01', 'подход', thesis('Шесть принципов, по которым работаем над каждым проектом', 'Смету и критерии приёмки фиксируем в договоре до начала работ, дальше показываем результат каждую неделю', 'l'), 1, N, net=True, cls='fr-milk')
P('post3-02', 'принципы 1 и 2 из 6', plist(PRINC, 0), 2, N)
P('post3-03', 'принципы 3 и 4 из 6', plist(PRINC, 2), 3, N)
P('post3-04', 'принципы 5 и 6 из 6', plist(PRINC, 4), 4, N)
P('post3-05', 'как работаем', lst('Декомпозируем проект на этапы и каждый завершаем конкретным результатом', [
    ('Разбор и план внедрения', 'Карта конкретного процесса и смета'),
    ('Разработка решения', 'Работающий продукт'),
    ('Внедрение и обучение', 'Обученная команда и регламент'),
    ('Передача и поддержка', 'Всё, что нужно для работы'),
]), 5, N)
P('post3-06', 'о сроках', thesis('Длительность этапов у проектов разная: на разбор одного хватит недели, а на другой может потребоваться три', 'Точные сроки и стоимость фиксируем в спецификации после встречи', 'm'), 6, N)
P('post3-07', 'следующий шаг', cta('30 минут в Zoom с партнёрами студии', 'Вы рассказываете про бизнес, мы задаём вопросы и совместно определяем цели. После присылаем запись разговора и разбор: что увидели и с чего рекомендуем начать'), 7, N, net=True)

# СТОРИС – хайлайт 1 «о студии»
S('story-01-studio-1', 'студия', thesis('Студия AI и IT-разработки для бизнеса', 'Соединяем AI, процессы и людей в устойчивую рабочую систему', 'xl', center=True), net=True)
S('story-01-studio-2', 'почему мы', thesis('Объединяем компанию с AI и ускоряем прогресс', 'Синапс – место, где сигнал переходит от одного нейрона к следующему, и из таких точек собрана любая нейросеть. Для того же работает наша команда: приходим в компанию и соединяем её процессы и людей с новыми технологиями', 'm'), net=True)
S('story-01-studio-3', 'миссия', thesis('Мы хотим, чтобы после нас задачи решались быстрее, показатели росли, а люди занимались тем, что двигает их и бизнес вперёд', 'Каждая такая связка помогает эволюционировать не только компании, но и человечеству', 'm'))
S('story-01-studio-4', 'команда', team('Кто ведёт проект', [
    ('Виктор Калугин', 'технический партнёр, архитектура системы'),
    ('Антон Орешкин', 'стратегический партнёр, продукт и развитие'),
    ('Никита', 'project manager студии'),
]), cls='graphite')
S('story-01-studio-5', 'следующий шаг', cta('30 минут в Zoom с партнёрами студии', 'Вы рассказываете про бизнес, мы задаём вопросы и совместно определяем цели. После присылаем запись разговора и разбор: что увидели и с чего рекомендуем начать'), net=True, logo=True)

# СТОРИС – хайлайт 2 «три шага»
S('story-02-steps-1', 'как устроено', lst('Сначала формируем карту процессов бизнеса, затем строим систему под неё', [
    ('AI-чекап бизнеса', 'две недели, сумма фиксированная'),
    ('AI-десант и обучение команды', 'месяц работы внутри компании'),
    ('AI-система', 'разрабатывается из блоков'),
]))
S('story-02-steps-2', 'шаг 1 из 3', metrics('AI-чекап бизнеса', [
    ('19 900 ₽', 'чекап целиком, сумма фиксированная'),
    ('14 дней', 'от Zoom до карты процессов и первого агента'),
], text='Две недели, после которых отдаём карту всех процессов компании с узкими местами, приоритеты по эффекту и план внедрения с вилкой бюджета', size='mid', tsize='l'))
S('story-02-steps-3', 'шаг 2 из 3', metrics('AI-десант и обучение команды', [
    ('30 дней', 'один специалист, полный рабочий месяц'),
    ('от 80 тыс. ₽', 'месяц работы специалиста внутри вашей команды'),
], text='Месяц работы внутри компании: специалист студии встраивает нейросети в повседневные задачи каждого отдела', size='mid', tsize='l'))
S('story-02-steps-4', 'шаг 3 из 3', metrics('AI-система, усиливающая и ускоряющая бизнес', [
    ('3-5 недель', 'до готового продукта'),
    ('60 дней', 'на связи после завершения'),
], text='Система разрабатывается из блоков. Какие именно нужны вам, показывают AI-чекап и AI-десант', size='mid', tsize='l'))
S('story-02-steps-5', 'следующий шаг', cta('Можно начать с небольшого решения?', 'Да, чекап за две недели или компактное решение под один процесс. Дальше добавляем модули по тому, что показала работа первого'), net=True, logo=True)

# СТОРИС – хайлайт 3 «кейсы»
S('story-03-cases-1', 'кейс, AI-десант', metrics('Поиск фабрики занимает 2 минуты, раньше уходило 10', [
    ('26 из 27', 'сотрудников офиса работают с AI'),
    ('25-35 ч', 'рутины в неделю освободилось'),
], kick_chip='INNORTO, оптовые закупки', size='mid', tsize='l'))
S('story-03-cases-2', 'кейс, AI-агент на базе знаний', metrics('Разбор бизнеса клиники приходит в чат за минуты', [
    ('1 500+', 'пар вопрос-ответ в базе знаний клуба'),
    ('24/7', 'ответ участнику клуба в любое время'),
], kick_chip='GlobalDent, клуб стоматологов', size='mid', tsize='l'))
S('story-03-cases-3', 'кейс, отдел продаж', cards('Руководитель впервые видит все диалоги и причины потерь', [
    ('до', 'Из 300 разговоров руководитель слушал 5'),
    ('после', '100% звонков и переписок в разборе, конверсия в сделку выросла на 20%'),
], on_last=True, tsize='m'))
S('story-03-cases-4', 'кейс, AI-агент в подборе', metrics('Бот подбирает блюда только из того, что сейчас есть на складе', [
    ('1 200+', 'карт меню поставщиков оцифровано'),
    ('30 тысяч', 'сообщений обрабатывает ежемесячно'),
], kick_chip='FoodTech-сервис, имя под NDA', size='mid', tsize='l'))
S('story-03-cases-5', 'кейс, разработка', metrics('30 лет расчётов переехали в браузер без расхождений', [
    ('100%', 'совпадение расчётов со старой системой'),
    ('30+ лет', 'накопленной логики сохранено'),
], kick_chip='Инженерное бюро, имя под NDA', size='mid', tsize='l'), logo=True)

# СТОРИС – хайлайт 4 «система» (главная synapt.tech: hero, 03 Как работаем, 05 Подход)
S('story-04-system-1', 'система', metrics('Соединяем AI, процессы и людей в устойчивую рабочую систему', [
    ('3-5 недель', 'до готового продукта'),
    ('60 дней', 'на связи после завершения'),
], size='mid', tsize='l'), net=True)
S('story-04-system-2', 'как работаем', lst('Декомпозируем проект на этапы и каждый завершаем конкретным результатом', [
    ('Разбор и план внедрения', 'Карта конкретного процесса и смета'),
    ('Разработка решения', 'Работающий продукт'),
    ('Внедрение и обучение', 'Обученная команда и регламент'),
    ('Передача и поддержка', 'Всё, что нужно для работы'),
]))
S('story-04-system-3', 'подход', lst('Шесть принципов, по которым работаем над каждым проектом', [
    ('Сначала проводим анализ, только потом определяем стоимость и критерии',),
    ('Работаем быстро и итеративно',),
    ('Система остаётся у вас целиком',),
    ('Данные не покидают ваш контур',),
    ('60 дней на связи после сдачи',),
    ('Берёмся только за то, что умеем',),
]))
S('story-04-system-4', 'передача', thesis('Система остаётся у вас целиком', 'Передаём вам всю систему: код, доступы, промпты, базу знаний и документацию. Продолжить работу можно с нами или с другой командой', 'l'), cls='graphite')
S('story-04-system-5', 'безопасность', thesis('Данные не покидают ваш контур', 'Фиксируем, какие поля уходят в модель. Обезличивание, ролевой доступ и логирование настраиваем мы, ваш юрист получает описание контура', 'l'), net=True, logo=True)

# СТОРИС – хайлайт 5 «вопросы» (FAQ главной synapt.tech и synapt.tech/checkup, дословно)
S('story-05-faq-1', 'частый вопрос', thesis('С чего начинается проект?', 'С короткой встречи на 30 минут. Разбираем задачу, текущие процессы, данные и то, какого результата вы ждёте. На ней же обсуждаем решение, и после отправляем план работ', 'l'))
S('story-05-faq-2', 'частый вопрос', thesis('Что будет с командой после интеграции AI?', 'До старта вместе с вами разбираем роли: что забирает агент, что остаётся за человеком и как меняется его рабочий день. Сокращения мы не предлагаем и не планируем, это решение собственника. Наша задача – снять с людей повторяющуюся рутину, а не отнять у них работу', 'm'))
S('story-05-faq-3', 'частый вопрос', thesis('Мы уже внедряли, эффекта не было?', 'Так бывает, когда инструмент дают людям без разбора процесса: инструкция есть, привычки нет. Мы начинаем с процессов и задач конкретных людей, а инструмент подбираем под них', 'l'))
S('story-05-faq-4', 'частый вопрос', thesis('Что происходит после запуска?', '60 дней поддержки: остаёмся на связи и обкатываем систему на реальных процессах, донастраиваем под то, как работает команда. Дальше продлеваем договор или полностью передаём систему вашей команде. Код, документация и методология в любом случае остаются у вас', 'm'))
S('story-05-faq-5', 'следующий шаг', cta('30 минут в Zoom с партнёрами студии', 'Вы рассказываете про бизнес, мы задаём вопросы и совместно определяем цели. После присылаем запись разговора и разбор: что увидели и с чего рекомендуем начать'), net=True, logo=True)

# ОБЛОЖКИ хайлайтов
for i, w in enumerate(['о студии', 'три шага', 'кейсы', 'система', 'вопросы'], 1):
    slides.append(('cover-%02d' % i, 'story', hlcover(w, i)))

manifest = []
for name, fmt, h in slides:
    p = os.path.join(OUT_HTML, name + '.html')
    open(p, 'w', encoding='utf-8').write(h)
    sc = scale(fmt)
    manifest.append(dict(html=p, png=os.path.join(OUT_PNG, name + '.png'), svg=os.path.join(OUT_PNG, 'svg', name + '.svg'), w=sc['w'], h=sc['h']))
json.dump(manifest, open(os.path.join(ROOT, 'manifest.json'), 'w'))
print(len(manifest), 'slides')
