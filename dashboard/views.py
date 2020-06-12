from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib import messages

from dashboard.forms import MassForm, MassRegisterForm, ParishSelectForm, UserProfileDeleteForm, ParishSubscribeForm
from registration.models import Mass, Attendee

from .forms import UserProfileForm, ParishionerProfileForm, ParishForm
from registration.models import Parish, AdditionalAttendee
from .validators import DateAcceptableValidator
from django.template.loader import render_to_string
from registration.utils import send_simple_message
from django.conf import settings


@login_required
def dashboard(request):
    mass = Mass.objects.filter(parish=request.user.parishioner.parish)
    attendance = Attendee.objects.filter(parishioner=request.user.parishioner)
    return render(request, 'dashboard.html', {'mass': mass, 'attendance': attendance})


@login_required
def view_profile(request):
    user_form = UserProfileForm(
        request.POST or None,
        prefix='user_form',
        instance=request.user
    )
    parishioner_form = ParishionerProfileForm(
        request.POST or None,
        prefix='parishioner_form',
        instance=request.user.parishioner
    )
    if user_form.is_valid() and parishioner_form.is_valid():
        user_form.save()
        parishioner_form.save()
        messages.success(request, "Your profile has been updated.")
        return redirect('dashboard:view_profile')
    return render(request, 'profile/view.html', {'user_form': user_form, 'parishioner_form': parishioner_form})


