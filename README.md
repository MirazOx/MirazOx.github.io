# mirazhossain.com — full site

Static website for Miraz Hossain. The current information architecture keeps the public navigation focused on Research, Academic, Reportage, Interventions, and About, with services, credentials, projects, and the personal "Beyond the work" room tucked into those sections.

## What's inside

```
mirazhossain-site/
├── index.html            Homepage
├── 404.html              Legacy redirect helper for old .html URLs
├── .htaccess             HTTPS/canonical-domain rules for Apache hosting
├── research/             All research projects
├── writing/              10 selected features + bylines
├── archive/              Searchable archive of published articles
├── academic/             Coursework and papers
├── interventions/        Trainings, workshops, community work + project shelf
├── about/                Bio hub with services, credentials, CV, contact
├── beyond/               Hidden personal room linked from About
├── credentials/          Detail page for certifications
├── services/             Detailed services sheet linked from About
├── projects/             Standalone project pages
├── docs/                 Setup notes and maintainer documentation
├── scripts/              Utility scripts and Apps Script snippets
├── assets/
│   ├── css/style.css     Shared stylesheet
│   ├── js/partials.js    (optional) shared nav/footer injector
│   └── images/           
├── content/              ← Edit these JSON files to update the site
│   ├── articles.json     223 published pieces
│   ├── certificates.json 75 certifications
│   ├── writing-selected.json  10 featured writings
│   ├── research.json     Research projects
│   ├── academic.json     Academic papers
│   └── services.json     Services offered
├── pdfs/
│   ├── miraz_cv.pdf
│   ├── miraz_cv_one_page.pdf
│   ├── advanced-english-writing-feature-layout.pdf
│   ├── algorithmic-news-feeds.pdf
│   ├── writing-without-writing-v6.pdf
│   ├── team-data-decoder.pdf
│   ├── campus-leader-english-olympiad.pdf
│   ├── comm-research-paper.docx
│   └── writing-without-writing-research-proposal.docx
```

## How to update content

Every dynamic section is driven by a JSON file in `content/`. Adding an article or certificate means editing one JSON file — no HTML changes needed.

**Add a new article:** open `content/articles.json`, add an object like:
```json
{
  "title": "Your new piece title",
  "date": "2026-05-01",
  "link": "https://...",
  "outlet": "The Business Standard"
}
```

**Add a new certificate:** open `content/certificates.json`:
```json
{
  "title": "Certificate name",
  "issuer": "Coursera / University X",
  "date": "May 01, 2026",
  "theme": "Research & Data"
}
```

Known themes: `Journalism & Fact-Checking`, `Research & Data`, `Science, Data & Technology`, `English Language & Communication`, `Career Development & Productivity`, `Project Management & Leadership`, `Negotiation & Conflict Resolution`, `Philosophy, Religion & Ethics`, `Psychology & Mental Health`, `Business & Economics`, `Language Learning`, `Awards & Recognition`. New themes will appear automatically at the bottom of the `/credentials/` page.

## Local preview

The site uses `fetch()` to load JSON, so opening the HTML directly via `file://` won't show the dynamic content. Either:

1. **Quick preview** — from this folder, run:
   ```
   python -m http.server 8000
   ```
   then open http://localhost:8000

2. **Or just upload it to ExonHost** — everything works as soon as it's on a real web server.

## Deploy to ExonHost

Two options:

**Option A — File Manager (easiest)**
1. Log into your ExonHost cPanel.
2. Open **File Manager** → navigate to `public_html/`.
3. (Optional) Back up your existing files first — download them as a ZIP from File Manager.
4. Upload the `mirazhossain-site.zip` into `public_html/`.
5. Right-click the ZIP → **Extract** → extract directly into `public_html/` (or a subfolder if you want to keep the old site temporarily).
6. If extracted into a subfolder, move the files up one level or update your domain root.
7. Visit mirazhossain.com — you should see the new site.

**Option B — FTP**
Use FileZilla or similar. Connect with the FTP credentials from your ExonHost welcome email. Upload all files from this folder into `public_html/`.

## Keeping the old site as a fallback

While testing, you can deploy the new site to a subfolder like `public_html/new/` and view it at `mirazhossain.com/new/` — once you're happy, move it to the root.
