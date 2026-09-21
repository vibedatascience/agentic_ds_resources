# Grab

---

## 2026-08-01 - How AI is transforming analytics at Grab

link: https://engineering.grab.com/how-ai-is-transforming-analytics
authors: Maanas Prabhakar
type: blog
tags: text-to-sql, semantic-layer, evals, agent-harness, mcp, bi
retrieved: 2026-09-21

---

## Introduction

At Grab, analytics sits close to almost every decision that matters. Our north star is the democratisation of intelligence, ensuring that anyone making a business call has immediate access to trustworthy answers.

Over the last two years, model capability has crossed a threshold enabling this shift. Agents now do in minutes what used to take a week: preparing the data, writing queries, running deep analysis and developing insights for business opportunities, designing experiments and interpreting the results, drafting the commentary that follows, and more. Our throughput is no longer rate-limited by how fast an individual can write code, build a deck, or run a deep-dive. It is rate-limited by how fast we can frame the right problem, judge the right answer, and influence the right decision.

As autonomy climbs, an analyst's impact moves from producing the artefact to owning the question and the call behind it, and the role evolves to become part builder, part advisor, part strategist, owning the loop rather than running it. That unlocks two things at once: work we already do, faster and at lower marginal cost, and work we could never staff before, sitting beside every product manager, business owner, and operator at the moment they decide.

## The ladder

We were heavily inspired by Dan Shapiro's framing of five levels for AI coding. We use a similar ladder that defines how much of the loop an agent should own and where human judgement stays for every analytics loop.

One distinction runs across every level: who owns the loop, and where human judgement is required.

| Level | What | Human role | Agent role |
| --- | --- | --- | --- |
| L2 | AI-Assisted | Owns and executes every step; uses AI to draft, suggest, summarise | Drafts SQL, suggests a visualisation |
| L3 | Human plans, agent owns steps, human reviews | Frames the question, picks the metric, the segment, and the comparison frame, reviews evidence, owns the recommendation | Discovers data, writes and runs the query, sanity checks, drafts the write-up, flags caveats |
| L4 | Agent plans, agent owns workflows, human reviews | Sets intent and guardrails; reviews at gates (anomaly, novel scope, sensitive cut); owns the stakeholder relationship and sign-off | Orchestrates discovery through query, analysis, validation, narrative and publish; runs validation, escalates exceptions |
| L5 | End-to-end autonomous | Sets objectives, quality bars, risk thresholds, escalation rules; reviews exceptions only | Detects anomalies and opportunities, runs the loop, surfaces insight, evolves the metric layer, context and skills |

Human judgement remains at every level, and autonomy never removes accountability. Humans own problem framing, canonical metric definitions, the causal story behind a move, business-case assumptions, the go/no-go, and the stakeholder relationship. A higher level means more of the mechanical loop sits with the agent and more human attention concentrates on the ambiguous, high-stakes work.

## Making the climb

Five core capabilities move a workflow up the ladder. They also gate the climb in order: L3 needs execution and certified context, L4 needs gates and agentic review good enough that reviewing only at gates is honest, L5 needs a learning loop that closes.

- Execution: A stack that runs the loop end to end rather than a notebook/workflow a human drives.
- Knowledge: Metrics certified at the right grain, discoverable in our catalogue, grounded in context an agent can read. Ambiguous definitions cause most analytics slop.
- Control: Repeatable expectations become mechanical checks, while human review handles what a rule cannot.
- Review and governance: Agents check their own output against the gates and escalate on defined triggers. We govern definitions, targets, risk and exceptions.
- Learning: When an agent fails the same way twice, we encode the fix into context documents, golden datasets, evals and gates.

## What this looks like in practice

What follows is a set of explorations from the last two years. Some run in production today, while others are still teaching us where the limits are.

### Loops that run end to end

Spartan is our end-to-end agentic analytics workflow, embedded across surface areas (like Slack), and most of its usage comes from people who are not analysts. On any given day, the Slack channel enables a range of analytics actions: from ads salespeople pulling spend breakdowns for a named merchant, to campaign managers sizing audiences for a target segment, and country teams asking why a number moved week on week. All of it in plain business language.

