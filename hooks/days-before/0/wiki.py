#!/usr/bin/env python3
"""
makes a new wiki page for the meeting (w/ meeting info) the day of.

the base of this script was shamelessly stolen from bgregos -- https://github.com/bgregos/MeetingCreateBot
o7
"""
import datetime, sys, json, requests, yaml, os
from mwclient import Site

cfg = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "config.yml"))
with open(cfg, "r") as f:
    cfg = yaml.safe_load(f.read())

def update_for(event):
    site = Site("vtluug.org")
    site.login(cfg["mediawiki-username"], cfg["mediawiki-passwd"])

    dtime = datetime.datetime.fromtimestamp(int(event["datetime"]))

    # pull the json resp for Category:Meetings (once!) and nab the latest
    #  the old script literally iteratively checked every day backwards 
    #   from the current until it got a hit, lol
    r = requests.get("https://vtluug.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:VTLUUG:Meetings&cmlimit=max&format=json")
    meetings = r.json()
    prevmeeting = meetings["query"]["categorymembers"][-1]["title"]
    if dtime.date().isoformat() in prevmeeting:
        prevmeeting = prevmeeting = meetings["query"]["categorymembers"][-2]["title"]


    # make new meeting
    page = site.pages["VTLUUG:"+dtime.date().isoformat()]
    if page.exists:
        return
    text = """
[[$$prevmeeting$$|Previous Meeting]]

[https://github.com/vtluug/calendarium generated using calendarium]


== Time/Location ==

Meeting:
* Time: $$datetime$$
* Location: $$location$$
* Subject: $$subject$$
* Presenter: $$presenter$$

== Plan/Description ==

$$description$$

== Meeting Notes ==


[[category:VTLUUG:$$year$$]][[category:VTLUUG:Meetings]]"""
    text = text.replace("$$prevmeeting$$", prevmeeting)
    text = text.replace("$$datetime$$", str(dtime))
    text = text.replace("$$subject$$", event["subject"])
    text = text.replace("$$location$$", event["location"])
    text = text.replace("$$presenter$$", event["presenter"])
    text = text.replace("$$description$$", event["description"].replace("\n", "\n\n"))
    text = text.replace("$$year$$", str(dtime.year))
    page.edit(text, "calendarium was here")

    # update next meeting
    page = site.pages["Next_meeting"]
    text = "#REDIRECT [[VTLUUG:$$iso$$]]"
    text = text.replace("$$iso$$", dtime.date().isoformat())
    page.edit(text, "calendarium was here")

    # update mainpage/calendar
    page = site.pages["Calendar"]
    text = """
Check out our [https://vtluug.org/calendar.html calendar] for this semester, including planned talks.

Last Meeting: [[$$prevmeeting$$]]

Upcoming Meeting: [[Next_meeting]]"""
    text = text.replace("$$prevmeeting$$", prevmeeting)
    page.edit(text, "calendarium was here")


# how many days before we're looking for
N = int(os.path.dirname(__file__).split("/")[-1])

events = {}

with open(sys.argv[1], "r") as f:
    events = json.loads(f.read())
    for sig, e in events.items():
        if "wiki" in e["hooked"]: continue # if we've run once don't go again
        if "/past/" in sig: continue
        then = datetime.datetime.fromtimestamp(int(e["datetime"])).date()
        now = datetime.date.today()
        if now == (then - datetime.timedelta(days=N)):
            # e is within our desired timeframe
            update_for(e)
            events[sig]["hooked"].append("wiki")

# write changes to hooked
with open(sys.argv[1], "w") as f:
    f.write(json.dumps(events, indent=4))