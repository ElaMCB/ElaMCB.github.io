# LLM Safety & Red-Teaming — community series

**Public hub:** [https://elamcb.github.io/community/llm-safety-red-team/](https://elamcb.github.io/community/llm-safety-red-team/)

## Purpose

This folder is the **only** place new articles for your LinkedIn group (“LLM Safety & Red-Teaming for QA Leaders”) are added by automation. The hub page lists every piece with stable URLs you can paste into the group.

## Cadence

- The workflow [Community LLM Safety publish](../../.github/workflows/community-llm-safety-publish.yml) is scheduled **daily** (UTC). The script publishes **at most one** article every **`intervalDays`** (default **21**, set in `manifest.json`) by comparing today to `lastPublished`.
- If `topics-queue.json` has at least one topic and the interval has passed, it generates a new HTML file under `articles/`, updates `manifest.json`, and commits to `main`.
- The Python script is shared with the [Ethical AI Frameworks](../ethical-ai-frameworks/) hub; CI sets `COMMUNITY_SERIES_SUBDIR=llm-safety-red-team`.

## Who writes the articles? (automation vs agent)

- **Today:** The workflow only **renders** whatever copy you place in `topics-queue.json` (headline, dek, sections). It does **not** call an LLM. You can draft in the JSON yourself, paste in text from an offline ChatGPT session, or ask a collaborator to PR the queue—**no GitHub “agent” is required** for full articles.
- **Review before it ships:** The **next** item to publish is always the **first** object in the `topics` array. Edit or reorder that entry anytime before the due date (`lastPublished` + `intervalDays`). After push, the next successful run publishes the top item.
- **Optional later:** A separate workflow could call an API (with repo secrets), open a **pull request** with generated JSON for you to approve, then merge—true hands-off drafting with a human gate. That is not wired in this repo yet.

## Section format in `topics-queue.json`

Each section supports either:

- `"body": "single paragraph"` (legacy), or
- `"paragraphs": ["first paragraph", "second …"]` for multi-paragraph sections, or
- `"body"` with **two or more** paragraphs separated by a **blank line** (`\\n\\n`) in the string.

## LinkedIn

**Posting to the LinkedIn group is not automated.** LinkedIn’s APIs do not reliably support third-party posting to groups for most developers. After each successful workflow run, open the hub, copy the newest article URL, and post it in the group.

## Add more articles

1. Edit `topics-queue.json` and append objects to the `topics` array:
   - `slug` — URL-safe, unique
   - `title`, `dek` — headline and subtitle
   - `sections` — array of `{ "heading", "body" }` and/or `{ "heading", "paragraphs": [ … ] }` (plain text; HTML is escaped on publish)

2. Commit and push. The next scheduled run (or a manual run with **force**) will consume the next queued topic.

## Manual publish now

**Actions → Community LLM Safety publish → Run workflow → enable “Publish next queued article now” (the boolean “force” checkbox).**

## Files

| File | Role |
|------|------|
| `manifest.json` | Series metadata, `lastPublished`, `intervalDays`, list of published articles |
| `topics-queue.json` | FIFO queue of not-yet-published topics |
| `articles/*.html` | Generated pages (do not hand-edit; edit the queue and re-run if you need changes) |
| `index.html` | Hub; loads `manifest.json` for the article list |
