
from django.urls import path
from .views import *

urlpatterns = [
    path('', jobs, name='jobs'),
    path('jobs/<id>/', jobInfo, name='jobInfo'),

    path('create-job', createJob, name='createJob'),
    path('recruiter-jobs', recruiterJobs, name='recruiterJobs'),


]
