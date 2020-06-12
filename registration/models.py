from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Parish(models.Model):
    # A Parish can have multiple owners ?? Should we make a OneToOne?
    owner = models.ForeignKey("registration.Parishioner", verbose_name=_("Owner"), related_name="owner", on_delete=models.CASCADE, null=True)

    name = models.CharField(verbose_name=_("Parish Name"), max_length=256)
    street_address = models.CharField(verbose_name=_("Street Address"), max_length=256)
    city = models.CharField(verbose_name=_("City"), max_length=256)
    STATE_CHOICES = [
        ('WA', 'WA'),
        ('OR', 'OR'),
    ]
    state = models.CharField(verbose_name=_("State"), max_length=2, choices=STATE_CHOICES, default='WA')
    priest = models.CharField(verbose_name=_("Priest Name"), max_length=256, blank=True)
    attendee_limit = models.IntegerField(verbose_name=_("Attendee Limit"), default=10, blank=False)
    # DurationField ?
    pre_register = models.IntegerField(verbose_name=_("Number of days ahead parishioner's may register for mass"), default="6")
    close_register = models.IntegerField(verbose_name=_("Days ahead to close registration"), default="1")

    def __str__(self):
        return f"{self.name}, {self.city}, {self.state}"

    class Meta:
        verbose_name_plural = _("Parishes")


class Parishioner(models.Model):

    # Parishioner can have one user account
    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE, null=True)

    # A Parishioner can have one subscription
    subscription = models.OneToOneField("registration.Subscription", verbose_name=_("Subscription"), on_delete=models.CASCADE, blank=True, null=True)

    # A Parish can have multiple Parishioners
    parish = models.ForeignKey("registration.Parish", verbose_name=_("Parish"), on_delete=models.SET_DEFAULT, blank=True, null=True, default=None)

    street_address = models.CharField(verbose_name=_("Street Address"), max_length=256, blank=True, null=True)
    city = models.CharField(verbose_name=_("City"), max_length=256, blank=True, null=True)
    STATE_CHOICES = [
        ('WA', 'WA'),
        ('OR', 'OR'),
    ]
    state = models.CharField(verbose_name=_("State"), max_length=2, choices=STATE_CHOICES, default='WA', blank=True, null=True)
    zipcode = models.IntegerField(verbose_name=_("Zipcode"), blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Parishioner.objects.create(user=instance)
    else:
        instance.parishioner.save()


class Mass(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=256, default="Mass")
    start = models.DateTimeField(verbose_name=_("Start"), auto_now=False, auto_now_add=False)
    limit_override = models.IntegerField(verbose_name=_("Override Attendee Limit"), blank=True, null=True)

    # A Parish can have Multiple Mass Events
    parish = models.ForeignKey(Parish, verbose_name=_("Parish"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Mass')
        verbose_name_plural = _('Masses')

    def __str__(self):
        attendees = self.attendee_set.all()
        additional_attendee = self.adtl_attendees.all()
        seats_available = (self.parish.attendee_limit - len(attendees) - len(additional_attendee))

        # more for testing purposes but if there is mistake, this will prevent more people from signing up
        if seats_available < 0:
            seats_available = 0

        return f"{self.start.strftime('%B %d, %Y %-I %p')} - {self.name} - {self.parish.name} - {str(seats_available)} seats remaining"


class Attendee(models.Model):
    # A Mass can have multiple Attendee
    mass = models.ForeignKey("registration.Mass", verbose_name=_("Masses"), on_delete=models.CASCADE)

    # A Parishioner can have multiple Attendee
    parishioner = models.ForeignKey("registration.Parishioner", verbose_name=_("Parishioner"), on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.parishioner.user.first_name} {self.parishioner.user.last_name} {self.mass}"

class AdditionalAttendee(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=256)

    # A Parishioner can have multiple AdditionalAttendee
    parishioner = models.ForeignKey("registration.Parishioner", verbose_name=_("Parishioner"), on_delete=models.CASCADE)

    # A Mass can have multiple AdditionalAttendee
    mass = models.ForeignKey("registration.Mass", verbose_name=_("Masses"), on_delete=models.CASCADE, related_name="adtl_attendees")
