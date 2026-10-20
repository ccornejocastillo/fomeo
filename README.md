# fomeo

Landing page for **fomeo TV**, published at [fomeo.cl](https://fomeo.cl).

Fully static site (HTML, CSS and JS), deployed with GitHub Pages from the `main` branch. DNS is handled by Cloudflare.

## Layout

- **Large screens:** two columns. Left: the title, tagline and social links. Right: a card with the latest video (thumbnail, title, date and a "Ver episodio" link).
- **Narrow screens (≤ 960px):** a single centered column, with the video card below the social links (max 560px wide).

The page is designed to fit the viewport without scrolling on common screen sizes.

## Structure

```
index.html                          Main page
assets/css/main.css                 Styles
assets/js/latest-video.js           Renders the latest video card
data/latest-video.json              Latest channel video (auto-generated)
scripts/fetch-latest-video.py       Fetches the latest video from YouTube
.github/workflows/latest-video.yml  Daily action that updates the JSON
CNAME                               GitHub Pages domain
```

## Latest video

The page shows the channel's most recent YouTube video without calling YouTube from the browser:

1. A GitHub Action runs once a day (03:17 UTC) and executes `scripts/fetch-latest-video.py`.
2. The script reads the channel's RSS feeds for long-form videos (`UULF…`) and live streams (`UULV…`), skips scheduled streams that haven't aired yet (0 views) and keeps the most recent one. Shorts are not included. It uses the 1280×720 thumbnail (`maxresdefault`) when available, falling back to `hqdefault`.
3. If the video changed, the action commits `data/latest-video.json` with the message `chore: update latest video (<videoId>)`, which triggers a new GitHub Pages deploy.
4. `assets/js/latest-video.js` reads that JSON and builds the card.

The action can also be run manually from **Actions → latest-video → Run workflow**.

## Local development

```bash
python3 -m http.server 8000
```

Open <http://localhost:8000>. The server is required: opening `index.html` directly (`file://`) makes the browser block loading the JSON.

To update the latest video locally:

```bash
python3 scripts/fetch-latest-video.py
```

## Notes

- The action needs **Settings → Actions → General → Workflow permissions → Read and write** to be able to push.
- GitHub disables scheduled workflows after 60 days of repository inactivity; re-enable them from the Actions tab.
