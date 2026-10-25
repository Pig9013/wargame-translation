# -*- coding: utf-8 -*-
"""
GBII Ds版 rulebook PDF builder.

Usage:
    cp build_rulebook_pdf.py rulebook_config.py <project>/_tools/
    # edit rulebook_config.py
    python -I build_rulebook_pdf.py

Config path can be overridden with RULEBOOK_CONFIG=/path/to/rulebook_config.py.
The builder does not modify the markdown; it is the layout-only step.
"""
import re, os, io, subprocess, html, sys, shutil, importlib.util
from pathlib import Path

# ---------- project config ----------
# Priority: RULEBOOK_CONFIG env -> rulebook_config.py next to this script
#           -> rulebook_config.example.py
_here = Path(__file__).resolve().parent
CONFIG_PATH = Path(os.environ.get('RULEBOOK_CONFIG', str(_here / 'rulebook_config.py')))
if not CONFIG_PATH.exists():
    CONFIG_PATH = _here / 'rulebook_config.example.py'
_spec = importlib.util.spec_from_file_location('rulebook_config', str(CONFIG_PATH))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
C = _mod.CONFIG

BASE = Path(C['base'])
WORK = BASE / C.get('work', '_layout_work')
WORK.mkdir(parents=True, exist_ok=True)

def _path(key, default):
    v = C.get(key, default)
    p = Path(v)
    return p if p.is_absolute() else BASE / p

MD = _path('md', 'rulebook.md')
OUT = _path('out', 'rulebook_out.pdf')
HTML = _path('html', WORK / 'rulebook.html')
PDF = _path('raw', WORK / 'rulebook_raw.pdf')
for _p in (OUT, HTML, PDF):
    _p.parent.mkdir(parents=True, exist_ok=True)
LABEL = C.get('label', '')
VERSION = C.get('version', 'v1.0')
DATE = C.get('date', '')
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

# ---------- inline markdown ----------
def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return s

def figure_class(src):
    """Map image filename to CSS class (config-driven)."""
    low = src.lower()
    for key, klass in C.get('figure_class_map', {}).items():
        if key.lower() in low:
            return klass
    return C.get('default_figure_class', 'fig-counter')

def is_counter_figure(src):
    """Counter-style figures float in a column; all others are full-width."""
    return figure_class(src) == C.get('default_figure_class', 'fig-counter')

# ---------- block parser ----------
def parse_blocks(lines):
    blocks = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].rstrip('\n')
        s = line.strip()
        if not s:
            i += 1; continue
        # heading
        m = re.match(r'^(#{1,4})\s+(.*)$', s)
        if m:
            level = len(m.group(1)); txt = m.group(2).strip()
            blocks.append({'t': 'h%d' % level, 'text': txt})
            i += 1; continue
        # hr
        if re.match(r'^-{3,}$', s):
            blocks.append({'t': 'hr'}); i += 1; continue
        # image
        m = re.match(r'^!\[(.*?)\]\((.*?)\)$', s)
        if m:
            blocks.append({'t': 'img', 'alt': m.group(1), 'src': m.group(2)})
            i += 1; continue
        # table
        if s.startswith('|') and i + 1 < n and re.match(r'^\|[\s:|-]+\|$', lines[i+1].strip()):
            header = [c.strip() for c in s.strip('|').split('|')]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            blocks.append({'t': 'table', 'header': header, 'rows': rows})
            continue
        # blockquote
        if s.startswith('>'):
            buf = []
            while i < n and lines[i].strip().startswith('>'):
                buf.append(re.sub(r'^>\s?', '', lines[i].strip()))
                i += 1
            blocks.append({'t': 'quote', 'text': '\n'.join(buf)})
            continue
        # lists
        if re.match(r'^([-*]|\d+\.)\s+', s):
            ordered = bool(re.match(r'^\d+\.', s))
            items = []
            while i < n:
                t = lines[i].strip()
                if not t:
                    # allow blank between items if next is list
                    j = i + 1
                    while j < n and not lines[j].strip(): j += 1
                    if j < n and re.match(r'^([-*]|\d+\.)\s+', lines[j].strip()):
                        i = j; continue
                    break
                m2 = re.match(r'^([-*]|\d+\.)\s+(.*)$', t)
                if not m2: break
                items.append(m2.group(2))
                i += 1
            blocks.append({'t': 'ol' if ordered else 'ul', 'items': items})
            continue
        # paragraph
        buf = [s]
        i += 1
        while i < n:
            t = lines[i].strip()
            if not t or re.match(r'^(#{1,4})\s+', t) or t.startswith('|') or t.startswith('>') \
               or re.match(r'^!\[.*?\]\(.*?\)$', t) or re.match(r'^([-*]|\d+\.)\s+', t) \
               or re.match(r'^-{3,}$', t):
                break
            buf.append(t); i += 1
        blocks.append({'t': 'p', 'text': ' '.join(buf)})
    return blocks

