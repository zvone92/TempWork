# Generated by Django 2.2.6 on 2020-01-26 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0011_auto_20200112_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(choices=[('read', 'Read'), ('unread', 'Unread'), ('archived', 'Archived')], default='unread', max_length=10),
        ),
    ]
