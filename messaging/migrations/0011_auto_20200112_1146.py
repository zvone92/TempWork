# Generated by Django 2.2.6 on 2020-01-12 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0010_auto_20200106_1944'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='conversation',
        ),
        migrations.AddField(
            model_name='conversation',
            name='mesagges',
            field=models.ManyToManyField(to='messaging.Message'),
        ),
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(choices=[('read', 'Read'), ('archived', 'Archived'), ('unread', 'Unread')], default='unread', max_length=10),
        ),
    ]
