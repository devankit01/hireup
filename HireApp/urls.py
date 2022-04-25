
from django.urls import path
from .views import *

urlpatterns = [
    path('', jobs, name='jobs'),
    path('<id>/', jobInfo, name='jobInfo'),
    path('apply/<id>/', applyjob, name='applyjob'),

    path('create-job', createJob, name='createJob'),
    path('edit-job/<id>/', editJob, name='editJob'),
    path('recruiter-jobs', recruiterJobs, name='recruiterJobs'),
    path('manage-job/<id>', manageJob, name='manageJob'),

    # Experience
    path('add-exp', addExp, name ='addExp'),
    path('add-edu', addEdu, name ='addEdu'),
    path('add-certificate', addCert, name ='addCert'),




]
