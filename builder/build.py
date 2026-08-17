# -*- coding: utf-8 -*-
# Генератор клиентских материалов Synapt (КП и кейсы) из единой дизайн-системы.
# Каждый материал -> отдельная папка out/<slug>/index.html (self-contained, две темы, кнопка Скачать PDF в шапке).
import os, re, sys, json, html, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "out")

# фото менеджера в блоке заявки
AVA = "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"

LOGO = '<svg viewBox="0 0 839 360" fill="currentColor"><g transform="translate(-30,0)"><path d="M416.193 232.251C403.922 232.402 389.832 229.229 379.378 222.582L386.65 207.775C392.71 211.099 404.225 215.178 416.193 215.481C426.344 215.632 437.403 212.912 439.524 204.301C440.585 199.013 438.312 194.48 433.767 192.063C425.435 187.379 414.527 185.869 405.134 183.149C390.438 178.768 378.166 170.609 379.378 153.386C380.893 130.27 402.255 124.529 421.95 124.68C433.161 124.831 443.615 126.796 453.917 130.875L447.857 146.738C439.827 143.717 429.828 141.753 420.89 141.753C412.557 141.602 399.074 142.961 398.316 154.141C398.013 161.847 404.225 164.717 410.285 166.681C422.556 170.156 434.07 171.063 445.281 177.559C456.341 184.056 460.583 194.934 457.856 207.322C453.766 226.661 433.313 232.1 416.193 232.251Z"/><path d="M476.072 257.33L475.617 242.071C484.556 242.675 490.767 241.618 494.555 232.402L496.221 228.02L460.316 151.573H480.314L505.312 206.567L527.431 151.573H547.126L511.372 237.388C504.706 253.402 492.282 258.539 476.072 257.33Z"/><path d="M552.394 231.344V151.573H566.484L568.453 157.616C577.24 153.537 586.936 151.271 595.724 151.422C612.843 151.573 627.236 160.487 627.236 183.602V231.344H609.359V183.602C609.359 171.365 602.693 166.983 593.754 166.832C585.573 166.681 576.028 169.854 570.12 174.689V231.344H552.394Z"/><path d="M699.051 210.495V171.516C694.354 166.681 685.113 164.566 677.992 164.868C665.721 165.17 655.57 173.48 655.57 190.854C655.57 208.531 665.721 216.689 677.992 217.143C685.113 217.294 694.354 215.027 699.051 210.495ZM637.844 190.854C637.844 166.681 654.51 150.062 678.447 150.062C685.719 150.062 694.203 151.724 700.566 155.803L702.081 150.666H716.777V231.344H702.081L700.566 226.056C694.203 230.287 685.719 231.949 678.447 231.949C654.51 231.949 637.844 215.178 637.844 190.854Z"/><path d="M767.811 216.689C782.81 216.689 791.143 206.114 791.143 191.459C791.143 174.537 781.901 166.983 770.387 166.379C762.812 165.926 754.025 167.588 748.116 173.631V210.797C752.51 215.027 760.539 216.689 767.811 216.689ZM730.39 257.33V151.573H744.329L746.45 156.861C753.873 152.933 761.297 150.818 769.932 150.818C794.173 150.818 809.02 167.286 809.02 191.459C809.02 215.783 791.597 232.1 767.811 232.1C760.994 232.1 754.328 230.589 748.116 227.567V257.33H730.39Z"/><path d="M852.032 232.251C837.942 232.402 825.519 223.941 825.519 205.358V165.624H812.793V151.573H825.519V138.731L843.396 133.745V151.573H860.819V165.624H843.396V205.358C843.396 214.423 847.941 216.84 853.85 216.991C857.183 217.143 860.97 216.538 864.607 215.33L869 229.229C863.243 231.344 857.637 232.251 852.032 232.251Z"/></g><path d="M159.195 0C171.173 0 181.31 7.88936 184.654 18.7451C184.861 19.4161 184.908 20.1234 184.851 20.8231C184.713 22.5205 184.642 24.2362 184.642 25.9672C184.642 28.5667 184.802 31.1306 185.112 33.6486C187.506 53.1417 198.885 69.8519 214.978 79.5476C215.737 80.0051 216.509 80.4455 217.289 80.8709C224.71 85.592 229.619 93.8647 229.619 103.279C229.619 111.25 226.1 118.397 220.517 123.269C220.133 123.604 219.697 123.871 219.237 124.09C216.415 125.431 213.707 126.973 211.137 128.703C197.248 138.051 187.307 152.808 184.361 169.958C183.768 173.416 183.459 176.969 183.459 180.59C183.459 183.918 183.72 187.188 184.223 190.38C186.834 206.945 195.96 221.343 208.889 230.892C212.572 233.613 216.567 235.941 220.808 237.814C228.573 241.244 237.163 243.148 246.19 243.148C255.217 243.148 263.807 241.244 271.571 237.814C275.309 236.163 278.854 234.158 282.164 231.844C282.713 231.46 283.316 231.153 283.966 230.988C286.076 230.451 288.29 230.164 290.575 230.164C305.283 230.164 317.206 242.054 317.206 256.721C317.206 271.389 305.283 283.279 290.575 283.279C289.033 283.279 287.524 283.148 286.058 282.898C285.232 282.758 284.465 282.394 283.783 281.908C279.702 279.002 275.256 276.569 270.525 274.695C263.358 271.855 255.544 270.295 247.373 270.295C237.26 270.295 227.695 272.684 219.226 276.931C216.488 278.304 213.866 279.87 211.377 281.612C196.983 291.686 187.018 307.649 185.013 326.007C184.768 328.256 184.642 330.541 184.642 332.852C184.642 334.869 184.739 336.864 184.927 338.833C184.993 339.532 184.956 340.239 184.758 340.913C181.523 351.944 171.299 360 159.195 360C144.487 360 132.564 348.11 132.564 333.443C132.564 326.274 135.408 319.772 140.041 314.99C140.506 314.511 141.068 314.141 141.672 313.855C145.364 312.109 148.859 310.015 152.111 307.614C165.04 298.064 174.165 283.666 176.777 267.101C177.28 263.91 177.541 260.64 177.541 257.311C177.541 253.69 177.232 250.137 176.638 246.679C173.508 228.455 162.48 212.934 147.205 203.731C146.398 203.245 145.579 202.777 144.75 202.327C135.849 197.497 125.645 194.754 114.81 194.754C105.616 194.754 96.8757 196.73 88.9992 200.28C85.7632 201.739 82.6721 203.462 79.7569 205.424C65.0769 215.305 54.8087 231.228 52.5479 249.63C52.2386 252.148 52.0786 252.942 52.0786 255.541C52.0786 257.632 52.9736 261.276 52.3826 263.512C49.3746 274.891 38.9818 283.279 26.6311 283.279C11.9232 283.279 0 271.389 0 256.721C0 249.645 2.77124 243.219 7.29812 238.456C10.0606 235.549 17.1676 233.615 21.4887 230.322C34.7668 220.202 43.882 204.903 45.7895 187.436C46.0352 185.186 46.1606 182.902 46.1606 180.59C46.1606 178.573 46.063 176.578 45.875 174.609C45.8083 173.91 45.8458 173.202 46.0434 172.529C49.279 161.498 59.5045 153.443 71.6081 153.443C73.1495 153.443 74.6579 153.573 76.1233 153.822C76.9496 153.962 77.7164 154.327 78.3985 154.812C82.4801 157.719 86.9264 160.152 91.6577 162.027C98.8255 164.866 106.639 166.426 114.81 166.426C123.836 166.426 132.427 164.523 140.191 161.093C144.433 159.219 148.427 156.892 152.111 154.171C165.8 144.06 175.226 128.512 177.17 110.715C177.415 108.465 177.541 106.18 177.541 103.869C177.541 101.269 177.381 98.7055 177.071 96.1875C174.677 76.6944 163.298 59.9841 147.205 50.2884C146.447 49.8315 145.675 49.3903 144.894 48.964C137.473 44.2427 132.564 35.9708 132.564 26.5574C132.564 11.8901 144.487 0 159.195 0ZM26.6311 76.7213C41.3391 76.7213 53.2622 88.6115 53.2622 103.279C53.2622 117.946 41.3391 129.836 26.6311 129.836C11.9231 129.836 0 117.946 0 103.279C0 88.6115 11.9231 76.7213 26.6311 76.7213ZM290.575 76.7213C305.283 76.7213 317.206 88.6115 317.206 103.279C317.206 117.946 305.283 129.836 290.575 129.836C275.867 129.836 263.944 117.946 263.944 103.279C263.944 88.6115 275.867 76.7213 290.575 76.7213Z"/></svg>'

TGICON = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M21.9 4.3 18.6 20c-.2 1.1-.9 1.3-1.8.8l-5-3.7-2.4 2.3c-.3.3-.5.5-1 .5l.4-5.1L18 6.6c.4-.3-.1-.5-.6-.2L7.2 13 2.3 11.5c-1.1-.3-1.1-1 .2-1.5l18.1-7c.9-.3 1.7.2 1.3 1.3z"/></svg>'
DLICON = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3v12m0 0l-4-4m4 4l4-4M4 21h16"/></svg>'

CSS = open(os.path.join(BASE, "theme.css"), encoding="utf-8").read()

# ---------- печатный слой ----------
# PDF собирается из того же HTML, что и страница: отдельный <style media="print"> подменяет
# токены на светлую половину theme.css и убирает всё экранное – шапку, форму, холсты, анимации.
# Правка текста в specs.json меняет сразу оба формата, расхождение между сайтом и PDF невозможно.
PRINT_CSS = r'''
@page{size:A4 portrait;margin:15mm 13mm 17mm}

/* палитра фиксируется независимо от темы, выбранной на экране: тот же графит и та же зелень */
:root,:root[data-theme="dark"],:root[data-theme="light"]{
  --bg-deep:#F4F6F5;--bg:#FFFFFF;--surface:#FFFFFF;--surface-2:#F6F8F7;--surface-3:#EDF0EE;
  --text:#161918;--text-2:#333836;--text-muted:#565C59;--text-dim:#6A716E;
  --accent:#D0E865;--accent-glow:#D0E865;--accent-deep:#A6BF41;--accent-light:#EDF7BD;
  --accent-txt:#5F7A18;--sage:#A6BF41;--danger:#C2544D;
  --line:#E1E5E3;--line-2:#D0D5D3;--line-accent:rgba(139,166,44,.45);
  --glow:none;--card-shadow:none;--btn-shadow:none;
  --maxw:none;--gutter:0px;--nav-h:0px;
}
html{overflow:visible;scroll-padding-top:0}
body{background:#FFFFFF;color:var(--text);overflow:visible;
  -webkit-print-color-adjust:exact;print-color-adjust:exact}
.wrap{max-width:none;margin:0;padding:0}
*,*::before,*::after{animation:none!important;transition:none!important;
  box-shadow:none!important;text-shadow:none!important;filter:none!important}
.reveal,.reveal.d1,.reveal.d2,.reveal.d3,.reveal.d4{opacity:1;transform:none}

/* экранная механика в документ не едет: шапка, кнопки, форма заявки, холсты */
.nav,.nav-sheet,.tgl,.nav-burger,.btn,.cover-cta,.leadbox,.mform,.fab,
.mf-err,.mf-ok,.mf-fail,.lf-after,.lc-ava,.tg-after,.mgr-web,
canvas,#synFx,.figbox,.fig-side .figbox{display:none!important}
/* реплика менеджера на полосе не может ссылаться на форму: она осталась на экране */
.mgr-pdf{display:block!important}
.r-cover::before{display:none}

/* обложка становится титульной страницей: логотип сверху, блок с названием по центру полосы */
.pbrand{display:block!important;color:#161918}
.pbrand svg{height:26px;width:auto}
.r-cover{padding:26px 0 0;overflow:visible;min-height:232mm;
  display:flex;flex-direction:column;justify-content:center;
  break-after:page;page-break-after:always}
.cover h1{margin-top:18px;max-width:24ch}
.cover .lead{margin-bottom:0}
.cover-grid{display:block}
.cover-dom{text-align:left;padding-bottom:0;margin-top:34px}
.cd-num{justify-content:flex-start}
.cd-cap{margin-left:0}

/* ритм плотнее: полоса печати короче экранной */
section{padding:26px 0!important}
.sec-head{margin-bottom:22px}
h2{max-width:28ch}

/* графика во всю ширину снята, подпись под ней остаётся текстом */
.bleed{margin-left:0;width:auto;max-width:none}
.fig-side{display:block}
.fig-side .fig-txt,.figcap{max-width:none;margin-top:0}

/* карточки и строки не разрываются между страницами */
.mstep,.vcard,.icol,.case,.upsell,.bento .b,.bn,.rel-card,.crow,.stmt,.dom,
.price-line,.ba .col,.lc-mgr,.fig-side,.metric,.rel-grid,.f-main,
h1,h2,h3,h4,.eyebrow,.sec-head,.rel-head{break-inside:avoid;page-break-inside:avoid}
h1,h2,h3,h4,.eyebrow,.sec-head,.rel-head{break-after:avoid;page-break-after:avoid}

/* доминанта держит раскладку сайта: текст слева, число справа, вынос за сетку снят */
.dom{grid-template-columns:1.15fr .85fr;gap:32px;align-items:end}
.dom-fig{margin-right:0;justify-self:end;text-align:right}
.dom-cap{margin-left:auto}

/* парные блоки остаются парой: на полосе А4 колонки читаются как сравнение, а не как два списка */
.incl,.ba,.vs{grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}
.icol,.ba .col,.vcard{padding:20px}
.vs .vcard:nth-child(2){margin-top:0}
.ba .t{width:66px}

/* смежные материалы держат три колонки: во вторую сетку девять карточек не ложатся ровно */
.rel-grid{grid-template-columns:repeat(3,minmax(0,1fr))}
.rel-card{padding:16px 16px;min-height:0}
.rel-t{font-size:14px}

/* подвал с реквизитами держится одним куском */
footer{margin-top:26px;padding:24px 0 0;break-inside:avoid;page-break-inside:avoid}
.f-bottom{margin-top:20px;padding-top:14px}

/* контакты вместо формы: те же адреса, но текстом и ссылкой */
.pc-sec{display:block!important;padding:0 0 8px!important}
.pcontacts{margin-top:0;padding:20px 22px;border:1px solid var(--line-accent);
  border-radius:16px;background:var(--surface-2);break-inside:avoid;page-break-inside:avoid}
.pc-k{font-family:var(--mono);font-size:10.5px;font-weight:500;letter-spacing:.11em;
  color:var(--sage);margin-bottom:14px;font-feature-settings:"case" 1,"liga" 0}
.pc-row{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 28px}
.pc-i{display:flex;flex-direction:column;gap:4px}
.pc-i span{font-size:12.5px;color:var(--text-dim);line-height:1.4}
.pc-i a{font-family:var(--mono);font-size:13px;color:var(--text-2);line-height:1.45;
  border-bottom:1px solid var(--line-accent);width:fit-content;font-feature-settings:"liga" 0}
'''

