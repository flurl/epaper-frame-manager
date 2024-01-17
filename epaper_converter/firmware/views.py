from django.core.exceptions import BadRequest
from django.http import FileResponse, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.datastructures import MultiValueDictKeyError

from .forms import FirmwareUpload
from .models import Firmware, firmware_filename_pattern


@user_passes_test(lambda u: u.is_superuser)
def upload_firmware(request):
    if request.method == 'POST':
        form = FirmwareUpload(request.POST, request.FILES)
        if form.is_valid():
            uploaded_fw = form.save(commit=False)
            match = firmware_filename_pattern.match(uploaded_fw.file.name)
            uploaded_fw.board = match.group(1).upper()
            uploaded_fw.arch = match.group(2).upper()
            uploaded_fw.version = int(match.group(3))
            uploaded_fw.save()
            # return redirect("")
    else:
        form = FirmwareUpload()
    return render(request, 'firmware/upload_firmware.html', {'form': form})


def check_for_new_firmware(request):
    try:
        current_version = int(request.GET['current_version'])
        arch = request.GET['arch']
        board = request.GET['board']
    except MultiValueDictKeyError as ex:
        return HttpResponseBadRequest('"{}" was not provided.'.format(ex))

    new_fw = get_list_or_404(
        Firmware.objects.order_by('version'), board=board, arch=arch, version__gt=current_version)[0]

    return redirect('firmware:download_firmware', board=new_fw.board, arch=new_fw.arch, version=new_fw.version)


def download_firmware(request, board, arch, version):
    fw = get_object_or_404(Firmware, board=board, arch=arch, version=version)
    return FileResponse(fw.file.open())
