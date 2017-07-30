from django.core.exceptions import ValidationError
from django.db.models import ForeignKey
from django.forms import IntegerField, HiddenInput

from demo.form_pseudo import Form


class ManagementForm(Form):
    TOTAL_FORMS = IntegerField(widget=HiddenInput)
    INITIAL_FORM = IntegerField(widget=HiddenInput)
    MIN_NUM_FORM = IntegerField(required=False, widget=HiddenInput)
    MAX_NUM_FORM = IntegerField(required=False, widget=HiddenInput)


class FormSet:
    form = None     # form class
    data = {}       # bind할 데이터 (request.POST)
    errors = []     # forms들의 valiate동작시 발생한 모든 에러
    can_order = False   # forms들의 순서를 저장할 수 있게
    can_delete = False  # forms들을 삭제할 수 있게
    prefix = 'form'     # 각 form의 name부분에 사용할 prefix

    def __init__(self, data=None):
        self.is_bound = data is not None

    @property
    def management_form(self):
        return ManagementForm(self.data)

    @property
    def forms(self):
        return [self.construct_form(i) for i in range(self.management_form.TOTAL_FORMS)]

    def construct_form(self, i, **kwargs):
        return self.form(data=self.data, prefix=self.prefix + '-' + i, **kwargs)

    @property
    def cleaned_data(self):
        return [form.cleaned_data for form in self.forms]

    def is_valid(self):
        self.clean()
        forms_valid = True
        for form in self.forms:
            forms_valid &= form.is_valid()
        return self.is_bound and forms_valid

    def clean(self):
        for form in self.forms:
            try:
                form.clean()
            except ValidationError as error:
                self.errors.append(error)


class ModelFormset(FormSet):
    queryset = None  # model formset의 경우

    def construct_form(self, i, **kwargs):
        instance = self.queryset()[i]
        return super().construct_form(instance=instance, **kwargs)

    def save(self):
        for form in self.forms:
            if form.is_deleted:
                form.instance.delete()
            else:
                form.save()


class InlineFormSet(ModelFormset):
    def __init__(self, parent_model, model, instance=None, **kwargs):
        # 실제로는 inlineformset_factory에서 실행됨
        self.fk = self.get_foreign_key(parent_model, model)
        self.instance = instance
        super().__init__(**kwargs)

    @staticmethod  # 실제는 Global function
    def get_foreign_key(parent_model, model):
        fks_to_parent = [
            field for field in model._meta.fields
            if isinstance(field, ForeignKey) and field.remote_field.model == parent_model
            ]
        return fks_to_parent[0]

    def construct_form(self, i, **kwargs):
        form = super().construct_form(i, **kwargs)
        # 각 form의 인스턴스에 FK값 저장
        setattr(form.instance, self.fk.get_attname(), self.instance.pk)
        return form

    def save(self):
        for form in self.forms:
            if form.is_deleted:
                form.instance.delete()
            elif form.pk:  # update
                form.save()
            else:  # new
                setattr(form.instance, self.fk.name, self.instance)
                form.save()