SYN_FX = r'''/* ==========================================================
   SYNAPT — графика связей, единая система
   белые и серые узлы, зелёный только на несущих смысл
   обложка: <canvas id="synFx" data-fx="converge|flow|mesh|contour"></canvas>
   в блоках: canvas.fx-matrix .fx-layers .fx-signal .fx-multiples .fx-halftone
   ========================================================== */
(function () {
  var DPR = Math.min(devicePixelRatio || 1, 2);
  var WH = '232,238,236', GR = '128,140,136', PH = '208,232,101';
  function rnd(s) { var x = Math.sin(s * 127.1) * 43758.5453; return x - Math.floor(x); }
  function vis(c) { var r = c.getBoundingClientRect(); return r.bottom > -200 && r.top < innerHeight + 200; }
  function fit(c, ratio) {
    var rt = typeof ratio === 'function' ? ratio() : ratio;
    var r = c.getBoundingClientRect(), W = r.width, H = rt ? W / rt : r.height;
    /* пропорция задаёт высоту, но min-height из стилей может её перебить:
       битмап считаем по фактической рамке, иначе картинка растягивается и мылит */
    if (rt) { c.style.height = H + 'px'; H = c.getBoundingClientRect().height || H; }
    c.width = W * DPR; c.height = H * DPR;
    var ctx = c.getContext('2d'); ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    return [ctx, W, H];
  }
  /* холст пересобирается не только на resize: высота блока меняется от шрифтов,
     раскрытия анимаций и переноса строк, а растянутый битмап мылит картинку */
  function watch(c, build) {
    addEventListener('resize', build);
    if (typeof ResizeObserver === 'undefined') return;
    var ro = new ResizeObserver(function () {
      var r = c.getBoundingClientRect();
      if (!r.width || !r.height) return;
      if (Math.abs(c.width - r.width * DPR) > 1.5 || Math.abs(c.height - r.height * DPR) > 1.5) build();
    });
    ro.observe(c);
  }
  function loop(c, draw, ratio) {
    var st = {};
    function build() { var f = fit(c, ratio); st.ctx = f[0]; st.W = f[1]; st.H = f[2]; if (st.onbuild) st.onbuild(); }
    st.rebuild = build;
    build(); watch(c, build);
    var t = 0;
    var seen = false;
  (function frame() { requestAnimationFrame(frame); if (!vis(c)) { if (seen) t++; return; } seen = true; draw(st, t); t++; })();
    return st;
  }

  /* ---------- обложка: сигналы сходятся в точку, из неё разворачивается сеть ---------- */
  function converge(c) {
    var ctx = c.getContext('2d'), W, H, cx, cy, lines = [], waves = [], t = 0;
    var CYCLE = 1020, P_IN = .46, P_LOCK = .54;
    function build() {
      var r = c.getBoundingClientRect(); W = r.width; H = r.height;
      c.width = W * DPR; c.height = H * DPR; ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
      cx = W < 900 ? W * .5 : W * .74; cy = W < 900 ? H * .32 : H * .48;
      var R = Math.hypot(W, H) * .62, n = W < 700 ? 10 : 16, i;
      lines = [];
      for (i = 0; i < n; i++) {
        var a = (i / n) * 6.283 + rnd(i) * .28, rr = R * (.72 + rnd(i + 9) * .5);
        var bend = (rnd(i + 3) - .5) * rr * .9;
        lines.push({x0: cx + Math.cos(a) * rr, y0: cy + Math.sin(a) * rr * .78,
          mx: cx + Math.cos(a) * rr * .48 - Math.sin(a) * bend,
          my: cy + Math.sin(a) * rr * .37 + Math.cos(a) * bend * .5,
          w: .6 + rnd(i + 5) * 1.5, d: rnd(i + 7) * .3, hot: rnd(i + 21) > .72});
      }
      waves = [];
      for (var ring = 1; ring <= 3; ring++) {
        var cnt = ring * 5 + 1;
        for (var k = 0; k < cnt; k++) {
          var aa = (k / cnt) * 6.283 + ring * .7, r2 = Math.min(W, H) * (.19 * ring + .07) + rnd(ring * 20 + k) * 46;
          waves.push({ring: ring, x: cx + Math.cos(aa) * r2 * (W / Math.min(W, H)) * .8, y: cy + Math.sin(aa) * r2,
            px: ring === 1 ? cx : null, py: ring === 1 ? cy : null, hot: rnd(ring * 40 + k) > .74});
        }
      }
      waves.forEach(function (nd) {
        if (nd.px !== null) return; var b = null, bd = 1e9;
        waves.forEach(function (q) { if (q.ring !== nd.ring - 1) return; var d = Math.hypot(q.x - nd.x, q.y - nd.y); if (d < bd) { bd = d; b = q; } });
        if (b) { nd.px = b.x; nd.py = b.y; }
      });
    }
    build(); watch(c, build);
    function eIn(p) { return p * p; } function eOut(p) { return 1 - Math.pow(1 - p, 3); }
    function qp(x0, y0, mx, my, x1, y1, p) { var k = 1 - p; return [k*k*x0 + 2*k*p*mx + p*p*x1, k*k*y0 + 2*k*p*my + p*p*y1]; }
    (function frame() {
      requestAnimationFrame(frame);
      if (c.getBoundingClientRect().bottom < -100) { t++; return; }
      ctx.clearRect(0, 0, W, H);
      var tt = (t % CYCLE) / CYCLE, fade = tt > .93 ? 1 - (tt - .93) / .07 : (tt < .04 ? tt / .04 : 1), arrived = 0;
      lines.forEach(function (L) {
        var p = Math.max(0, Math.min(1, (tt - L.d * .18) / (P_IN - L.d * .18)));
        if (p >= 1) arrived++; if (p <= 0) return;
        var head = eIn(p), tail = Math.max(0, head - .34), keep = tt < P_IN ? 1 : Math.max(0, 1 - (tt - P_IN) / .3);
        var col = L.hot ? PH : GR;
        for (var s = 0; s < 34; s++) {
          var A = qp(L.x0, L.y0, L.mx, L.my, cx, cy, tail + (head - tail) * (s / 34));
          var B = qp(L.x0, L.y0, L.mx, L.my, cx, cy, tail + (head - tail) * ((s + 1) / 34));
          var g = s / 34;
          ctx.beginPath(); ctx.moveTo(A[0], A[1]); ctx.lineTo(B[0], B[1]);
          ctx.strokeStyle = 'rgba(' + col + ',' + (.04 + g * .26) * fade * keep + ')';
          ctx.lineWidth = L.w * (.3 + g * .9) * (.4 + head * .8); ctx.lineCap = 'round'; ctx.stroke();
        }
        if (p < 1) {
          var Hd = qp(L.x0, L.y0, L.mx, L.my, cx, cy, head), hc = L.hot ? PH : WH;
          var gr = ctx.createRadialGradient(Hd[0], Hd[1], 0, Hd[0], Hd[1], 14);
          gr.addColorStop(0, 'rgba(' + hc + ',' + .42 * fade + ')'); gr.addColorStop(1, 'rgba(' + hc + ',0)');
          ctx.fillStyle = gr; ctx.beginPath(); ctx.arc(Hd[0], Hd[1], 14, 0, 7); ctx.fill();
          ctx.beginPath(); ctx.arc(Hd[0], Hd[1], 1.6, 0, 7); ctx.fillStyle = 'rgba(' + hc + ',' + .88 * fade + ')'; ctx.fill();
        }
      });
      var fl = arrived / lines.length;
      if (fl > 0) {
        var flash = tt >= P_IN && tt < P_LOCK + .1 ? 1 - Math.min(1, (tt - P_IN) / (P_LOCK + .1 - P_IN)) : 0;
        var rad = 4 + fl * 5 + flash * 26;
        var g2 = ctx.createRadialGradient(cx, cy, 0, cx, cy, rad * 4.2);
        g2.addColorStop(0, 'rgba(' + PH + ',' + (.26 * fl + .46 * flash) * fade + ')');
        g2.addColorStop(.4, 'rgba(' + PH + ',' + (.07 * fl + .14 * flash) * fade + ')');
        g2.addColorStop(1, 'rgba(' + PH + ',0)');
        ctx.fillStyle = g2; ctx.beginPath(); ctx.arc(cx, cy, rad * 4.2, 0, 7); ctx.fill();
        ctx.beginPath(); ctx.arc(cx, cy, 2.6 + fl * 1.8, 0, 7); ctx.fillStyle = 'rgba(' + PH + ',' + (.55 + .45 * fl) * fade + ')'; ctx.fill();
        if (flash > 0) { ctx.beginPath(); ctx.arc(cx, cy, (1 - flash) * Math.min(W, H) * .62, 0, 7);
          ctx.strokeStyle = 'rgba(' + PH + ',' + flash * .26 * fade + ')'; ctx.lineWidth = 1.2; ctx.stroke(); }
      }
      if (tt > P_LOCK) {
        var sp = Math.min(1, (tt - P_LOCK) / (.9 - P_LOCK));
        waves.forEach(function (nd) {
          var lo = Math.max(0, Math.min(1, (sp - (nd.ring - 1) * .22) / .5)); if (lo <= 0) return;
          var e = eOut(lo), x = nd.px + (nd.x - nd.px) * e, y = nd.py + (nd.y - nd.py) * e;
          ctx.beginPath(); ctx.moveTo(nd.px, nd.py); ctx.lineTo(x, y);
          ctx.strokeStyle = 'rgba(' + GR + ',' + .34 * lo * fade + ')'; ctx.lineWidth = 1.2 - nd.ring * .18; ctx.stroke();
          var nc = nd.hot ? PH : WH;
          ctx.beginPath(); ctx.arc(x, y, 2.5 - nd.ring * .45, 0, 7);
          ctx.fillStyle = 'rgba(' + nc + ',' + (nd.hot ? .85 : .6) * lo * fade + ')'; ctx.fill();
        });
      }
      t++;
    })();
  }

  /* ---------- обложка: поток по руслу, врозь и собирается ---------- */
  function flow(c) {
    /* поток заявок: у каждой частицы остаётся след, иначе на кадре видно только точки */
    var ctx = c.getContext('2d'), W, H, ps = [], t = 0, TAIL = 34;
    function seed(p, i, first) {
      p.tr = [];
      p.x = first ? rnd(i) * W : -14 - rnd(i + t * .01) * 40;
      p.y = (first ? rnd(i + 100) : Math.random()) * H;
      p.sp = .5 + rnd(i + 7) * 1.2; p.life = first ? rnd(i + 3) * 200 : 0;
      p.hot = rnd(i + 55) > .84;
    }
    function build() {
      var r = c.getBoundingClientRect(); W = r.width; H = r.height;
      c.width = W * DPR; c.height = H * DPR; ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
      ps = []; var n = W < 700 ? 120 : 320;
      for (var i = 0; i < n; i++) { var p = {i: i}; seed(p, i, true); ps.push(p); }
    }
    build(); watch(c, build);
    function ang(x, y) { return Math.sin(x * .0055 + y * .0035) * .5 + (H * .52 - y) / H * 1.55; }
    (function frame() {
      requestAnimationFrame(frame);
      if (c.getBoundingClientRect().bottom < -100) { t++; return; }
      ctx.clearRect(0, 0, W, H);
      ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      ps.forEach(function (p) {
        var a = ang(p.x, p.y);
        p.x += Math.cos(a) * p.sp * 1.7; p.y += Math.sin(a) * p.sp; p.life++;
        p.tr.push(p.x, p.y);
        if (p.tr.length > TAIL * 2) p.tr.splice(0, 2);
        var mid = 1 - Math.min(1, Math.abs(p.y - H * .52) / (H * .44));
        var base = p.hot ? PH : GR, k = p.tr.length / 2;
        for (var s = 1; s < k; s++) {
          var g = s / k;
          ctx.beginPath();
          ctx.moveTo(p.tr[(s - 1) * 2], p.tr[(s - 1) * 2 + 1]);
          ctx.lineTo(p.tr[s * 2], p.tr[s * 2 + 1]);
          ctx.strokeStyle = 'rgba(' + base + ',' + (p.hot ? .16 + mid * .46 : .09 + mid * .28) * g + ')';
          ctx.lineWidth = (.7 + mid * 1.3) * (.4 + g * .85);
          ctx.stroke();
        }
        if (p.hot) {
          ctx.beginPath(); ctx.arc(p.x, p.y, 1.5, 0, 7);
          ctx.fillStyle = 'rgba(' + PH + ',' + (.3 + mid * .5) + ')'; ctx.fill();
        }
        if (p.x > W + 14 || p.life > 320) seed(p, p.i, false);
      });
      t++;
    })();
  }

  /* ---------- обложка: сетка узлов с волной возбуждения ---------- */
  function meshCover(c) {
    var ctx = c.getContext('2d'), W, H, nodes = [], links = [], t = 0;
    function build() {
      var r = c.getBoundingClientRect(); W = r.width; H = r.height;
      c.width = W * DPR; c.height = H * DPR; ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
      var step = W < 700 ? 40 : 52; nodes = []; links = [];
      var cols = Math.ceil(W / step) + 1, rows = Math.ceil(H / step) + 1;
      for (var j = 0; j < rows; j++) for (var i = 0; i < cols; i++) {
        var k = j * cols + i;
        nodes.push({x: i * step + (rnd(k) - .5) * step * .6, y: j * step + (rnd(k + 77) - .5) * step * .6,
          i: i, j: j, hot: rnd(k + 300) > .9, ph: rnd(k + 5) * 6.28});
      }
      nodes.forEach(function (a) { nodes.forEach(function (b) {
        if (b.j < a.j || (b.j === a.j && b.i <= a.i)) return;
        if (Math.abs(a.i - b.i) > 1 || Math.abs(a.j - b.j) > 1) return;
        if (rnd(a.i * 13 + a.j * 29 + b.i * 7 + b.j * 3) > .58) return;
        links.push([a, b]);
      }); });
    }
    build(); watch(c, build);
    (function frame() {
      requestAnimationFrame(frame);
      if (c.getBoundingClientRect().bottom < -100) { t++; return; }
      ctx.clearRect(0, 0, W, H);
      var tt = t * .012, front = ((t * 1.7) % (W + 460)) - 230;
      links.forEach(function (L) {
        var mx = (L[0].x + L[1].x) / 2, near = Math.max(0, 1 - Math.abs(mx - front) / 200);
        ctx.beginPath(); ctx.moveTo(L[0].x, L[0].y); ctx.lineTo(L[1].x, L[1].y);
        ctx.strokeStyle = near > .38 ? 'rgba(' + PH + ',' + (.07 + near * .28) + ')' : 'rgba(' + GR + ',' + (.07 + near * .1) + ')';
        ctx.lineWidth = .7 + near * .9; ctx.stroke();
      });
      nodes.forEach(function (n) {
        var near = Math.max(0, 1 - Math.abs(n.x - front) / 180), br = .55 + .45 * Math.sin(tt + n.ph);
        ctx.beginPath(); ctx.arc(n.x, n.y, 1.5 + near * 2 + (n.hot ? .8 : 0), 0, 7);
        ctx.fillStyle = (n.hot || near > .62) ? 'rgba(' + PH + ',' + ((n.hot ? .75 : .3) * br + near * .4) + ')'
                                              : 'rgba(' + WH + ',' + (.16 + near * .32) * br + ')';
        ctx.fill();
      });
      t++;
    })();
  }

  /* ---------- обложка: изолинии рельефа ---------- */
  function contour(c) {
    var ctx = c.getContext('2d'), W, H, t = 0;
    function build() { var r = c.getBoundingClientRect(); W = r.width; H = r.height;
      c.width = W * DPR; c.height = H * DPR; ctx.setTransform(DPR, 0, 0, DPR, 0, 0); }
    build(); watch(c, build);
    function field(x, y, tt) {
      return Math.sin(x * .0085 + tt) * Math.cos(y * .012 - tt * .6)
           + Math.sin((x + y) * .0055 + tt * .45) * .85
           + Math.cos(Math.hypot(x - W * .72, (y - H * .45) * 1.4) * .0095 - tt * .8) * 1.05;
    }
    (function frame() {
      requestAnimationFrame(frame);
      if (c.getBoundingClientRect().bottom < -100) { t++; return; }
      ctx.clearRect(0, 0, W, H);
      var tt = t * .0032, st = 12;
      var nx = Math.ceil(W / st) + 1, ny = Math.ceil(H / st) + 1, g = new Float32Array(nx * ny), i, j;
      for (j = 0; j < ny; j++) for (i = 0; i < nx; i++) g[j * nx + i] = field(i * st, j * st, tt);
      for (var lv = -2.4; lv <= 2.4; lv += .3) {
        var key = Math.abs(lv) < .32;
        ctx.beginPath();
        for (j = 0; j < ny - 1; j++) for (i = 0; i < nx - 1; i++) {
          var a = g[j*nx+i], b = g[j*nx+i+1], d = g[(j+1)*nx+i+1], e = g[(j+1)*nx+i];
          var x0 = i * st, y0 = j * st, pts = [];
          if ((a < lv) !== (b < lv)) pts.push([x0 + st * (lv - a) / (b - a), y0]);
          if ((b < lv) !== (d < lv)) pts.push([x0 + st, y0 + st * (lv - b) / (d - b)]);
          if ((e < lv) !== (d < lv)) pts.push([x0 + st * (lv - e) / (d - e), y0 + st]);
          if ((a < lv) !== (e < lv)) pts.push([x0, y0 + st * (lv - a) / (e - a)]);
          if (pts.length >= 2) { ctx.moveTo(pts[0][0], pts[0][1]); ctx.lineTo(pts[1][0], pts[1][1]); }
          if (pts.length === 4) { ctx.moveTo(pts[2][0], pts[2][1]); ctx.lineTo(pts[3][0], pts[3][1]); }
        }
        ctx.strokeStyle = key ? 'rgba(' + PH + ',.34)' : 'rgba(' + GR + ',.2)';
        ctx.lineWidth = key ? 1.4 : .85; ctx.lineCap = 'round'; ctx.stroke();
      }
      t++;
    })();
  }

  /* ---------- обложка десанта: специалист спускается в команду ----------
     сначала команда стоит разрозненными точками, сверху приходит один узел,
     садится внутрь и от него по кругу протягиваются связи: сеть начинает работать ---------- */
  function desant(c) {
    var ctx = c.getContext('2d'), W = 0, H = 0, team = [], links = [], t = 0, CYCLE = 1400;
    function build() {
      var r = c.getBoundingClientRect(); W = r.width; H = r.height;
      if (!W || !H) return;
      c.width = W * DPR; c.height = H * DPR; ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
      var narrow = W < 900;
      var cols = narrow ? 6 : 10, rows = narrow ? 8 : 7;
      var pad = Math.max(18, Math.min(W, H) * .05);
      var stepX = (W - pad * 2) / (cols - 1), stepY = (H - pad * 2) / (rows - 1);
      team = [];
      /* сеть занимает правую верхнюю часть кадра и не залезает под текст */
      var x0 = narrow ? pad : W * .38, y0 = pad, x1 = W - pad, y1 = narrow ? H - pad : H * .74;
      var sx = (x1 - x0) / (cols - 1), sy = (y1 - y0) / (rows - 1);
      stepX = sx; stepY = sy;
      for (var gy = 0; gy < rows; gy++) for (var gx = 0; gx < cols; gx++) {
        var i = gy * cols + gx;
        team.push({
          x: x0 + gx * sx + (rnd(i * 7) - .5) * sx * .62,
          y: y0 + gy * sy + (rnd(i * 13) - .5) * sy * .62,
          r: 1.5 + rnd(i * 5) * 1.5, ph: rnd(i * 41) * 6.283
        });
      }
      var lim = Math.hypot(stepX, stepY) * .95;
      links = [];
      for (var a = 0; a < team.length; a++) for (var b = a + 1; b < team.length; b++) {
        var d = Math.hypot(team[a].x - team[b].x, team[a].y - team[b].y);
        if (d < lim && rnd(a * 31 + b * 17) > .28) links.push({a: team[a], b: team[b], d: d});
      }
      /* точка входа специалиста: середина нижней трети, там же центр расхождения волны */
      c._hub = {x: W * (narrow ? .5 : .72), y: H * (narrow ? .5 : .38)};
    }
    build(); watch(c, build);
    function eOut(p) { return 1 - Math.pow(1 - p, 3) }
    (function frame() {
      requestAnimationFrame(frame);
      if (!W || !H) { build(); return }
      if (c.getBoundingClientRect().bottom < -100) { t++; return }
      ctx.clearRect(0, 0, W, H);
      var hub = c._hub, k = t % CYCLE;
      var fade = k > CYCLE - 110 ? (CYCLE - k) / 110 : (k < 50 ? k / 50 : 1);
      /* спуск специалиста: 0 - 260 кадров */
      var drop = Math.max(0, Math.min(1, k / 260));
      var dx = hub.x + (1 - eOut(drop)) * (W * .12), dy = -30 + (hub.y + 30) * eOut(drop);
      /* волна знания расходится от точки входа */
      var waveR = k > 240 ? (k - 240) * (Math.hypot(W, H) / 620) : -1;
      links.forEach(function (ln) {
        var mx = (ln.a.x + ln.b.x) / 2, my = (ln.a.y + ln.b.y) / 2;
        var dd = Math.hypot(mx - hub.x, my - hub.y);
        var on = waveR > dd ? Math.min(1, (waveR - dd) / 140) : 0;
        ctx.beginPath(); ctx.moveTo(ln.a.x, ln.a.y); ctx.lineTo(ln.b.x, ln.b.y);
        ctx.strokeStyle = on > .02
          ? 'rgba(' + PH + ',' + (.08 + on * .3) * fade + ')'
          : 'rgba(' + GR + ',' + .13 * fade + ')';
        ctx.lineWidth = .8 + on * .8; ctx.stroke();
      });
      team.forEach(function (n) {
        var dd = Math.hypot(n.x - hub.x, n.y - hub.y);
        var on = waveR > dd ? Math.min(1, (waveR - dd) / 120) : 0;
        var live = .5 + .5 * Math.sin(t * .02 + n.ph);
        if (on > .05) {
          var g = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, 14);
          g.addColorStop(0, 'rgba(' + PH + ',' + (.22 * on + live * .1) * fade + ')');
          g.addColorStop(1, 'rgba(' + PH + ',0)');
          ctx.fillStyle = g; ctx.beginPath(); ctx.arc(n.x, n.y, 14, 0, 7); ctx.fill();
        }
        ctx.beginPath(); ctx.arc(n.x, n.y, n.r * (1 + on * .35), 0, 7);
        ctx.fillStyle = 'rgba(' + (on > .3 ? PH : WH) + ',' + (.3 + on * .5) * fade + ')';
        ctx.fill();
      });
      /* сам специалист: яркий узел со следом, пока идёт спуск */
      if (drop < 1) {
        ctx.beginPath(); ctx.moveTo(dx, dy - 46); ctx.lineTo(dx, dy);
        var lg = ctx.createLinearGradient(dx, dy - 46, dx, dy);
        lg.addColorStop(0, 'rgba(' + PH + ',0)'); lg.addColorStop(1, 'rgba(' + PH + ',' + .5 * fade + ')');
        ctx.strokeStyle = lg; ctx.lineWidth = 1.4; ctx.stroke();
      }
      var pulse = drop >= 1 ? .5 + .5 * Math.sin(t * .06) : 1;
      var hg = ctx.createRadialGradient(dx, dy, 0, dx, dy, 34 + pulse * 10);
      hg.addColorStop(0, 'rgba(' + PH + ',' + (.34 + pulse * .12) * fade + ')');
      hg.addColorStop(1, 'rgba(' + PH + ',0)');
      ctx.fillStyle = hg; ctx.beginPath(); ctx.arc(dx, dy, 34 + pulse * 10, 0, 7); ctx.fill();
      ctx.beginPath(); ctx.arc(dx, dy, 4.2, 0, 7);
      ctx.fillStyle = 'rgba(' + PH + ',' + .95 * fade + ')'; ctx.fill();
      /* низ кадра растворяется, а справа графика гаснет под цифрами */
      ctx.globalCompositeOperation = 'destination-out';
      if (W > 980) {
        var rg = ctx.createLinearGradient(W * .58, 0, W, 0);
        rg.addColorStop(0, 'rgba(0,0,0,0)');
        rg.addColorStop(1, 'rgba(0,0,0,.72)');
        ctx.fillStyle = rg; ctx.fillRect(W * .58, 0, W * .42, H);
      }
      var fade = ctx.createLinearGradient(0, H - 260, 0, H);
      fade.addColorStop(0, 'rgba(0,0,0,0)');
      fade.addColorStop(1, 'rgba(0,0,0,1)');
      ctx.fillStyle = fade; ctx.fillRect(0, H - 260, W, 260);
      ctx.globalCompositeOperation = 'source-over';
      t++;
    })();
  }

  var COVER = {converge: converge, flow: flow, mesh: meshCover, contour: contour, desant: desant};
  var cov = document.getElementById('synFx');
  if (cov) (COVER[cov.dataset.fx] || converge)(cov);

  /* ---------- блок: матрица связей, круглые ячейки ---------- */
  [].forEach.call(document.querySelectorAll('canvas.fx-matrix'), function (c) {
    var N = 14, cells = [];
    var st = loop(c, function (s, t) {
      var ctx = s.ctx, W = s.W, H = s.H;
      ctx.clearRect(0, 0, W, H);
      var side = Math.min(W, H) - 28, cs = side / N, ox = (W - side) / 2, oy = (H - side) / 2;
      cells.forEach(function (cl) {
        var v = cl.v * (.72 + .28 * Math.sin(t * cl.sp + cl.ph));
        if (v < .05) return;
        var x = ox + cl.j * cs + cs / 2, y = oy + cl.i * cs + cs / 2, r = cs * .42 * (.35 + v * .65);
        ctx.beginPath(); ctx.arc(x, y, r, 0, 7);
        ctx.fillStyle = cl.bridge ? 'rgba(' + PH + ',' + Math.min(1, v * 1.1) + ')'
          : cl.diag ? 'rgba(' + WH + ',' + v * .6 + ')' : 'rgba(' + GR + ',' + v * .62 + ')';
        ctx.fill();
        if (cl.bridge && v > .6) {
          var g = ctx.createRadialGradient(x, y, 0, x, y, r * 3.4);
          g.addColorStop(0, 'rgba(' + PH + ',.2)'); g.addColorStop(1, 'rgba(' + PH + ',0)');
          ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r * 3.4, 0, 7); ctx.fill();
        }
      });
      ctx.strokeStyle = 'rgba(150,160,155,.12)'; ctx.lineWidth = 1;
      ctx.strokeRect(ox - 3, oy - 3, side + 6, side + 6);
    }, 1);
    st.onbuild = function () {
      N = innerWidth < 700 ? 11 : 15; cells = [];
      var grp = function (i) { return Math.floor(i / (N / 3)); };
      for (var i = 0; i < N; i++) for (var j = 0; j < N; j++) {
        var noise = rnd(i * 41 + j * 17), same = grp(i) === grp(j);
        var v = i === j ? .95 : (same ? .3 + noise * .55 : (noise > .84 ? .45 + noise * .45 : noise * .16));
        cells.push({i: i, j: j, v: v, bridge: !same && v > .4, diag: i === j,
          ph: rnd(i * 3 + j * 11) * 6.28, sp: .008 + rnd(i + j * 5) * .016});
      }
    };
    st.onbuild(); st.rebuild();
  });

  /* ---------- блок: слои системы, сигнал идёт снизу вверх ---------- */
  [].forEach.call(document.querySelectorAll('canvas.fx-layers'), function (c) {
    var names = (c.dataset.layers || 'люди,интерфейс,модель,данные').split(',');
    loop(c, function (s, t) {
      var ctx = s.ctx, W = s.W, H = s.H;
      ctx.clearRect(0, 0, W, H);
      var cx = W * .46, cy = H * .5, half = Math.min(W * .21, 190), hh = half * .52, gap = H / (names.length + 1.1);
      ctx.font = '11px "JetBrains Mono", ui-monospace, monospace';
      for (var i = 0; i < names.length; i++) {
        var y = cy + (i - (names.length - 1) / 2) * gap;
        ctx.beginPath();
        ctx.moveTo(cx, y - hh); ctx.lineTo(cx + half, y); ctx.lineTo(cx, y + hh); ctx.lineTo(cx - half, y); ctx.closePath();
        ctx.fillStyle = 'rgba(' + GR + ',.07)'; ctx.fill();
        ctx.strokeStyle = 'rgba(' + GR + ',.5)'; ctx.lineWidth = 1; ctx.stroke();
        ctx.fillStyle = 'rgba(160,170,166,.85)';
        var lx = cx + half + 16;
        if (W < 400) {
          /* на узком экране подпись слоя идёт под ним по центру */
          ctx.textAlign = 'center';
          cap(ctx, names[i].trim(), cx, y + 16, W - 16, 9.5);
          ctx.textAlign = 'left';
          continue;
        }
        if (lx + 40 > W) { ctx.textAlign = 'right'; lx = cx - half - 16; }
        cap(ctx, names[i].trim(), lx, y + 4, Math.max(60, (ctx.textAlign === 'right' ? lx - 6 : W - lx - 6)), 11);
        ctx.textAlign = 'left';
        for (var k = 0; k < 3; k++) {
          var a = (k / 3) * 6.28 + i * .8 + t * .004;
          ctx.beginPath(); ctx.arc(cx + Math.cos(a) * half * .55, y + Math.sin(a) * hh * .5, 1.9, 0, 7);
          ctx.fillStyle = 'rgba(' + WH + ',.5)'; ctx.fill();
        }
      }
      var yTop = cy - (names.length - 1) / 2 * gap, yBot = cy + (names.length - 1) / 2 * gap;
      for (var m = 0; m < 3; m++) {
        var x = cx + (m - 1) * half * .48;
        ctx.beginPath(); ctx.moveTo(x, yTop); ctx.lineTo(x, yBot);
        ctx.strokeStyle = 'rgba(' + GR + ',.26)'; ctx.lineWidth = 1; ctx.stroke();
        var p = ((t * .006 + m * .33) % 1), py = yBot - (yBot - yTop) * p;
        var g = ctx.createRadialGradient(x, py, 0, x, py, 13);
        g.addColorStop(0, 'rgba(' + PH + ',.5)'); g.addColorStop(1, 'rgba(' + PH + ',0)');
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, py, 13, 0, 7); ctx.fill();
        ctx.beginPath(); ctx.arc(x, py, 1.8, 0, 7); ctx.fillStyle = 'rgba(' + PH + ',.9)'; ctx.fill();
      }
    }, function () { return innerWidth < 700 ? 1.25 : 2.3; });
  });

  /* ---------- блок: сигнал до и после ---------- */
  [].forEach.call(document.querySelectorAll('canvas.fx-signal'), function (c) {
    var la = c.dataset.a || 'было', lb = c.dataset.b || 'стало';
    loop(c, function (s, t) {
      var ctx = s.ctx, W = s.W, H = s.H, x;
      ctx.clearRect(0, 0, W, H);
      var tt = t * .015, yA = H * .32, yB = H * .72, amp = H * .17;
      ctx.strokeStyle = 'rgba(150,160,155,.07)'; ctx.lineWidth = 1;
      for (x = 0; x < W; x += 64) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke(); }
      ctx.font = '11px "JetBrains Mono", ui-monospace, monospace';
      ctx.fillStyle = 'rgba(150,160,155,.8)';
      ctx.fillText(la, 16, yA - amp - 12); ctx.fillText(lb, 16, yB - amp * .32 - 12);
      ctx.beginPath();
      for (x = 0; x <= W; x += 2) {
        var n = Math.sin(x * .09 + tt) * .5 + Math.sin(x * .31 - tt * 1.7) * .35 + Math.sin(x * .73 + tt * 2.3) * .3
              + (rnd(Math.floor(x / 2) + Math.floor(t / 6)) - .5) * .55;
        var y = yA + n * amp; x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      }
      ctx.strokeStyle = 'rgba(' + GR + ',.5)'; ctx.lineWidth = 1.1; ctx.stroke();
      ctx.beginPath();
      for (x = 0; x <= W; x += 2) { var y2 = yB + Math.sin(x * .045 + tt * .8) * amp * .27; x === 0 ? ctx.moveTo(x, y2) : ctx.lineTo(x, y2); }
      ctx.strokeStyle = 'rgba(' + PH + ',.72)'; ctx.lineWidth = 1.8; ctx.stroke();
      var px = (t * 2.6) % (W + 130) - 65;
      if (px > 0 && px < W) {
        var py = yB + Math.sin(px * .045 + tt * .8) * amp * .27;
        var g = ctx.createRadialGradient(px, py, 0, px, py, 20);
        g.addColorStop(0, 'rgba(' + PH + ',.45)'); g.addColorStop(1, 'rgba(' + PH + ',0)');
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(px, py, 20, 0, 7); ctx.fill();
      }
    }, function () { return innerWidth < 700 ? 1.5 : 3; });
  });



  /* подпись ужимается по кеглю, пока не влезет в отведённую ширину */
  function cap(ctx, text, x, y, maxw, base) {
    var size = base || 10.5;
    ctx.font = size + 'px "JetBrains Mono", ui-monospace, monospace';
    while (ctx.measureText(text).width > maxw && size > 7.5) {
      size -= .5;
      ctx.font = size + 'px "JetBrains Mono", ui-monospace, monospace';
    }
    ctx.fillText(text, x, y);
  }

  /* ---------- блок: охват отделов за месяц десанта ----------
     четыре отдела и четыре разные схемы: сетка мест, кольцо смен,
     стопка документов, ветка обращений. Точка загорается в день,
     когда человек начал работать с нейросетями ---------- */
  [].forEach.call(document.querySelectorAll('canvas.fx-adopt'), function (c) {
    /* четыре отдела, у каждого своя иконка и свои люди точками.
       Точка загорается в тот день, когда человек начал работать с нейросетями */
    var DEPTS = [
      {n: 'продажи', k: 16, ic: 'money'},
      {n: 'закупки', k: 12, ic: 'box'},
      {n: 'документы', k: 14, ic: 'doc'},
      {n: 'поддержка', k: 13, ic: 'chat'}
    ];
    function jd(i, j) { return 2 + ((i * 5 + j * 7) % 24) }
    function icon(ctx, kind, x, y, s, on) {
      ctx.save();
      ctx.translate(x, y);
      ctx.strokeStyle = 'rgba(' + (on ? PH : GR) + ',' + (on ? .85 : .5) + ')';
      ctx.fillStyle = 'rgba(' + (on ? PH : GR) + ',' + (on ? .18 : .08) + ')';
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      if (kind === 'money') {
        /* монета со столбиком роста */
        ctx.arc(0, 0, s * .5, 0, 7); ctx.fill(); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(-s * .16, s * .16); ctx.lineTo(-s * .16, -s * .04);
        ctx.moveTo(0, s * .16); ctx.lineTo(0, -s * .16);
        ctx.moveTo(s * .16, s * .16); ctx.lineTo(s * .16, -s * .1); ctx.stroke();
      } else if (kind === 'box') {
        /* коробка поставки */
        ctx.rect(-s * .5, -s * .34, s, s * .68); ctx.fill(); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(-s * .5, -s * .1); ctx.lineTo(s * .5, -s * .1);
        ctx.moveTo(0, -s * .1); ctx.lineTo(0, s * .34); ctx.stroke();
      } else if (kind === 'doc') {
        /* лист с таблицей */
        ctx.rect(-s * .38, -s * .48, s * .76, s * .96); ctx.fill(); ctx.stroke();
        ctx.beginPath();
        for (var r = -1; r <= 1; r++) { ctx.moveTo(-s * .24, r * s * .22); ctx.lineTo(s * .24, r * s * .22) }
        ctx.stroke();
      } else {
        /* облако диалога */
        if (ctx.roundRect) ctx.roundRect(-s * .5, -s * .42, s, s * .7, s * .2);
        else ctx.rect(-s * .5, -s * .42, s, s * .7);
        ctx.fill(); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(-s * .12, s * .28); ctx.lineTo(-s * .02, s * .46);
        ctx.lineTo(s * .1, s * .28); ctx.stroke();
      }
      ctx.restore();
    }
    function dot(ctx, x, y, on, r) {
      if (on) {
        var g = ctx.createRadialGradient(x, y, 0, x, y, r * 2.8);
        g.addColorStop(0, 'rgba(' + PH + ',.32)'); g.addColorStop(1, 'rgba(' + PH + ',0)');
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r * 2.8, 0, 7); ctx.fill();
      }
      ctx.beginPath(); ctx.arc(x, y, on ? r : r * .74, 0, 7);
      ctx.fillStyle = on ? 'rgba(' + PH + ',.9)' : 'rgba(' + GR + ',.3)';
      ctx.fill();
    }
    loop(c, function (s, t) {
      var ctx = s.ctx, W = s.W, H = s.H, i, j;
      ctx.clearRect(0, 0, W, H);
      var cycle = 900, kk = (t % cycle) / cycle, day = Math.floor(kk * 34);
      var pad = 10, headH = 30;
      var tw = (W - pad * 2) / 2, th = (H - headH - pad) / 2;
      var total = 0, lit = 0;
      for (i = 0; i < DEPTS.length; i++) {
        var d = DEPTS[i];
        var tx = pad + (i % 2) * tw, ty = headH + Math.floor(i / 2) * th;
        var done = 0;
        for (j = 0; j < d.k; j++) { total++; if (day >= jd(i, j)) { done++; lit++ } }
        var full = done === d.k;
        /* иконка отдела, рядом название, справа счётчик людей */
        ctx.textAlign = 'left'; ctx.fillStyle = 'rgba(' + GR + ',.85)';
        cap(ctx, d.n, tx + 2, ty + 12, tw * .5, 10.5);
        ctx.textAlign = 'right'; ctx.fillStyle = 'rgba(' + (full ? PH : GR) + ',.85)';
        cap(ctx, done + ' из ' + d.k, tx + tw - 10, ty + 12, tw * .34, 10);
        ctx.textAlign = 'left';
        /* люди отдела: сетка точек под иконкой */
        var bx = tx + 6, by = ty + 30, bw = tw - 20, bh = th - 40;
        var cols = Math.min(6, Math.ceil(Math.sqrt(d.k * 1.6)));
        var rows = Math.ceil(d.k / cols);
        var gx = Math.min(bw / (cols + .4), 42), gy = Math.min(bh / (rows + .3), 38);
        var mx = bx + bw / 2, my = by + bh / 2;
        for (j = 0; j < d.k; j++) {
          var x = mx + ((j % cols) - (cols - 1) / 2) * gx;
          var y = my + (Math.floor(j / cols) - (rows - 1) / 2) * gy;
          dot(ctx, x, y, day >= jd(i, j), 3.4);
        }
      }
      ctx.textAlign = 'left'; ctx.fillStyle = 'rgba(' + GR + ',.75)';
      cap(ctx, 'день ' + Math.max(1, day) + ' из 30', pad, 14, W * .4, 10.5);
      ctx.textAlign = 'right'; ctx.fillStyle = 'rgba(' + PH + ',.9)';
      cap(ctx, lit + ' из ' + total + ' работают с AI', W - pad, 14, W * .52, 10.5);
      ctx.textAlign = 'left';
    }, function () { return innerWidth < 700 ? 1.06 : 1.24; });
  });

  /* ---------- блок: переписка с агентом клуба ----------
     вопрос участника сверху слева, база знаний полками по центру,
     ответ агента снизу справа: сообщением со ссылкой или готовым файлом.
     Связи идут мягкими дугами, прямых пунктиров нет ---------- */
  [].forEach.call(document.querySelectorAll('canvas.fx-dialog'), function (c) {
    var Q = ['Как поднять загрузку кресел?', 'Что делать с оттоком пациентов?',
             'Как платить врачам?'];
    var A = [{t: 'Разбор по методологии клуба', f: 'разбор.pdf'},
             {t: 'Собрал аудит по вашим данным', f: null, src: 'источник: стандарт клуба'},
             {t: 'Расчёт оплаты труда готов', f: 'расчёт.xlsx'}];
    function rows(ctx, text, maxw) {
      var words = text.split(' '), out = [], cur = '';
      for (var i = 0; i < words.length; i++) {
        var test = cur ? cur + ' ' + words[i] : words[i];
        if (ctx.measureText(test).width > maxw && cur) { out.push(cur); cur = words[i]; }
        else cur = test;
      }
      if (cur) out.push(cur);
      return out;
    }
    function bubble(ctx, x, y, w, h, accent, a, right) {
      var col = accent ? PH : GR;
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(x, y, w, h, 12); else ctx.rect(x, y, w, h);
      ctx.fillStyle = 'rgba(' + col + ',' + (.1 * a) + ')'; ctx.fill();
      ctx.strokeStyle = 'rgba(' + col + ',' + (.42 * a) + ')'; ctx.lineWidth = 1; ctx.stroke();
      ctx.beginPath();
      if (right) { ctx.moveTo(x + w - 14, y + h); ctx.lineTo(x + w - 3, y + h + 6); ctx.lineTo(x + w - 5, y + h); }
      else { ctx.moveTo(x + 14, y + h); ctx.lineTo(x + 3, y + h + 6); ctx.lineTo(x + 5, y + h); }
      ctx.fillStyle = 'rgba(' + col + ',' + (.42 * a) + ')'; ctx.fill();
    }
    /* дуга вместо прямой линии: видно направление, но линия не режет кадр */
    function arc(ctx, x0, y0, x1, y1, cx, cy, accent, a, prog) {
      var col = accent ? PH : GR;
      ctx.beginPath(); ctx.moveTo(x0, y0); ctx.quadraticCurveTo(cx, cy, x1, y1);
      ctx.strokeStyle = 'rgba(' + col + ',' + (.1 + a * .22) + ')'; ctx.lineWidth = 1; ctx.stroke();
      if (prog > 0 && prog < 1) {
        var u = prog, iu = 1 - u;
        var px = iu * iu * x0 + 2 * iu * u * cx + u * u * x1;
        var py = iu * iu * y0 + 2 * iu * u * cy + u * u * y1;
        var g = ctx.createRadialGradient(px, py, 0, px, py, 9);
        g.addColorStop(0, 'rgba(' + col + ',.5)'); g.addColorStop(1, 'rgba(' + col + ',0)');
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(px, py, 9, 0, 7); ctx.fill();
        ctx.beginPath(); ctx.arc(px, py, 2.4, 0, 7);
        ctx.fillStyle = 'rgba(' + col + ',.95)'; ctx.fill();
      }
    }
    loop(c, function (s, t) {
      var ctx = s.ctx, W = s.W, H = s.H, i;
      ctx.clearRect(0, 0, W, H);
      var narrow = W < 470;
      var fs = narrow ? 10.5 : 12, lh = fs + 5, pad = narrow ? 10 : 14;
      var bw = narrow ? Math.min(W - pad * 2 - 24, 236) : Math.min(W * .46, 250);
      /* темп вдвое быстрее прежнего: полный цикл около пяти секунд */
      var cycle = 290, k = t % cycle, idx = Math.floor(t / cycle) % Q.length;
      var qa = Math.min(1, k / 24);
      var sp = k < 34 ? 0 : Math.min(1, (k - 34) / 44);
      var ra = k < 92 ? 0 : Math.min(1, (k - 92) / 38);
      var p1 = Math.max(0, Math.min(1, (k - 18) / 34));
      var p2 = Math.max(0, Math.min(1, (k - 70) / 30));
      ctx.font = fs + 'px "JetBrains Mono", ui-monospace, monospace';
      ctx.textAlign = 'left';

      /* база знаний: стеллаж с корешками книг, читается как библиотека */
      var shW = narrow ? 148 : 188, shelfH = narrow ? 28 : 34, SH_ROWS = 3;
      var shH = SH_ROWS * shelfH + 14;
      var sx = W / 2 - shW / 2, sy = H / 2 - shH / 2;
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(sx, sy, shW, shH, 8); else ctx.rect(sx, sy, shW, shH);
      ctx.fillStyle = 'rgba(' + GR + ',.06)'; ctx.fill();
      ctx.strokeStyle = 'rgba(' + GR + ',' + (.34 + sp * .24) + ')'; ctx.lineWidth = 1.4; ctx.stroke();
      /* боковые стойки стеллажа */
      var wall = 3;
      ctx.fillStyle = 'rgba(' + GR + ',.24)';
      ctx.fillRect(sx + 5, sy + 7, wall, shH - 14);
      ctx.fillRect(sx + shW - 5 - wall, sy + 7, wall, shH - 14);
      var inx = sx + 12, inw = shW - 24, total = 0, hot = 7 + idx * 9, BOOKS = 33;
      for (var r = 0; r < SH_ROWS; r++) {
        var base = sy + 7 + (r + 1) * shelfH - 4, ih = shelfH - 9, x = inx;
        for (i = 0; i < 20; i++) {
          var wd = (narrow ? 7 : 8) + rnd(r * 17 + i * 5) * (narrow ? 5 : 7);
          if (x + wd > inx + inw) break;
          var hh = ih * (.6 + rnd(r * 23 + i * 3) * .4);
          var tilt = rnd(r * 31 + i * 11) > .87 ? -.2 : 0;
          var on = sp * BOOKS > total, mine = total === hot;
          var col = on || mine ? PH : GR;
          var al = mine && ra > 0 ? .3 + .26 * Math.sin(t * .13) : (on ? .2 : .07);
          ctx.save();
          ctx.translate(x, base); ctx.rotate(tilt);
          ctx.beginPath();
          if (ctx.roundRect) ctx.roundRect(0, -hh, wd, hh, 1.5); else ctx.rect(0, -hh, wd, hh);
          ctx.fillStyle = 'rgba(' + col + ',' + al + ')'; ctx.fill();
          ctx.strokeStyle = 'rgba(' + col + ',' + (on || mine ? .5 : .3) + ')';
          ctx.lineWidth = 1; ctx.stroke();
          /* поперечная насечка на корешке: книга, а не просто блок */
          ctx.beginPath(); ctx.moveTo(1.5, -hh + 5); ctx.lineTo(wd - 1.5, -hh + 5);
          ctx.strokeStyle = 'rgba(' + col + ',' + (on || mine ? .38 : .18) + ')';
          ctx.lineWidth = .8; ctx.stroke();
          ctx.restore();
          x += wd + 2.4; total++;
        }
        /* полка под корешками */
        ctx.beginPath(); ctx.moveTo(sx + 5, base + 2); ctx.lineTo(sx + shW - 5, base + 2);
        ctx.strokeStyle = 'rgba(' + GR + ',.36)'; ctx.lineWidth = 1.4; ctx.stroke();
      }
      ctx.textAlign = 'center'; ctx.fillStyle = 'rgba(' + (sp > .15 ? PH : GR) + ',.85)';
      cap(ctx, 'база знаний клуба', W / 2, sy - 10, shW + 60, narrow ? 9.5 : 10.5);

      /* вопрос участника сверху слева */
      ctx.font = fs + 'px "JetBrains Mono", ui-monospace, monospace';
      var qr = rows(ctx, Q[idx], bw - 26), qh = qr.length * lh + 15, qy = narrow ? 30 : 36;
      ctx.textAlign = 'left'; ctx.fillStyle = 'rgba(' + GR + ',.75)';
      cap(ctx, 'участник клуба', pad + 2, qy - 8, bw, narrow ? 9.5 : 10.5);
      bubble(ctx, pad, qy, bw, qh, false, qa, false);
      ctx.font = fs + 'px "JetBrains Mono", ui-monospace, monospace';
      ctx.fillStyle = 'rgba(' + WH + ',' + (.88 * qa) + ')';
      qr.forEach(function (line, j) { ctx.fillText(line, pad + 13, qy + 13 + j * lh + 3); });

      /* ответ агента снизу справа: сообщение со ссылкой либо готовый файл */
      var ans = A[idx];
      var ar = rows(ctx, ans.t, bw - 26);
      var attach = narrow ? 20 : 22;
      var ah = ar.length * lh + 15 + attach;
      var ax = W - pad - bw, ay = H - pad - ah - (narrow ? 10 : 12);
      if (ra > 0) {
        ctx.textAlign = 'left'; ctx.fillStyle = 'rgba(' + PH + ',' + (.7 * ra) + ')';
        cap(ctx, 'агент клуба', ax + 2, ay - 8, bw, narrow ? 9.5 : 10.5);
        bubble(ctx, ax, ay, bw, ah, true, ra, true);
        ctx.font = fs + 'px "JetBrains Mono", ui-monospace, monospace';
        ctx.fillStyle = 'rgba(' + WH + ',' + (.92 * ra) + ')';
        ar.forEach(function (line, j) { ctx.fillText(line, ax + 13, ay + 13 + j * lh + 3); });
        var fy = ay + ar.length * lh + 8;
        if (ra > .55) {
          var la = (ra - .55) / .45;
          if (ans.f) {
            var fw = narrow ? 84 : 92, fh = narrow ? 16 : 18;
            ctx.beginPath();
            if (ctx.roundRect) ctx.roundRect(ax + 13, fy, fw, fh, 5); else ctx.rect(ax + 13, fy, fw, fh);
            ctx.fillStyle = 'rgba(' + PH + ',' + (.14 * la) + ')'; ctx.fill();
            ctx.strokeStyle = 'rgba(' + PH + ',' + (.5 * la) + ')'; ctx.lineWidth = 1; ctx.stroke();
            ctx.textAlign = 'left'; ctx.fillStyle = 'rgba(' + PH + ',' + (.92 * la) + ')';
            cap(ctx, ans.f, ax + 21, fy + fh - 5, fw - 14, 9.5);
          } else {
            /* ссылка на источник: подчёркивание идёт ровно под своим текстом */
            ctx.textAlign = 'left'; ctx.font = '9.5px "JetBrains Mono", ui-monospace, monospace';
            var tw = Math.min(ctx.measureText(ans.src).width, bw - 30);
            ctx.fillStyle = 'rgba(' + PH + ',' + (.9 * la) + ')';
            ctx.fillText(ans.src, ax + 13, fy + 10);
            ctx.beginPath(); ctx.moveTo(ax + 13, fy + 13.5); ctx.lineTo(ax + 13 + tw, fy + 13.5);
            ctx.strokeStyle = 'rgba(' + PH + ',' + (.6 * la) + ')'; ctx.lineWidth = 1; ctx.stroke();
          }
        }
      }

      /* дуги: вопрос идёт к полкам, ответ возвращается из них */
      arc(ctx, pad + 22, qy + qh + 7, sx + 12, sy - 3,
          pad + 16, sy - 26, false, qa, p1);
      arc(ctx, sx + shW - 12, sy + shH + 3, ax + bw - 26, ay - 6,
          ax + bw - 20, sy + shH + 22, true, ra + sp * .4, p2);
      ctx.textAlign = 'left';
    }, function () { return innerWidth < 700 ? 1.1 : 1.55; });
  });

  /* ---------- блок: как агент клуба ведёт разбор ----------
     слева живая переписка участника, в центре агент со слоями базы знаний,
     справа четыре сценария аудита. Виден весь путь от вопроса до документа ---------- */
  [].forEach.call(document.querySelectorAll('canvas.fx-routeq'), function (c) {
    var LAYERS = ['книги и протоколы', 'вопрос-ответ клуба', 'уроки и эфиры', 'данные клиники'];
    var SCEN = ['стратегический аудит', 'P&L-анализ', 'имплант-калькулятор', 'разбор переписки'];
    var SCEN_S = ['стратегия', 'P&L', 'импланты', 'переписка'];
    var CHAT = ['Как поднять загрузку кресел?', 'Смотрю ваш P&L и график записи', 'Собрал разбор на 17 разделов'];
    loop(c, function (s, t) {
      var ctx = s.ctx, W = s.W, H = s.H, i;
      ctx.clearRect(0, 0, W, H);
      var narrow = W < 620, tiny = W < 640;
      if (tiny) {
        /* на телефоне схема идёт сверху вниз: вопрос, агент со слоями, сценарии */
        ctx.font = '9px "JetBrains Mono", ui-monospace, monospace';
        var cxc = W / 2, ay = H * .46;
        ctx.fillStyle = 'rgba(' + GR + ',.8)'; ctx.textAlign = 'center';
        cap(ctx, 'вопрос участника', cxc, 16, W - 20, 9);
        for (var li = 0; li < 4; li++) {
          var rr2 = 20 + li * 9, a2 = t * (0.0026 - li * 0.0004) + li * 1.2;
          ctx.beginPath(); ctx.ellipse(cxc, ay, rr2, rr2 * .62, a2 * .3, 0, 7);
          ctx.setLineDash([3, 6]); ctx.strokeStyle = 'rgba(' + GR + ',' + (.3 - li * .05) + ')';
          ctx.lineWidth = 1; ctx.stroke(); ctx.setLineDash([]);
          var px2 = cxc + Math.cos(a2) * rr2, py2 = ay + Math.sin(a2) * rr2 * .62;
          ctx.beginPath(); ctx.arc(px2, py2, 1.8, 0, 7);
          ctx.fillStyle = 'rgba(' + PH + ',.8)'; ctx.fill();
        }
        ctx.beginPath(); ctx.arc(cxc, ay, 5, 0, 7);
        ctx.fillStyle = 'rgba(' + PH + ',.95)'; ctx.fill();
        ctx.fillStyle = 'rgba(' + GR + ',.85)';
        cap(ctx, 'агент клуба и база знаний', cxc, Math.min(ay + 32, H - 9 - SCEN_S.length * 12 - 6), W - 20, 9);
        var live2 = Math.floor(t / 170) % SCEN_S.length;
        for (var si2 = 0; si2 < SCEN_S.length; si2++) {
          /* строки сценариев считаем от нижнего края, чтобы последняя не срезалась */
          var on2 = si2 === live2, ly2 = H - 9 - (SCEN_S.length - 1 - si2) * 12;
          ctx.fillStyle = 'rgba(' + (on2 ? PH : GR) + ',' + (on2 ? .95 : .55) + ')';
          cap(ctx, SCEN_S[si2], cxc, ly2, W - 20, 9);
        }
        ctx.textAlign = 'left';
        return;
      }
      var chatX = W * (narrow ? .05 : .05), chatW = W * (narrow ? .34 : .30);
      var hubX = W * (narrow ? .52 : .53), hubY = H * .5;
      var scenX = W * (narrow ? .68 : .74);
      var names = narrow ? SCEN_S : SCEN;

      /* переписка участника: реплики появляются по очереди */
      ctx.font = (narrow ? 9 : 10.5) + 'px "JetBrains Mono", ui-monospace, monospace';
      var shown = 1 + Math.floor((t % 480) / 160);
      for (i = 0; i < Math.min(shown, CHAT.length); i++) {
        var mine = i % 2 === 0;
        var maxRow = Math.min(chatW - 20, W * .42);
        var words = CHAT[i].split(' '), rows = [], cur = '';
        words.forEach(function (w) {
          var test = cur ? cur + ' ' + w : w;
          if (ctx.measureText(test).width > maxRow && cur) { rows.push(cur); cur = w; } else cur = test;
        });
        if (cur) rows.push(cur);
        var lh = narrow ? 13 : 15, bh = rows.length * lh + 12;
        var by = H * .22 + i * (bh + 12);
        var bw = 0; rows.forEach(function (r) { bw = Math.max(bw, ctx.measureText(r).width); });
        ctx.fillStyle = mine ? 'rgba(' + GR + ',.14)' : 'rgba(' + PH + ',.14)';
        ctx.strokeStyle = mine ? 'rgba(' + GR + ',.3)' : 'rgba(' + PH + ',.4)';
        ctx.lineWidth = 1;
        if (ctx.roundRect) { ctx.beginPath(); ctx.roundRect(chatX, by, bw + 18, bh, 10); ctx.fill(); ctx.stroke(); }
        ctx.fillStyle = mine ? 'rgba(' + GR + ',.95)' : 'rgba(' + WH + ',.95)';
        rows.forEach(function (r, k) { ctx.fillText(r, chatX + 9, by + 12 + k * lh); });
        /* от последней реплики к агенту тянется связь */
        if (i === Math.min(shown, CHAT.length) - 1) {
          ctx.beginPath(); ctx.moveTo(chatX + bw + 18, by + bh / 2);
          ctx.lineTo(hubX - 26, hubY);
          ctx.strokeStyle = 'rgba(' + PH + ',.34)'; ctx.stroke();
        }
      }

      /* слои базы знаний вращаются вокруг агента */
      for (i = 0; i < LAYERS.length; i++) {
        var rr = (narrow ? 26 : 34) + i * (narrow ? 9 : 13);
        var a0 = t * (0.0028 - i * 0.0004) + i * 1.2;
        ctx.beginPath();
        ctx.ellipse(hubX, hubY, rr, rr * .62, a0 * .35, 0, 7);
        ctx.setLineDash([3, 6]);
        ctx.strokeStyle = 'rgba(' + GR + ',' + (.34 - i * .05) + ')'; ctx.lineWidth = 1; ctx.stroke();
        ctx.setLineDash([]);
        /* точка знания бежит по своему слою */
        var px = hubX + Math.cos(a0) * rr, py = hubY + Math.sin(a0) * rr * .62;
        var g = ctx.createRadialGradient(px, py, 0, px, py, 9);
        g.addColorStop(0, 'rgba(' + PH + ',.45)'); g.addColorStop(1, 'rgba(' + PH + ',0)');
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(px, py, 9, 0, 7); ctx.fill();
        ctx.beginPath(); ctx.arc(px, py, 1.9, 0, 7);
        ctx.fillStyle = 'rgba(' + PH + ',.85)'; ctx.fill();
      }
      /* ядро агента */
      var pulse = .5 + .5 * Math.sin(t * .03);
      var hg = ctx.createRadialGradient(hubX, hubY, 0, hubX, hubY, 26 + pulse * 8);
      hg.addColorStop(0, 'rgba(' + PH + ',' + (.22 + pulse * .12) + ')'); hg.addColorStop(1, 'rgba(' + PH + ',0)');
      ctx.fillStyle = hg; ctx.beginPath(); ctx.arc(hubX, hubY, 26 + pulse * 8, 0, 7); ctx.fill();
      ctx.beginPath(); ctx.arc(hubX, hubY, 5.4 + pulse, 0, 7);
      ctx.fillStyle = 'rgba(' + PH + ',.95)'; ctx.fill();
      ctx.font = (narrow ? 9 : 10.5) + 'px "JetBrains Mono", ui-monospace, monospace';
      ctx.textAlign = 'center'; ctx.fillStyle = 'rgba(' + GR + ',.85)';
      cap(ctx, 'агент клуба', hubX, Math.min(H - 6, hubY + (narrow ? 62 : 78)), W * .34, narrow ? 9 : 10.5);
      ctx.textAlign = 'left';

      /* четыре сценария справа: активный подсвечивается по очереди */
      var live = Math.floor(t / 170) % SCEN.length;
      for (i = 0; i < SCEN.length; i++) {
        var sy = H * (narrow ? .22 : .24) + i * H * (narrow ? .18 : .17);
        var on = i === live;
        ctx.beginPath(); ctx.moveTo(hubX + (narrow ? 30 : 44), hubY);
        ctx.quadraticCurveTo((hubX + scenX) / 2, sy, scenX - 6, sy);
        ctx.strokeStyle = 'rgba(' + (on ? PH : GR) + ',' + (on ? .55 : .16) + ')';
        ctx.lineWidth = on ? 1.4 : .9; ctx.stroke();
        ctx.beginPath(); ctx.arc(scenX - 6, sy, on ? 4 : 2.8, 0, 7);
        ctx.fillStyle = 'rgba(' + (on ? PH : WH) + ',' + (on ? 1 : .55) + ')'; ctx.fill();
        ctx.font = (narrow ? 8.5 : 10) + 'px "JetBrains Mono", ui-monospace, monospace';
        ctx.fillStyle = 'rgba(' + (on ? PH : GR) + ',' + (on ? .95 : .6) + ')';
        ctx.fillText(names[i], scenX + 6, sy + 3.5);
        /* по активному маршруту идёт документ */
        if (on) {
          var q = ((t % 170) / 170), m = 1 - q;
          var cx2 = (hubX + scenX) / 2;
          var dx = m * m * (hubX + (narrow ? 30 : 44)) + 2 * m * q * cx2 + q * q * (scenX - 6);
          var dy = m * m * hubY + 2 * m * q * sy + q * q * sy;
          ctx.beginPath(); ctx.arc(dx, dy, 2.6, 0, 7);
          ctx.fillStyle = 'rgba(' + PH + ',.9)'; ctx.fill();
        }
      }

      /* подписи сторон */
      ctx.font = (narrow ? 8.5 : 10) + 'px "JetBrains Mono", ui-monospace, monospace';
      ctx.fillStyle = 'rgba(' + GR + ',.7)';
      ctx.fillText('вопрос участника', chatX, H * .12);
      ctx.fillText('сценарии разбора', scenX - 6, H * .12);
    }, function () { return innerWidth < 700 ? 1.25 : 2.7; });
  });

  /* ---------- блок: очередь заявок до и после запуска ----------
     сверху обращения копятся и ждут ответа, снизу тот же поток разбирается сразу ---------- */
  [].forEach.call(document.querySelectorAll('canvas.fx-queue'), function (c) {
    var la = c.dataset.a || 'было', lb = c.dataset.b || 'стало';
    loop(c, function (s, t) {
      var ctx = s.ctx, W = s.W, H = s.H, i;
      ctx.clearRect(0, 0, W, H);
      var yA = H * .34, yB = H * .74, x0 = W * .10, x1 = W * .90;
      ctx.font = '11px "JetBrains Mono", ui-monospace, monospace';
      ctx.fillStyle = 'rgba(' + GR + ',.85)';
      ctx.fillText(la, x0, yA - H * .16); ctx.fillText(lb, x0, yB - H * .16);
      [yA, yB].forEach(function (y) {
        ctx.beginPath(); ctx.moveTo(x0, y); ctx.lineTo(x1, y);
        ctx.strokeStyle = 'rgba(' + GR + ',.2)'; ctx.lineWidth = 1; ctx.stroke();
      });
      /* верхняя дорожка: заявки доходят до менеджера и встают в очередь */
      var stop = W * .62, waiting = 0;
      for (i = 0; i < 14; i++) {
        var ph = ((t * .0022) + i * .07) % 1;
        var x = x0 + (x1 - x0) * ph;
        if (x > stop) { x = stop - waiting * 11; waiting++; }
        ctx.beginPath(); ctx.arc(x, yA, 3.4, 0, 7);
        ctx.fillStyle = x >= stop - waiting * 11 && waiting ? 'rgba(' + GR + ',.75)' : 'rgba(' + GR + ',.45)';
        ctx.fill();
      }
      ctx.setLineDash([4, 5]);
      ctx.beginPath(); ctx.moveTo(stop, yA - H * .1); ctx.lineTo(stop, yA + H * .1);
      ctx.strokeStyle = 'rgba(' + GR + ',.5)'; ctx.stroke(); ctx.setLineDash([]);
      ctx.fillStyle = 'rgba(' + GR + ',.7)';
      ctx.fillText('ждут ответа', stop + 10, yA + H * .13);
      /* нижняя дорожка: агент отвечает сразу, поток идёт ровно */
      for (i = 0; i < 14; i++) {
        var q = ((t * .0055) + i * .071) % 1;
        var bx = x0 + (x1 - x0) * q;
        ctx.beginPath(); ctx.arc(bx, yB, 3.4, 0, 7);
        ctx.fillStyle = 'rgba(' + PH + ',' + (.5 + .4 * Math.sin(q * Math.PI)) + ')'; ctx.fill();
      }
      ctx.fillStyle = 'rgba(' + PH + ',.8)';
      ctx.fillText('ответ сразу', x1 - 78, yB + H * .13);
    }, function () { return innerWidth < 700 ? 1.5 : 2.6; });
  });

  /* ---------- блок: переписка с агентом ----------
     реплики появляются по очереди, агент печатает ответ ---------- */
  [].forEach.call(document.querySelectorAll('canvas.fx-chat'), function (c) {
    var lines = (c.dataset.chat || 'Есть доставка в Казань?|Да, два раза в неделю. Подскажите объём|Паллета в неделю|Собрал заявку и передал менеджеру').split('|');
    loop(c, function (s, t) {
      var ctx = s.ctx, W = s.W, H = s.H;
      ctx.clearRect(0, 0, W, H);
      var pad = W * .07, bw = Math.min(W * .62, 330), lh = 17, gap = 14;
      var cycle = 150, shown = Math.min(lines.length, Math.floor((t % (cycle * (lines.length + 2))) / cycle));
      var y = H * .12;
      for (var i = 0; i < shown; i++) {
        var mine = i % 2 === 0;
        ctx.font = '12px "JetBrains Mono", ui-monospace, monospace';
        var words = lines[i].split(' '), rows = [], cur = '';
        words.forEach(function (w) {
          var test = cur ? cur + ' ' + w : w;
          if (ctx.measureText(test).width > bw - 26 && cur) { rows.push(cur); cur = w; } else cur = test;
        });
        if (cur) rows.push(cur);
        var h = rows.length * lh + 16;
        var w = 0; rows.forEach(function (r) { w = Math.max(w, ctx.measureText(r).width); });
        var x = mine ? pad : W - pad - (w + 26);
        ctx.fillStyle = mine ? 'rgba(' + GR + ',.16)' : 'rgba(' + PH + ',.16)';
        ctx.strokeStyle = mine ? 'rgba(' + GR + ',.3)' : 'rgba(' + PH + ',.42)';
        ctx.lineWidth = 1;
        if (ctx.roundRect) { ctx.beginPath(); ctx.roundRect(x, y, w + 26, h, 12); ctx.fill(); ctx.stroke(); }
        else { ctx.fillRect(x, y, w + 26, h); ctx.strokeRect(x, y, w + 26, h); }
        ctx.fillStyle = mine ? 'rgba(' + GR + ',.95)' : 'rgba(' + WH + ',.95)';
        rows.forEach(function (r, k) { ctx.fillText(r, x + 13, y + 15 + k * lh); });
        y += h + gap;
      }
      /* агент набирает следующий ответ */
      if (shown < lines.length) {
        var dots = Math.floor(t / 18) % 3 + 1, dx = W - pad - 54;
        ctx.fillStyle = 'rgba(' + PH + ',.16)';
        ctx.strokeStyle = 'rgba(' + PH + ',.35)';
        if (ctx.roundRect) { ctx.beginPath(); ctx.roundRect(dx, y, 54, 26, 12); ctx.fill(); ctx.stroke(); }
        for (var d = 0; d < dots; d++) {
          ctx.beginPath(); ctx.arc(dx + 16 + d * 11, y + 13, 2.4, 0, 7);
          ctx.fillStyle = 'rgba(' + PH + ',.8)'; ctx.fill();
        }
      }
    }, function () { return innerWidth < 700 ? 1.25 : 1.9; });
  });

  /* ---------- блок: малые кратные, разные сети рядом ---------- */
  [].forEach.call(document.querySelectorAll('canvas.fx-multiples'), function (c) {
    var nets = [];
    var st = loop(c, function (s, t) {
      var ctx = s.ctx, W = s.W, H = s.H;
      ctx.clearRect(0, 0, W, H);
      nets.forEach(function (nt) {
        nt.nodes.forEach(function (nd) {
          ctx.beginPath(); ctx.moveTo(nt.cx, nt.cy); ctx.lineTo(nd.x, nd.y);
          ctx.strokeStyle = 'rgba(' + GR + ',.38)'; ctx.lineWidth = .9; ctx.stroke();
          var p = (t * nt.sp + nd.ph) % 1;
          ctx.beginPath(); ctx.arc(nd.x + (nt.cx - nd.x) * p, nd.y + (nt.cy - nd.y) * p, 2, 0, 7);
          ctx.fillStyle = 'rgba(' + PH + ',' + .8 * Math.sin(p * Math.PI) + ')'; ctx.fill();
          ctx.beginPath(); ctx.arc(nd.x, nd.y, 2.3, 0, 7); ctx.fillStyle = 'rgba(' + WH + ',.5)'; ctx.fill();
        });
        ctx.beginPath(); ctx.arc(nt.cx, nt.cy, 4.2, 0, 7); ctx.fillStyle = 'rgba(' + PH + ',.9)'; ctx.fill();
      });
    }, function () { return innerWidth < 700 ? 1.1 : 3.2; });
    st.onbuild = function () {
      var W = st.W, H = st.H, cols = innerWidth < 700 ? 2 : 4, rows = innerWidth < 700 ? 2 : 1;
      nets = [];
      for (var k = 0; k < 4; k++) {
        var cw = W / cols, ch = H / rows, cx = (k % cols) * cw + cw / 2, cy = Math.floor(k / cols) * ch + ch / 2;
        var R = Math.min(cw, ch) * .3, cnt = 4 + Math.floor(rnd(k * 13) * 3), nodes = [];
        for (var i = 0; i < cnt; i++) {
          var a = (i / cnt) * 6.28 + rnd(k * 7 + i) * 1.1, rr = R * (.55 + rnd(k * 5 + i) * .6);
          nodes.push({x: cx + Math.cos(a) * rr, y: cy + Math.sin(a) * rr, ph: rnd(k * 3 + i) * 6.28});
        }
        nets.push({cx: cx, cy: cy, nodes: nodes, sp: .011 + rnd(k) * .008});
      }
    };
    st.onbuild(); st.rebuild();
  });

  /* ---------- блок: плотность, растр из точек ---------- */
  [].forEach.call(document.querySelectorAll('canvas.fx-halftone'), function (c) {
    /* охват по людям: каждый кружок это сотрудник, шаг сетки одинаков по обеим осям,
       поэтому точки остаются ровными на любой ширине холста */
    var PEOPLE = +(c.dataset.people || 27), DAYS = +(c.dataset.days || 30), FINAL = +(c.dataset.final || PEOPLE - 1);
    function joinDay(i) { return 2 + ((i * 7 + (i % 5) * 3) % (DAYS - 4)) }
    loop(c, function (s, t) {
      var ctx = s.ctx, W = s.W, H = s.H, i;
      ctx.clearRect(0, 0, W, H);
      var cycle = 520, day = Math.floor(((t % cycle) / cycle) * (DAYS + 4));
      var padX = 16, padTop = 34, padBot = 18;
      var cols = Math.max(4, Math.min(9, Math.round(Math.sqrt(PEOPLE * (W / Math.max(1, H))))));
      var rows = Math.ceil(PEOPLE / cols);
      /* шаг одинаковый по вертикали и горизонтали: сетка не растягивается */
      var step = Math.min((W - padX * 2) / cols, (H - padTop - padBot) / rows);
      var gw = step * cols, gh = step * rows;
      var x0 = (W - gw) / 2 + step / 2, y0 = padTop + (H - padTop - padBot - gh) / 2 + step / 2;
      var lit = 0;
      for (i = 0; i < PEOPLE; i++) {
        var cx = x0 + (i % cols) * step, cy = y0 + Math.floor(i / cols) * step;
        var on = day >= joinDay(i) && i < FINAL + 1;
        if (on) lit++;
        var r = Math.min(6, step * .2);
        if (on) {
          var glow = ctx.createRadialGradient(cx, cy, 0, cx, cy, r * 3.4);
          glow.addColorStop(0, 'rgba(' + PH + ',.3)'); glow.addColorStop(1, 'rgba(' + PH + ',0)');
          ctx.fillStyle = glow; ctx.beginPath(); ctx.arc(cx, cy, r * 3.4, 0, 7); ctx.fill();
        }
        ctx.beginPath(); ctx.arc(cx, cy, on ? r : r * .72, 0, 7);
        ctx.fillStyle = on ? 'rgba(' + PH + ',.9)' : 'rgba(' + GR + ',.28)';
        ctx.fill();
      }
      ctx.textAlign = 'left'; ctx.fillStyle = 'rgba(' + GR + ',.8)';
      cap(ctx, 'день ' + Math.max(1, Math.min(DAYS, day)) + ' из ' + DAYS, padX, 16, W * .42, 10.5);
      ctx.textAlign = 'right'; ctx.fillStyle = 'rgba(' + PH + ',.9)';
      cap(ctx, lit + ' из ' + PEOPLE + ' работают с AI', W - padX, 16, W * .52, 10.5);
      ctx.textAlign = 'left';
    }, function () { return innerWidth < 700 ? 1.15 : 1.6; });
  });

  [].forEach.call(document.querySelectorAll('canvas.fx-mesh'), function (c) {
    var nodes = [], links = [];
    var st = loop(c, function (s, t) {
      var ctx = s.ctx, W = s.W, H = s.H;
      ctx.clearRect(0, 0, W, H);
      var tt = t * .012, front = ((t * 1.6) % (W + 420)) - 210;
      links.forEach(function (L) {
        var mx = (L[0].x + L[1].x) / 2, near = Math.max(0, 1 - Math.abs(mx - front) / 190);
        ctx.beginPath(); ctx.moveTo(L[0].x, L[0].y); ctx.lineTo(L[1].x, L[1].y);
        ctx.strokeStyle = near > .35 ? 'rgba(' + PH + ',' + (.08 + near * .3) + ')' : 'rgba(' + GR + ',' + (.09 + near * .12) + ')';
        ctx.lineWidth = .7 + near * .9; ctx.stroke();
      });
      nodes.forEach(function (n) {
        var near = Math.max(0, 1 - Math.abs(n.x - front) / 170), br = .55 + .45 * Math.sin(tt + n.ph);
        ctx.beginPath(); ctx.arc(n.x, n.y, 1.5 + near * 2 + (n.hot ? .8 : 0), 0, 7);
        ctx.fillStyle = (n.hot || near > .6) ? 'rgba(' + PH + ',' + ((n.hot ? .8 : .34) * br + near * .4) + ')'
                                             : 'rgba(' + WH + ',' + (.18 + near * .35) * br + ')';
        ctx.fill();
      });
    }, function () { return innerWidth < 700 ? 2.6 : 5.4; });
    st.onbuild = function () {
      var W = st.W, H = st.H, step = innerWidth < 700 ? 30 : 36;
      nodes = []; links = [];
      var cols = Math.ceil(W / step) + 1, rows = Math.ceil(H / step) + 1;
      for (var j = 0; j < rows; j++) for (var i = 0; i < cols; i++) {
        var k = j * cols + i;
        nodes.push({x: i * step + (rnd(k) - .5) * step * .55, y: j * step + (rnd(k + 77) - .5) * step * .55,
          i: i, j: j, hot: rnd(k + 300) > .88, ph: rnd(k + 5) * 6.28});
      }
      nodes.forEach(function (a) { nodes.forEach(function (b) {
        if (b.j < a.j || (b.j === a.j && b.i <= a.i)) return;
        if (Math.abs(a.i - b.i) > 1 || Math.abs(a.j - b.j) > 1) return;
        if (rnd(a.i * 13 + a.j * 29 + b.i * 7 + b.j * 3) > .62) return;
        links.push([a, b]);
      }); });
    };
    st.onbuild(); st.rebuild();
  });
})();
'''


