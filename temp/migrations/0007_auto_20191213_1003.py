# Generated by Django 2.2.6 on 2019-12-13 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temp', '0006_auto_20191213_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='image',
            field=models.ImageField(blank=True, default='/images/default-avatar.png', null=True, upload_to='images'),
        ),
    ]
