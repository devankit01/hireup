from django.shortcuts import render

# Create your views here.
def jobs(request):
    return render(request, 'hireup/jobs.html')

def jobInfo(request, id):
    return render(request, 'hireup/jobInfo.html')

def createJob(request):
    return render(request, 'hireup/createjob.html')
