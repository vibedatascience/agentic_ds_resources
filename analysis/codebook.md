# Codebook

Status: **frozen 2026-10-08** after Rahul's OK on the pilot. Every change from the brief's schema is listed in `LOG.md`.

Pilot posts: OpenAI, Ramp, DoorDash.

## Scope decisions

| Company | How it is coded |
|---|---|
| Anthropic | Both posts, as one system |
| Grab | All analytics agents in the post together (Spartan, Scarlet, RCA commentary, BriX apps) |
| Kikoff | Kept; the system reviews experiment readouts |
| Pinecone | AskData only. Nexus is coded where the post says AskData runs on it; the public demo repo is not coded |
| Stripe | Only statements about data work, plus platform features that apply to every Kai session (interfaces, harness, access control) |

## General rules

| # | Rule |
|---|---|
| G1 | **Verbatim quotes.** A quote is one contiguous string copied from the post, 25 words or fewer. No ellipses, no joined fragments, no fixed typos. `check_quotes.py` rejects any quote not found character for character. |
| G2 | **Diagrams count.** Text labels inside an archived diagram are valid evidence. Quote the labels, joined with " / ", and set location to `diagram: <file name>`. |
| G3 | **Screenshots count only for what the UI shows.** Labels in a screenshot can support Interface, Tools and Trust measures (for example a visible "SQL Query" panel). They cannot support Users, Evaluation, Adoption or Lessons, because an example screen is not a claim about the system. Location `screenshot: <file name>`. |
| G4 | **Current system only.** Do not code abandoned approaches ("Our first approach was...") or future plans ("will allow", "Going forward"). Usage the post reports as already happening counts, even inside a "Looking forward" section. |
| G5 | **The agent, not the platform.** Numbers and features of the wider data platform are not the agent's. "Our data platform serves more than 3.5k internal users" is not adoption of the agent. |
| G6 | **Location** = the nearest heading above the quote, as written in the post. Text before the first heading is `Intro`. Italic caption and footnote lines add `(caption or note)`. For Anthropic, prefix the post title. `check_quotes.py` fills and checks this. |
| G7 | **One row per value.** The same quote may support several values in different rows. |
| G8 | **"not stated"** gets one row with empty quote and location. Use it whenever no sentence states a value. Never infer. |

## Fields

### 1. users

Who uses the agent.

| Value | Code when the post... |
|---|---|
| data team only | says use is limited to data scientists, analysts or data engineers |
| analysts and PMs | names specific roles or functions outside the data team (PMs, engineers, sales, finance) but does not claim company-wide reach |
| all employees | says anyone, any employee, all functions, or gives company-wide reach |
| executives | names executives, leadership, the CFO or board-level users. Add to one of the values above. |

Rule: code **one** of the first three (the widest reach the post states), plus `executives` if named. A director title alone is not `executives`.

- Counts: "This lowers the bar to pulling data and nuanced analysis across all functions, not just by our data team." (OpenAI, all employees)
- Does not count: "More than 10,000 people at DoorDash rely on a data ecosystem" (the data platform, not the agent; G5)

### 2. interface

Where users reach the agent. Pick all that apply.

| Value | Includes |
|---|---|
| Slack or chat app | Slack, Teams, an internal chat assistant (e.g. internal ChatGPT) |
| web app | a dedicated web UI or portal |
| notebook | Jupyter, Hex or similar |
| IDE or terminal | VS Code, Cursor, Claude Code, Codex CLI, Copilot CLI, any coding agent |
| BI tool | Looker, Tableau, a dashboard tool |

Rule: access "via MCP" into another tool is coded as that tool's category. MCP is not an interface.

- Counts: "as a Slack agent, through a web interface, inside IDEs, in the Codex CLI via MCP" (OpenAI)
- Does not count: "we built Vera, an internal conversational data agent" ("conversational" names no interface; DoorDash = not stated)

### 3. task_scope

What the agent is used for. Pick all that apply.

| Value | Code when the post... |
|---|---|
| answer a question with SQL | says the agent writes or runs SQL to answer a data question |
| multi-step analysis | describes investigations that span several queries or steps: root cause, diagnosis, end-to-end analysis, planning before execution |
| experiment review | says the agent reads, reviews or summarizes A/B test results |
| dashboard or report creation | says the agent produces dashboards, reports, notebooks or recurring digests |
| other: \<label\> | anything else, with a 1-3 word label (e.g. `other: data discovery`) |

- Counts (multi-step): "The agent handles the analysis end-to-end, from understanding the question to exploring the data, running queries, and synthesizing findings." (OpenAI)
- Does not count (report creation): "How do we build evals around more complex data analytics questions and reporting?" (an open question, not a current task; G4)

### 4. models_named

Every model the post names as running in the system. Value = name exactly as written, then a tag:

- `[production]` the post says this model runs the agent
- `[benchmarked]` the post says this model was tested in the agent's harness
- `[named]` the post names the model as used but gives no role

Rule: agent products and harnesses (Codex, Claude Code, Copilot, Cursor) are not models unless the post calls them a model. Embedding APIs without a model name are not recorded.

- Counts: "The current production model - GPT 5.5 - scores highest overall on the benchmark." (DoorDash, `GPT 5.5 [production]`)
- Does not count: "By crawling the codebase with Codex" (Codex is a product here, not a named model)

### 5. context_sources

What knowledge the agent draws on. Pick all that apply.

