#!/usr/bin/env python3
"""Build the Direction B static site for Netlify."""
import json, pathlib, html as H

SITE = "https://universal-spectrum-solutions.netlify.app"
OUT = pathlib.Path(__file__).resolve().parent.parent
D = json.load(open(pathlib.Path(__file__).resolve().parent / 'data.json'))
BANDS, DETAIL, PACKS = D['BANDS'], D['DETAIL'], D['PACKS']
PROJECTS, NEWS, TEAM, JOBS = D['PROJECTS'], D['NEWS'], D['TEAM'], D['JOBS']


# ---------------- cache-busting fingerprints ----------------
# css/js carry a year-long immutable cache header, so the filename must change
# when the contents do or returning visitors keep the old copy forever.
import hashlib
def fingerprint(rel):
    src = OUT / rel
    digest = hashlib.md5(src.read_bytes()).hexdigest()[:10]
    stem, dot, ext = rel.rpartition('.')
    for stale in src.parent.glob(f"{stem.split('/')[-1]}.*.{ext}"):
        stale.unlink()
    target = src.parent / f"{stem.split('/')[-1]}.{digest}.{ext}"
    target.write_bytes(src.read_bytes())
    return f"/{stem.rsplit('/',1)[0]}/{target.name}"

CSS_HREF = fingerprint('css/style.css')
JS_SRC   = fingerprint('js/script.js')


def un(s): return s.replace('&amp;', '&')
def esc(s): return H.escape(un(s), quote=True)

SHORT = ['Training', 'ICT', 'Renewable Energy', 'Security Systems',
         'Media', 'Environment & Agric', 'Property']

NAV = [("/", "Home"), ("/about/", "About"), ("/divisions/", "Divisions"),
       ("/projects/", "Projects"), ("/news/", "News"),
       ("/careers/", "Careers")]

WAVES = '<canvas class="waves" data-waves aria-hidden="true"></canvas>'

STAR = ('<svg class="{c}" viewBox="0 0 200 200" aria-hidden="true"><path fill="#fff" '
        'd="M100 0l12 56 40-40-20 52 56-12-48 32 48 32-56-12 20 52-40-40-12 56-12-56-40 40 '
        '20-52-56 12 48-32-48-32 56 12-20-52 40 40z"/></svg>')

def img_block(src, alt, w, h, small=None, style=""):
    st = f' style="{style}"' if style else ''
    srcset = f' srcset="/assets/{small} 640w, /assets/{src} 1140w" sizes="(max-width:700px) 92vw, 46vw"' if small else ''
    return (f'<div class="img-block"{st}>'
            f'<img src="/assets/{src}"{srcset} width="{w}" height="{h}" '
            f'loading="lazy" decoding="async" alt="{alt}"></div>')

def photo(label, cls="", style=""):
    st = f' style="{style}"' if style else ''
    return f'<div class="photo {cls}"{st}><b>{label}</b></div>'

def head(title, desc, path):
    url = SITE + path
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Universal Spectrum Solutions Limited">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/ussl-logo.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#296AFF">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{CSS_HREF}">
</head>
<body>
"""

def header(active):
    links = ''
    for href, label in NAV:
        key = href.strip('/') or 'home'
        on = ' class="on"' if key == active or (key == 'divisions' and active in
             [DETAIL[str(i)]['slug'] for i in range(7)]) else ''
        links += f'<a href="{href}"{on}>{label}</a>'
    con = ' class="on only-mobile"' if active == 'contact' else ' class="only-mobile"'
    links += f'<a href="/contact/"{con}>Contact</a>'
    cta_on = ' is-on' if active == 'contact' else ''
    return f"""<header>
  <div class="wrap bar">
    <a href="/"><img class="logo" src="/assets/ussl-logo.png" alt="Universal Spectrum Solutions Ltd." width="190" height="38"></a>
    <button class="menu" aria-expanded="false">Menu</button>
    <nav aria-label="Main">{links}</nav>
    <a class="pill{cta_on}" href="/contact/">Get in touch <span class="dot">&#8599;</span></a>
  </div>
