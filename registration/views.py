from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from .forms import SignUpForm, RegisterParishForm

from .models import Parish


def signup(request):
    return render(request, 'signup.html')


def signup_parishioner(request):
    form = SignUpForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['email']).exists():
                messages.error(request, 'Username already exists')
                return redirect('registration:signup')

            user = User(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            user.set_password(form.cleaned_data['password1'])
            user.save()

            try:
                user.parishioner.parish = form.cleaned_data['parish']
                user.parishioner.street_address = form.cleaned_data['street_address']
                user.parishioner.city = form.cleaned_data['city']
                user.parishioner.state = form.cleaned_data['state']
                user.parishioner.zipcode = form.cleaned_data['zipcode']
                user.groups.add(Group.objects.get(name='Parishioner'))
                user.save()
            except:
                # TODO : Find possible exceptions that can be thrown and add handling
                user.delete()
                messages.error(request, f'Unable to Create Account')
                return redirect('registration:signup')
            else:
                login(request, user)
                return redirect('dashboard:home')

    return render(request, 'signup_parishioner.html', {'form': form})


def signup_parish(request):
    form = RegisterParishForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['email']).exists():
                messages.error(request, 'Username already exists')
                return redirect('registration:register_parish')

            user = User(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            user.set_password(form.cleaned_data['password1'])
            user.save()

            try:
                parish = Parish(
                    name=form.cleaned_data.get('parish_name'),
                    street_address=form.cleaned_data.get('parish_address'),
                    city=form.cleaned_data.get('parish_city'),
                    state=form.cleaned_data.get('parish_state'),
                    priest=form.cleaned_data.get('priest'),
                    attendee_limit=form.cleaned_data.get('attendee_limit'),
                    pre_register=form.cleaned_data.get('pre_register'),
                    close_register=form.cleaned_data.get('close_register'),
                    owner=user.parishioner
                )
                parish.save()
                user.groups.add(Group.objects.get(name='Parish Owner'))
                user.parishioner.parish = parish
                user.save()
            except:
                # TODO : Find possible exceptions that can be thrown and add handling
                user.delete()
                messages.error(request, f'Unable to Create Account')
                return redirect('registration:register_parish')
            else:
                login(request, user)
                return redirect('dashboard:home')

    return render(request, 'signup_parish.html', {'form': form})
