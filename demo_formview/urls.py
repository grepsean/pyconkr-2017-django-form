from django.conf.urls import url

from demo_formview.views import ProgramFormViewList, ProgramFormViewCreate, ProgramFormViewUpdate, ProgramFormViewDelete

urlpatterns = [
    url('^$', ProgramFormViewList.as_view(), name='list'),
    url('^create/$', ProgramFormViewCreate.as_view(), name='create'),
    url('^(?P<pk>[0-9]+)/update/$', ProgramFormViewUpdate.as_view(), name='update'),
    url('^(?P<pk>[0-9]+)/delete/$', ProgramFormViewDelete.as_view(), name='delete'),
]