</header>
"""


# ---------------- social icons ----------------
SOCIAL_SVG = {
 "linkedin":'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.94 5a2 2 0 1 1-4-.002 2 2 0 0 1 4 .002zM7 8.48H3V21h4V8.48zm6.32 0H9.34V21h3.94v-6.57c0-3.66 4.77-4 4.77 0V21H22v-7.93c0-6.17-7.06-5.94-8.72-2.91l.04-1.68z"/></svg>',
 "facebook":'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 12.06C22 6.5 17.52 2 12 2S2 6.5 2 12.06c0 5 3.66 9.15 8.44 9.94v-7.03H7.9v-2.91h2.54V9.85c0-2.52 1.49-3.91 3.78-3.91 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.78-1.63 1.57v1.89h2.78l-.45 2.91h-2.33V22c4.78-.79 8.43-4.94 8.43-9.94z"/></svg>',
 "x":'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.53 3h3.07l-6.7 7.66L21.75 21h-5.98l-4.69-6.13L5.72 21H2.64l7.17-8.2L2.25 3h6.13l4.24 5.6L17.53 3zm-1.08 16.14h1.7L7.63 4.76H5.8l10.65 14.38z"/></svg>',
 "instagram":'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 3.25.15 4.77 1.69 4.92 4.92.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.15 3.23-1.66 4.77-4.92 4.92-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-3.26-.15-4.77-1.7-4.92-4.92-.06-1.27-.07-1.65-.07-4.85s.01-3.58.07-4.85C2.38 3.92 3.89 2.38 7.15 2.23 8.42 2.17 8.8 2.16 12 2.16zm0 5.68a4.16 4.16 0 1 0 0 8.32 4.16 4.16 0 0 0 0-8.32zm0 6.86a2.7 2.7 0 1 1 0-5.4 2.7 2.7 0 0 1 0 5.4zm5.34-7.03a.97.97 0 1 1-1.94 0 .97.97 0 0 1 1.94 0z"/></svg>',
 "email":'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 3.4-8 5-8-5V6l8 5 8-5v1.4z"/></svg>',
}

# Live links only. Leave a url empty and that icon is simply not rendered,
# rather than shipping a dead "#" link.
# Row is hidden while every url is empty. Paste a real profile URL next to a
# platform and its icon appears in the footer automatically.
SOCIAL = [
 ("linkedin",  "", "LinkedIn"),
 ("facebook",  "", "Facebook"),
 ("x",         "", "X"),
 ("instagram", "", "Instagram"),
 ("email",     "", "Email us"),
]

def social_row():
    out = ""
    for key, url, label in SOCIAL:
        if not url:
            continue
        out += (f'<a href="{url}" aria-label="{label}" title="{label}"'
                f'{" target=_blank rel=noopener" if url.startswith("http") else ""}>'
                f'{SOCIAL_SVG[key]}</a>')
    return f'<div class="social">{out}</div>' if out else ""


FOOT_DIV = ''.join(f'<a href="/{DETAIL[str(i)]["slug"]}/">{SHORT[i]}</a>' for i in range(7))

SOCIAL_ROW = social_row()

FOOTER = f"""<footer>
  <div class="wrap">
    <div class="foot">
      <div>
        <img src="/assets/ussl-logo-mono.png" alt="Universal Spectrum Solutions Ltd." width="190" height="40">
        <p>Technology, energy, security, media, agriculture, property and capacity development for Nigerian institutions.</p>
        {SOCIAL_ROW}
      </div>
      <div><h4>Divisions</h4>{FOOT_DIV}</div>
      <div><h4>Company</h4><a href="/about/">About us</a><a href="/about/#leadership">Leadership</a><a href="/projects/">Projects</a><a href="/partners/">Partners</a><a href="/careers/">Careers</a></div>
      <div><h4>Contact</h4>
        <a href="tel:+2347048223500">0704 822 3500</a>
        <a href="tel:+2348091379774">0809 137 9774</a>
        <a href="mailto:universalspectrumsolutionsltd@gmail.com">Email us</a>
        <a href="/contact/">Kaduna &amp; Abuja FCT</a>
      </div>
    </div>
    <div class="copy">&copy; 2026 Universal Spectrum Solutions Limited &nbsp;&middot;&nbsp; RC 9113492 &nbsp;&middot;&nbsp; Registered in Nigeria</div>
  </div>
</footer>
<script src="{JS_SRC}" defer></script>
</body>
</html>
"""

def write(path, active, title, desc, body, body_class=""):
    doc = head(title, desc, path) + header(active) + body + FOOTER
    if body_class:
        doc = doc.replace("<body>", f'<body class="{body_class}">', 1)
    d = OUT / path.strip('/')
    d.mkdir(parents=True, exist_ok=True)
    (d / 'index.html').write_text(doc)
    return path

def banner(eyebrow, h1, lede=None):
    sub = f'<p class="lede" style="color:#CFE0FF;margin-top:16px">{lede}</p>' if lede else ''
    return f"""<div class="wrap">
  <div class="banner">
    {WAVES}
    <div class="bglow" aria-hidden="true"></div>
    <div class="inner">
      <div class="eyebrow">{eyebrow}</div>
      <h1>{h1}</h1>
      {sub}
    </div>
  </div>
</div>
"""

def cta(title, body, label="Let's talk", link="/contact/"):
    return f"""<section>
  <div class="wrap">
    <div class="cta">
      <svg class="blob" viewBox="0 0 200 200" aria-hidden="true"><path fill="#4D84FF" d="M44 -62C58 -52 70 -40 75 -25C80 -10 78 8 71 24C64 40 52 54 36 62C20 70 0 72 -18 67C-36 62 -52 50 -63 34C-74 18 -80 -2 -76 -20C-72 -38 -58 -54 -42 -64C-26 -74 -8 -78 8 -76C24 -74 30 -72 44 -62Z" transform="translate(100 100)"/></svg>
      <svg class="dotgrid" width="78" height="54" aria-hidden="true"><g fill="rgba(255,255,255,.5)">
        <circle cx="4" cy="4" r="3"/><circle cx="26" cy="4" r="3"/><circle cx="48" cy="4" r="3"/><circle cx="70" cy="4" r="3"/>
        <circle cx="4" cy="26" r="3"/><circle cx="26" cy="26" r="3"/><circle cx="48" cy="26" r="3"/><circle cx="70" cy="26" r="3"/>
        <circle cx="4" cy="48" r="3"/><circle cx="26" cy="48" r="3"/><circle cx="48" cy="48" r="3"/><circle cx="70" cy="48" r="3"/>
      </g></svg>
      <div class="inner">
        <h2>{title}</h2>
        <p>{body}</p>
        <a class="pill light" href="{link}">{label} <span class="dot">&#8599;</span></a>
      </div>
    </div>
  </div>
