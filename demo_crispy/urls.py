from django.conf.urls import url

from demo_crispy.views import ProgramCrispyList, ProgramCrispyCreate, ProgramCrispyUpdate, ProgramCrispyDelete

urlpatterns = [
    url('^$', ProgramCrispyList.as_view(), name='list'),
    url('^create/$', ProgramCrispyCreate.as_view(), name='create'),
    url('^(?P<pk>[0-9]+)/update/$', ProgramCrispyUpdate.as_view(), name='update'),
    url('^(?P<pk>[0-9]+)/delete/$', ProgramCrispyDelete.as_view(), name='delete'),
]
