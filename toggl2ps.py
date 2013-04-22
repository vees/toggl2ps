import json
import dateutil.parser

with open("sample.txt") as togglapireply:
	weektimejson = togglapireply.read()
	weektime = json.loads(weektimejson)

entrylist = {}
for entry in weektime["data"]:
	startdate = dateutil.parser.parse(entry["start"])
	print startdate.date() ,entry["project"]["name"][0:5] ,entry["duration"]
	(dayofweek,project,minutes) = (startdate.date() ,entry["project"]["name"][0:5] ,entry["duration"])
	if dayofweek not in entrylist:
		entrylist[dayofweek] = {}
	if project not in entrylist[dayofweek]:
		entrylist[dayofweek][project] = 0
	entrylist[dayofweek][project] = entrylist[dayofweek][project] + minutes

print entrylist

#print weektime["data"][1]["start"],weektime["data"][1]["duration"],weektime["data"][1]["project"]["name"]

print "\t".join(sorted([str(k) for k in entrylist.keys()]))
jobslist = sorted(list(set(reduce(lambda x,y:x+y,[entrylist[x].keys() for x in sorted(entrylist.keys())]))))
for job in jobslist:
	print job + "\t" + "\t".join([str(entrylist[k][job]) if (job in entrylist[k]) else '0' for k in sorted(entrylist.keys())])