</section>
"""

def sec_title(h2, lede=None):
    s = f'<p class="lede">{lede}</p>' if lede else ''
    return f'<div class="sec-title"><h2>{h2}</h2>{s}</div>'

# ---------------- HOME ----------------
def home():
    svc = ('<div class="card hl"><span class="ic"><i></i></span>'
           '<h3>Information &amp; Communications Technology</h3>'
           '<p>Cybersecurity, software, hardware, data centres, cloud, analytics and AI.</p>'
           '<a class="arrow" href="/ict/">&#8594;</a></div>')
    for i in (2, 3, 0):
        svc += (f'<a class="card flat" href="/{DETAIL[str(i)]["slug"]}/"><span class="ic"><i></i></span>'
                f'<h3>{SHORT[i]}</h3><p>{un(BANDS[i]["s"])}</p></a>')
    tiles = ''
    for i, b in enumerate(BANDS):
        tiles += (f'<a class="tile" href="/{DETAIL[str(i)]["slug"]}/"><div class="num">{i+1}</div>'
                  f'<h3>{un(b["n"])}</h3><p>{un(b["s"])}</p></a>')
    tiles += ('<a class="tile" href="/contact/" style="background:var(--blue);color:#fff;display:grid;align-content:center">'
              '<h3 style="color:#fff;font-size:1.1rem">Not sure which you need?</h3>'
              '<p style="color:#D2E0FF;margin-top:6px">Send the problem. We\'ll scope it.</p>'
              '<span style="color:var(--green);font-weight:700;margin-top:12px">Talk to us &#8594;</span></a>')
    slides = [
      ("Seven divisions, one contract",
       "One Partner.<br>A Spectrum of Solutions.",
       "From technology and professional training to energy and infrastructure, we help businesses and communities turn ideas into progress.",
       "/divisions/", "Explore our solutions"),
      ("People and capability",
       "Empower Your People.<br>Transform Your Business.",
       "Build skills, strengthen your brand and embrace smarter technology with training, business development and digital solutions.",
       "/training/", "Grow with us"),
      ("Infrastructure and sustainability",
       "Smarter Solutions.<br>A Sustainable Future.",
       "Build for tomorrow with renewable energy, integrated security, smart agriculture and property development solutions.",
       "/contact/", "Discuss your project"),
    ]
    sl = ""
    for k, (eyebrow, title, sub, href, label) in enumerate(slides):
        tag = "h1" if k == 0 else "div"
        sl += (f'<div class="slide{" on" if k==0 else ""}" data-slide="{k}">'
               f'<div class="eyebrow">{eyebrow}</div>'
               f'<{tag} class="htitle">{title}</{tag}>'
               f'<p class="sub">{sub}</p>'
               f'<div class="hero-actions">'
               f'<a class="pill" href="{href}">{label} <span class="dot">&#8599;</span></a>'
               f'</div></div>')
    dots = "".join(f'<button class="hdot{" on" if k==0 else ""}" data-go="{k}" '
                   f'aria-label="Slide {k+1}"><span>0{k+1}</span></button>' for k in range(len(slides)))
    cards = ""
    for j, i in enumerate([1, 2, 3, 6]):
        cards += (f'<a class="hcard{" hl" if j==0 else ""}" href="/{DETAIL[str(i)]["slug"]}/">'
                  f'<span class="ic"><i></i></span><h3>{SHORT[i]}</h3>'
                  f'<p>{un(BANDS[i]["s"])}</p></a>')

    body = f"""<section class="hero">
  {WAVES}
  <div class="hero-glow" aria-hidden="true"></div>
  <div class="wrap hero-inner">
    <div class="slides">{sl}</div>
    <div class="hdots">{dots}</div>
  </div>
</section>

<div class="hero-cards-zone">
  <div class="wrap"><div class="hero-cards">{cards}</div></div>
</div>

<div class="stats-zone" style="padding:56px 0 20px">
  <div class="wrap">
    <div class="stats">
      <div><div class="n" data-count="7">7</div><div class="l">Operating divisions</div></div>
      <div><div class="n" data-count="2">2</div><div class="l">Offices, Kaduna &amp; Abuja</div></div>
      <div><div class="n" data-count="4">4</div><div class="l">Federal partners</div></div>
      <div><div class="n">RC&nbsp;9113492</div><div class="l">Registered in Nigeria</div></div>
    </div>
  </div>
</div>

