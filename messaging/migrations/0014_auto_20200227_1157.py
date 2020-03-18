# Generated by Django 2.2.6 on 2020-02-27 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0013_auto_20200215_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(choices=[('archived', 'Archived'), ('unread', 'Unread'), ('read', 'Read')], default='unread', max_length=10),
        ),
    ]