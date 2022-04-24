
from django.urls import path
from .views import *

urlpatterns = [
    path('', prepIndex, name='prepIndex'),
    path('interview-prep', interviewIndex, name='interviewIndex'),
    path('interview-prep/admin/', interviewIndexAdmin, name='interviewIndexAdmin'),
    path('admin/', PrepupAdmin, name="PrepupAdmin"),
    path('open-file/<int:id>', OpenFIle, name="OpenFIle"),
    path('prep-update/<int:id>/<str:status>', prepUpdate, name="prepUpdate"),
    path('prep-edit/<str:id>', prepEdit, name="prepEdit"),
    path('prep-edit/', prepEdit, name="prepEdit"),

    path('interview-prep-update/<int:id>/<str:status>',
         interviewPrepUpdate, name="interviewPrepUpdate"),
    path('interview-prep-edit/<str:id>',
         interviewPrepEdit, name="interviewPrepEdit"),
    path('interview-prep-edit/', interviewPrepEdit, name="interviewPrepEdit"),


]
