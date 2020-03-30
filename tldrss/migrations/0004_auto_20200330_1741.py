# Generated by Django 3.0.4 on 2020-03-30 22:41

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tldrss', '0003_summaryupvote'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='summaryupvote',
            unique_together={('user', 'summary')},
        ),
    ]
