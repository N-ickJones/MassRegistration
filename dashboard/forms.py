from aldryn_sso.admin import User
from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets
from registration.models import Mass, Attendee
from registration.models import Parishioner, Parish
from datetime import date


class MassForm(ModelForm):
    start = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime)

    class Meta:
        model = Mass
        fields = '__all__'
        exclude = ('parish',)


# custom class to change the way options are rendered in the dropdown box
class CustomMassSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):

        index = str(index) if subindex is None else "%s_%s" % (index, subindex)
        if attrs is None:
            attrs = {}
        option_attrs = self.build_attrs(self.attrs, attrs) if self.option_inherits_attrs else {}
        if selected:
            option_attrs.update(self.checked_attribute)
        if 'id' in option_attrs:
            option_attrs['id'] = self.id_for_label(option_attrs['id'], index)
        if value:
            mass = Mass.objects.get(id=value)
            option_attrs["start"] = mass.start
            option_attrs["pre_register"] = mass.parish.pre_register
            option_attrs["close_register"] = mass.parish.close_register
            limit = mass.parish.attendee_limit - len(mass.attendee_set.all()) - len(mass.adtl_attendees.all())
            option_attrs['limit'] = limit
        return {
            'name': name,
            'value': value,
            'label': label,
            'selected': selected,
            'index': index,
            'attrs': option_attrs,
            'type': self.input_type,
            'template_name': self.option_template_name,
            'wrap_label': True,
        }


class MassRegisterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        extra_fields = kwargs.pop('extra', 0)

        extra_deleted_fields = kwargs.pop('deleted_fields', '').split(",")

        super(MassRegisterForm, self).__init__(*args, **kwargs)
        self.fields['mass'].queryset = Mass.objects.filter(parish=user.parishioner.parish, start__gt=date.today()).order_by('start')
        self.fields['attendee_field_count'].initial = extra_fields
        self.fields['deleted_fields'].initial = extra_deleted_fields

        if len(extra_deleted_fields) > 1:
            extra_deleted_fields = [int(i) for i in extra_deleted_fields[1:]]
            is_there_deleted = True
        else:
            is_there_deleted = False

        for index in range(int(extra_fields)):
            if is_there_deleted:
                if index not in extra_deleted_fields:
                    # generate extra fields in the number specified via extra_fields
                    self.fields['attendee_field_{index}'.format(index=index)] = forms.CharField()
            else:
                self.fields['attendee_field_{index}'.format(index=index)] = forms.CharField()

    mass = forms.ModelChoiceField(queryset=None, widget=CustomMassSelect())
    attendee_field_count = forms.CharField(widget=forms.HiddenInput())
    deleted_fields = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Attendee
        fields = ('mass', 'additional', 'additional_names')

class MassAttendanceEditForm(ModelForm):
    class Meta:
        model = Attendee
        fields = '__all__'


class ParishForm(ModelForm):
    class Meta:
        model = Parish
        fields = '__all__'
        exclude = ('owner',)


class ParishSelectForm(ModelForm):
    class Meta:
        model = Parishioner
        fields = ('parish',)


# TODO: add subscription details to form... for now its only confirming migration
class ParishSubscribeForm(forms.Form):
    confirm = forms.BooleanField()


class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email'
        )


class ParishionerProfileForm(ModelForm):
    class Meta:
        model = Parishioner
        fields = (
            'parish',
            'street_address',
            'city',
            'state',
            'zipcode'
        )

class UserProfileDeleteForm(forms.Form):
    email = forms.EmailField(required=True, label="Email address")
    password = forms.CharField(required=True, widget=forms.PasswordInput())
