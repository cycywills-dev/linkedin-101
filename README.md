# LinkedIn 101 — Topic Presentations (Web)

Nine standalone, self-paced HTML slide decks adapted from the *Build Your Professional
Presence Online* session by **Cyhana Williams**. Each deck mirrors the original design
(LinkedIn brand blue, navy/light slides, card layouts) and carries the
`Cyhana Williams © 2026` watermark on every slide.

## Files
| File | Topic | Source slides | Slides |
|------|-------|---------------|--------|
| `index.html` | Landing page (links to all topics) | — | — |
| `topic-01.html` | Why LinkedIn Matters | 2–3 | 5 |
| `topic-02.html` | Personal Branding | 5 | 5 |
| `topic-03.html` | Profile Setup | 6–8 | 6 |
| `topic-04.html` | Headline & Summary | 9 | 5 |
| `topic-05.html` | Networking & Messages | 10–11 | 5 |
| `topic-06.html` | Content & Engagement | 12–13 | 6 |
| `topic-07.html` | Job Search & Applying | 14 | 6 |
| `topic-08.html` | Staying Safe Online | 15 | 6 |
| `topic-09.html` | Action Plan & Resources | 16–17 | 4 |

Shared assets: `styles.css`, `deck.js`. Source generator: `build_html.py`
(run `python build_html.py` to rebuild every page).

## Navigation
- **← / →** (or PageUp/PageDown, Space) to move between slides
- **Home / End** jump to first / last slide
- Click the **dots** or the **‹ ›** buttons; **swipe** on touch devices
- Each slide is deep-linkable, e.g. `topic-03.html#4`

## Host on GitHub Pages
1. Create a repo and push this folder's contents to the root (or a `/docs` folder):
   ```bash
   git init
   git add .
   git commit -m "LinkedIn 101 web decks"
   git branch -M main
   git remote add origin https://github.com/<you>/<repo>.git
   git push -u origin main
   ```
2. In the repo: **Settings → Pages → Build and deployment**.
   Set **Source: Deploy from a branch**, **Branch: `main`**, folder **`/ (root)`** (or `/docs`).
3. Wait ~1 minute. Your site goes live at
   `https://<you>.github.io/<repo>/` (opens `index.html`).

No build step or framework is required — these are static files. The only external
dependency is the Google Fonts link (Inter + Poppins); pages fall back to system fonts
gracefully if offline.

## Local preview
```bash
python -m http.server 8000
# then open http://localhost:8000
```
(Opening the files directly via `file://` works in most browsers too.)
