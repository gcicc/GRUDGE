# GRUDGE

A Drudge Report-style news aggregator. Fetches RSS headlines, scores them by drama, rewrites with ALL CAPS, and publishes a raw 1997-aesthetic HTML page to GitHub Pages.

Runs on GitHub Actions every 30 minutes. No LLM, no CSS, no mercy.

## Local dev

```bash
pip install -e ".[dev]"
python run.py
open docs/index.html
```

## How it works

1. Fetches RSS feeds from ~10 news sources
2. Scores headlines by "drama" (keyword hits + recency)
3. Rewrites headlines with strategic ALL CAPS
4. Generates raw HTML (Times New Roman, blue links, `<hr>` everywhere)
5. GitHub Actions commits and deploys to Pages
