from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('accounts/user-signup/', Usersignup, name="Usersignup"),
    path('accounts/recruiter-signup/', Recruitersignup, name="Recruitersignup"),
    path('accounts/signin/', signin, name="signin"),
    path('profile/', userprofile, name="userprofile"),
    path('edit-company/<int:id>/', editCompany, name="editCompany"),
    path('add-company/', editCompany, name="addCompany"),
    # path('recruiter-profile/', recruiterprofile, name="recruiterprofile"),
    path('activate/<uidb64>/<token>', activate, name="activate"),
    path('logout', logout, name="logout"),
    path('edit-recruiter-profile/',
         editRecruiterProfile, name="editRecruiterProfile"),
    path('update-company', setCompany, name='setCompany'),
    path('edit-user-profile/', editUserProfile, name='editUserProfile'),
    path('add-exp', addExp, name='addExp'),
    path('add-exp/<int:id>', addExp, name='addExp'),
    path('add-edu', addEdu, name='addEdu'),
    path('add-edu/<int:id>', addEdu, name='addEdu'),
    path('add-certificate', addCert, name='addCert'),
    path('add-certificate/<int:id>', addCert, name='addCert'),


    path('profile/<user>', profile, name='profile'),
    path('resume/<user>', resumeViewer, name='resumeViewer'),


]
