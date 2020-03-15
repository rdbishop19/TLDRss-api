# Generated by Django 3.0.4 on 2020-03-13 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('feed_url', models.URLField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('link', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField()),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tldrss.Feed')),
            ],
        ),
    ]