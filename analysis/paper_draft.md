# How companies build internal data agents: a coded comparison of 15 engineering blog posts

Rahul Chaudhary (rahul.chaudhary@outlook.com)

Draft, 2026-10-09. Target: DATA 2027 position or regular paper, or a VLDB 2027 workshop on agentic data systems (venue notes in `LOG.md`).

## Abstract

Between September 2025 and September 2026, fifteen companies published engineering blog posts on the internal agents they built to answer data questions. Each post describes one system in its own words, so the systems are hard to compare. We coded 16 posts from 15 companies on 12 design fields, such as who uses the agent, what context it reads, how it is evaluated and what it does to earn trust. Every coded value is backed by a verbatim quote of 25 words or fewer. Two independent coding passes agreed on 67% to 100% of companies per field; after tightening five definitions, we resolved all 38 disagreements by rereading the posts. The posts agree on several choices: 14 of 15 agents run SQL, 12 of 15 read table and column docs and 12 of 15 read notes written by people for the agent. They report evaluation much less often than adoption: 10 of 15 evaluate with a fixed question set, but only 5 of those report its size or a correctness number, while 12 of 15 report adoption numbers. Only 6 of 15 name the model that runs the agent.

## 1. Introduction

Many companies now give employees an agent that answers questions about company data. The agent takes a question in plain language, finds the right tables, writes and runs queries, and returns an answer. Several of these companies have described their systems in public engineering blog posts. The posts are detailed, but each uses its own terms and covers what its authors chose to cover. A reader who wants to know which design choices are common, and which are rare, has to read every post and build the comparison by hand.

This paper builds that comparison for one fixed set of posts. We ask a single question: across 15 companies that have described an internal data agent, what design choices do their agents share, and where do they differ?

We make three contributions:

- a corpus rule set and a 12-field coding schema for data agent posts, with a codebook that gives an example of a quote that counts and one that does not for each field;
- a 15 x 12 comparison table in which every cell is backed by a verbatim quote and its location in the post;
- counts of how many companies report each design choice, including how often each field is not reported at all.

We record what the posts say. We do not judge whether a system is good, rank the systems, or claim reasons for a choice that a post does not state.

## 2. Method

### 2.1 Corpus

The corpus is the `company-blog-posts/` folder of the public repository `vibedatascience/agentic_ds_resources` at commit `b9bf359` (2026-10-03). It holds 16 posts from 15 companies, 38,237 words in total, published between 2025-09-18 and 2026-09-30 [1-15]. Anthropic published two posts about one system, and we code them together. Each archived entry holds the post text verbatim and its diagrams. We read all 58 archived images, because some design facts appear only in a diagram. Ten DoorDash figures, two Clay interactive embeds and six OpenAI screenshots are not archived; the archived Anthropic appendix is truncated. We did not add posts, interview anyone or use general knowledge about a company.

Two posts needed a scope rule. Stripe's Kai is a general platform for knowledge work, so we coded only its statements about data work and platform features that apply to every session. Pinecone's post also promotes a product, so we coded only the internal agent, AskData. For Grab we coded all the analytics agents the post describes as one system.

### 2.2 Coding schema

Table 1 lists the 12 fields. Eight fields have fixed value lists, and a company can take several values. Four fields record free text: model names exactly as written, evaluation numbers, adoption numbers and up to three lessons the authors state.

**Table 1. Coding fields.**

| # | Field | Values |
|---|---|---|
| 1 | Users | data team only; named roles outside the data team; all employees; plus executives if named |
| 2 | Interface | Slack or chat app; web app; notebook; IDE or terminal; BI tool |
| 3 | Task scope | answer a question with SQL; multi-step analysis; experiment review; dashboard or report creation; other |
| 4 | Models named | as written, tagged production, benchmarked or named |
| 5 | Context sources | table and column docs; metric definitions or semantic layer; past queries; code repos; past analyses or docs; human-written domain notes; saved corrections or memory |
| 6 | Context delivery | always in prompt; retrieval search; tool calls or MCP; curated files the agent reads |
| 7 | Tools | SQL execution; Python; search over docs; chart creation; other |
| 8 | Evaluation method | fixed question set with known answers; LLM judge; human review; user feedback; none described |
| 9 | Evaluation size and quality | numbers as written |
| 10 | Adoption | numbers as written |
| 11 | Trust measures | shows its work; cites sources; access permissions enforced; human approval step; confidence or warnings |
| 12 | Main lessons | up to 3 verbatim quotes |

