"""Stock phrases in three tiers.

evidence: reported on every match (tell)
cluster:  reported only when at least CLUSTER_PARAGRAPH matches fall in one paragraph
          or CLUSTER_TEXT matches in the whole text (tell)
context:  always only a hint
"""

import re

CLUSTER_PARAGRAPH = 2
CLUSTER_TEXT = 3


def run(ctx):
    doc = ctx.doc
    src = doc.style_text
    cluster_hits = []
    for p in ctx.catalog["patterns"]:
        if p["category"] != "phrases" or not ctx.enabled(p["id"]) or "_rx" not in p:
            continue
        tier = p.get("tier", "evidence")
        for m in p["_rx"].finditer(src):
            a, b = m.start(), m.end()
            if not m.group(0).strip():
                continue
            blk = doc.block_at(a)
            if blk is None or blk.zone in ("code", "frontmatter", "sources", "meta"):
                continue
            if ctx.allowed(a, b):
                continue
            if tier == "evidence":
                ctx.add(p["id"], a, b, message=_msg(ctx, p, m.group(0)))
            elif tier == "context":
                ctx.add(p["id"], a, b, severity="hint", message=_msg(ctx, p, m.group(0)))
            else:
                cluster_hits.append((p, a, b, blk.index, m.group(0)))
    by_para = {}
    for h in cluster_hits:
        by_para.setdefault(h[3], []).append(h)
    text_trigger = len(cluster_hits) >= CLUSTER_TEXT
    for p, a, b, bi, matched in cluster_hits:
        if text_trigger or len(by_para[bi]) >= CLUSTER_PARAGRAPH:
            ctx.add(p["id"], a, b, message=_msg(ctx, p, matched, cluster=True))
    # nothing below the cluster threshold is reported: single uses are normal language


def _msg(ctx, p, matched, cluster=False):
    matched = re.sub(r"\s+", " ", matched).strip()
    if ctx.lang == "de":
        m = "Floskel „%s“ (%s): %s" % (matched, p["name"], p["description"])
        if cluster:
            m += " Gemeldet, weil sich solche Wendungen hier häufen."
    else:
        m = "Stock phrase \"%s\" (%s): %s" % (matched, p["name"], p["description"])
        if cluster:
            m += " Reported because such phrases pile up here."
    return m
