from io import BytesIO
import os
from PIL import Image as Img
from django.db import models
from django.core.files import File
from django.conf import settings
from django.apps import apps


# Create your models here.

# TODO: make this configurable
FRAME_IMAGE_WIDTH = 448
FRAME_IMAGE_HEIGHT = 600


# makemigrations failed when using lambdas for upload_to
# see https://stackoverflow.com/questions/27072222/django-1-7-1-makemigrations-fails-when-using-lambda-as-default-for-attribute
def upload_to(i, f):
    return f"user_{i.user.id}/images/{f}"


def upload_to_converted(i, f):
    return f"user_{i.user.id}/images/converted/{f}"


def upload_to_thumbs(i, f):
    return f"user_{i.user.id}/images/thumbs/{f}"


class Image(models.Model):
    original_image = models.ImageField(upload_to=upload_to)
    converted_image = models.ImageField(
        upload_to=upload_to_converted, null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to=upload_to_thumbs, null=True, blank=True)
    offset_x = models.FloatField(default=0.0)
    offset_y = models.FloatField(default=0.0)
    width = models.FloatField(default=FRAME_IMAGE_WIDTH)
    height = models.FloatField(default=FRAME_IMAGE_HEIGHT)
    rotation = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.PROTECT)

    def convert(self, dimensions=None, offset=(0, 0), rotation=0):
        orientation = 'portrait' if self.original_image.height > self.original_image.width else 'landscape'
        if dimensions is None:
            if orientation == 'portrait':
                w = FRAME_IMAGE_WIDTH * \
                    (self.original_image.width // FRAME_IMAGE_WIDTH)
                h = FRAME_IMAGE_HEIGHT * \
                    (self.original_image.width // FRAME_IMAGE_WIDTH)
            else:
                w = FRAME_IMAGE_WIDTH * \
                    (self.original_image.height // FRAME_IMAGE_HEIGHT)
                h = FRAME_IMAGE_HEIGHT * \
                    (self.original_image.height // FRAME_IMAGE_HEIGHT)
            dim = (w, h)
        else:
            dim = dimensions
        REMAP_FILE = os.path.join(apps.get_app_config(
            'images').path, "eink-7color.png")

        file_path = self.original_image.path
        path_components = os.path.splitext(file_path)
        tmp_file = path_components[0] + '.tmp.' + path_components[1]
        output_path = path_components[0] + '.bmp'

        # rotate it
        cmd = f"convert {file_path} -rotate {rotation} +repage '{tmp_file}'"
        os.system(cmd)

        # crop it
        size = f"{dim[0]}x{dim[1]}+{offset[0]}+{offset[1]}"
        cmd = f"convert {tmp_file} -crop {size} +repage '{tmp_file}'"
        os.system(cmd)

        # resize the image to either fit width or height depending on orientation
        size = f"{FRAME_IMAGE_WIDTH}x" if orientation == "portrait" else f"x{FRAME_IMAGE_HEIGHT}"
        cmd = f"convert '{tmp_file}' -resize {size} '{tmp_file}'"
        os.system(cmd)

        # then crop it to FRAME_IMAGE_WIDTHxFRAME_IMAGE_HEIGHT
        size = f"{FRAME_IMAGE_WIDTH}x{FRAME_IMAGE_HEIGHT}+0+0"
        cmd = f"convert {tmp_file} -crop {size} +repage '{tmp_file}'"
        os.system(cmd)

        # finally convert to bmp
        cmd = f"convert '{tmp_file}' -channel luminance -auto-level -modulate 120,200 -gravity center -resize 448x600^ -extent 448x600 -background white -dither FloydSteinberg -define dither:diffusion-amount=75% -remap {REMAP_FILE} -depth 4 -type Palette BMP3:{output_path}"
        os.system(cmd)

        # rotate it in correct position for e-paper display
        cmd = f"mogrify -rotate 270 +repage '{output_path}'"
        os.system(cmd)

        self.converted_image.delete()
        converted_img = open(output_path, 'rb')
        self.converted_image.save(os.path.basename(
            output_path), File(converted_img))
        self.offset_x, self.offset_y = offset
        self.width, self.height = dim
        self.rotation = rotation
        converted_img.close()

        cmd = f"rm '{tmp_file}' '{output_path}'"
        os.system(cmd)

        # create thumbnail
        left = offset[0]
        top = offset[1]
        right = left + dim[0]
        bottom = top + dim[1]

        self.thumbnail.delete()
        print("FILE: ", self.original_image.file)
        print("PATH: ", self.original_image.path)
        print("coords: ", (left, top, right, bottom))
        with self.original_image.open() as f:
            with Img.open(f) as pil_image:
                thumb = pil_image.crop((left, top, right, bottom))
                thumb_io = BytesIO()
                thumb.save(thumb_io, 'jpeg')
                self.thumbnail.save(os.path.basename(
                    self.original_image.name), File(thumb_io))

        self.save()
