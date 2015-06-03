from math import ceil
import json
import time
import dateutil.parser
import datetime
from dateutil import tz
from ConfigParser import SafeConfigParser
import sys
import base64
import urllib
import urllib2

def convert_json(weekending, apikey):
	#try:
	return convert_json_internal(weekending, apikey)
	#except Exception as e:
	#	raise e
	#	return json.dumps({'jobs' : [], 'entries' : [], 'errors' : ['Invalid inputs or parse failed']}, sort_keys=True, indent=4)

def convert_json_internal(weekending,apikey):
	weekending = dateutil.parser.parse(str(weekending))
	end_date = (weekending+datetime.timedelta(days=1)-datetime.timedelta(seconds=1)).isoformat() + "-04:00"
	start_date = (weekending-datetime.timedelta(days=6)).isoformat() + "-04:00"

	get_params = {
		'start_date' : start_date,
		'end_date'   : end_date,
		#'with_related_data' : 'true'
	}

	params = urllib.urlencode(get_params)
	r = urllib2.Request("https://www.toggl.com/api/v8/time_entries?%s" % params)
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

	# walk the entry list to get a list of the project names from that API
	get_params = {
		'with_related_data': 'true'
	}
	params = urllib.urlencode(get_params)
	r = urllib2.Request("https://www.toggl.com/api/v8/me?%s" % params)
	base64string = base64.encodestring('%s:%s' % (apikey, 'api_token')).replace('\n', '')
	r.add_header("Authorization", "Basic %s" % base64string)

	#params = urllib.urlencode(post_params)
	f = urllib2.urlopen(r)
	#print f.read()
	projectlist = json.load(f)

	#print projectlist["data"]["projects"]
	projecthash = {}
	for project in projectlist["data"]["projects"]:
		projecthash[project["id"]] = project["name"]

	#print projecthash

	errorlist = []

	entrylist = {}
	for entry in weektime:
		minutes=0
		if 'server_deleted_at' in entry:
			continue
		startdate = dateutil.parser.parse(entry["start"])
		startdate.replace(tzinfo=tz.gettz('UTC'))
		startdate = startdate.astimezone(tz.gettz('America/New York'))
		try:
			#print entry
			#print entry[u"duration"]
			print entry
			dayofweek,project,minutes = (str(startdate.date()), "00000"+str(projecthash[entry["pid"]][0:5]), entry[u"duration"])
			print dayofweek,project,minutes
		except:
			errorlist.append("Warning: no project associated with {0} ({1})".format(entry["description"], entry["start"]))
			print errorlist
			pass
		try:
			if minutes<0: minutes=0
		except NameError:
			minutes=0
		if dayofweek not in entrylist:
			entrylist[dayofweek] = {}
		if project not in entrylist[dayofweek]:
			entrylist[dayofweek][project] = 0
		entrylist[dayofweek][project] = entrylist[dayofweek][project] + minutes

	for x in entrylist.keys():
		for y in entrylist[x].keys():
			entrylist[x][y] = str(ceil((entrylist[x][y]/3600.0)*4)/4) if (y in entrylist[x]) else '0'

	listbyjob = {}
	for x in entrylist.keys():
		x2 = time.strptime(x,"%Y-%m-%d").tm_wday+6
		for y in entrylist[x].keys():
			if (y not in listbyjob):
				listbyjob[y] = {}
			listbyjob[y][x2] = entrylist[x][y]

	# If there are any projects with time in the entry list
	# this function simply creates a list of the job numbers
	if len(entrylist.keys())>0:
		jobslist = sorted(list(set(reduce(lambda x,y:x+y,[entrylist[x].keys() for x in sorted(entrylist.keys())]))))
	else:
		jobslist = {}
		errorlist.append("Warning: No time entries found")

	return json.dumps({'jobs' : jobslist, 'entries' : entrylist, 'errors' : errorlist, 'listbyjob': listbyjob }, sort_keys=True, indent=4)
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
			print "Failed"
			exit()

	print convert_json(weekending,apikey)
