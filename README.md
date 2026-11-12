# Universal Spectrum Solutions Ltd. — website

Static site for Universal Spectrum Solutions Limited (RC 9113492). Sixteen pages,
no framework, no build step required to deploy.

Currently live at <https://universal-spectrum-solutions.netlify.app>

---

## How this repo is laid out

```
/                 the deployable site — HTML at the root, ready to serve as-is
  index.html        home
  about/            about + leadership
  divisions/        all seven divisions
  training/         Training & Capacity Building (workshops + NSQ levels)
  ict/ energy/ security/ media/ environment/ property/
  projects/ news/ partners/ careers/ contact/ thanks/
  404.html
  css/ js/ assets/
  sitemap.xml robots.txt
  netlify.toml      Netlify config (headers, redirects)
  vercel.json       Vercel config (same rules, Vercel's format)
src/
  build.py          generates every page
  data.json         the content — divisions, projects, news, team, jobs
```

**The HTML in this repo is generated.** Editing a page by hand works, but the
next build overwrites it. For anything structural, change `src/` and rebuild.

## Editing content

Most copy lives in two places:

| What | Where |
|---|---|
| Division names, descriptions, capability lists, process steps, client types | `src/data.json` |
| Page layout, workshops, NSQ levels, hero slides, engagement models | `src/build.py` |
| All styling | `css/style.css` |
| Animations, slider, mobile menu | `js/script.js` |

Rebuild after any change to `src/`:

```bash
python3 src/build.py
```

No dependencies — standard library only. It rewrites every page, the sitemap
and `robots.txt`.

### Cache fingerprints

`css/style.css` and `js/script.js` are the files you edit. The build copies each
to a content-hashed name (`style.<hash>.css`) and points the HTML at that, because
the cache headers tell browsers to keep those files for a year. **If you edit CSS
or JS by hand and skip the build, nobody will see the change.** Always rebuild.

### Changing the domain

Edit `SITE` at the top of `src/build.py`, then rebuild. That updates the canonical
tags, Open Graph URLs, `sitemap.xml` and `robots.txt` together. Do this before
submitting the sitemap to Google Search Console.

## Deploying

### Netlify

Connect this repo under **Add new site → Import an existing project**.

| Setting | Value |
|---|---|
| Build command | *(leave empty)* |
| Publish directory | `.` |

`netlify.toml` handles headers and the `/team/` redirect. Every push to `main`
deploys automatically.

**Forms** are Netlify-specific: the contact form on `/contact/` uses
`data-netlify="true"`. Netlify detects it during deploy and submissions land under
the site's **Forms** tab. Set up an email notification there so enquiries actually
reach someone.

### Vercel

Import the repo and accept the defaults — no build command, output directory `.`.
`vercel.json` carries the equivalent headers and redirect.

**The contact form will not work on Vercel.** Netlify Forms is a Netlify feature.
On Vercel you need a form service (Formspree, Basin) or a serverless function.
Change the `<form>` in `src/build.py` accordingly.

### Custom domain

Point the domain at whichever host you choose, then update `SITE` in
`src/build.py` and rebuild so the metadata matches. Both hosts issue HTTPS
certificates automatically once DNS resolves.

## Still to do before this is finished

- **Photography.** 19 slots remain as labelled placeholders — hero, division
  overviews, CTA panels, three leadership portraits. Search the HTML for
  `class="photo"`. The About overview is the only real image so far.
- **Testimonials.** Two placeholder quotes on the home page. Replace with real
  client statements and get permission to publish them.
- **Projects.** Only the Youth Leadership Engagement Summit is real; four entries
  are marked Placeholder.
- **Leadership.** Only Ja'afar Bala Farouq is real; two slots are empty.
- **Careers.** All three roles are invented. Delete the page if USSL is not hiring.
- **NSQ accreditation.** `/training/` states that USSL delivers the National
  Skills Qualification in Creative Media Production. Confirm accreditation status
  with NBTE before this goes in front of a procurement officer.
- **Level 3 credits.** The NBTE document contradicts itself (a stated 30-credit
  minimum against units totalling 27 mandatory + 9 optional). The site uses the
  figure from the unit table. Worth confirming.
- **Engagement models.** Supply & Install / Turnkey / Managed Programme is a
  proposal, not confirmed company practice.
- **Social links.** The footer social row is hidden while all URLs are empty in
  `SOCIAL` in `src/build.py`. Add a real profile URL and its icon appears.

## Company details

Universal Spectrum Solutions Limited — RC 9113492, registered in Nigeria.

- **Kaduna** — No. 3, Ahmadu Bello Way, P.O. Box 555, Kaduna, Kaduna State
- **Abuja** — Suite A8 - A9, HCR Plaza, 521 Sylvester Ugo Crescent, Opposite
  Police Pension Office, Jabi, Abuja — FCT
- 0704 822 3500 · 0809 137 9774
- universalspectrumsolutionsltd@gmail.com

The seven divisions come from the company's registered objects.

## Design

| Token | Hex | Use |
|---|---|---|
| Blue | `#296AFF` | Primary — buttons, links, highlights |
| Orange | `#FD613F` | Accent |
| Green | `#A2D974` | Accent |
| Yellow | `#FFD84D` | Footer headings |
| Black | `#000000` | Footer |
| Deep navy | `#040D22` → `#0A255E` | Hero and banner gradient |

Poppins throughout — 600/700 headings, 400/500 body and buttons.

The hero and every inner banner run an animated contour-wave field drawn on
canvas (`js/script.js`), paused when offscreen or the tab is hidden, and reduced
to a single static frame under `prefers-reduced-motion`.
