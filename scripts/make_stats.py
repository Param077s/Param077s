#!/usr/bin/env python3
"""
Render stats.svg from the GitHub GraphQL API.

Everything is baked into the file at generation time: no scripts, no external
references, no request made when someone views the profile. GitHub sanitises
SVG in READMEs anyway, and a visitor-triggered image would be a tracking pixel.

Run:  GITHUB_TOKEN=... python3 scripts/make_stats.py
"""

import json
import os
import subprocess
import sys
from datetime import datetime

USER = os.environ.get("GH_USER", "Param077s")
OUT = os.environ.get("OUT", "stats.svg")

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount date weekday } }
      }
    }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}
"""


def fetch():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    cmd = ["gh", "api", "graphql", "-f", f"query={QUERY}", "-F", f"login={USER}"]
    env = dict(os.environ)
    if token:
        env["GH_TOKEN"] = token
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if r.returncode != 0:
        sys.exit(f"GraphQL failed: {r.stderr[:400]}")
    return json.loads(r.stdout)["data"]["user"]


def top_languages(repos, n=6):
    totals, colors = {}, {}
    for repo in repos:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            totals[name] = totals.get(name, 0) + edge["size"]
            colors[name] = edge["node"]["color"] or "#8b949e"
    ranked = sorted(totals.items(), key=lambda kv: -kv[1])[:n]
    grand = sum(v for _, v in ranked) or 1
    return [(k, v / grand, colors[k]) for k, v in ranked]


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# --- layout ---------------------------------------------------------------
CELL, GAP = 11, 2
STEP = CELL + GAP
PAD = 24
GRID_TOP = 128
W = 820


def build(user):
    cc = user["contributionsCollection"]
    cal = cc["contributionCalendar"]
    weeks = cal["weeks"]
    langs = top_languages(user["repositories"]["nodes"])
    stars = sum(r["stargazerCount"] for r in user["repositories"]["nodes"])

    peak = max((d["contributionCount"] for w in weeks for d in w["contributionDays"]), default=0)

    cells = []
    for x, week in enumerate(weeks):
        for day in week["contributionDays"]:
            c = day["contributionCount"]
            lvl = 0 if c == 0 else min(4, 1 + int(3 * (c - 1) / max(1, peak - 1)))
            cx = PAD + x * STEP
            cy = GRID_TOP + day["weekday"] * STEP
            cells.append(
                f'<rect x="{cx}" y="{cy}" width="{CELL}" height="{CELL}" rx="2" class="l{lvl}">'
                f'<title>{day["date"]}: {c}</title></rect>'
            )

    grid_h = 7 * STEP - GAP
    bar_y = GRID_TOP + grid_h + 34
    bar_w = W - 2 * PAD
    segs, tx, labels = [], PAD, []
    for i, (name, frac, color) in enumerate(langs):
        seg = bar_w * frac
        segs.append(
            f'<rect x="{tx:.1f}" y="{bar_y}" width="{max(seg - 2, 1):.1f}" height="9" rx="4.5" fill="{color}"/>'
        )
        tx += seg
        lx = PAD + i * 128
        labels.append(
            f'<circle cx="{lx + 4}" cy="{bar_y + 32}" r="4" fill="{color}"/>'
            f'<text x="{lx + 14}" y="{bar_y + 36}" class="lang">{esc(name)} {frac*100:.0f}%</text>'
        )

    H = bar_y + 56
    stat = lambda x, v, k: (
        f'<text x="{x}" y="72" class="num">{esc(v)}</text>'
        f'<text x="{x}" y="92" class="key">{esc(k)}</text>'
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="GitHub activity for {esc(USER)}">
<style>
  .bg   {{ fill:#ffffff; stroke:#d1d9e0; }}
  .name {{ fill:#1f2328; font:600 15px ui-monospace,SFMono-Regular,Menlo,monospace; }}
  .sub  {{ fill:#59636e; font:400 11px ui-monospace,SFMono-Regular,Menlo,monospace; }}
  .num  {{ fill:#1f2328; font:600 21px ui-monospace,SFMono-Regular,Menlo,monospace; }}
  .key  {{ fill:#59636e; font:400 10px ui-monospace,SFMono-Regular,Menlo,monospace; letter-spacing:.06em; }}
  .lang {{ fill:#59636e; font:400 11px ui-monospace,SFMono-Regular,Menlo,monospace; }}
  .l0 {{ fill:#ebedf0; }} .l1 {{ fill:#9be9a8; }} .l2 {{ fill:#40c463; }}
  .l3 {{ fill:#30a14e; }} .l4 {{ fill:#216e39; }}
  @media (prefers-color-scheme: dark) {{
    .bg   {{ fill:#0d1117; stroke:#3d444d; }}
    .name, .num {{ fill:#f0f6fc; }}
    .sub, .key, .lang {{ fill:#9198a1; }}
    .l0 {{ fill:#151b23; }} .l1 {{ fill:#033a16; }} .l2 {{ fill:#196c2e; }}
    .l3 {{ fill:#2ea043; }} .l4 {{ fill:#56d364; }}
  }}
</style>
<rect class="bg" x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" stroke-width="1"/>
<text x="{PAD}" y="34" class="name">{esc(USER)}</text>
<text x="{PAD}" y="52" class="sub">contributions in the last year</text>
{stat(PAD, cal["totalContributions"], "TOTAL")}
{stat(PAD + 150, cc["totalCommitContributions"], "COMMITS")}
{stat(PAD + 300, cc["totalPullRequestContributions"], "PULL REQUESTS")}
{stat(PAD + 480, cc["totalIssueContributions"], "ISSUES")}
{stat(PAD + 610, stars, "STARS")}
{chr(10).join(cells)}
<text x="{PAD}" y="{bar_y - 12}" class="sub">languages by bytes written</text>
{chr(10).join(segs)}
{chr(10).join(labels)}
<text x="{W - PAD}" y="34" class="key" text-anchor="end">UPDATED {datetime.utcnow():%Y-%m-%d}</text>
</svg>
"""


if __name__ == "__main__":
    svg = build(fetch())
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"wrote {OUT} ({len(svg)} bytes)")
