# Generated by Django 3.0.14 on 2022-04-27 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HireApp', '0006_auto_20220425_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='onboard',
            field=models.ManyToManyField(related_name='onboard', to='HireApp.UserProfile'),
        ),
    ]