<section class="blue" style="padding-top:10px">
  <div class="wrap">
    <div class="help">
      <div class="help-copy">
        <h2>We're here<br>to help</h2>
        <p>One contract, one scope document, one name to call — across every trade a project touches.</p>
        <div class="person-slot"><b>Photo slot — team / site, 560&times;640</b></div>
      </div>
      <div class="svc">{svc}</div>
    </div>
    <p style="margin-top:28px"><a class="pill light" href="/divisions/">Explore all seven <span class="dot">&#8599;</span></a></p>
  </div>
</section>

<section>
  <div class="wrap">
    {sec_title('Our core <span style="color:var(--blue)">divisions</span>', "Each one delivers on its own, or combines into a single programme with one point of accountability.")}
    <div class="grid-4">{tiles}</div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    {sec_title("Why choose us", "Three commitments we put in writing on every engagement.")}
    <div class="why">
      <div class="b"><span class="ic"><i></i></span><h3>Scope before spend</h3><p>A site survey and written scope before anyone quotes a number. No procurement surprises.</p></div>
      <div class="b"><span class="ic"><i></i></span><h3>Built for handover</h3><p>Drawings, runbooks and training at completion, so your people can run it without us.</p></div>
      <div class="b"><span class="ic"><i></i></span><h3>We stay after</h3><p>Maintenance with defined response times and a named engineer who knows your site.</p></div>
    </div>
  </div>
</section>

<section style="background:var(--soft);padding-top:70px">
  <div class="wrap">
    <div class="center"><h2 style="font-size:clamp(1.8rem,3.6vw,2.6rem)">What clients say</h2></div>
    <div class="quotes">
      <div class="avatars">
        <span class="av" style="left:8%;top:14%"></span><span class="av" style="right:10%;top:8%"></span>
        <span class="av" style="left:14%;bottom:12%"></span><span class="av" style="right:16%;bottom:18%"></span>
      </div>
      <div class="qmark">&#8220;</div>
      <p class="quote-body">Placeholder quote. Replace with a real client statement — what was delivered, and what changed because of it.</p>
      <div class="who"><div class="pic"></div><b>Client name</b><span>Role, organisation</span></div>
      <div class="dots"><i></i><i></i><i></i></div>
    </div>
    <div class="trusted">
      <div class="l">Working alongside</div>
      <div class="orgs">
        <span>National Information Technology Development Agency</span>
        <span>Nigerian Youth Parliament</span>
        <span>Federal Ministry of Youth Development</span>
        <span>National Orientation Agency</span>
      </div>
    </div>
  </div>
</section>

{cta("Let's scope your project together", "Send the site, the problem and the timeline. We come back with an approach and an estimate.")}
"""
    return write('/', 'home', 'Universal Spectrum Solutions Ltd. — Seven sectors, one standard of delivery',
                 'Nigerian multi-sector company delivering ICT, renewable energy, security systems, media, agriculture, property development and capacity building from Kaduna and Abuja. RC 9113492.', body, 'home')

# ---------------- ABOUT ----------------
def about():
    vals = [("Scope before spend", "A site survey and a written scope before anyone quotes a number."),
            ("Documentation is a deliverable", "Drawings, credentials, runbooks and as-builts, produced as the work happens."),
            ("Open standards first", "No design that locks you to one supplier — including us."),
            ("Local capacity", "Training at handover so your own people run it day to day."),
            ("One point of accountability", "A single contract and a named lead from scope to handover."),
            ("We stay after", "Maintenance with defined response times and a named engineer.")]
    caps = ''.join(f'<div class="cap"><span class="d"></span><span><b>{t}</b><br><span style="color:var(--muted);font-weight:400;font-size:.9rem">{d}</span></span></div>' for t, d in vals)
    ppl = ''.join(f'<div class="person">{photo("Portrait — 600×700")}<div class="body">'
                  f'<h3>{un(p["n"])}</h3><div class="role">{un(p["r"])}</div><p>{un(p["d"])}</p></div></div>' for p in TEAM)
    body = banner("About the company", "A Nigerian company built for multi-sector delivery",
                  "Incorporated under RC 9113492, operating across seven sectors from Kaduna and Abuja.") + f"""
<section>
  <div class="wrap split">
    <div>
      <h2 style="font-size:clamp(1.8rem,3.6vw,2.6rem)">Why a company <span style="color:var(--blue)">this broad</span></h2>
      <p class="lede" style="margin:18px 0 0 0;max-width:none">Large projects rarely sit inside one trade. An estate needs power, security systems, connectivity and property management. A national programme needs content, production and distribution. The gaps between suppliers are where budgets and timelines are lost.</p>
      <p class="lede" style="margin:14px 0 0 0;max-width:none">We are structured to take responsibility across those boundaries — one contract, one scope document, one name to call.</p>
      <div class="hero-actions" style="justify-content:flex-start;margin-top:26px">
        <a class="pill" href="/divisions/">See the divisions <span class="dot">&#8599;</span></a>
      </div>
    </div>
    {img_block("about-overview.jpg", "A business professional reviewing project information on a tablet in an office lobby", 1140, 840, "about-overview-sm.jpg")}
  </div>
</section>

