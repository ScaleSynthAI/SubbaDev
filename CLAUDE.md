# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Personal portfolio and blog for Subba Taniparti (subba.dev). Built with **Pelican** (Python static site generator), custom Jinja2 templates, and self-hosted fonts. Deployed as a Docker/Nginx container via Cloudflare Tunnels on a home Proxmox cluster.

## Development Commands

All dev commands go through `dev.sh`. Activate the venv first or let the script handle it.

```bash
./dev.sh              # Full pipeline: extract → compile → open browser → hot-reload server
./dev.sh setup        # Bootstrap venv + pip install -r requirements.txt
./dev.sh extract      # Parse .docx resume, fetch fonts, generate social card
./dev.sh compile      # Pelican build only (uses pelicanconf.py for local relative paths)
./dev.sh serve        # Launch local preview at http://localhost:8000
./dev.sh dev          # extract + compile + hot-reload server
```

Manual equivalents:
```bash
source venv/bin/activate
python build_resume.py          # Regenerate content/data/resume.json from SubbaTaniparti.docx
python download_fonts.py        # Re-fetch WOFF2 fonts into themes/subba/static/fonts/
python generate_social_card.py  # Rebuild output/images/social_share.png
pelican content -o output -s pelicanconf.py   # Local build
pelican -r -l -p 8000                          # Hot-reload dev server
```

Production Docker build (port 8090):
```bash
docker compose up --build -d
```

## Architecture

### Data Flow

```
SubbaTaniparti.docx
    └── build_resume.py → content/data/resume.json
                                └── pelicanconf.py loads it as RESUME_DATA
                                        └── themes/subba/templates/cv.html renders it

content/data/projects.json → PROJECTS_DATA → themes/subba/templates/projects.html
content/posts/*.md → themes/subba/templates/article.html (writing section)
```

### Two Pelican Configs

- `pelicanconf.py` — `SITEURL = ''` (blank = root-relative links for local and LAN IP access)
- `publishconf.py` — `SITEURL = 'https://subba.dev'` + `DELETE_OUTPUT_DIRECTORY = True`; imports from pelicanconf

The Dockerfile uses `publishconf.py`; local dev uses `pelicanconf.py`.

### Theme Structure

`themes/subba/` is a pure Jinja2 theme:
- `templates/base.html` — layout shell, nav, footer, font loading
- `templates/cv.html` — renders RESUME_DATA; has `@media print` styles for PDF export
- `templates/projects.html` — renders PROJECTS_DATA
- `templates/article.html` / `archives.html` — writing/blog
- `static/css/style.css` — ~200 lines, CSS custom properties only, no framework
- `static/fonts/` — self-hosted WOFF2 (Source Serif 4, Inter, JetBrains Mono)

### URL Structure

| Page | URL |
|------|-----|
| Home | `/` |
| Writing index | `/writing/` |
| Single post | `/writing/{slug}/` |
| CV | `/cv/` |
| Projects | `/projects/` |
| RSS | `/feed.xml` |

Tags, categories, authors pages are all disabled in config.

## Key Files to Know

- `content/data/resume.json` — **do not hand-edit**; regenerate via `build_resume.py`
- `content/data/projects.json` — manually maintained project list
- `content/posts/` — Markdown blog posts; Pelican standard frontmatter (`Title`, `Date`, `Tags`, `Summary`)
- `nginx.conf` — gzip, cache headers, CSP; served in production container
- `cloudflared.config.yml` — Cloudflare Tunnel config; requires `tunnel-credentials.json` (not in repo)
- `komodo.toml` — Komodo stack orchestrator config for Proxmox deployment

## Design Constraints

- No external CDN calls, no Google Fonts — all assets self-hosted
- No JS frameworks; vanilla CSS with `prefers-color-scheme` for dark mode
- Container width 720px max; line length 68ch
- `@media print` block on CV page renders cleanly for PDF export by recruiters
- All internal links must be root-relative (e.g., `/writing/` not `./writing/`) to work under both `localhost:8000` and LAN IP (e.g., `192.168.x.x:8090`)
