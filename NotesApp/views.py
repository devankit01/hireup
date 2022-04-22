
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render, HttpResponse
from . models import *
import logging
logger = logging.getLogger('watchtower-logger')
# Create your views here.


def prepIndex(request):
    studymaterials = StudyMaterials.objects.filter(IsApproved=True)
    print(studymaterials)
    logger.info('Study Page Loaded')
    return render(request, 'prepup/index.html', {'data': studymaterials})


def interviewIndex(request):
    Interviews = InterviewPrep.objects.filter(IsApproved=True)
    print(Interviews)
    logger.info('Interview  Page Loaded')
    return render(request, 'prepup/interviewPrep.html', {'data': Interviews})


# NotesAdmin begin:


def PrepupAdmin(request):
    studymaterials = StudyMaterials.objects.all()
    print(studymaterials)
    return render(request, 'prepup/Admin.html', {'data': studymaterials})


def OpenFIle(request, id):
    print(id)
    study = StudyMaterials.objects.get(id=id).file
    print(study)
    fs = FileSystemStorage()
    # filename,ext=str(study).split('.')
    # print(filename,ext)
    file = "media/"+str(study)
    print(type(file))
    # return FileResponse(open(study, 'rb'), content_type='application/pdf')
    with open(file, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        return response
    pdf.closed


def prepUpdate(request, id, status):
    if status == 'update':
        if StudyMaterials.objects.filter(id=id).first().IsApproved:
            StudyMaterials.objects.filter(id=id).update(IsApproved=False)
        else:
            StudyMaterials.objects.filter(id=id).update(IsApproved=True)
    if status == 'delete':
        StudyMaterials.objects.filter(id=id).delete()
    return redirect('PrepupAdmin')


def prepEdit(request, id=None):
    if request.method == 'POST':
        if id != None and id != 'None':
            material = StudyMaterials(id=id)
            material.IsApproved = material.IsApproved
        else:
            material = StudyMaterials()

        material.Name = request.POST['name']
        material.subject = request.POST['subject']
        material.year = request.POST['year']
        material.Branch = request.POST['branch']
        material.url = request.POST['url']
        if request.FILES.get('file', None) == None:
            if id != None and id != 'None':
                material.file = StudyMaterials.objects.filter(
                    id=id).first().file
        else:
            material.file = request.FILES['file']
        material.createdBy = request.user
        material.save()
        return redirect('PrepupAdmin')
    data = {'id': None}
    if id != None and id != 'None':
        data = StudyMaterials.objects.filter(id=id).first()
        page = 'Edit'
        button = 'Update'
    else:
        page = 'Add'
        button = 'Save'
    return render(request, 'prepup/addEditPrep.html', {'data': data, 'page': page, 'button': button})
