# Generated by Django 2.2.6 on 2020-03-18 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0023_auto_20200318_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(choices=[('read', 'Read'), ('archived', 'Archived'), ('unread', 'Unread')], default='unread', max_length=10),
        ),
    ]
