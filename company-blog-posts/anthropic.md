# Anthropic

Two posts from Anthropic's Data Science and Data Engineering team. The second builds directly on the first.

---

## 2026-06-03 - How Anthropic enables self-service data analytics with Claude

link: https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude
authors: Josh Cherry, Clement Peng, Johanne Jiao, Justin Leder, Chen Chang
type: blog
tags: text-to-sql, evals, semantic-layer, agent-harness, mcp
retrieved: 2026-09-21
note: The appendix skill-file skeleton is truncated in this archive. Read the full appendix at the link.

---

As many data science and data engineering teams can attest, enabling self-service data analytics has traditionally been a slog.

Making the data model more accessible to less technical coworkers via wide and denormalized tables often leads to overlapping views with inconsistent definitions as the business scales (and does little to bridge the gap for employees with little desire to learn SQL). Alternatively, creating more ringfenced environments for users often misses the long tail of business questions and leads to metric and dashboard bloat as teams silo their work.

The rise of LLMs provides an additional path for self-service analytics that avoids those challenges. However, pointing Claude at a warehouse and letting the agents execute can create a false sense of precision.

The initial elation of liberation from ad-hoc requests turns into dread with the realization that this setup separates stakeholders from the underlying infrastructure, documentation, and expertise that previously steered them toward carefully curated datasets.

At Anthropic, 95% of business analytics queries are automated via Claude, with ~95% accuracy in aggregate. By giving this often rote, repetitive work to Claude, our data science team can focus on more strategic work like causal modeling, forecasting, and machine learning.

After meeting with dozens of Anthropic's top Claude Code users and having seen myriad design patterns for analytics agents, we've cultivated some best practices for other data teams working with LLMs. In this post, we'll share these tips and approaches to maximizing Claude's ability to drive self-serve business insights, including:

- Why analytics accuracy is a context and verification problem, not a code generation issue;
- The three failure modes that cause most errors;
- The agentic analytics stack we built to address these errors;
- How we measure effectiveness; and
- A basic template for how we create the majority of our skills (see the appendix)

## Data is not software

LLMs' generative abilities are a double-edged sword: the mechanisms that enable creative solutions to complex problems can also hallucinate erroneous output. To fully understand the challenges with analytics agents, it's useful to compare them to coding agents.

Coding is an open-ended solution space that rewards the models' creativity, while documentation and tests provide natural guardrails against hallucination. In contrast, for analytics use cases, there's often only a single correct answer using a single correct source in which there's no deterministic way of proving the correctness.

For self-service agentic business analytics, the complexity mainly lies in the ambiguity of the data. The central problem comes down to our ability to map a user's question to specific and up-to-date entities in our data model and know the correct way of working with them. If we can do that, then the resulting execution and SQL becomes trivial.

We've identified three attributes of this problem that account for an overwhelming majority of inaccurate responses:

1. Concept <> entity ambiguity: with hundreds of viable options in a data model (out of potentially millions of fields), the agent is unable to choose the correct fields that best answer a user's question. For example, in measuring the number of active users: what actions constitute being "active"? Do you include fraudulent users? What lookback window do you use?

2. Data staleness: data sources, business definitions, and schemas change constantly; assets and agent knowledge go stale and start returning subtly wrong answers.

3. Retrieval failure: the right information may actually be in the data model and properly annotated, but given the vastness of the search space, the agent simply doesn't find it.

## Our agentic self-service analytics stack

At Anthropic, the main way we minimize these three errors is via our agentic data stack. Each layer exists primarily to attack one or more of these problems:

1. Entity ambiguity: data foundations and sources of truth shrink the space of plausible entities until there's a single governed answer.

2. Staleness: maintenance and validation processes keep everything from rotting as the business changes.

3. Retrieval failure: skills make sure the agent reliably finds and correctly uses that answer.

In this section, we'll discuss how we built each layer.

> For ad-hoc questions asked directly in Slack, see how our data team deploys a data analytics agent with Claude Tag.

### Data foundations

