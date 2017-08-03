from django.forms import ModelForm
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button

from demo.models import Program, Url


class ProgramForm(ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'desc', 'language']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'col-xs-12 col-sm-6 col-lg-4'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('전송')))
        if self.instance.pk:
            delete_url = reverse_lazy('program_formview:delete', kwargs={'pk': self.instance.pk})
            self.helper.add_input(Button('delete', _('삭제'), onclick='location.href="{}"'.format(delete_url)))


class UrlForm(ModelForm):
    class Meta:
        model = Url
        fields = '__all__'
