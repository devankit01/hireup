from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('accounts/user-signup/', Usersignup, name="Usersignup"),
    path('accounts/recruiter-signup/', Recruitersignup, name="Recruitersignup"),
    path('accounts/signin/', signin, name="signin"),
    path('user-profile/', userprofile, name="userprofile"),

]
