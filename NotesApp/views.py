from django.shortcuts import render
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