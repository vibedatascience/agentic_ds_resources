# DoorDash

---

## 2026-09-16 - Inside Vera, DoorDash's Data Agent

link: https://careersatdoordash.com/blog/inside-vera-doordashs-data-agent/
authors: Ian Baldwin, Jacopo Himberg, Akshat Khandelwal
type: blog
tags: text-to-sql, evals, agent-harness, semantic-layer
retrieved: 2026-09-21
status: TEXT NOT ARCHIVED

---

The site returns 403 to direct fetch and the crawler could not render it, so the article text is not archived here. Read it at the link above.

What the page contains, from its structure:

Vera is DoorDash's internal conversational data agent, covering 200,000+ datasets and 350 petabytes for 10,000+ employees. Pass rate moved from 43% to 90% across 1,900+ contributed evaluations spanning 19 business domains. The stated conclusion is that harness engineering mattered more than model choice: frontier models score within a few points of each other in the same harness, while Vera on Opus 4.8 scored 2.60/3.0 (73% pass) against Claude Code on the same model at 2.16/3.0 (48% pass) on a 100-question subset.

Architecture covered: two parallel searches over human-authored knowledge and modeled tables with access restricted to verified sources; a data modeling layer; three-criterion LLM judging on tool usage, table selection and answer correctness, with evals auto-mined from Slack threads and Jira tickets and vetted by domain owners; three complexity tiers (descriptive, decision-influencing, causal/forecasting) with an `/analysis` flow that plans before executing on the harder ones. Open questions the authors list: cost reduction, complex analytics eval development, and measuring business impact.

Figures in the post:

| # | Caption |
|---|---|
| Table 1 | One full benchmark run, every model in the same harness |
| Figure 1 | Accuracy against tokens per question on the 100-question subset |
| Figure 2 | Median and p90 answer time for the same models and effort levels |
| Figure 3 | Answer time distribution per model on the full run |
| Figure 4 | Average tool calls and agent steps per question |
| Figure 5 | Pass rate by model from March to September |
| Figure 6 | Vera's path from a question to a grounded answer |
| Figure 7 | Growth of the evaluation set |
| Figure 8 | Answer time against the data each run pulled back from tools |
| Figure 9 | Vera's /analysis flow on a merchant trend question |
