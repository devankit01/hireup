# Generated by Django 3.0.14 on 2022-03-20 09:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('HireApp', '0002_auto_20220319_0722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='college_branch',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='college_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='college_year',
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('start_year', models.CharField(max_length=100, null=True)),
                ('end_year', models.CharField(max_length=100, null=True)),
                ('degree', models.CharField(max_length=20, null=True)),
                ('username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]