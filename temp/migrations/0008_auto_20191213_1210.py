# Generated by Django 2.2.6 on 2019-12-13 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temp', '0007_auto_20191213_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='status',
            field=models.CharField(choices=[('published', 'Published'), ('draft', 'Draft')], default='draft', max_length=10),
        ),
    ]