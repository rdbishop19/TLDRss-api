# Generated by Django 3.0.4 on 2020-03-24 13:40

from django.db import migrations
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('tldrss', '0010_auto_20200323_2000'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': [django.db.models.expressions.OrderBy(django.db.models.expressions.F('pub_date'), descending=True, nulls_last=True), '-created_at']},
        ),
    ]