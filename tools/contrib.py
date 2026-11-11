"""Fetch the GitHub contribution calendar into assets/contrib.json. Run: python3 tools/contrib.py

This reads the same calendar the profile page renders, at
https://github.com/users/pragyaangaur/contributions, rather than the GraphQL API.
The two disagree by a contribution or two: the page buckets each day in the
account's own timezone while the API buckets in UTC, so commits near midnight
land on different days. Reading the page keeps the board's total identical to
the one on the profile. It also needs no token, because the page already shows
private contributions.

The workflow in .github/workflows/contrib.yml runs this, so the chart on the
board stays current.
"""

import json
import re
import urllib.request

USER = "pragyaangaur"
URL = "https://github.com/users/%s/contributions" % USER
DAY = re.compile(r'<td[^>]*\bdata-date="(\d{4}-\d\d-\d\d)"[^>]*\bid="([^"]+)"[^>]*\bdata-level="(\d)"')
TIP = re.compile(r'<tool-tip[^>]*\bfor="([^"]+)"[^>]*>(.*?)</tool-tip>', re.S)
COUNT = re.compile(r"^\s*(\d+|No)\b")

req = urllib.request.Request(URL, headers={"User-Agent": "contrib-chart", "Accept": "text/html"})
page = urllib.request.urlopen(req).read().decode("utf-8")

tips = {m.group(1): m.group(2) for m in TIP.finditer(page)}
days = []
for cell in DAY.finditer(page):
    date, ident, level = cell.group(1), cell.group(2), cell.group(3)
    found = COUNT.match(tips.get(ident, ""))
    if not found:
        raise SystemExit("no contribution count for %s, the page markup has changed" % date)
    number = 0 if found.group(1) == "No" else int(found.group(1))
    days.append([date, number, int(level)])
days.sort()

if len(days) < 360 or len(days) > 380 or len({d[0] for d in days}) != len(days):
    raise SystemExit("got %d days, the page markup has changed" % len(days))

out = {"total": sum(d[1] for d in days), "days": days}
with open("assets/contrib.json", "w") as f:
    json.dump(out, f, separators=(",", ":"))
print("%d contributions over %d days" % (out["total"], len(days)))
