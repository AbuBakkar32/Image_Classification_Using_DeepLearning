from django.shortcuts import render
from .forms import ImageUploadForm

from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np


# Create your views here.
def home(request):
    return render(request, 'home.html')


def handle_image_file(f):
    with open('Image/image.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def imageprocess(request):
    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
        handle_image_file(request.FILES['image'])

        model = ResNet50(weights='imagenet')
        img_path = 'image.jpg'
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        preds = model.predict(x)
        # print('Predicted:', decode_predictions(preds, top=2)[0])
        html = decode_predictions(preds, top=2)[0]
        res = []
        for e in html:
            res.append((e[1], np.round(e[2] * 100, 2)))

        return render(request, 'result.html', context={'res': res})
    return render(request, 'home.html')
