# Inventory

Corpus: `company-blog-posts/` at commit `b9bf359` ("Add Kikoff, Clay, Pinecone posts and Kuaishou A/B Agent paper", 2026-10-03). 16 posts, 15 companies, 38,237 words.

Word count = words in the post body after the metadata block. Image counts come from viewing every file in `company-blog-posts/assets/`.

- **Diagrams**: architecture, flow or concept drawings of the system.
- **Other images**: charts (C), UI screenshots (S), tables or memes (O).
- **Not archived**: figures that exist only as an italic caption line in the archive.

## Posts

| # | Company | Post title | Date | Words | Diagrams | Other images | Not archived | What the system does |
|---|---|---|---|---|---|---|---|---|
| 1 | Anthropic | How Anthropic enables self-service data analytics with Claude; Self-service data analytics in Slack: how Anthropic deploys Claude Tag for ad-hoc questions | 2026-06-03; 2026-08-13 | 6,555 (4,107 + 2,448) | 4 | 1 O, 3 S | 0 (appendix text truncated) | Claude answers business analytics questions in Claude Code and in Slack, guided by a governed semantic layer, per-domain skill files kept in the data repo, and offline and online checks. |
| 2 | Block | Building the Data Foundation for Automated Analytics | 2026-04-29 | 5,237 | 5 | 1 C | 0 | Two MCP servers: one returns pre-approved metric SQL from a governed metrics store, the other retrieves table docs and expert queries so the agent can write new SQL. |
| 3 | Clay | We gave everyone at Clay their own data scientist | 2026-09-30 | 2,237 | 0 | 0 | 2 (interactive embeds) | A Slack bot (monty) reads the data team's codebase through catalog files, queries approved dbt models in Snowflake, and uses Python for charts and statistics. |
| 4 | DoorDash | Inside Vera, DoorDash's Data Agent | 2026-09-16 | 2,380 | 0 | 0 | 10 (1 table, 9 figures) | A conversational agent (Vera) retrieves from a curated data model and human-written knowledge, writes and runs SQL, and is scored on a benchmark of 1,900+ evals by an LLM judge. |
| 5 | GitHub | How we built an internal data analytics agent | 2026-06-19 | 1,238 | 1 | 0 | 0 | A Copilot-based agent (Qubot) runs from Slack, VS Code or Copilot CLI, loads curated context over MCP, and queries Kusto or Trino. |
| 6 | Grab | How AI is transforming analytics at Grab | 2026-08-01 | 2,472 | 1 | 2 C, 5 S | 0 | Several analytics agents: a Slack workflow (Spartan) that routes questions to skills and analysis frameworks, scheduled root-cause commentary, a pipeline-repair agent, and a portal (BriX) for team-specific agent apps. |
| 7 | Kikoff | Building the AI Experiment Reviewer with Claude | 2026-03-27 | 1,469 | 0 | 0 | 0 | A Claude skill reviews each experiment readout with three sub-agents (statistics, data, business) using Notion, Statsig, Snowflake and Metabase, and posts comments to the Notion doc. |
| 8 | Meta | Inside Meta's Home Grown AI Analytics Agent | 2026-03-30 | 2,699 | 3 | 1 C, 3 S | 0 | An agent writes and runs SQL in a loop, seeded with each user's query history and LLM-written table descriptions, and extended by team-built Cookbooks of recipes and knowledge. |
| 9 | OpenAI | Inside OpenAI's in-house data agent | 2026-01-29 | 2,518 | 5 | 0 | 6 (screenshots) | A GPT-5.2 agent retrieves six layers of table and company context, runs SQL, and answers in Slack, a web UI, IDEs, Codex CLI and internal ChatGPT. |
| 10 | Pinecone | Inside AskData: How We Slashed Token Consumption by Over 90% | 2026-06-02 | 3,105 | 0 | 0 | 0 | A Slack agent (AskData) answers questions over BigQuery using a knowledge layer built from docs, Slack, call transcripts and SQL, rebuilt in 2026 on Pinecone Nexus. |
| 11 | Ramp | Meet Ramp Research: Our Agentic Data Analyst | 2025-09-18 | 991 | 2 | 1 C, 5 S, 1 O | 0 | A Slack agent (Ramp Research) answers data questions using indexed dbt, Looker and Snowflake metadata and domain docs written by analytics owners. |
| 12 | Snap | DS Agent: Snap's AI Data Scientist | 2026-09-10 | 2,939 | 3 | 0 | 0 | A shared git repo of instructions, skills and table docs that data scientists open in a coding agent (IDE or terminal), with MCP links to the data catalog, internal search and GitHub. |
| 13 | Spotify | Encoding Your Domain Expert: The Context Layer Behind Spotify's Data Assistant | 2026-06-10 | 1,366 | 1 | 3 S | 0 | A data assistant (Vedder) answers in Slack, a web UI and over MCP, using expert-curated clusters of tables, vetted question-SQL pairs and docs. |
| 14 | Stripe | Meet Stripe's Knowledge AI Platform | 2026-07-30 | 1,919 | 1 | 1 C, 3 S | 0 | A company-wide agent platform for knowledge work (Kai) with a web app, Slack and embedded surfaces; data analysis is one use among many. |
| 15 | Vercel | We removed 80% of our agent's tools | 2025-12-22 | 1,112 | 0 | 1 S | 0 | A Slack text-to-SQL agent (d0) rebuilt to give Claude Opus 4.5 a bash tool over Cube semantic layer files plus a SQL tool. |
| | **Total** | 16 posts | | **38,237** | **26** | | **18** | |

## Diagram files

| Company | Diagram files |
|---|---|
| Anthropic | article-0/image-02 (stack), article-0/image-03 (schema example), article-1/image-02 (warehouse + knowledge index), article-1/image-03 (telemetry views) |
| Block | image-01 (overview), image-02 (two MCP architecture), image-03 (metrics store), image-04 (Query Expert pipeline), image-05 (data domains) |
| GitHub | image-01 (architecture) |
| Grab | image-01 (index and router) |
| Meta | image-04 (reasoning loop), image-05 (shared memory pipeline), image-08 (Cookbook) |
| OpenAI | how-it-works, layers-of-context, codex-enrichment-pipeline, context-retrieval, eval-pipeline |
| Ramp | ramp-research-agent-architecture, analytics-bottleneck (the before state) |
| Snap | image-01 (work loop), image-02 (surfaces and repo), image-03 (local to prod promotion) |
| Spotify | image-01 (data platform scale) |
| Stripe | image1 (execution environment) |

## Scope questions for Rahul

These do not change the inventory. They affect whether and how each company is coded.

| Company | Question |
|---|---|
| Pinecone | AskData is internal, but the post also promotes Nexus, a Pinecone product, and links to sign-up. Keep, coding only AskData? |
| Anthropic | The second post deploys Claude Tag, which is in public beta. The system described is internal. Keep? |
| Stripe | Kai is a general knowledge-work platform, not a data agent. Code only what the post says about data analysis, or exclude? |
| Grab | The post describes several agents (Spartan, Scarlet, RCA, BriX apps). Code Spartan as the main system, or the whole set? |
| Kikoff | The system reviews experiment readouts only; it does not answer open questions. Keep (Task scope = experiment review)? |
