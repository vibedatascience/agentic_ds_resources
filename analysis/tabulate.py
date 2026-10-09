"""Write comparison.md and counts.md from the final coding.csv.

Run: python3 analysis/tabulate.py
Each cell value in comparison.md links to its row in coding.csv (GitHub CSV line anchors).
"""
import csv, os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = list(csv.DictReader(open(os.path.join(HERE, "coding.csv"), encoding="utf-8")))
for i, r in enumerate(ROWS):
    r["line"] = i + 2  # header is line 1

COMPANIES = sorted({r["company"] for r in ROWS})
N = len(COMPANIES)
FIELDS = ["users", "interface", "task_scope", "models_named", "context_sources", "context_delivery",
          "tools", "eval_method", "eval_size_quality", "adoption", "trust_measures", "main_lesson"]
HEAD = {"users": "Users", "interface": "Interface", "task_scope": "Task scope", "models_named": "Models",
        "context_sources": "Context sources", "context_delivery": "Context delivery", "tools": "Tools",
        "eval_method": "Eval method", "eval_size_quality": "Eval size / quality", "adoption": "Adoption",
        "trust_measures": "Trust", "main_lesson": "Lessons"}
CATEGORICAL = ["users", "interface", "task_scope", "context_sources", "context_delivery", "tools",
               "eval_method", "trust_measures"]
SHORT = {
    "data team only": "data team", "analysts and PMs": "analysts, PMs", "all employees": "all", "executives": "execs",
    "Slack or chat app": "Slack/chat", "web app": "web", "notebook": "notebook", "IDE or terminal": "IDE/terminal", "BI tool": "BI",
    "answer a question with SQL": "SQL Q&A", "multi-step analysis": "multi-step", "experiment review": "experiments",
    "dashboard or report creation": "reports",
    "table and column docs": "tables", "metric definitions or semantic layer": "metrics", "past queries": "queries",
    "code repos": "code", "past analyses or docs": "docs", "human-written domain notes": "notes",
    "saved corrections or memory": "memory",
    "always in prompt": "prompt", "retrieval search": "retrieval", "tool calls or MCP": "tools/MCP",
    "curated files the agent reads": "files",
    "SQL execution": "SQL", "Python": "Python", "search over docs": "search", "chart creation": "charts",
    "fixed question set with known answers": "question set", "LLM judge": "LLM judge", "human review": "human",
    "user feedback": "user feedback", "none described": "none",
    "shows its work": "work", "cites sources": "sources", "access permissions enforced": "access",
    "human approval step": "approval", "confidence or warnings": "warnings",
    "not stated": "n/s",
}


def short(field, value):
    if value in SHORT:
        return SHORT[value]
    if value.startswith("other: "):
        v = value[7:]
        return v if len(v) <= 22 else v[:20].rstrip() + "..."
    if field == "models_named":
        return value.replace("[production]", "(prod)").replace("[benchmarked]", "(bench)").replace(" [named]", "")
    return value if len(value) <= 34 else value[:32].rstrip(" ,;:") + "..."


def cells():
    d = defaultdict(lambda: defaultdict(list))
    for r in ROWS:
        d[r["company"]][r["field"]].append(r)
    return d


def comparison():
    d = cells()
    out = ["# Comparison table", "",
           f"{N} companies x 12 fields, from `coding.csv` ({len(ROWS)} rows). Each value links to its row in `coding.csv`, which holds the quote and its location. Full value labels are in `codebook.md`; \"n/s\" = not stated.", "",
           "Free-text fields (eval size / quality, adoption, lessons) show each value cut to about 32 characters.", "",
           "| Company | " + " | ".join(HEAD[f] for f in FIELDS) + " |",
           "|---" * (len(FIELDS) + 1) + "|"]
    for c in COMPANIES:
        line = [f"**{c}**"]
        for f in FIELDS:
            vals = [f"[{short(f, r['value']).replace('|', '/')}](coding.csv#L{r['line']})" for r in d[c][f]]
            line.append("; ".join(vals))
        out.append("| " + " | ".join(line) + " |")
    out += ["", "## Abbreviations", "",
            "| Field | Short label = codebook value |", "|---|---|"]
    for f in CATEGORICAL:
        labels = sorted({r["value"] for r in ROWS if r["field"] == f and r["value"] in SHORT and r["value"] != "not stated"})
        out.append(f"| {HEAD[f]} | " + "; ".join(f"{SHORT[v]} = {v}" for v in labels) + " |")
    out.append("| Models | (prod) = runs the agent; (bench) = tested in the agent's harness |")
    return "\n".join(out) + "\n"


def by_value():
    d = defaultdict(lambda: defaultdict(set))
    for r in ROWS:
        d[r["field"]][r["value"]].add(r["company"])
    return d


