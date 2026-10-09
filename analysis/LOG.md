# LOG

## 2026-10-08: Step 1, read and inventory

- Cloned `vibedatascience/agentic_ds_resources` at `b9bf359`. Work is on branch `analysis`. Existing folders are unchanged.
- Read all 16 posts and viewed all 58 archived images. Counts and summaries are in `inventory.md`.
- Corpus size: 38,237 words in post bodies (brief says about 38,000).

### Archive notes that affect coding

| Company | Note |
|---|---|
| DoorDash | None of the 10 figures is archived, including Figure 6 (architecture) and Figure 9 (/analysis flow). Only their captions are available. |
| Clay | The two interactive embeds (Slack thread, agentic loop walkthrough) are not archived. |
| OpenAI | 6 screenshots exist only as captions. The 5 SVG diagrams render with black boxes in common SVG renderers because of a dot-pattern fill; the hidden labels are readable once that fill is removed. One fact appears only in a diagram: retrieval uses both "SEMANTIC SEARCH RETRIEVAL" and "EXACT TEXT RETRIEVAL" (`context-retrieval.svg`). |
| Anthropic | The appendix skill skeleton is truncated in the archive. Coding uses only the archived summary of it. |
| Block | The adoption chart (`image-06.png`) shows Q1 2026 values of 1,938 and 2,770 unique users. The text says 1,812 and 1,899. Code the text; record the mismatch in the Block rows. |
| Ramp | `analytics-bottleneck.png` shows the setup before the agent, not the agent. |

## 2026-10-08: Step 2, pilot (OpenAI, Ramp, DoorDash)

85 rows in `coding.csv`. All quotes pass `check_quotes.py` (verbatim, 25 words or fewer, location matches the nearest heading).

### Changes to the brief's schema

The 12 fields and their value lists are unchanged. These are added definitions and rules.

| # | Change | Why (pilot case) |
|---|---|---|
| 1 | G1: quotes must be one contiguous verbatim string; a script checks them | Makes the check in step 4 mechanical |
| 2 | G2: diagram labels count as evidence, location `diagram: <file>` | Ramp's users appear only in its architecture diagram |
| 3 | G3: screenshot labels count only for Interface, Tools and Trust measures | Ramp shows SQL in a screenshot; its feedback buttons are not described in text |
| 4 | G4: code current state only | Ramp's abandoned human-in-the-loop review; its planned headless API |
| 5 | G5: platform numbers are not agent numbers | OpenAI "3.5k internal users" and DoorDash "10,000 people" describe the data platform |
| 6 | Users: one widest-reach value plus `executives` if named | Without this, every "all employees" company also gets "analysts and PMs", and counts mean little |
| 7 | Interface: MCP into another tool is coded as that tool | OpenAI's Codex CLI and ChatGPT connectors |
| 8 | Task scope: `other` takes a short label | OpenAI data discovery, Ramp workflow automation |
| 9 | Models: name as written plus `[production]`, `[benchmarked]` or `[named]`; agent products are not models | DoorDash names 4 models with different roles; OpenAI's Codex |
| 10 | Context sources: definitions per value; self-saved memory is not human-written | OpenAI memory layer |
| 11 | Eval method: `LLM judge` needs the post to say a model grades; vetting eval cases is not `human review` | OpenAI's "Evals grader"; DoorDash domain owners vet evals |
| 12 | Trust measures: knowledge-base approvals are not `human approval step` | DoorDash approval queue for knowledge changes |
| 13 | Main lesson: only from lessons/takeaways sections or explicit "we learned/found" sentences; value is a short tag | Ramp has no such section |

### Hard cases in the pilot

| Company | Field | Decision | Alternative |
|---|---|---|---|
| OpenAI | eval_method | No `LLM judge`: the post says "OpenAI's Evals grader" produces "a final score along with an explanation" but never says a model grades | Code `LLM judge` if a grader that writes explanations is read as a model |
| OpenAI | trust_measures | "summarizing assumptions and execution steps alongside each answer" fits no value; not coded | See question 1 |
| OpenAI | adoption | `not stated`; the only user number is for the data platform | |
| Ramp | task_scope | Diagnosing failed transactions coded as `multi-step analysis` | Code as `other: alert diagnosis` |
| Ramp | task_scope | Case studies and fraud-pattern detection coded as `other: workflow automation` | `dashboard or report creation` for case studies |
| Ramp | eval_method | Thumbs up/down in a screenshot and "helped guide our development" not coded as `user feedback` | Code `user feedback` from the screenshot |
| Ramp | trust_measures | In-thread CSV previews of results fit no value | See question 1 |
| Ramp | main_lesson | `not stated` under the rule | Use "we shifted to evaluating our context layer" |
| DoorDash | users | A finance director testing Vera coded as `analysts and PMs` | `not stated`: the post never says who the users are |
| DoorDash | interface | `not stated`; "/analysis flow" suggests a chat command but no surface is named | |
| DoorDash | context_sources | "semantic data layer" plus learned join patterns coded as `metric definitions or semantic layer` | The post never mentions metric definitions |
| DoorDash | context_sources | "filter out low-signal queries" coded as `past queries` | |
| DoorDash | task_scope | Tier 3 "experiment readouts" coded as `experiment review` | The tiers describe question difficulty, not a feature |