def block_html(b):
    t = b['t']
    if t == 'p':
        return '<p>%s</p>' % inline(b['text'])
    if t in ('h1','h2','h3','h4'):
        return '<%s>%s</%s>' % (t, inline(b['text']), t)
    if t == 'hr':
        return '<hr/>'
    if t == 'ul':
        return '<ul>%s</ul>' % ''.join('<li>%s</li>' % inline(x) for x in b['items'])
    if t == 'ol':
        return '<ol>%s</ol>' % ''.join('<li>%s</li>' % inline(x) for x in b['items'])
    if t == 'quote':
        txt = b['text']
        # bold label at start
        return '<blockquote>%s</blockquote>' % inline(txt).replace('\n', '<br/>')
    if t == 'table':
        h = ''.join('<th>%s</th>' % inline(x) for x in b['header'])
        rows = ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % inline(c) for c in r) for r in b['rows'])
        return '<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (h, rows)
    if t == 'img':
        src = b['src']
        cls = 'fig ' + figure_class(src)
        alt = b['alt']
        return '<figure class="%s"><img src="%s" alt="%s"/><figcaption>%s</figcaption></figure>' % (
            cls, (BASE / src).as_uri(), html.escape(alt), inline(alt))
    return ''

def render_flow(blocks):
    out = []
    colbuf = []
    def flush():
        nonlocal colbuf
        if colbuf:
            out.append('<section class="cols">' + ''.join(colbuf) + '</section>')
            colbuf = []
    just_part = False
    for b in blocks:
        t = b['t']
        is_counter = (t == 'img' and is_counter_figure(b['src']))
        full = t in ('h1','h2','table','img','quote','hr') and not is_counter
        if full:
            flush()
            if t == 'h1':
                just_part = True
                txt = inline(b['text'])
                pcls = 'part'
                if C.get('part_inline_keyword', '可选规则') in b['text']:
                    pcls = 'part part-inline'
                out.append('<div class="%s"><div class="part-kicker">%s</div><h1>%s</h1></div>' % (
                    pcls, inline(C.get('part_kicker', '')), txt))
            elif t == 'h2':
                txt = b['text']
                cls = 'section'
                _brk = False
                if not just_part:
                    _brk = bool(re.match(C.get('page_break_h2_regex', r'$^'), txt))
                    _brk = _brk or any(txt.startswith(x) for x in C.get('page_break_h2_prefixes', []))
                    _brk = _brk or txt in C.get('page_break_h2_exact', [])
                if _brk:
                    cls += ' section-break'
                just_part = False
                out.append('<div class="%s"><h2>%s</h2></div>' % (cls, inline(txt)))
            elif t == 'table':
                extra = ''
                if b['header'] and b['header'][0] in C.get('table_break_headers', []):
                    extra = ' table-break'
                out.append('<div class="full tablewrap%s">%s</div>' % (extra, block_html(b)))
            elif t == 'img':
                out.append('<div class="full">%s</div>' % block_html(b))
            elif t == 'quote':
                out.append('<div class="full">%s</div>' % block_html(b))
            elif t == 'hr':
                out.append('<div class="full"><hr/></div>')
        else:
            colbuf.append(block_html(b))
    flush()
    return '\n'.join(out)

# ---------- read md ----------
md = io.open(MD, encoding='utf-8').read()
lines = md.splitlines()

