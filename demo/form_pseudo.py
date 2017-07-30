from django.core.exceptions import ValidationError
from django import forms
from django.core.validators import RegexValidator
from django.forms import TextInput


class Field:
    widget = TextInput  # 각 필드를 렌더링할 위젯
    validators = []     # 각 필드를 검증할 validator들

    def __init__(self, validators):
        self.validators = validators

    def clean(self, value):
        self.run_validators(value)
        return value

    def run_validators(self, value):
        errors = []
        for validator in self.validators:
            try:
                validator(value)
            except ValidationError as error:
                errors.append(error)
        if errors:
            raise ValidationError(errors)


class Form:
    fields = []     # form에 선언한 field들
    data = {}       # bind할 데이터 (request.POST)
    initial = {}    # 초기값 데이터
    cleaned_data = {}  # validate를 통과한 데이터
    errors = []     # fields들의 valiate동작시 발생한 모든 에러

    def __init__(self, data=None):
        self.is_bound = data is not None

    def clean(self):
        for name, field in self.fields:
            try:
                value = field.clean()
            except ValidationError as error:
                self.errors.append(error)
            else:
                self.cleaned_data[name] = value

    def is_valid(self):
        self.clean()
        return self.is_bound and not self.errors


class ModelForm(Form):
    def __init__(self, instance=None, **kwargs):
        self.instance = instance
        super().__init__(**kwargs)

    def clean(self):
        super().clean()
        self.instance = self.construct_instance(self, self.instance)

    @staticmethod  # 실제는 Global function
    def construct_instance(form, instance):
        for field in form.fields:
            setattr(instance, field.name, form.cleaned_data[field.name])
        return instance

    def save(self):
        self.instance.save()


class MyForm(forms.Form):
    regex = RegexValidator(regex=r'^(\d{0,12})$', message=_('정확한 값을 입력해주세요.'))
    error_messages = {
        'field1_incorrect': _('field1이 올바르지 않습니다.'),
    }

    field1 = forms.IntegerField(min_value=0, max_value=100000, required=True)
    field2 = forms.CharField(max_length=10, validators=[regex], required=False)
    field3 = forms.BooleanField(widget=forms.CheckboxInput, required=True)

    def clean_field1(self):
        cleaned_field1 = self.cleaned_data['field1']
        if not self.additional_validate(cleaned_field1):
            raise forms.ValidationError(
                self.error_messages['field1_incorrect'],
                code='field1_incorrect',
            )
        return cleaned_field1