def counts():
    d = by_value()
    out = ["# Counts", "",
           f"How many of the {N} companies report each value, from `coding.csv`. A company counts once per value. Sorted by count within each field.", ""]
    for f in CATEGORICAL:
        out += [f"## {HEAD[f]}", "", "| Value | Companies | Which |", "|---|---|---|"]
        items = [(v, cs) for v, cs in d[f].items() if not v.startswith("other: ")]
        other = set().union(*[cs for v, cs in d[f].items() if v.startswith("other: ")]) if any(
            v.startswith("other: ") for v in d[f]) else set()
        if other:
            items.append(("other (any)", other))
        for v, cs in sorted(items, key=lambda x: (-len(x[1]), x[0])):
            out.append(f"| {v} | {len(cs)} of {N} | {', '.join(sorted(cs))} |")
        if other:
            labels = sorted((v[7:], sorted(cs)) for v, cs in d[f].items() if v.startswith("other: "))
            out += ["", "Other labels: " + "; ".join(f"{l} ({', '.join(cs)})" for l, cs in labels) + "."]
        out.append("")
    # models
    ms = d["models_named"]
    named = set(COMPANIES) - ms.get("not stated", set())
    prod = {c for v, cs in ms.items() if "[production]" in v for c in cs}
    out += ["## Models named", "", "| Value | Companies | Which |", "|---|---|---|",
            f"| names any model | {len(named)} of {N} | {', '.join(sorted(named))} |",
            f"| names the production model | {len(prod)} of {N} | {', '.join(sorted(prod))} |",
            f"| not stated | {len(ms.get('not stated', set()))} of {N} | {', '.join(sorted(ms.get('not stated', set())))} |", "",
            "| Model as written | Role | Company |", "|---|---|---|"]
    for v, cs in sorted(ms.items()):
        if v == "not stated":
            continue
        name, _, tag = v.partition(" [")
        out.append(f"| {name} | {tag.rstrip(']')} | {', '.join(sorted(cs))} |")
    out.append("")
    # free text
    out += ["## Free-text fields", "", "| Field | Stated | Not stated | Rows | Not stated by |", "|---|---|---|---|---|"]
    for f in ["eval_size_quality", "adoption", "main_lesson"]:
        ns = d[f].get("not stated", set())
        nrows = sum(1 for r in ROWS if r["field"] == f and r["value"] != "not stated")
        out.append(f"| {HEAD[f]} | {N - len(ns)} of {N} | {len(ns)} of {N} | {nrows} | {', '.join(sorted(ns))} |")
    out.append("")
    # not stated overview
    out += ["## Not stated, all fields", "", "| Field | Not stated (or none described) |", "|---|---|"]
    tally = []
    for f in FIELDS:
        cs = d[f].get("not stated", set()) | (d[f].get("none described", set()) if f == "eval_method" else set())
        tally.append((f, cs))
    for f, cs in sorted(tally, key=lambda x: -len(x[1])):
        out.append(f"| {HEAD[f]} | {len(cs)} of {N}" + (f" ({', '.join(sorted(cs))})" if cs else "") + " |")
    out.append("")
    # cross count used in findings
    fixed = d["eval_method"]["fixed question set with known answers"]
    sized = set(COMPANIES) - d["eval_size_quality"].get("not stated", set())
    adopt = set(COMPANIES) - d["adoption"].get("not stated", set())
    out += ["## Cross counts used in the findings", "",
            f"- Fixed question set and eval numbers reported: {len(fixed & sized)} of {len(fixed)} ({', '.join(sorted(fixed & sized))}).",
            f"- Fixed question set, no eval numbers: {', '.join(sorted(fixed - sized))}.",
            f"- Adoption numbers reported: {len(adopt)} of {N}; eval numbers reported: {len(sized)} of {N}.", ""]
    return "\n".join(out), d, fixed, sized, adopt, named, prod


def main():
    open(os.path.join(HERE, "comparison.md"), "w", encoding="utf-8").write(comparison())
    text, d, fixed, sized, adopt, named, prod = counts()
    n = lambda f, v: len(d[f][v])
    findings = [
        f"1. {n('task_scope', 'answer a question with SQL')} of {N} describe the agent answering data questions with SQL, and {n('task_scope', 'multi-step analysis')} of {N} also describe multi-step investigations such as root-cause analysis.",
        f"2. {n('context_sources', 'table and column docs')} of {N} give the agent table and column docs and {n('context_sources', 'human-written domain notes')} of {N} give it notes that people wrote for it, while {n('context_sources', 'past queries')} of {N} give it past queries.",
        f"3. {len(fixed)} of {N} evaluate with a fixed question set, but only {len(fixed & sized)} of those report the set's size or a correctness number; {len(adopt)} of {N} report adoption numbers.",
        f"4. {len(prod)} of {N} name the model that runs the agent; {N - len(named)} name no model at all.",
        f"5. {n('trust_measures', 'shows its work')} of {N} show the agent's work and {n('trust_measures', 'access permissions enforced')} of {N} limit its data access, while {n('trust_measures', 'human approval step')} of {N} describe a human approval step.",
    ]
    text += "\n## Findings\n\nEach finding is a count from the tables above. None of them states a cause.\n\n" + "\n".join(findings) + "\n"
    open(os.path.join(HERE, "counts.md"), "w", encoding="utf-8").write(text)
    print("\n".join(findings))


if __name__ == "__main__":
    main()
