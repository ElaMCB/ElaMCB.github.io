# LLM Safety & Red-Teaming — community series

**Public hub:** [https://elamcb.github.io/community/llm-safety-red-team/](https://elamcb.github.io/community/llm-safety-red-team/)

## Purpose

This folder is the **only** place new articles for your LinkedIn group (“LLM Safety & Red-Teaming for QA Leaders”) are added by automation. The hub page lists every piece with stable URLs you can paste into the group.

## Cadence

- **Every 21 days** (configurable via `intervalDays` in `manifest.json`), the workflow [Community LLM Safety publish](../../.github/workflows/community-llm-safety-publish.yml) runs.
- If `topics-queue.json` has at least one topic and the interval has passed, it generates a new HTML file under `articles/`, updates `manifest.json`, and commits.

## LinkedIn

**Posting to the LinkedIn group is not automated.** LinkedIn’s APIs do not reliably support third-party posting to groups for most developers. After each successful workflow run, open the hub, copy the newest article URL, and post it in the group.

## Add more articles

1. Edit `topics-queue.json` and append objects to the `topics` array:
   - `slug` — URL-safe, unique
   - `title`, `dek` — headline and subtitle
   - `sections` — array of `{ "heading", "body" }` (plain text; HTML is escaped on publish)

2. Commit and push. The next scheduled run (or a manual run with **force**) will consume the next queued topic.

## Manual publish now

**Actions → Community LLM Safety publish → Run workflow → enable “Publish next queued article now”.**

## Files

| File | Role |
|------|------|
| `manifest.json` | Series metadata, `lastPublished`, `intervalDays`, list of published articles |
| `topics-queue.json` | FIFO queue of not-yet-published topics |
| `articles/*.html` | Generated pages (do not hand-edit; edit the queue and re-run if you need changes) |
| `index.html` | Hub; loads `manifest.json` for the article list |
