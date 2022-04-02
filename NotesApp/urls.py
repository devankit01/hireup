
from django.urls import path
from .views import *

urlpatterns = [
    path('', prepIndex, name='prepIndex'),
    path('interview-prep', interviewIndex, name='interviewIndex'),
    path('admin/',PrepupAdmin,name="PrepupAdmin"),
    path('open-file/<int:id>',OpenFIle,name="OpenFIle")


]


