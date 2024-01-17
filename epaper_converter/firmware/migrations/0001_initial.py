# Generated by Django 5.0 on 2024-01-10 14:19

import firmware.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Firmware',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='firmwares/', validators=[firmware.models.validate_filename])),
                ('version', models.IntegerField()),
                ('arch', models.CharField(max_length=32)),
                ('downloads', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddConstraint(
            model_name='firmware',
            constraint=models.UniqueConstraint(fields=('version', 'arch'), name='firmware_arch_version_unique'),
        ),
    ]