*Figure 1. Index architecture across our knowledge base.*

Two requests from July best demonstrate how it works. A commercial manager asked why revenue fell in the Philippines mid-market segment in the last two weeks of June. Separately, a product manager asked for a summary of a frequency-cap experiment on the ads surface. Both arrived as natural language questions in Slack and took entirely different routes through the system.

The router reads the first as a root-cause question and sends it down the diagnostic path. It identifies the best analysis framework for ads revenue, which is codified knowledge of how the metrics in that domain relate to each other, which dimensions are worth decomposing, and what counts as a meaningful move. Then it works through segment, market and campaign type against certified metrics to isolate what changed. The second question never touches the data lake. The router reads it as an experiment question, selects the experiment skill, pulls the pre-computed scorecard and the test's own metadata from our experiment platform, and summarises the read rather than recomputing it. This is powered through 50+ skills and 120+ analysis frameworks that sit behind that routing decision. Underlying that is an index that tells the agent what to search, context that tells it how to query, and a framework that tells it how to think. Because the frameworks are shared rather than living in an analyst's head, the interpretation compounds instead of being re-derived every time someone asks.

The second example of such a loop is Scarlet, which powers near-self-healing pipelines (L4). When a pipeline fails, an agent runs the root-cause analysis, triages, and then either fixes it or hands it to the team that owns the upstream problem. It escalates when the failure sits outside its documented runbooks or the pre-defined gates fire.

*Figure 2. Scarlet in action on Slack.*

### Context that maintains itself

Context sets an agent's ceiling. An agent that does not know a metric's grain, its exclusions, and its caveats will guess and confidently produce wrong outputs at speed and at scale.

Realising the criticality of this, we have dedicated platform investment, as well as dedicated functional bandwidth to generate context docs.

*Figure 3. ContextIQ.*

Context goes out of date faster than anyone maintains it by hand, so we build the maintenance into our workflows. We built ContextIQ, and its Context Lifecycle Manager, to treat context as something with a lifecycle rather than a document somebody wrote once. A newer skill of ours reads an instrumentation spec alongside the existing context, proposes the SQL changes that follow from it, and updates the context document in the same pass. We work the problem from the other direction too. When we categorise an agent failure in production, we patch the context document behind it.

Two analysts recently used our internal agents to understand how the packaging fee is stored as a configuration. Having found the answer, the agent opened a merge request that committed both a certified-context table reference and a golden-dataset test case, so the next agent to ask the same question would find the answer already documented and the check already in place. One of the analysts spotted a false positive in it. The agent corrected itself and reopened the merge request. That is the learning capability working as designed, and it happened without anyone setting out to demonstrate it.

### Loops that run unattended

The step from L3 to L4 is mostly the step from interactive to scheduled, and it is where we go down the path of autonomous execution, because no human is watching at the moment the work runs.

We have built root-cause analysis (RCA) as a platform capability, and it powers our automated metric and OKR commentaries, which are published through automated agents (configurable cadence). It judges whether a move is meaningful against standard deviation over six months and year on year, walks the metric tree to find which country, segment or funnel stage carried it, and correlates the operational metrics that moved alongside. Importantly, it also scans internal context for what teams changed on the ground, such as delivery fee and incentive moves, merchant visibility shifts, and experiments shipped in the same period. It also compares the movement against the same period in the previous year, which separates a seasonal effect from a real one and enables it to report a Songkran (Thai New Year) dip as amplified rather than merely expected. All of it is grounded in our own context documents, which keeps the narrative about the business rather than generic model output. The analytics owner is tagged on every report, and edits sync back so corrections land in the system.

*Figure 4. OKR commentary shared through RCA agent.*

### Analysts as builders

The clearest evidence that our centre of gravity has moved is BriX, an internal portal we built and run ourselves.

*Figure 5. Home page of BriX.*

The premise is to configure once, host everywhere. We configure a system prompt, a set of context files, a model, the MCP connections and an interface once, and what comes out is a purpose-built analytics surface for a particular team or job. Each one inherits certified data, permissions and reusable agent skills rather than being wired up from scratch, and it runs wherever the work already happens: in Slack, invoked from inside an IDE, or on a schedule with nobody watching. We have grown usage more than 10x since September 2025, with strong retention, and every function at Grab now has users on it. Our aim is to put L3 workflows in the hands of people who are not advanced users.

