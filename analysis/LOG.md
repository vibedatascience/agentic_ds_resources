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

## Not included

Posts referred to inside the corpus. Not fetched and not added.

| Referred to in | Post |
|---|---|
| Snap | Later parts of the DS Agent series (hosted web app; quality evaluation) |
| Snap | A Pinterest post on its internal agent, cited in Snap's intro |
| DoorDash | Later posts in the Vera series |
| Stripe | A follow-up on how Kai selects skills |
| Pinecone | The Nexus deep dive |