### Questions for Rahul

1. Broaden "shows its SQL or code" to "shows its work (SQL, code, steps or result data)"? This would add OpenAI (assumptions and steps) and Ramp (CSV previews).
2. Add a context source value "saved corrections or memory"? OpenAI, Meta, Anthropic and Grab all describe one. Today it is coded only where users write the memory.
3. OpenAI's Evals grader: count as `LLM judge`?
4. OK with the users rule (one widest value plus executives)?
5. OK with screenshots as evidence for Interface, Tools and Trust measures only?
6. Scope questions in `inventory.md` (Pinecone, Anthropic, Stripe, Grab, Kikoff).

## 2026-10-08: Codebook frozen

Rahul approved the pilot and all 5 proposals ("sure"). Applied:

| # | Change | Pilot rows changed |
|---|---|---|
| 14 | Trust value "shows its SQL or code" renamed "shows its work" (SQL, code, steps, assumptions or result previews) | OpenAI +1 (assumptions and steps); Ramp row now cites the CSV previews text instead of the screenshot |
| 15 | New context source value "saved corrections or memory" | OpenAI memory moved from human-written domain notes |
| 16 | `LLM judge` also covers an automated grader that writes an explanation with its score | OpenAI +1 |
| 17 | Users rule (one widest value plus executives) and screenshot rule (Interface, Tools, Trust only) kept | none |
| 18 | Scope: keep all 15 companies; coding limits per company are in `codebook.md` | none |

The scope limits for Pinecone, Stripe and Grab were not spelled out in Rahul's reply. They are the defaults stated in the reply to him and can be revisited.

## 2026-10-08: Step 3, all 15 companies coded

- 402 rows in `coding.csv`. All 15 companies have all 12 fields. `check_quotes.py`: 0 problems. Diagram and screenshot rows (Ramp users, Ramp SQL, Meta sources and confidence) checked by eye against the image files.
- Codebook clarification (no change of meaning): when a post states more than 3 lessons, take lessons-section items first, then sentences framed as "we found/learned" or called a lesson, in post order. DoorDash recoded under it: the "strong indicator" sentence is out; two "We found" sentences are in.
- Most common "not stated": models named (9 of 15), evaluation size or quality (9 of 15).

### Hard cases in step 3

| Company | Field | Decision | Alternative |
|---|---|---|---|
| Block | interface | `not stated`; the only surface named is "Goose" in a diagram and "our internal AI platform" in text, neither mapping to a value | Code as `Slack or chat app` |
| Kikoff | interface | `not stated`; results are posted as Notion comments, which fit no value | Add an interface value for docs tools |
| Kikoff | users | `data team only`; the post frames it as tooling for DS peer reviewers | `not stated` |
| Kikoff | eval_method | `human review` from iterating on cases "where the output was wrong or vague" | `none described` |
| Meta | interface | `not stated`; screenshots show a UI but no label says web, Slack or IDE | `web app` |
| Spotify | users | `analysts and PMs` because over a quarter of users never wrote SQL; no roles named | `not stated` |
| Spotify | eval_method | Conversations and feedback shown to cluster owners coded as both `human review` and `user feedback` | `user feedback` only |
| Stripe | task_scope, tools | SQL coded from the intro's list of workflows Kai was built for ("querying data warehouses") | `not stated` |
| Stripe | context_sources | "context about data quality and our analytics layer" not coded as semantic layer | `metric definitions or semantic layer` |
| Snap | users | `all employees` from skills "curated for the whole company" powering a hosted app | `analysts and PMs`; the post centers on data scientists |
| Snap | task_scope | SQL coded from "the cost check dry-runs the query before execution" | `not stated` |
| Anthropic | context_sources | Past queries not coded: the post says the agent should not read query history directly | `past queries` |
| Grab | main_lesson | `not stated`; "Context sets an agent's ceiling" is followed by "Realising the criticality of this" in the next sentence, not the same one | Code it |
| Pinecone | users | `not stated`; the post names channels, not users or roles | |
| Block | adoption | Text says 1,812 and 1,899 Q1 2026 users; the chart shows 1,938 and 2,770. Text coded, mismatch noted in the value | |

## 2026-10-09: Step 4, agreement check (stop condition hit)

Pass 2 (`coding_pass2.csv`, 430 rows, commit `1039dd5`) was coded in a fresh scheduled session told not to open `coding.csv`, `LOG.md` or their history. Its quotes pass `check_quotes.py`. `compare_passes.py` compares the passes; method is in its docstring. Free-text fields are compared by the source sentence each quote comes from, so different cuts of one sentence agree.

