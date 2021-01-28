# Generated by Django 2.2.13 on 2021-01-18 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0028_auto_20210112_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(choices=[('read', 'Read'), ('archived', 'Archived'), ('unread', 'Unread')], default='unread', max_length=10),
        ),
    ]