The most important aspect of ensuring analytics agents are accurate is via strong data foundations, which include the data models, transforms, tests, and tables in a data warehouse, along with the metadata describing them. Standard data engineering and data quality practices such as dimensional modeling, shift-left testing, freshness and completeness checks on critical pipelines all still apply (and we won't relitigate these).

Standard data engineering practices like dimensional modeling are just as important as they ever were.

What does change is that the end user of your data model is no longer a data expert (e.g. data scientist), but rather agents acting on behalf of users with varying degrees of data expertise or understanding of the underlying infrastructure. This shift presents a challenge in that the results can't require the user to validate the underlying correctness simply because the end user doesn't know.

The data foundations layer is aimed primarily at ambiguity: if revenue, for example, resolves to one governed dataset instead of forty plausible candidates, the problem largely disappears before the agent ever has to search. It's also where the first staleness defense lives, since the same repo that defines the canonical models is the natural place to enforce that they stay current.

We've seen a few practices work especially well:

- Create canonical datasets: By far the most common failure is that the agent can't map a concept ("revenue for product X") to the single correct table, column, and metric definition, usually because there are multiple plausible candidates with subtly different implementations. The fix is fewer, more heavily governed logical models: curate a small set of canonical, single source-of-truth datasets that are clearly owned, consumption-ready, and discoverable, then aggressively deprecate the near-duplicates. Physical rollups and caches still matter for cost and performance, but they should derive mechanically from the canonical models rather than living alongside them as alternatives. The goal is that when an agent searches for a concept, it finds a single governed answer.
- Enforce your standards: We've found the foundations only hold if the canonical models and metric definitions are enforced by tooling (the agent is structurally routed to them first; more on that below), by CI (changes that bypass them fail review), and by mandate (downstream teams build on the governed layer or explain why not). Governance without enforcement otherwise quickly decays back to the multiple candidates problem.
- Colocate artifacts: Our main defense against constantly changing data models and business logic is colocation. Nearly all data code (i.e., modeling, semantic layer, reference docs, canonical dashboard definitions) lives in a single repo, with CI checks that protect cross-layer integrity. If a modeling change would break a downstream dashboard or invalidate a documented metric, CI flags it and the fix ships in the same PR. (We'll come back to the mechanics of this in the Skills section below.)
- Treat metadata as a first-class product: Coding agents perform well partly because codebases are legible: READMEs, type signatures, docstrings, etc. Your warehouse can be just as legible, but only if column and table descriptions, canonical metric definitions, grain documentation, valid value ranges, lineage, ownership, and model tiering are maintained with the same rigor as the transformations themselves. While not a new insight, good governance provides critical context that helps the agent choose the right dataset.

### Sources of truth

If data foundations are the data warehouse itself, sources of truth are the reference surfaces the agent consults to navigate it. This layer reduces concept <> entity ambiguity and turns "weekly active users" in a stakeholder's question into a specific, governed entity in your data model. Roughly in descending order of trust:

- Semantic layer: the compiled metric and dimension definitions. If a question maps cleanly to a defined metric, the agent calls a function and gets one number, the same number every other surface in the company produces. Our agents are structurally required (by skill instruction) to leverage the semantic layer first (see the appendix). One idea we tried that didn't work: bootstrapping the semantic layer by having an LLM auto-generate metric definitions from raw tables and query logs. It produced plausible-looking definitions that encoded the very ambiguities we were trying to eliminate, and was net-negative on our evals versus a smaller, human-curated layer. Therefore we recommend generating the documentation with Claude, but having a human own the definition.
- Lineage and the transformation graph: when the semantic layer doesn't cover a question, lineage and table ranking (based on number of references) let the agent reason about which upstream models feed a concept, which are deprecated, and which share grain. This transforms "I don't know the metric" into "I know which governed model to aggregate from." It's also the backbone of the freshness and provenance signals we surface in online validation below.
- Query corpus: historical SQL from dashboards, notebooks, and prior analyses. Intuitively, this should be high-value: it's a record of every question already answered correctly. In practice, we found that giving the agent raw retrieval access to thousands of prior queries moved accuracy by less than a point (we walk through that ablation in a later section below). Unstructured retrieval couldn't map a new question to the right precedent. What does work is distilling that corpus into structured per-domain reference docs and reusable analysis patterns described in skills. Treat the query history as raw material for curation, not as a source of truth the agent reads directly.
- Business context: the layer most teams skip, and the one we underrated the longest. An agent that doesn't understand your business will answer what the user asked, but not what they meant. It won't know that "the Q2 launch" refers to a specific product, that two teams define the same term differently, or that a question is being asked because a board meeting is on Thursday. We pipe in a company knowledge graph consisting of indexed docs, roadmaps, decision logs, and our organizational structure so the agent can resolve ambient references and ask better clarifying questions.

The common failure pattern across all four is the same one from the data foundations layer: poor or stale documentation. Claude is exceptionally useful for closing the gap (drafting column descriptions, proposing metric docs from query patterns, flagging undocumented models in CI), but the curation and ownership are managed by humans.

In the next two sections, we discuss how to make that ownership cheap enough that it actually happens.

### Skills

If the sources of truth are the agent's declarative knowledge (i.e., what a metric means) then a skill is its procedural knowledge: which sources to consult in what order, how to navigate ambiguous data, and what a finished analysis looks like.

In Claude Code, a skill is a folder of markdown the agent reads on demand. At Anthropic, the skills we developed are hugely value additive. Without skills, Claude's ability to answer analytics questions accurately didn't exceed 21% on our evals. Adding skills gets these numbers consistently above 95% in aggregate and regularly around 99% in certain domains. See the appendix for a skeleton we use to create a majority of our skills.

Some best practices:

Create pairwise skills: a knowledge skill acts as a thin top-level router that allows additional domain details to load on demand. It says "try the semantic layer first, but if there's no coverage, here are ~30 reference files for this domain describing the relevant tables, columns, joins and gotchas." This router is, in effect, our answer to retrieval failure: rather than letting the agent search a million-field warehouse, it narrows the space to a few dozen curated files before a query is ever written. The runbook skill encodes the process a senior analyst would follow: clarify the question, find sources (via the knowledge skill), run the query, and then loop the result through adversarial review sub-agents. It also bundles a dozen reusable analysis patterns (retention curves, rate decomposition, funnel analysis) so that common requests don't get reinvented each time.

Create proper reference docs: written for retrieval by an LLM. Our reference docs describe tables (grain, scope, and exclusions), the mechanics of gotchas (e.g., "exclude known free-email domains, but keep custom ones like anthropic.com"), and explicit routing triggers (e.g., "IF the question is about experiment lift… DO NOT use for raw event counts") without prescriptive recipes that go stale. See below for a skeleton we use to create reference docs.

```markdown
# [Domain] Tables

## Quick Reference
### Business Context — [what this domain means in plain words]
### Entity Grain — [what one row represents]
### Standard Hygiene Filter — [the filter every query in this domain applies]

## Dimensions
- [How the key dimensions are encoded, and how the same concept is named
  differently across tables]

## Key Tables
### [table_name]
- **Grain**: [...] · **Scope/exclusions**: [...]
- **Usage**: [when to use it, when NOT to, join keys, required filters]
[... one short section per governed table ...]

## Gotchas
- [The wrong-answer modes a senior analyst would warn you about]

## Best Practices / Common Query Patterns
- [Default choices, standard cuts, worked patterns where the exact query
  form is the hard part]

## Cross-References
- [Neighboring domain docs that own adjacent questions]
```

Treat skill maintenance as a first class citizen: Skill docs describe a data model that changes daily, so without active maintenance they're wrong within weeks. We watched our offline accuracy drift from ~95% at launch to ~65% over a month before we treated this as an engineering problem. That meant colocating skill markdown files in the same repo as our transformation models, so the PR that changes a model is the same PR that updates the doc describing it. A code-review hook flags any reporting-model change that doesn't touch a skill file. Roughly 90% of our data-model PRs now include a skill change in the same diff. We also regularly prune skill scaffolding as models improve and previous failure modes no longer apply.

Create a consistent and seamless experience across all surfaces: the same skill must provide the same answer to questions in Slack, in the IDE, in a dashboard tool, and in standalone agent sessions. We did this by ensuring one canonical source (the data repo) and that skill changes are synced automatically. On merge, the skill syncs to a plugin marketplace (for IDE users), to cloud-storage blobs (for hosted apps that read a single file), and is served directly as resources over MCP. We also designed for portability from the start by avoiding hardcoded repo paths and surface-specific namespaces.

### Validation

Finally, validation is how you find out which of the three failure modes is still leaking through.

#### Offline evaluations

A common pattern we see is that data teams will set up elaborate analytic environments without having any process to understand the accuracy of their analytics agents.

One way of addressing this gap is via offline evals, which are simple question / answer pairs. You can think of offline evals similar to offline testing for an ML model in that they don't tell you the performance of your online agents, but they do give you a good sense of whether you'll have any critical gaps.

We deploy two kinds of offline evals at Anthropic. Dashboard-based evals are auto-generated by Claude (then human validated), covering the most common stakeholder questions. Long tail evals are where we feed Claude business context (roadmaps, table docs) and have it generate plausible questions across the rest of the domain. We also continuously harvest every time a stakeholder corrects the agent in a thread as that correction is a candidate eval.

Other best practices, include:

- Anchor ground truth so it can't drift: An eval written against live data goes stale the moment the underlying number moves. Pin every eval to a snapshot date, write it against a stable fact table, or have the grader judge the agent's query rather than its number. Wire the suite into CI so a PR touching a dependency re-runs the affected evals.
- Store results like telemetry, not like test logs: Every run lands in a warehouse table with the skill version, git SHA, model ID, per-assertion pass/fail, token count, and wall-clock. "Did that change help?" becomes a query, and you get the time-series to catch slow regressions that a single CI run won't.
- Gate launches per domain: A domain owner can't announce the agent to their stakeholders until their slice of the eval set clears some threshold (we initially used ~90%). It forces reference-doc fixes before users see the failures.
- Create the appropriate number of evals: The number of evals you should have depends on the complexity of the business area and the complexity of the underlying data model. Calibrate by tracking how well offline accuracy predicts online accuracy: we've found there are diminishing returns past a few dozen per topic (e.g., "growth"), and that ceiling drops with each new model generation.
- Offline eval accuracy should be ~100%; every correct answer should also be hitting your semantic layer (if you have one). Again, this level of accuracy doesn't tell you your system isn't going to produce a wrong answer, just that there are no obvious gaps, assuming you have proper eval coverage.

#### Ablation techniques

Every structural decision about the skill (e.g., which sources to expose, whether a sub-agent earns its latency, whether to merge two skills into one) is made by holding our offline eval set fixed.

We vary exactly one component and compare pass rates. Each run only takes an hour and replaces a lot of arguments. The methodology matters more than any single result:

- Design for null results. Our most useful ablation was a negative one. We gave the agent direct grep access to our entire dashboard, transformation, and analyst-notebook SQL (thousands of files). We then verified in transcripts that it actually read them before every answer. Accuracy moved by less than a point in either direction. We then checked the obvious confounds: was the answer actually in the corpus for the questions it got wrong? About 80% of the time, yes. Did "answer present" predict "now gets it right"? No, the flip rate was flat. The information was there, the agent saw it, and it still didn't use it. That single experiment told us our bottleneck wasn't access to prior work, it was structure (i.e., mapping a question to the right entity). That insight redirected months of roadmap.
- Ablate at PR granularity. Every meaningful skill edit gets a before / after run on the relevant eval slice, with the delta in the PR description. It keeps "I improved the docs" honest and catches the surprisingly common case where a well-intentioned addition makes things worse.
- Keep a short list of what didn't work. Two of ours: stacking additional rounds of doc refinement past a certain point (we hit three consecutive net-negative iterations: the docs were getting longer, not better), and swapping the adversarial reviewer to a cheaper model to cut latency (it lost most of the accuracy wins, for no real speedup). Negative results are cheap to record and they prevent the next person from re-running the same experiment.

#### Online validation

The final step is ensuring the actual online system performance is as accurate as possible. Some of the steps we take include:

- Adversarial review: we've found that employing a Claude skill to aggressively challenge all underlying assumptions on a potential final answer increased accuracy by 6% within our eval set, but at the cost of 32% more tokens and 72% higher latency.
- Provenance footer: every response carries a footer that contains which source tier it came from (semantic layer › curated reference › raw table), how fresh the underlying data is, and who owns the model. It doesn't make the answer more correct, but it does help the consumer judge how much they can trust the response. A "raw table, freshness unknown" footer is a signal to verify before forwarding upstream, and it's one of the few mitigations we have for silent failures.
- Data quality checks: it's possible that your agent is using the right field in the appropriate way, but the data itself is incorrect. Adding basic data quality checks to ensure the referenced field is up-to-date, complete, and has no anomalies is generally good hygiene.
- Passive monitoring: two production signals we track continuously are the share of agent queries that resolve through the semantic layer, and the share of responses that use correction language ("that's the wrong table," "you're missing the fraud filter"). Both feed a dashboard reviewed weekly alongside the offline pass rate.
- Active correction harvesting: the part that closes the loop. A scheduled agent scans stakeholder channels every few hours for similar correction language, drafts a one-line fix to the relevant reference doc, and opens a PR tagged to the domain owner. The fix path is deliberately boring — edit a markdown file, merge, auto-sync everywhere — so a domain owner doesn't spend too much time on the task. The same corrections feed back into the offline eval set.

The failure mode none of this fully catches is the silent one. The answer is wrong, but looks plausible and is used without objection. Our mitigations are the provenance footer, explicit human sign-off on anything leadership-bound, and a standing eval for each domain's top KPIs that sanity-checks against the blessed dashboard daily, though we don't have a robust solution yet.

## Getting started with self-service analytics

If you're starting from zero, a handful of canonical datasets, a few dozen offline evals, and a thin knowledge skill will capture most of the upside; everything else in this post is what we added once those were built.

We also shared many best practices, and not all of them will be appropriate for every data team. Align with your organization on a few principles that will affect your approach by asking:

- How important is a correct answer today vs. in the future? AI models are progressing at a rapid pace. We often see companies building a significant amount of infrastructure to account for current model shortfalls that become moot once those models improve. Knowing where models fall short, and waiting for model improvements to fill the gap has significantly less overhead, but may not fit your company's risk tolerance.
- How do you anticipate the complexity of your business to change over time? Some of the processes we discussed may be overkill if, for example, you don't produce much data, you only have a few consumers of the output, or your data model is likely to remain simple.
- How technical is the intended audience of the output? Phrased differently, if you're building this analytics system for data scientists who can recognize when an answer is incorrect, you may be more tolerant of errors compared to a situation in which the audience has no familiarity with the underlying data model.
- How much are you willing to spend for improved accuracy? We've found certain processes like adversarial validation can significantly improve accuracy, but often at a higher cost and latency.
- What is your comfort around access controls and internal data privacy? Agents are often significantly more performant the more context they have; however, broad data access cuts against most companies' governance posture. This determines whether you're building one agent or many scoped ones.

Whatever your route, our greatest gains have come from addressing each of the three failure modes: collapsing ambiguity into a single governed answer, making the answer easily discoverable, and flagging when either has gone stale.

This article was written by Chen Chang, Clement Peng, Justin Leder, Johanne Jiao, and Josh Cherry, members of the Data Science and Data Engineering team. The authors would like to thank Michael Segner for his contributions.

### Appendix: Skill File Skeleton

*(Truncated in this archive. The full skeleton is at the source link. It covers: a frontmatter description with explicit IF/THEN invocation triggers; a query-execution priority list (managed connection, CLI fallback, else stop); a "Semantic Layer (REQUIRED first step)" section with a four-step required workflow and a "Don't bail early" list of pre-rebutted excuses agents use to skip the semantic layer; date-window and timezone conventions; and a "PART 1: MUST KNOW" section covering red flags, out-of-scope escalation, clarifying the request, checking existing dashboards, entity disambiguation, business terminology, and data integrity requirements.)*

---

## Self-service data analytics in Slack: how Anthropic deploys Claude Tag for ad-hoc questions

link: https://claude.com/blog/self-service-data-analytics-in-slack-how-anthropic-deploys-claude-tag-for-ad-hoc-questions
authors: Clement Peng, Lily Zhao, with contributions from Josh Cherry and Michael Segner
type: blog
tags: text-to-sql, evals, semantic-layer, agent-harness
retrieved: 2026-09-21
date: not shown on the page. Follows the June 3, 2026 post.

---

In our previous post, we described how we enabled Claude to answer data analytics questions with ~95% accuracy through three primary artifacts:

- A governed semantic layer;
- A set of skill files that encode our analytical conventions; and
- An evaluation suite to measure performance.

That post focused on Claude Code (the primary development surface for our data scientists and data engineers), and best practices for improving agentic accuracy.

This post discusses how the data team at Anthropic applies that foundation to where the rest of the company works using Claude Tag (public beta), which is the foundation for our data analytics agent in Slack. Anyone can ask it data-related questions and receive answers backed by the same governed definitions analysts use.

*Fictional recreation of a Claude Tag conversation for illustrative purposes. Details, names, and tools are not real.*

## Best practices for deploying a data analytics agent in Slack

Getting an agent to be accurate and getting it deployed where non-analysts can use it turned out to be quite different motions. We won't rehash our recommendations on accuracy from our prior post as they're still applicable here.

Rather, we'll cover our five most important learnings over the past year for how to deploy a data analytics agent in Slack and how you should think about distribution, permissions, freshness, and observability.

### Refresh skills as often as you refresh your data models

You can teach Claude how to do a task aligned with your style and requirements using a skill, which is a markdown file with natural language instructions and files Claude can reference when needed.

The single most important architectural decision we made was to treat skill files as served content, refreshed continuously, rather than something shipped once and forgotten.

Data models can change several times a day. For example, a column gets renamed, a metric definition is corrected, or a table is deprecated. Every one of those changes needs to land in a skill file in relatively short order. If Claude is reading last Tuesday's copy of the skill, it gives last Tuesday's wrong answer with full confidence.

This tendency can be especially damaging since the data consumer is now completely separated from the context they need to judge the accuracy of the response. They aren't looking at a dashboard with trend lines or associated metrics that can guide their "sniff test." They may receive just a single data point or two in Slack, and if it's not data they look at regularly, they are likely to accept that confidently wrong answer.

To control this ever-changing environment, Claude Tag's runtime mounts our data repo's skills/ directory and re-reads it on every conversation. The skill files are just markdown on disk; the agent reads them the same way it would read any project file.

### Give the agent skills beyond knowing what to query

Our initial instinct for deploying our data analytics agent using Claude Tag was to create a "knowledge skill," which teaches Claude which tables to use and how our semantic layer is organized, and call it a day. We quickly determined that approach would provide correct numbers, but stop short of useful insights.

Most data consumers tend to ask open-ended and ambiguous questions like "what's driving this dip?" or "can you forecast where this lands at month-end?" or "show me this data as a funnel." Answering those requires the agent to know not just where the data is but how an analyst would work with it.

So alongside this knowledge skill, we mounted Claude Tag with additional analytics or runbook skills, including:

- Forecasting: when and how to fit a simple trend, seasonality assumptions, and when to refuse because a series is too short or too noisy.
- Cohort and retention analysis: standard cohort definitions, the retention curve template reported to leadership, and any gotchas (left-censoring, survivorship) that trip up naive implementations.
- Funnel analysis: the canonical stage definitions for key product funnels, so "where are users dropping off in onboarding?" is consistent across responses.
- Charting: visualization conventions like which chart type to use for which question, color palettes, and when a table is clearer than a plot.
- Analytical writing: how to structure a finding (TL;DR first, number, mechanism, caveat), and the level of hedging that's appropriate given the degree of confidence.

Every data team likely already has these conventions; they just usually live in someone's head and are only occasionally documented. Writing them down as skills ensures Claude applies them as consistently as your data scientist would.

### Connect to business context, not just the warehouse

Even this combination of knowledge skills and runbook skills is not always enough to answer a question. When someone asks "why did sign-ups drop on Tuesday?", the answer often isn't in the data model, but rather is frequently spread across Slack threads, incident trackers, release notes, and docs.

To account for these gaps, we wire Claude Tag into our internal knowledge index, which catalogs documents, discussions, and events across the company. When the agent sees a metric move, it can search that index for contemporaneous context: an incident opened that morning, a feature flag flipped, a competitor announcement someone shared in a channel.

The answer now would look like "sign-ups dropped 12% Tuesday: there was a payment-service incident open 9-11am that morning, and the dip is concentrated in the affected region."

If your organization has a knowledge graph, internal search, or even just well-organized incident and changelog feeds, connecting Claude Tag to them is the highest-leverage information you can add after the warehouse itself. You can also connect Claude Tag so it can read and get context from key channels across Slack.

### Permission the service account deliberately

Claude Tag queries your warehouse as a service account, not as the human who asked the question. While that's the right design (since you don't want every Slack user requiring direct warehouse credentials), everyone who can mention the bot has the bot's data access. There is no per-user row-level security: what the service account can read, anyone in the channel can ask about.

We approach this in five ways (and we recommend taking this seriously as it's easy to get wrong and hard to undo):

1. Scope the service account to governed data only. At Anthropic, Claude Tag's service account can read the semantic layer's output tables and the curated marts that feed them. It cannot read raw event streams, staging schemas, or anything in a personal sandbox. If a question requires data outside that boundary, the agent says so rather than guessing. That is also the right user experience because data outside the governed layer hasn't been validated.

2. Classify PII at the column level and deny the service account clearance. Governed data isn't automatically PII safe data (e.g., a curated table can still carry an email address). We maintain a data catalog with column-level lineage, so every column's origin and downstream flow is known. When new columns land, Claude scans them and flags likely PII candidates for human review. A human then applies the classification in the column's metadata, and lineage propagates that label to derived tables. Given Claude Tag's service account holds no PII clearance, the warehouse's column-level access controls make any PII columns invisible to the agent. It can query the table, but the sensitive columns simply aren't readable.

3. Document the connection path in the skill itself. Our warehouse skill has a dedicated section on how the agent connects (whether via CLI, direct API, or an MCP server) and exactly how authentication works for each path. This prosaic feature allows us to differentiate between the agent failing cleanly ("I can't reach the warehouse from this surface; here's why") versus failing confusingly (a query that silently runs against the wrong project, or an auth prompt relayed somewhere it shouldn't be). When the connection mechanics are in the skill, the agent can explain its own constraints.

4. Treat Claude's channel membership as an access grant. Adding Claude Tag to a Slack channel is, in effect, granting that channel's members read access to whatever the agent can query. We made this explicit: Claude is added to a channel by a data-team member, and the data team owns the list of channels.

5. Label every query. For every warehouse query, Claude Tag carries labels identifying the surface, the conversation, and the requesting user (where Slack provides it). This doesn't enforce anything at query time, but it provides cost attribution and audit trails (you can determine who asked the question that scanned 4 TB after the fact).

Our general posture is that a data analytics agent in Slack is a shared read replica of your governed warehouse, and we try to scope it as such.

### Instrument every answer

Determining whether the agent gave a sufficient answer is not something you can eyeball.

We log a structured event for every question Claude Tag handles. This includes:

- Which skill files were loaded and at what version;
- Whether the user reacted with 👍/ 👎 or replied with a correction; and
- Any open data quality warnings on the tables it touched. We also surface any data quality warnings in the answer's footer, so a stale-data alert appears next to the number rather than being invisible.

This telemetry feeds two views. One tracks adoption or what fraction of agent queries route through the governed layer rather than ad hoc SQL by surface and domain. The other tracks correctness measured by the rate of 👎 reactions and corrections by domain. This is the online proxy for accuracy between eval runs.

The adoption metric turned out to be the single most actionable number we tracked. When it dips for a domain, it almost always means either a skill file has drifted or a new class of questions has appeared that the semantic layer doesn't cover.

### Claude Tag threads become the new meeting

Our favorite, most effective Claude Tag threads usually have multiple people in them. In these cases we see people contributing ideas and context while Claude handles the legwork.

For example, a data team member asked Claude why a revenue dashboard was taking a few minutes longer than usual to load. Claude discovered query results weren't being cached and a bug was slowing down how results reached the page.

Claude notified the dashboard owner who decided to fix the cache immediately while handling the bug in a separate motion.

The owner then asked what other dashboards had slowed, and it turned out dozens were impacted by the same caching error. Claude wrote the caching fix, the data team member reviewed it, and all impacted dashboards were functioning at full capacity in less than an hour.

*Fictional recreation of a Claude Tag conversation for illustrative purposes. Incident details, names, and tools are not real.*

These threads are open which is helpful for multiple reasons. People reading along pick up context (what broke, why, how it got fixed) without anyone writing a summary for them. More importantly, they don't have to remain passive readers. Anyone who knows something useful can jump in and contribute, the way the team members did in the example above.

So keep the agent in shared channels and keep the work in threads instead of DMs, as the thread can function as a reviewable historical record.

### Claude Tag handles repetitive tasks

A lot of data work is recurring: pipeline health checks, KPI monitoring, etc. You can ask Claude to create loops that can handle cyclical tasks on schedule or in response to unusual changes. Some data specific examples we've implemented include:

- Proactive Readouts: Claude provides a summary before a weekly standup: what moved last week, how it compares to the week prior, and what's worth noting.
- Test Monitoring: When we're monitoring a launch or an experiment, Claude provides readouts multiple times a day. During one recent experiment, it noticed the settings had changed partway through and helped us catch and fix it early.
- Observability: Other loops monitor our pipelines and dashboards. If a pipeline fails, Claude starts investigating, drafts a fix, and pings the person on call. If a KPI moves unexpectedly, Claude provides likely explanations: a holiday effect? an upstream data change? and checks them before anyone opens a dashboard.
- Triage: Another loop tracks our data questions channel. For each new question, it makes a call: answer it directly, start a deeper investigation, or bring in a human. By the time someone from the data team checks, most of the work is already done.

Claude can also help design the loop. Ask @Claude what repetitive jobs it's seen in your channels and how it can help.

### Stepping in when needed

You can allow Claude to be more proactive in any channel you choose, reading along and stepping in to help when needed. In one of our data channels over the last month, Claude Tag answered more than 75% of questions people posted, typically within a minute or two, even without being called.

For example, an Anthropic team member asked in a public channel whether a dashboard included a new usage category. Within 90 seconds Claude answered how the data was defined, confirmed the new segment was missing, proposed a fix, and drafted a PR. A data scientist reviewed and approved. Claude then merged the PR and refreshed the dashboard.

*Fictional recreation of a Claude Tag conversation for illustrative purposes. Incident details, names, and tools are not real.*

## Getting started

If you've already done the work from our first post, the Slack deployment is mostly plumbing, though the order is important:

1. Permissions first. Decide what the service account can read before you write a line of agent code. It's much easier to widen access later than to claw it back.
2. Distribution second. Pick mounted-repo or skills-over-MCP and verify freshness end-to-end: change a skill file, and confirm Claude Tag picks it up within your SLA.
3. Telemetry from day one. You will not retroactively instrument month-old conversations. Log the structured event on the very first question.
4. Knowledge index when you can. The warehouse answers what; your internal docs and incident feeds answer why. Wire them in as soon as the data path is stable.
5. Analytics skills last. Create the data-access skill first and then let real questions inform which analyst skills (forecasting, cohorts, funnels) your co-workers actually need.

This article was written by Clement Peng and Lily Zhao, members of Anthropic's Data Science and Data Engineering team, with contributions from Josh Cherry and Michael Segner.
