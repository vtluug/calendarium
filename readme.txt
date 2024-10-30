~calendarium~ is a filesystem-based calendar generator.

the main script,
$ calendarium.py <calendar-path>,
does the following:
- traverses the calendar/ filesystem, and generates a list of events to calendar/manifest.json
- calls each script in hooks/always with the manifest path as the first argument
- gets the current date, calculates the number of days before the next event N, then calls each
  script in hooks/days/before/once/N/ with the manifest path in the first argument, and updates the 
  - each called event gets added to the manifest event's hooked list (see below) and is ignored for
    subsequent matching runs

the intended deployment is a cronjob that periodically calls the script. for VTLUUG, the calendar path
  can be in /nfs/cistern/share/calendar, or somewhere else everyone can access.


the filesystem formats follow this pattern:

- calendar/
  - calendar/upcoming/year/month/day/event.yml
  - calendar/past/year/month/day/event.yml
  - where
    - year and day are numbers
    - month is a three-letter abbreviation
      - i.e. in {jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec}
    - <event>.yml can be one or multiple files that look like meeting.yml.sample
- hooks/
  - hooks/days-before-once/<# of days before the event the hook should trigger>/script.ext
    - e.g. placing a script twitter.py in hooks/days-before-once/0 runs twitter.py the day of the event
    - placing another script in [...]/days-before-once/2/[...] runs it two days before the event date 
  - current hooks
    - calendar.py generates the calendar.html to embed places
  - possible hooks
    - twitter/insta/etc integration for posting meeting reminders etc.

some sample events are included ;^)

the manifest.json follows this format:

calendar/upcoming|past/2024/oct/30/meeting.yml => {
    "upcoming": true/false, whether the event has happened already,
    "datetime": unix timestamp,
    "location": "e.g. McBryde 240",
    "subject": "e.g. Retro-encabulators",
    "presenter": "e.g. Renee Carte",
    "email": "e.g. rcarte@darkbloom.org",
    "description": "[...]",
    "hooked": [
        "days-before/2": true,
        "etc.": true
    ]
}


the meeting.yml files follow the format in meeting.yml.sample.