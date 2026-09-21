# Snap

---

## 2026-09-10 - DS Agent: Snap's AI Data Scientist

link: https://eng.snap.com/ds_agent
authors: not individually bylined
type: blog
tags: agent-harness, mcp, semantic-layer, evals
retrieved: 2026-09-21
note: Part 1 of a series. Later posts cover the hosted web app and quality evaluation.

---

Part 1 of a series on DS Agent, the data-science agent platform built inside Snap. This post stands on its own; later posts cover the hosted web app and how we evaluate quality.

Over the past year, some of the largest tech companies have written about their in-house data agents. OpenAI described a conversational agent over its warehouse with thousands of daily users. Meta shared an analytics agent adopted by most of its data scientists. Pinterest built the most-used internal agent at the company on top of its metadata platform. All of them are hosted chat services: a centrally built agent you visit, ask a question, and trust to go do the work.

We took a different path, and it started with a complaint.

The pitch was one sentence: "We're using AI, but the workflow is fragmented." For the last few years, data scientists at Snap used different AI tools for different jobs. One tool for coding. Another for analysis. A third for writing things up. Each was useful on its own. Together they were exhausting: copy a query here, paste results there, re-explain the context in every new window, lose the thread by lunch.

The solution we pitched was just as short: build an agent that can handle much of the workflow while keeping the analyst in the loop and the work transparent. But we didn't build it as an app. Snap's data science agent started — and still lives — inside a git repository. Data scientists open the repo in a supported coding-agent environment, and the checkout supplies the instructions, skills, domain knowledge, and guardrails needed to support data-science work. Doing your analysis and improving the agent are the same git workflow.

Six months after it took its current shape, that repo has roughly a hundred contributors across every single domain area and roughly 250 skills. This post is about why we built it this way, and what we learned turning a git repo into a product.

## It started with a deadline

The repo's first commits, from mid-2025, contained a hand-built pipeline of purpose-built agents: a Query Builder Agent, a Data Discovery Agent, an Analysis Agent with statistical testing. It was custom from orchestration to prompts. It didn't scale, and it lay dormant.

The real origin came in January 2026, when a new generation of frontier models landed that could genuinely sustain long-running work: editing dozens of files, running and re-running code, holding a plan across hours. At that same moment, one of us had just joined a new team and been handed a substantial piece of analysis on a tight deadline — a technical challenge compounded by having none of the team's context yet. The core of DS Agent came together in a few days as a practical way to complete that work on schedule.

That situation — a capable analyst with no institutional knowledge — left a permanent mark on the product. It is, almost verbatim, the persona the agent operates under today. More on that below.

The reasoning was simple once we saw it. The frontier labs were shipping better agent harnesses every month — planning, tool use, sub-agents, context management — and any orchestration we hand-rolled would be obsolete by the next model release. What the labs couldn't ship was everything specific to Snap: which tables to trust, what our metrics mean, how our experiment platform works, what a good analysis memo looks like here. So we stopped building the agent and started building its environment.

## Fifty forks in February

Through February we demoed the workspace in every forum that would have us, and the template did what templates do: people forked it. By the end of the month there were roughly fifty forks of DS Agent across DS teams.

Fifty forks were a strong demand signal, but they also exposed an architectural problem. The response was to strengthen shared quality controls at the platform level rather than rely on each user to assess quality independently. The fix was structure: one fast, permissive workspace where anything can be tried, and a clear path for the good parts to earn wider trust. We consolidated the forks into one shared repo where everyone works in the same checkout, so a skill improvement or a guardrail fix lands for every team at once. Most of what follows is what that looks like in practice.

## Why one repo, not a chat app

We started from an observation: data-science work at Snap is already repo-shaped. The queries live in repos. The pipelines live in repos. The notebooks live in repos. A single task can drag you through four or five of them, and every hop is a chance to lose context.

So the bet was: don't build a new place for the agent to live. Take the place where data scientists already work and make it legible to an agent. The product is a repository: instructions, skills, documented tables, guardrails. A capable coding agent that opens it can operate within a data-science workflow defined by the repository.

Three things pushed us that way and kept us there.

First, a DS project is already a directory: queries, notebooks, pipelines, memos. A chat app has to reconstruct that context in every conversation; a coding agent in a checkout simply has it. When an analysis spans days and dozens of files, the repo is the state.

Second, the best agent runtimes are coding agents. The most engineering effort in agentic tooling is being spent on the tools our analysts already use, and building on them means we can often adopt models and harness improvements with less integration work. Our job reduces to context engineering: making the checkout self-describing enough that any of those tools behaves like a Snap data scientist.

