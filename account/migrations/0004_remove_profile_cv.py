# Generated by Django 2.1.7 on 2019-07-31 03:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_profile_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='cv',
        ),
    ]
