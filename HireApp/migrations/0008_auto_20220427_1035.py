# Generated by Django 3.0.14 on 2022-04-27 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HireApp', '0007_work_onboard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='posted',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]