# Generated by Django 2.2.6 on 2020-02-27 11:28

from decimal import Decimal
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('temp', '0015_auto_20200215_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='cover',
            field=models.ImageField(blank=True, default='/images/default-avatar.png', null=True, upload_to='images'),
        ),
        migrations.AddField(
            model_name='worker',
            name='hourly_rate',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
        migrations.AddField(
            model_name='worker',
            name='lastname',
            field=models.CharField(default='No lastname', max_length=25),
        ),
        migrations.AddField(
            model_name='worker',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True),
        ),
        migrations.AlterField(
            model_name='worker',
            name='name',
            field=models.CharField(default='No name', max_length=25),
        ),
        migrations.AlterField(
            model_name='worker',
            name='status',
            field=models.CharField(choices=[('published', 'Published'), ('draft', 'Draft')], default='draft', max_length=10),
        ),
    ]
