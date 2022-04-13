from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('accounts/user-signup/', Usersignup, name="Usersignup"),
    path('accounts/recruiter-signup/', Recruitersignup, name="Recruitersignup"),
    path('accounts/signin/', signin, name="signin"),
    path('profile/', userprofile, name="userprofile"),
    path('edit-company/<int:id>/', editCompany, name="editCompany"),
    # path('recruiter-profile/', recruiterprofile, name="recruiterprofile"),
    path('activate/<uidb64>/<token>', activate, name="activate"),
    path('logout', logout, name="logout"),

]
