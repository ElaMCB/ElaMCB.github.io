#!/usr/bin/env python3
"""
Publish the next article for community/llm-safety-red-team/ every intervalDays (default 21).
Run from repository root. Set FORCE_PUBLISH=1 to ignore the date interval (manual workflow).
"""

from __future__ import annotations

import html
import json
import os
import sys
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(os.environ.get("GITHUB_WORKSPACE", ".")).resolve()
BASE = REPO_ROOT / "community" / "llm-safety-red-team"
MANIFEST_PATH = BASE / "manifest.json"
TOPICS_PATH = BASE / "topics-queue.json"
ARTICLES_DIR = BASE / "articles"
FORCE = os.environ.get("FORCE_PUBLISH", "").strip() in ("1", "true", "yes")


def days_since(iso_d: str) -> int:
    try:
        last = date.fromisoformat(iso_d[:10])
    except ValueError:
        return 9999
    return (date.today() - last).days


def article_html(
    title: str,
    dek: str,
    sections: list[dict],
    slug: str,
    pub_date: str,
) -> str:
    safe_title = html.escape(title)
    safe_dek = html.escape(dek)
    safe_slug = html.escape(slug)
    body_parts = []
    for sec in sections:
        h = html.escape(sec.get("heading", ""))
        b = html.escape(sec.get("body", ""))
        body_parts.append(f"<h2>{h}</h2>\n<p>{b}</p>")
    body_html = "\n".join(body_parts)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title} | LLM Safety &amp; Red-Teaming</title>
    <meta name="description" content="{safe_dek}">
    <link rel="icon" type="image/svg+xml" href="../../../images/favicon.svg">
    <link rel="canonical" href="https://elamcb.github.io/community/llm-safety-red-team/articles/{pub_date}-{slug}.html">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script data-goatcounter="https://elamcb.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
    <style>
        :root {{
            --secondary: #00d4ff;
            --accent: #7c3aed;
            --neon-blue: #00f5ff;
            --neon-purple: #bf00ff;
            --light: #e4e4e7;
            --card-bg: rgba(15, 15, 23, 0.9);
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
        body {{
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #533483 100%);
            background-attachment: fixed;
            color: var(--light);
            line-height: 1.8;
            min-height: 100vh;
        }}
        .container {{ width: 90%; max-width: 800px; margin: 0 auto; padding: 2rem 1rem 4rem; }}
        .back {{ display: inline-flex; align-items: center; gap: 0.5rem; color: var(--secondary); text-decoration: none; margin-bottom: 2rem; font-weight: 600; }}
        .back:hover {{ text-decoration: underline; }}
        header {{ margin-bottom: 2rem; padding-bottom: 1.5rem; border-bottom: 2px solid var(--secondary); }}
        h1 {{
            font-size: 1.85rem;
            background: linear-gradient(135deg, var(--neon-blue), var(--neon-purple));
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.75rem;
        }}
        .dek {{ font-size: 1.1rem; opacity: 0.95; }}
        .series {{ font-size: 0.85rem; color: var(--secondary); margin-top: 1rem; }}
        .content {{ background: var(--card-bg); border: 1px solid rgba(0, 212, 255, 0.25); border-radius: 12px; padding: 2rem; }}
        .content h2 {{ color: var(--secondary); font-size: 1.25rem; margin: 2rem 0 1rem; }}
        .content h2:first-of-type {{ margin-top: 0; }}
        .content p {{ margin-bottom: 1rem; text-align: justify; }}
    </style>
</head>
<body>
    <div class="container">
        <a href="../index.html" class="back"><i class="fas fa-arrow-left"></i> LLM Safety &amp; Red-Teaming hub</a>
        <header>
            <p class="series"><i class="fas fa-users"></i> Series for QA leaders · Published {html.escape(pub_date)}</p>
            <h1>{safe_title}</h1>
            <p class="dek">{safe_dek}</p>
        </header>
        <article class="content">
{body_html}
        </article>
    </div>
</body>
</html>
"""


def main() -> int:
    if not MANIFEST_PATH.is_file():
        print("ERROR: manifest.json missing", file=sys.stderr)
        return 1
    if not TOPICS_PATH.is_file():
        print("ERROR: topics-queue.json missing", file=sys.stderr)
        return 1

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    topics_data = json.loads(TOPICS_PATH.read_text(encoding="utf-8"))
    queue = topics_data.get("topics") or []

    if not queue:
        print("No topics in queue; nothing to publish.")
        return 0

    interval = int(manifest.get("intervalDays") or 21)
    last = manifest.get("lastPublished") or "1970-01-01"

    if not FORCE and days_since(last) < interval:
        print(
            f"Skip: lastPublished={last}, interval={interval}d, days_since={days_since(last)} (set FORCE_PUBLISH=1 to override)."
        )
        return 0

    topic = queue.pop(0)
    slug = topic.get("slug") or "article"
    title = topic.get("title") or "Untitled"
    dek = topic.get("dek") or ""
    sections = topic.get("sections") or []

    pub_date = date.today().isoformat()
    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{pub_date}-{slug}.html"
    out_path = ARTICLES_DIR / filename

    if out_path.exists():
        print(f"ERROR: {out_path} already exists", file=sys.stderr)
        return 1

    html_out = article_html(title, dek, sections, slug, pub_date)
    out_path.write_text(html_out, encoding="utf-8")

    summary = dek[:200] + ("…" if len(dek) > 200 else "")
    manifest.setdefault("articles", []).insert(
        0,
        {
            "date": pub_date,
            "slug": slug,
            "title": title,
            "summary": summary,
            "href": f"/community/llm-safety-red-team/articles/{filename}",
            "external": False,
        },
    )
    manifest["lastPublished"] = pub_date

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    TOPICS_PATH.write_text(json.dumps({"topics": queue}, indent=2) + "\n", encoding="utf-8")

    public_url = f"https://elamcb.github.io/community/llm-safety-red-team/articles/{filename}"
    print(f"Published: {public_url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
