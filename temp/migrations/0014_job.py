# Generated by Django 2.2.6 on 2020-01-26 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temp', '0013_auto_20200116_2001'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_type', models.CharField(max_length=200)),
                ('charging', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
