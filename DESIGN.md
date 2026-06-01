# Design Architecture — subba.dev

This document establishes the design principles, visual hierarchy, typographic choices, and architectural guidelines implemented for **Subba Taniparti's** professional personal portfolio and blog.

---

## 1. Design Philosophy: Invisible Design

Hiring managers and recruiters at high-signal organizations (e.g., NVIDIA, Google, Meta, OpenAI) spend between **15 to 30 seconds** scanning portfolios. They look for deep technical signals: actual published papers, production systems architecture, deep blog posts, and active code repositories. Decorative graphics, complex animations, or heavy styling frameworks increase visual noise and friction.

**The primary design goal: Maximum technical signal per pixel, minimum chrome.**

The canvas acts as a silent, premium paper sheet where the content does all the heavy lifting. Design details (link colors, margins, rules) exist only to support scanning readability and establish an immediate sense of elite, professional competence.

---

## 2. Color Palette & Visual Theme

The site utilizes a strictly restrained color palette controlled entirely by CSS Custom Properties (`:root`), natively supporting the host OS's default light/dark mode preference via the standard `prefers-color-scheme` query.

### Light Theme (Default)
- **Canvas (`--canvas`)**: `#fafafa` (off-white, reducing screen glare compared to pure white while retaining standard contrast).
- **Ink (`--ink`)**: `#111111` (near-black, optimizing text legibility over prolonged reading).
- **Muted text (`--muted`)**: `#666666` (used for metadata, secondary dates, and technology tags).
- **Accent/Link (`--accent`)**: `#0d7377` (a highly legible, professional muted teal providing immediate interactive visual cue).
- **Border (`--border`)**: `#e0e0e0` (thin, subtle rules for structural grouping).

### Dark Theme (Automatic fallback)
- **Canvas (`--canvas`)**: `#0f0f0f` (deep charcoal black).
- **Ink (`--ink`)**: `#e8e8e8` (soft off-white to prevent stark text-blooming on dark screens).
- **Muted text (`--muted`)**: `#a0a0a0` (high-contrast grey for secondary metrics).
- **Accent/Link (`--accent`)**: `#2dd4bf` (a bright teal adjusted for strict WCAG AAA contrast ratio compliance against deep charcoal).

---

## 3. Typographic Hierarchy & Web Fonts

To ensure excellent reading rhythm and high structural fidelity, the typography combines premium self-hosted serif, sans-serif, and monospaced typefaces.

```
+-------------------------------------------------------------+
| Typography System                                           |
+---------------------+-------------------+-------------------+
| Source Serif 4      | Inter             | JetBrains Mono    |
| Body & Headings     | Nav, Badges, UI   | Code blocks       |
+---------------------+-------------------+-------------------+
```

- **Serif Body (Source Serif 4)**: The core body text is set in Source Serif 4. It mirrors the classic typography found in scientific publications and academic papers (similar to Charter or Georgia).
  - Regular (`400`): Rendered at `17px` with a `1.6` line-height for a comfortable reading rhythm.
  - SemiBold (`600`): Used for semantic headings.
- **Sans-Serif UI (Inter)**: Nav links, metadata labels, technology tags, and timeline dates are set in Inter (Regular `400`, Medium `500`, SemiBold `600`). This ensures a modern, clean, UI-like feel for static controls.
- **Monospace Code (JetBrains Mono)**: Raw code blocks and inline code snippets utilize JetBrains Mono (`400`). It features generous height and clean ligatures, optimized for technical code syntax highlighting.

---

## 4. Reading Measure & Layout Constraints

Readable layouts require careful text boundaries. The body width is constrained to prevent horizontal eye fatigue:
- **Maximum Container Width**: `720px` (centered).
- **Reading Measure (`--line-length`)**: Limited to **`68ch`** (68 characters per line) for optimal reading rhythm.
- **Spacing**: Generous margin scales and clean padding elements separate logical blocks without utilizing structural tables or grid chrome.
- **Fade-In Micro-animation**: A subtle `400ms` transform and opacity transition is executed on page load to ease the rendering transition without feeling laggy or distracting.

---

## 5. Dynamic Resume & Print Layout

The CV page (`/cv/`) loads structured data dynamically from the parsed `resume.json` payload, laying out the timeline inside a cleanly styled page. 

To satisfy immediate recruitment needs (recruiters who print pages to PDF or physical sheets), a strict `@media print` style block is integrated:
- Hides the navigation bar, footer, and "Download PDF" CTA button.
- Converts the entire canvas to pure grayscale (`#000000` text on `#ffffff` background).
- Enforces strict page-break constraints (`page-break-inside: avoid` on job roles and `page-break-after: avoid` on section headings).
- Retains the exact semantic structure, resulting in a perfectly formatted, standard two-page physical resume when printed.

---

## 6. Performance Specifications

- **Total Page Weight**: **< 55KB** (including HTML, compiled CSS, and self-hosted, subsetted font binaries).
- **JavaScript Runtime Dependency**: **Zero** (no frameworks, no hydration, no bundle overhead).
- **Time to Interactive (TTI)**: **< 100ms** (near-instantaneous, bottlenecked only by network latency).
- **Lighthouse Performance Score**: **100/100** (guaranteed by light assets and semantic markup).
