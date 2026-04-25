# personal-site

Personal brand one-pager. Static HTML + FastAPI contact endpoint.

## Sitemap rule

Whenever any file in this project is modified, update the `<lastmod>` date in `sitemap.xml` to today's date (YYYY-MM-DD format).

```xml
<!-- sitemap.xml -->
<lastmod>YYYY-MM-DD</lastmod>
```

## Structure

- `index.html` — single-page site (hero, about, skills, projects, experience, contact)
- `robots.txt` — allows search engines, blocks AI training scrapers
- `llms.txt` — permissive, promotional content for LLM recommendation
- `sitemap.xml` — single URL sitemap
- `site.webmanifest` — PWA manifest
- `favicon.svg` — cyan "S" monogram
- `.well-known/security.txt` — security contact

## Domain

Production domain: `oresam.xyz`
Static files served from `/var/www/oresam.xyz` via nginx on the production server (157.90.149.209).
