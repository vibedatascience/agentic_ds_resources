# Company blog posts

Engineering and product posts from companies building data science agents, analytics agents, text to SQL systems, and agentic notebooks.

One file per company, named `YYYY-MM-DD_company.md` using the latest archived post’s publication date. Update the filename and index links when adding a newer post. Files are append-only and reverse chronological, so the newest post sits at the top.

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
| Anthropic | [2026-08-13_anthropic.md](2026-08-13_anthropic.md) | 2 | 2026-08-13 |
| Block | [2026-04-29_block.md](2026-04-29_block.md) | 1 | 2026-04-29 |
| DoorDash | [2026-09-16_doordash.md](2026-09-16_doordash.md) | 1 | 2026-09-16 |
| GitHub | [2026-06-19_github.md](2026-06-19_github.md) | 1 | 2026-06-19 |
| Grab | [2026-08-01_grab.md](2026-08-01_grab.md) | 1 | 2026-08-01 |
| Meta | [2026-03-30_meta.md](2026-03-30_meta.md) | 1 | 2026-03-30 |
| OpenAI | [2026-01-29_openai.md](2026-01-29_openai.md) | 1 | 2026-01-29 |
| Ramp | [2025-09-18_ramp.md](2025-09-18_ramp.md) | 1 | 2025-09-18 |
| Snap | [2026-09-10_snap.md](2026-09-10_snap.md) | 1 | 2026-09-10 |
| Spotify | [2026-06-10_spotify.md](2026-06-10_spotify.md) | 1 | 2026-06-10 |
| Stripe | [2026-07-30_stripe.md](2026-07-30_stripe.md) | 1 | 2026-07-30 |
| Vercel | [2025-12-22_vercel.md](2025-12-22_vercel.md) | 1 | 2025-12-22 |

## Assets

Diagrams and images archived from a post live in `assets/<company>/<YYYY-MM-DD>_<slug>/`. Prefer SVG where the source offers it. Link to them from a table inside the entry with a one-line description of each.
