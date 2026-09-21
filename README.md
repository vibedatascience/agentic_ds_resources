# Agentic data science resources

Tracking what is happening in agentic data science: how companies are building data science agents, what the research says, and which open source projects are worth watching.

Maintained by Rahul Chaudhary. Any agent adding material to this repo reads this file first, then the `README.md` inside the folder it is filing into.

## Repository layout

Only immediate children are listed here. Read the `README.md` inside each folder for its filing rules and index.

| Folder | Contents | Description |
|---|---|---|
| `company-blog-posts/` | One file per company, plus `README.md` | Engineering and product posts from companies building data science agents. Append-only, newest entry at the top of each file. |
| `papers/` | One file per paper, named `YYYY-MM-DD_slug.md`, plus `README.md` | Research papers, benchmarks, and evaluation work. One file each because a paper carries enough metadata to justify it. |
| `other-repos/` | `README.md` holding the index table | Open source projects and tools. Tracked as rows in one table, not as separate files. |

## How to add an entry

1. Pick the folder. A company post goes in `company-blog-posts/<company>.md`, a paper gets its own file in `papers/`, a project gets a row in `other-repos/README.md`.
2. Follow the entry format in that folder's `README.md`. Every entry carries a date, a link, and the source text as published.
3. Do not add summaries or commentary. Archive what the source published.

## Conventions

* Dates are `YYYY-MM-DD` and refer to when the thing was published, not when it was filed here.
* File names are lowercase, hyphen separated, date first where a date applies.
* Text is archived as published. Quote structure and headings are preserved.
* Links are to the original source. If a page is likely to disappear, paste the sections that matter into the entry.