# front matter sections
def section_between(start_pat, end_pat=None):
    si = None
    for i,l in enumerate(lines):
        if re.match(start_pat, l.strip()):
            si = i; break
    if si is None: return ''
    ei = len(lines)
    if end_pat:
        for j in range(si+1, len(lines)):
            if re.match(end_pat, lines[j].strip()):
                ei = j; break
    return '\n'.join(lines[si:ei]).strip()

trans = section_between(r'^## 翻译说明', r'^## 出版信息')
pub = section_between(r'^## 出版信息', r'^## 引言')
intro = section_between(r'^## 引言', r'^## 目录')

body_start = None
for i,l in enumerate(lines):
    if l.strip() == '# 主规则':
        body_start = i; break
body_lines = lines[body_start:]
body_blocks = parse_blocks(body_lines)
body_html = render_flow(body_blocks)

# ---------- toc entries ----------
toc_entries = []
for b in body_blocks:
    if b['t'] in ('h1','h2'):
        toc_entries.append((b['t'], b['text']))

def toc_html(pages=None):
    # group h1 as headers, h2 as entries
    out = ['<div class="toc-page"><div class="toc-head"><div class="toc-kicker">CONTENTS</div><h2>目录</h2></div><div class="toc-cols">']
    cur = []
    for typ, txt in toc_entries:
        if typ == 'h1':
            if cur:
                out.append('<div class="toc-group">' + ''.join(cur) + '</div>')
                cur = []
            out.append('<div class="toc-part">%s</div>' % inline(txt))
        else:
            page = ''
            if pages and txt in pages:
                page = str(pages[txt])
            cur.append('<div class="toc-row"><span class="toc-t">%s</span><span class="toc-d"></span><span class="toc-p">%s</span></div>' % (inline(txt), page))
    if cur:
        out.append('<div class="toc-group">' + ''.join(cur) + '</div>')
    out.append('</div></div>')
    return ''.join(out)

# ---------- front matter html ----------
def front_section(mdtext, cls=''):
    bl = parse_blocks(mdtext.splitlines())
    # drop the h2 heading itself for custom layout
    if bl and bl[0]['t'] == 'h2':
        title = bl[0]['text']
        rest = bl[1:]
    else:
        title = ''
        rest = bl
    h = '<section class="front %s">' % cls
    if title:
        h += '<h2>%s</h2>' % inline(title)
    h += ''.join(block_html(b) for b in rest)
    h += '</section>'
    return h

front_html = front_section(trans, 'trans') + front_section(pub, 'pub') + front_section(intro, 'intro')

