from django.conf.urls import url

from demo_formset.views import ProgramFormSetViewList, ProgramFormSetViewCreate, ProgramFormSetViewUpdate, ProgramFormSetViewDelete

urlpatterns = [
    url('^$', ProgramFormSetViewList.as_view(), name='list'),
    url('^create/$', ProgramFormSetViewCreate.as_view(), name='create'),
    url('^(?P<pk>[0-9]+)/update/$', ProgramFormSetViewUpdate.as_view(), name='update'),
    url('^(?P<pk>[0-9]+)/delete/$', ProgramFormSetViewDelete.as_view(), name='delete'),
]