def E(s):
    """Экранируем текст, но не ломаем уже готовые сущности вроде &nbsp;"""
    return re.sub(r"&amp;(nbsp|thinsp|mdash|ndash|laquo|raquo|#\d+);", r"&\1;",
                  html.escape(str(s), quote=False))
def bold(s):
    s = E(s)
    while "**" in s:
        s = s.replace("**", "<b>", 1).replace("**", "</b>", 1)
    return s


# ---------- ритм секций: лестница отступов вместо одинаковых 96px ----------
LADDER = [4, 8, 12, 16, 20, 24, 28, 32, 40, 48, 56, 64, 72, 80, 96, 120, 140, 160]

BASE_RHYTHM = {
    "stmt":    (130, 150),   # одна мысль, короткий текст
    "dom":     (120, 140),   # доминанта
    "fig":     (64, 130),    # схема во всю ширину
    "vs":      (64, 64),     # список или строки
    "arte":    (72, 96),     # три артефакта
    "contour": (80, 96),     # рамка контура компании
    "bignum":  (64, 64),     # строка метрик
    "steps":   (72, 96),     # плотный контент
    "bento":   (72, 96),
    "compare": (72, 96),
    "ba":      (72, 96),
    "case":    (72, 96),
    "cost":    (72, 96),
    "cta":     (96, 120),    # призыв и форма
}
PRE_CTA = (140, 96)


