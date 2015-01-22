from django.conf.urls import include, patterns, url

urlpatterns = patterns('veesnet.toggl',
    (r'(?P<apikey>[0-9a-f]+)/(?P<weekending>[0-9\-]+)/', 'views.index'),
)
