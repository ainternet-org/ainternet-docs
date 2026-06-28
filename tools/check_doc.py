#!/usr/bin/env python3
"""Doc-posture gate — dogfood the posture model on the docs themselves.

A page must carry what the reader needs. This checks each Markdown page against
the required posture for its type (learn / how-to / quickstart / build-your-own /
protocol / reference / ...). Fail-closed: a missing REQUIRED dimension fails the
page, so a how-to or "build your own AInternet" guide cannot silently ship without
a prerequisite, a guard, a next step — or with banned trust-score language.

Sibling to route-posture (routes) and repo-posture (deploys). Pure stdlib.

    python3 tools/check_doc.py                 # gate all of docs/, exit 1 on any fail
    python3 tools/check_doc.py docs/guides     # gate a subtree
    python3 tools/check_doc.py --advisory      # also print advisory (warn) misses

For the commons. Van de Meent.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "doc_posture.json")
DOCS_DEFAULT = os.path.normpath(os.path.join(HERE, "..", "docs"))


def load():
    with open(MANIFEST, encoding="utf-8") as fh:
        return json.load(fh)


def doc_type(m, rel):
    best = ("default", m["types"]["default"])
    for name, spec in m["types"].items():
        sub = spec.get("match")
        if sub and sub in rel and len(sub) >= len(best[1].get("match", "")):
            best = (name, spec)
    return best


# --- dimension checks: each returns (ok: bool, detail: str) -------------------

def _has_code_block(text):
    return bool(re.search(r"^```", text, re.MULTILINE))


def check_no_banned_doctrine(text, m):
    rules = m["banned_doctrine"]
    pat = re.compile("|".join(rules["patterns"]), re.IGNORECASE)
    allow = [a.lower() for a in rules["allow_if_line_contains"]]
    bad = []
    for i, line in enumerate(text.splitlines(), 1):
        if pat.search(line) and not any(a in line.lower() for a in allow):
            bad.append(i)
    if bad:
        return False, f"banned trust-score language at line(s) {bad[:5]} — {rules['replacement_hint']}"
    return True, ""


def check_identity_first(text, m):
    if re.search(r"\b(identity|JIS|\.aint|who acts|public key|Ed25519)\b", text, re.IGNORECASE):
        return True, ""
    return False, "no identity framing (JIS / .aint / who-acts) — reader sees mechanics before identity"


def check_prerequisites(text, m):
    head = "\n".join(text.splitlines()[:40])
    if re.search(r"(pip install|prerequisite|you (will )?need|before you (start|begin)|requires?|npm install|\]\(\.\.?/)", head, re.IGNORECASE):
        return True, ""
    return False, "no prerequisites near the top (install line / 'you need' / link to a prior page)"


def check_runnable(text, m):
    if _has_code_block(text):
        return True, ""
    return False, "no copy-pasteable code/CLI block"


def check_guard(text, m):
    if re.search(r"(fail[- ]?closed|dark[- ]?by[- ]?default|dark route|consent|SNAFT|Airlock|isolat|permission|posture|deny|revoke)", text, re.IGNORECASE):
        return True, ""
    return False, "no guard named (fail-closed / dark-by-default / consent / isolation / posture) for risky steps"


def check_next_step(text, m):
    tail = "\n".join(text.splitlines()[-25:])
    if re.search(r"(##+\s*(Related|Next|See also|Where to)|\]\(\.\.?/[^)]+\))", tail, re.IGNORECASE):
        return True, ""
    return False, "no onward link / Related section — reader is stranded"


def check_machine_surface(text, m):
    if re.search(r"(resources\.json|api\.json|ai-scan\.json|upip\.json|curl\s|machine-readable|machine-actionable)", text, re.IGNORECASE):
        return True, ""
    return False, "no machine-actionable counterpart (resources.json / api.json / curl path) — an AI curls, it does not read"


def check_conformance_pointer(text, m):
    if re.search(r"(conformance|vectors? (decide|test)|test-vectors)", text, re.IGNORECASE):
        return True, ""
    return False, "no conformance pointer (docs explain; vectors decide)"


CHECKS = {
    "no_banned_doctrine": check_no_banned_doctrine,
    "identity_first": check_identity_first,
    "prerequisites": check_prerequisites,
    "runnable": check_runnable,
    "guard": check_guard,
    "next_step": check_next_step,
    "machine_surface": check_machine_surface,
    "conformance_pointer": check_conformance_pointer,
}


def gate_page(m, path, rel):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    tname, spec = doc_type(m, rel)
    failures, warnings = [], []
    for dim in spec.get("required", []):
        ok, detail = CHECKS[dim](text, m)
        if not ok:
            failures.append((dim, detail))
    for dim in spec.get("advisory", []):
        ok, detail = CHECKS[dim](text, m)
        if not ok:
            warnings.append((dim, detail))
    return tname, failures, warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=DOCS_DEFAULT)
    ap.add_argument("--advisory", action="store_true", help="also print advisory (warn) misses")
    a = ap.parse_args()
    m = load()

    root = a.root
    md = []
    if os.path.isfile(root):
        md = [root]
        base = os.path.dirname(root)
    else:
        base = DOCS_DEFAULT
        for dp, _, fs in os.walk(root):
            for f in sorted(fs):
                if f.endswith(".md"):
                    md.append(os.path.join(dp, f))

    n_fail = n_warn = 0
    for path in sorted(md):
        rel = os.path.relpath(path, base)
        tname, failures, warnings = gate_page(m, path, rel)
        if failures:
            n_fail += 1
            print(f"⛔ {rel}  [{tname}]")
            for dim, detail in failures:
                print(f"     FAIL {dim}: {detail}")
        if warnings and a.advisory:
            n_warn += len(warnings)
            if not failures:
                print(f"⚠️  {rel}  [{tname}]")
            for dim, detail in warnings:
                print(f"     warn {dim}: {detail}")

    total = len(md)
    ok = total - n_fail
    print(f"\n— doc-posture: {ok}/{total} pages carry their required posture"
          + (f", {n_fail} failing" if n_fail else " ✓")
          + (f", {n_warn} advisory misses" if (a.advisory and n_warn) else ""))
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