Each value needs a supporting quote of 25 words or fewer, copied as one contiguous string, plus the heading it sits under. A script checks every quote against the archived text and fills its location. "Not stated" is a valid value and is common. Labels inside a diagram count as evidence. Labels in a screenshot count only for interface, tools and trust, because an example screen is not a claim about who uses a system or how well it works. We code the system as it is now, not abandoned approaches or plans, and we do not count numbers about a company's wider data platform as numbers about its agent.

### 2.3 Procedure

We first coded three posts that differ in length and style (OpenAI, Ramp, DoorDash), tightened the definitions that were hard to apply, and froze the codebook. The pilot added clarifying rules and three changes to the value lists: "shows its SQL or code" became "shows its work", which also covers listed steps and result previews; a value for saved corrections or memory was added; and an automated grader that explains its score was counted as an LLM judge.

Coding was done by an LLM agent (Claude) working from the codebook, with the author approving each codebook change. The first pass coded all 15 companies (402 rows). A second pass ran in a fresh session that had no access to the first pass or its log, and produced 430 rows. For each field, we counted the companies for which both passes gave the same set of values. For free-text fields, two quotes agreed when they came from the same sentence of the post.

### 2.4 Agreement

**Table 2. Share of the 15 companies on which the two passes agreed.**

| Field | Agreement |
|---|---|
| Models named | 100% |
| Users; interface; context delivery | 93% |
| Main lessons | 80% |
| Evaluation method; adoption; trust measures | 73% |
| Task scope; context sources; tools; evaluation size and quality | 67% |

Seven fields fell below 80%. Our protocol treats more than three such fields as a sign of unclear definitions, so we stopped before tabulating and studied the 38 disagreements. Most traced to five gaps, and we fixed each one in the codebook:

- whether retrieval that a pipeline runs for the agent also counts as a search tool (it does not);
- whether speed and token counts count as evaluation results (they do not);
- whether lists of needs, difficulty tiers and use cases of the wider platform count as tasks (they do not);
- what makes a section a lessons section;
- how to code a provenance footer and outputs that are only "shown to" owners.

We then resolved each disagreement by rereading the post under the revised codebook. The second pass was right in 19 cases, the first pass in 11, and 8 were mixed or the same fact quoted from different sentences. We also applied the five fixes to rows where both passes had agreed, which changed 12 more rows. The final coding has 407 rows. We did not run a third blind pass under the revised codebook, so Table 2 describes the codebook before the fixes (see Section 5).

## 3. Results

Table 3 gives the compact comparison. The full 15 x 12 table, with a link from each cell to its quote, is in the supplementary file `comparison.md`. Table 4 gives the counts.

**Table 3. Compact comparison.** Interface: S Slack or chat, W web, I IDE or terminal, B BI tool. Tasks: Q SQL questions, M multi-step, E experiments, R reports, O other. Context sources: T tables, S metrics or semantic layer, Q past queries, C code, P past analyses or docs, N human-written notes, M memory. Delivery: P prompt, R retrieval, T tool calls or MCP, F files. Tools: Q SQL, P Python, S search, C charts, O other. Eval: Q question set, J LLM judge, H human review, U user feedback. Trust: W shows work, S cites sources, A access limits, H human approval, C confidence or warnings. Number columns give the count of coded values. "-" = not stated or none.

