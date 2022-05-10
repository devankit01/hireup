from django.shortcuts import redirect, render, get_object_or_404
from .models import Work, CompanyProfile, RecruiterProfile, UserProfile, User
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, HttpResponse, Http404, get_object_or_404, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMultiAlternatives
from HireApp.models import RecruiterProfile, Skill, UserProfile
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import F, Q
from HireApp.models import CompanyProfile
from HireApp.models import Work, Education, Experience, Certification
from datetime import datetime
from django.http import FileResponse

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


def manageJob(request, id):
    work = Work.objects.filter(id=id).first()

    applicants = list(work.applicants.all())
    resume_selected = list(work.resume_selected.all())
    hired = list(work.hired.all())
    onboard = list(work.onboard.all())

    applicants = [item for item in applicants if item not in (
        resume_selected+hired+onboard)]
    resume_selected = [
        item for item in resume_selected if item not in (hired + onboard)]
    hired = [item for item in hired if item not in onboard]

    return render(request, 'admin-ui/hireUp/jobApplicants.html', {'work': work, 'applicants': applicants, 'resume_selected': resume_selected, 'hired': hired, 'onboard': onboard})


def selectInterview(request, userid, jobid, key):
    work = Work.objects.filter(id=jobid).first()
    profile = UserProfile.objects.filter(id=userid).first()

    if key == 'resume_selected':
        work.resume_selected.add(profile)
        mail_subject = 'Your resume is selected.'
        content=f"Your resume is selected, you are moving for interview round of {work.work_name}  {work.company.company_name}"
    elif key == 'interview':
        work.hired.add(profile)
        mail_subject = 'You are selected for the interview.'
        content=f"Hurrah! You are selected in the interview round of {work.work_name}  {work.company.company_name}."
    elif key == 'onboard':
        work.onboard.add(profile)
        mail_subject = 'Finally You are onboard.'
        content=f"Congratulations, You have successfully onboarded of {work.work_name}  {work.company.company_name}."

    message = render_to_string('email/confirmation_email.html', {
        'user': profile,
        'content':content
        
    })
    to_email = profile.username
    
    # send_mail(mail_subject, message, 'youremail', [to_email])
    msg = EmailMultiAlternatives(
        mail_subject, message, 'youremail', [to_email])
    msg.attach_alternative(message, "text/html")
    msg.send()
    print("mail has been send")
    return redirect(manageJob, jobid)

