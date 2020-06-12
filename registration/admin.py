from django.contrib import admin
from .models import Parish, Parishioner, Mass, Attendee, AdditionalAttendee
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# Define an inline admin descriptor for Parishioner model
# which acts a bit like a singleton
class ParishionerInline(admin.StackedInline):
    model = Parishioner
    can_delete = False
    verbose_name_plural = 'parishioners'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (
        ParishionerInline,
    )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Models
admin.site.register(Parish)
admin.site.register(Parishioner)
admin.site.register(Mass)
admin.site.register(Attendee)
admin.site.register(AdditionalAttendee)
