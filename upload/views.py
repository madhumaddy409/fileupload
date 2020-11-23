from django.shortcuts import render,redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from upload.models import Document
from upload.forms import DocumentForm

from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse

def home(request):
    documents = Document.objects.all()
    return render(request, 'home.html', { 'documents': documents })


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'simple_upload.html')

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery')
    else:
        form = DocumentForm()
    return render(request, 'model_form_upload.html', {
        'form': form
    })

# @api_view(['GET','POST'])
# def gallery(request):
#     if request.method == 'POST':
#         data = list(Document.objects.values('document'))
#         print(data)
#         return JsonResponse(data, safe=False)
#     else:
#         data ="get method"
#         return JsonResponse(data, safe=False)

def gallery(request):
  images = list(Document.objects.values('document'))
  print(images)
  return render(request, "gallery.html", {'images': images})