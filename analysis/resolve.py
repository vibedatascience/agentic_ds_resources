"""Build the final coding.csv from pass 1 plus the resolutions.

Every change to pass 1 is listed below with its reason code:
  Dn  = disagreement n in disagreements.md
  S-Fx = a sweep of fix Fx over rows where both passes agreed
Run: python3 analysis/resolve.py && python3 analysis/check_quotes.py analysis/coding.csv --write
"""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
P1 = list(csv.DictReader(open(os.path.join(HERE, "coding_pass1.csv"), encoding="utf-8")))
P2 = list(csv.DictReader(open(os.path.join(HERE, "coding_pass2.csv"), encoding="utf-8")))

DROP = [  # (company, field, value, reason)
    ("Spotify", "users", "analysts and PMs", "D1 F3"),
    ("Block", "task_scope", "dashboard or report creation", "D3 F3"),
    ("Block", "task_scope", "other: on-call triage", "S-F3 platform use case, same sentence as D3"),
    ("Clay", "task_scope", "multi-step analysis", "D4 F3"),
    ("DoorDash", "task_scope", "experiment review", "D5 F3"),
    ("GitHub", "task_scope", "other: data discovery", "D6 F3 benefit, not a task"),
    ("Stripe", "task_scope", "answer a question with SQL", "D7 F3"),
    ("DoorDash", "context_sources", "metric definitions or semantic layer", "D9 F3"),
    ("DoorDash", "context_sources", "past queries", "S-F3 queries are distilled into the data model"),
    ("Snap", "context_sources", "past queries", "D12"),
    ("Stripe", "tools", "SQL execution", "D18 F3"),
    ("DoorDash", "tools", "search over docs", "S-F1 retrieval is a pipeline step"),
    ("Kikoff", "eval_method", "human review", "D19 F5"),
    ("Pinecone", "eval_method", "LLM judge", "D20 F5"),
    ("Spotify", "eval_method", "human review", "D22 F5"),
    ("Block", "trust_measures", "human approval step", "D23 verification is optional"),
    ("GitHub", "eval_size_quality", "curated context: more accurate and 3x faster to the right answer", "S-F2 speed only"),
    ("Stripe", "adoption", "83% of Stripe weekly active", "S scope: platform-wide use, not data work"),
    ("Grab", "main_lesson", "not stated", "D37 F4"),
]

FROM_P2 = [  # (company, field, value, reason)
    ("GitHub", "task_scope", "dashboard or report creation", "D6"),
    ("Stripe", "task_scope", "other: data analysis", "D7"),
    ("Grab", "context_sources", "past analyses or docs", "D10"),
    ("GitHub", "tools", "other: pull request creation", "D14"),
    ("Pinecone", "tools", "other: correction submission", "D16"),
    ("Grab", "trust_measures", "human approval step", "D25 G3"),
    ("Grab", "trust_measures", "shows its work", "D25 G3"),
    ("Ramp", "trust_measures", "confidence or warnings", "D26 G3"),
    ("Anthropic", "eval_size_quality", "raw query corpus access moved accuracy under 1 point", "D27"),
    ("DoorDash", "eval_size_quality", "ablations on 100-question subset", "D29"),
    ("Grab", "adoption", "analyst intervention from half to under a quarter of threads", "S-F2 within D32 paragraph"),
    ("Grab", "adoption", "just under 3 in 4 threads from outside analytics", "S-F2"),
    ("Grab", "adoption", "about two-thirds of exploration tickets arrive via channel", "S-F2"),
    ("Grab", "adoption", "~230 tickets, 230 to 470 business days", "S-F2"),
    ("Pinecone", "adoption", "~49% follow-up runs", "D33"),
    ("Ramp", "adoption", "thousands of questions per month", "D34"),
    ("Grab", "main_lesson", "context is critical", "D37 F4"),
]

