# Generated by Django 2.1.7 on 2019-08-02 06:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20190802_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='user_like',
            field=models.ManyToManyField(blank=True, related_name='like_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
