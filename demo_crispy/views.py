from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from demo.models import Program
from demo_formview.views import ProgramFormViewList, ProgramFormViewCreate


class ProgramCrispyList(ProgramFormViewList):
    template_name = 'program_list_crispy.html'


class ProgramCrispyCreate(ProgramFormViewCreate):
    template_name = 'program_form_crispy.html'
    success_url = reverse_lazy('program_crispy:list')


class ProgramCrispyUpdate(ProgramCrispyCreate):
    model = Program

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class ProgramCrispyDelete(ProgramCrispyUpdate):
    model = Program
    template_name = 'program_delete.html'
    success_url = reverse_lazy('program_crispy:list')

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return HttpResponseRedirect(self.success_url)