def _down(v):
    if v in LADDER:
        return LADDER[max(0, LADDER.index(v) - 1)]
    # значение вне лестницы: берём ближайшую ступень ниже
    lower = [x for x in LADDER if x < v]
    return lower[-1] if lower else LADDER[0]


def _mob(v):
    if v <= 64:
        return v
    return min(LADDER, key=lambda x: abs(x - v / 1.5))


def assign_rhythm(secs):
    """Проставляет каждой секции свой вертикальный ритм и следит,
    чтобы у соседних секций отступы не совпадали."""
    pairs = []
    for i, s in enumerate(secs):
        if s["type"] == "cover":
            pairs.append(None)
            continue
        p = list(BASE_RHYTHM.get(s["type"], (72, 96)))
        if i + 1 < len(secs) and secs[i + 1]["type"] == "cta":
            p = list(PRE_CTA)
        pairs.append(p)
    for i in range(1, len(pairs)):
        if pairs[i] is None or pairs[i - 1] is None:
            continue
        guard = 0
        while pairs[i] == pairs[i - 1] and guard < 5:
            pairs[i] = [_down(pairs[i][0]), _down(pairs[i][1])]
            guard += 1
    mobs = [None if p is None else [_mob(p[0]), _mob(p[1])] for p in pairs]
    for i in range(1, len(mobs)):
        if mobs[i] is None or mobs[i - 1] is None:
            continue
        guard = 0
        while mobs[i] == mobs[i - 1] and guard < 5:
            mobs[i] = [_down(mobs[i][0]), _down(mobs[i][1])]
            guard += 1
    used = set()
    for s, p, m in zip(secs, pairs, mobs):
        if p is None:
            s["_rc"] = "r-cover"
            continue
        s["_rc"] = "r%d-%d-%d-%d" % (p[0], p[1], m[0], m[1])
        used.add((p[0], p[1], m[0], m[1]))
    return used