Third, a workspace compounds and a chat log doesn't. When an analyst finishes a piece of work in the repo, the artifacts stay: the SQL, the documented findings, the knowledge-base entry, sometimes a new skill. The next analyst's agent reads them. A thousand chat sessions in a hosted app produce a thousand transcripts; a thousand sessions in a shared repo produce a knowledge base.

The trade-off is real: a repo demands more of its users than a text box does. Much of the platform work described below exists to pay down that cost.

## An agent that joined Snap last week

The repo's core instruction file opens with the framing that shaped everything else: treat the agent as a data scientist who joined Snap last week. Smart, fast, fluent in SQL and Python. And completely ignorant of our tables, our metrics, our history. It knows nothing unless the workspace teaches it.

The framing is autobiography. It describes exactly the situation DS Agent was born in: someone new to a team, technically capable, and dangerously short on context. What kept that person safe — asking instead of assuming, citing sources, showing work for verification — is what keeps the agent safe.

It also targets the failure mode that matters most. Language models can produce confident-sounding answers even when important context is missing. Without sufficient context, an agent can confidently explain what "DAU" means at Snap, identify a table as canonical for engagement, or explain why a metric moved — and still be wrong. The "new analyst" framing turns that into a protocol: institutional knowledge must come from a documented source, and if it isn't documented, the agent is required to say "I don't know — is this documented somewhere?"

That framing gives us two rules.

First, the agent carries out the execution steps of the analysis workflow. It writes the code, runs it, reads the output, iterates, and writes up findings with real results. Not "here's a query you could run." It comes back to a human only for judgment calls, access problems, and decisions that genuinely belong to the analyst. The goal is to reduce routine handoffs while preserving human judgment where it matters.

Second, it shows its work. Analytical claims are expected to point back to the query or source that produced them. What's fact and what's inference is labeled as such. The deliverable is a draft for the analyst to verify, not a polished answer to accept on faith. Good analysts already work this way. A number is much more useful when its provenance and method are clear.

## Anatomy of the repo

Here it is, trimmed to what matters:

One instruction file is the brain. It carries the operating rules from the last section: do the work yourself, show everything, know what you don't know.

A skill is a markdown contract. Each one is a folder with a single file: a short description of when it applies, then the playbook.

Below that header sit the steps, the conventions, the known failure modes. The agent picks up a skill when a request matches its description. Our most-used skills are pure markdown. No code at all.

Which points at the counterintuitive lesson of running a skill library: the bottleneck isn't writing procedures, it's writing descriptions. Nobody invokes skills by name. The agent scans descriptions and auto-invokes on a match, so a vague description is a skill that never fires. We learned to treat the description as an API contract — and we now spend more review attention on skill descriptions than on skill bodies.

And every team gets its own corner. A team workspace holds that team's skills, its documented tables, its rules, even its own safety hooks. Teams customize aggressively, and that's by design. The repo deliberately preserves an experimental layer where teams can develop and test ideas before wider use.

## Many hands, one brain

We never wanted the repo to belong to one tool. Different teams like different agents. Some live in an IDE like Cursor. Some prefer a terminal agent like Claude Code or Codex CLI. Some will use something that doesn't exist yet. The repo doesn't care. One instruction file holds the rules, one skill tree holds the playbooks, and each tool reads the same instruction set — today that is one instruction canon serving three agent tools without separate per-tool forks.

That neutrality turned out to be cheap to keep and valuable to have. When a new agent shows up — an IDE, a command-line tool, a hosted service, or another compatible runtime — onboarding it can be a matter of configuration rather than a rewrite. And because no skill is written for a particular tool, skills outlive tools.

## Local metabolism

A workspace that only consumes knowledge decays. Docs drift, skills go stale, every session starts from zero. So we built the repo to digest its own usage. Every session starts with a short briefing: what changed in your area, what's in flight, what needs attention. And every session leaves a residue: a newly documented table, a fixed skill, a line in the log of unverified data someone touched. Capture is deliberately light. We record what happened, never the conversation itself. The last step, where the repo studies its own sessions and proposes new skills, is still being built, and we'd rather say that plainly than oversell it. But the residue is already real. A workspace that collects it on purpose compounds in a way a chat history never does. The anatomy explains how the agent works. It says nothing about what the agent knows. That comes from three places.

## What the agent knows

