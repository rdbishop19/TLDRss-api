# Generated by Django 3.0.4 on 2020-03-19 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tldrss', '0005_auto_20200318_2104'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='summary',
            options={'ordering': ('-created_on',), 'verbose_name_plural': 'summaries'},
        ),
    ]
