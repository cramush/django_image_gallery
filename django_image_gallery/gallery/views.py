from urllib.request import urlopen
from django.shortcuts import render
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.http import HttpResponseRedirect
from .models import Images
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import os
import glob

BASE_DIR = os.path.dirname(os.path.abspath("media"))


def home(request):
    data = Images.objects.all()
    domain = request.build_absolute_uri()
    request.session["domain"] = domain
    if len(data) == 0:
        return render(request, "gallery/home_if_len_0.html")
    else:
        return render(request, "gallery/home.html", {"data": data})


@csrf_exempt
def add(request):
    if request.method == "POST" and request.POST.get("link") and request.FILES:
        return render(request, "gallery/add_error_1.html")

    if request.method == "POST" and not request.POST.get("link") and not request.FILES:
        return render(request, "gallery/add_error_2.html")

    else:
        if request.method == "POST" and request.FILES:
            file = request.FILES['myfile']
            url = file.name
            format_list = [".raw", ".jpeg", ".jpg", ".gif", ".png", ".tiff", ".bmp"]
            for f in format_list:
                if f in url.lower():
                    Images.objects.create(image=request.FILES["myfile"])
                    return HttpResponseRedirect(f"/image/{url}")

            else:
                return render(request, "gallery/add_error_3.html")


        elif request.method == "POST" and request.POST.get("link"):
            link = request.POST.get("link")
            url_list = link.split("/")[-1:]
            url = url_list[0]
            format_list = [".raw", ".jpeg", ".jpg", ".gif", ".png", ".tiff", ".bmp"]
            for f in format_list:
                if f in url.lower():
                    url = url.split(f, 1)[0]
                    url += f

                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(urlopen(link).read())
                    img_temp.flush()
                    picture = Images()
                    picture.image.save(f"{url}", File(img_temp))
                    picture.save()
                    return HttpResponseRedirect(f"/image/{url}")

            else:
                return render(request, "gallery/add_error_3.html")

    return render(request, "gallery/add_base.html")


@csrf_exempt
def image(request, url):
    if not os.path.exists(f"{BASE_DIR}/media/resized/"):
        os.makedirs(f"{BASE_DIR}/media/resized/", exist_ok=True)
    files = glob.glob(f"{BASE_DIR}/media/resized/*")
    for file in files:
        os.remove(file)
    domain = request.session["domain"]

    if request.method == "POST" and not request.POST.get('Width') and not request.POST.get('Height'):

        data = {
            "domain": domain,
            "url": url
        }
        return render(request, "gallery/image_error_1.html", {"data": data})

    if request.method == "POST":
        width = request.POST.get('Width')
        height = request.POST.get('Height')
        input_image_path = BASE_DIR + f"/media/images/{url}"
        output_image_path = BASE_DIR + f"/media/resized/{width}*{height}-{url}"

        original_image = Image.open(input_image_path)
        w, h = original_image.size
        max_size = ()
        if width and height:
            max_size = (int(width), int(height))
        elif width:
            max_size = (int(width), h)
        elif height:
            max_size = (w, int(height))

        original_image.thumbnail(max_size, Image.ANTIALIAS)
        original_image.save(output_image_path)

        data = {
            "domain": domain,
            "width": width,
            "height": height,
            "url": url
        }
        return render(request, "gallery/image_done.html", {"data": data})

    data = {
        "domain": domain,
        "url": url
    }
    return render(request, "gallery/image_base.html", {"data": data})


def clear(request):
    data = Images.objects.all()
    for picture in data:
        picture.delete()

    files = glob.glob(f"{BASE_DIR}/media/images/*")
    for file in files:
        os.remove(file)

    files = glob.glob(f"{BASE_DIR}/media/resized/*")
    for file in files:
        os.remove(file)

    return HttpResponseRedirect("/")
