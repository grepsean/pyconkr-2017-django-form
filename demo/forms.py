from django.forms import ModelForm

from demo.models import Program, Url


class ProgramForm(ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'desc', 'language']


class UrlForm(ModelForm):
    class Meta:
        model = Url
        fields = '__all__'