The first place is the repo itself. It carries plain markdown docs: how our platforms work, what a good report looks like, and, most valuable of all, documented tables. A table doc doesn't just describe columns. It names the pipeline that produces the table and links the query that defines it, which is exactly what the agent needs the moment a number looks wrong.

The second place is live connections. Most knowledge is too alive to copy into a repo, so the agent reaches it over MCP, the open protocol for wiring agents to tools. Our most-used connections: DataHub, our data catalog; Glean, internal search, for Slack threads and Google Docs; and GitHub for code and pull requests. Everything is fetched at analysis time. Fetched content is not persisted into the repo as a substitute for the live source.

DataHub deserves a special mention because it is our primary catalog for data. Tables registered there carry metadata such as schema, ownership, documentation, lineage, and health. When the agent wants to know what a table means, where its numbers come from, or whether anyone still maintains it, the answer comes from DataHub, not from guesswork over column names. And as the next section shows, it's also where trust in data gets recorded.

The third place is other people's repos. Pipelines, models, and notebooks stay where they've always lived. The workspace just knows where that is, and its skills know how to work there without making a mess.

That's the quiet principle behind the whole integration story: we didn't migrate anything. We taught the agent where everything already was. The pipelines stayed in their repos. The docs stayed in their drives. The workspace only holds the map.

Knowing where everything is raises a harder question: out of all of it, what can be trusted?

## Verified or it doesn't ship

An agent will happily query a deprecated table, get plausible numbers, and write a confident report on top of them. A new hire would ask someone "is this the right table?" Our agent has to ask too. And we decided early that the agent should not treat its own judgment as verification. The rule is short: only treat results as trusted and shareable when they come from tables marked as verified in DataHub. That verification mark is the governing trust signal. Not who owns the table. Not how right the schema looks. Not how urgent the deadline is. The mark is where humans record a decision, and the agent reads decisions instead of making them. We put it in one line: governance is a decision, not a derivation.

Our first version of the rule gated access: unverified table, no query, full stop. It was safe and almost unusable — the long tail of undocumented tables is precisely where exploratory data science happens. Analysts don't route around a guardrail like that quietly; they just stop using the tool. So we redesigned it: verification gates trust and shipping, not access.

An unverified table that carries nothing sensitive can now be queried provisionally — after the agent names the table, shows what it knows from metadata alone, and gets explicit human sign-off. The access is logged, every number it touches is marked as provisional, and none of it may land in anything shared. Then the agent offers to document the table properly, and the exception becomes a verified table. The provisional path is a bridge, not a destination: verification stopped being the price of getting any answer and became the path to making numbers final.

And instructions in markdown shape behavior; they don't bound it. For the guardrails that matter, every written rule is paired with an enforcement mechanism in code — the cost check dry-runs the query before execution, and enforcement hooks cover alternate paths that could otherwise produce the same effect. The general lesson: an agent's guardrails are only as strong as the least-guarded layer it can reach the same effect through.

## The escape hatch is a sensor

The provisional-access log could have remained a standalone compliance artifact. We also made it a product-feedback pipeline. Every provisional query logs a reason code, and the codes deliberately split "can't verify" from "won't verify yet": the catalog structurally can't verify this kind of source, verification is stuck in a queue, the table family is too large to verify one by one, or the analyst is simply exploring. The first three are blameless signals routed to the data-platform team. They are, in aggregate, a ranked backlog of where the catalog fails real analysts. The guardrail's own escape hatch tells us exactly where the guardrail needs to grow.

## The trust ladder

Data isn't the only thing that needs trust. Skills need it too.

A skill starts on someone's laptop, where ideas are cheap. If it works, it moves into the team's workspace, where teammates run it and the team owns it. Skills that prove useful beyond one team get shared with everyone. And the best of those are curated for the whole company, powering a hosted app used by people who have never opened an editor.

Each step up widens the blast radius — from your team, to all of DS, to anyone at Snap with a browser — so each step demands a higher bar: review, evaluation against a golden dataset, a privacy and safety checklist. How a skill actually climbs — the reviews, the evaluation, what "proven" means — is a story of its own, and it's the next post in this series.

But notice the direction of flow, because it's the inversion that most distinguishes our architecture from the hosted-agent posts: the hosted app is downstream of the workspace, not the other way around. Capability is authored where the work happens, hardened by review, and only then served broadly. The chat app is a distribution channel for knowledge that practitioners already battle-tested in the repo.

The point of the ladder isn't process. It's that sharing became safe. Before, a broken shared skill was everyone's problem and nobody's fault. Now every skill carries a label that says how far it has been trusted, and by whom.