| Company | Users | Interface | Tasks | Context sources | Delivery | Tools | Eval | Eval numbers | Adoption numbers | Trust | Model named |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Anthropic | all | SIB | QMERO | TSPNM | RTF | QSCO | QU | 5 | 2 | SAHC | Claude |
| Block | all + execs | - | QMO | TSQPN | RT | QSO | QU | 1 | 4 | WSAC | - |
| Clay | all | S | QO | TSCPN | PF | QPC | - | - | 4 | SAC | Opus |
| DoorDash | named roles | - | QM | TCPN | R | QO | QJ | 6 | - | AH | GPT 5.5 |
| GitHub | all | SI | QR | TSQN | T | QO | Q | - | 1 | W | - |
| Grab | all | SWI | QMERO | TSPNM | RTF | QSCO | QH | - | 9 | WAHC | - |
| Kikoff | data team | - | E | SCP | PT | QCO | - | - | 1 | W | Claude |
| Meta | all | - | QM | TSQCPNM | PR | QPSCO | U | - | 6 | WSC | - |
| OpenAI | all | SWI | QMRO | TSQCPM | RT | QSO | QJ | - | - | WSAC | GPT-5.2 |
| Pinecone | - | S | QM | TSQCPNM | RT | QSO | Q | 2 | 4 | - | - |
| Ramp | named roles | S | QMO | TN | RTF | QS | Q | - | 5 | WAC | - |
| Snap | all | WI | QMR | TCPNM | TF | QPSO | Q | - | 2 | WSAHC | - |
| Spotify | - | SWI | Q | TQN | - | Q | U | - | 2 | WSC | - |
| Stripe | all | SWB | RO | N | RT | PO | - | - | 1 | A | - |
| Vercel | all | S | Q | S | F | QO | Q | 2 | - | W | Claude Opus 4.5 |

**Table 4. Companies reporting each value (of 15).**

| Field | Value: companies |
|---|---|
| Users | all employees 10; named roles 2; data team only 1; executives named 1; not stated 2 |
| Interface | Slack or chat 10; IDE or terminal 6; web app 5; BI tool 2; notebook 0; not stated 4 |
| Task scope | SQL questions 13; multi-step analysis 9; other 7; reports 6; experiment review 3 |
| Context sources | table and column docs 12; human-written notes 12; metrics or semantic layer 10; past analyses or docs 10; code repos 7; memory 6; past queries 6 |
| Context delivery | tool calls or MCP 10; retrieval search 9; curated files 6; always in prompt 3; not stated 1 |
| Tools | SQL 14; other 12; search over docs 8; charts 5; Python 4 |
| Evaluation method | fixed question set 10; user feedback 4; LLM judge 2; human review 1; none described 3 |
| Trust measures | shows its work 10; access permissions enforced 9; confidence or warnings 9; cites sources 7; human approval step 4; not stated 1 |
| Models named | names the production model 6; not stated 9 |
| Evaluation numbers | stated 5; not stated 10 |
| Adoption numbers | stated 12; not stated 3 |
| Main lessons | stated 12; not stated 3 |

### 3.1 Five findings

1. **Answering questions with SQL is the shared core.** 13 of 15 posts describe the agent answering data questions with SQL, and 14 of 15 agents can run SQL. 9 of 15 also describe multi-step investigations, such as tracing why a metric moved. The two exceptions are Kikoff, whose agent reviews experiment readouts and posts comments on the experiment's document [4], and Stripe, whose post reports data analysis sessions without saying the agent runs SQL [10].

2. **Most agents read table docs and notes that people wrote for them; fewer read past queries.** 12 of 15 give the agent table and column docs, and 12 of 15 give it notes that people wrote for it: glossaries, gotchas, domain docs or skill files. 6 of 15 give it past queries. Two posts explain why they curate rather than pass query history through. Spotify's domain experts "accepted only 12.5% of the proposed pairs" when shown question-SQL pairs mined from query logs [8]. Anthropic advises: "Treat the query history as raw material for curation, not as a source of truth the agent reads directly." [12]

3. **Evaluation is described more often than it is measured in public.** 10 of 15 evaluate with a fixed question set, but only 5 of those report the set's size or a correctness number. In contrast, 12 of 15 report adoption numbers. The reported evaluations differ widely in size, from 5 representative queries at Vercel [2] to more than 1,900 contributed evaluations at DoorDash [14]. Two of 15 grade with an LLM judge [3, 14], and 3 of 15 describe no evaluation [4, 10, 15].

