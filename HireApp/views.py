from django.shortcuts import redirect, render
from .models import Work, CompanyProfile, RecruiterProfile, UserProfile

# Create your views here.

import logging
logger = logging.getLogger('watchtower-logger')


def jobs(request):
    jobs = Work.objects.filter(status=True).order_by('posted')
    logger.info('All Jobs')
    return render(request, 'hireup/jobs.html', {'jobs': jobs})


def jobInfo(request, id):
    logger.info('Jobs by ID')
    job = Work.objects.filter(id=id).first()
    job.tech_stack = eval(job.tech_stack)
    user = UserProfile.objects.filter(username=request.user).first()

    if user in job.applicants.all():
        applied = True
    else:
        applied = False

    return render(request, 'hireup/jobInfo.html', {'job': job, 'Isapplied': applied})


def applyjob(request, id):
    user = UserProfile.objects.filter(username=request.user).first()
    job = Work.objects.filter(id=id).first()
    if user in job.applicants.all():
        job.applicants.remove(user)
    else:
        job.applicants.add(user)

    return redirect('jobInfo', id)


def createJob(request):
    if request.method == 'POST':

        if len(request.POST.getlist('stack')) == 0:
            print("SELECT ATLEAST ONE!")

            return render(request, 'hireup/createjob.html', {'error': 'Please select atleast one technology.'})
        company = RecruiterProfile.objects.filter(
            username=request.user).first()
        print(company)
        job_details = {
            "Type": request.POST['jobType'],
            "emp_type": request.POST['empType'],
            "work_name": request.POST['jobName'],
            "company": company.company,
            "experience_or_time": request.POST['experience'],
            "location": request.POST['location'],
            "salary_or_stipend": request.POST['salary'],
            "tech_stack": request.POST.getlist('stack'),
            "number_of_vacancy": request.POST['opening'],
            "created_by": company
        }
        Work.objects.create(**job_details)
        logger.info('Created Job')
        return redirect('recruiterJobs')
    print('hiiiii')
    logger.info('Create Job by user {0}'.format(request.user))
    return render(request, 'hireup/createjob.html')


def editJob(request, id):
    if request.method == 'POST':
        if len(request.POST.getlist('stack')) == 0:
            print("SELECT ATLEAST ONE!")
            return render(request, 'hireup/editjob.html', {'error': 'Please select atleast one technology.'})
        job_details = {
            "Type": request.POST['jobType'],
            "emp_type": request.POST['empType'],
            "work_name": request.POST['jobName'],
            "experience_or_time": request.POST['experience'],
            "location": request.POST['location'],
            "salary_or_stipend": request.POST['salary'],
            "tech_stack": request.POST.getlist('stack'),
            "number_of_vacancy": request.POST['opening'],
        }
        if request.POST['jobStatus'] == "Inactive":
            job_details['status'] = False
        else:
            job_details['status'] = True
        Work.objects.filter(id=id).update(**job_details)
        return redirect('recruiterJobs')
    work = Work.objects.filter(id=id).first()
    logger.info('Edit Job {0}'.format(id))

    return render(request, 'hireup/editjob.html', {'data': work})


def recruiterJobs(request):
    recruiter = RecruiterProfile.objects.filter(username=request.user).first()
    works = Work.objects.filter(created_by=recruiter)
    return render(request, 'admin-ui/hireUp/Admin.html', {'data': works})


def addExp(request):
    return render(request, 'hireup/AddEditExp.html')


def addEdu(request):
    return render(request, 'hireup/AddEditEdu.html')
