#!/usr/bin/env python3
import smtplib, os, yaml, sys, json, datetime
from email.message import EmailMessage

cfg = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "config.yml"))
with open(cfg, "r") as f:
    cfg = yaml.safe_load(f.read())

def acidburn_send(u, p, to, subject, text):
    print("sending mail")
    smtp = smtplib.SMTP("mail.vtluug.org", port="587")

    smtp.ehlo()
    smtp.starttls()

    smtp.login(u, p)  # login to our email server

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = u+"@vtluug.org"
    msg['To'] = to
    msg.set_content(text)

    smtp.send_message(msg)
                
    smtp.quit()

# how many days before we're looking for
N = int(os.path.dirname(__file__).split("/")[-1])

events = {}

with open(sys.argv[1], "r") as f:
    events = json.loads(f.read())
    for sig, e in events.items():
        if "listserv" in e["hooked"]: continue # if we've run once don't go again
        if "/past/" in sig: continue
        eventtime = datetime.datetime.fromtimestamp(int(e["datetime"]))
        then = eventtime.date()
        now = datetime.date.today()
        if now == (then - datetime.timedelta(days=N)):
            # e is within our desired timeframe
            body = f"""Time: {str(eventtime)}
Location: {e['location']}
Subject: {e['subject']}
Presenter: {e['presenter']}
Email: {e['email']}
Description: {e['description']}

generated by https://github.com/vtluug/calendarium"""
            acidburn_send(cfg["email-username"], cfg["email-passwd"], "vtluug-announce-g@vt.edu", "[EVENT] "+e["subject"]+", "+str(eventtime)+", "+e["location"], body)
            events[sig]["hooked"].append("listserv")

# write changes to hooked
with open(sys.argv[1], "w") as f:
    f.write(json.dumps(events, indent=4))
