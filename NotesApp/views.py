
from django.shortcuts import render,HttpResponse
from . models import *
# Create your views here.
def prepIndex(request):
    studymaterials=StudyMaterials.objects.filter(IsApproved=True)
    print(studymaterials)
    return render(request, 'prepup/index.html',{'data':studymaterials})


def interviewIndex(request):
    Interviews=InterviewPrep.objects.filter(IsApproved=True)
    print(Interviews)
    return render(request, 'prepup/interviewPrep.html',{'data':Interviews})


# NotesAdmin begin:
from django.http import FileResponse, Http404
from django.core.files.storage import FileSystemStorage

def PrepupAdmin(request):
    studymaterials=StudyMaterials.objects.all()
    print(studymaterials)
    return render(request,'prepup/Admin.html',{'data':studymaterials})
    
from django.http import FileResponse, Http404
from django.core.files.storage import FileSystemStorage

def OpenFIle(request,id):
    print(id)
    study=StudyMaterials.objects.get(id=id).file
    print(study)
    fs=FileSystemStorage()
    # filename,ext=str(study).split('.')
    # print(filename,ext)
    file="media/"+str(study)
    print(type(file))
    # return FileResponse(open(study, 'rb'), content_type='application/pdf')
    with open(file,'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        return response
    pdf.closed