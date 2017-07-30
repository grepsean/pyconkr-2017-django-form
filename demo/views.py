from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView

from demo.forms import ProgramForm
from demo.models import Program


class ProgramList(ListView):
    model = Program
    template_name = 'program_list.html'


class ProgramCreate(TemplateView):
    form_class = ProgramForm
    template_name = 'program_form.html'
    success_url = reverse_lazy('program:list')
    object = None

    def get_context_data(self, **kwargs):
        if 'object' not in kwargs:
            kwargs['object'] = self.object
        if 'form' not in kwargs:
            kwargs['form'] = self.form_class(instance=self.object)
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ProgramUpdate(ProgramCreate):
    model = Program

    def get_object(self):
        pk = self.kwargs.get('pk')
        return self.model.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class ProgramDelete(ProgramUpdate):
    template_name = 'program_delete.html'

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return HttpResponseRedirect(self.success_url)
