# Home Energy OS — Writeups

Source for two posts about a residential multi-vendor home energy controller.

## Posts

- [`article.md`](article.md) — A Practical Home Energy OS with Home Assistant. The architecture writeup.
- [`article-2.md`](article-2.md) — When the Gateway Goes Dark. A first-outage postmortem.

## Stack

Posts are written in Markdown and rendered to HTML via pandoc with a small CSS file.

```bash
pandoc article.md -s -c article.css -o article.html
pandoc article-2.md -s -c article.css -o article-2.html
```

`index.html` is a static landing page that links to both. Hosted via GitHub Pages
(once made public). All screenshots live under `screenshots/`. Provenance and
source references for each post are in `sources.md` and `screenshot-inventory.md`.

## Status

Repo is currently private while the posts are being finalized. Will go public
together with GitHub Pages enablement when ready.
