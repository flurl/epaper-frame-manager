# Generated by Django 5.0 on 2024-01-11 10:05

import firmware.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firmware', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='firmware',
            name='firmware_arch_version_unique',
        ),
        migrations.AddField(
            model_name='firmware',
            name='board',
            field=models.CharField(default='FIREBEETLE2', max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='firmware',
            name='file',
            field=models.FileField(storage=firmware.models.OverwriteStorage(), upload_to='firmwares/', validators=[firmware.models.validate_filename]),
        ),
        migrations.AddConstraint(
            model_name='firmware',
            constraint=models.UniqueConstraint(fields=('version', 'arch', 'board'), name='firmware_board_arch_version_unique'),
        ),
    ]
