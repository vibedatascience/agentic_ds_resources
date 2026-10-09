# Counts

How many of the 15 companies report each value, from `coding.csv`. A company counts once per value. Sorted by count within each field.

## Users

| Value | Companies | Which |
|---|---|---|
| all employees | 10 of 15 | Anthropic, Block, Clay, GitHub, Grab, Meta, OpenAI, Snap, Stripe, Vercel |
| analysts and PMs | 2 of 15 | DoorDash, Ramp |
| not stated | 2 of 15 | Pinecone, Spotify |
| data team only | 1 of 15 | Kikoff |
| executives | 1 of 15 | Block |

## Interface

| Value | Companies | Which |
|---|---|---|
| Slack or chat app | 10 of 15 | Anthropic, Clay, GitHub, Grab, OpenAI, Pinecone, Ramp, Spotify, Stripe, Vercel |
| IDE or terminal | 6 of 15 | Anthropic, GitHub, Grab, OpenAI, Snap, Spotify |
| web app | 5 of 15 | Grab, OpenAI, Snap, Spotify, Stripe |
| not stated | 4 of 15 | Block, DoorDash, Kikoff, Meta |
| BI tool | 2 of 15 | Anthropic, Stripe |

## Task scope

| Value | Companies | Which |
|---|---|---|
| answer a question with SQL | 13 of 15 | Anthropic, Block, Clay, DoorDash, GitHub, Grab, Meta, OpenAI, Pinecone, Ramp, Snap, Spotify, Vercel |
| multi-step analysis | 9 of 15 | Anthropic, Block, DoorDash, Grab, Meta, OpenAI, Pinecone, Ramp, Snap |
| other (any) | 7 of 15 | Anthropic, Block, Clay, Grab, OpenAI, Ramp, Stripe |
| dashboard or report creation | 6 of 15 | Anthropic, GitHub, Grab, OpenAI, Snap, Stripe |
| experiment review | 3 of 15 | Anthropic, Grab, Kikoff |

Other labels: data analysis (Stripe); data discovery (Block, OpenAI); forecasting (Anthropic); pipeline repair (Anthropic, Grab); simulation (Grab); statistical inference (Clay); workflow automation (Ramp).

## Context sources

| Value | Companies | Which |
|---|---|---|
| human-written domain notes | 12 of 15 | Anthropic, Block, Clay, DoorDash, GitHub, Grab, Meta, Pinecone, Ramp, Snap, Spotify, Stripe |
| table and column docs | 12 of 15 | Anthropic, Block, Clay, DoorDash, GitHub, Grab, Meta, OpenAI, Pinecone, Ramp, Snap, Spotify |
| metric definitions or semantic layer | 10 of 15 | Anthropic, Block, Clay, GitHub, Grab, Kikoff, Meta, OpenAI, Pinecone, Vercel |
| past analyses or docs | 10 of 15 | Anthropic, Block, Clay, DoorDash, Grab, Kikoff, Meta, OpenAI, Pinecone, Snap |
| code repos | 7 of 15 | Clay, DoorDash, Kikoff, Meta, OpenAI, Pinecone, Snap |
| past queries | 6 of 15 | Block, GitHub, Meta, OpenAI, Pinecone, Spotify |
| saved corrections or memory | 6 of 15 | Anthropic, Grab, Meta, OpenAI, Pinecone, Snap |

## Context delivery

| Value | Companies | Which |
|---|---|---|
| tool calls or MCP | 10 of 15 | Anthropic, Block, GitHub, Grab, Kikoff, OpenAI, Pinecone, Ramp, Snap, Stripe |
| retrieval search | 9 of 15 | Anthropic, Block, DoorDash, Grab, Meta, OpenAI, Pinecone, Ramp, Stripe |
| curated files the agent reads | 6 of 15 | Anthropic, Clay, Grab, Ramp, Snap, Vercel |
| always in prompt | 3 of 15 | Clay, Kikoff, Meta |
| not stated | 1 of 15 | Spotify |

## Tools

| Value | Companies | Which |
|---|---|---|
| SQL execution | 14 of 15 | Anthropic, Block, Clay, DoorDash, GitHub, Grab, Kikoff, Meta, OpenAI, Pinecone, Ramp, Snap, Spotify, Vercel |
| other (any) | 12 of 15 | Anthropic, Block, DoorDash, GitHub, Grab, Kikoff, Meta, OpenAI, Pinecone, Snap, Stripe, Vercel |
| search over docs | 8 of 15 | Anthropic, Block, Grab, Meta, OpenAI, Pinecone, Ramp, Snap |
| chart creation | 5 of 15 | Anthropic, Clay, Grab, Kikoff, Meta |
| Python | 4 of 15 | Clay, Meta, Snap, Stripe |

Other labels: 1,000+ skills and tools (BI dashboards, Zoom, Google Workspace) (Stripe); SQL validation (DoorDash); bash in a sandbox (Vercel); code search (Kikoff); correction submission (Pinecone); dashboard discovery, permission check, feedback (Block); data catalog (DataHub) (Snap); data platform systems (OpenAI); experiment platform (Kikoff); opens and merges PRs (Anthropic); opens merge requests (Grab); output validation by a separate AI (Meta); pull request creation (GitHub); semantic layer function (Anthropic); simulation (Grab); web search (OpenAI).

