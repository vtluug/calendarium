#!/usr/bin/env python3
from sys import argv, exit, modules
import datetime, os, json, yaml, subprocess

try: calendar = argv[1]
except:
    print("the proper calling format is ./calendarium.py <calendar-path>.\n"
        +"see the repo's readme.txt for more details")
    exit(1)

if not os.path.isdir(calendar):
    print(f"{calendar} does not exist or is not a directory")
    exit(1)

now = datetime.datetime.now()

checked_years = [now.year]
if now.month == 12:
    checked_years.append(now.year+1)
if now.month == 1:
    checked_years.append(now.year-1)
checked_months = [now.month]
if now.month != 12:
    checked_months.append(now.month+1)
if now.month != 1:
    checked_months.append(now.month-1)

mapping = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
checked_months = [mapping[i-1] for i in checked_months]

past_manifest = []
upcoming_manifest = []

for y in checked_years:
    for m in checked_months:
        for state in ["past", "upcoming"]:
            path = f"{calendar}/{state}/{y}/{m}/"
            
            if not os.path.isdir(path): continue
            days = os.listdir(path)
            for d in days:
                for event in os.listdir(f"{path}/{d}"):
                    manifest = getattr(modules[__name__], state+"_manifest")
                    manifest.append(f"{path}/{d}/{event}")

manifest_path = f"{calendar}/manifest.json"

if not os.path.exists(manifest_path):
    with open(manifest_path, "w") as f:
        f.write("{}")

with open(manifest_path, "r") as f:
    manifest = json.loads(f.read())

for e in past_manifest + upcoming_manifest:
    if manifest.get(e) is not None: continue
    e = e.replace("//", "/").replace("//", "/").replace("//", "/") #f1x shit hack

    x, upcoming, year, month, day, name = e.split("/")
    
    with open(e, "r") as f:
        info = yaml.safe_load(f.read())

    hour = int(info["time"] / 100)
    minute = info["time"] % 100

    dtime = datetime.datetime(int(year), mapping.index(month)+1, int(day), hour, minute)

    entry = info
    entry["upcoming"] = upcoming == "upcoming"
    entry["datetime"] = int(dtime.timestamp())
    entry["hooked"] = []
    manifest[e] = entry

with open(manifest_path, "w") as f:
    f.write(json.dumps(manifest, indent=4))

hooks = os.path.dirname(os.path.abspath(__file__))+"/hooks"

for script in os.listdir(hooks+"/always"):
    subprocess.run([f"{hooks}/always/{script}", os.path.abspath(calendar+"/manifest.json")])
