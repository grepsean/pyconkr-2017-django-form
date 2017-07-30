from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormView, ModelFormMixin

from demo.forms import ProgramForm, UrlForm
from demo.models import Program, Url


class ProgramFormSetViewList(ListView):
    model = Program
    template_name = 'program_list_formset.html'


class ProgramFormSetViewCreate(ModelFormMixin, FormView):
    form_class = ProgramForm
    formset_class = inlineformset_factory(parent_model=Program, model=Url, form=UrlForm,
                                          extra=1, can_order=True, can_delete=True)
    object = None
    template_name = 'program_form_formset.html'
    success_url = reverse_lazy('program_formset:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'formset' not in kwargs:
            context['formset'] = self.get_formset
        return context

    def get_formset(self, **kwargs):
        kwargs.update(instance=self.object)
        return self.formset_class(**kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = self.get_formset(data=self.request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_formset_valid(form, formset)
        else:
            return self.form_formset_invalid(form, formset)

    def form_formset_valid(self, form, formset):
        formset.instance = self.object = form.save()
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_formset_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ProgramFormSetViewUpdate(ProgramFormSetViewCreate):
    model = Program

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class ProgramFormSetViewDelete(ProgramFormSetViewUpdate):
    template_name = 'program_delete.html'

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return HttpResponseRedirect(self.success_url)
