"""
Compute remaining time in the workday based on clock time and project rounding time
"""
from math import ceil
import json
import time
import dateutil.parser
import datetime
from dateutil import tz
from configparser import SafeConfigParser
import sys
import base64
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
from functools import reduce



def convert_json(weekending, apikey):
	#try:
	return convert_json_internal(weekending, apikey)
	#except Exception as e:
	#	raise e
	#	return json.dumps({'jobs' : [], 'entries' : [], 'errors' : ['Invalid inputs or parse failed']}, sort_keys=True, indent=4)

def convert_json_internal(today, apikey):
	try:
		today = dateutil.parser.parse(str(today)).date()
	except ValueError:
		today = datetime.date.today()

	zone = '-05:00'
	start_date = datetime.datetime.combine(today,datetime.datetime.min.time()).isoformat() +zone
	end_date = datetime.datetime.combine(today,datetime.datetime.max.time()).isoformat() +zone

	get_params = {
		'start_date' : start_date,
		'end_date'   : end_date,
		#'with_related_data' : 'true'
	}

	print(get_params)

	params = urllib.parse.urlencode(get_params)
	r = urllib.request.Request("https://www.toggl.com/api/v8/time_entries?%s" % params)
	authbytes = ('%s:%s' % (apikey, 'api_token')).encode()
	base64string = base64.encodestring(authbytes).decode().replace('\n', '')
	r.add_header("Authorization", "Basic %s" % base64string)

	#params = urllib.urlencode(post_params)
	f = urllib.request.urlopen(r)
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
	params = urllib.parse.urlencode(get_params)
	r = urllib.request.Request("https://www.toggl.com/api/v8/me?%s" % params)
	authbytes = ('%s:%s' % (apikey, 'api_token')).encode()
	base64string = base64.encodestring(authbytes).decode().replace('\n', '')
	r.add_header("Authorization", "Basic %s" % base64string)

	#params = urllib.urlencode(post_params)
	f = urllib.request.urlopen(r)
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
			#print(entry)
			project,minutes = ("00000"+str(projecthash[entry["pid"]][0:5]), entry["duration"])
			#print(project,minutes)
		except:
			#errorlist.append("Warning: no project associated with {0} ({1})".format(entry["description"], entry["start"]))
			print(errorlist)
			pass
		try:
			if minutes<0: minutes=0
		except NameError:
			minutes=0
		if project not in entrylist:
			entrylist[project] = 0
		entrylist[project] = entrylist[project] + minutes

	#print(entrylist) 
	
	roundedlist = {}
	for y in list(entrylist.keys()):
		roundedlist[y] = (ceil((entrylist[y]/3600.0)*4)/4) if (y in entrylist) else '0'


	print (roundedlist)

	clocktime = sum(entrylist.values())/3600
	sheettime = sum(roundedlist.values())

	return json.dumps({'clocktime' : clocktime, 'sheettime' : sheettime, 'ctr': 8.0-clocktime, 'str': 8.0-sheettime }, sort_keys=True, indent=4)
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
			raise
			print("Failed")
			exit()

	print(convert_json(weekending,apikey))