We run it without a product manager, a technical programme manager or a designer. Our data engineers own the product, the platform, the support queue and the eval loop, with Claude Design doing the interface work and the builders triaging their own bugs. In the first half of this year, they shipped 31 production deployments, 283 merge requests and 60 features.

Three of our apps show the range:

- Insights Lab is the general-purpose surface: a stakeholder asks for a metric, a breakdown or a root-cause in natural language, and the agent loads a specialist skill and answers off certified metrics rather than from memory.
- We built Funnelytics to enable easy understanding of our consumer funnels. A funnel question used to mean an analyst writing the query and then assembling the view in Tableau or Power BI, and doing it again the next time someone wanted a slightly different path through the app. Now a stakeholder picks the events they care about and Funnelytics queries the raw event stream, builds the Sankey and funnel views, and writes the summary. If they cannot find the right instrumentation, which happens often on products still being redesigned, a live debugger lets them tap through the app on their own phone and watch the events fire.
- Monte (like Monte Carlo) runs simulations to put a probability on a business outcome. You give each uncertain input a range rather than a single value, and it runs ten thousand scenarios to return the likelihood of hitting a target.

*Figure 6. Interface of Insights Lab and Funnelytics.*

Outside the portal, the same instinct shows up in smaller ways. Our analysts have been building more bespoke tools that enable better workflows for themselves and stakeholders.

## The path forward

In February, 44% of the tickets our analysts closed were mechanical (data preparation, alerting, reporting); by June, that share had fallen to 30%. That capacity was redirected to other higher-leverage work, such as building new workflows to enable stakeholder self-serve, as well as more time spent on generating deeper insights for business opportunities.

*Figure 7. Comparison of percentage of tickets closed in Q1 vs Q2.*

Importantly, our cycle times reduced by ~33%.

*Figure 8. Comparison of time taken to resolve a ticket in Q1 vs Q2.*

The sharpest version of this sits in a Slack channel where self-serve agents are enabled. In March, an analyst had to step into half of them; by May, it was under a quarter. The share answered with no human involvement rose from 53% to 67% for metric questions, 63% to 90% for data pulls, and 50% to 81% for SQL requests. Just under three in four of the threads were started by someone outside the analytics team, and 85% of them got a first response inside a minute. Nearly every thread is logged as a ticket on the team's board, and roughly two-thirds of the data exploration tickets on that board now arrive through the channel rather than through an analyst, and are solved by our data agents. For the ~230 tickets that arrived via the channel, if we apply a conservative assumption of 1–2 days per ticket, that is 230 to 470 business days of stakeholder asks that would have been in the backlog.

None of these arrived on a roadmap. They came from analysts who saw a loop worth automating and built it, which is why the climb is uneven. These have been strong proof points for us to believe our investments are working, and many of these workflows are starting to operate at scale. We will keep experimenting and iterating, and we expect to get a fair amount of it wrong. An analyst who owns a loop, sets its quality bar and reviews its exceptions is doing a different job from one who answers questions. Most of our team is somewhere in that transition today, and we truly believe it is changing what analytics is at Grab.

Special thanks to the contributors: A3T Braintrust - Maanas Prabhakar, Sneh Agarwal, Nikhil Dwarakanath, Chun Kai Phang, Raghav Garg, Avishek Ghosh, Ankush Khandelwal, Nishant Gupta, Harshita Shah, Lara Pureum Yim, Alex Dobrev Spar/tan 3.0 - Lara Pureum Yim, Kenrick Tan, Tushar Bose, Yong Kai Lim, Dandy Kennedy, Glen Low, Zian Li BriX - Sneh Agarwal, Rishi Raj, Kartik Srinivasan, Aseem Kumar, Eddy Lim, Wen Zhong Tan Funnelytics - Chengxuan Feng, Wingyiu Ng, Zoey Zhou ContextIQ - Defi Mediana, Karen Koh, Anitha Sreedhar, Wanyi Zhu Butler Bot - Adhika Putra Monte - Nikhil Dwarakanath
