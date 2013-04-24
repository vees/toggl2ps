from math import ceil
import json
import dateutil.parser
import datetime
from ConfigParser import SafeConfigParser
import sys
import base64
import urllib
import urllib2

def convert_json(weekending, apikey):
	weekending = dateutil.parser.parse(str(weekending))
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

	errorlist = []

	entrylist = {}
	for entry in weektime["data"]:
		startdate = dateutil.parser.parse(entry["start"])
		try:
			(dayofweek,project,minutes) = (str(startdate.date()), "00000"+str(entry["project"]["name"][0:5]), entry["duration"])
		except:
			errorlist.append("Warning: no project associated with {0} ({1})".format(entry["description"], entry["start"]))
			pass
		if minutes<0: minutes=0;
		if dayofweek not in entrylist:
			entrylist[dayofweek] = {}
		if project not in entrylist[dayofweek]:
			entrylist[dayofweek][project] = 0
		entrylist[dayofweek][project] = entrylist[dayofweek][project] + minutes

	for x in entrylist.keys():
		for y in entrylist[x].keys():
			entrylist[x][y] = str(ceil((entrylist[x][y]/3600.0)*4)/4) if (y in entrylist[x]) else '0'

	if len(entrylist.keys())>0:
		jobslist = sorted(list(set(reduce(lambda x,y:x+y,[entrylist[x].keys() for x in sorted(entrylist.keys())]))))
	else:
		jobslist = {}
		errorlist.append("Warning: No time entries found")

	return json.dumps({'jobs' : jobslist, 'entries' : entrylist, 'errors' : errorlist})
	#print json.dumps(entrylist)

if __name__ == "__main__":
	parser = SafeConfigParser()
	parser.read('simple.ini')

	try:
		weekending = dateutil.parser.parse(sys.argv[1])
	except:
		weekending = datetime.datetime.now()

	try:
		apikey = sys.argv[2]
	except:
		try:
			apikey = parser.get('toggl','apikey')
		except:
			exit()

	print convert_json(weekending,apikey)
