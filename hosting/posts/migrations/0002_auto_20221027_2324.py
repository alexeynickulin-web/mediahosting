# Generated by Django 3.2.5 on 2022-10-27 20:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='date_create',
        ),
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
    ]