| Value | Includes |
|---|---|
| table and column docs | schemas, column descriptions, table metadata, lineage, per-table descriptions (human or LLM written) |
| metric definitions or semantic layer | metric definitions, a semantic layer or metrics store, governed metric logic, wherever stored |
| past queries | query history, query logs, labeled or example queries, question-SQL pairs |
| code repos | pipeline code, dbt or transformation code, codebases |
| past analyses or docs | existing documents, wikis, Slack threads, notebooks, prior reports |
| human-written domain notes | free-form notes people write for the agent: glossaries, gotchas, domain docs, rules, instructions |
| saved corrections or memory | corrections or learnings stored from past conversations and reused later, whether the agent or a person writes them |

Rule: anything the post calls memory, or corrections harvested from conversations, goes to `saved corrections or memory`, not `human-written domain notes`. Value added after the pilot.

- Counts (domain notes): "we relied on domain owners to write up technical documentation on their respective areas" (Ramp)
- Does not count (code repos): "At Ramp, that context lives in dbt, Looker, and Snowflake." (names tools that hold metadata; does not say the agent reads code)

### 6. context_delivery

How context reaches the model. Pick all that apply.

| Value | Code when the post says... |
|---|---|
| always in prompt | context is included in every prompt or system prompt |
| retrieval search | context is indexed, embedded or searched and the top results are passed in |
| tool calls or MCP | the agent calls tools or MCP servers at runtime to fetch context, including live warehouse inspection |
| curated files the agent reads | context is kept as files or folders the agent opens itself |

- Counts (curated files): "These documents were then organized into a file system that Ramp Research can access as needed." (Ramp)
- Does not count (tool calls): "New tables are discovered and indexed both agentically at inference time" (does not say how context reaches the model)

### 7. tools

What the agent can run. Pick all that apply.

| Value | Code when the post says the agent... |
|---|---|
| SQL execution | runs queries against a database |
| Python | runs Python or other code for analysis |
| search over docs | searches indexed docs, metadata or knowledge |
| chart creation | makes charts or visualizations |
| other: \<label\> | any other tool, with a short label (web search, SQL validation, bash) |

- Counts (other): "can web search for external information" (OpenAI, `other: web search`)
- Does not count (Python): "publishing notebooks and reports" (a notebook does not say the agent runs Python)

### 8. eval_method

How the team measures quality. Pick all that apply, or `none described`.

| Value | Code when the post says... |
|---|---|
| fixed question set with known answers | a set of questions with expected SQL, answers or rubrics is run against the agent |
| LLM judge | an LLM or model grades the agent's answers |
| human review | people grade the agent's outputs |
| user feedback | user ratings, reactions or corrections are collected as a quality signal |
| none described | the post describes no evaluation |

Rules: `LLM judge` needs the post to say an LLM or model grades, or that an automated grader writes an explanation with its score (OpenAI's Evals grader). A grader that only compares outputs is not a judge. People writing or vetting eval cases is not `human review`.

- Counts (LLM judge): "The final responses are scored with an LLM judge across three criteria" (DoorDash)
- Does not count (human review): "a human-in-the-loop system in Slack that pinged domain owners for every in-domain question. This solution didn't scale" (abandoned; G4)

### 9. eval_size_quality

Numbers about the evaluation, as written. One row per distinct result. Value = short restatement; quote carries the exact numbers. `not stated` if no numbers.

- Counts: "Vera scored 2.60/3.0, a 73% pass rate, while CC scored 2.16/3.0, a 48% pass rate." (DoorDash)
- Does not count: "domain owners accept 95% of the remaining candidates during review" (DoorDash; the share of proposed evals kept, not a quality result for the agent)

### 10. adoption

Numbers about use of the agent: users, questions, sessions, time saved, share of company. One row per distinct number. `not stated` if none.

- Counts: "Since launching in early August, Ramp Research has answered over 1,800 data questions across more than 1,200 conversations with 300 different users." (Ramp)
- Does not count: "OpenAI's data platform serves more than 3.5k internal users" (platform, not agent; G5)

### 11. trust_measures

Features that help users trust or check answers. Pick all that apply.

| Value | Code when the post says... |
|---|---|
| shows its work | the answer includes or links to the SQL or code that produced it, its steps or assumptions, or a preview of the result data (renamed from "shows its SQL or code" after the pilot) |
| cites sources | the answer names or links the tables, docs, results or source tiers it used |
| access permissions enforced | the agent's data access is limited, by user permissions or by a fixed scope for the agent |
| human approval step | a person approves the agent's plan, query, action or output before it runs or is used |
| confidence or warnings | the agent flags uncertainty, missing access, stale data or out-of-scope questions |

Rule: approval of changes to the knowledge base is not a `human approval step` (it governs context, not answers).

- Counts (human approval): "The plan is shown before any query runs, and nothing executes until the user approves or adjusts it." (DoorDash)
- Does not count (human approval): "Material changes result in a change proposal that flows through an approval queue" (knowledge changes, DoorDash)

### 12. main_lesson

Up to 3 lessons the authors state. Value = a short tag; quote = the lesson verbatim.

Rule: take lessons only from a section titled lessons, learnings or takeaways, or from a sentence where the authors say they learned, found, discovered or realized something, or call it a lesson. Otherwise `not stated`. When there are more than 3, take lessons-section items first, then the framed sentences, each in post order.

- Counts: "We also discovered that highly prescriptive prompting degraded results." (OpenAI)
- Does not count: "Collapsing the cost of asking a question to near-zero changes who asks, when they ask, and what they ask." (Ramp; an observation, not framed as a lesson)
