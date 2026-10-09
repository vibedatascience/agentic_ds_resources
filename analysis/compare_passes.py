"""Compare two coding passes field by field.

Agreement for one company and field = both passes give the same set of codes.
How a code is formed:
  - categorical fields: the value label; every "other: <label>" counts as "other"
  - models_named: the model name, lowercased, with the [tag] removed
  - eval_size_quality, adoption, main_lesson (free text): the source line each
    quote comes from, so two different cuts of the same sentence agree
  - "not stated" / "none described": the empty set (none described is kept as
    its own code for eval_method)
Usage: python3 analysis/compare_passes.py analysis/coding_pass1.csv analysis/coding_pass2.csv
Limit: a long paragraph is one source line, so two passes that cut different
numbers from the same paragraph count as agreeing (seen in Grab adoption).
Writes analysis/agreement.json with per-field rates and every disagreement.
"""
import csv, json, os, re, sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_quotes import posts  # noqa: E402

FIELDS = ["users", "interface", "task_scope", "models_named", "context_sources",
          "context_delivery", "tools", "eval_method", "eval_size_quality",
          "adoption", "trust_measures", "main_lesson"]
FREE = {"eval_size_quality", "adoption", "main_lesson"}


def source_line(company, quote):
    for title, body in posts(company):
        for i, line in enumerate(body.splitlines()):
            if quote and quote in line:
                return f"{title[:25]}#L{i}"
    return "?" + quote[:40]


def code(r):
    f, v, q = r["field"], r["value"], r["quote"]
    if v == "not stated":
        return None
    if f in FREE:
        if r["location"].startswith(("diagram:", "screenshot:")):
            return r["location"] + "|" + q
        return source_line(r["company"], q)
    if f == "models_named":
        return re.sub(r"\s*\[.*?\]", "", v).strip().lower().replace("-", " ")
    if v.startswith("other"):
        return "other"
    return v


def load(path):
    d = defaultdict(lambda: defaultdict(list))
    for r in csv.DictReader(open(path, encoding="utf-8")):
        c = code(r)
        d[r["company"]][r["field"]].append((c, r))
    return d


def main(p1, p2):
    a, b = load(p1), load(p2)
    companies = sorted(set(a) | set(b))
    rates, dis = {}, []
    for f in FIELDS:
        agree = 0
        for c in companies:
            s1 = {x for x, _ in a[c][f] if x}
            s2 = {x for x, _ in b[c][f] if x}
            if s1 == s2:
                agree += 1
                continue
            dis.append({
                "company": c, "field": f,
                "only_pass1": [dict(value=r["value"], quote=r["quote"], location=r["location"])
                               for x, r in a[c][f] if x and x not in s2],
                "only_pass2": [dict(value=r["value"], quote=r["quote"], location=r["location"])
                               for x, r in b[c][f] if x and x not in s1],
                "pass1_not_stated": not s1, "pass2_not_stated": not s2,
            })
        rates[f] = agree / len(companies)
    out = os.path.join(os.path.dirname(os.path.abspath(p1)), "agreement.json")
    json.dump({"rates": rates, "disagreements": dis}, open(out, "w"), indent=1, ensure_ascii=False)
    for f in FIELDS:
        print(f"{f:18} {rates[f]:5.0%}  ({round(rates[f]*len(companies))}/{len(companies)})")
    print(len(dis), "company-field disagreements")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
