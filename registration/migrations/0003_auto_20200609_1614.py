# Generated by Django 2.2.13 on 2020-06-09 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20200609_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parish',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owner', to='registration.Parishioner', verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='parishioner',
            name='parish',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.Parish', verbose_name='Parish'),
        ),
    ]
