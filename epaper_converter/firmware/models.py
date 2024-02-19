import re

from django.db import models
from django.core.exceptions import ValidationError

from overwrite_storage.storage import OverwriteStorage

# firmware filename format: firmware_BOARDNAME_ARCH_V.bin
firmware_filename_pattern = re.compile(r'firmware_(.*)_(.*)_(\d+)\.bin')


def validate_filename(file):
    if not firmware_filename_pattern.match(file.name):
        raise ValidationError("Filename not in valid format for firmware.")


class Firmware(models.Model):
    file = models.FileField(upload_to='firmwares/',
                            validators=[validate_filename], storage=OverwriteStorage())
    version = models.IntegerField()
    arch = models.CharField(max_length=32)
    board = models.CharField(max_length=32)
    downloads = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['version', 'arch', 'board'], name='firmware_board_arch_version_unique'),
            # models.CheckConstraint(check=models.Q(version__gt=models.Max('version')), name='firmware_arch_version_gt_check')
        ]

    def save(self, *args, **kwargs):
        # Find the highest version for the given architecture
        max_version = Firmware.objects.filter(arch=self.arch, board=self.board).order_by(
            '-version').first().version if Firmware.objects.filter(arch=self.arch, board=self.board).exists() else 0

        # If the version of the firmware being saved is lower than the maximum, raise a ValidationError
        if self.version <= max_version:
            raise ValidationError(
                "The version of the firmware being saved is not higher than the latest version.")

        super().save(*args, **kwargs)  # Call the "real" save() method.
