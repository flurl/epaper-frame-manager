from io import BytesIO

from PIL import Image as Img
from PIL import ExifTags

from django import forms
from django.forms import ValidationError
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile

from .models import Image, FRAME_IMAGE_WIDTH, FRAME_IMAGE_HEIGHT

class ImageUpload(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['original_image']

    def clean_original_image(self):
        """ Clean the uploaded image attachemnt.
        """
        image = self.cleaned_data.get('original_image', False)
                
        if not image:
            return image

        assert isinstance(image, TemporaryUploadedFile) or isinstance(image, InMemoryUploadedFile), "Image rewrite instance error"

        # Read data from cStringIO instance
        image.file.seek(0)
        pil_image = Img.open(image.file)

        # if the image is oriented in EXIF meta data really rotate it
        try:
            exif = dict(pil_image._getexif().items())
            for exif_orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[exif_orientation] == 'Orientation':
                    break
            

            if exif[exif_orientation] == 3:
                pil_image = pil_image.rotate(180, expand=True)
            elif exif[exif_orientation] == 6:
                pil_image = pil_image.rotate(270, expand=True)
            elif exif[exif_orientation] == 8:
                pil_image = pil_image.rotate(90, expand=True)
        except AttributeError:
            """No exif data saved in image"""
            pass

        # Rewrite the image contents in the memory
        # (bails out with exception on bad data)
        pil_image.thumbnail((2048, 2048), Img.LANCZOS)

        # check image dimensions
        width, height = pil_image.size
        if height < FRAME_IMAGE_HEIGHT or width < FRAME_IMAGE_WIDTH:
            raise ValidationError("Wrong image dimensions.")

        if isinstance(image, TemporaryUploadedFile):
            # overwrite the temp file
            pil_image.save(image.file.name)
        elif isinstance(image, InMemoryUploadedFile):
            # replace file in memory
            f = BytesIO()
            pil_image.save(f, "JPEG")
            image.file = f


        return image