# ---------- css ----------
CSS = r'''
@font-face { font-family:'NotoSerifSC'; src:url('file:///C:/Windows/Fonts/NotoSerifSC-VF.ttf'); font-weight:100 900; }
@font-face { font-family:'NotoSansSC'; src:url('file:///C:/Windows/Fonts/NotoSansSC-VF.ttf'); font-weight:100 900; }
@page { size: 215.9mm 279.4mm; margin: 19mm 18mm 20mm 18mm; }
* { box-sizing: border-box; }
html, body { margin:0; padding:0; }
body { font-family:'NotoSerifSC', serif; font-size:9.7pt; line-height:1.72; color:#1b1b1b; }
p { margin:0 0 2.6mm 0; text-align:justify; }
h1,h2,h3,h4 { font-family:'NotoSansSC', sans-serif; color:#111; margin:0; }
h3 { font-size:11.2pt; font-weight:700; margin:3.3mm 0 1.6mm; break-after:avoid; }
h4 { font-size:10pt; font-weight:700; margin:2.6mm 0 1.2mm; break-after:avoid; }
strong { font-weight:700; }
em { font-style:italic; color:#444; }
code { font-family:'NotoSansSC'; font-size:8.6pt; background:#f1f1f1; padding:0 1mm; }

/* cover */
.cover { height: 238mm; position:relative; page-break-after: always; overflow:hidden; }
.cover .topbar { position:absolute; top:0; left:0; right:0; height:13mm; background:#111; color:#fff;
  font-family:'NotoSansSC'; font-size:7.5pt; letter-spacing:1.6pt; padding:4.2mm 8mm 0; }
.cover .redline { position:absolute; top:13mm; left:0; right:0; height:2.2mm; background:#9e1b1b; }
.cover .series { position:absolute; top:26mm; left:8mm; font-family:'NotoSansSC'; font-size:8pt; letter-spacing:2pt; color:#666; }
.cover h1 { position:absolute; top:36mm; left:8mm; right:8mm; font-family:'NotoSerifSC'; font-size:45pt; line-height:1.12; font-weight:900; letter-spacing:-1pt; }
.cover h1 .red { color:#9e1b1b; }
.cover .sub { position:absolute; top:84mm; left:8mm; font-family:'NotoSansSC'; font-size:15pt; font-weight:500; letter-spacing:3pt; color:#222; }
.cover .en { position:absolute; top:98mm; left:8mm; font-family:'NotoSansSC'; font-size:9pt; letter-spacing:1.2pt; color:#777; }
.cover .star { position:absolute; top:124mm; left:8mm; width:18mm; height:18mm; background:#9e1b1b; clip-path:polygon(50% 0%,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%); }
.cover .rule { position:absolute; top:158mm; left:8mm; right:8mm; height:0.5pt; background:#bbb; }
.cover .meta { position:absolute; top:165mm; left:8mm; font-family:'NotoSansSC'; font-size:8.4pt; line-height:2.1; color:#444; }
.cover .bottom { position:absolute; bottom:0; left:0; right:0; height:16mm; background:#111; color:#ddd;
  font-family:'NotoSansSC'; font-size:7.2pt; letter-spacing:1pt; padding:5.2mm 8mm 0; }

/* front matter */
.front { }
.front h2 { font-size:19pt; font-weight:800; border-bottom:1.2pt solid #9e1b1b; padding-bottom:2mm; margin:0 0 5mm; }
.front.trans { font-size:9pt; }
.front.trans ul { margin:0 0 3mm 4mm; padding:0; }
.front.trans li { margin:0 0 1.2mm; }
.front.pub p { font-size:8.2pt; line-height:1.65; color:#333; }
.front.intro { break-before:page; }
.front.intro p { font-size:10.2pt; line-height:1.85; }

/* toc */
.toc-page { break-before:page; break-after:page; }
.toc-head { border-bottom:1.2pt solid #9e1b1b; margin-bottom:5mm; padding-bottom:2mm; }
.toc-kicker { font-family:'NotoSansSC'; font-size:7pt; letter-spacing:2pt; color:#9e1b1b; }
.toc-head h2 { font-family:'NotoSansSC'; font-size:20pt; font-weight:800; margin:0.8mm 0 0; }
.toc-cols { column-count:2; column-gap:10mm; font-family:'NotoSansSC'; font-size:8.4pt; }
.toc-part { font-weight:800; font-size:9.2pt; color:#9e1b1b; margin:3mm 0 1.2mm; break-after:avoid; }
.toc-group { margin-bottom:2mm; }
.toc-row { display:flex; align-items:baseline; gap:1.2mm; margin:0 0 0.85mm; }
.toc-t { white-space:nowrap; overflow:hidden; }
.toc-d { flex:1; border-bottom:0.4pt dotted #aaa; margin-bottom:0.7mm; }
.toc-p { font-variant-numeric:tabular-nums; color:#333; }

/* part */
.part { break-before:page; background:#111; color:#fff; padding:9mm 8mm 8mm; margin:0 0 6mm; position:relative; }
.part-inline { break-before:auto; margin-top:7mm; }
.part:after { content:''; position:absolute; left:0; bottom:0; width:100%; height:2mm; background:#9e1b1b; }
.part-kicker { font-family:'NotoSansSC'; font-size:7pt; letter-spacing:2pt; color:#bbb; margin-bottom:2mm; }
.part h1 { color:#fff; font-family:'NotoSerifSC'; font-size:25pt; font-weight:900; line-height:1.15; }

/* section */
.section { break-after:avoid; margin:0 0 3mm; }
.section h2 { font-size:14.5pt; font-weight:800; color:#111; border-left:3.2mm solid #9e1b1b; padding-left:3.2mm; line-height:1.3; }
.section-break { break-before:page; }

/* columns */
.cols { column-count:2; column-gap:8.5mm; column-fill:balance; }
.cols > p, .cols > ul, .cols > ol { break-inside:auto; }
.cols h3 { break-after:avoid; }
.cols ul, .cols ol { margin:0 0 2.6mm 4.5mm; padding:0; }
.cols li { margin:0 0 0.9mm; }
.full { break-inside:avoid; }

/* tables */
.tablewrap { margin:3mm 0 4mm; break-inside:auto; }
.table-break { break-before:page; }
table { width:100%; border-collapse:collapse; font-family:'NotoSansSC'; font-size:7.7pt; line-height:1.4; }
thead { display:table-header-group; }
thead th { background:#222; color:#fff; font-weight:700; padding:1.2mm 1.5mm; text-align:left; white-space:nowrap; }
tbody td { padding:1.0mm 1.5mm; border-bottom:0.4pt solid #d8d8d8; vertical-align:top; }
tbody tr:nth-child(even) td { background:#f4f4f4; }
tbody tr { break-inside:avoid; }

/* blockquote note */
blockquote { margin:3.2mm 0 4mm; padding:3mm 4mm 2.6mm; background:#f5f2ec; border-left:3mm solid #9e1b1b;
  font-size:8.8pt; line-height:1.68; color:#333; }
blockquote strong { color:#8f1d1d; }

/* figures */
figure { margin:3mm 0 4mm; text-align:center; break-inside:avoid; }
figure img { display:block; margin:0 auto; }
figcaption { font-family:'NotoSansSC'; font-size:7.4pt; color:#666; margin-top:1.2mm; }
.fig-counter { float:right; width:27mm; margin:0.5mm 0 2mm 3.5mm; text-align:center; }
.fig-counter img { width:100%; }
.fig-counter figcaption { font-size:6.8pt; line-height:1.3; }
.fig-symbols img { width:78mm; }
.fig-photos img { width:158mm; }
.rail_arty img { width:26mm; }

/* misc */
hr { border:0; border-top:0.5pt solid #ccc; margin:3mm 0; }
'''

