# Generated by Django 2.2.13 on 2020-06-10 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_merge_20200609_2241'),
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('type1', 'Type1'), ('type1', 'Type1'), ('type1', 'Type1'), ('type1', 'Type1')], default=None, max_length=32, null=True)),
                ('starts', models.DateTimeField()),
                ('ends', models.DateTimeField()),
                ('notes', models.CharField(default=None, max_length=128)),
                ('balance', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='parishioner',
            name='parish',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='registration.Parish', verbose_name='Parish'),
        ),
        migrations.AddField(
            model_name='parishioner',
            name='subscription',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='registration.Subscription', verbose_name='Subscription'),
        ),
    ]
