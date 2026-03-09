#!/usr/bin/env python3
"""
Research & Literary Agent – Monthly update script.
Finds the latest llm-discovery digest, parses it, and inserts a new month
section into docs/STATE_OF_AI_TESTING.html.
Run from repository root. Uses previous month (e.g. run on April 1 → add March section).
"""

import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(os.environ.get("GITHUB_WORKSPACE", ".")).resolve()
DOC_PATH = REPO_ROOT / "docs" / "STATE_OF_AI_TESTING.html"
LLM_DISCOVERY_DIR = REPO_ROOT / "llm-discovery"
MAX_ITEMS = 20
MONTHLY_START = "<!-- RESEARCH_AGENT_MONTHLY_START -->"
MONTHLY_END = "<!-- RESEARCH_AGENT_MONTHLY_END -->"


def get_previous_month():
    """Return (year, month) for the month we're publishing (previous calendar month)."""
    # When run on 1st, we publish "previous" month. When run manually, same.
    today = datetime.utcnow()
    first_this_month = today.replace(day=1)
    last_month = first_this_month - timedelta(days=1)
    return last_month.year, last_month.month


def month_label(year: int, month: int) -> str:
    """e.g. 2026, 3 -> 'March 2026'."""
    return datetime(year, month, 1).strftime("%B %Y")


def month_id(year: int, month: int) -> str:
    """e.g. 2026, 3 -> '2026-03'."""
    return f"{year}-{month:02d}"


def find_latest_discoveries_file() -> Path | None:
    """Return path to the most recent llm-discovery/*.md file, or None."""
    if not LLM_DISCOVERY_DIR.is_dir():
        return None
    files = list(LLM_DISCOVERY_DIR.glob("discoveries-*.md"))
    if not files:
        return None
    return max(files, key=lambda p: p.stat().st_mtime)


def parse_discoveries(path: Path) -> list[dict]:
    """Parse discoveries markdown into list of {title, description, url}."""
    text = path.read_text(encoding="utf-8", errors="replace")
    entries = []
    blocks = re.split(r"\n###\s*\d+\.\s*", text)
    for block in blocks:
        if not block.strip():
            continue
        lines = block.split("\n")
        title = lines[0].strip() if lines else ""
        # Skip header block (starts with # or "New LLM" etc.)
        if title.startswith("#") or "New LLM" in title or "Discoveries" in title:
            continue
        desc = ""
        url = ""
        for line in lines[1:]:
            if line.strip().startswith("- **Description**:"):
                desc = line.replace("- **Description**:", "").strip()
            if line.strip().startswith("- **URL**:"):
                url = line.replace("- **URL**:", "").strip()
        if title or desc or url:
            entries.append({"title": title, "description": desc, "url": url})
    return entries[:MAX_ITEMS]


def escape_html(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def build_month_section(year: int, month: int, discoveries: list[dict], source_file: Path | None) -> str:
    """Build HTML for one month section."""
    label = month_label(year, month)
    mid = month_id(year, month)
    lines = [
        f'            <div class="card month-section" id="month-{mid}">',
        f'                <span class="date-badge">{escape_html(label)}</span>',
        f'                <h3>{escape_html(label)}</h3>',
    ]
    if discoveries:
        lines.append("                <p>Curated discoveries from the LLM &amp; Gen AI research pipeline relevant to testing and quality engineering.</p>")
        for d in discoveries:
            title = escape_html((d.get("title") or "Item").strip())
            desc = escape_html((d.get("description") or "").strip())[:400]
            url = (d.get("url") or "").strip()
            if url:
                lines.append('                <div class="discovery-item">')
                lines.append(f'                    <strong>{title}</strong>')
                if desc:
                    lines.append(f'                    <p>{desc}</p>')
                lines.append(f'                    <a href="{escape_html(url)}" target="_blank" rel="noopener" class="source-link">Link</a>')
                lines.append("                </div>")
            else:
                lines.append('                <div class="discovery-item">')
                lines.append(f'                    <strong>{title}</strong>')
                if desc:
                    lines.append(f'                    <p>{desc}</p>')
                lines.append("                </div>")
        if source_file:
            lines.append(f'                <p class="agent-badge">Source: <code>{escape_html(source_file.name)}</code></p>')
    else:
        lines.append("                <p>No discoveries file found for this period. Add <code>llm-discovery/discoveries-YYYY-MM-DD.md</code> to feed the next run.</p>")
    lines.append('                <p class="agent-badge"><i class="fas fa-robot"></i> Research &amp; Literary Agent – State of AI Testing</p>')
    lines.append("            </div>")
    return "\n".join(lines)


def update_doc(year: int, month: int, new_section: str) -> str:
    """Insert new month section after RESEARCH_AGENT_MONTHLY_START. Skip if that month already exists.
    Returns: 'inserted' | 'skipped' | 'error'
    """
    if not DOC_PATH.is_file():
        print(f"ERROR: Doc not found: {DOC_PATH}", file=sys.stderr)
        return "error"
    content = DOC_PATH.read_text(encoding="utf-8", errors="replace")
    mid = month_id(year, month)
    if f'id="month-{mid}"' in content:
        print(f"Section for {month_label(year, month)} already exists; skipping insert.")
        return "skipped"
    if MONTHLY_START not in content or MONTHLY_END not in content:
        print("ERROR: RESEARCH_AGENT_MONTHLY_START/END markers not found.", file=sys.stderr)
        return "error"
    # Insert new section right after START (so newest first). Do not duplicate the marker.
    insert = f"\n{new_section}\n            "
    content = content.replace(MONTHLY_START, MONTHLY_START + insert, 1)
    DOC_PATH.write_text(content, encoding="utf-8")
    print(f"Inserted section for {month_label(year, month)}.")
    return "inserted"


def main() -> int:
    year, month = get_previous_month()
    print(f"Target month: {month_label(year, month)}")
    discoveries_path = find_latest_discoveries_file()
    discoveries = parse_discoveries(discoveries_path) if discoveries_path else []
    if discoveries_path:
        print(f"Using discoveries from: {discoveries_path.name} ({len(discoveries)} items)")
    else:
        print("No llm-discovery/*.md file found; section will have placeholder text.")
    new_section = build_month_section(year, month, discoveries, discoveries_path)
    result = update_doc(year, month, new_section)
    # Success: inserted or skipped (section already exists, nothing to do)
    if result in ("inserted", "skipped"):
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