4. **Most posts do not name the model.** 6 of 15 name the model that runs the agent, and 9 name no model. Only DoorDash reports comparing several models in its own harness [14].

5. **Trust comes mostly from showing work and limiting access, rarely from approval steps.** 10 of 15 show the agent's work, 9 of 15 limit its data access and 9 of 15 have the agent flag problems such as missing access or stale data. 4 of 15 describe a human approval step.

### 3.2 Notes by field

**Users and interface.** Ten of 15 posts give company-wide reach. OpenAI writes that its agent opens analysis "across all functions, not just by our data team" [3]. Kikoff's reviewer serves data scientists only [4]. Slack or a chat app is the most common surface (10 of 15), followed by IDEs and terminals (6 of 15). Snap's main surface is a git repository: "Data scientists open the repo in a supported coding-agent environment" [13]. No post describes a notebook interface.

**Context delivery.** Ten of 15 fetch context through tool calls or MCP at runtime, and 9 of 15 use retrieval search. Six of 15 keep context as files that the agent opens itself. Vercel replaced 17 specialized tools with a bash tool and a SQL tool; the team "stripped the agent down to a single tool: execute arbitrary bash commands" over semantic layer files [2]. Clay uses a catalog file per folder ("Every folder in our codebase has a catalog.yml file.") so the agent reads only what a question needs [15]. Anthropic describes skills the same way: "a skill is a folder of markdown the agent reads on demand" [12].

**Metrics.** Ten of 15 give the agent metric definitions or a semantic layer. Block goes furthest: its metrics tool retrieves approved SQL "and runs that SQL without revealing it to the LLM" [6].

**Evaluation.** The fixed question sets are built in different ways: hand-written golden SQL at OpenAI [3], evals contributed by domain owners and mined from work threads at DoorDash [14], 40 questions from finance leadership at Block [6], and evals drawn from Claude-generated questions plus harvested corrections at Anthropic [12]. Four of 15 also use user feedback as a quality signal.

**Trust.** Meta shows the query behind every number: "Every data point Analytics Agent surfaces is accompanied by the SQL query that produced it, front and center." [5] DoorDash's planning flow waits for the user: "The plan is shown before any query runs, and nothing executes until the user approves or adjusts it." [14] Snap trusts results only from tables a human has marked as verified in its catalog [13]. Anthropic and Clay add a provenance footer to each answer [12, 15].

**Lessons.** Twelve of 15 posts state lessons. Some recur across posts. OpenAI "restricted and consolidated certain tool calls" [3], and Pinecone lists "Fewer tools, better agents." [7] Several lessons concern context: Meta writes that "an AI agent without personalized context is just a chatbot with database access" [5], GitHub found that "the context layer is key" [9], and Kikoff warns that "Claude doesn't know your jargon." [4] DoorDash concludes that "it was data engineering around the harness that proved to be most impactful" [14].

## 4. What is not reported

The fields most often left unstated are the ones a reader would need to compare quality across systems. Evaluation numbers are not stated in 10 of 15 posts, and the model is not named in 9 of 15. Four posts name no interface, 3 describe no evaluation, 3 give no adoption numbers and 3 state no lessons. Where evaluation numbers do appear, they are measured on different sets with different rules, so they cannot be compared with each other. Adoption numbers also use different units: weekly active shares at Meta and Clay, questions answered at Ramp and Pinecone, users since launch at Spotify, and monthly and quarterly users at Block.

## 5. Limitations

- **Self-reported sources.** Every fact comes from a company's own blog post. Posts are written to present a system well, so they likely report successes more often than failures, and a value that is "not stated" does not mean a system lacks it.
- **Small, fixed corpus.** The corpus is 15 companies, mostly large technology firms, in English, frozen at one commit (2026-10-03). Newer posts and later parts of announced series are not included.
- **LLM coding.** Both passes were coded by the same LLM in separate sessions. Their agreement may overstate agreement between independent human coders, who would not share the same tendencies.
- **Agreement before the fixes.** Table 2 measures the codebook before the five fixes. The 38 disagreements were resolved by rereading, but no blind pass was run under the revised codebook, so its agreement is unmeasured.
- **Archive gaps.** Some figures and embeds are missing from the archive, and one Block number differs between text and chart (we coded the text). Coding the Stripe and Pinecone posts required scope rules.

