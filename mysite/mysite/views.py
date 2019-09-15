from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage(base_url=settings.MEDIA_ROOT)
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'simple_upload.html', {
            'file': open(uploaded_file_url).read().split('\n')
        })
    return render(request, 'simple_upload.html')


def dashboard(request):
    return render(request, 'dashboard.html', {'dashboards': ['plots.png']})
