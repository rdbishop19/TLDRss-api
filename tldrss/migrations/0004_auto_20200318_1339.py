# Generated by Django 3.0.4 on 2020-03-18 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tldrss', '0003_feedsubscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='pub_date',
            field=models.DateTimeField(null=True),
        ),
    ]