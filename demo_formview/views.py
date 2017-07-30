from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView
from django.views.generic.edit import ModelFormMixin

from demo.forms import ProgramForm
from demo.models import Program


class ProgramFormViewList(ListView):
    model = Program
    template_name = 'program_list_formview.html'


class ProgramFormViewCreate(ModelFormMixin, FormView):
    form_class = ProgramForm
    object = None
    template_name = 'program_form_formview.html'
    success_url = reverse_lazy('program_formview:list')


class ProgramFormViewUpdate(ProgramFormViewCreate):
    model = Program

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class ProgramFormViewDelete(ProgramFormViewUpdate):
    model = Program
    template_name = 'program_delete.html'
    success_url = reverse_lazy('program_formview:list')

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return HttpResponseRedirect(self.success_url)