<section style="background:var(--soft)">
  <div class="wrap">
    {sec_title("What guides the work")}
    <div class="caps">{caps}</div>
  </div>
</section>

<section>
  <div class="wrap">
    {sec_title("Where we operate")}
    <div class="offices" style="grid-template-columns:1fr 1fr;display:grid;gap:16px">
      <div class="office"><span class="pin"><i></i></span><div><h3>Kaduna</h3><p>No. 3, Ahmadu Bello Way, P.O. Box 555, Kaduna, Kaduna State.<br><br>Engineering base and project staging for the North West.</p></div></div>
      <div class="office"><span class="pin"><i></i></span><div><h3>Abuja FCT</h3><p>Suite A8 - A9, HCR Plaza, 521 Sylvester Ugo Crescent, Opposite Police Pension Office, Jabi, Abuja — FCT.<br><br>Client liaison for federal agencies and corporates.</p></div></div>
    </div>
  </div>
</section>

<section id="leadership" style="background:var(--soft)">
  <div class="wrap">
    {sec_title("The people on your engagement", "Senior staff stay on a project from scope to handover. You will not be passed to a team you have never met.")}
    <div class="people">{ppl}</div>
  </div>
</section>

{cta("Want to work with us?", "Tell us what the project needs and we will come back with an approach.")}
"""
    return write('/about/', 'about', 'About — Universal Spectrum Solutions Ltd.',
                 'Universal Spectrum Solutions Limited (RC 9113492) — who we are, how we work, where we operate, and the leadership who run engagements from Kaduna and Abuja.', body)

# ---------------- DIVISIONS ----------------
def divisions():
    BEST = [
      "You already know what you need, and you want it specified, supplied and commissioned properly.",
      "The project crosses several trades and you want one contract, one programme and one name to call.",
      "The system matters too much to run unsupported once the installers have left site.",
    ]
    packs = ''
    for k, p in enumerate(PACKS):
        packs += (f'<div class="pack{" lead" if p.get("lead") else ""}">'
                  f'<div class="top"><h3>{un(p["n"])}</h3><div class="sub">{un(p["sub"])}</div></div>'
                  '<ul>' + ''.join(f'<li>{un(x)}</li>' for x in p['li']) + '</ul>'
                  f'<div class="best"><b>Best when</b>{BEST[k]}</div></div>')
    tiles = ''
    for i, b in enumerate(BANDS):
        tiles += (f'<a class="tile" href="/{DETAIL[str(i)]["slug"]}/"><div class="num">{i+1}</div>'
                  f'<h3>{un(b["n"])}</h3><p>{un(b["s"])}</p>'
                  f'<span style="color:var(--blue);font-weight:700;font-size:.88rem;display:inline-block;margin-top:12px">View division &#8594;</span></a>')
    body = banner("Capability detail", "Seven divisions, end to end",
                  "Each can be contracted on its own or combined into a single programme. Capabilities reflect our registered objects.") + f"""
<section>
  <div class="wrap"><div class="grid-4">{tiles}</div></div>
</section>

<section style="background:var(--soft)">
  <div class="wrap">
    {sec_title("Three ways to work with us", "Pick the level of responsibility you want us to carry.")}
    <div class="packs">{packs}</div>
    <div class="packs-foot">
      <span>Most engagements start as one of these and move up as the scope settles.</span>
      <a class="pill" href="/contact/">Send us the scope <span class="dot">&#8599;</span></a>
    </div>
  </div>
</section>

{cta("Not sure which divisions you need?", "Send us the problem. We will scope it and tell you what it actually takes.", "Request a scope")}
"""
    return write('/divisions/', 'divisions', 'Divisions — Universal Spectrum Solutions Ltd.',
                 'Seven operating divisions: training, ICT, renewable energy, security systems, media, agriculture and property development.', body)

def division(i):
    b, x = BANDS[i], DETAIL[str(i)]
    name = un(b['n'])
    caps = ''.join(f'<div class="cap"><span class="d"></span>{un(c)}</div>' for c in b['c'])
    steps = ''.join(f'<div class="step"><div class="num">{k+1}</div><h3>{s[0]}</h3><p>{s[1]}</p></div>'
                    for k, s in enumerate(x['steps']))
    clients = ''.join(f'<span>{un(c)}</span>' for c in x['clients'])
    intro = ''.join(f'<p class="lede" style="margin:16px 0 0 0;max-width:none">{t}</p>' for t in x['intro'])
    body = banner(f"Division {i+1} of 7", esc(x['tag']), un(b['d'])) + f"""
<section>
  <div class="wrap split">
    <div>
      <h2 style="font-size:clamp(1.7rem,3.4vw,2.5rem)">{name}</h2>
      {intro}
      <div class="hero-actions" style="justify-content:flex-start;margin-top:26px">
        <a class="pill" href="/contact/">Request a quote <span class="dot">&#8599;</span></a>
        <a class="pill ghost" href="/divisions/">All divisions</a>
      </div>
    </div>
    {photo(f"{name} photo — 760×560", "soft")}
  </div>
</section>

<section style="background:var(--soft)">
  <div class="wrap">
    {sec_title("What this division covers")}
    <div class="caps">{caps}</div>
  </div>