@login_required
def delete_profile(request):
    form = UserProfileDeleteForm(request.POST or None)
    if form.is_valid():
        if request.user.email == form.cleaned_data['email']:
            user = authenticate(request, username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                user.delete()
                messages.success(request, 'Your account with all its data has been deleted.')
                return redirect('home')
            else:
                messages.error(request, 'Unable to authenticate.')
        else:
            messages.error(request, 'Email mismatch.')
    return render(request, 'profile/delete.html', {'form': form})


@permission_required('registration.view_parish')
def view_parish(request):
    if request.user.parishioner.parish:
        data = Parish.objects.filter(pk=request.user.parishioner.parish.pk)
        return render(request, 'parish/view.html', {'data': data})
    elif request.user.has_perm('registration.add_parish'):
        return render(request, 'parish/view.html', {'data': None})
    else:
        return redirect('dashboard:select_parish')


@permission_required('registration.add_parish')
def add_parish(request):
    form = ParishForm(request.POST or None)
    if form.is_valid():
        obj = Parish()
        obj.name = form.cleaned_data.get('name')
        obj.street_address = form.cleaned_data.get('street_address')
        obj.city = form.cleaned_data.get('city')
        obj.state = form.cleaned_data.get('state')
        obj.priest = form.cleaned_data.get('priest')
        obj.attendee_limit = form.cleaned_data.get('attendee_limit')
        obj.pre_register = form.cleaned_data.get('pre_register')
        obj.close_register = form.cleaned_data.get('close_register')
        obj.owner = request.user.parishioner
        obj.save()
        request.user.parishioner.parish = obj
        request.user.parishioner.save()
        messages.success(request, "Parish has been added.")
        return redirect('dashboard:view_parish')
    else:
        return render(request, 'parish/add.html', {'form': form})

# TODO : Add Feature to transfer of ownership to another user
@permission_required('registration.change_parish')
def change_parish(request, parish_id):
    try:
        obj = Parish.objects.get(id=parish_id)
        form = ParishForm(request.POST or None, instance=obj)
        if form.is_valid():
            if request.user.parishioner.parish == obj:
                form.save()
                messages.success(request, "Parish has been updated.")
        else:
            return render(request, 'parish/change.html', {'form': form})
    except Parish.DoesNotExist:
        messages.error(request, "Parish does not exist")
    return redirect('dashboard:view_parish')


@permission_required('registration.delete_parish')
def delete_parish(request, parish_id):
    try:
        obj = Parish.objects.get(id=parish_id)
        if request.user.parishioner.parish == obj:
            obj.delete()
            request.user.groups.remove(Group.objects.get(name='Parish Owner'))
            request.user.groups.add(Group.objects.get(name='Parishioner'))
            messages.success(request, "Parish has been deleted.")
    except Parish.DoesNotExist:
        messages.error(request, "Parish does not exist")
    return redirect('dashboard:view_parish')


@login_required
def select_parish(request):
    form = ParishSelectForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            request.user.parishioner.parish = form.cleaned_data['parish']
            request.user.parishioner.save()
            messages.success(request, "Parish has been added.")
            return redirect('dashboard:view_parish')
        else:
            messages.error(request, "Unable to select parish.")
    return render(request, 'parish/select.html', {'form': form})


@login_required
def subscribe_parish(request):
    form = ParishSubscribeForm(request.POST or None)
    if form.is_valid():
        request.user.groups.remove(Group.objects.get(name='Parishioner'))
        request.user.groups.add(Group.objects.get(name='Parish Owner'))
        request.user.parishioner.parish = None
        request.user.parishioner.save()
        return redirect('dashboard:add_parish')
    else:
        return render(request, 'parish/subscribe.html', {'form': form})


# TODO : Mass and Attendee Updates to Additional Attendee need to be performed
@permission_required('registration.view_mass')
def view_mass(request):
    data = Mass.objects.filter(parish=request.user.parishioner.parish).order_by('start')
    return render(request, 'mass/view.html', {'data': data})


@permission_required('registration.add_mass')
def add_mass(request):
    form = MassForm(request.POST or None)
    if form.is_valid():
        obj = Mass()
        obj.name = form.cleaned_data['name']
        obj.start = form.cleaned_data['start']
        obj.limit_override = form.cleaned_data['limit_override']
        obj.parish = request.user.parishioner.parish
        obj.save()
        messages.success(request, "Mass event has been added.")
        return redirect('dashboard:view_mass')
    else:
        return render(request, 'mass/add.html', {'form': form})


@permission_required('registration.change_mass')
def change_mass(request, mass_id):
    try:
        obj = Mass.objects.get(id=mass_id)
        form = MassForm(request.POST or None, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Mass event has been updated.")
        else:
            return render(request, 'mass/change.html', {'form': form})
    except Mass.DoesNotExist:
        messages.error(request, "Mass does not exist.")
    return redirect('dashboard:view_mass')


@permission_required('registration.delete_mass')
def delete_mass(request, mass_id):
    try:
        obj = Mass.objects.get(id=mass_id)
        obj.delete()
        messages.success(request, "Mass event has been deleted.")
    except Mass.DoesNotExist:
        messages.error(request, "Mass does not exist.")
    return redirect('dashboard:view_mass')


@permission_required('registration.view_attendee')
def view_attendee(request):
    data = Attendee.objects.filter(parishioner=request.user.parishioner)
    return render(request, 'attendee/view.html', {'data': data})


@permission_required('registration.add_attendee')
def add_attendee(request):
    if request.method == 'POST':
        # gives you the numbers of cells that were deleted by the user to skip in the for loop
        extra_deleted_fields = request.POST.get('deleted_fields', '[,]')

        form = MassRegisterForm(request.POST, user=request.user,
                                extra=request.POST.get('attendee_field_count'),
                                deleted_fields=extra_deleted_fields)
        if form.is_valid():
            mass = form.cleaned_data['mass']
            d = DateAcceptableValidator()
            if not d(mass):
                return render(request, 'fail_date.html')

            # how many seats are available before submitted form is registered
            seats_available = (
                mass.parish.attendee_limit - len(mass.adtl_attendees.all()) - len(mass.attendee_set.all())
            )
            if seats_available < 0:
                seats_available = 0

            # make deleted additional attendee fields into an array
            extra_deleted_fields = extra_deleted_fields.split(",")
            # if greater than one (empty value has [,]), then convert all except [,] into int
            if len(extra_deleted_fields) > 1:
                extra_deleted_fields = [int(i) for i in extra_deleted_fields[1:]]
            else:
                extra_deleted_fields = []

            attendee_field_count = int(form.cleaned_data['attendee_field_count'])
            # how many additional attendees the user is trying to register
            additional_attendee_count_submitted = attendee_field_count - len(extra_deleted_fields)
            # plus 1 because it is including the submitter
            if seats_available < additional_attendee_count_submitted + 1:
                return render(request, 'fail.html', {'seats_available': seats_available})

            attendee = Attendee(
                mass=mass,
                parishioner=request.user.parishioner,
            )

            additional_attendee_list = []
            # loop through how many cells were created
            for index in range(attendee_field_count):
                # skip the ones that were deleted by user
                if index not in extra_deleted_fields:
                    name = str(form.cleaned_data['attendee_field_{index}'.format(index=index)])
                    if name:
                        additional_attendee = \
                            AdditionalAttendee(
                                name=name,
                                parishioner=request.user.parishioner,
                                mass=mass
                            )
                        additional_attendee.save()
                        additional_attendee_list.append(additional_attendee.name)
            attendee.save()

            add_attendee_list_str = ', '.join(additional_attendee_list)
            render_values = {
                "request_user_first_name": request.user.first_name,
                "request_user_last_name": request.user.last_name,
                "attendee_mass": attendee.mass,
                "attendee_parishioner_parish": attendee.parishioner.parish,
                "additional_attendees": add_attendee_list_str
            }
            html_message = render_to_string('confirmation_email_template.html', render_values)

            resp = send_simple_message(
                request.user.email,
                f'Register for Mass <{settings.DEFAULT_FROM_EMAIL}>',
                "Mass registration confirmation",
                html_message)

            if resp.ok:
                email_fail_message = ""
            else:
                email_fail_message = "Unfortunately, we were unable to send you a confirmation email at this time"

            context = {
                'attendee': attendee,
                'additional_attendees': "",
                'email_fail_message': email_fail_message
            }
            if len(additional_attendee_list):
                context["additional_attendees"] = "with " + add_attendee_list_str

            messages.success(request, "Attendance has been added.")
            # @TODO: Add message from success to flash message
            return render(request, 'attendee/success.html', context)

    else:
        form = MassRegisterForm(user=request.user)

    return render(request, 'attendee/add.html', {'form': form})


"""  # Archive for reference
@permission_required('registration.add_attendee')
def add_attendee(request):
    form = AttendeeForm(request.POST or None, user=request.user)
    if form.is_valid():
        obj = Attendee()
        obj.mass = form.cleaned_data['mass']
        obj.parishioner = request.user.parishioner
        obj.additional = form.cleaned_data['additional']
        obj.additional_names = form.cleaned_data['additional_names']
        obj.save()
        messages.success(request, "Attendance has been added.")
        return redirect('dashboard:view_attendee')
    else:
        return render(request, 'attendee/add.html', {'form': form})
"""


@permission_required('registration.change_attendee')
def change_attendee(request, attendee_id):
    try:
        obj = Attendee.objects.get(id=attendee_id)
        form = MassRegisterForm(request.POST or None, instance=obj, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Attendance has been changed")
        else:
            return render(request, 'attendee/change.html', {'form': form})
    except Attendee.DoesNotExist:
        messages.error(request, "Attendance does not exist.")
    return redirect('dashboard:view_attendee')


@permission_required('registration.delete_attendee')
def delete_attendee(request, attendee_id):
    try:
        obj = Attendee.objects.get(id=attendee_id)
        obj.delete()
        messages.success(request, "Attendance has been deleted.")
    except Attendee.DoesNotExist:
        messages.error(request, "Attendance does not exist.")
    return redirect('dashboard:view_attendee')


# TODO: View Phone Permission Gives Instructions to Owners and Possibly Delegates on Register by Phone Possibly
#  add Phone Field to User Model
@login_required
def view_phone(request):
    return render(request, 'phone/view.html')
