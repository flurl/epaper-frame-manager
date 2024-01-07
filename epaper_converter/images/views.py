from datetime import datetime

from django.core.exceptions import BadRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import ImageUpload
from .models import Image

def list_images(request):
    images = Image.objects.all()
    return render(request, 'images/list_images.html', {'images': images})

def upload_image(request):
    if request.method == 'POST':
        form = ImageUpload(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            uploaded_image.convert()
            #return redirect("")
    else:
        form = ImageUpload()
    return render(request, 'images/upload_image.html', {'form': form})

def convert_image(request):
    if request.method == 'POST':
        src = request.POST['image'].removeprefix(settings.MEDIA_URL)
        print("img: ", src)
        img = get_object_or_404(Image, original_image=src)
        img.convert((request.POST['width'], request.POST['height']), 
                    (request.POST['offsetX'], request.POST['offsetY']), 
                    request.POST['rotate'])
        return JsonResponse({'status': 'OK'})
    return JsonResponse({'status': 'NOK'}, status=405)

def get_updates(request):
    since = 0
    try:
        since = request.POST['since']
    except KeyError:
        pass
    try:
        since = request.GET['since']
    except KeyError:
        pass

    try:
        since = int(since)
    except ValueError:
        since = 0

    # TODO: for testing purpose only
    since=0
    
    since_dt = datetime.utcfromtimestamp(since)

    updated_images = Image.objects.filter(updated_at__gt=since_dt)

    response = "%s\n" % int(datetime.now().timestamp())
    for img in updated_images:
        response += f"{'D' if img.deleted else 'U'} {request.build_absolute_uri(img.converted_image.url)}\n"

    return HttpResponse(response, content_type='text/plain')
