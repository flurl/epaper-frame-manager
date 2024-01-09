import os
from django.db import models
from django.core.files import File
from django.conf import settings


# Create your models here.

# TODO: make this configurable
FRAME_IMAGE_WIDTH = 448
FRAME_IMAGE_HEIGHT = 600

class Image(models.Model):
    original_image = models.ImageField(upload_to='images/')
    converted_image = models.ImageField(upload_to='images/converted/', null=True, blank=True)
    offset_x = models.FloatField(default=0.0)
    offset_y = models.FloatField(default=0.0)
    width = models.FloatField(default=FRAME_IMAGE_WIDTH)
    height = models.FloatField(default=FRAME_IMAGE_HEIGHT)
    rotation = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    

    def convert(self, dimensions=None, offset=(0,0), rotation=0):
        if dimensions is None:
            dim = (FRAME_IMAGE_WIDTH, FRAME_IMAGE_HEIGHT)
        else:
            dim = dimensions
        REMAP_FILE = "/home/flurl/raid/development/projects/epaper_frame/django/epaper_converter/images/eink-7color.png"        

        orientation = 'portrait' if self.original_image.height > self.original_image.width else 'landscape'

        file_path = self.original_image.path
        path_components = os.path.splitext(file_path)
        tmp_file = path_components[0] + '.tmp.' + path_components[1]
        output_path = path_components[0] + '.bmp'

        # rotate it
        cmd = f"convert {file_path} -rotate {rotation} +repage '{tmp_file}'"
        os.system(cmd)
        
        # crop it to supplied dimensions
        if dimensions is not None:
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
        self.converted_image.save(os.path.basename(output_path), File(converted_img))
        self.offset_x, self.offset_y = offset
        self.width, self.height = dim
        self.rotation = rotation
        self.save()
        converted_img.close()

        cmd = f"rm '{tmp_file}' '{output_path}'"
        os.system(cmd)
