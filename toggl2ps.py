from math import ceil
import json
import dateutil.parser
import datetime
from ConfigParser import SafeConfigParser
import sys
import base64
import urllib
import urllib2

parser = SafeConfigParser()
parser.read('simple.ini')

try:
	weekending = dateutil.parser.parse(sys.argv[1])
except:
	weekending = datetime.datetime.now()

try:
	apikey = sys.argv[2]
except:
	apikey = parser.get('toggl','apikey')

end_date = (weekending+datetime.timedelta(days=1)-datetime.timedelta(seconds=1)).isoformat() + "-04:00"
start_date = (weekending-datetime.timedelta(days=6)).isoformat() + "-04:00"

get_params = {
	'start_date' : start_date,
	'end_date'   : end_date
}

params = urllib.urlencode(get_params)
r = urllib2.Request("https://www.toggl.com/api/v6/time_entries.json?%s" % params)
base64string = base64.encodestring('%s:%s' % (apikey, 'api_token')).replace('\n', '')
r.add_header("Authorization", "Basic %s" % base64string)   

#params = urllib.urlencode(post_params)
f = urllib2.urlopen(r)
#print f.read()
weektime = json.load(f)

# For debugging
#with open("sample.txt") as togglapireply:
#	weektimejson = togglapireply.read()
#	weektime = json.loads(weektimejson)

entrylist = {}
for entry in weektime["data"]:
	startdate = dateutil.parser.parse(entry["start"])
	try:
		(dayofweek,project,minutes) = (startdate.date(), entry["project"]["name"][0:5], entry["duration"])
	except:
		print "Warning, no project associated with {0} ({1})".format(entry["description"], entry["start"])
		pass
	if minutes<0: minutes=0;
	if dayofweek not in entrylist:
		entrylist[dayofweek] = {}
	if project not in entrylist[dayofweek]:
		entrylist[dayofweek][project] = 0
	entrylist[dayofweek][project] = entrylist[dayofweek][project] + minutes

print "\t" + "\t".join(sorted([str(k)[5:] for k in entrylist.keys()]))
jobslist = sorted(list(set(reduce(lambda x,y:x+y,[entrylist[x].keys() for x in sorted(entrylist.keys())]))))
for job in jobslist:
	print job + "\t" + "\t".join([str(ceil((entrylist[k][job]/3600.0)*4)/4) if (job in entrylist[k]) else '0' for k in sorted(entrylist.keys())])

