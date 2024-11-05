# calendarium is a filesystem-based calendar generator for VTLUUG

## i want to make a new meeting

* navigate to the calendar folder on acidburn, `/nfs/cistern/share/calendar`

* make a new folder for your date, if neccesary
  * e.g. `/nfs/cistern/share/calendar/2024/nov/6`
  * the year is always 4 digits, the month is one of {jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec}, the day has no preceding zeroes

* copy meeting.yml.sample from this repository into that folder as \<something>.yml. edit to taste

* run the script (on acidburn this happens automatically)
  * your change should propagate to the html event calendar in <= one minute, and a wiki page / listserv post should be made the day of

## i want to make a new constant-update hook
* add an executable to the `hooks/always` folder. make sure it's +x.
* the main script will call it using the absolute path to the manifest as the first argument
* process all the events therein as you like.

## i want to make a new trigger that goes off once, N days before the event
* follow the same instructions as for `always` hooks, but with `hooks/days-before/N`
* note that handling the 'triggers N days before' part is up to the script
* look at `wiki.py` and `listserv.py` for guidance

## how it works
* the main script, `calendarium.py`, gets called (manually, by a cronjob, w/e) with the path to the calendar folder as the first argument
* it parses the calendar folder into an event manifest, in `calendar/manifest.json`
* it calls all the hooks.