## Eval method

| Value | Companies | Which |
|---|---|---|
| fixed question set with known answers | 10 of 15 | Anthropic, Block, DoorDash, GitHub, Grab, OpenAI, Pinecone, Ramp, Snap, Vercel |
| user feedback | 4 of 15 | Anthropic, Block, Meta, Spotify |
| none described | 3 of 15 | Clay, Kikoff, Stripe |
| LLM judge | 2 of 15 | DoorDash, OpenAI |
| human review | 1 of 15 | Grab |

## Trust

| Value | Companies | Which |
|---|---|---|
| shows its work | 10 of 15 | Block, GitHub, Grab, Kikoff, Meta, OpenAI, Ramp, Snap, Spotify, Vercel |
| access permissions enforced | 9 of 15 | Anthropic, Block, Clay, DoorDash, Grab, OpenAI, Ramp, Snap, Stripe |
| confidence or warnings | 9 of 15 | Anthropic, Block, Clay, Grab, Meta, OpenAI, Ramp, Snap, Spotify |
| cites sources | 7 of 15 | Anthropic, Block, Clay, Meta, OpenAI, Snap, Spotify |
| human approval step | 4 of 15 | Anthropic, DoorDash, Grab, Snap |
| not stated | 1 of 15 | Pinecone |

## Models named

| Value | Companies | Which |
|---|---|---|
| names any model | 6 of 15 | Anthropic, Clay, DoorDash, Kikoff, OpenAI, Vercel |
| names the production model | 6 of 15 | Anthropic, Clay, DoorDash, Kikoff, OpenAI, Vercel |
| not stated | 9 of 15 | Block, GitHub, Grab, Meta, Pinecone, Ramp, Snap, Spotify, Stripe |

| Model as written | Role | Company |
|---|---|---|
| Claude Fable 5 | benchmarked | DoorDash |
| Claude Opus 4.5 | production | Vercel |
| Claude | production | Anthropic, Kikoff |
| GLM 5.3 Flash | benchmarked | DoorDash |
| GPT 5.5 | production | DoorDash |
| GPT-5 | named | OpenAI |
| GPT-5.2 | production | OpenAI |
| Opus 4.8 | benchmarked | DoorDash |
| Opus | production | Clay |

## Free-text fields

| Field | Stated | Not stated | Rows | Not stated by |
|---|---|---|---|---|
| Eval size / quality | 5 of 15 | 10 of 15 | 16 | Clay, GitHub, Grab, Kikoff, Meta, OpenAI, Ramp, Snap, Spotify, Stripe |
| Adoption | 12 of 15 | 3 of 15 | 41 | DoorDash, OpenAI, Vercel |
| Lessons | 12 of 15 | 3 of 15 | 33 | Clay, Ramp, Spotify |

## Not stated, all fields

| Field | Not stated (or none described) |
|---|---|
| Eval size / quality | 10 of 15 (Clay, GitHub, Grab, Kikoff, Meta, OpenAI, Ramp, Snap, Spotify, Stripe) |
| Models | 9 of 15 (Block, GitHub, Grab, Meta, Pinecone, Ramp, Snap, Spotify, Stripe) |
| Interface | 4 of 15 (Block, DoorDash, Kikoff, Meta) |
| Eval method | 3 of 15 (Clay, Kikoff, Stripe) |
| Adoption | 3 of 15 (DoorDash, OpenAI, Vercel) |
| Lessons | 3 of 15 (Clay, Ramp, Spotify) |
| Users | 2 of 15 (Pinecone, Spotify) |
| Context delivery | 1 of 15 (Spotify) |
| Trust | 1 of 15 (Pinecone) |
| Task scope | 0 of 15 |
| Context sources | 0 of 15 |
| Tools | 0 of 15 |

## Cross counts used in the findings

- Fixed question set and eval numbers reported: 5 of 10 (Anthropic, Block, DoorDash, Pinecone, Vercel).
- Fixed question set, no eval numbers: GitHub, Grab, OpenAI, Ramp, Snap.
- Adoption numbers reported: 12 of 15; eval numbers reported: 5 of 15.

## Findings

Each finding is a count from the tables above. None of them states a cause.

1. 13 of 15 describe the agent answering data questions with SQL, and 9 of 15 also describe multi-step investigations such as root-cause analysis.
2. 12 of 15 give the agent table and column docs and 12 of 15 give it notes that people wrote for it, while 6 of 15 give it past queries.
3. 10 of 15 evaluate with a fixed question set, but only 5 of those report the set's size or a correctness number; 12 of 15 report adoption numbers.
4. 6 of 15 name the model that runs the agent; 9 name no model at all.
5. 10 of 15 show the agent's work and 9 of 15 limit its data access, while 4 of 15 describe a human approval step.
