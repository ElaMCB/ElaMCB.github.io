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
from datetime import date
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


STEEL_ARTICLE_CSS = """
        :root {
            --bg: #0a0a0f;
            --text: #e4e4e7;
            --steel: #5b7fb8;
            --steel-bright: #7aa3d8;
            --steel-dim: rgba(91, 127, 184, 0.35);
            --panel: rgba(26, 26, 46, 0.55);
            --card-bg: rgba(15, 15, 23, 0.88);
        }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Courier New', 'Monaco', monospace; }
        body {
            background: var(--bg);
            color: var(--text);
            line-height: 1.8;
            min-height: 100vh;
        }
        .container { width: 90%; max-width: 800px; margin: 0 auto; padding: 2rem 1rem 4rem; }
        .back {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 10px 20px;
            background: rgba(91, 127, 184, 0.2);
            border: 1px solid var(--steel-dim);
            border-radius: 8px;
            color: var(--steel);
            text-decoration: none;
            margin-bottom: 2rem;
            font-weight: bold;
            transition: background 0.2s ease, color 0.2s ease;
        }
        .back:hover {
            background: rgba(91, 127, 184, 0.32);
            color: var(--steel-bright);
        }
        header { margin-bottom: 2rem; padding-bottom: 1.5rem; border-bottom: 2px solid var(--steel-dim); }
        h1 {
            font-size: 1.85rem;
            color: var(--steel);
            text-shadow: 0 0 20px rgba(91, 127, 184, 0.18);
            margin-bottom: 0.75rem;
        }
        .dek { font-size: 1.05rem; opacity: 0.92; color: rgba(228, 228, 231, 0.9); }
        .series { font-size: 0.85rem; color: var(--steel-bright); margin-top: 1rem; }
        .content {
            background: var(--panel);
            border: 1px solid var(--steel-dim);
            border-radius: 10px;
            padding: 2rem;
        }
        .content h2 { color: var(--steel); font-size: 1.2rem; margin: 2rem 0 1rem; }
        .content h2:first-of-type { margin-top: 0; }
        .content p { margin-bottom: 1rem; text-align: justify; color: rgba(228, 228, 231, 0.92); }
"""


def section_html(sec: dict) -> str:
    """Render one section: optional paragraphs[] or body (single string); body may use blank lines for multiple <p>."""
    h = html.escape(sec.get("heading", ""))
    paras = sec.get("paragraphs")
    if isinstance(paras, list) and paras:
        chunks: list[str] = []
        for p in paras:
            t = str(p).strip()
            if t:
                chunks.append(f"<p>{html.escape(t)}</p>")
        inner = "\n".join(chunks)
        return f"<h2>{h}</h2>\n{inner}" if inner else f"<h2>{h}</h2>"
    raw = sec.get("body", "")
    if isinstance(raw, str) and "\n\n" in raw.strip():
        parts = [p.strip() for p in raw.split("\n\n") if p.strip()]
        inner = "\n".join(f"<p>{html.escape(p)}</p>" for p in parts)
        return f"<h2>{h}</h2>\n{inner}"
    return f"<h2>{h}</h2>\n<p>{html.escape(str(raw))}</p>"


def article_html(
    title: str,
    dek: str,
    sections: list[dict],
    slug: str,
    pub_date: str,
) -> str:
    safe_title = html.escape(title)
    safe_dek = html.escape(dek)
    body_html = "\n".join(section_html(s) for s in sections)

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
    <style>{STEEL_ARTICLE_CSS}
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
