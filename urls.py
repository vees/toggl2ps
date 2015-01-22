from django.conf.urls import include, patterns, url

urlpatterns = patterns('',
    (r'(?P<apikey>[0-9a-f]+)/(?P<weekending>[0-9\-]+)/', 'toggl2ps.views.index'),
)
