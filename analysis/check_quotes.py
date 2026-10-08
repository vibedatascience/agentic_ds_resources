"""Check every quote in coding.csv against the archived posts.

For each row with a quote:
  - the quote must appear verbatim in the company's post file (rows located at
    "diagram: <file>" or "screenshot: <file>" are skipped; check those by eye);
  - the quote must be 25 words or fewer;
  - location "AUTO" is replaced with the nearest heading above the quote, plus
    "(caption or note)" when the quote sits in an italic caption or footnote line.
A filled location is compared with the computed one and reported if different.

Usage: python3 analysis/check_quotes.py analysis/coding.csv [--write]
"""
import csv, glob, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "company-blog-posts")
FILES = {os.path.basename(p)[11:-3]: p for p in glob.glob(os.path.join(ROOT, "20*.md"))}


def posts(company):
    """Yield (post_title, body_lines) for each post of a company."""
    text = open(FILES[company.lower()], encoding="utf-8").read()
    parts = re.split(r"^## \d{4}-\d{2}-\d{2} - (.*)$", text, flags=re.M)
    for i in range(1, len(parts), 2):
        body = parts[i + 1]
        m = re.search(r"^---\s*$", body, flags=re.M)  # end of metadata block
        yield parts[i], body[m.end():] if m else body


def locate(company, quote):
    hits = []
    for title, body in posts(company):
        heading, in_code = "Intro", False
        for line in body.splitlines():
            if line.lstrip().startswith("```"):
                in_code = not in_code
            h = None if in_code else re.match(r"^#{1,6}\s+(.*)$", line)
            if h:
                heading = h.group(1).strip()
                continue
            if quote in line:
                cap = line.lstrip().startswith("*") and not line.lstrip().startswith("**")
                hits.append((title, heading + (" (caption or note)" if cap else "")))
    return hits


def main(path, write):
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    errors = 0
    for n, r in enumerate(rows, start=2):
        q, loc = r["quote"], r["location"]
        if not q:
            if r["value"] not in ("not stated", "none described"):
                print(f"row {n}: {r['company']}/{r['field']}: value without quote"); errors += 1
            continue
        words = len(q.split())
        if words > 25:
            print(f"row {n}: {r['company']}/{r['field']}: {words} words"); errors += 1
        if loc.startswith(("diagram:", "screenshot:")):
            continue
        hits = locate(r["company"], q)
        if not hits:
            print(f"row {n}: {r['company']}/{r['field']}: quote not found: {q[:60]}"); errors += 1
            continue
        multi_post = len({t for t, _ in posts(r["company"])}) > 1
        computed = "; ".join(f"{t} > {h}" if multi_post else h for t, h in hits)
        if loc == "AUTO":
            r["location"] = computed
        elif loc != computed:
            print(f"row {n}: {r['company']}/{r['field']}: location '{loc}' but found at '{computed}'"); errors += 1
    print(f"{len(rows)} rows checked, {errors} problems")
    if write:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys())
            w.writeheader(); w.writerows(rows)
    return errors


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1], "--write" in sys.argv) else 0)