| Field | Agreement |
|---|---|
| models_named | 100% |
| users, interface, context_delivery | 93% |
| main_lesson | 80% |
| eval_method, adoption, trust_measures | 73% |
| task_scope, context_sources, tools, eval_size_quality | 67% |

**7 fields are below 80%. The brief's rule is more than 3, so tabulating is on hold until the definitions are fixed.**

38 company-field disagreements are listed in `disagreements.md` with both quotes, a cause and a provisional call: pass 2 right 13, pass 1 right 8, both or mixed 5, unclear under the codebook 12.

### Proposed definition fixes (for Rahul)

| Fix | Causes | Rule |
|---|---|---|
| 1 | D1 | Tools "search over docs" only when the post says the agent calls a search tool. Retrieval done for the agent before the prompt is context delivery only. |
| 2 | D9 | eval_size_quality = set size and correctness numbers only; speed, tokens, steps and cost are out. Adoption = every stated number on use or time saved within scope; record all of them. |
| 3 | D2, D3, D4 | Code only what the post says the agent does or reads now. Lists of needs, difficulty tiers, platform use cases and raw material distilled into other docs do not count. Multi-step analysis needs a described investigation (root cause, diagnosis, several queries). |
| 4 | D11 | A lessons section is one whose heading or first sentence names lessons, learnings or takeaways. The framing word may be in the quoted sentence or the one right before it. |
| 5 | D5, D7, D8 | A provenance footer is "cites sources" only. "Human review" needs people to judge agent outputs; "shown to owners" is not enough. Evaluations of retrieved context are not answer evaluations. Both passes must check screenshots for interface, tools and trust (G3). |

## 2026-10-09: Fixes applied, disagreements resolved (step 4 done)

Rahul: "Just finish this" (08:01). Read as: accept fixes F1-F5, delegate the disagreement calls, finish steps 5-6.

- `codebook.md` revised with F1-F5, marked in place. One wording change from the proposal: F4 said a lessons section is one whose heading or *first sentence* names lessons. Applied literally, that would have excluded the Block and Pinecone lessons sections, which both passes coded, because the framing words come in their second sentence. F4 was written as "heading, or text before its first sub-heading or list".
- `coding.csv` moved to `coding_pass1.csv`. New `coding.csv` (407 rows) = pass 1 plus every change listed in `resolve.py`. All quotes pass `check_quotes.py`.
- Final calls on the 38 disagreements: pass 2 right 19, pass 1 right 11, mixed or same fact 8. Each is in `disagreements.md` next to the provisional call.
- Sweep of F1-F5 over rows where both passes agreed changed 12 rows: dropped Block on-call triage, DoorDash past queries, DoorDash search over docs, GitHub "3x faster" (speed), Stripe "83% weekly active" (platform-wide, outside scope); added Meta x2 and Clay x1 adoption numbers and one earlier Stripe lesson; requoted Block multi-step and Meta past queries; cut tokens and latency from one Anthropic eval value.
- Not done: a third blind pass under the revised codebook. Agreement in the paper is the pre-fix measure, stated as a limitation.
- `compare_passes.py` limit found: a long paragraph is one source line, so different numbers cut from one paragraph count as agreement (Grab adoption).

## 2026-10-09: Step 5, tabulate

- `tabulate.py` writes `comparison.md` (15 x 12, 407 cell values, each linked to its `coding.csv` line; all links checked) and `counts.md` (counts per value, not-stated tally, cross counts, 5 findings).

## 2026-10-09: Step 6, paper draft

- `paper_draft.md`, about 3,500 words in the body plus 4 tables, following the brief's outline. Every quote checked verbatim against the corpus; Table 4 and the compact matrix checked against `coding.csv` by script.
- Coding by an LLM agent in two sessions is disclosed in Method and Limitations.

### Venue dates checked

| Venue | What was found | Source |
|---|---|---|
| DATA 2027 | 16th International Conference on Data Science, Technology and Applications (INSTICC), Rome, July 19-21, 2027. Regular paper 1st stage Feb 16, 2027; position/regular paper 2nd stage Mar 25, 2027. | beri.net listing. The venue site (data.scitevents.org) could not be fetched without Rahul's approval; confirm there. |
| VLDB 2027 | Athens, Aug 23-27, 2027. No workshops or workshop deadlines listed yet. VLDB 2026 had "1st International Workshop on Agentic Data Systems (ADS) and the 3rd International Workshop on Data-Centric AI (DATAI)" and DASHSys (data-centric agents with human oversight). The "~May 2027" workshop deadline is unconfirmed. | vldb.org/2027/important-dates.html; vldb.org/2026/Workshops/vldb.html |

## Not included

Posts referred to inside the corpus. Not fetched and not added.

| Referred to in | Post |
|---|---|
| Snap | Later parts of the DS Agent series (hosted web app; quality evaluation) |
| Snap | A Pinterest post on its internal agent, cited in Snap's intro |
| DoorDash | Later posts in the Vera series |
| Stripe | A follow-up on how Kai selects skills |
| Pinecone | The Nexus deep dive |
