# Generated by Django 2.2.6 on 2020-03-22 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('temp', '0022_auto_20200318_2036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worker',
            name='medals',
        ),
    ]
