
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render, HttpResponse
from . models import *
import logging
from django.db.models import Q
logger = logging.getLogger('watchtower-logger')
# Create your views here.


def checkSuperUser(request):
    if request.user:
        user = request.user
        userObj = User.objects.filter(username=user).first()
        print(userObj.is_superuser)
        if userObj.is_superuser:
            return True
        else:
            return False


def prepIndex(request):
    studymaterials = StudyMaterials.objects.filter(IsApproved=True)
    print(studymaterials)
    logger.info('Study Page Loaded')
    return render(request, 'prepup/index.html', {'data': studymaterials})


def interviewIndex(request):
    Interviews = InterviewPrep.objects.filter(IsApproved=True)
    # for inter in Interviews:
    #     inter.file = "https://shift-agreements.s3.ap-south-1.amazonaws.com/" + \
    #         str(inter.file)
    logger.info('Interview  Page Loaded')
    return render(request, 'prepup/interviewPrep.html', {'data': Interviews})


def interviewIndexAdmin(request):
    if checkSuperUser(request):
        Interviews = InterviewPrep.objects.all()
        print(Interviews)
        logger.info('Interview  Page Loaded')
        return render(request, 'prepup/InterviewAdmin.html', {'data': Interviews})
    else:
        return redirect('signin')

# NotesAdmin begin:


def PrepupAdmin(request):
    if checkSuperUser(request):

        studymaterials = StudyMaterials.objects.all()
        print(studymaterials)
        return render(request, 'prepup/Admin.html', {'data': studymaterials})
    else:
        return redirect('signin')


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


def prepUpdate(request, id, status):
    if checkSuperUser(request):

        if status == 'update':
            if StudyMaterials.objects.filter(id=id).first().IsApproved:
                StudyMaterials.objects.filter(id=id).update(IsApproved=False)
            else:
                StudyMaterials.objects.filter(id=id).update(IsApproved=True)
        if status == 'delete':
            StudyMaterials.objects.filter(id=id).delete()
        return redirect('PrepupAdmin')
    else:
        return redirect('signin')


def prepEdit(request, id=None):
    if checkSuperUser(request):

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
    else:
        return redirect('signin')


def interviewPrepUpdate(request, id, status):
    if checkSuperUser(request):

        if status == 'update':
            if InterviewPrep.objects.filter(id=id).first().IsApproved:
                InterviewPrep.objects.filter(id=id).update(IsApproved=False)
            else:
                InterviewPrep.objects.filter(id=id).update(IsApproved=True)
        if status == 'delete':
            InterviewPrep.objects.filter(id=id).delete()
        return redirect('interviewIndexAdmin')
    else:
        return redirect('signin')

def SearchPreup(request):
    
    q=request.GET['q']
    try:
        studymaterials=StudyMaterials.objects.filter(Q(Name__icontains=q,IsApproved=True) | Q(subject__icontains=q,IsApproved=True) | Q(years__icontains=q,IsApproved=True) | Q(Branch__icontains=q,IsApproved=True) ).order_by('-id')
    except:
        studymaterials=[]

    return render(request, 'prepup/index.html', {'data': studymaterials})

def SearchInterview(request):
    q=request.GET['q']
    try:
        studymaterials=InterviewPrep.objects.filter(name__icontains=q,IsApproved=True).order_by('-id')
    except:
        studymaterials=[]
    return render(request, 'prepup/interviewPrep.html', {'data': studymaterials})


def interviewPrepEdit(request, id=None):
    if checkSuperUser(request):

        if request.method == 'POST':
            if id != None and id != 'None':
                material = InterviewPrep(id=id)
                material.IsApproved = material.IsApproved
            else:
                material = InterviewPrep()

            material.name = request.POST['name']
            material.category = request.POST['category']

            material.tags = Tags.objects.filter(name=request.POST['tags'])
            material.url = request.POST['url']
            if request.FILES.get('file', None) == None:
                if id != None and id != 'None':
                    material.file = InterviewPrep.objects.filter(
                        id=id).first().file
            else:
                material.file = request.FILES['file']
            material.createdBy = request.user
            material.save()
    else:
        return redirect('signin')