def rhythm_css(used):
    base = "".join(".r%d-%d-%d-%d{padding:%dpx 0 %dpx}" % (t, b, mt, mb, t, b) for t, b, mt, mb in sorted(used))
    mob = "".join(".r%d-%d-%d-%d{padding:%dpx 0 %dpx}" % (t, b, mt, mb, mt, mb) for t, b, mt, mb in sorted(used))
    return base + "@media(max-width:720px){" + mob + "}"


# ---------- секции ----------

def nav_from_sections(spec):
    """Меню страницы ведёт на её же разделы: подписи берём из кикеров."""
    out = []
    for sec in spec["sections"]:
        sid = sec.get("id")
        eb = sec.get("eyebrow") or ""
        if not sid or not eb:
            continue
        label = re.sub(r"<[^>]+>", "", eb).strip()
        label = re.sub(r"^\d+\s*", "", label).strip()
        if not label:
            continue
        out.append(f'<a href="#{sid}">{label}</a>')
    out.append('<a href="#cta">Заявка</a>')
    # меню отдаём целиком: хвост с условиями и заявкой терять нельзя
    return "".join(out)


_N_RE = re.compile(r'<span class="n">[^<]*</span>')


def renumber(spec):
    """Сквозная нумерация разделов: 01, 02, 03 подряд, у блока ссылок следующий номер."""
    n = 0
    for sec in spec["sections"]:
        if sec["type"] == "cover":
            continue
        eb = sec.get("eyebrow")
        if not eb:
            continue
        n += 1
        num = f"{n:02d}"
        if _N_RE.search(eb):
            sec["eyebrow"] = _N_RE.sub(f'<span class="n">{num}</span>', eb, count=1)
        else:
            m = re.match(r"^\s*\d+\s+(.*)$", eb)
            sec["eyebrow"] = f'<span class="n">{num}</span> ' + (m.group(1) if m else eb)
    spec["relnum"] = f"{n + 1:02d}"

