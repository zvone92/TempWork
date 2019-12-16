# Generated by Django 2.2.6 on 2019-12-13 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temp', '0005_auto_20191126_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='image',
            field=models.ImageField(blank=True, default='media/images/default-avatar.png', null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10),
        ),
    ]
