from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Parish
from django.utils.translation import ugettext_lazy as _


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=150, help_text=_("This will be your username as well"))
    parishes = Parish.objects.all()
    parish = forms.ModelChoiceField(queryset=parishes, help_text=_("Parish not on this list? Contact your administrator and ask them to join"))
    affirm_parish = forms.BooleanField(label="I affirm this is my parish")
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    state = forms.ChoiceField(choices=({('WA', 'Washington'), ('OR', 'Oregon')}))
    zipcode = forms.IntegerField()

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'parish',
            'affirm_parish',
            'street_address',
            'city',
            'state',
            'zipcode',
            'email',
            'password1',
            'password2',
        )


class RegisterParishForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, label="Your first name")
    last_name = forms.CharField(max_length=100, label="Your last name")
    email = forms.EmailField(max_length=150, label="Your email", help_text=_("This will be your username as well"))
    parish_name = forms.CharField(max_length=100)
    parish_address = forms.CharField(max_length=100)
    parish_city = forms.CharField(max_length=100)
    parish_state = forms.ChoiceField(choices=({('WA', 'Washington'), ('OR', 'Oregon')}))
    priest = forms.CharField(max_length=100, label="Pastor's name")
    attendee_limit = forms.IntegerField(required=False)
    pre_register = forms.IntegerField(min_value=0, max_value=30, initial=7, label="How many days ahead may parishioners register?")
    close_register = forms.IntegerField(min_value=0, max_value=30, initial=1, label="How many days ahead should registration end")

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'parish_name',
            'parish_address',
            'parish_city',
            'parish_state'
        )
