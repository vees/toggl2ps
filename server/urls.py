from django.conf.urls import include, url
from django.urls import path, re_path
import toggl2ps.views

urlpatterns = [ 
    re_path(r'(?P<apikey>[0-9a-f]+)/(?P<weekending>[0-9\-]+)/', toggl2ps.views.index),
]
