#!/usr/bin/env python3

def template_replace(r, subs):
    for sub in subs.keys():
        r = r.replace(f"$${sub}$$", str(subs[sub]))
    return r

from sys import argv, exit, modules
import json, os, datetime, yaml

OUTPUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config.yml"))
with open(OUTPUT, "r") as f:
    OUTPUT = yaml.safe_load(f.read())
OUTPUT = OUTPUT["calendar-output-path"]

past = ""
upcoming = ""

templates = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "util", "template"))

fevent = open(templates+"/event.html", "r")
fevents = open(templates+"/events.html", "r")

revent = fevent.read()
revents = fevents.read()

past_count = 0

with open(argv[1], "r") as f:
    events = json.loads(f.read())
    for e in sorted([e for e in events.values()], key=lambda x: int(x["datetime"])):
        dtime = datetime.datetime.fromtimestamp(int(e["datetime"]))
        e["datetime"] = dtime
        e["description"] = e["description"].replace("\n", "<br>")
        e["wiki"] = f"<emp><a href='/wiki/VTLUUG:{dtime.date().isoformat()}' target='_blank'>(wiki)</a></emp>" if not e["upcoming"] else ""
        if e["upcoming"]: upcoming += template_replace(revent, e)
        else:
            past += template_replace(revent, e)
            past_count += 1

with open(OUTPUT, "w") as f:
    f.write(template_replace(revents, {
        "past": past,
        "pastcount": past_count,
        "upcoming": upcoming
    }))

fevent.close()
fevents.close()