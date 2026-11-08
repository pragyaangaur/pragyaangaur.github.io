"""Fetch the GitHub contribution calendar into assets/contrib.json. Run: GITHUB_TOKEN=... python3 tools/contrib.py

The daily workflow in .github/workflows/contrib.yml runs this, so the chart on the board stays current.
"""

import json
import os
import urllib.request

QUERY = """{ user(login: "pragyaangaur") { contributionsCollection { contributionCalendar {
  totalContributions weeks { contributionDays { date contributionCount contributionLevel } } } } } }"""
LEVEL = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}

req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query": QUERY}).encode(),
                             headers={"Authorization": "bearer " + os.environ["GITHUB_TOKEN"], "User-Agent": "contrib-chart"})
cal = json.load(urllib.request.urlopen(req))["data"]["user"]["contributionsCollection"]["contributionCalendar"]
days = [[d["date"], d["contributionCount"], LEVEL[d["contributionLevel"]]] for w in cal["weeks"] for d in w["contributionDays"]]
out = {"total": cal["totalContributions"], "days": days}
with open("assets/contrib.json", "w") as f:
    json.dump(out, f, separators=(",", ":"))
print(f"{out['total']} contributions over {len(days)} days")