## 6. Conclusion

Across 15 companies, internal data agents share a common core: SQL over a warehouse, table docs and human-written notes as context, and answers that show their work. The posts differ in where the agent lives, how context reaches the model and how far the agent may act without approval. The largest gap is in measurement: most teams describe a fixed evaluation set, but few publish its size or results, and most do not name their model. The coded table, quotes and scripts are public so that others can check each cell and extend the comparison as new posts appear.

## References

1. Ramp. "Meet Ramp Research: Our Agentic Data Analyst." F. Hilaly, C. Duran, J. Sobel. 2025-09-18. https://builders.ramp.com/post/meet-ramp-research
2. Vercel. "We removed 80% of our agent's tools." A. Qu. 2025-12-22. https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools
3. OpenAI. "Inside OpenAI's in-house data agent." B. Xu, A. Suresh, E. Tang. 2026-01-29. https://openai.com/index/inside-our-in-house-data-agent/
4. Kikoff. "Building the AI Experiment Reviewer with Claude." J. Hou, K. Thangarasu. 2026-03-27. https://about.kikoff.com/build/ai-experiment-reviewer
5. Meta. "Inside Meta's Home Grown AI Analytics Agent." Analytics at Meta. 2026-03-30. https://medium.com/@AnalyticsAtMeta/inside-metas-home-grown-ai-analytics-agent-4ea6779acfb3
6. Block. "Building the Data Foundation for Automated Analytics." A. Ransbury, A. Kuttig, P. Azar, Z. Stanford. 2026-04-29. https://engineering.block.xyz/blog/building-the-data-foundation-for-automated-analytics
7. Pinecone. "Inside AskData: How We Slashed Token Consumption by Over 90%." S. Lu. 2026-06-02. https://www.pinecone.io/blog/inside-askdata/
8. Spotify. "Encoding Your Domain Expert: The Context Layer Behind Spotify's Data Assistant." P. Mitsou, J. Warburton. 2026-06-10. https://engineering.atspotify.com/2026/6/encoding-your-domain-expert-the-context-layer-behind-spotifys-data-assistant
9. GitHub. "How we built an internal data analytics agent." M. Vasirani, C. Joseph. 2026-06-19. https://github.blog/ai-and-ml/github-copilot/how-we-built-an-internal-data-analytics-agent/
10. Stripe. "Meet Stripe's Knowledge AI Platform." 2026-07-30. https://stripe.dev/blog/meet-stripes-knowledge-ai-platform
11. Grab. "How AI is transforming analytics at Grab." M. Prabhakar. 2026-08-01. https://engineering.grab.com/how-ai-is-transforming-analytics
12. Anthropic. "How Anthropic enables self-service data analytics with Claude." J. Cherry, C. Peng, J. Jiao, J. Leder, C. Chang. 2026-06-03. https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude; and "Self-service data analytics in Slack: how Anthropic deploys Claude Tag for ad-hoc questions." C. Peng, L. Zhao. 2026-08-13. https://claude.com/blog/self-service-data-analytics-in-slack-how-anthropic-deploys-claude-tag-for-ad-hoc-questions
13. Snap. "DS Agent: Snap's AI Data Scientist." 2026-09-10. https://eng.snap.com/ds_agent
14. DoorDash. "Inside Vera, DoorDash's Data Agent." I. Baldwin, J. Himberg, A. Khandelwal. 2026-09-16. https://careersatdoordash.com/blog/inside-vera-doordashs-data-agent/
15. Clay. "We gave everyone at Clay their own data scientist." J. Hanson, P. Mital. 2026-09-30. https://www.clay.com/blog/building-everyones-personal-data-scientist
16. Corpus and coding: vibedatascience/agentic_ds_resources, branch `analysis`. https://github.com/vibedatascience/agentic_ds_resources