NEW = [  # full rows written here, reason
    ({"company": "Spotify", "field": "users", "value": "not stated", "quote": "", "location": ""}, "D1"),
    ({"company": "Kikoff", "field": "eval_method", "value": "none described", "quote": "", "location": ""}, "D19"),
    ({"company": "GitHub", "field": "eval_size_quality", "value": "not stated", "quote": "", "location": ""}, "S-F2"),
    ({"company": "Meta", "field": "adoption", "value": "used by thousands within about six months",
      "quote": "Analytics Agent went from a weekend prototype on a devserver to a company-wide tool used by thousands in roughly six months.", "location": "AUTO"}, "S-F2"),
    ({"company": "Meta", "field": "adoption", "value": "H2 2025: 750+ feedback posts, 130+ wins posts, 40+ community talks",
      "quote": "In H2 2025 alone we had 750+ feedback posts, 130+ wins & best practices posts, 40+ community talks.", "location": "AUTO"}, "S-F2"),
    ({"company": "Clay", "field": "adoption", "value": "power users ask 10+ questions per week",
      "quote": "monty’s biggest power users ask upwards of 10+ per week.", "location": "AUTO"}, "S-F2"),
    ({"company": "Stripe", "field": "main_lesson", "value": "micro-agents were hard to maintain",
      "quote": "found the proliferation of these micro-agents increasingly hard to monitor and maintain", "location": "AUTO"}, "S-F4 framed sentence, first in post order"),
]

REQUOTE = [  # (company, field, value, new quote, reason)
    ("Block", "task_scope", "multi-step analysis",
     "follow up with an ad-hoc investigation into the underlying data (routed through Query Expert MCP), all in the same session.",
     "S-F3 old quote described a need, new quote describes an investigation"),
    ("Meta", "context_sources", "past queries",
     "Reference Experts: Points the agent to specific people whose SQL query history it should learn from.",
     "S-F3 old quote described queries distilled into descriptions"),
]

REVALUE = [  # (company, field, old value, new value, reason)
    ("Anthropic", "eval_size_quality", "adversarial review: +6% accuracy, +32% tokens, +72% latency",
     "adversarial review: +6% accuracy", "S-F2 tokens and latency out"),
]


def key(r):
    return (r["company"], r["field"], r["value"])


def main():
    rows = [dict(r) for r in P1]
    for c, f, v, _ in DROP:
        n = len(rows)
        rows = [r for r in rows if key(r) != (c, f, v)]
        assert len(rows) == n - 1, ("drop", c, f, v)
    for c, f, v, _ in FROM_P2:
        src = [r for r in P2 if key(r) == (c, f, v)]
        assert len(src) == 1, ("p2", c, f, v)
        r = dict(src[0]); r["location"] = r["location"] if r["location"].startswith(("diagram:", "screenshot:")) else "AUTO"
        rows.append(r)
    for r, _ in NEW:
        rows.append(dict(r))
    for c, f, v, q, _ in REQUOTE:
        hit = [r for r in rows if key(r) == (c, f, v)]
        assert len(hit) == 1, ("requote", c, f, v)
        hit[0]["quote"], hit[0]["location"] = q, "AUTO"
    for c, f, old, new, _ in REVALUE:
        hit = [r for r in rows if key(r) == (c, f, old)]
        assert len(hit) == 1, ("revalue", c, f, old)
        hit[0]["value"] = new
    # Stripe: put the earlier lesson first (post order)
    order = ["Anthropic", "Block", "Clay", "DoorDash", "GitHub", "Grab", "Kikoff", "Meta",
             "OpenAI", "Pinecone", "Ramp", "Snap", "Spotify", "Stripe", "Vercel"]
    fields = ["users", "interface", "task_scope", "models_named", "context_sources", "context_delivery",
              "tools", "eval_method", "eval_size_quality", "adoption", "trust_measures", "main_lesson"]
    lesson_first = {"micro-agents were hard to maintain": 0}
    rows.sort(key=lambda r: (order.index(r["company"]), fields.index(r["field"]),
                             lesson_first.get(r["value"], 1)))
    # every company-field has values xor a not stated / none described row
    for c in order:
        for f in fields:
            vs = [r["value"] for r in rows if r["company"] == c and r["field"] == f]
            empty = [v for v in vs if v in ("not stated", "none described")]
            assert vs and (not empty or len(vs) == 1), (c, f, vs)
    with open(os.path.join(HERE, "coding.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["company", "field", "value", "quote", "location"])
        w.writeheader(); w.writerows(rows)
    print(len(rows), "rows written to coding.csv")


if __name__ == "__main__":
    main()