def sec_cover(s):
    cta = "".join(f'<a class="btn {"pri" if b.get("pri") else "ghost"} lg" href="{b["href"]}">{E(b["label"])}</a>'
                  for b in s.get("cta", []))
    chip = f'<div class="chip reveal">{E(s["chip"])}</div>' if s.get("chip") else ""
    lead = f'<p class="lead reveal d2">{E(s["lead"])}</p>' if s.get("lead") else ""
    ctahtml = f'<div class="cover-cta reveal d3">{cta}</div>' if cta else ""
    dom = ""
    if s.get("dom"):
        d = s["dom"]
        sub = f'<span class="cd-sub">{E(d["sub"])}</span>' if d.get("sub") else ""
        dom = (f'<div class="cover-dom reveal d2"><div class="cd-num">{E(d["n"])}{sub}</div>'
               f'<div class="cd-cap">{E(d["cap"])}</div></div>')
    stats_cls = ""
    if s.get("stats"):
        st = s["stats"]
        # цифры идут одинаковым кеглем: ни одна не важнее другой
        def _num(v):
            # предлог «от» набираем мельче суммы, единицу измерения тоже мельче,
            # в паре «26 из 27» главная цифра крупная, остаток доли мельче
            pre = ""
            m = re.match(r"^(от|до|с)\s+(.+)$", v)
            if m:
                pre = f'<span class="cs-pre">{m.group(1)}</span> '
                v = m.group(2)
            m = re.match(r"^([0-9][^\s]*)\s+(из\s+[0-9].*)$", v)
            if m:
                return f'{pre}{m.group(1)}<span class="cs-of">{m.group(2)}</span>'
            m = re.match(r"^([0-9][^\s]*)\s+(.+)$", v)
            if m and not re.search(r"\d", m.group(2)):
                return f'{pre}{m.group(1)} <span class="cs-u">{m.group(2)}</span>'
            return pre + v
        cells = "".join(f'<div class="cs"><div class="cs-n">{_num(it["n"])}</div>'
                        f'<div class="cs-c">{it["cap"]}</div></div>' for it in st["items"])
        lk = st.get("link")
        if lk:
            cells += (f'<a class="cs cs-link" href="{lk["href"]}" target="_blank" rel="noopener">'
                      f'<span class="cs-k">{lk["k"]}</span>'
                      f'<span class="cs-b">{E(lk["label"])}</span></a>')
        dom = f'<div class="cover-stats reveal d2">{cells}</div>'
        stats_cls = " stats"
    if s.get("stats_bottom"):
        stats_cls += " sbottom"
    grid_open = f'<div class="cover-grid{stats_cls}">' if dom else ""
    cta_side = ""
    if dom and ctahtml:
        # кнопка уже стоит в шапке, на обложке её не дублируем
        ctahtml = ""
    grid_close = "</div>" if dom else ""
    return f'''<header class="cover r-cover"><canvas id="synFx" data-fx="{s.get("fx","converge")}"></canvas><div class="wrap">
  {grid_open}<div>
  <div class="cover-kick reveal">{chip}<div class="eyebrow">{s["eyebrow"]}</div></div>
  <h1 class="reveal d1">{f'<a class="h1-link" href="{s["h1_link"]}">{E(s["h1"])}</a>' if s.get("h1_link") else E(s["h1"])}</h1>
  {lead}
  {ctahtml}
  </div>{dom}{cta_side}{grid_close}
</div></header>'''


def sec_stmt(s):
    eb = f'<div class="eyebrow reveal">{s["eyebrow"]}</div>' if s.get("eyebrow") else ""
    return (f'<section id="{s.get("id","")}" class="{s.get("_rc","")}"><div class="wrap">{eb}'
            f'<div class="stmt reveal"><p>{bold(s["text"])}</p></div></div></section>')


def sec_dom(s):
    """Доминанта: одно проверяемое число, выходящее за правый край сетки."""
    eb = f'<div class="eyebrow reveal">{s["eyebrow"]}</div>' if s.get("eyebrow") else ""
    return f'''<section id="{s.get("id","")}" class="{s.get("_rc","")}"><div class="wrap">{eb}
  <div class="dom reveal">
    <p class="dom-txt">{bold(s["text"])}</p>
    <div class="dom-fig"><div class="dom-num">{E(s["num"])}</div><div class="dom-cap">{E(s["cap"])}</div></div>
  </div>
</div></section>'''


def sec_head(s):
    lead = f'<p class="lead">{E(s["lead"])}</p>' if s.get("lead") else ""
    return f'<div class="sec-head reveal"><div class="eyebrow">{s["eyebrow"]}</div><h2>{E(s["heading"])}</h2>{lead}</div>'


def sec_vs(s):
    """До и после одной шкалой: слева нынешний порядок, справа то, что меняется."""
    cards = ""
    for i, c in enumerate(s["cards"]):
        hot = " hot" if c.get("hot") else ""
        cards += (f'<div class="vrow{hot} reveal {("d%d" % i) if i else ""}">'
                  f'<span class="v-mark" aria-hidden="true"></span>'
                  f'<div class="v-body"><span class="k">{E(c["k"])}</span><p>{E(c["p"])}</p></div></div>')
    return (f'<section id="{s.get("id","")}" class="{s.get("_rc","")}"><div class="wrap">{sec_head(s)}'
            f'<div class="vs-line">{cards}</div></div></section>')


def sec_arte(s):
    """Три артефакта: равные плитки с крупным индексом и реакцией на наведение."""
    cards = "".join(
        f'<div class="art reveal {("d%d" % i) if i else ""}">'
        f'<div class="art-top"><span class="art-k">{E(c["k"])}</span>'
        f'<span class="art-i">{i + 1:02d}</span></div>'
        f'<span class="art-line"></span><p>{E(c["p"])}</p></div>'
        for i, c in enumerate(s["cards"]))
    return (f'<section id="{s.get("id","")}" class="{s.get("_rc","")}"><div class="wrap">{sec_head(s)}'
            f'<div class="arte">{cards}</div></div></section>')


def sec_contour(s):
    """Безопасность: рамка контура компании, внутри строки-правила, снаружи подпись."""
    rows = "".join(
        f'<div class="ct-row"><span class="ct-i">{i + 1:02d}</span>'
        f'<span class="ct-k">{E(c["k"])}</span><p>{E(c["p"])}</p></div>'
        for i, c in enumerate(s["cards"]))
    out = f'<div class="ct-out"><span>{E(s.get("out", "наружу не уходит"))}</span></div>' if s.get("out") else ""
    return (f'<section id="{s.get("id","")}" class="{s.get("_rc","")}"><div class="wrap">{sec_head(s)}'
            f'<div class="contour reveal"><div class="ct-frame">'
            f'<span class="ct-badge">{E(s.get("badge", "контур компании"))}</span>{rows}</div>{out}</div>'
            f'</div></section>')


def sec_steps(s):
    items = "".join(
        f'<div class="mstep reveal {("d%d" % i) if i else ""}"><div class="top">'
        f'<span class="num">{E(it["num"])}</span><span class="wk">{E(it["tag"])}</span></div>'
        f'<h3>{E(it["h"])}</h3><p>{E(it["p"])}</p></div>'
        for i, it in enumerate(s["items"]))
    return (f'<section id="{s.get("id","")}" class="{s.get("_rc","")}"><div class="wrap">{sec_head(s)}'
            f'<div class="month">{items}</div></div></section>')


def sec_compare(s):
    head = (f'<div class="crow head"><div class="task">{E(s["head"][0])}</div>'
            f'<div class="was">{E(s["head"][1])}</div><div class="now">{E(s["head"][2])}</div></div>')
    rows = "".join(f'<div class="crow"><div class="task">{E(r[0])}</div><div class="was">{E(r[1])}</div>'
                   f'<div class="now">{bold(r[2])}</div></div>' for r in s["rows"])
    link = (f'<div class="step-link reveal"><span class="sl-rule"></span>'
            f'<span>{E(s["link"])}</span></div>') if s.get("link") else ""
    note = ""
    if s.get("note"):
        note = ('<div class="upsell note reveal d1"><div class="ic">'
                '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">'
                '<circle cx="12" cy="12" r="9"/><path d="M12 11v6"/><path d="M12 7.6v.6"/></svg></div>'
                f'<div><h4>{E(s["note"]["h"])}</h4><p>{E(s["note"]["p"])}</p></div></div>')
    return (f'<section id="{s.get("id","")}" class="{s.get("_rc","")}"><div class="wrap">{sec_head(s)}'
            f'<div class="compare reveal">{head}{rows}</div>{note}{link}</div></section>')


def sec_shift(s):
    """Что меняется: каждая задача отдельным блоком, слева «до», справа «после».
    Подача намеренно не похожа на блок ссылок: широкие строки, а не плитки."""
    rows = ""
    for i, r in enumerate(s["rows"]):
        rows += (f'<article class="sh reveal {("d%d" % min(i, 2)) if i else ""}">'
                 f'<div class="sh-top"><span class="sh-i">{i + 1:02d}</span>'
                 f'<h3>{E(r["task"])}</h3></div>'
                 f'<div class="sh-pair">'
                 f'<div class="sh-c was"><span class="sh-k">до</span><p>{bold(r["was"])}</p></div>'
                 f'<div class="sh-c now"><span class="sh-k">после</span><p>{bold(r["now"])}</p></div>'
                 f'</div></article>')
    n = s.get("note") or s.get("upsell")
    note = ""
    if n:
        note = ('<div class="upsell note reveal d1"><div class="ic">'
                '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">'
                '<circle cx="12" cy="12" r="9"/><path d="M12 11v6"/><path d="M12 7.6v.6"/></svg></div>'
                f'<div><h4>{E(n["h"])}</h4><p>{E(n["p"])}</p></div></div>')
    link = (f'<div class="step-link reveal"><span class="sl-rule"></span>'
            f'<span>{E(s["link"])}</span></div>') if s.get("link") else ""
    return (f'<section id="{s.get("id","")}" class="{s.get("_rc","")}"><div class="wrap">{sec_head(s)}'
            f'<div class="shift">{rows}</div>{note}{link}</div></section>')


def sec_ba(s):
    cols = ""
    for c in s["cols"]:
        lis = "".join(f'<li><span class="t">{E(x["t"])}</span><span>{E(x["text"])}</span></li>' for x in c["items"])
        cls = "now" if c.get("now") else "was"
        ul = (f'<ul class="{"ba now2" if c.get("now") else ""}" '
              f'style="list-style:none;display:flex;flex-direction:column;gap:14px">{lis}</ul>')
        cols += f'<div class="col {cls}"><div class="lab">{E(c["lab"])}</div>{ul}</div>'
    return (f'<section id="{s.get("id","")}" class="{s.get("_rc","")}"><div class="wrap">{sec_head(s)}'
            f'<div class="ba reveal">{cols}</div></div></section>')


def sec_case(s):
    ms = "".join(f'<div class="metric"><b>{E(m["b"])}</b><span>{E(m["span"])}</span></div>' for m in s["metrics"])
    sub = f'<div class="sub">{E(s["sub"])}</div>' if s.get("sub") else ""
    lead = f'<p class="lead" style="margin-bottom:32px">{E(s["lead"])}</p>' if s.get("lead") else ""
    eb = f'<div class="eyebrow reveal">{s["eyebrow"]}</div>' if s.get("eyebrow") else ""
    tag = f'<span class="tag">{E(s["tag"])}</span>' if s.get("tag") else ""
    # кнопка стоит четвёртой ячейкой в сетке цифр: 2+1 и «Подробнее»
    if s.get("more"):
        ms += (f'<a class="metric metric-more" href="{s["more"]["href"]}">'
               f'<span class="mm-t">{E(s["more"]["label"])}</span>'
               f'<span class="mm-r" aria-hidden="true"></span></a>')
    return f'''<section id="{s.get("id","")}" class="{s.get("_rc","")}"><div class="wrap">{eb}
  <div class="case reveal case-split"><div class="cs-txt"><div class="ch">{tag}</div><h3>{E(s["h3"])}</h3>{sub}{lead}</div><div class="metrics quad">{ms}</div></div>
</div></section>'''


def sec_bignum(s):
    cells = "".join(f'<div class="bn"><b>{E(m["b"])}</b><span class="cap">{E(m["cap"])}</span></div>'
                    for m in s["items"])
    # split: две цифры друг под другом слева, третья по центру второй колонки
    split = " split" if s.get("split") else ""
    return (f'<section id="{s.get("id","")}" class="{s.get("_rc","")}"><div class="wrap">{sec_head(s)}'
            f'<div class="bignum{split} reveal">{cells}</div></div></section>')


