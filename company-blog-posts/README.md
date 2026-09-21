# Company blog posts

Engineering and product posts from companies building data science agents, analytics agents, text to SQL systems, and agentic notebooks.

One file per company, named after the company in lowercase with hyphens: `databricks.md`, `google-cloud.md`. Files are append-only and reverse chronological, so the newest post sits at the top.

A company gets its own file on its first entry. Do not create empty files in advance.

## Entry format

Each post is one `##` section inside the company file: a short metadata block, then the post's text as published.

```markdown
## 2026-09-15 - Title of the post
link: https://...
authors: First Last, First Last
type: blog | launch | docs | talk
tags: text-to-sql, evals, notebooks
retrieved: 2026-09-21

---

The article text, verbatim, with its own headings kept.
```

No summaries and no commentary. The text is the entry. Diagrams go inline at the position they appear in the post; screenshots that are not archived are left as their italic caption line.

Keep `tags` to a short controlled set so they stay groupable. Current tags in use: `text-to-sql`, `notebooks`, `evals`, `semantic-layer`, `agent-harness`, `bi`, `pipelines`, `mcp`.

## Companies tracked

| Company | File | Entries | Latest post |
|---|---|---|---|
| DoorDash | [doordash.md](doordash.md) | 1 | 2026-09-16 |
| GitHub | [github.md](github.md) | 1 | 2026-06-19 |
| Meta | [meta.md](meta.md) | 1 | 2026-03-30 |
| OpenAI | [openai.md](openai.md) | 1 | 2026-01-29 |

## Assets

Diagrams and images archived from a post live in `assets/<company>/<YYYY-MM-DD>_<slug>/`. Prefer SVG where the source offers it. Link to them from a table inside the entry with a one-line description of each.
