# Generated by Django 3.0.14 on 2022-04-25 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HireApp', '0005_auto_20220425_1031'),
    ]

    operations = [
        migrations.RenameField(
            model_name='certification',
            old_name='month_name',
            new_name='issue_date',
        ),
        migrations.RemoveField(
            model_name='certification',
            name='year',
        ),
    ]
