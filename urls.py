from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from quadmap.surveys.models import Survey, Area, Operator

# http://djangosnippets.org/snippets/499/
from django.core import urlresolvers

class lazy_string(object):
    def __init__(self, function, *args, **kwargs):
        self.function=function
        self.args=args
        self.kwargs=kwargs
        
    def __str__(self):
        if not hasattr(self, 'str'):
            self.str=self.function(*self.args, **self.kwargs)
        return self.str

def reverse(*args, **kwargs):
    return lazy_string(urlresolvers.reverse, *args, **kwargs)


# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'quadmap.views.home', name='home'),
    # url(r'^quadmap/', include('quadmap.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'quadmap.views.index', name="index"),

    url(r'^surveys/new/$', 'quadmap.surveys.views.survey_new', name='new_survey'),
    url(r'^surveys/edit/(\d+)/$', 'quadmap.surveys.views.survey_edit', name='edit_survey'),
    url(r'^surveys/delete/(?P<pk>\d+)/$', DeleteView.as_view(model=Survey, success_url=reverse('index')), name='delete_survey'),
    url(r'^surveys/compile/(\d+)/$', 'quadmap.surveys.views.survey_compile', name='compile_survey'),
    url(r'^surveys/report/(\d+)/$', 'quadmap.surveys.views.survey_report', name='report'),

    url(r'^areas/new/$', CreateView.as_view(model=Area), name='add_area'),
    url(r'^areas/edit/(?P<pk>\d+)/$', UpdateView.as_view(model=Area), name='edit_area'),
    url(r'^areas/delete/(?P<pk>\d+)/$', DeleteView.as_view(model=Area, success_url=reverse('index')), name='delete_area'),

    url(r'^operators/new/$', CreateView.as_view(model=Operator), name='add_operator'),
    url(r'^operators/edit/(?P<pk>\d+)/$', UpdateView.as_view(model=Operator), name='edit_operator'),
    url(r'^operators/delete/(?P<pk>\d+)/$', DeleteView.as_view(model=Operator, success_url=reverse('index')), name='delete_operator'),
)