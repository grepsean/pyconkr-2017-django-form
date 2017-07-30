from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from demo.models import Program


class ProgramGenericList(ListView):
    model = Program


class ProgramGenericManageMixin:
    model = Program
    fields = ['name', 'desc', 'language']
    success_url = reverse_lazy('program_generic:list')


class ProgramGenericCreate(ProgramGenericManageMixin, CreateView):
    pass


class ProgramGenericUpdate(ProgramGenericManageMixin, UpdateView):
    pass


class ProgramGenericDelete(ProgramGenericManageMixin, DeleteView):
    pass
