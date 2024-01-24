from django.urls import path

from . import views

app_name = 'images'

urlpatterns = [
    path("upload", views.upload_image, name="upload_image"),
    path("upload_success/<image_id>", views.upload_success, name="upload_image_success"),
    path("list", views.list_images, name="list_images"),
    path("convert", views.convert_image, name="convert_image"),
    path('updates', views.get_updates, name='get_updates'),
    path('delete/<int:image_id>', views.delete_image, name='delete_image'),
]
