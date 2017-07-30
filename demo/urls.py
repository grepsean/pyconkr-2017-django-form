from django.conf.urls import url

from demo.views import ProgramList, ProgramCreate, ProgramUpdate, ProgramDelete

urlpatterns = [
    url('^$', ProgramList.as_view(), name='list'),
    url('^create/$', ProgramCreate.as_view(), name='create'),
    url('^(?P<pk>[0-9]+)/update/$', ProgramUpdate.as_view(), name='update'),
    url('^(?P<pk>[0-9]+)/delete/$', ProgramDelete.as_view(), name='delete'),
]
