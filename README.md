# oresam.xyz

Personal brand site for Samuel O'Regan — founding engineer, AI-native builder, and agentic systems specialist based in Cape Town, South Africa.

## Stack

- **Frontend** — single-page HTML/CSS/JS, no framework, no build step
- **Fonts** — Rajdhani + Share Tech Mono via Google Fonts
- **Projects** — fetched live from the GitLab API on page load
- **Contact** — mailto link
- **Theme** — dark cyber aesthetic matching the [job-agent](https://gitlab.com/portfolio2112240/job-agent) dashboard

## Structure

```
index.html          # full site (hero, about, skills, projects, experience, contact)
robots.txt          # allows search crawlers, blocks AI training bots
llms.txt            # permissive content for LLM recommendation
sitemap.xml         # single-URL sitemap
site.webmanifest    # PWA manifest
favicon.svg         # cyan monogram
humans.txt          # attribution
.well-known/
  security.txt      # security contact
backend/
  main.py           # FastAPI contact endpoint (unused — replaced with mailto)
  requirements.txt
  .env.example
```

## Running locally

```bash
python3 -m http.server 3456
# open http://localhost:3456
```

## Deploy

Static files served from `oresam.xyz`. No build step required — push and serve.
