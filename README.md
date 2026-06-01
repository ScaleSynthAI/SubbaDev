# subba.dev — Personal Portfolio & Blog Stack

The self-hosted personal portfolio, writing platform, and resume center for **Subba Taniparti**, Lead AI Engineer based in Raleigh-Durham, NC. 

Designed under a strict **low-chrome, invisible design philosophy** to maximize technical signal per pixel for recruiters, the site compiles into a static, high-performance web asset bundle and hosts securely on local Proxmox hardware.

---

## Technical Architecture Overview

- **Static Engine**: Pelican (Python-based static site generator) with custom pure Jinja2 templates.
- **Visual Styles**: Less than 200 lines of highly optimized Vanilla CSS featuring automated system dark mode (`prefers-color-scheme`) and pixel-perfect physical print styles.
- **Self-Hosted Assets**: Zero Google Fonts calls or tracking CDNs. Subsetted WOFF2 fonts (**Source Serif 4**, **Inter**, **JetBrains Mono**) are fetched programmatically and bundled locally.
- **Dynamic Data Binding**: Resume contents are parsed from a master `.docx` resume and exported to structured `resume.json`. Pelican maps this data into templates at compile time, eliminating double-maintenance and hardcoded visual states.
- **Deployment Grid**: Multi-stage `Dockerfile` creating a high-performance, security-hardened `nginx:alpine` container.Exposed to the public via egress-only **Cloudflare Tunnels** (`cloudflared`) and managed on a home **Proxmox cluster** via **Komodo**.

---

## Directory Structure

```
.
├── build_resume.py           # Docx parsing engine (outputs resume.json)
├── download_fonts.py         # Programmatic WOFF2 asset bootstrapper
├── generate_social_card.py   # Pillow-based OpenGraph image generator
├── pelicanconf.py            # Local/dev configuration settings
├── publishconf.py            # Production site settings (enforces https://subba.dev)
├── requirements.txt          # Python dependencies
├── nginx.conf                # Gzip, Cache-Control, and CSP security rules
├── Dockerfile                # Multi-stage compilation & serve build
├── docker-compose.yml        # Multi-container local orchestration (Web + Tunnel)
├── cloudflared.config.yml    # Secure egress hostname router
├── komodo.toml               # Proxmox / Komodo CI deployment manifest
├── content/
│   ├── data/
│   │   ├── resume.json       # Parsed resume JSON data payload
│   │   └── projects.json     # Exhaustive project details for recruiter review
│   ├── pages/
│   │   ├── cv.md             # Maps `/cv/` page to cv.html template
│   │   └── projects.md       # Maps `/projects/` page to projects.html template
│   ├── posts/                # Seeded deep technical Markdown blog posts
│   └── cv/
│       └── SubbaTaniparti.pdf # CV PDF download payload
└── themes/
    └── subba/                # Custom structural theme
        ├── templates/        # Jinja2 layouts (base, index, article, cv, etc.)
        └── static/
            ├── css/style.css # Strict visual design system and custom tokens
            └── fonts/        # Local self-hosted font files
```

---

## Local Development & Setup

### 1. Initialize Virtual Environment and Dependencies

Create a local Python virtual environment and install the required build packages:

```bash
# Create and activate environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 2. Run the Extractor & Asset Generation

Before running compilation, trigger the parsing and bootstrapping scripts:

```bash
# 1. Parse SubbaTaniparti.docx into content/data/resume.json
python build_resume.py

# 2. Fetch and package the local subsetted webfonts
python download_fonts.py

# 3. Create the minimalist OpenGraph preview image (social_share.png)
python generate_social_card.py
```

### 3. Local Compilation and Live Preview

Compile the site and boot the lightweight local Pelican dev server:

```bash
# Compile using local relative paths
pelican content -o output -s pelicanconf.py

# Launch development preview server
pelican -l -p 8000
```

Open your browser and navigate to **`http://localhost:8000`** to review. To enable hot-reloading for writing draft posts, use `pelican -r` alongside the server.

---

## Production Deployment

### 1. Multi-Stage Docker Container

The included Dockerfile completely automates environment setup, dependency resolution, parsing, font downloading, OpenGraph rendering, sitemap generation, and Nginx compilation:

```bash
# Build and run the local production stack
docker compose up --build -d
```

This starts the `subba-web` Nginx container and the `cloudflared-tunnel` egress daemon inside an isolated internal Docker bridge network.

### 2. Cloudflare Tunnel Configuration

1. Expose your tunnel credentials inside `tunnel-credentials.json` on the host machine.
2. In `cloudflared.config.yml`, replace `YOUR_CLOUDFLARE_TUNNEL_UUID` with your specific tunnel ID.
3. Establish your public hostnames (`subba.dev`, `www.subba.dev`) inside the Cloudflare dashboard and link them to your tunnel. No incoming router ports (80/443) are required!

### 3. Komodo Orchestrator

The site is natively configured to integrate with the **Komodo stack orchestrator**. The `komodo.toml` config handles automated build updates and continuous deployments on your Proxmox cluster:

- Deploy the stack on Komodo pointing to this repository.
- Ensure `tunnel-credentials.json` is mapped via Komodo's volume mounting rules.
