from django.urls import path

from . import views

app_name = 'firmware'

urlpatterns = [
    path("upload", views.upload_firmware, name="upload_firmware"),
    path("check", views.check_for_new_firmware, name="check_for_new_firmware"),
    path("download/<board>/<arch>/<int:version>/", views.download_firmware, name="download_firmware"),
    
]
