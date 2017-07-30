from django.conf.urls import url

from demo_generic.views import ProgramGenericList, ProgramGenericCreate, ProgramGenericUpdate, ProgramGenericDelete

urlpatterns = [
    url('^$', ProgramGenericList.as_view(), name='list'),
    url('^create/$', ProgramGenericCreate.as_view(), name='create'),
    url('^(?P<pk>[0-9]+)/update/$', ProgramGenericUpdate.as_view(), name='update'),
    url('^(?P<pk>[0-9]+)/delete/$', ProgramGenericDelete.as_view(), name='delete'),
]
