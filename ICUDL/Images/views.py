from django.shortcuts import render
from .forms import ImageUploadForm


# Create your views here.
def home(request):
    return render(request, 'home.html')


def handle_image_file(f):
    with open('image.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def imageprocess(request):
    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
        handle_image_file(request.FILES['image'])
    return render(request, 'result.html')
