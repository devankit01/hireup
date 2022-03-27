from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def Usersignup(request):
    return render(request, 'users/userSignup.html')

def Recruitersignup(request):
    return render(request, 'users/recruiterSignup.html')

def signin(request):
    return render(request, 'users/signin.html')


def userprofile(request):
    return render(request, 'users/userProfile.html')