def sec_fig(s):
    """Единственный full-bleed блок материала: графика связей во всю ширину экрана."""
    kind = s.get("kind", "mesh")
    attrs = ""
    if s.get("layers"): attrs += f' data-layers="{E(s["layers"])}"'
    for k in ("people","days","final"):
        if s.get(k): attrs += f' data-{k}="{s[k]}"'
    if s.get("chat"): attrs += f' data-chat="{E(s["chat"])}"'
    if s.get("a"): attrs += f' data-a="{E(s["a"])}"'
    if s.get("b"): attrs += f' data-b="{E(s["b"])}"'
    cap = f'<div class="wrap"><div class="figcap">{E(s["cap"])}</div></div>' if s.get("cap") else ""
    head = f'<div class="wrap">{sec_head(s)}</div>' if s.get("heading") else ""
    if s.get("side"):
        capt = f'<div class="fig-txt">{E(s["cap"])}</div>' if s.get("cap") else ""
        flip = " flip" if s.get("flip") else ""
        flip += " card" if s.get("card") else ""
        flip += " big" if s.get("big") else ""
        return f'''<section id="{s.get("id","")}" class="{s.get("_rc","")}"><div class="wrap">{sec_head(s) if s.get("heading") else ""}
  <div class="fig-side reveal{flip}"><div class="figbox"><canvas class="fx-{kind}"{attrs}></canvas></div>{capt}</div>
</div></section>'''
    return f'''<section id="{s.get("id","")}" class="{s.get("_rc","")}">{head}
  <div class="figbox bleed reveal"><canvas class="fx-{kind}"{attrs}></canvas></div>{cap}
</section>'''


def sec_cost(s):
    p = s["price"]
    # предлог набираем мельче суммы, иначе «от» спорит с цифрой
    _big = E(p["big"])
    big_html = re.sub(r"^(от|до)\s+", lambda m: f'<span class="pre">{m.group(1)}</span> ', _big)
    incl = ""
    for col in s["incl"]:
        lis = "".join(f'<li><span class="ix">{i + 1:02d}</span><span>{E(x)}</span></li>'
                      for i, x in enumerate(col["items"]))
        incl += f'<div class="icol"><div class="k">{E(col["k"])}</div><ul>{lis}</ul></div>'
    up = ""
    if s.get("upsell"):
        up = ('<div class="upsell reveal d1"><div class="ic">'
              '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">'
              '<path d="M13 2L3 14h7l-1 8 10-12h-7z"/></svg></div>'
              f'<div><h4>{E(s["upsell"]["h"])}</h4><p>{E(s["upsell"]["p"])}</p></div></div>')
    start = (f'<div class="start"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             f'stroke-width="1.8"><path d="M12 6v6l4 2"/><circle cx="12" cy="12" r="9"/></svg> '
             f'{E(p["start"])}</div>') if p.get("start") else ""
    # заголовок стоит узкой колонкой и ложится в две строки, цена идёт во второй колонке
    lead = f'<p class="lead">{E(s["lead"])}</p>' if s.get("lead") else ""
    head = (f'<div class="cost-head reveal"><div class="eyebrow">{s["eyebrow"]}</div>'
            f'<h2>{E(s["heading"])}</h2>{lead}</div>')
    return f'''<section id="{s.get("id","")}" class="{s.get("_rc","")}"><div class="wrap">
  <div class="cost-top">{head}
  <div class="price-line reveal">
    <div class="big">{big_html} <small>{E(p["small"])}</small></div>
    <div class="pl-side"><div class="desc">{E(p["desc"])}</div>{start}</div>
  </div></div>
  <div class="incl reveal d1">{incl}</div>{up}
</div></section>'''


def sec_bento(s):
    cards = ""
    for it in s["items"]:
        num = f'<div class="bnum">{E(it["num"])}</div>' if it.get("num") else ""
        h = f'<h3>{E(it["h"])}</h3>' if it.get("h") else ""
        pp = f'<p>{E(it["p"])}</p>' if it.get("p") else ""
        k = f'<span class="bk">{E(it["k"])}</span>' if it.get("k") else ""
        cards += f'<div class="b">{k}<div>{num}{h}{pp}</div></div>'
    return (f'<section id="{s.get("id","")}" class="{s.get("_rc","")}"><div class="wrap">{sec_head(s)}'
            f'<div class="bento reveal">{cards}</div></div></section>')


def sec_cta(s):
    """Заявка: слева заголовок и менеджер, справа форма. Раскладка повторяет главную."""
    eb = f'<div class="eyebrow">{s["eyebrow"]}</div>' if s.get("eyebrow") else ""
    fm = s.get("form") or {}
    # форма одинаковая на всех материалах: подпись поля и кнопка не расходятся
    task_lbl = fm.get("task", "Коротко о&nbsp;контексте: что за&nbsp;задача и&nbsp;к&nbsp;какому результату хотите прийти")
    btn_lbl = fm.get("btn", "Оставить заявку")
    return (f'<section id="cta" class="{s.get("_rc","")}"><div class="wrap">'
            '<div class="lead-grid">'
            f'<div class="lead-copy reveal">{eb}'
            f'<h2>{E(s["heading"])}</h2><p class="lead">{s["p"]}</p>'
            '</div>'
            '<div class="leadbox reveal">'
            '<form class="mform" novalidate>'
            '<div class="lf-row">'
            '<div class="lf"><label>Как вас зовут <span class="req" title="обязательное поле">*</span></label>'
            '<input type="text" name="name" autocomplete="name" required></div>'
            '<div class="lf"><label>Телефон, почта или Telegram <span class="req" title="обязательное поле">*</span></label>'
            '<input type="text" name="contact" required></div>'
            '</div>'
            '<div class="lf"><label>Компания и сфера деятельности</label><input type="text" name="company"></div>'
            f'<div class="lf lf-task"><label>{task_lbl}</label><textarea name="task" rows="2"></textarea></div>'
            '<div class="slots" id="slots">'
            '<div class="sl-h">Когда вам удобно</div>'
            '<div class="sl-days" id="slDays"></div>'
            '<div class="sl-slots" id="slSlots"></div>'
            '<input type="hidden" id="lfSlot" name="slot">'
            '<div class="sl-note" id="slNote"></div></div>'
            '<label class="lf-check"><input type="checkbox" required>'
            '<span>Согласен на обработку персональных данных и принимаю '
            '<a href="/privacy" target="_blank">политику обработки персональных данных</a></span></label>'
            '<div class="mf-err">Не хватает вашего имени, контактов и согласия на обработку персональных данных</div>'
            f'<button class="btn pri lg" type="submit">{E(btn_lbl)}</button>'
            '<p class="lf-after">Подтвердим встречу в&nbsp;ответном сообщении в&nbsp;течение <span class="nb">1</span>&nbsp;рабочего дня</p>'
            '<div class="mf-ok"><b>Спасибо!</b> Получили заявку и свяжемся в рабочее время</div>'
            '<div class="mf-fail"><b>Заявка не ушла.</b> Напишите Никите в Telegram '
            '<a href="https://t.me/Anti4ay">@Anti4ay</a>, он примет заявку</div>'
            '</form>'
            '</div>'
            # блок про менеджера стоит после формы: сначала действие, потом кто ответит
            '<div class="lc-mgr after reveal">'
            f'<img class="lc-ava" src="data:image/jpeg;base64,{AVA}" alt="Никита, project manager студии" '
            'width="52" height="52" loading="lazy">'
            '<div class="lc-mgr-t">'
            '<b><span class="mgr-name">Никита</span>&nbsp;– project manager студии, '
            '<a href="https://t.me/Anti4ay" target="_blank" rel="noopener">@Anti4ay</a></b>'
            # на экране запись идёт через форму, в PDF формы нет – там та же мысль, но про прямое сообщение
            '<span class="mgr-web">На&nbsp;запись по&nbsp;форме ответим в&nbsp;течение <span class="nb">1</span>&nbsp;рабочего дня, '
            'а&nbsp;если задача срочная и&nbsp;нужен ещё более быстрый ответ, напишите нам напрямую</span>'
            '<span class="mgr-pdf" style="display:none">Напишите нам напрямую, ответим в&nbsp;течение '
            '<span class="nb">1</span>&nbsp;рабочего дня. Все контакты собраны ниже</span>'
            '</div></div>'
            '</div>'
            '</div></section>')


RENDER = {"cover": sec_cover, "stmt": sec_stmt, "dom": sec_dom, "vs": sec_vs, "steps": sec_steps,
          "compare": sec_compare, "ba": sec_ba, "case": sec_case, "bignum": sec_bignum,
          "fig": sec_fig, "cost": sec_cost, "bento": sec_bento, "cta": sec_cta,
          "arte": sec_arte, "contour": sec_contour, "shift": sec_shift}

# плавающая пара внизу справа: та же, что на главной, и на той же правой линии
FAB = ('<div class="fab" aria-hidden="false">'
       '<a class="fab-b fab-tg" href="https://t.me/Anti4ay" target="_blank" rel="noopener" '
       'aria-label="Написать в&nbsp;Telegram" title="Написать в&nbsp;Telegram">'
       '<svg viewBox="0 0 24 24" fill="currentColor" width="19" height="19">'
       '<path d="M21.9 4.3 18.9 19c-.2 1-.8 1.2-1.7.8l-4.6-3.4-2.2 2.1c-.3.3-.5.5-1 .5l.3-4.7L18.3 6c.4-.3-.1-.5-.6-.2L7.2 12.4l-4.5-1.4c-1-.3-1-1 .2-1.4l17.6-6.8c.8-.3 1.5.2 1.4 1.5z"/></svg></a>'
       '<a class="fab-b fab-lead" href="#cta" aria-label="Оставить заявку" title="Оставить заявку">'
       '<svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20" aria-hidden="true">'
       '<path d="M3.4 6.2 12 12.1l8.6-5.9c-.3-.7-1-1.1-1.8-1.1H5.2c-.8 0-1.5.4-1.8 1.1zM21 8.1l-8.4 5.8c-.4.3-.9.3-1.2 0L3 8.1v9c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2z"/></svg>'
       '<span>Оставить заявку</span></a>'
       '</div>')

SITE = "https://synapt-site.vercel.app"
LINKS = {
  "ai-desant":     {"t": "AI-десант", "u": "https://synapt-ai-desant.vercel.app", "k": "услуга"},
  "bezopasnost":   {"t": "Безопасный слой", "u": "https://synapt-bezopasnost.vercel.app", "k": "блок системы"},
  "otdel-prodazh": {"t": "AI-продавец в переписке", "u": "https://synapt-otdel-prodazh.vercel.app", "k": "блок системы"},
  "globaldent":    {"t": "GlobalDent", "u": "https://synapt-globaldent.vercel.app", "k": "кейс"},
  "innorto":       {"t": "INNORTO", "u": "https://synapt-innorto.vercel.app", "k": "кейс"},
  "checkup":       {"t": "AI-чекап бизнеса", "u": "https://synapt-checkup.vercel.app", "k": "услуга"},
  "automy":        {"t": "Automy AI", "u": "https://automyai.ru", "k": "обучение"},
}

# в блоке остаются только живые страницы: четыре соседние плюс обучение Automy AI
REL_KEYS = ["ai-desant", "bezopasnost", "checkup", "innorto", "globaldent", "automy"]


def sec_related(cur, num):
    """Четыре соседние страницы и обучение: отдельные карточки, общей рамки нет"""
    items = [LINKS[k] for k in REL_KEYS if k != cur and k in LINKS]
    order = {"услуга": 0, "блок системы": 1, "кейс": 2, "обучение": 3}
    items.sort(key=lambda v: (order.get(v["k"], 9), v["t"]))
    num = f"{int(num):02d}" if str(num).strip().isdigit() else num
    cards = "".join(
        f'<a class="rel-card" href="{v["u"]}"><span class="rel-k">{v["k"]}</span>'
        f'<span class="rel-t">{E(v["t"])}</span></a>' for v in items)
    return (f'<section id="related" class="r72-96-48-64"><div class="wrap">'
            f'<div class="rel-head reveal">'
            f'<div class="eyebrow"><span class="n">{E(num)}</span> Другие услуги и&nbsp;кейсы студии</div>'
            f'</div>'
            f'<div class="rel-grid split reveal">{cards}</div>'
            f'</div></section>')



# адрес страницы материала: нужен для превью в мессенджерах и канонической ссылки
DOMAINS = {
    "innorto": "https://synapt-innorto.vercel.app",
    "globaldent": "https://synapt-globaldent.vercel.app",
    "bezopasnost": "https://synapt-bezopasnost.vercel.app",
    "ai-desant": "https://synapt-ai-desant.vercel.app",
    "otdel-prodazh": "https://synapt-otdel-prodazh.vercel.app",
}

