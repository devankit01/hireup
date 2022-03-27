
from django.urls import path
from .views import *

urlpatterns = [
    path('', jobs, name='jobs'),
    path('jobs/<id>/', jobInfo, name='jobInfo'),

]