# ---------- assemble html (first pass, no toc numbers) ----------
def make_html(toc_pages=None):
    return f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="cover">
  <div class="topbar">{C.get('topbar','')}</div>
  <div class="redline"></div>
  <div class="series">{C.get('series_cn','')}</div>
  <h1>{C.get('title_cn_1','')}<br/><span class="red">{C.get('title_cn_2','')}</span> {C.get('title_cn_suffix','')}</h1>
  <div class="sub">{C.get('subtitle','')}{f' · {LABEL}' if LABEL else ''}</div>
  <div class="en">{C.get('title_en','')} &nbsp;·&nbsp; {C.get('title_en_suffix','REPRINT RULES')}{f' &nbsp;·&nbsp; {LABEL}' if LABEL else ''}</div>
  <div class="star"></div>
  <div class="rule"></div>
  <div class="meta">{C.get('meta_line','')}<br/>{C.get('meta_refs','')}<br/>翻译：{C.get('translator','')} &nbsp;·&nbsp; {VERSION}{f' &nbsp;·&nbsp; {LABEL}' if LABEL else ''} &nbsp;·&nbsp; {DATE}</div>
  <div class="bottom">{C.get('bottom','')}</div>
</div>
{front_html}
{toc_html(toc_pages)}
{body_html}
</body></html>'''

io.open(HTML, 'w', encoding='utf-8').write(make_html())
print('html written', HTML, len(make_html()))

# ---------- edge print ----------
def print_pdf(html_path, pdf_path):
    cmd = [EDGE, '--headless=new', '--disable-gpu', '--no-first-run', '--no-pdf-header-footer',
           '--print-to-pdf=' + str(pdf_path), Path(html_path).as_uri()]
    subprocess.run(cmd, check=True, timeout=180)
    print('printed', pdf_path, os.path.getsize(pdf_path))

print_pdf(HTML, PDF)

# ---------- page mapping pass ----------
import fitz

def find_pages(pdf_path, headings):
    d = fitz.open(pdf_path)
    body_start = None
    for i in range(2, d.page_count):
        if C.get('body_start_marker','') in d[i].get_text():
            body_start = i; break
    if body_start is None:
        body_start = 3
    # collect heading lines by font size
    found = {}
    for i in range(body_start, d.page_count):
        p = d[i]
        for bl in p.get_text('dict')['blocks']:
            if bl['type'] != 0:
                continue
            for ln in bl['lines']:
                txt = ''.join(sp['text'] for sp in ln['spans']).strip()
                sz = max((sp['size'] for sp in ln['spans']), default=0)
                if not txt:
                    continue
                if sz < 13:
                    continue
                found.setdefault(txt, i)
                # wrapped long heading: register first line prefix
                if len(txt) >= 6:
                    found.setdefault(txt[:6], i)
    pages = {}
    for h in headings:
        txt = re.sub(r'\s+', ' ', h).strip()
        cands = [txt, txt[:10], txt[:8], txt[:6]]
        for c in cands:
            if c in found:
                pages[h] = found[c] - body_start + 1
                break
    d.close()
    return body_start, pages

all_heads = [txt for typ, txt in toc_entries]
body_start, pages = find_pages(PDF, all_heads)
print('body_start', body_start, 'mapped', len(pages), '/', len(all_heads))

io.open(HTML, 'w', encoding='utf-8').write(make_html(pages))
print_pdf(HTML, PDF)

# ---------- header/footer + bookmarks ----------
d = fitz.open(PDF)
body_start = None
for i in range(2, d.page_count):
    if C.get('body_start_marker','') in d[i].get_text():
        body_start = i; break
if body_start is None:
    body_start = 3
MM = 2.834645669
W = d[0].rect.width
RED = (0.62, 0.105, 0.105)
GREY = (0.42, 0.42, 0.42)
for i in range(d.page_count):
    p = d[i]
    if i >= body_start:
        n = i - body_start + 1
        # header
        p.insert_text((18*MM, 11.5*MM), C.get('header_left', '') + (f' · {LABEL}' if LABEL else ''), fontsize=6.8,
                      fontname='NotoSerifSC', fontfile=r'C:/Windows/Fonts/NotoSerifSC-VF.ttf', color=GREY)
        p.insert_text((W-18*MM-32*MM, 11.5*MM), C.get('header_right', ''), fontsize=6.8,
                      fontname='NotoSerifSC', fontfile=r'C:/Windows/Fonts/NotoSerifSC-VF.ttf', color=GREY)
        p.draw_line((18*MM, 13.2*MM), (W-18*MM, 13.2*MM), color=RED, width=0.45)
        # footer
        p.insert_text((18*MM, 270*MM), f"{C.get('footer_left','')} {VERSION}" + (f' {LABEL}' if LABEL else ''), fontsize=6.6,
                      fontname='NotoSerifSC', fontfile=r'C:/Windows/Fonts/NotoSerifSC-VF.ttf', color=GREY)
        p.insert_textbox(fitz.Rect(W/2-10*MM, 266.5*MM, W/2+10*MM, 272.5*MM), str(n), fontsize=8.2,
                         fontname='NotoSansSC', fontfile=r'C:/Windows/Fonts/NotoSansSC-VF.ttf',
                         color=RED, align=1)
        p.insert_text((W-18*MM-45*MM, 270*MM), C.get('footer_right', ''), fontsize=6.4,
                      fontname='NotoSerifSC', fontfile=r'C:/Windows/Fonts/NotoSerifSC-VF.ttf', color=GREY)

# bookmarks
toc = []
for typ, txt in toc_entries:
    if txt in pages:
        toc.append([1 if typ == 'h1' else 2, txt, pages[txt] + body_start])
d.set_toc(toc)
_md = C.get('metadata', {})
d.set_metadata({
    'title': f"{C.get('header_left','')}（中文翻译）" + (f'·{LABEL}' if LABEL else ''),
    'author': _md.get('author', C.get('translator', '')),
    'subject': _md.get('subject', '') + (f'（{LABEL}）' if LABEL else ''),
    'keywords': _md.get('keywords', ''),
    'creator': _md.get('creator', ''),
    'producer': _md.get('producer', 'Edge + PyMuPDF'),
})
d.subset_fonts()
d.save(OUT, garbage=4, deflate=True, deflate_images=True, deflate_fonts=True, clean=True)
print('saved', OUT, 'pages', d.page_count)
