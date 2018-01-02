# Create your views here.
from . import toggl2ps
from django.http import HttpResponse

def index(request, weekending, apikey):
	callback = request.GET.get('callback')
	json_output=toggl2ps.convert_json(weekending,apikey)
	if callback:
        	json_output = '%s(%s)' % (callback, json_output)
	return HttpResponse(json_output, content_type='application/json')