</section>

<section>
  <div class="wrap">
    {sec_title("How an engagement runs", "Four stages, each ending in something written you can review before the next begins.")}
    <div class="steps">{steps}</div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    {sec_title("Who we work with here")}
    <div class="pillrow">{clients}</div>
  </div>
</section>

{workshops_block() if i == 0 else ""}{nsq_block() if i == 0 else ""}
{cta(f"Need {name.lower()} on a project?", "Send the site, the scope and the timeline. We respond with an approach and an estimate.")}
"""
    desc = ('Workshops on misinformation and hate speech, local government revenue generation, '
            'cybersecurity and technical systems, plus NSQ Creative Media Production Levels 1-3.') if i == 0 else un(b['d'])[:155]
    return write(f'/{x["slug"]}/', x['slug'], f'{name} — Universal Spectrum Solutions Ltd.',
                 un(b['d'])[:155], body)



WORKSHOPS = [
 {"t":"Curbing Fake News, Hate Speech, Misinformation and Disinformation",
  "d":"For agencies, newsrooms, schools and community organisations whose work depends on public trust. How false and inflammatory content spreads, how to recognise it, and how to communicate responsibly once it has.",
  "topics":[]},
 {"t":"Strategies for Improving Revenue Generation in Local Government Councils",
  "d":"For council leadership and finance teams, covering the structures and procedures that decide what a council can raise, retain and spend.",
  "topics":["Local Government Autonomy","Budget and Budgetary Procedures","Separation of Powers"]},
 {"t":"Cybersecurity and Technical Systems",
  "d":"Hands-on training for the staff who operate and maintain institutional systems, delivered by the same engineers who install them.",
  "topics":["Cybersecurity","Computer Appreciation","Fire Fighting Systems","Surveillance Systems Installation and Monitoring"]},
]

def workshops_block():
    cards = ""
    for k, w in enumerate(WORKSHOPS):
        chips = ""
        if w["topics"]:
            chips = ('<div class="wtopics">' +
                     "".join(f'<span>{t}</span>' for t in w["topics"]) + '</div>')
        cards += (f'<div class="wcard"><span class="wnum">{k+1}</span>'
                  f'<h3>{w["t"]}</h3><p>{w["d"]}</p>{chips}</div>')
    return f"""<section>
  <div class="wrap">
    {sec_title("Workshops and short courses",
               "Commissioned programmes we run for institutions, councils and corporate teams. Each is scoped to the audience and the outcome, delivered on site or at our facilities, and reported on afterwards.")}
    <div class="wgrid">{cards}</div>
    <p class="lede" style="text-align:center;margin-top:28px">
      Need a programme that is not listed? We design to a brief &mdash;
      <a href="/contact/" style="color:var(--blue);font-weight:500">tell us the audience and the outcome</a>.
    </p>
  </div>
</section>

"""

# ---------------- NSQ Creative Media Production (Training division) ----------------
NSQ_LEVELS = [
 {"n":"1","tag":"Foundation","units":10,"credits":26,"glh":260,
  "aim":"Work safely on a production, operate a camera and basic sound kit, use design software, and understand how digital media is made and distributed.",
  "list":["Occupational Health and Safety","Teamwork","Communication Skills",
          "Computer Appreciation and Application","Introduction to Performance Art",
          "Introduction to Graphics Design","Basics of Film Making",
          "Introduction to Basic Photography","Introduction to Sound Techniques","Digital Media"]},
 {"n":"2","tag":"Intermediate","units":10,"credits":26,"glh":260,
  "aim":"Light a scene, shoot video, work through a film production, build a story in sequential art, and edit the result.",
  "list":["Occupational Health and Safety","Communication Skills","Teamwork",
          "Computer Skills and Knowledge","Basic Photography","Understanding the Basics of Light",
          "Introduction to Videography","Techniques of Film Production",
          "Introduction to Illustration and Sequential Arts","Introduction to Video Editing"]},
 {"n":"3","tag":"Advanced","units":"8 + 3 optional","credits":27,"glh":"—",
  "aim":"Run a production as a project: direct, light, edit, engineer sound and manage the client relationship from pre-production to delivery.",
  "list":["Introduction to Project Management","Customer Service","Pre-Production Operation",
          "Internet Use and Procedure","Video Editing","Fundamentals of Film Directing",
          "Fundamentals of Lighting Techniques","Sound Engineering Techniques"],
  "opt":["Fundamentals of Scriptwriting","Photography","2D Animation Production"]},
]

def nsq_block():
    blocks = ""
    for L in NSQ_LEVELS:
        caps = "".join(f'<div class="cap"><span class="d"></span>{u}</div>' for u in L["list"])
        opt = ""
        if L.get("opt"):
            opt = ('<div class="opt-label">Optional units</div><div class="caps">' +
                   "".join(f'<div class="cap"><span class="d"></span>{u}</div>' for u in L["opt"]) +
                   '</div>')
        blocks += f"""<div class="level">
  <div class="level-head">
    <span class="level-badge">Level {L["n"]}</span>
    <div class="level-title"><h3>{L["tag"]}</h3><p>{L["aim"]}</p></div>
    <dl class="level-meta">
      <div><dt>Units</dt><dd>{L["units"]}</dd></div>
      <div><dt>Credits</dt><dd>{L["credits"]}</dd></div>
      <div><dt>Learning hours</dt><dd>{L["glh"]}</dd></div>
    </dl>
  </div>
  <div class="caps">{caps}</div>
  {opt}