def render(spec, slug=""):
    renumber(spec)
    secs = spec["sections"]
    nav_links = nav_from_sections(spec)
    nav_cta = spec.get("nav_cta", "Оставить заявку")
    # в подвале те же разделы, что и в шапке: ссылки ведут по своей странице
    foot_links = nav_links
    cta_cls = ""
    used = assign_rhythm(secs)
    used.add((72, 96, 48, 64))
    body = "".join(RENDER[s["type"]](s) for s in secs)
    foot_meta = "".join(f'<span>{E(x)}</span>' if not x.startswith("http")
                        else f'<a href="{x}">{E(x.replace("https://", ""))}</a>' for x in spec.get("footer", []))
    # страница политики лежит рядом с каждой сборкой, но без ссылки она сирота
    foot_meta += '<a href="/privacy">Политика обработки персональных данных</a>'
    page_url = DOMAINS.get(slug, SITE)
    # в PDF формы нет, поэтому контакты уходят строкой ссылок: адрес страницы, Telegram, сайт студии
    pcontacts = (
        '<section class="pc-sec" style="display:none"><div class="wrap">'
        '<div class="pcontacts">'
        '<div class="pc-k">контакты</div><div class="pc-row">'
        '<div class="pc-i"><span>Никита, project manager студии</span>'
        '<a href="https://t.me/Anti4ay">t.me/Anti4ay</a></div>'
        f'<div class="pc-i"><span>Эта страница в&nbsp;вебе</span>'
        f'<a href="{page_url}">{E(page_url.replace("https://", ""))}</a></div>'
        f'<div class="pc-i"><span>Все услуги и&nbsp;кейсы студии</span>'
        f'<a href="{SITE}">{E(SITE.replace("https://", ""))}</a></div>'
        '<div class="pc-i"><span>Обработка персональных данных</span>'
        f'<a href="{page_url}/privacy">{E(page_url.replace("https://", ""))}/privacy</a></div>'
        '</div></div></div></section>')
    return f'''<!doctype html>
<html lang="ru" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Synapt – {E(spec["title"])}</title>
<meta name="description" content="{E(spec.get("lead", spec["title"]))}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Synapt">
<meta property="og:title" content="Synapt – {E(spec["title"])}">
<meta property="og:description" content="{E(spec.get("lead", spec["title"]))}">
<meta property="og:url" content="{DOMAINS.get(slug, "https://synapt-site.vercel.app")}">
<meta property="og:image" content="{DOMAINS.get(slug, "https://synapt-site.vercel.app")}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Synapt – {E(spec["title"])}">
<meta name="twitter:image" content="{DOMAINS.get(slug, "https://synapt-site.vercel.app")}/og.png">
<link rel="canonical" href="{DOMAINS.get(slug, "https://synapt-site.vercel.app")}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@200..800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}
{rhythm_css(used)}
/* ссылка на политику: текст спокойный, акцент только в полоске */
.lf-check a,.agree a{{color:var(--text-muted)!important;border-bottom-color:var(--line-accent)!important}}
.lf-check a:hover,.agree a:hover{{color:var(--text)!important;border-bottom-color:var(--accent)!important}}

/* чипы: моно без разрядки */
.chip,.hero-chip,.cc-tag,.rel-k{{letter-spacing:.02em!important}}

/* обложка: анимация и текст центрируются друг относительно друга */
.cover .cover-grid{{align-items:center}}
.cover-stats{{align-self:center}}
/* схема и подпись стоят выше, вплотную к заголовку блока */
.fig-side.big{{align-items:start}}
.fig-side.big .figbox{{margin-top:0}}
.fig-side.big .fig-txt{{padding-top:0;margin-top:0}}
#spread .sec-head,#teams .sec-head{{margin-bottom:22px}}
/* блок итоговых цифр закрывается такой же линией, как открывается */
#metrics .bignum{{border-bottom:1px solid var(--line-2)!important;padding-bottom:6px}}

/* согласие ближе к предыдущему блоку и на пару пикселей выше */
.lf-check{{margin-top:-6px!important;padding-top:0!important}}
.lf-check input{{margin-top:0!important}}
.lf-check span{{padding-top:0}}
.mform .lf-check{{margin-top:-8px!important}}

.metric-more .mm-r{{display:none!important}}
.metric.metric-more{{align-self:center;gap:0}}

/* кейс: кнопка «Подробнее» рамкой, полоса под ней не тянется на всю ячейку */
.metric-more{{align-self:center}}
.metric-more .mm-t{{display:inline-flex;align-items:center;justify-content:center;min-height:44px;
  padding:0 22px;border:1px solid var(--line-accent);border-radius:var(--r-sm);font-size:15px}}
.metric-more .mm-r{{display:none}}
.metric-more:hover .mm-t{{border-color:var(--accent);color:var(--accent)}}
/* цифры кейса чуть спокойнее */
.case-split .metrics.quad .metric b{{font-size:clamp(24px,2.4vw,32px)}}

/* цифры обложки крупнее, подпись ближе, плашки под ними нет */
.cs{{background:transparent!important;backdrop-filter:blur(6px)!important;-webkit-backdrop-filter:blur(6px)!important}}
.cs-n{{font-size:clamp(38px,4.4vw,54px)!important;line-height:1}}
.cs-c{{margin-top:8px}}
.hs b{{font-size:clamp(30px,3.6vw,44px)!important;line-height:1}}
.hs span{{margin-top:8px}}

/* согласие: чекбокс одного размера и по верхней линии текста на всех страницах */
.lf-check{{align-items:flex-start!important}}
.lf-check input{{width:20px!important;height:20px!important;margin-top:2px!important;align-self:flex-start!important}}
.lf-check span{{padding-top:1px}}

/* форма материалов: единый шаг между блоками, как на главной */
.mform{{row-gap:18px!important}}
.mform .lf{{margin-bottom:0!important}}
.mform .slots{{margin-top:0!important}}
.mform .lf-after{{margin-top:0!important}}

.slots{{padding-top:0!important;border-top:0!important}}
.slots .sl-h{{margin-top:0!important}}
.lf-after{{margin-top:10px!important}}

/* крайние разделители списков: перед первым и после последнего линии нет */
.rule:first-child,.pr-row:first-child,.mstep:first-child,.step:first-child,
.zoom-row:first-child,.dayrow:first-child,.lstep:first-child{{border-top:0}}
.rule:last-child,.pr-row:last-child,.mstep:last-child,.step:last-child,
.zoom-row:last-child,.dayrow:last-child,.lstep:last-child,.faq details:last-child{{border-bottom:0}}

/* стоимость: заголовок слева и цена справа стоят на одной линии */
.cost-top{{align-items:start!important}}
.cost-head{{padding-top:0}}
.price-line{{margin-top:0!important}}
.price-line .big{{line-height:.92}}

/* итоговые цифры: карточками, две слева друг под другом, третья справа по центру */
.bignum{{border-top:0!important}}
.bignum.split{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}}
.bignum.split .bn{{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-lg);
  padding:22px 24px!important;border-left:0;border-top:0}}
.bignum.split .bn:nth-child(1){{grid-column:1;grid-row:1}}
.bignum.split .bn:nth-child(2){{grid-column:1;grid-row:2}}
.bignum.split .bn:nth-child(3){{grid-column:2;grid-row:1 / span 2;align-self:center}}
.bignum.split .bn .cap{{max-width:30ch}}
@media(max-width:760px){{
  .bignum.split{{grid-template-columns:1fr;gap:12px}}
  .bignum.split .bn,.bignum.split .bn:nth-child(1),.bignum.split .bn:nth-child(2),.bignum.split .bn:nth-child(3){{grid-column:1;grid-row:auto;align-self:auto}}
}}
/* крайние разделители в списках этапов не рисуем */
.zoom-list>*:first-child,.days>*:first-child,.steps-list>*:first-child,.rmap>*:first-child,.lad>*:first-child{{border-top:0}}
.zoom-list>*:last-child,.days>*:last-child,.steps-list>*:last-child,.rmap>*:last-child,.lad>*:last-child{{border-bottom:0}}

/* формы, финальная сверка: одинаковые интервалы и подчёркивание политики */
.lf{{margin-bottom:18px!important}}
.slots{{margin-top:14px!important}}
.lf-check input{{margin-top:2px!important}}
.lf-check a{{text-decoration:none!important;border-bottom:1px solid var(--line-accent)!important;padding-bottom:1px}}
.lf-after{{margin-top:10px!important}}

/* формы: единый вид на всех страницах */
.lf label,.f-l,.fld label{{font-family:var(--mono);font-size:11.5px;font-weight:500;letter-spacing:.06em;color:var(--text-muted)}}
.slots{{margin-top:14px!important}}
.lf-check,.agree{{align-items:flex-start}}
.lf-check input,.agree input{{margin-top:2px}}
.lf-check a,.agree a{{text-decoration:none;border-bottom:1px solid var(--line-accent);padding-bottom:1px}}
.lf-check a:hover,.agree a:hover{{border-bottom-color:var(--accent)}}
.lf-after{{margin-top:10px!important}}

/* чипы без разрядки: моно остаётся, межбуквенное как в обычном тексте */
.chip{{letter-spacing:.02em}}
/* цена: приставка и единица одного кегля, воздух между частями вдвое меньше */
.price-line .big{{display:inline-flex;align-items:baseline;gap:.16em;white-space:nowrap;word-spacing:normal}}
.price-line .big .pre,.price-line .big small{{font-size:.34em;letter-spacing:0;font-weight:500;color:var(--text-2)}}
.cost-top{{align-items:baseline}}
/* цифры обложки: приставка и единица прижаты к числу */
.cs-n{{display:inline-flex;align-items:baseline;gap:.14em;white-space:nowrap}}
.cs-n .cs-pre,.cs-n .cs-u{{font-size:.52em;margin-left:0;color:var(--text-2)}}
/* формы: подписи полей везде моно, согласие по верхней линии */
.lf label,.f-l,.fld label{{font-family:var(--mono);font-size:11.5px;font-weight:500;letter-spacing:.06em;color:var(--text-muted)}}
.lf-check,.agree{{align-items:flex-start}}
.lf-check input,.agree input{{margin-top:1px}}
.lf-check a,.agree a{{text-decoration:none;border-bottom:1px solid var(--line-accent);padding-bottom:1px}}
/* списки этапов: крайние разделители не рисуем */
.rmap-row:first-child,.lstep:first-child,.zoom-row:first-child,.days .d:first-child{{border-top:0}}
.rmap-row:last-child,.lstep:last-child,.zoom-row:last-child,.days .d:last-child{{border-bottom:0}}

/* единый мобильный ритм: одинаковые поля и вертикальные интервалы на всех страницах */
@media(max-width:640px){{
  :root{{--gutter:28px}}
  body>section[id]{{padding-top:64px!important;padding-bottom:72px!important}}
  body>section[id]:first-of-type{{padding-top:72px!important}}
  body>section[id]:last-of-type{{padding-bottom:80px!important}}
  body>section>.wrap>.sec-head,body>section>.wrap>.rsec-head{{margin-bottom:28px}}
  h2{{margin-bottom:0}}
  .lead,.sub{{margin-top:18px}}
}}
</style>
<style media="print">{PRINT_CSS}</style>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-512.png" sizes="512x512" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#0E1211">
</head>
<body>
<nav class="nav"><div class="wrap">
  <a class="brand" href="{SITE}" aria-label="synapt">{LOGO}</a>
  <div class="nav-links">{nav_links}</div>
  <div class="nav-act">
    <button class="tgl" id="tgl" type="button" aria-label="Тёмная тема" title="Тёмная тема"></button>
    <a class="btn sq" href="https://t.me/Anti4ay" target="_blank" rel="noopener" aria-label="Написать в Telegram" title="Написать в Telegram">{TGICON}</a>
    <a class="btn pri{cta_cls}" href="#cta">{nav_cta}</a>
    <button class="nav-burger" id="brg" type="button" aria-label="Меню" aria-expanded="false" aria-controls="sheet"><i></i><i></i></button>
  </div>
</div>
<div class="nav-sheet" id="sheet">{nav_links}
  <div class="ns-act">
    <button class="tgl ns-tgl" type="button" aria-label="Тёмная тема" title="Тёмная тема"></button>
    <a class="btn sq" href="https://t.me/Anti4ay" target="_blank" rel="noopener" aria-label="Написать в Telegram" title="Написать в Telegram">{TGICON}</a>
    <a class="btn pri" href="#cta">{nav_cta}</a>
  </div>
</div></nav>
<div class="pbrand" style="display:none">{LOGO}</div>
{body}
{pcontacts}
{sec_related(spec.get("id", ""), spec.get("relnum", ""))}
{FAB}
<footer><div class="wrap"><div class="f-main"><div class="f-brand"><a class="brand" href="{SITE}" aria-label="synapt">{LOGO}</a><p class="f-note">Студия AI и&nbsp;IT-разработки для&nbsp;бизнеса</p><a class="f-tg" href="https://t.me/Anti4ay" target="_blank" rel="noopener">Telegram менеджера</a></div><nav class="f-nav f-nav2"><span class="f-k">Разделы</span>{foot_links}</nav><div class="f-legal"><span class="f-k">Формальности</span><p>ИП Орешкин Антон Вадимович</p><p>ИНН 100123323420</p><p>ОГРНИП 324100000000411</p><p>185014, Республика Карелия, Петрозаводск</p><p>переулок Попова, дом&nbsp;6, квартира&nbsp;42</p><a href="/privacy">Политика обработки персональных данных</a></div></div><div class="f-bottom"><span>© 2026 Synapt</span></div></div></footer>
<script>
(function(){{var r=document.documentElement;var sv=null;try{{sv=localStorage.getItem('synapt_theme')}}catch(e){{}}
if(sv)r.setAttribute('data-theme',sv);
var sun='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
var moon='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
var bs=[].slice.call(document.querySelectorAll('.tgl'));
/* подпись на иконке называет тему, в которую переключит нажатие */
function pt(){{var light=r.getAttribute('data-theme')==='light';var lbl=light?'Тёмная тема':'Светлая тема';
  bs.forEach(function(b){{b.innerHTML=light?moon:sun;b.setAttribute('aria-label',lbl);b.setAttribute('title',lbl)}})}}
pt();
bs.forEach(function(b){{b.onclick=function(){{var t=r.getAttribute('data-theme')==='light'?'dark':'light';
  r.setAttribute('data-theme',t);try{{localStorage.setItem('synapt_theme',t)}}catch(e){{}}pt()}}}});}})();
(function(){{var g=document.getElementById('brg'),sh=document.getElementById('sheet');if(!g)return;
function shut(){{sh.classList.remove('open');g.classList.remove('on');
  document.body.classList.remove('menu-open');g.setAttribute('aria-expanded','false');g.setAttribute('aria-label','Меню')}}
g.onclick=function(){{var o=sh.classList.toggle('open');g.classList.toggle('on',o);
  document.body.classList.toggle('menu-open',o);g.setAttribute('aria-expanded',o?'true':'false');
  g.setAttribute('aria-label',o?'Закрыть меню':'Меню')}};
[].forEach.call(sh.querySelectorAll('a'),function(a){{a.onclick=shut}});
addEventListener('resize',function(){{if(innerWidth>1120) shut()}});}})();
(function(){{var els=document.querySelectorAll('.reveal');if(!('IntersectionObserver'in window)){{els.forEach(function(e){{e.classList.add('in')}});return}}
var io=new IntersectionObserver(function(en){{en.forEach(function(x){{if(x.isIntersecting){{x.target.classList.add('in');io.unobserve(x.target)}}}})}},{{threshold:.12,rootMargin:'0px 0px -8% 0px'}});els.forEach(function(e){{io.observe(e)}});}})();
{SYN_FX}
</script>
<script>
(function(){{
  var f=document.querySelector('.mform'); if(!f) return;
  f.addEventListener('submit',function(e){{
    e.preventDefault();
    var n=f.name.value.trim(), c=f.contact.value.trim(), ok=f.querySelector('input[type=checkbox]').checked;
    if(!n||!c||!ok){{ f.classList.add('err'); return }}
    f.classList.remove('err');
    var btn=f.querySelector('button[type=submit]'), was=btn?btn.textContent:'';
    if(btn){{ btn.disabled=true; btn.textContent='Отправляем' }}
    fetch('/api/lead',{{method:'POST',headers:{{'Content-Type':'application/json'}},
      body:JSON.stringify({{name:n,contact:c,page:document.title}})}})
      .then(function(r){{ if(!r.ok) throw 0; f.classList.add('sent') }})
      .catch(function(){{ f.classList.add('sent','fail') }})
      .then(function(){{ if(btn){{ btn.disabled=false; btn.textContent=was }} }});
  }});
}})();
/* набор обложки: кикер, заголовок, лид и цифры печатаются одновременно,
   символы стоят на местах и только проявляются, поэтому вёрстка не двигается */
(function(){{
  if(matchMedia('(prefers-reduced-motion:reduce)').matches) return;
  var targets=[].slice.call(document.querySelectorAll('.cover .chip, .cover .eyebrow, .cover h1, .cover .lead, .cover-stats .cs-n, .cover-stats .cs-c'));
  if(!targets.length) return;
  var runs=[];
  targets.forEach(function(el){{
    var chars=[];
    (function walk(node){{
      [].slice.call(node.childNodes).forEach(function(n){{
        if(n.nodeType===3){{
          var frag=document.createDocumentFragment();
          n.nodeValue.split('').forEach(function(ch){{
            var sp=document.createElement('span');
            sp.className='tch'; sp.textContent=ch;
            frag.appendChild(sp); chars.push(sp);
          }});
          node.replaceChild(frag, n);
        }} else if(n.nodeType===1) walk(n);
      }});
    }})(el);
    if(chars.length) runs.push(chars);
  }});
  var maxLen=0;
  runs.forEach(function(r){{ if(r.length>maxLen) maxLen=r.length }});
  var step=Math.max(10, Math.min(26, 1500/maxLen));
  runs.forEach(function(chars){{
    var i=0;
    (function tick(){{
      if(i>=chars.length) return;
      do {{ chars[i].classList.add('on'); i++ }} while(i<chars.length && chars[i-1].textContent===' ');
      setTimeout(tick, step + Math.random()*step*0.5);
    }})();
  }});
}})();
/* подложка шапки появляется, когда обложка уходит вверх */
(function(){{
  var nav=document.querySelector('.nav'), cov=document.querySelector('.cover');
  if(!nav) return;
  function upd(){{
    var h=cov?cov.getBoundingClientRect().height:0;
    nav.classList.toggle('solid', scrollY > Math.max(120, h-80));
  }}
  upd(); addEventListener('scroll',upd,{{passive:true}});
}})();


</script>
<script>
(function(){{
  var days=document.getElementById('slDays'), slotBox=document.getElementById('slSlots'),
      hid=document.getElementById('lfSlot'), note=document.getElementById('slNote');
  if(!days||!slotBox) return;
  var MN=['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря'];
  var WD=['вс','пн','вт','ср','чт','пт','сб'];
  var HOURS=['10:00','11:00','12:00','14:00','15:00','16:00','17:00'];
  var list=[], d=new Date(); d.setHours(0,0,0,0);
  while(list.length<10){{ d.setDate(d.getDate()+1); if(d.getDay()!==0&&d.getDay()!==6) list.push(new Date(d)); }}
  var sel={{day:null,time:null}};
  function label(x){{ return '<b>'+x.getDate()+'</b><span>'+WD[x.getDay()]+', '+MN[x.getMonth()].slice(0,3)+'</span>' }}
  list.forEach(function(x,i){{
    var b=document.createElement('button'); b.type='button'; b.className='sl-day'; b.innerHTML=label(x);
    b.addEventListener('click',function(){{
      /* повторный клик по выбранному дню сворачивает список времени */
      var same = b.classList.contains('on');
      [].forEach.call(days.children,function(e){{e.classList.remove('on')}});
      if(same){{ sel.day=null; sel.time=null; render(); return }}
      b.classList.add('on'); sel.day=x; sel.time=null; render();
    }});
    days.appendChild(b);
  }});
  function render(){{
    slotBox.innerHTML='';
    if(!sel.day){{ sync(); return }}
    HOURS.forEach(function(t){{
      var b=document.createElement('button'); b.type='button'; b.className='sl-t'+(sel.time===t?' on':''); b.textContent=t;
      b.addEventListener('click',function(){{ sel.time=t; render() }});
      slotBox.appendChild(b);
    }});
    sync();
  }}
  function sync(){{
    if(sel.day&&sel.time){{
      var v=sel.day.getDate()+' '+MN[sel.day.getMonth()]+', '+sel.time+' по Москве';
      hid.value=v;
      /* машинная метка для файла календаря: слоты объявлены по Москве, переводим в UTC */
      var hh=parseInt(sel.time.split(':')[0],10);
      var utc=new Date(Date.UTC(sel.day.getFullYear(),sel.day.getMonth(),sel.day.getDate(),hh-3,0,0));
      hid.dataset.iso=utc.toISOString();
      note.textContent='Выбрано: '+v;
    }} else {{ hid.value=''; note.textContent='' }}
  }}
  render();
}})();
</script>
<script>
/* плавающая пара прячется, когда на экране блок заявки: иначе кнопка ложится
   поверх формы и отправить заявку с телефона нечем */
(function(){{
  var fab=document.querySelector('.fab'), cta=document.getElementById('cta');
  if(!fab||!cta||!('IntersectionObserver' in window)) return;
  var io=new IntersectionObserver(function(en){{
    en.forEach(function(e){{
      fab.classList.toggle('is-off', e.isIntersecting);
      fab.setAttribute('aria-hidden', e.isIntersecting?'true':'false');
    }});
  }},{{rootMargin:'0px 0px -20% 0px'}});
  io.observe(cta);
}})();
</script>
</body>
</html>'''


# ---------- микротипографика: предлоги и союзы не остаются в конце строки ----------
_ORPHANS = ("а и к о с у в я ы б ж по на за из от до во со об не ни же бы ли "
            "но да то что как для или его её их им мы вы ты он").split()
_ORPHAN_RE = re.compile(r"(?<![\wА-Яа-яЁё&])(" + "|".join(sorted(_ORPHANS, key=len, reverse=True))
                        + r")\s+(?=[A-Za-zА-Яа-яЁё0-9])", re.IGNORECASE)


def typo_fix(doc):
    """Связывает короткие слова с последующими неразрывным пробелом. Код не трогает."""
    stash = []

    def hide(m):
        stash.append(m.group(0))
        return "\x00%d\x00" % (len(stash) - 1)

    doc = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", hide, doc, flags=re.I)
    doc = _ORPHAN_RE.sub(lambda m: re.sub(r"\s+$", "&nbsp;", m.group(0)), doc)
    return re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], doc)


SPECS = json.load(open(os.path.join(BASE, "specs.json"), encoding="utf-8"))


def make_pdf(folder, spec):
    """Печатает собранную страницу в PDF через хром. Печать не должна валить сборку HTML,
    поэтому ошибка печати остаётся предупреждением."""
    src = os.path.join(folder, "index.html")
    dst = os.path.join(folder, spec["pdf"])
    try:
        r = subprocess.run(["node", os.path.join(BASE, "pdf.mjs"), src, dst, spec["title"]],
                           capture_output=True, text=True, timeout=180)
    except Exception as e:
        print("   PDF не собрался:", e)
        return
    if r.returncode != 0 or not os.path.exists(dst):
        print("   PDF не собрался:", (r.stderr or r.stdout).strip()[:300])
        return
    print("   PDF:", spec["pdf"], "%.0f КБ" % (os.path.getsize(dst) / 1024))


if __name__ == "__main__":
    only = set(a for a in sys.argv[1:] if not a.startswith("-"))
    skip_pdf = "--no-pdf" in sys.argv[1:]
    for slug, spec in SPECS.items():
        if only and slug not in only:
            continue
        d = os.path.join(OUT, slug)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(typo_fix(render(spec, slug)))
        print("сгенерирован:", slug, "->", spec["pdf"])
        if not skip_pdf:
            make_pdf(d, spec)
