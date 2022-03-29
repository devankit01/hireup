
from django.urls import path
from .views import *

urlpatterns = [
    path('', prepIndex, name='prepIndex'),
    path('interview-prep', interviewIndex, name='interviewIndex'),
    path('Notes-Admin/',NotesAdmin,name="NotesAdmin"),
    path('open-file/<int:id>',OpenFIle,name="OpenFIle")


]