</div>"""
    return f"""<section style="background:var(--soft)">
  <div class="wrap">
    {sec_title("Accredited workshops &mdash; NSQ Creative Media Production",
               "We deliver the National Skills Qualification in Creative Media Production, the national standard set by the National Board for Technical Education. Three progressive levels, each assessed on real production work rather than on paper.")}
    {blocks}
    <div class="note" style="margin-top:28px">
      <b>How learners are assessed.</b> Assessment happens in a working production
      environment, through direct observation, oral questioning, witness testimony,
      personal statements or reflective practice, and assignments. Simulation is
      permitted for health and safety units at the lower levels. Each unit is signed
      off by the learner and assessor, with internal and external quality assurance
      sampling.
    </div>
  </div>
</section>

"""

# ---------------- LIST PAGES ----------------
def entry(meta, title, text, tags=None):
    t = ('<div class="chips">' + ''.join(f'<span>{un(x)}</span>' for x in tags) + '</div>') if tags else ''
    return f'<div class="entry"><div class="meta">{meta}</div><div><h3>{un(title)}</h3><p>{un(text)}</p>{t}</div></div>'

def projects():
    rows = ''.join(entry(f'<b>{un(p["c"])}</b>{un(p["m"])}<br>{un(p["dv"])}', p['t'], p['d'], p['g']) for p in PROJECTS)
    body = banner("Our work", "Selected engagements",
                  "A sample of recent and ongoing work. Full references available on request for tender submissions.") + \
        f'<section><div class="wrap"><div class="entries">{rows}</div></div></section>' + \
        cta("Have a similar project?", "Tell us the scope and we will come back with an approach and an estimate.")
    return write('/projects/', 'projects', 'Projects — Universal Spectrum Solutions Ltd.',
                 'Selected engagements across our seven divisions, including the Youth Leadership Engagement Summit convened with federal partners.', body)

def news():
    rows = ''.join(entry(f'<b>{un(p["m"])}</b>', p['t'], p['d']) for p in NEWS)
    body = banner("Newsroom", "News and updates",
                  "Project milestones, programme announcements and notes on how we build.") + \
        f'<section><div class="wrap"><div class="entries">{rows}</div></div></section>'
    return write('/news/', 'news', 'News — Universal Spectrum Solutions Ltd.',
                 'Project milestones and programme announcements from Universal Spectrum Solutions Limited.', body)

def careers():
    rows = ''.join(entry(f'<b>{un(p["m"])}</b>', p['t'], p['d']) for p in JOBS)
    body = banner("Careers", "Build things that get used",
                  "We hire engineers, technicians and programme staff across all seven divisions.") + f"""
<section>
  <div class="wrap">
    {sec_title("Open roles")}
    <div class="entries">{rows}</div>
    <div class="note" style="margin-top:26px"><b>Nothing listed that fits?</b> Send a CV and a note on what you build. We keep strong applications on file and contact people when a project starts. Email <a href="mailto:universalspectrumsolutionsltd@gmail.com">universalspectrumsolutionsltd@gmail.com</a>.</div>
  </div>
</section>"""
    return write('/careers/', 'careers', 'Careers — Universal Spectrum Solutions Ltd.',
                 'Open roles for engineers, technicians and programme staff across our seven divisions in Kaduna and Abuja.', body)

def team():
    ppl = ''.join(f'<div class="person">{photo("Portrait — 600×700")}<div class="body">'
                  f'<h3>{un(p["n"])}</h3><div class="role">{un(p["r"])}</div><p>{un(p["d"])}</p></div></div>' for p in TEAM)
    body = banner("Leadership", "The people on your engagement",
                  "Senior staff stay on a project from scope to handover.") + \
        f'<section><div class="wrap"><div class="people">{ppl}</div></div></section>'
    return write('/team/', 'team', 'Team — Universal Spectrum Solutions Ltd.',
                 'The leadership and senior staff who run engagements at Universal Spectrum Solutions Limited.', body)

def partners():
    orgs = ["National Information Technology Development Agency", "Nigerian Youth Parliament",
            "Federal Ministry of Youth Development", "National Orientation Agency"]
    cells = ''.join(f'<div>{o}</div>' for o in orgs)
    body = banner("Collaboration", "We work alongside institutions",
                  "Agencies and ministries we have collaborated with or delivered programmes alongside.") + f"""
<section>
  <div class="wrap">
    <div class="logos">{cells}</div>
    <p class="lede" style="margin-top:30px;text-align:center">Partner and client marks are added here as permissions are confirmed.</p>
  </div>
