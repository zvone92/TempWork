# Generated by Django 2.2.6 on 2019-10-31 08:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('temp', '0002_worker_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='status',
            field=models.CharField(choices=[('published', 'Published'), ('draft', 'Draft')], default='draft', max_length=10),
        ),
        migrations.AlterField(
            model_name='worker',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