</section>
{cta("Partner with us", "We take on joint ventures, consortium bids and subcontracts where the scope fits our divisions.", "Open a conversation")}"""
    return write('/partners/', 'partners', 'Partners — Universal Spectrum Solutions Ltd.',
                 'Agencies and ministries we have collaborated with, including NITDA, the Nigerian Youth Parliament and the National Orientation Agency.', body)

def contact():
    opts = ''.join(f'<option>{un(b["n"])}</option>' for b in BANDS) + '<option>Not sure yet</option>'
    body = banner("Get in touch", "Tell us the scope",
                  "Reach either office directly, or send the brief and we will respond with an approach.") + f"""
<section>
  <div class="wrap split" style="align-items:start">
    <div>
      <h2 style="font-size:1.6rem;margin-bottom:18px">Our offices</h2>
      <div class="offices">
        <div class="office"><span class="pin"><i></i></span><div><h3>Kaduna Office</h3><p>No. 3, Ahmadu Bello Way<br>P.O. Box 555, Kaduna, Kaduna State</p></div></div>
        <div class="office"><span class="pin"><i></i></span><div><h3>Abuja Office</h3><p>Suite A8 - A9, HCR Plaza, 521 Sylvester Ugo Crescent<br>Opposite Police Pension Office, Jabi, Abuja — FCT</p></div></div>
        <div class="office"><span class="pin"><i></i></span><div><h3>Direct lines</h3><p><a href="tel:+2347048223500">0704 822 3500</a><br><a href="tel:+2348091379774">0809 137 9774</a><br><a href="mailto:universalspectrumsolutionsltd@gmail.com">universalspectrumsolutionsltd@gmail.com</a></p></div></div>
        <div class="office"><span class="pin"><i></i></span><div><h3>Company</h3><p>Universal Spectrum Solutions Limited<br>RC 9113492 — Registered in Nigeria</p></div></div>
      </div>
    </div>
    <div>
      <h2 style="font-size:1.6rem;margin-bottom:18px">Send a brief</h2>
      <form name="brief" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="/thanks/">
        <input type="hidden" name="form-name" value="brief">
        <p hidden><label>Leave blank: <input name="bot-field"></label></p>
        <div class="f2">
          <div><label for="n">Your name</label><input id="n" name="name" required></div>
          <div><label for="o">Organisation</label><input id="o" name="organisation"></div>
        </div>
        <div class="f2">
          <div><label for="e">Email</label><input id="e" name="email" type="email" required></div>
          <div><label for="p">Phone</label><input id="p" name="phone" type="tel"></div>
        </div>
        <div><label for="d">Which division?</label><select id="d" name="division">{opts}</select></div>
        <div><label for="m">Brief</label><textarea id="m" name="message" placeholder="Scope, site, timeline, budget range if known." required></textarea></div>
        <button class="pill" type="submit" style="justify-self:start">Send brief <span class="dot">&#8599;</span></button>
      </form>
    </div>
  </div>
</section>"""
    return write('/contact/', 'contact', 'Contact — Universal Spectrum Solutions Ltd.',
                 'Kaduna and Abuja offices, direct lines and a project brief form. Universal Spectrum Solutions Limited, RC 9113492.', body)

def thanks():
    body = banner("Received", "Thank you — we have your message",
                  "We respond within two working days. If it is urgent, call 0704 822 3500.") + \
        '<section><div class="wrap" style="text-align:center"><a class="pill" href="/">Back to home <span class="dot">&#8599;</span></a></div></section>'
    return write('/thanks/', '', 'Thank you — Universal Spectrum Solutions Ltd.', 'Your message has been received.', body)

def notfound():
    body = banner("404", "That page does not exist",
                  "The link may be out of date. Try the divisions index or get in touch.") + \
        '<section><div class="wrap" style="text-align:center"><a class="pill" href="/">Back to home <span class="dot">&#8599;</span></a> <a class="pill ghost" href="/divisions/">All divisions</a></div></section>'
    doc = head('Page not found — Universal Spectrum Solutions Ltd.', 'Page not found.', '/404/') \
          + header('') + body + FOOTER
    (OUT / '404.html').write_text(doc)

# ---------------- run ----------------
urls = [home(), about(), divisions(), projects(), news(), partners(), careers(), contact()]
for i in range(7):
    urls.append(division(i))
thanks(); notfound()

sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    pr = '1.0' if u == '/' else ('0.8' if u in ('/divisions/', '/contact/') else '0.6')
    sm.append(f'  <url><loc>{SITE}{u}</loc><changefreq>monthly</changefreq><priority>{pr}</priority></url>')
sm.append('</urlset>')
(OUT / 'sitemap.xml').write_text('\n'.join(sm))
(OUT / 'robots.txt').write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
(OUT / 'netlify.toml').write_text("""[build]
  publish = "."

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "SAMEORIGIN"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

# the generator ships in the repo so the site can be rebuilt, but it has no
# business being fetchable over HTTP
[[redirects]]
  from = "/src/*"
  to = "/404.html"
  status = 404

[[redirects]]
  from = "/team/"
  to = "/about/#leadership"
  status = 301

[[headers]]
  for = "/css/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/js/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
""")
print(f'{len(urls)} pages + thanks + 404')
print(', '.join(urls))
